# SLTE CL-AIT Target Requirement(SRS) 작성 워크플로우
**목적:** Legacy 분석 및 SLTE Scope 분석 결과를 입력으로, 새로운 SLTE 기반 CL-AIT Manager의 Target Requirement를 정의한다.  
**연계 문서:** `CL_AIT_Legacy_to_SLTE_Phase01_02_Workflow_v3_20260827.md`  
**작성일:** 2026-08-28  
**대상 환경:** 사내 LLM / OpenCode / 저사양 LLM 환경  
**중요:** 이 문서는 Phase 1~2를 다시 수행하기 위한 문서가 아니다. **Phase 1~2 결과를 확인한 뒤 다음 단계인 Target Requirement를 만드는 문서**이다.

---

# 1. 배경

최종 목표는 **Legacy CL-AIT 코드를 포팅하는 것**이 아니라,

> **SLTE Base에 적합한 새로운 CL-AIT Manager를 설계하고 구현하는 것**

이다.

현재까지의 준비 흐름은 다음과 같다.

```text
Phase 1
Legacy CL-AIT 이해
- 기존 code-analyzer 결과
- 기존 일부 MSC
- 필요 시 Legacy source 확인
        ↓
Legacy Behavior Baseline

Phase 2
현재 SLTE 코드 Scope 확인
- 기존 SLTE analyzer 결과 재사용
- FEATURE_SCOPE_PROBE
- 관련 module/file/API/state 후보 확인
        ↓
SLTE Candidate Scope
```

그러나 여기서 바로 Legacy와 SLTE의 Gap을 계산하거나 HLD를 작성하면 안 된다.

그 이유는 아직 다음 질문에 대한 답이 없기 때문이다.

> **"새로운 SLTE CL-AIT Manager는 무엇을 해야 하는가?"**

Legacy는 과거 구현의 동작을 알려주는 **Evidence**이고, 현재 SLTE 코드는 구현 가능한 **현실적 Architecture/Interface 제약**을 알려준다.

둘 사이에서 먼저 **Target Requirement(SRS)** 를 정의해야 이후 HLD와 구현 방향이 올바르게 결정된다.

따라서 올바른 전체 흐름은 다음과 같다.

```text
Phase 1
Legacy Behavior Baseline
        ↓
Phase 2
SLTE Candidate Scope
        ↓
★ Phase 3
Target SLTE CL-AIT Requirement(SRS)
        ↓
Phase 4
Target SLTE CL-AIT HLD
        ↓
Phase 5
Implementation
        ↓
Phase 6
Verification
```

---

# 2. 이 문서에서 수행할 범위

이번 작업에서는 **Phase 3 — Target Requirement 정의까지만 수행한다.**

다음은 하지 않는다.

- Target HLD 작성
- Legacy ↔ SLTE 최종 코드 Gap 분석
- 코드 수정
- 구현
- UT 작성
- commit / push / PR

Requirement가 충분히 정의되면 **Requirement Gate에서 STOP**한다.

---

# 3. 가장 먼저 할 일 — Phase 1~2 결과 확인

회사에 복귀했을 때 처음 해야 할 일은 Phase 1~2를 다시 실행하는 것이 아니다.

먼저 기존 작업 결과를 확인한다.

우선 다음 파일/산출물을 찾는다.

```text
cl_ait_refactor/
├── phase01_legacy/
│   ├── legacy_cl_ait_behavior_inventory.md
│   ├── legacy_cl_ait_evidence.yaml
│   ├── legacy_cl_ait_msc_correlation.md
│   ├── legacy_unknowns.md
│   ├── legacy_conflicts.md
│   └── phase01_status.md
│
├── phase02_slte/
│   ├── slte_baseline.md
│   ├── slte_cl_ait_scope_facts.json
│   ├── slte_candidate_inventory.md
│   └── phase02_status.md
│
└── phase01_02_summary.md
```

실제 파일명이나 구조가 일부 다르더라도 **같은 의미의 산출물이 있으면 재사용**한다.

---

# 4. Phase 2 결과는 두 가지 경우로 나눈다

## Case A — Phase 2 결과가 충분한 경우

다음 정보가 있으면 Target Requirement 작성을 진행한다.

- 현재 SLTE branch/root가 명확함
- CL-AIT 관련 candidate module/file/API가 어느 정도 좁혀짐
- Legacy Behavior와 연결 가능한 symbol/state/timer/interface 등의 anchor가 있음
- 중요한 UNKNOWN/CONFLICT가 무엇인지 식별됨
- 전체 코드를 다시 분석하지 않아도 Target Requirement 논의가 가능함

이 경우 바로 **Phase 3 Target Requirement Definition**으로 이동한다.

---

## Case B — Phase 2 결과가 부족한 경우

예:

- CL-AIT 후보가 너무 넓음
- 주요 interface가 전혀 확인되지 않음
- current SLTE branch가 불명확함
- Legacy Behavior와 연결할 anchor가 없음
- `UNKNOWN`이 너무 많아 Requirement 판단 자체가 어려움

이 경우 Phase 1~2 전체를 처음부터 다시 수행하지 않는다.

**부족한 항목만 제한적으로 보강한다.**

예:

```text
State 처리 근거 부족
→ 관련 state/API 파일만 추가 확인

RF/HAL 전달 경로 부족
→ 해당 interface 주변만 추가 probe

Timer ownership 불명확
→ timer 관련 candidate만 제한 분석
```

보강 후 `phase01_02_summary.md`를 업데이트하고 다시 Gate를 판정한다.

---

# 5. Phase 3 — Target SLTE CL-AIT Requirement 정의

## 5.1 Requirement의 근거

Target Requirement는 Legacy 내용을 그대로 복사해서 만들지 않는다.

다음 네 가지 근거를 함께 사용한다.

```text
① Legacy Behavior Evidence
        +
② 현재 SLTE Architecture / Candidate Scope
        +
③ 사용자가 원하는 새로운 CL-AIT Manager 방향
        +
④ 필요한 경우 기존 L1/SLTE 공통 제약
        ↓
Target SLTE CL-AIT Requirement
```

가장 중요한 원칙:

> **Legacy는 Requirement의 유일한 출처가 아니다.**

Legacy에 있던 기능 중에서도:

- 반드시 유지할 것
- SLTE 구조에 맞게 변경할 것
- 제거할 것
- 새로 추가할 것

을 구분해야 한다.

---

# 6. 먼저 사용자의 Target Direction을 Requirement Input으로 만든다

사용자가 새로운 CL-AIT Manager를 어떤 방향으로 만들고 싶은지 알고 있다면, 이를 가장 먼저 기록한다.

예:

```text
Target Direction
- CL-AIT 동작을 중앙 Manager에서 관리하고 싶다.
- OL-AIT와 CL-AIT의 동시 동작을 명확히 방지하고 싶다.
- Event/Periodic trigger를 하나의 정책으로 관리하고 싶다.
- Stack/domain별 context가 명확해야 한다.
- HAL/RF 전달 책임을 상위 decision과 분리하고 싶다.
- 향후 기능 확장이 쉬운 구조여야 한다.
```

사용자가 아직 상세 내용을 정하지 않았다면 LLM이 임의로 확정하지 않는다.

대신 Legacy/SLTE Evidence를 기반으로 **Decision Needed** 형태로 정리한다.

예:

```text
DECISION-001
CL-AIT periodic timer ownership을 AitMngr가 가질지,
별도 CL procedure가 가질지 결정 필요.

Evidence:
- Legacy: ...
- Current SLTE: ...

Recommendation:
...
```

---

# 7. Legacy Behavior를 Requirement 후보로 변환

Phase 1의 Behavior를 그대로 Requirement로 복사하지 않는다.

각 Behavior마다 다음 질문을 적용한다.

```text
1. SLTE에서도 반드시 필요한가?
2. 동일한 동작을 유지해야 하는가?
3. SLTE 구조에 맞게 책임을 변경해야 하는가?
4. 제거 가능한 Legacy 제약인가?
5. 새로운 요구가 필요한가?
```

그리고 다음 상태 중 하나를 붙인다.

```text
KEEP
MODIFY
REMOVE
NEW
DECISION_NEEDED
```

예:

| Legacy Behavior | Target 판단 | 의미 |
|---|---|---|
| CL-AIT Trigger | MODIFY | SLTE trigger 구조에 맞게 재정의 |
| OL/CL 동시 방지 | KEEP | 필수 기능 |
| Legacy 특정 Timer Class | REMOVE | 구조 자체는 가져오지 않음 |
| Manager 중앙 상태관리 | NEW | Target에서 신규 요구 |
| Stack Context | DECISION_NEEDED | SLTE 구조 확인 후 결정 |

---

# 8. Requirement 종류

Target Requirement는 최소 다음 네 영역으로 나눈다.

## 8.1 Functional Requirement — FR

CL-AIT Manager가 **무엇을 해야 하는지** 정의한다.

예:

```text
FR-001
CL-AIT Manager는 CL-AIT 실행 요청을 수신하고
현재 상태 및 실행 조건을 평가해야 한다.

FR-002
CL-AIT Manager는 OL-AIT가 수행 중인 경우
CL-AIT와의 동시 실행을 허용하지 않아야 한다.

FR-003
CL-AIT Manager는 periodic/event trigger에 대해
CL-AIT 재평가를 수행해야 한다.
```

구현 클래스명이나 함수명은 Requirement에 넣지 않는 것을 기본으로 한다.

---

## 8.2 Non-Functional Requirement — NFR

Architecture에 영향을 주는 품질 요구사항을 정의한다.

최신 HLD Template과 연결하기 쉽도록 다음 관점을 우선 사용한다.

```text
Maintainability
Efficiency
Reliability
```

예:

```text
NFR-001 Maintainability
CL-AIT trigger/decision/send 책임은
변경 영향 범위를 최소화할 수 있도록 분리 가능해야 한다.

NFR-002 Efficiency
Periodic evaluation은 불필요한 RF/HAL command를
발생시키지 않아야 한다.

NFR-003 Reliability
OL/CL conflict 또는 invalid state에서
잘못된 command가 하위 계층으로 전달되지 않아야 한다.
```

---

## 8.3 Constraint — CON

현재 SLTE/HW/Interface 때문에 반드시 지켜야 하는 제약을 기록한다.

예:

```text
CON-001
기존 SLTE HAL/RF interface와 호환되어야 한다.

CON-002
현재 stack/domain context model을 위반해서는 안 된다.
```

근거가 부족한 제약을 임의로 만들지 않는다.

---

## 8.4 Open Decision — DEC

아직 결정되지 않은 Architecture/Policy 항목은 Requirement에 숨기지 않고 명시한다.

예:

```text
DEC-001
Periodic timer ownership

DEC-002
CL-AIT state ownership

DEC-003
OL/CL arbitration 위치
```

이 항목은 Target HLD로 넘어가기 전에 가능한 한 해결한다.

---

# 9. Requirement Traceability

각 Requirement에는 왜 필요한지 추적 가능한 근거를 붙인다.

권장 형식:

| Req ID | Requirement | Origin | Evidence | Status |
|---|---|---|---|---|
| FR-001 | CL-AIT 실행 조건 평가 | Legacy + Target | BHV-001/BHV-003 | DRAFT |
| FR-002 | OL/CL 동시 실행 방지 | Legacy | BHV-004 | CONFIRMED |
| FR-003 | SLTE 중앙 상태관리 | Target | User Direction | PROPOSED |
| CON-001 | 기존 HAL 인터페이스 호환 | SLTE | Candidate/API | CONFIRMED |

Origin 값:

```text
LEGACY
SLTE
TARGET
LEGACY+SLTE
LEGACY+TARGET
SLTE+TARGET
```

---

# 10. Requirement 작성 시 반드시 분리할 것

다음을 혼합하지 않는다.

## Requirement
```text
CL-AIT Manager는 OL-AIT와 CL-AIT의 동시 실행을 방지해야 한다.
```

## Design
```text
AitMngr::CheckAitConflict()에서 확인한다.
```

두 번째 문장은 HLD/구현 단계의 내용이다.

Phase 3에서는 **WHAT / WHY**를 정의하고,
Phase 4 HLD에서 **HOW / WHERE**를 결정한다.

---

# 11. Requirement 산출물

권장 구조:

```text
cl_ait_refactor/
└── phase03_requirement/
    ├── target_direction.md
    ├── legacy_behavior_disposition.md
    ├── slte_cl_ait_target_requirements.md
    ├── requirement_traceability.yaml
    ├── open_decisions.md
    ├── requirement_unknowns.md
    └── phase03_status.md
```

---

# 12. 핵심 산출물 — `slte_cl_ait_target_requirements.md`

권장 형식:

```markdown
# SLTE CL-AIT Manager Target Requirements

## 1. Purpose
새로운 SLTE 기반 CL-AIT Manager의 목적

## 2. Scope
### In Scope
...

### Out of Scope
...

## 3. Functional Requirements

### FR-001 <Name>
Requirement:
...

Rationale:
...

Origin:
LEGACY / SLTE / TARGET / combination

Evidence:
...

Acceptance Criteria:
...

Status:
DRAFT / CONFIRMED / DECISION_NEEDED

## 4. Non-Functional Requirements
### NFR-001 ...
...

## 5. Constraints
### CON-001 ...
...

## 6. Open Decisions
### DEC-001 ...
...

## 7. Legacy Behavior Disposition
| Behavior | KEEP/MODIFY/REMOVE/NEW | Related Requirement |
|---|---|---|

## 8. Traceability
| Req ID | Origin | Evidence | Related Behavior | Status |
|---|---|---|---|---|
```

---

# 13. Acceptance Criteria를 반드시 포함

Requirement를 추상적인 문장으로 끝내지 않는다.

각 주요 FR에는 최소한 확인 가능한 Acceptance Criteria를 붙인다.

예:

```text
FR-002
OL-AIT와 CL-AIT의 동시 실행을 방지해야 한다.

Acceptance Criteria:
AC-002-1
OL-AIT running 상태에서 CL-AIT 실행 요청이 들어오면
두 procedure가 동시에 RF command를 발생시키지 않는다.

AC-002-2
Block/defer 이후 재실행 조건이 정의되어야 한다.
```

이 Acceptance Criteria는 이후 HLD Verification Point와 UT의 입력이 된다.

---

# 14. Requirement Gate

## READY

다음을 만족하면 HLD 단계로 진행할 수 있다.

- Target CL-AIT 목적과 Scope가 명확함
- 핵심 Functional Requirement가 정의됨
- 주요 NFR/Constraint가 정의됨
- Legacy Behavior에 대한 KEEP/MODIFY/REMOVE 판단이 대부분 존재
- 중요한 Requirement마다 Evidence 또는 사용자 Target Direction이 있음
- 주요 FR에 Acceptance Criteria가 있음
- HLD 설계를 막는 P0 Open Decision이 없음

---

## PARTIAL

다음과 같은 경우:

- Requirement 대부분은 작성됨
- 일부 상세 policy가 미정
- HLD 후보 비교를 통해 결정 가능한 Open Decision만 남음

이 경우 HLD로 조건부 진행 가능하나 Open Decision을 명시적으로 전달한다.

---

## BLOCKED

다음 중 하나면 HLD로 넘어가지 않는다.

- 새로운 CL-AIT Manager의 목적 자체가 불명확
- 핵심 기능 KEEP/MODIFY/REMOVE 판단이 안 됨
- 중요한 SLTE 제약을 알 수 없음
- Legacy 동작을 그대로 Requirement로 복사했을 뿐 Target 판단이 없음
- Critical Acceptance Criteria를 정의할 수 없음

---

# 15. 회사 복귀 후 실제 실행 순서

가장 빠른 순서는 다음이다.

```text
STEP 1
어제 수행한 Phase 1~2 결과 찾기
        ↓
STEP 2
phase01_02_summary / status 확인
        ↓
STEP 3
Phase 2 충분성 판정
        │
        ├─ 부족
        │    ↓
        │  부족한 Evidence만 보강
        │    ↓
        │  Phase 2 재판정
        │
        └─ 충분
             ↓
STEP 4
Target Direction 반영
             ↓
STEP 5
Legacy Behavior
KEEP / MODIFY / REMOVE / NEW 판단
             ↓
STEP 6
Target FR/NFR/Constraint/Decision 작성
             ↓
STEP 7
Acceptance Criteria 작성
             ↓
STEP 8
Requirement Gate
             ↓
           STOP
```

---

# 16. 회사 LLM에 바로 요청할 프롬프트

아래 내용을 그대로 복사해 사용할 수 있다.

```text
어제 수행한 Legacy CL-AIT → SLTE 리팩토링 Phase 1~2 결과를 이어서 진행해줘.

최종 목표는 Legacy CL-AIT를 그대로 포팅하는 것이 아니라
새로운 SLTE Base의 CL-AIT Manager를 구현하는 것이다.

따라서 이번에는 HLD나 구현으로 바로 넘어가지 말고,
먼저 Target SLTE CL-AIT Manager Requirement(SRS)를 정의한다.

[STEP 1 — 기존 결과 확인]

1. 기존 cl_ait_refactor 작업 결과를 찾아라.
2. phase01_legacy / phase02_slte / phase01_02_summary에 해당하는 결과를 확인하라.
3. 기존 결과가 있으면 Phase 1~2를 처음부터 다시 수행하지 마라.
4. Phase 1/2가 READY/PARTIAL/BLOCKED 중 어떤 상태인지 확인하라.
5. 실제 산출물이 상태 판정과 일치하는지도 점검하라.

[STEP 2 — Phase 2 충분성 판정]

다음 정보가 Target Requirement 작성에 충분한지 확인하라.

- Legacy CL-AIT 주요 Behavior
- Code/MSC Evidence
- 주요 UNKNOWN/CONFLICT
- 현재 SLTE baseline/branch
- CL-AIT 관련 SLTE candidate module/file/API/state/timer/interface
- Legacy와 SLTE를 연결할 수 있는 search/evidence anchor

충분하면 Requirement 작성으로 진행한다.

부족하면 Phase 1~2 전체를 재실행하지 말고
Requirement 작성에 꼭 필요한 부족 Evidence만 제한적으로 보강하라.

[STEP 3 — Target Direction]

새로운 SLTE CL-AIT Manager의 목표는 Legacy 구조 복제가 아니다.

Legacy Behavior와 현재 SLTE Architecture를 참고하여
Target CL-AIT Manager가 가져야 할 기능/책임/제약을 정의한다.

내가 별도로 제공하는 방향이 있다면 가장 중요한 Target Input으로 사용한다.

사용자 결정이 필요한 부분을 임의로 확정하지 말고
DECISION_NEEDED로 기록한다.

[STEP 4 — Legacy Behavior Disposition]

각 Legacy Behavior를 다음 중 하나로 분류한다.

- KEEP
- MODIFY
- REMOVE
- NEW
- DECISION_NEEDED

Legacy class/function 구조 자체를 Requirement로 만들지 않는다.

[STEP 5 — Target Requirement 작성]

다음 유형으로 작성한다.

1. Functional Requirement — FR
2. Non-Functional Requirement — NFR
   - Maintainability
   - Efficiency
   - Reliability
3. Constraint — CON
4. Open Decision — DEC

Requirement는 WHAT/WHY 중심으로 작성하고
구체적인 class/function 배치는 HLD 단계로 남긴다.

각 Requirement에는 가능한 경우 다음을 포함한다.

- Requirement ID
- Requirement
- Rationale
- Origin
- Evidence
- Acceptance Criteria
- Status

Origin은 다음 중 사용한다.

LEGACY
SLTE
TARGET
LEGACY+SLTE
LEGACY+TARGET
SLTE+TARGET

[STEP 6 — Acceptance Criteria]

주요 Functional Requirement마다
향후 HLD Verification / UT로 연결 가능한 Acceptance Criteria를 작성한다.

[STEP 7 — 산출물]

다음 폴더를 생성 또는 갱신한다.

cl_ait_refactor/
└── phase03_requirement/
    ├── target_direction.md
    ├── legacy_behavior_disposition.md
    ├── slte_cl_ait_target_requirements.md
    ├── requirement_traceability.yaml
    ├── open_decisions.md
    ├── requirement_unknowns.md
    └── phase03_status.md

[STEP 8 — Gate]

READY:
- Target Purpose/Scope 명확
- 핵심 FR 정의
- 주요 NFR/Constraint 정의
- Legacy Behavior disposition 존재
- 주요 FR Acceptance Criteria 존재
- HLD를 막는 P0 Decision 없음

PARTIAL:
- 대부분 정의되었으나 일부 HLD 단계에서 결정 가능한 항목만 남음

BLOCKED:
- Target 목적/핵심 Requirement 자체를 결정할 정보 부족

[중요]

이번에는:
- Target HLD를 작성하지 않는다.
- Legacy↔SLTE 최종 코드 Gap을 확정하지 않는다.
- 코드를 수정하지 않는다.
- 구현하지 않는다.
- commit/push/PR하지 않는다.

Requirement Gate까지 수행하고 STOP한다.

[최종 보고]

아래 순서로 간결하게 보고한다.

1. Phase 1 상태
2. Phase 2 상태
3. Phase 2 보강 여부 및 보강 내용
4. Target CL-AIT Purpose/Scope
5. 핵심 Functional Requirement
6. 핵심 NFR/Constraint
7. Legacy KEEP/MODIFY/REMOVE/NEW 요약
8. Open Decision
9. Requirement Gate 결과
10. Target HLD 단계 진행 가능 여부
```

---

# 17. 사용자가 추가하면 좋은 정보

회사에서 위 프롬프트 실행 전에, 본인이 이미 생각해 둔 CL-AIT Manager 방향이 있다면 아래처럼 몇 줄만 추가하면 된다.

```text
[내가 원하는 Target 방향]

- ...
- ...
- ...
```

완성된 SRS를 미리 작성해서 줄 필요는 없다.

**"어떤 방향의 CL-AIT Manager를 만들고 싶은가" 수준의 요구만 있어도 된다.**

LLM은 이를 Legacy/SLTE Evidence와 결합해서 Requirement 후보를 만들고,
결정이 필요한 것은 사용자에게 명확히 구분해서 보여줘야 한다.

---

# 18. 다음 단계

Requirement Gate가 READY가 되면 그 다음 순서는:

```text
Phase 4
Target SLTE CL-AIT HLD
        ↓
Requirement ↔ Architecture Traceability
        ↓
Design Decision
        ↓
Legacy/Current Code와 구현 Gap 확정
        ↓
Phase 5
Implementation
        ↓
Phase 6
Verification
```

중요한 점은 **Gap 분석의 기준이 Legacy HLD가 아니라 Target Requirement + Target HLD가 된다는 것**이다.

즉 이후 질문은:

```text
"Legacy와 SLTE 코드가 얼마나 다른가?"
```

가 아니라

```text
"Target Requirement/HLD를 만족하기 위해
현재 SLTE 코드에 무엇을 추가/변경/제거해야 하는가?"
```

가 되어야 한다.

---

# 19. 핵심 요약

```text
어제 작업
Phase 1 Legacy Behavior
        ↓
Phase 2 SLTE Scope
        ↓

오늘 회사에서
Phase 2 결과 확인
        ↓
부족하면 필요한 부분만 보강
        ↓
★ Target SLTE CL-AIT Requirement(SRS)
        ↓
Requirement Gate
        ↓
STOP

그 다음
Target HLD
→ Implementation Gap
→ 구현
→ 검증
```

**새로운 SLTE CL-AIT Manager 구현의 기준은 Legacy 코드가 아니라 Target Requirement이다.  
Legacy 분석 결과와 현재 SLTE 코드는 그 Requirement를 정확하고 현실적으로 만들기 위한 Evidence다.**
