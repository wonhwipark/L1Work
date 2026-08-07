# SLTE TxMngr Contract UT — 저사양 모델용 Phase 기반 실행 가이드

## 0. 문서 목적

이 문서는 Legacy NR Tx 시나리오를 기준으로 SLTE TxMngr Contract UT를 준비할 때,
저사양 모델이 한 번에 전체 흐름을 추론하지 않고 **정해진 Phase와 스킬을 순차적으로 실행**하도록 하기 위한 운영 가이드다.

핵심 목표는 다음과 같다.

```text
Legacy Scenario Contract
+ SLTE TxMngr Architecture
+ 실제 SLTE UT Source Pattern
= SLTE Contract UT
```

이번 Feature의 기본 예시는 다음과 같다.

```text
Feature ID:
NR_TX_DCI_BWP_SWITCH_PCELL_UL_RANK

예상 Legacy Flow:
1. BWP ID switching event 수신
2. BCH → SCC: PATH_CONFIG_REQ
3. SCC → BCH: PATH_CONFIG_CNF
4. BCH message handler에서 PCell UL Rank update API
5. UL Rank가 실제로 변경되면 BCH → HAL CMD
```

목표는 Full UT 또는 Legacy UT 작성이 아니다.

Legacy 시나리오의 API 경계별 Input/Output을 검증 포인트(VP)로 정의하고,
이를 SLTE TxMngr 책임/API에 Mapping한 뒤,
실제 SLTE UT 소스에서 학습한 선언·Fixture·Jomock·검증 문법으로 Contract UT를 작성한다.

---

# 1. 저사양 모델 운영 원칙

## 1.1 한 번에 전체 작업을 수행하지 않는다

저사양 모델에게 아래처럼 요청하지 않는다.

```text
Legacy 분석하고 SLTE에 Mapping해서 UT까지 만들어줘.
```

반드시 Phase 단위로 진행한다.

```text
P0 → P1 → P2 → ... → P12
```

각 Phase는 이전 Phase의 산출물만 입력으로 사용한다.

---

## 1.2 스킬 선택을 모델에게 맡기지 않는다

각 Phase에서 사용할 스킬과 Action은 이 문서에 고정한다.

저사양 모델은 다음만 수행한다.

```text
1. 현재 Phase 확인
2. 지정된 스킬/Action 실행
3. status / stage / next / outputs 확인
4. 산출물 저장
5. Gate 충족 여부 판단
6. 다음 Phase로 이동 또는 STOP
```

---

## 1.3 가능한 실행은 skillsilent를 Gateway로 사용한다

가능하면 등록된 Action은 아래 형태로 실행한다.

```text
skillsilent run <skill> <action> ...
```

목적:

- 임의 shell 조합 최소화
- 승인 질문 최소화
- 저사양 모델의 명령 생성 부담 감소
- Resume/정책 일관성 유지

`skillsilent`는 분석 스킬이 아니라 **실행 Gateway**로 취급한다.

---

## 1.4 실제 UT 형식을 추정하지 않는다

아래 형식은 설명용 예시일 뿐 기본 형식이 아니다.

```cpp
TEST_F(TxMngrBwpSwitchTest,
       SendsPathConfigReqWithRankMappedFromTargetBwp);
```

실제 SLTE UT가 다른 Test 선언 macro, Fixture, Jomock, input injection,
verification syntax를 사용한다면 반드시 실제 소스에서 먼저 학습한다.

다음 조건이 모두 충족되기 전에는 실제 UT 코드 생성을 진행하지 않는다.

```text
generation_ready = true
UT structure profile status = APPROVED
code_generation_allowed = true
```

---

## 1.5 호출 여부만 검증하는 "껍데기 UT"를 금지한다

각 Verification Point는 다음 두 가지를 모두 가져야 한다.

```text
A. 외부 API/Mock 호출 검증
B. 최소 1개 이상의 실제 필드 값 assert
```

예:

```text
VP-01
- SCC sender가 호출됐는가?
- PATH_CONFIG_REQ의 targetBwpId 또는 ulRank가 Legacy 근거와 일치하는가?
```

`.Times(1)` 등 호출 여부만 있고 필드 값 비교가 없으면 미완성으로 처리한다.

assert 기대값은 반드시 다음 중 하나의 근거가 있어야 한다.

```text
Legacy SDM
Legacy code
code-analyzer field probe
```

근거가 없으면 값을 추정하지 않고 `NEED_REVIEW`로 남긴다.

---

## 1.6 Legacy → SLTE Mapping은 자동화하지 않는다

Code Analyzer가 할 일:

```text
SLTE에서 대응 가능성이 있는 파일/API/클래스 후보를 찾는다.
```

사람이 할 일:

```text
Legacy의 책임을 SLTE의 어느 API/모듈이 담당해야 하는지 결정한다.
```

따라서 다음은 금지한다.

```text
Legacy BCH function A
→ 이름이 비슷한 SLTE function A' 자동 확정
```

Mapping은 책임 기준으로 결정하고 아래 상태로 기록한다.

```text
MAPPED
PARTIAL
MISSING
NOT_APPLICABLE
NEED_REVIEW
```

---

# 2. 사용 스킬 및 현재 실행 가능한 주요 Action

## 2.1 필수 스킬

| 스킬 | 주요 역할 | 현재 사용 Action |
|---|---|---|
| `code-analyzer` | Legacy/SLTE 코드 근거 탐색, 실제 UT 구조 분석 | `route-request`, `feature-scope-probe`, `probe`, `ut-structure-analyze` |
| `slte-knowledge-manager` | 실제 UT 구조 후보 저장/승인/조회 | `learn-ut-structure`, `approve-ut-structure`, `query-ut-structure` |
| `code-fix` | Contract UT 생성 Context 준비, 후보 문법/스코프 검증 | `create-contract-ut`, `contract-ut-validate` |
| `skillsilent` | 위 Action의 Silent 실행 Gateway | `skillsilent run ...` |

## 2.2 조건부 사용 스킬

| 스킬 | 사용 시점 |
|---|---|
| `sdm-parser` | Raw SDM을 분석 가능한 로그로 구조화해야 할 때 |
| `issue-analyzer` | SDM이 복잡하거나 UE/Retry/실패 구간 분리가 필요할 때 |
| `doc-converter` | 최종 분석/Mapping 문서를 HTML 또는 Confluence 형식으로 변환할 때 |

---

# 3. 현재 실행용으로 사용하지 말아야 할 설계/향후 Action 이름

다음 이름들은 방법론 설계에서 논의된 적이 있으나,
현재 저사양 실행 Pipeline에서는 **존재한다고 가정하여 호출하지 않는다.**

```text
scenario-contract-analyze
log-code-correlate
learn-runtime-log
prepare-ut-verification
map-ut-verification-to-slte
```

저사양 모델은 없는 Action을 임의로 만들어 호출하면 안 된다.

해당 기능은 현재 존재하는 Action과 사람 Gate를 조합하여 수행한다.

---

# 4. 전체 State Machine

```text
P0  환경/스킬 확인
 ↓
P1  Legacy SDM 구조화
 ↓
P2  Legacy Feature Scope 탐색
 ↓
P3  Legacy Field/API Evidence 보완
 ↓
P4  Verification Point 작성
 ↓
P5  SLTE TxMngr 대응 후보 탐색
 ↓
P6  실제 SLTE UT 구조 학습
 ↓
P7  UT Structure Profile 저장/승인
 ↓
P8  Legacy → SLTE Mapping 확정
 ↓
P9  Contract UT 생성 Context 준비
 ↓
P10 VP별 UT 후보 작성 + Validation
 ↓
P11 Code Fix 변경 절차로 반영
 ↓
P12 신규 UT + Regression + As-built 정리
```

---

# 5. Phase별 상세 실행 가이드

## P0. 환경 및 스킬 확인

### 목적

작업 시작 전에 필요한 스킬과 신규 Action이 실제로 인식되는지 확인한다.

### 사용 스킬

```text
skillsilent
code-analyzer
slte-knowledge-manager
code-fix
```

### 확인 대상

최소 다음 Action이 존재해야 한다.

```text
code-analyzer:
- ut-structure-analyze

slte-knowledge-manager:
- learn-ut-structure
- approve-ut-structure
- query-ut-structure

code-fix:
- create-contract-ut
- contract-ut-validate
```

Legacy 탐색에는 가능한 경우 다음을 사용한다.

```text
code-analyzer:
- route-request
- feature-scope-probe
- probe
```

### PASS 조건

```text
required_skills_present = true
required_actions_present = true
```

### FAIL 시

다음 Phase로 넘어가지 않는다.

---

## P1. Legacy SDM 구조화

### 목적

Raw SDM에서 Feature 관련 시간 순서와 Message/Event를 읽을 수 있는 형태로 만든다.

### 사용 스킬

기본:

```text
sdm-parser
```

로그가 복잡한 경우:

```text
issue-analyzer
+ SDM converter/parser
```

### 입력

```text
Legacy SDM path
Feature ID
관련 keyword
```

예:

```text
DCI
BWP
PATH_CONFIG_REQ
PATH_CONFIG_CNF
UL Rank
PCell
HAL
```

### 출력

최소 다음 정보가 확보돼야 한다.

```text
event/order
cell context
message/API name
BWP ID
UL Rank
success/fail indication
```

### PASS 조건

```text
Feature 관련 로그 구간을 특정할 수 있음
```

### SKIP 조건

이미 분석 가능한 `_l1sw.txt` 또는 구조화 로그가 있다면 P1을 생략할 수 있다.

---

## P2. Legacy Feature Scope 탐색

### 목적

Legacy 1900에서 실제 Feature 관련 코드 파일/API 범위를 좁힌다.

### 사용 스킬

```text
code-analyzer
```

### 기본 진입

저사양 모델에서는 자유 코드 탐색보다 먼저:

```text
route-request
```

또는 Feature 범위 탐색이 필요한 경우:

```text
feature-scope-probe
```

를 사용한다.

### 입력

```text
Legacy source root
Feature ID
P1 로그 근거
관련 Message/API keyword
```

### 찾아야 할 항목

```text
BWP switching event handler
PATH_CONFIG_REQ 생성/전송 경로
PATH_CONFIG_CNF handler
PCell UL Rank update API
HAL CMD 생성/전송 경로
관련 데이터 구조체
```

### 출력

```text
legacy_feature_scope.json 또는 동등 산출물
관련 file/function/API 목록
evidence 위치
```

### PASS 조건

VP-01~03을 정의할 수 있는 최소 API 경계가 확보됨.

---

## P3. Legacy Field/API Evidence 보완

### 목적

UT에서 assert할 실제 필드 값 관계를 Legacy 근거로 확정한다.

### 사용 스킬

```text
code-analyzer
```

### 사용 Action

특정 필드 근거가 부족할 때:

```text
probe
```

또는 현재 Code Analyzer의 field probe 기능을 사용한다.

### 우선 추적 필드 예시

VP-01:

```text
Message ID
Cell ID
Target BWP ID
UL Rank
```

VP-02:

```text
PCell ID
BWP ID
Confirmed/Applied UL Rank
Result
```

VP-03:

```text
HAL CMD ID
Cell ID
Target BWP ID
Updated UL Rank
```

### 출력

각 필드에 대해:

```text
field
source
assignment/read evidence
expected relationship/value
confidence
```

### PASS 조건

각 VP에서 최소 1개 이상의 assert 후보 필드가 Legacy 근거를 가짐.

### 부족한 경우

```text
NEED_REVIEW
```

로 남기며 값을 추정하지 않는다.

---

## P4. Verification Point 작성

### 목적

Legacy 내부 함수명이 아니라 외부에서 관찰 가능한 Input/Output Contract를 작성한다.

### 사용 스킬

전용 자동 Action 없음.

```text
code-analyzer의 P2/P3 산출물
+ 정해진 Schema
+ 사람 의미 검토
```

### 저사양 모델이 채울 Schema

```text
VP_ID
Trigger
Input
Input_Evidence
Expected_External_Output
Required_Assert_Field
Expected_Value_or_Relationship
Legacy_Evidence
Negative_Candidate
Status
```

### 기본 VP

```text
VP-01:
BWP switching input
→ PATH_CONFIG_REQ output

VP-02:
PATH_CONFIG_CNF input
→ PCell UL Rank Update API

VP-03:
UL Rank changed input
→ HAL CMD output
```

### 필수 규칙

각 VP에는 반드시:

```text
mock/API call check
+ field value assert ≥ 1
```

이 포함돼야 한다.

### 출력

```text
ut_verification_points.md
```

권장 표:

| VP | Trigger | Input | Expected Output | 필수 Assert Field | Legacy 근거 | 상태 |
|---|---|---|---|---|---|---|

### 사람 Gate

VP 의미가 맞는지 확인하기 전 P8 Mapping 확정 또는 UT 생성으로 넘어가지 않는다.

---

## P5. SLTE TxMngr 대응 후보 탐색

### 목적

SLTE에서 각 VP 책임을 담당할 가능성이 있는 API/모듈 후보를 찾는다.

### 사용 스킬

```text
code-analyzer
```

### 권장 진입

```text
route-request
feature-scope-probe
```

### 입력

```text
SLTE TxMngr source root
VP-01~03
Feature ID
```

### 출력

예:

```text
VP-01 candidate:
- TxMngr::<candidate A>
- SCC adapter::<candidate B>

VP-02 candidate:
- TxMngr::<candidate C>

VP-03 candidate:
- TxMngr::<candidate D>
- HAL adapter::<candidate E>
```

### 중요

이 Phase에서는 후보를 찾을 뿐 `MAPPED`를 자동 확정하지 않는다.

---

## P6. 실제 SLTE UT 구조 학습

### 목적

실제 SLTE NR Tx UT가 사용하는 문법을 학습한다.

### 사용 스킬

```text
code-analyzer
```

### Action

```text
ut-structure-analyze
```

### 입력

```text
SLTE NR Tx UT root
Feature ID
대표 UT 후보
```

### 우선 학습 대상

```text
Test declaration token/macro
Fixture/Suite
SetUp/TearDown
Jomock pattern
input/message injection pattern
external API expectation
field comparator/assert syntax
build/registration pattern
representative files
```

### 출력

```text
ut_structure_profile.json
ut_structure_report.md
review_questions.json
```

### 반드시 확인

```text
generation_ready
allowed_declaration_tokens
forbidden_unobserved_default_tokens
fixture_patterns
mock_patterns
verification_patterns
representative_files
```

### PASS 조건

```text
generation_ready = true
```

### FAIL 시

UT를 생성하지 않는다.

다음 중 하나를 수행한다.

```text
Feature 인접 UT 파일 추가
TxMngr 관련 폴더로 범위 축소
SCC/HAL 유사 UT 추가
Jomock/Verification 예제 보완
```

---

## P7. UT Structure Profile 저장 및 승인

### 목적

P6의 실제 UT 형식을 지식매니저에 Candidate로 저장하고 승인한다.

### 사용 스킬

```text
slte-knowledge-manager
```

### Step 1

```text
learn-ut-structure
```

결과:

```text
CANDIDATE
code_generation_allowed = false
```

### Step 2 — 사람 Gate

대표 실제 파일과 학습 결과를 확인한다.

확인 대상:

```text
Test declaration
Fixture
Jomock
input injection
field comparator/assert
representative files
```

### Step 3

승인 시:

```text
approve-ut-structure
```

### Step 4

실사용 전:

```text
query-ut-structure
```

### PASS 조건

```text
profile status = APPROVED
code_generation_allowed = true
```

---

## P8. Legacy → SLTE Mapping 확정

### 목적

P4의 Verification Point를 P5에서 찾은 SLTE 후보에 책임 기준으로 Mapping한다.

### 자동화 수준

```text
수작업 / 사람 Gate
```

### 스킬 역할

`code-analyzer`:

```text
Legacy와 SLTE의 근거/후보 제공
```

`slte-knowledge-manager`:

```text
승인된 UT 구조 조회/지식 보조
```

하지만 대응 API 자체를 자동 확정하는 전용 Action으로 사용하지 않는다.

### Mapping 표

| VP | Legacy Responsibility | SLTE Candidate | 최종 Mapping | 상태 | 근거 |
|---|---|---|---|---|---|

### 상태

```text
MAPPED
PARTIAL
MISSING
NOT_APPLICABLE
NEED_REVIEW
```

### 중요

이 Phase는 전체 과정에서 공수가 가장 큰 구간으로 계획한다.

### PASS 조건

UT 작성에 필요한 VP의 Mapping이 최소 `MAPPED` 또는 의도된 `MISSING/PARTIAL` 상태로 명확함.

---

## P9. Contract UT 생성 Context 준비

### 목적

승인된 UT Source Pattern과 VP/Mapping만 남긴 제한된 생성 Context를 준비한다.

### 사용 스킬

```text
code-fix
```

### Action

```text
create-contract-ut
```

### 중요

```text
create-contract-ut
≠ C++ UT 파일을 최종 생성하는 Action

create-contract-ut
= 실제 UT 생성을 위한 제한된 Context/Guide 준비
```

### 입력

```text
APPROVED UT profile
ut_verification_points.md
slte_txmngr_mapping.md
target UT root
```

### PASS 조건

```text
status = READY
approved UT pattern available
target scope = UT folder only
```

---

## P10. VP별 UT 후보 작성 및 Validation

### 목적

한 번에 전체 UT를 만들지 않고 VP 하나씩 실제 후보를 작성·검증한다.

### 저사양 모델 필수 규칙

다음 순서를 반복한다.

```text
VP-01
→ 후보 작성
→ contract-ut-validate
→ field assert 의미 검토
→ 완료

VP-02
→ 후보 작성
→ contract-ut-validate
→ field assert 의미 검토
→ 완료

VP-03
→ 후보 작성
→ contract-ut-validate
→ field assert 의미 검토
→ 완료
```

### 사용 스킬

후보 Context:

```text
code-fix create-contract-ut 결과
```

문법/스코프 검증:

```text
code-fix contract-ut-validate
```

### Validator가 확인하는 것

주로:

```text
승인된 Test declaration token 사용 여부
UT scope 준수 여부
금지된/미관찰 Framework token 사용 여부
```

### Validator만으로 확인되지 않는 것

다음은 반드시 사람이 확인한다.

```text
assert 대상 필드가 실제 Feature 정답을 검증하는가?
assert 기대값이 Legacy 근거와 일치하는가?
호출 여부만 보고 끝나는 껍데기 UT가 아닌가?
```

### Semantic Gate 체크리스트

```text
[ ] 외부 API/Mock 호출 검증 존재
[ ] 최소 1개 field value assert 존재
[ ] assert 값/관계의 Legacy 근거 존재
[ ] 내부 private helper 호출에 과도하게 결합하지 않음
[ ] Feature와 관계없는 reserved/padding/runtime 값 비교하지 않음
```

### FAIL 시

다음 VP로 넘어가지 않는다.

---

## P11. 실제 변경 절차로 반영

### 목적

검증된 UT 후보를 기존 Code Fix 변경 Workflow로 반영한다.

### 사용 스킬

```text
code-fix
```

### 적용 원칙

```text
Allowed:
<SLTE NR Tx UT root>/**

Denied:
<SLTE production source>/**
```

Production 구현은 이번 Contract UT 생성 단계에서 자동 수정하지 않는다.

### Gate

기존 Code Fix의:

```text
G1
G2
```

승인 절차를 따른다.

---

## P12. 신규 UT 실행, Regression, As-built 정리

### 목적

Production 구현 이후 Contract UT가 실제 기능의 executable specification 역할을 하는지 확인한다.

### 확인

```text
신규 Contract UT PASS
기존 NR Tx UT Regression PASS
```

### 의미 확인

다음이 모두 성립해야 한다.

```text
UT PASS
= API가 호출됐음
+ Feature 관련 실제 필드 값이 Legacy Contract와 일치함
```

호출 여부만 PASS한 것은 완료가 아니다.

### 최종 산출물

```text
legacy_scenario_flow.md
ut_verification_points.md
slte_txmngr_mapping.md
slte_gap_report.md
approved_ut_structure_profile
contract_ut_context
validated_ut_patch
ut_execution_result.md
as_built_mapping.md
```

---

# 6. Phase 요약표

| Phase | 핵심 작업 | 스킬/Action | 자동화 | 사람 Gate |
|---|---|---|---|---|
| P0 | 환경 확인 | skillsilent + 각 스킬 | 자동 | 없음 |
| P1 | SDM 구조화 | sdm-parser / issue-analyzer | 자동 | 필요 시 |
| P2 | Legacy Scope | code-analyzer route-request / feature-scope-probe | 자동 | 낮음 |
| P3 | Field Evidence | code-analyzer probe/field probe | 자동 | 값 의미 확인 |
| P4 | VP 작성 | 정해진 Schema + 근거 | 반자동 | **필수** |
| P5 | SLTE 후보 탐색 | code-analyzer | 자동 | 후보만 |
| P6 | 실제 UT 구조 학습 | code-analyzer ut-structure-analyze | 자동 | 근거 확인 |
| P7 | UT Profile 승인 | knowledge-manager learn/approve/query | 반자동 | **필수** |
| P8 | Legacy→SLTE Mapping | 사람 + 코드 근거 | 수작업 | **필수/최대 공수** |
| P9 | 생성 Context | code-fix create-contract-ut | 자동 | 없음 |
| P10 | VP별 UT + validate | code-fix contract-ut-validate | 반자동 | **필드 의미 필수** |
| P11 | Patch 반영 | code-fix G1/G2 | 반자동 | **필수** |
| P12 | UT/Regression | Build/UT | 자동+검토 | 결과 검토 |

---

# 7. 저사양 Claude Code 최초 로딩용 프롬프트

아래 프롬프트를 이 문서와 함께 사용한다.

```text
첨부한 `slte_contract_ut_low_spec_model_phase_guide_0807.md`를 이번 작업의 실행 가이드로 사용해줘.

중요:
- 전체 작업을 한 번에 수행하지 마.
- 반드시 P0부터 시작해서 현재 Phase 하나만 수행해.
- 각 Phase 완료 시 status, outputs, next_phase, stop_reason을 짧게 출력해.
- 이전 Phase의 산출물을 다음 Phase 입력으로 사용해.
- 등록되지 않은 Action 이름을 임의로 만들지 마.
- 가능한 Action 실행은 skillsilent run을 사용해.
- 실제 SLTE UT 형식을 추정하지 마.
- TEST_F, TEST, TEST_P를 실제 소스에서 관찰하지 않았다면 사용하지 마.
- generation_ready=true, UT profile APPROVED, code_generation_allowed=true 전에는 UT 코드를 만들지 마.
- Legacy→SLTE Mapping을 자동 확정하지 마. P5에서는 후보만 찾고 P8에서 사람 검토 대상으로 남겨.
- VP는 호출 여부만 검증하면 안 되고 최소 1개 이상의 실제 field value assert를 가져야 해.
- assert 기대값은 Legacy SDM/code/field probe 근거가 있어야 하며 추정하지 마.
- P10에서는 VP-01, VP-02, VP-03을 한 번에 작성하지 말고 하나씩 작성→validate→의미 검토 순서로 진행해.
- Production source는 수정하지 마.

Feature ID:
NR_TX_DCI_BWP_SWITCH_PCELL_UL_RANK

예상 Legacy Flow:
1. BWP ID switching event
2. BCH → SCC PATH_CONFIG_REQ
3. SCC → BCH PATH_CONFIG_CNF
4. PCell UL Rank update
5. Rank changed → HAL CMD

먼저 P0만 수행해줘.
P0 결과에 필요한 경로가 없으면 필요한 경로 목록만 출력하고 STOP해줘.
```

---

# 8. Phase 완료 출력 형식

저사양 모델은 각 Phase 종료 시 자유 서술 대신 아래 형태로 출력한다.

```text
PHASE: Pn
STATUS: PASS | NEED_REVIEW | FAIL | STOP
SKILL:
ACTION:
INPUTS:
OUTPUTS:
EVIDENCE:
HUMAN_GATE_REQUIRED: true | false
STOP_REASON:
NEXT_PHASE:
```

예:

```text
PHASE: P6
STATUS: PASS
SKILL: code-analyzer
ACTION: ut-structure-analyze
OUTPUTS:
- ut_structure_profile.json
- ut_structure_report.md
EVIDENCE:
- declaration token: <actual observed token>
- representative files: 4
- jomock patterns: found
- verification patterns: found
HUMAN_GATE_REQUIRED: true
NEXT_PHASE: P7
```

---

# 9. STOP 규칙

아래 조건에서는 자동으로 다음 Phase로 넘어가지 않는다.

## STOP-01

```text
필수 스킬/Action 없음
```

→ P0에서 STOP

## STOP-02

```text
Legacy 시나리오 근거 부족
```

→ P2/P3에서 STOP 또는 NEED_REVIEW

## STOP-03

```text
VP assert 값 근거 없음
```

→ P4에서 `NEED_REVIEW`

## STOP-04

```text
generation_ready=false
```

→ P6에서 STOP

## STOP-05

```text
UT profile 미승인
```

→ P7에서 STOP

## STOP-06

```text
Legacy→SLTE Mapping 미확정
```

→ P8에서 STOP

## STOP-07

```text
contract-ut-validate FAIL
```

→ P10에서 해당 VP만 재작업

## STOP-08

```text
호출 검증만 있고 field value assert 없음
```

→ Validator가 PASS하더라도 Semantic Gate에서 STOP

---

# 10. 최종 성공 기준

다음이 모두 충족돼야 완료다.

```text
[ ] Legacy 시나리오 근거 확보
[ ] VP-01~03 정의
[ ] 각 VP에 최소 1개 field value assert 정의
[ ] assert 값에 Legacy 근거 존재
[ ] SLTE Mapping 상태 확정
[ ] 실제 UT Source Pattern 학습 완료
[ ] UT Structure Profile APPROVED
[ ] VP별 candidate가 actual UT syntax를 따름
[ ] contract-ut-validate PASS
[ ] Semantic Gate PASS
[ ] 신규 Contract UT PASS
[ ] 기존 NR Tx UT Regression PASS
[ ] As-built Mapping 정리 완료
```

---

# 11. 운영 판단 요약

저사양 모델에서 가장 중요한 것은 "더 많이 자동화"하는 것이 아니라
**모델이 판단해야 하는 범위를 줄이는 것**이다.

따라서 아래 역할 분리가 기준이다.

```text
Python/Skill:
- 탐색
- 구조화
- 실제 UT 패턴 추출
- 문법/스코프 검증
- 산출물 관리

저사양 모델:
- 정해진 Schema 채우기
- status/next 소비
- VP 하나씩 후보 작성

사람:
- VP 의미 확정
- Legacy → SLTE Mapping 결정
- field assert 정답 검토
- UT Profile 승인
- G1/G2 승인
```

이 분리를 유지하면 저사양 모델에서도 Contract UT 준비 Workflow를 단계적으로 수행할 수 있다.
