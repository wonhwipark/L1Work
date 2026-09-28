# Job-list 반복 실패 Root Cause Analysis Prompt — Evidence First / Detailed Multiple Choice

- Version: v1.2
- Date: 2026-09-28 KST
- 실행 위치: 사내 Windows PC
- 목적: 반복적으로 동작하지 못한 Job-list의 **First Failed Stage**와 **Primary Root Cause**를 실제 로그/상태/버전/Task Scheduler/Signal 근거로 확정한다.
- 사용자 응답 방식: **숫자 객관식 한 줄**
- 사용자 입력 최소화 원칙은 유지하되, **객관식이라면 Root Cause 분리에 필요한 질문을 더 세분화해도 된다.**
- Root Cause 확정 전에는 Job-list / Skill-updater / Dispatcher / AutoTask Builder를 수정하지 않는다.

---

# 0. 최우선 목표

이번 단계의 목적은 **수정이 아니라 진단**이다.

아래 실행 체인에서 실제로 가장 먼저 실패한 Gate를 찾는다.

```text
Job-list package
 → Skill-updater detection
 → version/schema validation
 → activation
 → duplicate / expired / processed gate
 → Job runner
 → first job step
 → AutoTask Builder
 → Windows Task Scheduler registration
 → Windows Task Scheduler execution
 → Dispatcher runtime
 → Signal writer
 → Signal update
```

반드시 다음 순서로 판단한다.

```text
1. First Failed Stage 확정
2. Primary Root Cause 확정
3. Contributing Factor 분리
4. Non-Cause 분리
5. Evidence 부족 항목 표시
6. Root Cause 확정 이후에만 복구/수정 논의
```

최종 판정은 아래 네 가지 중 하나만 사용한다.

```text
PRIMARY_ROOT_CAUSE
CONTRIBUTING_FACTOR
NOT_CAUSE
INSUFFICIENT_EVIDENCE
```

---

# 1. 절대 원칙

1. 추측으로 Root Cause를 확정하지 않는다.
2. 가능한 경우 실제 Production file/log/state/Task Scheduler evidence를 확인한다.
3. 자동 확인 가능한 항목은 사용자에게 묻지 않는다.
4. Root Cause 확정 전에는 다음을 수정하지 않는다.
   - Job-list
   - Skill-updater
   - Dispatcher
   - AutoTask Builder
   - Task Scheduler task
5. `signal 값 변화 없음 = Dispatcher 미동작`으로 단정하지 않는다.
6. Signal은 반드시 아래를 먼저 확인한다.
   - Writer
   - Write Condition
   - Increment / Overwrite 방식
   - Expected Frequency
   - Consumer
   - Precondition
7. Dispatcher 등록 전에 Dispatcher가 생성하는 signal을 precondition으로 사용하지 않는다.
8. 뒤 단계 증상보다 **앞 단계 FAIL**을 우선한다.
9. `Task Scheduler 실패`, `Dispatcher signal 정지`, `heartbeat 정지`가 보여도 그보다 앞서 Updater/Activation/State Gate가 실패했다면 앞 단계가 Primary Root Cause 후보이다.
10. 권한 상승, destructive cleanup, registry 수정, Task 삭제/재등록은 진단 중 금지한다.
11. 접근 거부 경로는 SKIP한다.
12. Evidence가 부족하면 억지로 결론 내리지 않고 `INSUFFICIENT_EVIDENCE`로 둔다.

---

# 2. 사용자 Interaction 규칙

## 2.1 기본 원칙

- 먼저 AI가 read-only evidence를 최대한 자동 확인한다.
- 자동 확인이 불가능한 항목 중 Root Cause 판별에 필요한 것만 묻는다.
- 질문은 모두 객관식 숫자 선택식이다.
- 사용자는 **숫자 한 줄**로만 답한다.
- 모든 질문에는 `0=모름/미확인` 선택지를 둔다.
- 사용자에게 로그 문장, 경로, 버전 문자열, 명령 결과를 직접 타이핑하게 하지 않는다.
- 같은 의미의 질문을 표현만 바꾸어 반복하지 않는다.

## 2.2 질문 수 정책 — v1.2 변경

기존처럼 무조건 질문 수를 최소화하는 것보다 **First Failed Stage를 정확히 분리하는 것**을 우선한다.

객관식 질문이라면 세부 질문을 허용한다.

권장 범위:

```text
1차 질문: 최대 15개
추가 질문: 한 번에 최대 8개
전체 질문: 원칙적으로 20개 이내
```

단, 다음 조건이면 20개를 초과하지 말고 `INSUFFICIENT_EVIDENCE`로 남긴다.

```text
- 사용자 기억에 의존해야 하는 항목
- 동일 내용을 반복 확인해야 하는 경우
- 실제 로그/상태 파일이 없어서 객관적으로 판별 불가능한 경우
```

## 2.3 질문을 더 세분화해야 하는 경우

다음 상황에서는 객관식 질문을 세분화한다.

```text
- 서로 다른 실행 회차의 evidence가 섞여 있을 가능성
- activation은 PASS인데 runner도 PASS/FAIL evidence가 동시에 존재
- duplicate/expired/processed 상태와 runner 진입 evidence가 충돌
- AutoTask Builder invoke와 Task Scheduler task 존재 여부가 충돌
- Task 존재와 Trigger/Last Run/Last Result가 서로 모순
- Dispatcher 실행 여부와 signal 값 변화가 일치하지 않음
- version만 변경했지만 동일 Job identity로 처리될 가능성
```

이 경우 반드시 `같은 실행인지 / 다른 실행인지 / 가장 최근 실패인지`를 분리해서 묻는다.

---

# 3. 조사 범위

가능한 범위에서 아래를 **read-only**로 자동 탐색한다.

```text
- 현재/최근 실패 Job-list package
- Skill-updater
- Windows Dispatcher bundle
- AutoTask Builder
- activation/history.jsonl
- core/processed.jsonl
- run/result/history/log 관련 json/jsonl/txt/log
- *.signal
- manifest/version metadata
- wrapper / bat / ps1 / python entry point
- lock / pid / deferred / running marker
- Windows Task Scheduler task / trigger / history
```

탐색 순서:

```text
현재 working directory
→ 현재 skill/job workspace
→ known skill root
→ HOME
→ LOCALAPPDATA
→ TEMP
→ project run/state/log directory
```

---

# 4. 실행 회차 분리 규칙

반복 실패 분석에서 가장 중요한 추가 규칙이다.

서로 다른 실행의 evidence를 하나의 Pipeline으로 합치지 않는다.

각 evidence에는 가능하면 아래 정보를 붙인다.

```text
Run ID:
Job ID:
Job Version:
Activation Timestamp:
Runner Timestamp:
Scheduler Timestamp:
Dispatcher Timestamp:
Signal Timestamp:
```

Run ID가 없으면 다음 조합으로 동일 실행 여부를 추정한다.

```text
Job ID + version + activation time + runner time + task creation time
```

충돌 evidence가 있으면 사용자에게 아래 형식으로 확인한다.

```text
Q. duplicate/skip evidence와 runner 진입 evidence가 같은 실행인가?
0=모름
1=같은 실행
2=서로 다른 실행
```

또는:

```text
Q. 가장 최근 실패한 실행만 보면 runner가 첫 step에 진입했는가?
0=모름
1=진입
2=미진입
```

**가장 최근 실패 실행**을 기준으로 First Failed Stage를 결정한다.

과거 성공 실행이나 다른 version 실행은 보조 evidence로만 사용한다.

---

# 5. Pipeline Evidence Matrix

반드시 작성한다.

| Stage | Evidence | Status | Same Run? | First Failure? |
|---|---|---|---|---|
| Job package detected | | | | |
| Updater detected job | | | | |
| Version/schema accepted | | | | |
| Activation created | | | | |
| Duplicate gate passed | | | | |
| Expiry gate passed | | | | |
| Processed gate passed | | | | |
| Runner entered | | | | |
| First job step entered | | | | |
| AutoTask Builder invoked | | | | |
| Task registered | | | | |
| Scheduler trigger valid | | | | |
| Scheduler executed | | | | |
| Dispatcher entered | | | | |
| Signal writer executed | | | | |
| Signal changed | | | | |

Status:

```text
PASS
FAIL
NOT_REACHED
UNKNOWN
N/A
```

First Failed Stage 선정 규칙:

```text
1. 동일 실행 회차만 본다.
2. 가장 앞선 명시적 FAIL을 찾는다.
3. 그 이후 단계가 연속 NOT_REACHED라면 앞 FAIL을 First Failed Stage로 확정한다.
4. 뒤 단계에도 FAIL이 있으면 Primary가 아니라 Contributing Factor 후보로 둔다.
5. 서로 다른 실행의 FAIL은 별도 케이스로 분리한다.
```

---

# 6. Version / Activation / State 검사

## 6.1 Version

실제 파일에서 확인한다.

```text
Job-list version
manifest version
package/folder label
updater supported schema/version
required updater version
dispatcher version
AutoTask Builder version
```

확인 항목:

```text
- package label과 manifest version이 일치하는가
- updater가 해당 schema/version을 지원하는가
- required updater version이 현재 updater보다 높은가
- version만 바뀌고 identity key는 동일한가
```

## 6.2 Activation

확인:

```text
request 생성
accepted
expired
duplicate
skipped
rejected
last accepted version
activation timestamp
```

## 6.3 Processed / State Machine

확인:

```text
동일 Job ID/version이 이미 processed인지
failed인데 processed로 기록되는지
expired state가 재실행을 막는지
duplicate key가 무엇인지
version 변경만으로 새로운 job으로 인정되는지
payload hash / identity key를 사용하는지
terminal state 이후 retry가 허용되는지
```

---

# 7. Runner 검사

확인:

```text
runner entry evidence
first step entry
step index
last completed step
failure code
deferred/running marker
lock/pid
retry count
stdout/stderr
```

특히 아래를 분리한다.

```text
Updater가 Job을 탐지함
≠
Activation이 accepted됨
≠
Runner가 호출됨
≠
First Job Step이 실행됨
```

`Updater가 실행되었다`는 사실만으로 Runner PASS로 판단하지 않는다.

---

# 8. AutoTask Builder 검사

확인:

```text
invoke evidence
input contract
generated command
target task name
trigger configuration
run-as configuration
working directory
result/status
Task Scheduler 호출 직전 실패 여부
```

AutoTask Builder가 호출되었더라도 Task 생성이 실패하면:

```text
AutoTask Builder invocation = PASS
Task registration = FAIL
```

로 구분한다.

---

# 9. Windows Task Scheduler 검사

반드시 확인:

```text
Task Name
Exists
Enabled
Trigger
15/45 minute schedule 여부
Run As User
Run only when user logged on 여부
Program
Arguments
Working Directory
Last Run Time
Last Run Result
Next Run Time
History
Missed start 처리
```

판정 예:

```text
Task 없음
→ Task registration FAIL

Task 있음 + Trigger 불일치
→ Scheduler configuration FAIL

Task 있음 + Trigger 정상 + Last Run 없음
→ execution gate FAIL 후보

Task 있음 + Last Run 있음 + Result 실패
→ runtime execution FAIL

Task 실행 성공 + Dispatcher evidence 없음
→ Dispatcher entry/runtime 조사
```

동일 PC의 다른 scheduled task가 정상이라면 Scheduler 서비스 전체 장애는 Non-Cause 후보가 될 수 있다.

---

# 10. Permission / Unattended 검사

확인:

```text
SYSTEM 계정 실행 여부
사용자 HOME 차이
LOCALAPPDATA 접근
working directory dependency
interactive prompt
권한 확인 popup
stdin 대기
stdout/stderr 저장
network path 접근
credential 요구
```

사용자 계정에서 정상인데 SYSTEM에서만 실패하면 `RC-I Permission/user-context` 후보로 분리한다.

---

# 11. Dispatcher 검사

확인:

```text
entry point 호출 여부
process start evidence
config load
job discovery
skill-updater invocation
exit code
runtime error
working directory
environment variables
user context
```

Scheduler가 정상 실행되었다고 Dispatcher 자체도 정상이라고 판단하지 않는다.

---

# 12. Signal 검사

각 signal마다 기록:

```text
Signal:
Writer:
Write Condition:
Increment / Overwrite:
Expected Frequency:
Last Modified:
Current Value:
Consumer:
Precondition:
```

특히 확인:

```text
updater가 쓰는가
dispatcher가 쓰는가
task 등록 전에 생성 가능한가
값이 증가하는 방식인가
timestamp만 갱신될 수 있는가
같은 값 overwrite가 가능한가
health gate로 사용 가능한가
```

중요:

```text
signal 값 고정
≠
writer 미실행
≠
dispatcher 미실행
```

Writer와 Write Condition 확인 전에는 signal을 Primary Root Cause evidence로 사용하지 않는다.

---

# 13. LLM Fallback 검사

지원되는 경우에만 확인한다.

```text
fallback trigger
실제 호출 여부
model
timeout
retry
prompt
tool availability
fallback result
state transition
```

LLM fallback은 아래를 자동 우회한다고 가정하지 않는다.

```text
version gate
schema gate
duplicate gate
expired gate
processed gate
activation reject
```

---

# 14. Root Cause Category

다음 분류를 사용한다.

```text
RC-A Job-list package/version
RC-B Skill-updater detection/activation
RC-C duplicate/expired/processed state machine
RC-D Job runner 미진입
RC-E AutoTask Builder invocation
RC-F Windows Task Scheduler registration/configuration
RC-G Dispatcher runtime
RC-H Signal writer/health interpretation
RC-I Permission/user-context
RC-J LLM fallback
```

각각 아래 중 하나로 판정한다.

```text
PRIMARY_ROOT_CAUSE
CONTRIBUTING_FACTOR
NOT_CAUSE
INSUFFICIENT_EVIDENCE
```

Root Cause 우선순위는 최대 3개까지만 작성한다.

---

# 15. 상세 객관식 질문 Pool

아래는 **질문 Pool**이다.

전부 묻지 않는다.

자동 evidence 확인 후 필요한 질문만 선택한다.

## A. 실행 회차 / 대상 식별

### Q1. 같은 실패가 발생했던 동일 사내 PC인가?
`0=모름, 1=동일, 2=다른 PC`

### Q2. 이전 state/log 파일이 남아 있는가?
`0=모름, 1=남아있음, 2=초기화/삭제됨`

### Q3. 최근 실패 Job-list package를 보유하고 있는가?
`0=없음, 1=있음, 2=일부 버전만`

### Q4. 분석 대상은 어느 실행인가?
`0=모름, 1=가장 최근 실패, 2=특정 과거 실패, 3=여러 실패 공통 원인`

### Q5. 서로 다른 version의 evidence가 섞여 있을 가능성이 있는가?
`0=모름, 1=있음, 2=없음`

---

## B. Updater / Activation

### Q6. Skill-updater 실행 흔적은?
`0=모름, 1=있음, 2=없음`

### Q7. Updater가 실패 Job을 탐지했는가?
`0=모름, 1=탐지, 2=미탐지`

### Q8. Version/schema validation 결과는?
`0=모름, 1=PASS, 2=FAIL, 3=validation 진입 전 종료`

### Q9. Activation 상태는?
`0=모름, 1=accepted, 2=expired, 3=duplicate/skip, 4=rejected, 5=entry 없음`

### Q10. Activation accepted 이후 다음 단계 evidence가 있는가?
`0=모름, 1=있음, 2=없음`

---

## C. Duplicate / Expired / Processed

### Q11. core/processed 상태는?
`0=모름, 1=success/processed, 2=failed, 3=expired, 4=entry 없음`

### Q12. 동일 Job ID/version key 재사용 가능성은?
`0=모름, 1=있음, 2=명확히 다름`

### Q13. version만 변경하고 identity/payload는 유사했는가?
`0=모름, 1=맞음, 2=아님`

### Q14. expired가 반복됐는가?
`0=모름, 1=반복, 2=1회, 3=없음`

### Q15. duplicate/skip이 반복됐는가?
`0=모름, 1=반복, 2=1회, 3=없음`

### Q16. failed/expired 이후 재실행이 state 때문에 막힌 정황은?
`0=모름, 1=있음, 2=없음`

---

## D. Runner

### Q17. Runner가 호출된 evidence가 있는가?
`0=모름, 1=있음, 2=없음`

### Q18. First Job Step에 진입했는가?
`0=모름, 1=진입, 2=미진입`

### Q19. Runner 이전 validation 종료 정황이 있는가?
`0=모름, 1=있음, 2=없음`

### Q20. `duplicate/skip`과 `runner 진입` evidence는 같은 실행인가?
`0=모름, 1=같은 실행, 2=서로 다른 실행`

### Q21. `validation 종료`와 `runner 진입` evidence는 같은 실행인가?
`0=모름, 1=같은 실행, 2=서로 다른 실행`

### Q22. 가장 최근 실패 실행만 보면 Runner는?
`0=모름, 1=first step 진입, 2=runner 진입 후 first step 전 실패, 3=runner 미진입`

---

## E. AutoTask Builder

### Q23. AutoTask Builder invoke evidence가 있는가?
`0=모름, 1=있음, 2=없음`

### Q24. AutoTask Builder가 Task Scheduler 등록 요청까지 진행했는가?
`0=모름, 1=진행, 2=등록 요청 전 실패`

### Q25. AutoTask Builder 결과는?
`0=모름, 1=성공, 2=실패, 3=부분 성공`

---

## F. Windows Task Scheduler

### Q26. Dispatcher task가 생성됐는가?
`0=모름, 1=있음, 2=없음, 3=생성 후 삭제`

### Q27. Trigger는 의도한 15/45분과 일치하는가?
`0=모름, 1=일치, 2=불일치, 3=task 없음`

### Q28. Task가 Enabled인가?
`0=모름, 1=Enabled, 2=Disabled, 3=task 없음`

### Q29. Last Run Time은 갱신됐는가?
`0=모름, 1=갱신, 2=미갱신, 3=task 없음`

### Q30. Last Run Result는?
`0=모름, 1=성공, 2=실패, 3=실행 기록 없음, 4=task 없음`

### Q31. AutoTask Builder가 만든 task와 현재 확인한 task가 같은가?
`0=모름, 1=같음, 2=기존/다른 task`

### Q32. 동일 PC의 다른 scheduled task는 정상 실행되는가?
`0=모름, 1=정상, 2=다른 task도 문제`

---

## G. Dispatcher

### Q33. Dispatcher 수동 실행 결과는?
`0=미확인, 1=정상, 2=실패`

### Q34. Scheduler 실행 후 Dispatcher entry evidence는?
`0=모름, 1=있음, 2=없음`

### Q35. Dispatcher process가 시작된 뒤 오류 종료했는가?
`0=모름, 1=맞음, 2=아님`

---

## H. Signal

### Q36. dispatcher-windows-heartbeat-ok.signal 값 변화는?
`0=모름, 1=증가, 2=계속 동일`

### Q37. heartbeat signal timestamp는?
`0=모름, 1=갱신되나 값 동일, 2=timestamp도 동일, 3=값도 갱신`

### Q38. dispatcher-windows-skill-updater-ok.signal writer는?
`0=모름, 1=Dispatcher, 2=Skill-updater, 3=기타`

### Q39. 해당 signal이 Dispatcher 등록 전에 생성 가능한가?
`0=모름, 1=가능, 2=불가능`

### Q40. 해당 signal은 precondition으로 사용 가능한가?
`0=모름, 1=가능, 2=불가능`

---

## I. Permission / Unattended

### Q41. 무인 실행 중 권한 popup/확인 질문이 발생했는가?
`0=모름, 1=있음, 2=없음`

### Q42. Task가 SYSTEM 계정으로 등록됐는가?
`0=모름, 1=맞음, 2=아님`

### Q43. 사용자 HOME/LOCALAPPDATA 설정이 필요한 구조인가?
`0=모름, 1=맞음, 2=아님`

### Q44. working directory가 달라지면 실패할 가능성이 있는 구조인가?
`0=모름, 1=맞음, 2=아님`

---

## J. LLM Fallback

### Q45. LLM fallback 기능이 존재하는가?
`0=모름, 1=있음, 2=없음`

### Q46. 실패 실행에서 fallback 호출 로그가 있는가?
`0=모름, 1=있음, 2=없음, 3=fallback 기능 없음`

### Q47. fallback 이후 state transition이 진행됐는가?
`0=모름, 1=진행, 2=중단`

---

## K. 반복 실패 특성

### Q48. 실패가 여러 Job-list version에서 반복됐는가?
`0=모름, 1=여러 버전, 2=특정 버전만`

### Q49. 실패 지점이 매번 동일했는가?
`0=모름, 1=대체로 동일, 2=실행마다 다름`

### Q50. Root Cause 확정 후 허용 범위는?
`0=진단만, 1=최소 복구까지, 2=직접 관련 component 수정까지`

---

# 16. 질문 선택 우선순위

질문은 아래 순서로 선택한다.

```text
1. 가장 최근 실패 실행 식별
2. 서로 다른 실행 evidence 분리
3. First Failed Stage 판별
4. Primary Root Cause 분리
5. Contributing Factor 분리
6. Non-Cause 확인
7. Signal 의미 확인
8. Permission / LLM fallback 보조 확인
```

예를 들어 아래처럼 evidence가 충돌하면:

```text
activation = duplicate/skip
runner = entered
validation = stopped before runner
```

Q20/Q21/Q22를 우선 질문한다.

아래처럼 Scheduler evidence가 충돌하면:

```text
AutoTask Builder invoked
Task exists
Trigger mismatch
Last Run failed
```

Q24/Q25/Q27/Q30/Q31을 우선한다.

---

# 17. 현재 반복 실패 분석 시 우선 확인할 후보

과거 Seed Evidence는 Root Cause가 아니라 **우선 조사 대상**으로만 취급한다.

```text
- dispatcher-windows-heartbeat-ok.signal 값이 1에 머문 사례
- dispatcher-linux-heartbeat-ok.signal은 증가한 사례
- Windows Dispatcher 15/45분 등록 실패 가능성
- activation/history.jsonl의 expired / duplicated_skipped 사례
- core/processed.jsonl의 expired 사례
- v0.3.97 / v0.3.98 반복 실패
- Skill-updater가 runner까지 넘기지 못했을 가능성
- dispatcher-windows-skill-updater-ok.signal을 등록 전 precondition으로 쓸 수 있는지 의문
```

이 항목은 반드시 현재 Production evidence로 재검증한다.

---

# 18. Root Cause 판정 규칙

예시 1:

```text
Job detected = PASS
Updater detected = PASS
Activation = duplicate/skip FAIL
Runner = NOT_REACHED
AutoTask Builder = NOT_REACHED
Scheduler = NOT_REACHED
Dispatcher = NOT_REACHED

→ First Failed Stage = Duplicate Gate
→ RC-C = PRIMARY_ROOT_CAUSE
```

예시 2:

```text
Activation = PASS
Runner = PASS
AutoTask Builder = PASS
Task created = PASS
Trigger = FAIL
Last Run = FAIL

→ First Failed Stage = Scheduler Configuration
→ RC-F = PRIMARY_ROOT_CAUSE
```

예시 3:

```text
Task = PASS
Last Run = PASS
Dispatcher entry = PASS
Signal writer = UNKNOWN
Signal value unchanged

→ Dispatcher 등록 문제로 단정 금지
→ RC-H 조사 계속
```

예시 4:

```text
Run A: duplicate/skip → runner 미진입
Run B: runner 진입 → AutoTask Builder 실행 → Scheduler 실패
```

이 경우:

```text
두 실행을 하나로 합치지 않는다.

Run A Primary = RC-C
Run B Primary = RC-F 또는 RC-G

반복 실패의 공통 원인을 별도로 평가한다.
```

---

# 19. 최종 보고 형식

## A. Executive Summary

```text
Analysis Target:
Primary Root Cause:
First Failed Stage:
Confidence: HIGH / MEDIUM / LOW
```

## B. Pipeline Result

| Stage | Status | Evidence | Same Run |
|---|---|---|---|
| Job detected | | | |
| Updater detected | | | |
| Version/schema | | | |
| Activation | | | |
| Duplicate/Expiry/Processed | | | |
| Runner | | | |
| First Step | | | |
| AutoTask Builder | | | |
| Task Registration | | | |
| Scheduler Execution | | | |
| Dispatcher | | | |
| Signal Writer | | | |
| Signal | | | |

## C. Root Cause Ranking

| Rank | Category | Verdict | Evidence |
|---|---|---|---|
| 1 | | PRIMARY_ROOT_CAUSE | |
| 2 | | CONTRIBUTING_FACTOR | |
| 3 | | CONTRIBUTING_FACTOR / INSUFFICIENT_EVIDENCE | |

## D. Confirmed Non-Causes

실제 evidence로 배제된 항목만 작성한다.

```text
NOT_CAUSE:
- ...
```

## E. Evidence Conflict

서로 다른 실행 evidence가 섞여 있었으면 반드시 작성한다.

```text
Evidence A:
Evidence B:
Same Run: YES / NO / UNKNOWN
Resolution:
```

## F. Signal Interpretation

```text
Signal:
Writer:
Write Condition:
Expected Change:
Actual Change:
Can Be Used As Precondition: YES / NO / UNKNOWN
Verdict:
```

## G. Version / State

```text
Job-list:
Skill-updater:
Dispatcher:
AutoTask Builder:

Activation:
Processed:
Duplicate:
Expired:
Retry Allowed:
Identity Key:
```

## H. Scheduler

```text
Task Exists:
Enabled:
Trigger:
Run As:
Program:
Arguments:
Working Directory:
Last Run:
Last Result:
Next Run:
```

## I. Permission / Unattended

```text
Run As:
HOME/LOCALAPPDATA:
Interactive Prompt:
Permission Block:
Working Directory Dependency:
Verdict:
```

## J. LLM Fallback

```text
Supported:
Triggered:
Result:
State Transition:
Verdict:
```

## K. Next Action

Q50 기준:

```text
0 → 진단 결과만 보고하고 STOP
1 → Primary Root Cause의 최소 복구만 수행
2 → Root Cause와 직접 관련된 component만 수정
```

Root Cause와 무관한 refactoring은 금지한다.

---

# 20. 성공 조건

아래를 만족해야 Root Cause 분석 완료로 본다.

1. 분석 대상 실행 회차가 명확하다.
2. 서로 다른 실행 evidence가 섞여 있으면 분리했다.
3. First Failed Stage를 확정했거나 evidence 부족을 명시했다.
4. Primary Root Cause를 최소 1개 확정했거나 `INSUFFICIENT_EVIDENCE`로 표시했다.
5. Updater/Activation/State 문제와 Dispatcher 문제를 분리했다.
6. duplicate/expired/processed 영향을 확인했다.
7. Runner 진입 여부를 확인했다.
8. AutoTask Builder invoke와 Task 등록을 분리했다.
9. Task Scheduler 등록/Trigger/실행 결과를 확인했다.
10. Dispatcher 실행 여부를 Scheduler와 분리했다.
11. Signal writer와 signal 의미를 확인했다.
12. Permission/user-context를 확인했다.
13. LLM fallback 실제 동작 여부를 확인했다.
14. Primary Root Cause / Contributing Factor / Non-Cause를 구분했다.
15. 미확인 가설은 가설로 유지했다.
16. Root Cause 확정 전 component 수정이 없었다.

---

# 21. 최종 실행 지시

1. 먼저 사내 Windows PC에서 가능한 evidence를 **read-only**로 자동 수집한다.
2. 자동 확인 가능한 항목은 사용자에게 묻지 않는다.
3. 가장 최근 실패 실행을 우선 식별한다.
4. 서로 다른 실행 evidence가 섞였는지 확인한다.
5. 질문은 모두 숫자 객관식으로 한다.
6. 객관식이면 Root Cause 분리를 위해 세부 질문을 충분히 허용한다.
7. 최초 질문은 원칙적으로 최대 15개로 한다.
8. 추가 질문은 한 번에 최대 8개로 한다.
9. 사용자는 숫자 한 줄로 답한다.
10. `0=모름/미확인`을 항상 제공한다.
11. First Failed Stage를 가장 먼저 확정한다.
12. Primary Root Cause / Contributing Factor / Non-Cause / Insufficient Evidence를 구분한다.
13. Signal 정지만으로 Dispatcher 실패를 단정하지 않는다.
14. Root Cause 확정 전에는 Job-list / Skill-updater / Dispatcher / AutoTask Builder를 수정하지 않는다.
15. Root Cause와 관련 없는 refactoring은 하지 않는다.

사용자에게 다음을 요구하지 않는다.

```text
긴 설명
로그 복사
경로 직접 입력
버전 문자열 입력
명령어 결과 입력
실패 상황 자유서술
```

필요한 정보는 가능한 한 AI가 직접 찾는다.

---

# 22. 사용자 질문 출력 템플릿

질문을 시작할 때 반드시 다음 형식을 사용한다.

```text
자동으로 확인 가능한 항목은 먼저 확인했습니다.
현재 Root Cause를 분리하기 위해 아래 N개만 추가 확인하면 됩니다.
모르면 0입니다.

Q1. ...
0=모름, 1=..., 2=...

Q2. ...
0=모름, 1=..., 2=...

...

답변 예:
1 0 2 1 3 2
```

사용자는 반드시 **숫자 한 줄만** 입력할 수 있어야 한다.

---

# 23. 핵심 원칙 한 줄

```text
Evidence First → Same Run 분리 → First Failed Stage → Primary Root Cause → Contributing Factor → Non-Cause → 그 다음에만 수정
```
