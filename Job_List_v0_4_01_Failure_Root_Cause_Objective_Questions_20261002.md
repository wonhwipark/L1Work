# Job-list v0.4.01 실패 Root Cause 진단 — 숫자 객관식 질문

- 기준 시점: 2026-10-02 KST
- 분석 대상: `job-list_v0_4_01_1002`
- 대상 환경: 사내 Windows PC
- 목적: **수정 전에 First Failed Stage와 Primary Root Cause를 evidence 기준으로 확정**
- 중요: **이 프롬프트 수행 중에는 어떤 파일도 수정/삭제/재등록하지 않는다. 진단만 수행한다.**

---

# 0. 분석 대상과 핵심 전제

이번 분석 대상 Job은 다음이다.

```text
Job-list version
v0.4.01

Job ID
JOB-20261002-DISPATCHER-RECOVERY-V0401

Profile
dispatcher-autotask-register-windows

Target OS
Windows

Target schedule
매시 15분 / 45분
cron = 15,45 * * * *
Windows Scheduler representation:
StartBoundary phase = :15 또는 :45
Repetition Interval = PT30M

Expected semantic output
output/dispatcher_autotask_register/latest_result.json
```

v0.4.01의 의도된 실행 체인은 다음과 같다.

```text
job-list v0.4.01 package
→ skill-updater detection/install
→ job-list validation
→ bundled request activation
→ queue
→ runtime / pending gate
→ runner
→ dispatcher-autotask-register-windows
→ AutoTask Builder
→ Windows Task Scheduler
→ immediate run request
→ Dispatcher
→ local state / heartbeat evidence
→ latest_result.json
→ job result validation
→ processed SUCCESS
```

## 매우 중요

다음은 **동일한 실패가 아니다.**

```text
A. v0.4.01 자체가 updater에서 탐지되지 않음
B. 탐지/설치됐지만 bundled request activation 실패
C. activation됐지만 과거 PENDING/RUNNING Job 때문에 실행 지연
D. runner까지 갔지만 profile entrypoint 미진입
E. AutoTask Builder 단계 실패
F. Scheduler 등록/실행 실패
G. Dispatcher는 실행됐지만 heartbeat signal만 실패
H. 실제 Job은 성공했는데 후단 output/result validation이 실패
```

**signal counter가 증가하지 않았다는 사실만으로 Dispatcher 실패로 결론 내리지 않는다.**

---

# 1. 수행 원칙

아래 순서를 반드시 지켜라.

```text
1. 자동으로 확인 가능한 파일/로그/state를 먼저 확인
2. 추측 금지
3. 서로 다른 날짜/run/attempt evidence 혼합 금지
4. 최신 v0.4.01 attempt를 우선 식별
5. 질문 Q1~Q40에 숫자로 답변
6. 필요한 경우에만 Evidence E1~E10 추가
7. 수정/복구/재실행 금지
8. 최종적으로 First Failed Stage 후보까지만 판정
```

파일을 찾을 때 전체 디스크 recursive scan을 하지 말고 아래 표준 위치와 실제 configured path를 우선 사용한다.

```text
~/l1sw-private-skills/job-list/
~/l1sw-private-skills/skill-updater/
~/l1sw-private-skills/l1sw-dispatcher/
~/.claude/skills/job-list/
Windows Task Scheduler
Job-list data/
Job-list output/
Updater data/output/log/history
Dispatcher data/state/log/signals
```

---

# 2. 답변 규칙

모든 Q 질문은 아래 숫자 중 하나만 선택한다.

```text
0 = 확인 불가 / evidence 없음
1 = YES / 정상 / 존재 / PASS
2 = NO / 비정상 / 없음 / FAIL
3 = 해당 없음 또는 다른 상태
```

질문의 개별 선택지가 별도로 정의되어 있으면 그 선택지를 우선한다.

## 최종 답변 형식

반드시 아래 형태로만 답한다.

```text
Q1-Q10:
1 1 2 0 1 1 3 1 2 0

Q11-Q20:
...

Q21-Q30:
...

Q31-Q40:
...

E1: <요청된 evidence 한 줄>
E2: <요청된 evidence 한 줄>
...
```

장문의 설명이나 해결책은 작성하지 않는다.

---

# 3. Phase A — 패키지 / Skill-Updater 탐지

## Q1. 사내 canonical Job-list VERSION은 실제로 `0.4.01`인가?

확인 예:

```text
~/l1sw-private-skills/job-list/VERSION
```

```text
1 = 0.4.01
2 = 다른 버전
0 = 확인 불가
```

---

## Q2. 설치된 Job-list lifecycle.json의 version도 `0.4.01`인가?

```text
1 = 0.4.01
2 = 다른 버전 또는 lifecycle 불일치
0 = 확인 불가
```

---

## Q3. 설치된 Job-list에 `JOB-20261002-DISPATCHER-RECOVERY-V0401` 정의/evidence가 존재하는가?

README/lifecycle/bundled request/activation source 중 실제 실행에 사용되는 위치를 확인한다.

```text
1 = 존재
2 = 없음
0 = 확인 불가
```

---

## Q4. 설치된 Skill-Updater는 v0.5.33 계열인가?

```text
1 = v0.5.33
2 = v0.5.32 이하 또는 다른 버전
0 = 확인 불가
```

---

## Q5. v0.4.01 배포 이후 Skill-Updater가 실제로 최소 한 번 실행되었는가?

timestamp/history/log evidence 기준.

```text
1 = 실행됨
2 = 실행 evidence 없음
0 = 확인 불가
```

---

## Q6. 해당 updater cycle에서 Job-list v0.4.01 package를 탐지했는가?

```text
1 = v0.4.01 탐지 evidence 있음
2 = 탐지하지 못함
0 = 확인 불가
```

---

## Q7. updater가 v0.4.01을 canonical Job-list 위치에 설치/갱신했는가?

```text
1 = 설치 성공 evidence 있음
2 = 설치 실패 또는 이전 버전 유지
0 = 확인 불가
```

---

## Q8. 설치 후 Job-list self-test / validation은 PASS했는가?

예:

```text
python scripts/job_core.py validate
```

기존 실행 로그/evidence만 확인하고 새로 변경 작업은 하지 않는다.

```text
1 = PASS
2 = FAIL
0 = 실행 결과 확인 불가
```

---

## Q9. updater가 v0.4.01 설치 후 Job-list activation/launch를 호출한 evidence가 있는가?

```text
1 = activation/launch 호출됨
2 = 설치만 하고 activation 호출 없음
0 = 확인 불가
```

---

## Q10. Updater 단계에서 fatal/error 때문에 Job-list activation 전 종료된 evidence가 있는가?

```text
1 = fatal/error 있음
2 = 없음
0 = 확인 불가
```

Q10=1이면 `E1`에 **최초 fatal/error 문구 + 파일 + line/timestamp**를 기록한다.

---

# 4. Phase B — Activation / Queue / 이전 Job 충돌

## Q11. `JOB-20261002-DISPATCHER-RECOVERY-V0401`이 activation history 또는 queue에 실제 등장했는가?

```text
1 = 등장함
2 = 등장하지 않음
0 = 확인 불가
```

---

## Q12. v0.4.01 Job이 duplicate / already-used / processed gate에 막혔는가?

```text
1 = 막힘
2 = 막히지 않음
0 = 확인 불가
```

Q12=1이면 `E2`에 관련 status/error를 기록한다.

---

## Q13. v0.4.01 Job이 expired gate에 막혔는가?

```text
1 = EXPIRED evidence 있음
2 = 아님
0 = 확인 불가
```

---

## Q14. v0.4.01 activation 직후 queue에 해당 Job이 PENDING으로 존재했는가?

```text
1 = 존재
2 = 존재하지 않음
0 = 확인 불가
```

---

## Q15. 당시 v0.4.00 또는 그 이전 recovery Job이 PENDING 상태로 남아 있었는가?

특히 다음 계열을 확인한다.

```text
V0397
V0399
V0400
기타 recovery/updater-gate Job
```

```text
1 = 과거 PENDING 존재
2 = 없음
0 = 확인 불가
```

Q15=1이면 `E3`에 **job_id / profile / priority / created_at**을 기록한다.

---

## Q16. v0.4.01보다 먼저 생성된 priority 100 Job이 queue에 있었는가?

```text
1 = 있음
2 = 없음
0 = 확인 불가
```

---

## Q17. v0.4.01과 과거 PENDING Job의 profile이 서로 달랐는가?

v0.4.01 profile:

```text
dispatcher-autotask-register-windows
```

```text
1 = 서로 다름
2 = 동일 profile
0 = 확인 불가
```

---

## Q18. v0.4.01이 same-profile supersede로 과거 Dispatcher PENDING을 `SUPERSEDED` 처리한 evidence가 있는가?

```text
1 = 있음
2 = 없음
3 = supersede할 동일 profile PENDING 자체가 없었음
0 = 확인 불가
```

---

## Q19. activation 당시 `running.json`이 존재했는가?

```text
1 = 존재
2 = 없음
0 = 확인 불가
```

---

## Q20. `running.json`의 Job이 실제 살아 있는 프로세스였는가?

PID/process/started_at 등으로 확인한다.

```text
1 = 실제 RUNNING process 존재
2 = stale running marker 또는 process 없음
3 = running.json 자체 없음
0 = 확인 불가
```

Q20=1 또는 2이면 `E4`에 **running job_id / profile / PID / 실제 process 존재 여부**를 기록한다.

---

# 5. Phase C — Runner 진입 여부

## Q21. v0.4.01 Job이 queue에서 실제 선택되어 RUNNING으로 전환된 evidence가 있는가?

```text
1 = RUNNING 진입
2 = PENDING에서 멈춤
0 = 확인 불가
```

---

## Q22. `dispatcher-autotask-register-windows` profile entrypoint가 실제 시작되었는가?

가장 강한 evidence 중 하나:

```text
output/dispatcher_autotask_register/latest_result.json
status = RUNNING
```

또는 해당 attempt의 fresh timestamp.

```text
1 = entrypoint 시작 evidence 있음
2 = 없음
0 = 확인 불가
```

---

## Q23. `latest_result.json`의 timestamp가 v0.4.01 실행 시점과 일치하는 새로운 파일인가?

과거 실행 결과를 잘못 읽지 않는다.

```text
1 = 이번 attempt의 fresh result
2 = 오래된/stale result
0 = 확인 불가
```

---

## Q24. profile 실행 전에 required output validation 때문에 실패했는가?

v0.4.01 Dispatcher profile required output:

```text
output/dispatcher_autotask_register/latest_result.json
```

```text
1 = entrypoint 전에 output validation failure
2 = 아님
0 = 확인 불가
```

---

# 6. Phase D — Dispatcher recovery script 내부

## Q25. Dispatcher canonical/allowlisted root를 찾았는가?

`latest_result.json`에서 `DISPATCHER_NOT_FOUND` 여부 포함.

```text
1 = 찾음
2 = DISPATCHER_NOT_FOUND
0 = 확인 불가
```

---

## Q26. AutoTask Builder를 찾았는가?

```text
1 = 찾음
2 = AUTOTASK_NOT_FOUND
3 = Builder는 없지만 이미-valid Scheduler task를 보존하여 진행 가능
0 = 확인 불가
```

---

## Q27. v0.4.01이 생성/사용한 canonical schedule이 `15,45 * * * *`였는가?

```text
1 = 정확히 15,45
2 = 다른 schedule
0 = 확인 불가
```

---

## Q28. AutoTask Builder YAML validation/check는 성공했는가?

```text
1 = PASS
2 = FAIL
3 = 기존 valid Scheduler task를 보존하여 deploy 불필요
0 = 확인 불가
```

Q28=2이면 `E5`에 check/deploy의 최초 error를 기록한다.

---

## Q29. Scheduler 등록 후 readback이 요구 조건을 만족했는가?

요구 조건:

```text
Enabled
+ StartBoundary phase :15 또는 :45
+ Repetition Interval PT30M
```

```text
1 = 모두 만족
2 = 하나 이상 불일치
0 = 확인 불가
```

---

## Q30. Scheduler 등록/검증 단계가 최종적으로 FATAL `SCHEDULER_NOT_VERIFIED`로 끝났는가?

```text
1 = FATAL/SCHEDULER_NOT_VERIFIED
2 = 아님
0 = 확인 불가
```

Q30=1이면 `E6`에 scheduler_after/readback 핵심값을 기록한다.

---

# 7. Phase E — Windows Scheduler 실제 실행

## Q31. v0.4.01이 Scheduler immediate run request까지 실행했는가?

예:

```text
scheduler-run-once
```

```text
1 = 실행 요청함
2 = 그 단계까지 도달하지 못함
0 = 확인 불가
```

---

## Q32. Scheduler task의 Last Run Time/Last Result가 immediate run 이후 갱신되었는가?

```text
1 = 갱신됨
2 = 갱신 안 됨
0 = 확인 불가
```

---

## Q33. Scheduler 실행 결과가 성공 계열이었는가?

```text
1 = 성공 / return code 0 계열
2 = 실패 / non-zero
3 = 실행 자체가 관측되지 않음
0 = 확인 불가
```

Q33=2이면 `E7`에 **Last Result / return code / task principal 정보**를 기록한다.

---

## Q34. 기존 정상 동작 중인 Skill-Updater Scheduled Task와 Dispatcher Task의 실행 principal/context가 달랐는가?

```text
1 = 다름
2 = 동일
3 = 비교 가능한 updater task 없음
0 = 확인 불가
```

---

# 8. Phase F — Dispatcher 자체 실행 및 heartbeat

## Q35. Scheduler immediate run 이후 Dispatcher의 local state가 advance했는가?

예:

```text
dispatcher_state_advanced
scheduler_state_advanced
```

```text
1 = advance함
2 = advance하지 않음
0 = 확인 불가
```

---

## Q36. heartbeat signal/counter가 실제 증가했는가?

```text
1 = 증가
2 = 증가하지 않음
0 = 확인 불가
```

**Q36=2만으로 Dispatcher 실패라고 판정하지 않는다.**

---

## Q37. 로그에 `signal failed os=windows stage=heartbeat-ok`가 존재하는가?

```text
1 = 존재
2 = 없음
0 = 확인 불가
```

---

## Q38. Scheduler 경로는 실패했지만 `autotask_direct_run`에서는 Dispatcher state가 advance했는가?

```text
1 = direct AutoTask 실행에서는 advance
2 = direct AutoTask에서도 advance하지 않음
3 = 해당 진단을 수행하지 않음
0 = 확인 불가
```

---

## Q39. AutoTask 경로도 실패했지만 `direct_dispatcher_run`에서는 Dispatcher state가 advance했는가?

```text
1 = direct Dispatcher 실행에서는 advance
2 = direct Dispatcher에서도 advance하지 않음
3 = 해당 진단을 수행하지 않음
0 = 확인 불가
```

---

# 9. 최종 결과

## Q40. v0.4.01의 `latest_result.json` 최종 status는 무엇인가?

```text
1 = VERIFIED_OK
2 = SCHEDULED_OK
3 = RECOVERED
4 = DEGRADED
5 = FATAL
6 = RUNNING에서 멈춤
7 = latest_result.json 자체가 이번 attempt에 생성되지 않음
0 = 확인 불가
```

Q40이 4~7이면 `E8`에 **status / summary / warnings**를 그대로 짧게 기록한다.

---

# 10. 추가 Evidence — 필요한 경우만

아래는 숫자 답변으로 Root Cause가 분리되지 않을 때만 작성한다.

```text
E1 = Updater 최초 fatal/error
E2 = activation duplicate/processed/expired evidence
E3 = v0.4.01보다 앞선 PENDING Job 정보
E4 = running.json + PID/process evidence
E5 = AutoTask check/deploy 최초 실패
E6 = Scheduler readback 핵심값
E7 = Scheduler Last Result + principal/context
E8 = latest_result 최종 status/summary/warnings
E9 = processed.jsonl에서 v0.4.01 최종 record
E10 = queue에서 v0.4.01 최종 상태
```

Evidence는 최대 1~3줄만 쓴다.

---

# 11. 숫자 답변 후 내부적으로 분류할 First Failed Stage 후보

이 항목은 **사용자 답변용이 아니라 분석자가 숫자 결과를 해석하기 위한 규칙**이다.

```text
A. PACKAGE_NOT_INSTALLED
   Q1/Q2/Q6/Q7 중 설치 체인이 깨짐

B. UPDATER_ACTIVATION_NOT_CALLED
   설치는 됐으나 Q9=2

C. ACTIVATION_GATE_FAILURE
   Q12=1 또는 Q13=1

D. LEGACY_PENDING_BLOCK
   Q14=1 + Q15=1/Q16=1 + Q21=2

E. LIVE_RUNNING_BLOCK
   Q19=1 + Q20=1 + Q21=2

F. RUNNER_NOT_ENTERED
   Q21=1이어야 하는데 Q22=2

G. DISPATCHER_PROFILE_START_FAILURE
   Q22=1이나 Q25/Q26에서 FATAL

H. AUTOTASK_VALIDATION_OR_DEPLOY_FAILURE
   Q28=2 또는 Q30=1

I. SCHEDULER_EXECUTION_CONTEXT_FAILURE
   Q29=1 + Q31=1 + Q32/Q33 실패
   특히 Q38=1이면 Scheduler/logon context 우선 의심

J. AUTOTASK_RUNNER_FAILURE
   Scheduler 실패 + Q38=2 + Q39=1

K. DISPATCHER_RUNTIME_FAILURE
   Q39=2

L. HEARTBEAT_TRANSPORT_ONLY
   Q35=1 + Q36=2 + Q37=1
   이 경우 Dispatcher 실행 자체와 signal transport를 분리

M. RESULT_VALIDATION_FAILURE
   실행 evidence는 성공인데 processed 최종 상태가 FAIL인 경우
```

---

# 12. 분석 종료 조건

숫자 답변과 E1~E10을 확보하면 **여기서 종료**한다.

금지:

```text
- Job-list 수정
- Skill-Updater 수정
- Dispatcher 수정
- AutoTask Builder 수정
- Scheduler task 삭제/재등록
- processed.jsonl 삭제
- queue 강제 초기화
- running.json 강제 삭제
- signal 파일 강제 생성
- v0.4.02 실행
```

다음 대화에서 이 답변을 기반으로:

```text
First Failed Stage
→ Primary Root Cause
→ Contributing Factor
→ NOT_CAUSE
→ 최소 수정 대상
```

순서로 판정한다.

---

# 13. 사용자에게 보여줄 최종 답변 템플릿

```text
Q1-Q10:
_ _ _ _ _ _ _ _ _ _

Q11-Q20:
_ _ _ _ _ _ _ _ _ _

Q21-Q30:
_ _ _ _ _ _ _ _ _ _

Q31-Q40:
_ _ _ _ _ _ _ _ _ _

E1:
E2:
E3:
E4:
E5:
E6:
E7:
E8:
E9:
E10:
```

**설명 추가 금지. 숫자 객관식 + 요청된 evidence만 출력.**
