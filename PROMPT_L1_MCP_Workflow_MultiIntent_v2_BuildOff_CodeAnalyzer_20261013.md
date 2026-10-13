# 사내 Linux MCP Workflow 다목적 요청 개선 v2

대상: 기존 `run_l1_fix_workflow` MCP Wrapper와 `l1-fix-workflow`, 관련 Provider. 기준 패키지 `l1-fix-workflow v1.6.13`, `work-ledger-kernel v0.7.10`. **먼저 사내 설치본·실제 CLI 계약·Provider 실행기를 확인**하고 확인된 경로만 수정해줘. 미설치/미지원은 정확히 표시해줘.

## 유지 조건
- 기존 MCP Tool 3개(`run_skill_updater`, `run_l1_fix_workflow`, `run_l1_fla`) 유지. 신규 Tool·범용 셸·임의 파일 조회 기능 추가 금지. Updater/Job-list/Dispatcher 정책 변경 금지.
- Work Ledger가 상태의 기준. 기존 Work·RCA·결정·Evidence 보존. 조회로 Work 생성/Push/브랜치 변경/재분석 금지. worktree 자동 생성 금지.
- `work_docs`, `source_code`, `knowledge`, 외부 `L1Work` 역할 분리. 사내 코드·로그·기밀정보 외부 게시 금지.

## 구현 요구
1. **자연어 Intent**: Work 목록/상세/히스토리, 명시적 Work 생성, 요구·결정 기록, Scope Seal, Jira 로그 분석·추가 분석, 코드/API 분석, HLD/MSC 검토, 승인된 코드 수정, UT/빌드, Work 문서 게시를 구분. 정확한 Work/Jira 식별, 모호할 때 자동 실행·생성 금지.
2. **코드/API 분석**: `RF_Set_Tx API 분석`, `TxSwitchMngr 클래스 분석`, `ClAitProcNr 함수 분석`, `호출 경로/영향도/Side Effect`를 `REQUEST_CODE_FACT` → `code-analyzer`로 라우팅. 로그 분석용 `l1-log-analysis`/`l1-fla`와 혼동 금지. 실제 설치된 code-analyzer 엔트리·입력 스키마·작업 디렉터리·결과 계약 확인 후 읽기 전용 Runner 연결. RoutePlan만 생성한 경우 COMPLETED로 표시 금지. 결과에 소스 파일/라인/리비전, 요약, blocker 출력.
3. **빌드 기본 OFF (모든 코드 수정/UT 경로)**: `build=false`, `ut_build=false`, `ut_run=false`를 기본값으로 고정. `코드 수정해줘`, `UT 작성해줘`, `수정 후 검토해줘`는 일반 빌드·UT 빌드·UT 실행 모두 금지. 사용자가 명시적으로 `빌드해줘`, `UT 빌드해줘`, `UT 실행해줘`라고 요청한 작업만 별도로 허용. UT 실행 요청만 있을 때 실행 파일이 없으면 자동 빌드하지 말고 차단 사유 보고. `code-fix`, `l1-issue-ut`를 포함한 하위 Runner에서도 동일 정책 강제. 미실행은 `BUILD_NOT_RUN`/`UT_NOT_RUN`, Evidence 미확보 상태로 정확히 보고.
4. **승인 경계**: Scope Seal은 분석 범위만 확정. Source 수정은 기존 FSM USER 승인 및 source gate 준수. P4 CL/Jira Comment/Jira Issue는 실제 인증된 사용자별·operation별·target별·payload hash별 사전 승인과 `external-gate --consume` 확인 후 실행. 모델이 생성한 `--actor USER` 문자열은 신원 확인이 아님. Provider 직접 쓰기 우회 금지.
5. **MCP 결과 요약**: MCP 채팅창에 Work ID, Intent, 실제 Provider/Run ID, NOT_STARTED/QUEUED/RUNNING/COMPLETED/FAILED/UNAVAILABLE, 분석 핵심 결과, 빌드 수행/미수행, Evidence, blocker, 다음 단계 출력. 파일 경로만 출력 금지. 확인 불가는 UNKNOWN.

## 검증 (부작용 없는 작업부터)
① 통합 Work 조회 무부작용 ② 기존 Work 상세 ③ API 요청 `REQUEST_CODE_FACT` 분류 ④ code-analyzer 실제 Runner 실행 또는 명확한 UNAVAILABLE ⑤ 코드/API 결과 근거 ⑥ 코드 수정 기본 빌드 OFF ⑦ UT 작성 기본 UT 빌드·실행 OFF ⑧ 명시적 빌드만 허용 ⑨ Scope/외부 쓰기 승인 분리 ⑩ MCP 첫 화면 요약 ⑪ 기존 FLA/Updater Tool 회귀 ⑫ 중복 실행·기존 Evidence 보존.

테스트용 변경은 격리된 샘플 Work로 하고 실제 Jira/P4 쓰기를 발생시키지 마. 진단만 가능하면 수정 완료로 보고하지 마.

**응답 방식**: 위 12개 항목 순서로 `1=PASS, 2=FAIL, 3=NOT_TESTED` 숫자 12개를 한 줄로 출력. 다음 줄에는 설치된 Workflow/Kernel/code-analyzer 버전, MCP Wrapper 수정 여부만 표기. 실패 시 핵심 오류 코드 1줄 이내. 화면 캡처·긴 주관식 응답 요구 금지.
