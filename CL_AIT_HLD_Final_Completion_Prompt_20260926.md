# CL-AIT HLD Final Completion Prompt

- Version: v1.0
- Date: 2026-09-26 KST
- Mode: One-shot completion
- Goal: 기존 CL-AIT 결과를 최대한 재사용하여 NR HLD와 LTE HLD를 각각 독립적으로 완결하고, Common HLD의 필요성을 실제 구현 근거로 재판정한 뒤 Class Diagram, PlantUML MSC, traceability까지 최종 정합화한다.

---

# 0. 작업 성격

이 작업은 새로운 architecture 설계가 아니다.

다음을 우선 재사용한다.

- 기존 Common HLD
- 기존 NR HLD
- 기존 LTE HLD
- 기존 Integrated HLD
- Decision Ledger
- Gap Matrix
- As-Built 자료
- Scenario UT
- Production Code
- 기존 PlantUML
- 기존 CL-AIT skill 산출물

목표 흐름:

```text
기존 결과 재사용
    ↓
Production Code 재확인
    ↓
잘못된 HLD abstraction 제거
    ↓
NR HLD 독립 완결
    ↓
LTE HLD 독립 완결
    ↓
Class Diagram + MSC 필수 보강
    ↓
Common HLD 필요성 재판정
    ↓
Cross-HLD contradiction 제거
    ↓
Final Completion Gate
```

처음부터 HLD를 다시 작성하지 않는다.

---

# 1. Source of Truth

Architecture, class ownership, inheritance, interface, runtime sequence 판단 우선순위:

```text
1. Current Production Code
2. Verified As-Built artifact
3. Verified Decision Ledger
4. Scenario UT / Build evidence
5. Existing HLD
6. 추론
```

Existing HLD와 Production Code가 충돌하면 Production Code 기준으로 HLD를 수정한다.

HLD에 맞추기 위해 production code를 임의 변경하지 않는다.

---

# 2. 핵심 Guardrail — Commonality != Inheritance

반드시 다음을 구분한다.

```text
같은 목적
!= 같은 runtime concept
!= 같은 class
!= 공통 Base Class
!= inheritance
```

NR과 LTE가 유사한 기능이나 sequence를 가진다는 이유만으로 공통 Base Class를 만들거나 HLD에 표현하지 않는다.

Inheritance는 실제 코드에 다음 증거가 있을 때만 표현한다.

- 실제 Base Class 선언
- 실제 상속 선언
- 실제 shared abstract interface
- 실제 virtual/pure virtual contract

근거가 없으면 inheritance 표현 금지.

현재 확인된 전제:

```text
NR CL-AIT = NR 전용 concrete class
LTE CL-AIT = LTE 전용 concrete class
NR/LTE 공통 Base Class 사용 안 함
```

따라서 기존 Common/Integrated HLD에 가상의 공통 Base Class가 있으면 오류 후보로 분류하고 실제 코드 근거가 없으면 제거한다.

---

# 3. 최종 Mandatory 산출물

1. NR HLD — FINAL SSOT
2. LTE HLD — FINAL SSOT
3. NR PlantUML Class Diagram
4. LTE PlantUML Class Diagram
5. NR PlantUML MSC
6. LTE PlantUML MSC
7. NR/LTE HLD ↔ Code ↔ Diagram Traceability
8. Common HLD 필요성 판정
9. Common을 유지하면 정정된 Common HLD
10. Integrated HLD가 기존 deliverable이면 정정된 Integrated HLD
11. Contradiction Audit
12. Final Completion Report

기존 파일이 있으면 update한다. 불필요한 중복 파일을 새로 만들지 않는다.

---

# 4. Common HLD 필요성 재판정

Common HLD를 자동 유지하지 않는다.

반드시 실제 code fact로 다음 중 하나를 판정한다.

```text
KEEP
REDUCE
RETIRE
```

## KEEP

실제 공통 구현이 충분히 존재할 때:

- 공통 Manager/Orchestrator
- 공통 runtime owner
- 공통 DB
- 공통 state machine
- 공통 interface class
- 공통 SHM owner
- 공통 timer/periodic owner
- 공통 lifecycle implementation
- 공통 error/skip implementation
- 실제 shared production component

단, 실제 존재하지 않는 Base Class는 추가하지 않는다.

## REDUCE

다음과 같은 경우:

- NR/LTE production class는 별도
- 주요 state도 RAT별 별도
- 주요 runtime ownership도 RAT별 별도
- 다만 목적/용어/상위 orchestration/공통 policy는 공유

이 경우 Common HLD는 얇은 공통 개념 문서로 축소한다.

포함 가능:

- Purpose
- Scope
- Terminology
- Common high-level lifecycle concept
- Common external trigger concept
- Common policy/constraint
- 실제 shared component
- NR/LTE HLD navigation

포함 금지:

- 가상의 Base Class
- 가상의 common FSM
- 가상의 common state ownership
- 가상의 inheritance
- RAT별 구현 detail
- RAT별 payload를 하나의 common payload처럼 표현

## RETIRE

다음과 같은 경우:

- 실제 common implementation이 사실상 없음
- Common HLD가 NR/LTE HLD를 반복 요약하는 수준
- 유지할수록 abstraction 오류나 중복이 발생
- 공통 내용이 README/index 수준을 넘지 않음

이 경우 Architecture SSOT는 다음으로 고정한다.

```text
NR HLD  = SSOT
LTE HLD = SSOT
```

필요하면 Common 문서는 `CL-AIT Overview / HLD Index / Common Concepts` 수준의 비-SSOT 문서로만 남긴다.

---

# 5. 기존 HLD 재사용 규칙

각 section을 다음 상태로 분류한다.

- KEEP
- FIX
- MOVE
- REMOVE
- ADD
- N/A
- NEEDS_DECISION

기존에 맞는 내용은 유지한다.
문서 전체 rewrite 금지.

---

# 6. NR HLD 독립 완결

NR HLD는 NR 문서 하나만 읽어도 구현과 runtime을 이해할 수 있어야 한다.

최소 포함:

## 6.1 Purpose / Scope
- 목적
- 적용 범위
- 제외 범위

## 6.2 Architecture
- 실제 NR concrete class
- owner
- creation
- caller
- dependency
- Common manager가 있으면 실제 관계
- HAL/PHY/RF 관계

## 6.3 Runtime
- Init
- TX ON
- Operation Info Update
- DUMP_IND
- START_REQ
- START_CNF
- Periodic
- Skip
- Retry
- Failure
- TX OFF
- Release
- Cleanup

## 6.4 NR-specific Contract
- SHM
- demod/CC handling
- dump payload
- SAR/MTPL
- state
- timer
- PHY IPC
- RF interaction

## 6.5 Error / Corner Case
실제 코드에 존재하는 항목만 작성:
- invalid state
- duplicate event
- TX OFF race
- Release race
- pending START_CNF
- invalid indication
- periodic skip/retry

## 6.6 Implementation Status
- implemented
- partial
- N/A
- pending verification

---

# 7. LTE HLD 독립 완결

LTE HLD도 LTE 문서 하나만 읽어도 구현과 runtime을 이해할 수 있어야 한다.

기존 Legacy LTE 분석 + 현재 SLTE LTE As-Built 결과를 재사용한다.

## 7.1 Purpose / Scope
- 목적
- 적용 범위
- 제외 범위

## 7.2 Architecture
- 실제 LTE concrete class
- owner
- creation
- caller
- dependencies
- Common manager와 실제 관계
- HAL/PHY/RF 관계

## 7.3 Runtime
- Init
- TX ON
- operation info update
- DUMP_IND
- START_REQ
- START_CNF
- periodic
- skip/retry
- fail
- TX OFF
- Release
- Cleanup

## 7.4 LTE-specific Contract

### LTE Shared Memory
Legacy LTE도 runtime 정보를 SHM에 write한다.
현재 SLTE LTE implementation과 실제 contract 정합 확인.

### LTE demod CC
LTE는 PCell fixed.
NR식 dynamic demod resolver를 LTE에 새로 설계하지 않는다.

### LTE Dump Payload
LTE-specific payload contract를 사용.
NR payload를 근거 없이 재사용하지 않는다.

### MTPL/SAR
현재 SLTE LTE CL-AIT scope에서는 dependency 없음.
`NOT_APPLICABLE` 또는 명확한 scope-out으로 기록.

## 7.5 Error / Corner Case
- START_CNF fail
- TX OFF / Release race
- periodic skip
- cleanup
- invalid state
- duplicate/late event

실제 코드 기준으로 작성한다.

---

# 8. PlantUML Class Diagram — REQUIRED

Class Diagram은 선택 산출물이 아니다.

NR과 LTE 각각 반드시 존재해야 한다.

## 8.1 NR Class Diagram

실제 production code 기준.

포함:
- 핵심 NR CL-AIT concrete class
- owner/manager
- 주요 dependency
- DB/Observer/SharedMemory
- HAL/PHY interface
- 주요 runtime/public method
- composition / association / dependency
- 실제 inheritance가 있으면 inheritance

금지:
- 코드에 없는 class
- 코드에 없는 Base Class
- 이름 유사성만으로 관계 생성
- 가상의 layer/class 생성

## 8.2 LTE Class Diagram

동일 원칙 적용.

특히 NR과 LTE를 가상의 공통 Base Class로 묶지 않는다.

## 8.3 Relation Verification

각 관계를 실제 code evidence와 함께 다음 중 하나로 분류한다.

```text
Inheritance
Composition
Aggregation
Association
Dependency
Call
None
```

---

# 9. PlantUML MSC — REQUIRED

MSC는 단순 illustrative diagram이 아니라 actual runtime sequence의 As-Built representation이어야 한다.

NR과 LTE 각각 반드시 생성/갱신한다.

---

# 10. NR MSC Required Scenarios

실제 구현에 존재하는 scenario 기준으로 최소 다음을 커버한다.

1. Initialization
2. TX ON / Operation Info Update
3. DUMP_IND → START_REQ → START_CNF Success
4. START_CNF Failure
5. Periodic / Skip / Retry
6. TX OFF / Release / Cleanup

필요하면 실제 코드 기준 scenario를 추가한다.

---

# 11. LTE MSC Required Scenarios

최소 다음을 커버한다.

1. Initialization
2. TX ON / SHM Operation Info Update
3. DUMP_IND — LTE-specific payload 반영
4. START_REQ → START_CNF Success — PCell fixed demod CC 반영
5. START_CNF Failure
6. Periodic / Skip / Retry
7. TX OFF / Release / Cleanup

Legacy와 현재 target 차이가 필요한 경우 note로 표시하되,
최종 runtime은 current As-Built target 기준으로 작성한다.

---

# 12. MSC 작성 규칙

Participant는 실제 component/class/interface를 사용한다.

실제 코드에 없는 다음과 같은 participant 생성 금지:

```text
GenericBase
CommonClAitBase
SharedClAit
```

메시지는 가능한 한 실제 API/event/IPC 명칭을 사용한다.

예:
- MEAS_RESULT_IND
- DUMP_IND
- START_REQ
- START_CNF
- UpdateClAitOperationInfo()

최종 명칭은 실제 코드에서 검증한다.

---

# 13. Architecture Evidence Matrix — REQUIRED

HLD 수정 전에 다음 matrix를 작성한다.

| Item | Common | NR | LTE | Code Evidence | HLD Action |
|---|---|---|---|---|---|
| Main Class | | | | | |
| Base Class | | | | | |
| State Owner | | | | | |
| Periodic Owner | | | | | |
| SHM Owner | | | | | |
| Dump Payload | | | | | |
| START_REQ Owner | | | | | |
| START_CNF Owner | | | | | |
| Release Owner | | | | | |

Base Class는 특히 명확하게 기록한다.

실제 코드가 그렇다면:

```text
NR Base Class  : NONE
LTE Base Class : NONE
Shared Base    : NONE
```

을 HLD와 Diagram에도 그대로 반영한다.

---

# 14. HLD ↔ Diagram Completion Gate

다음을 모두 통과하지 못하면 SSOT 완료로 판정하지 않는다.

## NR

```text
NR HLD ↔ Production Code    = MATCH
NR HLD ↔ Class Diagram      = MATCH
NR HLD ↔ MSC                = MATCH
NR Class Diagram ↔ Code     = MATCH
NR MSC ↔ Runtime Code       = MATCH
```

## LTE

```text
LTE HLD ↔ Production Code   = MATCH
LTE HLD ↔ Class Diagram     = MATCH
LTE HLD ↔ MSC               = MATCH
LTE Class Diagram ↔ Code    = MATCH
LTE MSC ↔ Runtime Code      = MATCH
```

하나라도 mismatch면 `FIX_REQUIRED`.

---

# 15. Common HLD Correction

Common을 KEEP 또는 REDUCE하는 경우 반드시 제거:

- 코드에 없는 Base Class
- 코드에 없는 inheritance
- 실제로 RAT별인 state를 shared state처럼 표현한 내용
- 실제로 RAT별인 payload를 common payload처럼 표현한 내용
- RAT별 구현을 common implementation처럼 표현한 내용

Common에는 실제 공통 수준만 남긴다.

---

# 16. Integrated HLD

기존 Integrated HLD가 deliverable이면 유지/갱신한다.

Integrated HLD는 SSOT가 아니다.

정본은:

```text
NR HLD
LTE HLD
```

Common이 실제로 필요하면 보조 shared-concept 문서로 둔다.

Integrated 목적:
- review
- cross-RAT comparison
- overview
- architecture navigation

Integrated에서도 가상의 Base Class를 사용하지 않는다.

---

# 17. NR vs LTE Difference Table

최종 문서에 실제 사실 기반 비교표를 유지한다.

| Item | NR | LTE |
|---|---|---|
| Main concrete class | actual | actual |
| Common Base Class | NONE/actual | NONE/actual |
| SHM | NR contract | LTE contract |
| demod/CC | NR-specific | PCell fixed |
| Dump payload | NR-specific | LTE-specific |
| SAR/MTPL | actual behavior | CL-AIT N/A |
| Periodic | actual | actual |
| Release | actual | actual |

추측 금지.

---

# 18. Traceability

NR/LTE 각각 다음 연결을 완성한다.

```text
Requirement / Decision
        ↓
Code Fact
        ↓
Production Code
        ↓
Class Diagram
        ↓
MSC
        ↓
Scenario UT
        ↓
HLD
```

Scenario UT 또는 Build evidence가 없으면 상태만 정확히 표시한다.
그 이유로 HLD architecture를 다시 열지 않는다.

---

# 19. Contradiction Audit — REQUIRED

최종 단계에서 탐지:

- HLD Base Class 존재 / Code Base Class 없음
- HLD inheritance / Code inheritance 없음
- HLD common state / Code RAT-specific state
- HLD common payload / Code RAT-specific payload
- Class owner mismatch
- API owner mismatch
- MSC participant mismatch
- MSC message mismatch
- HLD sequence와 runtime code sequence mismatch
- NR behavior를 LTE에 복사
- LTE behavior를 NR에 복사
- Common과 NR/LTE 간 중복/모순

결과 형식:

| ID | Artifact | Problem | Code Fact | Action | Status |
|---|---|---|---|---|---|

---

# 20. 사용자 질문 최소화

Code Fact로 해결 가능한 것은 사용자에게 묻지 않는다.

다음 경우에만 `[NEEDS_DECISION]`:

- 실제 코드에 두 개 이상의 동등한 architecture 선택지가 존재
- branch가 불완전하여 fact 확인 불가
- 기존 Decision과 production code가 직접 충돌
- 문서 수정이 아닌 새로운 architecture 결정이 필요

그 외에는 자동으로 끝까지 진행한다.

---

# 21. Production Code 변경 정책

기본 목적은 HLD final completion이다.

```text
HLD 오류       → HLD 수정
Diagram 오류   → Diagram 수정
Traceability 부족 → Artifact 보강
```

Production code를 HLD에 맞추기 위해 변경하지 않는다.

실제 runtime defect가 발견되면 자동 refactoring하지 말고:

```text
[CODE_DEFECT_FOUND]

Fact:
Impact:
Affected Code:
Required Action:
HLD Impact:
```

로 별도 기록한다.

---

# 22. One-shot 수행 순서

중간 종료 없이 다음 순서대로 수행한다.

```text
01. 기존 Common / NR / LTE / Integrated HLD inventory
02. 기존 PlantUML inventory
03. Decision / Gap / As-Built / Scenario UT inventory
04. Current Production Code class inventory
05. NR actual class hierarchy 확인
06. LTE actual class hierarchy 확인
07. Common implementation 존재 여부 확인
08. Architecture Evidence Matrix 작성
09. Common Base Class 오류 탐지
10. Common HLD KEEP / REDUCE / RETIRE 판정

11. NR HLD KEEP/FIX/MOVE/REMOVE/ADD 분류
12. NR HLD As-Built 보강
13. NR Class Diagram 생성/보강
14. NR MSC 생성/보강
15. NR HLD ↔ Code ↔ Diagram audit

16. LTE HLD KEEP/FIX/MOVE/REMOVE/ADD 분류
17. LTE HLD As-Built 보강
18. LTE Class Diagram 생성/보강
19. LTE MSC 생성/보강
20. LTE HLD ↔ Code ↔ Diagram audit

21. Common HLD 수정 / 축소 / retire
22. Integrated HLD가 있으면 As-Built 기준 갱신
23. NR vs LTE difference 정리
24. Traceability 보강
25. Global contradiction audit
26. 누락 artifact 재검사
27. Final Completion Gate
28. 최종 파일 상태 확정
29. Completion Report 작성
```

실제 새로운 architecture decision이 필요하지 않는 한 중간에 STOP하지 않는다.

---

# 23. Final Completion Gate

## NR

다음 모두 만족:
- architecture complete
- runtime complete
- error/release complete
- NR-specific contract complete
- Class Diagram exists
- MSC exists
- code aligned
- traceability aligned

상태:

```text
NR HLD = SSOT_COMPLETE
```

## LTE

다음 모두 만족:
- architecture complete
- runtime complete
- LTE SHM complete
- PCell fixed demod complete
- LTE-specific dump complete
- MTPL/SAR scope complete
- release/error complete
- Class Diagram exists
- MSC exists
- code aligned
- traceability aligned

상태:

```text
LTE HLD = SSOT_COMPLETE
```

## Common

다음 중 하나:

```text
COMMON_HLD_KEEP_COMPLETE
COMMON_HLD_REDUCED_COMPLETE
COMMON_HLD_RETIRED
```

Common HLD가 없어져도 NR/LTE HLD가 완결되어 있으면 전체 HLD는 완료될 수 있다.

## Integrated

존재하는 경우:

```text
INTEGRATED_HLD_REVIEW_COMPLETE
```

Integrated는 SSOT가 아니다.

---

# 24. 파일 원칙

가능하면 기존 파일명을 유지하고 update한다.

새 파일이 필요한 경우 repository naming convention을 우선한다.

예:

```text
CL_AIT_NR_HLD.md
CL_AIT_LTE_HLD.md

CL_AIT_NR_ClassDiagram.puml
CL_AIT_NR_Runtime_MSC.puml

CL_AIT_LTE_ClassDiagram.puml
CL_AIT_LTE_Runtime_MSC.puml
```

Common 유지 시:

```text
CL_AIT_Common_HLD.md
```

Integrated가 있으면:

```text
CL_AIT_Integrated_HLD.md
```

---

# 25. 최종 보고 형식

## A. Final HLD Structure

```text
NR HLD:
LTE HLD:
Common HLD:
Integrated HLD:
```

Common은 `KEEP / REDUCE / RETIRE` 이유를 한 줄로 기록.

## B. Actual Class Architecture

NR/LTE actual class 관계와 다음을 명시:

```text
Shared Base Class:
NR Base:
LTE Base:
```

## C. NR Completion

| Item | Result | Evidence |
|---|---|---|
| HLD | | |
| Class Diagram | | |
| MSC | | |
| Code Alignment | | |
| Traceability | | |

## D. LTE Completion

| Item | Result | Evidence |
|---|---|---|
| HLD | | |
| Class Diagram | | |
| MSC | | |
| SHM | | |
| PCell demod | | |
| LTE Dump | | |
| MTPL/SAR Scope | | |
| Code Alignment | | |
| Traceability | | |

## E. Common HLD Decision

```text
Decision : KEEP / REDUCE / RETIRE
Reason:
Code Evidence:
Impact:
```

## F. Contradiction Audit

```text
Resolved:
Remaining Blocking:
Remaining Non-blocking:
Needs Decision:
```

## G. Modified Files

### NR
- ...

### LTE
- ...

### Common
- ...

### Integrated
- ...

### PlantUML
- ...

### Traceability
- ...

## H. Verification

```text
NR HLD ↔ Code              :
NR Class Diagram ↔ Code    :
NR MSC ↔ Code              :

LTE HLD ↔ Code             :
LTE Class Diagram ↔ Code   :
LTE MSC ↔ Code             :

Common ↔ NR/LTE            :
Integrated ↔ SSOT          :

Build Evidence             :
UT Evidence                :
```

---

# 26. 최종 성공 조건

최종 구조:

```text
                Production Code
                     ↑  ↓
        ┌────────────┴────────────┐
        │                         │
    NR HLD                    LTE HLD
        │                         │
   Class Diagram             Class Diagram
        │                         │
       MSC                       MSC
        │                         │
 Scenario/Traceability     Scenario/Traceability
        └────────────┬────────────┘
                     │
           Common 필요성 재판정
                     │
            Integrated Review
```

최종적으로:

```text
NR HLD  = 독립적으로 완결된 SSOT
LTE HLD = 독립적으로 완결된 SSOT
```

Common HLD는 실제 공통 구현 근거가 있을 때만 architecture 문서로 유지한다.

핵심 원칙:

```text
문서의 abstraction을 코드에 강제하지 않는다.
코드의 As-Built architecture를 문서가 정확하게 설명해야 한다.
```

---

# 27. 최종 실행 지시

현재 repository / artifact에서 기존 CL-AIT 결과를 최대한 재사용하여 위 절차를 처음부터 끝까지 수행하라.

- 기존 정상 결과는 보존한다.
- NR/LTE를 처음부터 재설계하지 않는다.
- Common Base Class를 추론하지 않는다.
- NR/LTE Class Diagram을 반드시 완성한다.
- NR/LTE PlantUML MSC를 반드시 완성한다.
- NR HLD와 LTE HLD를 각각 독립 SSOT로 완결한다.
- Common HLD 필요성을 code fact 기준으로 재판정한다.
- 모든 contradiction을 제거한다.
- 중간 artifact 생성만으로 완료 처리하지 않는다.
- Final Completion Gate까지 수행한다.

새로운 architecture decision이 실제로 필요한 경우에만 `[NEEDS_DECISION]`으로 보고하고 중단한다.

그 외에는 최종 HLD와 PlantUML이 완결될 때까지 계속 진행한다.
