# CL-AIT NR/LTE 통합 후속 작업 프롬프트
**Target:** NR Architecture Remediation → NR Scenario UT Revalidation → LTE As-Built Review → LTE Scenario UT → Integrated HLD Alignment  
**Recommended skill:** `cl-ait-dev-orchestrator v0.1.8`  
**Environment constraint:** CL-AIT Build / Runtime UT 환경 없음  
**Important:** SkillSilent 사용 금지

---

# 0. 현재 상태

현재 상태는 다음과 같다.

```text
NR:
- 코드 구현 완료
- Scenario UT 존재
- 그러나 production .cpp/.hpp에서 Mock*.hpp include 등
  test dependency contamination 가능성이 확인됨
- 따라서 architecture remediation 필요

LTE:
- 코드 구현 완료
- 이후 As-Built 검증 + Scenario UT 작성 필요

공통:
- Build 환경 없음
- Runtime UT 환경 없음
- SkillSilent 사용 금지
```

이번 작업은 코드를 처음부터 다시 구현하는 작업이 아니다.

전체 목표:

```text
NR mock/test contamination 정리
→ NR Scenario UT 재검증
→ NR Architecture Gate PASS
→ LTE As-Built 코드 검증
→ LTE Existing UT Reference First
→ LTE HLD-derived Scenario 도출
→ LTE Scenario UT 작성
→ LTE Architecture Gate PASS
→ NR/LTE 잔여 Gap 정리
→ LTE As-Built HLD 갱신 준비
→ NR/LTE Integrated HLD 갱신 준비
→ 최종 보고
```

Build/Runtime UT는 실행하지 않는다.

```text
Build      = NOT EXECUTED
Runtime UT = NOT EXECUTED
```

---

# 1. 사용자 질문 규칙

사용자 판단이 필요한 경우 자유서술형 질문을 하지 않는다.

반드시 객관식으로 질문한다.

예:

```text
Production test seam이 필요합니다.

1. 기존 UT/seam을 더 탐색
2. 최소 adapter seam 추가 승인
3. 최소 interface/function seam 추가 승인
4. 해당 Scenario를 BLOCKED 처리

번호로 답해주세요.
```

Yes/No도 다음처럼 번호로 묻는다.

```text
1. 예
2. 아니오
```

사용자의 명시적 승인 없이 production architecture를 변경하지 않는다.

---

# 2. 절대 원칙

금지:

```text
- SkillSilent 사용
- Git commit/push
- P4 shelve/submit
- Build 실행
- Runtime UT 실행
- production 코드에 Mock/Test dependency 신규 추가
- #ifdef UNIT_TEST로 real/mock 선택
- IsUnitTest()/IsMockMode()/MockMode 같은 test-only production branch
- NR behavior를 LTE에 자동 복사
- LTE HLD에 없는 NR-only semantics 추가
- 근거 없는 Decision Ledger 변경
- 대규모 DI/interface 리팩토링 자동 수행
```

허용/우선:

```text
- READ-ONLY code/history/UT 탐색
- 기존 production seam 재사용
- 기존 UT architecture 재사용
- 기존 UT 확장 우선
- 최소 변경
- 사용자 승인 후 최소 seam 추가
```

SSOT 우선순위:

```text
1. 확정 Decision Ledger
2. RAT별 Target HLD
3. HLD-Code Compare / Gap artifact
4. 실제 As-Built code
5. 기존 관련 UT
```

문서와 코드가 다르면 다음 중 하나로 분류한다.

```text
DESIGN_GAP
IMPLEMENTATION_GAP
DOCUMENTATION_GAP
TEST_ARCHITECTURE_GAP
```

---

# 3. PHASE A — 전체 Context READ-ONLY 복구

먼저 다음을 확인한다.

```text
- project/source root
- current branch/worktree
- modified production files
- modified/added UT files
- NR Target/As-Built HLD
- LTE Target HLD
- Decision Ledger
- NR/LTE Gap/Compare artifact
- persisted orchestrator state
- Scenario UT state
```

Git/P4는 상태 확인에만 사용한다.

예:

```text
git status
git diff --name-only
git diff
p4 opened
```

write 작업 금지.

결과:

```text
CL_AIT_CURRENT_CONTEXT
```

---

# 4. PHASE B — NR Architecture Remediation

## 4.1 NR production contamination 탐색

현재 NR 변경 production diff를 대상으로 다음을 검사한다.

금지 패턴:

```text
#include "Mock*.hpp"
#include ".../mock/..."
#include ".../test/..."
gmock/gtest dependency
#ifdef UNIT_TEST
IsUnitTest()
IsMockMode()
MockMode
test-only runtime branch
```

이번 변경에서 새로 유입된 것과 기존 legacy code에 있던 것을 구분한다.

결과:

```text
NR_PRODUCTION_ARCHITECTURE_SCAN
```

각 finding:

```text
file
line/function
pattern
introduced_by_current_change = YES/NO
dependency being mocked
reason it was introduced
```

## 4.2 Mock include를 단순 삭제하지 말 것

Mock*.hpp include가 있으면 먼저:

```text
왜 production code가 mock symbol을 알아야 했는가?
```

를 분석한다.

다음 순서로 해결한다.

```text
1. 대상 class의 기존 UT 탐색
2. 같은 module의 UT 탐색
3. 동일 RF/PHY/HAL dependency UT 탐색
4. 기존 production seam/interface/adapter 탐색
5. 기존 seam이 있으면 재사용
6. 그래도 불가능할 때만 최소 seam 검토
```

## 4.3 Existing UT Reference First — NR

우선순위:

```text
1. 대상 NR class/function 기존 UT
2. 같은 NR module/package UT
3. 동일 dependency 사용 UT
4. 동일 manager/singleton 구조 UT
5. 유사 LTE UT
6. 신규 test architecture는 마지막
```

각 reference에서 추출:

```text
fixture
setup/teardown
helper
mock/fake injection
existing seam
expectation style
assertion style
test file placement
```

결과:

```text
NR_EXISTING_UT_REFERENCE_EVIDENCE
```

## 4.4 NR 수정 전략

다음 우선순위를 강제한다.

```text
A. 기존 production seam 존재
→ Mock include 제거
→ 기존 seam 재사용

B. 기존 UT에 동일 dependency 처리 방식 존재
→ 해당 패턴 재사용
→ production 변경 최소화

C. 기존 seam 없음
→ 자동 production refactoring 금지
→ 사용자 객관식 승인 필요
```

필요 시:

```text
NR Scenario UT를 유지하려면 production seam이 필요합니다.

1. 기존 UT/seam을 더 탐색
2. 최소 adapter seam 추가
3. 최소 interface/function seam 추가
4. 해당 Scenario를 BLOCKED 처리

번호로 답해주세요.
```

## 4.5 NR Architecture Gate

수정 후 다음 조건을 만족해야 한다.

```text
Production Mock include        = NONE
Production test-dir include    = NONE
UNIT_TEST real/mock branch     = NONE
Test-only runtime branch       = NONE
Existing UT reference evidence = PASS
Existing seam reused           = YES
  또는
New seam                       = USER_APPROVED
```

결과:

```text
NR_ARCHITECTURE_GATE = PASS / FAIL
```

---

# 5. PHASE C — NR Scenario UT 재검증

기존 NR Scenario UT를 다시 확인한다.

중요:

```text
기존 UT가 존재한다는 이유만으로 PASS 처리하지 않는다.
Architecture remediation 이후에도 scenario evidence와
test architecture가 유효한지 다시 확인한다.
```

검증 대상:

```text
scenario_id
test_name
ut_file
production code evidence
reference UT evidence
expected assertion
architecture gate result
```

각 Scenario:

```text
COVERED
BLOCKED
NOT_REQUIRED
```

UNKNOWN 금지.

정책:

```text
DISCOVER_EXISTING_UT_FIRST
→ REUSE_EXISTING_TEST_ARCHITECTURE
→ EXTEND_EXISTING_FIRST
→ NEW_UT_LAST_RESORT
```

결과:

```text
NR_SCENARIO_UT_REVALIDATED
```

완료 조건:

```text
NR Architecture Gate PASS
AND
필수 Scenario coverage 정합
AND
Production Mock/Test contamination 없음
```

---

# 6. PHASE D — LTE As-Built 코드 검증

LTE 코드 구현은 완료된 상태이므로 재구현하지 않는다.

LTE Target HLD와 실제 구현을 비교한다.

각 항목:

```text
MATCH
PARTIAL
MISSING_IN_CODE
EXTRA_IN_CODE
DOC_OUTDATED
NEEDS_DECISION
```

최소 검증:

```text
ownership / class responsibility
init / release lifecycle
enable/disable condition
TX ON/OFF sequence
shared-memory/config update
periodic/event behavior
RF/PHY/HAL interface
race/error handling
retry/skip behavior
LTE-specific eligibility
```

중요:

```text
NR에 있다는 이유만으로
START_REQ/CNF, retry, isScg, TX_SWAP_REQ 등
NR-specific behavior를 LTE requirement로 만들지 않는다.
```

결과:

```text
LTE_AS_BUILT_GAP_MATRIX
```

---

# 7. PHASE E — LTE Production Architecture Scan

LTE production diff에도 NR과 동일 Architecture Gate를 적용한다.

검사:

```text
Mock*.hpp include
mock/test directory include
gmock/gtest production dependency
UNIT_TEST conditional
IsUnitTest/IsMockMode/MockMode
test-only runtime branch
```

신규 문제가 있으면:

```text
LTE_ARCHITECTURE_GATE = FAIL
```

자동 대규모 리팩토링 금지.

기존 seam 우선.

필요 시 사용자 객관식 승인.

---

# 8. PHASE F — Existing UT Reference First — LTE

LTE Scenario UT 작성 전에 반드시 기존 UT를 먼저 탐색한다.

우선순위:

```text
1. 대상 LTE class/function 기존 UT
2. 같은 LTE module/package UT
3. 동일 RF/PHY/HAL dependency UT
4. 동일 manager/singleton 구조 UT
5. 같은 LTE 기능 계열 UT
6. 유사 NR UT
7. 신규 test architecture 설계는 마지막
```

기존 NR UT를 참고할 경우:

재사용 가능:

```text
fixture
helper
mock injection pattern
seam pattern
assertion style
naming convention
```

자동 복사 금지:

```text
isScg
TX_SWAP_REQ
NR-specific START/CNF retry
NR-only RF/PHY path
기타 LTE HLD에 없는 semantics
```

결과:

```text
LTE_EXISTING_UT_REFERENCE_EVIDENCE
```

---

# 9. PHASE G — LTE HLD-derived Scenario 도출

`cl-ait-dev-orchestrator v0.1.8` 정책을 사용한다.

LTE에 NR fixed SCENARIO_CATALOG 사용 금지.

Scenario source:

```text
LTE Target HLD
+ Decision Ledger
+ LTE As-Built implementation
+ LTE As-Built Gap Matrix
```

각 Scenario 필수 필드:

```text
scenario_id
title
HLD reference
HLD evidence
code evidence
precondition
stimulus/event
expected behavior
negative/skip condition
reference UT
```

Scenario 수를 무조건 늘리지 않는다.

실제 requirement를 커버하는 최소 집합 우선.

검토 category:

```text
normal enable/start
disable/ineligible
state transition
event/periodic trigger
error/negative response
TX OFF/release race
duplicate/re-entry
boundary/invalid input
```

단, HLD/Decision/As-Built 근거가 있을 때만 생성.

---

# 10. PHASE H — LTE Scenario UT 구현

정책:

```text
DISCOVER_EXISTING_UT_FIRST
→ REUSE_EXISTING_TEST_ARCHITECTURE
→ EXTEND_EXISTING_FIRST
→ NEW_UT_LAST_RESORT
```

새 UT file을 만들기 전에:

```text
기존 UT를 왜 확장할 수 없는지
```

근거를 남긴다.

각 Scenario UT evidence:

```text
test_name
ut_file
scenario_id
HLD evidence
production code evidence
reference UT evidence
expected assertion
architecture gate result
```

완료 조건:

```text
Scenario coverage recorded
AND
Existing-UT reference evidence recorded
AND
UT code written
AND
LTE Architecture Gate PASS
```

그 전에는:

```text
SCENARIO_UT_CODE_READY
```

처리 금지.

---

# 11. PHASE I — NR/LTE 공통 정적 검증

Build/Runtime UT 대신 가능한 정적 검증 수행.

## NR

```text
production mock/test include 없음
test-only conditional 없음
Scenario mapping 유효
기존 UT convention 준수
approved seam only
```

## LTE

```text
production mock/test include 없음
test-only conditional 없음
LTE HLD-derived scenario 연결
NR semantics leakage 없음
기존 UT convention 준수
approved seam only
```

결과:

```text
NR_ARCHITECTURE_GATE
LTE_ARCHITECTURE_GATE
```

둘 다 PASS 필요.

---

# 12. PHASE J — Decision Ledger / HLD 정합화

## 12.1 Decision Ledger

새로운 설계 결정이 실제로 생긴 경우에만 갱신한다.

단순 code fact는 Decision으로 승격하지 않는다.

필요 시:

```text
NEW_DECISION_REQUIRED
```

로 표시하고 사용자 승인 요청.

## 12.2 NR As-Built HLD

Architecture remediation으로 production dependency 구조가 바뀌었다면
실제 구현 기준으로 반영 필요 여부 확인.

## 12.3 LTE As-Built HLD

actual code + Scenario UT mapping 기준으로 갱신 준비.

포함:

```text
실제 class/function
ownership
call sequence
condition
error/race handling
actual RF/PHY/HAL interaction
Scenario UT mapping
```

## 12.4 NR/LTE Integrated HLD

두 RAT의 공통/차이점을 분리한다.

권장 구조:

```text
Common CL-AIT Runtime Principles
NR-specific Runtime
LTE-specific Runtime
Shared Architecture
RAT-specific IPC/RF/PHY differences
Scenario UT Mapping
Known Build/Runtime Validation Gap
```

결과:

```text
NR_LTE_AS_BUILT_HLD_UPDATE_READY
```

---

# 13. 최종 성공 조건

다음을 모두 만족해야 한다.

```text
1. NR production Mock/Test contamination 제거
2. NR Architecture Gate PASS
3. NR Scenario UT revalidation 완료
4. LTE code ↔ HLD As-Built review 완료
5. LTE Existing UT Reference evidence 확보
6. LTE HLD-derived Scenario 정의 완료
7. LTE Scenario UT 코드 작성 완료
8. LTE Architecture Gate PASS
9. 미해결 implementation blocker 없음
10. NR/LTE As-Built HLD 갱신 evidence 확보
```

Build/Runtime UT 미실행은 실패 사유가 아니다.

최종 권장 reason:

```text
NR_LTE_CODE_REVIEW_AND_SCENARIO_UT_READY
```

---

# 14. 최종 보고 형식

```markdown
# CL-AIT NR/LTE Integrated Post-Implementation Review

## 1. Current State
- NR implementation:
- LTE implementation:
- Source root:
- Modified production files:
- Modified/added UT files:

## 2. NR Architecture Remediation
- Mock/Test contamination found:
- Existing UT references:
- Existing seam reused:
- New seam:
- User approval:
- Architecture Gate:
- Scenario UT revalidation:

## 3. LTE HLD ↔ As-Built
- MATCH:
- PARTIAL:
- MISSING_IN_CODE:
- EXTRA_IN_CODE:
- DOC_OUTDATED:
- NEEDS_DECISION:

## 4. LTE Existing UT References
1. ...
2. ...
3. ...

## 5. LTE Scenario Coverage
| Scenario | HLD Ref | Code Ref | UT | Status |
|---|---|---|---|---|

## 6. Architecture Gates
NR:
- Production Mock include:
- Test-only branch:
- Result:

LTE:
- Production Mock include:
- Test-only branch:
- Result:

## 7. Validation
- NR Scenario UT code:
- LTE Scenario UT code:
- Build: NOT EXECUTED
- Runtime UT: NOT EXECUTED

## 8. Documentation
- Decision Ledger:
- NR As-Built HLD:
- LTE As-Built HLD:
- NR/LTE Integrated HLD:
- Remaining Gap:

## 9. Final State
<PASS / BLOCKED / FAILED>

Reason:
<NR_LTE_CODE_REVIEW_AND_SCENARIO_UT_READY or blocker>

## 10. Next Step
1. NR/LTE As-Built HLD 실제 갱신
2. Integrated HLD 완성
3. Build/Runtime UT 환경 확보 후 검증
4. 다른 작업
```

사용자 판단이 필요한 경우 반드시 번호형 객관식으로만 질문한다.

---

# 핵심 수행 문장

```text
현재 NR/LTE CL-AIT 코드는 모두 구현된 상태다.

먼저 NR에서 이미 발견된 production Mock*.hpp/test dependency 문제를
기존 UT와 기존 seam을 우선 참고해서 최소 변경으로 remediation하고,
NR Scenario UT를 다시 검증해 Architecture Gate를 PASS시켜줘.

그 다음 LTE 구현을 Target HLD/Decision과 As-Built 기준으로 검증하고,
기존 LTE/인접 UT를 먼저 참고해서 LTE HLD-derived Scenario UT를 작성해줘.

NR/LTE 모두 production 코드에 Mock/Test dependency를 새로 넣지 말고,
기존 seam으로 해결되지 않는 경우에만 최소 seam 후보를 제시하고
반드시 1,2,3,4... 객관식으로 사용자 승인을 받아줘.

마지막으로 NR/LTE As-Built HLD와 Integrated HLD 갱신에 필요한 evidence까지 정리해줘.

Build와 Runtime UT는 현재 환경이 없으므로 실행하지 말고
NOT EXECUTED로 기록해줘.

SkillSilent는 사용하지 마.
Git commit/push, P4 shelve/submit도 하지 마.
```
