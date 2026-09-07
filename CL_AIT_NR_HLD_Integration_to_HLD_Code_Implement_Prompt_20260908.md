# CL-AIT NR HLD Integration → Gap Refresh → Code Implement Prompt
## 사내 LLM 실행용 / HLD 통합 허용 최종 버전

- 작성일: 2026-09-08
- 대상: 사내 LLM / Windows 개발환경
- 현재 범위: **NR CL-AIT 구현**
- 이후 계획: NR 구현 완료 후 NR As-Built를 기준으로 NR/LTE Gap을 작성하여 LTE 구현
- 사용 스킬:
  - HLD 통합/Revision: 기존 HLD Composer workflow 사용 가능
  - Gap 재생성/검증: `hld-code-compare`
  - 코드 구현: `hld-code-implement`
- 사용하지 않음:
  - `code-fix`
  - LTE 코드 구현
  - 확정되지 않은 Architecture 신규 창작

---

# 0. 현재 상태

다음 상태가 이미 준비되어 있다고 가정한다.

```text
NR Target HLD 존재
NR Gap 문서 존재
NR gap_report.yaml 존재
LTE Legacy 분석 완료
CL-AIT Consolidated Decision 문서 존재
```

현재 구현 전에 추가로 필요한 작업은:

```text
Class Naming 확정
        ↓
기존 HLD UPDATE LOCK 해제
        ↓
확정 Decision / Code Fact / Naming을 HLD에 통합
        ↓
HLD 내부 정합성 검증
        ↓
hld-code-compare 재실행
        ↓
gap_report.yaml 재생성/갱신
        ↓
hld-code-implement
```

---

# 1. Authoritative Design Sources

설계 판단 우선순위는 다음과 같다.

## Priority 1

```text
CL_AIT_SLTE_Design_Review_Consolidated_20260906.md
```

Target Architecture 및 Runtime Decision의 최상위 기준이다.

## Priority 2

```text
CL_AIT_DECISION_LEDGER_v1_1.md
```

존재하는 경우 Consolidated MD와 정합되는 최신 Decision Ledger로 사용한다.

## Priority 3

```text
CL_AIT_Basic_Runtime_Concept_Detail_KR_20260906.md
```

Legacy runtime / timing concept 근거로 사용한다.

## Priority 4

```text
현재 NR Target HLD
```

기존 구조를 최대한 재사용하되 상위 Decision과 충돌하는 경우 갱신한다.

## Priority 5

```text
기존 gap_report.yaml
```

현재 구현 gap의 출발점으로 사용한다.
단, HLD 통합 후에는 반드시 compare를 다시 수행하여 새 report로 갱신한다.

---

# 2. 기존 HLD UPDATE LOCK 해제

이전 단계에서 HLD를 변경하지 않도록 막아둔 정책은 **현재 단계에서 해제한다.**

이유:

```text
기존 HLD
→ 이전 Architecture 전제 포함 가능
→ 이후 Decision / Code Fact / Naming이 추가 확정됨
→ 구현 전에 HLD 통합 필요
```

따라서 현재부터는 다음 목적의 HLD 수정은 허용한다.

```text
CONFIRMED Decision 반영
CONFIRMED Code Fact 반영
Class Naming 반영
MSC/Class/API/Traceability 정합화
기존 잘못된 Architecture 전제 제거
```

단, 다음은 허용하지 않는다.

```text
근거 없는 신규 Architecture 추가
Legacy behavior 임의 변경
사용자 확정 없이 class ownership 변경
LTE 미확인 behavior를 NR/LTE 공통으로 추정
구현 편의를 위한 HLD 의미 변경
```

즉 이번 HLD 수정은:

```text
Controlled HLD Revision
```

으로 취급한다.

---

# 3. Class Naming Gate — 반드시 먼저 사용자에게 질문

코드 구현 전에 사용자에게 아래 질문을 한 번 수행한다.

```text
[CL-AIT NR Class Naming Gate]

현재 HLD class:
- ClAitProcNr

변경 제안:
- RfClAitProcNr

기본 반영 조건:
- Ownership: HAL 유지
- Responsibility: 변경 없음
- Runtime behavior: 변경 없음
- API semantics: 변경 없음
- 기존 HAL 파일 ownership 우선 유지
- LTE 구현은 이번 단계에서 제외

선택:
A. RfClAitProcNr로 확정
B. 다른 클래스명 사용
C. 클래스명과 파일명 모두 변경
```

사용자가:

```text
A
확정
진행
RfClAitProcNr
```

등 의미상 동일한 응답을 하면:

```text
CLASS_NAMING_CONFIRMED
target_class = RfClAitProcNr
change_type = RENAME_ONLY
```

로 처리한다.

---

# 4. Naming Change Classification

## RENAME_ONLY

다음이 모두 유지되는 경우:

```text
HAL ownership
class responsibility
runtime sequence
public API semantics
state semantics
RF/PHY/HAL responsibility boundary
```

판정:

```text
RENAME_ONLY
```

Architecture 재분석은 하지 않는다.

## ARCH_CHANGE

다음 중 하나라도 바뀌는 경우에만:

```text
class split/merge
ownership 변경
responsibility 변경
runtime flow 변경
interface semantics 변경
```

판정:

```text
ARCH_CHANGE
```

이 경우 구현으로 바로 가지 않고 HLD를 먼저 수정한 뒤 compare를 다시 수행한다.

현재 기본 기대:

```text
RfClAitProcNr = RENAME_ONLY
```

---

# 5. HLD Integration Gate

Class Naming이 확정되면 기존 NR HLD를 **통합 Revision**한다.

목표는 새 HLD를 처음부터 다시 작성하는 것이 아니라:

```text
Existing NR HLD
        +
Consolidated Decision
        +
Decision Ledger
        +
Confirmed Code Fact
        +
Confirmed Class Naming
        ↓
Integrated NR HLD Revision
```

이다.

---

# 6. HLD에서 반드시 통합/갱신할 항목

## 6.1 Architecture

Target:

```text
TxCfgMngrNr
        ↓
Existing TX_ONOFF_NR_CMD
        ↓
HAL
        ↓
RfClAitProcNr
        ↓
Shared Memory / PHY
        ↓
RF Driver / FBRX
```

다음 기존 전제는 제거한다.

```text
L1C ClAitMngr
ClAitConfigBuilder
L1C CL-AIT runtime ownership
```

---

## 6.2 Class / File Ownership

Class:

```text
RfClAitProcNr
```

Ownership:

```text
HAL
```

파일은 현재 검증된 HAL 파일 구성을 우선 유지한다.

예:

```text
ch_HalAitProcNr.hpp
ch_HalAitProcNr.cpp
```

단, 실제 현재 HLD/코드의 검증된 filename이 다르면 실제 값을 사용한다.

---

## 6.3 NR Update API

Target API:

```cpp
RfClAitProcNr::UpdateClAitOperationInfo(isScg, domainType);
```

---

## 6.4 TX ON Sequence

HLD와 MSC에 다음 순서를 명확히 반영한다.

```text
TX_ONOFF_NR_CMD
        ↓
RF TX ON
        ↓
RF TX ON Success
        ↓
RfClAitProcNr::UpdateClAitOperationInfo(isScg, domainType)
        ↓
Shared Memory
 - Enable
 - TxPwrThreshold
 - Period
        ↓
TX_SWAP_REQ
```

순서를 임의 변경하지 않는다.

---

## 6.5 Eligibility

```text
isScg = false
→ NR SA
→ CL-AIT Eligible

isScg = true
→ ENDC NR SCG
→ CL-AIT Not Eligible
```

---

## 6.6 Shared Memory

Logical fields:

```text
Enable
TxPwrThreshold
Period
```

값은 RAT Type 기반 RF Driver API에서 제공한다.

NR은 `isScg` eligibility를 최종 Enable에 적용한다.

---

## 6.7 Period

Target:

```text
single logical period
```

Legacy:

```text
period1
period2
```

가 실제로 같은 값을 사용하던 구조를 Target에서는 이중 representation으로 유지하지 않는다.

---

## 6.8 NR Runtime

필수 MSC:

```text
CL_AIT_DUMP_IND
        ↓
TX Path ON check
        ↓
clait_enable check
        ↓
CL_AIT_START_REQ
        ↓
CL_AIT_START_CNF
        ↓
fail 시 retry 1회
        ↓
PAL Timer
        ↓
PAL Timer expiry
        ↓
RF Driver AIT_Dump()
        ↓
Current Period END
```

---

## 6.9 Failure / Skip

HLD에 다음을 명시한다.

```text
TX Path OFF
→ Current Period Skip

clait_enable = false
→ Current Period Skip

START_CNF false
→ START_REQ/CNF retry 1회

두 번째 START_CNF false
→ Current Period Skip

AIT_Dump() == false
→ Current Period End
→ no retry
```

---

## 6.10 Period-local Transaction

```text
Period N
→ 독립 CL-AIT transaction
→ END

Period N+1
→ New Independent Transaction
```

다음 state는 carry하지 않는다.

```text
retry count
START_CNF failure
AIT_Dump failure
previous dump state
```

---

## 6.11 PAL Timer

Target HLD 원칙:

```text
Legacy PAL Timer timing semantics 그대로 차용
```

새 timing algorithm을 설계하지 않는다.

Exact API / field / formula는 Code Fact로 확인된 것만 HLD에 반영한다.

---

## 6.12 Legacy Complex FSM

다음 구조는 Target에 그대로 복사하지 않는다.

```text
ENDC SCG NR 목적용 CL-AIT
period1 / period2 기반 dual flow
이에 종속된 complex FSM
```

Target은 필요한 최소 event-driven runtime만 유지한다.

---

# 7. HLD Section 정합화

Class 이름만 바꾸고 일부 Section을 놓치지 않도록 최소 아래 영역을 모두 확인한다.

```text
Architecture Diagram
Class Diagram
Module Responsibility
Sequence Diagram
MSC
Interface
API
Data Structure
State/Runtime Context
Constraints
Error Handling
Traceability
Implementation Target
Gap Mapping
Verification Point
```

기존:

```text
ClAitProcNr
```

reference가 남아 있으면 각각 의미를 확인한다.

단순 과거 설명/비교 문맥이 아니라 Target reference이면:

```text
RfClAitProcNr
```

로 갱신한다.

---

# 8. HLD Internal Consistency Check

HLD 통합 후 아래 항목을 검사한다.

## Naming

```text
Target class naming mismatch = 0
```

## Architecture

```text
L1C ClAitMngr target reference = 0
ClAitConfigBuilder target reference = 0
```

## Runtime

```text
TX ON ordering mismatch = 0
START_REQ/CNF 누락 = 0
retry 1회 누락 = 0
TX Path Guard 누락 = 0
single period 원칙 누락 = 0
```

## LTE Leakage

```text
LTE implementation content mixed into NR HLD = 0
```

---

# 9. HLD Integration 결과 판정

## PASS

다음 조건:

```text
Naming synchronized
Architecture synchronized
MSC synchronized
Interface synchronized
Traceability synchronized
No unresolved Architecture change
```

이면:

```text
HLD_INTEGRATION_PASS
```

## PARTIAL

Exact Code Fact만 남아 있는 경우:

```text
HLD_INTEGRATION_PASS_WITH_CODE_FACT_REQUIRED
```

로 처리하고 compare 단계로 계속 진행한다.

## FAIL

다음이면 구현으로 가지 않는다.

```text
Architecture contradiction
wrong HLD selected
wrong branch
class responsibility conflict
unresolved architecture change
```

---

# 10. gap_report.yaml 직접 수정 금지

중요:

```text
기존 gap_report.yaml을 LLM/text editor로 직접 수정하지 않는다.
```

이유:

```text
HLD가 변경됨
→ compare input 변경
→ 기존 gap_report의 hld_ref/target/symbol/confidence가 stale 가능
```

따라서 반드시:

```text
Integrated HLD
        ↓
hld-code-compare 재실행
        ↓
새 gap_report.yaml
```

로 갱신한다.

---

# 11. hld-code-compare 재실행 목적

전체 설계를 처음부터 재분석하는 것이 목적이 아니다.

목표:

```text
RfClAitProcNr naming 반영
최신 HLD reference 반영
기존 Gap 유지 여부 확인
target symbol/file 정합화
stale gap 제거
duplicate gap 제거
implementability 재검증
```

---

# 12. 새 gap_report.yaml 검증

최소 확인:

```text
Target class == RfClAitProcNr
HLD reference == 최신 Integrated HLD
Code reference == 현재 NR branch code
Implementable code Gap 존재
Wrong LTE target 없음
Duplicate Gap 없음
Stale ClAitProcNr target 없음
```

또한:

```text
implement_allowed
fact_status
confidence
code_ref
hld_ref
```

를 확인한다.

---

# 13. Compare 결과에 따른 처리

## PASS

```text
Gap report valid
Implementable NR Gap 존재
No Architecture blocker
```

이면:

```text
GAP_REFRESH_PASS
```

후 implement로 진행한다.

## Code Fact 부족

```text
CODE_FACT_REQUIRED
```

가 남아 있어도 해당 Gap의 implementation이 허용되는지 report policy를 따른다.

근거 없이 `implement_allowed=true`로 바꾸지 않는다.

## Architecture mismatch

Architecture 의미 변경이 발견되면 구현 전에 HLD로 되돌아간다.

---

# 14. hld-code-implement 연결

Gap Refresh PASS 후 반드시:

```text
hld-code-implement
```

를 사용한다.

`code-fix`는 사용하지 않는다.

권장 호출 경로:

```text
skillsilent run hld-code-implement <action> -- <args>
```

직접 helper script를 우회 호출하지 않는다.

---

# 15. Implement Input

입력 SSOT:

```text
Integrated NR HLD
+
new gap_report.yaml
```

구현 대상은:

```text
NR CL-AIT
RfClAitProcNr
```

로 제한한다.

---

# 16. Implement Candidate 확인

먼저 최신 report를 discover하고 candidate를 확인한다.

논리적 절차:

```text
discover
        ↓
candidates
```

확인할 항목:

```text
GAP ID
target files
target symbols
planned change
implement_allowed
fact_status
```

LTE Gap은 제외한다.

---

# 17. G1 — Write Approval

Class Naming 승인과 코드 Write 승인은 별개다.

`hld-code-implement`가 계산한 실제 write scope를 사용자에게 보여준다.

형식:

```text
[NR CL-AIT Implementation G1]

Target Class
- RfClAitProcNr

HLD
- <path>

Gap Report
- <path>

Selected GAP
- GAP-...

Files
- ...

Symbols
- ...

Planned Changes
- ...

Out of Scope
- LTE implementation
- unrelated refactoring
- code-fix
- Architecture redesign

선택:
A. 승인하고 구현
B. 범위 수정
C. 중단
```

사용자 승인 후에만 write한다.

---

# 18. NR Implementation

G1 승인 후 `hld-code-implement`의 정상 workflow를 따른다.

```text
prepare-run
→ G1 scope
→ G1 승인
→ seal-run
→ start-gap
→ code write
→ build / UT
→ finalize-gap-review
→ G2 diff review
→ 사용자 G2 승인
→ finalize-gap --approve
→ next gap if needed
→ finalize-run
```

---

# 19. 구현 중 보존해야 할 핵심 Behavior

## TX ON

```text
RF TX ON Success
→ RfClAitProcNr::UpdateClAitOperationInfo(isScg, domainType)
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
→ Period End
```

## No Carry

```text
previous retry/failure state
→ next period로 carry 금지
```

## No New FSM

```text
Legacy complex FSM 재도입 금지
```

---

# 20. Build / UT

기존 project의 검증 방법을 재사용한다.

임의 build command를 새로 만들지 않는다.

최소:

```text
compile/build
existing UT
CL-AIT related UT
header/source linkage
changed-symbol compile consistency
```

---

# 21. G2 Review

각 Gap 구현 후 실제 diff로 확인한다.

```text
RfClAitProcNr naming 일치
HLD와 implementation 일치
Gap scope 밖 수정 없음
LTE source 수정 없음
Legacy runtime semantic 보존
Build/UT 결과
```

사용자 G2 승인 전 완료 처리하지 않는다.

---

# 22. LTE는 이번 Run에서 제외

LTE Legacy 분석이 이미 완료되어 있어도 이번 실행에서는:

```text
RfClAitProcLte 구현 금지
LTE source 변경 금지
NR code를 LTE로 자동 port 금지
```

NR 구현 완료 후 별도 단계:

```text
NR As-Built
        +
LTE Legacy Analysis
        ↓
NR/LTE Gap
        ↓
LTE Target HLD
        ↓
LTE gap_report.yaml
        ↓
LTE hld-code-implement
```

로 수행한다.

---

# 23. NR As-Built 확보

NR 구현 완료 후 다음 단계의 LTE Gap 기준으로 사용할 수 있도록 기록한다.

최소:

```text
실제 class/file
실제 API
실제 runtime call flow
실제 member/context
실제 PAL Timer integration
실제 PHY IPC integration
실제 RF Driver integration
HLD 대비 deviation
```

이 결과를:

```text
NR As-Built
```

로 관리한다.

---

# 24. 최종 종료 조건

이번 프롬프트의 종료점은:

```text
Class Naming Confirmed
        ↓
HLD Update Lock 해제
        ↓
Integrated NR HLD Revision
        ↓
HLD Consistency PASS
        ↓
hld-code-compare
        ↓
new gap_report.yaml
        ↓
Gap Refresh PASS
        ↓
hld-code-implement
        ↓
G1
        ↓
NR implementation
        ↓
Build/UT
        ↓
G2
        ↓
NR Implementation Finalized
        ↓
STOP
```

LTE 구현으로 자동 진행하지 않는다.

---

# 25. 최종 보고 형식

```text
[CL-AIT NR HLD Integration / Implementation Status]

1. Class Naming
- Before: ClAitProcNr
- After: RfClAitProcNr
- Type: RENAME_ONLY / ARCH_CHANGE

2. HLD Update Lock
- RELEASED / NOT_RELEASED

3. HLD Integration
- PASS / PASS_WITH_CODE_FACT_REQUIRED / FAIL
- HLD path:

4. Major Integrated Items
- HAL ownership:
- TX ON ordering:
- START_REQ/CNF:
- Retry:
- TX Path Guard:
- Single Period:
- PAL Timer:
- Legacy FSM simplification:

5. HLD Consistency
- PASS / FAIL

6. Gap Refresh
- hld-code-compare: PASS / FAIL
- new gap_report.yaml:
- stale gap removed:
- duplicate gap:

7. Implement Candidate
- GAP IDs:
- target files:
- target symbols:

8. G1
- APPROVED / WAITING / BLOCKED

9. Implementation
- NOT_STARTED / IN_PROGRESS / COMPLETE

10. Build
- PASS / FAIL / NOT_RUN

11. UT
- PASS / FAIL / NOT_RUN

12. G2
- APPROVED / WAITING / BLOCKED

13. LTE Modified
- NO

14. NR As-Built
- READY / NOT_READY

15. Next
- <single next action>
```

---

# 핵심 원칙

> **현재 단계에서는 기존 HLD update lock을 해제하고, 사용자가 확정한 `RfClAitProcNr` naming과 이미 확정된 CL-AIT Decision/Code Fact를 기존 NR HLD에 통합한다. 통합된 HLD를 기준으로 `hld-code-compare`를 다시 실행하여 `gap_report.yaml`을 재생성/정합화한 뒤, 그 report만을 입력으로 `hld-code-implement`의 G1/G2 절차를 통해 NR 구현을 진행한다. 기존 `gap_report.yaml`을 직접 수정하거나 `code-fix`를 사용하지 않는다.**
