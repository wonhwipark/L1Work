# Job-list Stuck Recovery Baseline 준비 프롬프트

## 사용 조건

이 프롬프트는 이전 주말 2시간 Autotask 설정 결과가:

```text
8 = PASS_WITH_RECOVERY_GAP
```

인 경우에만 실행한다.

목적은 **현재 정상 상태를 baseline으로 저장하고, 향후 job-list/updater가 stuck 되었을 때 안전하게 판단할 수 있는 정보만 준비하는 것**이다.

이번 작업에서는:

```text
프로세스 강제 종료 금지
job-list 코드 수정 금지
skill-updater 코드 수정 금지
skillsilent 코드 수정 금지
retry 강제 실행 금지
remote job revision 변경 금지
Wave / Activation 실행 금지
```

한다.

---

# 0. 현재 기준

```text
skill-updater = v0.5.11
skillsilent = v0.2.38
job-list = v0.2.1

주말 autotask = 토/일 2시간 간격
OVERLAP_POLICY = DO_NOT_START_NEW_INSTANCE
```

운영 목적:

```text
stuck이 생겼을 때
무조건 kill/retry하지 않고
현재 process와 job identity를 정확히 식별할 수 있도록 baseline을 준비한다.
```

---

# 1. STEP 1 — 현재 실행 상태 확인

현재 다음 프로세스가 실행 중인지 READ-ONLY로 확인한다.

```text
skill-updater
job-list
skillsilent
Claude/OpenCode CLI
```

각 프로세스에 대해 가능한 경우:

```text
PID
process name
command line
start time
parent PID
```

를 수집한다.

중요:

```text
어떤 프로세스도 종료하지 않는다.
```

현재 updater/job-list가 실행 중이라면
이 baseline 준비 작업 때문에 중단하지 않는다.

---

# 2. STEP 2 — Scheduler baseline 수집

실제 skill-updater 예약 task에서 다음을 읽는다.

```text
TASK_NAME
TASK_ID
STATUS
NEXT_RUN_TIME
LAST_RUN_TIME
LAST_RUN_RESULT
TRIGGER
REPETITION_INTERVAL
MULTIPLE_INSTANCES_POLICY
START_WHEN_AVAILABLE
```

기대:

```text
SCHEDULE = SAT_SUN_EVERY_2H
OVERLAP_POLICY = DO_NOT_START_NEW_INSTANCE
```

실제 설정값을 그대로 기록한다.

---

# 3. STEP 3 — skill-updater baseline 수집

현재 설치된 `skill-updater v0.5.11`의 실제 runtime/config/log에서 다음을 확인한다.

```text
installed version
job_sync enabled 여부
remote repository
remote branch/ref
remote job path
latest updater run
latest updater exit/result
```

remote job path는 실제 설정을 사용하고 추측하지 않는다.

기대 기본 형태:

```text
automation/job-list.json
```

remote queue 파일은 READ-ONLY로 확인한다.

---

# 4. STEP 4 — job-list runtime 상태 수집

현재 설치된 `job-list v0.2.1`의 실제 runtime/output/history에서
존재하는 파일만 읽는다.

우선 후보:

```text
~/.claude/main/job-list/output/last_run.json
~/.claude/main/job-list/output/runs/
~/.claude/main/job-list/output/actions/
~/.claude/main/job-list/history/job_history.jsonl
```

실제 경로가 다르면 package/config 근거로 실제 경로를 사용한다.

최근 job에 대해 가능한 범위에서 다음을 수집한다.

```text
job_id
revision
run_id
status
started_at
finished_at
exit_code
skill
action/mode
```

없는 필드는 임의로 만들지 말고 `UNKNOWN`으로 둔다.

---

# 5. STEP 5 — Stuck 판정에 사용할 identity 필드 확인

현재 구현에서 다음 정보가 실제로 기록되는지 확인한다.

```text
job_id
revision
run_id
pid
process command
started_at
last_heartbeat
status
retry_count
```

각 항목:

```text
YES
NO
PARTIAL
UNKNOWN
```

으로 분류한다.

이 단계는 향후 자동 recovery 설계에 필요한 gap을 찾기 위한 것이다.

---

# 6. STEP 6 — Heartbeat / lease / lock 현황 확인

현재 job-list/updater 코드와 runtime을 READ-ONLY로 확인해서
다음 기능을 실제 지원하는지 판정한다.

```text
RUNNING lock/lease
heartbeat writer
heartbeat timestamp
stale heartbeat threshold
max runtime
stale RUNNING detection
safe recovery
retry/resume
completed id:revision guard
```

각 항목:

```text
YES
NO
PARTIAL
UNKNOWN
```

으로 출력한다.

구현되지 않은 기능을 임의로 생성하지 않는다.

---

# 7. STEP 7 — Baseline snapshot 저장

가능하면 현재 정상 상태 정보를 하나의 JSON으로 저장한다.

권장 위치:

```text
~/.claude/main/job-list/recovery/
```

단, 기존 job-list/runtime이 이미 recovery/baseline용 정상 위치를 제공하면
그 위치를 우선 사용한다.

새 디렉터리 생성이 필요하고 안전하게 가능한 경우에만 생성한다.

파일명:

```text
stuck_recovery_baseline_<YYYYMMDD_HHMMSS>.json
```

최소 내용:

```json
{
  "captured_at": "...",
  "scheduler": {},
  "updater": {},
  "job_list": {},
  "current_processes": [],
  "identity_fields": {},
  "recovery_capabilities": {}
}
```

이 JSON은 **관찰 결과만 기록**해야 한다.

프로세스 제어 명령이나 자동 kill 명령을 포함하지 않는다.

---

# 8. STEP 8 — 수동 Recovery 판단 규칙 파일 준비

같은 위치에 가능하면 다음 파일을 생성한다.

```text
stuck_recovery_manual_guide.md
```

내용은 아래 규칙만 포함한다.

## A. 정상 실행 중

```text
process exists
+ command identity matches
+ 최근 heartbeat 또는 최근 로그 진행 존재
```

→ 아무 작업도 하지 않는다.

```text
ACTION=KEEP_RUNNING
```

## B. 다음 trigger 도래했지만 이전 실행 존재

Scheduler가:

```text
DO_NOT_START_NEW_INSTANCE
```

이면 정상 보호 동작으로 본다.

```text
ACTION=BUSY_SKIP
```

프로세스를 kill하지 않는다.

## C. Stuck 의심

다음이 모두 객관적으로 확인될 때만:

```text
동일 job_id
동일 revision
동일 run_id
PID 존재
process command 일치
장시간 로그/heartbeat 진행 없음
```

stale 후보로 분류한다.

```text
ACTION=STALE_CANDIDATE
```

여기서도 자동 kill하지 않는다.

## D. 완료된 동일 revision

```text
status = completed
same id:revision
```

이면:

```text
ACTION=NEVER_RETRY
```

## E. 작업 내용을 변경해서 다시 실행해야 함

```text
revision 증가 필요
```

로 기록한다.

## F. 단순 interrupted/stale 복구

현재 구현에 공식 retry/resume 인터페이스가 있을 때만
그 인터페이스 사용 후보로 기록한다.

공식 기능이 없으면 임의 실행하지 않는다.

---

# 9. STEP 9 — Stuck recovery 개선 필요사항 정리

현재 기능 gap을 다음 우선순위로 정리한다.

```text
P0 = 중복 실행 방지
P1 = process/job identity
P1 = heartbeat
P1 = stale detection
P1 = safe retry/resume
P2 = max runtime
P2 = recovery history
```

각 항목에 대해:

```text
IMPLEMENTED
PARTIAL
MISSING
UNKNOWN
```

을 기록한다.

이번 프롬프트에서 구현은 하지 않는다.

---

# 10. STEP 10 — 퇴근 가능 여부 확인

최종적으로 다음 조건을 확인한다.

```text
주말 2시간 Scheduler 정상
OVERLAP_POLICY=DO_NOT_START_NEW_INSTANCE
skill-updater/job_sync 설정 정상
remote queue 존재
baseline 저장 성공
현재 실행 중인 updater/job-list가 비정상 상태 아님
```

모두 만족하면:

```text
SAFE_TO_LEAVE=YES
```

현재 updater/job-list가 정상 실행 중이어도
CLI/VSCode에 의존하지 않는 예약 실행 구조라면:

```text
SAFE_TO_CLOSE_VSCODE_AND_CLI=YES
```

로 판정할 수 있다.

단, 현재 수동 CLI 프로세스가 작업 자체를 소유하고 있어
종료하면 실행이 중단되는 구조라면 `NO`로 판정한다.

---

# 11. 최종 판정 코드

첫 줄에는 숫자 하나만 출력한다.

```text
1 = BASELINE_READY
    baseline/guide 생성 완료
    schedule/overlap 안전
    퇴근 가능

2 = BASELINE_PARTIAL
    일부 정보는 부족하지만 운영 상태는 안전
    추후 recovery 설계 가능

3 = PROCESS_IDENTITY_GAP
    stuck 시 안전하게 process를 식별할 정보가 부족

4 = HEARTBEAT_GAP
    heartbeat/stale 판정 근거가 부족

5 = SCHEDULER_UNSAFE
    overlap 방지가 보장되지 않음

6 = JOB_SYNC_UNSAFE
    updater/job_sync/remote queue 상태 이상

7 = CURRENT_RUN_UNSAFE
    현재 updater/job-list 실행 상태가 비정상

8 = SNAPSHOT_FAIL
    baseline 파일 저장 실패

9 = CRITICAL
    예상하지 않은 변경/중복 실행/위험 상태 발견

0 = UNKNOWN
```

---

# 12. 최종 출력 형식

첫 줄:

```text
<0~9 숫자>
```

그 아래 최대 18줄:

```text
SCHEDULE=PASS|FAIL|UNKNOWN
OVERLAP_POLICY=PASS|FAIL|UNKNOWN
CURRENT_UPDATER_PROCESS=RUNNING|NOT_RUNNING|UNKNOWN
CURRENT_JOBLIST_PROCESS=RUNNING|NOT_RUNNING|UNKNOWN
JOB_ID=<value|NONE|UNKNOWN>
REVISION=<value|NONE|UNKNOWN>
RUN_ID=<value|NONE|UNKNOWN>
PID_TRACKING=YES|NO|PARTIAL|UNKNOWN
COMMAND_TRACKING=YES|NO|PARTIAL|UNKNOWN
HEARTBEAT=YES|NO|PARTIAL|UNKNOWN
STALE_DETECTION=YES|NO|PARTIAL|UNKNOWN
RETRY_RESUME=YES|NO|PARTIAL|UNKNOWN
COMPLETED_REVISION_GUARD=YES|NO|UNKNOWN
BASELINE_JSON=<path|NONE>
MANUAL_GUIDE=<path|NONE>
SAFE_TO_CLOSE_VSCODE_AND_CLI=YES|NO
SAFE_TO_LEAVE=YES|NO
NEXT_STEP=NONE|DESIGN_STUCK_RECOVERY|STOP_AND_ANALYZE
```

---

# 13. NEXT_STEP 규칙

## 결과 1

```text
NEXT_STEP=DESIGN_STUCK_RECOVERY
```

운영은 그대로 시작하고,
향후 별도 버전에서 stuck recovery를 보강한다.

## 결과 2 / 3 / 4

```text
NEXT_STEP=DESIGN_STUCK_RECOVERY
```

단, 현재 overlap 보호가 PASS일 때만 주말 운영을 허용한다.

## 결과 5~9 / 0

```text
NEXT_STEP=STOP_AND_ANALYZE
```

---

# 14. 절대 원칙

이번 프롬프트는 **관찰 + baseline 저장 + manual guide 생성**까지만 한다.

절대 하지 않는다:

```text
task kill
PID kill
lock 삭제
running state 강제 수정
history 삭제
queue 삭제
retry 강제 실행
revision 증가
job-list 코드 수정
skill-updater 코드 수정
skillsilent 코드 수정
Wave 진행
Activation 진행
```

추가 질문하지 말고 현재 PC의 실제 정보로 최대한 수행한다.
