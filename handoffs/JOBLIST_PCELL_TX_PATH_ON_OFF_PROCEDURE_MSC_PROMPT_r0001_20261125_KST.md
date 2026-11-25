# Job-list 단일 실행 인계 — PcellTxPathOnOff API Procedure MSC

- r0001 / 2026-11-25 KST
- 전달 저장소: GitHub PUBLIC `wonhwipark/L1Work` / `main`
- 문서 경로: `handoffs/JOBLIST_PCELL_TX_PATH_ON_OFF_PROCEDURE_MSC_PROMPT_r0001_20261125_KST.md`
- 요청 목표: **기존 job-list를 통해 업무 호스트의 실제 `code-analyzer`를 호출하여 `PcellTxPathOnOff` API의 코드 근거 기반 Procedure MSC를 생성**하고, 가능할 때 `doc-converter`로 SVG/HTML을 변환하여 기존 개인 L1 Workspace Work에 근거와 함께 저장·재조회.
- 범위: **이번 API 1건, one-shot.** Recovery 결함 분석·제품 코드 수정·전체 모듈 분석·자동 예약·그룹 Knowledge 게시·Viewer/Kernel/Job-list 스킬 자체 업데이트는 요청하지 않음.
- 본 공개 MD는 **업무 GPT/허용된 Linux Agent에 전달할 실행 프롬프트**이며 운영 Job의 등록·큐잉·실행·승인·설치를 이미 수행했다는 뜻이 아님. 실제 업무 코드, 상세 MSC, 로그, 토큰은 업무 Work에만 보존.

## 업무 GPT → Job-list 실행 프롬프트

> 아래 목적을 기존 `job-list`의 **실제 지원되는 one-shot 실행 경로**로 처리해 주세요. Job-list는 요청·단계·실행 ID·영수증을 관리하고, 분석 주체는 **실제로 설치되어 호출 가능한 `code-analyzer`**입니다. `doc-converter`는 검증된 Code Facts/시나리오 흐름의 시각화에 사용하며 원인·호출 순서를 창작하지 않습니다. 이미 동일 소스 revision·동일 목표로 유효한 Job/결과가 있으면 **기존 Work/Evidence·산출물을 우선 재사용**, 소비된 Job은 재큐잉하지 마세요. G0에서 실행 경로/승인/모델 비용이 불명확하면 생성 가능한 프롬프트·진단 계획만 준비하고 실행은 `BLOCKED`로 기록하세요.

### G0. 기존 실행·원본·권한 확인

1. 운영 Linux에서 실제 활성 `job-list`, `code-analyzer`, `doc-converter`, 기존 Work writer/Kernel, Linux MCP의 **로딩 버전·action/CLI·I/O·결과 조회 경로**를 확인합니다. 공개 `code-analyzer_v0_15_6_1125.zip`은 전체 회귀·설치 검증 전 개발 후보이므로 **새로 설치하지 않고 현재 활성본 사용**. 필요한 도구가 없으면 해당 단계만 `BLOCKED`.
2. 동일 목적 기존 Job·Work·Code Facts·MSC·실행/사용 영수증을 검색해 중복을 피합니다. 원본 C++ 저장소·브랜치/P4 CL·빌드 타깃·RAT/Stack·source revision과 조회 권한을 확인하며, 불명확한 코드 경로는 **제한적 검색**으로 찾습니다.
3. **정확한 심볼 `PcellTxPathOnOff`**의 선언/정의/동명 오버로드·별칭·매크로 래핑을 구분. 위치와 빌드 활성화가 확인되기 전에는 NR/LTE, HAL/DRIVER, ON/OFF 효과나 entry point를 단정하지 않습니다. 검색 결과가 0개 또는 여러 구현이면 `SOURCE_PATH_MISMATCH`/ `AMBIGUOUS_ENTRY`로 기록하고 업무 GPT가 현장 근거로 범위를 정합니다. 필요하면 사용자에게 **하나의 식별 질문**을 요청하고 막힌 범위 외에는 계속 진행합니다.
4. 기존 Job-list의 정확한 Job 정의·스키마·등록/실행 도구를 읽고 **유일한 새 Job ID는 해당 등록기가 생성**하게 합니다. 이 문서의 임의 Job ID나 가짜 Run ID/영수증을 쓰지 않습니다. 승인된 one-shot 실행 수단이 없으면 `JOB_NOT_REGISTERED`와 원인을 회신합니다.

### G1. code-analyzer 실제 호출과 코드 사실 고정

1. source revision을 고정한 뒤 실제 지원하는 bounded scope/probe/Procedure 또는 caller·callee/flow 분석을 호출합니다. 문자 검색 결과만으로 분석 호출 PASS를 주장하지 말고 실제 action·입력·출력·호출 영수증을 남깁니다.
2. API **호출자 → 진입 전제 → 분기/guard → 하위 호출·dispatch/IPC·callback → 상태 변경 → 동기 반환/비동기 완료 → 실패/종료**를 확인된 코드 범위에서 추적합니다. 호출자와 피호출자 중 필요한 범위만 확장하고 탐색 상한, 미탐색 경로, 종료 이유를 기록합니다.
3. 정확한 `파일:행/심볼/호출 조건/실제 build·source revision`과 함께 `CONFIRMED / INFERRED / UNKNOWN`을 구분합니다. 함수 이름만으로 호출 순서·시점·RAT·반환 성공·송수신 메시지 의미를 확정하지 않습니다. 비동기/멀티 Stack 순서가 미검증이면 순서 미확정으로 보존합니다.
4. ON과 OFF 분기가 실제 코드로 확인되면 각각 독립 시나리오로 분리하고 공통 구간은 재사용합니다. 실제 구현이 단일 분기·다른 조건이라면 발견된 경로만 작성하며 **의미를 이름으로 추정하지 않습니다**. 타 모듈 경계의 영향/부작용은 실제 인과 증거가 있는 경우만 기록합니다.

### G2. Procedure MSC 작성·SVG/HTML 변환

1. **AS-IS Procedure MSC 1건 이상**을 목표로 실제 확인된 trigger, caller, callee, IPC/응답, callback, state/guard 및 완료/실패 흐름을 메시지별 근거와 대응시킵니다. participant는 실제 클래스/모듈을 기반으로 정하고 읽기용 alias만 부여합니다.
2. `code-analyzer`가 실제 지원하는 Code-centric MSC/Procedure 산출 형식을 우선 사용합니다. 필요한 별도 Scenario IR/PlantUML은 검증된 Analyzer 산출에 연결해서만 작성합니다. **TO-BE MSC나 Recovery 제안은 이번 요청의 기본 산출물이 아닙니다.**
3. `doc-converter` 실제 지원 IR/호출 계약을 확인한 뒤 가능한 경우 **원본 PUML + SVG + HTML(B형 뷰어)**로 변환합니다. 출력 파일이 실제 생성됐는지, source revision·participant·분기/비동기 순서가 보존됐는지 점검하고 파일별 bytes/SHA-256·변환 영수증을 기록합니다. Converter 지원/호출 부재면 `MSC_CA=PASS`와 `MSC_HTML_SVG=BLOCKED/NOT_RUN`을 분리합니다.
4. 확정 근거가 없는 시퀀스·메시지·복귀 지점을 만들어 MSC를 꾸미지 않습니다. 불명확한 엣지는 해당 메시지/구간만 UNKNOWN으로 표시하고, 검증된 구간까지의 MSC는 유지합니다.

### G3. 기존 Work/Evidence 보존과 MCP readback

1. 유효한 기존 개인 `l1-workspace` Work를 검색·재개하고, 필요한 경우 기존 표준 Work 생성 계약/승인에 따라 진행합니다. Code Facts, Procedure 분석 MD, MSC 원문/PUML/SVG/HTML, source pin, 범위·미확인, 실행 영수증을 기존 승인 writer/Kernel으로 같은 Work에 등록합니다.
2. 동일 Work의 Evidence/Artifact ID, 원본 SHA·revision, 실제 출력 경로를 **저장 후 재조회**. Viewer의 실제 read adapter가 HTML/SVG 연결을 지원하면 표시·클릭도 검사하되, 허용되지 않은 URL/HTML 직접 삽입이나 새 writer 구현은 금지합니다.
3. Linux MCP에는 실제 노출된 `job_catalog_read`/`job_status_read`/`job_queue_read`/`job_result_read` **또는 현행 동등 도구**로 Job ID·실행 단계·Worker 시작/종료·artifact 실재를 각각 확인합니다. `DONE/SUCCESS`만으로 분석·MSC 완료를 선언하지 않습니다. `RESULT_UNSUPPORTED`면 기존 로컬 출력/영수증/Work readback으로 우회 조회하며 임의 allowlist/운영 MCP를 변경하지 않습니다.

### G4. 수락 기준과 최종 회신

| ID | 실제 확인 |
|---|---|
| P01 | 정확한 심볼 선언/정의/활성 코드 revision·RAT/build·범위 |
| P02 | `code-analyzer` 실제 호출·영수증·Code Facts 파일/행 근거 |
| P03 | caller/entry/guard·callee/상태·동기/비동기/실패 흐름 및 coverage |
| P04 | 실제 확인된 ON/OFF 경로의 Procedure MSC와 미확인 구간 구분 |
| P05 | Converter 실제 호출 및 PUML/SVG/HTML 각각 생성·SHA 확인 |
| P06 | 기존 Work/Evidence/Artifact 등록·원본 SHA/revision readback |
| P07 | Job-list 실제 Worker/Run·결과 및 Linux MCP 또는 허용된 로컬 대체 조회 |
| P08 | 입력 변경·중복 Job·잘못된 링크/경로·근거 없는 시퀀스 차단 |

**최종 반환 표:** `SOURCE_REPO/BRANCH/REV`, `SYMBOL_RESOLUTION`, `JOB_ID/PROFILE/RUN_ID`, `ANALYZER_VERSION/ACTION/RECEIPT`, `ENTRY_CALLERS/STATE/COVERAGE`, `MSC_CA`, `CONVERTER_ACTION`, `PUML/SVG/HTML_SHA`, `WORK_ID/EVIDENCE_READBACK`, `MCP_RESULT`, `P01~P08`, `FIRST_FAILURE_STAGE`, `NEXT_ONE_ACTION`. 각 결과는 `PASS/FAIL/SKIP/NOT_RUN/BLOCKED/UNKNOWN` 및 재현 가능한 근거로 답합니다.

**운영 경계:** 이 1건 분석은 제품 코드 수정이나 그룹 `l1sw-dev-knowledge` 게시 요청이 아닙니다. 신규 유료 모델 호출·운영 Job 등록/실행·설치/서비스 변경은 실제 사전 위임·승인 범위를 확인해 실행합니다. 유효한 기존 승인 범위에서는 중복 승인 요구 없이 진행하되, 없거나 불명확하면 `BLOCKED_APPROVAL`로 남기고 지원되는 읽기·계획 단계를 계속 수행합니다. 불확실/완료 Job의 재실행은 금지하며, 결과 게시 실패 때문에 모델을 재호출하지 않습니다.

## 참고 계약(읽기 전용)

- L1Work `handoffs/L1_KNOWLEDGE_UPDATER_NIGHTLY_MODULE_PROCEDURE_MSC_HANDOFF_r0001_20261123_KST.md`: Procedure·MSC·기존 analyzer/converter/work writer.
- L1Work `handoffs/CODE_ANALYZER_V0156_DEVELOPMENT_DELIVERY_r0001_20261125_KST.md`: v0.15.6 개발 후보의 미검증 경계.
- L1Work `handoffs/JOBLIST_V0438_MCP_RECOVERY_STATUS_HANDOFF_r0001_20261117_KST.md`: Job-list/MCP 실행·결과 조회 제한(당시 기준).
