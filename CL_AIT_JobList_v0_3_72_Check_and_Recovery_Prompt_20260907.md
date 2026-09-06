# CL-AIT Job-list v0.3.72 실행 점검 및 부족분 자동 복구 프롬프트
## 사내 Windows PC / 사내 LLM·OpenCode 실행용

### 목적

사내 Windows PC에서 `job-list v0.3.72`가 CL-AIT HLD 작업을 정상 수행했는지 객관적으로 확인한다.

정상 수행되지 않았거나 일부만 수행된 경우:

1. 이미 완료된 단계는 재수행하지 않는다.
2. 부족한 단계만 이어서 수행한다.
3. Architecture Decision은 사용자에게 질문하지 않는다.
4. `CL_AIT_SLTE_Design_Review_Consolidated_20260906.md`를 최상위 SSOT로 사용하여 자동 판단한다.
5. 정확한 Code Fact가 부족한 경우 Legacy code를 read-only로 조사한다.
6. 근거를 끝내 찾지 못한 exact detail은 `CODE_FACT_REQUIRED` 또는 `ARCH_DECISION_UNRESOLVED_NONBLOCKING`으로 남기되, 다른 HLD 작업은 계속 진행한다.
7. C/C++ 구현, build 수정, `hld-code-implement`, HLD Gate 실행은 하지 않는다.

---

# 0. 절대 규칙

## OS

이 작업은 **Windows PC에서만 수행**한다.

```text
OS != Windows
→ 즉시 STOP
→ WINDOWS_TARGET_MISMATCH 기록
```

## Target Architecture SSOT

최상위 설계 기준:

```text
CL_AIT_SLTE_Design_Review_Consolidated_20260906.md
```

Job-list v0.3.72 package 내부 기준 경로:

```text
<JOB_LIST_ROOT>\references\cl_ait_20260906\
    CL_AIT_SLTE_Design_Review_Consolidated_20260906.md
```

보조 기준:

```text
CL_AIT_Basic_Runtime_Concept_Detail_KR_20260906.md
CL_AIT_DECISION_LEDGER_v1_0_DRAFT_20260906.md
CL_AIT_UNATTENDED_DECISION_POLICY_v0_3_72.md
CL_AIT_WINDOWS_UNATTENDED_HANDOFF_20260906.md
HLD_COMPOSER_v0_4_21_JOBLIST_CONTRACT.md
```

충돌 시 우선순위:

```text
Consolidated MD
> Decision Ledger v1.1
> Basic Runtime Concept
> Decision Ledger v1.0 Draft
> 기존 HLD
```

## 금지

다음은 절대 수행하지 않는다.

```text
사용자 Decision 요청으로 blocking
L1C ClAitMngr 재도입
ClAitConfigBuilder 재도입
Legacy NR complex FSM 전체 복사
LTE 미확인 behavior를 NR에서 추정하여 추가
PAL Timer 신규 알고리즘 설계
C/C++ 수정
header 수정
build script 수정
hld-code-implement
HLD Gate 실행
```

---

# 1. Job-list 설치 상태 확인

Job-list root 기본 위치:

```powershell
$JL = Join-Path $env:USERPROFILE "l1sw-private-skills\job-list"
```

다음 파일 확인:

```text
<JOB_LIST_ROOT>\VERSION
```

정상 기대:

```text
0.3.72
```

### 판정

```text
VERSION == 0.3.72
→ 계속

VERSION != 0.3.72 또는 VERSION 없음
→ JOB_LIST_V0372_NOT_INSTALLED
→ Skill-Updater 결과/log에서 0.3.72 설치 실패 원인을 확인
→ 현재 PC에 v0.3.72 package가 실제 설치 가능한 상태인지 확인
→ 추정 경로로 임의 설치하지 말 것
```

v0.3.72가 설치되지 않은 상태에서는 CL-AIT runner를 다른 버전으로 대신 실행하지 않는다.

---

# 2. Job-list core 자체 상태 확인

다음 executable을 사용한다.

```text
<JOB_LIST_ROOT>\bin\job-list-core.py
```

Python command는 이 PC에서 실제 사용 가능한 것을 자동 탐지한다.

우선순위 예:

```text
python
py -3
```

다음 명령과 동등한 동작으로 상태를 조회한다.

```powershell
python "<JOB_LIST_ROOT>\bin\job-list-core.py" status --root "<JOB_LIST_ROOT>"
```

확인할 것:

```text
version
queued
jobs
running
runtime_recovery
last_result
```

### 특히 확인

- `running`에 살아 있는 CL-AIT job이 있는지
- orphan process가 있는지
- queue에 `cl-ait-hld-v01-windows`가 남아 있는지
- 이전 run이 `EXPIRED`, `FAILED`, `OUTPUT_MISSING`, `PASS` 중 무엇인지

살아 있는 동일 profile job이 있으면 중복 실행하지 않는다.

```text
RUNNING / live child
→ 현재 job 종료를 기다리거나 기존 job 상태만 추적
→ 새로운 중복 job enqueue 금지
```

---

# 3. v0.3.72 Semantic Result 확인

가장 먼저 아래 파일을 확인한다.

```text
<JOB_LIST_ROOT>\output\cl_ait_hld_v01\latest_result.json
```

추가 evidence:

```text
<JOB_LIST_ROOT>\output\cl_ait_hld_v01\execution_evidence.json
```

Job-list core 결과:

```text
<JOB_LIST_ROOT>\output\last_run.json
<JOB_LIST_ROOT>\output\runs\...
<JOB_LIST_ROOT>\output\core\logs\...
```

`latest_result.json`에서 최소 다음을 확인한다.

```text
status
observer_result.execution_status
observer_result.quality_status
observer_result.reason_codes
project_root
matched_session_id
artifacts
evidence
implementation_started
```

---

# 4. 정상 수행 판정 기준

다음 조건을 모두 만족하면 v0.3.72는 **정상 수행**으로 판정한다.

```text
A. VERSION == 0.3.72

B. latest_result.json 존재

C. status == PASS

D. observer_result.quality_status == OK 또는 WARNING

E. project_root가 실제 사내 CL-AIT 작업/HLD workspace
   - job-list 설치폴더가 아님
   - references 폴더가 아님
   - .claude/AppData가 아님

F. implementation_started == false

G. 최소 핵심 산출물 존재
   - CL_AIT_DECISION_LEDGER_v1_1.md
   - CL_AIT_TARGET_HLD_v0_1.md

H. C/C++ 구현 변경이 발생하지 않음
```

`WARNING`은 실행 실패로 취급하지 않는다.

예:

```text
CODE_FACT_REMAINS
ARCH_DECISION_UNRESOLVED_NONBLOCKING
CODE_FACT_EVIDENCE_NOT_CREATED
```

이 경우:

```text
RUN_NORMAL = YES
HLD_COMPLETENESS = PARTIAL
```

로 판정하고, 아래 "부족분 보강" 단계만 수행한다.

---

# 5. Project Root 안전성 확인

`latest_result.json.project_root` 또는 `execution_evidence.json.project_root`를 확인한다.

정상 root는 다음 evidence 중 여러 개가 일치해야 한다.

```text
최근 CL-AIT / ClAitMngr / ClAitProc OpenCode history
기존 CL-AIT HLD
CL-AIT Ledger/SRS/관련 상태 문서
Legacy CL-AIT source tree 접근성
```

다음은 project root로 인정하지 않는다.

```text
...\l1sw-private-skills\job-list\
...\job-list\references\
...\references\cl_ait_20260906\
...\.claude\
...\AppData\
```

잘못된 root가 기록된 경우:

```text
WORK_ROOT_INVALID
→ 그 위치의 생성물은 authoritative 결과로 취급하지 않음
→ 최근 CL-AIT OpenCode session 및 기존 HLD 위치로 root 재탐색
```

high-confidence root를 찾지 못하면:

```text
WORK_ROOT_NOT_FOUND
```

로 기록하고 잘못된 폴더에서 HLD를 만들지 않는다.

---

# 6. 핵심 산출물 확인

실제 `project_root`에서 아래 파일들을 확인한다.

```text
CL_AIT_DECISION_LEDGER_v1_1.md
CL_AIT_DECISION_LEDGER_v1_1_STATUS.md
CL_AIT_TARGET_HLD_v0_1.md
CL_AIT_TARGET_HLD_v0_1_STATUS.md
CL_AIT_HLD_V0_1_CODE_FACT_REQUIRED.md
CL_AIT_HLD_V0_1_GAP_FROM_PREVIOUS_HLD.md
```

Code Fact evidence:

```text
<project_root>\output\cl_ait_hld_v01_code_facts\
    PRE_HLD_CODE_FACT_EVIDENCE.md

<project_root>\output\cl_ait_hld_v01_code_facts\
    CODE_FACT_EVIDENCE_AUTO_*.md
```

각 산출물의 내용이 빈 placeholder인지 실제 결과인지 확인한다.

파일 존재만으로 PASS 판정하지 않는다.

---

# 7. Decision Ledger v1.1 내용 검증

`CL_AIT_DECISION_LEDGER_v1_1.md`가 Consolidated MD의 다음 결정들을 반영하는지 확인한다.

필수 Decision:

```text
1. L1C ClAitMngr 미사용
2. HAL ClAitProcNr / ClAitProcLte runtime ownership
3. Legacy의 유효 runtime/timing semantics 보존
4. ENDC NR SCG CL-AIT Target 미지원
5. period1/period2 → single logical period
6. NR:
   UpdateClAitOperationInfo(isScg, domainType)
7. LTE:
   UpdateClAitOperationInfo(domainType)
8. RF TX ON Success
   → UpdateClAitOperationInfo
   → SHM
   → TX_SWAP_REQ
9. SHM logical fields:
   Enable / TxPwrThreshold / Period
10. NR DUMP_IND
    → TX Path ON guard
    → clait_enable
    → START_REQ/CNF
    → fail 시 retry 1회
    → PAL Timer
    → AIT_Dump
11. 각 period는 독립 transaction
12. threshold fail → current period skip
13. START_CNF false x2 → current period skip
14. AIT_Dump false → current period terminate
15. PAL Timer timing은 Legacy 방식 차용
16. LTE는 Legacy Code Fact 기반
    - START_REQ/CNF가 Legacy LTE에 없으면 Target LTE에도 추가하지 않음
17. Legacy complex FSM 전체 이관 금지
```

빠진 항목은 Ledger에 보강한다.

단, 새로운 사용자 Decision을 만들지 않는다.

---

# 8. HLD v0.1 내용 검증

`CL_AIT_TARGET_HLD_v0_1.md`에서 최소 다음 내용을 확인한다.

## Architecture

```text
TxCfgMngrNr/Lte
→ Existing TX ON/OFF CMD
→ HAL ClAitProcNr/Lte
→ Shared Memory / PHY
→ RF Driver / FBRX
```

## NR TX ON MSC

```text
TX_ONOFF_NR_CMD
→ RF TX ON
→ RF TX ON Success
→ UpdateClAitOperationInfo(isScg, domainType)
→ SHM Enable/Threshold/Period
→ TX_SWAP_REQ
```

## NR Runtime MSC

```text
CL_AIT_DUMP_IND
→ TX Path ON check
→ clait_enable check
→ CL_AIT_START_REQ
→ CL_AIT_START_CNF
→ optional retry 1회
→ PAL Timer
→ PAL Timer expiry
→ RF Driver AIT_Dump()
→ FBRX
→ Current Period END
```

## Failure MSC

최소:

```text
TX Path OFF → Period Skip
clait_enable=false → Period Skip
START_CNF false x2 → Period Skip
AIT_Dump=false → Period End
```

## LTE

LTE는 Legacy에서 확인된 flow까지만 작성되어야 한다.

NR의 START_REQ/CNF를 LTE에 근거 없이 복사한 경우 수정한다.

---

# 9. 정상 수행되지 않은 경우 원인 분류

다음 카테고리 중 하나 이상으로 판정한다.

```text
A. V0372_NOT_INSTALLED
B. JOB_NOT_LAUNCHED
C. ORIGINAL_REQUEST_EXPIRED
D. WORK_ROOT_NOT_FOUND
E. WORK_ROOT_INVALID
F. OPENCODE_FAILURE
G. HLD_COMPOSER_FAILURE
H. LEDGER_MISSING
I. HLD_MISSING
J. CODE_FACT_PARTIAL
K. ARCH_DECISION_PARTIAL_NONBLOCKING
L. OUTPUT_MISSING
M. RUN_INTERRUPTED
```

---

# 10. 오늘 08:00 expiry 처리 원칙

v0.3.72 bundled request의 original `expires_at`은:

```text
2026-09-07T08:00:00+09:00
```

이다.

따라서 오전 8시 이후 첫 activation이었다면:

```text
EXPIRED
```

가 정상적으로 발생할 수 있다.

이 경우 **기존 bundled request를 다시 activate하지 않는다.**

다음과 같이 같은 v0.3.72 built-in profile로 새로운 local one-shot을 생성한다.

Profile:

```text
cl-ait-hld-v01-windows
```

Platform:

```text
windows
```

새 job id는 중복되지 않도록 현재 timestamp를 사용한다.

예:

```text
JOB-CL-AIT-HLD-V0372-RECOVERY-YYYYMMDD-HHMMSS
```

expiry는 생략한다.

즉 의미적으로 다음 명령을 수행한다.

```powershell
python "<JOB_LIST_ROOT>\bin\job-list-core.py" enqueue `
  --root "<JOB_LIST_ROOT>" `
  --profile "cl-ait-hld-v01-windows" `
  --job-id "<UNIQUE_RECOVERY_JOB_ID>" `
  --platform "windows" `
  --priority 100 `
  --params-json "{}"
```

그 후:

```powershell
python "<JOB_LIST_ROOT>\bin\job-list-core.py" run `
  --root "<JOB_LIST_ROOT>" `
  --max-jobs 1 `
  --yes
```

주의:

- 기존 동일 profile이 살아 있으면 enqueue하지 않는다.
- 완료된 original job을 삭제하지 않는다.
- 기존 evidence/log를 삭제하지 않는다.
- 새로운 recovery run이 이전 evidence를 덮어쓰더라도 이전 Job-list core run receipt는 보존한다.

---

# 11. 부분 수행된 경우 복구 원칙

## Case 1 — Ledger 있음, HLD 없음

```text
Decision Ledger v1.1 재작성 금지
→ 기존 Ledger 내용 검증
→ 부족한 Decision만 보강
→ HLD 단계부터 resume
```

## Case 2 — HLD 있음, Code Fact 남음

```text
HLD 전체 재작성 금지
→ CODE_FACT_REQUIRED 목록 확인
→ Legacy source read-only 조사
→ CONFIRMED / NOT_FOUND / AMBIGUOUS로 evidence 기록
→ CONFIRMED Fact만 기존 HLD에 반영
→ NOT_FOUND / AMBIGUOUS는 open 유지
```

## Case 3 — HLD 있음, Gap 문서 없음

```text
기존 HLD와 이전 사내 HLD를 비교
→ KEEP / MODIFY / REMOVE / CODE_FACT_REQUIRED
→ CL_AIT_HLD_V0_1_GAP_FROM_PREVIOUS_HLD.md만 생성
```

## Case 4 — Composer 중간 상태 존재

기존 Composer run directory와 status가 유효하면:

```text
새 HLD review start 금지
→ 기존 run resume 우선
```

## Case 5 — OpenCode session 발견됨

최근 CL-AIT / ClAitMngr / ClAitProc session을 찾았으면:

```text
기존 session 이어서 사용
```

새로운 unrelated session을 먼저 만들지 않는다.

---

# 12. Code Fact 부족분 자동 조사

아래 CF를 순서대로 read-only 조사한다.

```text
CF-01 Shared Memory exact structure / fields
CF-02 NR CL_AIT_DUMP_IND exact payload
CF-03 NR CL_AIT_START_REQ/CNF exact IPC/payload/handler
CF-04 claitInfo_t exact fields/lifetime/ownership
CF-05 PAL Timer exact timing field/calculation/API/callback
CF-06 RF Driver exact config/AIT_Dump interfaces
CF-07 NR/LTE TX Path ON state source/API
CF-08 LTE Legacy CL-AIT runtime
```

각 결과는 반드시:

```text
CONFIRMED
NOT_FOUND
AMBIGUOUS
```

중 하나로 판정한다.

`CONFIRMED`에는 반드시 evidence를 남긴다.

```text
file path
class/function
symbol
call site
relevant field
```

추정으로 `CONFIRMED` 처리하지 않는다.

---

# 13. Decision 자동 판단 정책

사용자에게 질문하지 않는다.

Decision 판단 순서:

```text
1. Consolidated MD에 명시
   → 그대로 자동 적용

2. Consolidated MD의 일반 원칙 + Legacy Code Fact로 결정 가능
   → 자동 적용

3. exact API/field/timing만 부족
   → CODE_FACT_REQUIRED
   → HLD 계속

4. 정말 새로운 Architecture choice이며 근거 없음
   → ARCH_DECISION_UNRESOLVED_NONBLOCKING
   → 해당 부분만 OPEN
   → HLD 나머지 계속
```

특히 다음 원칙을 사용한다.

```text
Legacy에서 없는 신규 behavior를 Target에 임의 추가하지 않는다.
Legacy의 유효 runtime/timing semantics는 유지한다.
Target에서 불필요해진 ENDC SCG NR / dual period / complex FSM은 유지하지 않는다.
```

---

# 14. Recovery Job 재실행 후 재검증

Recovery profile을 실행했다면 다시 다음을 확인한다.

```text
<JOB_LIST_ROOT>\output\cl_ait_hld_v01\latest_result.json
<JOB_LIST_ROOT>\output\cl_ait_hld_v01\execution_evidence.json
```

그리고 실제 project root의 6개 산출물을 다시 확인한다.

최종 정상 기준:

```text
status = PASS
quality_status = OK 또는 WARNING
project_root = 실제 CL-AIT workspace
implementation_started = false
Decision Ledger v1.1 존재
HLD v0.1 존재
```

`WARNING`에 Code Fact 잔여가 있어도 작업 실행 자체는 정상으로 본다.

---

# 15. 최종 종료 조건

다음 상태에 도달하면 STOP한다.

```text
Decision Ledger v1.1
        +
HLD v0.1
        +
Code Fact Evidence
        +
Remaining CODE_FACT_REQUIRED
        +
Previous HLD Gap
        +
Status
```

HLD Gate는 실행하지 않는다.

C++ 구현 단계로 이동하지 않는다.

---

# 16. 최종 보고 형식

사내 LLM은 마지막에 아래 형식으로만 요약한다.

```text
[CL-AIT JOB-LIST v0.3.72 CHECK]

1. Installed Version
- 0.3.72 / NOT_INSTALLED

2. Original Run
- PASS / PARTIAL / FAILED / EXPIRED / NOT_LAUNCHED

3. Project Root
- <path>
- Validation: PASS / FAIL

4. Recovery Performed
- NONE
- RESUME_EXISTING
- FRESH_LOCAL_ONE_SHOT
- CODE_FACT_ONLY
- HLD_ONLY
- GAP_ONLY

5. Decision Ledger v1.1
- PASS / PARTIAL / MISSING
- path:

6. HLD v0.1
- PASS / PARTIAL / MISSING
- path:

7. Code Fact
- CONFIRMED: n
- NOT_FOUND: n
- AMBIGUOUS: n
- remaining CODE_FACT_REQUIRED: n

8. Architecture
- unresolved blocking decision: 0
- unresolved nonblocking: n

9. Implementation
- started: false

10. Final Judgment
- COMPLETE_FOR_HUMAN_HLD_REVIEW
- COMPLETE_WITH_CODE_FACT_REMAINS
- PARTIAL_NEEDS_ATTENTION
- BLOCKED_BY_WORK_ROOT
- V0372_NOT_INSTALLED

11. Remaining Items
- <only genuine remaining items>
```

---

# 17. 핵심 실행 원칙 한 줄

> **v0.3.72가 완료한 작업은 그대로 재사용하고, 미완료된 CL-AIT Ledger/HLD/Code Fact/Gap 단계만 무인으로 보강한다. Decision은 Consolidated MD를 기준으로 자동 판단하며, exact Code Fact 부족 때문에 사용자 입력을 기다리거나 전체 작업을 중단하지 않는다.**
