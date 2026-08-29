# l1-sam-fixer MCD CSV 5개 역할 확인 — 읽기 전용 객관식 프롬프트

## 목적

회사 Linux PC의 **최신 l1-sam-fixer 직접 실행 MCD 결과**에서 생성된 CSV 5개의 역할을 확인한다.

현재 확인된 기본 정보:

```text
최신 직접 실행 결과 예:
~/l1sw-private-skills/l1-sam-fixer/20260828_212929_MCD

현재 Fixer가 MCD 입력으로 사용한 CSV:
sam_metrics_mcd_detail_mfs_relations.csv

현재 확인된 relations CSV header 일부:
FromPath
ToPath
FromEntity
ToEntity

현재 확인된 유효 FromPath/ToPath pair:
333
```

이번 확인의 핵심 질문:

```text
1. CSV 5개는 각각 무엇을 담고 있는가?
2. 어떤 CSV가 cycle / dependency edge의 SSOT인가?
3. 어떤 CSV가 파일/클래스/함수/모듈/score 등의 보강 정보를 제공하는가?
4. 현재 사용 중인 relations CSV 하나만으로 MCD 기본 분석이 충분한가?
5. 다른 CSV를 추가로 JOIN하면 실제 보고서 품질이 좋아지는가?
6. 5개를 모두 읽어야 하는가, 아니면 필요한 CSV만 선택적으로 써야 하는가?
```

---

# 0. 절대 원칙

이번 작업은 **읽기 전용 확인**만 수행한다.

금지:

```text
파일 수정
Fixer 재실행
Job-list 조회
Job 재실행
Skill 수정
Git/GitHub write
CSV 내용 변경
임의 retry
```

허용:

```text
ls/find
head
python/csv 모듈을 이용한 header/row count/sample/stat 확인
grep
read-only JSON/HTML/CSV 확인
```

중요:

```text
CSV 전체를 LLM이 직접 읽지 말 것.
Python으로 header / row count / unique count / null count / sample만 추출한 뒤 판단할 것.
```

---

# 1. 최신 MCD run 경로 확인

최신 직접 실행 결과 디렉터리를 하나만 특정한다.

우선 확인 후보:

```text
~/l1sw-private-skills/l1-sam-fixer/
~/l1sw-parivate-skills/l1-sam-fixer/
```

오타 경로가 실제 환경에 존재하면 실제 존재하는 경로를 사용한다.

출력:

```text
QRUN=A   # 최신 MCD run 명확히 특정
QRUN=B   # 복수 run 중 최신 특정 불가
QRUN=C   # MCD run 없음
```

추가:

```text
RUN=<actual_path|NA>
```

---

# 2. CSV 파일 정확히 5개 확인

최신 run 하위의 MCD 관련 CSV를 확인한다.

출력:

```text
Q5=A   # 관련 CSV 정확히 5개
Q5=B   # 5개보다 많음
Q5=C   # 5개보다 적음
Q5=D   # 확인 불가
```

그리고 실제 파일명을 한 줄로 출력:

```text
CSV1=<filename>
CSV2=<filename>
CSV3=<filename>
CSV4=<filename>
CSV5=<filename>
```

파일명은 정렬하여 출력한다.

---

# 3. 각 CSV 기본 프로파일

각 CSV에 대해 아래 정보를 Python으로 확인한다.

```text
filename
row count (header 제외)
column count
exact header list
file size
```

출력 예:

```text
C1_ROWS=333 C1_COLS=8
C2_ROWS=...
C3_ROWS=...
C4_ROWS=...
C5_ROWS=...
```

그리고 header는 각 파일당 한 줄:

```text
C1_HDR=col1|col2|col3|...
C2_HDR=...
C3_HDR=...
C4_HDR=...
C5_HDR=...
```

---

# 4. 각 CSV의 구조적 키 후보 확인

각 CSV header에서 다음 종류의 key 후보가 있는지 확인한다.

```text
Cycle / CycleIndex / SCC / Group
FromPath / ToPath
FromEntity / ToEntity
SourceFile / TargetFile
src_path / dst_path
file / filepath / fullpath
class / classname
function / method / symbol
folder / directory
score / penalty / MCD / metric
count / weight / frequency
relation / dependency / edge
```

각 CSV별 출력:

```text
C1_KEY=<pipe separated detected keys|NONE>
C2_KEY=...
C3_KEY=...
C4_KEY=...
C5_KEY=...
```

---

# 5. 각 CSV의 sample 3행 확인

민감한 전체 데이터를 출력하지 말고, 각 CSV의 첫 3개 데이터 row만 구조 파악용으로 확인한다.

LLM 최종 출력에는 전체 row를 그대로 붙이지 말고 역할 판단에 필요한 형태만 요약한다.

예:

```text
C1_SAMPLE=path-pair + entity-pair + cycle-index
C2_SAMPLE=file + metric + score
...
```

---

# 6. relations CSV 여부 확인

현재 사용 중인 파일:

```text
sam_metrics_mcd_detail_mfs_relations.csv
```

이 파일이 실제 5개 중 존재하는지 확인한다.

출력:

```text
QREL=A   # 존재
QREL=B   # 파일명 변형으로 존재
QREL=C   # 없음
QREL=D   # 확인 불가
```

존재하면 다음도 확인:

```text
REL_ROWS=<integer|NA>
REL_FROMPATH=<present|absent>
REL_TOPATH=<present|absent>
REL_FROMENTITY=<present|absent>
REL_TOENTITY=<present|absent>
REL_CYCLE=<exact_cycle_column|NA>
```

---

# 7. relations CSV의 기본 MCD 분석 충분성

다음 조건을 각각 확인한다.

### 7-1. Cycle 식별 가능

```text
QREL_CYCLE=A   # cycle 식별 가능
QREL_CYCLE=B   # cycle 식별 불가
QREL_CYCLE=C   # 확인 불가
```

### 7-2. dependency edge 생성 가능

```text
QREL_EDGE=A   # FromPath/ToPath 또는 동등한 path pair로 가능
QREL_EDGE=B   # entity pair만 있고 path edge 불가
QREL_EDGE=C   # edge 정보 없음
QREL_EDGE=D   # 확인 불가
```

### 7-3. cycle member 생성 가능

```text
QREL_MEMBER=A   # path/entity + cycle id로 member 생성 가능
QREL_MEMBER=B   # 일부 정보 부족
QREL_MEMBER=C   # 생성 불가
QREL_MEMBER=D   # 확인 불가
```

### 7-4. 코드 분석 대상 path 생성 가능

```text
QREL_CODE=A   # 실제 file/path 기반 targeted 분석 가능
QREL_CODE=B   # entity만 있어 코드 path resolve 불충분
QREL_CODE=C   # 불가
QREL_CODE=D   # 확인 불가
```

---

# 8. 나머지 4개 CSV의 추가 가치 확인

relations CSV를 제외한 각 CSV가 아래 정보 중 무엇을 **추가로 제공**하는지 판단한다.

역할 코드:

```text
R1 = cycle topology
R2 = dependency edge/path pair
R3 = entity/class/function relation
R4 = file-level metrics
R5 = folder-level metrics
R6 = score/penalty/ranking
R7 = member/detail list
R8 = summary/aggregate
R9 = duplicate/derived of relations
R10 = 기타
```

각 CSV별:

```text
C1_ROLE=R2,R3,R7
C2_ROLE=R4,R6
...
```

---

# 9. relations CSV에 없는 컬럼 확인

각 다른 CSV의 header 중 `relations CSV`에는 없는 컬럼을 확인한다.

출력:

```text
C2_EXTRA=<colA|colB|...|NONE>
C3_EXTRA=...
C4_EXTRA=...
C5_EXTRA=...
```

중요:

단순히 컬럼명이 다르다고 추가 가치가 있다고 판단하지 말 것.

실제 sample/unique 값 구조를 보고 다음 중 하나로 분류한다.

```text
NEW_INFO     # relations에 없는 새로운 의미 정보
DERIVED      # relations로부터 계산 가능한 정보
DUPLICATE    # 사실상 중복
UNKNOWN
```

출력:

```text
C2_INFO=NEW_INFO
C3_INFO=DERIVED
...
```

---

# 10. CSV 간 JOIN 가능 key 확인

relations CSV와 나머지 CSV를 연결할 수 있는 key를 찾는다.

우선순위 후보:

```text
CycleIndex
FromPath/ToPath
Path/File
Entity
Class
Function
ID
```

각 CSV:

```text
C2_JOIN=<exact_column_or_columns|NONE>
C3_JOIN=...
C4_JOIN=...
C5_JOIN=...
```

그리고 실제 join 가능성:

```text
C2_JOINQ=A   # 안정적으로 join 가능
C2_JOINQ=B   # 부분 join 가능
C2_JOINQ=C   # 위험/중복 가능성 큼
C2_JOINQ=D   # join 불필요
C2_JOINQ=E   # 확인 불가
```

---

# 11. 중복/카디널리티 위험 확인

다른 CSV를 relations CSV와 JOIN할 때 row 폭증 가능성을 확인한다.

각 CSV의 join key에 대해:

```text
unique key count
duplicate key count
max rows per key
```

최종 판정:

```text
QJOINRISK=A   # 대부분 1:1 또는 안전한 N:1
QJOINRISK=B   # 1:N 있으나 제어 가능
QJOINRISK=C   # N:M 가능성 높음
QJOINRISK=D   # join 불필요
QJOINRISK=E   # 확인 불가
```

CSV별 필요하면:

```text
C2_CARD=1:1
C3_CARD=1:N
C4_CARD=N:M
```

---

# 12. HTML과 CSV 역할 중복 여부

최신 MCD HTML 또는 `sam-result.html`이 제공하는 정보와 CSV들의 역할을 비교한다.

최소 확인:

```text
fullpath
score_penalty
folder/dir
file/class
ranking
```

출력:

```text
QHTML=A   # HTML이 score/ranking/folder SSOT 역할
QHTML=B   # CSV가 해당 역할을 더 정확히 제공
QHTML=C   # HTML/CSV가 상호 보완
QHTML=D   # 확인 불가
```

추가:

```text
HTML_UNIQUE=<HTML에만 있는 핵심 정보|NONE|NA>
CSV_UNIQUE=<CSV에만 있는 핵심 정보|NONE|NA>
```

---

# 13. 각 CSV 최종 분류

각 CSV를 반드시 아래 하나로 분류한다.

```text
PRIMARY
  = MCD 기본 분석에 반드시 필요한 주 CSV

ENRICH
  = 기본 분석은 가능하지만 보고서 품질/세부 evidence 향상에 유용

OPTIONAL
  = 특정 요청 시에만 가치 있음

IGNORE
  = 중복/파생 정보라 기본 파이프라인에서는 불필요

UNKNOWN
  = 근거 부족
```

출력:

```text
C1_CLASS=PRIMARY
C2_CLASS=ENRICH
C3_CLASS=OPTIONAL
C4_CLASS=IGNORE
C5_CLASS=IGNORE
```

---

# 14. 현재 relations CSV 하나면 충분한지 최종 판정

반드시 하나만 선택:

```text
QSUFF=A
# relations CSV + HTML만으로
# cycle / dependency_edges / cycle_members / targeted code analysis / folder worst 기본 분석 충분

QSUFF=B
# 기본 MCD 분석은 충분하지만
# 파일/클래스/함수 또는 상세 evidence 품질 향상을 위해 다른 CSV 1개 이상 권장

QSUFF=C
# relations CSV만으로 기본 MCD 분석 자체가 불충분하며 다른 CSV가 필수

QSUFF=D
# 5개 CSV 모두 필요

QSUFF=E
# 확인 불가
```

---

# 15. 권장 CSV 사용 전략

반드시 하나 선택:

```text
QSTRAT=A
# relations CSV 1개를 Primary SSOT
# HTML을 score/folder SSOT
# 나머지 CSV는 사용하지 않음

QSTRAT=B
# relations CSV를 Primary SSOT
# HTML을 score/folder SSOT
# 다른 CSV 중 필요한 것만 선택적으로 enrichment

QSTRAT=C
# 2개 이상 CSV를 항상 고정 JOIN

QSTRAT=D
# 5개 CSV를 모두 항상 분석

QSTRAT=E
# 판단 불가
```

---

# 16. 가장 가치 있는 보강 CSV

`QSTRAT=B/C/D`인 경우만 선택한다.

```text
QBEST=A   # 보강 CSV 1개 명확
QBEST=B   # 보강 CSV 2개 이상 필요
QBEST=C   # 보강 필요 없음
QBEST=D   # 확인 불가
```

추가:

```text
BEST=<filename|filename1,filename2|NONE|NA>
WHY=<FILE|CLASS|FUNCTION|METRIC|SCORE|MEMBER|SUMMARY|OTHER|NA>
```

---

# 17. l1-sam-fixer 수정 영향 판정

CSV 역할 확인 결과를 기준으로 v0.2.46 이후 설계 방향을 판정한다.

```text
QIMPACT=A
# FromPath/ToPath mapping 수정만 하면 됨
# CSV 입력 구조 변경 불필요

QIMPACT=B
# mapping 수정 + optional enrichment CSV 지원 권장

QIMPACT=C
# 기본 입력 CSV 자체를 복수 CSV 구조로 변경해야 함

QIMPACT=D
# 현재 5개 CSV 모두 읽도록 재설계 필요

QIMPACT=E
# 확인 불가
```

---

# 18. 최종 출력 형식

설명문 없이 아래 형식 중심으로 출력한다.

```text
QRUN=A RUN=...
Q5=A
CSV1=...
CSV2=...
CSV3=...
CSV4=...
CSV5=...

C1_ROWS=... C1_COLS=...
C1_HDR=...
C1_KEY=...
C1_SAMPLE=...
C1_ROLE=...
C1_CLASS=...

C2_ROWS=... C2_COLS=...
C2_HDR=...
C2_KEY=...
C2_SAMPLE=...
C2_EXTRA=...
C2_INFO=...
C2_JOIN=...
C2_JOINQ=...
C2_CARD=...
C2_ROLE=...
C2_CLASS=...

C3_ROWS=... C3_COLS=...
C3_HDR=...
C3_KEY=...
C3_SAMPLE=...
C3_EXTRA=...
C3_INFO=...
C3_JOIN=...
C3_JOINQ=...
C3_CARD=...
C3_ROLE=...
C3_CLASS=...

C4_ROWS=... C4_COLS=...
C4_HDR=...
C4_KEY=...
C4_SAMPLE=...
C4_EXTRA=...
C4_INFO=...
C4_JOIN=...
C4_JOINQ=...
C4_CARD=...
C4_ROLE=...
C4_CLASS=...

C5_ROWS=... C5_COLS=...
C5_HDR=...
C5_KEY=...
C5_SAMPLE=...
C5_EXTRA=...
C5_INFO=...
C5_JOIN=...
C5_JOINQ=...
C5_CARD=...
C5_ROLE=...
C5_CLASS=...

QREL=A
REL_ROWS=...
REL_FROMPATH=present
REL_TOPATH=present
REL_FROMENTITY=present
REL_TOENTITY=present
REL_CYCLE=...

QREL_CYCLE=A
QREL_EDGE=A
QREL_MEMBER=A
QREL_CODE=A

QJOINRISK=...
QHTML=...
HTML_UNIQUE=...
CSV_UNIQUE=...

QSUFF=...
QSTRAT=...
QBEST=... BEST=... WHY=...
QIMPACT=...
```

---

# 19. 마지막 전달용 한 줄

반드시 마지막에 아래 형식으로 한 줄 출력한다.

```text
MCD5CSV: Q5=A C1=<filename>:<CLASS>/<ROLE> C2=<filename>:<CLASS>/<ROLE> C3=<filename>:<CLASS>/<ROLE> C4=<filename>:<CLASS>/<ROLE> C5=<filename>:<CLASS>/<ROLE> QREL_CYCLE=A QREL_EDGE=A QREL_MEMBER=A QREL_CODE=A QHTML=C QSUFF=B QSTRAT=B QBEST=A BEST=<filename> WHY=<role> QIMPACT=B
```

사용자는 이 `MCD5CSV:` 한 줄만 사외에 전달할 수 있어야 한다.

---

# 20. 판단 원칙

다음 원칙을 지킨다.

```text
1. 파일명만 보고 역할을 추정하지 말 것.
2. header + sample + row/cardinality 근거로 판단할 것.
3. relations CSV로 계산 가능한 파생 CSV는 PRIMARY로 올리지 말 것.
4. HTML에 이미 있는 score/ranking 정보를 CSV가 중복한다고 해서 필수로 판단하지 말 것.
5. 다른 CSV가 file/class/function evidence를 실질적으로 추가할 때만 ENRICH로 판단할 것.
6. 5개를 모두 읽는 것이 항상 더 좋다고 판단하지 말 것.
7. N:M JOIN 위험이 있으면 기본 pipeline에 무조건 병합하지 말 것.
8. 저사양 LLM 환경을 고려하여 CSV 원본 전체를 context에 넣지 말 것.
9. Python preprocessing으로 필요한 구조 정보만 추출할 것.
10. 현재 mapping bug와 CSV 역할 문제를 혼동하지 말 것.
```
