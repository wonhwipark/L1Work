# HANDOFF — whpark-mcp 코드분석 결과·소스 근거 읽기 도구 보완 + SDM E2E

- 버전: **v1.1** / 2026-10-24 KST
- 기반: `HANDOFF_L1_MCP_Freeform_Code_Analysis_Remote_v1_0.md`의 요구사항을 유지하되 **기존 분석 요청 기능 재사용 / 조회 기능 우선 보완**으로 수정
- 반영 신규 입력: **코드분석 요청 자체는 가능하지만, 사내 Agent가 MCP를 통해 분석 결과를 읽는 도구가 없다.**
- 추가 소스: `work-ledger-kernel_v0_7_27 (1).zip` 실제 ZIP 검토
- 구현 주체: 사내 Linux에서 **사내 LLM**. 사내 구현 프롬프트는 **3,000자 제한 없음**. 사외 메신저 응답만 짧게 유지.
- 현재 상태: 설계서. MCP 소스와 사내 도구 레지스트리 미열람, 배포·실환경 테스트 **NOT TESTED**.

## 0. 이번 변경의 결론: 요청 도구가 아니라 **읽기 도구**가 우선

사용자 관측을 기준으로 이미 가능한 경로:

```text
모바일 → 사내 Agent → 기존 코드분석 요청 경로 → code-analyzer 등 실제 사내 분석 처리
                                                  │
                                                  └── 분석 결과/근거 산출물
```

현재 부족한 경로:

```text
모바일 → 사내 Agent → whpark-mcp ──[결과·근거 READ tool 부재]──> 결과/Work/코드
```

따라서 **기존 분석 요청 도구를 재구현·대체하지 않는다.** 먼저 현재 Agent가 성공적으로 분석을 요청하는 정확한 도구/Skill/Runner 이름, 실제 응답의 작업 키, 결과 저장 위치·포맷만 사내에서 추적한다. 원격 진단 `SOURCE=2 REUSE=2 DEPLOY=2 NEXT=3`은 *그 시점에 노출된 조회·수정 인터페이스가 없었다*는 뜻으로 해석하며, 사용자가 확인한 **기존 분석 요청 가능** 사실과 혼동하지 않는다.

### ‘읽기’는 서로 다른 3가지

| 우선 | 읽기 대상 | 기대 질문 | 원칙 |
|---|---|---|---|
| P0 | **분석 상태/저장 결과** | “SOC-420517 분석 결과 알려줘”, “왜 DAC가 달라?” | 작업 결과 조회, 분석 재실행 0회 |
| P0 | **Work 이력/등록 Evidence** | “지난번 결론과 근거 보여줘” | `work-ledger-kernel` SSOT 조회; 추론·자동 수정 금지 |
| P1 | **근거가 된 소스 코드 구간** | “그 분기문 실제 코드 30줄 보여줘” | 승인 저장소·고정 revision·범위 제한. 파일 전체/임의 경로 열람 금지 |

구현 전 실제 장애가 단순 `MCP TOOL_NOT_EXPOSED`인지, 저장된 결과가 아예 없어 `RESULT_NOT_FOUND`인지 구별해야 한다. **분석 요청 성공 ≠ 분석 결과 파일 보존 ≠ MCP에서 결과 읽기 가능**.

## 1. 출처별 사실과 미확인

| 구성 | ZIP/보고 기준 확인 | 미확인 또는 주의 |
|---|---|---|
| `whpark-mcp` | 기존 Agent를 통한 **코드분석 요청 가능**: 사용자 최신 설명 | 소스 미제공. 요청의 실제 MCP tool/Skill 이름, 반환 ID, 읽기 도구 노출 목록, ACL·restart 경로는 사내 확인 |
| `code-analyzer` | 실사용 분석 스킬이라는 운영 배경 | 이번 첨부에 최신 패키지 없음. 실제 결과 파일 구조/위치·코드 근거 출력·호출 계약 미검증 |
| `work-ledger-kernel v0.7.27` | `work_ledger_kernel/cli.py`에 `work-find`, `work-list`, `work-refs`, `status`, `resume` 인터페이스 존재. `work_ledger_kernel/work_refs.py:WorkReferences.find/read`, `work_ledger_kernel/work_ux.py:brief_resume/diagnostic_resume`, `work_ledger_kernel/feature_design.py:read` 구현 | 이 CLI가 **MCP tool로 노출됐다는 의미 아님**. 실제 Work의 분석 Evidence가 등록됐는지, Agent에서 접근 가능한지 확인 필요 |
| Ledger 영속 저장 | `docs/WORK_LEDGER_CONTRACT_v1.md`: `record.json`, `evidence/`, `journal.jsonl`, `bindings.json`. `work_ledger_kernel/kernel.py`에서 evidence SHA 검증 로직 존재 | 증거의 *목록*과 증거 *본문*은 별도; 결과 산출물이 Ledger에 자동 등록된다고 단정 금지 |
| Ledger 보안·쓰기 | 동일 계약: **Kernel만 Ledger 변경 가능**. `TL_PRIVATE_LOCAL_ONLY`는 공유/원격 view에서 제외 | MCP read tool이 승인/문서 게시/Work 수정 권한을 얻는 것 아님 |
| Ledger 조회의 엄격성 | `feature_design.read()`에는 no-lock/no-new-state 의도가 명시됨 | `LedgerStorage.__init__()`는 `root.mkdir()` 호출. **존재하지 않는 루트에서 초기화하는 것조차 읽기 전용이 아님**. 사내 Adapter에서 검증 |
| `job-list v0.4.22` | 큐·Runner·상태/observer 존재. 단순 observer summary에는 길이 제한 | `job_core.py status`는 레이아웃/복구 동작을 동반할 수 있으므로 엄격한 MCP GET에 직접 연결하지 않음 |
| `issue-analyzer v0.11.48` | 기존 TXT 직접 분석 지원 | 이번 요구는 **코드분석 READ 우선**. SDM→TXT→issue-analyzer 실 E2E는 별도 후속 단계 |
| PLUS Parser | 과거 Agent에서 독립 `run_plus_sdm_to_txt` 등록 보고 | fixture·실 변환·실 분석 E2E는 **NOT TESTED** |

**경계:** `work-ledger-kernel`에는 일부 Work 메타/스냅샷 뷰만 있고, 개별 `code-analyzer`의 상세 분석 결과가 실제로 연계되어 있는지는 입증되지 않았다. 없다면 사내 승인된 결과 store/인덱스를 별도로 만들어 **읽기만** 제공하며, Work SSOT를 임의 조작하지 않는다.

## 2. 수정된 아키텍처

```text
[모바일 자연어]
   │ 코드분석 요청(기존 기능)    │ 분석 상태/근거/Work 조회(신규 P0 READ)
   ▼                          ▼
[사내 Agent]             [사내 Agent]
   │                          │
   ▼                          ▼
[기존 코드분석 도구]       [whpark-mcp Read Adapter]  ← 이번 핵심 구현
   │                          ├── analysis_find / list
   │                          ├── analysis_status_read
   │                          ├── analysis_result_read (section/cursor)
   │                          ├── analysis_evidence_read (등록 Evidence)
   │                          ├── work_summary_read (kernel 공식 read 경로)
   │                          └── code_excerpt_read (P1: pinned SCM snapshot)
   ▼                          │
[승인 Runner/code-analyzer]    │ 인증·ACL·허용 repo/work 검증
   │                          │
   ├── 작업/분석 상태 ───────────┤
   ├── 결과 보고서·근거 ──────────┤
   └── Ledger Work/Evidence(등록된 경우) ─┘

[후속질문] Agent가 기존 저장 결과+증거를 읽고 답변
  └─ 근거 부족 → NEEDS_NEW_ANALYSIS(새 분석은 명시적 별도 요청)

[SDM] 승인 fixture → 독립 PLUS Parser → TXT 검증 → issue-analyzer (별도 P2)
```

**새 분석 요청 / 새 분석 실행 / 조회는 분리**한다. READ API는 원칙적으로 순수 조회; 조회만으로 작업 재개·큐 enqueue·브랜치 전환·Work mutation·결과 파일 생성 금지. 세션이 달라도 analysis_id, work_id, evidence_id 기준으로 조회한다.

## 3. 우선 구현: MCP 조회 도구 계약 (제안 이름이며 **실등록 API 아님**)

사내 MCP 도구 네이밍 컨벤션과 등록 상태부터 조사. 기존 조회 도구가 동일 계약을 안전하게 제공하면 이름만 Mapping하고 새로 만들지 않는다.

### R1. `l1_analysis_find` — 자연어 작업 식별

입력: `{ "query":"SOC-420517", "kind":"code", "limit":10, "cursor":null }`

반환: 권한 있는 후보 `analysis_id`, `work_id`, `source=runner|ledger|job`, `submitted_at`, `state`, `short_title`, `next_cursor`.

- Jira 키 ↔ Work ID는 `work_find`/`work_refs`의 **실제 확인된 참조만** 매핑. 유사한 제목만으로 다른 Work를 연결하지 않는다.
- 결과가 여럿이면 목록 반환, 최신 결과 자동 지정은 사용자 의도가 명확할 때만.
- 기존 Runner 출력에 `analysis_id`가 없다면 **읽기 전용 레거시 인덱스**의 안정된 result reference를 설계. 이전 결과를 옮기거나 덮어쓰지 않는다.

### R2. `l1_analysis_status_read` — 상태만 읽기

입력: `{ "analysis_id":"verified-id" }`

반환: `state`, `stage`, `updated_at`, `reason_code`, `artifact_available`, `result_ref`, `source_type`.

- `status`와 `result`는 분리: 완료 상태라도 결과 본문이 없다면 `artifact_available=false`.
- Queue/Job의 기존 상태 파일을 읽을 때 잠금/복구/스케줄/정리/조회 기록 작성 같은 부작용이 없어야 함.
- 프로세스 exit=0만으로 **분석 성공**이나 원인 확정으로 표시 금지.

### R3. `l1_analysis_result_read` — 저장된 분석 보고서 읽기 (핵심)

입력:

```json
{
  "analysis_id": "verified-id",
  "section": "cause",
  "cursor": null,
  "max_chars": 2200
}
```

- `section`: `summary | symptoms | cause | callflow | variables | evidence | recommendation | next | all` (기존 산출물에 없는 섹션은 **NO_SECTION**, 모델 추정 생성 금지).
- 결과: `analysis_id`, `section`, `text`, `evidence_refs[]`, `source_revision`, `confidence`, `next_cursor`, `complete`, `source_kind`.
- 기본 모바일 응답은 짧게. 페이지 cursor 안정성 보장 (원본 콘텐츠 digest/버전 고정). `all`도 제한된 페이지로만.
- 저장 결과가 MD/HTML/JSON/TXT 등일 수 있으므로 **현재 실제 Runner 포맷 확인 후** 안전한 Reader/파서 결정. MD/HTML의 실행 코드·스크립트 렌더링 금지, 텍스트로 안전하게 제공.
- 조회 요청은 **code-analyzer 실행 0회**, Ledger 기록 0회, Git 쓰기 0회.

### R4. `l1_analysis_evidence_read` — Work/Evidence 근거 읽기

입력: `{ "work_id":"resolved-work", "evidence_id":"registered-id", "section":"summary", "cursor":null, "max_chars":1800 }`

- `work-ledger-kernel`의 공식 조회 인터페이스를 우선하고, `record.json > evidence_index`의 **등록된 경로·sha256·confidence_state·code_rev** 확인.
- 내용 제공 전 승인된 scope, regular file, ledger 내부 경로, SHA-256 일치 여부, 민감정보 정책 검증. 불일치→`EVIDENCE_STALE`.
- confidence(`AUTO_CANDIDATE`, `HUMAN_CONFIRMED` 등)는 그대로 명시; 원인 확정이나 승인 상태로 둔갑 금지.
- evidence가 없다면 `EVIDENCE_NOT_LINKED` 반환. Work title/상태만 보고 가상의 원인 분석 작성 금지.
- `TL_PRIVATE_LOCAL_ONLY`, 외부 게시 금지 객체, 타 사용자 범위, 비승인 원문은 직접 반환 불가. 기존 Ledger writer 정책 변경 금지.

### R5. `l1_work_summary_read` — Work 기준 한 번에 요약

입력: `{ "work_ref":"SOC-420517", "view":"brief" }`

- `work-find` → 정확한 Work 선택 → `brief_resume` 등 **읽기 전용 View**를 허용된 스코프에서 활용.
- 반환: `work_id`, `title`, `status`, `current_state`, `last_decisions[]`, `next_actions[]`, `analysis_refs[]`, `freshness`.
- `analysis_refs`는 실제 Analyzer→Work 연결 근거가 있을 때만 제공. 없으면 `UNLINKED`, 아직 분석 진행 중으로 추정하지 않는다.
- 레거시 `TL_REVIEW`/private-only 자료는 공용 메신저 요약에 섞지 않는다.

### R6. `l1_code_excerpt_read` — 소스 구간 읽기 (P1, 강한 권한 통제)

입력:

```json
{
  "repo_alias": "smp1900",
  "revision": "verified-commit-sha",
  "relative_path": "verified/repo/relative/path.cpp",
  "line_start": 110,
  "line_count": 30,
  "analysis_id": "verified-id"
}
```

- **분석 근거로 연결된 소스만** 기본 허용. 별도 코드 열람 권한이 있더라도 승인된 `repo_alias`/SCM snapshot/relative path로 한정.
- Git: 가능하면 pinned `commit_sha:path` 내용을 작업 트리 변경 없이 읽기. `git checkout/switch/worktree` 불가. 수정된 working copy를 그대로 신뢰하지 않고 snapshot과 구분.
- P4: 실제 승인된 depot/client/changelist 계약 확인 후 pinned revision만 조회. 임의 depot 경로·P4 명령 실행 도구 노출 금지.
- symlink/traversal(`..`), 절대 경로, 숨김 secret/key/token 파일, `.git`, 리포 외부 파일 차단. 예: 최대 40줄/호출, 2,000자/페이지(실제 정책에서 더 좁힐 수 있음).
- 요청한 줄 범위가 코드 근거와 불일치하면 `REVISION_MISMATCH` 또는 `EVIDENCE_RANGE_INVALID`.
- 사내 정보 보호 정책이 소스 본문 송신을 금지하면 **파일 별칭·함수·라인·해시만** 반환하고 코드 발췌는 `NOT_AUTHORIZED`.

### R7. 자연어 후속 질문 처리 (우선 **Agent 라우팅**, 별도 MCP tool 신설은 조건부)

- 사용자: “왜 값이 다른지 다시 설명해줘” → Agent가 R3/R4/R6 저장 근거를 읽고 요약. **자동 재분석 금지**.
- 저장 근거로 답할 수 없으면 `NEEDS_NEW_ANALYSIS` + 필요한 분석 범위 안내.
- “새로 분석해줘” 명시 시 기존 **코드분석 요청 도구**를 다시 사용. 생성된 ID가 있으면 `parent_analysis_id` 연결(해당 도구 계약이 지원할 경우); 미지원이면 내부 읽기 인덱스로 관계만 기록할지 검토하되 Ledger 무단 기록 금지.
- 별도 `followup` MCP 기능은 Agent의 일반 자연어 기능만으로 위 동작을 제공하지 못할 때에만 추가.

## 4. 결과 연결 및 저장 전략 — `work-ledger-kernel` 기반

### 조회 우선순위

1. **기존 분석 요청 경로가 반환한** `analysis_id` / job receipt / 직접 연결된 result ref.
2. **실제 code-analyzer가 작성한** 분석 artifact와 실행 metadata. 읽기 허가 및 안전 검증 필요.
3. Work에 정식 등록된 `evidence_index` / immutable Evidence (SHA 확인).
4. job-list observer는 상태·요약에만 사용 (자세한 원인 근거 대체 금지).
5. GitHub `l1-workspace` publish 문서는 승인되어 실제 Push/readback이 확인된 경우에만 보조 조회(로컬 최신 원장으로 가정 금지).

### 절대 금지

- MCP read tool이 `record.json`, `journal.jsonl`, `bindings.json`을 직접 변경.
- Work 갱신을 위해 status/read API에서 `context`, `note`, `record`, `docs-export`, `migration`, `sync`, `push`를 자동 호출.
- 다른 PC의 Work 데이터가 아직 동기화되지 않았는데 최신이라고 표시.
- 기존 Evidence가 없는 경우 Runner 요약을 “HUMAN_CONFIRMED RCA”로 생성.
- 과거 `l1-workspace-artifacts-migrate-linux` Job 이력 삭제·재실행·자동 정리.

### 조회 전용 설계상의 구현 주의

`LedgerStorage`의 constructor는 루트를 만드는 코드가 있으므로, 읽기 전용 요청 시 먼저 **루트 존재/권한을 비변경 방식으로 확인**한다. 실제 Kernel·View 초기화 중 파일/디렉터리 작성이 없는지 테스트해야 한다. `job-list status` 역시 복구 부작용이 있을 수 있으므로 전용 read-only store/reader로 결과를 읽거나 안전한 공식 조회 API가 있으면 그것을 이용한다.

### 내부 최소 인덱스 (필요할 때만)

```json
{
  "schema":"l1-analysis-index/1",
  "analysis_id":"actual-id-or-stable-legacy-ref",
  "work_id":"resolved-work-if-proven",
  "owner_scope":"authenticated-principal",
  "runner_kind":"actual-analyzer-name",
  "artifact_ref":"approved-private-result-id",
  "state_ref":"approved-private-state-id",
  "scm_revision":"verified-sha-or-cl",
  "result_digest":"sha256-of-verified-artifact"
}
```

인덱스 생성/마이그레이션은 **별도 승인된 운영 작업**이다. 조회 함수는 기존 인덱스/파일만 열어야 한다. 권한 없는 분석자에게 경로·본문/메타정보를 반환하지 않는다.

## 5. 에러·상태 구분

| 상태 | 정확한 의미 | 조회 시 동작 |
|---|---|---|
| `READ_TOOL_NOT_EXPOSED` | 분석 요청은 가능하지만 조회 MCP 도구가 Agent에 노출 안 됨 | MCP 등록·배포 우선 |
| `READ_TOOL_NOT_AUTHORIZED` | 존재하나 인증/스코프 거부 | 승인 경로 확인; 우회 없음 |
| `ANALYSIS_ID_UNKNOWN` | 요청에 맞는 결과 ID를 찾지 못함 | R1 후보 조회 |
| `RESULT_NOT_FOUND` | 분석 작업은 존재하나 결과 artifact 확인 안 됨 | 재실행 금지, 저장 경로 진단 |
| `RESULT_NOT_READY` | 실행 중이어서 결과 미완성 | 상태만 표시 |
| `EVIDENCE_NOT_LINKED` | Work 또는 분석 결과에 정식 Evidence 링크 없음 | 결론 확정 금지 |
| `EVIDENCE_STALE` | 저장된 Evidence hash 불일치 | 원문 차단 |
| `NO_SECTION` | 요청한 결과 섹션 자체가 없음 | 다른 섹션만 안내 |
| `REVISION_MISMATCH` | 현재 소스/근거가 동일 revision 아님 | pinned revision 재확인 |
| `NEEDS_NEW_ANALYSIS` | 현재 저장 근거만으로 답변 불가 | 명시 요청 전 재분석 금지 |
| `RUNNER_UNKNOWN` | 기존 요청 실행 경로의 사내 계약이 미확인 | 원인 추정 금지 |

코드는 설계 식별자이며 기존 프로토콜 enum에 우선 매핑. `NOT_FOUND`와 `NOT_AUTHORIZED` 등 응답은 외부에서 타 사용자 결과 존재 여부를 누설하지 않도록 권한 정책에 따라 노출 수준 조정.

## 6. 사내 구현 순서 (원샷, **조회 기능 우선**)

**G0 — 무변경 실사**

1. Agent에서 성공하는 실제 코드분석 요청 호출을 **한 건만** 관찰 (기존 저장 이력 우선), 반환 ID/결과 저장 포맷 식별. 분석기 재실행 금지.
2. MCP tool registry 및 auth/allowlist 확인. 조회 기능이 없다는 사실을 도구 목록으로 확인.
3. `code-analyzer`의 결과 계약/보존 위치/작업 상태 식별. 현재 결과의 조회 가능성 확인.
4. `work-ledger-kernel v0.7.27` `work-find/work-refs/brief_resume/evidence_index`를 검토하여 Work 링크가 실제 생성되는지 확인.
5. `job-list` 결과/observer와 Analyzer artifact 연계를 확인. 기존 조회 API 재사용 가능 여부 판단.
6. 읽기 전용 기능에 필요한 별도 principal/ACL/민감정보 노출 정책 확인.

**G1 — 최소 구현**

- 요청 submit은 원칙적으로 **무변경**.
- R1~R4+R5 중 기존 인터페이스에 없는 것만 추가, R6은 코드 원문 접근 승인이 있을 경우 P1로 분리.
- 가능하면 `ReadAdapter`를 공통 구현해 JSON/MD/텍스트 산출물을 안정적으로 섹션화. 실제 포맷에 없던 원인·숫자 값을 LLM이 만들어 반환하지 못하도록 형식·근거 필드를 명확히 한다.
- MCP tool 등록, 명세 공개, ACL, 서비스 반영을 별도 검증.

**G2 — 결과 연결과 UX**

- `SOC-420517 분석 결과 알려줘` → 실제 결과 ID 자동 후보화 → 결과 요약+증거 ID 반환.
- `main_dac_path 설정 조건만` → `cause/variables` 섹션.
- `해당 함수 30줄` → R6 권한·revision 검사 후 조회.
- 각 질의가 **전부 조회**인지 새 분석이 필요한지 명시; GET에서 Runner 호출 0회.

**G3 — SDM 별도 트랙**

- 승인 fixture ID 조회→기존 PLUS 독립 Parser→유효 TXT→issue-analyzer의 TXT 분석 경로 검증.
- 실제 fixture 없는 동안 SDM E2E는 **NOT TESTED**, mock 테스트와 구분.

## 7. 상세 검증 매트릭스

| Test | 상황 | PASS 기준 |
|---|---|---|
| RD01 | 기존 분석 요청 회귀 | 변경 전후 같은 요청 경로, 결과 ID·기존 정책 정상 |
| RD02 | 도구 등록 | Agent에서 신규 READ 도구 발견, 스키마·권한 검증 |
| RD03 | Work/analysis ID 해석 | SOC↔Work↔실제 분석 ID 정확 매칭; 모호성 방어 |
| RD04 | 상태만 조회 | GET 100회 중 enqueue/Runner/파일생성/복구/원장수정 **0회** |
| RD05 | 결과 조회 | 실제 분석 artifact의 summary/cause를 chunk와 cursor로 읽기 |
| RD06 | 상세 Evidence 조회 | 등록 evidence ID/파일/해시 일치, confidence 유지 |
| RD07 | Code excerpt 조회 | pinned revision/파일/라인 일치, 허가되지 않은 소스 비노출 |
| RD08 | 재분석 억제 | 후속 자연어 확인만으로 Runner 호출 **0회** |
| RD09 | 근거 부재 | RESULT_NOT_FOUND, EVIDENCE_NOT_LINKED 등을 명확히 출력; 추정 답변 금지 |
| RD10 | 접근 통제 | cross-user/무권한/우회경로/secret/상위 디렉터리 공격 차단 |
| RD11 | 보존성 | Ledger 기존 파일 해시, job-list 큐/기존 이력, Git status 불변 |
| RD12 | 서비스 재시작 | 승인 후 등록·reload/restart 시 MCP 도구 가시성 확인, rollback |
| RD13 | Windows/Linux | 실제 실행한 OS만 PASS; 미실행 OS는 NOT TESTED |
| SD01~03 | SDM fixture/변환/분석 | 승인 실SDM으로 별도 E2E 검증, mock과 혼동 금지 |

## 8. 사용자 사용 예시 (배포·검증 후)

- **기존 요청**: “SOC-420517의 `main_dac_path`와 `tx_dac_path`가 다른 조건을 코드분석해줘.”
- **결과 조회**: “SOC-420517 최신 코드분석 결과 원인만 보여줘.”
- **근거 조회**: “원인을 판단한 함수/파일/라인 근거를 알려줘.”
- **소스 읽기**: “그 분기문 코드 30줄을 분석 당시 commit 기준으로 보여줘.”
- **후속 질문**: “그때 `allocated DAC bitmap`이 바뀐 순서만 설명해줘. 새 분석 말고 저장된 결과를 읽어줘.”
- **Work 확인**: “SOC-420517 Work의 마지막 결정과 분석 Evidence를 보여줘.”
- **재분석 명시**: “근거가 부족하면 추가로 읽기 전용 분석을 새로 요청해줘.”

## 9. 구현 범위와 전달 파일

- **필수 후보**: `whpark-mcp`의 **READ tool 등록/ACL/ReadAdapter/페이지 처리/테스트**.
- **변경 필요성 판단 후**: 기존 `code-analyzer`의 artifact output 계약, `job-list` 결과 조회, `work-ledger-kernel`의 기존 안전한 공식 reader 재사용. 무조건 패키지 변경 금지.
- **기본 유지**: 기존 코드분석 요청 도구, `l1-fix-workflow`, `skill-updater`, GitHub Push 경로, `work-ledger-kernel` writer/SSOT, 기존 Job.
- 배포 전 승인된 백업/롤백, 실제 적용 버전·런타임 도구 목록·read-only E2E 확인.

사내 개발의 단계별 구현 지시: `PROMPT_INHOUSE_L1_MCP_Code_Analysis_v1_1.md` (사내 LLM 3,000자 제한 없음).

## 10. 최종 보고 형식 (사내 증거 보고는 길이 제한 없음)

```text
REQUEST_EXISTING=1 confirmed / 2 broken / 3 unknown
READ_TOOL=1 registered / 2 missing / 3 unverified
RESULT_READ=1 real-pass / 2 fail / 3 not-tested
EVIDENCE_READ=1 real-pass / 2 fail / 3 not-tested
CODE_EXCERPT=1 real-pass / 2 denied / 3 not-tested
WORK_LINK=1 evidence-linked / 2 unlinked / 3 unknown
READ_ONLY=1 verified / 2 violated / 3 unverified
SDM_E2E=1 real-pass / 2 fail / 3 not-tested
BLOCKER=NONE|...
NEXT=...
```

사내 개발 보고서에는 실제 수정 파일/테스트·에러 증거/롤백 정보를 충분히 기술하고, 메신저로만 전송되는 **원격 요약**은 `READ_TOOL, RESULT_READ, WORK_LINK, BLOCKER, NEXT` 정도로 간결하게 표시한다.
