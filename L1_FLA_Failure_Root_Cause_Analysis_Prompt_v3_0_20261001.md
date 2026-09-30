# L1-FLA 로그분석 실패 Root Cause Analysis Prompt — 최소 입력형

- Version: v3.0
- Date: 2026-10-01 KST
- 목적: L1-FLA 로그분석 실패의 최초 실패 지점과 Root Cause를 실제 run/result/analyzer/download 근거로 확정한다.
- 사용자 응답 방식: **숫자 객관식만**
- 사용자 입력 최소화: **AI가 먼저 자동 조사하고, 정말 필요한 질문만 최대 10개 제시**
- 추가 질의가 필요한 경우에도 **한 번에 최대 5개 숫자 질문만 허용**

---

## 사용자 Interaction 최우선 규칙

이 규칙은 아래 모든 질문/진단 규칙보다 우선한다.

1. 자동 확인 가능한 항목은 사용자에게 절대 묻지 않는다.
2. 먼저 최신 실패 Run, final report, run_state/result, analyzer selection, preflight, download/SDM/QB/provider 로그를 AI가 직접 read-only로 조사한다.
3. 자동 조사 후에도 판단할 수 없는 항목만 질문한다.
4. 최초 사용자 질문은 **최대 10개**만 제시한다.
5. 추가 질문이 필요하더라도 한 번에 **최대 5개**만 제시한다.
6. 모든 질문은 `0/1/2/3/...` 숫자 선택식이어야 한다.
7. 사용자는 공백으로 구분한 숫자 한 줄만 입력하면 된다.
8. 모르면 항상 `0`을 선택할 수 있어야 한다.
9. 사용자에게 이유, 경로, 파일명, Jira 번호, 버전 문자열, 로그 문장, 명령 결과를 직접 타이핑하게 하지 않는다.
10. 필요한 파일/로그/경로/Run/Jira 후보는 AI가 직접 찾는다.
11. 자유서술 답변을 요구하지 않는다.
12. 같은 내용을 표현만 바꿔 재질문하지 않는다.
13. 이미 evidence로 확인된 항목을 사용자에게 다시 확인하지 않는다.
14. 질문을 늘리기보다 `INSUFFICIENT_EVIDENCE`로 남기는 편을 우선한다.
15. 사용자에게 질문하는 문장에는 반드시 바로 아래 줄에 숫자 선택지가 있어야 한다.
16. 숫자 선택지가 없는 질문이 하나라도 있으면 해당 응답을 폐기하고 객관식으로 다시 작성한다.

사용자에게 질문할 때는 반드시 아래 형식으로 시작한다.

```text
자동으로 확인할 수 있는 항목은 먼저 확인했습니다.
아래 N개만 숫자로 답해주세요. 모르면 0입니다.

Q1. ...
0=모름, 1=..., 2=...

Q2. ...
0=모름, 1=..., 2=...

답변 예:
1 0 2 1
```

---

## 0. 목표

이번 단계에서는 먼저 수정하지 않는다. 아래 실행 체인 중 **가장 먼저 실패한 Gate**를 찾는다.

```text
Jira target
 → Jira/Remote Link 접근
 → 로그 후보 탐색
 → 로그 다운로드/획득
 → SDM/QB/Binary 준비
 → Analyzer selection
 → Analyzer availability/preflight
 → Analyzer invocation
 → Analyzer execution
 → Analyzer result validation
 → FLA final aggregation/report
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
2. 실제 run/result/state/log/config를 확인한다.
3. Root Cause 확정 전에는 L1-FLA/analyzer/config를 수정하지 않는다.
4. `로그획득실패`라는 HTML 표시만 보고 다운로드 문제로 확정하지 않는다.
5. `Analyzer 이름이 설정에 존재 = 실제 호출 가능`으로 판단하지 않는다.
6. fallback 설정과 fallback 실제 수행을 구분한다.
7. 뒤 단계 증상보다 **First Failed Stage**를 우선한다.
8. 자동 확인 가능한 항목은 사용자에게 질문하지 않는다.
9. 사용자 질문은 모두 숫자 선택지만 제공한다.
10. 권한 상승, destructive cleanup, 위험한 전체 디스크 탐색은 하지 않는다.

---

## 2. Analyzer 기준 — 재검증 필수

현재 기대 기본 Analyzer가 `l1-log-analysis`일 수 있지만, 실제 분석에서는 반드시 아래 순서로 확인한다.

1. 현재 profile/config의 default analyzer
2. target별 override
3. legacy analysis.skill
4. analyzer registry
5. actual analyzer_selection
6. preflight result
7. fallback selection

설정에 이름이 적혀 있다는 이유만으로 실제 사용 Analyzer라고 단정하지 않는다.

---

## 3. 필수 조사 대상

가능한 범위에서 read-only로 자동 탐색한다.

- 최신 실패 L1-FLA Run
- `final_report.html`
- `final_report.md`
- `run_state.json`
- Jira별 `result.json`
- Jira별 `issue_detail.html`
- analyzer selection/preflight/invocation 관련 json/log
- stdout/stderr
- profile/config
- analyzer registry
- 다운로드/remote link/attachment/FTP/WIZNET 관련 로그
- SDM converter 결과
- QB/build/binary/symbol 관련 상태
- provider(OpenCode/Claude Code/Qwen Code 등) 실행 정보
- timeout/retry/fallback 정보

탐색 순서:

```text
현재 working directory
 → 현재 L1-FLA run/output
 → known persistent output
 → HOME
 → project run/state/log directory
```

접근 거부 경로는 SKIP한다.

---

## 4. Pipeline Evidence Matrix

반드시 작성한다.

| Stage | Evidence | Status | First Failure? |
|---|---|---|---|
| Jira target resolved | | | |
| Jira access | | | |
| Remote Link/source discovery | | | |
| Log candidate selected | | | |
| Log downloaded/acquired | | | |
| SDM conversion | | | |
| QB/Binary ready | | | |
| Analyzer selected | | | |
| Analyzer preflight | | | |
| Analyzer invoked | | | |
| Analyzer completed | | | |
| Result validated | | | |
| Final report aggregated | | | |

Status:

```text
PASS / FAIL / NOT_REACHED / UNKNOWN / N/A
```

가장 앞선 `FAIL` 또는 그 이후 연속 `NOT_REACHED`를 First Failed Stage 후보로 삼는다.

---

## 5. Root Cause Categories

```text
RC-A SOURCE_ACCESS
RC-B LOG_DISCOVERY
RC-C DOWNLOAD
RC-D SDM_CONVERSION
RC-E BUILD_BINARY
RC-F SKILL_UNAVAILABLE
RC-G ANALYZER_INVOCATION
RC-H ANALYZER_TIMEOUT
RC-I ANALYZER_RESULT
RC-J PROVIDER_INFRA
RC-K PATH_PERMISSION
RC-L FALLBACK_FAILURE
RC-M FINAL_AGGREGATION
RC-N UNKNOWN
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

## 6. Analyzer 검사

실제 파일/로그에서 확인한다.

```text
Configured Default Analyzer
Target Override
Legacy analysis.skill
Selected Analyzer
Analyzer Preset
Analyzer Registry Entry
Preflight Status
Provider
Invocation Started
Return Code
Timeout
Result Contract
Fallback Target
Fallback Invoked
Fallback Result
```

특히 확인:

- 실제 선택된 Analyzer가 무엇인지
- 선택 후 preflight가 수행됐는지
- skill 존재/호출 가능 판정이 무엇인지
- provider/headless 환경에서 호출 가능한지
- invocation prompt/command가 생성됐는지
- timeout 전까지 진행 흔적이 있는지
- fallback이 실제 수행됐는지

---

## 7. 로그 획득 검사

`SOURCE_ACCESS`, `LOG_DISCOVERY`, `DOWNLOAD`, `로그획득실패` 관련이면 확인한다.

```text
Jira Read
Comment Read
Remote Link Read
Attachment Discovery
External Source Discovery
Selected Source
Download Attempt
Download Result
HTTP/Protocol Result
Output File Exists
File Size
File Extension
Original SDM Name
Acquisition Owner
```

다음을 구분한다.

```text
Jira 자체 접근 실패
≠ 로그 위치 탐색 실패
≠ 로그 URL 확보 후 다운로드 실패
≠ 다운로드 성공했지만 FLA가 파일을 못 찾음
≠ delegated analyzer가 직접 획득해야 하는데 호출 전 실패
```

---

## 8. SDM / QB / Binary 검사

확인:

```text
Original SDM Exists
Converted TXT Exists
Converter Invoked
Converter Return Code
QB Link Resolved
Build/Binary Found
Symbol Found
Required Binary Match
```

SDM 원본 미확보와 변환 실패를 같은 원인으로 묶지 않는다.

---

## 9. Provider / Timeout / Unattended 검사

확인:

- OpenCode / Claude Code / Qwen Code 중 실제 provider
- interactive / unattended
- subprocess 시작 여부
- stdout/stderr
- timeout 값
- retry 횟수
- process 종료 코드
- permission/user-context
- HOME/TEMP/LOCALAPPDATA 의존성
- 사용자 입력 대기 여부

---

# 10. 사용자 객관식 질문 Pool

아래 Q1~Q24는 **질문 Pool**일 뿐이다. Q1~Q24 전체를 사용자에게 한 번에 보여주지 않는다.

수행 순서:

```text
1. AI가 먼저 가능한 evidence를 자동 확인
2. 자동 확인된 질문 제거
3. First Failed Stage/Root Cause 분리에 필요한 질문만 선택
4. 최초 최대 10개만 사용자에게 제시
5. 사용자는 숫자 한 줄로 응답
6. AI가 evidence와 결합해 재분석
7. 꼭 필요한 경우에만 추가 최대 5개 질문
```

질문 우선순위는 `First Failed Stage 판별 > Root Cause 분리 > fallback/provider 구분 > 보조 확인`이다.

응답 예:

```text
1 0 2 1
```

설명형 답변을 요구하지 않는다.

### Q1. 분석 대상은 가장 최근 실패 Run인가?
`0=모름, 1=맞음, 2=아님`

### Q2. 실패가 모든 Jira에서 발생했는가?
`0=모름, 1=모두 실패, 2=일부만 실패`

### Q3. 실패 HTML에서 `로그획득실패`로 표시됐는가?
`0=모름, 1=맞음, 2=다른 상태`

### Q4. 실패 Jira의 로그 파일이 output 폴더에 실제 존재했는가?
`0=모름, 1=존재, 2=없음`

### Q5. Jira 본문/댓글 자체는 정상 조회됐는가?
`0=모름, 1=정상, 2=실패`

### Q6. Jira Remote Link까지 조회됐는가?
`0=모름, 1=정상, 2=실패, 3=Remote Link 없음`

### Q7. 로그 다운로드 시도 흔적이 있었는가?
`0=모름, 1=있음, 2=없음`

### Q8. 다운로드 실패 코드가 확인됐는가?
`0=모름, 1=403/권한, 2=404/경로, 3=timeout/network, 4=기타 코드`

### Q9. 원본 SDM은 확보됐는가?
`0=모름, 1=있음, 2=없음, 3=SDM 대상 아님`

### Q10. SDM→TXT 변환 결과가 생성됐는가?
`0=모름, 1=생성, 2=실패, 3=변환 대상 아님`

### Q11. QB/build/binary 정보는 확보됐는가?
`0=모름, 1=확보, 2=미확보, 3=필요 없는 로그`

### Q12. 실제 선택 Analyzer가 확인됐는가?
`0=모름, 1=l1-log-analysis, 2=issue-analyzer, 3=기타 Analyzer`

### Q13. Analyzer preflight 결과가 있었는가?
`0=모름, 1=AVAILABLE, 2=UNAVAILABLE, 3=preflight 없음`

### Q14. Analyzer invocation 흔적이 있었는가?
`0=모름, 1=있음, 2=없음`

### Q15. Analyzer process가 시작된 뒤 timeout됐는가?
`0=모름, 1=timeout, 2=timeout 아님, 3=process 미시작`

### Q16. Analyzer return code가 확인됐는가?
`0=모름, 1=0/정상, 2=non-zero, 3=return code 없음`

### Q17. Analyzer 결과 파일/contract가 생성됐는가?
`0=모름, 1=정상 생성, 2=생성됐지만 invalid, 3=미생성`

### Q18. Primary Analyzer 실패 후 fallback 흔적이 있었는가?
`0=모름, 1=실행됨, 2=실행 안 됨, 3=fallback 비활성`

### Q19. fallback Analyzer도 실패했는가?
`0=모름, 1=성공, 2=실패, 3=fallback 미실행`

### Q20. 실행 provider는 무엇이었는가?
`0=모름, 1=OpenCode, 2=Claude Code, 3=Qwen Code, 4=기타`

### Q21. 실행 OS는?
`0=모름, 1=Windows, 2=Linux`

### Q22. 실행 방식은?
`0=모름, 1=직접/interactive, 2=job-list 무인실행, 3=dispatcher/autotask 무인실행`

### Q23. 동일 실패가 반복되는가?
`0=모름, 1=반복, 2=1회성`

### Q24. Root Cause 확정 후 허용 범위는?
`0=진단만, 1=최소 수정안까지, 2=실제 L1-FLA 수정까지`

---

# 11. First Failure Principle

예:

```text
Jira access PASS
→ Remote Link PASS
→ Download FAIL
→ SDM NOT_REACHED
→ Analyzer NOT_REACHED

Primary Root Cause는 Analyzer가 아니라 DOWNLOAD/SOURCE 쪽이다.
```

또는:

```text
Log acquired PASS
→ SDM conversion PASS
→ Analyzer selected PASS
→ Preflight UNAVAILABLE
→ Invocation NOT_REACHED

Primary Root Cause는 SKILL_UNAVAILABLE이다.
```

또는:

```text
Preflight PASS
→ Invocation PASS
→ Process started
→ Timeout FAIL
→ Result NOT_REACHED

Primary Root Cause는 ANALYZER_TIMEOUT이다.
```

---

# 12. 최종 보고 형식

## A. Executive Summary

```text
Primary Root Cause:
First Failed Stage:
Actual Analyzer:
Fallback:
Confidence: HIGH / MEDIUM / LOW
```

## B. Pipeline Result

| Stage | Status | Evidence |
|---|---|---|
| Jira access | | |
| Source discovery | | |
| Download | | |
| SDM conversion | | |
| QB/Binary | | |
| Analyzer selection | | |
| Preflight | | |
| Invocation | | |
| Execution | | |
| Result | | |
| Final aggregation | | |

## C. Root Cause Ranking

| Rank | Category | Verdict | Evidence |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## D. Confirmed Non-Causes

실제 evidence로 배제된 것만 작성한다.

## E. Analyzer

```text
Configured Default:
Actual Selected:
Preset:
Preflight:
Provider:
Invocation:
Return Code:
Timeout:
Fallback:
```

## F. Source / Download

```text
Jira:
Remote Link:
Selected Source:
Download Attempt:
Download Result:
Local File:
```

## G. SDM / QB

```text
Original SDM:
Converted TXT:
QB:
Binary:
Symbol:
```

## H. Next Action

Q24 기준:

```text
0 → 진단 결과만 보고하고 STOP
1 → Primary Root Cause의 최소 수정 방향만 제시
2 → Root Cause와 직접 관련된 L1-FLA 수정까지 허용
```

원인과 무관한 리팩토링은 금지한다.

---

# 13. 성공 조건

1. 최초 실패 Gate 확인
2. Primary Root Cause 최소 1개 확정 또는 evidence 부족 명시
3. 로그 획득 문제와 Analyzer 문제 분리
4. SDM/QB 문제와 source/download 문제 분리
5. 실제 Analyzer selection 확인
6. preflight/invocation/timeout 구분
7. fallback 실제 수행 여부 확인
8. provider/OS/unattended 영향 확인
9. 미확인 가설은 가설로 유지
10. 다음 복구 대상 component를 정확히 특정

---

# 14. 최종 실행 지시

1. 먼저 가능한 evidence를 **read-only**로 자동 수집한다.
2. Q1~Q24 전체를 사용자에게 보여주지 않는다.
3. 자동 확인 불가능하면서 Root Cause 판별에 꼭 필요한 질문만 고른다.
4. 최초 질문은 **최대 10개**만 제시한다.
5. 사용자는 숫자 한 줄로만 응답한다.
6. 응답 후 AI가 다시 evidence를 분석한다.
7. 추가 확인이 반드시 필요하면 **최대 5개** 숫자 질문만 한 번 더 제시한다.
8. 충분한 evidence가 확보되면 추가 질문 없이 First Failed Stage를 결정한다.
9. Root Cause를 최대 3개까지 우선순위화한다.
10. Q24 범위에 맞춰 STOP/최소수정안/실제수정 단계로 이동한다.

사용자에게 다음을 요구하지 않는다.

```text
긴 설명
로그 내용 복사
경로 직접 입력
Jira 번호 직접 입력
버전 문자열 직접 입력
명령어 결과 직접 입력
실패 상황 자유서술
```

필요한 정보는 가능한 한 AI가 직접 찾는다.

**Root Cause 분석이 끝나기 전에는 component를 수정하지 않는다.**

---

# 15. 실제 사용자 Interaction 예시

좋은 예:

```text
자동 확인 결과:
- 최신 실패 Run 발견
- Jira 접근 PASS
- 원본 로그 파일 미확보
- Analyzer selection은 l1-log-analysis
- Analyzer invocation은 NOT_REACHED

추가로 3개만 확인하면 됩니다. 모르면 0으로 답해주세요.

Q1. 동일 실패가 반복되는가?
0=모름, 1=반복, 2=1회성

Q2. 실행 방식은?
0=모름, 1=직접 실행, 2=job-list 무인실행, 3=dispatcher/autotask 무인실행

Q3. Root Cause 확정 후 허용 범위는?
0=진단만, 1=최소 수정안, 2=실제 L1-FLA 수정

답변 예:
1 2 1
```

나쁜 예:

```text
실패한 Jira 번호를 알려주세요.
로그 경로를 입력해주세요.
어떤 에러가 났는지 설명해주세요.
현재 사용한 Analyzer가 무엇인지 알려주세요.
추가 정보를 제공해주세요.
```

위 방식은 사용하지 않는다.
