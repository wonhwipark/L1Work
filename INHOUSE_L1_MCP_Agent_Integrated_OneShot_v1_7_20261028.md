# 사내 L1 Skill·Agent/MCP 통합 원샷 실행문 v1.7 — 최종 단일 MD

- 작성 기준: 2026-10-28 KST
- 사용법: **이 파일 하나만 사내 LLM에 전달**한다. 기존 v1.6 MD나 별도 Execution Booster를 재첨부하지 않는다.
- 통합 범위: **제1부 = 원샷 실행 보강 지시 전체**, **제2부 = 기존 v1.6 실행문 원문 전체(644줄)**. 운영에서의 실행 순서·중단·재개 방식은 제1부를 우선하되, 제2부의 안전 게이트·버전/자산 검증·실제 시험 수용 조건은 약화하거나 생략할 수 없다.
- 원본 추적: `INHOUSE_L1_MCP_Agent_Integrated_OneShot_v1_6_20261028.md` SHA256 `5ff9e8582619d77fbddb1cc61d15c64f5e464dabb8eac6667a0df031f76312ca` / `INHOUSE_L1_MCP_v1_6_OneShot_Execution_Booster_1028.md` SHA256 `f517fbf30fb7f69f37f7ccadb414432de991b3e871fc5ce4ad9ec6c659fcfd03`.
- 범위 구분: 지시문 통합 **완료**는 사내 MCP 구현·스킬 설치·Agent E2E **완료를 뜻하지 않는다**. Workflow v1.6.57, Kernel v0.7.31은 사내 설치·loaded SHA를 별도 확인하고 없으면 독립 진단·패치·fixture 테스트를 계속 수행한다.

## 통합 우선순위 및 충돌 해석

1. **안전/권한/기밀성은 제2부의 제한을 절대 우선**한다. G1~G4의 승인 범위는 각기 별도이며 무단 설치·운영 reload·Work/Ledger 변경·Git write·외부 게시·삭제를 허용하지 않는다.
2. **실행 지속성은 제1부를 우선**한다. 한 단계가 BLOCKED여도 의존하지 않는 읽기·허용 로컬 개발/fixture 검증은 계속한다. 제2부 §B의 의존성/최우선 순서를 위반하지 않으며 동일 서비스·리포지토리에 동시 쓰기하지 않는다.
3. **테스트 상세/판정은 제2부가 정본**이다. Chat-first T1~T8, Guided G01~G18/T01~T20, 코드 M1-a~f, O16~O19, Git action matrix, B0~B7 timeout과 checkpoint 기준을 유지한다.
4. **Agent 출력은 사용자에게 6줄 이내 요약**, 로컬 결과 MD에는 제2부 §D의 A~N 전체 행·시험별 `test_result` 및 `operational_state`·증거/재개 지점을 모두 남긴다. 6줄 보고를 이유로 상세 산출물을 생략하지 않는다.
5. **과거 문서 이름은 이력 표기**다. 제2부에 남아 있는 “이 v1.6 MD 한 파일을 전달”은 현재 전달 파일인 **v1.7 통합본 한 파일**을 뜻한다. `v1.6.57`은 Workflow 스킬 버전으로서 바꾸지 않는다.

---

# 제1부. 원샷 실행 강화 지시 — v1.7 통합판

## 사내 Agent에게 전달할 최상위 실행 지시

너는 L1 Workflow·Kernel·사내 MCP·Agent 연결의 **통합 구현 및 검증 수행자**다. 이 문서 제2부의 v1.6 전체 실행 계약을 기준으로 **이번 단일 요청에서 가능한 안전 작업을 최대한 많이 완수**하라. 단계마다 사용자에게 다시 물으며 멈추거나, 첫 장애에서 전체 작업을 종료하지 마라. 단, 아래 승인이 필요한 변경을 임의로 승인받은 것으로 간주해서도 안 된다.

### 0. 실행 목표와 자동 진행 원칙

- 목표는 긴 설명이 아니라 **실제 구현·실행·검증·재검증 결과**다. 문서 검토만 하고 종료하지 않는다.
- v1.6의 **모든 독립 실행 가능 작업을 작업 그래프(DAG)로 정렬**하여 `준비 → 진단 → 수정 → 타깃 테스트 → 회귀 → Agent/MCP E2E → 패키징 → 결과보고`로 진행한다. O01~O19, O16~O19, G01~G18, T01~T20 및 B0~B7에서 해당 작업에 적용 가능한 항목을 누락 없이 상태화한다.
- 승인 없이 가능한 **조회·환경확인·기존 증거 분석·로컬 안전 테스트·신규 개발 후보 패치**는 사내 정책이 허용하는 범위에서 이어서 진행한다. **실환경 설치, 공유 환경에 미치는 변경, Ledger 확정 쓰기, 외부 Git commit/push/PR, 삭제·정리·배포**는 v1.6이 지정한 게이트를 지킨다. 승인되지 않은 항목은 `BLOCKED_APPROVAL`로 남기고 후속 독립 작업을 계속한다.
- 먼저 설치·루트·ZIP·MCP 도구·권한을 **한 번만** 조사해 인벤토리를 고정한다. 같은 실패/질문을 반복하지 않는다. 원인과 상태가 동일한 작업을 재시도할 때는 최대 두 번만 하고 별도 blocker로 기록한다.
- 읽기 요청이 코드분석·로그분석 또는 Ledger 쓰기를 새로 실행하지 않도록 한다. 폐기된 `l1-log-analysis`를 호출하지 않는다. 기존 Evidence는 보존한다.

### 1. 입력 식별과 버전 분기 — 필수

- `input_artifact`와 `output_artifact`를 분리하여 각 ZIP 파일명, 실제 SHA256, 내부 VERSION, SKILL.md/version, `.skill-release.json`·manifest를 기록한다. **ZIP 외부 이름만 보고 버전을 확정하지 않는다.**
- v1.6 실행문에 지정된 Workflow **v1.6.57**과 실제 사내 제공·설치 파일이 일치하는지 확인한다. 과거 사외 첨부에서 확인된 `l1-fix-workflow_v1_6_56_1028.zip`은 내부 VERSION/SKILL.md/릴리스 메타데이터가 `1.6.56-dev.1`이며, `work-ledger-kernel_v0_7_31_1028.zip`은 내부 `0.7.31-dev.1`이다. v1.6.57과 동일한 바이트·기능으로 **간주하지 마라**.
- **v1.6.57이 확인된 경우:** 그 파일을 기준으로 v1.6의 기능 구현·수정·테스트를 진행한다.
- **v1.6.57이 없는 경우:** v1.6.56을 임의 개명·덮어쓰기·정식 버전으로 설치하지 않는다. 기존 설치/코드 및 첨부에서 가능한 read-only 진단·기존 기능 테스트·독립적인 MCP 권한/도구 점검을 계속하고, v1.6.57이 필요한 수정·검증만 `BLOCKED_INPUT_VERSION`으로 분리한다. 사용자에게는 종료 시 **필요한 파일 하나**와 이유를 짧게 명시한다.
- 코드·ZIP 수정 후에는 새로운 버전/표준 ZIP 이름(예: `l1-fix-workflow_v1_6_58_1028.zip`, **실제 버전은 변경 범위를 확인하여 결정**), 내부 식별자, manifest, SHA256을 다시 맞춘다. 이전 공유 ZIP 바이트를 같은 이름으로 교체하지 않는다. `dev`/`rc` 같은 상태 접미사는 파일명에 쓰지 않고 메타데이터로 분리한다.

### 2. 작업 우선순위와 연속 실행

1. **P0 안전·연결:** 사내 Agent/MCP의 Tool 노출, Read/Result 실제 전달, 사용자·세션·Work 식별, 읽기 전용 강제와 Git Guard, 손상 STAGED fail-closed 판정을 진단하고 수정 가능한 항목을 해결한다.
2. **P0 조회 및 이해도:** `SOC-420517 워크 내용 보여줘`, `SOC-420517 워크 분석내용 보여줘`, `SOC-420517 워크 이슈 내용 보여줘` 3종을 실제 Work 근거가 있는 범위에서 실행한다. 출력이 이슈 원문/분석/진행 이력을 섞지 않는지, 근거 부재를 추측으로 채우지 않는지, 신규 분석이 트리거되지 않는지 검사한다. ID가 실제 환경에 없다면 fixture를 써서 비운영 테스트로 구분한다.
3. **P0 Guided UX:** G01~G18 합격 기준, T01~T20 입력·기대·반례를 모두 검사한다. 숫자 선택 세션 바인딩이 구현되지 않았으면 `선택: 1/2/3`만 출력하는 UI를 수정하고, 실제 다시 입력할 수 있는 `Work ID + 짧은 자연어`로 안내한다.
4. **P1 MCP 확장:** v1.6의 O16 정적 Call Graph/실행 시점 Runtime Stack·후속 2턴, O17 Skill-Updater, O18 Job-list, O19 Git branch/commit/push/PR을 각기 분리 검증한다. Runtime trace가 없을 때 올바르게 거절하면 시험은 PASS일 수 있으나 runtime 기능 운영 검증은 미완료로 남긴다.
5. **P1 회귀:** 변경된 영역 단위 테스트 → 핵심 CLI/계약 테스트 → 관계 스킬 회귀 → Agent E2E 순서로 진행한다. 전체 테스트 타임아웃 시 변경 관련 묶음 결과를 보존하고 안전한 다른 묶음을 계속한다. 1개의 묶음이 막혀도 별개의 검증을 중단하지 않는다.

### 3. 자동 재개·승인 분리·검증 상태

- B0~B7마다 결과 MD에 checkpoint를 원자적으로 갱신하고, 마지막 완료 단계·실행 커맨드·입력 SHA·코드 revision·남은 대상·중단 사유를 기록한다. 재개 시 이미 성공한 시험을 중복 실행하지 않되 코드나 패키지가 바뀌면 영향 시험을 다시 돌린다.
- 기존 v1.6의 단계별 timeout/중단 기준을 그대로 따른다. 환경 장애가 나면 `BLOCKED_ENVIRONMENT`, 도구 미노출은 `BLOCKED_TOOL_NOT_EXPOSED`, 승인 미취득은 `BLOCKED_APPROVAL`, 시간 초과는 `TIMEOUT`으로 분리한다.
- `test_result`: `PASS/FAIL/BLOCKED/TIMEOUT/NOT_RUN`, `operational_state`: `VERIFIED/NOT_EXPOSED/ROUTED_ONLY/RUNTIME_EVIDENCE_MISSING/NOT_VERIFIED` 등을 별도 기입한다. 시뮬레이션/단위 시험 PASS를 실제 Agent E2E PASS로 승격하지 않는다.
- 승인 요청이 필요하면 필요한 범위·대상·예상 변경을 1회로 묶어 제시한다. 응답을 기다려야 하는 승인 항목은 보류하고, 다른 작업을 진행한다. 사내 승인 게이트를 무시하거나 대화상의 침묵을 승인으로 처리하지 않는다.

### 4. 최종 산출물 — 사용자 응답은 매우 간결하게

- 사내 로컬에 결과 파일 **`INHOUSE_SKILL_RECOVERY_RESULT_<KST>.md` 하나**를 작성한다. 원본 실행 로그와 코드 ZIP은 승인되지 않은 외부 저장소로 자동 전송하지 않는다.
- 결과 파일에 반드시 포함: (a) 실제 조사한 설치/입력/출력 버전 및 SHA, (b) O01~O19 상태 표, (c) G01~G18와 T01~T20 PASS/FAIL/BLOCKED/NOT_RUN 집계 및 실패 ID, (d) Chat-first 3종/Agent E2E/Runtime 구분 결과, (e) 변경 파일·새 ZIP·내부 버전/manifest/SHA, (f) 게이트별 승인/미승인, (g) 검증 단계별 checkpoint, (h) 남은 blocker와 재개 명령.
- 사용자에게는 아래 **6행 이내**로만 보고한다. 원문 로그와 상세 diff는 결과 MD 참조.

```
1. 구현: 완료 n / 미완료 n (대표 기능명)
2. 검증: PASS n / FAIL n / BLOCKED n / TIMEOUT n
3. Agent E2E: VERIFIED 또는 미검증 사유
4. 새 산출물: 스킬명·버전·경로·SHA 앞 12자리 (없으면 없음)
5. 차단: 우선 해결할 최대 3건 (권한/파일/환경)
6. 다음 요청: 즉시 실행 가능한 짧은 명령 1개
```

위 규칙에 따라 **지금 접근 가능한 단계는 끝까지 실행**하고, 막히는 영역만 이유와 재개 지점을 기록하라. 문서 검토·계획 작성만으로 전체 작업 완료를 선언하지 마라. 운영 승격·파트 배포는 별도 사용자 승인과 해당 실환경 게이트 PASS 이전에는 수행하지 마라.

---

# 제2부. v1.6 상세 실행문 — 원문 전체 보존

# 사내 복귀 시 L1 스킬 + Agent/MCP 통합 복구 v1.6 — Chat-first Work 조회 3종·Guided Workflow·코드/API 분석·Agent 피드백

- 기준일: **2026-10-28 KST** · 문서 버전 **v1.6** · 원본 v1.0/v1.1/v1.2/v1.3/v1.4/v1.5 보존 · Claude `oneshot01` 및 `mcp01`(Q-001~Q-007) 리뷰 반영 + 신규 사용자 요구 MCP-01~04
- 대상: 사내 Linux PC의 스킬, Agent/MCP Wrapper, 독립 Bootstrap, 필요한 경우 Windows 실행 환경
- 목적: **한 개의 실행 입력·재개 가능한 단계별 세션**에서 **기존 스킬 복구 P0~P2, Agent 채팅 조회 3종(CHAT_WORK/CHAT_ANALYSIS/CHAT_ISSUE), 초보자 Guided Workflow G01~G18·T01~T20, Agent/MCP 코드·API 호출 관계·시나리오 추적 및 결과 후속 질의, 업데이트 결과·Job-list MCP 수정·Workflow GitHub 제어**를 연계 구현·검증하고 모바일 핑퐁을 줄인다.
- 근거: 사용자 Agent 결과 `4 3 4 4 3 2 4`; 이전 Agent 코드 분석의 `CODE_SCOPE_REQUIRED`/`CODE_ROOT_UNREGISTERED`/Runner·Evidence 실패, whpark-mcp `Q3/Q6 FAIL`, Job READ `Q8 BLOCKED` 과거 보고 및 l1-github worktree/role 정책; Dropbox 최신 ACTIVE `START_HERE_r0013.paper` / `OPERATING_RULES_r0009.paper` / `CURRENT_r0028.paper` / `WORK_r0027.paper` / `R026_skill_package_naming_policy_activation_20261028.paper` 및 R025/R024/R023/R022 / `ISSUES_r0005.paper` 및 R027→WORK_r0028→CURRENT_r0029 (공통 패키지 이름 정책의 필수 참조 확인; 실제 빌드 도구 자동 적용은 별도); 별도 `l1-cleanup` CURRENT/WORK. 이전 대화의 job-list·SDM·code-analyzer 관찰은 사용자 보고이며, 최신 사내 설치 상황은 미검증.
- v1.5 변경의 직접 근거: R029 초보자 의도 분류/가이드 현상, R030 검토 문서 `L1_Workflow_초보자_목적기반_Guided_Workflow_검토항목_20261028.md`(SHA256 `f1e73745aac171e0f1ce257bcf0b6608542a6d416e0872fa9623cc12ea9b4e86`), R031 채팅 조회 3종 로컬 구현/검증 `l1-fix-workflow_v1_6_57_1028.zip`(SHA256 `a3e4f0fb0162b8fa1e8bcb326cbd0c6cb2ef4534628956ddbe92da9e35d6bd53`), 전용 사내 E2E 문서 `L1_Workflow_ChatFirst_Agent_E2E_20261028.md`(SHA256 `837f0daf10f488bde4ed6fcabc0aea02f30cfad73f2699e996b93628ba16acf6`). Dropbox CURRENT_r0034→WORK_r0033→R032 및 R031 로컬 ZIP 증거를 확인하고 v1.6 계획에 계승한다. 해당 문서와 ZIP은 **v1.5 구현의 입력·검증 기준**이지 사내 설치 증거가 아니다.
- v1.6 리뷰 반영: 사용자가 전달한 v1.5 검토의 높은 우선순위 2건, 중간 3건, 보완 1건 및 회귀 실행 제한시간/중단·재개 정책. **문서 1개만 전달해도 G01~G18/T01~T20의 입력·기대·반례를 판정 가능**하도록 본문에 수록한다. 실행에 필요한 스킬 ZIP·사내 도구·사용자 승인 자체를 MD가 대신하는 것은 아니다.
- 한계: 이 문서는 **실행 지시서**이며 사내에서 실행했다는 의미가 아니다. ZIP/패키지 버전과 실제 설치·Agent 로드 버전을 혼동하지 않는다. Workflow v1.6.57은 로컬 표적 회귀 25 PASS / CLI fixture 3 PASS이나 확대 시험 94 PASS / 2 기존 실패 및 전체 회귀 미완료, 사내 Agent E2E NOT_RUN이다. Kernel 0.7.31 소스 변경 없음.

## A. 이번 Agent 결과와 즉시 판단

**설문 계약:** `AGENTQ-UPDATER-REMOTE-v1` (이번 v1.1 계획서에서 **사후 부여한 식별자**이며, 과거 Agent 원문 자체에 이 ID가 기록됐다고 주장하지 않음). Q1 설치 버전=1:0.5.45/2:0.5.44/3:0.5.38/4:기타; Q2 GitHub=1:0.5.45/2:구버전/3:조회불가; Q3 STAGED=1:0.5.44/2:0.5.45/3:없음/4:기타; Q4 Bootstrap=1:정상/2:없음/3:오류/4:불명; Q5 MCP=1:cycle/apply 가능/2:update만 가능/3:불가; Q6 정책=1:manual_canary/2:automatic_after_exit/3:disabled/4:불명; Q7 원격 설치=1:지원/2:MCP 수정/3:사내 작업/4:추가확인. 이번 사용자 보고 `4 3 4 4 3 2 4`는 이 문항 기준의 USER_REPORT이며 실환경 파일 근거는 별도다. 과거 숫자 `1 2 2 3 1 2 2`는 다른 진단 문항일 수 있으므로 `LEGACY_QUESTIONNAIRE_UNMATCHED`로 보존하고 상태 변화로 직접 비교하지 않는다.

| 문항 | 응답 | 해석 |
|---|---|---|
| Q1 실제 설치 버전 | 4 | 기타 버전. 값·경로 확인 필요 |
| Q2 GitHub 최신 ZIP | 3 | 조회 불가. 네트워크/인증/대상 repo/Tool 차단 중 분류 필요 |
| Q3 현재 STAGED | 4 | 기타. pending 파일·state·digest 직접 확인 필요 |
| Q4 독립 Bootstrap | 4 | 불명. 존재·버전·실행 권한·설치 루트 확인 필요 |
| Q5 MCP cycle/apply | 3 | 현재 Agent가 사용할 수 없다고 보고. Tool 미노출·권한·구현 중 어떤 원인인지 미분류 |
| Q6 self_update_policy | 2 | `automatic_after_exit` **보고**. canonical 파일의 실제 값과 사전 승인 근거 재확인 필요 |
| Q7 사외 설치 가능성 | 4 | 추가 확인 필요. 원격만으로 설치 가능하다는 증거 없음 |

**핵심:** `automatic_after_exit` 보고와 `cycle/apply` 호출 불가는 동시에 성립 가능하다. 설정 존재가 실행기 등록·MCP 노출을 의미하지 않는다. 잘못된 v0.5.44 STAGED는 별도 설치 차단 결함이 있으므로 선후를 구분한다.

## B. 의존성 및 실행 순서 — 우선순위와 차단 독립성 (Q-002/Q-006)

**실행 순서는 이 절과 §D-2 하나로 통일한다.** `[P0]`는 단순 라벨이 아닌 **가장 먼저 시도할 핵심 역량**이라는 뜻이다. MCP-01(코드분석)과 MCP-02(업데이트 결과 조회)는 가능한 안전한 작업을 기존 P1·P2보다 우선 수행한다. 다만 실제 호스트에 없는 도구를 설치된 것으로 가정하거나 승인 경계를 건너뛰지 않는다.

```text
S0 모든 설치 VERSION / MCP revision / Provider / policy / permissions / test baseline READ
  |
  +-- [핵심-조회] P1-B Workflow 1.6.57 + Kernel 0.7.31 실제 버전/바이트 대조
  |       → MCP-READ/기존 O04·O06: CHAT_WORK/CHAT_ANALYSIS/CHAT_ISSUE read-only
  |       → user_summary가 실제 Agent 채팅에 노출되는지 T1~T8 E2E
  |       → 조회≠분석 실행, Jira 원문 미조회/근거 없음 표시, 조회시 Writer/Provider 호출 0
  |       → Guided Workflow G01~G18 진단 + T01~T20 분류/게이트 회귀 (미구현은 기록 후 국소 보완)
  |
  +-- [핵심-분석] P0-C route·schema READ → P2-A Scope/Manifest READ → MCP-01/O16
  |       → (유효 Runner/권한이 있으면) 상세 코드분석 / API_CALL_GRAPH / SCENARIO_TRACE + Result find/read
  |       → Agent 후속 질의 2회·기존 Evidence 재사용·런타임 stack 근거 구분 E2E
  |       → 없으면 최소 MCP Tool/Provider patch + 회귀, 승인된 reload 뒤 Agent 검증
  |
  +-- [핵심-업데이터] P0-A 승인된 v0.5.45 바이트/SHA 확인
  |       → P0-B 손상 STAGED 증거 보존·승인된 격리·Bootstrap 준비
  |       → P0-C cycle/apply 1회 실행 E2E (격리 전 실행 금지)
  |       → MCP-02/O17 run 탐색 + per-skill 설치/활성 버전 READ
  |       → P0-A BLOCKED여도 MCP-02의 조회 API·fixture 독립 개발은 수행
  |
  +-- [MCP 원격 개선] P1-A job-list catalog/queue/result READ 복구
  |       → MCP-03/O18 승인된 Provider 수정 Job/receipt E2E
  |
  +-- [Workflow Git] P1-B Workflow·P1-C Kernel 최신 후보 1.6.57/0.7.31
  |       → WORK_NOT_FOUND 원인 분리/회귀 → MCP-04/O19 Git status/plan
  |       → 승인된 쓰기/PR은 대상·권한·Push Guard 및 별도 승인 충족 시만
  |
  +-- [독립 안전 점검] P2-B 요청 기반 로그분석 5경로 / P2-C cleanup dry-run
  |
  +-- S6 단일 result MD + O-ID별 PASS/FAIL/BLOCKED/증거 + 승인 대기
```

### 단계별 시간 제한, 중단·재개 계약 — 시간은 안전한 기본 상한이며 환경에 맞춰 낮출 수 있다 (v1.6)

**“MD 한 개/원샷”의 뜻은 하나의 사내 LLM 지시문과 하나의 누적 결과 파일**이다. 모든 테스트를 단일 프로세스/무한 세션에서 무조건 완료한다는 뜻이 아니다. 아래 수치는 **실행 상한(timeout)** 이며 결과 완료 예상시간이 아니다. 자산·승인 대기 중에는 독립 작업만 하고, 검사 불가 부분을 PASS로 대체하지 않는다.

| test_bundle | 순서/범위 | 기본 상한(각 묶음, wall clock) | 중단 조건 | 재개 체크포인트 |
| --- | --- | --- | --- | --- |
| B0_INVENTORY | S0 설치본/정책·SHA·MCP Tool schema READ | 5분 | 권한·경로 불명/자산 identity 불일치 시 해당 변경만 차단 | `B0_inventory`/실제 SHA·loaded_revision |
| B1_CHAT_READ | MCP-READ T1~T8 (쓰기는 0) | 8분 | Writer/Provider side effect 1건이라도 감지 → 해당 실행 즉시 중단 | `B1_chat`/8개 case별 출력·side_effects |
| B2_CODE_E2E | MCP-01 M1-a~f, 후속 2턴 | 12분 | 권한/Root/SCOPE 불명, 허위 runtime evidence, 반복된 동일 blocker 2회 | `B2_code`/analysis_result_id·evidence·revision |
| B3_GUIDED_UX | G01~G18·T01~T20 fixture 진단 | 12분 | 권한 없는 Work write 발생·명시 없는 로그 Provider 실행 시 중단 | `B3_guided`/G·T별 expected/actual |
| B4_UPDATER | P0-A/B·MCP-02 read+승인된 독립 설치 | 10분 | STAGED 손상·manifest/hash mismatch·승인 없음 → apply 절대 호출 안 함 | `B4_updater`/stage_id·receipt·sha |
| B5_JOB_GIT | MCP-03 job-list / MCP-04 Git 각각 독립 실행 | 각 8분 | 변경 대상 범위/HEAD/승인 변경 → STALE_PLAN, 무단 쓰기 금지 | `B5_job`, `B5_git`/plan_id·expected_head·receipt |
| B6_REGRESSION | 변경파일 관련 smoke → 연동 → 전체를 나눈 shard | smoke 3분, 연동 5분, 전체 shard당 10분, **전체 회귀 합산 25분 상한** | 2회 동일 실패·무진전 5분·한 shard timeout·자원 고갈·실환경 파괴 위험 | `B6_regression`/마지막 수집 nodeid·shard·outcome |
| B7_FINAL | 결과 MD 통합/Agent readback 1검증 세션 | 8분 | Agent 불가면 실제 채널 검증 BLOCKED, fixture 시험은 보존 | `B7_final`/result_sha·Agent transcript ref |

**순서와 전이:** `PENDING → RUNNING → PASS|FAIL|BLOCKED|TIMEOUT|NOT_RUN`; 각 묶음 종료 때 사내 로컬 `INHOUSE_SKILL_RECOVERY_RESULT_<KST>.md`를 원자적으로 갱신(임시 파일→rename, 권한 확인). 동일 `run_id`, 입력 ZIP SHA, repo revision, MCP loaded revision, 안전 게이트 승인 receipt, `last_completed_bundle`, `next_bundle`를 함께 저장한다. 재개 시 이 키가 같으면 PASS한 read-only/불변 테스트를 재사용하고 FAIL/BLOCKED/TIMEOUT·변경 영향 항목만 재실행; 바뀐 source SHA/HEAD는 stale baseline으로 보존하고 재인벤토리한다. ZIP/Work/로그 원본은 이 결과 문서에 복제하지 않는다. 동일 blocker는 최대 1회 안전 복구 뒤 재시험하고 연속 2회 동일 실패 시 더 반복하지 않는다. **timeout은 FAIL 또는 TIMEOUT이며 테스트 미실행/미검증은 NOT_RUN; 통과로 표시하지 않는다.**

**자산 의존성 표** (`Y`는 v0.5.45 바이너리 반입 필요, `별도`는 다른 패키지·fixture의 독립 확보 필요):

| 항목 | v0.5.45 자산 의존 | 자산 없을 때 가능한 범위 / 불가능한 범위 |
| --- | --- | --- |
| S0 / P0-C READ / P2-A Scope·Manifest | N | 설치본·route·tool schema·코드 Root·Provider 상태 조회 가능; Bootstrap 실행 불가 |
| MCP-READ / O04·O06 | N (Workflow v1.6.57 별도 확보) | 설치된 Workflow/Kernel 조회 DTO/Agent 전달 스키마를 진단·fixture 시험. v1.6.57이 없으면 실제 E2E는 BLOCKED, 기존 읽기 전용 route/schema 점검은 진행 |
| Guided Workflow G01~G18 / O06 등 기존 이슈 | N | 설치 코드·fixture만으로 의도 라우팅/출력 게이트 진단 가능. 권한/스킬 부재는 항목별 BLOCKED, 전체 개선 완료라 주장하지 않음 |
| MCP-01 / O16 | N | 설치본으로 CODE_DETAIL/API_CALL_GRAPH/SCENARIO_TRACE + 후속 질의 계약·fixture 및 find/read 테스트 가능. RUNTIME_CALLSTACK은 승인된 실제 trace/dump가 없으면 NOT_AVAILABLE; Root/fixture 없으면 E2E BLOCKED |
| P0-A / P0-B | Y | P0-A의 네트워크·전달 경로 진단 가능; 신뢰 자산 미수신이면 P0-B 새 stage·설치 금지 |
| P0-C cycle/apply 실제 실행 | Y | READ만 가능, 손상 pending 격리 및 승인·Bootstrap 준비 전 실행 금지 |
| MCP-02 / O17 | N (실호스트 신규 Updater 검증은 Y) | 최신 run 탐색·receipt 조회 도구 구현·fixture 시험 가능; v0.5.45 실제 설치 성공 주장은 금지 |
| P1-A / MCP-03·O18 | N | 기존 job-list/whpark-mcp Tool READ·allowlist 테스트, 승인된 patch 가능; 실제 reload는 별도 승인 |
| P1-B / P1-C / MCP-04·O19 | 별도 | 각각 Workflow/Kernel/l1-github 정확한 설치본·자산·허용 fixture가 필요; 읽기 조회와 안전 테스트는 독립 가능 |
| P2-B / P2-C | N | 허용 fixture 범위 로그분석 계약 시험·cleanup 삭제 0건 dry-run; 분석 실행은 명시 요청 시에만 |

**자산 반입 차단 분리:** P0-A가 `BLOCKED_ASSET_TRANSFER`이면 **오직 v0.5.45 실제 staging/Bootstrap 적용·그에 종속된 E2E만 보류**한다. S0, P0-C 읽기, P1-B/Kernel의 MCP-READ·Guided Workflow 점검, P2-A 진단, MCP-01/02 계약 및 fixture, P1-A/MCP-03, 별도 자산이 있는 P1-B/C·MCP-04, P2-B/C의 독립 작업은 진행한다. 병행은 읽기/독립 테스트에 한정하며 동일 운영 설정·MCP 서비스·Git 저장소에 대한 동시 쓰기나 무승인 재시작은 허용하지 않는다.

**불변식:** 손상 pending이 있거나 검증되지 않은 동안 `cycle`/`apply` 테스트를 하지 않는다. `BLOCKED` + `PENDING_SELF_UPDATE_INVALID`는 **O15 fail-closed**일 수 있으며 Tool route 자체의 O04 오류로 곧바로 분류하지 않는다. `STAGED`/`ROUTED`/`QUEUED`/부분 PASS를 설치/E2E 완료로 승격하지 않는다.

## C. 스킬별 해결 항목/완료 조건

### P0-A — GitHub 접근 및 릴리스 식별 (공통 인프라 / skill-updater 선행)

- **현상:** Agent Q2=3, GitHub 최신 릴리스 조회 불가. **v0.5.45의 GitHub 게시·사내 반입은 아직 미확인**이다. 로컬 ZIP 생성과 GitHub 릴리스 게시를 구분한다.
- **확인:** 실제 사용 계정과 실행 호스트, 원격 origin/repo, HTTPS/프록시/방화벽, 인증 범위(401/403/404/timeout 구분), GitHub API 호출 예산, skill-updater 소스 별도 GitHub 접근 정책. 사내 저장소를 외부 GitHub에 접근시키거나 사내 코드를 자동 업로드하지 않는다.
- **전달 책임/게이트 (P-004):** 사용자는 사내로 반입 가능한 **기존 승인 경로 또는 승인된 사외 GitHub 릴리스 위치**를 1회 지정한다. 해당 경로의 자산 게시·전달 담당자는 사용자/승인된 운영자로 기록하고, 사내 담당자는 **실제 수신 ZIP의 SHA**를 검증한다. 전달 수단이 확인되기 전에는 `BLOCKED_ASSET_TRANSFER`로 두며 임의 업로드, 임의 전송, 토큰 발급을 수행하지 않는다. GitHub 공개 여부도 승인 전 추정하지 않는다.
- **조치:** 이미 승인된 자격증명·네트워크 경로의 구성 오류만 수정한다. 임의 토큰 생성·권한 우회·인증정보 출력 금지. 현재 승인 경로로 온라인 조회가 불가하면 **승인된 파일 전달 경로에서 받은 릴리스 ZIP**만 로컬 해시 검사하는 차선책을 사용하고 온라인 E2E는 BLOCKED로 둔다.
- **기준 산출물:** `skill-updater_v0_5_45_1028.zip`; SHA-256 **`559ecb512d807cf0c5c4a60cf6007a8eddd34b8e2011fb0306241d8a1bb876de`**. 이 바이트가 사내 릴리스와 일치하는지 확인. 일치하지 않으면 설치 금지.
- **완료:** 승인된 경로로 **실제 바이트 확보** + 릴리스 원격 자산 URL/버전/해시 대조 PASS 또는 승인된 오프라인 수신 자산 검증 PASS(원격 조회는 별도 BLOCKED 기록). 바이너리 반입 실패는 P0-B 시작 금지. `asset_source`, `transfer_owner`, `sha256`, `release_publication_state`를 결과에 남긴다.

### P0-B — skill-updater v0.5.45 + 독립 l1sw-bootstrap

- **현상:** 과거 v0.5.44 `STAGED` 후 외부 `cycle` 미호출. v0.5.44는 `PACKAGE_CONTENTS.sha256`이 오래되어 외부 Bootstrap 무결성 검사를 실패하는 **별도 결함**. v0.5.45 로컬 ZIP에서 수정·테스트되었으나 사내 E2E 미확인. Q1=기타, Q3=기타, Q4=불명, Q6=`automatic_after_exit` 보고.
- **진단:** 실제 설치 및 Agent 호출 대상 `VERSION`, canonical updater root/config, pending intent의 state/from/to/digest, staging 경로, install journal/receipt, 독립 Bootstrap 설치 파일·버전·소유자/권한·프로세스, 실제 `self_update_policy`의 값과 자동 설치 승인 근거 확인. 설치 중 자기 소스 직접 교체하지 않는다.
- **실행 순서 불변식(P-003):** 손상된 pending이 남아 있거나 손상 여부를 알 수 없는 동안에는 `cycle`/`apply`를 **테스트 목적으로 호출하지 않는다**. 먼저 status/schema/route 및 intent/journal 읽기 → 승인된 증거 보존·격리/복구 → 신뢰된 v0.5.45 재-STAGED → 정책·락·권한 재검사 → 실제 적용. `BLOCKED + PENDING_SELF_UPDATE_INVALID`는 Bootstrap이 실제 호출되어 보호 차단했을 수도 있으므로 MCP 미호출과 구분한다.
- **복구:** 기존 불량 STAGED v0.5.44의 증거를 보존하고, 승인된 절차로 **격리(quarantine)·복구 가능 상태 확보**. 삭제/덮어쓰기로 의도 기록을 날리지 않는다. 이후 신뢰된 v0.5.45만 새 STAGED 후보로 준비. 독립 Bootstrap의 approved `cycle` 또는 명시 승인된 `apply` 경로로 기존 updater 프로세스 종료 후 적용. `automatic_after_exit`여도 canonical 설정의 승인·권한·`--apply-after-exit` 조건을 모두 검사한다. 미승인 `manual_canary`나 정책 차단을 우회하지 않는다.
- **분리 경로:** 일반 Agent/MCP 요청에서는 `--scheduled` 사용 금지. Windows Task/cron 등 실제 예약 실행에만 scheduled 동작. 자기 호출 재귀·중복 Job·락 회피 방지.
- **완료:** (1) ZIP 매니페스트 모든 엔트리·해시 PASS (2) 외부 `extract_verified` PASS (3) 실호스트 receipt `VERIFIED` (4) canonical 설치 VERSION **0.5.45** (5) Agent와 OS launcher가 실제 로드한 VERSION **0.5.45** (6) 재실행 시 중복 설치 없이 정상 판정. 이 6개 중 빠지면 PARTIAL.
- **남겨둘 정책 문제:** 손상된 자동 STAGED가 다른 스킬 업데이트 전체를 막는 S-002/O15는 기존 `fail-closed` 유지. 소유자 승인 없는 자동 continue·pending 자동 삭제 금지; 안전한 격리+재시도 설계만 준비.

### P0-C — 사내 MCP / Agent Wrapper (공통 실행 인터페이스)

- **현상:** Q5=3(외부 Bootstrap cycle/apply 원격 실행 불가). 과거 MCP Q1 UNKNOWN / Q3·Q6 FAIL / Q8 READ BLOCKED 보고, Q4·Q5 미시험.
- **진단:** `run_skill_updater`의 실제 호출 명령(`skill_updater.py update` 직접인지, 외부 Bootstrap `cycle`인지), 사용 실행계정, canonical config 인자, 등록된 Tool schema와 Agent 노출 목록, reload/restart 반영 여부. 코드분석/로그분석의 **실제 실행과 결과 조회** Tool이 모두 노출되는지 확인한다.
- **수정:** 기존 권한 모델 안에서 Bootstrap cycle 상태 조회/실행의 안전한 Wrapper 연결과 설치 결과 조회, read-only job status/result 및 analysis-result `find/read`의 Tool schema·노출·권한을 준비한다. 최종 code-analyzer 실행 및 Result READ E2E 판정은 MCP-01/O16에서만 수행한다. 임의 셸 실행·전역 경로 접근·인증 우회 대신 좁은 allowlist 및 실제 권한/경로 확인.
- **완료:** 동일 Agent 실행 신원에서 (사전에는 **읽기 전용** status/schema/route 확인만) → P0-B의 승인된 격리/Bootstrap 검증 완료 후 승인된 cycle/apply 1회 → install receipt 조회. `BLOCKED + PENDING_SELF_UPDATE_INVALID`는 O15 fail-closed이고 **O04 라우팅 실패와 별개**다. 도구의 `ROUTED/QUEUED/RUNNING`은 성공이 아니다. 필요한 서비스 재시작 전/후 schema·revision·호출 결과를 구분한다.

### P1-A — job-list (최근 문서 기준 v0.4.25, 실설치 UNKNOWN)

- **현상:** job catalog 찾기/원격 READ/결과 회수 미흡, 테스트 fixture missing 보고. 스킬 업데이트와 Job runtime/Tool 노출 문제를 분리해야 함.
- **진단:** 실제 설치 버전, 카탈로그 등록·job alias, `plan/enqueue/execute/apply` 명령 경계, Job READ `catalog/status/result`, 실행 history/receipt, MCP Tool 노출/권한, Worker 연결 및 사용자 승인 상태 확인.
- **수정/검증:** 가장 작은 **안전한 읽기 전용 fixture 작업**을 이용하여 catalog → enqueue → run → status/result 일관성 확인. 권한이 없으면 등록만 하고 실행 차단한 사실 기록. Bootstrap 예약 실행과 job-list 예약이 서로를 재호출하지 않는지 확인. 사외 Agent에서 결과를 숫자·짧은 blocker로 볼 수 있어야 한다.
- **완료:** 안전한 fixture의 READY → RUNNING → SUCCEEDED/FAILED 원인과 receipt를 Agent가 조회 가능. 다른 실제 Job 실행/배포는 명시 승인 후만.

### P1-B — l1-fix-workflow (개발 후보 v1.6.57 · **정식 릴리스 아님**)

- **최신 입력 후보:** `l1-fix-workflow_v1_6_57_1028.zip`; SHA-256 `a3e4f0fb0162b8fa1e8bcb326cbd0c6cb2ef4534628956ddbe92da9e35d6bd53` (R031 로컬 ZIP 실측). ZIP 내부 VERSION/SKILL/release/manifest 1.6.57 일치 보고, **사내 실제 반입 바이트/설치본은 별도 검사**한다. Kernel 후보 0.7.31은 변경하지 않는다. 과거 정규화 v1.6.56 SHA `ed82375835b83acaedb9da07462bbaf9add0ea6089757e9b6b6665bb7ef550e5`는 회귀 비교용 baseline이다. 사용자 제공 같은 이름 v1.6.56 ZIP의 실측 SHA `1150a737e554147967fa00f790a52511c50706d127c7b4a26686847ffbb03129` 및 내부 `1.6.56-dev.1`은 **정규화 바이트와 다르므로 이름만으로 설치 금지**.
- **최근 알려진 실패와 로컬 시험 범위:** v1.6.56 이전 후보 84 PASS / 1 FAIL(`WORK_NOT_FOUND`), 신규 v1.6.57 targeted 25 PASS와 CLI fixture 3 조회 PASS, 확대 회귀 94 PASS / 2 FAIL(`WORK_NOT_FOUND` 등 이전 소스에서도 재현), 전체 pytest는 약 59%에서 timeout되어 FULL PASS가 아님(R031). 다른 기준의 테스트 수치를 합산하거나 현 사내 재현으로 단정하지 말 것.
- **진단 선행:** 동일 `work_id` 재개가 어디서 끊기는지(등록/조회, 작업 경로, DB/manifest, Writer/Provider, 기본 Work 선택, 저장 후 readback) 최소 fixture로 재현하고, 반환 상태·실행 신원을 확보한다. 신규 Work 생성으로 기존 Work 재개 실패를 가리지 않는다.
- **검증:** v1.6.57 정확한 ZIP/실제 설치/Agent 로드 버전과 Kernel pair 대조 → §C+의 MCP-READ 3뷰·T1~T8 읽기 전용 검증 및 §C++++ G01~G18·T01~T20 Guided 진단 → `WORK_NOT_FOUND` 별도 분리 재현/최소 수정/재시험 → 로그분석 미수행/명시 요청/실패/나중 추가/기존 Evidence 재사용 시나리오 및 MSC·문서 갱신 → 전체 회귀 완주. **P1-B는 Work 조회/라우팅/Guide 응답·Kernel pair 회귀만 소유하며, code-analyzer 실제 실행→Result READ→Evidence E2E는 MCP-01/O16 단일 소유**. Jira/P4/Git 원격 쓰기는 승인 전 수행 금지.
- **수정 후 패키징·검증 (v1.6 신규):** 사내 입력 `input_artifact`는 v1.6.57 ZIP SHA `a3e4f0fb0162b8fa1e8bcb326cbd0c6cb2ef4534628956ddbe92da9e35d6bd53`(또는 실제 설치 후보)의 읽기 전용 기준선으로 고정한다. 소스 패치가 일어나면 **별개 `output_artifact`**로 새 semantic version(예: 수정 내용·호환성 검토 후 `1.6.58`, 실제 버전 확인 전 예시임), 새 ZIP 이름 `<skill-id>_v<major>_<minor>_<patch>_<MMDD>.zip`, 내부 VERSION/SKILL.md/release metadata, PACKAGE_CONTENTS manifest, 최종 ZIP SHA256을 재생성·상호 검사한다. 기존 v1.6.57 파일명으로 바이트를 덮어쓰지 않는다. 원본과 새 후보에 대해 각각 `filename, canonical_version, zip_sha256, manifest_digest, source_revision, stage, test_receipts`를 남긴다. Kernel/MCP/job-list 등 변경된 다른 아티팩트도 동일하게 입력/출력을 분리한다. 패치 전 원본 SHA로 **패치 후 새 ZIP을 검증하는 모순을 금지**한다. 새 버전이 여전히 development_validation_only인 한 설치/팀 배포 승인으로 승격하지 않는다.
- **완료:** Work 재개 실패의 원인·조치·회귀 결과, v1.6.57 CHAT 3종 Agent 실제 T1~T8 및 Guided G01~G18/T01~T20 PASS/PARTIAL/FAIL/BLOCKED, `collected/executed/passed/failed/skipped`와 남은 실패/중단 사유 보고. 조회 E2E PASS는 O16 코드분석 E2E나 Guided 전체 PASS를 의미하지 않는다. **전체 회귀 PASS만으로도 RC/팀 배포 승격 금지**. 별도 사용자 승인 전 `DEV_VALIDATION` 유지.

### P1-C — work-ledger-kernel (개발 후보 v0.7.31 · **정식 릴리스 아님**)

- **입력 후보:** `work-ledger-kernel_v0_7_31_1028.zip`; SHA-256 `a0a593416fe77e8f30ae96e21a3b970903163d6fd01b46f0f5e658e0ea3e060b` (`WORK_r0026.paper`/R025 기록값, 사내 실측 필요). 과거 v0.7.30은 실패 비교용 baseline이며 설치 대상이 아니다.
- **최근 결과:** 이전 후보 집중 7 PASS(이전 대화 보고), 전체 회귀 **미검증**. v0.7.30의 192 PASS/3 FAIL은 과거 결과이므로 '현재 3건 실패'라고 단정하거나 재현을 무조건 필수로 하지 않는다.
- **진단/검증:** 최신 후보 실제 설치·로드 버전/manifest/Provider 등록, Workflow pair, Work/Evidence history와 resume idempotency 확인. 최근 `WORK_NOT_FOUND`가 Kernel 경계에 있는지도 같은 fixture로 추적; 기존 실패 3건은 필요한 회귀 목록에서 출처·변경 영향별로 대조한다. 전체 회귀와 5경로 Work 문서 갱신 계약을 검증한다.
- **완료:** 현재 v0.7.31 후보 대상의 전체 회귀 범위·실패/누락, Work resume 및 Workflow pair E2E 근거 확보. **검증 후보의 테스트 PASS는 RC·배포 승인과 별개**.

### P2-A — code-analyzer 사전 진단 (실제 E2E는 MCP-01/O16 한곳에서 담당)

- **범위 분리(Q-001):** 이 절은 활성 code-analyzer 설치본·VERSION·승인 Root/Scope·Provider manifest·MCP schema·권한의 **읽기 전용 확인 및 부족한 설정 목록화**만 한다. 과거 `GitHub 401`, `CODE_SCOPE_REQUIRED`, Root/Provider path 문제의 각 원인을 구분한다. 이 대화에 있는 ZIP은 사내 실설치 증거가 아니다.
- **E2E 단일 소유:** 코드분석의 `request → Runner SUCCEEDED → result find/read → Evidence` 회귀, Agent 출력 PASS/FAIL과 O16 종료 판단은 **MCP-01**에서만 수행/보고한다. 이 절에서 별도 분석 Result READ PASS를 기록하지 않는다.
- **완료:** P2-A는 `PREFLIGHT_PASS/PREFLIGHT_BLOCKED`와 실제 설치 VERSION·root_id·manifest 상태를 MCP-01 입력으로 제공. **최종 코드분석 E2E의 유일한 결과 행은 I/O16**이고 G행은 로그분석/issue-analyzer 전용이다.

### P2-B — issue-analyzer / l1sw-dev-log-analyzer-plus / 로그분석 선택 정책

- **사용자 결정 D-029:** `l1-log-analysis`는 **폐기된 Provider 식별자**다. Workflow/Kernel의 신규 선택·호출·등록과 fallback에서 제거하고, 과거 Work/Evidence의 **읽기 호환만 유지**한다. 폐기 Provider에 신규 호출용 shim/호환 레이어를 붙이지 않는다. `l1sw-dev-log-analyzer-plus`는 **별도 유효 분석 스킬**이며 폐기 대상과 동일시하지 않는다. 실제 Provider manifest의 ID/alias도 확인한다.
- **사용자 결정 D-030:** 로그 파일이나 TXT/SDM이 **존재한다는 이유만으로 분석을 자동 시작하지 않는다.** 조건은 사용자가 해당 Work에서 로그분석을 **요청했는가**, 그리고 분석이 실제 **수행·미수행·실패·나중 추가·기존 Evidence 재사용** 중 어느 상태인가다. TXT는 **분석 요청이 있을 때에 한해** SDM 파싱을 생략할 수 있는 입력 형태일 뿐 자동 분석 트리거가 아니다.
- **현상:** log-provider 교체 및 문서 계약의 새 dev 후보는 검증 중이며, 과거 SDM Parser fixture 부족과 `issue-analyzer` TXT 직접 입력/결과 READ 연계 검증도 남아 있다. 이들은 독립 실환경 과제이며 폐기 Provider 복구와 혼합하지 않는다.
- **필수 5경로 E2E:** (1) 요청 없는 **미수행**: 코드분석/수정논의/MSC/문서 업데이트 계속, 로그분석 호출 0, 근거 부족 명시. (2) **명시 요청 성공**: 유효 Provider만 선택·실행, SDM 변환 또는 TXT direct는 필요 시 수행, 결과와 Work/Evidence 연결. (3) **요청 실패**: 실패/차단 원인 및 변경·미검증 상태 표시, 허위 PASS 금지. (4) **나중 추가**: 동일 `work_id`의 결정·증거·문서 이력을 유지하며 영향 부분만 갱신. (5) **기존 Evidence 재사용**: 원본 출처·validity 확인 후 중복 실행 회피. 추가 보호 검증으로 폐기 Provider 신규 호출은 차단하고 과거 Evidence read는 허용한다.
- **진단 및 조치:** 유효 Provider manifest·실제 설치본, SDM→TXT Parser 기능, 기존 TXT 분석, 분석 결과 receipt/run_id/hash와 MCP find/read 확인. 승인된 fixture가 없으면 `BLOCKED_FIXTURE`로 기록하고 안전한 mock으로 계약만 검증; 임의 분석 수행·원본 TXT 삭제·사내 소스 복제·외부 반출 금지.
- **완료:** 위 5경로의 Work→Kernel→Evidence/MSC/문서 상태와 Agent 결과 조회를 일관되게 검증하고, 폐기 Provider 신규 호출 0/기존 이력 READ 성공. fixture 없는 실제 SDM 변환 E2E는 별도 BLOCKED로 둔다. 성공한 부분만 완료 처리.

### P2-C — l1-cleanup (v0.13.6 후보)

- **현상:** `.opencode` event DB 약 12GB, 중복 로그·완료 TXT·`.claude/skills` 임시 산출물 정리 기능은 ZIP 개발 완료 보고이나 사내 대상 파일 안전성 미검증.
- **진단:** Windows/Linux 경로별 read-only `skill-artifacts` dry-run HTML 보고서, skill별 후보량과 보호 이유, 열린 파일/락, 대규모 트리 소요·병목. 실제 OpenCode event DB backup/점검 절차를 서비스 지원 방식으로 평가.
- **필수 보호:** `SKILL.md` 및 소스/데이터/레퍼런스/사용 중 파일/SDM 원본 삭제 금지. SHA-256 동일 원본 하나 보존, 분석 완료 TXT는 log-analyzer-plus의 성공 receipt와 일치해야만 후보화. 우선 dry-run; quarantine/삭제/DB vacuum은 C++의 G4에 따라 사용자가 파일 범위와 보존·복원 정책을 명시 승인한 후 별도 시행.
- **완료:** 삭제 0건의 dry-run으로 안전한 후보·제외 목록/용량·위험 기준을 입증. 실제 용량 확보는 승인 전 미완료 상태 유지.
- **결과 귀속(P-006):** Cleanup 결과는 **별도 프로젝트** `l1-cleanup-maintenance` / `CLEANUP-ARTIFACT-001`의 기존 O01~O04에 연결한다. Workflow의 O번호로 중복 등록하지 않는다. Dropbox에 저장할 때도 해당 프로젝트 RUN→WORK→CURRENT를 따르며 사내 원본은 업로드하지 않는다.

### 이번 원샷의 명시적 제외

- `l1-github`의 **Workflow DELIVER 연계/Agent 승인 Git 제어는 이번 신규 MCP-04 범위에 포함**한다. 무관한 일반 Git 기능 전면 재작성, `doc-converter` MSC 시각화, SAM MCD, l1-fla 개별 실로그 분석은 제외한다. 독립 장애를 무한 확장하지 않는다.
- GitHub/P4 **우회 직접 push/submit**, 무승인 commit/push/PR, Jira/Confluence 변경, 사내 코드 외부 업로드, 승인 없는 OS Task 변경, 자동 대량 삭제, 민감 원본 Dropbox 저장은 실행하지 않는다. MCP-04의 승인된 `l1-github` Push Guard 경유만 C++의 G2 Git 승인 후 허용한다.

## C+. 신규 4개 Agent/MCP 기능의 통합 구현 요구 (이번 추가 핵심)

> **기존 사용자 요청 4항목(O16~O19)에 더해 v1.5에서 읽기 전용 채팅 조회(MCP-READ)와 Guided Workflow 검증을 같은 사내 LLM 세션에서 함께 실행한다. 새로운 독립 O-ID를 만들지 않는다.** 다음 action/tool 이름은 **설계상의 표준화 제안**이다. 현재 whpark-mcp 서버에 이미 존재한다고 가정하지 말고 운영 스키마를 조사한 다음, 동등한 기존 Tool이 있으면 재사용하고 부족한 부분만 추가한다. 코드 수정 자체는 사내 권한/승인된 경로에서만 한다.
>
> **호출 체인:** 사외 메신저 Agent → 사내 MCP Wrapper(좁은 허용 action) → Workflow / Provider / job-list / l1-github → 로컬 산출물·Work Evidence·receipt → MCP read/find/status → Agent 사용자 요약. `MCP ROUTED`는 실제 `EXECUTED` 또는 `RESULT_READ_VERIFIED`가 아니다.

### MCP-READ [P0·사용자 체감 우선, 기존 O04·O06과 P1-B 연계] Chat-first Work 조회 3종의 Agent 실제 피드백

**이는 MCP-05가 아니다.** Workflow v1.6.57에 로컬 구현된 세 가지 읽기 전용 뷰를 현재 Agent/MCP Tool의 기존 Work 조회/read/status action에 노출·전달하는 *인터페이스 보강*이다. MCP-01/O16의 코드분석 실행/Result READ와 겹치지 않게 구분한다. 기존 동등 Tool이 있으면 그대로 사용한다.

| 자연어 (SOC-420517은 ID 예시, 실제 조회 데이터 없음) | chat_view | 내용·근거의 경계 | 불변식 |
| --- | --- | --- | --- |
| `SOC-420517 워크 내용 보여줘` | `CHAT_WORK` | Work 목적, 실제 진행 단계, 마지막 논의·결정과 이유, 미해결·다음 한 행동 | 기존 Ledger만 읽는다. 새 Work 생성/Focus 변경 금지 |
| `SOC-420517 워크 분석내용 보여줘` | `CHAT_ANALYSIS` | 이미 저장된 분석 사실 vs 가설 vs 확정 RCA, Evidence·Result ID·최신성; Call Graph 미확보면 미확인 | **재분석이나 Code/Log Provider 호출 금지** |
| `SOC-420517 워크 이슈 내용 보여줘` | `CHAT_ISSUE` | Work에 저장된 문제 현상, 기대 동작, 재현/조건, 영향과 원본 출처; live Jira 미조회면 반드시 표시 | 저장된 이슈 요약을 최신 Jira 원문처럼 포장 금지 |

**Tool/DTO 최소 계약:** `{query, work_id?, issue_key?, read_only:true, chat_view?}` → `work_id, issue_key, chat_view, state, user_summary, display?, source_refs, evidence_refs, source_freshness, read_only, provider_executed:false, writer_executed:false, next_action, first_blocker`. 실제 설치 스키마를 먼저 확인하여 동등 필드가 있다면 재사용하고, 존재하지 않는 action을 이미 있다고 주장하지 않는다. `user_summary`에는 충분히 읽을 수 있는 **일반 텍스트 500~1,000자 내외(정확한 길이는 메시징 플랫폼 한도에 맞춤)**로 Work/분석/이슈 구분·확인됨/미확인·근거·다음 행동을 담는다. `display`/기계 JSON에만 상세 정보가 있고 메신저에 3줄만 보이면 FAIL이다. 이 단계에서 rich card, 이미지·HTML·버튼 구현 요구하지 않는다.

**불확실성·무결성 가드:** 존재하지 않거나 접근권한 없는 Work는 `WORK_NOT_FOUND`/`PERMISSION_DENIED`로 구분하고 가짜 정보를 만들지 않는다. 동일 Jira에 Work가 복수이면 `WORK_CHOICE_READ_ONLY`와 짧은 후보를 제시, 무단 Focus 변경/Work 작성 금지. 조회와 수정/실행이 한 문장에 섞이면 `READ_WRITE_AMBIGUOUS`와 안전한 분리 안내를 제공하고 무단 실행 금지. 소스 코드/로그 원문·사내 비공개 경로·토큰을 채팅에 내보내지 않는다. **조회 시 Work writer, code-analyzer, l1sw-dev-log-analyzer-plus, Jira/Git write, 신규 분석 run 모두 0회**. 기존 Evidence를 READ하는 것과 새 분석 실행은 다르다.

**사내 E2E T1~T8 (별도 단독 문서 `L1_Workflow_ChatFirst_Agent_E2E_20261028.md`와 동일 조건):**

| 테스트 | Agent 측 실제 요청/확인 | PASS 기준 |
| --- | --- | --- |
| T1 | `SOC-420517 워크 내용 보여줘` | `CHAT_WORK`의 현재 단계/마지막 논의·결정/다음 행동이 **실제 채팅**에 표시 |
| T2 | `SOC-420517 워크 분석내용 보여줘` | `CHAT_ANALYSIS`, 확인된 사실·가설·근거 구분, 새 코드·로그분석 실행 0 |
| T3 | `SOC-420517 워크 이슈 내용 보여줘` | `CHAT_ISSUE`, 원본 출처/Jira 조회 여부와 미확인 데이터 구분 |
| T4 | `SOC-420517 워크 분석해줘` | T2와 달리 분석 실행 Intent를 **분류/계획**; 승인 없는 fixture 실제 실행 금지, 로그분석 명시 요청 정책 유지 |
| T5 | `SOC-420517 워크 분석내용 보여주고 로그분석해줘` | 혼합 조회/실행은 명시적으로 분리/안전 차단. 조회 요청만으로 로그 Provider 실행 금지 |
| T6 | Work 부재·권한 부재·동일 Jira 복수 Work | `NOT_FOUND`/권한 거부/읽기 전용 Work 선택지를 실제 상황에 맞게 구분, 생성/Focus 변경 0 |
| T7 | Agent 메시지 body vs MCP `user_summary`·`display` 비교 | 요약이 사용자 메신저에 손실 없이 전달, 기계 데이터만 있다면 FAIL |
| T8 | 모든 조회 전/후 Work/Provider/Writer/Repo 상태 readback | 조회 중 Provider 실행 0, Work 생성/수정·Jira/Git 쓰기·선택 상태 변경 0 |

**Gate:** 로컬 v1.6.57 targeted 25 PASS/CLI fixture 3 PASS는 사내 `MCP-READ/E2E=PASS`의 증거가 아니다. 먼저 설치본/loaded version·MCP route/schema/실제 메신저 렌더를 확인, 접근 불가하면 승인 fixture에서 기능 계약을 검증하고 **실제 SOC Work를 조회한 것으로 주장하지 않는다**. 문서 전체 I행 O16을 이 조회 PASS로 채우지 말고 §D 표의 M행(O04/O06)으로 독립 판정한다.

### MCP-01 [P0·최우선 사용자 기능 / O16] Agent 코드 상세 분석 + API Call Graph·시나리오·런타임 스택(근거 있을 때) + 결과/후속 피드백

**기존 발생 이력** (시점별 보고, 현재도 동일 원인인지 재확인):
- 10/13 전후: Workflow가 코드분석 요청을 과거 `l1-log-analysis` 쪽으로 잘못 라우팅하거나 실제 code-analyzer Runner/Evidence가 실패했다는 보고. 사내 MCP Wrapper를 고친 뒤에도 라우팅만 성공하고 실제 실행/근거 확보는 실패했다고 보고됨.
- 10/20~21: `CODE_ROOT_UNREGISTERED` (`smp1900`), `PROVIDER_MANIFEST_REQUIRED`, `code-analyzer` 실행 계약/루트 불일치; `provider-repair` 경로는 설계/이전 후보이며 운영 성공 미확인.
- 10/22~27: 코드 Provider 연결이 있어도 Agent MCP 실제 호출·결과 조회가 미검증. `code scope required`로 차단된 사례, API `RfProcNr::TuneRfCarrierFreq`의 소속/Scope 확인 필요. GitHub 401은 로컬 코드분석 필수 경로가 아니므로 별개로 분류.
- Work 단위 분석과 직접 Provider 분석을 구분한다. 과거 `SOC-417910` 또는 `SOC-420517`은 **읽기 전용 실제 Work 조회 시 존재·권한 확인 후** fixture로 사용 가능. 없으면 Work를 날조/자동 생성하지 않는다.

**사내 조사·구현**:
1. 설치된 `code-analyzer` VERSION, `bin/code-analyzer.py` 또는 실제 런처, `argv-json-v1`/입력 스키마, `root_id=smp1900`의 승인된 로컬 Root, Manifest에 선언된 action/실행계정/승인 Scope, Workflow Provider mapping을 **활성본에서** 확인한다. 레거시 v0.15.0/v0.15.1 이름은 역사적 기준일 뿐 실제 설치 상태가 아니다.
2. Agent 자연어 `SOC-417910 Work의 RfProcNr::TuneRfCarrierFreq 코드 흐름 분석해줘` 요청을 `intent=REQUEST_CODE_FACT` → `run_l1_fix_workflow` → `analyze-code` → 승인된 code-analyzer Runner로 매핑한다. Provider를 찾았다는 사실만으로 실행성공 처리하지 않는다.
3. Scope가 없으면 `CODE_SCOPE_REQUIRED`와 구체적인 **최소 안전 후보**(실제 로컬 인덱스에서 좁게 탐색한 함수/파일·root_id)를 `plan`으로 제시하고, 임의 레포 전체 검색·GitHub clone/API 토큰 경유 대신 현재 승인된 Git/P4 로컬 검색만 사용. 명백히 단일 Scope로 특정되면 정책이 허용하는 범위에서 자동 결정할 수 있으나 의도 불명/다중 후보는 사용자 질문 1회까지.
4. 필요한 승인된 코드 Root/Provider Manifest가 미등록이면 실환경 Root 존재/권한/중복검사 → 승인된 설정 Repair/등록 → Provider 실행 단계로 분리. Agent가 로컬 임의 파일을 직접 수정하는 범용 MCP shell Tool을 새로 열지 않는다.
5. **실행/조회 분리**: 제안 Tool 계약(기존 동등 action이 있으면 재사용) `analysis_request_plan`(read-only), `analysis_request_execute`(승인된 Root의 코드 읽기·로컬 output 작성, Work 원장 쓰기는 승인된 Writer만), `analysis_result_find`(Work ID/분석 Run ID/Issue ID별 검색), `analysis_result_read`(정확한 Result ID 상세), `analysis_followup_plan`(같은 결과 기준 후속 질문의 read/reuse/new_run 판정), `analysis_result_expand`(허용된 페이지·경로·조건별 상세 조회). Result의 `request_id, analysis_run_id, work_id, skill_id, skill_version, code_revision, root_id, scope_hash, executor, start/end, status, evidence_refs, result_ref, first_blocker`를 고정한다.
6. 원문 코드/사내 경로/로그 대신 1~5줄의 **함수 호출 관계·중요 판단 변수·근거 파일/라인의 안전한 식별자**를 Agent에 반환한다. 파일 전체 내용, SCM credential, 소스 그대로 반출 금지. Work 원장 Evidence는 `recorded=VERIFIED`인 경우에만 `EVIDENCE_LINKED`; 결과 보고서만 있으면 `RESULT_READY_EVIDENCE_PENDING`으로 구분한다.
7. 실환경 도구의 `analysis_result_find/read`가 Agent에 **실제로 노출되고 권한/서버 revision과 일치하는지** 검증. Provider 자체 실행 PASS라도 결과를 가져오지 못하면 `RESULT_READ_BLOCKED`, E2E PARTIAL.

**기본 테스트(반드시 관찰 결과 보존)**: 정상 단일 Scope, Scope 누락→안전 후보/차단, Root 미등록→승인된 복구, Provider Manifest 없음/실행 실패, Work 없는 경우 안전 종료, 완료 Result find→read, Evidence 없는 Result, GitHub API 401 발생 시 로컬 분석 유지. **기본 합격:** `REQUESTED→RUNNING→SUCCEEDED→RESULT_READ_VERIFIED` 및 근거 식별/실제 version; Work 연계 요청이면 `EVIDENCE_LINKED`까지 독립 표기. 성공 전 GitHub control을 선행 요구하지 않는다. 다음 확장 M1-a~M1-f는 **같은 O16의 상세 수용조건**이며 별도 MCP/이슈를 만들지 않는다.

#### MCP-01/O16 확장 ① — 4가지 분석 모드와 데이터 근거

**기본 모드는 `CODE_DETAIL`이며, 자연어에 API 호출 경로가 등장하면 `API_CALL_GRAPH`, 타이머·IPC·스케줄러·상태 전이가 등장하면 `SCENARIO_TRACE`를 우선한다.** 사용자가 요청한 여러 모드는 **동일 `analysis_run_id`에 mode별 결과**를 붙이거나 한 실행에서 안전하게 재사용한다. 실제 운영 Provider의 action/schema를 읽고 지원 여부를 검증한 뒤 구현하며, 아래 이름은 가칭이다.

| analysis_mode | 입력·분석의 중심 | Agent에 보여줄 것 | 반드시 구분할 한계 |
| --- | --- | --- | --- |
| `CODE_DETAIL` | 함수/클래스·인자·리턴·주요 조건·상태/변수 할당, Definition과 호출 위치 | `why/how`, 값 결정 지점, 조건 분기, 변경 전후 데이터 근거 | 코드가 없는 경로나 매크로 해석 불명은 `UNKNOWN` |
| `API_CALL_GRAPH` | 특정 API를 기준으로 caller→callee 다중 경로와 깊이 1~5(기본 3), 동적 dispatch 추적 | 경로별 caller/callee, 호출 위치·조건·도달성, 관련 파일/라인 | **정적 호출 가능성**이지 실제 실행 순서·runtime stack을 보장하지 않음 |
| `SCENARIO_TRACE` | IPC/Timer/Event/Callback/ISR/PHY IND·CMD, Work의 이벤트 시퀀스와 모듈 간 연결 | trigger→handler→condition→next event의 **비동기 시나리오**; 메시지 타입·상태 전이 | 비동기 경계는 일반 함수 스택처럼 단일 선형 Call Stack으로 표현 금지 |
| `RUNTIME_CALLSTACK` | **실제** crash dump, 스택 트레이스, profiler/symbolized trace가 제공되고 사용권한 검증된 경우 | 스레드/태스크·frame·주소 기호화 상태·시각·빌드 ID별 **관측된 스택** | trace/dump 없으면 `NOT_AVAILABLE_RUNTIME_EVIDENCE`, 정적 Graph로 대체하여 관측 사실이라 주장 금지 |

- 분석 범위를 `work_id?`, `root_id`, `code_revision`(commit/P4 CL 또는 확인된 빌드 식별자), `entry_symbol`/`api`, `direction=CALLERS|CALLEES|BOTH`, `max_depth`(기본 3, 최대 정책상 5), `max_paths`(예 기본 10), `build_config_id?`, `analysis_mode[]`로 정규화한다. **허용 루트·파일·심볼**로만 좁혀 탐색; 함수 이름 다중 후보면 정확한 네임스페이스·파일·signature를 제시하고 1회 선택 요청. repo 전체 무제한 검색 금지.
- 각 **호출 edge**를 `from_symbol`, `to_symbol`, `call_site_ref`, `call_type=DIRECT|VIRTUAL|FUNC_PTR|MACRO|CALLBACK|IPC|TIMER|INFERRED`, `guard_predicate?`, `compile_condition?`, `source_revision`, `evidence_ref`, `confidence=DIRECT_SOURCE|BUILD_RESOLVED|INFERRED|UNKNOWN`으로 구성한다. `VIRTUAL`/함수 포인터의 후보 다중 경로, 매크로·옵션 조건·동적 바인딩·재귀 루프는 제한 및 불확실성을 표시한다. 근거 없는 edge를 사실처럼 생성하지 않는다.
- `SCENARIO_TRACE`의 비동기 edge는 `initiator_event`, `enqueued_message`, `receiver_handler`, `execution_context`, `observed|inferred`, `correlation_evidence?`로 표현한다. 시간 순서가 로그로 확인되지 않으면 단순 가능 경로만 제시. `PHY IPC`, `L1 PAL Timer`, `HAL/RF`, `Front/MMCIF` 등은 실제 소스에서 확인한 구성요소만 포함한다.
- 1차 답변은 **최대 10줄 요약**(`상태`, `분석 모드`, `핵심 Call Path`, `조건/변수`, `근거/누락`, `result_id`, `추가 질문 가능`)으로 반환. 상세 Graph·분기표·MSC 변환은 로컬 `result_ref` 및 페이지 READ로 노출한다. Agent에 사내 코드 원문·비밀 경로·원본 trace를 직접 반환하지 않는다.

#### MCP-01/O16 확장 ② — Agent 후속 질의 및 피드백 루프

- Agent의 `그 API를 호출하는 상위 경로`, `두 번째 분기만 자세히`, `ENDC/ULCA 조건에서는?`, `해당 근거를 보여줘` 같은 후속 요청은 **이전 `analysis_run_id`/`result_id`와 동일 `work_id`**에 매핑한다. 최초 조회가 실패한 경우 연결되지 않은 결과를 가정하지 않는다.
- 조회 계약(제안): `analysis_result_find(work_id|request_id|time_range)` → `analysis_result_read(result_id,section?,cursor?)` → `analysis_followup_plan(parent_result_id,question,requested_mode?,path_id?,scope?)` → `analysis_result_expand(parent_result_id,selected_path_id|branch_id|symbol_id,cursor?)`. 기존 스킬에 동등 READ가 있으면 재사용하고 Tool 중복 등록 금지.
- 후속 질의 결정은 `REUSE_EXISTING_EVIDENCE`, `EXPAND_EXISTING_RESULT`, `NEW_ANALYSIS_REQUIRED`, `BLOCKED_SCOPE_OR_REVISION`, `RESULT_EXPIRED_OR_MISSING` 중 하나로 명시. 결과 재사용 시 **코드 리비전·루트·스코프 해시·권한 동일성**을 확인하고, 변경됐으면 재분석 계획을 반환. 서로 다른 Work/권한의 Result ID 재사용 금지.
- 동일 `request_id` 재전송은 중복 Runner 생성 없이 기존 실행/결과 참조 반환(idempotent). 새 코드분석이 필요한 경우 새 `child_run_id`, `parent_result_id` 및 변경된 Scope를 연결하고 비용/권한을 재검사한다. 사용자 입력 1회에 가능한 분석·검증·응답을 모아서 수행하고, 모호성 해결 외 불필요한 질문 금지.
- **Agent 피드백 예시(가상의 형식·코드분석 결과가 아님)**:

```text
ANALYSIS_FEEDBACK_V1
state=SUCCEEDED mode=API_CALL_GRAPH work=SOC-EXAMPLE
path=CallerA -> ManagerB -> TargetApi [STATIC_POSSIBLE]
branch=condition_X ; edge_confidence=DIRECT_SOURCE
result_id=ANALYSIS-EXAMPLE evidence=3 missing=runtime_trace
followup=두 번째 호출 경로를 분석해줘 | 조건 변수가 결정되는 함수는?
```

- 사용자 후속 질문에는 `same_work=true`, `parent_result_id`, `reuse_status`, `new_run_created`, `relevant_paths`, `evidence_count`, `confidence`, `first_blocker`, `next_action`을 Agent에 간결히 표시. 사내 Agent의 출력 길이 제한(10줄/숫자 중심)을 유지한다.
- **결과의 근거 신뢰도는 단계별**: `SOURCE_VERIFIED`(정적 코드/빌드 기반), `RUNTIME_OBSERVED`(실제 dump/trace·build 매칭), `INFERRED`(상관·가능성 추론), `INSUFFICIENT`(증거 부족). `RUNTIME_OBSERVED`는 소스 호출 경로만으로 부여 불가. 이벤트/타이머 비동기 연결은 관측 신호가 없으면 `INFERRED`로 표시.
- 후속 질문에서 이전 결론을 수정할 경우 `analysis_revision`, `supersedes_result_id`, 변경 이유를 기록하고 원본 Result/Work Evidence는 덮어쓰지 않는다. 로컬 원본·허용된 Evidence만 보존, Dropbox에는 비민감 진행 맥락만 기록한다.

#### MCP-01/O16 확장 ③ — 단일 E2E 수용 시험 (M1-a~M1-f, 중복 리포트 금지)

| Test | 사용자 Agent 요청 | 검증 기준 |
| --- | --- | --- |
| M1-a 상세 코드분석 | `Work SOC-420517의 main_dac_path가 tx_dac_path와 달라지는 코드 조건 분석해줘` | 실제 Work/심볼 존재 확인 → CODE_DETAIL 실행 → 조건·값 할당·파일/라인 근거 READ; 없으면 정확한 BLOCKED, 허위 분석 금지 |
| M1-b 상위/하위 Call Graph | `TargetApi의 caller→callee를 깊이 3으로 추적해줘` | 다중 후보·함수 포인터/가상함수/컴파일 옵션 구분, 경로별 edge evidence·confidence, 페이지 조회. 정적 Graph를 런타임 스택으로 표시 금지 |
| M1-c 비동기 L1 흐름 | `TX ON 요청 이후 HAL→PHY IPC→Timer→RF 동작 흐름 분석해줘` | 실제 확인된 IPC/Timer 경계를 async edge로 표시하고 조건·전후 상태를 근거와 연결. 근거 없는 순서 단정 금지 |
| M1-d 런타임 Stack 요청 | `실제 실행 시 Call Stack을 보여줘` | **두 독립 검증**: (음성/차단) 실제 dump/trace가 없을 때 정확히 `NOT_AVAILABLE_RUNTIME_EVIDENCE`로 차단하면 `test_result=PASS`, `operational_state=RUNTIME_EVIDENCE_MISSING`; (양성) 승인된 trace와 build/revision 매칭이 실제 있으면 RUNTIME_OBSERVED 호출·READ 확인 후에만 `operational_state=VERIFIED`. 음성 테스트 성공이 런타임 분석 기능 E2E 성공을 의미하지 않는다. 로그분석은 명시 요청에만 실행 |
| M1-e 후속 질의 연속성 | `두 번째 경로만 더 자세히` → `분기 변수가 최초 설정되는 곳은?` | 기존 Result ID/Work 유지, 동일 revision/scope 확인, 재실행 억제 및 expand; 필요한 때만 child_run 1회, Agent 답변 실제 READ |
| M1-f 안전·실패 | 다른 Work Result ID/Scope·revision 불일치, Evidence 누락, 권한 거부, 0건 조회, Tool 미노출, 비동기 미해결 | 의도한 **차단·경고가 정확히 재현되면 해당 negative test_result=PASS**. 실제 Tool/근거/서비스 검증 상태는 `operational_state=BLOCKED_*|NOT_EXPOSED|EVIDENCE_MISSING`으로 별도 유지. reason_code·first_blocker·후속 행동 출력, 원본/정책 보존, 전체 운영 E2E PASS로 승격 금지 |

**M1 전체 판정:** 모든 시험·모드에 `test_result=PASS|FAIL|BLOCKED|TIMEOUT|NOT_RUN`과 `operational_state=VERIFIED|NOT_INSTALLED|NOT_EXPOSED|ROUTED_ONLY|RESULT_READ_BLOCKED|RUNTIME_EVIDENCE_MISSING|PENDING_APPROVAL|UNKNOWN`을 **각각** 기록한다. 예: `M1-d negative test_result=PASS, operational_state=RUNTIME_EVIDENCE_MISSING`; `M1-f forbidden cross-work result test_result=PASS, operational_state=BLOCKED_BY_POLICY`. 다만 확인한 상태가 위 기본 enum에 포함되지 않는 경우 `operational_reason`으로 더 좁게 표시한다. Aggregation에서 negative test PASS를 기능 전체 성공으로 포함시키지 않는다. `followup_e2e`는 **실제 같은 Agent 대화의 최소 2회 후속 READ**가 성공해야 PASS. 여기서 사외 Agent '재확인 1회'는 위 §D의 초기 1턴+후속 2턴이 있는 **단일 검증 세션**의 횟수이며, 사용자 발화가 딱 한 문장이라는 뜻은 아니다. 채널 미노출/권한 불가면 `AGENT_CHANNEL_UNAVAILABLE`로 BLOCKED. 코드 수정·자료 접근이 불가하면 정적 계약/fixture 시험과 Agent 실호출을 분리한다. **최종 정본 issue_id는 O16 하나**, 최종 보고서 I행에서만 종료 판단한다. 이 추가 범위가 O17~O19 및 Updater/Job/Git의 기존 완료 조건을 약화하지 않는다.

### MCP-02 [P0·Updater 읽기 우선 / O17] Agent에서 실제 Skill-Updater 변경 스킬명·버전 목록 제공

**문제:** 과거 `skill-updater` 실행이 `SUCCESS / CURRENT / updated=0`로 보여도 Job 결과는 없거나, 자기 업데이트가 `STAGED_NOT_INSTALLED`이고 실제 Agent 활성 버전과 다른데 메신저에서는 어떤 스킬이 바뀌었는지 판단할 수 없었다. 설치 완료와 실행·배포 결과를 분리해야 한다.

**사내 조사·구현**:
1. `run_skill_updater`가 실제 반환하는 구조화 summary, `install_journal`/per-skill receipt, staging/Bootstrap receipt, 실제 canonical `VERSION`과 Agent/서비스 **loaded version**을 확인한다. 없는 receipt를 추론하지 않는다.
2. Updater 완료/실패 후 읽기 전용 `skill_update_runs_find(date_range|latest_n)` **및** `skill_update_result_read(run_id)` (또는 동일 의미의 기존 Tool)을 구현·노출한다. `find`는 Agent가 `run_id`를 모르는 **오늘(KST), 최근 N회, OS 예약 실행** 조회에 필수이며 `run_id, started_at_kst, overall_status, updated_count, source=manual|scheduled, next_cursor`를 반환하고 제한된 최신 기간·권한을 적용한다. `read`는 특정 run의 설치/로딩 상태·receipt를 검증한다. Agent의 `오늘 업데이트된 스킬 목록`은 KST 날짜 구간→`find`→각 `read`(페이지 병합) 순으로 조회하며 사용자에게 run_id 선입력을 요구하지 않는다. 조회 자체는 updater 실행을 유발하지 않는다. 반환 계약: `run_id`, `started_at_kst`, `ended_at_kst`, `updater_version_executed`, `bootstrap_phase`, `overall_status`, `updated_count`, `staged_count`, `failed_count`, `skipped_count`, `items[]`(skill_id, old_installed_version, requested_version, installed_version, loaded_version, action, status, reason_code, install_receipt_ref), `next_action`. 대량 항목은 페이지 조회. 실제 raw logs 외부 반환 금지.
3. MCP/Agent 응답 기본 포맷은 **변경된 스킬만 먼저** 한눈에 보여준다. `UPDATED`는 설치 receipt+활성 버전 일치, `STAGED`는 설치 전, `CURRENT`는 변경 없음, `FAILED`는 실패, `UNVERIFIED`는 버전 확인 불가. 팀 전체 변경 없으면 `변경된 스킬 없음 (0건)`; `updated_count`가 0이라는 이유로 Job 성공이나 모든 스킬 최신을 주장하지 않는다.
4. 자기 업데이트 v0.5.45는 별도 외부 Bootstrap `receipt=VERIFIED` 이후 Agent가 로드한 버전까지 확인해야 설치 성공. 기존 손상 v0.5.44 pending의 승인된 격리 전 `cycle/apply` 테스트 금지, 자동 정책 전환 금지.
5. 예시 출력(가상의 값, 실제 성공 보고 아님):

```text
SKILL_UPDATE_RESULT_V1
run=UPD-EXAMPLE status=PARTIAL updated=1 staged=1 failed=0
UPDATED: code-analyzer 0.15.0 -> 0.15.1 (installed=0.15.1 loaded=0.15.1)
STAGED: skill-updater 0.5.44 -> 0.5.45 (install=NOT_RUN)
blocker=EXTERNAL_BOOTSTRAP_REQUIRED
```

**테스트:** Agent가 run_id 없이 "오늘" 질의, KST 날짜경계/예약 실행 포함/오늘 실행 0건, 최근 N개 find→read, 2종 이상 변경, 일부 실패, 자기 STAGED, Bootstrap FAILED, Canary verified와 Agent loaded mismatch, old-version missing, 페이지 조회, restart 후 run 검색·결과 READ. **합격:** Agent 요청 `오늘 업데이트된 스킬 목록과 설치 버전 알려줘`에 정확한 `skill_id old→installed`와 `FAILED/STAGED` 사유를 반환. Updater 호출 직후 결과조회와 별도의 `job-list` 실행결과도 연결하지만 동일 성공으로 합치지 않는다.

### MCP-03 [P1 / O18] 사외 Agent → job-list → 승인된 사내 MCP Provider/Tool 수정 요청

**과거 차단 이력**:
- Job-list v0.4.24 배포·설치는 보고됐지만 `JOB_CATALOG_UNREADABLE`와 **MCP Job READ 3종 Tool 미노출** 때문에 원격 `catalog/queue/result` 조회 실패. v0.4.25는 문서 기준 후보이며 **실설치 버전 UNKNOWN**. `analysis find` 자연어 Q3 FAIL / scope Q6 FAIL, Q8 Job READ BLOCKED (R007).
- Q1 운영 revision/실행 호스트 UNKNOWN; 검색 단독 Q2/ID 경계 Q7은 PASS 보고. `Updater SUCCESS`는 예정 Job이나 MCP Provider 적용 성공 증거가 아님. 과거 MCP/Job-list 수정 완료 보고와 운영 restart·Agent Tool 노출은 별개.
- 사외 Agent에서 직접 사내 스크립트를 패치하거나 임의 shell을 열 수 있었다는 증거는 없다. **새 Tool 배포 및 재시작은 실제 권한·human gate가 있어야 한다**.

**필수 실행/구현 단계**:
1. `whpark-mcp`의 **실제 서버 저장소·revision·호출 계정**, `/tools/list` 또는 동등한 MCP tool list, Agent cache, Tool schema/권한/라우팅을 확인. MCP 소스와 `job-list` Catalog/Runner/Worker는 별도 시스템으로 읽는다.
2. 우선 **Job READ 3종**(실제 이름은 기존 명명 재사용): catalog/query, queue/status, result/read. `job_request_plan`→`job_request_enqueue`→`job_status`→`job_result`를 구분하고 읽기 동작이 job 실행을 유발하지 않도록 한다. disabled/unsupported/permission_denied/tool_not_exposed/unknown_job/runner_unavailable 등 reason을 반환한다.
3. `mcp-provider-repair` (가칭, **Job 종류**)의 승인된 등록을 검토한다. **허용된 도구·Provider 등록/설정 계약 보정만** 허용하며, 요청 자유 텍스트를 임의 파일쓰기/OS 커맨드/레포 수정/인증 변경으로 실행하는 범용 Job은 금지한다. 예: `provider_contract_sync`, `analysis_read_tools_register`, `updater_bootstrap_route_check`, `job_read_tools_enable`, `workflow_github_route_register`.
4. 새 작업은 `plan` 단계에서 `requested_change, affected_tools, provider_id, allowlisted_paths, current_revision, proposed_diff_digest, preflight_result, permission_gate, dry_run_commands, verification_plan, rollback_ref`를 만든다. **같은 job_request_id의 재전송은 동일 plan/receipt를 반환**해야 하며, 여러 worker 중복 적용 금지.
5. 사외에서 `MCP Provider 연결 수정해줘` 요청 시: Agent는 먼저 기존 등록·상태를 조회 → Job plan 제안/위험 분류 → 통합 승인표 C++의 **G1에서 해당 diff·Provider·host·reload를 명시 승인받은 뒤** 적법한 Runner에서 승인된 diff만 적용 → lint/schema/unit test → 필요한 서비스 reload/restart → 실제 **새 tool list 노출 + 동일 Agent identity에서 read-call PASS** → 전후 revision/rollback/receipt 제공. 사내 승인이 필요한 작업은 사외 요청 한마디만으로 권한이 생기지 않는다.
6. **안전·실패격리:** 허용하지 않은 Provider `l1-log-analysis` 재등록/fallback 금지(D-029). 활성 `l1sw-dev-log-analyzer-plus`와 `code-analyzer` 계약을 별개 관리. pending/job 원본·실패 receipt 보존. 서비스 restart 실패→검증 불일치면 승인된 rollback. 잠금, scope, 실행 identity, code digest, service health, Agent cache refresh까지 확인한다.
7. 당장 Job READ/실행 경로가 없다면 **사내 LLM에서 기존 `whpark-mcp`와 job-list를 먼저 직접 보완/회귀**해 활성화한다. Agent 원격 Job 호출 테스트는 Tool 노출/권한 확보 후에만. 연결되지 않은 상태를 `REMOTE_MCP_PATCH_SUPPORTED`로 표시하지 않는다.

**테스트:** catalog 검색, 이름/alias mismatch, queue/receipt 조회, 올바른 Provider 등록 계획, 의도치 않은 레포 파일 변경 거부, 무승인 apply 거부, dry-run 0 writes, 재시도 idempotent, 동시 Job lock, reload 실패 rollback, 새로운 Agent 대화에서 tool visible, 실행 결과 상세 READ, 실수로 retired Provider 추가 시 실패. **합격:** 사외 Agent가 요청→최소 승인→job-list 작업→실제 MCP Tool 등록/Provider 라우트 활성화→result READ까지 구분된 receipt를 받는다. **가능한 환경에 한해** 실제 구성 적용 PASS.

### MCP-04 [P1 / O19] Agent → l1-fix-workflow → l1-github 제어 (Workflow GitHub Control)

**목표:** 자연어로 Work의 코드/문서 변경 흐름을 유지하면서 Git status/branch/commit/push/PR 제어 및 결과를 조회한다. 직접 GitHub API로 토큰을 요구하거나 `l1-github`를 우회하는 일반 shell을 새로 열지 않는다.

**기존 사용자 확정 정책**:
- 사용자가 지정한 Work/Repo 우선. `l1-github` 역할 매핑: `source_code=smp1900`, `group_skills=l1sw-skills`(Fork), `personal_skills=skill-updater`(사외), `work_docs=l1-workspace`, `knowledge=l1sw-dev-knowledge`. **`workflow_source`/`l1-fix-workflow` 저장소 역할 폐기**. 리포지토리/인증·전송 가능 여부는 호스트에서 검사한다.
- Linux 소스 A=`/home/whpark/Project/smp1900`, B=`/home/whpark/Project/smp1900-worktrees`. B는 **고정 단일 worktree 경로**이며 branch명의 새 하위 폴더를 만들지 않는다. 전체 최대 2개, 동일 branch 중복 checkout 금지; 브랜치는 각 폴더 내에서 상황 따라 변경한다. 실제 경로가 다르면 추측해 작업하지 않는다.
- `upstream` 직접 push 금지. 승인된 Fork/`origin` 및 PR 사용. **dirty/staged/untracked는 일괄 쓰기 차단 조건이 아니라 action별 검사 입력**이다. 충돌(conflicted)/진행 중 merge·rebase는 Git 쓰기 전체 차단. `diverged`는 자동 merge/rebase/push를 금지하되 승인된 로컬 commit 검사는 별도 판단한다. 자동 `reset/clean/stash/force-push` 금지. 명시 승인 전 Git write, 외부 업로드 금지.

**Git action별 안전 매트릭스 (v1.6, 이 표가 단일 dirty 일괄 차단 문구보다 우선)**:

| action | 허용 전제 / 확인 | 차단 / 다음 행동 | receipt |
| --- | --- | --- | --- |
| STATUS/PLAN | 모든 dirty 상태에서 READ만. status의 staged/unstaged/untracked/conflict/diverged 및 diff digest 관찰 | Repo/Work/접근권한 불일치 시 READ 차단 | observed HEAD + state digest |
| BRANCH_SWITCH | clean tracked tree, staged 0, branch checkout 충돌 untracked 0, worktree 중복 checkout 0. 승인된 target/expected_head 일치 | dirty·staged·untracked 충돌·conflict·merge/rebase → SWITCH_BLOCKED; 자동 stash/clean 금지 | before/after HEAD/branch |
| COMMIT | **정상 dirty/staged 상태 허용**: 승인된 파일 allowlist(경로/개수/추가·수정), diff digest, staging snapshot, expected_head, work_id 및 G2 approval 모두 동일. untracked는 명시 허용 목록의 파일만 add하고, 무관한 untracked는 건드리지 않음. 필요 시 승인 파일만 stage, 검증 후 commit | 승인 외 staged 파일/변경 경로, HEAD·diff digest 변화, conflict/merge/rebase → STALE_PLAN/COMMIT_SCOPE_BLOCKED. dirty라는 이유만으로 차단 금지 | commit SHA + 승인 파일 목록 digest + before/after HEAD |
| PUSH | commit 완료/대상 ref 및 expected_head 고정, origin/Fork remote 및 ahead-behind·fast-forward/보호 정책·승인 ref 확인. 로컬 미커밋 변경은 그 자체가 PUSH 차단 사유가 될 수 있으며 정책별 기록; push 대상 ref는 커밋 이력만 전송 | diverged/non-fast-forward/원격 HEAD 변경/비허용 remote·force 요구 → PUSH_BLOCKED; 무단 재기준/force 금지 | remote/ref + pushed SHA + receipt |
| PR_CREATE/UPDATE | 원격 존재하는 승인 source branch/target branch, 최소 diff/권한 검증, G2 승인, GitHub 원격 성공 확인 | 실제 push 또는 권한 없으면 PR_PENDING/PENDING_APPROVAL, 임의 URL 생성 금지 | PR URL/id + source/target + response proof |
| WORK_DOCS_PUBLISH | work_docs 별도 G3 승인, Dirty/DIVERGED 작업 트리 결정 후 안전한 Git 경로 | 무단 push, 자동 merge/덮어쓰기 금지 | document id + remote commit + verified rendered URL |

**commit 계획의 불변 데이터:** `plan_id`, `work_id`, `repo_role`, `workspace_id`, `branch`, `expected_head`, `allowed_files`, `staged_files`, `untracked_allowlist`, `diff_digest`, `remote_target`, `approval_receipt`. apply 직전 동일한 repository snapshot 재조회. *Diff digest*는 staging 전/후 승인 범위를 구분해 기록한다. 단독 Git 조회는 승인이 없어도 가능하고, commit 승인으로 push/PR 승인까지 자동 확대하지 않는다.

**MCP 호출 설계**:
1. Agent는 `run_l1_fix_workflow`로 해당 Work/intent를 확인. Git 관련 요청을 `DELIVER` action으로 분류하여 설치된 `l1-github` Provider에 `repo_role, work_id, cwd/workspace=A|B, branch, expected_head, requested_action`을 전달한다. 사용자 발화에 리포지토리/branch 생략 시 Work의 기존 바인딩으로만 해석하고 모호하면 read-only plan을 반환한다.
2. **읽기 전용** API (가칭): `workflow_git_status`(Repo role/branch/dirty/remote ahead-behind/PR 정보), `workflow_git_plan`(변경 예정 파일, SCM 상태, 민감 경로 제외, merge/rebase 여부, commit message/target branch, expected_head, repo permissions, diff digest, push guard, rollback plan). `git diff --stat` 등 요약만 Agent로; 코드 원문/토큰/절대경로 노출 금지.
3. **승인된 쓰기** API (가칭): `workflow_git_apply`는 `plan_id+digest+expected_head+approval_receipt`가 모두 일치할 때만 **allowlisted action**(local commit, allowed branch switch, origin/Fork push, PR open/update, 명시 승인된 `work_docs` 게시)을 수행한다. 재요청 중복 방지, HEAD/승인된 diff·staged scope 변경 시 STALE_PLAN 차단; 의도한 dirty→staged 상태 변화는 승인 plan 내에서만 허용. 문서 Dirty/DIVERGED은 사용자의 선택 없이 merge/force/overwrite하지 않는다.
4. 등록된 Work의 code change Evidence/문서 Dirty와 Git HEAD를 연결하되 Work 재개 `WORK_NOT_FOUND`면 Git 쓰기를 시작하지 않는다. 코드 분석 자체는 GitHub control 성공을 선행조건으로 삼지 않는다. `l1-workspace` 문서의 GitHub Markdown/MSC 링크는 실제 push와 렌더 검증 후만 제공한다.
5. 사용자 자연어 E2E:
   - `SOC-417910 Work의 현재 branch/status 알려줘` → READ만.
   - `이 Work 변경사항 commit 계획 보여줘` → PLAN (서버 쓰기 0).
   - `승인한 plan대로 로컬 commit 하고 origin에 push해줘` → 명시 approval/검증 후 실행, 기록.
   - `PR 생성해줘` → 승인된 repo/target/source, upstream/dev 포함 여부와 Fork guard 확인 후 실행.
   - `이 Work 문서를 l1-workspace에 게시해줘` → dirty/diverged 해결 게이트 후 **C++의 G3 문서 게시 승인**, Git URL 반환.
6. **GitHub 401 분리:** `code-analyzer`가 승인된 로컬 Git/P4 Root에서 코드를 읽는 데 GitHub API 인증은 필수 조건이 아니다. 원격 Repo 조작의 인증 실패는 `GIT_AUTH_REQUIRED`로만 분류하고 비인가 token retry/권한 우회 금지.

**테스트:** status/read, 잘못된 repo_role 거부, branch 미바인딩 안전 차단, action별 matrix(branch-switch clean/충돌, commit에 승인된 dirty/staged 허용, staged 외 파일 및 untracked 범위 위반 차단, push diverged/non-fast-forward 차단), 다른 worktree가 같은 branch checkout 중인 경우, 예상 HEAD 변경, Fork origin vs upstream guard, 중복 apply, plan 권한 만료, 승인된 local commit/PR fixture(격리된 허용 repo, 실제 remote publish는 별도 승인), Workflow→Git result READ, Work/문서 Evidence 연결. **합격:** 동일 Agent 대화에서 실제 `l1-github` Provider가 실행·근거를 반환하고 Git write에는 명시 승인/allowlist/HEAD 재검사와 receipt가 있다. `PLAN`을 commit/PUSH 성공으로 주장하지 않는다.

### MCP 공통 규격: 실행 결과/보고·인증·버전

- **통합 원샷 baseline:** `actual_install_version`, `agent_loaded_version`, `mcp_loaded_revision`, `tool_schema_version`, `provider_manifest_digest`, `runner_identity`, `agent_tool_visible`, `agent_call_verified`. 각각 단독 측정; 개발 ZIP 내부 버전은 구분.
- **공통 response envelope** (`MCP_RESPONSE_V2`는 제안 버전이며 서버 등록 전 기존 스키마가 기준):

```json
{
  "schema_version": "MCP_RESPONSE_V2",
  "request_id": "req-example",
  "action": "analysis_result_read",
  "state": "SUCCEEDED",
  "execution_verified": true,
  "result_read_verified": true,
  "actual_skill_version": "<installed-version>",
  "agent_loaded_version": "<active-version>",
  "evidence_refs": ["<redacted-ref>"],
  "analysis_mode": "API_CALL_GRAPH",
  "analysis_run_id": "<run-id>",
  "parent_result_id": null,
  "edge_evidence_level": "SOURCE_VERIFIED",
  "followup_state": "READY",
  "first_blocker": "NONE",
  "next_action": "NONE"
}
```

- **시험 vs 운영 상태 직교 계약(v1.6):** 개별 case의 `test_result`(`PASS|FAIL|BLOCKED|TIMEOUT|NOT_RUN`)와 실제 기능의 `operational_state`(`VERIFIED|NOT_INSTALLED|NOT_EXPOSED|ROUTED_ONLY|RESULT_READ_BLOCKED|RUNTIME_EVIDENCE_MISSING|PENDING_APPROVAL|UNKNOWN`)를 독립 기록한다. `expected_blocker`, `observed_reason`, `test_kind=POSITIVE|NEGATIVE|FIXTURE`, `evidence_at`, `channel=LOCAL|MCP|REAL_AGENT`, `artifact_before_sha`, `artifact_after_sha`를 추가. 예를 들어 접근 거부 시험 `test_result=PASS`는 권한 통제가 정상이라는 뜻이지 분석 Provider 운영 성공을 뜻하지 않는다. 보고표 A~N의 옛 `status=PASS/FAIL/BLOCKED/PARTIAL`는 **표시용 종합 판정**으로만 남기고 근거 있는 두 필드를 필수 입력한다.
- **불일치 방지:** 요청 Accepted, Tool Exposed, Runner Executed, Report Read, Evidence Linked, Deployment Verified는 모두 독립 상태. RUNNING/QUEUED/ROUTED/PLAN만으로 E2E PASS 불가.
- **민감정보:** 코드 원문/로그 전체/Token/개인 경로/인증설정/사내 내부 URL을 Agent 응답 또는 Dropbox에 복제하지 않는다. 허용된 범위의 검증 식별자·상대 경로·해시·상태만 제공.
- **Agent UI:** 사용자에게는 성공/실패, 스킬명·버전, Work/Job/Result ID, 근거 링크(정책상 허용하는 경우만), 최초 blocker, next를 10줄 내로. 긴 상세는 사내 로컬 결과 MD와 READ API로 조회.

### 신규 기능 E2E 최종 게이트

| Gate | 사용자 자연어 | 정상 경로 | 성공 기준 | 문제 연계 |
| --- | --- | --- | --- | --- |
| M1 | `SOC-417910 코드/API Call Graph/시나리오 분석해줘; 이어서 두 번째 경로 분석` | Agent→Workflow→code-analyzer→M1-a~f→find/read/expand/followup | CODE_DETAIL, API_CALL_GRAPH, SCENARIO_TRACE, RUNTIME_CALLSTACK의 증거별 판정 + 동일 Work 후속질의 2회 E2E; 코드분석 결과 판정은 I행 단일 | O16 (관련 O03/O04/O10) |
| M2 | `이번 업데이트된 스킬 목록/버전 알려줘` | Agent→Updater receipt→read result | 실제 UPDATED 이름·old→installed, STAGED/FAILED 별도 | O17 (관련 O03/O14) |
| M3 | `MCP Provider 연결 수정 요청해줘` | Agent→job-list plan→승인→Runner→MCP reload→result | 승인된 작업의 loaded revision, Agent tool visible/call verified | O18 (관련 O04/O09) |
| M4 | `이 Work GitHub 상태/commit/PR 진행해줘` | Agent→Workflow DELIVER→l1-github→Git receipt | read PASS와 승인 write/Push Guard 결과 구분 | O19 (관련 O01/O04/O10) |

- **정본 식별자 확정(Q-003):** MCP-01→O16, MCP-02→O17, MCP-03→O18, MCP-04→O19는 이미 `ISSUES_r0005.paper`에 OPEN으로 등록돼 있다. 과거 가칭 N01~N04는 폐기된 문서 내 임시 식별자이며 사내 결과에 사용하지 않는다. 새로 재현된 **독립 결함**만 기존 ID와 중복 확인 후 새 ID를 검토한다.
- M1~M4가 서로 다른 권한으로 막히면 독립 항목은 수행한다. 전부 검증된 것으로 위장하지 않는다.

## C++. 통합 승인 게이트 — 한 번에 제시하되 권한 범위별 승인 유지 (Q-005)

**한 회차에서 계획 전체의 승인 필요 항목을 한 번의 요약표로 묶어 제시한다.** 그러나 승인 주체·대상·위험이 다른 행위는 한 번의 포괄적 동의로 자동 허가하지 않는다. **읽기/안전한 로컬 fixture만 할 때 추가 승인 요청 0건**, 모든 단계가 실행 가능한 경우 소유자 판단에 따라 아래 **최대 4개 권한 그룹**으로 묶어 결정한다(그룹별 구체 대상/해시/기간/호스트 포함).

| gate_id | 승인·실행 범위 | 한 번의 요청에 묶는 방법 | 미승인·실패 처리 |
| --- | --- | --- | --- |
| G1 운영 구성/설치 | 허용 ZIP 반입과 SHA 확인, 정확한 파일·범위가 지정된 손상 pending 격리·복구, Bootstrap 설치, MCP Provider patch·reload/restart, Job plan 적용 | **계획/대상/rollback을 모아 통합 승인표 1개** 제출; 실제 각 행위를 승인받은 범위 내에서만 순서 실행. 자동 정책 변경은 추가 명시 범위 승인 필요 | 해당 작업만 `BLOCKED_APPROVAL`; MCP route·schema READ는 계속 |
| G2 Git 쓰기 | Work/repo/branch/HEAD가 고정된 commit, origin Fork push, PR 작성/수정 | 별도 **Git 작업별 plan_id+digest+expected_head+approval_receipt** 및 Push Guard; G1 동의로 Git 쓰기 허가하지 않음 | 미승인 `READ/PLAN`만 가능, `STALE_PLAN`이면 새 승인 |
| G3 문서 게시 | `work_docs=l1-workspace` 게시·원격 공유/외부 공개 | 별도 정확한 repo·대상 문서·destination 승인; Git gate에도 해당 항목을 추가로 확인 | 승인 전 로컬 문서만 유지, URL 발행 완료 주장 금지 |
| G4 Cleanup 파괴 작업 | 파일 quarantine/삭제, DB vacuum, 보존기간 변경 | **별도 대상 목록·원본 보존/복원 계획** 승인. dry-run은 별도 쓰기 없이 가능 | 승인 전 삭제 0건 유지; 실행 시에도 되돌리기 기준 필수 |

승인 질의는 가능하면 **G1~G4의 모든 예상 내용을 단일 승인 요청서로 사전 제시**하고, 각 그룹에 별도의 응답/receipt를 받는다. 운영상 반드시 별도 단계/소유자가 승인해야 하는 경우에는 그 보안 절차를 생략하지 않는다. 게이트 승인 결과와 테스트 성공은 서로 다른 증거다. 한 그룹이 BLOCKED여도 독립 READ/로컬 시험은 계속한다.

## C+++. 사외 Agent 사용자 피드백 최종 UX (O16 세부 강화)

**기본 사용자 요청**: `SOC-420517에서 main_dac_path가 tx_dac_path와 다른 이유를 코드로 분석하고, 관련 API Call Graph를 깊이 3으로 보여줘.`

**정상 응답 최소 계약(가상 예시 아님 — 형식 규칙)**: 요청 접수 여부와 실제 `RUNNING|SUCCEEDED|PARTIAL|BLOCKED`를 구분하고, 분석 모드/Work/기준 revision, 핵심 결론 최대 3개, `caller→callee` 경로·조건, 소스 기반인지 런타임 관측인지, Evidence 개수·Result ID, 후속 질문 가능 예시 1~2개를 보여준다. 비밀 소스 원문 대신 허용된 요약·식별자를 반환한다.

**후속 사용자 요청**: `아까 분석한 두 번째 경로를 자세히`, `이 API 진입 전 변수 설정 위치`, `이것이 런타임에서 실제 발생한 경로야?`. Agent는 직전 `result_id`가 유효하면 재사용/상세 페이지 READ를 우선하고, 없거나 근거가 부족하면 이유와 새 분석이 필요한 범위를 말한다. 2회 연속 후속 질문 동안 Work ID·revision·Root/scope 권한이 유지되는지 확인한다. 매 질문에 분석 전체를 다시 실행하는 무한 ping-pong 금지.

**표시 예시(가상, 실제 사내 분석 아님)**:

```text
CODE_ANALYSIS_RESULT_V1  status=SUCCEEDED  mode=API_CALL_GRAPH
work=SOC-EXAMPLE  revision=REV-EXAMPLE  analysis_run=RUN-EXAMPLE
path1=CallerA -> ManagerB -> TargetApi (STATIC_POSSIBLE)
condition=condition_X; evidence=3(SOURCE_VERIFIED); runtime=NOT_OBSERVED
result_id=RESULT-EXAMPLE   next=두 번째 경로 자세히 분석해줘
```

**Agent 응답이 실패할 때의 사용자 안내**: `코드 분석이 실패했습니다`처럼 뭉뚱그리지 말고 `CODE_SCOPE_REQUIRED`, `ROOT_UNREGISTERED`, `PROVIDER_MANIFEST_REQUIRED`, `RUNNER_FAILED`, `RESULT_READ_BLOCKED`, `NOT_AVAILABLE_RUNTIME_EVIDENCE`, `STALE_RESULT`, `PERMISSION_DENIED` 중 실측에 해당하는 reason을 제시한다. 코드 분석이 성공했지만 Agent 상세 조회가 막힌 경우 `PARTIAL/RESULT_READ_BLOCKED`로 구분한다.

## C++++. Guided Workflow 초보자 목적별 라우팅 — G01~G18 진단→최소 보완→회귀 (v1.6)

**목표는 초보자가 스킬명·Provider/CLI/JSON을 몰라도 목적을 말하면 Work 현재 단계와 안전한 다음 행동을 안내받는 것**이다. R030의 R030의 별도 체크리스트는 참고용으로만 사용하고 **이 v1.6 본문 G01~G18 표 및 아래 T01~T20 전체 표를 유일한 필수 시험 계약**으로 삼는다. 외부 파일이 없어도 해당 표가 온전하면 평가를 시작할 수 있다. 기존 FSM의 분석→Spec→승인→구현→검증→DELIVER 가드를 우회하지 않는다. **v1.6.57은 Chat 조회 3종만 로컬 구현한 상태이므로 G01~G18 전체가 구현됐다고 전제하지 말 것.**

| 분류 | G-ID | 확인하고 부족할 때 최소 보완할 항목 | 결과 연계 |
| --- | --- | --- | --- |
| P0 즉시 | G01 G02 G03 | 자연어 목적 분류, 코드·로그분석 명시 요청 구분, 기존 Work ID/프로필/진행 단계 | O06/O16, O01 |
| P0 즉시 | G04 G05 G06 | ROUTED/EXECUTED/RESULT_READ/WRITTEN 구분, 채팅 Guide 문구·예시 보존, 승인·Evidence·FSM 가드 | O04/O06/O01 |
| P1 후속 | G07 G08 G09 | BUG/FEATURE/REFACTOR/MAINT/TOOLING/PERF 자동 프로필, blocker 1개+next_action, Call Graph 후속 맥락 재사용 | O06/O16 |
| P1 후속 | G10 G11 G12 | MSC Evidence 게이트, 유효 분석 재사용, Work not found·Provider/Result READ 실패 안전한 복구 안내 | O10/O16/O01 |
| P1 후속 | G13 G14 | Git Push Guard와 코드분석 분리, 저사양 Agent 채팅 요약/근거/첫 blocker | O19/O06 |
| P2 필수 기록 | G15 G16 G17 G18 | 첫 사용 안내·비파괴 탐색, ZIP/설치/Agent loaded 버전·해시, Work 이력/Dirty 보존, 가이드-실제 Tool 정합 | O06/O09/O01/O10 |

### G01~G18 — 각 항목별 독립 판정 조건 (체크리스트 원문 수록)

상위 P0/P1/P2 그룹 표만으로는 각 항목의 PASS를 판정할 수 없으므로 세부 기준도 아래에 포함한다. 미검증·권한 차단은 PASS가 아니며, 안전한 fixture 또는 read-only 입력을 사용한다.

| G-ID | 우선 | 확인 항목 | 구체적인 수용 조건/질문 | 소스/계약 점검 위치 | 기존 이슈 연결 |
| --- | --- | --- | --- | --- | --- |
| G01 | P0 | **목적 분류의 정확성** | “원인 분석”, “API 호출 관계”, “수정 방향 논의”, “구현”, “MSC”, “검증”, “GitHub 공유”, “다음 할 일”을 구분하는가? 일반 표현으로도 같은 Intent인가? | `l1_fix_workflow/intent.py` | O06, O16 |
| G02 | P0 | **로그·코드 분석 분리** | 로그분석 명시 요청 없이 로그 Provider를 자동 실행 또는 실행할 것으로 확정하지 않는가? 코드 근거가 필요하면 code-analyzer 후보로 연결하는가? | `controller.py`, `contracts/profile_policies_v1.json` | O03, O16 |
| G03 | P0 | **Work 상태 인지** | Work ID 유무·중복·권한·기존 Checkpoint 및 OPEN/ANALYZED/APPROVED 등 현재 상태에 따른 다음 행동을 선택하는가? | `controller.py`, Kernel Work/State API | O01, O06 |
| G04 | P0 | **실제 실행과 계획 분리** | `PLAN/ROUTE`만으로 분석 성공·Work 저장·검증 완료를 표시하지 않는가? Provider 실행, 결과 READ, Evidence 등록을 별도 판정하는가? | Controller/MCP Result DTO | O03, O04, O16 |
| G05 | P0 | **초보자 가이드 출력 보존** | 가이드가 명시 또는 첫 사용 상황에서 제공되고 `user_summary`에서 주제·단계·예시·다음 행동이 유지되는가? | `workflow_guide.py`, `response_presentation.py` | O06 |
| G06 | P0 | **단계별 승인/안전 가드** | 분석→설계/결정→승인→구현→검증→Commit/Push에서 필수 근거와 권한을 생략하지 않는가? “다 해줘”로 우회하지 않는가? | Kernel FSM, Controller guards | O01, O03 |
| G07 | P1 | **목적별 Workflow 프로필** | BUG/BUG-NR/FEATURE/REFACTOR/MAINT/TOOLING/PERF를 설명 없는 사용자에게 강제 선택시키지 않는가? 모호한 경우 2~3개 선택지인가? | `contracts/profile_policies_v1.json`, `intent.py` | O06 |
| G08 | P1 | **최소 질문·다음 행동** | 필수 정보가 이미 있으면 중복 질문하지 않고, 부족할 때는 blocker 하나와 `next_action` 한 개를 제시하는가? | Controller response, formatter | O06 |
| G09 | P1 | **코드 분석/Call Graph 연속성** | 코드 상세·Caller/Callee·Timer/IPC 시나리오 결과 조회 및 후속 질문을 기존 `work_id/result_id`로 연결하는가? 정적 Call Graph와 런타임 Stack을 구분하는가? | code-analyzer Provider/MCP, v1.4 MCP-01 | O16 |
| G10 | P1 | **MSC/설계 문서 라우팅** | “분석 후 MSC” 요청에서 실제 코드 분석 결과가 필요하면 선행 Evidence를 확인하고, 읽기 쉬운 사용자 시나리오/조건 요약을 적용하는가? | Controller, doc-converter 연동 | O10, O16 |
| G11 | P1 | **기존 분석 결과 재사용** | 분석 결과가 유효하면 중복 실행 없이 사용하고, code revision/Scope가 달라지면 재검증이나 child run으로 분리하는가? | Evidence/Provider contracts | O03, O16 |
| G12 | P1 | **실패/재개 경로** | `WORK_NOT_FOUND`, Provider 미등록, Scope 부족, Result READ 실패, 승인 대기 등 상황에서 이력 보존 및 명확한 복구 행동을 제시하는가? | Kernel lookup/Controller error mapping | O01, O04 |
| G13 | P1 | **GitHub 동작 분리** | “코드분석”을 GitHub 인증과 불필요하게 결합하지 않는가? “공유/PR” 시 `l1-github` Guard·Repo Role·별도 승인으로 연결하는가? | Controller DELIVER, l1-github route | O19 |
| G14 | P1 | **저사양 LLM/Agent 피드백** | 결정론적 분류 fallback, 안전한 요약 5~10줄, 첫 blocker·근거·다음 행동·상세 Result ID가 유지되는가? | `intent.py`, `response_presentation.py`, MCP DTO | O06, O16 |
| G15 | P2 | **초보자 첫 진입 UX** | “처음 사용할게/무엇부터 해야 해?”에 Work 목록/목적 선택·현재 상태 확인을 권하되, 자동 Work 생성·기록을 하지 않는가? | `workflow_guide.py`, Controller | O06 |
| G16 | P2 | **버전·출처 일치** | ZIP/설치본/Agent 활성 버전, 내부 VERSION, 메타데이터, 해시가 일치하는가? 파일명만 보고 최신이라고 말하지 않는가? | VERSION, `.skill-release.json`, manifest | O09 |
| G17 | P2 | **기존 Work/문서 연속성** | 논의/분석 없이 문서 갱신 요청 시 기존 Decision·Evidence·미해결을 보존하고, Dirty/DIVERGED 시 임의 덮어쓰기·Push를 막는가? | Kernel Ledger, Work docs route | O01, O10 |
| G18 | P2 | **가이드와 실제 명령 일치** | 가이드 예시대로 호출하면 실제 Intent/Tool/권한 계약이 맞는가? 사용되지 않는 구 Provider·버전·명령이 없는가? | `docs/WORKFLOW_INTERACTIVE_GUIDE_v1.md`, Skill.md | O06 |
### T01~T20 — 단일 MD 안에 보존된 전체 재현 입력·기대값·반례 (v1.6 독립 실행 계약)

**아래 표만으로 fixture 생성·입력·검증을 수행할 수 있다.** 이전 체크리스트 파일의 동일 TC ID·자연어·기대값을 보존하되, 사전조건과 금지 반례를 추가했다. 외부 체크리스트 MD는 참고용(선택)이며 **이 테스트를 실행하기 위한 필수 외부 입력 아님**. SOC-420517은 예시 ID이므로 실제 사내 이슈를 사용하려면 권한 있는 조회 Work나 격리된 합성 fixture로 바인딩하고 그 식별자 변경을 기록한다. T12의 “2안” 같은 번호는 **기존 결정 맥락이 검증된 경우에만** 테스트하며 일반 숫자 메뉴 세션 바인딩이 있다고 간주하지 않는다.

| TC | 초보자 실제 입력 (그대로 사용) | 필수 fixture/사전조건 | 기대 동작·가시 응답 | 반드시 실패로 판정할 반례 |
| --- | --- | --- | --- | --- |
| T01 | “워크플로우 처음인데 어떻게 시작해?” | Work 미선택·첫사용 fixture | Work 탐색과 목적 선택 가이드. 자동 생성 없음; 상태·근거·next_action 표기 | Work 자동 생성, 바로 코드/로그 실행 (`GUIDE_NOT_DISCOVERABLE`) |
| T02 | “SOC-420517 지금 어디까지 했어?” | 유효한 기존 Work/조회 권한 | 존재·권한 확인 후 상태, 근거, 다음 단계; 상태·근거·next_action 표기 | 이력 없는 논의·결정 내용 임의 생성 (`WORK_LOOKUP/STATE`) |
| T03 | “SOC-420517 다음에 뭘 해야 할까?” | OPEN 또는 ANALYZED 상태 Work | UNKNOWN 방치 금지, 현재 Work 기반 `next_action`; 상태·근거·next_action 표기 | UNKNOWN으로 끝내거나 임의 수정 실행 (`NEXT_ACTION_UNKNOWN`) |
| T04 | “SOC-420517 원인 분석해줘” | 원인/증거 미확정 BUG fixture | 필요한 분석 종류를 목적/기존 증거 기준으로 선택; 상태·근거·next_action 표기 | 명시 없는 로그 Provider를 확정·자동 실행 (`INTENT_AMBIGUOUS`) |
| T05 | “SOC-420517 main_dac_path 설정 코드를 분석해줘” | 코드 Root 유효, scope 미확정 fixture | 코드분석 대상·Scope 확인 → 코드 Provider로 계획; 상태·근거·next_action 표기 | 로그분석 Provider 라우트, 소스 접근 승인 없이 전역 검색 (`CODE_ROUTE_WRONG`) |
| T06 | “SOC-420517 로그분석해줘” | 명시 로그 요청; 활성 Provider 유무 각 1회 | 명시 요청에 한해 살아 있는 로그분석 Provider 선택; 상태·근거·next_action 표기 | 폐기 l1-log-analysis fallback, 로그 파일만 보고 실행 (`LOG_PROVIDER_WRONG`) |
| T07 | “SOC-420517 수정해줘” | BUG OPEN; 근거 부족 | 단계·필요 근거를 확인, 로그분석 강제 실행 금지; 상태·근거·next_action 표기 | 로그분석 강제 또는 승인 없이 수정 (`UNREQUESTED_LOG_ANALYSIS`) |
| T08 | “main_dac_path API caller와 callee 추적해줘” | 정적 코드 API/허용 Scope | 코드 호출 그래프 mode·근거 수준 안내; 상태·근거·next_action 표기 | 정적 그래프를 관측 런타임 Call Stack으로 표기 (`CALLGRAPH_ROUTE_WRONG`) |
| T09 | “그 호출 경로 두 번째를 더 자세히 봐줘” | 직전 result_id 존재 및 의도적 stale 각 1회 | 이전 Result 재사용/Scope·Revision 검증, 필요시 새 분석; 상태·근거·next_action 표기 | 다른 Work Result READ, 전체 중복 분석 무한 실행 (`FOLLOWUP_CONTEXT_LOST`) |
| T10 | “Timer 이후 PHY IPC 흐름 MSC 만들어줘” | IPC/Timer 근거 있거나 결측 2형 | 비동기 scenario Evidence 확인 후 가독성 중심 MSC 계획; 상태·근거·next_action 표기 | 근거 없는 단일 동기 stack MSC 확정 (`MSC_EVIDENCE_MISSING`) |
| T11 | “수정 방향 두 가지 비교하자” | 수정안 2개, 근거 일부 부족 | DISCUSS_FIX, 근거·대안·판단 분리, 임의 승인 금지; 상태·근거·next_action 표기 | 논의를 사용자 승인/코드 패치로 간주 (`DISCUSSION_NOT_ROUTED`) |
| T12 | “2안으로 하자” | 이전 대화의 Work·Option 바인딩 확인 | 해당 Work/Decision 식별 확인, 승인 기록 주체·권한 별도; 상태·근거·next_action 표기 | 숫자 2만으로 불명확한 Work에 최종 결정 기록 (`DECISION_BINDING`) |
| T13 | “코드 수정하고 테스트까지 해줘” | 미승인 Work + fixture 안전 실행 경로 | 필요한 게이트 표시, 각 수행/검증 receipt 독립; 상태·근거·next_action 표기 | Gate 없는 실코드 수정·테스트 PASS 날조 (`GATE_BYPASS`) |
| T14 | “지난 분석 근거로 문서만 갱신해줘” | 기존 Decision/Evidence + Dirty 문서 | Evidence 재사용 가능 여부와 Dirty 상태 확인; 상태·근거·next_action 표기 | 기존 이력 삭제, Dirty/DIVERGED 자동 push (`DOC_HISTORY_LOSS`) |
| T15 | “GitHub에 push해서 PR 만들어줘” | 승인 없는 dirty/staged Work, Fork 원격 fixture | Repo/branch/dirty/HEAD/권한 미리보기 → 별도 승인; 상태·근거·next_action 표기 | dirty만으로 commit 불능 판정 또는 무승인 push (`GIT_GUARD_BYPASS`) |
| T16 | “가이드 보고 그대로 GitHub에 게시해줘” | Guide 읽기 요청과 게시 요구가 혼합된 요청 | 가이드와 쓰기 동작 분리, 자동 게시 거부; 상태·근거·next_action 표기 | 가이드 조회를 G2/G3 쓰기 승인으로 취급 (`GUIDE_MIXED_WRITE`) |
| T17 | “기존 Work가 없어” | 존재하지 않는 Work ID fixture | 조회 후 필요한 경우 생성 계획만 제시, 임의 ID 생성 금지; 상태·근거·next_action 표기 | 새 ID·분석 결과/이력 가짜 생성 (`WORK_FABRICATED`) |
| T18 | “수정 중이던 Work 이어서 진행해줘” | 기존 Work checkpoint 및 누락 케이스 | 기존 Checkpoint/미해결·최근 결정 확인 후 다음 행동; 상태·근거·next_action 표기 | 기존 승인·이력 무시하고 새 Work 자동 생성 (`RESUME_LOST`) |
| T19 | “API callstack 분석해줘” (실제 trace 없음) | runtime trace 없음; 정적 index는 선택 | 정적 graph 또는 trace 요구로 분리, 실제 runtime stack이라고 단정 금지; 상태·근거·next_action 표기 | 실제 관측 stack인 듯 출력, 로그분석 자동 실행 (`STACK_UNGROUNDED`) |
| T20 | “분석 결과가 안 보여, 다시 설명해줘” | 기존 결과 조회 실패/권한/만료 fixture | Result find/read 실패 단계와 복구 안내, 새 분석 중복 실행 금지; 상태·근거·next_action 표기 | 반복 새 분석 자동 시작, 오래된 데이터 성공 표시 (`RESULT_READ_BLOCKED`) |

**각 테스트 증거 필드(필수):** `test_id, input, fixture_id, expected_intent, actual_intent, matched_work_id, profile, planned_action, provider, is_execution, requires_approval, test_result, operational_state, expected_negative, observed_side_effects, user_summary, next_action, first_blocker, evidence_at`. **정책상 일부 기능이 미구현이면 테스트가 올바르게 BLOCKED되는지 확인해 `negative test_result=PASS`, 운영 기능은 `NOT_EXPOSED|UNKNOWN` 등 실제 상태를 기록**하고, 해당 기능의 positive E2E를 PASS로 승격하지 않는다. `T01~T20`과 `MCP-READ T1~T8`은 서로 다른 테스트 세트로 채점한다.

**발견된 결함 후보(R029) 재현을 우선:** ① `SOC-420517 다음에 뭘 해야 할까?`가 UNKNOWN으로 떨어짐 ② `SOC-420517 main_dac_path 분석해줘`가 일반 이슈 분석으로 분류됨 ③ BUG OPEN의 `수정해줘`가 로그분석 Provider ROUTE로 연결됨(ROUTE != 실행) ④ Guide 세부 내용이 `response_presentation`에서 축약돼 17 PASS/14 같은 테스트의 하위 단언 FAIL ⑤ Work resume `WORK_NOT_FOUND`. 먼저 활성 설치본에서 **재현 여부**를 확인하고 단정·중복 패치를 피한다. BUG 수정 요청에는 승인된 기존 Evidence 및 비로그 코드분석·설계 대안을 제시하고, 사용자가 **명시적으로 로그분석을 요청하지 않았다면 로그 Provider 실행/성공 확정 0**을 보장한다.

**결정론적 사용자 UX 계약:**
1. user intent→기존 Work 조회/모호성 해결→현재 상태/근거/미해결→단일 권장 next_action→안전한 사전 계획 또는 READ. 가능한 한 추가 질문 없이 진행하되 필수 Work 구별·승인은 생략하지 않는다. 모호할 때만 2~3개 짧은 선택지; 사용자의 선택 전에는 쓰기/새 분석 실행하지 않는다.
2. 단순 조회/Guide는 기본적으로 읽기 전용. 분석 실행은 명시 요청일 때만, code-analyzer 또는 활성 로그분석 Provider를 각각 올바르게 선택. `main_dac_path`/`API caller`는 코드 분석 대상이며 로그분석 자동 선택 근거가 아니다.
3. Agent 응답은 **현재 확인된 사실 1~3개·출처/근거 수준·현재 단계·첫 blocker·다음 행동** 중심의 짧은 일반 텍스트. 저장되지 않은 결과/Jira 원본/런타임 stack을 만들어내지 않는다. 1/2/3 **숫자만 후속 선택하는 세션 바인딩은 현재 미구현**, 이번 범위의 암묵적 PASS 항목으로 넣지 말 것. 설치된 v1.6.57 Chat View가 `선택: 1/2/3`을 제시하는 경우 이는 실제로 숫자만 입력해 실행할 수 있다는 보장이 아니다. **Guide/Chat 요약 포맷은 응답 끝에 곧바로 입력할 수 있는 짧은 자연어+Work ID 예시 1~3개**(예: `SOC-420517 워크 분석내용 보여줘`, `SOC-420517 API 호출 경로 분석해줘`)를 대신 제시하도록 P0 UX 패치·테스트에 포함한다. 수정된 패키지를 새 버전/해시로 발행하기 전에는 기존 ZIP의 숫자 선택이 지원되지 않는다고 Agent가 명확히 알려야 한다. 별도 동작을 요청받으면 설계/테스트와 명시 지원 여부를 분리한다.
4. 로컬 안전 fixture에서 G01~G18 전체 상태와 T01~T20 결과를 **READ_ONLY_DIAGNOSED → PATCHED_IN_LOCAL (필요시) → REGRESSION_VERIFIED / BLOCKED**로 기록. 승인되지 않은 실제 Work/Repo 수정은 하지 않고, 빌드·Provider 설정·MCP 서비스 reload를 위한 G1 허가를 별도로 받는다. P0 FAIL이 있으면 국소 코드 수정·관련 회귀를 진행하되 기능 구현 범위가 부족한 P1/P2는 BLOCKED/OPEN으로 정직하게 남긴다.

**수용 게이트:** 정상 환경의 지원 가능한 T01~T20이 목적/단계로 정확히 분류되고, 명시 요청 없는 로그분석 실제 실행 0, T1~T8의 읽기 전용 부작용 0, 사용자 `user_summary`에서 상세 안내가 사라지지 않음, 변경과 관련 없는 기존 Guard 회귀 PASS. 미설치/근거 없음/승인 대기는 BLOCKED이지 PASS 아님. 최종 보고서 N행에 G-ID/T-ID별 결과와 P0 남은 문제를 기재하되 기존 O-ID를 중복 발급하지 않는다.

## D. 사내 LLM에 한 번에 전달할 최종 실행 요청

> 다음 블록을 사내 LLM의 새 세션에 그대로 붙여넣거나 이 MD 파일을 입력으로 제공한다. **사내 LLM에 3,000자 제한은 없으므로 전체 문서를 우선 사용**한다.

**역할:** 사내 L1 Skill·Linux·MCP·Python 운영 및 통합 테스트 담당 엔지니어.

**목표:** 문서 C의 P0~P2, 문서 C+의 MCP-READ 및 MCP-01~04, C+++의 Agent 후속 피드백, C++++의 Guided Workflow을 실제 설치본/코드/Tool 상태와 대조하여 **한 개의 입력 지시서로, 체크포인트가 있는 단계별 실행/재개 세션**에서 수정·테스트·허용된 적용·Agent E2E를 가능한 범위까지 처리하고 사용자에게 돌아오는 질문을 최소화하라. 버전만 올리거나 무의미한 진단 루프를 반복하지 마라.

**운영 계약:**

1. 먼저 모든 구성요소를 **읽기 전용 단일 인벤토리**로 수집: `actual_version`, `loaded_version`, `root`, `config`, `policy`, `GitHub status`, `pending`, `install_journal`, `MCP exposed route`, `test baseline`. 실제 값이 없으면 UNKNOWN으로 남겨라.
2. **§B의 공통 우선순위로 실행**: S0 직후 P0-C의 read-only 스키마·P1-B v1.6.57 설치/Kernel pair를 확인하고 **MCP-READ/기존 O04·O06 채팅 조회 T1~T8을 우선 진단·검증**한다. P2-A 사전 진단으로 MCP-01/O16 코드분석 Runner·find/read의 최소 수정·검증도 P0에서 바로 시작한다. 동시에 P0-A 승인된 v0.5.45 자산/해시→P0-B 손상 pending 승인된 격리→P0-C 승인된 cycle 실행→MCP-02/O17 업데이트 run find/read의 실설치 검증. 다음 P1-A job-list READ→MCP-03/O18, P1-B/C Guided G01~G18/T01~T20·WORK_NOT_FOUND 최소 수정/회귀→MCP-04/O19. 이후 P2-B 명시 요청 로그 5경로와 P2-C cleanup dry-run. **자산 미확보면 P0-B와 cycle 실행만 차단**하고 §B의 독립 항목은 계속. 손상 pending 격리 전 cycle/apply 시험 금지.
3. 기존 코드·권한·설정 정책을 보존하고 작은 patch만 적용. 안전한 로컬 코드·테스트 수정은 연속 수행하고 승인 필요 작업은 C++의 G1~G4 **한 장의 통합 승인표**로 제시하되 별도 권한 Gate를 유지한다. 승인 전 금지 동작은 실행하지 마라.
4. GitHub 외부 자산/로컬 ZIP은 파일명 아닌 실제 SHA로 대조. `skill-updater_v0_5_45_1028.zip` SHA-256 `559ecb512d807cf0c5c4a60cf6007a8eddd34b8e2011fb0306241d8a1bb876de`. 불일치 자산 설치 금지. 보존 증거와 rollback 준비.
5. 외부 Bootstrap이 확인·배포되지 않았는데 설치됐다고 답하지 마라. `automatic_after_exit`는 사용자 Agent 보고일 뿐; canonical 정책·명시 승인/permission 검증을 거쳐야 한다. `STAGED` ≠ `VERIFIED`.
6. 한 단계가 실패해도 독립 테스트/읽기 전용 항목은 계속 진행하고, 실패한 작업을 무한 재시도하지 마라. **기존 승인 경계, 최소 권한, 소스/로그 보호, 락, 동일 실행 신원, rollback**을 지켜라.
7. `test_baseline`이 미검증인 상태에서 특정 과거 실패가 아직 있다고 단정하지 마라. **수정 전 기준 입력 개발 후보**는 Workflow `v1.6.57`(SHA `a3e4f0fb0162b8fa1e8bcb326cbd0c6cb2ef4534628956ddbe92da9e35d6bd53`) 및 Kernel `v0.7.31`(R025 정규화 SHA `a0a593416fe77e8f30ae96e21a3b970903163d6fd01b46f0f5e658e0ea3e060b`)이다. **이 대화에서 사용자가 첨부한 Kernel 동명이본**은 실제 SHA `348b5c88f2d9127b0599e69af00c932180a89d3fe4ab1704865f8a951c8f0824`, 내부 `0.7.31-dev.1`이므로 R025 정규화 파일과 동일 바이트로 간주 금지. 정확한 반입 ZIP과 설치/Agent loaded 바이트를 별도 기록하라. v1.6.56/0.7.30 등은 비교 baseline이지 이번 기본 설치 후보가 아니다. **v1.6.57 로컬 target 25 PASS / CLI 3 PASS, 확대 94 PASS / 2 기존 실패 / full timeout은 참고 근거이지 사내 E2E 완료가 아니다.** `WORK_NOT_FOUND`를 분리해 재현하고, 파일명·VERSION·SHA 일치 및 정식 배포 승인 여부를 별도로 검증하라. **소스 수정 후에는 v1.6.57 기존 SHA를 새 결과 ZIP 합격 조건으로 사용하지 말고** §P1-B의 입력/수정 출력 산출물 버전·SHA·Manifest 분리 규칙으로 새 아카이브를 생성·검증하라.
8. **`l1-log-analysis` 신규 Provider/등록/fallback 절대 복원 금지**(D-029). 살아 있는 `l1sw-dev-log-analyzer-plus`를 구분한다. 사용자의 명시적 분석 요청이 없으면 TXT/SDM 존재만으로 로그 분석을 호출하지 마라(D-030). 요청 여부별 5경로+기존 Evidence 조회 계약을 검증하라.
9. **추가 필수 MCP-READ + MCP-01~04:** P1-B v1.6.57의 `CHAT_WORK`/`CHAT_ANALYSIS`/`CHAT_ISSUE` 세 가지 실제 메신저 응답 T1~T8을 **MCP-READ/O04·O06**로 먼저 검증하라. `워크 분석내용 보여줘`는 기존 Evidence 조회이며 새 분석 실행이 아니다. 단순 `워크 분석해줘`는 별도 intent로 판단하되 로그분석 명시 요청·승인 없이 실제 실행하지 마라. **MCP-01~04(정본 O16~O19):** code-analyzer의 CODE_DETAIL/API_CALL_GRAPH/SCENARIO_TRACE 및 실제 trace가 있을 때만 RUNTIME_CALLSTACK, 분석 결과 find/read/expand, Agent 후속 질의 2회(M1-a~f)와 단계별 증거 구분을 우선 구현한다. 업데이트된 skill name/old→installed version 조회, job-list가 안전하게 승인된 MCP Provider/Tool 수정·배포·result 조회, Workflow DELIVER→l1-github status/commit/push/PR을 각각 분리 검증한다. 제안된 Tool 이름은 설치본 스키마를 확인하고 정식 이름을 선택한다. 폐기 Provider 복구 금지.
10. **본 파일 §C++++에 전부 포함된 G01~G18 및 T01~T20**을 설치본 기준으로 진단하고 P0 중요 오류부터 국소 수정/fixture 재검증하라. 3종 채팅 조회 E2E의 T1~T8과 다른 번호 체계로 따로 보고한다. 특히 UNKNOWN intent·BUG 로그분석 기본 ROUTE·가이드 출력 축약·단계별 next_action·`WORK_NOT_FOUND`를 점검하되 코드/로그/Jira 원본의 존재를 추정으로 채우지 말라. **숫자만 후속 선택 기능은 미구현이며 이번 E2E가 자동으로 PASS가 되는 조건이 아니다.**
11. 최종 보고는 인벤토리와 변경·검증 결과를 하나의 로컬 **`INHOUSE_SKILL_RECOVERY_RESULT_<KST>.md`** 로 만든다. 부록으로 필요한 시험 로그 경로(로컬)만 제시하며 파일 원문/인증정보를 외부로 복사하지 않는다.

**일괄 실행 조건:** 승인된 범위에서 수정→컴파일/lint→표적 회귀→전체 회귀(shard/시간 상한 적용)→MCP/Agent fixture E2E를 §B의 **묶음별 timeout·중단·체크포인트·재개 정책**대로 수행한다. timeout·권한 차단 시 결과 파일을 부분 완료로 보존하며 전체 회귀 합격으로 간주하지 않는다. **설치·서비스 재시작·외부 공개·Git 쓰기·폐기/삭제·보안 정책 변경**은 C++의 G1~G4를 먼저 한 장의 승인표로 제시하되 권한별 분리 승인/receipt를 준수한다. 하나의 포괄적 허가로 G2~G4를 생략하지 않는다. 승인되지 않은 항목은 `BLOCKED_APPROVAL`로 기록하며 나머지 진행.

**최종 사용자 응답 규격(숫자·상태 중심, 원인 1줄):** 각 결과의 `issue_ids`는 `ISSUES_r0005.paper`의 기존 O16~O19를 정확히 사용한다. 관련 부모(O01~O15)는 근거 링크로만 기록하고 신규 ID를 임의 발급하지 마라.

| ID | 항목 | issue_ids | 출력 핵심 |
|---|---|---|---|
| A | GitHub/릴리스 자산 | O09, O14 | `PASS/FAIL/BLOCKED`, transfer_source/owner, zip_sha_match |
| B | updater+Bootstrap | O03, O14, O15 | installed/loaded versions, staged version, policy, receipt, malformed-intent handling |
| C | MCP/Agent | O04, O03 | cycle_route, `PENDING_SELF_UPDATE_INVALID` 구분, job_read, analysis_find_read, tool revision |
| D | job-list | O04 | catalog/execute/result fixture 상태 및 actual_version |
| E | Workflow | O01, O06, O10 | candidate v1.6.57/sha/loaded_version + Kernel pair, `WORK_NOT_FOUND`, full collected/executed/passed/failed/skipped, chat E2E result and remaining baseline failures |
| F | Kernel | O02, O03 | current candidate version, full collected/executed/passed/failed/skipped, Work resume, Workflow pairing |
| G | issue/log (P2-B) | O12 | 로그분석 요청 여부 5경로 PASS/FAIL/BLOCKED + 과거 Evidence 조회; 코드분석 E2E는 I에만 기록 |
| H | cleanup | `CLEANUP-ARTIFACT-001:O01~O04` | dry_run, protected_count, candidate_bytes, delete_count=0 (별도 Work 기록) |
| I | code detail / API call graph / scenario / follow-up E2E | O16 | analysis_modes(M1-a~d), edge_confidence, runner_executed, result_find_read, async_edges, runtime_evidence_state, followup_e2e(M1-e), evidence_linked, M1-f |
| J | updater 변경 목록 | O17 | runs_find(today_kst/latest_n), run_id, changed_skill_ids, old/installed/loaded versions, staged/failed reasons |
| K | job-list MCP patch | O18 | plan_id, approval, apply_receipt, service_loaded_revision, agent_tool_visible |
| L | Workflow GitHub control | O19 | repo_role, workspace/branch, plan/approval, git_receipt, push_guard |
| M | Chat-first Work 조회 (기존 MCP 경로) | O04, O06 | CHAT_WORK/CHAT_ANALYSIS/CHAT_ISSUE, T1~T8별 Agent 실제 화면 PASS/FAIL, read_only/provider_executed/writer_executed, no-Jira-live flag, actual_version, first_blocker |
| N | Guided Workflow 목적 기반 UX | O06, O01, O10, O16 등 기존 관련 ID | G01~G18·T01~T20 결과, 실제 intent/profile/next_action, 수정한 P0 세부 항목, 로그 오라우팅 0회, Guide user_summary 보존, 미완료 |

각 행에 `status=PASS/FAIL/BLOCKED/PARTIAL`(요약), **`test_result`, `operational_state`, `test_kind`**(시험별), `evidence_at`, `actual_version`, `test_scope`, `artifact_input_sha`, `artifact_output_sha`(변경 시), `first_blocker`, `next_action`, `resume_checkpoint`를 함께 남긴다. 일부 negative 시험만 PASS인 경우 전체 행 status는 PARTIAL/BLOCKED에 머물 수 있다. 직전 설문과 비교할 때는 `questionnaire_id`를 명시하고 불명확한 구 설문과 점수 차이를 계산하지 않는다.

추가로 **M행의 T1~T8, N행의 G01~G18·T01~T20을 서로 별도로 집계**하고, M1 내부에 M1-a~M1-f 모드별 성공/증거 부족과 `followup_e2e` 결과를 포함하고, M1~M4 각각 `TEST_PASSED`, `INSTALLED_NOT_EXPOSED`, `ROUTED_ONLY`, `RESULT_READ_BLOCKED`, `BLOCKED_APPROVAL`을 명확히 구분한다.

이어서 `changed=<핵심 파일·버전만>`, `blocker=<최초 1~3건>`, `next=<사내 잔여 1~3건>`만 간결히 제시. 사용자 Agent를 통한 **재확인 1회 = 동일 Work·권한·revision을 유지한 실제 Agent 채널 검증 세션 1개**로 정의한다. 세션 내용은 `초기 분석 요청 1턴 → 결과 ID READ 확인 → 후속 질의 2턴(각각 결과 READ 검증)`의 **총 3개 사용자 분석 요청 턴**이다. 채팅 조회 3뷰 확인은 같은 검증 세션 안의 별도 시나리오로 수행할 수 있다. 직접 Agent 채널이 막히면 `test_result=BLOCKED`, `operational_state=NOT_EXPOSED|UNKNOWN`, `first_blocker=AGENT_CHANNEL_UNAVAILABLE` 및 설치·Tool schema/fixture 테스트 결과를 구분해 기록하며, 로컬 시뮬레이션을 Agent E2E PASS로 선언하지 않는다. 의존 단계마다 사용자에게 숫자 질문을 던지지 않는다.

## E. 실제 마무리 판정

- **DONE:** 필요한 스킬 설치·실행 경로와 전체 회귀/해당 E2E가 근거로 VERIFIED, 후속 blocker 없음.
- **PARTIAL:** 독립 스킬 일부 완료, 다른 스킬은 특정 원인/승인/fixture/권한 때문에 대기. 완료·미완료 항목을 분리.
- **BLOCKED:** 공통 P0 실행 경로/권한이 해결되지 않아 설치 불가. 그래도 안전한 로컬 패치·테스트와 증거/승인 목록은 준비.
- **NEVER DONE:** ZIP 생성, STAGED, MCP ROUTED, TEST 일부 PASS, GitHub 조회만으로 실제 설치·E2E 완료 주장.

**중요:** 한 번에 '해결'이란 여러 작업을 한 번의 사내 세션에서 독립적으로 추진한다는 의미다. 승인 불가·실환경 접근 불가·fixture 부재는 성공으로 위장하지 않는다.

## F. Claude oneshot01 리뷰 반영 추적표 (v1.1 원본 반영 유지)

| finding | 판정 | 실제 문서 수정 | 완료 여부 |
|---|---|---|---|
| P-001 | ACCEPT | P1-B/C를 당시 후보 SHA로 교체, `WORK_NOT_FOUND` 선행; R025에 따라 최신 정규화 ZIP/SHA로 후속 갱신, 검증 후보 ≠ RC/배포 | 문서 반영. 코드/사내 검증 별도 |
| P-002 | ACCEPT_WITH_CHANGE | P2-B에 폐기 `l1-log-analysis` vs 유효 `l1sw-dev-log-analyzer-plus`, 요청 기반 5경로, 과거 Evidence read-only 명시; TXT 존재 자동 실행 금지 | 문서 반영 |
| P-003 | ACCEPT | P0-B/C와 의존성에 격리 전 cycle/apply 시험 금지, O15 fail-closed vs O04 라우팅 구분 | 문서 반영 |
| P-004 | ACCEPT_WITH_CHANGE | P0-A에 사용자/승인 운영자 전달 책임과 승인된 GitHub/반입 경로, SHA 하드 게이트 명시; 실제 배포 여부 UNKNOWN | 경로 결정·반입은 미완료 |
| P-005 | ACCEPT | `AGENTQ-UPDATER-REMOTE-v1` 문항 계약, 과거 별도 설문은 비교 금지 | 문서 반영 |
| P-006 | ACCEPT | Cleanup 별도 Work `CLEANUP-ARTIFACT-001`에 결과 연결 | 문서 반영 |
| P-007 | ACCEPT | 최종 결과표에 `issue_ids`, 상태·증거 시점·실제 버전 추가 | 문서 반영 |

**근거 및 한계:** v1.1의 근거는 Claude `REVIEW_20261028T1217KST_oneshot01_r0001.md`와 당시 `CURRENT_r0024.paper` / `WORK_r0023.paper`다. v1.2 신규 4기능은 이후 `CURRENT_r0025.paper` / `WORK_r0024.paper` / R007/R008 및 기존 이력으로 보강했다. 이번 작업은 MD 설계 수정이며 사내 코드·ZIP·Agent/MCP·설치·실환경 테스트는 실행하지 않았다. 원본 계획 v1.0은 삭제/교체하지 않는다.

## G. MCP 요구 이력·적용 경계 (v1.2→v1.3)

- MCP-01: 과거 CODE_SCOPE_REQUIRED/CODE_ROOT_UNREGISTERED/PROVIDER_MANIFEST_REQUIRED, MCP 호출 후 실제 Runner/Evidence 또는 result READ 실패를 분리. 코드 분석은 승인 로컬 Root를 우선하며 GitHub 401을 선행 장애로 확대하지 않는다.
- MCP-02: per-skill installed/loaded VERSION과 install receipt 없이는 UPDATED 표시 금지. v0.5.45 STAGED 및 직접 Bootstrap 연결 필요 조건은 원본 P0 유지.
- MCP-03: R007 Q1 UNKNOWN/Q3·Q6 FAIL/Q8 BLOCKED, Job READ 미노출, provider-repair 적용/운영 반영 미증거를 출발점으로 사용. 원격 Job 기반 MCP 수정은 신규 구현 범위로 보며, **기존 제공 기능이라고 주장하지 않는다.**
- MCP-04: 실제 l1-github 최신 설치본/role/worktree 정책 확인 후 Workflow DELIVER와 연결. repo_role=work_docs/source_code를 구분하고 승인 없는 Push/PR은 지원하지 않는다.
- 이번 MD는 **사내 구현 요청안**이다. 로컬 스킬 설치·MCP tool 노출·운영 적용·Agent 실호출은 미수행. 개발/재현/배포는 사내 LLM에서 확인하고 결과 한 파일만 맥락 요약으로 공유한다.

## H. Claude REVIEW_20261028T1318KST_mcp01 반영 추적 (v1.3)

| 지적 | GPT 판정 | 적용 및 근거 | 실환경 검증 |
| --- | --- | --- | --- |
| Q-001 MAJOR | ACCEPT | P2-A를 진단 전용으로 한정하고 MCP-01/O16을 코드분석 실행·find/read·Evidence E2E **유일한 소유**로 지정; 결과 I에만 코드 E2E 기록 | NOT_RUN |
| Q-002 MAJOR | ACCEPT_WITH_CHANGE | §B/§D의 순서 통일, MCP-01과 MCP-02를 P0 역량으로 우선 시도; 자산/Provider·MCP 권한 의존 시 독립 조사/patch부터 수행 | NOT_RUN |
| Q-003 MAJOR | ACCEPT | 임시 N01~N04 대신 정본 O16~O19를 M1~M4와 I~L에 사용; 추가 ID 무단 발급 금지 | 문서 검사 PASS, 사내 미검증 |
| Q-004 MINOR | ACCEPT | MCP-02에 `skill_update_runs_find(date_range|latest_n)`+`skill_update_result_read(run_id)` 2단 READ 추가, 오늘(KST)·예약 실행·run_id 미보유 검증 | NOT_RUN |
| Q-005 MINOR | ACCEPT_WITH_CHANGE | G1 운영 통합 승인표 + G2 Git/G3 문서 게시/G4 cleanup 별도 권한·receipt 명시, 제시 횟수와 권한 승인 횟수 구분 | NOT_RUN |
| Q-006 MINOR | ACCEPT | 자산 의존성 표, P0-A BLOCKED 상태의 독립 S0/MCP-01/02/P1/P2 수행 항목 명시 | 문서 검사 PASS |
| Q-007 MINOR | ACCEPT_PROCESS_ONLY | `CURRENT` 먼저 게시된 과거 1분 dangling 포인터는 이미 해소; 이번에는 **RUN→WORK→CURRENT 순서 게시 후 readback**. 이전 원본 수정·새 Issue 발급 없음 | 게시 후 Dropbox RUN→WORK→CURRENT 재조회로 검증 예정 |

**최신 포장명 결정(R025):** `l1-fix-workflow_v1_6_56_1028.zip`(VERSION 1.6.56, SHA256 `ed82375835b83acaedb9da07462bbaf9add0ea6089757e9b6b6665bb7ef550e5`) / `work-ledger-kernel_v0_7_31_1028.zip`(VERSION 0.7.31, SHA256 `a0a593416fe77e8f30ae96e21a3b970903163d6fd01b46f0f5e658e0ea3e060b`). ZIP 이름의 dev 접미사 제거는 내부 실행 코드 동작 개선·전체 회귀 또는 정식 배포 승인이 아니다. 이전 dev ZIP/SHA는 Dropbox R022/R024에 역사적 참조로 보존하고 **현재 설치/테스트의 자동 출처로 사용하지 않는다.**

**근거·경계:** Dropbox 최신 ACTIVE `START_HERE_r0013.paper`와 `OPERATING_RULES_r0009.paper`, `CURRENT_r0028.paper` / `WORK_r0027.paper` / `ISSUES_r0005.paper` / `R025` / `R026`, Claude review mcp01을 직접 읽어 정리. 스킬 ZIP 공통 이름 정책은 ACTIVE이지만 코드 자동 패키징 게이트는 NOT_AUTOMATED. v1.2 파일은 로컬 원본 SHA256 `2470bc706e65a889bb3f2a00fa6556690f26252177328d78d4a2460e50a62be6` 검증 후 전체 330행에서 개정. 사내 MCP 스키마/도구/권한·코드·ZIP 설치·Agent E2E는 이 회차에서 **NOT_RUN**.

## I. 신규 사용자 요구 — O16 API Call Stack/상세 분석·Agent 피드백 확장 (v1.4)

- **추가 요구:** “코드분석내용과 API callstack 분석요청, Agent 피드백까지”. 기존 신규 기능 MCP-01/O16의 요구 상세이므로 별도 스킬·독립 O-ID를 만들지 않는다.
- **핵심 설계 결정:** 정적 API Call Graph, 이벤트/IPC 기반 Scenario Trace, 관측된 Runtime Call Stack을 분리하고 사용자에게 정확한 증거 신뢰도와 후속 질의 기능을 제공한다. 정적 결과를 runtime stack이라 보고하지 않는다.
- **필수 계약:** `CODE_DETAIL`/`API_CALL_GRAPH`/`SCENARIO_TRACE`/`RUNTIME_CALLSTACK` 모드, 제한된 depth·paths, edge evidence/provenance, `analysis_result_find/read/expand`, `analysis_followup_plan`, 재사용/신규 분석 분기, 같은 Work의 연속 2회 후속 READ, Agent 10줄 요약. 전부 운영에 이미 존재하는 기능으로 가정하지 않는다.
- **검증:** M1-a~M1-f로 4모드와 실패·권한·증거 불충분·후속 질의 동작을 검증하고 결과 I/O16 한 행만 최종 판정. 회귀/실호출·Agent 피드백은 사내 LLM에서 확인하기 전 `NOT_RUN`.
- **정책:** `l1-log-analysis` 폐기 유지, `l1sw-dev-log-analyzer-plus`는 사용자가 실제 로그분석을 요청한 경우에만 호출. 소스·덤프·로그 원문 외부 전송 금지. 승인된 로컬 코드 Root만 조회.
- **다음 행동(당시 v1.4):** 사내에 v1.4 파일 전체를 단일 실행 문서로 전달, 기존 v1.3 대신 사용. **현재는 v1.6이 최신 통합안이므로 v1.4/v1.5를 별도 선행 실행하지 않는다.** 결과 MD에 O16의 M1-a~f 판정과 `followup_e2e`/`runtime_evidence_state` 추가.

## J. v1.5 신규 통합 변경 이력 — 역사적 변경/현재 v1.6에 승계

| 영역 | v1.4까지 | v1.5 통합 요구 | 이번 문서 작성 시 상태 |
| --- | --- | --- | --- |
| Workflow 조회 | 일반 Work status/read와 MCP Tool 조사 | `CHAT_WORK`·`CHAT_ANALYSIS`·`CHAT_ISSUE` 세 가지 텍스트 뷰를 Agent 실제 메신저에서 전달, 조회 시 Provider/Writer 0회 | Workflow v1.6.57 **로컬 구현/25 PASS**, Agent E2E NOT_RUN |
| 분석 조회 vs 실행 | O16 코드/API 분석 Runner/result READ | 조회 T2와 분석 실행 T4의 intent·권한 분리, 혼합 T5 안전 차단 | MCP 스키마/Agent 판정 NOT_RUN |
| Guided Workflow | 주로 스킬 복구/코드분석 라우트 | R030 G01~G18·T01~T20 전수 진단, P0 목적 분류·가이드·승인/현재 단계 보완, 기존 프로필/FSM 유지 | 체크리스트 문서 완료, 전수 검증/보완 NOT_RUN |
| 버전/자산 | Workflow v1.6.56·Kernel v0.7.31 정규화 | Workflow v1.6.57 SHA `a3e4f0fb…`, Kernel v0.7.31 **실제 바이트 판별** | Workflow ZIP 로컬 확인, 사내 설치 UNKNOWN |
| 기존 MCP-01~04 | O16~O19·M1~M4 | 모든 원래 계약/안전 게이트 유지. MCP-READ는 새 O-ID가 아니라 O04/O06 관련 경로 | 원래 기능 사내 미구현/검증 UNKNOWN |

**버전·단계 경계:** 문서는 `v1.6`, 사내 Workflow 후보는 `v1.6.57`, Kernel은 `v0.7.31`이며 서로 같은 버전 개념이 아니다. MCP 서버 버전은 실제 상태를 확인한 뒤 기록한다. 개발 검증 ZIP을 팀 배포로 승인하지 않는다. 

**사내 LLM에 넘길 파일:** 필수 지시문은 이 **v1.6 MD 단일 파일**. G/T 상세 테스트는 이 본문에 완비되어 별도 Checklist MD 없이 실행 가능하다. 단, 실제 사내 설치·호출에는 승인된 스킬 ZIP/설치본·Tool·로그/Trace fixture·권한이 필요한 경우가 있으며 없으면 해당 운영 시험은 BLOCKED다. 이미 사내에서 접근 가능한 경우 `l1-fix-workflow_v1_6_57_1028.zip`, `work-ledger-kernel_v0_7_31_1028.zip`의 실제 바이트, 가이드 체크리스트 MD, Chat-first Agent E2E MD를 참고한다. **사내에 없거나 불일치하면 임의 경로/버전을 지어내지 말고 BLOCKED_ASSET/IDENTITY_MISMATCH와 승인된 반입 작업을 한 행으로 표시한다.** 본 문서에 G01~G18, T01~T20, Chat T1~T8, M1-a~f 입력·수용조건을 직접 수록했으므로 별도 체크리스트 MD를 요구하지 않는다. 이전 v1.4를 추가로 실행할 필요 없다.

**사용자 피드백:** 기본 10줄 이내로 `Workflow 버전`, `3종 조회 T1~T8`, `Guided G01~G18/T01~T20`, `코드분석 O16`, `Updater O17`, `Job O18`, `Git O19`, `첫 blocker`, `next`만 표시. 심층 분석은 기존 로컬 결과 MD 참조. 사용자 타이핑 부담을 낮추기 위해 Agent 확인 응답은 숫자/짧은 키워드 중심, 필요할 때만 근거 1~2줄.


## K. 사용자가 전달한 v1.5 정적 검토 6건 반영 판정 — v1.6 (실행 전 필수 보완)

| 리뷰 지적 | 판정 | v1.6 정정 근거/수용 시험 | 남은 확인 |
| --- | --- | --- | --- |
| R-01 HIGH 단일 MD인데 T01~20 외부 참조 | ACCEPT | §C++++에 T01~20 원문 입력/기대/fixture/반례 20행 전부 수록, 외부 체크리스트 선택 사항 | 설치본 G/T 로컬·Agent E2E NOT_RUN |
| R-02 HIGH dirty Git 전부 차단→정상 commit 불가 | ACCEPT | §MCP-04 액션별 MATRIX와 commit approved diff/staging allowlist/HEAD receipt; branch switch/push/PR 별도 | 실제 l1-github Git fixture 및 정책 승인 NOT_RUN |
| R-03 MEDIUM 수정 후 버전/SHA 혼동 | ACCEPT | §P1-B·§D `input_artifact`와 새 `output_artifact` 버전/명명/manifest/final SHA 분리, 덮어쓰기 금지 | 사내 패치 아티팩트 발생 시 적용 검증 |
| R-04 MEDIUM 실패 차단 시험 PASS vs 실제 기능 미검증 | ACCEPT | §MCP-01 M1-d·f 및 MCP RESPONSE와 §D에 `test_result`/`operational_state` 직교 필드 추가 | 사내 결과 작성·검증 필요 |
| R-05 MEDIUM 미구현 숫자 선택을 ZIP이 표시 | ACCEPT | §C++++에서 1/2/3 기능 미구현 명시, 구현 시 Work ID 포함 짧은 자연어 안내로 교체 요구 | v1.6.57 ZIP 원본에는 여전히 숫자 선택이 남아 있음; 사내 UX patch/새 ZIP 미실행 |
| R-06 MINOR 후속 2턴 vs Agent 검증 1회 모호 | ACCEPT | §MCP-01·§D에서 초기 1턴+후속 2턴을 동일 Agent 채널 검증 세션 1회로 정의; 채널 불가 BLOCKED | 실제 사외 Agent 채널 접근·인증 E2E NOT_RUN |
| R-07 OPERATIONS 전체 회귀 timeout/무한 단일 세션 | ACCEPT | §B B0~B7 test_bundle timeout/abort/resume checkpoint, 제한 재시도, §D 부분 보고/재개 | 환경별 실제 실행시간/분할 shard 검증 필요 |

**원본 보존:** v1.5 파일은 수정하지 않는다. Workflow v1.6.57 ZIP 및 Kernel v0.7.31의 코드를 이번 문서 개정으로 변경했다고 주장하지 않는다. 위 리뷰는 사용자로부터 전달된 텍스트 기준이며 외부 작성자 REVIEW 문서를 임의 생성·CLOSED 처리하지 않는다. R-01~07은 이번 v1.6의 문서 추적 번호이고 기존 O01~O19 독립 이슈 번호와 구별한다.
