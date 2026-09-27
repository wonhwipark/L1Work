# Job-list 반복 실패 Root Cause Analysis Prompt — 최소 입력형

- Version: v1.1
- Date: 2026-09-27 KST
- 실행 위치: 사내 Windows PC
- 목적: 반복적으로 동작하지 못했던 Job-list의 최초 실패 지점과 Root Cause를 실제 로그/상태/버전/Task Scheduler 근거로 확정한다.
- 사용자 응답 방식: **숫자 객관식만**
- 사용자 입력 최소화: **AI가 먼저 자동 조사하고, 정말 필요한 질문만 최대 10개 제시**
- 추가 질의가 필요한 경우에도 **한 번에 최대 5개 숫자 질문만 허용**

---

## 사용자 Interaction 최우선 규칙

이 규칙은 아래 모든 질문/진단 규칙보다 우선한다.

1. 자동 확인 가능한 항목은 사용자에게 절대 묻지 않는다.
2. 먼저 로그/상태파일/버전/Task Scheduler/signal을 AI가 직접 read-only로 조사한다.
3. 자동 조사 후에도 판단할 수 없는 항목만 질문한다.
4. 최초 사용자 질문은 **최대 10개**만 제시한다.
5. 추가 질문이 필요하더라도 한 번에 **최대 5개**만 제시한다.
6. 모든 질문은 `0/1/2/3/...` 숫자 선택식이어야 한다.
7. 사용자는 공백으로 구분한 숫자 한 줄만 입력하면 된다.
8. 모르면 항상 `0`을 선택할 수 있어야 한다.
9. 사용자에게 이유, 경로, 파일명, 버전 문자열, 로그 문장, 명령어 결과를 직접 타이핑하게 하지 않는다.
10. 필요한 파일/로그/경로는 AI가 직접 찾는다.
11. 자유서술 답변을 요구하지 않는다.
12. 같은 내용을 표현만 바꿔 재질문하지 않는다.
13. 이미 evidence로 확인된 항목을 사용자에게 다시 확인하지 않는다.
14. 질문을 많이 하는 것보다 `INSUFFICIENT_EVIDENCE`로 남기는 편을 우선한다.

사용자에게 질문할 때는 반드시 아래 형식으로 시작한다.

```text
자동으로 확인할 수 있는 항목은 먼저 확인했습니다.
아래 N개만 숫자로 답해주세요. 모르면 0입니다.

Q1 ...
0=모름, 1=..., 2=...

Q2 ...
0=모름, 1=..., 2=...

답변 예:
1 0 2 1 1
```


## 0. 목표

이번 단계에서는 먼저 수정하지 않는다. 아래 실행 체인 중 **가장 먼저 실패한 Gate**를 찾는다.

```text
Job-list package
 → Skill-updater detection
 → version/schema validation
 → activation
 → duplicate/expired/processed gate
 → Job runner
 → Job step
 → AutoTask Builder
 → Windows Task Scheduler
 → Dispatcher
 → Signal writer
```

최종 판정은 다음 4개만 사용한다.

```text
PRIMARY_ROOT_CAUSE
CONTRIBUTING_FACTOR
NOT_CAUSE
INSUFFICIENT_EVIDENCE
```

---

## 1. 절대 원칙

1. 추측으로 결론 내리지 않는다.
2. Production file/log/state/Task Scheduler를 실제 확인한다.
3. Root Cause 확정 전에는 Job-list, updater, dispatcher, AutoTask Builder를 수정하지 않는다.
4. `signal 값 변화 없음 = dispatcher 미동작`으로 자동 판단하지 않는다.
5. signal writer와 write condition을 먼저 확인한다.
6. dispatcher 등록 전에 dispatcher가 생성하는 signal을 precondition으로 사용하지 않는다.
7. 뒤 단계 증상보다 **First Failed Stage**를 우선한다.
8. 자동 확인 가능한 항목은 사용자에게 질문하지 않는다.
9. 사용자 질문은 모두 숫자 선택지만 제공한다.
10. 권한 상승, 위험한 전체 디스크 탐색, destructive cleanup은 하지 않는다.

---

## 2. 기존 관찰 — Seed Evidence, 재검증 필수

과거 다음 현상이 있었다. 현재 PC에서 사실 여부를 다시 검증한다.

- `dispatcher-windows-heartbeat-ok.signal` 값이 `1`에 머문 사례.
- Linux 쪽 `dispatcher-linux-heartbeat-ok.signal`은 `558`까지 증가한 사례.
- Windows dispatcher를 매시 `15/45분`에 실행하도록 AutoTask Builder로 등록하려 했으나 실제 등록 실패 가능성.
- `activation/history.jsonl`에서 과거:
  - `expired=1`, v0388 expired
  - `duplicates=1`, `duplicated_skipped`
- `core/processed.jsonl`에서 v0388 `state=expired` 사례.
- v0.3.97 / v0.3.98 계열 반복 실패.
- Dispatcher보다 **Skill-updater가 Job-list를 runner까지 넘기지 못하는 문제**가 핵심일 가능성이 제기됨.
- `dispatcher-windows-skill-updater-ok.signal`이 dispatcher 등록 이전에도 유효한 검증 신호인지 의문이 있었음.

위 내용은 Root Cause가 아니라 조사 우선순위다.

---

## 3. 필수 조사 대상

가능한 범위에서 read-only로 자동 탐색한다.

- 현재/최근 실패 Job-list package
- Skill-updater
- Windows Dispatcher bundle
- AutoTask Builder
- `activation/history.jsonl`
- `core/processed.jsonl`
- run/result/history/log 관련 json/jsonl/txt/log
- `*.signal`
- manifest/version metadata
- wrapper/bat/ps1/python entry point
- lock/pid/deferred/running marker
- Windows Task Scheduler task/trigger/history

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

접근 거부 경로는 SKIP한다.

---

## 4. Pipeline Evidence Matrix

반드시 작성한다.

| Stage | Evidence | Status | First Failure? |
|---|---|---|---|
| Job package detected | | | |
| Updater detected job | | | |
| Version/schema accepted | | | |
| Activation created | | | |
| Duplicate gate passed | | | |
| Expiry gate passed | | | |
| Processed gate passed | | | |
| Runner entered | | | |
| First job step entered | | | |
| AutoTask Builder invoked | | | |
| Task registered | | | |
| Dispatcher executed | | | |
| Signal writer executed | | | |
| Signal changed | | | |

Status:

```text
PASS / FAIL / NOT_REACHED / UNKNOWN / N/A
```

가장 앞선 `FAIL` 또는 그 이후 연속 `NOT_REACHED`를 First Failed Stage 후보로 삼는다.

---

## 5. Version / Activation / State 검사

실제 파일에서 확인:

### Version
- Job-list version
- manifest version
- package/folder label
- updater supported schema/version
- required updater version
- dispatcher version
- AutoTask Builder version

### Activation
- request 생성 여부
- accepted 여부
- expired 여부
- duplicate 여부
- skipped 여부
- last accepted version

### Processed
- 동일 Job ID/version이 이미 processed인지
- failed인데 processed 처리됐는지
- expired state가 재실행을 막는지
- duplicate key가 무엇인지
- version 변경만으로 새로운 job으로 인정되는지

---

## 6. Signal 검사

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

- updater가 쓰는지 dispatcher가 쓰는지
- task 등록 전에 생성 가능한지
- 값이 증가하는 방식인지 단순 overwrite인지
- timestamp만 갱신되고 값은 그대로일 수 있는지
- health gate로 사용할 수 있는지

Writer 검증 전에는 signal을 Root Cause evidence로 단정하지 않는다.

---

## 7. Windows Task Scheduler 검사

확인:

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

Task가 없다면 dispatcher signal 정지는 후행 증상일 수 있다.

---

## 8. Permission / Unattended 검사

확인:

- SYSTEM 계정으로 실행되어 사용자 HOME이 달라지는지
- HOME/LOCALAPPDATA config를 못 찾는지
- working directory dependency가 있는지
- interactive prompt 대기 여부
- 권한 확인 때문에 unattended 실행이 중단되는지
- stdout/stderr 저장 여부

---

## 9. LLM Fallback 검사

지원되는 경우에만 확인:

- fallback trigger
- 실제 호출 여부
- model
- timeout
- retry
- prompt/tool availability
- fallback 이후 state transition

LLM fallback이 activation/version/state gate를 자동 우회한다고 가정하지 않는다.

---

# 10. 사용자 객관식 질문 Pool

아래 Q1~Q30은 **질문 Pool**일 뿐이다. Q1~Q30 전체를 사용자에게 한 번에 보여주지 않는다.

수행 순서:

```text
1. AI가 먼저 가능한 evidence를 자동 확인
2. 자동 확인된 질문 제거
3. First Failed Stage/Root Cause 분리에 필요한 질문만 선택
4. 최초 최대 10개만 사용자에게 제시
5. 사용자는 숫자 한 줄로 응답
6. AI가 다시 evidence와 결합해 분석
7. 꼭 필요한 경우에만 추가 최대 5개 질문
```

질문 우선순위는 `First Failed Stage 판별 > Root Cause 분리 > 보조 확인`이다. 단순 참고용 질문은 생략한다.

응답 예:

```text
1 0 2 1 1
```

설명형 답변을 요구하지 않는다.

### Q1. 같은 실패가 발생했던 동일 사내 PC인가?
`0=모름, 1=동일, 2=다른 PC`

### Q2. 이전 state/log 파일이 현재도 남아있는가?
`0=모름, 1=남아있음, 2=초기화됨`

### Q3. 최근 실패 Job-list package를 보유하고 있는가?
`0=없음, 1=있음, 2=일부 버전만`

### Q4. 현재 Skill-updater 버전을 알고 있는가?
`0=모름, 1=알고 있음, 2=여러 버전 공존`

### Q5. 실패 당시 Skill-updater 실행 로그가 있었는가?
`0=모름, 1=있음, 2=없음`

### Q6. activation/history에 실패 Job이 나타났는가?
`0=모름, 1=accepted, 2=expired, 3=duplicate/skip, 4=entry 없음`

### Q7. core/processed에 실패 Job이 나타났는가?
`0=모름, 1=processed/success, 2=failed, 3=expired, 4=entry 없음`

### Q8. Job runner가 첫 step에 진입한 evidence가 있었는가?
`0=모름, 1=있음, 2=없음`

### Q9. AutoTask Builder invoke evidence가 있었는가?
`0=모름, 1=있음, 2=없음`

### Q10. Windows Task Scheduler에 dispatcher task가 생성됐는가?
`0=모름, 1=있음, 2=없음, 3=생성 후 삭제`

### Q11. Trigger가 의도한 15/45분과 일치했는가?
`0=모름, 1=일치, 2=불일치, 3=task 없음`

### Q12. Task Last Run Time이 갱신됐는가?
`0=모름, 1=갱신, 2=미갱신, 3=task 없음`

### Q13. Last Run Result는?
`0=모름, 1=성공, 2=실패, 3=실행 기록 없음`

### Q14. Dispatcher를 수동 실행하면 동작하는가?
`0=미확인, 1=정상, 2=실패`

### Q15. dispatcher-windows-heartbeat-ok.signal 값이 증가한 적이 있는가?
`0=모름, 1=있음, 2=계속 동일`

### Q16. signal timestamp는 갱신됐는데 값만 동일했던 적이 있는가?
`0=모름, 1=있음, 2=timestamp도 동일`

### Q17. dispatcher-windows-skill-updater-ok.signal writer를 알고 있는가?
`0=모름, 1=dispatcher, 2=skill-updater, 3=기타`

### Q18. 무인 실행 중 권한 팝업/확인 질문이 발생한 적이 있는가?
`0=모름, 1=있음, 2=없음`

### Q19. Task가 SYSTEM 계정으로 등록된 적이 있는가?
`0=모름, 1=있음, 2=없음`

### Q20. 사용자 HOME/LOCALAPPDATA config가 필요한 구조인가?
`0=모름, 1=맞음, 2=아님`

### Q21. 실패 Job이 이전 Job과 동일 Job ID/version key를 재사용했을 가능성이 있는가?
`0=모름, 1=있음, 2=명확히 다름`

### Q22. v0.3.97→v0.3.98처럼 version만 변경하고 Job identity/payload는 유사했는가?
`0=모름, 1=맞음, 2=아님`

### Q23. activation history에서 expired가 반복됐는가?
`0=모름, 1=반복, 2=1회, 3=없음`

### Q24. duplicated_skipped가 반복됐는가?
`0=모름, 1=반복, 2=1회, 3=없음`

### Q25. failed/expired인데 processed state 때문에 재실행이 차단된 것으로 보이는가?
`0=모름, 1=의심, 2=아님`

### Q26. updater가 runner에 넘기기 전 validation에서 종료된 정황이 있는가?
`0=모름, 1=있음, 2=없음`

### Q27. LLM fallback 실제 호출 로그가 있었는가?
`0=모름, 1=있음, 2=없음, 3=fallback 없음`

### Q28. 실패가 여러 Job-list 버전에서 반복됐는가?
`0=모름, 1=여러 버전, 2=특정 버전만`

### Q29. 동일 PC의 다른 scheduled task는 정상 실행되는가?
`0=모름, 1=정상, 2=다른 task도 문제`

### Q30. Root Cause 확정 후 허용 범위는?
`0=진단만, 1=최소 복구까지, 2=필요 component 수정까지`

---

# 11. Root Cause Categories

응답 + 실제 evidence로 분류:

```text
RC-A Job-list package/version
RC-B Skill-updater detection/activation
RC-C duplicate/expired/processed state machine
RC-D Job runner 미진입
RC-E AutoTask Builder invocation
RC-F Windows Task Scheduler registration
RC-G Dispatcher runtime
RC-H Signal writer/health interpretation
RC-I Permission/user-context
RC-J LLM fallback
```

각각:

```text
PRIMARY_ROOT_CAUSE
CONTRIBUTING_FACTOR
NOT_CAUSE
INSUFFICIENT_EVIDENCE
```

최대 3개까지만 우선순위를 매긴다.

---

# 12. First Failure Principle

예:

```text
Updater activation reject
→ Runner NOT_REACHED
→ AutoTask Builder NOT_REACHED
→ Dispatcher signal 정지

Primary Root Cause는 Dispatcher가 아니라 Updater/Activation 쪽이다.
```

또는:

```text
Task 등록 PASS
Dispatcher Last Run PASS
Signal writer 진입 UNKNOWN
Signal 값 정지

→ Dispatcher 등록 문제로 단정하지 말고 Signal Writer를 조사한다.
```

---

# 13. 최종 보고 형식

## A. Executive Summary

```text
Primary Root Cause:
First Failed Stage:
Confidence: HIGH / MEDIUM / LOW
```

## B. Pipeline Result

| Stage | Status | Evidence |
|---|---|---|
| Job detected | | |
| Updater accepted | | |
| Activation | | |
| Duplicate/Expiry | | |
| Runner | | |
| AutoTask Builder | | |
| Task Scheduler | | |
| Dispatcher | | |
| Signal | | |

## C. Root Cause Ranking

| Rank | Category | Verdict | Evidence |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## D. Confirmed Non-Causes
실제로 증거로 배제된 것만 작성.

## E. Signal Interpretation

```text
Signal:
Writer:
Expected Change:
Actual Change:
Can Be Used As Precondition: YES/NO
```

## F. Version / State

```text
Job-list:
Skill-updater:
Dispatcher:
AutoTask Builder:
Activation:
Processed:
Duplicate:
Expired:
```

## G. Scheduler

```text
Task Exists:
Trigger:
Run As:
Last Run:
Last Result:
Next Run:
```

## H. Next Action

Q30 기준:

```text
0 → 진단 결과만 보고하고 STOP
1 → Primary Root Cause의 최소 복구만 수행
2 → Root Cause와 직접 관련된 Job-list/Updater/Dispatcher/AutoTask Builder 수정까지 허용
```

원인과 무관한 리팩토링은 금지한다.

---

# 14. 성공 조건

다음을 모두 만족해야 분석 완료다.

1. 최초 실패 Gate 확인
2. Primary Root Cause 최소 1개 확정 또는 evidence 부족 명시
3. Updater/Job-list 선행 문제와 Dispatcher 문제를 분리
4. duplicate/expired/processed 영향 확인
5. Task Scheduler 실제 등록/실행 확인
6. signal writer와 signal 의미 확인
7. permission/user-context 확인
8. LLM fallback 실제 동작 여부 확인
9. 미확인 가설은 가설로 유지
10. 다음 복구 대상 component를 정확히 특정

---

# 15. 최종 실행 지시

1. 먼저 사내 PC에서 가능한 evidence를 **read-only**로 자동 수집한다.
2. Q1~Q30 전체를 사용자에게 보여주지 않는다.
3. 자동 확인 불가능하면서 Root Cause 판별에 꼭 필요한 질문만 고른다.
4. 최초 질문은 **최대 10개**만 제시한다.
5. 사용자는 숫자 한 줄로만 응답한다.
6. 응답 후 AI가 다시 evidence를 분석한다.
7. 추가 확인이 반드시 필요하면 **최대 5개** 숫자 질문만 한 번 더 제시한다.
8. 충분한 evidence가 확보되면 추가 질문 없이 First Failed Stage를 결정한다.
9. Root Cause를 최대 3개까지 우선순위화한다.
10. Q30 범위에 맞춰 STOP/최소복구/수정 단계로 이동한다.

사용자에게 다음을 요구하지 않는다.

```text
긴 설명
로그 내용 복사
경로 직접 입력
버전 문자열 직접 입력
명령어 결과 직접 입력
실패 상황 자유서술
```

필요한 정보는 가능한 한 AI가 직접 찾는다.

**Root Cause 분석이 끝나기 전에는 component를 수정하지 않는다.**


---

# 16. 실제 사용자 Interaction 예시

좋은 예:

```text
자동 확인 결과:
- Job package 발견
- Skill-updater 실행 흔적 발견
- activation entry 발견
- Task Scheduler에는 dispatcher task 없음

추가로 4개만 확인하면 됩니다. 모르면 0으로 답해주세요.

Q1. 이 PC가 이전 실패가 발생한 동일 PC인가?
0=모름, 1=동일, 2=다름

Q2. dispatcher를 수동 실행해본 적이 있는가?
0=미확인, 1=정상, 2=실패

Q3. 무인 실행 중 권한 팝업이 나온 적이 있는가?
0=모름, 1=있음, 2=없음

Q4. Root Cause 확정 후 허용 범위는?
0=진단만, 1=최소복구, 2=필요 component 수정

답변 예:
1 0 2 1
```

나쁜 예:

```text
Q1~Q30 전체를 모두 보여줌
로그를 복사해달라고 요청
경로/버전/명령어 결과를 직접 입력하게 함
실패 당시 상황을 길게 설명하게 함
```

위 방식은 사용하지 않는다.
