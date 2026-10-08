# L1SW Dev Knowledge Gotcha Review Scope Prompt

`v1.2 · 2026-10-08` · v1.1 리뷰 보강 + SLTE Mode별 사용자 편집 Scope Map 추가. 상세는 문서 끝 **변경 이력** 참조.

## 목적

`l1sw-dev-knowledge`가 Gotcha/암묵지를 검색·검토·업데이트하기 전에,
사용자가 지정한 **Feature Mode + Folder/File Scope**를 SSOT로 사용하도록 한다.

코드 전체를 대상으로 적용범위를 추론하지 말고,
사용자가 지정한 Scope 안에서만 Gotcha의 신규/중복/보강/충돌 여부를 검토한다.

이 Scope는 **이번에 검토할 범위**이며, 저장되는 Gotcha의 **적용범위**와 구분한다(§4-7).

---

## 1. Analysis Context

```text
Domain            = TX
MODE              = <필수: OPTION_SLTE_DISABLE | OPTION_SLTE_ENABLE | CUSTOM>
CUSTOM_DEFINITION = NONE   (MODE = CUSTOM이면 필수: 빌드 옵션 조합 등)
RAT               = <필수: LTE | NR | COMMON | UNKNOWN>
Path Base         = <필수: 경로 비교 기준 — depot 경로 또는 workspace 루트>
Release/Branch    = NONE   (코드 근거를 쓰려면 필수)
Feature           = NONE
Scenario          = NONE
```

- 해당 없음은 `NONE`으로 적는다.
- `<…>` 표식이나 빈 칸이 남아 있으면 검토가 중단된다(§6 Step 0).

---

## 2. User-Editable SLTE Mode Scope Map

> 아래 영역은 **사용자가 직접 수정하는 Scope 설정 영역**이다.
> `l1sw-dev-knowledge`는 이 값을 SSOT로 사용하며, 코드 전체를 분석해서 Scope를 재추론하지 않는다.
>
> **중요:** 실제 경로는 프로젝트 환경에 맞게 사용자가 직접 채운다.
> `OPTION_SLTE_DISABLE`과 `OPTION_SLTE_ENABLE` 각각에 대해 검토할 Folder/File을 독립적으로 관리한다.

작성 규칙

- 경로는 `Path Base` 기준 상대경로로, 한 줄에 하나씩 적는다.
- 폴더는 `/`로 끝나며 하위 폴더 전체를 포함한다.
- 와일드카드(`*`, `**`)는 쓰지 않는다.
- 사용하지 않는 항목은 `NONE`으로 둔다.
- 같은 경로를 Include/Exclude에 동시에 넣지 않는다.
- Legacy 코드가 SLTE Enable 빌드에 포함되더라도, 아래 Enable Scope에 사용자가 넣지 않았다면 검토 대상이 아니다.

### 2.1 OPTION_SLTE_DISABLE Scope

`MODE = OPTION_SLTE_DISABLE`일 때 사용하는 기본 Scope다.

#### Include Folders

```text
<사용자가 입력 또는 NONE>
```

#### Include Files

```text
<사용자가 입력 또는 NONE>
```

#### Exclude Folders

```text
NONE
```

#### Exclude Files

```text
NONE
```

#### Shared / Exception Files

현재 Mode에서 함께 검토해야 하는 공통/예외 파일이다.

```text
NONE
```

---

### 2.2 OPTION_SLTE_ENABLE Scope

`MODE = OPTION_SLTE_ENABLE`일 때 사용하는 기본 Scope다.

> SLTE Enable 빌드에 Legacy LTE/NR 코드가 함께 포함되더라도,
> **실제로 Gotcha 검토가 필요한 Legacy Folder/File만 사용자가 명시적으로 여기에 추가한다.**

#### Include Folders

```text
<사용자가 입력 또는 NONE>
```

#### Include Files

```text
<사용자가 입력 또는 NONE>
```

#### Exclude Folders

```text
NONE
```

#### Exclude Files

```text
NONE
```

#### Shared / Exception Files

SLTE Enable 상태에서도 실제 동작·연계·예외 처리 때문에 함께 검토해야 하는
Legacy/Common 파일을 사용자가 명시한다.

```text
NONE
```

---

### 2.3 CUSTOM Scope

`MODE = CUSTOM`일 때만 사용한다.

#### Include Folders

```text
<사용자가 입력 또는 NONE>
```

#### Include Files

```text
<사용자가 입력 또는 NONE>
```

#### Exclude Folders

```text
NONE
```

#### Exclude Files

```text
NONE
```

#### Shared / Exception Files

```text
NONE
```

---

### 2.4 Current Review Additional Scope (선택)

선택한 Mode의 기본 Scope에 **이번 검토에서만 추가**할 경로가 있을 때 사용한다.
기본값은 모두 `NONE`이다.

#### Additional Include Folders

```text
NONE
```

#### Additional Include Files

```text
NONE
```

#### Additional Exclude Folders

```text
NONE
```

#### Additional Exclude Files

```text
NONE
```

#### Additional Shared / Exception Files

```text
NONE
```

---

### 2.5 Mode Scope 적용 규칙

1. `MODE = OPTION_SLTE_DISABLE`
   - §2.1을 기본 Scope로 사용한다.
2. `MODE = OPTION_SLTE_ENABLE`
   - §2.2를 기본 Scope로 사용한다.
3. `MODE = CUSTOM`
   - §2.3을 기본 Scope로 사용한다.
4. §2.4가 있으면 선택된 기본 Scope에 추가 적용한다.
5. Additional Exclude가 Include보다 우선한다.
6. 선택된 Mode가 아닌 다른 Mode Scope의 경로는 비교·업데이트 대상에 자동 포함하지 않는다.
7. 다른 Mode Scope에서 관련성이 높은 Knowledge를 발견하더라도 `[Out-of-Scope References]`로만 보고한다.
8. Scope Map을 코드 분석 결과로 자동 변경하지 않는다. 변경이 필요하면 사용자에게 후보 경로만 제안하고, 사용자가 프롬프트의 §2를 직접 수정한다.

---

## 3. 검토 대상 암묵지

```text
[G-01]
원문: <필수: 암묵지/주의사항 원문>
출처: NONE   (선택: BD·FT·REC ID, JIRA 키, 구두 등)
```

- 여러 건이면 `[G-02]`, `[G-03]` … 블록을 추가한다.
- ID가 없으면 입력 순서대로 G-01부터 부여한다.

---

## 4. 절대 규칙

아래 규칙은 어떤 판단보다 우선한다.

1. Scope는 §1–§3 입력과 §5 해석 규칙으로만 정한다. 폴더명, 파일명, semantic similarity, 코드 존재 여부로 Scope를 확장하지 않는다.
2. Exclude로 제외된 경로와, 그 경로에만 해당하는 Knowledge는 검색·비교·업데이트 대상에서 뺀다.
3. `MODE = OPTION_SLTE_ENABLE`이어도 Legacy LTE/NR 코드 일부가 빌드에 포함될 수 있다. 빌드 포함 사실만으로 Knowledge를 Applicable로 판단하지 않는다.
4. Scope 밖에서 관련성이 높은 코드/Knowledge를 발견해도 자동 포함하지 않고 [Out-of-Scope References]로만 보고한다.
5. Scope나 판정 근거가 불명확하면 추론하지 말고 `UNKNOWN`(기존 Knowledge는 `SCOPE_UNKNOWN`)으로 둔다.
6. 사용자 원문에 없는 원인, 조건, failure mechanism을 사실처럼 생성하지 않는다.
7. 리뷰 Scope를 Gotcha의 적용범위로 복사하지 않는다. 적용범위는 진술·근거가 직접 뒷받침하는 최소 범위다.
8. Scope 밖 근거만으로 `VERIFIED`를 주지 않는다.
9. 사용자 승인 전에는 Knowledge를 생성·수정하지 않고 Scope를 변경하지 않는다(§9).
10. `검색은 넓게 한다`는 기존 Knowledge/KB 검색에만 적용한다. Source Code, Log, HLD, JIRA 등 Evidence 탐색은 선택된 Review Scope 또는 사용자가 명시적으로 제공한 Evidence 위치로 제한하며, 전체 Repository를 재귀 탐색하지 않는다.
11. `OUT_OF_SCOPE` Evidence는 참고 정보로만 사용한다. OUT_OF_SCOPE Evidence만으로 조건·함정·Root Cause/Mechanism·올바른 규칙·제외 조건·Applicability를 새로 만들거나 보강하지 않는다.

---

## 5. Scope 해석 규칙

1. 먼저 §1의 `MODE`에 따라 §2.1/§2.2/§2.3 중 하나를 선택하고, §2.4 Additional Scope를 합쳐 Review Scope를 만든다.
2. 스킬 런타임이 Resolved Scope를 제공하면 그 결과를 그대로 사용하고 다시 해석하지 않는다.
3. 그렇지 않으면 아래 순서로 해석한다.
   1. 같은 경로가 포함 계열(Include Folders·Files, Shared)과 제외 계열(Exclude Folders·Files)에 동시에 있으면 `SCOPE_CONFLICT`로 중단한다.
   2. 파일 단위 지정이 폴더 단위 지정보다 우선한다.
   3. 폴더끼리는 더 깊은 경로의 지정이 우선한다.
   4. 어느 지정에도 해당하지 않는 경로는 Scope 밖이다.
4. KB 태그의 Mode·RAT·경로 표기가 이 문서와 다르면 대응표를 Resolved Scope에 적는다. 대응시킬 수 없는 기존 항목은 `SCOPE_UNKNOWN`이다.
5. `RAT = UNKNOWN`이면 RAT 축은 비교 집합 필터에 쓰지 않는다(모든 항목을 RAT 겹침으로 본다).
6. `MODE = CUSTOM`이면 같은 CUSTOM 정의 또는 `ANY`로 태그된 Knowledge만 Mode가 겹친다고 본다. 그 외 Mode 태그는 겹침 여부를 정할 수 없으므로 `SCOPE_UNKNOWN`이다.

---

## 6. 검토 절차

Step 0은 한 번, Step 1–7은 입력 항목(G-xx)마다 수행한다. 각 Step은 앞 Step의 결과만 사용한다.

### Step 0. Scope 검증·해석

§1의 MODE를 기준으로 §2의 해당 Mode Scope를 선택하고 §3 입력을 확인한 뒤 §5로 Resolved Scope를 만든다. 다음 중 하나면 중단하고 누락·충돌 항목만 질문한다.

- 입력 표식(`<…>`)이 남아 있거나 빈 칸이 있음
- 선택된 Mode Scope에서 Include Folders와 Include Files가 모두 `NONE`이고 §2.4 Additional Include도 모두 `NONE`
- `MODE = CUSTOM`인데 `CUSTOM_DEFINITION = NONE`
- `SCOPE_CONFLICT`

### Step 1. 진술 추출

원문에 명시된 내용만 Stated Claims(C-01, C-02 …)로 나눈다.
원문에 없지만 판정에 필요한 정보는 Unknown으로 적는다.
이 단계의 진술은 검증된 사실이 아니다.

### Step 2. 근거 확인

진술마다 근거를 찾고 §7.2로 Claim Status를 정한다.

- 근거 종류: Code / JIRA·Issue / FLA / HLD·MSC / Log / PR·CL·Commit
- 근거마다 위치와 Scope 위치(IN / OUT)를 적는다. Scope 위치를 정할 수 없는 근거는 OUT으로 취급한다.
- 코드 근거는 파일, 심볼(또는 라인), CL을 함께 적는다. CL을 특정하려면 Release/Branch가 필요하다.
- 근거를 찾지 못하면 `NO_EVIDENCE`로 두고 추론으로 메우지 않는다.
- Evidence 탐색은 Review Scope 안으로 제한한다. Scope 밖 Evidence가 이미 입력/검색 결과로 발견된 경우 참고는 가능하지만 Gotcha Structure나 Applicability를 생성·보강하는 근거로 사용하지 않는다.

### Step 3. 구조화와 적용범위

- Gotcha Structure(조건 / 함정 / 관측 증상 / 올바른 규칙 / 제외 조건)는 진술과 근거로만 채운다. 없으면 `UNKNOWN`.
- Applicability는 진술·근거가 직접 뒷받침하는 최소 범위이며, Resolved Scope의 부분집합이어야 한다.
  - Mode·RAT: §1 입력값을 기본으로 하되, 진술·근거가 더 좁히면 그에 따른다. `ANY`는 진술이나 근거가 모드 무관임을 보일 때만 쓴다.
  - Folder/File: 기본값이 없다. 진술·근거가 가리키는 파일·폴더만 적고, 없으면 `UNKNOWN`. Include 목록을 그대로 옮기지 않는다.

### Step 4. Confidence

§7.3으로 정한다.

### Step 5. 비교 집합 확정

§7.1로 기존 Knowledge를 검색·분류한다.

- **기존 Knowledge/KB 검색만** 넓게 한다(제외 경로만 뺀다). Source Code/Log/HLD/JIRA 등 Evidence 탐색 범위를 넓히라는 의미가 아니다. Scope 밖 KB 항목을 찾는 것은 Scope 확장이 아니며, 찾은 항목은 분류만 한다.
- 비교는 `IN_SCOPE`와 `SCOPE_UNKNOWN`만 한다.
- `OUT_OF_SCOPE`는 관련성이 높을 때 [Out-of-Scope References]로 보고한다.

### Step 6. 매칭 판정

비교 집합 안에서만 §7.4로 판정한다.

### Step 7. 권고 조치

§7.5로 조치를 정한다. 모든 항목의 조치를 모아 §9에 따라 [Update Preview]를 만든다.

---

## 7. 판정 기준

### 7.1 기존 Knowledge Scope 분류

세 축이 모두 겹쳐야 Scope 안이다.

- Mode: 같은 Mode이거나 한쪽이 `ANY` (CUSTOM은 §5-6)
- RAT: 같은 RAT이거나 한쪽이 `COMMON` (리뷰 RAT가 UNKNOWN이면 §5-5)
- 경로: 항목의 경로가 포함 경로 안에 있거나, 포함 경로의 상위 폴더다

| 분류 | 기준 | 처리 |
|---|---|---|
| `IN_SCOPE` | 세 축 모두 겹침 | 비교 |
| `OUT_OF_SCOPE` | 한 축이라도 명확히 겹치지 않음 | 비교 제외, 관련성이 높으면 보고 |
| `SCOPE_UNKNOWN` | 명확히 어긋나는 축은 없지만, 태그 누락·표기 대응 불가로 판단할 수 없는 축이 있음 | 비교 포함, 자동 병합·수정 금지 |

### 7.2 Claim Status

| 상태 | 기준 |
|---|---|
| `CONFIRMED` | Scope 안 근거가 진술을 직접 뒷받침하고 위치가 고정됨 (코드는 파일·심볼 또는 라인·CL, 그 외는 JIRA 키·로그 파일과 시각 등 다시 확인 가능한 위치) |
| `WEAK_SUPPORT` | 뒷받침 근거가 Scope 밖(`OUT_OF_SCOPE`)이거나 위치가 고정되지 않음(`UNPINNED`) |
| `NO_EVIDENCE` | 근거를 찾지 못함 |
| `CONTRADICTED` | 근거가 진술과 반대 |

### 7.3 Confidence

| 등급 | 기준 |
|---|---|
| `VERIFIED` | 조건·함정·올바른 규칙이 모두 채워져 있고, 해당 진술이 모두 `CONFIRMED`이며, `CONTRADICTED`가 없음 |
| `PARTIAL` | `CONTRADICTED`가 없고, `CONFIRMED` 또는 `WEAK_SUPPORT`가 하나 이상이지만 `VERIFIED` 기준을 채우지 못함 |
| `UNVERIFIED` | 모든 진술이 `NO_EVIDENCE`이거나, `CONTRADICTED`가 하나라도 있음 |

Scope 밖 근거만으로는 `VERIFIED`가 될 수 없다.

### 7.4 매칭 판정

| 판정 | 기준 |
|---|---|
| `DUPLICATE` | 조건·함정·올바른 규칙이 같고, 기존 항목의 적용범위가 신규 후보의 적용범위를 포함함 |
| `ENHANCEMENT` | 조건·함정이 같고, 신규 후보가 조건 구체화·관측 증상·올바른 규칙 보완(모순 없음)·적용범위 확장(Resolved Scope 안)을 더함 |
| `CONFLICT` | 적용범위가 겹치는데 함정 또는 올바른 규칙이 서로 모순됨 |
| `NEW` | 위에 해당하는 기존 항목이 없음 |

- 신규 후보 Applicability의 Mode / RAT / Folder/File 중 매칭에 필요한 축이 `UNKNOWN`이면 `DUPLICATE` 또는 `ENHANCEMENT`를 확정하지 않는다. 잠정 판정 뒤에 `(APPLICABILITY_UNKNOWN)`을 붙이고 `HOLD`한다.
- `SCOPE_UNKNOWN` 항목과 매칭되면 판정 뒤에 `(SCOPE_UNKNOWN)`을 붙인다.
- 여러 항목과 매칭되면 항목별로 모두 적는다.

### 7.5 권고 조치

| 조건 | 조치 |
|---|---|
| `NEW` + `VERIFIED` | `CREATE` |
| `NEW` + `PARTIAL` | `CREATE` 가능 — Confidence=`PARTIAL` 명시 |
| `NEW` + `UNVERIFIED` | `HOLD` — Tacit Candidate로만 유지, Canonical Gotcha 생성 금지 |
| `DUPLICATE` | `NO_ACTION` — 새 근거가 있으면 근거 추가로 `UPDATE` |
| `ENHANCEMENT` | `UPDATE` — 대상 KB ID와 변경 전/후 필수 |
| `CONFLICT` | `HOLD` — 자동 해소 금지, 양쪽 진술·근거를 나란히 제시 |
| 판정에 `(SCOPE_UNKNOWN)` 또는 `(APPLICABILITY_UNKNOWN)` | `HOLD` — Scope/Applicability 확인 필요 |
| `CONTRADICTED` 진술 포함 | 판정과 무관하게 `HOLD` |

여러 조건에 해당하면 `HOLD`가 우선한다.

---

## 8. 출력 형식

```text
[Scope Summary]

Mode:              (CUSTOM이면 정의 포함)
Domain:
RAT:
Path Base:
Release/Branch:

Resolved Scope:
- Scope Source: §2.1 OPTION_SLTE_DISABLE / §2.2 OPTION_SLTE_ENABLE / §2.3 CUSTOM
- Additional Scope 적용: YES / NO
- 포함 경로:
- 제외 경로:
- 우선순위 적용 지점:
- SCOPE_CONFLICT: 없음 / 내용
- KB 태그 표기 대응:   (필요 시)


[Gotcha Review: G-01]          ← 입력 항목마다 반복

Title:

Original Tacit Knowledge:      (원문 그대로)
Source:

Stated Claims:
- C-01:

Unknown / Needs Verification:
-

Evidence:
- E-01: 종류 | 위치 | Scope: IN / OUT | 관련 진술: C-01

Claim Status:
- C-01: CONFIRMED / WEAK_SUPPORT(OUT_OF_SCOPE·UNPINNED) / NO_EVIDENCE / CONTRADICTED

Gotcha Structure:              (진술·근거로만 채움, 없으면 UNKNOWN)
- 조건:
- 함정:
- 관측 증상:
- 올바른 규칙:
- 제외 조건:

Applicability:                 (최소 범위, Resolved Scope의 부분집합)
- Mode: OPTION_SLTE_DISABLE / OPTION_SLTE_ENABLE / ANY / CUSTOM(정의) / UNKNOWN
- RAT: LTE / NR / COMMON / UNKNOWN
- Folder/File:
- 뒷받침: C-/E- ID

Confidence:
- VERIFIED / PARTIAL / UNVERIFIED — 사유

Comparison Set:                (검색에 걸린 항목만)
- IN_SCOPE: KB ID 목록
- SCOPE_UNKNOWN: KB ID 목록 (누락된 태그)

Existing Knowledge Match:
- 판정: NEW / DUPLICATE / ENHANCEMENT / CONFLICT   (해당 시 + SCOPE_UNKNOWN)
- 대상 KB ID:
- 같은 점 / 다른 점:

Recommended Action:
- CREATE / UPDATE / NO_ACTION / HOLD — 사유


[Out-of-Scope References]

- Path / KB ID:
- Reason:
- Suggested action:


[Update Preview]

Preview ID:
- G-01 | 조치 | 대상 KB ID (현재 버전) | 변경 요약

승인 방법: "승인: G-01, G-03" 또는 "승인: 전체 <Preview ID>"
```

---

## 9. Update Guard

`l1sw-dev-knowledge`에 실제로 반영하기 전에 반드시 [Update Preview]를 먼저 제공한다.

1. Preview에는 Preview ID(예: `PV-YYYYMMDD-HHMM`), 항목별 조치, 대상 KB ID와 현재 버전(또는 최종 수정 시각), 변경 요약을 넣는다. `UPDATE`는 변경 전/후를 함께 보인다.
2. 승인은 항목 ID를 명시한 메시지로만 인정한다.
   - "승인: G-01, G-03" 또는 "승인: 전체 <Preview ID>"
   - "좋네요", "진행" 같은 표현은 승인으로 보지 않고 대상 ID를 되묻는다.
3. 승인된 항목만 반영한다. `HOLD` 항목은 사용자가 조치를 지정해 승인할 때만 반영한다(예: "승인: G-02 CREATE").
4. Preview 이후 §1–§3 입력이 바뀌었거나 대상 KB 항목의 버전이 달라졌으면 그 Preview는 무효다. 반영하지 말고 다시 Preview한다.
5. 승인 전에는 신규 Gotcha 생성, 기존 Knowledge 수정, Scope 변경을 하지 않는다.

---

## 10. 실행 요청

위 입력과 규칙으로 Gotcha/암묵지를 검토하라.
§4 절대 규칙 안에서 판단이 갈리면 아래 순서로 우선한다.

1. 사용자가 §2에 정의한 SLTE Mode별 Folder/File Scope 준수
2. Legacy / SLTE 구조 혼용 방지
3. Scope 밖 Knowledge/Evidence의 오적용 방지
4. 누락 방지 — 태그가 불완전한 기존 항목도 비교에서 빼지 않는다
5. 중복 / 보강 / 충돌의 정확한 구분

---

## 변경 이력

> 문서 관리용 섹션이다. 검토 실행 지시가 아니다.

| 버전 | 일시 | 내용 |
|---|---|---|
| v1.0 | 2026-10-08 | 최초 작성 |
| v1.1 | 2026-10-08 09:01 KST | v1.0 리뷰 반영 (P0 2건, P1 5건, P2 2건) |
| v1.2 | 2026-10-08 | SLTE Mode별 사용자 편집 Scope Map + v1.1 리뷰 보강 |

### v1.1 반영 내역

| 리뷰 ID | 변경 | 위치 |
|---|---|---|
| P0-1 | 기존 Knowledge를 IN_SCOPE / OUT_OF_SCOPE / SCOPE_UNKNOWN으로 분류해 비교 집합을 확정한 뒤 매칭하도록 절차 순서 변경. 검색은 제외 경로만 빼고 넓게 | §6 Step 5–6, §7.1 |
| P0-2 | 리뷰 Scope와 Gotcha 적용범위를 분리하고 최소 범위 원칙 명시 | 목적, §4-7, §6 Step 3 |
| P1-1 | Scope 해석 규칙 신설(우선순위, SCOPE_CONFLICT, Path Base, 하위 폴더 포함, 와일드카드 미사용, 입력 표식·빈 칸 시 중단). 입력 칸의 예시 경로 제거 | §1, §2, §5, §6 Step 0 |
| P1-2 | FACT를 Stated Claims로 변경. 사실 여부는 근거 확인 후 Claim Status로 판정 | §6 Step 1–2, §8 |
| P1-3 | 근거의 Scope 위치·CL 기록, Claim Status·Confidence 기준 정의, Scope 밖 근거로 VERIFIED 금지. INSUFFICIENT_EVIDENCE를 매칭 판정에서 제거 | §4-8, §6 Step 2, §7.2–7.3 |
| P1-4 | Applicable Mode에 ANY 추가, CUSTOM_DEFINITION 필수화, Mode 표기를 OPTION_SLTE_* 형식으로 통일 | §1, §5-5, §6 Step 3, §8 |
| P1-5 | 입력 항목 ID(G-xx), 대상 KB ID, Preview ID, 승인 형식, Preview 무효 조건 추가 | §3, §8, §9 |
| P2-1 | 절대 규칙과 판단 우선순위 분리 | §4, §10 |
| P2-2 | Gotcha Structure(조건 / 함정 / 관측 증상 / 올바른 규칙 / 제외 조건) 도입, Excluded Condition을 출력에 반영, 출처 필드 추가 | §3, §6 Step 3, §8 |

### 프롬프트 밖 확인 사항

- §9 Update Guard의 런타임 강제 — 스킬 쓰기 경로가 승인된 Preview ID 없는 쓰기를 거부하는지
- §5 해석 규칙의 resolver 이관 — 이관 후에는 §5-1에 따라 런타임 결과만 사용
- KB 태그 표기와 이 문서 enum의 대응표 확정

### v1.2 반영 내역

| 리뷰 ID | 변경 | 위치 |
|---|---|---|
| V12-1 | SLTE Disable/Enable/CUSTOM별 사용자 편집 Folder/File Scope Map 추가 | §2 |
| V12-2 | 선택 Mode + Additional Scope로 Resolved Scope 생성 | §2.5, §5, §6 Step 0 |
| V12-3 | `검색은 넓게`를 기존 Knowledge/KB 검색으로 한정, 전체 코드 재귀 분석 금지 | §4, §6 Step 5 |
| V12-4 | OUT_OF_SCOPE Evidence가 Gotcha Structure/Applicability를 오염시키지 못하도록 제한 | §4, §6 Step 2 |
| V12-5 | 신규 후보 Applicability가 UNKNOWN이면 자동 중복/보강 확정 금지 | §7.4–7.5 |
| V12-6 | `NEW + UNVERIFIED`는 Canonical Gotcha 생성 대신 HOLD | §7.5 |

### v1.2 사용자 수정 포인트

실제 사용 시 사용자가 주로 수정할 곳은 아래뿐이다.

1. §1 `MODE`, `RAT`, `Path Base`, `Release/Branch`
2. §2.1 `OPTION_SLTE_DISABLE` Folder/File 목록
3. §2.2 `OPTION_SLTE_ENABLE` Folder/File 목록
4. 필요 시 §2.3 `CUSTOM` 또는 §2.4 이번 검토용 Additional Scope
5. §3 검토할 암묵지 원문

특히 SLTE 구조가 바뀌거나 검토 대상 Legacy 파일이 추가/제거되면,
코드 분석 로직을 바꾸는 대신 §2의 목록을 사용자가 직접 갱신한다.

---

### v1.1 파일럿 검증 케이스

1. 같은 내용이 Legacy 태그 항목에만 있음(해당 경로는 Exclude 아님), `MODE = OPTION_SLTE_ENABLE` → `NEW`, Legacy 항목은 Out-of-Scope로만 보고. `DUPLICATE`면 실패
2. 같은 내용이 태그 없는 항목에 있음 → `(SCOPE_UNKNOWN)` 매칭 + `HOLD`. `NEW`면 실패
3. Include 3개 폴더, 근거는 파일 1개 → Applicability Folder/File = 그 파일
4. Shared 파일의 Gotcha, 근거가 모드 무관을 보임 → Mode = `ANY`
5. 근거가 Legacy JIRA뿐 → `VERIFIED` 불가, 최대 `PARTIAL`
