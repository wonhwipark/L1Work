# CL-AIT LTE Legacy 분석 재점검 프롬프트

## 목적

현재 CL-AIT NR은 구현/HLD/PlantUML/UT 흐름을 기준으로 정리된 상태다.

LTE는 이전에 Legacy 분석을 한 번 수행한 적이 있으나, 이번 단계에서는 그 기존 분석 결과를 그대로 신뢰하지 않고 **실제 LTE Legacy 코드 기준으로 다시 검증**한다.

이번 단계의 목적은 오직 다음이다.

```text
기존 LTE Legacy 분석 결과
        ↓
Actual LTE Legacy Code 재검증
        ↓
Fact-by-Fact 판정
        ↓
LTE_Legacy_Confirmed_Facts.md
        ↓
STOP
```

이번 단계에서는 LTE Target 설계, HLD 작성, 구현, UT 작성까지 진행하지 마라.

---

# 1. 최우선 원칙

1. **Legacy Fact와 Target Design을 섞지 마라.**
2. 기존 LTE 분석 결과는 참고자료일 뿐, 최종 근거는 실제 코드다.
3. 실제 코드에서 확인되지 않은 내용은 추정하지 마라.
4. NR 구조를 LTE에 복사하지 마라.
5. NR에 존재하는 START_REQ/CNF, retry, PAL Timer flow가 LTE에도 있다고 가정하지 마라.
6. LTE Legacy에 실제로 존재하는 동작만 Fact로 기록하라.
7. 이번 단계에서는 코드 수정 금지.
8. HLD 수정 금지.
9. Target class 이름 결정 금지.
10. LTE 구현 시작 금지.
11. 전체 Repository를 한 번에 분석하지 말고 bounded analysis로 진행하라.
12. 확인되지 않은 내용은 `UNRESOLVED_CODE_FACT`로 남겨라.

---

# 2. 입력 우선순위

가능하면 아래 순서로 자료를 찾는다.

```text
1. 기존 LTE Legacy 분석 MD / report
2. 기존 LTE CL-AIT 관련 코드
3. 관련 IPC / SHM / RF Driver / Timer 코드
4. 기존 LTE UT / Mock / SHM support
5. 필요 시 관련 공통 HAL 코드
```

기존 분석 문서를 찾지 못하면:

```text
PREVIOUS_LTE_ANALYSIS_NOT_FOUND
```

로 기록한 뒤 Actual Code 기준 Legacy Fact 분석을 진행한다.

---

# 3. 기존 분석 결과 재검증 방식

기존 분석 결과의 각 항목을 아래 상태 중 하나로 판정한다.

```text
CONFIRMED
PARTIALLY_CONFIRMED
INCORRECT
NOT_ANALYZED
UNRESOLVED_CODE_FACT
```

각 판정에는 반드시 코드 근거를 붙인다.

예:

```text
Item:
START_REQ/CNF 존재 여부

Previous Analysis:
존재함

Actual Code:
<file>
<class/function>
<relevant symbol>

Result:
CONFIRMED | INCORRECT | ...

Evidence:
- ...
```

---

# 4. 반드시 재점검할 LTE Legacy Fact

## 4.1 Runtime Owner / Class

확인:

```text
- LTE CL-AIT runtime owner class
- 실제 file
- singleton 여부
- facade/runtime owner 구조
- helper/context 구조
```

출력:

```text
Runtime Owner:
Class:
File:
Ownership:
Confidence:
Evidence:
```

## 4.2 TX ON 이후 CL-AIT 설정 처리

확인:

```text
- LTE TX ON command
- RF TX ON 성공 이후 어떤 함수가 호출되는지
- CL-AIT config update 위치
- caller / callee
- domainType 전달 여부
- TX scheduling enable과의 ordering
```

가능하면 실제 순서를 정리한다.

```text
TX_ONOFF_LTE_CMD
→ ...
→ ...
→ CL-AIT operation/config update
→ ...
```

순서를 확인할 수 없으면 추정하지 않는다.

## 4.3 Shared Memory

반드시 확인:

```text
Enable
Tx Power Threshold
Period
Domain Index
```

확인 항목:

```text
- 실제 struct 이름
- 실제 field 이름
- write 위치
- owner
- domain indexing
- initialization/reset
- RF Driver에서 값 가져오는 위치
```

Logical name과 실제 field name을 구분해서 기록한다.

## 4.4 DUMP_IND

확인:

```text
- 실제 LTE CL-AIT DUMP indication 존재 여부
- 정확한 IPC 이름
- handler
- payload
- timing 정보
- clait_enable 또는 유사 enable field
- grant 관련 조건
```

없으면:

```text
NOT_PRESENT_IN_LTE_LEGACY
```

로 명시한다.

## 4.5 START_REQ / START_CNF 존재 여부

다음 세 가지를 각각 실제 코드로 확인한다.

```text
CL_AIT_START_REQ
CL_AIT_START_CNF
FBRX availability handshake
```

결론:

```text
PRESENT
NOT_PRESENT
PARTIALLY_PRESENT
UNRESOLVED_CODE_FACT
```

**NR에 존재한다는 이유로 LTE에도 있다고 가정하지 마라.**

## 4.6 Retry 동작

확인:

```text
- START_CNF false 시 retry 존재 여부
- retry count
- retry trigger
- retry state 저장 위치
- period 간 carry-over 여부
```

결론:

```text
NO_RETRY
RETRY_PRESENT
RETRY_PRESENT_BUT_DIFFERENT_FROM_NR
UNRESOLVED_CODE_FACT
```

## 4.7 PAL Timer

확인:

```text
- PAL Timer 사용 여부
- timer API
- timer handle/context
- callback
- timer owner
- timer start condition
- expire 이후 RF Driver 호출
```

NR과 동일하다고 가정하지 않는다.

## 4.8 RF Driver API

확인:

```text
- Enable get API
- Threshold get API
- Period get API
- Dump API
- Dump indication helper
- LTE-specific RF API
```

각 API는 실제 symbol/file과 함께 기록한다.

## 4.9 TX Path Guard

확인:

```text
- TX Path ON/OFF guard 존재 여부
- guard source
- API/field
- DUMP_IND 수신 시 guard 여부
- TX OFF 시 동작
```

없으면 없다고 명확히 기록한다.

## 4.10 Period 처리

확인:

```text
- period1 / period2 존재 여부
- 실제 운영 값
- 동일/상이 여부
- single period처럼 사용되는지
- period reset 방식
```

NR 구조를 기준으로 단순화하지 마라.

## 4.11 ENDC / LTE MCG / Eligibility

확인:

```text
- LTE MCG에서 CL-AIT 사용 조건
- ENDC 관련 조건
- LTE 단독 동작 조건
- NR SCG와의 FBRX resource 영향
- enable eligibility
```

Legacy code fact와 architecture inference를 구분한다.

## 4.12 Legacy FSM / State Machine

확인:

```text
- 명시적 FSM 존재 여부
- state enum
- transition
- retry state
- dump state
- period state
```

복잡한 FSM이 있더라도 이번 단계에서는 단순화하지 말고 사실 그대로 기록한다.

## 4.13 LTE 기존 UT

확인:

```text
- 기존 LTE CL-AIT UT 존재 여부
- Functional UT
- Scenario UT
- Fixture
- PHY Mock
- RF Driver Mock
- SHM support
- PAL Timer Fake/Trigger
```

UT가 없는 경우:

```text
LTE_LEGACY_UT_NOT_FOUND
```

로 기록한다.

---

# 5. NR과의 비교는 아직 최소화

이번 단계의 핵심은 LTE Legacy Fact 확정이다.

따라서 NR As-Built와의 본격 비교 Matrix는 아직 만들지 마라.

단, LTE fact를 이해하기 위해 필요한 최소 주석은 허용한다.

예:

```text
Note:
NR에는 START_REQ/CNF가 존재하지만
LTE Legacy에서는 현재 코드 기준 NOT_PRESENT.
```

하지만 아직 다음 결론까지 가지 마라.

```text
→ LTE Target에도 추가하지 않는다
→ LTE Target 구조는 이렇게 한다
```

이것은 다음 단계에서 결정한다.

---

# 6. 저사양 LLM 실행 방식

전체 Repository를 한 번에 분석하지 마라.

아래 단위로 나눠 진행한다.

```text
Task 1:
Runtime Owner + TX ON

Task 2:
SHM + RF Driver config

Task 3:
DUMP_IND + START_REQ/CNF

Task 4:
Retry + PAL Timer

Task 5:
TX Path Guard + Period

Task 6:
ENDC / Eligibility

Task 7:
Legacy FSM

Task 8:
Existing LTE UT
```

각 Task는:

```text
1. 관련 symbol 후보 탐색
2. 관련 file 1~5개 확인
3. fact 추출
4. evidence 기록
5. unresolved 기록
6. 다음 Task
```

순서로 처리한다.

이미 확인한 범위를 반복해서 재분석하지 마라.

---

# 7. Evidence 작성 규칙

각 Fact에는 가능한 한 다음을 기록한다.

```text
File:
Class:
Function:
Symbol:
Behavior:
Evidence:
Confidence:
```

Confidence:

```text
HIGH
MEDIUM
LOW
```

근거가 약한 경우 HIGH를 사용하지 마라.

---

# 8. Fact 충돌 처리

기존 분석과 실제 코드가 충돌하면 기존 분석을 우선하지 마라.

형식:

```text
[Legacy Analysis Conflict]

Item:
Previous:
Actual Code:
Decision:
INCORRECT | PARTIALLY_CONFIRMED

Evidence:
- ...

Impact:
- 다음 NR/LTE Gap 단계에서 재검토 필요
```

---

# 9. 이번 단계의 최종 산출물

반드시 다음 파일을 생성한다.

```text
CL_AIT_LTE_Legacy_Confirmed_Facts_<date>.md
```

가능하면 추가로:

```text
CL_AIT_LTE_Legacy_Validation_Matrix_<date>.md
CL_AIT_LTE_Legacy_OpenFacts_<date>.md
```

---

# 10. Confirmed Facts 문서 구조

최종 문서는 다음 구조를 권장한다.

```text
1. Purpose
2. Analysis Scope
3. Previous Analysis Source
4. Runtime Owner
5. TX ON Flow
6. Shared Memory
7. DUMP_IND
8. START_REQ/CNF
9. Retry
10. PAL Timer
11. RF Driver APIs
12. TX Path Guard
13. Period Handling
14. ENDC / Eligibility
15. Legacy FSM
16. Existing LTE UT
17. Previous Analysis Validation Result
18. Confirmed Facts Summary
19. Unresolved Code Facts
20. Evidence Index
```

---

# 11. 최종 Summary 형식

문서 마지막에 다음 표를 넣는다.

| Item | Result | Confidence | Evidence |
|---|---|---|---|
| Runtime Owner | CONFIRMED | HIGH | file/function |
| START_REQ/CNF | PRESENT/NOT_PRESENT/... | HIGH | file/function |
| Retry | ... | ... | ... |
| PAL Timer | ... | ... | ... |
| SHM | ... | ... | ... |
| TX Path Guard | ... | ... | ... |

---

# 12. STOP 조건

아래 조건을 만족하면 이번 단계는 종료한다.

```text
기존 LTE Legacy 분석 검토 완료
AND
Actual Code 기준 주요 Fact 재확인 완료
AND
Fact별 Validation 상태 기록 완료
AND
Unresolved Code Fact 분리 완료
AND
Confirmed Fact Report 생성 완료
```

완료 상태:

```text
LTE_LEGACY_FACTS_CONFIRMED
```

그 다음 단계는 아직 자동으로 실행하지 마라.

다음 단계는 별도로:

```text
NR As-Built
vs
LTE Legacy Confirmed Facts
→ NR/LTE Gap Matrix
```

이다.

---

# 13. 최종 사용자 보고 형식

```text
[CL-AIT LTE Legacy Revalidation Result]

Previous Analysis:
- FOUND | NOT_FOUND

Runtime Owner:
- CONFIRMED | PARTIAL | UNRESOLVED

TX ON:
- CONFIRMED | PARTIAL | UNRESOLVED

SHM:
- CONFIRMED | PARTIAL | UNRESOLVED

DUMP_IND:
- PRESENT | NOT_PRESENT | PARTIAL | UNRESOLVED

START_REQ/CNF:
- PRESENT | NOT_PRESENT | PARTIAL | UNRESOLVED

Retry:
- PRESENT | NOT_PRESENT | DIFFERENT_FROM_NR | UNRESOLVED

PAL Timer:
- CONFIRMED | PARTIAL | NOT_PRESENT | UNRESOLVED

RF Driver:
- CONFIRMED | PARTIAL | UNRESOLVED

TX Path Guard:
- PRESENT | NOT_PRESENT | UNRESOLVED

LTE Legacy UT:
- FOUND | PARTIAL | NOT_FOUND

Open Facts:
- ...

Output:
- CL_AIT_LTE_Legacy_Confirmed_Facts_<date>.md
- CL_AIT_LTE_Legacy_Validation_Matrix_<date>.md
- CL_AIT_LTE_Legacy_OpenFacts_<date>.md

Status:
- LTE_LEGACY_FACTS_CONFIRMED
또는
- BLOCKED
```

---

# 14. 작업 시작

기존 LTE Legacy 분석 결과를 먼저 찾는다.

찾은 경우:
- 기존 결과를 Fact-by-Fact로 실제 코드와 대조한다.

찾지 못한 경우:
- `PREVIOUS_LTE_ANALYSIS_NOT_FOUND`로 기록한다.
- Actual LTE Legacy Code 기준으로 Fact 분석을 수행한다.

이번 단계에서는 **Target Design, HLD 작성, 구현, Scenario UT를 시작하지 마라.**

**목표는 오직 “LTE Legacy 실제 코드 Fact를 다시 검증하고 Confirmed Fact를 고정하는 것”이다.**
