# Job-list v0.4.6 S8/R16 + TLS Dual-Failure 추가 Deep-Dive 진단 프롬프트

- 작성 시각: **2026-10-03 14:28 KST**
- 대상: 사내 Windows PC
- 대상 패키지: `job-list v0.4.6`
- 목적: 1차 진단에서 이미 확인된 **S8 Scheduler 검증 실패(R16)** 와 **외부 signal TLS 실패**를 분리하여, v0.4.7 수정 전에 실제 Root Cause를 코드/로컬 증거 기반으로 확정한다.
- 작업 모드: **진단 전용 / 수정 금지 / 삭제 금지 / 재등록 금지**
- 사용자 입력 원칙: **객관식 우선, 주관식은 한두 단어 또는 한 줄만**

---

# 0. 이미 확정된 1차 진단 결과

아래 사실은 다시 사용자에게 질문하지 말고 **고정 입력**으로 사용한다.

```text
ROOT_CAUSE_1ST = R16
CONFIDENCE = 1
FIRST_FAIL_STAGE = S8
LOCAL_EXECUTION = 2
SIGNAL_TRANSPORT = 2
RETRYABLE_SAME_V0406 = 2
```

확인된 증거:

```text
E1.
V0406 activation/queue 정상 도달
queue: 10:06:03
worker spawned: pid=75832
processed terminal:
  returncode=1
  state=consumed
  time=10:07:49

E2.
latest_result.json:
  scheduler_after.valid=false
  enabled=""
  logon_type=InteractiveToken
  warning/error:
    SCHEDULER_NOT_VERIFIED
    "Could not establish an enabled :15/:45 PT30M dispatcher schedule ..."

E3.
외부 signal GET:
  external_signal_v0406_activation.ok=false
  terminal_signal.ok=false
  error:
    CERTIFICATE_VERIFY_FAILED
    "basic constraints of CA cert not marked critical"
```

따라서 이번 진단에서는 아래를 다시 검증하는 데 시간을 쓰지 않는다.

- Skill-Updater가 V0406을 전혀 실행하지 않았다는 가설
- V0406가 queue에 진입하지 않았다는 가설
- worker가 spawn되지 않았다는 가설
- v0.4.6 파일 자체가 설치되지 않았다는 가설

이번 포커스는 정확히 두 축이다.

```text
AXIS-A = S8 Scheduler 검증 실패의 실제 원인
AXIS-B = 외부 signal TLS transport 실패의 실제 원인
```

---

# 1. 사용자 응답 규칙

## 1.1 가능한 것은 직접 확인

사내 PC의 파일, JSON, Python, PowerShell, Scheduler 상태를 읽을 수 있으면 **사용자에게 묻지 말고 직접 확인**한다.

## 1.2 질문은 객관식

질문이 필요하면 한 번에 최대 8개.

사용자는 아래처럼 숫자만 답할 수 있어야 한다.

```text
1 2 1 3 0 1
```

공통 선택지:

```text
0 = 확인 불가 / 모름
1 = Yes / 있음 / 일치
2 = No / 없음 / 불일치
3 = 해당 없음
```

## 1.3 주관식은 최소 단답만

허용 예:

```text
E1=Ready
E2=0
E3=Python313
E4=dispatcher_autotask_register_windows_job.py:215
```

금지:

- 긴 로그 복사 요청
- JSON 전체 붙여넣기
- traceback 전체 요청
- 여러 줄 설명 요구

파일의 특정 값이 필요하면 직접 파싱한다.

---

# 2. 절대 금지

이번 단계에서는 아래 작업을 하지 않는다.

- Scheduler Task 삭제
- Scheduler Task 재등록
- `/Run`으로 Dispatcher 강제 실행
- Job-list queue/history 삭제
- `processed.jsonl` 수정/삭제
- V0406 state 초기화
- Skill-Updater 재설치
- Job-list 재설치
- TLS verify 강제 OFF 변경
- 인증서 설치/삭제
- 코드 수정
- v0.4.7 패키지 생성

**목표는 원인 확정과 수정 명세 작성까지다.**

---

# 3. 핵심 코드 위치

우선 canonical Job-list root에서 아래 파일을 직접 찾는다.

```text
scripts/dispatcher_autotask_register_windows_job.py
scripts/job_core.py
bootstrap/payload/skill-updater/scripts/skill_updater.py
bootstrap/payload/skill-updater/tests/test_v058_tls_profile.py
```

전체 디스크 recursive search 금지.

---

# 4. Axis-A — S8 Scheduler Failure Deep Dive

## A1. scheduler_query_xml() 판정식 확인

`dispatcher_autotask_register_windows_job.py`의 `scheduler_query_xml()`을 읽어 아래 조건을 확인한다.

v0.4.6 기준 핵심 판정은 다음 형태다.

```python
exact = (
    interval == "PT30M"
    and minute in (15, 45)
    and enabled == "true"
    and "--scheduled" in arguments
    and runner_ok
    and yaml_ok
)
```

확인 항목:

```text
A1-1 interval == PT30M
A1-2 minute == 15 or 45
A1-3 enabled == "true"
A1-4 --scheduled 존재
A1-5 windows_task_runner.py 존재
A1-6 canonical YAML match
```

결과를 내부적으로 아래 형식으로 기록한다.

```text
A1 = [1,1,2,1,1,1]
```

사용자에게 묻지 않는다.

---

## A2. `enabled=""`의 의미를 실제 Scheduler 상태로 분리

중요:

```text
enabled="" != 즉시 Disabled 확정
```

다음 두 상태를 반드시 구분한다.

```text
CASE-A = Task 자체가 실제 Disabled
CASE-B = Task는 Enabled/Ready인데 XML <Enabled> text가 비어 있거나 누락되어 parser가 "" 반환
```

읽기 전용 PowerShell로 확인:

```powershell
$task = Get-ScheduledTask -TaskName "autotask-dispatcher_observer" -ErrorAction SilentlyContinue
$info = Get-ScheduledTaskInfo -TaskName "autotask-dispatcher_observer" -ErrorAction SilentlyContinue
```

필요 값만 수집:

```text
Task.State
Task.Settings.Enabled
Task.Principal.UserId
Task.Principal.LogonType
Task.Principal.RunLevel
Info.LastTaskResult
Info.LastRunTime
Info.NextRunTime
```

또한:

```text
schtasks.exe /Query /TN "autotask-dispatcher_observer" /XML
```

에서 다음만 확인:

```text
<Enabled> 존재 여부
<Enabled> text
<Interval>
<StartBoundary>
<UserId>
<LogonType>
<RunLevel>
<Command>
<Arguments>
```

### A2 판정 코드

```text
A2-1 = ACTUAL_DISABLED
A2-2 = READY_BUT_XML_ENABLED_EMPTY
A2-3 = RUNNING_BUT_XML_ENABLED_EMPTY
A2-4 = ENABLED_TRUE_BUT_OTHER_VALIDATION_FAILED
A2-5 = TASK_MISSING
A2-6 = QUERY_INCONSISTENT
```

**A2-2 또는 A2-3이면 `scheduler_query_xml()` false-negative 가능성을 P0로 올린다.**

---

## A3. XML parser 자체 문제인지 확인

`local_xml_text(root, "Enabled")`가 `<Enabled>`를 어디서 가져오는지 확인한다.

다음 중 하나로 분류:

```text
1 = <Settings><Enabled>true</Enabled> 정상 발견
2 = <Enabled> element 자체 없음
3 = element는 있으나 text empty
4 = 다른 namespace/element 충돌 가능
5 = XML parse 결과 자체 이상
```

특히 `<Enabled>`가 XML에서 실제로 없는데 Windows Scheduler 상태가 Ready/Enabled이면:

```text
S8_SUBROOT = XML_OPTIONAL_FIELD_FALSE_NEGATIVE
```

로 기록한다.

---

## A4. `scheduler_task_info()`와 `scheduler_query_xml()`의 불일치 확인

코드에서 `scheduler_task_info()`가 이미 PowerShell JSON을 통해 다음을 얻는지 확인:

```text
State
LastTaskResult
NextRunTime
UserId
LogonType
```

그 뒤 **최종 scheduler.valid 계산에 이 정보가 사용되는지** 확인한다.

분류:

```text
1 = PowerShell evidence가 valid 판정에 사용됨
2 = 수집만 하고 valid 판정에는 사용하지 않음
3 = 일부만 사용
0 = 확인 불가
```

`2`이면 다음 후보를 기록:

```text
DEFECT_A = DUAL_READBACK_NOT_RECONCILED
SEVERITY = P0
```

---

## A5. 실제 등록 성공 여부를 독립적으로 판정

아래 조건을 코드의 `valid`와 별도로 계산한다.

```text
TASK_EXISTS
AND State in {Ready, Running, Queued}
AND Settings.Enabled != false
AND Interval == PT30M
AND start minute in {15,45}
AND canonical runner/arguments match
AND NextRunTime is present or task is Running
```

결과:

```text
A5-1 = INDEPENDENTLY_VALID
A5-2 = INDEPENDENTLY_INVALID
A5-3 = PARTIAL
```

만약:

```text
scheduler_after.valid = false
A5 = INDEPENDENTLY_VALID
```

이면 최종:

```text
S8_ROOT_A = VALIDATION_FALSE_NEGATIVE
```

---

# 5. Axis-A2 — InteractiveToken은 Root Cause인가 Secondary Risk인가

## A6. 현재 Dispatcher Task principal 확인

현재 값:

```text
LogonType = InteractiveToken
```

이 사실만으로 Root Cause로 확정하지 않는다.

다음을 확인:

```text
Task.State
LastTaskResult
NextRunTime
현재 PC 로그인 세션 존재 여부
Skill-Updater task의 LogonType
Skill-Updater task의 LastTaskResult
```

---

## A7. 정상 동작 중인 Skill-Updater Task와 비교

자동으로 Windows Scheduled Task 중 **Skill-Updater로 식별 가능한 정확한 Task**만 확인한다.

전체 Task를 사용자에게 나열하지 말 것.

비교 표 내부 생성:

| Field | Dispatcher | Skill-Updater |
|---|---|---|
| UserId |  |  |
| LogonType |  |  |
| RunLevel |  |  |
| State |  |  |
| LastTaskResult |  |  |
| NextRunTime |  |  |

분류:

```text
A7-1 = PRINCIPAL_MATCH
A7-2 = LOGON_TYPE_DIFF
A7-3 = USER_DIFF
A7-4 = MULTIPLE_DIFF
A7-5 = WORKING_UPDATER_NOT_FOUND
```

### 판정 원칙

```text
InteractiveToken + Ready + NextRunTime 정상
=> 즉시 Scheduler 등록 실패 Root Cause로 보지 않음

InteractiveToken + 로그오프 환경에서 실행 불가 증거
=> SECONDARY_RISK 또는 EXECUTION_ROOT_CAUSE 후보

현재 실패가 Scheduler "valid=false" 단계에서 /Run 이전 발생
=> InteractiveToken은 우선 S8 최초 실패의 직접 원인으로 두지 않음
```

---

# 6. Axis-A3 — bounded recovery가 왜 실패했는지 확인

## A8. deploy attempt 별 readback

`latest_result.json`에서 각 deploy attempt를 추출한다.

최대 다음 필드만:

```text
attempt number
deploy returncode
scheduler.exists
scheduler.valid
interval
start_minute
enabled
runner_ok
yaml_ok
logon_type
```

내부적으로 아래처럼 요약:

```text
A8:
1 rc=0 valid=0 enabled=""
2 rc=0 valid=0 enabled=""
```

사용자에게 전체 JSON을 요구하지 않는다.

분류:

```text
1 = deploy 자체 실패
2 = deploy rc=0이나 동일 readback false 반복
3 = 1차 실패 후 recovery action이 잘못됨
4 = LLM recovery가 STOP/MARK_DEGRADED
5 = 기타
```

`2`이면 `enabled=""` false-negative 가능성이 더 강해진다.

---

# 7. Axis-B — TLS Signal Transport Deep Dive

## B1. Job-list signal 구현 확인

`job_core.py`의 `emit_dispatcher_recovery_signal()`을 읽는다.

v0.4.6에서 아래 구조인지 확인:

```python
urllib.request.Request(...)
urllib.request.urlopen(...)
```

그리고 별도 `ssl.SSLContext`, custom CA, updater network profile을 직접 전달하는지 확인한다.

분류:

```text
B1-1 = plain urllib only
B1-2 = custom CA context 있음
B1-3 = updater transport 재사용
B1-4 = 기타
```

---

## B2. Skill-Updater의 GitHub transport와 비교

Embedded `skill_updater.py`에서 아래 기능 존재 여부를 직접 확인한다.

```text
_ssl_context()
_open_url()
network.ca_bundle
network.ca_bundle_env
SSL_CERT_FILE
persisted network profile
certificate failure detection
insecure fallback policy
```

특히 확인:

```text
Skill-Updater는 certificate verify failure 발생 시
환경/설정에 따라 별도 fallback 또는 remembered network profile을 사용할 수 있는가?
```

분류:

```text
B2-1 = Updater와 Job-list signal transport 동일
B2-2 = Updater가 더 강한 TLS/proxy recovery 보유
B2-3 = Job-list가 더 강함
B2-4 = 판단 불가
```

`B2-2`이면:

```text
TLS_SUBROOT = TRANSPORT_POLICY_DIVERGENCE
```

후보로 올린다.

---

## B3. Skill-Updater가 실제 어떤 TLS profile로 성공했는지 확인

allowlist 내에서만 다음을 확인한다.

예상 후보:

```text
%USERPROFILE%\l1sw-private-skills\skill-updater\data\
%USERPROFILE%\l1sw-private-skills\skill-updater\data\config\
%USERPROFILE%\l1sw-private-skills\skill-updater\data\state\
%USERPROFILE%\l1sw-private-skills\autotask-builder\data\environment\skill-updater.env
%USERPROFILE%\l1sw-private-skills\autotask-builder\data\environment\dispatcher.env
```

정확한 파일명은 코드에서 먼저 확인한다.

다음 값만 추출:

```text
tls_verify
tls_verify source
route
ca_bundle
ca_bundle_env
SSL_CERT_FILE
HTTPS_PROXY 존재 여부
HTTP_PROXY 존재 여부
NO_PROXY 존재 여부
```

보안상 proxy URL/token/password 값 자체는 출력하지 않는다.

출력 예:

```text
tls_verify=false
route=environment-proxy
SSL_CERT_FILE=SET
HTTPS_PROXY=SET
```

---

## B4. 가장 중요한 분기 — Updater가 insecure fallback으로 성공했는지

다음 조건을 판단한다.

```text
Skill-Updater GitHub remote access = SUCCESS
AND
persisted/active tls_verify = false
AND
Job-list signal urllib = verified default SSL
AND
Job-list signal = CERTIFICATE_VERIFY_FAILED
```

모두 참이면:

```text
TLS_ROOT_B = UPDATER_INSECURE_FALLBACK_NOT_SHARED_WITH_SIGNAL_CLIENT
CONFIDENCE = HIGH
```

단, **진단 중 새로 TLS verify를 끄지 않는다.**

---

## B5. CA bundle divergence 확인

다음 경우도 분리한다.

```text
Skill-Updater:
  explicit ca_bundle 사용

Job-list signal:
  plain urllib
  해당 CA bundle을 직접 context로 사용하지 않음
```

분류:

```text
B5-1 = SAME_CA_PATH_EFFECTIVE
B5-2 = UPDATER_ONLY_CA
B5-3 = SYSTEM_DEFAULT_ONLY
B5-4 = NO_CA_CONFIG
B5-5 = UNKNOWN
```

`B5-2`이면:

```text
TLS_ROOT_B = CUSTOM_CA_NOT_PROPAGATED
```

---

## B6. Python executable 차이 확인

다음 executable path만 확인한다.

```text
V0406 worker sys.executable
Skill-Updater scheduled execution Python executable
Dispatcher runner Python executable
```

값 자체는 짧게 기록.

분류:

```text
B6-1 = SAME_PYTHON
B6-2 = DIFFERENT_PYTHON
B6-3 = UNKNOWN
```

다르면 각 Python의:

```text
python --version
ssl.OPENSSL_VERSION
ssl.get_default_verify_paths()
```

만 확인한다.

인증서 전체 덤프 금지.

---

## B7. 정확한 SSL failure fingerprint

이미 확인된 문자열:

```text
certificate verify failed
basic constraints of CA cert not marked critical
```

추가로 필요한 것은 **한 줄 fingerprint**뿐이다.

자동 확인 가능하면 사용자에게 묻지 않는다.

분류:

```text
1 = SSLCertVerificationError
2 = URLError wrapping SSLCertVerificationError
3 = proxy TLS interception 관련
4 = custom CA load 실패
5 = 기타
```

Root certificate 이름/전체 인증서 내용은 필요 없다.

---

# 8. V0406 재실행 가능성 Deep Dive

## C1. processed 상태 확인

고정 증거:

```text
state=consumed
returncode=1
```

코드에서 같은 Job ID가 다시 activation될 때 어떤 상태가 되는지 확인한다.

분류:

```text
C1-1 = same ID 재queue 가능
C1-2 = DUPLICATE_SKIPPED
C1-3 = FAILED_RETRY
C1-4 = 기타
```

---

## C2. DUPLICATE_SKIPPED와 external breadcrumb 의미 확인

`job_core.py`에서 아래 로직을 확인한다.

```text
target.status in {"QUEUED", "DUPLICATE_SKIPPED"}
=> job-list-deferred signal
```

존재 시:

```text
DEFECT_C = DUPLICATE_SKIPPED_EMITS_DEFERRED
```

다음을 판단:

```text
1 = 정상 의도이며 의미 명확
2 = 외부에서 "재실행 대기"로 오해할 수 있음
3 = 실제 retry semantics와 충돌
```

`2` 또는 `3`이면 v0.4.7 수정 후보로 기록한다.

---

# 9. Root Cause 결정 트리

최종적으로 아래 중 하나씩 선택한다.

## Scheduler Root Cause

```text
RA1 = Task 실제 Disabled
RA2 = XML Enabled 누락/empty로 인한 false-negative
RA3 = schedule interval/start minute 불일치
RA4 = runner/arguments/YAML 불일치
RA5 = Task deploy 자체 실패
RA6 = principal/logon context 문제
RA7 = PowerShell/XML readback 불일치
RA8 = 기타
```

## TLS Root Cause

```text
RB1 = Updater insecure fallback과 Job-list verified urllib 정책 불일치
RB2 = Updater custom CA가 Job-list signal에 전달되지 않음
RB3 = proxy env 전달 불일치
RB4 = Python/OpenSSL runtime 차이
RB5 = 시스템 CA 자체 문제
RB6 = signal endpoint/네트워크 문제
RB7 = 기타
```

## Retry Root Cause/Policy

```text
RC1 = consumed Job ID는 동일 버전 재실행 불가
RC2 = same-ID retry 가능
RC3 = retry policy 불명확
```

---

# 10. 사용자 질문이 필요한 경우의 1차 객관식

가능하면 모두 직접 확인한다.

정말 접근이 안 될 때만 아래 질문 중 필요한 것만 묻는다.

```text
Q1. Scheduler State?
1 Ready
2 Running
3 Disabled
0 모름

Q2. Get-ScheduledTask의 Settings.Enabled?
1 True
2 False
0 모름

Q3. NextRunTime?
1 있음
2 없음
0 모름

Q4. Skill-Updater Task LastTaskResult?
1 0
2 0 아님
0 모름

Q5. Skill-Updater TLS profile의 tls_verify?
1 true
2 false
3 항목 없음
0 모름

Q6. SSL_CERT_FILE?
1 설정됨
2 미설정
0 모름

Q7. Dispatcher와 Updater Python?
1 동일
2 다름
0 모름

Q8. 같은 V0406 재activation 결과?
1 DUPLICATE_SKIPPED
2 QUEUED
3 기타
0 모름
```

사용자 답변 형식:

```text
1 1 1 1 2 1 1 1
```

---

# 11. 주관식이 꼭 필요한 경우

최대 3개까지만.

예:

```text
E1=Ready
E2=0
E3=Python313
```

파일/라인이 필요한 경우:

```text
E1=dispatcher_autotask_register_windows_job.py:215
```

그 이상 설명을 요구하지 않는다.

---

# 12. 최종 출력 형식

분석 후 **긴 서술 대신 아래 형식으로 먼저 결론**을 낸다.

```text
[FINAL]

SCHEDULER_ROOT = RA?
SCHEDULER_CONFIDENCE = HIGH / MEDIUM / LOW

TLS_ROOT = RB?
TLS_CONFIDENCE = HIGH / MEDIUM / LOW

RETRY_POLICY = RC?

FIRST_FATAL_STAGE = S8
V0406_REUSE = YES / NO

V0407_REQUIRED = YES / NO
```

그 다음 핵심 증거만 최대 6줄:

```text
[EVIDENCE]
1. ...
2. ...
3. ...
4. ...
5. ...
6. ...
```

그 다음 수정 대상만 표시:

```text
[PATCH_SCOPE]

P0:
- file:function
- file:function

P1:
- file:function
```

아직 코드는 수정하지 않는다.

---

# 13. v0.4.7 수정 필요성 판정

아래 중 하나라도 맞으면:

```text
RA2
RA7
RB1
RB2
RC1 + V0406 already consumed
```

다음으로 판정:

```text
V0407_REQUIRED = YES
```

단, 새 버전 제작 전에 이번 프롬프트의 진단 결과를 사용자에게 먼저 보여준다.

---

# 14. 특히 확인해야 할 현재 유력 가설

현재 증거상 아래 두 가설의 우선순위가 높지만 **증거 확인 전 확정하지 않는다.**

```text
H-A:
Scheduler Task는 실제 정상/Enabled 상태인데,
scheduler_query_xml()이 enabled=""를 false로 처리하여
S8에서 false-negative FATAL이 발생했다.

H-B:
Skill-Updater는 별도의 TLS profile/fallback으로 GitHub 접근에 성공했지만,
Job-list signal client는 plain urllib verified TLS를 사용하여
사내 CA의 basicConstraints 검증에서 실패했다.
```

추가 후보:

```text
H-C:
InteractiveToken은 현재 S8의 최초 원인이 아니라
로그오프 시 무인 실행 실패를 만들 수 있는 secondary risk다.

H-D:
V0406는 이미 consumed라 동일 Job ID 자동 retry가 되지 않으며,
수정본은 V0407 신규 Job ID가 필요하다.
```

---

# 15. 완료 조건

아래 5개가 모두 결정되면 진단을 끝낸다.

```text
1. scheduler_after.valid=false가 실제 invalid인지 false-negative인지
2. InteractiveToken이 direct root인지 secondary risk인지
3. Skill-Updater 성공과 signal TLS 실패가 왜 공존하는지
4. 같은 V0406가 다시 실행 가능한지
5. v0.4.7에서 수정할 정확한 file:function 목록
```

완료 후 추가 질문을 남발하지 말고 STOP한다.
