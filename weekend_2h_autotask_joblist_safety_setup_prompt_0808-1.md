# 주말 2시간 Autotask + Job-list 안전 운영 설정 프롬프트

## 목적

회사 PC의 현재 실제 설정을 기준으로 다음을 수행한다.

```text
1. 현재 autotask / Windows Task Scheduler 설정 확인
2. 주말에만 2시간 간격으로 skill-updater가 실행되도록 설정
3. 이전 실행이 끝나지 않았으면 새 인스턴스를 시작하지 않도록 설정/검증
4. skill-updater → job_sync → job-list 흐름이 유지되는지 확인
5. job-list stuck recovery 기능이 현재 구현되어 있는지 READ-ONLY 점검
6. 다음 실행 시각을 실제 Scheduler 값으로 확인
7. 퇴근 가능한 상태인지 최종 판정
```

이번 작업에서는 Skill migration/Wave/Activation을 수행하지 않는다.

---

# 0. 현재 기준

현재 기준 버전:

```text
skill-updater = v0.5.11
skillsilent = v0.2.38
job-list = v0.2.1
```

운영 의도:

```text
평일 자동 실행 = 하지 않음
주말 자동 실행 = 2시간 간격
```

주말의 의미:

```text
Saturday
Sunday
```

기대 실행 시각의 논리 기준:

```text
토요일:
00:00 / 02:00 / 04:00 / 06:00 / 08:00 / 10:00
12:00 / 14:00 / 16:00 / 18:00 / 20:00 / 22:00

일요일:
00:00 / 02:00 / 04:00 / 06:00 / 08:00 / 10:00
12:00 / 14:00 / 16:00 / 18:00 / 20:00 / 22:00
```

단, 실제 autotask-builder/Windows Scheduler가 이 표현을 지원하는지 먼저 확인하고,
지원하지 않는 방식을 임의로 만들지 않는다.

---

# 1. 절대 금지

이번 설정 작업에서는 다음을 하지 마.

```text
Skill Wave 진행
Activation
Skill source 수정
Skill source MOVE/DELETE/RENAME
~/.claude/main/<skill> 수정
~/.claude/skills/<skill> 수정
~/l1sw-skills/private-skills/<skill> 수정
skillsilent 업데이트
skill-updater 업데이트
job-list 코드 수정
job-list 버전업
stuck process 강제 kill
GitHub unrelated 파일 변경
```

`job-list stuck recovery`는 이번에는 기능 존재 여부와 안전성만 점검한다.

---

# 2. STEP 1 — 현재 Autotask 실제 설정 확인

현재 회사 PC에 설치된 autotask-builder 및 Windows Task Scheduler에서
skill-updater를 실행하는 실제 task를 찾는다.

추측하지 말고 다음을 실제 설정에서 확인한다.

```text
TASK_NAME
TASK_ID
EXECUTABLE / COMMAND
START_BOUNDARY
REPETITION_INTERVAL
REPETITION_DURATION
DAYS_OF_WEEK / TRIGGER
ENABLED
MULTIPLE_INSTANCES_POLICY
RUN_WHETHER_USER_LOGGED_ON
WAKE_TO_RUN
START_WHEN_AVAILABLE
NEXT_RUN_TIME
LAST_RUN_TIME
LAST_RUN_RESULT
```

가능하면 autotask-builder가 관리하는 YAML/config도 함께 확인한다.

중복 task가 존재하면 어떤 것이 실제 운영 task인지 객관적으로 구분한다.

판정:

```text
STEP1=1  # 실제 운영 task 식별 성공
STEP1=2  # task 없음
STEP1=3  # 중복/충돌 task 존재
STEP1=9  # 확인 불가
```

STEP1이 1이 아니면 변경하지 말고 STOP.

---

# 3. STEP 2 — 주말 2시간 표현 가능 여부 확인

현재 autotask-builder의 실제 CLI/help/config/schema를 읽어서 다음 조건을
공식적으로 표현할 수 있는지 확인한다.

```text
Saturday + Sunday only
2 hour interval
00:00 anchor
주말 전체 반복
```

## 우선 원칙

autotask-builder가 직접 지원하면 해당 정상 인터페이스를 사용한다.

지원하지 않으면 Windows Task Scheduler의 기존 task 구조에서
동등하고 명확하게 표현 가능한지 확인한다.

### 허용 가능한 예

```text
토요일 00:00 시작 + 2시간 반복 + 1일 duration
일요일 00:00 시작 + 2시간 반복 + 1일 duration
```

또는 Scheduler가 지원하는 동등한 주말 trigger.

### 금지

```text
임의 PowerShell background loop
sleep 기반 무한 loop
새로운 별도 daemon
정체불명의 wrapper script
평일까지 실행되는 7일 반복
```

판정:

```text
STEP2=1  # 안전하게 표현 가능
STEP2=2  # 현재 도구에서 정확한 주말 2시간 표현 불가
STEP2=9  # 확인 불가
```

STEP2가 1이 아니면 변경하지 말고 STOP.

---

# 4. STEP 3 — 주말 2시간 Schedule 설정

STEP1/2 PASS일 때만 실제 schedule을 설정한다.

목표:

```text
평일 = 자동 실행 없음
토요일 = 00:00부터 2시간 간격
일요일 = 00:00부터 2시간 간격
```

기존 skill-updater 실행 command 자체는 변경하지 않는다.

가능하면 기존 autotask-builder의 정상 deploy/update 흐름을 사용한다.

기존 task를 업데이트할 수 있으면 불필요한 새 task를 만들지 않는다.

변경 전 설정을 rollback 가능한 형태로 기록한다.

예:

```text
~/.claude/main/autotask/.../backup/
```

또는 기존 도구가 사용하는 정상 backup/state 위치.

새 위치를 임의로 만들 필요가 없다.

---

# 5. STEP 4 — 중복 실행 방지

가장 중요한 안전 조건이다.

Windows Task Scheduler 또는 autotask-builder 설정에서
이전 skill-updater 실행이 아직 살아 있을 때 다음 예약 시각이 도래하면:

```text
새 인스턴스를 시작하지 않는다.
```

를 보장해야 한다.

Windows Task Scheduler 의미상 가능한 경우:

```text
If the task is already running:
Do not start a new instance
```

계열 설정을 사용한다.

현재 도구가 지원하는 정확한 option 이름을 확인해서 적용한다.

금지:

```text
parallel instance
queue unlimited
stop existing instance and restart
```

이번 단계에서는 기존 실행 프로세스를 강제로 종료하지 않는다.

판정:

```text
OVERLAP_POLICY=DO_NOT_START_NEW_INSTANCE
```

가 객관적으로 확인되어야 PASS.

---

# 6. STEP 5 — 놓친 실행 / 전원 상태 관련 설정

회사 정책 및 현재 task 기능이 허용하는 범위에서 확인한다.

권장:

```text
START_WHEN_AVAILABLE = enabled
```

즉 예약 시각을 놓쳤으면 가능한 다음 시점에 실행.

PC 절전 정책과 충돌하지 않는 범위에서:

```text
WAKE_TO_RUN
```

지원 여부를 확인한다.

단, 회사 보안/전원 정책을 우회하지 않는다.

`RUN_WHETHER_USER_LOGGED_ON`도 현재 회사 정책과 기존 task 설정을 존중한다.
기존에 정상 동작하던 보안 context를 임의 변경하지 않는다.

---

# 7. STEP 6 — updater / job_sync 구조 검증

schedule 변경 후 command 자체가 여전히 기존 skill-updater를 호출하는지 확인한다.

기대 흐름:

```text
Windows Task Scheduler
→ skill-updater v0.5.11
→ 일반 Skill update/check
→ job_sync
→ remote automation/job-list.json
→ 새 id:revision 존재 시 job-list
```

다음을 확인한다.

```text
skill-updater self-update = scheduled target 아님
skillsilent self-update = scheduled target 아님
job_sync = enabled
remote job-list path = 기존 정상 값 유지
```

remote:

```text
automation/job-list.json
```

이 실제 repository에 존재하는지도 READ-ONLY로 확인한다.

없으면 이번 작업에서 임의 migration job을 만들지 말고 FAIL 판정한다.

---

# 8. STEP 7 — Job-list stuck recovery 현황 READ-ONLY 점검

현재 설치된:

```text
skill-updater v0.5.11
job-list v0.2.1
```

코드/config/help를 읽어서 다음 기능이 실제 구현되어 있는지 확인한다.

```text
A. running job lock / lease
B. heartbeat
C. stale heartbeat 판단
D. max runtime / timeout
E. stale RUNNING recovery
F. retry/resume
G. PID + command/run_id 검증 후 종료
H. completed id:revision 재실행 방지
```

각 항목을:

```text
YES
NO
PARTIAL
UNKNOWN
```

으로 분류한다.

중요:

```text
이번 프롬프트에서는 stuck process를 kill하지 않는다.
job-list/updater 코드를 수정하지 않는다.
```

현재 recovery가 미흡해도 schedule 설정 자체가 안전하면
`RECOVERY_STATUS=PARTIAL`로 기록하고 운영 가능 여부를 별도로 판정한다.

---

# 9. STEP 8 — 2시간 주기와 stuck 상태의 안전성 판정

다음 조건이면 주말 2시간 주기를 허용한다.

```text
OVERLAP_POLICY = DO_NOT_START_NEW_INSTANCE
```

즉 한 job/updater가 2시간을 넘겨 살아 있어도
다음 Scheduler trigger가 두 번째 updater를 병렬 시작하지 않아야 한다.

이 경우:

```text
stuck recovery가 완전하지 않아도
중복 실행 사고는 방지 가능
```

하지만 장시간 stuck은 다음 주기까지 계속 block할 수 있으므로
별도 개선 대상으로 표시한다.

다음이면 운영 금지:

```text
이전 실행이 살아 있는데 새 인스턴스가 병렬 실행됨
```

---

# 10. STEP 9 — 실제 다음 실행 시각 확인

설정 완료 후 Windows Task Scheduler가 계산한 실제 값을 읽는다.

추측해서 계산하지 말고 실제:

```text
Next Run Time
```

을 출력한다.

현재 시각 이후의 최소 다음 4개 예약 시각도 가능한 경우 확인한다.

기대 패턴:

```text
Saturday/Sunday
2시간 간격
```

평일 시각이 포함되면 FAIL.

---

# 11. STEP 10 — 수동 실행은 선택적으로 1회만

schedule 변경만으로 검증이 충분하면 skill-updater를 실행하지 않아도 된다.

기존 task command 자체의 동작 검증이 필요할 경우에만
현재 정상 인터페이스로 수동 1회 실행할 수 있다.

수동 실행한 경우:

```text
동시에 예약 실행이 겹치지 않는지 확인
job_sync까지 정상 도달하는지 확인
```

반복 실행 금지.

Wave/Activation job은 생성하지 않는다.

---

# 12. STEP 11 — 퇴근 전 종료 상태 확인

자동 실행 설정과 별개로 다음을 확인한다.

```text
현재 skill-updater process = 없음
현재 job-list process = 없음
현재 skillsilent 실행 process = 없음
Claude/OpenCode CLI = 종료 가능 상태
VSCode = 종료 가능 상태
Task Scheduler = Ready
Next Run Time = 정상
```

주의:

Claude/VSCode를 자동으로 강제 종료하지 마.

최종 결과에서:

```text
SAFE_TO_CLOSE_VSCODE_AND_CLI=YES
```

가 확인되면 사용자에게 종료 가능하다고 알려준다.

---

# 13. 최종 판정 코드

첫 줄에 숫자 하나만 출력한다.

```text
1 = PASS
    주말 2시간 schedule 정상
    overlap 방지 정상
    updater/job_sync 구조 정상
    next run 정상
    퇴근 가능

2 = TASK_NOT_FOUND
    실제 운영 autotask를 찾지 못함

3 = SCHEDULE_UNSUPPORTED
    현재 도구에서 주말 2시간을 안전하게 표현 불가

4 = SCHEDULE_APPLY_FAIL
    설정 변경 실패

5 = OVERLAP_UNSAFE
    이전 실행 중 새 인스턴스가 시작될 가능성 있음

6 = JOB_SYNC_CONFIG_FAIL
    updater/job_sync/remote queue 구조 이상

7 = SCHEDULE_VERIFY_FAIL
    Next Run Time 또는 주말 조건 검증 실패

8 = PASS_WITH_RECOVERY_GAP
    주말 2시간 운영은 가능하지만 job-list stuck 자동복구가 불완전함

9 = CRITICAL
    중복 실행/잘못된 command/예상 밖 파일 변경 등 위험 상태

0 = UNKNOWN
    객관적 판단에 필요한 정보 부족
```

---

# 14. 최종 출력 형식

첫 줄:

```text
<0~9 숫자>
```

그 아래 최대 18줄:

```text
TASK_NAME=<value|UNKNOWN>
SCHEDULE=SAT_SUN_EVERY_2H|OTHER|UNKNOWN
ANCHOR=00:00|OTHER|UNKNOWN
NEXT_RUN=<actual scheduler value|UNKNOWN>
OVERLAP_POLICY=DO_NOT_START_NEW_INSTANCE|OTHER|UNKNOWN
START_WHEN_AVAILABLE=YES|NO|UNKNOWN
WAKE_TO_RUN=YES|NO|POLICY_DEPENDENT|UNKNOWN
UPDATER_VERSION=0.5.11|OTHER|UNKNOWN
SILENT_VERSION=0.2.38|OTHER|UNKNOWN
JOB_LIST_VERSION=0.2.1|OTHER|UNKNOWN
JOB_SYNC=PASS|FAIL|UNKNOWN
REMOTE_QUEUE=PASS|FAIL|UNKNOWN
HEARTBEAT=YES|NO|PARTIAL|UNKNOWN
STALE_RECOVERY=YES|NO|PARTIAL|UNKNOWN
RETRY_RESUME=YES|NO|PARTIAL|UNKNOWN
COMPLETED_REVISION_GUARD=YES|NO|UNKNOWN
SAFE_TO_CLOSE_VSCODE_AND_CLI=YES|NO
NEXT_STEP=NONE|DESIGN_STUCK_RECOVERY|STOP_AND_ANALYZE
```

## NEXT_STEP 규칙

`1 = PASS`:

```text
NEXT_STEP=NONE
```

`8 = PASS_WITH_RECOVERY_GAP`:

```text
NEXT_STEP=DESIGN_STUCK_RECOVERY
```

나머지:

```text
NEXT_STEP=STOP_AND_ANALYZE
```

---

# 15. 최종 운영 원칙

이번 작업의 성공 상태는:

```text
주말 2시간마다 Scheduler가 skill-updater를 호출한다.
이전 실행이 남아 있으면 다음 인스턴스는 시작하지 않는다.
새 remote job revision이 있을 때만 job-list가 처리한다.
완료된 동일 revision은 재실행하지 않는다.
stuck 자동복구가 부족하면 별도 개선 대상으로 남긴다.
VSCode/CLI를 열어두는 것에 의존하지 않는다.
```

이다.

추가 질문하지 말고 현재 PC의 실제 설정과 실제 코드만 근거로 최대한 진행한다.
