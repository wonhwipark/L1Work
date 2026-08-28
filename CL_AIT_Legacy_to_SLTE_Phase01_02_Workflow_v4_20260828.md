# Legacy CL-AIT → SLTE 리팩토링 준비 워크플로우
**범위:** Phase 1~2 — Legacy Behavior Baseline 복원 + 현재 SLTE 대상 코드 범위 확정  
**작성일:** 2026-08-27  
**Revision:** v2 — Legacy HLD 없음 / 기존 일부 MSC 보유 조건 반영  
**대상 환경:** OpenCode / 저사양 LLM / skillsilent 기반 L1 SW 개발 환경

---

## 1. 배경

Legacy L1의 **CL-AIT(Closed Loop AIT)** 기능에 대해 다음 자산이 존재한다.

### 현재 확보된 Legacy 자산
- 기존 `code-analyzer` 분석 결과
- Legacy CL-AIT 관련 **일부 MSC**
- 필요 시 확인 가능한 Legacy source

### 현재 없는 자산
- 완성된 Legacy CL-AIT HLD

따라서 이번 리팩토링의 출발점은 Legacy HLD가 아니다.

> **기존 code-analyzer 결과를 1차 Evidence로 사용하고, 기존 MSC를 동작 흐름 보강용 2차 Evidence로 활용하여 Legacy CL-AIT Behavior Baseline을 복원한다.**

목표는 Legacy 코드 구조를 SLTE에 그대로 복제하는 것이 아니다.

> **Legacy에서 확인된 동작·책임·제약을 Behavior 단위로 복원한 뒤, 현재 SLTE Architecture에서 그 책임이 어디에 존재하거나 재배치되어야 하는지를 찾는다.**

---

# 2. 이번 단계의 목표

이번 실행에서는 아래 두 단계까지만 수행한다.

## Phase 1 — Legacy CL-AIT Behavior Baseline 복원
기존 code-analyzer 결과와 일부 MSC를 이용하여 다음을 정리한다.

- Trigger
- Periodic Scheduling
- State Gate
- OL/CL Arbitration
- Event / Update Handling
- CL Decision
- Command/Data Build
- HAL/RF/PHY Interface
- Context / State Update
- Stop / Restart
- Exception / Boundary
- Stack / Domain Isolation

## Phase 2 — Current SLTE CL-AIT Scope 확정
현재 SLTE branch/root에서 전체 코드를 다시 분석하지 않고 CL-AIT 관련 후보만 좁힌다.

---

# 3. 이번 단계에서 하지 않는 것

Phase 1~2에서는 아래 작업을 수행하지 않는다.

- Legacy HLD 신규 작성
- Target SLTE HLD 작성
- Legacy ↔ SLTE 최종 Gap 판정
- `EQUIVALENT / PARTIAL / MISSING / ARCH_CONFLICT / NEEDS_DECISION` 최종 분류
- 코드 수정
- commit / push / PR
- Legacy 구현 구조를 Knowledge Manager의 승인 지식으로 등록

Phase 1~2 완료 후 반드시 STOP한다.

---

# 4. 전체 Workflow

```text
Legacy code-analyzer output
        │
        │  1차 Evidence
        ▼
┌───────────────────────────────┐
│ Phase 1A                      │
│ Legacy Code Fact Extraction   │
└───────────────┬───────────────┘
                │
                │
Legacy 일부 MSC │  2차 Evidence
        ────────┤
                ▼
┌───────────────────────────────┐
│ Phase 1B                      │
│ Behavior Reconstruction       │
│                               │
│ Code Fact + MSC Correlation   │
└───────────────┬───────────────┘
                │
                ▼
      Legacy Behavior Baseline
                │
                ▼
         [Phase 1 Gate]
                │
                ▼
Current SLTE root / branch
                │
                ▼
┌───────────────────────────────┐
│ Phase 2                       │
│ SLTE FEATURE_SCOPE_PROBE      │
│                               │
│ manifest reuse               │
│ → bounded source scan        │
└───────────────┬───────────────┘
                │
                ▼
       SLTE Candidate Scope
                │
                ▼
         [Phase 2 Gate]
                │
                ▼
             STOP
```

---

# 5. Evidence 우선순위

Legacy CL-AIT Behavior를 복원할 때 Evidence의 우선순위를 다음과 같이 적용한다.

```text
1. Legacy source에서 직접 확인된 Code Fact
2. 기존 code-analyzer 결과
3. 기존 MSC
4. 기존 분석 메모 / 문서
5. 추론
```

단, 기존 code-analyzer 결과가 실제 source의 revision/provenance와 연결되어 있다면 실무적으로 1차 입력으로 재사용한다.

---

# 6. MSC의 역할

기존 MSC는 매우 유용하지만 **완전한 설계 명세로 간주하지 않는다.**

MSC는 주로 아래 항목을 보강하는 데 사용한다.

- caller / callee 순서
- module 간 interaction
- trigger 이후 call sequence
- command 전달 경로
- response / callback
- start / stop / retry 흐름
- timer/event에 따른 sequence
- 특정 예외 scenario

MSC만으로 다음을 확정하지 않는다.

- 전체 state machine
- 모든 exception
- 모든 조건문
- concurrency ownership
- 모든 interface
- 전체 CL-AIT Architecture

---

# 7. Code Analysis와 MSC가 충돌하는 경우

예:

```text
MSC:
A → B → C → RF

Code Analyzer / Source:
A → B → D → C → RF
```

이 경우 MSC를 자동 수정하거나 무시하지 않는다.

다음과 같이 기록한다.

```text
STATUS: CONFLICT

MSC Evidence:
A → B → C → RF

Code Evidence:
A → B → D → C → RF

Possible Reason:
- MSC 작성 시점이 이전 revision일 가능성
- diagram 단순화 가능성
- optional path 생략 가능성
- implementation 변경 가능성

Decision:
Phase 1에서는 Code Fact 우선
MSC discrepancy는 별도 unresolved item으로 유지
```

---

# 8. Phase 1 — Legacy CL-AIT Behavior Baseline 복원

## 8.1 입력 우선순위

### 필수 또는 우선 입력
1. Legacy `code_analysis_manifest.json`
2. Legacy `code-analyzer` output
3. Legacy CL-AIT 관련 일부 MSC

### 필요 시 보조 입력
4. Legacy source root
5. 관련 log / state / enum / timer 이름
6. 기타 분석 문서

Legacy HLD는 필수 입력이 아니다.

---

# 9. Phase 1A — Legacy Code Fact Extraction

기존 code-analyzer 결과에서 CL-AIT 관련 항목을 먼저 찾는다.

우선 확인 대상:

```text
feature name
symbol
class
function
caller
callee
state
enum
timer
callback
message
HAL API
RF API
PHY interface
context
log string
```

전체 Legacy code를 처음부터 재분석하지 않는다.

---

# 10. Legacy Provenance 기록

가능한 범위에서 다음을 기록한다.

| 항목 | 내용 |
|---|---|
| Source Type | code-analyzer / source / MSC |
| Legacy Branch | 확인 가능한 값 |
| Revision | CL / commit / tag |
| Code Root | 분석 대상 root |
| Analyzer Version | 확인 가능한 경우 |
| Manifest | 존재 여부 |
| MSC Name | MSC 파일/문서명 |
| MSC Revision | 확인 가능한 경우 |
| Scope | CL-AIT 관련 범위 |
| Confidence | HIGH / MEDIUM / LOW |

모르는 값은 `UNKNOWN`으로 유지한다.

---

# 11. Phase 1B — MSC Correlation

기존 MSC에서 다음을 추출한다.

```text
MSC Scenario
Actor / Module
Entry Event
Call Sequence
Message
Callback
State Change
Timer
Result
Stop / Restart
Exception Path
```

MSC의 각 step을 code-analyzer 결과와 가능한 범위에서 연결한다.

예:

```text
MSC-01 Step 1
AitMngr → ClAitProc : StartClAit()

Code Evidence
file: ...
symbol: ...
caller: ...
callee: ...

Correlation:
MATCHED
```

---

# 12. MSC Correlation 상태

각 MSC step은 다음 중 하나로 표시한다.

```text
MATCHED
PARTIALLY_MATCHED
CODE_ONLY
MSC_ONLY
CONFLICT
UNKNOWN
```

### 의미

| 상태 | 의미 |
|---|---|
| MATCHED | 코드와 MSC가 동일한 동작을 지지 |
| PARTIALLY_MATCHED | 일부 flow만 확인 |
| CODE_ONLY | 코드에서 확인되나 MSC에는 없음 |
| MSC_ONLY | MSC에는 있으나 코드 분석에서 미확인 |
| CONFLICT | 순서/책임/조건이 서로 다름 |
| UNKNOWN | 현재 자료로 판단 불가 |

---

# 13. Legacy Behavior Inventory

Legacy 구현의 클래스/함수를 그대로 나열하기보다 Behavior 단위로 정규화한다.

권장 ID:

```text
BHV-CL-AIT-001  Trigger
BHV-CL-AIT-002  Periodic Scheduling
BHV-CL-AIT-003  State Gate
BHV-CL-AIT-004  OL/CL Arbitration
BHV-CL-AIT-005  Update/Event Handling
BHV-CL-AIT-006  CL Decision
BHV-CL-AIT-007  Command/Data Build
BHV-CL-AIT-008  HAL/RF/PHY Send
BHV-CL-AIT-009  Context/State Update
BHV-CL-AIT-010  Stop/Restart
BHV-CL-AIT-011  Exception/Boundary
BHV-CL-AIT-012  Stack/Domain Isolation
```

각 Behavior에 반드시 Evidence 종류를 붙인다.

예:

```text
Behavior ID:
BHV-CL-AIT-004

Behavior:
OL-AIT와 CL-AIT 동시 수행 방지

Evidence:
- CODE_ANALYZER: ...
- MSC: MSC_CL_AIT_02 / step 4~7
- SOURCE: ...

Evidence Status:
MATCHED

Confidence:
HIGH
```

---

# 14. Legacy Behavior Baseline에서 구분할 상태

각 Behavior는 아래 중 하나로 관리한다.

```text
CONFIRMED
PARTIAL
MSC_ONLY
CODE_ONLY
CONFLICT
UNKNOWN
```

`MSC_ONLY`를 `CONFIRMED`로 자동 승격하지 않는다.

---

# 15. Phase 1 산출물

권장 구조:

```text
<WORK_ROOT>/cl_ait_refactor/
└── phase01_legacy/
    ├── legacy_source_inventory.md
    ├── legacy_provenance.yaml
    ├── legacy_cl_ait_code_facts.yaml
    ├── legacy_cl_ait_msc_inventory.md
    ├── legacy_cl_ait_msc_correlation.md
    ├── legacy_cl_ait_behavior_inventory.md
    ├── legacy_cl_ait_evidence.yaml
    ├── legacy_unknowns.md
    ├── legacy_conflicts.md
    └── phase01_status.md
```

---

# 16. `legacy_cl_ait_msc_inventory.md`

권장 형식:

```markdown
# Legacy CL-AIT MSC Inventory

| MSC ID | Scenario | Source | Revision | Coverage | Status |
|---|---|---|---|---|---|
| MSC-001 | CL-AIT Start | ... | UNKNOWN | Partial | AVAILABLE |
| MSC-002 | Periodic CL-AIT | ... | ... | Partial | AVAILABLE |
```

---

# 17. `legacy_cl_ait_msc_correlation.md`

권장 형식:

```markdown
# Legacy CL-AIT MSC ↔ Code Correlation

## MSC-001

| Step | MSC Flow | Code Evidence | Correlation | Note |
|---|---|---|---|---|
| 1 | A → B | file/symbol | MATCHED | |
| 2 | B → C | file/symbol | PARTIALLY_MATCHED | condition 확인 필요 |
| 3 | C → RF | 미확인 | MSC_ONLY | source 확인 필요 |
```

---

# 18. `legacy_conflicts.md`

Code와 MSC가 충돌하는 항목만 별도로 관리한다.

예:

```markdown
## CONFLICT-001

Behavior:
CL-AIT command send path

MSC:
A → B → RF

Code:
A → B → Resolver → RF

Possible Cause:
MSC revision 불일치 또는 simplification

Status:
OPEN

Phase 1 Decision:
Code Fact 우선.
Phase 3에서 설계 의미 재검토.
```

---

# 19. Phase 1 Gate

## READY

다음을 만족하면 READY로 본다.

- Legacy CL-AIT 관련 code-analyzer 결과를 식별 가능
- 주요 procedure/call path를 추적 가능
- Trigger / 주요 Behavior / Interface에 대한 코드 근거 확보
- 일부 MSC가 Behavior flow 보강에 사용됨
- MSC와 코드 간 차이는 별도 상태로 관리됨
- SLTE 탐색에 사용할 feature/symbol/API/state/timer hint 확보

---

## PARTIAL

다음과 같은 경우:

- 일부 Behavior는 MSC만 존재
- 일부 state/exception이 미확인
- MSC revision이 불명확
- 일부 flow가 code-analyzer와 부분적으로만 매칭

단, SLTE Feature Scope Probe에 사용할 anchor가 충분하면 Phase 2 진행 가능하다.

---

## BLOCKED

다음과 같은 경우:

- code-analyzer 결과에서 CL-AIT 범위를 식별할 수 없음
- MSC에도 usable actor/API/state anchor가 없음
- Legacy source/분석 결과와 MSC 사이 provenance를 전혀 연결할 수 없음
- SLTE 후보 검색에 사용할 anchor를 만들 수 없음

---

# 20. Phase 2 — Current SLTE CL-AIT Scope 확정

## 20.1 입력

다음 중 하나 이상을 확보한다.

- 현재 SLTE working branch root
- SLTE repository root
- 현재 branch의 `code_analysis_manifest.json`
- 기존 SLTE code-analyzer output

필수적으로 기록:

```text
Repository
Branch
Commit
Code Root
Existing Code Analyzer Manifest
```

---

# 21. SLTE 분석 및 보강 원칙

저사양 OpenCode를 고려하여 다음 순서를 지킨다.

```text
기존 SLTE manifest
        ↓
기존 code-analyzer output
        ↓
FEATURE_SCOPE_PROBE
        ↓
Phase 2 Gate
        │
        ├─ READY → STOP
        │
        └─ PARTIAL / BLOCKED
                 ↓
        Missing Evidence Triage
                 ↓
        ┌────────────────────────────┐
        │ code-analyzer             │
        │ 현재 코드 Fact 보강        │
        └─────────────┬──────────────┘
                      │
        ┌─────────────▼──────────────┐
        │ l1-knowledge-manager       │
        │ 승인 지식 read-only 조회   │
        └─────────────┬──────────────┘
                      │
                      ▼
            부족 Evidence만 재평가
```

전체 repository 재분석은 기본 동작으로 사용하지 않는다.

## 21.1 두 스킬의 역할을 혼합하지 않는다

### `code-analyzer`
현재 SLTE 코드의 **실제 구현 Fact**를 확인한다.

대표 확인 대상:

```text
current symbol
caller / callee
state transition
timer ownership
API call
HAL/RF/PHY interface
build/revision provenance
runtime/procedure evidence
```

### `l1-knowledge-manager`
현재 코드 스캔을 대신하는 도구가 아니다.

다음과 같은 **기존 승인 지식**을 read-only로 조회하여 코드 확인 범위와 해석을 보강한다.

```text
component responsibility
ownership scope
known interface rule
approved state/policy rule
known legacy ↔ SLTE relation
approved domain knowledge
known replacement/commonization information
```

Phase 2 보강 중에는 새로운 지식을 자동 등록하거나 승인하지 않는다.

---

# 22. Phase 1 결과를 Phase 2 검색 Anchor로 사용

Phase 1에서 확보한 다음 정보를 SLTE scope probe와 Knowledge 조회 selector에 사용한다.

```text
feature name
legacy symbol
API
state
enum
timer
message
HAL/RF interface
log string
caller/callee
MSC actor/module name
component/path hint
```

MSC에만 존재하는 이름은 검색 hint로 사용할 수 있지만, SLTE에 동일한 구조가 있다고 가정하지 않는다.

---

# 23. FEATURE_SCOPE_PROBE

자연어 요청 예:

```text
현재 SLTE branch에서 CL-AIT 관련 scope만 찾아줘.

Phase 1에서 확보한 Legacy code evidence와 MSC actor/API/state/timer hint를 검색 anchor로 사용해줘.

기존 code_analysis_manifest.json이 현재 branch와 유효하면 우선 재사용하고,
전체 코드 재분석은 하지 말아줘.

Legacy class/module 이름이 SLTE에 없더라도
동일한 이름이 없다는 이유만으로 MISSING으로 판정하지 말고
renamed/commonized/restructured 가능성을 고려해서 candidate만 수집해줘.
```

---

# 24. SLTE Candidate 수집 대상

| 분류 | 대상 |
|---|---|
| Module | CL-AIT 책임 후보 |
| File | source/header |
| API | update/start/stop/send |
| State | connected/running/pending |
| Timer | periodic/timer |
| Data | context/info/config |
| Interface | HAL/RF/PHY |
| Caller | Front/Measure/Tx/Config 등 |
| Evidence | symbol/call/state/string/analyzer fact |

각 candidate는 다음 정보를 가진다.

```text
candidate_id
path
symbol
candidate_type
evidence
evidence_source
legacy_anchor
confidence
reason
```

---

# 25. Phase 2 부족 Evidence 보강 절차

Phase 2가 `PARTIAL` 또는 `BLOCKED`이면 바로 사용자에게 막연히 "정보가 부족하다"고 요청하지 않는다.

먼저 부족 항목을 다음 네 종류로 분류한다.

```text
AUTO_CODE_CHECK
AUTO_KNOWLEDGE_LOOKUP
USER_INPUT_REQUIRED
DECISION_REQUIRED
```

## 25.1 AUTO_CODE_CHECK

현재 source에서 확인 가능한 항목이다.

예:

```text
- 특정 state의 실제 update 위치
- timer start/cancel/expiry owner
- HAL/RF API 호출자
- candidate class의 caller/callee
- 특정 interface의 build/runtime 사용 여부
```

처리 원칙:

> `code-analyzer`를 사용하여 필요한 candidate 주변만 제한적으로 확인한다.

전체 분석을 재시작하지 않는다.

---

## 25.2 AUTO_KNOWLEDGE_LOOKUP

기존 승인 지식으로 보강할 수 있는 항목이다.

예:

```text
- 해당 component의 승인된 책임 범위
- ownership scope
- 기존 SLTE interface 정책
- 승인된 state/policy rule
- legacy component가 SLTE에서 대체/commonize되었다는 기존 지식
```

처리 원칙:

> `l1-knowledge-manager`의 read-only 조회를 사용한다.

저사양 환경에서는 자연어 요청을 먼저 `route`하고, 반환된 조회 action만 실행한다.

예시 요청:

```text
CL-AIT scope 보강을 위해
현재 SLTE branch의 AIT 관련 component, symbol, path에 대한
승인된 L1/SLTE 지식과 ownership 정보를 조회해줘.
새 candidate를 만들거나 승인하지 말고 read-only로 조회해줘.
```

`CANDIDATE_ONLY` 지식은 현재 사실처럼 사용하지 않는다.

---

## 25.3 USER_INPUT_REQUIRED

코드와 승인 지식만으로 복구할 수 없는 외부 입력이다.

예:

```text
- 실제 target branch/root가 어느 것인지
- 분석 대상에서 제외해야 할 별도 경로
- 사내에서만 알고 있는 feature naming/ownership 변경
- 추가 MSC/source 위치
```

이 경우에만 사용자에게 **필요한 최소 정보**를 요청한다.

---

## 25.4 DECISION_REQUIRED

코드 Fact 부족이 아니라 새로운 Target 설계 방향에 대한 결정이다.

예:

```text
- Target CL-AIT Manager가 timer를 직접 소유할 것인가
- OL/CL arbitration을 어느 책임 레이어에서 정의할 것인가
- Legacy 정책을 SLTE에서도 유지할 것인가
```

이 항목은 Phase 2를 억지로 해결하기 위해 사용자에게 구현 결정을 요구하지 않는다.

Phase 2 후보 탐색이 가능하다면 `DECISION_REQUIRED`로 보존하고,
다음 Target Requirement 단계의 `Open Decision` 입력으로 전달한다.

---

# 26. Code Fact ↔ Knowledge 충돌 처리

현재 코드와 Knowledge Manager의 승인 지식이 다르면 둘 중 하나를 자동으로 덮어쓰지 않는다.

예:

```text
Current Code Fact:
AitProc가 Timer를 직접 소유

Approved Knowledge:
AitMngr가 Timer ownership을 가진다고 기록
```

다음과 같이 처리한다.

```text
status: CODE_KNOWLEDGE_CONFLICT

current_implementation_fact:
  source/revision/evidence

approved_knowledge:
  rule/id/scope/revision(if available)

possible_interpretation:
  - knowledge stale
  - code regression
  - branch/scenario scope difference
  - architecture transition in progress
```

원칙:

- **현재 구현이 무엇인지** 판단할 때는 `code-analyzer` Fact를 사용한다.
- **기대 Architecture/정책이 무엇인지** 판단할 때는 승인 Knowledge를 참고한다.
- 어느 쪽이 Target Requirement가 되어야 하는지는 Phase 3에서 결정한다.
- Phase 2에서 Knowledge를 자동 stale 처리하거나 업데이트하지 않는다.

---

# 27. Phase 2 산출물

```text
<WORK_ROOT>/cl_ait_refactor/
└── phase02_slte/
    ├── slte_baseline.md
    ├── slte_manifest_reference.yaml
    ├── slte_cl_ait_scope_facts.json
    ├── slte_candidate_inventory.md
    ├── missing_evidence_triage.md
    ├── code_check_supplement.md
    ├── knowledge_lookup_summary.md
    ├── code_knowledge_conflicts.md
    └── phase02_status.md
```

`missing_evidence_triage.md`에는 각 부족 항목을 반드시 아래 중 하나로 표시한다.

```text
AUTO_CODE_CHECK
AUTO_KNOWLEDGE_LOOKUP
USER_INPUT_REQUIRED
DECISION_REQUIRED
RESOLVED
```

---

# 28. Phase 2 Gate

## READY
- SLTE branch/root 확정
- CL-AIT 관련 candidate scope 확보
- 각 candidate에 Evidence 존재
- Legacy Behavior와 비교 가능한 anchor 존재
- Requirement 작성에 필요한 핵심 코드 Fact 확보
- unresolved `USER_INPUT_REQUIRED` blocker 없음

## PARTIAL
- file/module 범위는 충분히 좁혀짐
- 일부 상세 state/decision은 추가 확인 또는 Phase 3 결정 필요
- `DECISION_REQUIRED`만 남아 있거나 비차단성 UNKNOWN만 존재
- 전체 repository 재분석은 필요하지 않음

## BLOCKED
- SLTE target branch/root 불명확
- feature probe 결과가 없음
- 기존 manifest가 현재 baseline과 불일치하며 대체 evidence도 없음
- code-analyzer 보강 및 승인 Knowledge 조회 후에도 usable candidate를 얻지 못함
- Target Requirement 작성에 필요한 필수 `USER_INPUT_REQUIRED` 항목이 남음

후보가 없다고 즉시 `MISSING`으로 판정하지 않는다.



# 29. 다음 단계

Phase 1~2 완료 후에만 다음 흐름으로 진행한다.

```text
Phase 3
Legacy Behavior
 + Code Evidence
 + MSC Evidence
        ↕
SLTE Candidate
        ↓
Behavior Mapping
        ↓
EQUIVALENT
PARTIAL
MISSING
ARCH_CONFLICT
NEEDS_DECISION

Phase 4
Target SLTE CL-AIT HLD

Phase 5
Implementation

Phase 6
Verification
```

Legacy HLD는 새로 만들지 않는다.

HLD는 **SLTE Target Architecture가 결정된 이후에 Target HLD로 작성**한다.

---

# 30. Knowledge Manager 사용 원칙

Knowledge Manager는 이번 워크플로우에서 **두 가지 역할을 명확히 분리**한다.

## Phase 1
Legacy 구현 구조를 승인 지식으로 등록하지 않는다.

다음은 자동 등록 대상이 아니다.

```text
Legacy class name
Legacy file path
Legacy function name
Legacy timer implementation
```

## Phase 2
`l1-knowledge-manager`는 **read-only 보강 도구**로 사용한다.

조회 우선 대상:

```text
approved responsibility
ownership scope
approved interface/state/policy
known component mapping/replacement
approved L1/SLTE domain knowledge
```

다음은 금지한다.

```text
- Phase 2 중 자동 Candidate 생성
- 자동 승인
- 현재 코드와 다르다는 이유만으로 Knowledge 수정
- Candidate-only 지식을 confirmed fact로 사용
```

현재 코드와 승인 지식의 불일치는 `code_knowledge_conflicts.md`에 남긴다.

## 향후 Phase 3~4 이후
사용자 검토와 설계 결정이 끝난 뒤에만 아래처럼 안정적인 항목을 Knowledge candidate로 고려한다.

```text
Behavior invariant
Architecture responsibility
Confirmed interface rule
State/policy rule
Validated exception behavior
```



# 31. 저사양 OpenCode 실행 원칙

1. 기존 analyzer output을 우선 재사용
2. MSC 전체를 반복적으로 LLM context에 넣지 않음
3. Python 기반 inventory/correlation 결과를 우선 사용
4. manifest 우선 재사용
5. `FEATURE_SCOPE_PROBE` 사용
6. Phase 2 부족 항목을 먼저 triage
7. 코드 Fact 부족은 `code-analyzer`로 bounded 확인
8. 승인 지식 부족은 `l1-knowledge-manager` read-only 조회
9. Knowledge 조회로 code runtime fact를 대체하지 않음
10. candidate 파일만 직접 확인
11. Evidence packet을 작게 유지
12. UNKNOWN을 추론으로 채우지 않음
13. MSC↔Code 및 Code↔Knowledge conflict를 자동 해결하지 않음
14. 사용자 질문은 `USER_INPUT_REQUIRED`에 한정
15. 설계 선택 문제는 `DECISION_REQUIRED`로 Phase 3에 전달


# 32. 완료 조건

- [ ] Legacy code-analyzer 결과 위치 확인
- [ ] Legacy provenance 기록
- [ ] 기존 CL-AIT MSC 목록 작성
- [ ] MSC별 scenario/coverage 기록
- [ ] MSC ↔ Code correlation 수행
- [ ] Legacy CL-AIT Behavior Inventory 생성
- [ ] Code/MSC/Inference Evidence 구분
- [ ] CONFLICT/UNKNOWN 별도 관리
- [ ] 현재 SLTE root/branch 확인
- [ ] 기존 SLTE manifest 재사용 가능 여부 확인
- [ ] FEATURE_SCOPE_PROBE 수행
- [ ] SLTE candidate 목록 생성
- [ ] candidate별 Evidence 기록
- [ ] PARTIAL/BLOCKED이면 missing evidence triage 수행
- [ ] 필요한 코드 Fact는 code-analyzer로 제한 보강
- [ ] 필요한 승인 지식은 l1-knowledge-manager read-only 조회
- [ ] Code↔Knowledge conflict 별도 기록
- [ ] USER_INPUT_REQUIRED와 DECISION_REQUIRED 분리
- [ ] Phase 1 Gate 판정
- [ ] Phase 2 Gate 판정
- [ ] `phase01_02_summary.md` 생성
- [ ] HLD/코드 수정 없이 STOP

---

# 33. OpenCode에서 한 번에 실행하는 요청문

```text
Legacy CL-AIT 분석 정보를 이용해서 현재 SLTE 기준 CL-AIT 리팩토링을 준비하려고 한다.

현재 상황:
- Legacy CL-AIT 완성 HLD는 없다.
- 기존 code-analyzer 분석 결과가 있다.
- Legacy CL-AIT 동작을 설명하는 일부 MSC가 있다.
- 필요하면 Legacy source를 제한적으로 확인할 수 있다.

목표:
Legacy 구조를 그대로 SLTE에 복사하지 않고,
기존 code-analyzer 결과와 MSC를 이용해 Legacy CL-AIT Behavior Baseline을 복원한 뒤
현재 SLTE에서 대응 가능한 코드 scope를 찾는다.

이번 실행에서는 Phase 1~2까지만 수행한다.

[Phase 1 — Legacy Behavior Baseline]

1. Legacy code-analyzer output과 code_analysis_manifest.json을 우선 탐색한다.
2. Legacy HLD는 없는 것으로 처리하고 찾기 위해 불필요한 시간을 쓰지 않는다.
3. 제공된 기존 CL-AIT MSC를 inventory한다.
4. MSC별 scenario, actor/module, entry event, call sequence, message, callback, timer, state change, result를 가능한 범위에서 추출한다.
5. 각 MSC step을 기존 code-analyzer 결과와 correlation한다.
6. Correlation 상태는 MATCHED / PARTIALLY_MATCHED / CODE_ONLY / MSC_ONLY / CONFLICT / UNKNOWN으로 구분한다.
7. Code와 MSC가 충돌하면 자동으로 하나를 삭제하거나 맞추지 않는다.
8. 실제 코드 근거가 있는 경우 Code Fact를 우선하고 MSC 차이는 legacy_conflicts.md에 남긴다.
9. CL-AIT를 Trigger, Scheduling, State Gate, OL/CL Arbitration, Event Handling, Decision, Data Build, HAL/RF/PHY Send, Context Update, Stop/Restart, Exception, Isolation Behavior로 정규화한다.
10. 각 Behavior에 CODE_ANALYZER / MSC / SOURCE / INFERENCE Evidence 종류를 기록한다.
11. MSC_ONLY 항목을 CONFIRMED로 자동 승격하지 않는다.
12. 부족한 정보는 UNKNOWN으로 유지한다.
13. Legacy class/function/module 구조를 Target SLTE Architecture로 가정하지 않는다.
14. Phase 1 결과를 READY / PARTIAL / BLOCKED로 판정한다.

[Phase 2 — Current SLTE Scope]

1. 제공된 SLTE code root/branch를 기준점으로 사용한다.
2. 기존 code_analysis_manifest.json이 현재 branch에 유효하면 우선 재사용한다.
3. 전체 code-analyzer 재분석을 기본으로 하지 않는다.
4. Phase 1에서 확보한 feature name, symbol, API, state, timer, message, HAL/RF interface, caller/callee와 MSC actor 이름을 검색 anchor로 활용한다.
5. code-analyzer FEATURE_SCOPE_PROBE를 사용해 CL-AIT 관련 candidate만 좁힌다.
6. manifest가 없으면 bounded source scan을 사용한다.
7. Legacy와 동일한 class/module 이름이 없더라도 MISSING으로 판단하지 않는다.
8. renamed/commonized/restructured 가능성을 고려해서 module/file/API/state/timer/interface 후보를 찾는다.
9. candidate별 path/symbol/evidence/source/legacy_anchor/confidence를 기록한다.
10. Phase 2 결과를 READY / PARTIAL / BLOCKED로 판정한다.
11. PARTIAL/BLOCKED이면 부족 Evidence를 AUTO_CODE_CHECK / AUTO_KNOWLEDGE_LOOKUP / USER_INPUT_REQUIRED / DECISION_REQUIRED로 분류한다.
12. AUTO_CODE_CHECK는 code-analyzer로 필요한 candidate 주변만 제한 확인한다.
13. AUTO_KNOWLEDGE_LOOKUP은 l1-knowledge-manager의 승인 지식을 read-only로 조회한다.
14. Knowledge Manager 조회 중 Candidate 생성/승인은 하지 않는다.
15. code-analyzer 현재 Fact와 승인 Knowledge가 충돌하면 CODE_KNOWLEDGE_CONFLICT로 별도 기록하고 자동으로 하나를 정답 처리하지 않는다.
16. USER_INPUT_REQUIRED만 사용자에게 요청한다.
17. DECISION_REQUIRED는 Target Requirement 단계의 Open Decision으로 넘길 수 있으면 Phase 2 blocker로 만들지 않는다.

[중요]

이번 실행에서는:
- Legacy HLD를 만들지 않는다.
- Target SLTE HLD를 만들지 않는다.
- Legacy↔SLTE 최종 Gap 판정을 하지 않는다.
- EQUIVALENT/PARTIAL/MISSING/ARCH_CONFLICT/NEEDS_DECISION을 최종 확정하지 않는다.
- 코드를 수정하지 않는다.
- commit/push/PR을 하지 않는다.
- Knowledge Manager에 Legacy 구현 구조를 승인 지식으로 저장하지 않는다.

Phase 1~2가 완료되면 phase01_02_summary.md를 생성하고 STOP한다.

[최종 보고]

1. Legacy baseline/provenance
2. Legacy 주요 Code Behavior
3. 기존 MSC 목록과 coverage
4. MSC ↔ Code correlation 결과
5. Code ↔ MSC conflict/unknown
6. SLTE baseline/branch
7. SLTE CL-AIT candidate Top 목록
8. 부족 Evidence triage 결과
9. code-analyzer 보강 결과
10. Knowledge Manager read-only 조회 결과
11. Code↔Knowledge conflict
12. USER_INPUT_REQUIRED / DECISION_REQUIRED
13. Phase 1/2 Gate
14. 다음 단계 진행 가능 여부

Legacy 분석 경로:
<LEGACY_ANALYSIS_PATH>

Legacy MSC 경로:
<LEGACY_MSC_PATH>

현재 SLTE code root/branch:
<SLTE_CODE_ROOT>
```

---

# 34. 핵심 원칙

```text
Legacy Code Analysis = 1차 Fact Source
Legacy MSC           = 동작 Flow 보강 Evidence
Legacy HLD           = 없음 / Phase 1에서 생성하지 않음

        ↓

Legacy Behavior Baseline

        ↓

SLTE Scope Probe

        ↓

비교 가능한 Evidence가 확보되면 STOP
```

**Phase 1의 성공 기준은 Legacy HLD를 만드는 것이 아니라, 기존 코드 분석과 일부 MSC를 서로 교차검증하여 SLTE와 비교 가능한 Behavior Evidence를 만드는 것이다.**

---

# 35. 구현 반영 — hld-code-compare v0.10.16

본 워크플로우의 Phase 1~2는 `hld-code-compare v0.10.16`의 아래 action으로 실행한다.

```text
legacy-refactor-prepare
```

기존 `legacy-feature-port-prepare`는 Old HLD가 존재하는 기존 use case 전용으로 유지한다.

자연어 요청은 `route`를 통해 `legacy-refactor-prepare`로 결정형 routing된다.

```text
Legacy CL-AIT 분석 결과와 기존 MSC를 이용해서
현재 SLTE 리팩토링 준비를 Phase 1~2까지만 해줘.
```

직접 action 계약:

```text
skillsilent run hld-code-compare legacy-refactor-prepare -- \
  --branch-root <SLTE_CODE_ROOT> \
  --feature cl_ait \
  --legacy-analysis-root <LEGACY_ANALYSIS_PATH> \
  --msc <LEGACY_MSC_1> \
  --msc <LEGACY_MSC_2> \
  --code-analysis-manifest <SLTE_MANIFEST_IF_AVAILABLE> \
  --json
```

Legacy source 직접 확인이 필요한 경우에만 추가한다.

```text
--legacy-source-root <LEGACY_SOURCE_ROOT>
```

종료 계약:

```text
STOP_AFTER_PHASE_1_2_NO_GAP_NO_HLD_NO_CODE_MUTATION
```

따라서 이 action의 정상 완료 후에도 Gap classification, Target HLD 작성, 코드 수정은 자동으로 이어지지 않는다.


---

# 36. v4 운영 주의 — 자동화 경계

현재 `hld-code-compare v0.10.16`의 `legacy-refactor-prepare`는 Phase 1 및 `code-analyzer FEATURE_SCOPE_PROBE` 기반 Phase 2 준비를 자동화하는 경로다.

본 v4에서 추가한 **Phase 2 부족 Evidence의 Knowledge Manager 보강**은 다음 운영 계약을 따른다.

```text
legacy-refactor-prepare
        ↓
Phase 2 Gate
        ↓
READY → STOP
PARTIAL/BLOCKED
        ↓
missing evidence triage
        ├─ AUTO_CODE_CHECK
        │      → code-analyzer
        ├─ AUTO_KNOWLEDGE_LOOKUP
        │      → l1-knowledge-manager read-only
        ├─ USER_INPUT_REQUIRED
        │      → 사용자 최소 입력 요청
        └─ DECISION_REQUIRED
               → Phase 3 Open Decision
```

향후 이 보강 흐름을 완전 무인화하려면 `hld-code-compare` top-level action이 위 child-skill 호출을 소유하도록 구현하는 것이 바람직하다. 저사양 모델이 임의로 여러 child command를 조합하는 구조로 만들지 않는다.
