# 사내 MCP 동적 기능 게이트웨이 + 스킬 장애 자동복구 통합 설계·구현 원샷

- 문서 버전: **v1.0 / 2026-10-31**
- 대상: `whpark-mcp`(사내 Agent MCP), `job-list`, `code-analyzer`, `issue-analyzer`, 필요 시 `skill-updater`
- 목적: 사외 Agent에서 **기능 탐색 → 실행 가능성 진단 → 승인된 작업 요청 → 실제 결과 조회 → 장애 원인 식별 → 안전한 자동복구 → 재검증**을 하나의 공통 경로로 제공한다.
- 결정: 사용자 요청에 따라 *자동복구를 포함*한다. 단, **자동복구 권한은 사전 승인된 한정된 조치와 격리된 수정안 생성·테스트**까지를 기본으로 하며, 운영 소스 변경·배포·MCP 재시작·권한 상승·새 소스 매핑 추정은 자동 승인하지 않는다.
- 상태: **설계 및 사내 LLM 작업지시서. 사내 구현·실환경 동작·배포 성공을 의미하지 않는다.**

## 0. 근거·현재 기준·충돌 예방

1. 기존 Dropbox 맥락: ACTIVE `START_HERE_r0022` → `CURRENT_r0047` → `WORK_r0046` → `R045_dynamic_gateway_proposal_20261031`. 기존 정책 `OPERATING_RULES_r0012`, `JOB_LIST_ONESHOT_OPERATING_CONTRACT_r0002`의 안전·증거·단계적 배포 원칙을 계승한다. 이번 문서는 R045의 **동적 Gateway 제안**에 **자동 장애복구**를 합친 후속 설계다.
2. 보고된 사내 실행 기준은 `job-list v0.4.26`, `skill-updater v0.5.44`다. 첨부로 직접 열어본 ZIP은 **`job-list v0.4.25`**와 **`skill-updater v0.5.44`**이며, 첨부 v0.4.25는 과거 설계 참고 자료일 뿐 설치된 v0.4.26의 동일 코드라는 보장은 없다. 사내에서 *실제 설치본과 live MCP 소스, 해시, 실행 경로*를 먼저 식별하고 이를 정본으로 삼는다. 버전 불일치가 있으면 자동 덮어쓰지 않는다.
3. v0.4.25의 `scripts/mcp_job_read_bridge.py`는 제한된 Job ID의 **로컬 읽기 CLI**를 제공하지만 원격 MCP 도구를 자동 등록하지 않는다. `scripts/mcp_job_read_stage_linux_job.py`의 Stage는 운영 적용이 아니다. 과거 문서에는 `BLOCKED`에서도 프로세스 종료 코드가 0일 수 있는 사례가 있어 **Receipt 성공 ≠ 의미적 성공** 계약을 별도로 유지해야 한다.
4. 기존 SDM 조회 장애: `JOB-20261031-MCP-SDM-PARSER-READ-STAGE-01`은 보고상 queue `DONE`/receipt `SUCCESS`지만 Agent MCP `job_result_read`에서 `RESULT_UNSUPPORTED`, 실제 semantic result `UNKNOWN`. **기존 Job 재실행/재등록 없이 읽기 복구부터** 수행한다. 로컬 결과의 실체와 MCP backend가 미확인일 때 원인을 확정하지 않는다.
5. 목표는 향후 `code-analyzer`, `issue-analyzer`, `l1-fix-workflow` 등 **기존 및 신규 스킬에 공통 적용**하는 것. 코드·민감 경로·원문 로그·패치 본문·토큰은 사내에서만 보관하며 Dropbox `/AI-CONTINUITY/`는 비민감 맥락 관리 전용이다.

## 1. 사용자 관점 완료 조건

| 사용자 요청 | 기대되는 Agent 동작 | 성공 증거 |
| --- | --- | --- |
| "현재 사용 가능한 분석 기능 확인해줘" | 승인된 Registry에서 기능·버전·입력 요구조건·권한·상태 조회 | 지원 기능만, 실제 installed/available 구분 |
| "code-analyzer로 함수 분석해줘" | 분석 기능 탐색, 입력·소스·엔진 preflight, 기존 승인 profile 실행, 결과 조회 | 분석 run ID / source revision / semantic result / evidence 수준 |
| "분석이 안 되는데 원인 확인해줘" | 오류 발생 지점을 MCP·실행기·설정·스킬·산출물 계층으로 구분 | 진단 코드 + 근거 출처 + 차단 지점 |
| "원인 확인하고 자동복구해줘" | 자동복구 policy의 안전 조치만 실행하고 같은 요청으로 독립 재검증 | 적용된 remediation ID / 재검증 PASS·FAIL / 잔여 blocker |
| "새로운 스킬/Job도 Agent에서 써줘" | 관리자가 등록·승인한 manifest 기반으로 기능 발견, 고정 MCP API 재사용 | 등록 검증·권한·profile/version 호환 PASS; MCP 코드의 Job별 hardcoding 제거 |
| "운영 적용됐어?" | Stage/시험/승인/운영 적용/E2E 별도 조회 | 실제 승인 및 운영 E2E 증거 없이 적용 완료 표시 금지 |

**금지할 가짜 성공**: Queue DONE, Worker Receipt SUCCESS, updater install PASS, Stage patch 생성, 도구 목록 등재는 그 자체로 사용자 작업 완료가 아니다.

## 2. 목표 아키텍처와 책임

```text
외부 사용자 / ChatGPT Agent (의도·질문, 승인된 도구만 사용)
                 │  안정된 소수의 MCP tool
                 ▼
        whpark-mcp Capability Gateway
        ├─ authn/authz + 인자 schema 검증 + audit
        ├─ capability list / contract negotiate
        ├─ diagnostics/read status/result
        ├─ recovery controller (정책·횟수·동일성 검사)
        └─ 승인된 Job manifest 검증 / registry adapter
                 │  ID·profile·version·role 고정 매핑
                 ▼
        Job-list / Skill execution controller
        ├─ Preflight (source mapping/설치/권한/runner/용량/의존성)
        ├─ approved job launcher (no remote shell)
        ├─ immutable result & status evidence reader
        └─ isolated repair/test profile runner
                 │
                 ▼
        사내 code-analyzer / issue-analyzer / OpenCode / repo
        └─ 로컬 원본 코드·패치·민감 로그 보관(외부 유출 금지)
```

- **MCP**: 호출·검증·인증·상태 전달·정책 집행. 원본 소스 수정기가 아님.
- **Job-list**: 허용된 작업 manifest, 큐·실행·receipt·semantic result 연결 및 preflight.
- **분석기**: 실제 분석 실행 및 정상 입력/오류/출력 schema 준수.
- **Recovery controller**: 오류 코드에 맞춘 *승인된 복구 playbook* 실행, 원복 가능성·재검증·재시도 제한 관리.
- **Skill-Updater**: 설치 버전 확인 및 기존 업데이트 기능 유지. MCP 동적 기능 추가 때마다 자동 업데이트나 새 배포를 강제하지 않는다.
- **승인 주체**: 관리자/사내 배포 규칙이 프로덕션 변경과 고위험 복구의 최종 결정권을 가진다.

## 3. MCP 고정 인터페이스(제안)

실제 Tool 이름·handler 방식은 **live whpark-mcp 소스 확인 뒤** 기존 사용 도구와 충돌하지 않게 확정한다. 신규 도구 수를 최소화하고 기존 READ와 호환 adapter를 우선한다.

| 후보 API | 입력(화이트리스트·typed) | 정규화 응답 |
| --- | --- | --- |
| `capability_list` | `category?`, `limit`, `cursor?` | 기능 ID/설치 버전/권한/실행 가능/manifest revision |
| `capability_preflight` | `capability_id`, `profile_id`, 승인된 `request_ref` | PASS/BLOCKED, reason codes, 의존성 및 결과조회 준비 |
| `capability_submit` | `capability_id`, `profile_id`, 제한된 validated params 또는 사내 저장 request_ref, idempotency key | Job/run id, enqueue state; preflight fail 시 미등록 |
| `capability_status` | 승인된 `job_id` 또는 `run_id`(타입 구분) | queue/receipt/semantic/deployment/MCP E2E 독립 상태 |
| `capability_result` | 승인된 ID, pagination/byte cap | 최소화된 결과 schema, 요약·reason codes·evidence ref |
| `capability_diagnose` | 승인된 `request_id`/Job ID/analysis run ID | failure_stage, probable_cause, confidence, safe recovery options |
| `capability_recover` | `incident_id`, `approved_playbook_id`, idempotency key, optional approved change ref | 조치 전후 state, allowed scope, outcome, revalidation, rollback ref |

고정 MCP 메서드 자체가 backend의 임의 명령·프롬프트 실행기로 변하면 안 된다. `job_id`는 승인된 레지스트리에서 처리하되 사용자 제공 arbitrary path, repo root, command, shell, env, URL, raw patch 내용을 실행 파라미터로 받지 않는다. 입력이 필요하면 사내 저장된 승인된 요청 객체/제한된 타입 필드로 전달한다. JSON schema 엄격 검증, 인가 검사, byte cap, rate limit, deadline, replay/idempotency를 적용한다. Agent가 목록을 볼 수 있는 권한과 소스 수정·배포 권한은 분리한다.

## 4. Job/Skill Registry 정합성

각 승인된 capability는 다음 최소 필드를 가진다: `capability_id`, `version`, `manifest_revision`, `job_type`, `profile_id`, `backend_id`, `backend_contract_version`, `job_id_pattern_or_resolved_id`(임의 와일드카드 읽기 권한 아님), `input_schema`, `result_schema`, `required_roles`, `approved_source_roots_ref`(사내 서버 내부 설정), `preflight_profile`, `diagnostic_profile`, `recovery_playbook_refs`, `timeouts`, `resource_limits`, `enabled`, `approval_record`, `content_digest`, `expires_at`(필요한 경우).

- **설치 감지 ≠ 자동 권한 부여**: Manifest는 관리자 승인 및 무결성 검증 후에만 활성. 미승인 신규 Job은 `DISCOVERED_UNAPPROVED`로 표시하고 실행 불가.
- 새 Job 추가 시 MCP 소스의 고정 Job ID 목록을 매번 고치지 않도록 **정규화된 registry adapter** 사용. backend가 해당 Job의 결과 위치를 승인된 profile로 결정하고, 외부는 원문 경로를 전달할 수 없다.
- Job ID와 Run ID를 혼동하거나 변환하지 않는다. 동일 요청 중복 등록 방지(idempotency), schema mismatch/manifest rollback/version drift 시 fail-closed.
- `RESULT_NOT_FOUND`(실행 전 정상일 수 있음)와 `RESULT_UNSUPPORTED`(지원 계약 누락)를 엄격히 구분. 신규 작업은 지원·인가·결과 조회 경로가 확보되어야 활성화 가능.

## 5. 자동복구 정책: 진단부터 재검증까지

**실행 플로우**: `DISCOVER → PREFLIGHT → SUBMIT → OBSERVE → DIAGNOSE → SELECT_PLAYBOOK → REPAIR → REVALIDATE → REPORT`.

1. **자동복구 허용(AUTO_SAFE)**: 상태 조회 재시도(읽기 전용·일시 오류·백오프), 사내 승인된 정해진 캐시/임시 상태 재동기화(보존성 검증), 프로세스가 안전하게 재시작 가능한 *비운영 격리 워커*의 1회 재시도, 이미 등록된 승인된 executable 경로/manifest reload(무중단·보존 가능한 경우) 등. 실제 playbook 세부 조건은 사내 담당자가 증명하고 활성화해야 한다. 임의 `kill`·`rm`·permission change는 포함하지 않는다.
2. **격리된 수정안 자동 생성(STAGE_ONLY)**: `code-analyzer`/`issue-analyzer`의 재현 가능한 입력 계약 위반, 내부 호출 연결 오류 등은 원본과 분리된 사내 sandbox/worktree **격리 작업공간**에 수정안 작성 → 정적검사 → 관련 단위·통합 테스트 → diff/sha + rollback 후보 생성까지 자동화 가능. 이는 운영 소스 적용이 아님. 실제 격리는 OS·FS 권한으로 강제하며 OpenCode prompt만으로 sandbox라 부르지 않는다.
3. **승인 필요(APPROVAL_REQUIRED)**: 프로덕션 소스 수정, 라이브 MCP 등록/재시작, 서비스 설정 변경, 접근권한 확대, 설치·업데이트, 실 사용자 데이터 변경, Git commit/push/PR merge, Job 재실행으로 부작용 가능성이 있는 작업. 승인 이전에는 Stage 결과와 적용 계획만 제공한다. 사내 기존 정책상 더 엄격한 승인 경계가 있으면 그 규칙 우선.
4. **자동복구 금지(BLOCKED)**: 소스 설정 누락 시 임의 경로 탐색·추정, 승인되지 않은 capability 실행, 원본 데이터 덮어쓰기/삭제, 보안 정책 우회, 임의 셸과 원격 명령, 기존 Job 무단 재등록/재실행, 반복 무한 재시도, 외부로 소스·원문 로그 유출.
5. 모든 playbook은 `id/버전`, `allowed_error_codes`, `preconditions`, `scope`, `max_attempts`(기본 1), `timeout`, `reversible`, `undo_plan`, `verify_probe`, `required_approval`, `audit_fields` 명시. 사전조건 미충족 시 복구 실행 금지. 동일 incident에 무한 순환 금지.
6. **검증**은 장애를 발생시킨 원래 요청의 동일 스킬/입력 계약/승인된 source revision(또는 명시된 변경 revision)으로 실행한다. 원본 실패 사례와 정상 사례 및 권한 거부 반례 모두 점검. 재검증 실패 시 안전하게 rollback 또는 `BLOCKED/REVIEW_REQUIRED`로 종료. 기존 성공 결과·queue·원본 증거 보존.

### 자동복구 사례·경계

| 감지 증상 | 원인 판정 | 가능한 자동 조치 | 수동 승인으로 전환 |
| --- | --- | --- | --- |
| 분석기 목록 없음 | 레지스트리/설치/권한 mismatch 구분 | read-only 재검색·정합성 진단 | 스킬 설치 또는 Registry 권한 부여 |
| `LOCAL_SOURCE_CONFIG_MISSING` | 승인된 source map 미설정 | 원인·필요 설정 키 안내, Job 등록 차단 | 실제 source root 등록/변경 |
| MCP `RESULT_UNSUPPORTED` | live MCP adapter / backend contract mismatch | 로컬 결과 읽기(사내 인증 컨트롤), 버전·허용 목록 비교, **Stage 패치 생성·시험** | 운영 MCP 변경 및 재시작 |
| `RESULT_NOT_FOUND` | 아직 실행 전/아직 결과 생성 전/이상 소실 분리 | 제한된 재조회, 상태·시각 상관관계 검사 | 임의 재실행·데이터 복구 |
| OpenCode executable 미발견 | 설치/경로 불일치 | 승인된 바이너리 후보의 **읽기 검사** 후 복구안 생성 | 새 설치·경로 등록 |
| 분석기 실행 예외 | 입력/schema/종속 코드 오류 | 격리 재현·패치·단위테스트 | 운영 소스 반영 |
| 일시적 read timeout | 제한된 transient 실패 | 지수 백오프, 기본 1회 재시도 | 지속 반복 오류 또는 서비스 리스타트 |
| semantic `BLOCKED` + receipt `SUCCESS` | 상태 해석 불일치 | envelope/semantic 구분 보고, 계약 수정안 테스트 | 운영 실행기 변경 |
| 운영 인증·권한 거부 | 정책상 허용되지 않은 접근 | 조치 없음, 안전한 오류/담당자 보고 | 사용자·관리자 승인 및 정책 개정 |

## 6. 상태·증거 계약(최소)

모든 결과는 외부 노출 전 sanitize: `schema_version`, `capability_id`, `job_id?`, `analysis_run_id?`, `source_revision?`, `stage`, `queue_state`, `receipt_state`, `semantic_state` (`SUCCESS|FAILED|BLOCKED|REVIEW_PENDING|NOT_RUN|UNKNOWN`), `deployment_state`, `agent_e2e_state`, `failure_stage`, `reason_codes[]`, `diagnostic_confidence`, `repair_playbook_id?`, `repair_status` (`NOT_ATTEMPTED|STAGED|APPLIED_SAFE|BLOCKED|ROLLED_BACK|FAILED`), `revalidation_status`, `evidence_level`, `evidence_ref`(비민감, 인가된 참조), `next_action`, `observed_at`.

- 성공 정의: **요청한 분석 산출물의 semantic SUCCESS 및 동일성·근거 검사 PASS**. 운영 MCP 기능 개선 요청이면 **승인된 운영 적용 + 실제 Agent E2E**도 별도로 PASS여야 완료.
- 결과가 미확인인 경우 UNKNOWN, 시험만 완료했다면 TEST_PASS_NOT_DEPLOYED. 진단 confidence가 LOW이면 자동 복구보다 단계 제한·추가 증거를 우선.
- 원본 stderr/stdout, source path, patch, token, PII, 자격증명은 MCP 출력 금지. 외부 에이전트는 요약 코드 및 비민감 참조만 받는다.

## 7. 사내 단계별 구현 지시(S0~S6)

### S0 — 기존 SDM Job 안전 복구(필수 선행)
- live MCP tool registry/handler/authorization, 설치된 job-list v0.4.26 read bridge/CLI 및 대상 Job의 로컬 결과를 **조회만** 한다.
- 로컬 `job-result-read` 결과가 OK이면 Agent MCP가 `RESULT_UNSUPPORTED`를 내는 정확한 계층을 특정. 신규 Job ID 하나만 인식하도록 하되 장기적으로 registry adapter로 연결하도록 설계한다.
- 로컬 결과가 `BLOCKED/NOT_FOUND/UNREADABLE`이면 그대로 보존하여 원인을 분리. queue/receipt를 다시 실행하지 않는다.
- 기존 세 Job 조회, invalid ID, 잘못된 결과 producer/schema, symlink/path escape, 민감정보 노출 방지 반례를 보존한다.

### S1 — Baseline·실제 계약 조사
- 실제 설치 버전 및 runtime path, MCP tool schema, 보안 모델, 실행 profile, job-list core, skill-updater scheduled boundary를 소스 근거로 조사한다.
- `code-analyzer`, `issue-analyzer`, workflow analyzer 호출을 포함한 연결 그래프와 지원 작업 목록을 조사. 확인 불가 기능은 `UNKNOWN`.
- 기존 작업과 충돌/호환 이슈 목록과 변경 최소 표를 작성. 새 job 자동 생성 금지.

### S2 — Dynamic Registry와 공통 READ
- 관리자 검증·승인된 capability manifest를 load/validate하고 기존 고정 읽기 도구를 호환 adapter로 잇는다.
- 목록·사전 점검·상태·결과·진단 API를 제공하고 RBAC/입력 검증·pagination·관찰 시각을 보장한다.
- Registry 새 승인 항목 추가 시 MCP 소스 변경 없이 발견/조회 가능한 통합 시험을 구축한다. 권한 없는 항목은 실행 불가.

### S3 — Preflight와 실행·결과 구분
- 큐 등록 **전** Job ID/profile/결과 reader 지원, approved source mapping, executable, OS/권한/공간, 입력 schema, 설치 버전과 backend contract 검사. 실패 시 미등록 및 명확한 blocker.
- Receipt 종료 코드와 semantic status, operation deployment, Agent E2E를 서로 독립 관리. 이미 실행 중인 Job/queue 중복·파손 감지 시 불변 보존.
- 기존 Updater 자동 주기는 변경하지 않고, 변경 필요 시 별도 이유·영향 분석·승인을 거친다.

### S4 — Skill 공통 진단 + 자동복구
- 실패 코드별 playbook을 **처음에는 read-only 및 STAGE_ONLY**로 구현하고 `code-analyzer`·`issue-analyzer` 샘플 장애(설치/호출/source/runner/결과)를 커버한다.
- 안전한 자동조치는 개별 playbook별 권한을 켜기 전 테스트·롤백 증거를 요구. 새 playbook이 있다고 자동 실행 허용하지 않는다.
- 근거 수집 → 원인 분류 → 복구 후보 선택 → allowed gate → 작업 → 동일 요청 재검증 → 결과보고가 동일 incident ID에 연결되어야 한다.

### S5 — 자동 회귀 / 보안 / 장애 주입
- 정상: 기존 3 Job 조회, 신규 승인 Job 조회, 두 analyzer의 정상 분석(모의 fixture), receipt/semantic 분리, preflight PASS, 안전복구 후 PASS.
- 차단: 신규 미승인 Job, 잘못된 job_id/run_id 혼동, path traversal, symlink, arbitrary shell/prompt/env, 결과 파일 오염, 잘못된 producer, 소스 매핑 누락, schema/version drift, permissions, 타임아웃, 중복 실행/재시도 폭주, 운영 적용 미승인, 민감정보 유출 시도.
- 복구: 동일 playbook 2회 요청 시 idempotent, 첫 복구 실패 후 무한 루프 금지, rollback 검증, 타인 Job 결과/권한 상승 차단.
- 기존 스킬의 public API/입력/출력과 기존 예약 실행, source/work ledger evidence를 회귀 시험한다.

### S6 — 운영 적용 게이트와 인계
- 산출: 사내 변경 목록/근거 함수/모의 테스트 결과/수정 해시/백업·롤백/마이그레이션·MCP 재등록 절차/운영 E2E 점검표.
- **운영 MCP apply/restart, 실제 소스/권한 변경, 공식 스킬 release는 별도 승인** 및 조직 정책 준수. 승인 전 Stage·테스트 결과만 제출한다.
- 적용 승인 후에는 MCP tools/list → capability_list → 진단 → 승인된 Job read → 예외 재현 → AUTO_SAFE 복구 → Agent 실제 재조회까지 관찰. 실패 시 즉시 rollback 경로 준비.
- Dropbox는 비민감 완료/미완료/버전/원인/결정만 수동 게시; 원본 코드·ZIP·실행 로그 자동 보관 금지.

## 8. 범위 제한·비기능 수용기준

- 보안: least privilege, allowlisted manifest 및 profile, server-side path pinning, read/write/repair/deploy role 분리; 외부 Agent에서 일반 셸·임의 파일 브라우징 불가.
- 신뢰성: Job 등록 전 조회 contract 확인; 이미 처리한 요청은 중복 실행되지 않음; 알 수 없는 실행 상태는 UNKNOWN으로 재조사, 임의 재실행 금지.
- 관찰성: 실패 이유와 책임 계층을 출력하는 stable error code, incident correlation ID, 운영 audit, 민감정보 sanitize 테스트.
- 자동복구: Playbook별 명시적인 허용·승인·종료·원복·재검증, **복구 후 같은 요청의 기능 결과로 PASS 판정**.
- 하위호환: 기존 Job/Run 식별자, queue/receipt, 기존 MCP read, updater 자동 스케줄은 변경 필요성과 회귀 증거 없이 파괴하지 않음.
- 스테이징 패치 생성은 완료 아님. 사내 설치 확인, 로컬 테스트, 운영 apply, Agent E2E 상태는 각각 별도 표시.

## 9. 사내 LLM 원샷 전달용 프롬프트(복사 영역, 3,000자 이내)

```text
첨부 MD를 정본 요구사항으로 하여 S0~S6을 순서대로 수행해줘.
목표: whpark-mcp를 동적 Job/Skill Capability Gateway로 보강하고,
code-analyzer/issue-analyzer 등 실패 시 원인 진단→허용된 자동복구→동일 요청 재검증까지 구현.
우선 설치된 job-list·updater·live MCP·두 analyzer의 실제 버전/계약을 확인해.
첨부 job-list 0.4.25는 참고용이며 운영 job-list 0.4.26과 동일하다고 추정 금지.
S0에서 JOB-20261031-MCP-SDM-PARSER-READ-STAGE-01 로컬 결과와 MCP RESULT_UNSUPPORTED
차단 원인부터 확인. 기존 Job 재실행·재등록·삭제, Updater 재실행 금지.
S1에서 live MCP 코드를 확인해 schema/auth/backend 간 정확한 차이를 보고,
S2~S5는 실제 소스 구조에 맞춰 격리 작업공간에서 구현·모의 테스트해.
새 승인 Job은 개별 MCP hardcode 없이 Registry에서 탐색·조회하되
미승인 Job·임의 경로/셸/프롬프트·권한 상승은 반드시 차단해.
Preflight는 enqueue 전에, receipt/semantic/deployment/Agent E2E는 별개 상태로.
AUTO_SAFE는 사전 승인된 playbook만; 코드 수정안은 STAGE_ONLY로 검사·테스트.
운영 MCP 적용·재시작·권한/소스 변경·배포는 승인 전 실행 금지.
특히 code-analyzer와 issue-analyzer의 설치, source mapping, runner, 호출,
실행 결과, MCP 조회 오류를 장애 주입으로 분리 검증하고 복구 후 동일 요청 재검증.
테스트 근거 없는 PASS 금지. 실패 시 원인·미해결·다음 최소 조치 제출.
외부 결과에는 코드·사내 경로·패치·원문 로그·비밀·개인정보 금지.
최종 숫자 8개 한 줄(S0/S1/S2/S3/S4/S5/S6/자동복구E2E):
1=PASS, 2=STAGED_OR_PARTIAL, 3=BLOCKED, 4=NOT_RUN.
그다음 BLOCKER와 NEXT 각각 1줄. 승인 필요한 작업은 별도 목록으로 보고.
```

## 10. 최종 리포트 양식과 단계 구분

```text
S0 S1 S2 S3 S4 S5 S6 AUTO_E2E: 1 1 2 2 2 1 4 4  # 예시, 실제 결과 아님
BLOCKER: (한 줄)
NEXT: (한 줄)
APPROVAL_REQUIRED: (한 줄)
```

결과 코드 `1=PASS, 2=STAGED_OR_PARTIAL, 3=BLOCKED, 4=NOT_RUN`. 사용자가 모바일로 결과를 타이핑할 때는 **위 숫자 8개 + 단문 최대 3줄**만 전달해도 다음 판정을 이어갈 수 있어야 한다. 코드/패치 상세는 사내 보관.

## 11. 미해결 항목 / 수행하지 않은 일

- S0 실제 Job 결과: 미확인. 현 시점에 `RESULT_UNSUPPORTED` 보고만 있음.
- live `whpark-mcp` source/registry/auth/backend: 이 대화에서 직접 열람하지 못함.
- `code-analyzer`/`issue-analyzer` 설치 환경·실행 계약: 사내 확인 필요.
- Registry/Preflight/diagnostic playbook/auto-recovery: **설계에만 존재**, 구현·테스트·배포 미실시.
- 다음 행동: 사내 LLM에 본 단일 MD를 전달하여 S0 원인복구와 S1 live 조사부터 시작하고, S2~S5를 **격리 환경에서만** 진행. 변경 적용은 결과 검토와 승인 후 별도 수행.
