# l1-sam-fixer v0.2.47 — score_matched_count=0 원인확인 초간단 프롬프트

## 목적

회사 Linux PC에서 최신 `l1-sam-fixer v0.2.47` 직접 실행 결과를 읽기 전용으로 확인한다.

현재 증상:

```text
score_matched_count = 0 / 333
ranking_basis = EDGE_COUNT_FALLBACK
```

즉 333개 MCD cycle은 존재하지만 `mcd.htm`의 `score_penalty`가 하나도 병합되지 않았다.

이번 확인 목표는 아래 중 **어디에서 끊기는지 정확히 분리**하는 것이다.

```text
1. mcd.htm에서 score_penalty 자체를 추출하지 못함
2. HTML에서는 score 333개를 추출했지만 cycle key가 없음
3. HTML cycle key와 CSV CycleIndex 값 형식이 다름
4. CSV 쪽 CycleIndex를 잘못 읽음
5. HTML parser가 다른 table/section을 보고 있음
6. score map은 정상인데 merge 단계에서 lookup 실패
7. 다른/stale HTML을 읽고 있음
```

---

# 0. 절대 원칙

읽기 전용만 수행한다.

금지:

```text
Fixer 재실행
파일 수정
Skill 수정
Job-list 조회
Git/GitHub write
임의 retry
```

허용:

```text
ls/find
grep
head
Python read-only parsing
HTML/CSV/JSON/log 확인
```

HTML 전체를 LLM context에 넣지 말고 Python/grep로 필요한 값만 추출한다.

---

# 1. 최신 run과 실제 HTML 확인

최신 직접 실행 MCD run을 하나만 특정한다.

그 run에서 실제 score 입력으로 사용된 HTML 파일을 확인한다.

출력 내부 확인 항목:

```text
RUN
HTML_FILE
HTML_EXISTS
HTML_SIZE
HTML_MTIME
```

특히 `mcd.htm`인지, 다른 `.html/.htm`인지 실제 사용 파일을 확인한다.

---

# 2. HTML에 score_penalty 문자열이 실제 존재하는지

대소문자 변형 포함:

```text
score_penalty
ScorePenalty
scorePenalty
score penalty
```

를 검색한다.

판정:

```text
H_SCORE=A   # score_penalty 계열 문자열 존재
H_SCORE=B   # score 개념은 있으나 다른 이름
H_SCORE=C   # score 관련 문자열 없음
H_SCORE=D   # 확인 불가
```

추가 내부 값:

```text
HTML_SCORE_TOKEN_COUNT=<integer>
```

---

# 3. HTML에서 실제 score 값 개수 추출

HTML parser가 실제로 cycle별 score row를 몇 개 찾는지 확인한다.

가능하면 현재 fixer parser와 동일 코드/함수를 read-only로 호출하되 파일 수정은 하지 않는다.

판정:

```text
H_PARSED=A   # score row 333개 또는 cycle 수와 거의 동일
H_PARSED=B   # 1개 이상이지만 333보다 적음
H_PARSED=C   # 0개
H_PARSED=D   # parser 호출 불가/확인 불가
```

내부 값:

```text
HTML_PARSED_SCORE_COUNT=<integer|NA>
```

---

# 4. HTML score row의 cycle key 확인

score row마다 어떤 key를 가지고 있는지 확인한다.

후보:

```text
CycleIndex
cycle_index
cycleIndex
Cycle
id
name
path
logical group
```

판정:

```text
H_KEY=A   # CycleIndex 계열 key 존재
H_KEY=B   # Cycle만 존재
H_KEY=C   # 다른 key만 존재
H_KEY=D   # score는 있으나 cycle key 없음
H_KEY=E   # 확인 불가
```

내부 값:

```text
HTML_KEY_NAME=<exact_name|NA>
HTML_KEY_SAMPLE=<1개 예시|NA>
HTML_SCORE_SAMPLE=<1개 예시|NA>
```

---

# 5. CSV CycleIndex 확인

실제 PRIMARY CSV:

```text
sam_metric_mcd_detail_mfs_relations.csv
```

또는 최신 run에서 선택된 primary CSV를 확인한다.

CSV의 cycle key를 확인한다.

판정:

```text
C_KEY=A   # CycleIndex 존재
C_KEY=B   # Cycle만 존재
C_KEY=C   # CycleIndex와 Cycle 둘 다 존재
C_KEY=D   # 다른 key
C_KEY=E   # 확인 불가
```

내부 값:

```text
CSV_KEY_NAME=<exact_name|NA>
CSV_CYCLE_COUNT=<unique count|NA>
CSV_KEY_SAMPLE=<최대 5개, comma separated|NA>
```

---

# 6. HTML key와 CSV key의 실제 교집합 계산

문자열 그대로 비교한 교집합과,
정규화 후 비교한 교집합을 각각 계산한다.

정규화 규칙:

```text
trim
"12.0" -> "12"
int-like numeric normalization
case normalization only for field name, not arbitrary value
```

내부 값:

```text
RAW_INTERSECTION=<integer>
NORMALIZED_INTERSECTION=<integer>
HTML_UNIQUE_KEYS=<integer>
CSV_UNIQUE_KEYS=<integer>
```

판정:

```text
K_MATCH=A   # normalized intersection = 333 또는 거의 전체
K_MATCH=B   # 일부만 일치
K_MATCH=C   # 0개
K_MATCH=D   # 확인 불가
```

---

# 7. HTML key 형식 확인

HTML cycle key sample 5개와 CSV cycle key sample 5개를 비교해서 형식을 분류한다.

판정:

```text
K_FMT=A   # 동일 숫자형
K_FMT=B   # HTML은 "Cycle 12" 같은 prefix 포함
K_FMT=C   # HTML은 hash/id 형식
K_FMT=D   # HTML은 logical path/group 형식
K_FMT=E   # CSV는 숫자형, HTML은 다른 식별체계
K_FMT=F   # 기타 명확한 형식 차이
K_FMT=G   # 확인 불가
```

---

# 8. 현재 fixer가 실제 생성한 score map 확인

최신 run output/evidence/debug JSON/log에서 score map이 존재하는지 확인한다.

가능한 항목:

```text
score_map
score_by_cycle
score_penalty_by_cycle
score_matched_count
ranking_basis
```

판정:

```text
S_MAP=A   # score map에 1개 이상 존재
S_MAP=B   # score map 필드 있으나 0개
S_MAP=C   # score map 자체 없음
S_MAP=D   # 확인 불가
```

내부 값:

```text
SCORE_MAP_COUNT=<integer|NA>
```

---

# 9. merge 직전 key 확인

가능하면 score merge 직전:

```text
cycle_id
cycle_index
work_unit cycle key
lookup key
```

중 실제 lookup에 쓰이는 값을 확인한다.

판정:

```text
M_KEY=A   # CycleIndex 사용
M_KEY=B   # Cycle 사용
M_KEY=C   # hash/work_unit_id 사용
M_KEY=D   # path/logical group 사용
M_KEY=E   # 다른 값 사용
M_KEY=F   # 확인 불가
```

내부 값:

```text
MERGE_KEY_NAME=<exact_name|NA>
MERGE_KEY_SAMPLE=<value|NA>
```

---

# 10. stale/wrong HTML 여부

현재 run이 읽은 HTML이 동일 SAM 실행 결과의 HTML인지 확인한다.

가능하면:

```text
run timestamp
HTML mtime
CSV mtime
artifact directory
report metadata
```

를 비교한다.

판정:

```text
STALE=A   # 동일 run의 HTML/CSV로 보임
STALE=B   # HTML이 이전/stale artifact
STALE=C   # HTML과 CSV run 혼재 가능성
STALE=D   # 확인 불가
```

---

# 11. 최종 원인 분류

반드시 하나만 선택한다.

```text
ROOT=A
# mcd.htm 자체에 score_penalty가 없거나 parser 대상 HTML이 잘못됨

ROOT=B
# HTML에 score는 있으나 현재 parser가 score row를 추출하지 못함

ROOT=C
# HTML score row는 추출되지만 HTML cycle key가 없거나 잘못 추출됨

ROOT=D
# CSV CycleIndex 선택/추출 문제

ROOT=E
# HTML key와 CSV CycleIndex가 서로 다른 식별체계/형식이라 join 불가

ROOT=F
# key 정규화 문제 (예: 12 vs "Cycle 12", 12.0 등)

ROOT=G
# score map 생성은 정상이나 merge lookup key가 잘못됨

ROOT=H
# stale/wrong HTML과 CSV가 섞임

ROOT=I
# 복수 문제

ROOT=J
# 증거 부족
```

우선순위 예:

```text
H_SCORE=C
→ ROOT=A

H_SCORE=A AND H_PARSED=C
→ ROOT=B

H_PARSED=A/B AND H_KEY=D
→ ROOT=C

C_KEY에 CycleIndex가 있는데 실제 merge는 Cycle 사용
→ ROOT=D 또는 G

RAW_INTERSECTION=0 AND NORMALIZED_INTERSECTION>0
→ ROOT=F

NORMALIZED_INTERSECTION=0
AND HTML/CSV key 체계 자체가 다름
→ ROOT=E

S_MAP=A
AND score_matched_count=0
AND merge lookup key가 CycleIndex가 아님
→ ROOT=G

STALE=B/C
→ ROOT=H
```

---

# 12. 사용자가 전달할 최종 출력

**상세 설명은 출력하지 말고 마지막 한 줄만 출력한다.**

형식:

```text
MCDSCORE: H_SCORE=<A/B/C/D> H_PARSED=<A/B/C/D> N=<HTML_PARSED_SCORE_COUNT> H_KEY=<A/B/C/D/E> HK=<HTML_KEY_NAME> C_KEY=<A/B/C/D/E> CK=<CSV_KEY_NAME> CU=<CSV_CYCLE_COUNT> RAW=<RAW_INTERSECTION> NORM=<NORMALIZED_INTERSECTION> K_FMT=<A/B/C/D/E/F/G> S_MAP=<A/B/C/D> SM=<SCORE_MAP_COUNT> M_KEY=<A/B/C/D/E/F> MK=<MERGE_KEY_NAME> STALE=<A/B/C/D> ROOT=<A/B/C/D/E/F/G/H/I/J>
```

예시:

```text
MCDSCORE: H_SCORE=A H_PARSED=A N=333 H_KEY=B HK=Cycle C_KEY=C CK=CycleIndex CU=333 RAW=0 NORM=0 K_FMT=E S_MAP=A SM=333 M_KEY=A MK=CycleIndex STALE=A ROOT=E
```

사용자는 이 한 줄만 복사해 전달하면 된다.

---

# 13. 중요

- 원인 추측 금지
- 실제 파일/파서 결과 기준으로만 판정
- Fixer 재실행 금지
- 수정 금지
- 질문 금지
- 사용자가 직접 숫자/파일명을 입력하지 않아도 되게 AI가 자동 확인
- 최종 출력은 반드시 `MCDSCORE:` 한 줄
