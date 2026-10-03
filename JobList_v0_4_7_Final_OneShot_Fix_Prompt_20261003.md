# Job-list v0.4.7 최종 One-Shot 수정·검증·패키징 실행 프롬프트

- 작성 시각: **2026-10-03 15:36 KST**
- 기준 버전: `job-list v0.4.6`
- 목표 버전: **`job-list v0.4.7`**
- 목표 산출물: **`job-list_v0_4_7_1003.zip`**
- 실행 성격: **마지막 1회 수행 / 사용자 추가 질의 없이 끝까지 진행**
- 우선순위: **P0 Root Cause 3개만 최소 수정 → 테스트 → 패키징**
- 금지: 범위 확장, 구조 대개편, unrelated refactoring, 기능 추가

---

# 0. 최우선 지시

이번 실행은 시간이 제한된 최종 수정 기회다.

**사용자에게 중간 질문하지 말고**, 현재 코드와 로컬 증거를 직접 확인하여 아래 작업을 순서대로 끝까지 수행한다.

```text
1. v0.4.6 baseline 확인
2. RA2 수정
3. RB1 수정
4. RC1 대응용 V0407 신규 Job identity 적용
5. targeted regression test 작성/수행
6. 전체 self-test/가능한 regression 수행
7. version/manifest/release metadata 정합
8. PACKAGE_CONTENTS.sha256 재생성/검증
9. 최종 ZIP 생성
10. 최종 보고서 작성
11. STOP
```

중간에 P1/P2 개선점이 보여도 **이번 버전에 구현하지 않는다.**
별도 `DEFERRED_IMPROVEMENTS`에 기록만 한다.

---

# 1. 확정된 Root Cause — 재분석 금지

아래는 이미 사내 PC 실증으로 확정되었다.

```text
SCHEDULER_ROOT = RA2
SCHEDULER_CONFIDENCE = HIGH

TLS_ROOT = RB1
TLS_CONFIDENCE = HIGH

RETRY_POLICY = RC1

FIRST_FATAL_STAGE = S8
V0406_REUSE = NO
V0407_REQUIRED = YES
```

## Evidence A — Scheduler

```text
Task.State = Ready
Task.Settings.Enabled = true
LastTaskResult = 0

schtasks /Query /XML:
<Enabled> element 자체가 존재하지 않음

v0.4.6:
scheduler_query_xml()
  line ~188: enabled = local_xml_text(root, "Enabled").lower()
  line ~209: and enabled == "true"

따라서:
XML Enabled missing
→ enabled=""
→ enabled=="true" false
→ scheduler_after.valid=false
→ S8 FATAL

실제 Scheduler Task는 정상인데 v0.4.6 validation이 false-negative.
```

## Evidence B — TLS

```text
Skill-Updater GitHub access = 성공

Job-list external signal GET:
external_signal_v0406_activation.ok=false
terminal_signal.ok=false

error:
CERTIFICATE_VERIFY_FAILED
basic constraints of CA cert not marked critical
```

v0.4.6 Job-list signal path는 plain/default `urllib.request.urlopen()`을 사용한다.

Embedded Skill-Updater v0.5.36은 다음 capability가 있다.

```text
_ssl_context()
_open_url()
proxy candidates
CA bundle
SSL_CERT_FILE
persisted network-profile.json
certificate verification error detection
allow_insecure_tls_fallback
remembered successful TLS profile
```

따라서:

```text
RB1 =
Skill-Updater의 이미 검증된 TLS/network policy와
Job-list signal transport policy가 서로 달라 발생
```

## Evidence C — Retry

```text
V0406:
processed.jsonl
state=consumed
returncode=1
```

동일 V0406 Job ID 재사용 불가.

**반드시 신규 V0407 Job identity를 사용한다.**

---

# 2. Baseline 확인

현재 작업 루트가 `job-list v0.4.6`인지 먼저 확인한다.

필수 확인:

```text
VERSION = 0.4.6
.skill-release.json version = 0.4.6
lifecycle.json version = 0.4.6
skillsilent manifest/contract skill_version = 0.4.6
requests/one-shot-jobs.json:
  JOB-20261002-DISPATCHER-RECOVERY-V0406
embedded skill-updater VERSION = 0.5.36
```

하나라도 다르면 임의 추측하지 말고 현재 트리를 기준으로 **0.4.6 → 0.4.7 최소 diff**를 유지한다.

Embedded `skill-updater 0.5.36`은 이번 작업에서 버전 변경하지 않는다.

---

# 3. P0-1 — RA2 Scheduler false-negative 수정

대상:

```text
scripts/dispatcher_autotask_register_windows_job.py
```

현재 핵심:

```python
enabled = local_xml_text(root, "Enabled").lower()

exact = (
    interval == "PT30M"
    and minute in (15, 45)
    and enabled == "true"
    and "--scheduled" in arguments
    and runner_ok
    and yaml_ok
)
```

이 구조를 그대로 두면 안 된다.

## 3.1 요구 동작

`<Enabled>`를 tri-state로 취급한다.

```text
XML "true"   -> TRUE
XML "false"  -> FALSE
XML missing/empty -> UNKNOWN
```

**UNKNOWN을 자동 PASS시키면 안 된다.**

UNKNOWN이면 PowerShell ScheduledTask readback을 사용한다.

우선 evidence:

```text
Get-ScheduledTask
Task.Settings.Enabled
Task.State
```

판정 규칙:

```text
A. XML Enabled == true
   -> enabled validation PASS

B. XML Enabled == false
   -> enabled validation FAIL

C. XML Enabled missing/empty
   AND PowerShell Task.Settings.Enabled == true
   AND State in {Ready, Running, Queued}
   -> enabled validation PASS
   -> source = powershell-fallback

D. XML Enabled missing/empty
   AND Settings.Enabled == false
   -> FAIL

E. XML Enabled missing/empty
   AND PowerShell readback unavailable/ambiguous
   -> FAIL conservatively
```

중요:

```text
enabled="" 자체를 PASS시키지 말 것.
PowerShell evidence가 있을 때만 fallback PASS.
```

---

# 4. scheduler_task_info() 보강

현재 `scheduler_task_info()`가 최소 다음 값을 읽는지 확인한다.

```text
State
UserId
LogonType
RunLevel
LastRunTime
LastTaskResult
NextRunTime
```

**Settings.Enabled도 반드시 추가한다.**

PowerShell JSON 예:

```powershell
Enabled=$t.Settings.Enabled
```

Python 결과에서는 명확한 bool로 유지한다.

예:

```json
{
  "State": "Ready",
  "Enabled": true,
  "LastTaskResult": 0
}
```

---

# 5. Scheduler validation 결합 방식

가능하면 한 곳에서 최종 판정을 만들고 중복 판정을 피한다.

필수 결과 필드:

```text
enabled_xml
enabled_effective
enabled_source
task_state
valid
```

예상 정상 결과:

```json
{
  "enabled_xml": "",
  "enabled_effective": true,
  "enabled_source": "powershell-fallback",
  "task_state": "Ready",
  "valid": true
}
```

XML `<Enabled>`가 없는 정상 Task가 더 이상 S8 FATAL을 만들면 안 된다.

---

# 6. InteractiveToken 처리

현재 실증:

```text
State=Ready
Settings.Enabled=true
LastTaskResult=0
LogonType=InteractiveToken
```

따라서 이번 P0에서:

```text
InteractiveToken != S8 direct root cause
```

기존 `logged_off_execution_risk` 정보는 유지한다.

**이번 v0.4.7에서 principal을 강제로 바꾸지 않는다.**

관련 자동 repair가 이미 있더라도 RA2 수정 때문에 불필요하게 principal repair가 먼저 실행되지 않게 한다.

로그오프 무인실행 위험은 P1 기록만 한다.

---

# 7. P0-2 — RB1 Signal TLS transport 정합

현재 plain urllib 경로를 전부 찾는다.

최소 확인 대상:

```text
scripts/job_core.py
  emit_dispatcher_recovery_signal()

scripts/dispatcher_autotask_register_windows_job.py
  external_signal_transport_probe()
  external_signal_probe_with_task_env()
```

v0.4.6에서 확인된 plain path 예:

```python
urllib.request.urlopen(...)
```

이 경로가 Skill-Updater와 다른 TLS policy를 사용해서는 안 된다.

---

# 8. TLS 수정 원칙

목표는:

```text
"인증서 검증을 무조건 끄기"
가 아니라

"Skill-Updater가 이미 성공해 기억한 network/TLS policy를
Job-list signal GET도 동일하게 사용"
```

이다.

## 절대 금지

아래를 전역/무조건 적용하지 않는다.

```python
ssl._create_unverified_context()
ssl.CERT_NONE
check_hostname = False
```

또한 시스템 인증서 설치/삭제를 수행하지 않는다.

---

# 9. 권장 구현 — remembered profile 기반의 제한적 fallback

Skill-Updater canonical profile:

```text
~/l1sw-private-skills/skill-updater/data/config/network-profile.json
```

v0.5.36 profile에는 최소 다음 의미가 있다.

```json
{
  "schema_version": ...,
  "tls_verify": false,
  "route": "...",
  "source": "last-successful-github-connection"
}
```

Job-list는 이 profile을 **read-only**로 참조한다.

## 9.1 Signal TLS policy

다음 순서로 구현한다.

```text
1. 기존 env/proxy 정보를 로드
2. Skill-Updater remembered network profile 확인
3. SSL_CERT_FILE / configured CA가 있으면 verified context 우선
4. 일반 verified TLS 시도
5. certificate verification failure인 경우에 한해서만:
     remembered profile.tls_verify == false
     또는 updater가 명시적으로 허용한 기존 persisted policy가 false
   라면 동일 request를 unverified TLS로 단 1회 retry
6. 성공/실패 결과에 tls mode/source를 기록
```

**Job-list가 자체적으로 새로운 insecure policy를 결정/저장하지 않는다.**
정책 SSOT는 Skill-Updater의 이미 검증된 remembered profile로 둔다.

즉:

```text
Updater가 insecure 성공 기록 없음
→ Job-list가 임의로 insecure fallback 금지

Updater remembered tls_verify=false
→ 동일 GitHub GET signal에 한해서 제한적으로 재사용 가능
```

---

# 10. 공통 Signal Transport helper 권장

가능하면 signal GET 구현을 하나로 통합한다.

예:

```text
scripts/signal_transport.py
```

또는 기존 적절한 공통 모듈.

필수 API 개념:

```python
get_signal(
    url,
    env,
    timeout,
    user_agent
) -> dict
```

결과 예:

```json
{
  "ok": true,
  "status": 200,
  "tls_verify": false,
  "tls_source": "skill-updater-remembered-success",
  "route": "...",
  "certificate_fallback_used": true
}
```

다음 3개 caller가 동일 transport를 써야 한다.

```text
emit_dispatcher_recovery_signal()
external_signal_transport_probe()
external_signal_probe_with_task_env()
```

복붙으로 서로 다른 TLS 정책을 다시 만들지 않는다.

---

# 11. Proxy/CA handling

기존 allowlist 환경 로딩을 유지한다.

현재 Job-list가 읽는 예:

```text
autotask-builder/data/environment/skill-updater.env
autotask-builder/data/environment/dispatcher.env
```

다음 environment를 지원/전달한다.

```text
HTTPS_PROXY / https_proxy
HTTP_PROXY / http_proxy
NO_PROXY / no_proxy
SSL_CERT_FILE
REQUESTS_CA_BUNDLE (필요 시 CA source로 호환)
```

Proxy URL, token, password는 결과 JSON/로그에 노출하지 않는다.

---

# 12. TLS certificate error detection

Updater v0.5.36과 동일 수준으로 certificate verification error를 식별한다.

최소:

```text
ssl.SSLCertVerificationError

URLError.reason chain

message:
certificate verify failed
certificateverifyfailed
certificate_verify_failed
certificate verify error
```

**인증서 오류일 때만** remembered `tls_verify=false` fallback 적용.

HTTP 404, 403, 429, timeout 등에는 insecure retry를 사용하지 않는다.

---

# 13. P0-3 — V0407 신규 Job identity

수정:

```text
requests/one-shot-jobs.json
```

신규 ID:

```text
JOB-20261003-DISPATCHER-RECOVERY-V0407
```

날짜는 이번 release 날짜인 `20261003`으로 한다.

기존 V0406 ID를 재사용하지 않는다.

---

# 14. stale recovery cleanup

V0407 activation 시 known legacy recovery Job 중 **PENDING 상태만** 제한적으로 supersede 하는 기존 정책을 유지한다.

기존 allowlist에 V0406가 없다면 추가한다.

```text
... V0404
... V0405
... V0406
```

단:

```text
RUNNING은 건드리지 않음
consumed history 삭제하지 않음
unrelated business Job 건드리지 않음
processed.jsonl 삭제/수정하지 않음
```

---

# 15. Signal naming

기존 외부 signal contract를 깨지 않는다.

유지:

```text
dispatcher-windows-job-list-deferred.signal
dispatcher-windows-job-list-ok.signal
dispatcher-windows-job-list-fail.signal
dispatcher-windows-autotask-error.signal
dispatcher-windows-heartbeat-ok.signal
```

v0.4.7에서도 사외 관찰자가 같은 파일명을 계속 확인할 수 있어야 한다.

User-Agent 등에 버전 문자열이 있으면:

```text
v0.4.6 -> v0.4.7
```

으로 갱신한다.

---

# 16. 필수 Regression Tests

새 파일 권장:

```text
tests/test_v0407_scheduler_tls_recovery.py
```

테스트는 실제 Windows Scheduler나 실제 GitHub를 변경하지 않고 mock/fixture 기반으로 수행한다.

최소 아래를 모두 구현한다.

## T1

```text
XML Enabled=true
interval=PT30M
minute=15/45
runner/yaml 정상
=> valid=true
```

## T2

```text
XML Enabled=false
PowerShell Enabled=true여도
=> valid=false
```

explicit false가 우선한다.

## T3 — 이번 Root Cause 재현

```text
XML <Enabled> 없음
PowerShell:
  Enabled=true
  State=Ready
  LastTaskResult=0
other schedule fields 정상

=> valid=true
enabled_source=powershell-fallback
```

## T4

```text
XML Enabled 없음
PowerShell Enabled=false
=> valid=false
```

## T5

```text
XML Enabled 없음
PowerShell readback 실패
=> valid=false
```

## T6

```text
verified TLS success
=> insecure fallback 사용 안 함
```

## T7 — 이번 TLS Root Cause

```text
verified request
=> SSLCertVerificationError

Skill-Updater remembered profile:
tls_verify=false

=> unverified TLS 1회 retry
=> success
=> ok=true
=> certificate_fallback_used=true
```

## T8

```text
verified cert error
remembered profile 없음 또는 tls_verify=true
=> insecure retry 금지
=> failure
```

## T9

```text
HTTP 404/403/timeout
=> insecure TLS retry 금지
```

## T10

```text
V0407 신규 ID 존재
V0406 ID를 current one-shot으로 사용하지 않음
```

## T11

```text
legacy V0406 PENDING
=> V0407이 narrow supersede 가능
```

## T12

```text
legacy V0406 RUNNING
=> 보존
```

## T13

```text
unrelated Job
=> 보존
```

---

# 17. 기존 관련 테스트도 반드시 수행

최소:

```text
tests/test_v0406_signal_observability.py
tests/test_v0404_legacy_pending_cleanup.py
tests/test_v0401_dispatcher_recovery.py
```

그리고 새 `test_v0407_*`.

가능하면 기존 v0.4.0~v0.4.6 targeted set 전체 수행.

---

# 18. 기존 전체 regression failure 처리

v0.4.6에서 이전 분석 시 기존 regression 중 하나가:

```text
test_v0352_does_not_delete_persistent_processed_state_by_contract
```

release-note wording assertion 때문에 실패한 이력이 있다.

이번 v0.4.7에서는 **실제 processed-history 보존 정책을 바꾸지 않는다.**

release metadata에 아래 의미가 명확히 포함되게 하여,
가능하면 해당 regression도 PASS시키되,
본 작업 핵심 로직을 왜곡하지 않는다.

```text
processed history is never deleted
data/** and output/** remain persistent
```

---

# 19. 전체 Test 실행 순서

아래 순서를 지킨다.

```text
1. python scripts/job_core.py validate
2. 신규 v0407 targeted tests
3. v0406/v0404/v0401 관련 tests
4. v0.4.x targeted suite 가능한 범위
5. 전체 pytest
```

전체 pytest에서 unrelated legacy failure가 남을 경우:

```text
- 핵심 v0407 tests PASS 여부 별도 기록
- 실패 test 이름/원인 한 줄 기록
- 신규 변경에 의한 regression인지 판단
```

**신규 변경으로 인한 실패면 ZIP 생성 전에 수정한다.**

---

# 20. Version bump

최종 패키지 identity를 정확히:

```text
0.4.7
```

로 맞춘다.

최소 확인:

```text
VERSION
.skill-release.json
lifecycle.json
skillsilent/manifest.json
skillsilent/contract.json
README.md
SKILL.md
install.py 내 release/version 관련 항목
필요한 user-agent/release 설명
```

과거 release history/fixture의 `0.4.6` 문자열을 무차별 replace 하지 않는다.

---

# 21. Release Notes

신규 파일:

```text
RELEASE_NOTES_v0_4_7_1003.md
```

핵심 내용:

```text
1. Fix RA2:
   schtasks XML에서 optional <Enabled>가 없을 때
   PowerShell Settings.Enabled + State fallback으로 정상 Task false-negative 방지.

2. Fix RB1:
   Job-list external signal transport가 Skill-Updater remembered TLS policy를
   read-only로 재사용하여 사내 CA certificate verification incompatibility 대응.

3. Security:
   insecure TLS는 updater의 기존 remembered tls_verify=false가 있을 때,
   certificate verification failure에 대해서만 1회 제한 fallback.
   global verify disable 없음.

4. V0407:
   fresh one-shot identity.
   V0406 consumed state 재사용 안 함.

5. Preserve:
   persistent data/output/processed history 보존.
   unrelated/running Jobs 보존.
```

---

# 22. PACKAGE_CONTENTS.sha256

모든 수정과 metadata 정합 후 마지막에 재생성한다.

ZIP에 자기 자신이나 임시 캐시/pytest cache가 들어가지 않게 한다.

제외:

```text
__pycache__/
*.pyc
.pytest_cache/
.git/
temporary backup
old output generated solely by this patch session
```

패키지에 원래 포함되던 정상 persistent-layout placeholder는 유지한다.

---

# 23. 최종 ZIP

정확한 이름:

```text
job-list_v0_4_7_1003.zip
```

ZIP 내부 top directory도 가능하면:

```text
job-list_v0_4_7_1003/
```

으로 통일한다.

ZIP 생성 후 다시 열어서 최소 검증:

```text
VERSION == 0.4.7
one-shot ID == JOB-20261003-DISPATCHER-RECOVERY-V0407
embedded skill-updater == 0.5.36
new test 존재
release notes 존재
PACKAGE_CONTENTS.sha256 verify PASS
```

---

# 24. 최종 보고서

ZIP과 함께:

```text
JOB_LIST_V0407_FINAL_REPORT_20261003.md
```

를 생성한다.

형식:

```text
[RESULT]
VERSION=0.4.7
ZIP=job-list_v0_4_7_1003.zip
READY=YES/NO

[ROOT_CAUSE_FIXED]
RA2=PASS/FAIL
RB1=PASS/FAIL
RC1=PASS/FAIL

[TEST]
SELF_TEST=PASS/FAIL
V0407_TARGETED=x/y PASS
RELATED_REGRESSION=x/y PASS
FULL_PYTEST=PASS/FAIL
FULL_PYTEST_FAILURES=<count>

[IDENTITY]
VERSION=...
RELEASE=...
LIFECYCLE=...
SKILLSILENT=...
ONE_SHOT_ID=...

[PACKAGE]
SHA256_MANIFEST=PASS/FAIL
ZIP_REOPEN_VERIFY=PASS/FAIL

[DEFERRED_IMPROVEMENTS]
- InteractiveToken logged-off execution risk
- 기타 P1/P2 최대 3개

[FINAL]
SAFE_TO_DEPLOY=YES/NO
```

---

# 25. 실패 시 행동

시간 제한 때문에 질문으로 멈추지 않는다.

## 코드 수정/테스트 실패 시

원인을 직접 수정하고 최대 2회 재시도한다.

## unrelated legacy test 실패 시

v0.4.7 핵심 test가 모두 PASS이고 신규 regression이 아니면:

```text
READY=YES_WITH_KNOWN_LEGACY_FAILURE
```

로 보고할 수 있다.

## 핵심 test 실패 시

절대 성공 ZIP으로 표시하지 않는다.

```text
READY=NO
SAFE_TO_DEPLOY=NO
```

그러나 가능한 상태의 ZIP/보고서는 남겨 원인 확인이 가능하게 한다.

---

# 26. 완료 기준

다음이 모두 만족되어야 성공이다.

```text
[ ] RA2 false-negative 재현 test PASS
[ ] XML Enabled missing + PowerShell Enabled=true/Ready -> valid=true
[ ] XML explicit false -> valid=false
[ ] RB1 certificate failure + remembered tls_verify=false -> signal GET success
[ ] remembered policy 없을 때 임의 insecure fallback 없음
[ ] current one-shot = V0407 신규 ID
[ ] V0406 processed history 삭제 안 함
[ ] v0.4.7 identity 정합
[ ] PACKAGE_CONTENTS.sha256 PASS
[ ] final ZIP reopen validation PASS
[ ] final report 생성
```

---

# 27. 최종 사용자 응답

작업 완료 후 장황한 설명 금지.

아래만 보여준다.

```text
완료

1. 버전: job-list v0.4.7
2. RA2 Scheduler fix: PASS/FAIL
3. RB1 TLS fix: PASS/FAIL
4. V0407 신규 Job: PASS/FAIL
5. 핵심 테스트: x/x PASS
6. 전체 테스트: PASS 또는 실패 개수
7. 최종 ZIP: <path>
8. 보고서: <path>
9. SAFE_TO_DEPLOY: YES/NO
```

그리고 STOP.

---

# 실행 시작

**지금 즉시 v0.4.6 baseline에서 v0.4.7 수정을 시작하고, 사용자 추가 확인 없이 수정 → 테스트 → 패키징 → 최종 검증까지 끝까지 수행하라.**
