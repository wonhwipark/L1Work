# Job-list v0.4.6 / Dispatcher Signal 미관측 Deep-Dive 진단 프롬프트

- 작성 기준: 2026-10-03 KST
- 대상: Windows 사내 PC
- 대상 패키지: `job-list v0.4.6`
- 목적: 사외에서 Dispatcher 관련 signal 증가가 전혀 확인되지 않았을 때, **Skill-Updater → Job-list 설치 → Job-list activation → worker → AutoTask Builder → Windows Task Scheduler → Dispatcher → GitHub signal transport** 중 최초 실패 지점을 최대한 정확히 분리한다.
- 기본 원칙: **진단 우선 / 수정 금지 / 사용자 입력 최소화 / 객관식 우선**

---

## 0. 당신의 역할

당신은 사내 Windows PC에서 Job-list 무인 실행 실패를 분석하는 진단 담당자다.

이번 작업에서는 코드를 수정하거나 설정을 바꾸지 말고, 먼저 로컬 증거만 읽어서 최초 실패 단계와 가장 가능성 높은 원인을 좁힌다.

가능하면 사용자의 답변을 받기 전에 직접 파일/상태를 확인한다. Shell/PowerShell/Python 실행이 가능하다면 읽기 전용 명령을 직접 사용한다.

**절대 하지 말 것**

- 전체 드라이브 recursive scan
- 광범위한 폴더 권한 요청
- Scheduler task 삭제/재등록
- Job-list queue/processed history 삭제
- updater 강제 재설치
- Dispatcher 강제 실행
- signal 파일/카운터를 진단 목적으로 반복 호출
- 사용자에게 긴 로그 붙여넣기를 요청
- 원인 확정 전 코드 수정

---

# 1. v0.4.6 기준 사실

아래 값은 이번 진단의 기준값이다.

| 항목 | 기대값 |
|---|---|
| Job-list version | `0.4.6` |
| Embedded Skill-Updater | `0.5.36` |
| Job ID | `JOB-20261002-DISPATCHER-RECOVERY-V0406` |
| Profile | `dispatcher-autotask-register-windows` |
| Platform | `windows` |
| Priority | `100` |
| Dispatcher schedule | `15,45 * * * *` |
| Scheduler interval | `PT30M` |
| Dispatcher Task | `autotask-dispatcher_observer` |
| AutoTask Builder 권장 버전 | `0.4.24` 이상 |

v0.4.6의 외부 signal 의미는 아래와 같다.

| Signal | 의미 |
|---|---|
| `dispatcher-windows-job-list-deferred.signal` | V0406 activation/queue 단계까지 도달한 초기 breadcrumb |
| `dispatcher-windows-job-list-ok.signal` | Dispatcher recovery Job이 비치명적 terminal 상태까지 도달 |
| `dispatcher-windows-job-list-fail.signal` | Job-list recovery가 fatal terminal 경로에 도달 |
| `dispatcher-windows-autotask-ok.signal` | Scheduler 등록 readback이 정상 |
| `dispatcher-windows-autotask-error.signal` | AutoTask/Scheduler fatal fault domain |
| `dispatcher-windows-heartbeat-ok.signal` | 실제 Dispatcher execution이 외부 heartbeat 경로까지 도달한 가장 강한 증거 |

**중요:** 외부 signal이 전혀 증가하지 않았다고 해서 Job-list 자체가 실행되지 않았다고 즉시 결론 내리지 않는다. 로컬 실행은 정상인데 GitHub Release GET signal transport만 실패했을 수도 있다.

---

# 2. 사용자 응답 규칙 — 반드시 지킬 것

## 2.1 객관식 우선

사용자에게 질문이 필요하면 한 번에 최대 10개까지만 묻는다.

각 질문은 반드시 숫자 선택지로 제공한다.

사용자는 아래처럼 **숫자 한 줄**만 입력할 수 있어야 한다.

`1 1 2 0 3 1`

기본 선택지 의미가 가능한 경우 다음을 사용한다.

- `0` = 모름 / 확인 불가
- `1` = 정상 / 있음 / 기대값 일치
- `2` = 비정상 / 기대값 불일치
- `3` = 없음
- `4` = 기타

## 2.2 주관식 최소화

주관식 질문은 객관식만으로 분기할 수 없을 때만 허용한다.

허용되는 주관식은 다음처럼 **단답 하나**뿐이다.

- `E1=1`
- `E2=FAILED`
- `E3=0.5.33`
- `E4=127`
- `E5=latest.json`

긴 로그, 설명문, 여러 줄 복사 요청 금지.

정말 코드 위치가 필요하면 최대 다음 정도만 요청한다.

- `E1=파일명:라인번호`
- 예: `E1=job_core.py:1612`

## 2.3 이미 로컬에서 확인 가능한 것은 사용자에게 묻지 말 것

파일, JSON, VERSION, Scheduler XML, return code를 직접 읽을 수 있으면 질문하지 말고 자동 판정한다.

---

# 3. 고정 탐색 경로

우선 아래 경로만 확인한다. 다른 위치가 필요해도 먼저 사용자에게 묻지 말고 이 allowlist 내에서 해결한다.

```text
%USERPROFILE%\l1sw-private-skills\job-list
%USERPROFILE%\l1sw-private-skills\skill-updater
%USERPROFILE%\l1sw-private-skills\autotask-builder
%USERPROFILE%\l1sw-dispatcher
%USERPROFILE%\l1sw-private-skills\l1sw-dispatcher
%USERPROFILE%\.claude\skills\job-list
%USERPROFILE%\.claude\skills\skill-updater
```

Job-list 핵심 증거:

```text
job-list\VERSION
job-list\.skill-release.json
job-list\data\state\install-self-check.json
job-list\data\state\activation\latest.json
job-list\data\state\activation\history.jsonl
job-list\data\state\core\queue.json
job-list\data\state\core\processed.jsonl
job-list\data\state\core\running.json
job-list\data\state\observer\latest_result.json
job-list\data\state\core\recovery-latest.json
job-list\output\core\last_run.json
job-list\output\core\lifecycle_events.jsonl
job-list\output\dispatcher_autotask_register\latest_result.json
job-list\output\updater_gate_rescue_v0400\install_repair.json
```

Skill-Updater 핵심 증거:

```text
skill-updater\VERSION
skill-updater\data\state\last_run.json
skill-updater\data\state\current_run.json
skill-updater\output\update_result.json
skill-updater\output\update_report.md
```

경로에 파일이 없다고 전체 디스크를 검색하지 말고 `MISSING`으로 기록한다.

---

# 4. 자동 진단 Stage

아래 순서대로 진행한다. 뒤 단계 증거가 있어도 앞 단계 최초 실패를 우선한다.

## S0. 설치 Identity

확인:

1. `job-list/VERSION == 0.4.6`
2. `.skill-release.json.version == 0.4.6`
3. discovery `~/.claude/skills/job-list/SKILL.md`가 0.4.6을 가리키는지
4. `skill-updater/VERSION == 0.5.36`

판정 코드:

- `S0_OK`
- `S0_JOBLIST_OLD`
- `S0_UPDATER_OLD`
- `S0_INSTALL_INCOMPLETE`
- `S0_DISCOVERY_MISMATCH`

---

## S1. Skill-Updater 자체 실행 여부

확인:

1. 최근 `last_run.json/current_run.json` 존재
2. 최근 예약 실행 시각과 갱신 시각이 맞는지
3. 상태가 RUNNING에서 오래 멈췄는지
4. update 결과에 Job-list target이 존재하는지
5. remote freshness가 verified인지
6. `REMOTE_FRESHNESS_UNVERIFIED` 여부

판정 코드:

- `S1_OK`
- `S1_SCHEDULER_NOT_FIRED`
- `S1_UPDATER_STUCK`
- `S1_REMOTE_FRESHNESS_FAIL`
- `S1_JOBLIST_TARGET_NOT_SEEN`
- `S1_UPDATER_FAILED_BEFORE_TARGET`

---

## S2. Job-list v0.4.6 설치 여부

확인:

1. updater 결과가 Job-list `UPDATED` 또는 이미 `CURRENT`인지
2. 실제 canonical root VERSION이 0.4.6인지
3. `install-self-check.json` 존재/상태
4. install 중 embedded updater gate repair 결과
5. updater gate가 `VERIFIED`인지

판정 코드:

- `S2_OK`
- `S2_DOWNLOAD_FAIL`
- `S2_INSTALL_FAIL`
- `S2_INSTALL_ROLLBACK`
- `S2_UPDATER_GATE_REPAIR_FAIL`
- `S2_PACKAGE_INSTALLED_BUT_NO_POST_HOOK`

---

## S3. Skill-Updater → Job-list activation hook

Skill-Updater v0.5.36의 non-check cycle은 canonical Job-list에 다음 의미의 호출을 해야 한다.

```text
job-list-core activate --launch
```

확인:

1. updater 결과의 `job_sync` 존재
2. `job_sync.status`
3. `job_sync.returncode`
4. `job-list/data/state/activation/latest.json` 갱신 여부
5. activation history에 V0406 존재 여부

판정 코드:

- `S3_OK`
- `S3_JOB_SYNC_NOT_CALLED`
- `S3_JOB_SYNC_NOT_AVAILABLE`
- `S3_JOB_SYNC_TIMEOUT`
- `S3_JOB_SYNC_FAILED`
- `S3_ACTIVATION_NOT_REACHED`

**핵심:** Job-list 0.4.6이 설치되어 있는데 activation/latest가 갱신되지 않았다면 Dispatcher보다 앞단 문제다.

---

## S4. V0406 activation 결과

`activation/latest.json` 또는 history에서 다음 Job ID를 찾는다.

```text
JOB-20261002-DISPATCHER-RECOVERY-V0406
```

상태 분류:

- `QUEUED`
- `DUPLICATE_SKIPPED`
- `TARGET_MISMATCH`
- `REJECTED`
- `EXPIRED`
- 없음

추가 확인:

- `worker.status`
- `pending_after`
- `runtime_recovery.blocking_live_process`
- `external_signal_v0406_activation.ok`

판정 코드:

- `S4_QUEUED`
- `S4_DUPLICATE`
- `S4_TARGET_MISMATCH`
- `S4_REJECTED`
- `S4_WORKER_LAUNCH_FAIL`
- `S4_DEFERRED_LIVE_RUNTIME`
- `S4_SIGNAL_TRANSPORT_FAIL_AT_ACTIVATION`

### 중요 해석

`DUPLICATE_SKIPPED`이면 반드시 `processed.jsonl`과 `queue.json`을 함께 본다.

- processed에 이미 terminal V0406가 있고 queue에는 없다 → **v0.4.6 one-shot은 자동 재실행되지 않음**
- queue에 V0406가 남아 있다 → 다음 worker launch recovery 가능

이 둘을 같은 상태로 취급하지 말 것.

---

## S5. Job-list worker / profile 실행

확인:

1. `queue.json`에 V0406가 남아 있는가
2. `running.json` 존재 여부
3. `lifecycle_events.jsonl`에서 아래 이벤트 존재 여부
   - `ACTIVATION_WORKER_SPAWNED`
   - `WORKER_RUN_START`
   - `JOB_STARTING`
   - `CHILD_SPAWNED`
   - `CHILD_EXIT`
   - `JOB_RECEIPT_WRITTEN`
   - `WORKER_RUN_END`
4. `processed.jsonl`의 V0406 terminal record
5. `output/core/last_run.json`

판정 코드:

- `S5_OK`
- `S5_PENDING_NO_WORKER`
- `S5_STALE_RUNNING`
- `S5_CHILD_SPAWN_FAIL`
- `S5_CHILD_TIMEOUT`
- `S5_OUTPUT_MISSING`
- `S5_PROFILE_FAILED`

---

## S6. Dispatcher recovery profile 자체 결과

확인:

```text
job-list\output\dispatcher_autotask_register\latest_result.json
```

우선 다음 필드만 읽는다.

```text
status
warnings
summary
autotask_builder_version
deploy_attempts
scheduler_after.valid
scheduler_task_info_after_deploy
heartbeat_changed
scheduler_state_advanced
dispatcher_state_advanced
terminal_signal_sent
terminal_signal.ok
stage_signal_autotask_ok.ok
external_signal_transport_probe.ok
external_heartbeat_transport_probe.ok
external_heartbeat_task_env_probe.ok
```

상태 분류:

- `VERIFIED_OK`
- `SCHEDULED_OK`
- `DEGRADED`
- `FATAL`
- 파일 없음

판정 코드:

- `S6_VERIFIED_OK`
- `S6_SCHEDULED_NO_EXECUTION_PROOF`
- `S6_DEGRADED`
- `S6_FATAL`
- `S6_PROFILE_NEVER_STARTED`

---

## S7. AutoTask Builder

확인:

1. canonical AutoTask Builder 존재
2. VERSION
3. CLI 존재
4. generated dispatcher YAML 존재
5. check 결과
6. deploy 결과

판정 코드:

- `S7_OK`
- `S7_AUTOTASK_NOT_FOUND`
- `S7_VERSION_OLD`
- `S7_CHECK_FAIL`
- `S7_DEPLOY_FAIL`
- `S7_CLI_EXEC_FAIL`

버전이 0.4.24보다 낮아도 그것만으로 root cause로 확정하지 않는다. 실제 check/deploy evidence를 우선한다.

---

## S8. Windows Task Scheduler 등록

Task 이름:

```text
autotask-dispatcher_observer
```

반드시 XML readback으로 확인한다.

정상 조건:

- Enabled = true
- Interval = `PT30M`
- StartBoundary minute = `15` 또는 `45`
- Arguments에 `--scheduled`
- `windows_task_runner.py`
- canonical YAML 경로 포함

판정 코드:

- `S8_OK`
- `S8_TASK_MISSING`
- `S8_TASK_DISABLED`
- `S8_INTERVAL_WRONG`
- `S8_ARGUMENT_WRONG`
- `S8_YAML_PATH_WRONG`
- `S8_READBACK_FAIL`

---

## S9. Scheduler 실행 Context / Principal

확인:

- UserId
- LogonType
- RunLevel
- LastTaskResult
- LastRunTime
- NextRunTime

가능하면 정상 동작 중인 Skill-Updater Scheduled Task와 비교한다.

판정 코드:

- `S9_OK`
- `S9_LOGON_CONTEXT_SUSPECT`
- `S9_LAST_RESULT_NONZERO`
- `S9_TASK_NOT_TRIGGERED`
- `S9_UPDATER_PRINCIPAL_DIFF`

**InteractiveToken이면 PC 로그오프 상태에서 실행되지 않을 위험을 별도 표시한다.**

---

## S10. Scheduler vs AutoTask vs Dispatcher 분리

아래 증거로 fault domain을 분리한다.

### A. Scheduler 실행 후 Dispatcher state 증가

→ Scheduler/AutoTask/Dispatcher 실행 경로 정상 가능성이 높음.

### B. Scheduler 실행은 안 되지만 direct AutoTask 실행 시 Dispatcher state 증가

→ `WINDOWS_SCHEDULER_OR_LOGON_FAULT`

### C. direct AutoTask도 안 되지만 direct Dispatcher cycle에서 state 증가

→ `AUTOTASK_AND_SCHEDULER_FAULT`

### D. direct Dispatcher에서도 state 증가 없음

→ `DISPATCHER_RUNTIME_FAULT`

진단 단계에서는 직접 실행을 새로 수행하지 않는다. `latest_result.json`에 이미 기록된 기존 evidence만 우선 사용한다.

---

## S11. 외부 Signal Transport

사외에서 모든 signal이 그대로인 경우 가장 중요하다.

확인:

1. `external_signal_v0406_activation.ok`
2. `terminal_signal.ok`
3. `stage_signal_autotask_ok.ok`
4. `external_signal_transport_probe.ok`
5. `external_heartbeat_transport_probe.ok`
6. `external_heartbeat_task_env_probe.ok`
7. 오류 문자열 종류만 분류

오류는 전체 문장을 요구하지 말고 아래 코드로 분류한다.

- `1` = timeout
- `2` = DNS/name resolution
- `3` = SSL/certificate
- `4` = proxy
- `5` = HTTP 403/401
- `6` = HTTP 404
- `7` = connection refused/reset
- `8` = 기타 network
- `9` = signal call 자체가 없음
- `0` = 모름

판정 코드:

- `S11_OK`
- `S11_SIGNAL_GET_BLOCKED`
- `S11_PROXY_ENV_MISMATCH`
- `S11_CERTIFICATE_FAIL`
- `S11_HEARTBEAT_ONLY_FAIL`
- `S11_SIGNAL_CALL_NOT_REACHED`

**중요 분리:** updater의 GitHub remote 조회가 성공해도 Release asset GET 경로가 별도 redirect/proxy/certificate 문제로 실패할 수 있다.

---

# 5. 사용자에게 질문해야 하는 경우의 1차 객관식

로컬 접근이 불가능하거나 일부 증거가 없을 때만 아래 질문을 한다.

한 번에 전부 묻지 말고 최대 10개만 선택한다.

### Q1. Job-list VERSION

0. 모름  
1. 0.4.6  
2. 0.4.6 아님  
3. 파일 없음

### Q2. Skill-Updater VERSION

0. 모름  
1. 0.5.36  
2. 다른 버전  
3. 파일 없음

### Q3. 최근 Skill-Updater 실행 흔적

0. 모름  
1. 있음 + 완료  
2. 있음 + RUNNING/중단  
3. 없음

### Q4. updater 결과의 Job-list 상태

0. 모름  
1. UPDATED  
2. CURRENT  
3. FAILED  
4. Job-list 항목 없음

### Q5. updater `job_sync`

0. 모름  
1. CALLED  
2. FAILED_NONBLOCKING  
3. NOT_AVAILABLE  
4. 항목 없음

### Q6. activation latest에 V0406 존재

0. 모름  
1. QUEUED  
2. DUPLICATE_SKIPPED  
3. REJECTED/EXPIRED  
4. TARGET_MISMATCH  
5. V0406 없음

### Q7. activation worker

0. 모름  
1. spawned/started  
2. deferred live runtime  
3. failed  
4. worker 정보 없음

### Q8. `dispatcher_autotask_register/latest_result.json`

0. 모름  
1. VERIFIED_OK  
2. SCHEDULED_OK  
3. DEGRADED  
4. FATAL  
5. 파일 없음

### Q9. Scheduler task

0. 모름  
1. :15/:45 정상 등록  
2. 등록은 있으나 설정 불일치  
3. task 없음  
4. 조회 실패

### Q10. 로컬 Dispatcher 실행 증거

0. 모름  
1. heartbeat/state 증가 확인  
2. state만 증가  
3. 실행 요청은 있으나 증가 없음  
4. 실행 흔적 없음

응답 예:

`1 1 1 1 1 2 1 3 1 2`

---

# 6. 조건부 2차 객관식

1차 결과로 fault domain이 충분히 좁혀지면 불필요한 질문은 생략한다.

## Branch A — Updater 앞단 의심

### A1. Scheduled Task LastRunTime
0 모름 / 1 예상 시각 갱신 / 2 오래됨 / 3 task 없음

### A2. LastTaskResult
0 모름 / 1 `0` / 2 non-zero / 3 없음

### A3. Remote freshness
0 모름 / 1 fresh verified / 2 unverified / 3 기록 없음

### A4. Job-list remote candidate
0 모름 / 1 0.4.6 관측 / 2 구버전만 관측 / 3 target 자체 없음

---

## Branch B — Installation/activation 의심

### B1. install-self-check
0 모름 / 1 존재+정상 / 2 존재+실패 / 3 없음

### B2. embedded updater repair
0 모름 / 1 VERIFIED / 2 FAILED_ROLLED_BACK / 3 파일 없음

### B3. activation latest 갱신 시각
0 모름 / 1 이번 updater 실행 이후 / 2 이전 시각 / 3 파일 없음

### B4. V0406 queue 상태
0 모름 / 1 queue에 있음 / 2 processed에만 있음 / 3 둘 다 없음 / 4 둘 다 있음

---

## Branch C — Worker/profile 의심

### C1. WORKER_RUN_START
0 모름 / 1 있음 / 2 없음

### C2. CHILD_SPAWNED
0 모름 / 1 있음 / 2 없음

### C3. CHILD_EXIT returncode
0 모름 / 1 `0` / 2 non-zero / 3 CHILD_EXIT 없음

### C4. required output
0 모름 / 1 생성 / 2 미생성

### C5. terminal processed status
0 모름 / 1 SUCCESS / 2 FAILED / 3 TIMEOUT / 4 OUTPUT_MISSING / 5 기록 없음

---

## Branch D — AutoTask/Scheduler 의심

### D1. AutoTask Builder
0 모름 / 1 >=0.4.24 / 2 <0.4.24 / 3 없음

### D2. AutoTask check
0 모름 / 1 pass / 2 fail / 3 미실행

### D3. Scheduler XML readback
0 모름 / 1 valid / 2 invalid / 3 task 없음

### D4. Scheduler immediate run
0 모름 / 1 요청 성공 / 2 요청 실패 / 3 미실행

### D5. direct AutoTask evidence
0 모름 / 1 Dispatcher advanced / 2 not advanced / 3 미실행

### D6. direct Dispatcher evidence
0 모름 / 1 advanced / 2 not advanced / 3 미실행

---

## Branch E — Signal transport 의심

### E1. activation signal local result
0 모름 / 1 ok=true / 2 ok=false / 3 call 없음

### E2. terminal job-list signal
0 모름 / 1 ok=true / 2 ok=false / 3 call 없음

### E3. autotask-ok signal
0 모름 / 1 ok=true / 2 ok=false / 3 call 없음

### E4. heartbeat GET
0 모름 / 1 성공 / 2 실패 / 3 호출 흔적 없음

### E5. 실패 유형
0 모름 / 1 timeout / 2 DNS / 3 SSL / 4 proxy / 5 401/403 / 6 404 / 7 reset/refused / 8 기타

---

# 7. Root Cause 코드

최종적으로 반드시 아래 중 하나를 1순위 원인으로 선택한다.

| 코드 | 의미 |
|---|---|
| R01 | Skill-Updater Scheduled Task가 실행되지 않음 |
| R02 | Skill-Updater가 실행됐으나 중단/정지 |
| R03 | GitHub fresh remote 관측 실패 |
| R04 | Job-list v0.4.6을 원격에서 보지 못함 |
| R05 | Job-list 다운로드/설치 실패 |
| R06 | Embedded Skill-Updater 0.5.36 gate repair 실패/rollback |
| R07 | Job-list 설치는 됐으나 post-update activation hook 미도달 |
| R08 | `job_sync` 실패/timeout/not available |
| R09 | V0406 activation 자체가 reject/target mismatch |
| R10 | V0406가 pending인데 worker가 실행되지 않음 |
| R11 | stale/live Job-list runtime이 worker 실행을 막음 |
| R12 | Job-list child/profile spawn 또는 execution 실패 |
| R13 | required output / semantic result 미생성 |
| R14 | AutoTask Builder 없음/실행 실패 |
| R15 | AutoTask YAML check/deploy 실패 |
| R16 | Windows Scheduler 등록/readback 불일치 |
| R17 | Scheduler logon/principal/context 문제 |
| R18 | Scheduler는 실패하지만 direct AutoTask는 정상 |
| R19 | AutoTask도 실패하지만 direct Dispatcher는 정상 |
| R20 | Dispatcher 자체 runtime 실패 |
| R21 | Job-list/Dispatcher는 로컬 정상, 외부 signal GET transport 실패 |
| R22 | heartbeat 경로만 실패하고 일반 signal transport는 정상 |
| R23 | V0406가 이미 terminal processed되어 same ID one-shot 재실행이 차단됨 |
| R24 | 증거 불충분 — 추가 1회 객관식 필요 |

---

# 8. 중요한 v0.4.6 특이점

## 8.1 `processed.jsonl`은 삭제하지 않는다

진단 목적으로도 processed history를 초기화하지 않는다.

## 8.2 V0406는 one-shot identity다

V0406가 한 번 terminal processed 상태가 되면 같은 ID는 다음 activation에서 `DUPLICATE_SKIPPED`가 될 수 있다.

따라서 실제 V0406 profile이 terminal failure로 끝났다면 단순히 다음 Skill-Updater 주기를 기다리는 것만으로 동일 V0406가 다시 실행된다고 가정하지 않는다.

이 경우 `R23` 가능성을 반드시 판정한다.

## 8.3 `job-list-deferred`는 성공 signal이 아니다

이 signal은 activation/queue 도달 breadcrumb다.

`heartbeat-ok`가 실제 Dispatcher execution의 더 강한 증거다.

## 8.4 모든 외부 signal이 0 변화인 경우

우선순위는 다음처럼 본다.

1. activation 자체가 수행되지 않음
2. activation은 수행됐지만 signal GET transport 실패
3. Windows target/platform 판정 이상
4. signal 호출 전 install/updater 단계 실패

Dispatcher Scheduler 문제를 처음부터 1순위로 두지 않는다.

---

# 9. 최종 출력 형식

장문 보고서 금지. 진단 완료 시 아래 형식만 사용한다.

```text
[진단결과]
ROOT_CAUSE=Rxx
CONFIDENCE=1|2|3
FIRST_FAILED_STAGE=Sx
LOCAL_EXECUTION=0|1|2
SIGNAL_TRANSPORT=0|1|2
RETRYABLE_SAME_V0406=0|1|2

EVIDENCE
1. <한 줄>
2. <한 줄>
3. <한 줄>

NEXT
1. 수정안 검토
2. 추가 객관식 진단
3. 신규 Job-list 버전 필요성 검토
4. 진단 종료
```

`CONFIDENCE`

- `1` = High
- `2` = Medium
- `3` = Low

`LOCAL_EXECUTION`

- `0` = 모름
- `1` = 로컬 실행 확인
- `2` = 로컬 실행 미확인/실패

`SIGNAL_TRANSPORT`

- `0` = 모름
- `1` = 정상
- `2` = 실패/의심

`RETRYABLE_SAME_V0406`

- `0` = 모름
- `1` = queue에 남아 있어 재개 가능
- `2` = terminal processed/dedupe 때문에 동일 ID 자동 재실행 불가

EVIDENCE는 최대 3줄만 작성한다.

---

# 10. 진단 시작 지시

지금부터 아래 순서로 시작한다.

1. 먼저 고정 경로의 파일과 Scheduler 상태를 직접 읽을 수 있는지 확인한다.
2. 직접 확인 가능하면 사용자 질문 없이 S0 → S11 순서로 evidence를 수집한다.
3. 직접 확인할 수 없는 항목만 객관식으로 질문한다.
4. 첫 질문 batch는 최대 10문항이다.
5. 사용자가 숫자열로 답하면 그 답을 이용해 다음 branch만 진행한다.
6. root cause가 High confidence로 좁혀지면 추가 질문을 중단한다.
7. 수정은 시작하지 않는다.
8. 최종 결과에서 반드시 `R01~R24` 중 하나를 선택한다.

**첫 응답부터 긴 설명을 하지 말고, 자동 확인 가능한지 먼저 확인한 뒤 필요한 객관식 질문만 제시하라.**
