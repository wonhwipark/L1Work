# L1SW Dev Knowledge Gotcha Review Prompt v1.3

`v1.3 · 2026-10-10`

## 목적

`l1sw-dev-knowledge`의 기존 Gotcha 분석 기능을 유지하면서,
Legacy / SLTE 구조 혼용을 막고 사용자 입력을 최소화한다.

핵심 원칙:

1. Scope는 사용자가 한 번 등록한다.
2. 평소 Gotcha 검토에서는 `Profile + 암묵지 원문`만 입력한다.
3. `l1sw-dev-knowledge`는 등록된 Profile의 Folder/File Scope 안에서만 Evidence를 검토한다.
4. 기존 Knowledge 검색은 넓게 할 수 있지만 Scope 밖 Knowledge/Evidence를 현재 Gotcha의 근거로 승격하지 않는다.
5. 실제 Knowledge 생성/수정 전 반드시 Preview를 제공하고 사용자 승인 후 반영한다.

---

# A. 사용자 입력 영역

## A-1. 최초 1회 설정: Scope Profile

> 아래 Profile은 프로젝트 구조가 바뀔 때만 수정한다.
> 매 Gotcha 검토마다 다시 입력하지 않는다.

### PROFILE: TX_LEGACY

```text
PROFILE_NAME = TX_LEGACY
MODE         = OPTION_SLTE_DISABLE
DOMAIN       = TX
PATH_BASE    = <사용자 입력 필요>

INCLUDE_FOLDERS:
<사용자 입력 필요 또는 NONE>

INCLUDE_FILES:
<사용자 입력 필요 또는 NONE>

EXCLUDE_FOLDERS:
NONE

EXCLUDE_FILES:
NONE

SHARED_EXCEPTION_FILES:
NONE
```

### PROFILE: TX_SLTE

```text
PROFILE_NAME = TX_SLTE
MODE         = OPTION_SLTE_ENABLE
DOMAIN       = TX
PATH_BASE    = <사용자 입력 필요>

INCLUDE_FOLDERS:
<사용자 입력 필요 또는 NONE>

INCLUDE_FILES:
<사용자 입력 필요 또는 NONE>

EXCLUDE_FOLDERS:
NONE

EXCLUDE_FILES:
NONE

SHARED_EXCEPTION_FILES:
NONE
```

> `OPTION_SLTE_ENABLE` 빌드에 Legacy LTE/NR 코드가 함께 포함되어도
> `TX_SLTE` Profile에 사용자가 명시하지 않은 Legacy Folder/File은
> Gotcha 검토 대상에 자동 포함하지 않는다.

### PROFILE: TX_CUSTOM (선택)

```text
PROFILE_NAME       = TX_CUSTOM
MODE               = CUSTOM
CUSTOM_DEFINITION  = <필요 시 사용자 입력>
DOMAIN             = TX
PATH_BASE          = <사용자 입력>

INCLUDE_FOLDERS:
<사용자 입력 또는 NONE>

INCLUDE_FILES:
<사용자 입력 또는 NONE>

EXCLUDE_FOLDERS:
NONE

EXCLUDE_FILES:
NONE

SHARED_EXCEPTION_FILES:
NONE
```

---

## A-2. 평소 검토 시 사용자 입력

평소에는 아래 두 가지만 입력한다.

```text
PROFILE = <TX_LEGACY | TX_SLTE | TX_CUSTOM>

[G-01]
원문: <검토할 암묵지/Gotcha 원문>
출처: NONE
```

자연어 호출 예시:

```text
/l1sw-dev-knowledge

TX_SLTE 기준으로 아래 암묵지 검토해줘.

"ENDC에서 NR Tx switching 전에 LTE Tx 상태를 확인해야 한다."
```

또는:

```text
/l1sw-dev-knowledge gotcha review TX_SLTE

"ENDC에서 NR Tx switching 전에 LTE Tx 상태를 확인해야 한다."
```

---

## A-3. 이번 검토에서만 Scope 예외 추가 (선택)

```text
TEMP_INCLUDE_FOLDERS:
NONE

TEMP_INCLUDE_FILES:
NONE

TEMP_EXCLUDE_FOLDERS:
NONE

TEMP_EXCLUDE_FILES:
NONE

TEMP_SHARED_EXCEPTION_FILES:
NONE
```

자연어 예:

```text
TX_SLTE 기준으로 검토해줘.
이번 분석만 LegacyTxSwitch.cpp도 포함해줘.
```

이 경우 기본 Profile은 수정하지 않고 이번 실행에만 Temporary Scope로 적용한다.

---

# B. l1sw-dev-knowledge 내부 동작 규칙

## B-1. Profile Resolution

1. 사용자가 지정한 `PROFILE`을 먼저 해석한다.
2. Profile에 정의된 `MODE / PATH_BASE / Folder / File`을 Review Scope의 SSOT로 사용한다.
3. Temporary Scope가 있으면 이번 실행에만 합친다.
4. Profile이 없거나 정의되지 않았으면 임의 추정하지 말고 Profile 선택을 요청한다.
5. Source Code, CMake, Build 포함 여부만으로 Profile Scope를 자동 확장하지 않는다.

## B-2. Scope Guard

1. Source Code Evidence 탐색은 Review Scope 안으로 제한한다.
2. 전체 Repository 재귀 분석으로 Scope를 다시 찾지 않는다.
3. Scope 밖 파일이 검색 결과에 나타나도 자동 포함하지 않는다.
4. Scope 밖 Knowledge는 관련성 확인 용도로만 사용할 수 있다.
5. Scope 밖 Evidence만으로 다음을 생성/보강하지 않는다.
   - 조건
   - 함정
   - Root Cause / Mechanism
   - 관측 증상
   - 올바른 규칙
   - 제외 조건
   - Applicability
6. Scope 불명확 시 `UNKNOWN`, 기존 Knowledge는 `SCOPE_UNKNOWN`으로 둔다.
7. 사용자 원문에 없는 원인/조건을 사실처럼 생성하지 않는다.

---

# C. Gotcha 검토 절차

## Step 0. Scope 확인

먼저 다음을 확정한다.

```text
Profile:
Mode:
Domain:
Path Base:
Included Scope:
Excluded Scope:
Temporary Scope:
```

다음이면 중단한다.

- Profile 미정
- Profile 정의 없음
- Include Folder/File이 모두 NONE
- Include/Exclude 충돌
- CUSTOM인데 CUSTOM_DEFINITION 없음

## Step 1. 암묵지 원문 분해

원문에 명시된 내용만 Claim으로 분리한다.

```text
C-01:
C-02:
...
```

원문에 없지만 필요한 정보는:

```text
UNKNOWN:
- ...
```

으로 둔다.

## Step 2. Evidence 확인

사용 가능한 근거:

- Code
- JIRA / Issue
- FLA
- HLD / MSC
- Log
- PR / CL / Commit

각 Claim은 다음 중 하나로 판정한다.

```text
CONFIRMED
WEAK_SUPPORT
NO_EVIDENCE
CONTRADICTED
```

원칙:

- Code Evidence는 가능하면 `File + Symbol/Line + CL/Revision`을 남긴다.
- JIRA/Log 등은 다시 확인 가능한 ID/위치를 남긴다.
- Scope 밖 Evidence는 참고만 가능하다.
- 근거가 없으면 추론으로 채우지 않는다.

## Step 3. Gotcha Structure 생성

```text
조건:
함정:
관측 증상:
올바른 규칙:
제외 조건:
```

근거가 없으면 `UNKNOWN`으로 둔다.

## Step 4. Applicability 결정

Review Scope 전체가 아니라 실제 Claim/Evidence가 뒷받침하는 최소 범위만 사용한다.

```text
Mode:
RAT:
Folder/File:
Evidence:
```

핵심 축이 `UNKNOWN`이면 자동 병합/수정하지 않는다.

## Step 5. 기존 Knowledge 검색

기존 `l1sw-dev-knowledge`의 Gotcha/Knowledge 검색 기능을 사용한다.

검색 항목:

```text
IN_SCOPE
OUT_OF_SCOPE
SCOPE_UNKNOWN
```

- `IN_SCOPE`: 정상 비교
- `SCOPE_UNKNOWN`: 비교 가능, 자동 UPDATE/MERGE 금지
- `OUT_OF_SCOPE`: 비교 대상에서 제외, 참고만 표시

> "검색은 넓게"는 기존 Knowledge/KB 검색에만 적용한다.
> Source Code/Evidence 검색 범위를 넓히라는 의미가 아니다.

## Step 6. 매칭 판정

```text
NEW
DUPLICATE
ENHANCEMENT
CONFLICT
```

- `DUPLICATE`: 조건/함정/규칙이 같고 기존 Knowledge가 신규 후보 범위를 포함
- `ENHANCEMENT`: 핵심은 같고 신규 후보가 조건/증상/Rule/Evidence 등을 보완
- `CONFLICT`: 적용범위가 겹치지만 Rule/함정이 서로 모순
- `NEW`: 위 항목과 매칭되지 않음

Applicability 핵심 축이 `UNKNOWN`이면:

```text
(APPLICABILITY_UNKNOWN)
HOLD
```

로 처리한다.

## Step 7. Confidence / Action

Confidence:

```text
VERIFIED
PARTIAL
UNVERIFIED
```

Action:

| 조건 | 조치 |
|---|---|
| NEW + VERIFIED | CREATE |
| NEW + PARTIAL | CREATE 가능, PARTIAL 명시 |
| NEW + UNVERIFIED | HOLD |
| DUPLICATE | NO_ACTION, 새 Evidence만 있으면 UPDATE 후보 |
| ENHANCEMENT | UPDATE 후보 |
| CONFLICT | HOLD |
| SCOPE_UNKNOWN | HOLD |
| APPLICABILITY_UNKNOWN | HOLD |
| CONTRADICTED 포함 | HOLD |

`HOLD`가 다른 Action보다 우선한다.

---

# D. 기본 출력 UX

기본 출력은 짧게 한다.

```text
[Gotcha Review G-01]

Profile      : TX_SLTE
Result       : NEW / DUPLICATE / ENHANCEMENT / CONFLICT
Confidence   : VERIFIED / PARTIAL / UNVERIFIED
Existing KB  : <KB ID 또는 NONE>
Action       : CREATE / UPDATE / NO_ACTION / HOLD

핵심:
- 조건:
- 함정:
- 규칙:

근거:
- <핵심 Evidence 1~3개>

주의:
- <UNKNOWN / SCOPE_UNKNOWN / OUT_OF_SCOPE가 있으면 표시>

선택:
1. 상세 근거 보기
2. 변경 Preview 보기
3. HOLD
```

사용자가 상세 결과를 요청한 경우에만 Claim/Evidence/Applicability 전체를 출력한다.

---

# E. Update Preview / 승인

실제 `l1sw-dev-knowledge`를 생성/수정하기 전에 반드시 Preview한다.

```text
[Update Preview]

Preview ID: PV-YYYYMMDD-HHMM

G-01
Action:
Target KB:
Before:
After:
Confidence:
```

승인은 다음처럼 항목 ID를 명시한 경우만 인정한다.

```text
승인: G-01
```

또는:

```text
승인: 전체 PV-YYYYMMDD-HHMM
```

Preview 이후 아래가 바뀌면 기존 Preview는 무효다.

- Scope Profile
- Temporary Scope
- 입력 암묵지
- 대상 KB 버전

---

# F. 사용자에게 필요한 입력 요약

## 최초 1회

반드시 사용자가 채워야 하는 값:

```text
TX_LEGACY
- PATH_BASE
- INCLUDE_FOLDERS 또는 INCLUDE_FILES

TX_SLTE
- PATH_BASE
- INCLUDE_FOLDERS 또는 INCLUDE_FILES
```

필요할 때만:

```text
- EXCLUDE_FOLDERS / EXCLUDE_FILES
- SHARED_EXCEPTION_FILES
- TX_CUSTOM
```

## 평소 Gotcha 검토

사용자가 입력할 것은 사실상 두 가지다.

```text
1. PROFILE
2. 암묵지 원문
```

예:

```text
TX_SLTE 기준으로 이 암묵지 검토해줘.

"..."
```

## 필요할 때만

```text
- Temporary Include/Exclude
- 출처
- Release/Branch
- Feature/Scenario
```

---

# G. 목표 사용자 경험

```text
[최초 1회]

사용자
  ↓
TX_LEGACY / TX_SLTE Folder/File 등록
  ↓
Profile 저장


[평소]

사용자
  ↓
"TX_SLTE 기준으로 이 암묵지 검토해줘"
  ↓
l1sw-dev-knowledge
  ├─ Profile 자동 로드
  ├─ Scope Guard 적용
  ├─ 기존 Gotcha 검색
  ├─ Evidence 확인
  ├─ NEW/DUPLICATE/ENHANCEMENT/CONFLICT 판정
  └─ 요약 결과
  ↓
사용자
  ├─ 1 상세 근거
  ├─ 2 Preview
  └─ 3 HOLD
  ↓
명시적 승인
  ↓
Knowledge 반영
```

---

# H. 구현 권장사항

이 문서는 장기적으로 사용자가 매번 붙이는 실행 프롬프트가 아니라,
검증 후 `l1sw-dev-knowledge` 내부의 **Gotcha Review Policy / Scope Guard**로 내장하는 것을 권장한다.

사용자에게 노출되는 기능은 다음 두 개면 충분하다.

```text
1. Scope Profile 관리
2. Gotcha Review
```

최종적으로 사용자는 아래처럼 자연어만 입력하면 된다.

```text
TX_SLTE 기준으로 아래 암묵지 검토해줘.

"..."
```
