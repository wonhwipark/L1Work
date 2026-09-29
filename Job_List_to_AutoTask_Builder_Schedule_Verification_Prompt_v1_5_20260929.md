# Job-list → AutoTask Builder Schedule 전달 검증 Prompt

- Version: v1.5
- Date: 2026-09-29 KST
- 목적: 반복 실패의 남은 핵심 가설인 **Job-list → AutoTask Builder schedule 전달값 오류 여부**를 read-only로 확정한다.
- 실행 위치: 사내 Windows PC
- 사용자 응답 방식: 필요한 경우에만 숫자 객관식 한 줄
- 중요: **검증 전에는 Job-list / Skill-updater / AutoTask Builder / Dispatcher / Task Scheduler를 수정하지 않는다.**

---

# 0. 이번 검증의 핵심 질문

이번 단계에서는 아래 한 가지를 최우선으로 확인한다.

```text
Job-list 의도
"Dispatcher를 매시 15분 / 45분에 실행"

        ↓

Job-list가 AutoTask Builder에 실제 전달한 schedule

A. "15,45 * * * *"
또는
B. "*/30 * * * *"
또는
C. 그 외
```

Root Cause 판정 전에 추측하지 않는다.

---

# 1. 현재 확인해야 할 가설

## H1. Job-list 전달값 오류

```text
사용자 의도 = 15/45
하지만 Job-list가 Builder에 전달한 값 = */30
```

이 경우:

```text
00/30 등록은 Builder의 생성 오류가 아니라
Job-list → Builder contract/config 생성 오류
```

가 된다.

---

## H2. Builder phase 검증 누락

Job-list가 정상적으로:

```text
15,45 * * * *
```

를 전달했는데도 실제 Scheduler가:

```text
00/30
```

으로 등록됐다면 AutoTask Builder 쪽을 조사한다.

특히 단순히:

```text
Interval = PT30M
```

만 비교하면:

```text
15/45
00/30
```

을 구분하지 못할 수 있으므로 반드시 `StartBoundary / phase`까지 확인한다.

---

## H3. Job-list와 Builder는 정상, 검증/관찰만 잘못됨

실제 Scheduler XML이:

```text
15/45 phase
```

로 정상인데 기존 진단 결과만 `Trigger mismatch`로 판단했다면:

```text
Root Cause = schedule 생성이 아니라 validation/observation 오류
```

로 분리한다.

---

# 2. 절대 원칙

1. 모든 확인은 read-only로 한다.
2. Job-list 수정 금지
3. Skill-updater 수정 금지
4. AutoTask Builder 수정 금지
5. Dispatcher 수정 금지
6. Task Scheduler task 수정/삭제/재등록 금지
7. Job 재실행 금지
8. activation / processed / history 삭제 금지
9. signal 초기화 금지
10. version bump 금지
11. 자동 확인 가능한 항목은 사용자에게 묻지 않는다.
12. 사용자에게 경로/로그/명령 결과를 타이핑하게 하지 않는다.
13. 질문이 필요한 경우 숫자 객관식만 사용한다.
14. 사용자 답변에는 항상 `0=모름`을 제공한다.
15. 기존 결론에 맞추기 위해 evidence를 해석하지 않는다.

---

# 3. 조사 대상

최소한 아래를 찾는다.

```text
1. 가장 최근 실패 Job-list package
2. 해당 Job-list manifest
3. Dispatcher 등록 step
4. AutoTask Builder 호출부
5. AutoTask Builder input YAML/JSON/task definition
6. Builder가 생성한 canonical task
7. schtasks /Create 또는 등록 wrapper 입력
8. 실제 Windows Task Scheduler XML
9. 관련 run/result/log/history
```

가능하면 아래 버전도 기록한다.

```text
Job-list version:
Skill-updater version:
AutoTask Builder version:
Dispatcher version:
```

---

# 4. Step 1 — 가장 최근 실패 Job-list 식별

먼저 현재 분석 대상이 정확히 무엇인지 확정한다.

확인:

```text
Job ID
Job version
Run ID
Attempt ID
activation timestamp
runner timestamp
AutoTask Builder invoke timestamp
```

여러 version 또는 attempt가 섞이지 않게 한다.

최종 분석 기준:

```text
가장 최근 실패 실행의 최종 attempt
```

---

# 5. Step 2 — Job-list의 사용자 의도 확인

Job-list 안에서 Dispatcher 등록 의도를 찾는다.

검색 대상 예:

```text
15/45
15,45
*/30
30 minute
30min
dispatcher
autotask
schedule
cron
task_dispatcher
```

결과를 아래처럼 기록한다.

```text
Intended Schedule:
Source File:
Source Section:
Evidence:
```

사용자 자연어 요청이 별도 prompt/md에 있으면 그것도 evidence로 사용한다.

---

# 6. Step 3 — Job-list가 Builder에 실제 전달한 값 확인

가장 중요하다.

아래 경로를 추적한다.

```text
Job-list step
→ generated task definition
→ AutoTask Builder input
→ normalized/canonical task
```

반드시 **실제 값**을 기록한다.

```text
Job-list requested cron:
Generated cron:
Builder input cron:
Canonical cron:
```

아래 세 경우로 분류한다.

### CASE A

```text
Job-list intent        = 15/45
Builder input          = */30
```

판정 후보:

```text
Job-list → Builder schedule translation/config 오류
```

### CASE B

```text
Job-list intent        = 15/45
Builder input          = 15,45
```

판정:

```text
Job-list 전달은 정상
→ Builder / Scheduler 단계 계속 조사
```

### CASE C

```text
Job-list intent 자체가 */30
```

판정:

```text
요구사항 반영 누락 또는 잘못된 template 사용
```

---

# 7. Step 4 — Template / Default 영향 확인

AutoTask Builder 또는 Job-list가 template을 참조한다면 아래를 확인한다.

```text
template file
default cron
override 가능 여부
override 실제 적용 여부
merge order
precedence
```

특히:

```text
default = */30
job override = 15,45
```

인 경우 최종 canonical 결과가 무엇인지 확인한다.

가능한 문제:

```text
- override 미적용
- default 우선
- merge 순서 오류
- field name mismatch
- schedule object 재생성
```

---

# 8. Step 5 — Builder 내부 normalize / render 확인

Builder가 받은 값이:

```text
15,45 * * * *
```

이었다면 이후 변환을 추적한다.

기록:

```text
Input cron:
Parsed minute field:
Normalized interval:
Calculated StartBoundary:
Calculated repetition interval:
Generated schtasks/XML:
```

15/45의 예상 의미:

```text
실행 간격 = 30분
phase = 매시 15분 / 45분
```

중요:

```text
Interval = PT30M
```

만으로는 phase 검증이 불충분하다.

반드시 `StartBoundary` 또는 동등한 phase 정보도 확인한다.

---

# 9. Step 6 — 실제 Task Scheduler XML 검증

read-only query로 실제 Task Scheduler 설정을 확인한다.

확인:

```text
Task Name
Enabled
StartBoundary
Repetition Interval
ScheduleByDay/TimeTrigger
Program
Arguments
WorkingDirectory
```

15/45 요구사항에 대해 다음을 구분한다.

### 정상

```text
StartBoundary phase = :15 또는 동등한 15/45 반복
Interval = 30분
```

### 비정상

```text
StartBoundary phase = :00
Interval = 30분
```

### 불명확

```text
XML/query 결과만으로 phase 판별 불가
```

---

# 10. Step 7 — 기존 Trigger mismatch evidence 재검증

과거 다음과 같은 evidence가 있었다면:

```text
Trigger mismatch
```

이번에는 무엇을 비교해서 mismatch로 판단했는지 확인한다.

```text
Cron text?
Interval?
StartBoundary?
Next Run Time?
Task XML?
Builder internal post-check?
Job-list post-check?
```

단순:

```text
Interval = PT30M
```

만 보고 15/45 여부를 판단했다면 해당 evidence는 무효 또는 불충분으로 재분류한다.

---

# 11. Step 8 — First Failed Stage 재판정

이 검증 결과에 따라 아래 중 하나로 판정한다.

---

## Verdict A — Job-list schedule 전달 오류

조건:

```text
User intent = 15/45
Job-list/Builder input = */30
```

판정:

```text
FIRST_FAILED_STAGE
Job-list schedule/config generation

PRIMARY_ROOT_CAUSE
RC-A Job-list package/config
또는
Job-list → AutoTask Builder contract
```

AutoTask Builder는 입력대로 동작한 것이므로 Primary가 아니다.

---

## Verdict B — Builder normalize/render 오류

조건:

```text
Builder input = 15,45
하지만 generated Scheduler config = 00/30
```

판정:

```text
FIRST_FAILED_STAGE
AutoTask Builder schedule render/translation

PRIMARY_ROOT_CAUSE
RC-E AutoTask Builder
```

---

## Verdict C — Builder 등록은 정상, validation 문제

조건:

```text
Builder input = 15,45
Scheduler XML = 15/45 정상
하지만 Builder/Job-list가 FAIL 판정
```

판정:

```text
FIRST_FAILED_STAGE
Post-registration validation

PRIMARY_ROOT_CAUSE
검증 로직이 위치한 component
```

반드시 Builder 내부 validator인지 Job-list 후처리 validator인지 구분한다.

---

## Verdict D — Evidence 부족

조건:

```text
실제 Builder input 또는 Scheduler XML을 찾을 수 없음
```

판정:

```text
INSUFFICIENT_EVIDENCE
```

추측으로 Root Cause를 확정하지 않는다.

---

# 12. Pipeline Evidence Matrix

반드시 작성한다.

| Stage | Actual Value | Expected | Status | Evidence |
|---|---|---|---|---|
| User intent | | 15/45 | | |
| Job-list schedule | | 15/45 | | |
| Generated task definition | | 15/45 | | |
| Builder input | | 15/45 | | |
| Canonical task | | 15/45 | | |
| StartBoundary | | :15 phase | | |
| Interval | | 30 min | | |
| Scheduler XML | | 15/45 | | |
| Post-validation | | PASS | | |

Status:

```text
PASS
FAIL
UNKNOWN
N/A
```

---

# 13. 자동 확인 불가 시 사용자 질문 Pool

자동 조사 후에도 꼭 필요한 경우에만 묻는다.

### Q1. 최근 실패 Job-list가 의도한 Dispatcher 실행 시간은?
`0=모름, 1=매시 15/45, 2=매시 00/30, 3=기타`

### Q2. 실제 Task Scheduler에서 보인 실행 phase는?
`0=모름, 1=15/45, 2=00/30, 3=그 외`

### Q3. Job-list 또는 생성 task YAML에서 cron 값을 직접 확인했는가?
`0=미확인, 1=15,45, 2=*/30, 3=기타`

### Q4. AutoTask Builder input 파일에서 cron 값을 확인했는가?
`0=미확인, 1=15,45, 2=*/30, 3=기타`

### Q5. Builder가 생성한 canonical task에서 cron은?
`0=미확인, 1=15,45, 2=*/30, 3=기타`

### Q6. 실제 Scheduler XML의 StartBoundary minute는?
`0=미확인, 1=15, 2=00, 3=기타`

### Q7. 실제 Scheduler XML의 repetition interval은?
`0=미확인, 1=30분, 2=다름`

### Q8. Trigger mismatch를 판정한 component는?
`0=모름, 1=Job-list, 2=AutoTask Builder, 3=별도 validation script, 4=사용자 수동 확인`

### Q9. 최근 실패 실행과 현재 확인한 Task는 동일 Task인가?
`0=모름, 1=동일, 2=다름`

### Q10. Root Cause 확정 후 허용 범위는?
`0=진단만, 1=최소 수정, 2=관련 component 수정 + 신규 Job-list 생성`

질문 출력 예:

```text
자동 확인 가능한 항목은 먼저 확인했습니다.

현재 schedule 전달 경로 확정에 필요한 4개만 확인합니다.
모르면 0입니다.

Q1 ...
Q2 ...
Q3 ...
Q4 ...

답변 예:
1 2 2 2
```

---

# 14. 최종 출력 형식

## A. Executive Summary

```text
Expected Schedule:
Actual Job-list Schedule:
Actual Builder Input:
Actual Scheduler Schedule:

First Failed Stage:
Primary Root Cause:
Confidence:
```

---

## B. Schedule Trace

```text
User Intent
  ↓
Job-list
  ↓
Generated Task
  ↓
Builder Input
  ↓
Canonical Task
  ↓
Scheduler XML
```

각 단계 실제 값을 함께 표기한다.

---

## C. Root Cause Classification

```text
PRIMARY_ROOT_CAUSE:
CONTRIBUTING_FACTOR:
NOT_CAUSE:
INSUFFICIENT_EVIDENCE:
```

---

## D. Exact Failure Point

```text
Component:
File:
Function/Step:
Expected:
Actual:
Why It Failed:
```

파일/함수까지 evidence로 확인 가능한 경우에만 작성한다.

---

## E. Next Action

분석 완료 후에만 제안한다.

예:

```text
1. Job-list cron을 15,45로 수정
2. Builder에 StartBoundary/phase validation 추가
3. 15,45 regression test 추가
4. 신규 Job ID/version 생성
5. 기존 processed/activation state와 충돌하지 않는지 확인
6. Dispatcher 등록 전용 복구 Job-list 실행
```

단, Root Cause와 무관한 수정은 금지한다.

---

# 15. 성공 조건

다음을 모두 만족하면 검증 완료다.

```text
1. 가장 최근 실패 Job-list 식별
2. 사용자 의도 schedule 확인
3. Job-list 실제 schedule 확인
4. AutoTask Builder input schedule 확인
5. canonical task schedule 확인
6. Scheduler XML phase 확인
7. 15/45 vs 00/30 차이의 최초 발생 위치 확인
8. First Failed Stage 확정
9. Primary Root Cause 확정 또는 INSUFFICIENT_EVIDENCE
10. 수정 없이 진단 종료
```

---

# 16. 핵심 원칙

```text
"30분 간격"과 "15/45 phase"는 같은 의미가 아니다.

Interval만 보지 말고
Job-list cron → Builder input → StartBoundary → Scheduler XML
전체 전달 경로를 확인한다.
```
