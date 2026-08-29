# l1-sam-fixer v0.2.45 MCD 추가 확인 — 원인분리 객관식 프롬프트

## 목적

회사 Linux PC에서 이미 수행한 `l1-sam-fixer v0.2.45`의 **최신 직접 실행 결과만 읽기 전용으로 확인**한다.

현재 1차 확인 결과는 다음과 같다.

```text
QVER=A
QOUT=A
QCSV=C SRC=FromPath DST=ToPath
QEDGE=B
QMEM=B
QERR=B
QEVID=F
QCODE=C
QBOUND=A
QBREAK=C
QCONS=A
QHASH=C
QUNRES=D
QAN=D
QTOP=B
QFILE=C
FINAL=C
```

핵심 확인 목표:

```text
FromPath / ToPath 열은 인식했는데
왜 dependency_edges / cycle_members가 비었는지

왜 동시에 MCD_EDGE_COLUMNS_UNRESOLVED가 남았는지

어느 단계에서 edge 정보가 소실되었는지
```

---

# 0. 절대 원칙

읽기 전용 확인만 수행한다.

금지:

```text
파일 수정
Fixer 재실행
Job-list 조회
Job 재실행
processed state 조회/삭제
Skill 수정
Git/GitHub write
임의 retry
```

추측 금지.

반드시 **실제 최신 실행 결과 / 로그 / JSON / CSV / report 내용에 존재하는 증거만** 사용한다.

---

# 1. 최신 실행 결과 경로

최신 MCD 직접 실행 결과의 기준 디렉터리를 하나만 특정한다.

출력:

```text
QRUN=A   # 최신 run 디렉터리 명확히 특정
QRUN=B   # 서로 다른 결과가 섞여 있어 특정 불가
QRUN=C   # run 단위 디렉터리 자체 없음
```

추가:

```text
RUN=<absolute_or_home_relative_path|NA>
```

---

# 2. 실제 입력 CSV 파일 특정

MCD edge parsing에 실제 사용된 CSV 파일을 확인한다.

출력:

```text
QIN=A   # 실제 입력 CSV 파일 명확히 특정
QIN=B   # 복수 CSV 중 어느 파일인지 불명확
QIN=C   # 입력 CSV 확인 불가
```

추가:

```text
CSV=<path_or_filename|NA>
```

---

# 3. 실제 CSV header 원문

입력 CSV의 **첫 header row 원문**에서 방향 열을 확인한다.

출력:

```text
QHDR=A   # 정확히 FromPath / ToPath 존재
QHDR=B   # 대소문자/공백/기호 차이 있는 변형
QHDR=C   # 다른 별칭
QHDR=D   # 실제 CSV에는 해당 방향 열 없음
QHDR=E   # 확인 불가
```

추가:

```text
HDR_SRC=<exact_header_text|NA>
HDR_DST=<exact_header_text|NA>
```

---

# 4. CSV 전체 row 수

header 제외 데이터 row 수를 확인한다.

출력:

```text
QROW=A   # 1개 이상
QROW=B   # 0개
QROW=C   # 확인 불가
```

추가:

```text
ROWS=<integer|NA>
```

---

# 5. 유효 edge 후보 row 수

FromPath / ToPath가 둘 다 비어 있지 않은 row 수를 확인한다.

출력:

```text
QPAIR=A   # 1개 이상
QPAIR=B   # 0개
QPAIR=C   # 확인 불가
```

추가:

```text
PAIRS=<integer|NA>
```

---

# 6. parser 단계 source/target mapping

실제 parser 결과나 로그에서 source/target mapping을 확인한다.

출력:

```text
QMAP=A   # source=FromPath, target=ToPath로 mapping됨
QMAP=B   # 열은 찾았지만 source/target mapping 단계에서 실패
QMAP=C   # 다른 열로 mapping됨
QMAP=D   # mapping 정보 없음
QMAP=E   # 확인 불가
```

추가:

```text
MAP_SRC=<actual_value|NA>
MAP_DST=<actual_value|NA>
```

---

# 7. MCD_EDGE_COLUMNS_UNRESOLVED 발생 위치

reason code가 **어느 단계/파일에서 생성됐는지** 확인한다.

출력:

```text
QERLOC=A   # CSV header resolve 단계
QERLOC=B   # edge normalize 단계
QERLOC=C   # dependency_edges 생성 단계
QERLOC=D   # report/improvement 출력 단계
QERLOC=E   # 이전 run의 stale 결과
QERLOC=F   # 위치 확인 불가
```

추가:

```text
ERR_FILE=<filename_or_path|NA>
ERR_STAGE=<actual_stage_text|NA>
```

---

# 8. reason code와 FromPath/ToPath 인식이 같은 run인지

가장 중요하다.

출력:

```text
QSAME=A   # 같은 최신 run에서 둘 다 발생
QSAME=B   # FromPath/ToPath 인식은 최신 run, unresolved는 이전/stale run
QSAME=C   # 서로 다른 artifact에서 발생해 run 동일성 확인 불가
QSAME=D   # 확인 불가
```

---

# 9. dependency_edges 생성 직전 edge count

가능하면 intermediate JSON/log를 확인한다.

출력:

```text
QPRE=A   # 생성 직전 edge 후보 1개 이상
QPRE=B   # 생성 직전 이미 0개
QPRE=C   # intermediate 정보 없음
QPRE=D   # 확인 불가
```

추가:

```text
PRE_EDGES=<integer|NA>
```

---

# 10. dependency_edges 최종 count

출력:

```text
QDEPCNT=A   # 1개 이상
QDEPCNT=B   # 0개
QDEPCNT=C   # 필드 자체 없음
QDEPCNT=D   # 확인 불가
```

추가:

```text
DEP_EDGES=<integer|NA>
```

---

# 11. cycle count

cycle 탐지 결과 개수를 확인한다.

출력:

```text
QCYCLE=A   # cycle 1개 이상
QCYCLE=B   # cycle 0개
QCYCLE=C   # cycle 필드/결과 없음
QCYCLE=D   # 확인 불가
```

추가:

```text
CYCLES=<integer|NA>
```

---

# 12. cycle_members 최종 count

출력:

```text
QMEMCNT=A   # 전체적으로 member 1개 이상
QMEMCNT=B   # cycle은 있으나 member 0개
QMEMCNT=C   # cycle 자체가 0개라 member도 0개
QMEMCNT=D   # 필드 자체 없음
QMEMCNT=E   # 확인 불가
```

추가:

```text
MEMBERS=<integer|NA>
```

---

# 13. edge 소실 단계

위 결과를 **실제 증거로만** 판정한다.

```text
QDROP=A   # CSV row 단계부터 유효 edge 없음
QDROP=B   # header/mapping 단계에서 소실
QDROP=C   # mapping 이후 normalize/filter 단계에서 소실
QDROP=D   # dependency_edges 변환 단계에서 소실
QDROP=E   # dependency_edges는 있으나 cycle 생성 단계에서 소실
QDROP=F   # artifact stale/mixed 문제
QDROP=G   # 확인 불가
```

---

# 14. topology fallback 직접 원인

`QEVID=F`, `QCODE=C`의 원인을 실제 reason/evidence로 확인한다.

출력:

```text
QFALL=A   # dependency edge/fact 없음 때문에 topology fallback
QFALL=B   # Code Analyzer 호출 실패
QFALL=C   # Code Analyzer 결과는 있으나 evidence 변환 실패
QFALL=D   # repository/code path resolve 실패
QFALL=E   # cycle/member 부재 때문에 분석 대상 생성 실패
QFALL=F   # 기타 명시적 원인
QFALL=G   # 확인 불가
```

`QFALL=F`일 때만:

```text
FALL_REASON=<actual_reason_code_or_short_text>
```

---

# 15. Code Analyzer 호출 흔적

최신 run 기준.

출력:

```text
QCALL=A   # 실제 호출 흔적 있음
QCALL=B   # 호출 시도했으나 실패 흔적 있음
QCALL=C   # 호출 자체 없음
QCALL=D   # 확인 불가
```

추가 가능하면:

```text
CALL_REASON=<actual_reason_or_NA>
```

---

# 16. MCD-<hash> 노출 위치

현재 `QHASH=C`의 구체 위치를 확인한다.

출력:

```text
QHLOC=A   # report 제목
QHLOC=B   # cycle/section 제목
QHLOC=C   # table의 사용자 표시용 ID
QHLOC=D   # improvement points 제목/본문
QHLOC=E   # 내부 metadata에만 존재
QHLOC=F   # 복수 위치
QHLOC=G   # 확인 불가
```

추가:

```text
HASH_SAMPLE=<one_actual_visible_example|NA>
```

내부 `work_unit_id`만 존재하면 `QHLOC=E`.

---

# 17. Worst Top10 일부 폴더만 생성된 이유

현재 `QTOP=B`.

출력:

```text
QTOPWHY=A   # 실제 분석 대상이 있는 폴더만 출력되어 정상
QTOPWHY=B   # 일부 폴더 데이터가 누락됨
QTOPWHY=C   # edge/cycle 부재 때문에 일부만 출력
QTOPWHY=D   # 출력 제한/TopN 로직 때문에 일부 누락
QTOPWHY=E   # 확인 불가
```

---

# 18. 문제 파일/클래스 미표시 위치

현재 `QFILE=C`.

출력:

```text
QFILEWHY=A   # source 데이터에 file/class 정보 자체 없음
QFILEWHY=B   # source에는 있으나 report 변환에서 누락
QFILEWHY=C   # edge/cycle 미생성 때문에 산출 불가
QFILEWHY=D   # feature 자체가 최신 report path에서 호출되지 않음
QFILEWHY=E   # 확인 불가
```

---

# 19. 최종 원인 판정

반드시 하나만 선택.

```text
ROOT=A   # 입력 CSV 자체에 유효 edge row 없음
ROOT=B   # header alias/mapping 문제
ROOT=C   # normalize/filter 단계에서 edge 소실
ROOT=D   # dependency_edges 생성 로직 문제
ROOT=E   # cycle 생성/연결 로직 문제
ROOT=F   # stale/mixed artifact 때문에 잘못 판정됨
ROOT=G   # Code Analyzer 연결이 1차 원인
ROOT=H   # 복수 원인이 있으나 edge pipeline 문제가 1차
ROOT=I   # 증거 부족으로 판단 불가
```

권장 우선순위:

```text
QSAME=B 또는 QDROP=F
→ ROOT=F

QPAIR=B
→ ROOT=A

QMAP=B/C
→ ROOT=B

QPRE=B AND QPAIR=A
→ ROOT=C

QPRE=A AND QDEPCNT=B/C
→ ROOT=D

QDEPCNT=A AND QCYCLE=B/C
→ ROOT=E

dependency/cycle 정상인데 QCALL=B/C이고 evidence 실패
→ ROOT=G

edge pipeline + 후속 Code Analyzer 문제 동시 존재
→ ROOT=H
```

---

# 20. 최종 출력 형식

**설명문 없이 아래 형식으로만 출력한다.**

```text
QRUN=A RUN=~/l1sw-private-skills/l1-sam-fixer/output/...
QIN=A CSV=...
QHDR=A HDR_SRC=FromPath HDR_DST=ToPath
QROW=A ROWS=12345
QPAIR=A PAIRS=12340
QMAP=A MAP_SRC=FromPath MAP_DST=ToPath
QERLOC=C ERR_FILE=... ERR_STAGE=...
QSAME=A
QPRE=A PRE_EDGES=12340
QDEPCNT=B DEP_EDGES=0
QCYCLE=B CYCLES=0
QMEMCNT=C MEMBERS=0
QDROP=D
QFALL=E
QCALL=C CALL_REASON=NA
QHLOC=B HASH_SAMPLE=MCD-1234abcd
QTOPWHY=C
QFILEWHY=C
ROOT=D
```

마지막 한 줄:

```text
MCD245ROOT: QRUN=A QIN=A QHDR=A QROW=A ROWS=12345 QPAIR=A PAIRS=12340 QMAP=A QERLOC=C QSAME=A QPRE=A PRE_EDGES=12340 QDEPCNT=B DEP_EDGES=0 QCYCLE=B CYCLES=0 QMEMCNT=C MEMBERS=0 QDROP=D QFALL=E QCALL=C QHLOC=B QTOPWHY=C QFILEWHY=C ROOT=D
```

---

# 21. 출력 제한

- 설명문 금지
- 원인 추측 금지
- 조치 제안 금지
- 수정 금지
- 재실행 금지
- Job-list 언급 금지
- 질문 금지
- 확인 불가 시 반드시 해당 `E/F/G/I` 계열 코드 사용
- 마지막 `MCD245ROOT:` 한 줄만 복사해 전달 가능해야 함
