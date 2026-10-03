# L1-FLA 정상동작 실패 Root Cause Deep-Dive Prompt — 숫자 객관식 최소입력형

- Version: v1.0
- Date: 2026-10-03 KST
- 대상 기준: L1-FLA v0.3.34
- 목적: L1-FLA 전체 실행 체인을 실제 증거로 추적하여 **First Failed Stage와 Primary Root Cause를 확정**
- 사용자 응답 방식: **숫자 객관식만**
- 최초 질문: 최대 10개
- 추가 질문: 한 번에 최대 5개
- 수정 정책: **Root Cause 확정 전 수정 금지**

---

## 사용자 Interaction 최우선 규칙

이 규칙은 모든 진단 규칙보다 우선한다.

1. 자동 확인 가능한 항목은 사용자에게 묻지 않는다.
2. 설치 상태, route, action, profile, status, Analyzer, Jira 환경, 최근 Run, result/report를 먼저 read-only로 조사한다.
3. 자동 조사 후에도 Root Cause 분리에 필요한 항목만 질문한다.
4. 모든 질문은 `0/1/2/3/...` 숫자 선택식이다.
5. 사용자는 공백으로 구분한 숫자 한 줄만 입력한다.
6. 모든 질문에 `0=모름/미확인`을 둔다.
7. 사용자에게 경로, Jira 번호, 로그 문장, 버전 문자열, 명령 출력, 에러 문자열을 직접 입력하게 하지 않는다.
8. 이미 evidence로 확인한 내용은 다시 묻지 않는다.
9. 자유서술 질문을 만들지 않는다.
10. evidence가 부족하면 질문을 남발하지 말고 `INSUFFICIENT_EVIDENCE`로 남긴다.
11. 숫자 선택지가 없는 질문 문장이 하나라도 있으면 응답을 다시 작성한다.

질문이 필요할 때는 반드시 아래 형식만 사용한다.

```text
자동으로 확인할 수 있는 항목은 먼저 확인했습니다.
Root Cause 확정을 위해 아래 N개만 숫자로 답해주세요. 모르면 0입니다.

Q1. ...
0=모름, 1=..., 2=...

Q2. ...
0=모름, 1=..., 2=...

답변 예:
1 0 2 3
```

다음과 같은 질문은 금지한다.

```text
어떤 문제가 발생하나요?
에러 메시지를 알려주세요.
경로를 알려주세요.
로그를 복사해주세요.
실패한 Jira 번호를 입력해주세요.
현재 설정을 설명해주세요.
```

---

# 0. v0.3.34 정상 Baseline

아래는 기대값이며 **실제 설치본에서 반드시 재검증**한다.

### Canonical route

```text
skillsilent run l1-fla route -- --request "<사용자 원문 요청>" --json
```

기대 흐름:

```text
Natural Language
→ route 1회
→ ROUTED
→ registered action 1개
→ canonical skillsilent run
→ result
```

Agent가 canonical workflow를 우회해 내부 Python script를 직접 실행하면 안 된다.

### 기본 Analyzer

```text
Preset ID : l1log
Skill     : l1-log-analysis
```

Analyzer 선택 우선순위:

```text
Target analyzer_id
→ profile analysis.default_analyzer
→ legacy analysis.skill
```

### 상태 확인

다음 요청은 read-only `status`로 route되어야 한다.

```text
FLA 상태 확인해줘
어떤 분석 스킬 사용해?
except 설정 확인해줘
fallback 설정 보여줘
```

기대 schema:

```text
l1-fla-status/2
```

### 설정 변경

전용 action:

```text
set-default-analyzer
set-analyzer-fallback
set-except
model-setup
```

설정 변경은 persistent profile만 수정하고 분석을 자동 실행하지 않는다.

### 실패 진단

```text
diagnose-failure
```

실패 원인 요청은 일반 `run`이 아니라 read-only 진단으로 route되어야 한다.

### Local Environment SSOT

```text
~/l1sw-local-environment/l1-fla/jira/jira_access.json
~/l1sw-local-environment/l1-fla/repositories/log_repositories.json
~/l1sw-local-environment/l1-fla/secrets/repository_credentials.json
```

확인:

```text
skillsilent run l1-fla environment-status -- --json
skillsilent run l1-fla jira-access-status -- --json
```

---

# 1. 전체 실행 체인

이번 단계에서는 수정하지 않는다.

가장 먼저 깨지는 Gate를 찾는다.

```text
[0] Skill discovery / installed version
→ [1] skillsilent registration / public action
→ [2] Natural-language route
→ [3] Action registry / policy / argument hints
→ [4] Persistent profile load / migration
→ [5] status / config visibility
→ [6] Target / Jira input resolution
→ [7] Except / skip evaluation
→ [8] Jira provider / Local Environment SSOT
→ [9] Jira / Remote Link / source discovery
→ [10] Log acquisition / download
→ [11] SDM / QB / Binary preparation
→ [12] Analyzer selection
→ [13] Analyzer availability / preflight
→ [14] Provider / headless invocation
→ [15] Analyzer execution
→ [16] Analyzer result contract
→ [17] Escalation / fallback
→ [18] Per-Jira result persistence
→ [19] final_report aggregation / render
→ [20] observer / exit status
→ [21] unattended / scheduler path
```

판정은 아래 4개만 사용한다.

```text
PRIMARY_ROOT_CAUSE
CONTRIBUTING_FACTOR
NOT_CAUSE
INSUFFICIENT_EVIDENCE
```

---

# 2. 진단 절대 원칙

1. 추측으로 확정하지 않는다.
2. 후행 증상보다 **First Failed Stage**를 우선한다.
3. HTML 문구 하나만 보고 원인을 결정하지 않는다.
4. Analyzer 이름이 config에 있다는 이유만으로 실제 호출 가능하다고 판단하지 않는다.
5. 문서상 기본이 `l1-log-analysis`라는 이유만으로 현재 profile도 같다고 가정하지 않는다.
6. fallback 설정과 실제 fallback 실행을 구분한다.
7. 로그 획득 실패와 Analyzer 실패를 분리한다.
8. route 실패와 action implementation 실패를 분리한다.
9. status 실패와 일반 run 실패를 분리한다.
10. shipped default와 기존 persistent profile override를 분리한다.
11. interactive와 unattended를 분리한다.
12. Windows/Linux 차이를 분리한다.
13. 등록 action 실패를 임의 interpreter 실행으로 우회해 성공으로 판정하지 않는다.
14. Root Cause 확정 전 설정 reset/reinstall/refactoring 금지.

---

# 3. 자동 조사 — 사용자에게 질문하기 전에 수행

## 3.1 설치 / Discovery

확인:

```text
~/.claude/skills/l1-fla/SKILL.md
~/l1sw-private-skills/l1-fla/
```

기록:

- Discovery SKILL 존재/버전
- canonical root 존재/버전
- runtime version
- discovery와 canonical version mismatch
- duplicate/stale installation
- Windows/Linux 설치본 차이
- partial update 정황

## 3.2 skillsilent / Public action

확인:

- skillsilent 실행 가능
- l1-fla 등록 여부
- `route`
- `status`
- `run`
- `diagnose-failure`
- `environment-status`
- `jira-access-status`
- `list-analyzers`
- `set-default-analyzer`
- `set-analyzer-fallback`
- `set-except`

action/policy/registry mismatch를 확인한다.

## 3.3 현재 운영 상태

가능하면 canonical action으로:

```text
skillsilent run l1-fla status -- --detail --json
skillsilent run l1-fla environment-status -- --json
skillsilent run l1-fla jira-access-status -- --json
skillsilent run l1-fla list-analyzers -- --json
```

실패해도 stdout/stderr/exit code를 evidence로 보존한다.

## 3.4 최근 Run

자동으로 찾는다.

- 최신 실패 Run
- 최신 성공 Run
- 마지막 정상 버전
- 최초 비정상 버전
- `run_state.json`
- Jira별 `result.json`
- `observer_result.json`
- `final_report.md`
- `final_report.html`
- Analyzer/preflight/result log
- stdout/stderr

## 3.5 실행 환경

확인:

- OS
- OpenCode / Claude Code / Qwen Code
- interactive / unattended
- HOME
- private root
- local environment root
- executable absolute path
- permission
- stale lock
- concurrent run

---

# 4. Master Evidence Matrix

반드시 작성한다.

| Gate | Expected | Evidence | Status | First Failure? |
|---|---|---|---|---|
| Skill discovery | SKILL 발견 | | | |
| Version consistency | discovery/runtime 일치 | | | |
| skillsilent registration | l1-fla 등록 | | | |
| route | route 실행 가능 | | | |
| NL mapping | 올바른 action | | | |
| action policy | action 허용 | | | |
| profile load | 정상 | | | |
| status | l1-fla-status/2 | | | |
| Analyzer registry | 정상 | | | |
| default Analyzer | l1log/l1-log-analysis 또는 사용자 설정 | | | |
| except | 정상 | | | |
| Jira SSOT | 정상 | | | |
| Jira access | 정상 | | | |
| source discovery | 정상 | | | |
| download | 정상 | | | |
| SDM/QB | 필요 시 정상 | | | |
| Analyzer selection | 정상 | | | |
| preflight | 정상 | | | |
| provider invocation | process 시작 | | | |
| Analyzer result | contract 정상 | | | |
| fallback/escalation | 정책대로 | | | |
| per-Jira result | 저장 | | | |
| final_report | MD/HTML 생성 | | | |
| observer | 일치 | | | |
| unattended | 해당 시 정상 | | | |

Status:

```text
PASS / FAIL / NOT_REACHED / UNKNOWN / N/A
```

가장 앞선 `FAIL`과 이후 `NOT_REACHED`를 우선 분석한다.

---

# 5. Gate A — 설치 / 버전 / Discovery

확인:

```text
Discovery SKILL path/version
Canonical root/version
Runtime code version
Latest release note
Duplicate skill roots
Stale extracted package
Partial update
```

후보:

```text
RC-A1 Discovery stale
RC-A2 Canonical runtime stale
RC-A3 Partial update
RC-A4 Duplicate installation shadowing
RC-A5 Windows/Linux version mismatch
RC-A6 Migration/install failure
```

특히 `SKILL.md만 최신이고 runtime code가 구버전`인지 확인한다.

---

# 6. Gate B — Natural Language → route

아래 representative request를 route probe한다.

```text
FLA 상태 확인해줘
어떤 분석 스킬 사용해?
except 설정 확인해줘
SOC-123 분석해줘
FLA 로그분석 실패 원인 분석해줘
기본 분석 스킬을 issue-analyzer로 바꿔
```

기대:

| Request | Expected Action |
|---|---|
| 상태 확인 | status |
| 분석 스킬 확인 | status |
| except 확인 | status |
| Jira 분석 | run |
| 실패 원인 | diagnose-failure |
| Analyzer 변경 | set-default-analyzer |

확인:

```text
status
action/recommended_action
approval_required
usage
next_command_prefix
run_argument_hints
next_action
NEXT_COMMAND
```

후보:

```text
RC-B1 Route parser mismatch
RC-B2 low_spec_routes stale
RC-B3 policy/action registry mismatch
RC-B4 Korean intent phrase mismatch
RC-B5 query/change intent collision
RC-B6 compound request misrouting
RC-B7 argument hints missing
```

---

# 7. Gate C — status / persistent profile

`status --detail --json` 기대:

```text
schema = l1-fla-status/2
Version
Configured Default Analyzer
Fallback Analyzer
Registered Analyzers
Provider
Except title rules
Except status rules
Latest Run actual Analyzer
Latest fallback
Latest skip
```

구분:

- status action 자체 실패
- old schema 반환
- profile load 실패
- except 누락
- recent run parsing만 실패

후보:

```text
RC-C1 status action missing
RC-C2 stale status implementation
RC-C3 profile load failure
RC-C4 config migration failure
RC-C5 recent-run parser failure
RC-C6 except compatibility failure
```

---

# 8. Gate D — Analyzer Registry / Default / Fallback

반드시 기록:

```text
Configured preset:
Configured skill:
Expected default:
Actual selected preset:
Actual selected skill:
Fallback preset:
Fallback skill:
Selection reason:
```

v0.3.34 fresh baseline:

```text
l1log → l1-log-analysis
```

그러나 기존 persistent profile은 보존될 수 있으므로 실제 config 기준으로 판정한다.

확인:

- `l1log` preset 존재
- skill이 정확히 `l1-log-analysis`
- `issue` preset 존재
- `l1sw-log-analyzer`가 legacy preset으로만 남았는지
- fallback target이 실제 존재하는 preset인지
- stale target override
- legacy `analysis.skill` precedence 문제

후보:

```text
RC-D1 Default migration 미적용
RC-D2 Existing profile override
RC-D3 l1log registry missing
RC-D4 Preset wrong skill
RC-D5 Fallback missing
RC-D6 Target override stale
RC-D7 Legacy precedence bug
```

---

# 9. Gate E — Except / Skip

기본 status skip 기대:

```text
PENDING
VERIFICATION_REQUEST
```

확인:

- except overall enable
- title enable/pattern
- status enable/value
- legacy alias
- normalized matching
- 실제 Jira title/status
- `analysis_skipped`
- `skip_reason`
- matched_status / matched_keyword

`Jira 미분석 = Analyzer 실패`로 단정하지 않는다.

후보:

```text
RC-E1 Unintended except match
RC-E2 Except unexpectedly disabled
RC-E3 Legacy/new config collision
RC-E4 Normalization overmatch
RC-E5 Skip/report display mismatch
```

---

# 10. Gate F — Jira / Local Environment SSOT

확인:

```text
jira_access.json
provider
provider launcher
Remote Link config
log_repositories.json
credential reference
Windows/Linux command
```

후보:

```text
RC-F1 SSOT missing
RC-F2 Provider config stale
RC-F3 Mango MCP unavailable
RC-F4 OS command mismatch
RC-F5 Remote Link required but unavailable
RC-F6 Credential/reference issue
RC-F7 Old internal config incorrectly used
```

---

# 11. Gate G — Source discovery / Download

확인 source 후보:

```text
latest comment
older comments
description
ADF href
attachment
custom field
Remote Link
repository pattern
```

기록:

```text
Candidate count
Selected source
Acquisition owner
Download attempted
Protocol/result
Destination
Local file exists
File size
Original filename
```

반드시 구분:

```text
SOURCE_ACCESS
LOG_DISCOVERY
DOWNLOAD
```

후보:

```text
RC-G1 Source hint not detected
RC-G2 Remote Link failure
RC-G3 Repository mapping failure
RC-G4 Auth/permission
RC-G5 403/404
RC-G6 Network/timeout
RC-G7 Download succeeded but file not recognized
RC-G8 Destination permission
RC-G9 Delegated ownership mismatch
```

---

# 12. Gate H — SDM / QB / Binary

해당 시 확인:

```text
Original SDM
Converted TXT
Converter
Return code
QB link
Binary
Symbol
Compatibility
```

후보:

```text
RC-H1 SDM absent
RC-H2 Converter failure
RC-H3 parser/DMConsole problem
RC-H4 QB unresolved
RC-H5 Binary absent
RC-H6 Binary mismatch
```

---

# 13. Gate I — Analyzer Preflight / Availability

기본 `l1-log-analysis`에 대해 확인:

- selected Analyzer
- invocation type
- preflight 수행 여부
- headless provider에서 skill discovery 가능 여부
- AVAILABLE / UNAVAILABLE / INFRASTRUCTURE / BLOCKED
- fallback decision

기대 원칙:

```text
SKILL_UNAVAILABLE / INFRASTRUCTURE → fallback 가능
BLOCKED → pending 유지, 임의 Analyzer 변경 금지
```

후보:

```text
RC-I1 l1-log-analysis not installed
RC-I2 Installed but not discoverable
RC-I3 Preflight contract failure
RC-I4 Provider skill visibility mismatch
RC-I5 Fallback selection failure
RC-I6 BLOCKED misclassified
```

---

# 14. Gate J — Provider / Headless runtime

확인:

```text
Selected provider
Absolute executable
Fallback order
Process start
Return code
stdout/stderr
Timeout
Retry
Working directory
HOME
Environment
```

후보:

```text
RC-J1 Provider executable missing
RC-J2 Absolute path stale
RC-J3 PATH/user-context mismatch
RC-J4 Process start failure
RC-J5 Timeout
RC-J6 Prompt/tool availability mismatch
RC-J7 Unattended interactive wait
```

---

# 15. Gate K — Analyzer result contract

Delegated analyzer 기대 contract:

```text
l1-fla-delegated-result/1
```

Native issue-analyzer 관련:

```text
issue-analyzer-status/1
```

확인:

- schema
- status
- COMPLETE/BLOCKED/INFRASTRUCTURE/SKILL_UNAVAILABLE
- next_action
- summary
- limitations
- output refs
- malformed JSON
- exit 0 + invalid contract 여부

후보:

```text
RC-K1 Contract missing
RC-K2 Invalid JSON/schema
RC-K3 Exit/status mismatch
RC-K4 COMPLETE missing
RC-K5 Result parse failure
```

---

# 16. Gate L — Escalation / Fallback

확인:

```text
LLM_ANALYZE_CONTEXT
RUN_CODE_ANALYZER_ONCE
CONVERT_LOG_ONCE
SELECT_LOG_FILE
```

및:

- max escalation steps
- child availability
- actual child invocation
- finalize
- pending state
- primary failure kind
- fallback allowed 여부
- fallback target
- actual fallback result

후보:

```text
RC-L1 Escalation not executed
RC-L2 Child skill missing
RC-L3 Max steps exceeded
RC-L4 Wrong fallback condition
RC-L5 Fallback target unavailable
RC-L6 Evidence lost after fallback
```

---

# 17. Gate M — Persistence / Final HTML

확인:

```text
result.json
result_state
result_view
action_for
errors
skip_reason
Analyzer
Failure Stage
Failure Kind
Provider
Return Code
Timeout
Fallback
final_report.md
final_report.html
issue_detail.html
```

v0.3.32+ 기대:

- 실제 Analyzer 표시
- SOURCE_ACCESS를 로그획득실패로 구분
- provider/return code/timeout/fallback 보존
- Analyzer 실행 전 실패라도 analyzer_selection 보존 가능

후보:

```text
RC-M1 Runtime success but persistence failed
RC-M2 result incomplete
RC-M3 aggregation mismatch
RC-M4 stale HTML renderer
RC-M5 MD/HTML mismatch
RC-M6 error/skip reason lost
```

---

# 18. Gate N — Unattended / Scheduler

무인 실행 문제일 때만 본다.

정상 entrypoint:

```text
bin/l1-fla-auto.py run
```

확인:

```text
Scheduled command
Working directory
User
HOME
Executable
Profile resolution
Local environment resolution
Lock
stdout/stderr
Start/end
Exit code
observer_result
Interactive wait
```

후보:

```text
RC-N1 Wrong entrypoint
RC-N2 User context mismatch
RC-N3 HOME/profile missing
RC-N4 Provider unavailable unattended
RC-N5 Stale lock
RC-N6 Interactive wait
RC-N7 Scheduler timeout
```

---

# 19. 사용자 숫자 객관식 Question Pool

아래 Q1~Q36은 **질문 Pool**이다. 전부 보여주지 않는다.

먼저 자동 조사한 후 필요한 것만 고른다.

## Q1. 가장 큰 증상은?
`0=모름, 1=FLA 호출 안 됨, 2=route 이상, 3=status 이상, 4=분석 run 이상, 5=무인실행만 이상, 6=여러 기능 이상`

## Q2. v0.3.34 설치 후부터 문제인가?
`0=모름, 1=맞음, 2=이전부터, 3=처음 설치`

## Q3. 같은 PC의 이전 FLA는 정상 동작했는가?
`0=모름, 1=정상 이력 있음, 2=정상 이력 없음`

## Q4. OS는?
`0=모름, 1=Windows, 2=Linux, 3=둘 다`

## Q5. 실행 front는?
`0=모름, 1=OpenCode, 2=Claude Code, 3=Qwen Code, 4=기타`

## Q6. `FLA 상태 확인해줘` 결과는?
`0=미확인, 1=정상, 2=실패, 3=엉뚱한 action`

## Q7. `어떤 분석 스킬 사용해?` 결과는?
`0=미확인, 1=l1-log-analysis, 2=다른 Analyzer, 3=응답 실패`

## Q8. except 조회는?
`0=미확인, 1=정상, 2=누락/오류, 3=status 실패`

## Q9. Jira 분석 자연어 route는?
`0=미확인, 1=run 정상, 2=다른 action, 3=route 실패`

## Q10. 실패 원인 자연어 route는?
`0=미확인, 1=diagnose-failure 정상, 2=run으로 잘못 route, 3=route 실패`

## Q11. 설치 version은?
`0=모름, 1=v0.3.34, 2=v0.3.33 이하, 3=경로마다 다름`

## Q12. Discovery와 canonical runtime version은?
`0=모름, 1=일치, 2=불일치`

## Q13. skillsilent action 등록은?
`0=미확인, 1=정상, 2=l1-fla 없음, 3=일부 action 누락`

## Q14. 현재 default Analyzer는?
`0=모름, 1=l1-log-analysis, 2=issue-analyzer, 3=l1sw-log-analyzer, 4=기타/비어있음`

## Q15. `l1-log-analysis` 호출 가능 여부는?
`0=미확인, 1=가능, 2=불가, 3=설치 여부 불명`

## Q16. Analyzer preflight는?
`0=모름, 1=AVAILABLE, 2=UNAVAILABLE, 3=INFRASTRUCTURE, 4=BLOCKED, 5=없음`

## Q17. fallback 설정은?
`0=모름, 1=정상, 2=없음/비활성, 3=잘못된 preset`

## Q18. Jira provider status는?
`0=미확인, 1=정상, 2=실패, 3=설정 없음`

## Q19. Mango MCP Jira 조회는?
`0=미확인, 1=정상, 2=실패, 3=Mango 미사용`

## Q20. Jira 본문/댓글은 읽히는가?
`0=모름, 1=정상, 2=실패`

## Q21. 로그 source 후보는?
`0=모름, 1=정상 발견, 2=0건, 3=잘못된 source`

## Q22. 로그 다운로드는?
`0=모름, 1=성공, 2=시도 후 실패, 3=시도 자체 없음`

## Q23. 원본 SDM은?
`0=모름, 1=있음, 2=없음, 3=SDM 대상 아님`

## Q24. SDM 변환은?
`0=모름, 1=성공, 2=실패, 3=대상 아님`

## Q25. QB/Binary는?
`0=모름, 1=정상, 2=미확보, 3=불필요`

## Q26. Analyzer process는 시작됐는가?
`0=모름, 1=시작, 2=시작 못함`

## Q27. Analyzer 결과는?
`0=모름, 1=완료, 2=timeout, 3=non-zero, 4=contract invalid`

## Q28. fallback은 실제 실행됐는가?
`0=모름, 1=실행 성공, 2=실행 실패, 3=미실행, 4=불필요`

## Q29. Jira별 result.json은?
`0=모름, 1=정상, 2=미생성, 3=불완전`

## Q30. final_report.html은?
`0=모름, 1=정상, 2=미생성, 3=내용 오류`

## Q31. MD와 HTML은 일치하는가?
`0=모름, 1=일치, 2=불일치`

## Q32. interactive/unattended 영향은?
`0=모름, 1=둘 다 문제, 2=interactive만, 3=unattended만`

## Q33. OS 영향은?
`0=모름, 1=Windows만, 2=Linux만, 3=둘 다`

## Q34. 재현성은?
`0=모름, 1=항상, 2=간헐적, 3=1회성`

## Q35. 최근 정상 Run은?
`0=모름, 1=있음, 2=없음`

## Q36. Root Cause 확정 후 진행 범위는?
`0=진단만, 1=P0 수정안 상세검토, 2=실제 L1-FLA 수정, 3=재현/검증, 4=다른 실패 Jira 비교, 5=모름, 6=NEXT`

---

# 20. Root Cause Categories

```text
RC-A Installation / Discovery / Version
RC-B skillsilent Registration / Route
RC-C Status / Operational UX
RC-D Persistent Profile / Analyzer Registry
RC-E Except / Skip
RC-F Jira Provider / Local Environment SSOT
RC-G Source Discovery / Download
RC-H SDM / QB / Binary
RC-I Analyzer Availability / Preflight
RC-J Provider / Headless Runtime
RC-K Analyzer Result Contract
RC-L Escalation / Fallback
RC-M Result Persistence / Report
RC-N Unattended / Scheduler
RC-O Concurrency / Lock / State
RC-P Unknown
```

각 category:

```text
PRIMARY_ROOT_CAUSE
CONTRIBUTING_FACTOR
NOT_CAUSE
INSUFFICIENT_EVIDENCE
```

최대 3개까지만 ranking한다.

---

# 21. Root Cause Confidence

## HIGH
- 독립적인 직접 evidence 2개 이상 일치, 또는
- First Failed Stage의 explicit error와 후행 NOT_REACHED 일치, 또는
- Last Known Good와 Failing Run diff가 원인을 직접 특정

## MEDIUM
- 직접 evidence 1개 + 정황 evidence 일치

## LOW
- 핵심 로그 부재 또는 evidence 상충

LOW에서는 실제 수정하지 않는다.

---

# 22. Last Known Good 비교

최근 정상 Run이 있으면 반드시 비교한다.

| 항목 | Last Known Good | Failing |
|---|---|---|
| L1-FLA version | | |
| Discovery path | | |
| Profile | | |
| Default Analyzer | | |
| Fallback | | |
| Except | | |
| Provider | | |
| Jira provider | | |
| Source | | |
| Preflight | | |
| Analyzer | | |
| Return code | | |
| Result schema | | |
| final_report | | |

`무엇이 바뀐 직후부터 실패했는가`를 핵심 evidence로 사용한다.

---

# 23. 최종 보고 형식

## A. Executive Summary

```text
L1-FLA Version:
Primary Root Cause:
First Failed Stage:
Affected Scenario:
Actual Analyzer:
Provider:
Confidence: HIGH / MEDIUM / LOW
```

## B. First Failure

```text
Last PASS:
First FAIL:
Following NOT_REACHED:
```

## C. Evidence Matrix
Master Evidence Matrix를 요약한다.

## D. Root Cause Ranking

| Rank | Category | Verdict | Evidence |
|---|---|---|---|
| 1 | | PRIMARY_ROOT_CAUSE | |
| 2 | | | |
| 3 | | | |

## E. Confirmed Non-Causes
실제 evidence로 배제된 항목만 쓴다.

## F. Expected vs Actual

```text
Expected:
Actual:
Mismatch:
```

## G. Minimal P0 Direction

실제 수정 없이:

```text
P0 Target Component:
P0 Change Scope:
Regression Risk:
Required Validation:
```

## H. Evidence Gaps

```text
INSUFFICIENT_EVIDENCE:
- ...
```

---

# 24. 최종 NEXT ACTION — 반드시 숫자 객관식

분석 완료 후 반드시 아래 메뉴로 끝낸다.

```text
[NEXT ACTION]

0 : 진단만 종료
1 : P0 수정안 상세검토
2 : 실제 L1-FLA 수정
3 : 동일 실패 재현/검증 절차 작성
4 : 다른 실패 Jira 비교 분석
5 : 모름 / 판단 보류
6 : NEXT — 분석 결과 기준 안전한 다음 단계 진행

답변 예:
1
```

`6=NEXT` 규칙:

- HIGH confidence이나 재현 검증 필요 → 3
- HIGH confidence이고 수정 전 설계 검토 필요 → 1
- 여러 Jira 비교가 Root Cause 확정에 중요 → 4
- **사용자가 명시적으로 2를 선택하지 않으면 실제 수정 금지**

---

# 25. 좋은 Interaction 예시

```text
자동으로 확인할 수 있는 항목은 먼저 확인했습니다.

확인 결과:
- Discovery SKILL: v0.3.34
- Canonical runtime: v0.3.33
- route action 존재
- status는 old schema 반환
- run은 profile 단계 이전에 종료

Root Cause 확정을 위해 아래 3개만 숫자로 답해주세요. 모르면 0입니다.

Q1. v0.3.34 설치 직후부터 문제가 시작됐는가?
0=모름, 1=맞음, 2=이전부터

Q2. 같은 PC에서 v0.3.33은 정상 동작했는가?
0=모름, 1=정상, 2=비정상

Q3. Root Cause 확정 후 진행 범위는?
0=진단만, 1=P0 상세검토, 2=실제 수정, 3=재현검증, 4=다른 Jira 비교, 5=모름, 6=NEXT

답변 예:
1 1 1
```

---

# 26. 금지 예시

```text
현재 어떤 문제가 발생하나요?
에러 메시지를 보내주세요.
설치 경로를 입력해주세요.
로그를 복사해주세요.
Analyzer 이름을 알려주세요.
설정을 자세히 설명해주세요.
```

또한 금지:

- Q1~Q36 전체를 한 번에 제시
- 자동 확인 가능한 것을 재질문
- Root Cause 확정 전 수정
- route/action 실패를 내부 Python 직접 실행으로 우회
- 최종 HTML 한 줄만 보고 Root Cause 확정

---

# 27. 최종 실행 지시

지금부터 현재 PC의 L1-FLA 정상동작 실패를 딥다이브한다.

1. 설치/Discovery/version을 read-only로 확인한다.
2. skillsilent registration과 public action을 확인한다.
3. 대표 자연어 요청의 route를 probe한다.
4. status/environment/Jira access/analyzer registry를 확인한다.
5. 최신 실패 Run과 최근 정상 Run을 찾아 비교한다.
6. Master Evidence Matrix를 채운다.
7. 가장 앞선 FAIL을 First Failed Stage로 지정한다.
8. 후행 오류를 Root Cause로 오판하지 않는다.
9. 필요한 사용자 정보만 숫자 객관식으로 질문한다.
10. 최초 최대 10개, 추가 최대 5개만 질문한다.
11. Root Cause를 최대 3개까지 ranking한다.
12. confidence를 HIGH/MEDIUM/LOW로 표시한다.
13. 실제 수정은 사용자가 최종 메뉴에서 `2`를 명시적으로 선택하기 전까지 금지한다.
14. 분석 완료 후 반드시 `[NEXT ACTION]` 숫자 메뉴로 끝낸다.

**사용자에게 주관식 입력을 요구하지 않는다.**
