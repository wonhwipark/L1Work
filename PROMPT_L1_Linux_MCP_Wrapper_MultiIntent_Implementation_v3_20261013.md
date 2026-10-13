# Linux MCP Wrapper Multi-Intent 실제 구현 프롬프트 v3

**실행 장소:** MCP Wrapper 소스/서비스 설정에 접근 가능한 **사내 LLM** (사외 SLSI Agent 아님).

## 목적
기존 `run_l1_fix_workflow` MCP Tool의 자연어 요청을 **실제 Workflow 실행**까지 연결한다. 기준: Workflow v1.6.13, Kernel v0.7.10 (사내 실설치 버전 확인). 최근 사외 실측: Work 식별 PASS, code-analyzer 라우팅 PASS, **Runner 실제 실행 FAIL**, 분석 완료·근거 FAIL, 빌드 미실행 PASS. 이전 12개 PASS로 실제 실행을 확정하지 마라.

## 수정 범위·금지 사항
- **1차 수정 대상은 기존 사내 Linux MCP Wrapper**다. Wrapper 입력/호출/출력 및 Workflow CLI·Provider 계약을 확인하고 수정하라. Workflow/Kernel 재구현 금지, 누락 확인 시 최소 변경만.
- 노출 Tool은 기존 **3개**(`run_skill_updater`, `run_l1_fix_workflow`, `run_l1_fla`) 그대로 유지한다. 범용 셸·임의 파일 조회 Tool/엔드포인트를 신규 노출하지 마라. 명령 allowlist 사용, 사용자 입력 셸 실행 금지.
- Updater/Job-list/Dispatcher 정책 변경 금지. 기존 Work, Journal, Evidence, RCA, 승인 이력을 보존한다. 조회만으로 Work 생성·재분석·Git Push·checkout·worktree 생성 금지.

## 구현 작업
1. **Intent Bridge:** Work 목록/상태·이력, 명시적 Work 생성, 분석 Scope Seal, Jira·로그 신규/추가 분석, API·클래스·함수 코드 분석, 요구·설계 검토, 승인된 구현/UT, 문서 게시 요청을 정확한 Work ID와 함께 기존 Workflow CLI/Provider로 연결. 모호하면 BLOCKED. `l1-log-analysis`와 `code-analyzer` 라우팅 혼동 금지.
2. **실제 code-analyzer 연결:** `RF_Set_Tx API 분석해줘`, `TxSwitchMngr 클래스 분석해줘` 요청에서 `REQUEST_CODE_FACT → analyze-code → code-analyzer`가 실행까지 연결되는지 점검. `code-analyzer` 실제 엔트리/인자/작업 디렉터리/출력/권한을 확인해 Runner 연결. **RoutePlan 생성만으로 PASS 금지**. 실제 process 시작, Run ID/종료 상태, 결과 파일, 소스 경로·라인·revision 근거 확인. 불가 시 `UNAVAILABLE`+BLOCKER 반환.
3. **빌드 기본 OFF:** 코드 수정, UT 작성, 분석 요청 모두 `build=false`, `ut_build=false`, `ut_run=false`를 기본으로 한다. 사용자 명시적 빌드/UT 실행 요청에 한해 해당 동작만 허용. UT 실행 시 실행파일이 없으면 자동 빌드 금지. 하위 code-fix/l1-issue-ut에도 적용; 강제 불가하면 실행 차단. 미실행을 `BUILD_NOT_RUN` / `UT_NOT_RUN`으로 구분.
4. **승인 정책:** Scope Seal은 분석 범위 확정일 뿐 FSM 구현 승인 아님. 코드 쓰기는 기존 인증 USER 승인·범위 Gate를 통과한 경우만. P4 CL/Jira Comment/Jira Issue 등 외부 쓰기는 해당 작업·대상·payload hash에 결합된 인증 승인 및 `external-gate --consume`를 실제 Provider 쓰기 직전에 검사한다. 문자열 `--actor USER`만으로 승인된 것으로 보지 마라. 인증·검증 경로가 없으면 쓰기 차단.
5. **MCP 응답:** 파일 경로만 반환하지 말고 KST, Work, Intent, Provider, Run ID, 실제 상태(`NOT_STARTED/QUEUED/RUNNING/COMPLETED/FAILED/UNAVAILABLE`), 코드 분석 요약·근거, 빌드 여부, Evidence, BLOCKER, 다음 조치를 **MCP 대화창 본문**에 출력. 시작/큐잉과 완료를 구분. 민감한 내부 코드·로그를 사외로 반출하지 않도록 기존 출력 정책 준수.

## 반영·검증
- 변경 전 백업/롤백 확보. 적용·필요 시 재시작 후 **실제로 로드된 Wrapper** 버전 확인. 재시작 권한이 없으면 `NOT_APPLIED`로 명시하라.
- 실제 제품 코드·Jira·P4 쓰기 및 빌드는 테스트하지 마라. 읽기 전용 Work에서 `RF_Set_Tx` 분석의 프로세스 증거·분석 근거 확인.
- 수락 항목: ① 기존 Tool 3개 유지 ② Wrapper 수정·서비스 반영 ③ Work 조회 무부작용 ④ API 요청 라우팅 ⑤ **code-analyzer 실제 프로세스 실행** ⑥ **결과·파일/라인 근거** ⑦ 빌드/UT 기본 OFF ⑧ 승인 없는 외부 쓰기 차단 ⑨ MCP 화면 상세 요약 ⑩ 기존 FLA/Updater 회귀.

**출력은 모바일용:** 위 10항목에 대해 `1=실제 확인 PASS, 2=FAIL, 3=미확인`으로 숫자 10개를 한 줄 출력하라. 다음 줄: `Wrapper 반영=YES/NO, code-analyzer=COMPLETED/FAILED/UNAVAILABLE, Run ID=<값/없음>`. 마지막 줄: 실패·차단 핵심 오류 1줄. 모의 테스트/계획/RoutePlan/UNAVAILABLE만으로 ⑤⑥ PASS 처리 금지. 긴 주관식 요청 금지.
