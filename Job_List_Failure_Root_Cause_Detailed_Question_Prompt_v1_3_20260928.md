# Job-list 반복 실패 Root Cause — Detailed Question & Evidence Prompt

- Version: v1.3
- Date: 2026-09-28 KST
- 목적: 기존 v1.2 분석에서 남은 evidence 충돌을 해소하고 **First Failed Stage → Primary Root Cause → Contributing Factor → Non-Cause**를 확정한다.
- 실행 위치: 사내 Windows PC
- 분석 방식: **Evidence First / Read-only / Detailed Multiple Choice**
- 사용자 응답 방식: **숫자 객관식 한 줄**
- 중요: Root Cause 확정 전에는 Job-list / Skill-updater / Dispatcher / AutoTask Builder / Windows Task Scheduler 설정을 수정하지 않는다.

---

# 0. 현재까지 확보된 사용자 응답

아래는 v1.2 Q1~Q50에 대한 사용자 응답이다.

```text
1 1 1 1 1 1 1 2 3 2 2 1 1 0 2 1 1 1 1 1 1 2 1 1 2 1 2 1 1 2 1 1 0 1 2 2 2 1 2 2 0 2 1 1 0 2 0 1 1 0
```

해석 시 반드시 v1.2 Q1~Q50 정의 순서를 그대로 사용한다.

현재 중요한 관찰:

```text
- 동일 실패 PC: YES
- 이전 state/log 존재: YES
- 최근 실패 Job package 존재: YES
- 분석 대상: 가장 최근 실패 실행
- 서로 다른 version evidence 혼재 가능성: YES

- Skill-updater 실행 흔적: YES
- Updater가 Job 탐지: YES
- Version/schema validation: FAIL
- Activation: duplicate/skip
- Activation accepted 이후 evidence: NO

- core/processed: failed
- 동일 Job ID/version key 재사용 가능성: YES
- version만 변경하고 identity/payload 유사: YES
- expired 반복 여부: UNKNOWN
- duplicate/skip: 1회
- failed/expired 후 재실행 state 차단 정황: YES

- Runner 호출 evidence: YES
- First Job Step 진입: YES
- Runner 이전 validation 종료 정황: YES
- duplicate/skip과 runner evidence: 같은 실행
- validation 종료와 runner evidence: 같은 실행
- 가장 최근 실패 실행 Runner: runner 진입 후 first step 전 실패

- AutoTask Builder invoke: YES
- Task Scheduler 등록 요청까지 진행: YES
- AutoTask Builder 결과: FAIL

- Dispatcher task 존재: YES
- Trigger 15/45분: 불일치
- Task Enabled: YES
- Last Run Time 갱신: YES
- Last Run Result: FAIL
- AutoTask Builder가 만든 task와 현재 확인 task: 동일
- 동일 PC의 다른 scheduled task: 정상

- Dispatcher 수동 실행: 미확인
- Scheduler 실행 후 Dispatcher entry evidence: YES
- Dispatcher process 오류 종료: NO

- heartbeat signal 값: 동일
- heartbeat timestamp: 동일
- dispatcher-windows-skill-updater-ok.signal writer: Dispatcher
- 해당 signal은 Dispatcher 등록 전에 생성 불가
- 해당 signal은 precondition으로 사용 불가

- 권한 popup: 미확인
- Task SYSTEM 계정 등록: NO
- 사용자 HOME/LOCALAPPDATA 필요 구조: YES
- working directory dependency: YES

- LLM fallback 존재 여부: 미확인
- 실패 실행에서 fallback 호출 로그: NO
- fallback 이후 transition: 미확인

- 여러 Job-list version에서 반복 실패: YES
- 실패 지점: 대체로 동일
- Root Cause 확정 후 허용 범위: 진단만
```

---

# 1. 현재 Evidence Conflict

아래 충돌을 반드시 해소해야 한다.

## Conflict A — Validation FAIL vs Runner Entry

현재 응답:

```text
Version/schema validation = FAIL
Runner 호출 evidence = YES
First Job Step 진입 = YES
Runner 이전 validation 종료 정황 = YES
validation 종료와 runner evidence = 같은 실행
```

이는 단순 1-path pipeline으로는 모순이다.

가능한 설명:

```text
A1. validation FAIL이 warning/non-fatal이었다.
A2. validation FAIL 후 retry/re-evaluation에서 PASS했다.
A3. 여러 attempt가 하나의 실행으로 묶여 있다.
A4. runner evidence가 다른 sub-job/previous attempt이다.
A5. first-step evidence 해석이 잘못됐다.
A6. validation FAIL은 Job-level이 아닌 optional sub-check였다.
```

추측하지 말고 실제 timestamp / attempt / run-id / log sequence를 확인한다.

---

## Conflict B — First Step 진입 여부

현재 응답:

```text
First Job Step 진입 = YES
가장 최근 실패 실행 = runner 진입 후 first step 전 실패
```

반드시 동일 run/attempt인지 확인한다.

---

## Conflict C — Activation duplicate/skip vs Runner Entry

현재 응답:

```text
Activation = duplicate/skip
duplicate/skip과 runner evidence = 같은 실행
Runner 호출 evidence = YES
```

가능한 설명:

```text
C1. duplicate/skip은 일부 item만 skip하고 실행은 계속됨.
C2. duplicate check와 runner 대상 identity가 다름.
C3. retry attempt가 하나의 실행 기록으로 합쳐짐.
C4. duplicate 상태가 terminal이 아니었다.
C5. evidence timestamp가 다른 attempt를 가리킴.
```

---

## Conflict D — AutoTask Builder FAIL vs Task Exists

현재 응답:

```text
AutoTask Builder invoke = YES
Task Scheduler 등록 요청 = YES
AutoTask Builder result = FAIL
Task exists = YES
현재 task = Builder가 만든 동일 task
```

가능한 설명:

```text
D1. Task 생성 성공 후 validation 실패
D2. Trigger 설정만 실패
D3. Task update 일부 실패
D4. Post-check 실패
D5. Task는 생성됐지만 command/argument/working-directory validation 실패
```

---

# 2. 절대 원칙

1. 현재는 진단 단계다.
2. 어떤 component도 수정하지 않는다.
3. Task 재등록/삭제/수정 금지.
4. Job 재실행 금지. 단, 사용자가 별도로 허용한 read-only dry-run이 있으면 그 범위만 허용.
5. 로그/state/history/Task Scheduler 상태 확인은 read-only로 수행한다.
6. 자동 확인 가능한 질문은 사용자에게 묻지 않는다.
7. 자동 확인이 불가능하거나 evidence 해석이 필요한 항목만 객관식으로 질문한다.
8. 질문 수를 억지로 줄이지 않는다.
9. 단, 질문은 Root Cause 판별에 직접 필요한 항목만 포함한다.
10. 사용자에게 자유서술을 요구하지 않는다.
11. 사용자는 숫자 한 줄만 답할 수 있어야 한다.
12. 모든 질문에는 `0=모름/미확인`을 둔다.
13. 서로 다른 run/attempt/sub-job evidence를 합치지 않는다.
14. 가장 최근 실패 실행의 **최종 attempt**를 First Failed Stage 기준으로 한다.
15. 과거 실패는 반복 패턴 확인용 보조 evidence로 사용한다.

---

# 3. Read-only 자동 조사 우선순위

아래를 먼저 자동 확인한다.

## 3.1 Run / Attempt correlation

가능하면 각 evidence에 아래 필드를 붙인다.

```text
Job ID
Job Version
Job Identity Key
Run ID
Attempt ID
Activation Timestamp
Validation Timestamp
Runner Timestamp
First Step Timestamp
AutoTask Builder Timestamp
Task Creation/Update Timestamp
Scheduler Last Run Timestamp
Dispatcher Entry Timestamp
Signal Timestamp
```

동일 실행 여부는 timestamp만으로 단정하지 말고 ID/key가 있으면 함께 사용한다.

---

## 3.2 Version / Schema

확인:

```text
- 실제 Job-list manifest version
- package folder/version label
- supported schema range
- required updater version
- validation failure code
- fatal/non-fatal 여부
- retry 여부
- validation 이후 state transition
```

---

## 3.3 Activation / Duplicate / Processed

확인:

```text
- activation/history.jsonl 실제 entry
- accepted / duplicate / skip / expired / rejected
- duplicate key
- processed key
- terminal state 여부
- retry allowed 여부
- same version vs new version identity 처리
- failed인데 processed 처리됐는지
```

---

## 3.4 Runner

확인:

```text
- runner entry
- attempt number
- first step entry
- first step name
- last completed step
- failure before/after first step
- retry/re-entry
```

---

## 3.5 AutoTask Builder

확인:

```text
- invoke
- generated Task name
- create/update command
- command return code
- post-validation result
- trigger validation
- action/program validation
- working-directory validation
```

---

## 3.6 Windows Task Scheduler

read-only로 확인:

```text
Task Name
Exists
Enabled
Trigger
15/45 minute schedule 여부
Run As
Logon Type
Program
Arguments
Working Directory
Last Run Time
Last Run Result
Next Run Time
History
Event ID
```

---

## 3.7 Dispatcher

확인:

```text
entry evidence
process start
exit code
config load
working directory
HOME/LOCALAPPDATA
skill-updater invocation
exception/error
```

---

## 3.8 Signal

반드시 writer 기준으로 확인한다.

```text
Signal
Writer
Write Condition
Increment / Overwrite
Expected Frequency
Last Modified
Current Value
Consumer
Precondition
```

현재 seed:

```text
dispatcher-windows-skill-updater-ok.signal
Writer = Dispatcher
Dispatcher 등록 전 생성 불가
Precondition 사용 불가
```

이 seed도 실제 코드/evidence로 재검증한다.

---

# 4. 상세 객관식 질문 생성 규칙

자동 조사 후에도 남는 충돌에 대해서만 질문한다.

질문 개수:

```text
1차: 최대 20개
2차: 최대 10개
```

20개를 다 채울 필요는 없다.

정확한 Root Cause 판별에 필요한 경우에는 15~20개까지 사용해도 된다.

---

# 5. 우선 질문 Pool — Conflict Resolution

아래 질문 중 자동 확인할 수 없는 항목만 사용자에게 제시한다.

## A. Validation

### Q1. Version/schema FAIL은 실행을 중단시키는 fatal validation이었는가?
`0=모름, 1=fatal 즉시 종료, 2=warning/non-fatal, 3=첫 attempt FAIL 후 retry PASS`

### Q2. Validation FAIL 이후 동일 attempt에서 Runner가 호출됐는가?
`0=모름, 1=같은 attempt에서 호출, 2=다른 retry/attempt에서 호출`

### Q3. Validation FAIL 로그와 Runner entry 로그의 시간 순서는?
`0=모름, 1=Validation FAIL → Runner, 2=Runner → Validation FAIL, 3=서로 다른 attempt`

### Q4. Validation FAIL 대상은 무엇이었는가?
`0=모름, 1=Job package 전체, 2=manifest/schema, 3=특정 step/sub-job, 4=optional check`

### Q5. Validation FAIL 후 state는?
`0=모름, 1=terminal failed, 2=retry/deferred, 3=continued, 4=accepted`

---

## B. Activation / Duplicate

### Q6. duplicate/skip은 전체 Job을 종료시키는 terminal gate였는가?
`0=모름, 1=전체 Job 종료, 2=일부 item만 skip, 3=retry attempt만 skip`

### Q7. duplicate/skip의 identity key와 Runner가 실행한 identity key는 같은가?
`0=모름, 1=같음, 2=다름`

### Q8. duplicate/skip 이후 state transition은?
`0=모름, 1=Runner NOT_REACHED, 2=Runner entered, 3=retry/deferred`

### Q9. processed=failed 상태가 다음 실행을 막았는가?
`0=모름, 1=막음, 2=막지 않음, 3=새 version에서는 해제`

### Q10. version만 변경했을 때 신규 Job identity로 인정됐는가?
`0=모름, 1=신규로 인정, 2=기존 identity 재사용, 3=조건부`

---

## C. Runner / First Step

### Q11. 가장 최근 실패의 최종 attempt에서 Runner는?
`0=모름, 1=미진입, 2=진입`

### Q12. 최종 attempt에서 First Job Step은?
`0=모름, 1=미진입, 2=진입`

### Q13. "First Step 진입 YES" evidence는 최종 attempt의 것인가?
`0=모름, 1=맞음, 2=이전 attempt`

### Q14. Runner 진입 후 First Step 전 실패 evidence는 최종 attempt의 것인가?
`0=모름, 1=맞음, 2=이전 attempt`

### Q15. 동일 Job 실행 안에서 retry가 있었는가?
`0=모름, 1=있음, 2=없음`

### Q16. retry가 있었다면 attempt별 결과는?
`0=모름, 1=초기 validation FAIL → 후속 runner 진입, 2=초기 runner 진입 → 후속 validation FAIL, 3=기타`

---

## D. AutoTask Builder

### Q17. AutoTask Builder FAIL은 어느 단계인가?
`0=모름, 1=Task create/update command 실패, 2=Task 생성 후 validation 실패, 3=Trigger 설정 실패, 4=Action/Program 설정 실패, 5=Working Directory 설정 실패, 6=Post-check 실패`

### Q18. Task가 생성된 시점은 Builder FAIL 이전인가 이후인가?
`0=모름, 1=FAIL 이전 이미 생성, 2=Builder 실행 중 생성 후 FAIL, 3=기존 task였음`

### Q19. Task 생성/수정 command return code는?
`0=모름, 1=성공, 2=실패`

### Q20. Builder가 실패로 판정한 직접 조건은?
`0=모름, 1=Trigger mismatch, 2=Last Run 실패, 3=Task 존재 검증 실패, 4=Program/Args mismatch, 5=Working Directory mismatch, 6=기타 validation`

---

## E. Scheduler

### Q21. 15/45 Trigger 불일치는 실제 Task XML/config에서도 확인되는가?
`0=모름, 1=확인됨, 2=실제 config는 정상`

### Q22. Last Run 실패 시 Dispatcher executable/script 자체는 시작됐는가?
`0=모름, 1=시작됨, 2=Scheduler가 시작하지 못함`

### Q23. Last Run Result 실패 원인은 어느 계층인가?
`0=모름, 1=Task launch, 2=Program/path, 3=Arguments, 4=Working Directory, 5=Dispatcher 내부 종료, 6=권한/user-context`

### Q24. Task History에 실행 시작 Event가 있는가?
`0=모름, 1=있음, 2=없음`

### Q25. Task History에 Action start Event가 있는가?
`0=모름, 1=있음, 2=없음`

### Q26. Task History에 Action completed/failure Event가 있는가?
`0=모름, 1=성공, 2=실패, 3=없음`

---

## F. Dispatcher

### Q27. Scheduler 실행 시 Dispatcher entry 로그가 생성됐는가?
`0=모름, 1=생성, 2=미생성`

### Q28. Dispatcher entry 후 정상 종료했는가?
`0=모름, 1=정상 종료, 2=오류 종료, 3=중간 중단/timeout`

### Q29. Dispatcher가 Skill-updater 호출까지 도달했는가?
`0=모름, 1=도달, 2=미도달`

### Q30. Dispatcher 실행 계정의 HOME/LOCALAPPDATA는 예상 사용자와 동일했는가?
`0=모름, 1=동일, 2=다름`

### Q31. Dispatcher working directory는 예상 경로였는가?
`0=모름, 1=정상, 2=다름`

---

## G. Signal

### Q32. heartbeat signal writer code path에 Dispatcher가 실제 도달했는가?
`0=모름, 1=도달, 2=미도달`

### Q33. heartbeat signal은 increment 방식인가 overwrite 방식인가?
`0=모름, 1=increment, 2=overwrite`

### Q34. signal 값이 같아도 timestamp만 갱신될 수 있는 구조인가?
`0=모름, 1=가능, 2=불가능`

### Q35. signal writer 실행 조건이 별도 성공 조건에 묶여 있는가?
`0=모름, 1=맞음, 2=항상 실행`

---

## H. Permission / Unattended

### Q36. Scheduler 실행 시 interactive prompt 또는 confirmation 대기 흔적이 있는가?
`0=모름, 1=있음, 2=없음`

### Q37. HOME/LOCALAPPDATA 설정 누락 로그가 있는가?
`0=모름, 1=있음, 2=없음`

### Q38. Working Directory mismatch 로그가 있는가?
`0=모름, 1=있음, 2=없음`

### Q39. 네트워크/사내 리소스 접근 실패가 있는가?
`0=모름, 1=있음, 2=없음`

---

## I. LLM Fallback

### Q40. 실패 실행에서 fallback 조건 자체가 충족됐는가?
`0=모름, 1=충족, 2=미충족, 3=fallback 기능 없음`

### Q41. fallback 호출 자체가 없었던 이유는?
`0=모름, 1=trigger 미충족, 2=validation/state gate 이전 종료, 3=tool/model unavailable, 4=fallback 비활성`

---

# 6. First Failed Stage 결정 규칙

가장 최근 실패 실행의 **최종 attempt**만 기준으로 아래 순서대로 평가한다.

```text
1. Job package detected
2. Updater detected
3. Version/schema accepted
4. Activation accepted
5. Duplicate gate passed
6. Expiry gate passed
7. Processed gate passed
8. Runner entered
9. First Job Step entered
10. AutoTask Builder invoked
11. Task registration/configuration valid
12. Scheduler executed
13. Dispatcher entered
14. Dispatcher internal step
15. Signal writer executed
16. Signal changed
```

규칙:

```text
- 첫 명시적 FAIL = First Failed Stage 후보
- 그 이후 NOT_REACHED가 이어지면 확정
- 이후 단계도 실행됐다면:
    1) retry/attempt 혼재 여부를 먼저 조사
    2) non-fatal gate 여부를 조사
    3) 동일 pipeline이 아닌 sub-path인지 조사
- 서로 다른 attempt면 attempt별 pipeline을 분리
```

---

# 7. Root Cause 판정 기준

## RC-A Job-list package/version

PRIMARY 조건 예:

```text
- 최종 attempt에서 fatal schema/version reject
- 이후 Runner NOT_REACHED
```

## RC-B Skill-updater detection/activation

PRIMARY 조건 예:

```text
- package는 있으나 updater 미탐지
- activation request 미생성/거부
```

## RC-C duplicate/expired/processed state machine

PRIMARY 조건 예:

```text
- duplicate/expired/processed terminal gate
- 이후 Runner NOT_REACHED
```

## RC-D Runner

PRIMARY 조건 예:

```text
- activation/state gates 모두 PASS
- Runner entry 실패 또는 first step 전 termination
```

## RC-E AutoTask Builder

PRIMARY 조건 예:

```text
- Runner/step PASS
- Builder 호출 또는 Builder 내부에서 최초 terminal failure
```

## RC-F Scheduler

PRIMARY 조건 예:

```text
- Builder가 정상적으로 task 등록 완료
- Task config/trigger/action/launch에서 최초 failure
```

## RC-G Dispatcher

PRIMARY 조건 예:

```text
- Scheduler가 process를 정상 launch
- Dispatcher 내부에서 최초 failure
```

## RC-H Signal

PRIMARY 조건은 매우 제한적으로 사용한다.

```text
Scheduler PASS
Dispatcher PASS
Signal writer path 도달
Signal write 자체 실패
```

단순 signal 값 정지는 Primary 근거가 아니다.

---

# 8. 최종 출력 형식

## A. Executive Summary

```text
Analysis Target:
Final Attempt:
First Failed Stage:
Primary Root Cause:
Confidence:
```

---

## B. Attempt Separation

| Attempt | Version | Key | Validation | Activation | Runner | Builder | Scheduler | Dispatcher |
|---|---|---|---|---|---|---|---|---|

---

## C. Pipeline Evidence Matrix

| Stage | Status | Evidence | Attempt |
|---|---|---|---|

Status:

```text
PASS / FAIL / NOT_REACHED / UNKNOWN / N/A
```

---

## D. Root Cause Classification

| Rank | Category | Verdict | Evidence |
|---|---|---|---|
| 1 | | PRIMARY_ROOT_CAUSE | |
| 2 | | CONTRIBUTING_FACTOR | |
| 3 | | CONTRIBUTING_FACTOR / INSUFFICIENT_EVIDENCE | |

---

## E. Confirmed Non-Causes

실제 evidence로 배제된 것만 기록한다.

```text
NOT_CAUSE:
- ...
```

---

## F. Evidence Conflict Resolution

```text
Conflict:
Evidence A:
Evidence B:
Same Attempt:
Resolution:
```

---

## G. Scheduler / Dispatcher Boundary

```text
Task Created:
Task Valid:
Task Trigger:
Task Last Run:
Action Started:
Dispatcher Entered:
Dispatcher Exit:
```

---

## H. Signal Interpretation

```text
Signal:
Writer:
Write Condition:
Increment / Overwrite:
Writer Reached:
Expected Change:
Actual Change:
Can Be Used As Precondition:
Verdict:
```

---

## I. Final Verdict

반드시 아래 네 가지로 구분한다.

```text
PRIMARY_ROOT_CAUSE:
CONTRIBUTING_FACTOR:
NOT_CAUSE:
INSUFFICIENT_EVIDENCE:
```

---

# 9. 사용자 질문 출력 형식

자동 evidence 조사 후 사용자 질문이 필요하면 다음 형식을 사용한다.

```text
자동 확인 가능한 항목은 먼저 확인했습니다.

현재 First Failed Stage와 Root Cause를 확정하기 위해
아래 N개만 추가 확인하면 됩니다.

모르면 0입니다.
설명은 필요 없고 숫자 한 줄만 답해주세요.

Q1. ...
0=모름, 1=..., 2=...

Q2. ...
0=모름, 1=..., 2=...

...

답변 예:
1 2 0 3 1 1 2
```

---

# 10. 금지 사항

Root Cause 확정 전 다음을 하지 않는다.

```text
- Job-list 수정
- Skill-updater 수정
- Dispatcher 수정
- AutoTask Builder 수정
- Task Scheduler task 삭제/재등록/변경
- signal 초기화
- state/history 삭제
- processed state 강제 삭제
- version bump로 우회
- duplicate key 변경
- retry 강제 실행
```

진단을 위해 상태를 훼손하지 않는다.

---

# 11. 종료 조건

다음을 만족하면 진단 완료다.

```text
1. 가장 최근 실패 실행의 최종 attempt 식별
2. Validation/Activation/Runner evidence 충돌 해소
3. duplicate/processed state 영향 확정
4. First Failed Stage 확정
5. AutoTask Builder FAIL 의미 확정
6. Scheduler와 Dispatcher 경계 확정
7. signal writer 의미 확정
8. Primary Root Cause 최소 1개 확정 또는 INSUFFICIENT_EVIDENCE
9. Contributing Factor 분리
10. Non-Cause 분리
11. 수정 없이 진단 결과만 보고
```

---

# 12. 핵심 한 줄

```text
Read-only Evidence → Run/Attempt 분리 → Conflict 해소 → First Failed Stage → Primary Root Cause → Contributing Factor → Non-Cause
```
