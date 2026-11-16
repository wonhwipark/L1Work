# 업무 LLM 실행 요청 — Job-list v0.4.38 / Linux MCP 근본 원인 분석·최소 복구·실증 검증

- **문서:** r0003 / 2026-11-17 KST

> **PUBLIC 게시본:** 운영 호스트의 절대 경로·일부 파일 지문은 비식별화. `[MCP_ROOT]`, `[JOB_LIST_ROOT]`, `[SKILL_UPDATER_ROOT]`, `[CODE_REPO_ROOT]` 등은 업무 LLM이 실제 호스트에서 확인해야 함. 원본 상세 진단값은 승인된 로컬 입력으로만 취급. 이 문서의 게시 자체는 MCP 실행·복구 승인 또는 Job 실행 트리거가 아님.

- **목표:** 기존 `NR L1 Tx Init RACH` Job의 **실제 분석 완료 여부를 증거로 확정**하고, 확인된 결함이 있다면 **현행 Linux MCP/Job-list 연결의 최소 복구와 관련 시험**을 수행한다.
- **실행자:** 업무 LLM 및 연결된 Linux MCP/허용된 로컬 도구
- **범위:** 이번 단일 RACH Job의 설치·정의·등록·큐·Worker·결과 저장/조회 경로. 다른 스킬·Job·서비스 전면 개편 금지.
- **진행 방식:** 별도 분석 보고만 하고 종료하지 말 것. `상태 확인 → 소스/로그 기반 재현 → 직접 원인 확정 → 허용 범위 최소 수정 → 시험 → 운영 적용 여부 판정 → 결과 readback`을 **한 작업**으로 수행하라.

## 0. 최신 실증 입력: 모바일 Agent 읽기 전용 검증 (2026-11-17 00:54 KST)

다음은 **Agent가 보고한 관측 사실**이며, 업무 LLM은 운영 호스트에서 다시 확인하라.

| 구분 | 보고된 결과 | 주의 |
|---|---|---|
| GitHub PAT / Job-list | 인증 복구 후 Job-list `v0.4.38` 설치·live 확인 | 설치 성공은 분석 완료가 아님 |
| Skill-Updater | 운영본 `v0.5.43`, 목표 `v0.5.44` 미적용 | 이번 RACH 복구에 무관하면 업그레이드 금지 |
| Linux MCP 코드 | 소스·설정 변경 증거 없음. `state_files=[]`, `deploy_receipt_ref=null`, `deployment_status=CURRENT` | `CURRENT`만으로 수정·배포 성공 주장 금지 |
| MCP 서비스 | PID 변경 관측, 새 프로세스 시작 `2026-11-16 13:32` | 재시작 ≠ 코드 수정. MCP 파일 13개 mtime은 시작 전 |
| MCP 도구 파일 | `tools/job_list_read.py` mtime `2026-11-07 17:06:10`; SHA-256 `[MCP_TOOL_SHA256_VERIFY_ON_HOST]` 보고 | 실제 파일 해시 재검증 |
| RACH Job 정의 | `job_catalog_read: source=active`, `profile=nr-l1tx-init-rach-analysis-linux`, 만료 `2026-12-15` | 카탈로그 ACTIVE와 Worker 실행 구별 |
| 대상 ID | `JOB-20261115-NR-L1TX-INIT-RACH-EXEC-01` | 정확한 canonical ID / 프로필 관계 확인 |
| Queue | `job_queue_read: state=DONE`, `receipt_state=SUCCESS`, `attempts=1`, `pending_count=0`, `last_error_code=null` | 어느 단계의 SUCCESS인지 소스로 확인 |
| 실행 식별 | `enqueued_at=null`, `worker_started_at=null`, `job_status_read.run_id=null` | 실행 증거 부족. 없는 Run ID 임의 생성 금지 |
| MCP 결과 조회 | `job_result_read: ok=false`, `query_status=RESULT_UNSUPPORTED` | API 미지원과 실제 결과 미생성을 구분 |
| 결과 조회 allowlist | `bridge_result_allowlist` 9건에 대상 Job ID 없음 | 누락이 직접 원인인지 호출 계약과 함께 확인 |
| Registry / Catalog / Bootstrap | Registry 6건, Catalog 9건, Bootstrap 5건, RACH 항목·EXEC 계열 ID 매핑 불일치 보고 | 목록 역할이 다를 수 있음. 무조건 동기화 금지 |
| 산출물 | `artifact_path`, `proposal_sha256` 없음, `semantic_state=UNKNOWN` | 기존 CODE_FACTS·MSC 결과 파일 실재 여부 별도 조사 |
| 배포 추적 | `first_failure_stage=deployment_tracking`, `blocker_code=DEPLOYMENT_NOT_TRACKED` | 이 필드가 Job 실패인지 검증기/배포 추적 실패인지 확인 |

**최종 문제 정의:** `v0.4.38` 설치와 Job 활성화는 보고됐지만, **실제 코드 분석 Worker의 실행·산출물 확인·MCP 조회 성공은 입증되지 않았다.** 이전 자율 복구 요청에 대한 운영 MCP 패치 적용 증거도 없다.

## 1. 실행 시작 시 준수할 승인·안전 규칙

1. 사용자 요청은 이 **단일 장애의 원인 분석과 복구 작업 진행 지시**다. 기존 유효 승인·사전 위임의 대상·기한·비용·호스트 권한을 확인하고 **허용된 로컬 진단, 최소 개발·수정, 무비용 재현·시험은 추가 질문 없이 진행**하라.
2. 운영 설치·서비스 설정·실DB 변경·서비스 재시작·Job 재큐잉/재실행·신규 유료 LLM 호출은 **해당 동작이 기존 승인 범위에 포함됨을 확인했을 때만** 수행. 확인되지 않으면 해당 부분만 `BLOCKED_APPROVAL`로 구분하고 나머지 개발·검증은 계속 수행하라. 이미 유효한 승인을 재요청하지 말 것.
3. `DONE/SUCCESS`이고 실행 식별자가 없는 Job은 **중복 실행 위험**으로 간주. 기존 큐·영수증·Worker·원본 파일을 먼저 확인. 승인 없이 동일 Job 재실행, 재큐잉, 임의 READY 게시, 모델 호출 금지.
4. 토큰·키·민감 코드·원본 상세 MSC·로그·업무용 분석 결과는 외부 대화나 CoWork PRIVATE/PUBLIC 저장소로 반출 금지. 이 문서는 로컬 진단 프롬프트다. 작업 결과는 허용된 로컬 경로에 증빙하고 비민감 요약만 전달.
5. 변경 전 실제 대상 파일·실행 중인 경로·설정 및 영수증/상태를 보존하고 롤백 계획을 준비하라. 영수증·과거 성공/실패 이력의 삭제·덮어쓰기 금지. 실제로 수정하지 않았으면 `NOT_APPLIED`로 보고하라.
6. **새 API·DB 스키마·일괄 배포·전체 스킬 감사·전면 리팩터링 금지.** `REUSE → CONNECT → 증명된 GAP만 최소 EXTEND`. 이미 존재하는 Job-list CLI, MCP tool, runner, 결과 조회 인터페이스를 우선 재사용하라.

## 2. 현장 진단: 추측보다 실제 코드·경로·원본 계약

### A. 호스트·버전·실행 경로 확인

- 실제 MCP의 PID, 프로세스 시작 시각, 서비스/실행 진입점, Python 환경, `cwd`, 환경변수 **이름만**, 서버 코드 경로, 로딩된 모듈 경로를 확인. 다른 MCP 프로세스/가상환경/중복 설치본이 있는지 대조.
- 보고 경로: `[MCP_ROOT]/` (`server.py`, `tools/job_list_read.py`); `[JOB_LIST_ROOT]/` (`VERSION=0.4.38`). **실제 로딩 경로 우선**, 경로가 다르면 근거와 함께 기록.
- Skill-Updater 로그: `[SKILL_UPDATER_ROOT]/output/logs/auto_20261116_191039_0fdaf32e/auto.log`
- 설치 결과 보고: `[SKILL_UPDATER_ROOT]/output/20261116/auto_20261116_153232_868295e7/update_report.md`
- 먼저 최신 설치·서비스 상태를 기록한다. **Skill-Updater v0.5.44로 올리는 작업은 이번 목표와 직접 관련 없으면 수행하지 않는다.**

### B. RACH Job 단일 흐름의 계약·단계 재구성

1. 설치본 `v0.4.38`에서 실제 RACH Job 정의, canonical ID, profile, 입력/출력, 만료, 트리거, `activate`/`launch`/`schedule`/one-shot 의미를 원문 파일과 소스 행 번호로 확인하라.
2. `job_catalog_read`, `job_scheduled_read`, `job_queue_read`, `job_status_read`, `job_result_read`의 **실제로 노출된 도구명·인자·응답 스키마**부터 확인. 과거 보고 이름이 다르면 현행 이름으로 설명하고, 추측한 도구를 반복 호출하지 말 것.
3. `Catalog 9 / Registry 6 / Bootstrap 5`가 서로 **동일 집합이어야 하는지** 계약으로 판정. 특히 EXEC-01/02/03 및 Registry의 EXEC-03 관련 보고는 원본 목록을 얻어 **각 ID가 어느 목록에 있는지 표로 정확히 정리**. 목록 수를 임의로 맞추지 말 것.
4. 실행 단계별 `Skill-Updater post-update → Job-list install → active catalog → (필요 시) registry/activate → queue/launch → worker start → code analyzer → result write → result bridge`를 추적하고, 각 단계에 **KST 시각, ID, 영수증, 로그, 파일**을 매핑하라.
5. `DONE/SUCCESS`를 기록하는 소스 함수를 확인하여 그것이 **업데이트/등록 성공, 큐 처리 성공, Worker 성공, 분석 결과 성공** 중 무엇을 의미하는지 확정. `attempts=1`의 대상 단계를 확인.
6. `enqueued_at=null`, `worker_started_at=null`, `run_id=null`이 설계상 허용되는 경우인지, 누락된 실행 추적 결함인지 확인. 이미 존재하는 PID/receipt/trace와 매핑하되 **가짜 Run ID나 사후 성공 영수증을 만들지 말 것**.

### C. 실제 산출물 선확인 — 가장 먼저 종료시킬 수 있는 분기

- 해당 Job 정의에 기재된 `output_dir`, artifacts 위치, 실제 Worker 로그를 근거로 **기존** `CODE_FACTS`, 코드 분석 MD, MSC MD/HTML/SVG, 결과 영수증을 파일 검색·readback으로 확인하라. 먼저 정의된 경로를 조사하고 필요 범위 밖 디스크 전체 스캔은 피할 것.
- 파일이 있으면 **정확한 절대 경로, 파일 종류, 크기, mtime(KST), SHA-256, 내용 확인 범위**를 기록. 단순 존재와 실제 요청된 Init RACH 내용의 적합성을 구별하라.
- 파일이 없으면 실제 Worker 실행 여부를 먼저 판정하고, '결과 조회만 실패'라고 결론 내리지 말 것.
- 실제 코드 위치는 과거 `[CODE_REPO_ROOT]`로 알려졌으나 **현행 접근·브랜치·리비전·권한을 확인**. 접근 불가 시 해당 분석 단계만 BLOCKED.

### D. 조회·배포 추적 분리

- `RESULT_UNSUPPORTED`를 만든 소스의 분기와 `bridge_result_allowlist`의 구성 근거를 확인. 단순 ID 미등재 외에 **지원 결과 형식/출력 소스/접근 범위**가 필요한지 검증.
- allowlist에 추가하기 전에 이미 기록된 결과 파일을 지원되는 로컬 인터페이스로 읽을 수 있는지 확인. **결과가 없으면 allowlist만 수정해도 복구되지 않는다.**
- `DEPLOYMENT_NOT_TRACKED`를 출력한 검사기/함수와 그 의미를 확인. MCP 패치 배포 기록 미존재인지, 분석 Job 결과와 무관한 검증 단계인지 분리. 근거 없이 배포 추적용 파일을 조작하거나 성공으로 채우지 말 것.

## 3. 근본 원인 판정과 최소 복구 분기

**우선순위:** (1) 이미 분석 결과 존재? → (2) Worker 실제 실행? → (3) registry/launch 누락? → (4) 조회 allowlist와 배포 추적은 별도 결함?

| 판정된 원인 | 최소 복구 방안 | 반드시 지킬 경계 |
|---|---|---|
| A. 분석 산출물은 이미 있고 조회만 실패 | 기존 결과 경로·매핑을 연결. allowlist에 대상 Job이 포함돼야 한다는 계약이 입증되면 **해당 ID 하나만** 최소 수정 | 과거 결과 무손실, Job 재실행하지 않음 |
| B. 활성화·큐 성공만 기록됐고 Worker 시작이 없음 | 정의된 launch/runner 연결이 실제 어디서 끊겼는지 재현, 경로·등록·트리거 중 직접 원인을 최소 수정 | 운영 Job launch/재큐잉은 승인 확인 전 금지 |
| C. Worker가 시작했으나 코드 분석 실패 | 오류 코드/원본 로그 기반 입력 경로·권한·스킬/Agent 연결만 최소 수정 | 실제 코드 내용·민감 로그 외부 전송 금지 |
| D. Worker 결과는 생성됐으나 Run ID·영수증 연결이 끊김 | 기존 결과/receipt 참조를 우선 복원. 필요 시 제한된 추적 코드만 수정 | ID 사후 조작·허위 영수증 금지 |
| E. Catalog·Registry·Bootstrap은 설계상 다른 집합 | 차이를 정상 계약으로 문서화. 미필수 등록을 새로 만들지 않음 | 6·9·5개 수를 일괄 일치시키지 않음 |
| F. 실제 필요 등록 누락이 입증됨 | RACH 한 건의 기존 표준 등록 경로만 복구, 중복/만료 검증 | 기존 실행 이력과 충돌·재등록 중복 확인 |
| G. `RESULT_UNSUPPORTED`가 설계상 정상 | 이미 지원되는 결과 디렉터리/영수증 조회 사용; 사용자에겐 대체 조회 방법 제공 | MCP 신규 툴·DB 확장 불필요 |
| H. `DEPLOYMENT_NOT_TRACKED`가 별도 추적 결함 | 실제 운영 적용/영수증 존재를 보존된 근거로 판정, 필요한 경우 추적만 최소 보완 | 미적용을 적용 완료로 표시하지 않음 |

분기마다 `원인 = FACT / INFERENCE / UNKNOWN`, `영향 파일`, `변경 필요 여부`, `재현 시험`, `승인 범위`, `롤백안`을 먼저 간단히 기록한 다음 해당 분기에만 조치하라.

## 4. 실제 수정·재시험·복구 적용

1. **수정 전에 실패를 재현**하되 기존 RACH 분석 Job을 재실행하지 않는 읽기 전용 검사/단위시험/격리 모의 호출을 우선 사용.
2. 실제 source와 설정을 대조해 **직접 원인 1~2개만** 최소 패치. 불필요한 MCP 기능 추가나 Skill-Updater 업데이트, 여러 Job 정의 변경 금지.
3. 개발 영역 수정 전 원본 파일·SHA-256·백업/롤백안 확보. 수정 후 lint/단위/모의 MCP 시험 및 다음 핵심 케이스 수행:
   - 동일 Job ID/프로필/정의 버전 매핑; 스케줄 vs one-shot 구분
   - 등록·활성·실행·결과 판정의 각기 다른 상태가 혼동되지 않음
   - 기존 큐 `DONE/SUCCESS`의 원본 영수증과 중복 방지가 보존됨
   - `RESULT_UNSUPPORTED`의 지원/미지원 분기 및 allowlist 보안 정책 유지
   - 기존 result 파일을 찾고 안전하게 읽음; 없는 결과를 성공이라 표시하지 않음
   - 배포 적용/비적용, Run ID 부재, artifact 부재를 정확히 출력
4. **운영 적용이 유효 승인 범위로 확인되는 경우에만**: 영향 경로·프로세스·백업·롤백 및 기존 Job 중복 위험 확인 → 필요한 설정/파일만 적용 → 운영 readback. 재시작은 필요성과 승인 확인 후 최소 1회. 실제 새 파일 해시와 로딩된 코드 경로 확인.
5. 운영 적용에 승인 없으면 **후보 패치·격리시험까지 진행**하고 `OPERATIONAL_APPLY=BLOCKED_APPROVAL`. 이 상태를 '복구 완료'라 보고하지 말 것.
6. 실제 RACH 코드 분석 재실행이 필요하면 **기존 결과/진행 이력과 비용·중복 위험을 먼저 확인**. 기존 유효한 실행 승인 범위가 입증된 경우에만 1회 실행하고 원본 Job ID/입력 revision·request/receipt/run ID 또는 대체 식별자·결과 경로를 연결. 그 외에는 `JOB_RERUN=BLOCKED_APPROVAL`. 기존 불확실 Job을 임의 재큐잉하지 말 것.
7. 각 작업 단계와 결과에 대해 `PASS/FAIL/SKIP/NOT_RUN/BLOCKED`를 적용. 수정된 파일이 디스크에 존재하는 사실과 운영 프로세스에 실제 적용된 사실은 별도로 검증.

## 5. 완료 기준과 증거 분리

- **원인 확정:** `DONE/SUCCESS`가 의미하는 정확한 단계, Run ID 누락 이유, 6/9/5 목록 관계, `RESULT_UNSUPPORTED` 이유가 소스/영수증으로 설명됨.
- **연결 복구:** 실제 결함이 있었다면 최소 수정과 관련 시험이 통과하고, 운영 적용 범위·증거·롤백이 확인됨. 결함이 아니라 계약상 정상이라면 변경하지 않은 이유와 대체 경로가 제시됨.
- **분석 결과 검증:** 기존 결과 파일 또는 승인된 유효 실행으로 생성된 CODE_FACTS·MSC가 **실제 파일/내용**으로 확인됨. 결과가 없으면 `ANALYSIS_RESULT=UNKNOWN/FAIL/NOT_RUN` 등으로 정직하게 기록.
- **최종 성공 판정:** MCP/Job-list 도구가 다시 보인다는 것만으로는 성공 불가. **원인, 적용, 시험, 실제 분석 결과**를 각각 독립 판정한다.

## 6. 최종 보고 형식 (분량 제한 없음, 숫자 객관식 우선)

아래 항목에 **숫자 선택 + 실제 증거 경로/행 번호 + 설명 한 줄**을 표로 출력하라.

| 번호 | 항목 | 선택지 |
|---|---|---|
| ① | 기존 분석 실행 | `1 Worker·결과 모두 확인 / 2 Worker 시작·실패 / 3 활성화·큐만 성공 / 4 기록 없음 / 5 미확인` |
| ② | 기존 CODE_FACTS/MSC | `1 둘 다 존재·내용 확인 / 2 일부 존재 / 3 없음 입증 / 4 미확인` |
| ③ | Registry/Bootstrap 누락 | `1 설계상 정상 / 2 실제 결함·수정 완료 / 3 결함·미수정 / 4 미확인` |
| ④ | Run ID 누락 | `1 원인 확정·대체 증거 연결 / 2 결함 수정·실증 / 3 미해결 / 4 설계상 비필수` |
| ⑤ | RESULT_UNSUPPORTED | `1 지원 경로로 조회 해결 / 2 최소 패치 적용·실증 / 3 설계상 미지원·대체 경로 제시 / 4 미해결` |
| ⑥ | MCP 실제 변경 | `1 운영 변경·해시/실행본 확인 / 2 개발 패치·시험만 / 3 수정 불필요 / 4 미적용·승인 대기 / 5 변경 실패` |
| ⑦ | RACH Job 재실행 | `1 승인 범위에서 1회 실행 / 2 재실행 불필요 / 3 승인 대기 / 4 미실행` |
| ⑧ | 최종 복구 | `1 전체 PASS / 2 일부 PASS·잔여 BLOCKED / 3 FAIL / 4 NOT_RUN/UNKNOWN` |

**보고 순서:** 현재 상태 → 최초 실패 지점·근본 원인(FACT/INFERENCE/UNKNOWN) → 수정 대상·실제 diff → 실행한 시험 PASS/FAIL/SKIP/NOT_RUN → 운영 적용 여부 및 승인 경계 → 분석 산출물 실재·검증 → 변경 파일·SHA-256·정확한 로컬 경로·KST 시각 → **다음 한 동작**.

마지막에 다음 키를 그대로 출력하라.

```text
HOST_VERIFIED=<PASS|PARTIAL|FAIL|UNKNOWN>
OPERATIONAL_APPLY=<APPLIED_VERIFIED|NOT_APPLIED|BLOCKED_APPROVAL|NOT_NEEDED>
JOB_EXECUTION=<CONFIRMED|REQUEST_ONLY|FAILED|UNKNOWN>
ANALYSIS_RESULT=<VERIFIED|PARTIAL|MISSING|UNKNOWN>
INDEPENDENT_REVIEW=<PASS|FAIL|NOT_RUN>
DUPLICATE_JOB_EXECUTIONS=<정수 또는 UNKNOWN>
NEXT_ACTION=<정확한 1개 조치>
```

**절대로** 로컬에서 직접 확인하지 못한 내용에 대해 `PASS`, `APPLIED_VERIFIED`, `VERIFIED`를 쓰지 말고, 실제 모델 호출·운영 배포·분석 작업을 수행하지 않았으면서 실행했다고 보고하지 말 것.
