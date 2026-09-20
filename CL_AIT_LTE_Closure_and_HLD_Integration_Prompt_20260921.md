# CL-AIT LTE Open Item Closure → HLD Integration Prompt

## 목적

현재까지 진행된 CL-AIT 결과를 재사용하여 다음 두 작업을 순서대로 수행한다.

1. **LTE Open Item을 Legacy LTE Code Fact 기반으로 닫고, 이미 구현된 SLTE LTE 코드를 필요한 범위에서만 보정**
2. **Common / NR / LTE HLD를 SSOT로 정합화한 뒤, 이를 기반으로 Integrated HLD를 생성**

처음부터 다시 설계하거나 기존 완료 결과를 재작성하지 않는다.

---

## 0. 절대 전제

현재 CL-AIT 작업은 greenfield가 아니다.

- NR 구현 및 HLD는 상당 부분 완료되어 있다.
- LTE도 이전 단계에서 **코드가 일부 구현된 상태**다.
- 기존 LTE 구현을 삭제하거나 처음부터 재작성하지 않는다.
- 기존 Phase 결과, Decision Ledger, Gap Matrix, As-Built 자료, Scenario UT, 실제 코드 diff를 최대한 재사용한다.
- NR 구현 방식을 근거 없이 LTE에 복사하지 않는다.
- Legacy LTE의 실제 runtime behavior와 code contract를 우선 확인한다.
- Code Fact로 해결 가능한 사항을 사용자 Decision으로 다시 올리지 않는다.
- 이미 아래에서 **USER_CONFIRMED**로 확정한 항목은 사용자에게 다시 질문하지 않는다.
- 단, 실제 Legacy 코드가 USER_CONFIRMED 내용과 명백히 충돌하면 임의 수정하지 말고 `CONTRADICTION_FOUND`로 보고한다.

---

# 1. USER_CONFIRMED — LTE 확정 사항

아래 4건은 사용자와 이미 확인 완료한 사항이다.

## LTE-DEC-U01 — Legacy LTE CL-AIT Shared Memory

**확정:**

Legacy LTE CL-AIT도 runtime 정보를 **Shared Memory에 write하는 구조**다.

따라서 현재 SLTE LTE의 `UpdateClAitOperationInfo()`에서 Shared Memory write가 빠져 있다면, 단순히 NR 구조를 복사하지 말고 **Legacy LTE SHM contract를 실제 코드에서 확인한 뒤 동일 의미가 유지되도록 보정**한다.

확인할 Code Fact:

- Legacy LTE SHM structure/type
- writer
- PHY consumer
- Enable field
- Tx Power Threshold field
- Period field
- write timing
- TX ON / TX OFF / Release 시 lifetime
- 기존 RF config API와 SHM write의 연결 관계

상태:

`USER_CONFIRMED + CODE_FACT_VERIFY_REQUIRED`

사용자에게 다시 질문하지 않는다.

---

## LTE-DEC-U02 — LTE demod_cc

**확정:**

LTE는 NR과 달리 demod CC가 동적으로 선택되는 문제가 아니다.

- LTE CL-AIT 대상은 **PCell 고정**
- 따라서 `demod_cc` 선택 자체를 architecture decision으로 취급하지 않는다.
- NR식 동적 demod_cc resolver를 LTE에 새로 설계하지 않는다.

현재 SLTE LTE 코드에 다음과 같은 placeholder가 있다면:

```cpp
u8 demod_cc = domain_type;
```

Legacy LTE에서 PCell demod CC를 표현하는 실제 기존 방법/API/상수를 확인해서 정리한다.

적용 대상 예:

- `SendClAitStartToPhy()`
- `SendClAitFailInd()`
- 기타 LTE CL-AIT PHY IPC path

상태:

`USER_CONFIRMED + IMPLEMENTATION_VERIFY_REQUIRED`

사용자에게 다시 질문하지 않는다.

---

## LTE-DEC-U03 — LTE Dump Payload Type

**확정:**

Legacy LTE는 **LTE 전용 Dump payload type**을 사용했다.

따라서 현재 SLTE LTE 구현에서 `NrAitDump_t`를 재사용하고 있다면 이를 자동 승인하지 않는다.

Legacy LTE에서 실제 전용 payload type과 PHY IPC contract를 확인한 뒤 다음을 비교한다.

- type name
- binary layout
- field semantics
- producer
- consumer
- `ProcClAitDumpInd()`
- `ProcClAitSa()`
- 관련 IPC payload

Legacy LTE 전용 type을 그대로 사용하거나 SLTE target에 대응되는 LTE 전용 type으로 정리할 수 있으면 그 방향을 우선한다.

상태:

`USER_CONFIRMED + CODE_FACT_VERIFY_REQUIRED`

사용자에게 다시 질문하지 않는다.

---

## LTE-DEC-U04 — MTPL / SAR Scope

**확정:**

Legacy LTE에서 MTPL 관련 동작은 **OL-AIT 쪽**에 있었던 것으로 본다.

현재 SLTE 기반 LTE CL-AIT 구현은 MTPL과 dependency가 없으므로:

- CL-AIT SLTE refactoring의 필수 구현 대상으로 보지 않는다.
- NR의 SAR/MTPL 처리 코드를 LTE에 복제하지 않는다.
- LTE CL-AIT HLD에서 해당 항목은 `NOT_APPLICABLE` 또는 이에 준하는 명시적 scope 처리 대상으로 정리한다.
- 실제 Legacy 코드에서 이 전제가 맞는지만 확인한다.

상태:

`USER_CONFIRMED / CL-AIT SCOPE OUT`

사용자에게 다시 질문하지 않는다.

---

# 2. 이번 작업의 1차 목표 — LTE Open Item Closure

현재 SLTE LTE 구현을 baseline으로 고정한 뒤, Legacy LTE를 필요한 범위만 Deep Dive한다.

## 2.1 현재 SLTE LTE baseline 보호

먼저 현재 branch에서 아래를 inventory 한다.

- 이미 구현된 LTE production code
- TODO / placeholder
- Scenario UT
- 현재 LTE HLD
- LTE As-Built HLD
- Gap Matrix
- Decision Ledger
- 관련 PlantUML / traceability artifact

각 항목을 다음 상태로만 분류한다.

- `KEEP`
- `FIX`
- `ADD`
- `REMOVE`
- `N/A`
- `NEEDS_DECISION`

이미 정상 구현된 코드는 다시 작성하지 않는다.

---

## 2.2 Legacy LTE Deep Dive 범위

전체 Legacy LTE를 무작정 분석하지 말고 아래 runtime contract 중심으로 추적한다.

### A. CL-AIT Entry / Trigger
- CL-AIT가 시작되는 entry
- caller
- state/condition
- connected / TX ON dependency

### B. TX ON / TX OFF
- TX ON 이후 operation info 갱신 시점
- TX OFF 시 동작
- Release race
- cleanup

### C. Init / Release
- initialization
- state reset
- timer/resource cleanup

### D. DUMP_IND
- PHY → L1 indication
- payload
- eligibility
- state transition

### E. START_REQ / START_CNF
- L1 → PHY START_REQ
- PHY → L1 START_CNF
- success/fail handling

### F. FSM / State
- Legacy LTE state
- Target SLTE에서 유지해야 할 behavior
- 제거 가능한 legacy complexity

### G. Timer / Periodic
- periodic trigger
- owner
- period source
- skip/retry semantics

### H. RF Config / Shared Memory
특히 LTE-DEC-U01 기준으로 실제 Legacy contract를 확인한다.

### I. PCell / demod_cc
LTE-DEC-U02 기준으로 PCell 고정 path를 확인한다.

### J. Dump Payload
LTE-DEC-U03 기준으로 LTE 전용 type을 확인한다.

### K. OL-AIT / MTPL Boundary
LTE-DEC-U04 기준으로 CL-AIT scope 밖임을 검증한다.

---

# 3. Legacy ↔ Current SLTE LTE Differential Analysis

Legacy Code Fact가 확인되면 즉시 현재 SLTE LTE 구현과 비교한다.

다음 형식으로 matrix를 만든다.

| Item | Legacy LTE Fact | Current SLTE LTE | Gap | Action |
|---|---|---|---|---|
| SHM Enable |  |  |  | KEEP/FIX/ADD |
| SHM Threshold |  |  |  | KEEP/FIX/ADD |
| SHM Period |  |  |  | KEEP/FIX/ADD |
| PCell demod CC |  |  |  | KEEP/FIX |
| Dump type | LTE-specific |  |  | KEEP/FIX |
| MTPL | OL-AIT scope |  |  | N/A |
| TX ON timing |  |  |  |  |
| TX OFF/Release |  |  |  |  |
| START_REQ/CNF |  |  |  |  |
| Timer |  |  |  |  |

---

# 4. LTE Production Code 보정 정책

Legacy와 현재 SLTE의 차이가 확인되면 **필요한 부분만 최소 수정**한다.

원칙:

1. Legacy runtime behavior를 유지한다.
2. 기존 SLTE architecture 원칙을 깨지 않는다.
3. 이미 구현된 정상 LTE 코드는 보존한다.
4. NR code를 그대로 복제하지 않는다.
5. 새로운 Manager/FSM/Timer를 필요 이상으로 만들지 않는다.
6. production code에 test/mock dependency를 넣지 않는다.
7. 현재 class ownership을 임의로 다시 설계하지 않는다.
8. 새 architecture decision이 필요한 경우에만 사용자에게 질문한다.

특히 다음은 우선 확인/보정한다.

### P0
- LTE `UpdateClAitOperationInfo()` SHM write
- LTE PCell 기준 demod CC 처리
- LTE 전용 Dump payload 적용/복원

### P1
- DUMP_IND → START_REQ → START_CNF runtime consistency
- TX OFF / Release race
- periodic behavior
- failure indication path
- init / cleanup

### Scope-out
- LTE CL-AIT의 MTPL/SAR 신규 구현

---

# 5. Scenario UT 및 Traceability 정리

Production code 보정 후 기존 LTE Scenario UT를 우선 재사용한다.

확인:

- 기존 LTE Scenario UT가 현재 runtime contract를 커버하는지
- SHM update 검증
- PCell demod CC
- LTE-specific dump payload
- START_REQ/CNF success
- START_CNF fail
- TX OFF / Release
- periodic skip
- cleanup

부족한 경우에만 UT를 추가한다.

기존 UT를 이유 없이 재작성하지 않는다.

또한 다음을 일치시킨다.

```text
Requirement / Decision
        ↓
Legacy Code Fact
        ↓
Target Production Code
        ↓
Scenario UT
        ↓
HLD / As-Built
```

---

# 6. LTE Closure 완료 조건

LTE는 아래가 모두 충족될 때 `CLOSED_FOR_HLD_INTEGRATION`으로 판정한다.

- USER_CONFIRMED 4건이 코드 사실과 정합
- SHM write contract 확인 및 필요한 보정 완료
- PCell demod CC 처리 확인 완료
- LTE-specific dump payload 확인 및 필요한 보정 완료
- MTPL/SAR가 CL-AIT scope out으로 정리
- 남은 TODO/placeholder 분류 완료
- Scenario UT 정합성 확인
- 새로운 unresolved architecture decision 없음

실제 Build/UT가 아직 수행되지 않았다면 다음과 같이 구분한다.

```text
Design/Code Closure : COMPLETE
Build/UT Evidence    : PENDING
```

Build/UT 미수행을 이유로 다시 설계를 열지 않는다.

단, Final verification 상태에는 명확히 표시한다.

---

# 7. HLD 통합 작업

LTE Closure 이후에 HLD를 통합한다.

중요:

**Integrated HLD를 SSOT로 만들지 않는다.**

정본 구조는 다음과 같다.

```text
00 Common HLD  ─┐
10 NR HLD      ├── SSOT
20 LTE HLD     ┘

       ↓ derived

Integrated CL-AIT HLD
```

---

## 7.1 Step A — Common / NR / LTE SSOT 정합화

먼저 세 HLD를 각각 정리한다.

### 00 Common HLD

NR/LTE 공통 runtime concept만 포함한다.

예:

- CL-AIT 목적
- 공통 terminology
- 공통 lifecycle
- TX ON dependency
- DUMP_IND → START_REQ → START_CNF 기본 sequence
- common ownership principle
- shared error/skip policy
- common architecture rule

RAT-specific 세부 구현은 Common으로 억지로 올리지 않는다.

### 10 NR HLD

NR 전용 내용을 유지한다.

예:

- NR-specific SHM
- NR-specific demod/CC handling
- NR-specific dump payload
- NR-specific SAR/MTPL behavior
- NR-specific timer/state difference
- NR-specific implementation detail

기존에 검증/완료된 NR 내용을 불필요하게 재설계하지 않는다.

### 20 LTE HLD

이번 Legacy Deep Dive + SLTE 보정 결과를 반영한다.

반드시 포함:

- Legacy LTE runtime에서 유지된 behavior
- LTE SHM contract
- PCell fixed demod CC
- LTE-specific dump payload
- MTPL/SAR = CL-AIT scope out
- START_REQ/CNF
- periodic behavior
- TX OFF / Release behavior
- 현재 SLTE class ownership
- As-Built implementation status
- Scenario UT traceability

---

# 8. 중복 제거 규칙

Common / NR / LTE HLD를 정합화할 때 다음 규칙을 사용한다.

```text
NR와 LTE 모두 동일
→ Common HLD로 이동

개념은 같지만 구현이 다름
→ Common에는 concept만
→ NR/LTE에 각각 implementation detail

NR only
→ NR HLD

LTE only
→ LTE HLD
```

Decision 번호만 나열하는 형태로 문서를 채우지 않는다.

사용자가 HLD를 읽을 때 필요한 것은:

- 왜 필요한가
- 누가 owner인가
- 언제 동작하는가
- 어떤 sequence인가
- 실패 시 어떻게 되는가
- RAT별 차이가 무엇인가

이다.

Decision Ledger는 근거 추적용 reference로 사용하고, HLD 본문을 Decision ID 목록으로 만들지 않는다.

---

# 9. Integrated HLD 생성

Common / NR / LTE SSOT 정합화가 끝난 뒤 Integrated HLD를 새로 생성한다.

Integrated HLD는 **derived review artifact**다.

권장 구조:

```text
1. Purpose / Scope
2. Architecture Overview
3. Common CL-AIT Runtime
4. Common Sequence
5. NR Design
6. LTE Design
7. NR vs LTE Difference
8. Error / Skip / Release Handling
9. Shared Memory / IPC Contract
10. Scenario / Traceability
11. Implementation Status
12. Verification Status
13. Remaining Non-blocking Items
```

Integrated HLD 안에서 Common 내용을 NR/LTE section에 반복 복사하지 않는다.

가능하면 다음 구조로 작성한다.

```text
Common behavior
    ├─ NR delta
    └─ LTE delta
```

---

# 10. HLD 상태 정책

HLD 상태를 명확히 구분한다.

### Common / NR / LTE

내용이 코드/Decision과 정합되면:

`SSOT_READY`

Build/UT까지 완료되었다면:

`VERIFIED`

### Integrated HLD

생성 직후:

`DERIVED_REVIEW_READY`

Build/UT 미수행 상태라면 최종 검증을 의미하는 `FINAL_VERIFIED` 같은 표현은 사용하지 않는다.

---

# 11. 사용자 질문 정책

아래 USER_CONFIRMED 4건은 다시 묻지 않는다.

1. Legacy LTE는 SHM write 구조
2. LTE demod CC는 PCell 고정
3. Legacy LTE는 LTE 전용 Dump type
4. MTPL은 OL-AIT scope이며 SLTE LTE CL-AIT dependency 없음

새 질문은 다음 조건에서만 한다.

- 실제 Legacy 코드가 위 확정사항과 명백히 충돌
- 두 개 이상의 architecture 선택지가 실제로 존재
- 기존 Decision Ledger로 결정할 수 없음
- 코드 사실만으로 결론을 낼 수 없음

질문이 필요하면:

```text
[NEEDS_DECISION]

Fact:
Impact:
Option 1:
Option 2:
Option 3:
Recommended implementation impact:
```

형식으로 하나씩 질문하고 STOP한다.

단순 Code Fact 부족은 사용자 질문으로 올리지 말고 코드를 더 조사한다.

---

# 12. 최종 수행 순서

아래 순서를 반드시 지킨다.

```text
1. 기존 결과/현재 branch baseline 확인
2. USER_CONFIRMED 4건을 확정 입력으로 등록
3. Legacy LTE targeted deep dive
4. Legacy ↔ Current SLTE differential matrix 작성
5. 필요한 LTE production code만 보정
6. LTE Scenario UT / traceability 보강
7. LTE Closure 판정
8. Common HLD 정합화
9. NR HLD 기존 결과 재사용 + 최소 정합화
10. LTE HLD를 실제 As-Built 기준으로 갱신
11. Common / NR / LTE 중복 및 contradiction audit
12. 세 HLD를 SSOT_READY로 정리
13. Integrated HLD 생성
14. Integrated HLD cross-check
15. 최종 결과 보고
```

---

# 13. 최종 보고 형식

## A. LTE Closure

| Item | Result | Evidence | Code Change |
|---|---|---|---|
| SHM | | | |
| PCell demod CC | | | |
| Dump type | | | |
| MTPL/SAR | N/A | | |
| START_REQ/CNF | | | |
| TX OFF/Release | | | |
| Periodic | | | |

## B. Remaining LTE Items

- BLOCKING:
- NON_BLOCKING:
- BUILD/UT_PENDING:
- NEEDS_DECISION:

## C. HLD SSOT

- Common HLD:
- NR HLD:
- LTE HLD:

## D. Integrated HLD

- 생성 여부:
- Source HLD:
- Common/NR/LTE 중복 제거:
- RAT-specific delta 반영:
- Review status:

## E. 변경 파일

### Production Code
- ...

### UT
- ...

### HLD / Artifact
- ...

## F. 다음 단계

다음 단계가 Build/UT라면 정확히 그렇게 표시한다.

HLD 내용 정합화가 끝났더라도 실제 Build/UT evidence가 없다면 이를 숨기지 않는다.

---

# 핵심 완료 조건

이번 작업의 성공 조건은 단순히 Integrated HLD 파일 하나를 만드는 것이 아니다.

다음 상태가 되어야 한다.

```text
Legacy LTE Fact
      ↕
SLTE LTE Code
      ↕
LTE Scenario UT
      ↕
LTE HLD
      ↕
Common / NR HLD
      ↓
Integrated HLD
```

각 계층이 서로 모순 없이 연결되어 있어야 한다.

특히 이미 확정한 LTE 4개 항목을 다시 사용자에게 질문하지 말고,
Legacy 코드에서 세부 구현 사실을 검증한 뒤 현재 SLTE LTE 구현을 필요한 만큼만 보정하고,
그 결과를 Common / NR / LTE SSOT에 반영한 다음 Integrated HLD를 생성하라.
