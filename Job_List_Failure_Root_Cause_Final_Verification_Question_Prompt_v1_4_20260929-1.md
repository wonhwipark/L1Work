# Job-list 반복 실패 Root Cause — Final Verification Question Prompt

- Version: v1.4
- Date: 2026-09-29 KST
- 목적: 현재까지 도출된 Root Cause를 뒤집거나 보강할 수 있는 **남은 불확실성만 추가 확인**한다.
- 실행 위치: 사내 Windows PC
- 분석 방식: Read-only / Evidence First / 숫자 객관식
- 사용자 응답 방식: 숫자 한 줄
- 중요: 이번 단계에서도 **수정 금지**. 추가 확인만 수행한다.

---

# 0. 현재 잠정 결론

현재까지 가장 최근 실패 실행의 최종 attempt 기준으로 다음이 확인되었다.

```text
Job package                    PASS
Skill-updater detection        PASS
Version/schema                 PASS (최종 attempt 기준)
Activation/state               PASS
Duplicate/processed gate       PASS / terminal blocker 아님
Runner                         PASS
First Job Step                 PASS
AutoTask Builder invoke        PASS
Task create/update command     PASS
Task 실제 생성                 PASS
AutoTask Builder post-check    FAIL
```

현재 잠정 판정:

```text
FIRST_FAILED_STAGE
AutoTask Builder Post-validation

PRIMARY_ROOT_CAUSE 후보
RC-E AutoTask Builder

CONTRIBUTING_FACTOR 후보
- 과거 attempt의 fatal Version/schema validation failure
- Signal writer/health signal 이상 가능성

NOT_CAUSE 후보
- Job package 부재
- Skill-updater 미탐지
- 최종 attempt의 duplicate/processed terminal block
- Runner 미진입
- Task 자체 미생성
- 실제 15/45 Trigger 설정 오류
- Scheduler가 Dispatcher를 launch하지 못한 문제
- Dispatcher 미진입
- HOME/Working Directory 오류
- LLM fallback
```

이번 추가 확인의 목적은 위 결론을 다시 넓게 조사하는 것이 아니다.

아래 네 가지 불확실성만 정리한다.

```text
1. AutoTask Builder post-validation의 정확한 실패 조건
2. Task Scheduler Last Run Result와 Dispatcher 정상 종료의 불일치
3. Signal writer path 도달 후 signal 변화가 없는 이유
4. 네트워크/사내 리소스 접근 실패가 Primary Root Cause와 연관되는지
```

---

# 1. 절대 원칙

1. Job-list 수정 금지
2. Skill-updater 수정 금지
3. Dispatcher 수정 금지
4. AutoTask Builder 수정 금지
5. Task Scheduler task 수정/삭제/재등록 금지
6. signal 초기화 금지
7. state/history 삭제 금지
8. processed/activation state 강제 변경 금지
9. Job 강제 재실행 금지
10. read-only evidence만 확인
11. 자동 확인 가능한 항목은 사용자에게 묻지 않음
12. 사용자 질문은 모두 숫자 객관식
13. 사용자는 숫자 한 줄로만 답변
14. 모르면 `0`
15. 기존에 확정된 PASS/NOT_CAUSE를 다시 질문하지 않음

---

# 2. Read-only 자동 확인 우선순위

사용자 질문 전에 가능한 경우 아래를 자동 확인한다.

## A. AutoTask Builder Post-validation

확인:

```text
- Builder result/status log
- create/update command exit code
- post-check 함수/step 이름
- post-check에서 비교한 실제 항목
- expected value
- actual value
- comparison normalization 여부
- retry/post-check timeout 여부
- Task XML read-back 여부
- locale/timezone/string formatting 영향
```

특히 아래를 찾는다.

```text
Trigger comparison
Task Name comparison
Enabled comparison
Run As comparison
Program comparison
Arguments comparison
Working Directory comparison
Schedule/time comparison
Task XML equality/hash comparison
Last Run Result comparison
Existence check
```

## B. Scheduler Result vs Dispatcher Exit

확인:

```text
- Task Scheduler Last Run Result raw code
- Scheduler event history
- Action start event
- Action complete event
- Program/wrapper exit code
- Dispatcher process exit code
- wrapper/bat/ps1/python propagation 여부
```

중요:

```text
Dispatcher 내부 정상 종료
≠
Task Scheduler Last Run Result = success
```

wrapper가 다른 exit code를 반환할 수 있으므로 경계를 분리한다.

## C. Signal Writer

확인:

```text
Signal file path
writer function
write condition
increment/overwrite
atomic write/rename 여부
file open mode
error handling
write return code
flush/close
timestamp behavior
same-value overwrite behavior
actual target path
```

특히:

```text
writer code path reached
≠
file write success
```

를 구분한다.

## D. Network / Internal Resource Failure

확인:

```text
실패 timestamp
AutoTask Builder timestamp
Dispatcher timestamp
Skill-updater timestamp
resource name/type
retry 여부
fatal/non-fatal 여부
state transition 영향
```

Primary Root Cause와 시간적/논리적으로 연결되지 않으면 `NOT_CAUSE` 또는 별도 contributing factor로 둔다.

---

# 3. 추가 질문 Pool

자동 확인 후에도 남는 항목만 묻는다.

## A. AutoTask Builder Post-validation

### Q1. Builder가 실패로 판정한 post-check 항목이 확인됐는가?
`0=모름, 1=확인됨, 2=아직 미확인`

### Q2. 실패한 post-check 항목은 무엇인가?
`0=모름, 1=Trigger, 2=Task 존재, 3=Enabled, 4=Run As, 5=Program/Path, 6=Arguments, 7=Working Directory, 8=Schedule/Time, 9=Task XML/전체 비교, 10=Last Run Result, 11=기타`

### Q3. 실제 Task 상태는 해당 post-check 기대값과 일치했는가?
`0=모름, 1=실제 상태는 정상인데 Builder가 FAIL 판정, 2=실제 상태도 불일치`

### Q4. Builder post-check가 Task 생성 직후 즉시 수행됐는가?
`0=모름, 1=즉시 수행, 2=대기/재시도 후 수행`

### Q5. post-check가 retry 없이 1회 실패로 최종 FAIL 처리됐는가?
`0=모름, 1=맞음, 2=retry 있음`

### Q6. Builder가 읽은 Task와 사용자가 확인한 Task가 완전히 같은 Task Name/Path인가?
`0=모름, 1=같음, 2=다름`

### Q7. Trigger 시간 비교에서 locale/timezone/표현 형식 차이가 있었는가?
`0=모름, 1=있음, 2=없음`

### Q8. Task XML read-back 또는 Scheduler query 자체는 성공했는가?
`0=모름, 1=성공, 2=실패`

---

## B. Scheduler / Dispatcher Exit Code

### Q9. Task Scheduler Last Run Result의 raw code를 자동 확인했는가?
`0=미확인, 1=확인됨`

### Q10. Scheduler Action 자체는 시작됐는가?
`0=모름, 1=시작됨, 2=시작 실패`

### Q11. Dispatcher process exit code는 0이었는가?
`0=모름, 1=0/정상, 2=non-zero`

### Q12. Dispatcher 앞뒤에 wrapper(bat/ps1/python)가 있는가?
`0=모름, 1=있음, 2=없음`

### Q13. wrapper exit code와 Dispatcher exit code가 다를 가능성이 있는가?
`0=모름, 1=있음, 2=없음`

### Q14. Scheduler FAIL은 Dispatcher 종료 후 wrapper/post-check에서 발생했는가?
`0=모름, 1=맞음, 2=아님`

---

## C. Signal Writer

### Q15. heartbeat signal writer 함수가 실제 file write 호출까지 도달했는가?
`0=모름, 1=도달, 2=writer 함수 진입만 확인`

### Q16. signal write 호출 결과는?
`0=모름, 1=성공, 2=실패`

### Q17. signal 방식은?
`0=모름, 1=increment, 2=overwrite, 3=timestamp only`

### Q18. 동일 값 overwrite 시 파일 timestamp가 갱신되는 구조인가?
`0=모름, 1=갱신, 2=갱신 안 됨`

### Q19. writer가 사용하는 실제 signal path와 확인한 signal path가 같은가?
`0=모름, 1=같음, 2=다름`

### Q20. signal write error가 로그에 남아 있는가?
`0=모름, 1=있음, 2=없음`

---

## D. Network / Internal Resource

### Q21. 네트워크/사내 리소스 실패 시점은 AutoTask Builder FAIL보다 앞인가?
`0=모름, 1=앞, 2=뒤, 3=동시/연관 불명`

### Q22. 해당 네트워크 실패가 AutoTask Builder post-check가 사용하는 리소스와 관련 있는가?
`0=모름, 1=관련 있음, 2=관련 없음`

### Q23. 네트워크 실패가 fatal 처리됐는가?
`0=모름, 1=fatal, 2=warning/non-fatal`

### Q24. 네트워크 실패 후에도 Builder가 Task 생성과 post-check까지 진행했는가?
`0=모름, 1=진행, 2=진행 못함`

---

# 4. 판정 규칙

## Case 1 — Builder false negative 확정

아래가 확인되면:

```text
Task create/update command = success
Task 실제 상태 = 정상
Builder post-check = FAIL
동일 Task 확인 = YES
```

판정:

```text
PRIMARY_ROOT_CAUSE
RC-E AutoTask Builder post-validation false negative
```

추가로 정확한 validator 항목까지 식별한다.

## Case 2 — 실제 Task config 문제

아래가 확인되면:

```text
Builder post-check FAIL
실제 Task 상태도 기대값과 불일치
```

판정:

```text
PRIMARY_ROOT_CAUSE
RC-E 또는 RC-F

First Failed Stage는 실제 불일치가 생성된 위치를 기준으로 결정
```

## Case 3 — Scheduler Last Run Result만 별도 실패

아래가 확인되면:

```text
Task launch PASS
Dispatcher exit 0
wrapper/post-check non-zero
```

판정:

```text
Scheduler 자체 문제 아님
wrapper/exit-code propagation 또는 post-check 문제
```

이는 Primary Root Cause와 별개의 contributing factor일 수 있다.

## Case 4 — Signal path mismatch

아래가 확인되면:

```text
writer 호출 PASS
write success PASS
확인 signal 변화 없음
writer target path != 확인 path
```

판정:

```text
RC-H Signal interpretation/path mismatch
CONTRIBUTING_FACTOR 또는 NOT_CAUSE
```

## Case 5 — Signal write 자체 실패

아래가 확인되면:

```text
writer path reached
actual write FAIL
```

판정:

```text
RC-H Signal writer defect
```

단, AutoTask Builder failure보다 뒤라면 Primary가 아니라 contributing factor다.

## Case 6 — Network failure

아래를 모두 만족해야 Primary 후보로 올릴 수 있다.

```text
AutoTask Builder FAIL보다 선행
Builder post-check가 해당 resource 사용
fatal state transition 발생
```

그렇지 않으면:

```text
CONTRIBUTING_FACTOR
또는
NOT_CAUSE
```

---

# 5. 최종 출력 형식

## A. Final Verification Summary

```text
Primary Root Cause:
First Failed Stage:
Exact Failing Validator:
Confidence:
```

## B. Remaining Uncertainty

```text
Resolved:
- ...

Still Unknown:
- ...
```

## C. Root Cause Classification

```text
PRIMARY_ROOT_CAUSE:
CONTRIBUTING_FACTOR:
NOT_CAUSE:
INSUFFICIENT_EVIDENCE:
```

## D. AutoTask Builder

```text
Create Command:
Create Result:
Actual Task State:
Post-check:
Post-check Item:
Expected:
Actual:
False Negative: YES / NO / UNKNOWN
```

## E. Scheduler / Dispatcher

```text
Task Last Result:
Action Started:
Dispatcher Exit:
Wrapper Exit:
Mismatch:
Verdict:
```

## F. Signal

```text
Writer:
Writer Reached:
Write Called:
Write Result:
Write Mode:
Target Path:
Observed Path:
Timestamp Behavior:
Verdict:
```

## G. Network

```text
Failure Time:
Related Resource:
Fatal:
Builder Dependency:
Verdict:
```

---

# 6. 사용자 질문 출력 템플릿

```text
자동 확인 가능한 항목은 먼저 확인했습니다.

현재 Root Cause 최종 검증에 필요한 항목만 질문합니다.
모르면 0입니다.
설명 없이 숫자 한 줄만 답해주세요.

Q1. ...
0=모름, 1=..., 2=...

...

답변 예:
1 9 1 1 1 1 2 1
```

---

# 7. 종료 조건

아래 중 하나면 추가 질문을 종료한다.

```text
A. AutoTask Builder post-validation false negative가 확정됨
B. 실제 Task config 불일치가 확정됨
C. 정확한 failing validator는 미확인이지만 First Failed Stage/Primary Root Cause는 HIGH confidence로 확정됨
D. 추가 evidence가 없어 더 이상 객관적 분리가 불가능함
```

D인 경우:

```text
INSUFFICIENT_EVIDENCE
```

로 남기고 질문을 반복하지 않는다.

---

# 8. 핵심 한 줄

```text
이미 좁혀진 Root Cause를 다시 넓히지 말고,
AutoTask Builder post-validation을 중심으로 남은 불확실성만 검증한다.
```
