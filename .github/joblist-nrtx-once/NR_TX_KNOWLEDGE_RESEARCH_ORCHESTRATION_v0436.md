# NR L1 Tx — 무인 Knowledge Updater 1차 코드조사 / AS-IS MSC One-shot v0.4.36

- 실행 주체: 사내 Linux의 기존 예약 Skill-Updater가 활성화한 One-shot Job-list → 등록된 OpenCode / LLM
- 사용자 지시: 무인 동작, **기존 소스·설정·Knowledge 정본에 대한 수정 없이 가능한 조사·스킬 호출·검증·새 로컬 산출물 작성 권한 최대로 사용**. 사내 추가 승인 필요 작업은 임의 승인 대신 상태만 남김.
- 주관: **이미 설치된 `l1-knowledge-updater`**. 새로운 Updater/분류 엔진을 만들지 않는다.
- 보조: 기존 `code-analyzer` 코드 사실 조사, 기존 `doc-converter` MSC 스타일·변환·렌더, 필요시 기존 Workflow/Kernel Work/Evidence 참조
- 소스: 실행 호스트에서 Job-list Worker가 승인·검증한 현재 Git checkout만. 외부 제공 파일/문서는 소스 사실의 증거가 아니다.
- 작업: **read-only 코드 조사 + 기존 스킬의 등록된 비파괴 action 호출 + 사내 신규 분석 산출물 생성**. 소스/기존 Work·Evidence/기존 Knowledge 정본 수정, 그룹 자동 게시, 사외 전송, 패치·Jira/Confluence write, 임의 skill 설치/업데이트 및 Git push 금지.
- **질문 없이 최대한 자동 진행:** 실제 설치된 SKILL.md와 Skillsilent policy를 직접 읽고 허용된 Read/Analyze/Candidate action을 사용. Write/Apply/Publish/Commit/Submit action은 절대 호출하지 않는다. 미설치·차단·명령 계약 미확인 사항만 BLOCKED/PARTIAL로 격리하고 가능한 시나리오는 계속 조사.
- 사내 Linux에 승인된 LLM/스킬이 이미 노출되어 있으면 그 기존 연결을 사용. 과거 사내 GPT가 사용한 오케스트레이션 방식 재사용; GitHub PUBLIC Job-list 요청 자체로 새 권한/임의 액션을 만들어내지 않는다.
- 담당 범위: **NR L1 Tx**. LTE·L2·PHY는 인터페이스 경계 확인에 필요한 최소 증거만 포함.

## 실행 절차

1. 기존 `l1-knowledge-updater`의 설치된 SKILL.md·Skillsilent 정책/실제 action/entrypoint를 읽고, **기존 오케스트레이션 절차 중 비파괴 분석·후보 생성 action만** 호출. 호출 경로가 확인되지 않으면 `BLOCKED_UPDATER_CONTRACT`으로 구분하되, 설치된 `code-analyzer`의 허용된 독립 코드 분석과 `doc-converter`의 허용된 독립 MSC 생성은 계속 진행하여 PARTIAL 결과라도 남긴다. 임의 CLI·API·권한 추정이나 외부 연결 탐색은 금지.
2. Code Analyzer를 이용해 현재 Git branch/HEAD, dirty/scope, source anchors 및 build option별 분기 상태를 확보. 로컬 현재 checkout에 수정된 tracked 파일이 있으면 **해당 working-tree 바이트/해시를 별도로 식별**하고 commit-only 결과로 오인하지 않는다. 파일을 수정하거나 `git checkout/reset/stash`를 사용하지 않는다. 기존 `l1sw-dev-knowledge`는 보조 참조만 하고 코드 사실 확정은 소스 근거 우선.
3. 아래 네 개의 시나리오를 **서로 분리해서** entrypoint부터 실제 최종 경계까지 call / state / DB / condition / message / IPC payload를 분석. 자동 확장하지 말고 L1 소유 모듈을 중심으로 bounded scope 준수.
4. `code-analyzer`의 실제 CODE_FACTS/behavior facts/flow 문서/PlantUML 기반 근거를 생산. 파악되지 않은 path/line/compile condition은 `REVIEW_NEEDED`이며 추정으로 메우지 않는다.
5. `doc-converter` v0.2.21의 **`L1_USER_SCENARIO`**, `l1-scenario-ir/v1`, `participant_policy: SOURCE_PARENT_DIR_V1` 및 `msc-scenario-adapt / msc-scenario-build / msc-package` 의 현재 설치 정책을 우선 준수. 실제 소스 경로가 검증된 participant만 마지막 부모 폴더명으로 그룹화. `BCH_CTRLR→BCH`, `DRX_CTRLR→DRX`, 동일 TxMngr 폴더의 TxCfgMngr/TxCmdMngr는 **TxMngr 하나**로 표시. 같은 participant 내부 helper/self call은 그림에 표시하지 않고 trace/evidence에 유지. Stack/RAT 구별과 모듈 ID는 보존.
6. Updater를 통해 그룹 `l1sw-dev-knowledge`의 기존 NR Tx 지식과 중복·변경된 코드 경로를 **읽기 전용** 대조하고 **HLD/상세설계/AS-IS MSC/기술 이슈 히스토리의 새 수정 후보 파일**을 사내 출력 경로에 작성. K5.8 tier와 K6 MSC 정책은 설치본 기준으로 판단; 정책 개정이 아직 반영되지 않았다면 `POLICY_MISMATCH_REVIEW` 기록. **게시·원문 덮어쓰기 금지**.
7. 개인 Work ID·EvidenceRef·Code Analyzer 결과·source revision·MSC 생성 manifest와 그룹 지식 후보의 대응 관계를 **기존 데이터를 변경하지 않고** 정리. 기존 Work ID가 없으면 새 ID를 임의 생성·등록하지 말고 `WORK_LINK_PENDING` 기록.
8. 실제 명령·결과·산출물·실패 항목을 Linux 사내의 스킬별 승인된 신규 출력 저장소에 보존. 무인 실행 중 사용자 질문·정책 변경·권한 우회 없이 종료 상태까지 진행. 모델 답변 문장으로 PASS를 대체하지 말고 실행 영수증/실제 파일 확인. Run Catalog 자동 등록이 없으면 `RUN_CATALOG_NOT_VERIFIED` 명시.

## 시나리오

### NR-TX-01 — Init RACH

- **Start:** NR L1 Tx가 `L2_L1_TX_REQ` message를 수신한 실제 handler
- **End:** NR Tx/RF/HAL 경계에서 PHY로 해당 procedure **IPC를 실제 전송**하는 지점. PHY 내부 동작은 제외
- 확인: message dispatch, 초기화/config 및 TxPath/Resource selection 관련 실제 코드, trigger-to-IPC 함수 흐름, async/callback, guard, 실패·skip·retry 및 IPC message/payload 생성 경로. 범위 밖 확장은 보류.

### NR-TX-02 — UL SCell Configuration

- **Start:** `PHY_CONFIG_REQ` message를 수신하는 실제 NR L1 경로
- **End:** NR Tx의 UL SCell configuration 관련 하위 전달/PHY IPC 및 관련 state update의 **코드로 확인되는 유효 경계**
- 확인: UL SCell 구성 정보 해석, PCell/SCell 및 band/CC mapping, Tx 경로 구성, 조건부 branch와 IPC/설정 순서. 실제 코드에 없는 설정 메시지 이름은 추론하지 않음.

### NR-TX-03 — UL SCell Activation

- **Start:** `SCELL_STATUS_IND` 수신, **Activation**에 해당하는 실제 branch
- **End:** 해당 SCell의 UL Tx enable·상태 전환 및 PHY/하위 명령 전달의 실제 코드 경계
- 확인: activation guard/현재 상태, config 선행 관계, Tx resource/ULCA/ENDC와의 실제 충돌/분기, 명령 순서·IPC·동기/비동기 경계.

### NR-TX-04 — UL SCell Deactivation

- **Start:** `SCELL_STATUS_IND` 수신, **Deactivation**에 해당하는 실제 branch
- **End:** 해당 SCell의 UL Tx disable·상태 해제 및 PHY/하위 명령 전달의 실제 코드 경계
- 확인: 활성화와 비대칭적인 release/order/guard, 재활성화에 남는 state, pending/rollback, 스택·도메인 scope가 실제 코드에서 확인되는 경우만.

## 산출물/완료 판정

- 4개 시나리오별 `*_CODE_FACTS.md` 또는 기존 Analyzer canonical 결과, `*.puml`, 실제 렌더 가능한 `*.svg`, MSC style/manifest JSON, 근거 file/line·function·branch 및 SourceSnapshot.
- `NR_L1TX_KNOWLEDGE_CANDIDATES.md`: 모듈→feature→scenario, 기존 그룹 지식 충돌/중복·업데이트 제안. `AS_IS_CODE_VERIFIED / REVIEW_NEEDED / TO_BE_NOT_CURRENT` 구별.
- `NR_L1TX_EXECUTION_RECEIPT.json`: Job ID, Work ID, source SHA, scenario별 `PASS/FAIL/SKIP/NOT_RUN`, Code Analyzer/Converter/Updater 실제 호출 영수증, MSC 렌더 결과, `GROUP_WRITE=NOT_RUN`, Run Catalog와 Evidence 상태.
- 소스 파일·고객자료·사내 로그·실제 상세 MSC 본문을 사외 서비스에 게시하지 않음. Job-list의 외부 허용 요약은 상태 코드/개수만.
- **PASS**: 코드 근거와 실제 도구 호출·생성물·같은 Run 영수증 4시나리오 모두 확인됐을 때만. 렌더 미실행, 미확인 compile option, 로컬 모델 문장뿐이면 `PARTIAL`.
- **기존 Knowledge 그룹 정본 및 기존 프로젝트 소스/설정은 이번 Job에서 절대 수정하지 않는다.** 신규 파일로 만든 분석 결과/MSC/수정 제안은 허용된 사내 출력에만 저장. K5.8/K6 독립 리뷰가 사내에서만 가능한 경우 `INDEPENDENT_REVIEW=PENDING`으로 기록하고 별도 호출/유료 실행을 가정하지 않는다.
