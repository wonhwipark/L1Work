# 사내 MCP Dynamic Gateway·자동복구 E2E 실패 원인 조사 및 복구 — 통합 원샷 지시서

- 버전: **v1.0 / 2026-10-31**
- 실행 주체: **사내 LLM** (사내 저장소/실행 환경 접근 권한 내에서 수행)
- 대상: `whpark-mcp`, `job-list`, `code-analyzer`, `issue-analyzer`, 필요한 경우 `skill-updater` 및 사내 분석 실행기
- 작업 목표: **기존 구현을 재활용하여 Agent에 노출되지 않는 기능을 복구하고, 안전한 자동복구를 실제로 동작·검증할 수 있는 상태로 만든다.** 단순 재진단이나 새 설계서 제출로 종료하지 말 것.
- 입력 길이 제한 없음. **이 문서 하나만으로 수행**하고, 존재하지 않는 첨부파일/과거 대화/임의의 외부 자료를 선행조건으로 요구하지 말 것.

## 0. 사용자 보고 및 정확한 해석

사내 LLM이 이전 통합 개발 요청을 완료했다고 보고한 뒤 Agent E2E 시험 결과는 다음과 같았다.

```text
2 3 3 2 1 3 3
```

시험 코드: `1=PASS`, `2=FAIL`, `3=미구현`, `4=검증불가`.

| 항목 | Agent 보고 | 반드시 확인할 사항 |
| --- | --- | --- |
| T1. MCP 신규 Gateway 기능 등록 | FAIL | 소스 구현 여부, 설치된 실행본, 실제 등록 도구 목록 및 Agent 세션 도구 노출이 일치하는가? |
| T2. 분석기 기능 탐색 | 미구현 | **소스 미구현인지, 등록·노출 누락인지** 분리할 것 |
| T3. 분석 요청→실행→결과 조회 | 미구현 | 호출 계약, 승인된 실행 profile, 결과 producer/reader 연결을 구간별로 추적할 것 |
| T4. 기존 SDM Job 결과 조회 | FAIL | `RESULT_UNSUPPORTED`의 정확한 발생 계층과 로컬 실제 결과 상태 |
| T5. Preflight | PASS | 어떤 검사 범위를 실제 통과했는지 증거 확보; 전체 환경 정상으로 확대 해석 금지 |
| T6. 장애 진단→자동복구→재검증 | 미구현 | 플레이북 자체 부재, 비활성, 권한 차단, MCP 미노출 중 무엇인지 구분 |
| T7. 복구 실패 중단·롤백·중복 실행 방지 | 미구현 | 격리 장애 주입 테스트 존재·통과 여부 구분 |

**핵심 주의:** Agent가 `미구현`이라고 답해도 실제 소스가 비어 있다는 증거는 아니다. 소스→설치→런타임→MCP 등록→Agent 노출 중 끊긴 지점을 먼저 확인한다. 테스트하지 못한 항목은 PASS로 올리지 않는다.

기존 SDM 원샷 식별자: `JOB-20261031-MCP-SDM-PARSER-READ-STAGE-01`.
이전 관찰: queue `DONE`, worker receipt `SUCCESS`, Agent `job_result_read`는 `RESULT_UNSUPPORTED`, semantic result는 `UNKNOWN`. 이 조합은 실제 SDM 조사·수정 성공을 입증하지 않는다.

버전 참고: 설치 보고 기준 `job-list v0.4.26`, `skill-updater v0.5.44`. 실제 설치 파일·코드·런타임의 버전과 해시는 사내에서 다시 확인해야 한다. **버전 숫자만으로 코드 동일성을 추정하지 말 것.**

## 1. 이번 원샷의 성공 정의

1. **원인 규명:** T1~T7 각각을 `소스 코드 누락 / 빌드·설치 누락 / MCP 등록·배선 누락 / 권한·환경·입력 문제 / 런타임 실행 오류 / 검증 경로 부재`로 분류하고, 실제 함수·설정·실행본 근거에 연결한다.
2. **복구:** 허용된 범위의 수정은 **조사만 하지 말고 직접 구현·테스트**한다. 새 구조를 무조건 재작성하지 않고 기존 구현을 활용한다.
3. **연동:** 사내에 설치된 MCP 실행본이 새 기능을 실제 등록·호출하도록 연결한다. 운영 변경 승인이 필요하면 **격리·스테이징에서 구현·시험까지 진행**하고 실제 적용은 승인 대기로 둔다.
4. **자동복구:** 적어도 재현 가능한 분석기 장애 한 건에 대해 `진단→허용된 조치→원래 요청 재검증→성공/안전 중단`을 코드와 테스트로 확인한다.
5. **최종 검증:** 기능별 소스/단위테스트/설치/등록/MCP 직접 호출/Agent 실제 호출을 별도 상태로 기록한다. **Agent에서 실제 보이지 않는데 E2E PASS로 보고하면 실패**다.
6. **호환·보존:** 기존 MCP, 세 기존 Job 결과, 신규 SDM Job 기록, queue/receipt, 스킬 호출 계약과 정기 Updater 경로를 보존한다.

## 2. 수행 절차 — S0부터 S6까지 중단 없이 진행

### S0 — 운영 대상 및 실행 경로 확보 (READ-ONLY)

- 실제 개발 저장소 기준 경로, HEAD/branch/dirty state, 배포/설치본의 버전·해시·경로, 실행 중 MCP 프로세스가 로드한 모듈·설정, 활성 서비스/실행 엔트리를 확인한다.
- MCP 서버 소스에서 tool 정의, handler, 등록 루틴, authz, 결과 reader, capability registry를 찾아 호출 흐름을 그린다.
- **소스에 구현됨 → 설치본 포함 → 서버에서 등록됨 → 도구 목록에 나타남 → Agent에 노출됨**의 5단계에서 최초 단절 지점을 결정한다. 실제 Agent 측 목록을 읽을 수 없으면 `검증불가`라고 기록한다.
- `code-analyzer`, `issue-analyzer` 설치/설정/runner/analysis result의 실제 contract를 확인한다. 경로·명령·시크릿을 외부로 출력하지 않는다.
- 소스나 런타임 자체에 접근 실패 시, 가능한 범위의 로컬 조사·테스트를 먼저 끝내고 정확한 차단 원인 1개를 보고한다. 임의 경로 추정 금지.

### S1 — SDM Job 결과 조회 복구 (우선순위 P0)

- `JOB-20261031-MCP-SDM-PARSER-READ-STAGE-01`의 로컬 canonical result reader를 **읽기 전용**으로 호출해 실제 semantic 상태(`SUCCESS/BLOCKED/FAILED/REVIEW_PENDING/NOT_FOUND/UNKNOWN`)를 조회한다.
- `RESULT_UNSUPPORTED` 발생 위치를 Agent-facing MCP wrapper의 고정 allowlist, 런타임 registry, 연결된 이전 backend, 결과 producer schema 또는 authz 중 실제 근거로 판별한다.
- 로컬 결과가 존재하는 경우 허용된 읽기 계약을 **최소 수정**하여 동일 Job ID를 MCP에서 조회 가능하게 만든다. 신규 Job마다 ID 하드코딩을 늘리는 대신, 승인된 manifest 기반의 공통 reader adapter를 우선한다.
- 결과가 `BLOCKED` 또는 `NOT_FOUND`이면 내용을 성공으로 바꾸거나 Job을 재실행하지 않는다. 대신 실제 차단 코드와 다음 조치를 조회 가능하도록 한다.
- 기존 Job 3개 조회, 지원하지 않는 ID 거부, ID·Run ID 혼동 거부, path traversal/symlink 및 민감정보 노출 차단 회귀 테스트.

### S2 — Gateway 등록·동적 기능 탐색 복구 (우선순위 P0)

- 이미 작성된 Gateway 소스와 실제 서버 tool 등록 기능을 대조하고, 빠진 handler/export/manifest loading/설치 package 포함/실행 프로세스 binding을 완성한다.
- 승인된 skill/job manifest를 사내에서 검사하여 `capability_id`, 설치 버전, 권한, profile, 입력·결과 schema, reader, 의존성, 상태를 연결한다.
- 외부에 노출되는 MCP 메서드는 **소수의 공통 인터페이스**로 유지한다. 새로 승인한 capability는 MCP 소스의 Job-ID 목록 수정을 반복하지 않아도 탐색·결과 조회 가능해야 한다.
- 소스에 미구현된 API는 필요 범위만 구현하고, 구현되어 있으나 서버에 등록되지 않은 경우 등록·설치·버전 정합성만 수정한다.
- 기존 MCP 도구와 하위호환, 명시적 승인 없는 기능의 검색·실행 거부, 입력 schema 오류·권한 거부 시험.

### S3 — 분석 실행·진단 경로 복구 (우선순위 P1)

- `code-analyzer` 및 `issue-analyzer` 각각에 대해 `capability discovery → preflight → approved analysis submit → queue/run correlation → semantic result → MCP result` 구간을 개별 추적한다.
- 기존 승인된 실행 profile을 활용한다. 신설 공통 API 이름은 실제 서버 구조와 호환되도록 결정하며 새 분석 Job 임의 생성/중복 실행 금지.
- 사내 fixture 또는 기존 저장된 분석 결과를 우선 사용하여 MCP E2E를 구성한다. **실제 운영 코드/로그를 대상으로 하는 분석 재실행은 별도 승인·환경 검사를 거친다.**
- source mapping, runner, runtime, timeout, 결과 누락, schema mismatch, 권한 오류를 서로 구분한 stable error code 반환.
- T5 Preflight 통과는 다시 확인하고, enqueue 전에 결과 조회 가능성·소스 매핑·권한·실행기를 검사하도록 연결한다. 미준비 시 무해한 `BLOCKED` 반환, 신규 큐 등록 없음.

### S4 — 자동 진단 및 안전한 자동복구 실제 구현 (우선순위 P1)

1. 장애마다 `incident_id`, `failure_stage`, `reason_code`, `evidence`, `proposed_playbook_id`, `approval_requirement`를 기록한다.
2. 사전에 등록·승인한 playbook만 선택하고, `preconditions`, `allowed error codes`, `max_attempts(기본 1)`, `timeout`, `idempotency key`, `undo plan`, `verify probe`를 확인한다.
3. **AUTO_SAFE:** read-only 조회 재시도, 제한된 일시 오류의 bounded retry, 승인된 캐시/상태 동기화 등 *무해성과 복원성 검증을 통과한 조치*만 자동 수행한다.
4. **STAGE_ONLY:** 코드·설정 수정이 필요한 경우 격리 작업공간에서 실제 수정안 작성→단위·통합 테스트→diff 및 rollback 근거 생성까지 수행한다. 단순 권고안만 나열하고 종료하지 않는다.
5. **APPROVAL_REQUIRED:** 운영 MCP 배포·재시작, 실제 소스/권한/매핑 변경, 설치·업데이트, Git push/merge, 운영 데이터 변경 또는 기존 Job 재실행. 사내 규정상 명시 승인된 경우에만 반영한다. 자동 승인·우회 금지.
6. 동일 오류 재발 시 무한 재시도 금지. 실패한 복구는 원본 상태 확인→안전한 롤백(가능한 범위)→재검증→`BLOCKED/REVIEW_REQUIRED` 종료.
7. 모든 자동복구는 **원래 실패했던 요청과 같은 입력·스킬·source revision 조건**으로 재검증한다. 변경을 의도한 revision은 명시하고 비교한다.

자동복구 검증 사례: (a) 일시적인 결과 조회 오류는 제한된 재조회로 회복, (b) 기존 분석기 호출 계약 누락은 격리 스테이지에서 패치·검증, (c) source mapping 부재는 임의 경로 생성하지 않고 조치 필요로 종료, (d) 허용되지 않은 권한·명령·결과 파일 접근 요청은 거부.

### S5 — 테스트·실행본 정합성·실제 MCP 호출 확인

- 정상 경로: T1~T7 관련 단위/통합 fixture, 두 분석기 탐색 및 결과 조회, 고정 SDM Job 결과 조회, preflight 통과, 안전한 복구 후 동일 요청 재검증.
- 반례: 미등록 capability, 잘못된 role, schema/버전 불일치, 미존재 reader, idempotency 중복, 기존 Job 재실행 시도, 무한 복구, 실패 시 롤백, 비밀/경로 유출, 임의 shell·prompt·filesystem 입력.
- **스테이징 MCP 프로세스**에서 tools/list 혹은 실제 서버가 제공하는 동등한 기능 목록 조회, 신규 handler 호출, 기존 handler 호환성, 설치본 로드 버전 비교를 실시한다.
- 운영 서버 적용에 승인 권한이 있으면 정상 승인 절차로 반영하고, 운영 노출 도구 목록을 다시 확인한다. 승인 없으면 운영 적용을 시도하지 않는다.
- 외부 Agent를 직접 호출할 수 없는 환경이면 `LOCAL_MCP_PASS / AGENT_NOT_VERIFIED`를 명확히 분리한다. 모의 테스트만으로 Agent E2E PASS 금지.
- 각 단계 실제 실행 테스트 수·PASS/FAIL·SKIP 이유를 사내 결과 파일에 기록한다.

### S6 — 사후 점검·원인 재발 방지

- 신규 승인 Job 등록 시 `manifest ↔ 설치 backend ↔ MCP handler/reader ↔ Agent 노출 계약`의 자동 정합성 검사를 도입한다. 기존 스킬·Job의 등록·결과 조회가 회귀하지 않아야 한다.
- 설치/배포 직후 등록 기능 검증을 표준 gate로 만들고, 소스 변경만 되고 운영 실행본이 갱신되지 않으면 `NOT_DEPLOYED`로 종료.
- 부분 실패 복구/rollback, 타임아웃 및 중복 요청에 대한 audit와 관리자 확인 경로를 제공한다.
- 하나의 원샷 작업 안에서 진단→격리 수정→테스트→승인 가능한 조치까지 최대한 완료하고, 정말 필요한 승인 또는 환경 정보만 사용자에게 요청한다.

## 3. 변경·복구 권한과 안전장치

| 등급 | 수행 여부 | 예 |
| --- | --- | --- |
| READ_ONLY | 자동 수행 | 소스·설치본·tool registry·결과·상태 조회 |
| AUTO_SAFE | playbook 사전 승인·검증된 경우 수행 | 제한된 read retry, 안전성 검증된 캐시 정합성 회복 |
| STAGE_ONLY | 격리 실행 허용 시 수행 | MCP adapter/registry/분석기 adapter 코드 수정안 작성, 테스트, 롤백 후보 |
| APPROVAL_REQUIRED | 명시된 조직 승인 없이는 미적용 | 운영 소스 변경, 서비스 재시작, 신규 설치, 권한 변경, 실제 기존 Job 재실행 |
| DENY | 항상 차단 | 무제한 원격 shell, 임의 경로/명령 실행, 민감 원문 외부 출력, 불명확한 쓰기, 조치 무한루프 |

- 거절되거나 불가능한 수정을 `완료`로 보고하지 않는다. 기존 소스 dirty 상태, 동시 변경, 브랜치/업스트림 기준 불명확하면 무단 덮어쓰기나 자동 commit 금지.
- 변경 최소화. 기존 `job-list v0.4.26` / `skill-updater v0.5.44` 동작 보존을 기본으로 하고, 수정이 필요한 경우에만 근거를 제시한다.
- 스킬별 진단/복구 코드를 공통 MCP에 통째로 복사하지 말고, 승인된 skill-specific adapter/playbook으로 분리한다.

## 4. 반드시 남길 내부 산출물 및 판정 기준

사내에만 저장하고, 사용자에게는 민감정보가 없는 요약만 반환한다.

- `baseline`: 소스·설치·실행 버전과 해시(사내 보관)
- `failure_matrix`: T1~T7 최초 실패 계층, 정확한 root cause, 코드/설치/등록/권한 구분
- `change_manifest`: 수정 파일·변경 범위, 영향 받은 API, stage/운영 반영 구분
- `test_report`: 수행한 테스트·PASS/FAIL/SKIP·근거·안전 반례 결과
- `recovery_report`: 실제 실행 playbook, 실행 횟수, 변경 전후 상태, 롤백/재검증 결과
- `runtime_evidence`: 실행 프로세스가 로드한 버전, 등록 도구 목록, 사내 MCP 직접 E2E, Agent 측 E2E(확인 가능한 경우)
- `blockers`: 미승인·미확인 사항과 **최소 필요한 다음 한 동작**

### T1~T7 최종 PASS 조건

| 항목 | PASS 조건 (다른 단계 통과로 대체하지 말 것) |
| --- | --- |
| T1 | 실제 대상 MCP 런타임에서 신규 Gateway 기능이 등록되고 허가된 도구 목록에 보임 |
| T2 | 두 분석기의 승인된 capability 검색 결과가 해당 설치·권한·버전과 일치 |
| T3 | 승인된 fixture의 분석 요청이 실제 backend 경로로 처리되고 semantic 결과를 MCP에서 읽음 |
| T4 | 기존 SDM Job ID가 Agent 조회에서 `RESULT_UNSUPPORTED` 없이 실제 semantic 상태 또는 정당한 `BLOCKED/NOT_FOUND`를 반환 |
| T5 | 소스 맵·버전·권한·reader가 누락된 fixture에서 enqueue 전 `BLOCKED`, 정상 fixture에서 PASS |
| T6 | 승인된 장애 fixture에 대해 진단→자동복구→동일 요청 재검증이 실제 코드와 테스트로 확인됨 |
| T7 | 실패 시 rollback/중단, 재요청 idempotency, 무한 retry 금지를 실제 장애 주입 테스트로 확인 |

**진짜 Agent E2E:** 실제 Agent 도구 호출까지 확인해야 한다. 내부 테스트만 통과한 경우 `4=검증불가`로 보고하되, 내부 스테이징 단계의 통과 여부는 별도 내부 산출물에 기록한다.

## 5. 사내 LLM 수행 요청(이 문서 자체가 실행 요청)

> **S0~S6을 순서대로 수행하라. 이번 목표는 원인 보고만이 아니라 승인된 범위 내에서 실제 복구·테스트까지 완료하는 것이다.** T1·T4를 P0로 우선 복구하되, S2~S5에서 T2·T3·T6·T7의 소스 구현·등록 누락을 실제로 보강한다. 작업 중 진행 가능한 부분은 승인 요청 때문에 불필요하게 중단하지 말고 스테이징으로 완료한다. 운영 반영·재시작은 별도 승인 없이는 금지한다. 이미 운영 적용이 승인되었다는 검증 가능한 근거가 있을 때만 그 범위에서 수행한다. 기존 Job/Updater를 반복 실행하지 않는다. 실제 Agent 호출 근거가 없으면 PASS 판정하지 않는다.**

### 최종 사용자 보고: 7개 숫자 + 1개 원인 코드 + 2줄

T1~T7은 **반드시 아래 한 가지 기준**만 사용한다.

- `1` = PASS: 해당 항목의 실제 Agent 경로까지 검증 완료
- `2` = FAIL: 필요한 기능이 실행·등록됐으나 실제 동작 검증 실패
- `3` = 미구현: 실제 코드/배포 대상에서 필요한 기능이 없다는 직접 근거 확보
- `4` = 검증불가: 적용 미승인, 런타임/Agent 경로 접근 불가, 또는 상태가 불명확하여 E2E 확정 불가

원인 분류(최상위): `1=코드 누락`, `2=설치·실행본 누락`, `3=MCP 등록·도구 노출 누락`, `4=복합`, `5=미확인`.

```text
E2E: T1 T2 T3 T4 T5 T6 T7 = 4 4 4 4 4 4 4
ROOT_CAUSE: 5
BLOCKER: [한 줄, 없으면 NONE]
NEXT: [한 줄, 가장 작은 다음 조치]
```

위 숫자는 **출력 형식 예시**일 뿐 실제 결과가 아니다. 내부 산출물에는 세부 stage 결과, 실제 테스트 횟수, 최초 실패 코드·복구 시도·검증 근거를 남길 것. 사용자에게는 원본 소스·절대 경로·토큰·패치·내부 실행 로그를 출력하지 않는다.
