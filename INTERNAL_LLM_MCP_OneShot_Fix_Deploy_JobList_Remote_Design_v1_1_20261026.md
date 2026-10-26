# whpark-mcp 원샷 수정·배포·E2E + Job-list 사외 작업 연계 — 사내 LLM 구현 지시 v1.1

- 기준일: 2026-10-26
- 문서 상태: **구현 요청 / 사내 소스·권한·운영 설치본 최종 미검증**
- 기반: `MCP_OneShot_Diagnostics_Pingpong_Reduction_Design_20261026.md`, `INTERNAL_LLM_MCP_Improvement_Prompt_v1_1_20261026.md`, `AGENT_MCP_Analysis_Find_E2E_Verification_20261026.md`
- 기존 사용자 Agent 결과: `3 1 2 3 3 2 1 4` (Q1~Q8; **이번 실행 결과가 아님**)
- 기존 관련 패키지: `job-list v0.4.25` 및 `skill-updater v0.5.43`은 앞선 인계 문서의 기준이다. **현재 사내 설치 버전은 별도 대조 필요**.
- 주요 요청: **단순 진단 보고로 종료하지 말고, 합법적으로 가능한 범위에서 원인 재현 → 수정 → 테스트 → 승인된 배포 → 실제 MCP·Agent E2E까지 연속 수행.** 향후 사외 `job-list` 작업의 MCP 접점도 함께 분석·단계별 구축.

> 아래 목표 인터페이스명(`mcp_diagnose`, `job_request_plan` 등)은 **가칭**이다. 기존 서버의 도구명·MCP transport/권한 구조를 우선 확인하고, 동등 기능이 있으면 새 도구를 만들지 않는다. 설계나 개발 테스트를 운영 검증으로 주장하지 않는다.

---

## 1. 무엇을 이번에 끝내야 하는가

### 1.1 지금 발생한 8항목 문제 해결 (P0)

| 항목 | 보고 | 이번 수용 조건 | 분리할 원인 |
|---|---:|---|---|
| Q1 운영 패치 반영 | 3 | 실행 중 **실제 MCP 서비스**의 로드 revision 및 배포 증거 확인 | 개발 소스 vs 배포 artifact vs 실행 프로세스 |
| Q2 SOC 단독 검색 | 1 | 기존 authorized 조회 회귀 유지 | 응답 계약·권한 변경 방지 |
| Q3 SOC 포함 자연어 | 2 | `SOC-420517의 ...`에서 같은 SOC scope 해석 + 관련 질문 보존 | 인자 전달/파서/검색 필터/데이터 연결 |
| Q4 근거 연결 | 3 | WORK/RUN/ANALYSIS/EVIDENCE 참조 또는 근거 부족을 정직하게 반환 | 링크 유무 vs 데이터 유무 |
| Q5 상세 READ | 3 | 응답에서 허용된 참조를 실제 READ 호출하여 결과 확인 | 서버 등록/권한/참조 유효성 |
| Q6 SOC 없는 질문 | 2 | 명시적 scope 없으면 전체 검색 금지, 명확한 범위 확인 응답 | 범위 누락 vs 정책적 차단 |
| Q7 ID 경계 | 1 | `SOC-4205170`을 `SOC-420517`과 혼동하지 않음 | 과다 매칭 방지 |
| Q8 Job READ | 4 | 서버 등록/접근권한/실제 Agent 노출을 분리해 고치거나 정확한 blocker 제시 | Tool 미등록 vs auth vs client allowlist |

숫자 정의는 기존 Agent 계약 준수: **1=실제 호출 PASS, 2=FAIL, 3=미검증/자료 부족, 4=도구 미노출 또는 권한 차단**. 모든 성공 판정은 **신규 호출 근거** 필요. 과거 결과를 그대로 PASS로 재표시 금지.

### 1.2 반복 문의를 줄일 공통 기능 (P0/P1)

- **Runtime Identity**: 현재 서비스에 실제 적용된 코드·설정·배포 receipt의 신원과 불일치 여부를 READ로 확인.
- **One-shot diagnosis**: 한 번의 Agent 요청에 Q1~Q8 및 실패 위치, 관련 evidence_ref, 권장 조치를 묶어 반환.
- **Diagnostic receipt**: 같은 오류 반복 시 최근 진단의 실행 환경·근거·수정 전후 비교를 재조회.
- **Deploy→auto verify**: 기존 승인된 배포 경로에서 적용한 뒤 자동 smoke/회귀/실제 MCP call을 수행하고 실패 시 안전하게 복구.
- **Client exposure 확인**: 서버가 도구를 안다는 사실과 사외 Agent의 실제 `tools/list`/`tools/call` 결과를 별도로 기록.

### 1.3 미래 `job-list` 사외 작업의 목표 (P1/P2, 현재 지원 확정 아님)

사용자 자연어 예:

1. `SOC-420517 코드 분석 요청해줘` → 기존 분석 근거 확인 → 없거나 부족하면 **허용된 Job plan**을 제시.
2. `그 Job 등록해줘` → 요청 내용·대상·권한·중복·승인 검사 → 안전하게 queue/receipt 연결 (**기존 지원 확인 후에만**).
3. `분석 어디까지 됐어?` → 동일 job_id의 queue/worker/receipt/semantic result 및 evidence refs를 READ.
4. `왜 막혔어? 다음엔 뭘 해야 해?` → 첫 실패 단계, 재시도 가능 여부, 필요한 사내 조치 반환.
5. `결과 근거 보여줘` → 권한 내 분석 근거의 **요약·참조**, 필요 시 후속 READ. 민감 원문 외부 반환 금지.

**제안 생성(Stage), 큐 등록(Enqueue), 실제 Job 실행(Execute), 승인 후 운영 적용(Apply), 후속 결과 조회(Read)**는 다른 상태다. 특히 기존 v0.4.25 Stage가 제안만 생성하는 구조라면, Apply Job이 있다고 가정하지 말 것.

---

## 2. 사내 LLM 작업 규칙: 원샷으로 진행하되 권한은 우회하지 말 것

1. 먼저 사내 실제 `whpark-mcp` 소스/manifest/router/권한 설정, `job-list`, `skill-updater`의 활성 설치본과 revision, 배포 방식 및 진단 이력을 읽는다. 사용자에게 이미 서버가 확인할 수 있는 경로·버전을 묻지 않는다.
2. 하나의 작업 회차에서 **원인 조사 → 재현 테스트 → 최소 코드 수정 → 개발 회귀 → 변경 diff/해시 → 배포 경로 확인 → 승인된 경우 적용 → 프로세스 reload 및 health → MCP 실제 호출 → Agent 검증 자료 작성**을 순서대로 수행한다.
3. **승인이 이미 적법하게 존재하면** 범위(revision, patch SHA256, 서비스, rollback)를 대조하여 그 범위 안에서 진행. **승인이 없으면** 개발 수정·테스트와 배포 준비까지 끝내고, 필요한 운영 승인만 **한 번에** 제시한다. 승인 없이 적용/재시작/운영 Job 등록/Push하지 않는다.
4. 사용자는 **단일 기본 저장소·브랜치 전환**을 선호한다. Worktree 생성 금지. 미커밋 변경, 다른 작업 브랜치, divergence는 보존하고 격리 가능한 대안 제시. 기존 사용자 변경 덮어쓰기 금지.
5. MCP 진단은 READ-only. 진단 호출을 핑계로 Job 실행, 예약 변경, queue/receipt 변경, 서비스를 수정하지 않는다. 진단 receipt **별도 영역에 기록**은 승인된 관측 경로에서만, 운영 원장과 구별한다.
6. MCP의 `tools/list` 또는 로컬 unit test만으로 운영·사외 E2E PASS를 주장하지 않는다. Agent가 실행할 수 없는 환경이면 `REMOTE_E2E=NOT_TESTED`를 유지하고 1회 실행 가능한 Agent 프롬프트를 작성한다.
7. 토큰·사내 원문 로그·절대경로·소스 패치 본문·내부 인프라 상세를 사외 반환 또는 개인 Dropbox/GitHub 자동 전송하지 않는다. 권한별 필드 allowlist·사이즈 상한을 적용한다.
8. 실패 하나 때문에 독립적으로 가능한 나머지 검증을 멈추지 않는다. 마지막에 확인이 필요한 사람 결정을 **한 번에 묶어** 질문한다.

### 구현 전 우선 확인 — 최초 1회

- 개발 HEAD, 패치 hash, 배포 package ID, 운영 서비스가 실제 로드한 revision, feature flags의 차이.
- `analysis find`의 실제 tool 인자와 호출 체인: Agent → MCP router → SOC 식별자 추출 → scope → index/search → reference linkage → READ.
- Job READ bridge `catalog/queue/result`의 실제 MCP 등록명, server auth, 외부 Agent visibility, ID allowlist.
- 기존 진단/status endpoint 및 로깅·trace ID, 기존 승인된 rollout/rollback 절차.
- Job-list 요청 접수/큐 enqueue 실행 엔트리의 유무와 권한 경계. 기능이 없다면 “현재 미구현”으로 기록.

---

## 3. P0 현재 문제 수정 + 배포 + 재검증 상세

### 3.1 수정 전 실패 재현

- 동일 actor/권한/scope/데이터로 `analysis find SOC-420517`와 `analysis find SOC-420517의 main_dac_path와 tx_dac_path가 다른 이유는?`를 비교.
- `SOC-420517의`를 **SOC-420517**로 인식하고 나머지 심볼 2개와 자연어 질문을 잃지 않아야 함.
- `SOC-4205170` 등 인접 유효 ID 혼동, 복수 SOC, explicit scope 충돌, SOC 없는 요청 모두 검증.
- 같은 SOC scope에 자료가 존재하지만 심볼과 직접 연결된 근거가 없다면 **scope search 결과**와 **질문 답변 근거 부족**을 분리. 성공한 scope 결과를 0건으로 숨기거나 원인 설명을 생성하지 말 것.
- Q8에서 서버 도구 **미등록/기능부재**, 서버 권한 거부, Agent tool list 미노출, 실제 tools/call 실패를 별도 분류. 클라이언트 측 증거 없이 서버에서 Agent 노출 성공이라고 할 수 없음.

### 3.2 코드 수정 범위

- 새 LLM/벡터DB를 기본 전제로 삼지 말고 **기존 인자 파서·scope·링크 조회·serializer**의 최소 결함만 수정.
- 한국어 조사, 구두점, 식별자 경계는 기존 ID 규칙과 테스트로 고정.
- 기존 READ bridge / Job allowlist는 유지. `RUN-*`를 `JOB-*`로 허용하는 식의 임의 입력 확대 금지.
- Q6 응답은 기존 범위확인 에러가 있으면 재사용하고, 없을 때만 호환되는 scope-required 상태를 제안/구현.
- Q4/5: 근거 참조와 READ action을 연결하되, 존재하지 않는 참조·권한 없는 자료를 만들거나 노출하지 않는다.
- Q8: MCP 노출 누락이면 **기존 허용된 READ 도구만** 등록/수정; 권한 정책이 필요하면 무단 allowlist 확대 대신 승인 대상과 영향 평가를 명시.

### 3.3 런타임 신원 / 원샷 진단

기존 API가 없다면 read-only 도구 `mcp_diagnose` (가칭) 및 runtime status를 제안한다. 이 도구의 권한·응답은 실제 구현에서 확정.

```json
{
  "schema": "mcp-diagnostics-request/1",
  "profile": "ANALYSIS_FIND_E2E",
  "issue_id": "SOC-420517",
  "question": "SOC-420517의 main_dac_path와 tx_dac_path가 다른 이유는?",
  "job_id": "JOB-20261024-MCP-JOB-READ-STAGE-01",
  "dry_run": true
}
```

읽기 전용 8체크 후 아래 정보 제공:

- `runtime.loaded_revision`, `deployed_patch_sha256`, `deploy_receipt_ref`, `observed_at`, `deployment_status` (확인 가능한 것만).
- `checks.Q1...Q8`: `PASS/FAIL/NOT_TESTED/UNAVAILABLE`, **원래 1~4 변환**도 함께 반환.
- `first_failure.stage`, `blocker_code`, `evidence_refs`, `next_action`, `owner_boundary` (MCP 코드/배포/Agent 클라이언트/권한).
- 단계별 trace: input parsing, normalized scope, filter, result refs count, linkage, actual subsequent READ; 내부 source/경로/토큰 없이 안전한 메타데이터만.
- `server_registered`, `server_authorized`, `server_call_verified`와 `agent_tool_visible`, `agent_call_verified`를 구분. 후자 둘은 실제 Agent 확인 결과가 없으면 `UNKNOWN`.
- 진단 오류는 기존 의미와 호환되는 코드로 표현. 신규 에러명은 사내 계약 확인 후 매핑하며 ‘구현 완료’로 가정하지 않음.

**멱등:** 진단 request_id/trace_id가 중복되면 최신 재실행인지 이전 receipt 조회인지 구분. 변경 이력을 덮어쓰지 말고, 시간·loaded revision을 비교 가능하게 기록.

### 3.4 개발에서 운영까지의 한 번의 폐루프

```text
READ BASELINE (운영·개발 identity)
  → REPRODUCE (Q1~Q8, 실패·근거)
  → PATCH (minimal scope; protected branch, no worktree)
  → TEST (unit + regression + security + protocol)
  → DEPLOY PLAN (diff/hash/target/restart/rollback)
  → AUTHORIZED? ─ No → READY_FOR_APPROVAL, 멈춤, 단일 승인 요청
               └ Yes → BACKUP → APPLY → RESTART → HEALTH
                        → RUNTIME IDENTITY 재조회
                        → 실제 MCP tools/list + tools/call
                        → Q1~Q8 재검증 + diagnostic receipt
                        → CLIENT E2E(가능 시)
                        → PASS 또는 실패시 정책에 따라 ROLLBACK/정확한 blocker
```

- 운영 변경 권한이 없으면 `PATCH_TESTED / NOT_DEPLOYED / REMOTE_E2E_NOT_TESTED`를 분리.
- **배포 완료**는 실제 loaded revision+배포 receipt가 일치해야 함. Git HEAD, Updater SUCCESS, service health, 도구 노출만으로 부족.
- smoke 실패 시 승인된 롤백 정책에 따라 **코드/설정만** 복구하고 기존 Job 원본 이력·queue·receipt는 훼손하지 않는다.
- 자동 검증 결과는 기존 Jobs와 다른 `diagnostic_id`의 append-like receipt로 남겨 과거·현재 상태 비교 가능하게 한다.
- Agent에서 직접 E2E 호출할 수 없으면 최종 문서에 복사해 쓸 **3000자 이내, 읽기 전용, 숫자형** 사외 검증 프롬프트를 반드시 생성.

---

## 4. 향후 Job-list 사외 작업용 MCP: GAP 분석 및 단계별 기능

### 4.1 먼저 경계를 확인

기존 Job-list v0.4.25 인계에는 `job-catalog-read`, `job-queue-read`, `job-result-read`, `job-bootstrap-status --compact` 및 고정 3개 Job에 대한 Stage/READ 계약이 보고돼 있다. **이 문서가 이 기능들의 운영 노출·정상 호출을 증명하지는 않는다.** 현재 Q8은 도구 미노출 또는 권한 차단 보고.

현재 수동 Job 진행에서 반복 질문을 유발하는 공백:

1. **작업 선택:** catalog 미조회/ID 매핑 실패 → 같은 Job 재등록 요구.
2. **작업 접수:** 채팅의 자연어 요청이 실제 `job-list` 작업 스키마에 맞게 변환됐는지 확인 어려움.
3. **실행 상태:** Updater 예약 결과, queue, running marker, terminal receipt, semantic result가 섞여 완료처럼 보임.
4. **근거 회수:** Job SUCCESS 후 실제 분석 Work/Run/Evidence와 후속 READ 경로가 연결되지 않음.
5. **수정·배포:** Stage proposal.patch 생성과 운영 적용 여부가 뒤섞임.
6. **재시도:** 재실행 가능한지와 기존 Job 손상 방지 규칙을 원격 Agent가 판단하기 어려움.

### 4.2 권장 MCP capability (단계별; 실제 지원 여부를 먼저 점검)

| 단계 | 필요한 기능 (가칭) | 실행 모드 | 목적/주의 |
|---|---|---|---|
| P0 | `mcp_runtime_status`, `mcp_diagnose` | READ | 배포·도구·검색·Job READ 첫 실패 지점 찾기 |
| P0 | `job_catalog_read`, `job_queue_read`, `job_result_read` | READ | 기존 고정 Job 이력·실제 semantic result 확인. 현재 미노출 경로 우선 복구 |
| P1 | `job_capabilities_read`, `job_request_validate` | READ / PLAN | 수행 가능한 job 종류, 요청 필수정보, runner/provider 상태, 권한 미리 확인 |
| P1 | `job_request_plan` | PLAN | 자연어 → canonical job type/target/input refs/실행 예상 경계·중복 후보. **등록 없음** |
| P2 | `job_request_enqueue` | MUTATION (별도 승인) | 기존 허용 Job 타입만 접수, permission/allowlist/idempotency/receipt 필수 |
| P2 | `job_execution_status`, `job_artifact_refs_read` | READ | 접수→대기→실행→완료·차단·제안 상태를 동일 job_id로 추적 |
| P2 | `job_retry_plan` | PLAN | 실패 근거·중복/재시도 안전성·기존 ID 정책 평가, 자동 실행 아님 |
| P3 | `job_cancel` 또는 승인된 `job_retry` | MUTATION (별도 승인) | 시스템 정책이 허용할 때만; running receipt/원장 무단 변경 금지 |
| P3 | `deployment_receipt_read`, `job_apply_plan` | READ / PLAN | Stage patch의 실제 배포 여부를 독립 추적. **Apply Job 존재 가정 금지** |

권장: **P0 READ와 P1 PLAN을 먼저 구축**, P2의 원격 작업 접수는 내부 승인·runner 계약·역할 기반 권한이 확인된 후에만. `job-list` 버전 증가나 updater 교체를 기본 해결책으로 삼지 말 것.

### 4.3 Job lifecycle / 출처 상태를 하나의 READ 응답으로

```text
REQUEST_NOT_FOUND
  → PLAN_READY (미등록, 실행 아님)
  → APPROVAL_REQUIRED (미등록)
  → ENQUEUED → PENDING → RUNNING
  → terminal receipt [SUCCESS | FAILED | BLOCKED | CANCELLED]
  → semantic result [COMPLETE | REVIEW_PENDING | NEEDS_EVIDENCE | ...]
  → (별도) patch deployment [NOT_APPLIED | APPLIED_VERIFIED | UNKNOWN]
```

- 위 명칭은 **예시 모델**이며 실제 기존 status enum에 매핑. 레거시 queue/receipt를 바꾸지 않는다.
- `UPDATER_SUCCESS`, `ACTIVATION_CALLED`, `SCHEDULED`, `RUNNING`, `RECEIPT_SUCCESS`, `REVIEW_PENDING`, `PATCH_APPLIED`는 서로 다른 단계.
- 예약된 과거 snapshot을 현재 프로세스 alive와 동일시하지 않는다. `observed_at`, `source`, `run_id` 제공.
- UI에서는 사용자가 `왜 아직 안 끝났는지`, `어디까지 왔는지`, `결과 근거는 무엇인지`, `다음 행동이 무엇인지`를 **한 번에** 확인하도록 한다.

### 4.4 원격 Job 요청 계약 (P1/P2 제안, 현재 구현 아님)

**계획/검증(읽기 전용)**

```json
{
  "schema": "job-request-plan/1",
  "user_request": "SOC-420517 코드 분석해줘",
  "target": {"kind": "SOC", "id": "SOC-420517"},
  "work_ref": null,
  "desired_output": "CODE_FACTS_SUMMARY"
}
```

계획 응답에는 `candidate_job_type`, `eligible_provider`, `missing_inputs`, `allowed_operations`, `expected_result_refs`, `duplicate_candidate`, `authorization_required`, `plan_digest`를 포함하되 모두 서버가 허용한 값만.

**등록(향후 권한 승인 시에만)**

- Client는 임의 `shell`, 실행 파일, `root`, `cwd`, 사내 경로, 환경변수, credential, 임의 provider/action을 넣을 수 없음.
- **Canonical job type allowlist + 서버측 target/scope 검증**; 거부 사유를 안전하게 반환.
- `plan_digest`와 actor/권한/입력 revision/만료를 바인딩한 서버 신뢰 승인. 채팅에서 `approved=true` 쓰기만으로 enqueue 불가.
- 중복 요청에는 `idempotency_key`와 기존 job_id를 반환. 원래 고정 Job ID 3개를 새 ID로 복제하거나 재등록하지 않는다.
- 새 ID는 **새로운 승인된 사용자 작업**일 때만 canonical allocator가 발급. 사용자 임의 ID로 과거 큐 이력 덮어쓰기 금지.
- 성공할 때만 `ENQUEUED` 선언; 예약 호출 성공만으로 작업 완료 선언 금지.
- job 실행은 기존 스케줄러/런처가 수행; MCP 요청에서 임의 subprocess 직접 실행 금지.

### 4.5 관측/진단이 재사용 가능한 공통 Response Contract

```json
{
  "schema": "job-remote-status/1",
  "job_id": "server-authorized-opaque-job-id",
  "read_source": "queue|receipt|semantic_result|deployment",
  "observed_at": "server-generated-time",
  "queue_state": "UNKNOWN",
  "receipt_state": "UNKNOWN",
  "semantic_state": "UNKNOWN",
  "deployment_state": "UNKNOWN",
  "first_failure_stage": null,
  "blocker_code": null,
  "evidence_refs": [],
  "next_allowed_actions": ["READ_RESULT"]
}
```

다른 READ 결과들을 **상태별로 투명하게 조합하는 뷰**이지 Jobs 원장에 쓰지 않는다. detail은 권한 검증 후 추가 READ. 내부 절대경로·raw 로그·patch 본문을 외부 노출하지 않는다.

### 4.6 사내 Job-list/skill-updater와의 정합성

- 먼저 **패키지 버전과 실제 MCP/Job-list 설치본**을 확인한다. `job-list v0.4.25`에 `Stage`와 고정 Job READ가 있었다는 인계 내용은 사내 운영 확인과 구분.
- `skill-updater v0.5.43`의 **예약 자동 실행 경로**와 일반 run/update를 구분; 예약 `scheduled_job_result`가 있으면 그것만 scheduler 근거로 처리.
- `requests/preserved`는 활성 큐가 아니다. 큐 등록/worker 시작/terminal receipt의 별도 근거 필요.
- 정상 RUNNING 시 queue와 running marker 동시 존재를 무조건 `STATE_CONFLICT`로 판단하지 않는다.
- 고정 3개 Job (`JOB-20261024-MCP-JOB-READ-STAGE-01`, `JOB-20261024-MCP-ANALYSIS-FIND-PROPOSAL-01`, `JOB-20261021-L1-WORKSPACE-ARTIFACTS-MIGRATE-01`)의 기존 기록을 보존한다.
- 기존 `job-catalog-read/queue-read/result-read` 입력 allowlist와 bytes 상한을 우회하지 않는다. 확장은 명시된 설계·승인·회귀가 있을 때만.
- 현재 `job-list` 안에 원격 Request/Enqueue API가 없으면 **P1 PLAN까지만** 구현하고 P2는 제안 패치/권한 요구사항으로 남긴다.

### 4.7 사용자 체감 UX — 장기 목표

사외 Agent 호출 1회:

```text
"SOC-420517 코드 분석 요청하고, 같은 Job의 현재 상태와 확인 가능한 근거도 알려줘"
```

응답 예시(실제 상태 아님):

```text
작업: CODE_ANALYSIS (요청 계획 수립, 아직 등록 안 됨)
상태: PLAN_READY / APPROVAL_REQUIRED
근거: 기존 Work 결과 1개, 상세 READ 가능 여부 UNKNOWN
차단: REMOTE_ENQUEUE_NOT_AUTHORIZED
다음: 승인된 PC 경로로 작업 접수
```

원격 권한이 없다면 성공처럼 꾸미지 않고 **계획·조회까지만** 제공하므로 이 예시도 현재 구현 완료를 뜻하지 않는다.

---

## 5. 핑퐁 감소 관점 우선순위 / 선택 기준

| 변경 | 핑퐁 감소 이유 | P0/P1/P2 | 사내 실측 필요한 것 |
|---|---|---|---|
| Runtime identity + deploy receipt | “수정했는데 운영에는 옛 코드?” 확인 1회화 | P0 | 배포 서비스/런처·receipt |
| `mcp_diagnose` Q1~Q8 | 매번 8문항 원인별 재질문 제거 | P0 | 기존 MCP 등록/권한/trace |
| analysis find parser/scope + refs | 같은 SOC인데 0건 문제 해결 | P0 | 실제 코드 재현 |
| Job READ bridge 실제 Agent 노출 | Job 결과를 다시 타이핑하지 않음 | P0 | server/client tool visibility |
| Deploy smoke/rollback+receipt | 사내 수정 후 Agent 재시험 횟수 감소 | P1 | 승인된 배포 정책 |
| Job status 통합 READ | queue/receipt/semantic 구별 질문 감소 | P1 | job-list 로컬 계약 |
| Job request plan/validation | 실행 전 “도구 없음/대상 없음” 반복 방지 | P1 | runner/provider allowlist |
| Remote Enqueue (authorized) | 사외에서 실제 작업 요청까지 연결 | P2 | 인증/승인/스케줄러 계약 |
| Remote retry/cancel/apply | 반복 실험·운영 조치 감소 가능하지만 위험 큼 | P3 | 별도 정책/승인 필요 |

**권장:** 이번 개발에서는 **현재 8문항 복구 + P0 도구 통합 + P1 status/plan의 계약/테스트까지** 우선한다. P2 이후는 설계와 근거를 남기되, 실제 정책 미승인 상태에서 운영 mutation을 추가하지 않는다.

---

## 6. 테스트/인수 조건 (이번 과제의 Done 정의)

### 6.1 현재 Q1~Q8

- Q1: 실행 중 MCP runtime identity와 배포 receipt 일치 (불가하면 3·blocker 유지).
- Q2/Q7: 기존 작동 회귀 및 권한/경계 검증.
- Q3: SOC 포함 한국어 조사 질의가 Q2와 같은 SOC 범위를 식별하고 심볼 보존. 범위 레코드와 질문 근거 부족을 구분.
- Q4: 존재하는 참조만 연결, 연결 정보 없으면 `INSUFFICIENT`/미확인 정직 표기.
- Q5: 허용된 근거 READ 1회 이상 실제 호출. 자료 없는 경우 정직한 3 판정.
- Q6: scope 없는 질의는 안전한 범위 확인/정책 응답, 글로벌 검색 수행 0회.
- Q8: 서버 등록/권한/Agent 노출 분리, 실제 Agent에서 호출 확인. 미노출이면 4 유지.

### 6.2 원샷·상태·안전성

- **One-shot** 진단 응답에 각 Q의 상태+첫 실패 단계+증거 참조+다음 조치가 존재.
- 배포 권한 없는 경우 실제 운영 수정/재시작 0건, `NOT_APPLIED`로 표시.
- 허용된 배포 진행 시 백업→적용→reload→runtime 비교→실제 tool 호출→receipt 기록. 실패 시 승인된 rollback 시나리오 검증.
- 서버/Agent tools/list만 있고 tools/call 없으면 운영 E2E PASS 금지.
- Job-list request PLAN 호출이 queue/receipt/work/evidence 원본을 **수정하지 않음**.
- 동일 요청 2회 시 원격 Job 중복 등록 0건(향후 enqueue 활성 시).
- 허가 없는 Job 타입/임의 command/root/job ID/외부 출력 시도는 거부.
- 기존 고정 Job 이력·Updater 예약 진단 정상 보존. 미지원 기능을 `VERIFIED` 표시 0건.

### 6.3 구현·운영 결과 판정은 별개

- `DEVELOPMENT_TESTED`: 수정 코드 및 unit/regression 증거.
- `READY_FOR_APPROVAL`: 배포 계획/hash/대상/롤백까지 준비했으나 승인 없음.
- `DEPLOYED_VERIFIED`: 대상 서비스 로드 revision과 승인된 배포 receipt가 일치.
- `MCP_E2E_VERIFIED`: 실제 MCP 실행 호출로 Q 관련 항목 확인.
- `REMOTE_AGENT_E2E_VERIFIED`: **사외 Agent 자신의 tool list + tool call 실제 근거** 확보.
- `JOB_REMOTE_PLAN_SUPPORTED`: Job plan이 실제 READ/PLAN으로 검증.
- `JOB_REMOTE_ENQUEUE_SUPPORTED`: 별도 승인된 mutation까지 실제 검증. 설계만으로 이 상태 사용 금지.

---

## 7. 사내 LLM 최종 실행 지시 (복사·전달용)

> **whpark-mcp 소스 개발 담당 LLM에게 지시한다.**
>
> 1. 본 문서 §1의 Agent 결과 `3 1 2 3 3 2 1 4`를 출발점으로 Q1/Q3/Q6/Q8 원인을 확정하고 Q4/Q5도 실제 READ까지 검사해라. Q2/Q7은 보존해라.
> 2. 기존 소스/manifest/서버 노출·권한·운영 loaded revision과 `job-list` 설치본을 직접 확인해라. 사용자에게 디버깅 질문을 반복하지 말고 조회 가능한 정보를 한 번에 수집해라.
> 3. 최소 코드 수정과 unit/security/regression 테스트를 실제 수행해라. 임의 근거 생성, 무관한 버전 업데이트, 새 Job ID 복제, Worktree 사용을 금지한다.
> 4. Runtime Identity + 원샷 진단 + 장애 단계 분류를 기존 MCP API에 맞춰 구현하고, 실제 Job READ 노출을 복구해라. 중복 도구는 만들지 마라.
> 5. **승인된 배포 권한이 이미 있을 때는** 백업→적용→재시작→loaded revision 확인→MCP smoke+Q1~Q8 재호출→diagnostic receipt→필요시 rollback까지 수행해라. **승인 없으면** 패치·테스트·revision/hash·롤백계획을 완성하고 **단일 승인 요청**으로 멈춰라.
> 6. 향후 사외 Job-list 작업 지원을 위해 §4의 현재 capability를 실측해 GAP 표를 작성해라. P0 READ·P1 PLAN은 가능하면 구현/검증, P2 MUTATION은 승인·권한·스케줄러 계약이 확인된 경우에만 구현해라. 원격 Agent가 임의 명령을 수행하게 하지 마라.
> 7. 결과를 사용자에게 숫자 위주로 짧게 보고하고, 상세 근거는 사내 검토용 MD에 남겨라. 마지막 Agent 검증이 불가능하면 **3,000자 이내 read-only Agent 검증 MD**도 작성해라.

### 사내 필수 산출물

- `MCP_ROOT_CAUSE_AND_FIX.md`: 원인 위치(파일/함수), 수선 전후 재현, 변경 요약.
- `MCP_PATCH_AND_TEST.md`: 대상 revision, 패치 SHA256, unit/regression/security 결과, 기존 기능 영향.
- `MCP_DEPLOY_AND_ROLLBACK.md`: 적용 권한, patch/target binding, 백업/재시작/복구, 실행 증거.
- `MCP_ONE_SHOT_DIAGNOSTIC_REPORT.md`: Q1~Q8, runtime identity, 서버/Agent 노출 구분, blocked-by 단계와 evidence refs.
- `MCP_JOB_LIST_REMOTE_GAP_AND_ROADMAP.md`: 현재 등록된 MCP Job 도구·Job-list 로컬 CLI의 실제 계약, 추가 필요 기능, P0~P3 구분.
- `AGENT_REMOTE_E2E_VERIFY_3000.md`: 사외 Agent 읽기 전용 확인용. 실제 Agent E2E가 사내에서 불가할 때 제공.

### 사용자에게 전달할 최종 요약: 숫자 입력 최소화

```text
Q=<Q1 Q2 Q3 Q4 Q5 Q6 Q7 Q8>
PATCH=<TESTED|FAILED|NOT_TESTED>
DEPLOY=<APPLIED_VERIFIED|READY_FOR_APPROVAL|NOT_APPLIED|UNKNOWN|ROLLED_BACK>
MCP_E2E=<PASS|FAIL|NOT_TESTED>
AGENT_E2E=<PASS|FAIL|NOT_TESTED>
JOB_READ=<PASS|FAIL|BLOCKED|NOT_TESTED>
JOB_PLAN=<PASS|GAP_ONLY|NOT_TESTED>
JOB_ENQUEUE=<SUPPORTED_VERIFIED|NOT_ALLOWED|NOT_IMPLEMENTED|NOT_TESTED>
FIRST_FAILURE=<stage|none|UNKNOWN>
BLOCKER=<핵심 코드 하나 또는 none>
NEXT=<다음 행동 한 줄 또는 완료>
```

`AGENT_E2E=NOT_TESTED`와 `DEPLOY=READY_FOR_APPROVAL`을 성공으로 합산하지 말 것. **향후 Job-list 설계만 했다면 `JOB_PLAN=GAP_ONLY`**, 사외 등록도 지원된다고 보고하지 않는다.

---

## 8. 이번 문서에서 직접 확인하지 못한 사항

- 사내 `whpark-mcp` 서버 저장소, 설치/인증/실행 프로세스, tool registry, 현재 loaded revision 및 배포 승인 정책.
- 현재 설치된 job-list / skill-updater의 실제 버전, READ bridge 노출과 scheduler 진입 경로.
- 원격 Job enqueue/apply/취소 권한과 사내 운영 policy. 기존 인계는 Job READ/Stage 위주였으며 원격 mutation 지원을 증명하지 않음.
- 실제 `SOC-420517` 데이터의 현재 건수와 해당 코드 경로의 실측 분석 결과.

**따라서 본 문서는 ‘사내 구현을 위한 통합 작업 지시 및 설계’이며, 수정·배포·사외 E2E 성공을 주장하지 않는다.**
