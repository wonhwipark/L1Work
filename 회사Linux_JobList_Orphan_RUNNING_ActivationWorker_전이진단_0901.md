# 회사 Linux — Job-list orphan RUNNING / activation worker 전이 진단 프롬프트

아래 작업을 **회사 Linux PC에서 현재 상태 기준으로 읽기 전용 진단**해줘.

목적:

```text
최신 MCD Job이 RUNNING으로 남아 있지만
child_pid 프로세스는 존재하지 않고
completion receipt도 없으며
activation worker log도 비어 있는 원인을 찾는다.
```

현재 확인된 대상:

```text
JOB=JOB-20260901-MCD-VERIFY-REPAIR-0110
PROFILE=l1-study-mcd
JOBLIST_VER=0.3.63
```

현재 관측:

```text
Job state       = RUNNING
child_pid       = 4033283
child process   = 없음
completion      = 없음
activation log  = 비어 있음
Study result    = 대상 Job 결과 없음
SAM report      = 2026-08-29 stale
Dispatcher      = job_list=FAIL, l1-study-runner=NOT_RUN
```

이번 단계에서는 **수정/재실행보다 먼저 root cause를 확정**한다.

---

# 1. 절대 원칙

이번 작업은 **읽기 전용 진단**이다.

하지 말 것:

```text
Job 재실행
Job 신규 enqueue
RUNNING state 강제 변경
processed/history 삭제
activation state 삭제
stale state 삭제
child process kill
Study Runner 실행
SAM Fixer 실행
Code Analyzer 실행
Dispatcher cycle 실행
systemd timer 수정
Skill 코드 수정
Git/GitHub write
```

허용:

```text
파일 읽기
JSON/JSONL/로그 확인
mtime 확인
PID 존재 여부 확인
systemd journal 읽기
Job-list 코드의 lifecycle 경로 읽기
bounded grep
프로세스 종료 흔적 확인
exit code / receipt / tmp artifact 확인
```

---

# 2. 우선 확인할 실제 Job state

다음 Job을 기준으로 한다.

```text
JOB-20260901-MCD-VERIFY-REPAIR-0110
```

Job-list 아래에서 다음을 찾는다.

```text
activation/latest.json
observer/current_run.json
observer/latest_result.json
core/processed.jsonl
job history / observation JSONL
worker state
temporary receipt
pid/lock 관련 state
```

판정:

```text
1=A   # RUNNING state와 child_pid=4033283 확인
1=B   # 현재 state가 이미 다른 값으로 변경됨
1=C   # 대상 Job state 찾지 못함
1=D   # 서로 다른 state 파일 간 값 충돌
```

추가:

```text
STATE=<actual>
PID=<actual|NA>
```

---

# 3. RUNNING 상태를 누가 기록했는지 확인

Job-list v0.3.63 코드에서
`RUNNING` 상태를 기록하는 정확한 함수/경로를 찾는다.

확인할 것:

```text
RUNNING 기록 시점
child spawn 전/후인지
child_pid 저장 시점
worker log open 시점
receipt path 생성 시점
```

판정:

```text
2=A   # RUNNING은 child spawn 성공 후 기록
2=B   # RUNNING은 child spawn 전에 기록
2=C   # RUNNING과 child_pid 기록이 서로 다른 단계
2=D   # 코드상 lifecycle이 모호함
2=E   # 확인 불가
```

추가:

```text
RUNNING_WRITE=<짧은 함수명/단계>
```

---

# 4. child process가 실제 spawn 되었는지 확인

현재 PID가 사라졌다는 사실만으로
"실행되지 않았다"고 단정하지 않는다.

다음 근거를 확인:

```text
subprocess/Popen 생성 직후 기록
child_pid 기록
start timestamp
worker stdout/stderr target
temporary file
systemd journal
Job-list log
shell/process wrapper log
```

판정:

```text
3=A   # child 실제 spawn 근거 있음
3=B   # child spawn 시도했으나 즉시 실패 근거 있음
3=C   # child_pid만 기록됐고 실제 spawn 근거 부족
3=D   # spawn 자체가 수행되지 않은 것으로 판단
3=E   # 확인 불가
```

추가:

```text
SPAWN=<짧은 근거>
```

---

# 5. activation worker log가 비어 있는 이유 확인

현재 가장 중요한 항목이다.

activation worker log 파일이:

```text
0 byte
미생성
생성됐으나 stdout/stderr redirect 실패
실제 worker가 다른 로그 위치 사용
buffer flush 전 process 종료
worker 시작 전 crash
```

중 무엇인지 확인한다.

판정:

```text
4=A   # 로그 파일은 정상 위치이나 worker 시작 전 종료
4=B   # stdout/stderr redirect 또는 log open 실패
4=C   # 실제 로그는 다른 경로에 존재
4=D   # log file 생성만 되고 내용 flush 전 종료 가능성 높음
4=E   # worker가 로그를 쓰지 않는 코드 경로
4=F   # 판단 불가
```

추가:

```text
WORKER_LOG=<path|NA>
LOG_REASON=<짧은 이유>
```

---

# 6. child 종료 원인 확인

spawn 근거가 있다면
child가 왜 사라졌는지 확인한다.

우선순위:

```text
1. recorded exit_code
2. completion/temporary receipt
3. systemd journal
4. Job-list stderr/stdout
5. OS OOM / signal termination
6. executable/profile invocation error
7. parent process 종료로 child 정리
```

판정:

```text
5=A   # 정상 종료했으나 receipt 기록 실패
5=B   # child 자체 실행 실패
5=C   # child crash/exception
5=D   # timeout/kill
5=E   # OOM/SIGKILL 등 OS 종료
5=F   # parent/worker 종료 영향
5=G   # exit 흔적 전혀 없음
5=H   # 판단 불가
```

추가:

```text
EXIT=<exit_code/signal/reason|NA>
```

---

# 7. completion receipt가 없는 이유 확인

Job-list v0.3.63 코드에서
`RUNNING → COMPLETED/FAILED/PARTIAL` 전이 조건과
completion receipt write 경로를 확인한다.

확인:

```text
receipt 작성 주체
receipt 파일명/path
atomic write 여부
child exit 후 누가 status 전이를 수행하는지
worker 재기동 시 orphan recovery가 있는지
```

판정:

```text
6=A   # child 정상 종료 후 receipt write에서 실패
6=B   # worker가 child exit를 회수하지 못함
6=C   # parent/worker가 먼저 종료되어 transition 미수행
6=D   # receipt는 다른 경로에 있으나 observer가 못 읽음
6=E   # Job-list에 orphan recovery 로직이 없음/불충분
6=F   # lifecycle code bug 가능성
6=G   # 판단 불가
```

추가:

```text
TRANSITION=<짧은 실제 경로/실패지점>
```

---

# 8. systemd/autotask-builder 실행과의 관계 확인

Dispatcher가 아니라
**Job-list activation worker를 실제로 기동한 상위 실행 owner**를 확인한다.

가능한 범위:

```text
autotask-builder
systemd service/timer
Job-list 내부 worker launcher
```

확인:

```text
worker parent PID
service invocation timestamp
service exit status
service가 child 종료를 기다리는 구조인지
service 종료 시 child도 함께 정리되는지
```

판정:

```text
7=A   # systemd/autotask-builder 정상, worker 내부 문제
7=B   # 상위 service가 worker/child를 조기 종료
7=C   # service timeout 영향
7=D   # service restart 영향
7=E   # 상위 실행 owner 불명확
7=F   # 판단 불가
```

추가:

```text
OWNER=<actual>
```

---

# 9. l1-study-mcd profile 호출 명령 확인

실행 자체가 시작됐는지 판단하기 위해
해당 Job이 생성한 실제 child command를 확인한다.

출력은 민감정보 제외하고
명령의 구조만 짧게 보여준다.

확인:

```text
target skill
profile
mode=mcd
source=latest-sam-report
target=SMPF/Protocol/Channel/L1
python executable
working directory
timeout
stdout/stderr redirect
```

판정:

```text
8=A   # child command 정상
8=B   # executable/path 오류
8=C   # profile/path 오류
8=D   # cwd/environment 오류
8=E   # timeout/launcher 옵션 오류
8=F   # command 자체가 만들어지지 않음
8=G   # 판단 불가
```

---

# 10. 실제 Study Runner 진입 흔적 확인

Study Runner 결과 파일이 없더라도
entrypoint까지 진입했는지 확인한다.

확인 가능한 근거:

```text
Study Runner log
checkpoint 생성 시각
temporary run directory
observer tmp
startup marker
run_id
```

판정:

```text
9=A   # Study Runner entrypoint 진입 확인
9=B   # launcher까지만 실행, Study Runner 진입 전 실패
9=C   # Study Runner 진입 근거 없음
9=D   # 진입했으나 초기화 단계에서 종료
9=E   # 판단 불가
```

---

# 11. orphan RUNNING 자동복구 로직 확인

Job-list v0.3.63에 다음 로직이 있는지 코드 기준으로 확인한다.

```text
RUNNING
+
child_pid dead
+
completion receipt 없음
```

일 때:

```text
ORPHANED / FAILED / RECOVERABLE
```

등으로 전환하는 로직이 있는지 확인한다.

판정:

```text
10=A   # 자동 orphan recovery 존재 + 정상 조건
10=B   # recovery 로직은 있으나 이번 Job에는 동작하지 않음
10=C   # recovery 로직 없음
10=D   # recovery 조건이 너무 제한적
10=E   # recovery 자체에 버그 가능성
10=F   # 판단 불가
```

추가:

```text
RECOVERY=<짧은 설명>
```

---

# 12. 안전한 재시도 가능 여부만 판정

이번 단계에서는 실제 재시도하지 않는다.

다음 중 하나를 선택한다.

```text
11=A   # 기존 RUNNING을 명확히 terminal 처리 후 동일 Job 재시도 가능
11=B   # orphan recovery 후 새 Job ID로 재시도 권장
11=C   # 기존 Job을 resume할 수 있음
11=D   # 중복 실행 위험 때문에 현재 재시도 금지
11=E   # lifecycle 코드 수정 전 재시도 금지
11=F   # 근거 부족으로 판단 불가
```

---

# 13. root cause 분류

가장 앞단의 실제 원인을 하나만 선택한다.

```text
12=A   # child spawn 이전 failure
12=B   # child spawn 직후 즉시 종료
12=C   # activation worker logging/redirect failure
12=D   # parent/systemd/autotask-builder 조기 종료
12=E   # child exit 회수(wait/poll) 실패
12=F   # completion receipt write 실패
12=G   # RUNNING→terminal state transition bug
12=H   # orphan recovery 부재/실패
12=I   # l1-study-mcd command/profile 문제
12=J   # Study Runner 초기화 실패
12=K   # OS kill/OOM/timeout
12=L   # 복합 문제
12=M   # 현재 증거만으로 root cause 확정 불가
```

---

# 14. 최종 결론

다음 중 하나만 선택한다.

```text
13=A   # 원인 확정 + 안전한 복구 경로 명확
13=B   # 원인 거의 확정, 코드 수정 필요
13=C   # orphan 상태는 확정, root cause는 추가 증거 필요
13=D   # 실제 child 정상 종료 가능성 있으나 receipt만 유실
13=E   # 상위 scheduler/service 문제
13=F   # 판단 불가
```

---

# 15. 다음 조치 제안

실제 수정은 하지 말고
가장 작은 다음 조치 하나만 제안한다.

객관식:

```text
14=A   # Job-list orphan recovery만 보강
14=B   # worker logging/receipt 기록 보강
14=C   # child spawn/exit lifecycle 수정
14=D   # systemd/autotask-builder service 설정 수정
14=E   # l1-study-mcd command/profile 수정
14=F   # Study Runner 초기화 문제 수정
14=G   # 진단 증거(log/receipt)부터 추가
14=H   # 현재 상태 안전 terminal 처리 후 새 Job으로 재실행
14=I   # 추가 정보 필요
```

---

# 16. 최종 출력 형식

설명은 길게 쓰지 말고 아래 형식만 사용해줘.

```text
1=A STATE=RUNNING PID=4033283
2=C RUNNING_WRITE=<...>
3=A SPAWN=<...>
4=D WORKER_LOG=<...> LOG_REASON=<...>
5=G EXIT=NA
6=C TRANSITION=<...>
7=A OWNER=<...>
8=A
9=C
10=C RECOVERY=<...>
11=E
12=G
13=B
14=C

15=문제: <한 줄 root cause>
16=근거: <가장 강한 실제 증거 1~2개>
17=다음조치: <최소 조치 1줄>
```

---

# 17. 출력 제한

```text
번호는 숫자만 사용
객관식 우선
한 항목 최대 1줄
로그 대량 출력 금지
소스코드 전체 출력 금지
추측 금지
자동 수정 금지
자동 재실행 금지
민감정보 출력 금지
```

특히 이번 진단의 핵심은 다음 세 질문이다.

```text
1. child가 실제 spawn 되었는가?
2. spawn 되었다면 왜 completion receipt 없이 사라졌는가?
3. Job-list가 dead child를 왜 RUNNING에서 회수하지 못했는가?
```

이 세 가지를 실제 증거로 판정해줘.
