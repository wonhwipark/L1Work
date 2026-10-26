# 사내 LLM 작업 지시 — whpark-mcp 자연어 검색 수정 및 결과 확인 완결

기준일: 2026-10-26 KST  
기반: job-list v0.4.25 / 기존 skill-updater v0.5.43  
최근 사용자 보고: `1 3 1 2 1`  
사용법: 이 문서 전체를 사내 whpark-mcp 소스와 승인된 개발 환경에 접근할 수 있는 LLM에게 전달한다.

> **v1.1 보완:** 이 지시서의 구현 범위는 `whpark-mcp`의 자연어 검색·기존 근거 READ 및 필요한 Job 상태 조회이다. `l1-fix-workflow` v1.6.50 / `work-ledger-kernel` v0.7.28의 **수정논의 Draft·원장 승인·문서 렌더를 MCP에 신규 연동하는 작업은 별도 범위**이며, 이 프롬프트를 실행했다고 완료 판정하지 않는다. 실환경에서 기존 기능이 있으면 재사용하되 확인되지 않은 Provider나 도구를 만들었다고 주장하지 않는다.

## 1. 무엇을 해결해야 하는가

최종 사용자 목표는 **사외에서 자연어로 사내 코드 분석·수정을 요청하고, MCP를 통해 관련 근거와 실행 결과를 확인하는 것**이다.

이번 수정의 주목적은 **whpark-mcp의 `analysis find`가 SOC 식별자 단독 검색은 처리하지만, 같은 식별자가 포함된 자연어 질문에서는 관련 자료를 찾지 못하는 문제를 해결하는 것**이다.

기존에 보고된 재현 사례는 다음과 같다.

| 입력 | 과거 관측 | 이번 수정에서 확인할 동작 |
| --- | --- | --- |
| `analysis find SOC-420517` | 3건: RUN 2, WORK 1 | 기존 식별자 검색 동작 유지 |
| `analysis find SOC-420517의 main_dac_path와 tx_dac_path가 다른 이유는?` | 0건 | SOC 범위를 식별하고 두 심볼에 관한 관련 자료·근거 조회로 연결 |
| `analysis find main_dac_path와 tx_dac_path가 다른 이유는?` | 0건, linkage unlinked | 명시적으로 전달된 유효 범위가 있으면 그 안에서 검색. 범위가 없으면 필요한 범위를 명확히 요청 |

`3건`은 과거 데이터에 대한 관측이다. 운영 데이터의 현재 건수를 3으로 고정하거나 결과를 하드코딩하지 마라. 같은 테스트 데이터·권한·시점에서 SOC 단독 질의와 SOC 포함 문장이 같은 SOC 범위를 해석하는지 검증하라.

Job-list의 카탈로그·큐·결과 조회는 이 수정 작업의 실행 상태와 패치를 확인하기 위한 지원 기능이다. **Job 조회가 가능해졌다는 이유로 자연어 검색 문제까지 해결됐다고 보고하지 마라.** 새 Job-list 버전 제작이나 Updater 교체를 기본 해결책으로 삼지 마라.

설계 설명으로 끝내지 말고, 승인된 개발 작업공간에서 재현 → 원인 확정 → 최소 코드 수정 → 테스트 → 검토 가능한 패치와 반영 계획까지 진행하라. 운영 반영 권한이 이미 구체적으로 주어졌다면 그 범위에서 적용과 검증까지 이어가라.

## 2. 현재 상태를 정확하게 이어받기

최근 숫자 보고는 이전 검증 프롬프트의 **설치 / 예약호출 / 대상큐 / 대상결과 / 원격조회** 순서다.

| 항목 | 보고값 | 해석과 한계 |
| --- | ---: | --- |
| 설치 | 1 | 설치 단계의 직접 근거를 확인했다는 사용자 보고 |
| 예약호출 | 3 | 예약 활성화 근거 부족 또는 미확인. 예약 실행 실패로 단정하지 않음 |
| 대상큐 | 1 | 대상의 PENDING/RUNNING 또는 종료 receipt 근거를 확인했다는 보고. 정확한 상태는 숫자만으로 알 수 없음 |
| 대상결과 | 2 | 불일치·실패·미완료 근거를 확인했다는 보고. REVIEW_PENDING도 이 값에 포함 |
| 원격조회 | 1 | 승인된 응답으로 특정 Job의 실제 상태를 읽었다는 보고. 모든 READ 도구 또는 새 패치의 운영 반영까지 증명하지 않음 |

숫자의 의미는 `1=해당 단계 직접 근거 확인`, `2=불일치·실패·미완료 근거 확인`, `3=미확인`, `4=도구 미노출·권한 차단`이다.

현재 인계에는 Agent의 상세 `STATE/EVIDENCE/BLOCKER/NEXT` 값이 없다. 따라서 `대상결과=2`를 곧바로 `REVIEW_PENDING`, 실행 실패 또는 패치 부재로 확정하지 마라. 승인된 사내 근거를 읽어 구분하라. 과거의 “원격 조회 도구가 전혀 없다”는 진단도 현재 사실로 그대로 재사용하지 마라.

이 숫자 보고의 주 대상은 **MCP READ Stage Job**이다. 원래 검색 수정 Job과 다르다.

| 역할 | 고정 Job ID |
| --- | --- |
| 최신 숫자 보고의 주 대상 / MCP READ Stage | `JOB-20261024-MCP-JOB-READ-STAGE-01` |
| 원래 자연어 검색 수정 제안 / 보존 대상 | `JOB-20261024-MCP-ANALYSIS-FIND-PROPOSAL-01` |
| 기존 Workspace Migration / 보존 대상 | `JOB-20261021-L1-WORKSPACE-ARTIFACTS-MIGRATE-01` |

`requests/preserved`에 선언이 있다는 것과 활성 큐에 등록됐다는 것은 다르다. 위 ID를 바꾸거나 새 ID로 복제해서 기존 실행·승인 이력을 우회하지 마라.

## 3. 작업 권한과 진행 방식

- 실제 저장소의 작업 지침과 기존 승인된 사내 소스 매핑을 먼저 확인하라. **Worktree는 사용하지 않는다.** 운영 중인 파일을 바로 덮어쓰지 않고 기존 저장소의 안전한 개발 브랜치(미커밋 변경 충돌 확인 후 전환) 또는 승인된 격리 복사본에서 수정하라. 사용자 변경 사항을 자동 stash/reset/clean하지 마라.
- 조회, 원인 분석, 개발 코드 수정, 테스트, 패치 작성은 중간 확인 질문을 반복하지 말고 진행하라. 환경에서 직접 확인할 수 있는 버전·경로·상태를 사용자에게 다시 조사해 달라고 하지 마라.
- 기존 Stage 산출물이 있으면 읽고 재사용 가능성을 확인하라. 오래된 패치를 검토 없이 적용하거나, 산출물을 얻기 위해 완료된 one-shot Job을 재실행하지 마라.
- 운영 반영은 기존 인계의 **패치 단위 승인** 조건을 따른다. 승인 대상 패치 SHA256·대상 revision·재시작·롤백 범위가 이미 확인되면 재승인을 요구하지 마라. 승인이 없다면 구현과 테스트 및 구체적인 반영안을 완성한 뒤 필요한 승인만 한 번에 제시하라.
- 이 문서는 기존 Stage 전용 자동 실행기의 권한을 변경하지 않는다. Stage 실행기는 계속 제안 생성까지만 수행한다. 별도 Apply Job은 v0.4.25에 포함돼 있지 않다. 사내의 기존 승인된 배포 방식이 있으면 이를 사용하고, Apply Job이 있는 척하지 마라.
- 기존 Job, queue, running marker, receipt, Work/Run/Analysis/Evidence 원본과 무관한 사용자 변경을 보존하라. 강제 완료·취소·큐 삭제·재정렬·Job 재등록·일반 Updater 반복 실행을 하지 마라.

## 4. 한 번의 조사로 작업 근거 확보

다음 정보를 가능한 범위에서 모아 짧은 사실표를 만든 뒤 바로 구현으로 넘어가라. 한 항목이 막혀도 독립적으로 가능한 검색 코드 수정과 테스트는 계속하라.

1. **현재 코드**: 실제 whpark-mcp 저장소, 개발 기준 revision, 운영 revision 식별 방식, 사용 중인 MCP 등록·라우팅 구조, 테스트 명령.
2. **검색 경로**: Agent 입력 → 실제 MCP tool 인자 → 라우터/파서 → query 정규화 → SOC/Work/Run 범위 결정 → 검색 → Analysis/Evidence 연결 → 응답 직렬화.
3. **기존 제안**: 자연어 검색 Stage와 MCP READ Stage 각각의 semantic result, terminal receipt, proposal.patch 존재 및 SHA256, 제안이 만들어진 기준 소스와 현재 소스의 차이.
4. **현재 READ 경로**: 실제 노출 도구와 응답을 확인하여 이미 가능한 조회는 유지하고 빠진 정보만 특정.
5. **예약 근거**: 기존 예약 기록을 읽을 수 있는지, v0.4.25 이후 기록인지, 일반 Updater 실행과 구별되는지 확인. 예약 기록이 없다는 이유만으로 현재 Job 결과까지 무효로 취급하지 않음.

사내에서 참고할 v0.4.25 파일은 다음과 같다. 설치 루트는 기존 승인 설정에서 얻고 아래 상대경로를 결합하라. 사외 요청이 임의 루트를 선택하게 하지 마라.

| 목적 | 패키지 상대경로 |
| --- | --- |
| v25 전달 계약 | `docs/MCP_BOOTSTRAP_STATUS_v0425.md` |
| READ 계약 | `scripts/mcp_job_read_bridge.py` |
| 압축 상태 요약 | `scripts/job_bootstrap_status.py` |
| CLI 진입점 | `bin/job-list-core.py` |
| 검색 Stage 결과 | `output/mcp_analysis_find/stage_fix/latest_result.json` |
| READ Stage 결과 | `output/mcp_job_read/stage/latest_result.json` |
| 검색 Stage 제안 | `output/mcp_analysis_find/stage_fix/runs/<검증된 run_id>/proposal.patch` |
| READ Stage 제안 | `output/mcp_job_read/stage/runs/<검증된 run_id>/proposal.patch` |

결과 JSON의 임의 파일 경로를 그대로 따라가지 마라. 허용된 출력 트리와 검증된 ID로 경로를 구성하라. 패치가 없거나 현재 소스에 맞지 않으면 그 사실을 기록하고 승인된 개발 소스에서 수정안을 작성하라.

### 대상결과=2 처리

| 실제 근거 | 조치 |
| --- | --- |
| PENDING/RUNNING | 기존 실행을 보존하고 관찰 시각 기록. 같은 Job 재등록 금지. 코드 조사·독립 테스트는 계속 |
| receipt SUCCESS + result REVIEW_PENDING | 해당 Job의 패치를 검토·검증. 운영 적용 완료로 표시하지 않음 |
| BLOCKED/FAILED | 실제 error_code와 원인 파일·설정 근거 확보. 필요한 수정만 수행하고 재실행 권한과 이력은 별도 보존 |
| receipt SUCCESS + semantic result 없음 | `RESULT_EVIDENCE_REQUIRED`. 성공을 채우거나 receipt를 고치지 않음 |
| 손상·권한 차단·상태 충돌 | 원인별 조회 오류로 보고. `JOB_NOT_FOUND`로 바꾸지 않음 |

## 4.1 사내 MCP 구현 계약 — 검색 성공과 문제 답변을 구별 [v1.1 보완]

아래 검증을 **코드 수정 전 1회** 수행하고, 소스에서 찾은 구체 tool/function 이름으로 수정 대상을 확정한다. 실제 함수명·스키마는 임의로 만들지 않는다.

1. **호출 계약:** 외부 Agent 입력 → MCP `tools/list` 등록 도구 → 실제 `tools/call` 이름과 인자 JSON → 라우터/파서/검색 함수 → 응답 스키마를 추적한다. `analysis find`가 명령 텍스트인지 실제 action인지 구별한다. Tool 입력이 질문을 손실 없이 전달하는지 확인한다.
2. **검색 범위:** `scope_id`, 남은 질문, 심볼 목록을 내부적으로 분리한다. SOC 검색 결과 존재 여부(`scope_found`)와 질문에 답할 근거 충족 여부(`answer_evidence`)를 별개로 판정한다. 새 응답 필드를 추가하려면 기존 호출자 호환성과 정보 노출 정책을 먼저 확인한다.
3. **근거 추적:** 반환된 WORK/RUN/ANALYSIS/EVIDENCE 참조에서 **실제로 등록·노출된 READ 도구로 이어질 수 있는지** 검증한다. 참조가 있더라도 READ 권한이 없으면 근거 확인 완료로 표시하지 않는다. 관련 문서에 근거가 없으면 `SCOPE_FOUND_EVIDENCE_INSUFFICIENT` 같은 상태를 *기존 응답 스키마와 호환되는 방식*으로 표현한다. 이 값은 제안 명칭이지 현행 서버에 존재한다고 가정하지 않는다.
4. **안전 경계:** MCP READ 호출로 사내 코드 수정이나 원장 기록을 수행하지 않는다. 소스 패치는 승인된 로컬 개발 환경에서만 작성하고, 배포·서비스 재시작은 기존 승인 정책을 따른다. Agent가 전달한 임의 path/command/env/tool 이름으로 외부 명령을 실행하지 않는다.
5. **검증 가능한 예시:** `analysis find SOC-420517`와 `analysis find SOC-420517의 main_dac_path와 tx_dac_path가 다른 이유는?`는 동일 권한·데이터에서 같은 SOC 범위를 인식해야 한다. 단, 심볼 원인에 대한 증거가 없는 경우 **검색 범위 성공 + 근거 부족**을 함께 반환해야 하며 원인 답변을 만들어내면 실패다.

완료 판정은 세 수준으로 구분한다.

| 수준 | 충족 조건 | 미충족 시 |
| --- | --- | --- |
| A. 개발 수정 | 원인 파일/함수 확인, 수정 diff/패치, 관련 자동 테스트 통과 | `DEV_NOT_VERIFIED` |
| B. MCP 통합 | 실제 서버 등록 도구가 새로운 입력을 수신하고 허용된 참조/후속 READ를 반환 | `MCP_E2E_NOT_VERIFIED` |
| C. 운영/사외 검증 | 승인된 패치 적용, 서비스 재시작 필요 시 정상 확인, 사외 Agent에서 실제 요청 E2E 통과 | `REMOTE_E2E_NOT_VERIFIED` |

**A만 PASS여도 B·C를 PASS로 간주하지 마라.** 작업 중 하나가 막혀도 가능한 부분의 소스 수정·테스트·패치와 미검증 보고는 끝까지 수행한다.

## 5. 핵심 구현 — analysis find 자연어 처리

### 5.1 먼저 실패를 재현하고 실제 원인을 확정

동일 데이터와 권한으로 SOC 단독 질의와 SOC 포함 문장을 비교하는 실패 테스트부터 만든다. 실제 tool 인자에 이미 질문이 잘려 들어오는지, MCP 내부 정규화에서 잃는지, 검색 조건에서 문장 전체를 식별자로 쓰는지, 링크 조회에서 누락되는지 각각 구분하라.

과거에 제기된 “SOC 추출 누락”, “문자열 전체 일치”, “Work–Run–Evidence 연결 누락”은 가설이다. 실제 파일·함수·조건문과 재현 테스트로 확인한 원인만 확정으로 기록하라. 이미 수정된 경로는 재작성하지 말고 남은 실패 지점에 집중하라.

### 5.2 식별자·질문·검색 범위를 분리

- 문장 속 유효한 SOC 식별자를 기존 식별자 규칙에 맞춰 추출한다. `SOC-420517의`처럼 한국어 조사가 붙은 사례를 처리한다.
- 기존 규칙이 허용하는 대소문자·공백·유니코드 정규화 범위를 명시한다. 숫자를 붙이거나 잘못된 ID를 임의 보정하지 않는다. `SOC-420517`이 `SOC-4205170`과 일치하지 않도록 경계를 검증한다.
- 추출한 SOC는 검색 범위를 결정한다. 나머지 질문과 `main_dac_path`, `tx_dac_path` 같은 심볼은 관련 근거를 선택하는 정보로 보존한다. 질문 전체를 단일 정확일치 검색 키로 사용하지 않는다.
- SOC 단독 조회의 기존 동작과 응답 호환성을 유지한다. 문장 검색에서 심볼 관련 근거가 부족해도 이미 찾은 SOC 범위의 레코드가 사라져 `0건`으로만 반환되지 않게 한다. 범위 검색 결과와 질문에 답할 근거의 충족 여부를 구분한다.
- 복수 SOC나 명시적 scope와 SOC의 충돌은 기존 계약에 맞게 명시적으로 처리한다. 임의로 첫 SOC를 선택하거나 권한 범위를 넓히지 않는다.
- SOC 없는 문장은 요청에 전달된 유효한 Work/Run/Analysis 등 명시적 scope가 있을 때만 해당 범위에서 검색한다. 확인되지 않은 이전 대화 내용을 서버의 암묵적 범위로 사용하지 않는다.
- 범위가 없거나 모호하면 기존 응답 체계에 맞는 범위 확인 상태를 반환한다. 이 문서에서 예시로 사용하는 `SCOPE_REQUIRED` 같은 새 코드는 구현 제안이며 현재 서버에 이미 있다고 가정하지 않는다.
- 단순 식별자·범위 처리를 위해 새 LLM 호출, 임베딩 DB, 광역 검색 시스템을 먼저 도입하지 않는다. 현재 구조에서 재현된 결함을 해결하는 최소 변경을 우선한다.

### 5.3 Work·Run·Analysis·Evidence 연결과 근거 반환

실제 데이터 모델에 존재하는 참조 관계를 따라 관련 결과를 찾고 각 단계에 기존 접근 권한을 적용하라. 모든 Work에 Analysis/Evidence가 반드시 존재한다고 가정하거나 없던 연결을 생성하지 마라.

응답에서는 기존 계약을 보존하면서 다음 의미를 구분할 수 있어야 한다.

| 정보 | 의미 |
| --- | --- |
| 정규화된 범위 | 어떤 SOC 또는 명시적 범위로 검색했는가 |
| 관련 항목 | WORK/RUN/ANALYSIS/EVIDENCE 종류와 허용된 참조 ID |
| 연결 상태 | 실제 연결됨, 연결 누락, 범위 모호, 근거 부족 등을 구별 |
| 근거 참조 | 기존 승인된 상세 조회로 이어질 수 있는 참조 |
| 질문 처리 상태 | 관련 근거가 충분한지, 일부만 있는지, 추가 범위가 필요한지 |

MCP의 `analysis find`가 검색 도구라면 답변 생성기를 새로 붙일 필요는 없다. 기존 Agent가 허용된 후속 READ로 근거를 읽고 답변할 수 있는 구조를 완성하라. `main_dac_path`와 `tx_dac_path`가 다른 이유는 실제 근거가 있을 때만 설명하게 하고, 검색 성공만으로 차이의 원인을 만들어내지 마라.

권한 없는 자료의 존재 여부를 알려줄지 여부도 기존 서버 정책을 따른다. 원문 소스, 내부 절대경로, 패치 본문, 토큰, 인증 헤더, 전체 로그를 새 응답 필드로 내보내지 않는다. 외부 응답에는 승인된 요약과 참조만 사용한다.

### 5.4 기존 기능 회귀 방지

기존 `read/lookup/fallback`, Work/Run 직접 조회, 입력 검증, 권한, 결과 개수·크기 상한을 보존하라. `RUN-*` 조회 검증을 완화해서 `JOB-*`를 받도록 만들지 마라. 검색의 no-match를 감추려고 무관한 글로벌 결과를 반환하거나 테스트 기대값만 낮추지 마라.

## 6. 지원 구현 — 필요한 Job 상태 전달만 보완

최근 원격조회=1 보고를 출발점으로 삼아 현재 도구를 먼저 확인한다. 이미 동등한 기능이 있으면 재사용하고, 불완전한 래퍼만 고친다. 이 작업 때문에 핵심 검색 수정을 계속 미루지 마라.

### 6.1 로컬 READ 계약 연결

필요한 경우 기존 MCP 등록 관례에 맞춰 아래 기능을 연결한다. 아래 MCP 이름은 목표 의미이며 실제 서버의 접두사·기존 이름을 따른다. 중복 도구를 만들지 않는다.

| MCP 기능 | 재사용할 로컬 CLI | 경계 |
| --- | --- | --- |
| `job_catalog_read` | `job-catalog-read` | 선택 job_id, 기본 limit 20, 최대 20 |
| `job_queue_read` | `job-queue-read` | 필수 job_id, queue와 receipt를 구분 |
| `job_result_read` | `job-result-read` | 필수 job_id, 실제 semantic result와 proposal SHA256 |
| 상태 요약이 필요한 기존 응답 | `job-bootstrap-status --compact` | v25의 고정 3개 Job만 지원. 별도 도구 신설은 필요할 때만 |

현재 bridge의 `job_id` 문법과 결과 allowlist는 서로 다른 검사다. 결과 READ는 위 3개 ID에 대한 allowlist를 갖는다. `cursor`는 현재 비어 있거나 null인 경우만 지원하며, `max_bytes`는 기본 4096, 512~8192 범위다. 실제 CLI/함수 스키마를 읽고 그대로 연결하라. 미구현 pagination을 지원한다고 광고하지 마라.

MCP 호출자가 root/path/env/command/shell을 지정할 수 없게 한다. 서버 소유의 고정 설치 루트와 검증된 인자만 사용한다. subprocess가 필요하면 shell 문자열을 조합하지 말고 고정 executable과 인자 배열, timeout·출력 상한을 사용한다. 서버 권한 검증은 로컬 allowlist와 별도로 유지한다.

반환값은 허용된 필드·타입·코드만 선별해 직렬화한다. bridge의 artifact_path를 파일 접근 API로 확장하지 말고, 외부 계약상 필요하면 내부에서 검증한 불투명 참조로 대체한다. JSON을 바이트 중간에서 잘라 반환하지 않는다.

`CATALOG_UNREADABLE`, `QUEUE_UNREADABLE`, `RECEIPT_UNREADABLE`, `RESULT_NOT_FOUND`, `RESULT_UNREADABLE`, `RESULT_UNSUPPORTED`, `STATE_CONFLICT`, `INVALID_INPUT`의 의미를 유지한다. 권한 차단과 정상적인 미존재도 구분하되 외부 공개 수준은 기존 정책을 따른다.

### 6.2 예약 근거 전달 공백

현재 Updater v0.5.43의 일반 `run/update`는 Job을 활성화하지 않는다. OS 예약 진입점 `scripts/skill_updater_auto.py`가 `run_job_list_post_update()`를 호출하고 `scheduled_job_result`를 기록한다. 이 동작을 바꾸지 마라.

일반 Updater result와 예약 auto 기록은 별도다. 설치된 Updater의 실제 canonical runtime 경로를 확인해 다음 상대 위치의 예약 기록을 읽는 기존 MCP 래퍼를 보완할 수 있다.

- `skill-updater/data/state/runtime/state/auto_run.json`
- `skill-updater/data/state/runtime/state/history/auto_*.json`

순서는 다음과 같다.

1. 승인된 고정 위치의 예약 기록을 읽고 일반 `run_*` 기록과 분리한다. 최신 기록이 손상됐는데 조용히 과거 성공 기록을 현재 상태로 대체하지 않는다.
2. `scheduled_job_result.stdout_tail`에서 마지막 완전한 `"job_bootstrap_status":` 필드의 JSON 값만 추출한다. 잘린 tail 전체에 JSON 파서를 적용하거나 정규식으로 중첩 JSON 전체를 해석하지 않는다.
3. 필드 위치·한 줄 경계·JSON 종료 경계, `schema=job-list-bootstrap-status/1`, 허용 타입·고정 Job ID·최대 3200 ASCII bytes를 검증한다. 모호한 중복·불완전 JSON·한도 초과는 구조화된 조회 오류로 처리한다.
4. 같은 상위 auto 기록의 run_id와 실행 시각을 별도 메타데이터로 붙인다. 일반 Updater의 최근 run_id나 다른 history 파일에서 가져와 결합하지 않는다.
5. snapshot의 `scheduled_run_id=null`은 정상일 수 있다. 원본 snapshot은 보존하고, wrapper 메타데이터에 실제 상위 기록과의 연결을 표시한다.
6. 현재 READ 결과와 예약 시점 snapshot을 함께 반환하면 `read_source`, `observed_at`, 실행 시각을 각각 표시한다. 오래된 PENDING/RUNNING snapshot을 현재 실행 상태나 프로세스 생존으로 단정하지 않는다.
7. 시간대가 명확한 시각만 KST로 변환하고, 원본에 시간대가 없고 호스트 시간대도 검증되지 않으면 unknown으로 둔다.

원본 Updater는 마지막 20줄/4000자를 캡처한다. tail 안에는 원문 출력이 함께 있을 수 있으므로 **전체 stdout_tail·auto 기록·로그를 외부로 중계하지 않는다.** 검증된 compact 필드와 최소 메타데이터만 반환한다.

기록 없음, 접근 차단, 손상, 설치 전 기록, snapshot 없음은 각각 구별한다. 조회 공백은 MCP의 READ 연결로 해결할 수 있는지 먼저 확인하고, Updater 교체나 예약 강제 실행으로 증거를 만들지 마라.

### 6.3 실행·제안·적용을 서로 구분

- Updater SUCCESS 또는 activation CALLED는 대상 Job 완료가 아니다.
- queue의 PENDING/RUNNING 또는 종료 receipt 존재는 큐 단계의 근거다.
- 실행 중 같은 Job이 queue와 running marker에 함께 있는 것은 v25의 정상 RUNNING 사례다. terminal receipt까지 충돌하면 보수적으로 상태 충돌로 둔다.
- receipt SUCCESS + semantic result REVIEW_PENDING은 검토할 제안 상태다. 실제 patch 존재·SHA256도 확인해야 한다.
- Stage 결과를 운영 적용 뒤 SUCCESS로 덮어쓰지 않는다. 적용한 patch SHA256, 대상 revision, 배포 검증 결과는 별도 배포 근거로 남긴다.
- v25 snapshot의 `remote_read=NOT_VERIFIED`, `mcp_e2e=NOT_TESTED`는 로컬 생산자가 원격 검증을 하지 않았다는 뜻이다. 실제 wrapper/클라이언트 검증을 별도 근거로 기록하고 원본 필드를 임의로 PASS로 바꾸지 않는다.

## 7. 테스트와 인수 기준

실제 MCP 저장소의 테스트 체계를 사용한다. 변경 전 실패 재현, 수정 후 통과, 관련 기존 회귀를 실행하고 명령·결과·미실행 사유를 기록한다. 아래 항목 중 Job wrapper 관련 항목은 해당 경로를 수정했거나 기존 결함이 확인된 범위에 적용한다.

| 구분 | 테스트 | 통과 기준 |
| --- | --- | --- |
| 검색 | SOC 단독 | 기존 authorized 결과·응답 호환 유지 |
| 검색 | SOC + 한국어 조사 + 질문 | 같은 SOC 범위 인식, 문장 전체 일치로 인한 검색 탈락 해소 |
| 검색 | 두 심볼 포함 질문 | 두 심볼 보존, 관련 근거/근거 부족 상태 구분 |
| 검색 | ID 경계·잘못된 ID | 인접 숫자 오매칭·임의 보정 없음 |
| 검색 | SOC 없음 + 유효 scope | 명시적 범위 안에서만 검색 |
| 검색 | SOC 없음 + scope 없음 | 범위 요청 또는 기존 동등 상태, 무관한 전체 검색 없음 |
| 검색 | 복수 SOC·scope 충돌 | 문서화된 모호성 처리, 임의 선택 없음 |
| 검색 | 자료 연결 일부 누락 | 없는 Work/Run/Analysis/Evidence 관계 생성 없음 |
| 검색 | 실제 no-match·fallback | 무관한 결과로 성공을 꾸미지 않음, 기존 fallback 유지 |
| 검색 | 권한이 다른 사용자 | 범위 및 참조마다 기존 권한 적용, 정보 누출 없음 |
| 회귀 | 기존 read/lookup/Run 조회 | 기존 입력·출력·오류 의미 유지 |
| READ | 현재 3개 고정 Job | catalog/queue/receipt/semantic result 개별 판정 |
| READ | RUN/JOB 네임스페이스 | JOB 전용 조회 사용, RUN 검증 완화 없음 |
| READ | 손상·누락·충돌 | 오류 구분 유지, 미존재·성공으로 치환 없음 |
| READ | symlink·경로 탈출·비정규 파일·대형 입력 | 승인된 파일 읽기 범위·크기 상한 유지 |
| READ | 반복 조회 | 대상 queue/receipt/activation 파일 수정·worker 시작·Job 실행 없음 |
| 예약 | 일반 run 및 auto 기록 공존 | auto 기록만 예약 근거로 선택, ID 혼합 없음 |
| 예약 | 잘린 tail·누락·중복·초과 | compact JSON 경계 검증, 전체 tail 외부 반환 없음 |
| 비동기 | 과거 PENDING snapshot + 현재 완료 | 각각의 출처·시각·상태 보존 |
| 배포 | 적용 대상 revision/해시 불일치 | 자동 강제 적용하지 않고 검토 가능한 차이 보고 |
| 운영 | 실제 MCP 클라이언트 호출 | tools/list 확인뿐 아니라 실제 권한·응답·후속 READ까지 검증 |
| MCP 입력 | 자연어 문장 실제 tools/call 인자 확인 | tool 인자에서 SOC/질문/심볼 손실 0, 기존 소비자 스키마 호환 |
| 응답 수준 | SOC 범위 존재·근거 부족 분리 | 기존 SOC 목록을 0건으로 숨기지 않고 근거 충족 수준 구분 |
| 단계 구분 | 개발 테스트→MCP E2E→사외 E2E | 단일 테스트 PASS로 다른 단계 성공 표시 0 |

외부에서 만든 v0.4.25 패키지의 선택 검증 기록은 **62 PASS / 3 FAIL**이었다. 남은 3건은 Workspace Migration 테스트의 외부 fixture 부재로 원본 v0.4.24에서도 같은 실패가 확인됐다. 이 기록은 whpark-mcp의 회귀 또는 사내 예약/OpenCode/운영 E2E 통과를 뜻하지 않는다. MCP 변경에 대한 실제 검증을 별도로 수행하라.

완료 기준은 다음과 같다.

1. SOC 포함 자연어 질문이 정확한 범위와 관련 근거로 이어지고 기존 SOC 단독 조회가 유지된다.
2. 근거가 충분하면 기존 Agent가 후속 READ를 통해 질문에 답할 수 있고, 부족하면 무엇이 부족한지 알 수 있다.
3. 이번에 손댄 Job/예약 조회는 실행 상태·제안 상태·적용 상태와 시점을 구별하며 기존 이력을 보존한다.
4. 운영 완료를 주장하려면 해당 패치의 적용 근거와 실제 승인된 클라이언트 E2E가 있다. 개발 테스트만 통과했다면 개발 검증 완료로 한정한다.

## 8. 검토 가능한 패키지와 운영 반영

사내 작업공간에 다음 산출물을 남긴다. 파일명은 프로젝트 관례에 맞춰도 된다.

- `MCP_CHANGE_REPORT.md`: 재현 증상, 확정 원인 파일·함수, 변경 이유, 호환성, 남은 제한. 검색 수정과 상태 전달 수정을 구분.
- 패치 또는 검토 가능한 commit: 기준 revision, 변경 파일, patch SHA256. 기존 Stage 패치 재사용 여부와 차이를 기록. 독립 변경이면 각각 검토·적용할 수 있게 구성.
- `MCP_TEST_REPORT.md`: 실행 명령, 실패 전/수정 후 결과, 회귀, 미실행 항목. 모의 데이터와 실환경 결과를 구분.
- `MCP_DEPLOY_ROLLBACK.md`: 적용 대상, 백업 범위, 적용·재시작 명령, 완료 판정, 실패 시 복구 방법. 실제 서비스 이름과 경로는 사내 설정에서 확인하고 추정 명령을 실행하지 않음.
- `MCP_REMOTE_VERIFY.md`: 사외 Agent가 실제 노출된 도구로 검색·후속 근거·Job 상태를 한 번에 확인할 요청문. 내부 경로·소스·패치 본문·전체 로그는 제외.
- `MCP_TOOL_CONTRACT.md`: 변경 전·후 실제 도구 이름, 입력/출력 필드, 권한 경계, 기존 호출자 호환성, 후속 READ 연결, 불가능한 기능을 짧게 명시.

운영 반영 전 정확한 패치 해시와 대상 소스가 일치하는지 확인하라. 기존 미커밋 변경과 충돌하면 덮어쓰지 말고 격리된 수정안을 유지한다. 승인된 운영 반영은 백업 → 적용 → 필요한 재시작 → health → 실제 tool 호출 → 검색 및 권한 회귀 순서로 검증한다.

정적 검사·서비스 기동·tools/list 성공만으로 완료하지 마라. 실제 클라이언트에서 SOC 단독, SOC 포함 문장, 범위 없는 문장, 관련 근거 후속 READ를 확인하라. 사외 클라이언트를 직접 호출할 권한이 없으면 그 마지막 검증만 미완료로 표시하고 완성된 확인 요청문을 제공하라.

실패 시 승인된 롤백 절차로 서비스 변경을 복구한다. Job 이력, queue, receipt를 롤백 대상 코드에 섞어 덮어쓰지 않는다. 사용자에게 일반 Updater를 다시 실행하거나 새 Job ID를 만들도록 반복 안내하지 마라.

## 9. 최종 보고 형식

첫 문장에 **자연어 검색의 어떤 동작을 고쳤고, 어디까지 실제로 검증했는지** 적어라. 다음은 짧은 표로 제시하라.

| 항목 | 결과 | 직접 근거 |
| --- | --- | --- |
| 확정 원인 | 확인/미확인 | 사내 보고서의 파일·함수·재현 테스트 |
| 자연어 검색 수정 | PASS/FAIL/NOT_TESTED | SOC 단독과 문장 비교 |
| 근거 연결·후속 READ | PASS/FAIL/NOT_TESTED | 실제 허용 참조와 호출 결과 |
| Job/예약 상태 보완 | PASS/FAIL/NOT_NEEDED/NOT_TESTED | 기존 경로 재사용 또는 수정 범위 |
| 관련 회귀 | PASS/FAIL/NOT_TESTED | 실제 실행 결과 |
| 운영 적용 | APPLIED/NOT_APPLIED/ROLLED_BACK | 정확한 patch SHA256와 대상 revision |
| 사외 E2E | PASS/FAIL/NOT_TESTED | 실제 클라이언트·시각·검증 항목 |
| 신규 Workflow 연동 | OUT_OF_SCOPE | 이 프롬프트 범위 밖. 별도 구현/검증 필요 |

마지막에 기존 숫자 체계를 그대로 유지한 상태 요약을 덧붙여라. 순서와 정의를 바꾸지 마라.

```text
<설치> <예약호출> <대상큐> <대상결과> <원격조회>
STATE=<MCP READ Stage의 queue / receipt / semantic result>
EVIDENCE=<예약 run_id 또는 unknown; 실행시각; observed_at; 확인된 시각은 KST>
SEARCH_FIX=<PASS|FAIL|NOT_TESTED>
LIVE_APPLY=<APPLIED|NOT_APPLIED|ROLLED_BACK>
REMOTE_E2E=<PASS|FAIL|NOT_TESTED>
BLOCKER=<핵심 코드 하나 또는 none>
NEXT=<남은 조치 한 문장 또는 완료>
```

대상결과의 1은 receipt와 semantic result가 완료를 함께 뒷받침할 때만 사용한다. REVIEW_PENDING/PENDING/RUNNING은 2이며, REVIEW_PENDING이면 `PATCH_REVIEW_REQUIRED`로 구분한다. 과거 Stage 결과가 REVIEW_PENDING인 채로 남아 있어도 별도 승인 배포로 검색 수정이 완료될 수 있으므로, 숫자 전부를 1로 만들기 위해 과거 이력을 바꾸지 마라.

질문은 사내에서 확인할 수 없는 필수 정보나 구체적인 운영 승인에 한정하고 한 번에 묶어라. 막힌 단계의 원인·필요 조치만 남기고, 가능한 구현·검증·산출물 작성은 끝까지 수행하라.

## 10. 인계 근거와 해석 우선순위

이 문서는 다음 자료를 기준으로 작성됐다.

- `HANDOFF_L1_JobList_MCP_Bootstrap_RootCause_20261025_v1_0.md`: 원래 목적과 검색 재현, 당시의 조회 공백 및 운영 승인 경계.
- `job-list_v0_4_25.zip`: bootstrap/read bridge/기존 Stage 코드와 문서. 패키지 SHA256: `e9b4bfad6f014d07fb61b6f7a23aef07fc051d6f2aa5ad11d12b53c14bc43c30`.
- `job-list_v0_4_25_VERIFICATION.md`: 패키지 선택 테스트 범위와 실환경 미검증 한계.
- `AGENT_JobList_v0_4_25_Verification_3000.md`: 이번 숫자 5개의 정확한 순서·판정 정의.
- 사용자의 최신 `1 3 1 2 1` 보고. 상세 상태·실행 ID·패치 해시는 이 보고에 포함되지 않았다.

실제 사내 소스·설치본·현재 실행 근거가 가장 우선이다. 최신 보고로 갱신된 부분을 과거 문서의 진단으로 되돌리지 마라. 패키지의 오래된 문서에 “버전이 증가할 때만 활성화” 같은 표현이 남아 있어도 v0.5.43의 실제 예약 전용 코드와 v0.4.25 계약을 기준으로 판단하라.
