# l1-sam-fixer v0.2.47 — MCD score match 0 원인분석 및 수정방향 제안 프롬프트

## 1. 목적

회사 Linux PC의 실제 데이터와 `l1-sam-fixer v0.2.47` 코드를 기준으로,
현재 발생 중인 아래 문제의 **근본 원인(Root Cause)** 을 분석하고
**v0.2.48 수정 방향**을 제안해줘.

현재 증상:

```text
score_matched_count = 0
ranking_basis = EDGE_COUNT_FALLBACK
```

현재까지 외부 확인으로 확보된 사실:

```text
[HTML]
H_SCORE=A
H_PARSED=A
HTML score record count = 49
HTML score key = cycle_index
score_map count = 49

[CSV / merge]
mfs_relations 쪽 현재 확인 key = Key
unique = 25
HTML cycle_index ↔ CSV Key:
RAW intersection = 0
NORMALIZED intersection = 0

[merge code]
현재 merge lookup key = cycle_index

[artifact]
stale HTML 아님
동일 run artifact로 확인됨

[기타]
mfs_relations 쪽 relation row 수로 보이는 값 = 333
```

즉 현재 가장 중요한 의문은 다음이다.

```text
HTML score 49개
CSV unique Key 25개
mfs relation 333개

이 세 숫자가 서로 다른 granularity인지,
어떤 파일/키를 통해 연결해야 하는지
실제 데이터와 코드로 확인해야 한다.
```

---

# 2. 이번 작업 범위

이번 작업은 **분석 + 수정방향 제안만 수행**한다.

절대 금지:

```text
파일 수정
Skill 수정
Fixer 재실행
Git/GitHub write
Job-list 조회/실행
자동 patch 적용
버전 변경
패키지 재생성
```

허용:

```text
read-only 파일 확인
grep/head/find
Python을 이용한 CSV/HTML 구조 분석
현재 v0.2.47 코드 읽기
최신 실행 산출물/JSON/log 읽기
간단한 read-only 비교 script 실행
```

---

# 3. 저사양 LLM 실행 원칙

이 작업은 저사양 사내 LLM에서도 수행 가능해야 한다.

반드시 다음 방식으로 진행:

```text
1. HTML 전체를 context에 넣지 말 것.
2. CSV 전체를 context에 넣지 말 것.
3. Python으로 먼저 구조/통계/교집합/cardinality를 계산할 것.
4. LLM에는 Python이 추출한 요약 정보만 전달할 것.
5. 코드도 전체 파일을 한 번에 읽지 말고 관련 함수 중심으로 확인할 것.
```

특히 Python으로 다음을 먼저 계산:

```text
- 각 CSV header
- row count
- unique count
- candidate join key
- intersection
- cardinality
- sample 3~5개
```

---

# 4. 확인 대상

## 4.1 최신 MCD run

최신 직접 실행 결과 디렉터리를 하나 특정한다.

우선 후보:

```text
~/l1sw-private-skills/l1-sam-fixer/
~/l1sw-parivate-skills/l1-sam-fixer/
```

실제 존재하는 경로 기준으로 판단한다.

---

## 4.2 HTML

실제 score 입력으로 사용된 HTML:

```text
mcd.htm
```

또는 실제 run에서 사용된 `.htm/.html`.

확인할 것:

```text
score_penalty
cycle_index
cycle/group 구조
TOP/HAL
TOP/L1C
score record count
```

---

## 4.3 CSV 5개

현재 알려진 CSV 역할:

```text
sam_metric_mcd.csv
  OPTIONAL / summary aggregate

sam_metric_mcd_detail_all_relations.csv
  ENRICH / relation + entity

sam_metric_mcd_detail_cycle.csv
  ENRICH / cycle topology + member

sam_metric_mcd_detail_mfs_relations.csv
  PRIMARY / physical dependency relation

sam_metric_mcd_detail_modules.csv
  OPTIONAL / module/folder aggregate
```

실제 파일명은 run에서 확인할 것.

---

## 4.4 v0.2.47 코드

다음 기능과 관련된 실제 코드를 우선 확인:

```text
HTML score parser
cycle_index 추출
score_map 생성
CSV header resolve
Cycle/CycleIndex/Key 선택
mfs_relations parser
cycle.csv parser
score merge
score_matched_count 계산
ranking_basis 결정
Worst Top10 생성
TOP/HAL, TOP/L1C handling
logical vs physical path handling
```

---

# 5. 반드시 답해야 할 핵심 질문

## Q1. 333은 실제로 무엇인가?

현재 333이 정말 cycle 수인지 확인한다.

가능한 후보:

```text
cycle count
relation row count
edge count
member count
work unit count
기타
```

반드시 실제 데이터 근거로 답한다.

---

## Q2. HTML의 49개 score record는 무엇인가?

`mcd.htm`의:

```text
cycle_index
score_penalty
```

49개가 무엇을 의미하는지 확인한다.

가능한 후보:

```text
MCD cycle
SCC
logical group relation
module pair
aggregated cycle
기타
```

파일 구조/HTML 구조에 근거하여 판단한다.

---

## Q3. HTML cycle_index 49개와 직접 대응되는 CSV는 무엇인가?

CSV 5개 전체의 모든 합리적 column에 대해
HTML `cycle_index` 49개와 교집합을 자동 계산한다.

반드시 표로 정리:

```text
CSV
candidate column
unique count
raw intersection
normalized intersection
match ratio
```

특히:

```text
sam_metric_mcd_detail_cycle.csv
```

를 우선 확인하되,
파일명만 보고 정답으로 가정하지 말 것.

---

## Q4. cycle.csv가 score join의 중간 SSOT인가?

다음 구조가 실제 데이터상 맞는지 검증한다.

```text
mcd.htm
  score_penalty + cycle_index
        ↓
sam_metric_mcd_detail_cycle.csv
  cycle topology / members
        ↓
sam_metric_mcd_detail_mfs_relations.csv
  FromPath / ToPath
  FromEntity / ToEntity
        ↓
physical source path / file
```

맞다면:

```text
어떤 column ↔ 어떤 column
```

으로 JOIN해야 하는지 정확히 제시한다.

아니라면 실제 올바른 구조를 제시한다.

---

## Q5. mfs_relations의 `Key` 25개는 무엇인가?

현재 확인된:

```text
CSV key = Key
unique = 25
```

의 의미를 실제 sample/header/cardinality로 분석한다.

다음 중 무엇인지 확인:

```text
cycle key
module key
relation type
SCC key
group key
aggregate key
기타
```

HTML cycle_index와 직접 JOIN하면 안 되는 이유가 있다면 명확히 설명한다.

---

## Q6. 실제 score merge 실패 지점은 어디인가?

v0.2.47 코드 기준으로 다음 파이프라인을 추적한다.

```text
HTML parsing
→ score_map 생성
→ cycle key normalize
→ CSV/cycle work unit key 생성
→ lookup
→ score_matched_count
→ ranking_basis
```

각 단계별 실제 값 수를 가능한 범위에서 확인:

```text
HTML score rows
score_map entries
cycle/work units
lookup attempts
lookup hits
lookup misses
```

그리고 **최초로 의미가 어긋나는 지점**을 특정한다.

---

# 6. TOP/HAL, TOP/L1C 문제도 함께 확인

원본 HTML 자체에 다음과 같이 보인다.

```text
TOP(3)
  HAL
  L1C
```

그리고 예:

```text
TOP/HAL -> TOP/L1C : 45
TOP/L1C -> TOP/HAL : 625
```

실제 source tree에는 `TOP`이라는 physical folder가 없다.

실제 예:

```text
HAL/MODEM/CmdHdlr
  LTE
  NR
    RF_BLOCK

L1C/Common
  TxMngr
```

따라서 다음을 확인한다.

```text
1. TOP/HAL, TOP/L1C가 HTML logical hierarchy인지
2. 실제 filesystem path로 사용하면 안 되는지
3. score/cycle grouping과 TOP logical hierarchy가 연관되는지
4. physical path는 mfs_relations의 FromPath/ToPath를 SSOT로 쓰는 게 맞는지
```

현재 권장 가설:

```text
HTML:
logical group / score / ranking

cycle.csv:
cycle topology / member

mfs_relations.csv:
physical relation / FromPath / ToPath
```

하지만 반드시 실제 데이터로 검증할 것.

---

# 7. FromPath / ToPath 기존 이슈 재확인

이전 v0.2.46에서 확인된 문제:

```text
CSV에는:
FromPath
ToPath
FromEntity
ToEntity

모두 존재

하지만 mapping이:
FromEntity
ToEntity

를 먼저 선택해서
dependency_edges=0
cycle_members=0
```

v0.2.47에서 이 문제가 실제로 수정됐는지도 함께 확인한다.

확인:

```text
effective source column
effective target column
dependency_edges count
cycle_members count
```

예상:

```text
FromPath / ToPath 사용
dependency_edges > 0
cycle_members > 0
```

score 문제와 이 문제를 서로 혼동하지 말 것.

---

# 8. 실제 데이터 모델 제안

분석 완료 후 MCD 데이터를 최소한 아래처럼 계층화해서 제안해줘.

예시 형식:

```text
L1. Logical MCD Layer
  source:
    mcd.htm
  key:
    ...
  contains:
    score_penalty
    TOP/HAL
    TOP/L1C
    ...

L2. Cycle Layer
  source:
    sam_metric_mcd_detail_cycle.csv
  key:
    ...
  contains:
    cycle/member
    ...

L3. Physical Relation Layer
  source:
    sam_metric_mcd_detail_mfs_relations.csv
  key:
    ...
  contains:
    FromPath
    ToPath
    FromEntity
    ToEntity
    ...

L4. Optional Enrichment
  all_relations.csv
  modules.csv
  sam_metric_mcd.csv
```

실제 데이터가 다르면 실제 구조로 바꾼다.

---

# 9. v0.2.48 최소 수정 방향 제안

수정은 실행하지 말고,
**최소 수정 포인트만 구체적으로 제안**한다.

반드시 포함:

```text
1. 수정 대상 파일
2. 수정 대상 함수
3. 현재 잘못된 가정
4. 수정할 logic
5. join key
6. fallback policy
7. fail-visible reason code
```

예:

```text
파일:
scripts/mcd_worst_report.py

함수:
build_score_map(...)
merge_score(...)
...

현재:
HTML cycle_index → mfs_relations generic Key 직접 join

수정:
HTML cycle_index → cycle.csv <actual column>
→ cycle member <actual key>
→ mfs_relations <actual key>
```

실제 코드에 맞게 정확히 작성한다.

---

# 10. fallback 정책 제안

score join 실패 시 조용히 fallback하지 않도록 설계한다.

현재:

```text
score_matched_count=0
→ EDGE_COUNT_FALLBACK
```

권장 여부를 검토하고,
다음처럼 fail-visible이 필요한지 판단한다.

예:

```text
MCD_SCORE_JOIN_UNRESOLVED
MCD_SCORE_JOIN_PARTIAL
MCD_SCORE_SOURCE_MISMATCH
```

권장 정책 예:

```text
score source 존재
AND parsed score > 0
AND matched score = 0
→ 단순 EDGE_COUNT_FALLBACK 처리 금지
→ explicit warning/reason code 출력
```

적절한 정책을 제안한다.

---

# 11. 회귀 테스트 제안

실제 회사 데이터 형태를 최소 fixture로 재현하는 테스트를 제안한다.

반드시 포함:

## Test A — score join

```text
HTML:
cycle_index + score_penalty

cycle.csv:
실제 matching key

mfs_relations.csv:
physical member/relation
```

검증:

```text
score_matched_count > 0
ranking_basis = SAM_SCORE_PENALTY
```

## Test B — granularity

```text
49 score cycles
333 relations
```

처럼 cycle과 relation row 수가 다를 때도 정상.

## Test C — FromPath 우선

```text
FromPath
ToPath
FromEntity
ToEntity
```

동시 존재 시:

```text
FromPath/ToPath 선택
```

## Test D — TOP logical group

```text
TOP/HAL
TOP/L1C
```

이 실제 physical folder Top10에 들어가지 않음.

## Test E — fail-visible

HTML score는 존재하지만 join 0이면:

```text
silent EDGE_COUNT_FALLBACK 금지
reason code 출력
```

---

# 12. 분석 결과의 신뢰도

각 결론을 아래로 구분한다.

```text
FACT
  실제 파일/코드에서 직접 확인

INFERENCE
  여러 사실을 기반으로 추론

UNKNOWN
  증거 부족
```

중요한 결론마다 FACT/INFERENCE/UNKNOWN을 표시한다.

---

# 13. 최종 출력 형식

최종 보고서는 아래 순서로 작성한다.

```text
1. 결론 요약
2. ROOT CAUSE
3. 333 / 49 / 25의 실제 의미
4. 실제 MCD 데이터 모델
5. HTML ↔ cycle.csv ↔ mfs_relations JOIN 관계
6. v0.2.47 코드의 잘못된 가정
7. v0.2.48 최소 수정 포인트
8. TOP/HAL / TOP/L1C 처리 원칙
9. fallback / reason code 정책
10. 필수 regression tests
11. 남은 UNKNOWN
```

---

# 14. 마지막 전달용 요약

보고서 맨 마지막에 반드시 아래 형식으로 작성한다.

```text
MCDROOT:
ROOT=<한 줄 핵심 원인>
HTML_SCORE=<count>/<key>
CYCLE_SSOT=<filename>:<column>
REL_SSOT=<filename>:<column(s)>
JOIN=<HTML key> -> <cycle key> -> <relation key>
GRANULARITY=<49와333의 의미>
TOP=<LOGICAL/PHYSICAL/UNKNOWN>
PATCH=<수정파일:함수 1~3개>
FALLBACK=<정책>
CONFIDENCE=<HIGH/MEDIUM/LOW>
```

예:

```text
MCDROOT:
ROOT=HTML cycle_index를 mfs_relations Key에 직접 join한 잘못된 granularity 가정
HTML_SCORE=49/cycle_index
CYCLE_SSOT=sam_metric_mcd_detail_cycle.csv:CycleIndex
REL_SSOT=sam_metric_mcd_detail_mfs_relations.csv:FromPath,ToPath
JOIN=cycle_index -> CycleIndex -> CycleMemberKey
GRANULARITY=49 cycle / 333 relation
TOP=LOGICAL
PATCH=mcd_worst_report.py:build_score_map,merge_cycle_score,build_physical_relations
FALLBACK=parsed_score>0 && matched=0이면 explicit error
CONFIDENCE=HIGH
```

사용자는 이 마지막 `MCDROOT:` 블록만 외부에 전달할 수 있어야 한다.

---

# 15. 중요

- 원인 추측만으로 결론 내리지 말 것.
- 반드시 실제 코드 + 실제 artifact + 실제 CSV/HTML 구조를 함께 볼 것.
- 333을 cycle 수라고 미리 가정하지 말 것.
- 49를 누락된 score라고 미리 가정하지 말 것.
- `cycle.csv`가 정답이라고 미리 가정하지 말 것.
- 5개 CSV 모두 강제 JOIN하는 방향을 기본값으로 제안하지 말 것.
- 가장 단순하고 안정적인 SSOT + selective enrichment 구조를 우선 검토할 것.
- 수정은 수행하지 말고 분석과 수정방향만 제안할 것.
