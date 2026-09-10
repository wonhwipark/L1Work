# CL-AIT NR HLD-Based Scenario UT 작성 → Build/UT 검증 프롬프트

## 목적

현재 CL-AIT NR 상태:

```text
NR 기능 코드 구현            : 완료
기존 Functional UT            : 존재
NR HLD                        : 작성 완료
PlantUML MSC                  : 작성 완료
PlantUML Class Diagram        : 작성 완료
Scenario-Based UT             : 미완료
Build / Scenario UT 실행 검증 : 다음 단계
```

이번 작업의 목적은 **이미 작성된 HLD와 PlantUML을 기준으로 Scenario-Based UT를 실제 코드로 작성한 뒤**, 그 다음 Build와 UT 실행 검증을 수행하는 것이다.

**중요: Scenario-Based UT 코드 작성 전에 Build 성공을 선행 조건으로 요구하지 마라.**

현재 Functional UT가 존재한다는 이유로 "먼저 Build부터 수행"하는 방향으로 전환하지 마라.  
Functional UT와 Scenario-Based UT는 목적이 다르다.

---

# 0. 최우선 실행 순서

반드시 아래 순서를 따른다.

```text
[현재 완료]
NR Code
+ Functional UT
+ HLD
+ PlantUML MSC
+ PlantUML Class Diagram
        ↓
[STEP 1]
HLD/MSC에서 Runtime Scenario 추출
        ↓
[STEP 2]
기존 Functional UT와 Scenario Mapping
        ↓
[STEP 3]
Scenario Coverage Gap 식별
        ↓
[STEP 4]
누락 Scenario의 실제 UT 코드 작성
        ↓
[STEP 5]
Scenario UT 코드 정적 검토
        ↓
[STEP 6]
Build
        ↓
[STEP 7]
Scenario UT 실행
        ↓
[STEP 8]
실패 시 bounded repair
        ↓
[STEP 9]
Scenario ↔ HLD ↔ Code ↔ UT Traceability 최종 정리
        ↓
[STEP 10]
HLD Verification/UT Coverage 섹션 최종 반영
```

## 금지 순서

```text
HLD
→ Build 먼저
→ Build PASS 후 Scenario UT 작성
```

이번 작업에서는 위 순서를 사용하지 마라.

Build는 **Scenario-Based UT 코드를 작성한 뒤**, production code와 UT code를 함께 검증하기 위한 단계다.

---

# 1. 현재 HLD의 역할

현재 HLD와 PlantUML은 이미 존재한다.

따라서 이번 작업에서 HLD를 처음부터 다시 작성하지 마라.

HLD는 Scenario-Based UT의 **Requirement / Behavior Source**로 사용한다.

```text
HLD
+ PlantUML MSC
+ PlantUML Class Diagram
        ↓
Scenario Requirement 추출
        ↓
UT Scenario 생성
```

실제 코드와 HLD가 다르면 임의로 추정하지 말고 다음 중 하나로 기록한다.

```text
MATCH
IMPLEMENTATION_DETAIL_REFINED
DEVIATION
UNRESOLVED_CODE_FACT
```

---

# 2. UT 기본 Boundary

CL-AIT NR Unit Test Boundary:

```text
SUT
└─ L1 Production Code = REAL

External Dependency
├─ RF DRV = MOCK
├─ PHY    = MOCK
├─ PAL Timer = 기존 UT framework의 Fake/Trigger 방식
└─ SHM = 기존 L1 UT framework 지원 방식 재사용
```

원칙:

1. L1 production logic은 실제 코드로 검증한다.
2. RF DRV 내부 동작은 Mock 처리한다.
3. PHY 내부 동작은 Mock 처리한다.
4. PAL Timer는 실제 시간을 기다리지 않는다.
5. SHM은 신규 Mock 구조를 임의 생성하지 않는다.
6. 기존 UT framework의 SHM helper / fixture / fake region을 먼저 찾아 재사용한다.
7. 기존 방식이 확인되지 않으면 `UT_SHM_SUPPORT_UNRESOLVED`로 남긴다.
8. 필요 시 사용자에게 기존 SHM UT 예제 파일 1개만 요청한다.

---

# 3. 기존 Functional UT 처리 원칙

기존 Functional UT를 삭제하거나 전부 다시 작성하지 마라.

먼저 기존 UT가 어떤 requirement를 이미 검증하는지 분류한다.

```text
Existing Functional UT
        ↓
Scenario Mapping
        ↓
COVERED
PARTIALLY_COVERED
NOT_COVERED
NOT_APPLICABLE
```

단일 함수/값 검증만 하고 runtime sequence를 검증하지 않는다면 `PARTIALLY_COVERED`로 판정할 수 있다.

Scenario-Based UT 추가 목적은 기존 UT를 대체하는 것이 아니라 **HLD runtime behavior와 sequence coverage를 보강하는 것**이다.

---

# 4. Scenario 추출 기준

HLD 및 PlantUML MSC에서 실제 behavior scenario를 추출한다.

권장 Scenario ID:

```text
SCN-CFG-xxx    : TX ON / Configuration / SHM
SCN-RUN-xxx    : Normal Runtime
SCN-ERR-xxx    : Failure / Retry / Skip / Recovery
SCN-BUILD-xxx  : Build Option / CMake / Generated Source
```

최소 검토 대상:

| Scenario ID | Scenario | Expected L1 Behavior |
|---|---|---|
| SCN-CFG-001 | TX ON 정상 | RF TX ON success 이후 OperationInfo update + SHM write |
| SCN-CFG-002 | SCG 비대상 | eligibility에 따라 CL-AIT enable 제어 |
| SCN-RUN-001 | DUMP_IND 정상 | START_REQ → CNF success → PAL Timer → RF Dump |
| SCN-ERR-001 | TX Path OFF | current period 즉시 skip |
| SCN-ERR-002 | clait_enable=false | START_REQ 없이 skip |
| SCN-ERR-003 | START_CNF 1차 실패 → 2차 성공 | retry exactly once → PAL Timer → RF Dump |
| SCN-ERR-004 | START_CNF 2회 실패 | current period skip |
| SCN-ERR-005 | 다음 Period 독립성 | 이전 retry/failure state carry-over 없음 |
| SCN-ERR-006 | RF Dump 실패 | current period 종료 및 다음 period 독립 |
| SCN-BUILD-001 | Build Option ON | 요청된 generated source/file 포함 |
| SCN-BUILD-002 | Build Option OFF | 신규 source 제외 + 기존 build 영향 없음 |

위 목록은 기준이다.  
**실제 코드/HLD에 없는 behavior를 억지로 UT로 만들지 마라.**

---

# 5. Scenario 정의 형식

각 시나리오는 Given / When / Then으로 정리한다.

예:

```text
Scenario ID : SCN-ERR-003
Title       : START_CNF 1차 실패 후 재시도 성공

Given
- TX Path = ON
- CL-AIT Enable = true
- PHY START_CNF sequence = false → true
- RF Dump result = success

When
- CL_AIT_DUMP_IND 발생

Then
- START_REQ exactly 2
- PAL Timer start exactly 1
- RF AIT_Dump exactly 1
- retry state가 다음 period로 carry-over 되지 않음
```

---

# 6. Scenario-Based UT 코드 작성

Scenario Coverage Gap을 확인한 다음, **누락 시나리오에 대해서 실제 UT 코드를 작성하라.**

"UT 추가 필요"라는 문서만 작성하고 종료하지 마라.

이번 단계의 필수 산출물은 **실제 UT source code modification/addition**이다.

작성 원칙:

- 기존 UT framework 사용
- 기존 Fixture / Mock / Helper 우선 재사용
- 기존 naming convention 준수
- 기존 include 구조 준수
- 테스트 하나에 불필요하게 많은 requirement를 넣지 않음
- Scenario ID와 Test Case를 추적 가능하게 유지
- production code를 UT 편의를 위해 임의 변경하지 않음
- 필요한 경우 production seam이 정말 부족한지 먼저 확인

가능하면:

```text
SCN-ERR-003
→ <actual test suite>.<actual test name>
```

형태로 연결한다.

---

# 7. PHY Mock 정책

PHY는 Mock으로 사용한다.

가능한 입력:

```text
- CL_AIT_DUMP_IND
- CL_AIT_START_CNF true
- CL_AIT_START_CNF false
- false → true
- false → false
```

L1에서 확인할 출력:

```text
- CL_AIT_START_REQ 전송 여부
- START_REQ 호출 횟수
- TX_SWAP_REQ ordering
- 잘못된 상황에서 IPC가 호출되지 않는지
```

PHY 내부 logic은 테스트하지 않는다.

---

# 8. RF DRV Mock 정책

RF DRV는 Mock으로 사용한다.

Mock 가능한 값:

```text
- CL-AIT Enable
- Tx Power Threshold
- Period
- RF TX ON result
- AIT_Dump result
```

L1에서 검증:

```text
RF config
→ L1 eligibility / conversion
→ SHM write
```

및

```text
PAL Timer expiry
→ RF DRV AIT_Dump 호출
```

RF Driver 내부 구현 자체는 UT scope가 아니다.

---

# 9. SHM UT 정책

SHM은 기존 L1 UT framework의 지원 방식을 사용한다.

먼저 repository에서 다음을 탐색한다.

```text
- SHM UT Fixture
- Shared Memory test helper
- fake/test SHM region
- SHM reset/init helper
- 기존 다른 feature의 SHM assertion example
```

찾으면 같은 방식으로 CL-AIT UT에 적용한다.

가능하면 실제 L1 코드가 UT SHM 영역에 값을 쓰도록 하고 결과를 검증한다.

검증 대상:

```text
Enable
Tx Power Threshold
Period
Domain index
```

개념:

```text
RF DRV Mock
        ↓
RfClAitProcNr (REAL)
        ↓
Existing UT SHM Support
        ↓
ASSERT actual SHM fields
```

SHM write API를 통째로 Mock하여 실제 field mapping 검증이 사라지지 않도록 한다.

---

# 10. PAL Timer UT 정책

실제 1초를 기다리는 UT를 작성하지 마라.

기존 UT framework의 timer Fake / Trigger를 재사용한다.

```text
L1
→ Start PAL Timer

UT Harness
→ TriggerTimerExpiry()

L1 Timer Callback
→ RF DRV Mock AIT_Dump
```

확인:

```text
- Timer start 호출 여부
- Timer parameter
- Callback owner
- Timer expiry 후 RF Dump 호출
- skip/retry failure 시 잘못된 Timer start가 없는지
```

---

# 11. 호출 순서 검증

CL-AIT는 단순 결과값뿐 아니라 ordering이 requirement다.

가능하면 Mock sequence / ordered expectation으로 검증한다.

TX ON:

```text
RF TX ON success
→ UpdateClAitOperationInfo
→ SHM update
→ TX_SWAP_REQ
```

Periodic:

```text
DUMP_IND
→ START_REQ
→ START_CNF
→ PAL Timer
→ AIT_Dump
```

Retry:

```text
DUMP_IND
→ START_REQ #1
→ CNF false
→ START_REQ #2
→ CNF true
→ PAL Timer
→ AIT_Dump
```

---

# 12. Build Option / CMake Integration

현재 구현에 Build Option과 CMake 연동이 포함되어 있으므로 Scenario UT 작성 이후 Build 단계에서 함께 검증한다.

확인:

```text
Build Option
    ↓
CMakeLists.txt condition
    ↓
Generated file/source
    ↓
Target linkage
```

검증 기준:

```text
Option ON
→ 요청된 generated source/file이 실제 build target에 포함

Option OFF
→ 신규 source/file 제외
→ 기존 build path 영향 없음
```

**이 검증은 Scenario UT 코드 작성 이후 수행한다.**

Build Integration이 미완료되어 Scenario UT source 자체를 target에 넣을 수 없는 경우에만 해당 CMake 수정을 먼저 보완할 수 있다.

그러나 "Build PASS를 먼저 얻어야 Scenario UT 코드를 작성할 수 있다"는 gate로 사용하지 마라.

---

# 13. 저사양 LLM 실행 정책

전체 repository를 한 번에 분석하지 마라.

아래 순서로 bounded task를 사용한다.

```text
Scenario 1개 선택
        ↓
관련 HLD section / MSC 확인
        ↓
관련 production symbol 확인
        ↓
기존 유사 UT 1~3개 확인
        ↓
필요 Mock/SHM helper 확인
        ↓
UT code 작성
        ↓
다음 Scenario
```

한 번에 모든 Scenario UT를 생성하려고 하지 마라.

각 task packet은 가능하면 다음만 포함한다.

```text
- Scenario ID
- Given/When/Then
- target production function/class
- target UT file
- reusable fixture/helper
- expected Mock calls
- expected SHM values
- expected ordering
```

---

# 14. UT 작성 완료 Gate

Build 전에 아래를 확인한다.

```text
Scenario Matrix 생성 완료
AND
기존 Functional UT Mapping 완료
AND
Scenario Coverage Gap 식별 완료
AND
필요한 Scenario UT 실제 코드 작성 완료
AND
Mock/SHM/Timer dependency 연결 완료
```

모두 만족하면:

```text
SCENARIO_UT_CODE_READY
```

그 다음에만 Build로 이동한다.

---

# 15. Build / UT 실행

`SCENARIO_UT_CODE_READY` 이후 수행한다.

```text
Scenario UT Code Ready
        ↓
Build
        ↓
Scenario UT Run
```

Build 실패 시:

```text
BUILD_REPAIR_REQUIRED
```

로 처리하고 현재 작업 범위 안에서만 bounded repair한다.

UT 실패 시:

```text
UT_REPAIR_REQUIRED
```

로 처리하고 실패 Scenario만 대상으로 수정한다.

---

# 16. HLD 최종 업데이트 시점

HLD의 Architecture/Runtime/PlantUML은 이미 만들어져 있으므로 UT를 위해 다시 처음부터 작성하지 않는다.

Scenario UT 작성 및 실행 후에는 HLD 중 아래 부분만 최종 보강한다.

```text
Verification / UT Coverage
Scenario Traceability
As-Built Deviation
Open Code Facts
```

즉:

```text
Existing HLD / PlantUML
        ↓
Scenario UT 작성
        ↓
Build / UT 검증
        ↓
HLD Verification/Traceability 최종 보강
```

Architecture/MSC/Class Diagram의 실제 코드 불일치가 발견될 때만 해당 section을 수정한다.

---

# 17. Traceability

최종 매핑:

| HLD Section | Scenario ID | Requirement | Actual UT Test | Boundary | Result |
|---|---|---|---|---|---|
| TX ON | SCN-CFG-001 | SHM update | `<actual test>` | RF Mock + SHM UT | PASS |
| Periodic | SCN-ERR-003 | Retry once | `<actual test>` | PHY Mock + RF Mock + Timer Fake | PASS |

Result:

```text
PASS
FAIL
NOT_RUN
NOT_COVERED
UNRESOLVED
```

---

# 18. 산출물

최소 산출물:

```text
1. 실제 Scenario-Based UT 코드
2. CL_AIT_NR_UT_Scenario_Matrix_<date>.md
3. CL_AIT_NR_UT_Coverage_Gap_<date>.md
4. CL_AIT_NR_AsBuilt_Traceability_<date>.md
```

Build/UT 이후:

```text
5. Build result/evidence
6. Scenario UT result/evidence
7. 기존 NR As-Built HLD의 Verification/Traceability 업데이트본
```

---

# 19. 최종 보고 형식

```text
[CL-AIT NR Scenario UT Result]

Scenario extraction : COMPLETE | PARTIAL
Existing UT mapping : COMPLETE | PARTIAL
Scenario UT code    : COMPLETE | PARTIAL
SHM UT support      : VERIFIED | UNRESOLVED
PHY Mock            : VERIFIED | UNRESOLVED
RF DRV Mock         : VERIFIED | UNRESOLVED
PAL Timer Fake      : VERIFIED | UNRESOLVED
Build Integration   : PASS | FAIL | NOT_RUN
Build               : PASS | FAIL | NOT_RUN
Scenario UT         : PASS | FAIL | NOT_RUN

Scenario Summary:
- COVERED:
- PARTIALLY_COVERED:
- NEWLY_IMPLEMENTED:
- NOT_COVERED:

Modified UT Files:
- ...

Production Files Modified:
- ...
  ※ UT 지원을 위해 production 수정이 없으면 NONE

Traceability:
- <path>

Next:
- BUILD
- RUN_UT
- REPAIR
- UPDATE_HLD_VERIFICATION
- COMPLETE
```

---

# 20. 작업 시작 지시

현재 HLD와 PlantUML이 이미 작성되어 있고 Functional UT도 존재한다.

따라서 다음과 같이 시작하라.

```text
1. 기존 HLD/PlantUML에서 Scenario 추출
2. 기존 Functional UT와 Mapping
3. Scenario Coverage Gap 식별
4. 누락 Scenario의 실제 UT 코드 작성
5. SCENARIO_UT_CODE_READY 판정
6. 그 다음 Build
7. Scenario UT 실행
8. 실패 시 bounded repair
9. HLD Verification/Traceability 최종 보강
```

**Scenario-Based UT 코드를 작성하기 전에 Build PASS를 요구하지 마라.**

**이번 작업의 핵심 목표는 HLD 기반 Scenario를 실제 L1 Unit Test 코드로 구현하는 것이다.**
