# Job-list v0.4.9 Signal 급증 원인 확인 프롬프트

- 작성 시각: 2026-10-05 10:06 KST
- 목적: `job-list v0.4.9` 적용 전후 signal count 급증이
  1) 과거 실패 요청의 backlog/replay인지,
  2) GitHub/TLS 연결 정상화 이후 새 실행들이 정상 관측된 것인지,
  3) 기존 PENDING/DEFERRED Job의 후속 실행 때문인지,
  4) Scheduler/Dispatcher 중복 실행 때문인지
  를 **읽기 전용으로 판별**한다.
- 대상 환경: Windows 회사 PC
- 중요: **코드 수정 / 설정 변경 / Scheduler 재등록 / Job 재실행 / signal 강제 전송 금지**
- 중요: **진단만 수행하고 종료**
- 답변은 최대한 아래 객관식 번호로만 작성한다.
- 근거가 필요한 항목만 파일명/라인/타임스탬프/카운트를 짧게 첨부한다.

---

## 0. 현재 알려진 외부 관측값

아래 값은 사외에서 확인한 최신 관측값이다.

```text
Baseline captured : 2026-09-24T00:14:48.625762+09:00
After captured    : 2026-10-05T09:21:49.894918+09:00

dispatcher-windows-heartbeat-ok.signal        1 -> 82   (+81)
dispatcher-windows-skill-updater-ok.signal    1 -> 121  (+120)
dispatcher-windows-skill-updater-fail.signal  0 -> 0    (+0)
dispatcher-windows-job-list-ok.signal         0 -> 21   (+21)
dispatcher-windows-job-list-fail.signal       0 -> 6    (+6)
dispatcher-windows-job-list-deferred.signal   0 -> 12   (+12)
dispatcher-windows-autotask-ok.signal         0 -> 5    (+5)
dispatcher-windows-autotask-error.signal      0 -> 18   (+18)
```

현재 가설:

```text
H1. 과거 TLS/GitHub 실패 요청이 persistent queue에 저장되었다가
    연결 성공 후 한꺼번에 replay되었다.

H2. persistent replay는 없고,
    GitHub/TLS 연결이 정상화된 뒤 Scheduler/Updater/Dispatcher의
    새로운 실행들이 성공하면서 signal이 누적되기 시작했다.

H3. 과거 PENDING/DEFERRED Job이 연결 복구 후 실제로 실행되면서
    짧은 시간에 새 signal 요청이 많이 발생했다.

H4. Dispatcher Scheduler가 중복 등록되었거나
    v0.4.9 recovery가 여러 번 실행되어 heartbeat가 비정상적으로 증가했다.

H5. 위 원인이 둘 이상 동시에 발생했다.
```

---

# 1. 진단 원칙

반드시 다음 원칙을 지킨다.

1. 모든 작업은 읽기 전용이다.
2. Scheduler `/Run`, AutoTask 실행, Job-list 실행, Dispatcher 직접 실행 금지.
3. GitHub signal GET을 새로 발생시키는 테스트 금지.
4. token/password/proxy credential 값 출력 금지.
5. 기존 로그와 state 파일의 timestamp를 우선 사용한다.
6. 추측으로 결론 내리지 않는다.
7. `heartbeat count +81`이라는 누적 숫자만으로 폭주 여부를 판단하지 않는다.
8. 반드시 **언제 signal이 발생했는지**와 **실행 횟수**를 함께 본다.
9. 과거 실패 HTTP 요청을 저장하는 persistent queue/retry spool이 실제 존재하는지 코드/파일 evidence로 확인한다.
10. 최종 답변은 아래 객관식 포맷을 따른다.

---

# 2. 먼저 확인할 파일/상태

존재하는 것만 확인한다.

## A. Job-list

- 설치된 `VERSION`
- `requests/one-shot-jobs.json`
- `data/state/core/processed.jsonl`
- activation/history 관련 jsonl
- `output/dispatcher_autotask_register/latest_result.json`
- v0.4.9 bridge receipt 파일
- Job-list 로그
- signal transport 로그/결과

## B. Dispatcher

- Dispatcher 설치 root
- dispatcher state 파일
- dispatcher log
- `run.lock`
- Scheduler task 이름/상태/trigger
- 최근 실행 시간 및 LastTaskResult
- 동일 Dispatcher task가 2개 이상 등록되어 있는지

## C. AutoTask / Scheduler

- `:15/:45`, PT30M trigger 여부
- 동일 기능의 중복 Task 존재 여부
- 최근 실행 history
- v0.4.9 recovery 수행 시 direct/retry/fallback 실행 evidence

## D. Skill-Updater / Signal transport

- 현재 Skill-Updater version
- TLS/proxy/network profile
- 최근 TLS 성공/실패 timestamp
- signal 전송 시도 기록
- persistent replay queue/spool/retry DB 존재 여부

---

# 3. 객관식 질문

## Q1. 현재 설치된 Job-list 버전

```text
0 = 확인 불가
1 = 0.4.9
2 = 0.4.8
3 = 기타
```

## Q2. 현재 설치된 Skill-Updater 버전

```text
0 = 확인 불가
1 = 0.5.36
2 = 기타
```

## Q3. v0.4.9 one-shot Job ID 상태

대상:

```text
JOB-20261004-DISPATCHER-RECOVERY-V0409
```

```text
0 = 흔적 없음
1 = PENDING
2 = RUNNING
3 = processed SUCCESS
4 = processed FAIL
5 = DEFERRED
6 = 기타
```

## Q4. 과거 실패 signal 요청을 저장하는 persistent queue/spool이 실제 존재하는가?

예:
- retry queue
- unsent signal DB
- pending HTTP request spool
- 실패 signal 재전송 목록
- reboot 후에도 유지되는 retry JSON/JSONL

```text
0 = 확인 불가
1 = 존재함
2 = 존재하지 않음
3 = 메모리 retry만 존재하며 프로세스 종료 후 유지되지 않음
```

### Q4 Evidence
다음 형식으로 짧게 작성:

```text
E4=<파일/코드/디렉터리 근거>
```

---

## Q5. 과거 TLS 실패 signal을 나중에 자동 replay하는 코드가 존재하는가?

```text
0 = 확인 불가
1 = 명시적 persistent replay 코드 존재
2 = replay 코드 없음
3 = 동일 실행 안에서의 단기 retry만 존재
```

---

## Q6. 현재 확인 가능한 signal 발생 기록에 과거 timestamp를 가진 요청이 뒤늦게 전송된 evidence가 있는가?

예:
- 9/24 실패 요청이 10/5에 replay되었다는 기록
- original_created_at != sent_at 형태

```text
0 = 확인 불가
1 = 있음
2 = 없음
```

---

## Q7. GitHub/TLS signal transport가 정상화된 최초 시각을 특정할 수 있는가?

```text
0 = 특정 불가
1 = 특정 가능
```

가능한 경우:

```text
E7=YYYY-MM-DD HH:MM:SS KST, 근거=<파일/로그>
```

---

## Q8. 정상화 직전에는 `CERTIFICATE_VERIFY_FAILED` 또는 동일 계열 TLS 오류가 있었는가?

```text
0 = 확인 불가
1 = 있음
2 = 없음
```

---

## Q9. 정상화 이후 처음 성공한 signal 종류는 무엇인가?

```text
0 = 확인 불가
1 = heartbeat-ok
2 = skill-updater-ok
3 = job-list-*
4 = autotask-*
5 = 둘 이상 거의 동시에
```

---

## Q10. heartbeat +81이 짧은 시간에 집중적으로 발생했는가?

판정 기준:
- 로그/state timestamp로 실제 발생 구간을 본다.

```text
0 = 확인 불가
1 = 10분 이내 대부분 발생
2 = 1시간 이내 대부분 발생
3 = 수시간에 걸쳐 분산
4 = 수일에 걸쳐 분산
5 = 기타
```

가능하면:

```text
E10=first=<KST>, last=<KST>, observed_count=<N>
```

---

## Q11. Dispatcher Scheduler의 정상 등록 주기는 무엇인가?

```text
0 = 확인 불가
1 = 매시 :15/:45, 30분 주기
2 = 1시간 주기
3 = 3시간 주기
4 = 기타
```

---

## Q12. 동일 Dispatcher 기능을 실행하는 Windows Scheduled Task가 중복 등록되어 있는가?

```text
0 = 확인 불가
1 = 1개만 존재
2 = 2개 존재
3 = 3개 이상 존재
```

가능하면 task name만:

```text
E12=<task-name-1>,<task-name-2>...
```

---

## Q13. 동일한 Scheduler Task 내부에 trigger가 중복 생성되어 있는가?

```text
0 = 확인 불가
1 = 정상 trigger 1세트
2 = 동일/유사 trigger 2세트
3 = 3세트 이상
```

---

## Q14. Dispatcher 실제 cycle 수와 heartbeat 성공 수가 대략 1:1인가?

```text
0 = 확인 불가
1 = 거의 1:1
2 = heartbeat가 cycle보다 많음
3 = cycle이 heartbeat보다 많음
4 = 심하게 불일치
```

가능하면:

```text
E14=dispatcher_cycles=<N>, heartbeat_success=<N>
```

---

## Q15. 한 Dispatcher cycle 안에서 heartbeat-ok가 2회 이상 호출된 evidence가 있는가?

```text
0 = 확인 불가
1 = 없음, 최대 1회
2 = 일부 cycle에서 2회
3 = 일부 cycle에서 3회 이상
```

---

## Q16. v0.4.9 recovery 과정에서 Scheduler `/Run` 또는 Dispatcher 직접 실행이 몇 번 시도되었는가?

```text
0 = 확인 불가
1 = 0회
2 = 1회
3 = 2회
4 = 3회 이상
```

가능하면:

```text
E16=<timestamp 목록 요약>
```

---

## Q17. v0.4.9 recovery가 동일 Job에서 반복 재진입한 evidence가 있는가?

```text
0 = 확인 불가
1 = 없음
2 = 1회 재진입
3 = 2회 이상 재진입
```

---

## Q18. processed/activation history에서 과거 PENDING/DEFERRED Job이 10/5 전후 실제로 처리된 흔적이 있는가?

```text
0 = 확인 불가
1 = 없음
2 = 1~2개
3 = 3~5개
4 = 6개 이상
```

---

## Q19. `job-list-deferred +12`와 대응되는 local history entry를 몇 개 확인할 수 있는가?

```text
0 = 확인 불가
1 = 0개
2 = 1~5개
3 = 6~12개
4 = 12개 초과
```

---

## Q20. `job-list-fail +6`와 대응되는 local failure entry를 몇 개 확인할 수 있는가?

```text
0 = 확인 불가
1 = 0개
2 = 1~3개
3 = 4~6개
4 = 6개 초과
```

---

## Q21. `autotask-error +18`와 대응되는 local AutoTask/Scheduler error entry를 몇 개 확인할 수 있는가?

```text
0 = 확인 불가
1 = 0개
2 = 1~5개
3 = 6~18개
4 = 18개 초과
```

---

## Q22. Skill-Updater OK +120은 실제 updater 실행 횟수와 대략 일치하는가?

```text
0 = 확인 불가
1 = 대략 일치
2 = signal count가 실행 횟수보다 현저히 많음
3 = updater 실행 횟수가 signal count보다 현저히 많음
```

---

## Q23. signal count 급증의 가장 강한 원인은 무엇인가?

```text
0 = 판정 불가
1 = 과거 실패 HTTP 요청 persistent replay
2 = GitHub/TLS 연결 정상화 후 신규 실행 signal이 정상 관측됨
3 = 과거 PENDING/DEFERRED Job의 후속 실행
4 = Dispatcher/Scheduler 중복 등록
5 = v0.4.9 recovery 반복 실행
6 = 복합 원인
```

---

## Q24. H1: "과거 signal 요청이 쌓여 있다가 GitHub 연결 성공 후 한꺼번에 replay"

```text
0 = 판정 불가
1 = 매우 유력
2 = 가능성 있음
3 = 가능성 낮음
4 = 코드/증거상 사실상 배제
```

---

## Q25. H2: "연결 정상화 이후 새 실행 signal이 정상적으로 보이기 시작함"

```text
0 = 판정 불가
1 = 매우 유력
2 = 가능성 있음
3 = 가능성 낮음
4 = 사실상 배제
```

---

## Q26. H3: "PENDING/DEFERRED Job이 뒤늦게 실행되며 signal 증가"

```text
0 = 판정 불가
1 = 매우 유력
2 = 가능성 있음
3 = 가능성 낮음
4 = 사실상 배제
```

---

## Q27. H4: "Scheduler/Dispatcher 중복 또는 recovery 반복으로 heartbeat 과다"

```text
0 = 판정 불가
1 = 매우 유력
2 = 가능성 있음
3 = 가능성 낮음
4 = 사실상 배제
```

---

## Q28. 현재 heartbeat 증가 속도는 정상 30분 주기 범위를 초과하는가?

가능하면 **최근 1~3시간 데이터만** 사용한다.

```text
0 = 최근 데이터 부족
1 = 정상 범위 (대략 시간당 0~2회)
2 = 경계 (시간당 3회)
3 = 비정상 의심 (시간당 4~5회)
4 = 명확한 비정상 (시간당 6회 이상)
```

---

## Q29. 즉시 수정이 필요한가?

```text
0 = 판정 불가
1 = 수정 불필요, 추가 관찰만 필요
2 = Scheduler 중복 제거 필요
3 = v0.4.9 recovery 반복 방지 수정 필요
4 = signal retry/replay 정책 수정 필요
5 = Job-list PENDING/DEFERRED cleanup 필요
6 = 복합 수정 필요
```

주의:
- 이 질문은 **진단 결론만 작성**
- 실제 수정은 수행하지 않는다.

---

## Q30. 추가 진단이 필요한가?

```text
0 = 필요 없음, 원인 충분히 특정됨
1 = 최근 1시간 signal delta만 추가 필요
2 = Scheduler history 추가 필요
3 = Job-list processed/activation history 추가 필요
4 = Dispatcher log 추가 필요
5 = Skill-Updater network log 추가 필요
6 = 둘 이상 필요
```

---

# 4. 최종 답변 형식

설명문을 길게 쓰지 말고 우선 아래 형식으로 답한다.

```text
Q1=<번호>
Q2=<번호>
Q3=<번호>
Q4=<번호>
Q5=<번호>
Q6=<번호>
Q7=<번호>
Q8=<번호>
Q9=<번호>
Q10=<번호>
Q11=<번호>
Q12=<번호>
Q13=<번호>
Q14=<번호>
Q15=<번호>
Q16=<번호>
Q17=<번호>
Q18=<번호>
Q19=<번호>
Q20=<번호>
Q21=<번호>
Q22=<번호>
Q23=<번호>
Q24=<번호>
Q25=<번호>
Q26=<번호>
Q27=<번호>
Q28=<번호>
Q29=<번호>
Q30=<번호>
```

그 다음 evidence가 있는 항목만 작성한다.

```text
E4=...
E7=...
E10=...
E12=...
E14=...
E16=...
```

마지막으로 반드시 아래 5줄을 작성한다.

```text
FINAL_ROOT=<H1|H2|H3|H4|H5|UNKNOWN>
PERSISTENT_REPLAY=<YES|NO|UNKNOWN>
DUPLICATE_DISPATCHER=<YES|NO|UNKNOWN>
HEARTBEAT_RATE=<NORMAL|BORDERLINE|ABNORMAL|UNKNOWN>
NEXT_ACTION=<OBSERVE|CHECK_RECENT_DELTA|FIX_SCHEDULER|FIX_RECOVERY|FIX_REPLAY|CLEANUP_JOBS|DEEP_DIVE>
```

---

# 5. 판정 우선순위

최종 판정은 아래 순서를 따른다.

```text
1. persistent replay queue/code가 실제 존재하는가?
   YES -> H1 검토
   NO  -> H1 우선순위 크게 낮춤

2. signal transport 정상화 timestamp 이후
   새로운 Scheduler/Updater/Dispatcher 실행과 signal 성공이 시간적으로 일치하는가?
   YES -> H2 강화

3. PENDING/DEFERRED Job이 같은 시각대에 처리됐는가?
   YES -> H3 강화

4. 동일 Scheduler task/trigger/Dispatcher cycle이 중복되어 있는가?
   YES -> H4 강화

5. 둘 이상 동시 확인
   -> H5
```

특히 다음 논리를 반드시 지킨다.

```text
TLS 실패한 과거 HTTP 요청이 단순히 존재했다
!=
persistent replay가 존재한다

heartbeat count가 많이 증가했다
!=
heartbeat 폭주

누적 +81
!=
짧은 시간 +81
```

실제 원인은 반드시 **코드/queue 존재 여부 + timestamp + 실행 횟수**로 판정한다.

---

# 6. 진단 종료 조건

아래 중 하나가 충족되면 추가 작업 없이 종료한다.

```text
A. persistent replay 존재 여부가 확인되고,
   signal 증가 시간대와 일치함

B. recent heartbeat rate가 정상이고,
   Scheduler 중복이 없으며,
   transport 정상화 이후 신규 실행과 signal 증가가 일치함

C. Scheduler 중복 또는 recovery 반복 evidence가 명확함

D. 현재 evidence 부족으로 UNKNOWN이며,
   Q30에서 필요한 추가 evidence 종류를 특정함
```

**코드 수정이나 재실행은 하지 말고 진단 결과만 반환한다.**
