# l1-sam-fixer v0.2.61 사내 수동 검증 + 특정 폴더 MCD 개선 리포트 생성 프롬프트

## 목적

현재 사내 Linux PC에서 `l1-sam-fixer v0.2.61`을 사용한다.

현재 공식 SAM HTML MCD 점수는 **3.65**, 목표는 **3.66**이다.

이전에 야간/무인 실행으로 아래 분석이 일부 또는 전부 수행되었을 수 있다.

- `mcd_improvement_points.json`
- `mcd_readiness.json`
- `mcd_target_plan.json`
- 기본 MCD HTML/MD/Jira 보고서
- Job List state/result
- Dispatcher에서 참조한 최신 결과

이번에는 무인 Job을 처음부터 무조건 다시 실행하지 않는다.

**기존 최신 결과가 정상이라면 그대로 재사용하고, 부족하거나 실패한 단계만 수동으로 보완한 뒤 특정 폴더 MCD 개선 리포트를 작성한다.**

---

# 수행 원칙

1. **가장 최신 run을 사용하라.**
   - timestamp / run_id를 비교한다.
   - 과거 run과 최신 run을 섞지 않는다.

2. **기존 결과를 우선 재사용하라.**
   - 정상 결과가 있으면 동일 분석을 처음부터 반복하지 않는다.
   - 무인 Job을 다시 전체 수행하는 것은 금지한다.
   - 필요한 단계만 선택적으로 재실행한다.

3. 현재 공식 점수는 반드시:
   - `current_official_score = 3.65`
   - `target_score = 3.66`

4. 목표를 과거 값인 3.77 등으로 변경하지 않는다.

5. `probe_promoted_count = 0`을 Job 실패라고 단정하지 않는다.

6. Code Analyzer가 `INSUFFICIENT`인 경우:
   - 분석 미실행으로 단정하지 않는다.
   - evidence는 있으나 authoritative 조건을 통과하지 못했을 가능성을 먼저 확인한다.

7. topology 검증 없이 예상 gain을 부여하지 않는다.
   - `EDGE_RESOLVES_CYCLE`: 예상 gain 사용 가능
   - `EDGE_DOES_NOT_RESOLVE_CYCLE`: gain = 0
   - `TOPOLOGY_GAIN_UNVERIFIED`: 예상 gain 확정 금지

8. 실제 C++ Before / After를 추측하지 않는다.
   - 실제 source / symbol / line / authoritative evidence가 확인될 때만 코드 Before/After를 제안한다.
   - 근거가 부족하면 `ANALYSIS_REQUIRED`로 표시한다.

---

# STEP 1. v0.2.61 설치/활성 상태 확인

현재 설치된 `l1-sam-fixer`가 **v0.2.61**인지 먼저 확인하라.

확인 항목:

- 설치 경로
- 실제 호출되는 `SKILL.md`
- 버전
- 중복/legacy 설치 경로 여부
- 현재 실행 시 v0.2.61이 선택되는지

정상이라면 다음 단계로 이동한다.

비정상이라면 원인과 수정 명령만 제시하고 수정 후 계속 진행한다.

---

# STEP 2. 최신 기존 MCD 결과 탐색

사내 Linux PC의 `l1-sam-fixer` output/state 및 관련 영구 영역에서 가장 최근 MCD 결과를 찾는다.

우선 확인할 파일:

- `mcd_improvement_points.json`
- `mcd_readiness.json`
- `mcd_target_plan.json`
- 최신 기본 `mcd_report*.html`
- 최신 기본 `mcd_report*.md`
- 최신 기본 `mcd_report*.jira*`
- Job List state/result JSON
- Dispatcher 참조 결과

각 결과에 대해 다음을 표로 정리한다.

| 결과 | 존재 | 최신 timestamp/run_id | 정상 여부 | 재사용 가능 |
|---|---|---|---|---|
| improvement-points | | | | |
| readiness | | | | |
| target-plan | | | | |
| 기본 MCD report | | | | |

**중요:**
정상 결과가 있으면 다시 생성하지 말고 재사용한다.

---

# STEP 3. 기존 결과의 최소 유효성 검증

다음 핵심 값을 확인한다.

## Improvement Points

- `probe_promoted_count`
- `probe_candidates`
- `promotion_blocker_counts`
- quick-win 후보 수
- 후보별:
  - `cycle/work_unit`
  - `break_edge`
  - `edge_property`
  - `fix_pattern`
  - `risk`
  - file/class/type 정보

## Readiness

- `CURRENT_OFFICIAL_SCORE_REQUIRED`
- `CODE_EDGE_FACT_REQUIRED`
- `CODE_EDGE_FACT_NOT_AUTHORITATIVE`
- `PROBE_PROMOTION_RECOMMENDATION_ONLY`
- `HTML_UNMATCHED_PRESENT`
- `code_analyzer.status`
- `authoritative_fact_ready`
- `insufficient_files`
- `recommendation_ready`
- `quick_win_ready`

## Target Plan

입력 점수가 반드시 아래인지 확인:

- current = **3.65**
- target = **3.66**

확인:

- `score_model.status`
- `verification_error`
- `expected_current_score`
- `unexplained_score_delta`
- recommendations / candidates
- topology 상태
- 예상 gain
- 예상 수정 후 점수

다음 topology 상태별 후보 개수를 계산하라.

- `EDGE_RESOLVES_CYCLE`
- `EDGE_DOES_NOT_RESOLVE_CYCLE`
- `TOPOLOGY_GAIN_UNVERIFIED`

필요하다면 다음 값을 파생 계산해도 된다.

- `minimum_fix_set`
- `predicted_score_after_fix`
- `topology_resolved_candidate_count`
- `topology_zero_resolve_candidate_count`
- `topology_unverified_candidate_count`

단, JSON에 해당 필드명이 직접 없다는 이유만으로 Job 실패로 판정하지 않는다.

---

# STEP 4. 재실행 필요 여부 판단

다음 기준으로 처리한다.

## Case A — 기존 결과 정상

아래가 충족되면 전체 재실행하지 않는다.

- 최신 improvement-points 정상
- readiness 정상/해석 가능
- target-plan current=3.65, target=3.66
- topology 결과 확인 가능

→ **STEP 5로 바로 이동**

## Case B — 일부 결과만 문제

예:

- improvement-points만 누락
- readiness만 과거 run
- target-plan의 target score가 잘못됨

→ **문제 있는 단계만 재실행**

## Case C — 입력 SAM 결과 자체가 바뀜

현재 SAM CSV/HTML이 이전 run 이후 변경된 것이 확인되면:

→ 필요한 MCD 분석부터 다시 수행

단, 이유를 먼저 설명한다.

---

# STEP 5. 기본 MCD 보고서 확인

가장 최신 정상 기본 MCD 보고서를 읽는다.

다음을 확인한다.

1. 현재 MCD
2. Worst Folder Top 10
3. Worst Cycle
4. Problem File
5. 주요 Break Edge
6. Fix Pattern
7. Risk
8. 예상 Gain
9. Diagnostics
10. HTML unmatched count

현재 알려진 참고값:

- 공식 MCD = 3.65
- 목표 MCD = 3.66
- cycle 수 = 26
- CSV unmatched = 0
- HTML unmatched = 35

값이 실제 최신 결과와 다르면 **실제 최신 결과를 우선**하고 차이를 명시한다.

---

# STEP 6. 특정 폴더 선택

사용자가 지정한 폴더를 대상으로 한다.

## TARGET_FOLDER

`<여기에 분석할 폴더 경로 입력>`

예:

`SMPF/Protocol/Channel/L1`

사용자가 정확한 폴더명을 별도로 입력하지 않았다면,
기본 MCD 보고서의 Worst Folder Top 10을 보여주고 분석 후보를 제시한다.

단, 이미 사용자가 폴더를 지정했다면 다시 질문하지 않는다.

---

# STEP 7. 특정 폴더 MCD 개선 리포트 생성

자연어 요청과 동일한 의미로 수행한다.

> `<TARGET_FOLDER> 폴더 MCD 개선 리포트 작성해줘`

최신 정상 기본 MCD run을 재사용하고,
가능한 경우 새 SAM 전체 분석을 반복하지 않는다.

리포트는 최소 아래 구조로 작성한다.

---

## 01. Executive Summary

- Target Folder
- 현재 공식 MCD: 3.65
- 목표 MCD: 3.66
- 필요 Gain: +0.01
- 해당 Folder 관련 cycle 수
- scored cycle 수
- penalty 기여도
- quick-win 후보 수
- topology 검증 통과 후보 수
- 이 Folder만 수정해서 3.66 도달 가능한지

최종 판단:

- `HIGH POSSIBILITY`
- `CONDITIONAL`
- `INSUFFICIENT`
- `ANALYSIS_REQUIRED`

중 하나로 표시한다.

---

## 02. Folder MCD 현황

- Physical Folder
- 관련 Logical Group
- Folder Rank
- 관련 Cycle 수
- 해당 Folder의 penalty
- 전체 MCD에서의 영향
- 내부 dependency / cross-folder dependency 구분

---

## 03. Problem File Top N

각 파일별:

- Repository Relative Path
- Absolute Path
- File
- Class / Type / Symbol
- 관련 Cycle
- 관련 Edge 수
- penalty 영향
- evidence 수준

절대경로는 실제 filesystem에서 확인할 수 있는 경우만 기록한다.

추측 금지.

---

## 04. Worst Cycle Top N

각 Cycle별:

- cycle/work_unit
- 참여 file/class
- dependency chain
- 핵심 break candidate
- break_edge
- edge_property
- fix_pattern
- risk
- topology status
- 예상 gain

---

## 05. Recommended Fix Top 3

다음 기준으로 우선순위화한다.

1. `EDGE_RESOLVES_CYCLE`
2. LOW risk
3. 수정 파일 수 최소
4. runtime behavior 변화 최소
5. authoritative evidence 우선
6. 예상 MCD gain이 큰 후보

각 후보:

- Candidate #
- Repository Path
- Absolute Path
- File
- Class / Function / Symbol
- Cycle
- Break Edge
- Fix Pattern
- Risk
- 수정 예상 파일 수
- 예상 Gain
- 현재 MCD
- 예상 수정 후 MCD
- 3.66 도달 여부

---

# STEP 8. Detailed Code Proposal

**동일 HTML/MD 보고서 후반부에 포함한다.**

각 Candidate별 다음 형식을 사용한다.

```text
[Candidate #]

Target Folder:
Repository Path:
Absolute Path:
File:
Class:
Function/Symbol:
Source Line:

Problem:
Dependency Chain:
Break Edge:
Edge Property:

Fix Pattern:
Risk:

Evidence:
- source:
- code-analyzer:
- topology:

[Before]
실제 코드에서 확인된 부분만 기재

[After]
실제 source/type/namespace가 확정된 경우에만 기재

[수정 내용]
- 무엇을 변경하는가
- 왜 edge가 끊기는가
- runtime behavior 영향
- build/ABI/API 영향
- 예상 side effect

[Topology Verification]
- EDGE_RESOLVES_CYCLE / EDGE_DOES_NOT_RESOLVE_CYCLE / TOPOLOGY_GAIN_UNVERIFIED

[Expected MCD]
Current Official MCD: 3.65
Expected Gain:
Predicted MCD After Fix:
Target 3.66 Reachable: YES / NO / CONDITIONAL

[Verification]
- Build
- UT
- 관련 regression test
- SAM 재측정
```

---

# STEP 9. Before / After 생성 안전 규칙

다음을 엄격히 지킨다.

## PATCH_READY_FOR_REVIEW

다음이 확인된 경우만 사용:

- 실제 source file 존재
- 실제 line 확인
- 정확한 class/type/function 확인
- dependency evidence 존재
- fix pattern이 source와 일치
- topology 검증 가능

## ANALYSIS_REQUIRED

다음 중 하나라도 해당하면 Before/After를 추측하지 않는다.

- source file 미확인
- class/type 미확인
- namespace 불확실
- line 불확실
- 실제 dependency 근거 부족
- Code Analyzer authoritative evidence 부족
- topology unverified

특히:

- header 이름만 보고 forward declaration type을 추측하지 않는다.
- include가 존재한다는 이유만으로 삭제 제안하지 않는다.
- `UNUSED include` 제거는 authoritative evidence가 있을 때만 제안한다.
- `simulated_resolved = 0` 후보에 cycle 전체 penalty gain을 부여하지 않는다.

---

# STEP 10. Cross-Folder Dependency 분석

대상 폴더 문제의 원인이 외부 폴더와 연결되어 있다면 반드시 표시한다.

예:

```text
Target Folder:
SMPF/Protocol/Channel/L1

Local File:
SMPF/Protocol/Channel/L1/A.cpp

External Dependency:
Common/B.hpp

cross_folder: true
```

다음을 구분한다.

- Target Folder 내부 수정만으로 해결 가능
- 외부 폴더 수정 필요
- 양쪽 수정 가능
- ownership 확인 필요

가능하면 **Target Folder 내부에서 해결 가능한 수정안을 우선**한다.

---

# STEP 11. 예상 MCD 계산

예상 MCD는 아래 조건을 만족하는 후보만 사용한다.

- topology status = `EDGE_RESOLVES_CYCLE`
- score model 해석 가능
- expected gain이 근거 있음

예:

```text
Current Official MCD = 3.650
Verified Expected Gain = +0.012
Predicted MCD After Fix = 3.662
Target = 3.660

Result = TARGET REACHABLE
```

단, 예상값은 공식 확정 점수가 아니다.

반드시:

> 최종 MCD는 실제 코드 수정 후 공식 SAM 재측정으로 확정해야 한다.

라고 기록한다.

---

# STEP 12. 산출물

가능하면 다음 파일을 생성한다.

### 사용자 보고서

- `mcd_report_folder_<safe_folder_name>.html`
- `mcd_report_folder_<safe_folder_name>.md`
- `mcd_report_folder_<safe_folder_name>.jira.md`

### 머신리더블

- `mcd_code_proposals_folder_<safe_folder_name>.json`

JSON에는 최소:

```json
{
  "target_folder": "",
  "current_official_score": 3.65,
  "target_score": 3.66,
  "candidates": [
    {
      "rank": 1,
      "repository_path": "",
      "absolute_path": "",
      "class": "",
      "symbol": "",
      "cycle": "",
      "break_edge": "",
      "fix_pattern": "",
      "risk": "",
      "proposal_status": "",
      "topology_status": "",
      "expected_gain": null,
      "predicted_score_after_fix": null,
      "before": "",
      "after": "",
      "verification_required": []
    }
  ]
}
```

형태의 정보를 포함한다.

---

# STEP 13. 최종 사용자 출력

작업 완료 후 긴 설명을 하지 말고 아래 형식으로 요약한다.

```text
[MCD 폴더 개선 리포트 완료]

Target Folder:
사용한 MCD Run:
Current MCD:
Target MCD:

기존 결과 재사용:
- improvement-points: YES/NO
- readiness: YES/NO
- target-plan: YES/NO

재실행한 단계:
- 없음 / 단계명

Topology Verified Candidate:
Quick-win Candidate:

1순위 수정 대상:
Repository Path:
Absolute Path:
Class/Symbol:
Break Edge:
Fix Pattern:
Risk:
Expected Gain:
Predicted MCD:

Code Proposal:
PATCH_READY_FOR_REVIEW / ANALYSIS_REQUIRED

3.65 → 3.66:
REACHABLE / CONDITIONAL / NOT VERIFIED

생성 파일:
- HTML:
- MD:
- Jira:
- JSON:

다음 1개 Action:
```

---

# 금지사항

- 무조건 전체 무인 Job부터 다시 돌리지 말 것.
- 정상 최신 결과를 버리고 처음부터 다시 분석하지 말 것.
- 과거 run과 최신 run을 혼합하지 말 것.
- 공식 현재 점수를 3.65 이외 값으로 임의 변경하지 말 것.
- 목표를 3.77로 변경하지 말 것.
- topology 미검증 후보를 실제 quick-win으로 확정하지 말 것.
- 실제 source 확인 없이 C++ Before/After를 작성하지 말 것.
- 파일 경로 / class / namespace / symbol을 추측하지 말 것.
- 예상 MCD를 실제 SAM 결과처럼 표현하지 말 것.
- `INSUFFICIENT`를 분석 미실행과 동일시하지 말 것.

---

# 최종 목표

이번 작업의 최종 목적은 단순한 MCD 분석 보고서 생성이 아니다.

**현재 공식 MCD 3.65를 3.66 이상으로 올리기 위해, 지정한 폴더에서 실제 C++의 어떤 파일/클래스/의존성을 최소한으로 변경해야 하는지 코드 기준으로 제안하고, 그 제안의 topology 근거와 예상 MCD 효과까지 검증 가능한 형태로 제공하는 것**이다.

정상적인 기존 결과가 있다면 반드시 재사용하고,
부족한 단계만 수동으로 보완한 후 최종 폴더 개선 리포트를 작성하라.
