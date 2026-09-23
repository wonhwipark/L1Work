# RooCode — Off-site Windows Dispatcher Signal Check for Job-list v0.3.91

## 0. 목적

휴일/사외 환경에서 회사 Windows PC에 직접 접속하지 않고,
기존 `l1sw-dispatcher v0.3.11`이 보내는 GitHub Release signal의 `download_count` 변화만으로
다음 흐름을 READ-ONLY로 확인한다.

```text
Skill Updater
  -> job-list v0.3.91 감지/설치
  -> V0391 one-shot activation
  -> Job-list Windows worker
  -> CL-AIT HLD quality-upgrade
  -> final Job-list observer receipt
  -> Job-list가 기존 Dispatcher cycle을 best-effort 1회 호출
  -> Dispatcher Windows signal count 변화
```

Dispatcher 자체는 업데이트/수정하지 않는다.

---

## 1. 절대 금지

사외 확인 과정에서는 아래를 하지 않는다.

- signal asset의 `browser_download_url`을 직접 GET/download 하지 않는다.
- `dispatcher-windows-*.signal` 파일을 다운로드하지 않는다.
- GitHub Release asset을 수정/삭제/재업로드하지 않는다.
- 회사 PC로 command/queue를 보내지 않는다.
- Job-list/Skill Updater를 원격에서 재실행하지 않는다.

이유:
Dispatcher의 외부 신호는 해당 Release asset GET이 발생할 때 `download_count`가 증가하는 방식이다.
사외 모니터가 asset 자체를 다운로드하면 측정값을 오염시킨다.

**사외에서는 GitHub Release API의 asset metadata만 읽는다.**

---

## 2. Signal source

Dispatcher v0.3.11 signal release:

```text
repository : wonhwipark/Fail
release tag: signal-v1
```

GitHub REST metadata endpoint:

```text
repos/wonhwipark/Fail/releases/tags/signal-v1
```

가능하면 인증된 `gh api`를 사용한다.
Public/API 접근이 가능한 경우 read-only REST GET도 허용한다.

---

## 3. 이번 확인에 필요한 Windows 핵심 signal

필수:

```text
dispatcher-windows-heartbeat-ok.signal

dispatcher-windows-skill-updater-ok.signal
dispatcher-windows-skill-updater-fail.signal

dispatcher-windows-job-list-ok.signal
dispatcher-windows-job-list-fail.signal
dispatcher-windows-job-list-deferred.signal
```

보조:

```text
dispatcher-windows-autotask-ok.signal
dispatcher-windows-autotask-error.signal
```

`heartbeat-stale`은 회사 PC가 멈추었을 때 스스로 보낼 수 있는 신호가 아니므로
STALE 판단에 사용하지 않는다.
STALE은 `heartbeat-ok` count가 일정 관측 구간 동안 증가하지 않는 것으로 사외에서 판정한다.

---

## 4. RooCode 1차 실행 — Job 예상 시각 전 baseline

RooCode에 아래 작업을 수행시킨다.

```text
READ-ONLY 작업만 수행한다.

GitHub Release API를 사용하여
repo=wonhwipark/Fail, tag=signal-v1 의 asset metadata를 조회한다.

중요:
- asset 자체를 download하지 말 것.
- browser_download_url GET 금지.
- Release API metadata만 읽을 것.

아래 Windows signal의 name, asset id, download_count를 추출한다.

1. dispatcher-windows-heartbeat-ok.signal
2. dispatcher-windows-skill-updater-ok.signal
3. dispatcher-windows-skill-updater-fail.signal
4. dispatcher-windows-job-list-ok.signal
5. dispatcher-windows-job-list-fail.signal
6. dispatcher-windows-job-list-deferred.signal
7. dispatcher-windows-autotask-ok.signal
8. dispatcher-windows-autotask-error.signal

현재 시각과 함께 다음 파일로 저장한다.

DISPATCHER_SIGNAL_BEFORE_V0391.json

형식:
{
  "captured_at": "ISO-8601",
  "repo": "wonhwipark/Fail",
  "tag": "signal-v1",
  "signals": {
    "dispatcher-windows-heartbeat-ok.signal": {
      "asset_id": 0,
      "download_count": 0
    }
  }
}

마지막에 사람이 보기 쉬운 baseline 표도 출력한다.
```

### `gh` 사용 예시

RooCode가 shell을 사용할 수 있다면 다음과 같은 **metadata API** 형태를 사용한다.

```bash
gh api repos/wonhwipark/Fail/releases/tags/signal-v1
```

직접 Release asset URL을 `curl -L` 하는 방식은 사용하지 않는다.

---

## 5. 중간 확인 — Skill Updater 예상 실행 이후

Job 자체가 끝나기 전이라도 Skill Updater 단계가 통과했는지 먼저 구분할 수 있다.

baseline과 동일한 방식으로 API metadata를 다시 읽고 delta를 계산한다.

### 기대 신호

정상 updater cycle이 관측되었다면 일반적으로:

```text
heartbeat-ok        delta > 0
skill-updater-ok    delta > 0
skill-updater-fail  delta = 0
```

해석:

| 상태 | 해석 |
|---|---|
| heartbeat `+` / updater-ok `+` | Dispatcher와 Skill Updater 관측이 살아 있음 |
| heartbeat `+` / updater-fail `+` | Updater cycle 자체가 실패 상태로 관측됨 |
| heartbeat `+` / updater 변화 없음 | Dispatcher는 살아 있으나 아직 새 updater event가 없거나 schedule 이전 |
| heartbeat 변화 없음 | 회사 PC/Dispatcher cycle/외부 GET 경로 중 하나가 관측되지 않음 |

주의:
`skill-updater-ok`만으로 V0391 Job이 실제 queue/완료됐다고 판단하지 않는다.
최종적으로 `job-list-*` 변화를 확인해야 한다.

---

## 6. Job-list 동작 예상시간 이후 2차 확인

다시 동일 API metadata를 읽어 다음 파일을 생성한다.

```text
DISPATCHER_SIGNAL_AFTER_V0391.json
DISPATCHER_SIGNAL_DIFF_V0391.md
```

`DIFF`에는 반드시 다음 표를 만든다.

```text
SIGNAL | BEFORE | AFTER | DELTA | 판정
```

### Job-list 핵심 판정

#### A. 정상 완료 신호

```text
job-list-ok delta > 0
job-list-fail delta = 0
job-list-deferred delta = 0
```

그리고 같은 관측 구간에 heartbeat도 증가했다면:

```text
Dispatcher observer cycle 정상
+
새 Job-list PASS receipt 관측
```

으로 판단한다.

v0.3.91은 final Job-list observer receipt 기록 후 Windows에서 기존 Dispatcher의 `cycle`을
best-effort로 한 번 호출하므로, Dispatcher가 정상 설치되어 있으면 final signal 반영 지연을 줄인다.
이 호출 실패/Dispatcher 부재는 Job-list 자체 결과를 실패로 바꾸지 않는다.

#### B. Job 실패

```text
job-list-fail delta > 0
```

판정:

```text
Job-list worker 또는 target Job 결과가 FAIL receipt로 관측됨
```

#### C. Deferred

```text
job-list-deferred delta > 0
```

판정:

```text
Job-list가 실행을 완료한 것이 아니라 deferred 상태로 관측됨
```

#### D. Updater 성공 신호는 있는데 Job signal 변화 없음

```text
skill-updater-ok delta > 0
heartbeat delta > 0
job-list-ok/fail/deferred delta = 0
```

초기 판정:

```text
Updater event는 관측되었으나 새로운 Job-list final receipt는 아직 관측되지 않음
```

가능 범위:

- HLD Job이 아직 RUNNING
- activation/queue/worker 단계에서 final receipt 이전
- Dispatcher의 post-receipt best-effort cycle이 실패했고 다음 natural Dispatcher cycle 전
- Job-list handoff 문제

이 경우 `FAIL`로 즉시 단정하지 않는다.
추가 heartbeat cycle 이후에도 job-list signal이 계속 변하지 않는지 비교한다.

#### E. heartbeat는 계속 증가하지만 Updater/Job 모두 변화 없음

```text
heartbeat delta > 0
skill-updater delta = 0
job-list delta = 0
```

판정:

```text
Dispatcher는 살아 있음.
해당 관측 구간에서 새로운 Updater/Job-list event가 보이지 않음.
```

---

## 7. v0.3.91 실행시간 관련 기준

현재 `cl-ait-hld-quality-upgrade-windows` profile의 설정은:

```text
timeout_sec = 28800  # 8 hours / attempt
retry       = 1
```

따라서 signal 확인을 두 단계로 나눈다.

1. **Updater 확인:** 예정된 Skill Updater cycle 직후 비교
2. **Job final 확인:** 실제 HLD 작업 완료 예상 이후 비교

첫 attempt의 hard timeout은 8시간이고 retry 1회가 허용되므로,
비정상 timeout/retry까지 포함하면 두 attempt가 수행될 수 있다.
이 값은 실제 소요시간 예측이 아니라 Job-list에 설정된 실행 상한이다.

---

## 8. RooCode 최종 판정 출력 형식

두 snapshot을 비교한 뒤 아래 형식으로만 요약한다.

```text
V0391 OFF-SITE OBSERVATION

Baseline captured : <time>
After captured    : <time>

Dispatcher heartbeat : ALIVE / NO_NEW_HEARTBEAT
Skill Updater         : NEW_OK / NEW_FAIL / NO_NEW_EVENT
Job-list              : NEW_OK / NEW_FAIL / NEW_DEFERRED / NO_NEW_FINAL_EVENT

Signal deltas:
- heartbeat-ok       : +N
- skill-updater-ok   : +N
- skill-updater-fail : +N
- job-list-ok        : +N
- job-list-fail      : +N
- job-list-deferred  : +N
- autotask-ok        : +N
- autotask-error     : +N

Interpretation:
<evidence-based 3~6 lines>

Next local evidence needed:
<없으면 NONE, 있으면 회사 PC 복귀 후 확인할 정확한 파일명만>
```

---

## 9. 판정 시 주의사항

- `download_count` 자체에는 마지막 다운로드 시각이 없다.
- 따라서 `last_seen`은 **사외 baseline/after 비교 시각**으로 관리한다.
- asset `updated_at`을 Dispatcher last-seen 시각으로 해석하지 않는다.
- 사외 측에서 asset 자체를 다운로드하면 count가 증가해 결과가 오염되므로 금지한다.
- `job-list-ok`은 Job-list final receipt의 PASS 관측이다. CL-AIT HLD 문서 품질을 사외 signal만으로 세부 검증하는 신호는 Dispatcher v0.3.11에 없다.
- 이번 목적은 **Updater -> Job-list -> final receipt까지 살아 있는지**를 사외에서 판별하는 것이다.

---

## 10. 이번 v0.3.91에서 기대하는 최소 변화

정상 end-to-end라면 baseline 대비 최소한 다음 흐름이 보여야 한다.

```text
heartbeat-ok        증가
skill-updater-ok    증가
job-list-ok         증가
```

반대로 가장 중요한 이상 패턴은:

```text
heartbeat 증가
skill-updater-ok 증가
job-list signal 변화 없음
```

이다.

이 경우 회사 PC 복귀 후 최우선 local evidence는:

```text
~/l1sw-private-skills/job-list/data/state/activation/latest.json
~/l1sw-private-skills/job-list/data/state/activation/history.jsonl
~/l1sw-private-skills/job-list/data/state/core/queue.json
~/l1sw-private-skills/job-list/data/state/core/processed.jsonl
~/l1sw-private-skills/job-list/data/state/observer/current_run.json
~/l1sw-private-skills/job-list/data/state/observer/latest_result.json
~/l1sw-private-skills/job-list/output/core/last_run.json
```

이다.
