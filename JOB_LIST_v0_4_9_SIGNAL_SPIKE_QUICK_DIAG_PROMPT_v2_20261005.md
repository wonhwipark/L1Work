# Job-list v0.4.9 Signal 급증 원인 QUICK 진단 프롬프트 v2

## 목적

아래 현상이 무엇 때문인지 **읽기 전용으로 빠르게 판별**한다.

```text
2026-09-24 baseline -> 2026-10-05 09:21 KST

heartbeat-ok       : 1 -> 82   (+81)
skill-updater-ok   : 1 -> 121  (+120)
job-list-ok        : 0 -> 21   (+21)
job-list-fail      : 0 -> 6    (+6)
job-list-deferred  : 0 -> 12   (+12)
autotask-ok        : 0 -> 5    (+5)
autotask-error     : 0 -> 18   (+18)
```

확인할 핵심 가설은 4개뿐이다.

```text
H1 = 과거 실패 signal이 persistent queue에 쌓였다가 GitHub 연결 복구 후 replay
H2 = replay는 없고, 연결 복구 이후 새 실행들이 정상적으로 signal을 발생
H3 = 과거 PENDING/DEFERRED Job이 뒤늦게 처리되며 signal 증가
H4 = Scheduler/Dispatcher 중복 또는 recovery 반복 실행으로 heartbeat 과다
```

---

# 0. 매우 중요한 실행 제한

이 프롬프트는 **QUICK 진단**이다.

반드시 아래 제한을 지킨다.

1. 코드 수정 금지.
2. Scheduler `/Run` 금지.
3. Job-list / Dispatcher / AutoTask / Skill-Updater 실행 금지.
4. GitHub signal GET을 새로 발생시키는 테스트 금지.
5. 파일 시스템 전체 검색 금지.
6. `C:\`, 사용자 HOME 전체, WSL 전체, `/home` 전체 recursive search 금지.
7. 현재 설치된 `job-list` root와 그 설정에서 직접 참조하는 Dispatcher root만 본다.
8. 경로가 즉시 확인되지 않으면 추가 탐색하지 말고 `0=확인 불가`로 답한다.
9. 로그는 **최근 200줄까지만** 본다.
10. JSONL/history는 **마지막 100개 record까지만** 본다.
11. 분석 대상 시간은 우선 **2026-10-05 00:00~13:00 KST**로 제한한다.
12. 필요해도 2026-10-04 이전 전체 history를 재분석하지 않는다.
13. source code 확인은 아래 3개 파일까지만 허용한다.

```text
scripts/signal_transport.py
scripts/dispatcher_cycle_bridge.py
scripts/dispatcher_autotask_register_windows_job.py
```

14. 위 3개 파일에서 `queue`, `replay`, `retry`, `spool`, `pending` 문자열 검색까지만 허용한다.
15. 8개 질문에 답할 evidence가 없으면 더 찾지 말고 `0`으로 종료한다.

---

# 1. 확인 대상

아래 파일/상태만 확인한다.

```text
A. job-list VERSION
B. requests/one-shot-jobs.json
C. data/state/core/processed.jsonl              마지막 100 records
D. output/dispatcher_autotask_register/latest_result.json
E. 최신 bridge receipt 1개
F. Dispatcher 최신 log                         마지막 200 lines
G. Windows Scheduled Task 중 Dispatcher 관련 task 목록과 trigger
H. 위 3개 source file의 queue/replay 관련 문자열
```

**그 외 파일은 열지 않는다.**

---

# 2. 질문

## Q1. 현재 Job-list가 v0.4.9인가?

```text
0 = 확인 불가
1 = YES
2 = NO
```

---

## Q2. persistent signal replay 기능이 실제 존재하는가?

판정 방법:

```text
scripts/signal_transport.py
scripts/dispatcher_cycle_bridge.py
scripts/dispatcher_autotask_register_windows_job.py
```

에서 `queue/replay/spool/pending/retry`만 검색한다.

중요:

- 동일 HTTP 호출 내부의 즉시 retry는 persistent replay가 아니다.
- 실패 요청을 파일/DB에 저장하고 다음 실행에서 재전송해야 H1의 replay로 인정한다.

```text
0 = 확인 불가
1 = persistent replay 존재
2 = persistent replay 없음
3 = 동일 실행 내부 retry만 존재
```

Evidence:

```text
E2=<파일명:근거 한 줄>
```

---

## Q3. 2026-10-05에 과거 PENDING/DEFERRED Job이 실제 처리된 흔적이 있는가?

`processed.jsonl` 마지막 100 records와 one-shot 상태만 본다.

```text
0 = 확인 불가
1 = 없음
2 = 1~2건
3 = 3~5건
4 = 6건 이상
```

Evidence:

```text
E3=<count 및 대표 job id 최대 3개>
```

---

## Q4. Dispatcher Scheduled Task가 중복 등록되어 있는가?

Windows Scheduler에서 **Dispatcher 관련 Task 이름과 trigger만** 본다.

```text
0 = 확인 불가
1 = task 1개 / trigger 정상
2 = task가 2개 이상
3 = task 1개지만 동일/유사 trigger가 중복
4 = task와 trigger 모두 중복 의심
```

Evidence:

```text
E4=<task name / trigger 요약>
```

---

## Q5. v0.4.9 recovery가 동일 실행에서 Dispatcher를 여러 번 강제 실행한 흔적이 있는가?

`latest_result.json`, 최신 bridge receipt, Dispatcher 최근 200 log lines만 본다.

```text
0 = 확인 불가
1 = 추가 강제 실행 없음
2 = 1회 추가 실행
3 = 2회 추가 실행
4 = 3회 이상 또는 반복 loop 의심
```

Evidence:

```text
E5=<timestamp 또는 cycle_id 요약>
```

---

## Q6. 한 Dispatcher cycle에서 heartbeat-ok가 여러 번 전송되는가?

최신 bridge receipt + Dispatcher 최근 200줄만 확인한다.

```text
0 = 확인 불가
1 = cycle당 최대 1회
2 = 일부 cycle에서 2회
3 = 일부 cycle에서 3회 이상
```

Evidence:

```text
E6=<cycle_id / count>
```

---

## Q7. 현재 가장 유력한 원인은?

```text
0 = UNKNOWN
1 = H1 persistent replay
2 = H2 연결 복구 후 신규 signal 정상 관측
3 = H3 과거 PENDING/DEFERRED 처리
4 = H4 Scheduler/Dispatcher 중복 또는 recovery 반복
5 = H2 + H3
6 = H2 + H4
7 = H3 + H4
8 = 복합 원인
```

판정 우선순위:

```text
persistent replay 코드 없음
-> H1은 원칙적으로 제외

Scheduler/task 중복 없음
AND cycle당 heartbeat 1회
-> H4 우선순위 낮춤

10/5 처리된 old pending/deferred 다수 존재
-> H3 강화

위 문제가 없고 transport 성공 이후 새 cycle과 signal이 정상 대응
-> H2
```

---

## Q8. 다음 행동은?

```text
0 = 추가 확인 불필요
1 = signal count를 새 baseline으로 잡고 다음 :15/:45 delta만 관찰
2 = Scheduler 중복 수정 필요
3 = recovery 반복 실행 수정 필요
4 = pending/deferred cleanup 필요
5 = replay 로직 수정 필요
6 = 별도 deep-dive 필요
```

---

# 3. 최종 답변 형식

**아래 형식 외의 긴 설명을 하지 않는다.**

```text
Q1=<0~2>
Q2=<0~3>
Q3=<0~4>
Q4=<0~4>
Q5=<0~4>
Q6=<0~3>
Q7=<0~8>
Q8=<0~6>

E2=<없으면 NONE>
E3=<없으면 NONE>
E4=<없으면 NONE>
E5=<없으면 NONE>
E6=<없으면 NONE>

FINAL_ROOT=<H1|H2|H3|H4|H2+H3|H2+H4|H3+H4|COMPLEX|UNKNOWN>
PERSISTENT_REPLAY=<YES|NO|UNKNOWN>
DUPLICATE_SCHEDULER=<YES|NO|UNKNOWN>
MULTI_HEARTBEAT_PER_CYCLE=<YES|NO|UNKNOWN>
NEXT_ACTION=<OBSERVE_NEXT_CYCLE|FIX_SCHEDULER|FIX_RECOVERY|CLEANUP_JOBS|FIX_REPLAY|DEEP_DIVE|NONE>
```

---

# 4. 강제 종료 조건

아래 중 하나라도 발생하면 추가 탐색하지 말고 즉시 현재 결과를 반환한다.

```text
1. 대상 파일 경로를 알기 위해 상위 디렉터리 recursive scan이 필요함
2. 하나의 로그가 너무 커서 전체 파싱이 필요함
3. Scheduler history 전체 export가 필요함
4. GitHub API 호출이 필요함
5. signal을 직접 발생시켜야 확인 가능함
6. 현재 설치 root 밖의 과거 패키지들을 비교해야 함
```

이 경우 해당 질문은 `0=확인 불가`로 답하고:

```text
Q8=6
NEXT_ACTION=DEEP_DIVE
```

로 종료한다.

---

# 5. 핵심 판정 규칙

```text
[Rule 1]
persistent queue/replay 코드가 없으면
"예전 TLS 실패 HTTP 요청이 GitHub 연결 후 한꺼번에 재전송됐다"
라는 가설 H1은 배제한다.

[Rule 2]
Scheduler task가 1개이고 trigger도 정상이며
cycle당 heartbeat가 최대 1회면
heartbeat +81만으로 중복 실행을 주장하지 않는다.

[Rule 3]
old PENDING/DEFERRED Job이 10/5에 다수 처리됐다면
그 작업이 만든 신규 signal 증가는 H3로 분류한다.

[Rule 4]
위 세 문제가 없으면
GitHub/TLS 연결 정상화 후 새 실행 signal이 관측되기 시작한 H2가 기본 결론이다.

[Rule 5]
누적 delta +81은 발생 시간 분포를 모르면
"폭주"의 증거로 사용하지 않는다.
```

진단만 수행하고 종료한다.
