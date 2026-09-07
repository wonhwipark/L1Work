# CL-AIT SLTE Refactoring 설계 검토 정리
## Decision Ledger 보강 및 HLD Gap Review 준비본

- 문서 상태: Review Consolidation
- 기준일: 2026-09-06
- 목적:
  1. 지금까지 논의한 CL-AIT Target Architecture / Runtime Decision을 통합 정리
  2. 기존 Decision Ledger의 빈 시나리오 및 예외 시나리오를 보강
  3. 남은 Code Fact를 명확히 식별
  4. Ledger가 충분히 닫힌 뒤 기존 사내 HLD와 Gap Review 수행
  5. 이후 HAL `ClAitProcNr/Lte` 중심으로 HLD 갱신
- 기준 문서:
  - `CL_AIT_Basic_Runtime_Concept_Detail_KR_20260906.md`
  - `CL_AIT_DECISION_LEDGER_v1_0_DRAFT_20260906.md`
- 중요:
  - 기존 `L1C ClAitMngr` 전제는 사용하지 않는다.
  - Target Architecture는 HAL `ClAitProcNr/Lte` 중심으로 설계한다.
  - Legacy의 유효한 Runtime Behavior / HW / PHY / RF timing semantics는 보존한다.
  - 단, Legacy ENDC SCG NR 및 `period1/period2` 운용 때문에 복잡해진 FSM 구조는 Target에서 그대로 유지하지 않는다.

---

# 1. 핵심 Target Architecture 원칙

## 1.1 L1C `ClAitMngr` 미사용

Target Architecture에서는 L1C 레벨의 별도 `ClAitMngr`를 두지 않는다.

```text
L1C
┌──────────────────────────────┐
│ TxCfgMngrNr / TxCfgMngrLte  │
│ - TX ON/OFF context         │
│ - NR: isScg                 │
│ - domainType                │
└──────────────┬───────────────┘
               │
               │ Existing TX ON/OFF CMD
               ▼
HAL
┌──────────────────────────────┐
│ ClAitProcNr / ClAitProcLte  │
│ - CL-AIT runtime owner      │
│ - Eligibility              │
│ - RF config query          │
│ - Shared Memory update     │
│ - Dump Ind handling        │
│ - START_REQ/CNF (NR)       │
│ - PAL Timer                │
│ - RF Driver integration    │
└──────────────┬───────────────┘
               ▼
      Shared Memory / PHY
               ▼
        RF Driver / FBRX
```

---

# 2. Legacy Behavior 보존 원칙 재정의

기존 Decision Ledger의 "Legacy Runtime Behavior 보존"은 다음 의미로 정교화한다.

## 보존 대상

- TX ON 기반 CL-AIT activation
- Shared Memory 기반 L1-HAL-PHY config 전달
- PHY periodic / threshold 판단
- PHY → HAL Dump Ind flow
- FBRX availability 확인 flow
- PAL Timer 기반 timing synchronization
- RF Driver `AIT_Dump()` 호출
- 실제 TX / Feedback RX timing coordination
- 해당 period 내 retry / skip semantics

## 그대로 보존하지 않는 대상

Legacy에서는 ENDC 상황에서 SCG NR CL-AIT를 특정 목적으로 사용하면서 다음 구조가 존재했다.

```text
ENDC SCG NR CL-AIT
+
period1 / period2
+
complex FSM
```

Target SLTE에서는:

```text
NR SCG = CL-AIT Not Eligible
period = single logical period
period-local transaction
```

로 단순화한다.

따라서 Legacy의 복잡한 FSM 구조 자체는 보존 대상이 아니다.

---

# 3. TX ON 정상 Sequence

TX ON 정상 sequence는 다음으로 확정한다.

```text
TX_ONOFF_NR_CMD
        ↓
RF TX ON
        ↓
[RF TX ON Success]
        ↓
ClAitProcNr::UpdateClAitOperationInfo(isScg, domainType)
        ↓
Shared Memory Write
 - Enable
 - TxPwrThreshold
 - Period
        ↓
TX_SWAP_REQ
```

핵심 원칙:

> RF TX ON 성공 후에만 `UpdateClAitOperationInfo()`를 수행하며, Shared Memory update 이후 `TX_SWAP_REQ`를 전송한다.

Legacy 동작과 동일한 concept을 유지한다.

---

# 4. `UpdateClAitOperationInfo()` Target API

## NR

```cpp
ClAitProcNr::UpdateClAitOperationInfo(isScg, domainType);
```

NR은 `TX_ONOFF_NR_CMD`를 통해 `isScg`와 `domainType`을 HAL로 전달한다.

`isScg`는 NR CL-AIT eligibility 판단에 사용한다.

```text
isScg = false
→ NR SA
→ CL-AIT Eligible

isScg = true
→ ENDC NR SCG
→ CL-AIT Not Eligible
```

## LTE

```cpp
ClAitProcLte::UpdateClAitOperationInfo(domainType);
```

LTE에는 NR의 `isScg` 조건이 없으므로 `domainType`만 사용한다.

---

# 5. Shared Memory Update

Shared Memory에는 아래 3개 logical information만 설정한다.

```text
1. Enable
2. Tx Power Threshold
3. Period
```

각 정보는 RF Driver API에서 RAT Type을 기준으로 제공한다.

```text
ClAitProc
   ↓
RF Driver API (with RAT Type)
   ↓
Enable / Threshold / Period
   ↓
Shared Memory
```

NR은 RF Driver에서 받은 Enable에 `isScg` eligibility를 추가 적용한다.

예:

```text
RF Driver Enable = true
isScg = false
→ final Enable = true

RF Driver Enable = true
isScg = true
→ final Enable = false
```

별도 `ClAitConfigBuilder`는 두지 않는다.

---

# 6. Periodic 동작

CL-AIT period는 RF Driver에서 제공하는 CL-AIT operation period를 사용한다.

현재 default:

```text
1 sec
```

Legacy에는 `period1`, `period2`가 존재하나 실제 운용에서는:

```text
period1 == period2
```

로 동일한 값을 사용한다.

Target SLTE에서는 이를 단순화하여 하나의 logical period만 사용한다.

```text
Legacy:
period1
period2
  ↓
same value

Target:
period
```

Target에서는 `period1` 하나의 의미만 유지하는 방향으로 정리한다.

---

# 7. CL-AIT Dump Runtime — NR

NR 기준 runtime은 다음 1-cycle transaction으로 정의한다.

```text
TX ON
  ↓
Shared Memory 설정
  ↓
PHY periodic / threshold 확인
  ↓
TX Grant 존재
  ↓
CL_AIT_DUMP_IND
  ↓
TX Path ON 여부 확인
  ↓
clait_enable 확인
  ↓
CL_AIT_START_REQ
  ↓
CL_AIT_START_CNF
  ↓
필요 시 retry 1회
  ↓
PAL Timer
  ↓
PAL Timer Expire
  ↓
RF Driver AIT_Dump()
  ↓
FBRX Dump
  ↓
Current Period 종료
```

---

# 8. `CL_AIT_DUMP_IND` 처리

PHY는 실제 TX Grant가 있는 경우에만 `CL_AIT_DUMP_IND`를 전달한다.

따라서 TX OFF 상태에서는 새로운 CL-AIT Dump cycle이 생성되지 않는다.

## 8.1 TX Path Guard

`ClAitProcNr/ClAitProcLte`는 Dump Ind 수신 시 TX Path가 현재 ON인지 확인해야 한다.

```text
CL_AIT_DUMP_IND
       ↓
Check TX Path
       │
       ├─ OFF
       │    ↓
       │ Current Period Skip
       │
       └─ ON
            ↓
       Continue Runtime
```

목적:

```text
TX Grant
  ↓
Dump Ind 발생
  ↓
TX state 변경
  ↓
stale CL-AIT operation 실행
```

을 HAL 경계에서 방지한다.

---

# 9. Threshold 미충족 처리

PHY가 threshold 조건을 만족하지 못한 경우:

```text
CL_AIT_DUMP_IND
└─ clait_enable = false
```

로 전달한다.

HAL은 이 경우 해당 period를 종료한다.

```text
CL_AIT_DUMP_IND
   ↓
clait_enable == false
   ↓
Current Period Skip
```

이 경우 수행하지 않는 동작:

```text
No CL_AIT_START_REQ
No PAL Timer
No RF AIT_Dump()
```

---

# 10. FBRX Availability Arbitration — NR

Feedback RX HW Resource는 하나이며, NR에서는 PHY와의 START handshake로 사용 가능 여부를 확인한다.

```text
PHY
 │
 │ CL_AIT_DUMP_IND
 ▼
L1 HAL
 │
 │ CL_AIT_START_REQ
 ▼
PHY
 │
 │ CL_AIT_START_CNF
 ▼
L1 HAL
```

## START_CNF = true

```text
CL_AIT_START_CNF = true
        ↓
PAL Timer Set
```

## START_CNF = false

첫 번째 failure 시 1회 retry한다.

```text
CL_AIT_START_REQ
      ↓
CL_AIT_START_CNF = false
      ↓
CL_AIT_START_REQ      ← retry 1회
      ↓
CL_AIT_START_CNF
      │
      ├─ true  → PAL Timer
      └─ false → Current Period Skip
```

별도 global lock/resource manager를 Target에서 신규 도입하지 않는다.

---

# 11. Retry Information — NR Legacy

NR Legacy에서는 retry 관련 정보를 static `claitInfo_t`로 관리하고 있다.

특징:

- L1 HAL / RF Driver가 공용 사용
- `AIT_Dump_Ind(*claitInfo)` 형태로 정보 전달
- retry count는 현재 period 내에서만 의미가 있다

Target에서 반드시 보존할 것은:

- retry semantics
- runtime information semantics
- `AIT_Dump_Ind()`에 필요한 정보

반면 아래 구현 방식은 Target에서 그대로 유지해야 하는 mandatory requirement는 아니다.

- static storage 방식
- HAL / RF Driver가 동일 static object를 직접 공유하는 방식

따라서 `claitInfo_t`의 exact field / ownership은 Code Fact 확인 후 Target class member / context 설계 시 결정한다.

---

# 12. Period-local Transaction 원칙

한 period에서 시작된 CL-AIT Dump operation은 해당 period 내에서 종료된다.

다음 period로 어떠한 retry / failure state도 이월하지 않는다.

```text
Period N
 │
 ├─ DUMP_IND
 ├─ START_REQ/CNF
 ├─ optional retry 1회
 ├─ PAL Timer
 ├─ AIT_Dump()
 └─ END

Period N+1
 │
 └─ New Independent Cycle
```

즉 다음 값은 period 간 carry하지 않는다.

- retry count
- previous START_CNF failure
- previous AIT_Dump failure
- previous dump operation state

---

# 13. RF Driver `AIT_Dump()` Failure

PAL Timer expiry 후 RF Driver `AIT_Dump()`를 호출한다.

```text
PAL Timer Expire
       ↓
RF Driver AIT_Dump()
       ↓
return false
       ↓
Current Period Skip / Terminate
```

`AIT_Dump()`가 false를 반환하면:

- RF Driver가 해당 dump 동작을 수행하지 못한 것으로 판단
- 해당 period를 종료
- 별도 retry 없음
- 다음 period는 새로운 독립 cycle로 시작

---

# 14. TX OFF / Release 처리

TX OFF에서는 별도 CL-AIT Shared Memory disable / cleanup flow를 추가하지 않는다.

근거:

- `CL_AIT_DUMP_IND`는 TX Grant가 존재하는 경우에만 PHY가 전송
- TX OFF 시 새로운 TX Grant가 존재하지 않음
- 따라서 새로운 CL-AIT Dump cycle이 생성되지 않음
- Legacy behavior와 동일 concept 유지

추가로 Dump Ind 수신 시 HAL에서 TX Path ON 여부를 확인하는 guard를 둔다.

---

# 15. PAL Timer

PAL Timer timing 계산 및 동작 방식은 Legacy를 그대로 차용한다.

새로운 timing algorithm을 설계하지 않는다.

따라서 PAL Timer는 Architecture Decision은 이미 닫혀 있으며, 남은 항목은 exact implementation Code Fact이다.

확인 필요:

```text
1. DUMP_IND에서 사용하는 timing field
2. PAL Timer delay 계산식 / 단위
3. PAL Timer create/start API
4. Timer expiry callback
5. Timer expiry → RF Driver AIT_Dump() call flow
6. NR/LTE 구현 차이
```

Target 원칙:

```text
Legacy PAL Timer Timing Semantics
        ↓
Same Timing Semantics Preserve
        ↓
ClAitProcNr/Lte ownership으로 refactoring
```

---

# 16. Complex FSM 단순화

Legacy에서는 ENDC SCG NR CL-AIT와 `period1/period2` 운용 때문에 복잡한 FSM이 존재했다.

Target에서는 해당 Legacy FSM 전체를 그대로 이관하지 않는다.

Target에 필요한 runtime은 아래 정도의 event-driven transaction으로 단순화한다.

```text
DUMP_IND RX
    ↓
TX Path ON?
 ┌───────┴────────┐
 NO               YES
 ↓                 ↓
END          clait_enable?
              ┌────┴────┐
             false      true
              ↓          ↓
             END     START_REQ
                         ↓
                    START_CNF
                    ┌────┴────┐
                   true      false
                    ↓          ↓
                 TIMER      Retry 1회
                               ↓
                          START_CNF
                          ┌────┴────┐
                         true      false
                          ↓          ↓
                       TIMER        END
                          ↓
                    TIMER EXPIRY
                          ↓
                       AIT_Dump
                       ┌────┴────┐
                    success     fail
                       ↓          ↓
                      END        END
```

중요:

> END는 persistent FSM state가 아니라 해당 period transaction의 종료를 의미한다.

---

# 17. LTE Target 설계 원칙

NR과 LTE는 CL-AIT의 전체 개념은 유사하지만 interface/runtime detail을 억지로 공통화하지 않는다.

특히 NR에는 다음 IPC flow가 존재한다.

```text
CL_AIT_DUMP_IND
CL_AIT_START_REQ
CL_AIT_START_CNF
```

LTE Legacy code에서는 동일 IPC가 존재하는지 아직 확인 필요하다.

따라서 Target 원칙:

```text
LTE Legacy에 START_REQ/CNF 존재
→ ClAitProcLte에서도 동일 의미 유지

LTE Legacy에 START_REQ/CNF 없음
→ ClAitProcLte에 신규로 추가하지 않음
```

NR behavior를 LTE에 강제로 복사하지 않는다.

---

# 18. Updated Decision 후보

## DEC-001 — Legacy Runtime Behavior Preservation
**Status: CONFIRMED / Wording Update Required**

Legacy의 유효한 runtime semantics 및 timing constraints는 보존한다.

단, Target에서 의미가 사라진 다음 Legacy 구조는 그대로 보존하지 않는다.

- ENDC SCG NR CL-AIT support
- period1 / period2 dual representation
- 이에 종속된 complex FSM state / transition

---

## DEC-010 — TX ON Ordering
**Status: CONFIRMED**

```text
RF TX ON Success
→ UpdateClAitOperationInfo(...)
→ Shared Memory Write
→ TX_SWAP_REQ
```

---

## DEC-011 — Update API
**Status: UPDATE REQUIRED**

NR:

```cpp
ClAitProcNr::UpdateClAitOperationInfo(isScg, domainType);
```

LTE:

```cpp
ClAitProcLte::UpdateClAitOperationInfo(domainType);
```

---

## DEC-015 — TX OFF Cleanup
**Status: CONFIRMED / Rationale Update**

TX OFF 시 별도 CL-AIT disable / cleanup을 추가하지 않는다.

`CL_AIT_DUMP_IND`는 TX Grant가 있는 경우에만 발생하므로 TX OFF 상태에서는 새로운 CL-AIT Dump cycle이 생성되지 않는다.

---

## DEC-022 — FBRX Availability Arbitration
**Status: CONFIRMED (NR)**

NR은 `CL_AIT_START_REQ/CNF` handshake로 FBRX 사용 가능 여부를 확인한다.

`START_CNF=true`인 경우에만 PAL Timer를 설정한다.

---

## DEC-023 — START_CNF Retry
**Status: CONFIRMED (NR)**

첫 `CL_AIT_START_CNF=false` 시 `START_REQ/CNF`를 1회 retry한다.

두 번째도 false이면 해당 period를 종료한다.

---

## DEC-024 — Period-local Transaction
**Status: CONFIRMED**

각 CL-AIT Dump operation은 해당 period 내에서만 유효하며 다음 period로 state/retry를 carry하지 않는다.

---

## DEC-025 — DUMP_IND Disable Handling
**Status: CONFIRMED**

`CL_AIT_DUMP_IND.clait_enable == false`인 경우 해당 period를 종료한다.

---

## DEC-026 — RF AIT_Dump Failure
**Status: CONFIRMED**

`AIT_Dump()` return=false이면 해당 period를 종료하고 별도 retry하지 않는다.

---

## DEC-027 — Single Period
**Status: CONFIRMED**

Legacy의 `period1`, `period2`는 동일 값으로 운용되고 있으므로 Target SLTE에서는 하나의 logical period만 사용한다.

---

## DEC-028 — TX Path Validity Guard
**Status: CONFIRMED**

Dump Ind 수신 시 `ClAitProcNr/ClAitProcLte`에서 TX Path ON 여부를 확인한다.

TX Path OFF이면 해당 period를 종료한다.

---

## DEC-029 — Legacy Complex FSM Simplification
**Status: CONFIRMED**

Legacy ENDC / period1 / period2 운용을 위해 존재한 complex FSM을 Target에 그대로 이관하지 않는다.

Target은 필요한 최소 event-driven runtime transaction으로 단순화한다.

---

# 19. 현재 CLOSED 된 Scenario

| Scenario | Status | 비고 |
|---|---|---|
| TX ON exact ordering concept | CLOSED | RF TX ON success 후 Update → SHM → TX_SWAP_REQ |
| NR eligibility input | CLOSED | `isScg`, `domainType` |
| NR Update API | CLOSED | `UpdateClAitOperationInfo(isScg, domainType)` |
| LTE Update API | CLOSED | `UpdateClAitOperationInfo(domainType)` |
| SHM logical fields | CLOSED | Enable / Threshold / Period |
| Period1/Period2 target policy | CLOSED | single period |
| TX OFF new dump pending 여부 | CLOSED | TX grant 없으면 Dump Ind 없음 |
| Dump Ind stale defense | CLOSED | TX Path ON guard |
| Threshold fail | CLOSED | `clait_enable=false` → period skip |
| NR FBRX arbitration concept | CLOSED | START_REQ/CNF |
| NR START retry | CLOSED | 1회 |
| period 간 retry/state carry | CLOSED | 없음 |
| AIT_Dump false | CLOSED | current period terminate |
| Legacy complex FSM target policy | CLOSED | simplified transaction |

---

# 20. 남은 Code Fact

현재 남은 항목은 대부분 Architecture Decision이 아니라 HLD exact interface / implementation detail 확인용이다.

## CF-01 — Shared Memory Exact Structure
확인 필요:

- Shared Memory struct name
- Enable field
- Threshold field
- Period field
- domain indexing 방식
- NR/LTE 구조체 차이

---

## CF-02 — NR `CL_AIT_DUMP_IND`
확인 필요:

- exact IPC name
- payload struct
- `clait_enable` field
- timing field
- slot / TTI 관련 field
- power 관련 field

---

## CF-03 — NR `CL_AIT_START_REQ/CNF`
확인 필요:

- exact IPC name
- request payload
- confirm payload
- handler
- retry trigger
- retry counter field
- `claitInfo_t`와의 관계

Architecture behavior 자체는 이미 확정되어 있다.

---

## CF-04 — `claitInfo_t`
확인 필요:

- exact struct definition
- fields
- retry count field
- lifetime
- static 선언 위치
- L1 HAL / RF Driver 사용 위치
- `AIT_Dump_Ind(*claitInfo)` call flow

Target에서 static 구현을 그대로 유지할지는 HLD class design 시 결정한다.

---

## CF-05 — PAL Timer
확인 필요:

- DUMP_IND timing field
- delay 계산식
- 단위
- create/start API
- timer handle
- expiry callback
- expiry → `AIT_Dump()` call path

Timing semantics는 Legacy를 그대로 보존한다.

---

## CF-06 — RF Driver Interface
확인 필요:

- Enable query API
- Threshold query API
- Period query API
- `AIT_Dump()` exact API
- `AIT_Dump_Ind()` exact interface
- RAT Type 전달 방식

---

## CF-07 — TX Path ON Guard Source
확인 필요:

- NR TX path state source/API
- LTE TX path state source/API
- Dump Ind handler에서 어느 시점에 확인 가능한지

---

## CF-08 — LTE Legacy Runtime
**P0**

확인 필요:

```text
LTE TX ON flow
LTE Shared Memory
LTE Dump Ind
LTE START_REQ/CNF 존재 여부
LTE retry 존재 여부
LTE PAL Timer
LTE RF Driver AIT_Dump
LTE TX Path guard
LTE period handling
```

특히:

> LTE Legacy에 START_REQ/CNF가 없다면 Target LTE에도 해당 flow를 추가하지 않는다.

---

# 21. 더 이상 HLD Blocker로 보지 않는 항목

다음 항목은 별도 Architecture OPEN으로 유지할 필요가 없다.

## PAL Timer algorithm 신규 설계

불필요.

```text
Legacy 방식 그대로 차용
```

따라서 exact Code Fact만 확인한다.

## Legacy NR Complex FSM 전체 복원

불필요.

Target에서 필요한 최소 behavior만 확인한다.

```text
DUMP_IND
→ START_REQ/CNF
→ retry 1회
→ PAL Timer
→ AIT_Dump
→ current-period terminate
```

## 신규 FBRX global manager / lock 설계

현재 NR은 PHY `START_REQ/CNF` handshake로 resource availability를 확인하므로 신규 manager를 설계하지 않는다.

---

# 22. 최종 NR Target Runtime Sequence

```text
TxCfgMngrNr
 │
 │ TX_ONOFF_NR_CMD
 │ - isScg
 │ - domainType
 ▼
HAL TX ON Handler
 │
 │ RF TX ON
 ▼
[RF TX ON SUCCESS]
 │
 ▼
ClAitProcNr
 │
 │ UpdateClAitOperationInfo(isScg, domainType)
 │
 ├─ RF API(NR) → Enable
 ├─ RF API(NR) → Threshold
 ├─ RF API(NR) → Period
 ├─ Apply isScg eligibility
 │
 ▼
Shared Memory
 │
 │ Enable / Threshold / Period
 ▼
TX_SWAP_REQ
 │
 ▼
PHY TX Scheduling


=================================
         Periodic Runtime
=================================

PHY
 │
 │ TX Grant + Period Condition
 ▼
CL_AIT_DUMP_IND
 │
 ▼
ClAitProcNr
 │
 ├─ Check TX Path ON
 │      ├─ OFF → Current Period END
 │      └─ ON
 │
 ├─ Check clait_enable
 │      ├─ false → Current Period END
 │      └─ true
 │
 ▼
CL_AIT_START_REQ
 │
 ▼
PHY
 │
 │ CL_AIT_START_CNF
 ▼
ClAitProcNr
 │
 ├─ true
 │    ↓
 │ PAL Timer Set
 │
 └─ false
      ↓
   START_REQ Retry #1
      ↓
   START_CNF
      ├─ false → Current Period END
      └─ true
             ↓
         PAL Timer Set
             ↓
         PAL Timer Expire
             ↓
       RF Driver AIT_Dump()
             │
             ├─ false → Current Period END
             └─ success
                    ↓
                 FBRX Dump
                    ↓
             Current Period END

=================================
 Next Period = New Independent Cycle
=================================
```

---

# 23. LTE HLD 작성 전 확인 원칙

LTE는 NR flow를 복사하지 않는다.

순서:

```text
NR Target Runtime 정리
        ↓
LTE Legacy Code Fact 분석
        ↓
NR/LTE Delta 추출
        ↓
ClAitProcLte Target Runtime 확정
```

비교 Matrix:

| Item | NR | LTE |
|---|---|---|
| TX ON command | known | confirm exact |
| Update API | `(isScg, domainType)` | `(domainType)` |
| Shared Memory | Code Fact | Code Fact |
| Dump Ind | Yes | Code Fact |
| START_REQ | Yes | Code Fact |
| START_CNF | Yes | Code Fact |
| Retry | 1 | Code Fact |
| PAL Timer | Yes | Code Fact |
| AIT_Dump | Yes | Code Fact |
| TX Path Guard | Target Yes | Target Yes |
| Period | Single | confirm Legacy |

---

# 24. HLD Gap Review 진입 조건

Decision Ledger를 아래 조건까지 닫은 후 기존 사내 HLD와 Gap Review를 수행한다.

## Required

- NR Target Runtime Decision close
- LTE Legacy Runtime Code Fact 확보
- NR/LTE exact interface Code Fact 확보
- PAL Timer exact timing detail 확보
- Shared Memory exact fields 확보
- RF Driver exact APIs 확보

## Ledger 상태 목표

```text
Architecture Decision:
CLOSED

Remaining OPEN:
Exact interface / code naming only
```

---

# 25. 이후 HLD Gap Review 방향

기존 사내 HLD는 `L1C ClAitMngr` 전제를 사용했으므로 아래 순서로 수정한다.

```text
Existing Internal HLD
        ↓
Decision Ledger 기준 Gap Review
        ↓
L1C ClAitMngr structure 제거
        ↓
L1C ClAitConfigBuilder 제거
        ↓
Existing TX_ONOFF CMD 유지
        ↓
HAL ClAitProcNr/Lte ownership 반영
        ↓
NR START_REQ/CNF runtime 반영
        ↓
Period-local transaction 반영
        ↓
Legacy complex FSM 제거/단순화
        ↓
NR/LTE Delta 반영
        ↓
MSC / Class / Interface 갱신
        ↓
HLD Revision
```

---

# 26. HLD에서 반드시 표현해야 할 핵심

## Architecture

```text
TxCfgMngr
→ Existing TX ON/OFF CMD
→ HAL ClAitProc
→ PHY / Shared Memory / RF Driver
```

## NR TX ON

```text
RF TX ON Success
→ UpdateClAitOperationInfo(isScg, domainType)
→ SHM
→ TX_SWAP_REQ
```

## Runtime

```text
DUMP_IND
→ TX Path Guard
→ clait_enable
→ START_REQ/CNF
→ retry 1회
→ PAL Timer
→ AIT_Dump
→ END
```

## Period

```text
Each period = Independent transaction
```

## Failure policy

```text
Threshold fail
→ Current Period Skip

TX Path OFF
→ Current Period Skip

START_CNF false x2
→ Current Period Skip

AIT_Dump false
→ Current Period Skip
```

## LTE

```text
Legacy fact 기반으로만 반영
NR flow 강제 공통화 금지
```

---

# 27. 최종 설계 결론

> SLTE CL-AIT는 기존 L1C `ClAitMngr`를 사용하지 않고, HAL `ClAitProcNr/Lte`가 CL-AIT runtime owner가 된다.

> Legacy의 유효한 TX / PHY / FBRX / PAL Timer / RF Driver timing behavior는 보존하지만, Legacy ENDC SCG NR 동작과 `period1/period2` 때문에 존재했던 복잡한 FSM 구조는 Target에서 유지하지 않는다.

> NR은 TX ON 성공 후 `UpdateClAitOperationInfo(isScg, domainType)`를 통해 Enable / Threshold / Period를 Shared Memory에 설정하고, 이후 `TX_SWAP_REQ`를 통해 PHY TX scheduling을 진행한다.

> NR periodic runtime은 `CL_AIT_DUMP_IND → TX Path Guard → clait_enable → CL_AIT_START_REQ/CNF → retry 1회 → PAL Timer → AIT_Dump()`의 period-local transaction으로 단순화한다.

> 한 period에서 발생한 retry / failure / runtime state는 다음 period로 이월하지 않는다.

> PAL Timer timing은 Legacy 방식을 그대로 차용하며, exact calculation/API는 Code Fact로만 확인한다.

> LTE는 Legacy code 분석 결과에 따라 설계하며, NR의 `START_REQ/CNF` flow가 LTE Legacy에 존재하지 않는다면 Target LTE에 신규 추가하지 않는다.

---

# 28. 다음 진행 순서

```text
[현재]
Decision Ledger 보강 검토 완료
        ↓
1. 남은 Code Fact 확인
   - Shared Memory exact fields
   - NR Dump Ind
   - NR START_REQ/CNF
   - claitInfo_t
   - PAL Timer
   - RF Driver API
   - TX Path state
   - LTE Legacy Runtime
        ↓
2. Decision Ledger v1.1 통합
        ↓
3. Architecture OPEN close 확인
        ↓
4. Decision Ledger Freeze
        ↓
5. 기존 사내 HLD Gap Review
        ↓
6. HAL ClAitProcNr/Lte 중심 HLD Revision
        ↓
7. HLD Gate
        ↓
8. 구현 단계
```
