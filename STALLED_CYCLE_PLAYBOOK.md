# 정지된 예약 cycle 진단·복구 플레이북

대상: skill-updater 예약 cycle이 돌지 않아 원격 관측 신호가 전부 `0`인 상태.

이 문서는 특정 버전에 종속되지 않는다. 명령의 실제 형태는 설치된 버전에 따라
다를 수 있으므로, 각 단계의 **확인 기준**을 근거로 판단한다.

---

## 0. 시작 전 주의

- 진단 스크립트는 **읽기 전용**이다. 설치·설정·예약 작업을 바꾸지 않는다.
- 진단 중 **신호 asset을 브라우저로 직접 열지 않는다.** 원격 delta 측정이 오염된다.
  (관측 문서 §16-6)
- 복구 조치는 관측 구간을 오염시키므로, 조치 후에는 baseline을 다시 잡는다. (§13.2)

---

## 1. 진단 실행

스크립트를 대상 PC로 가져와 실행한다.

```powershell
curl -sL -o diagnose_stalled_cycle.py ^
  https://raw.githubusercontent.com/wonhwipark/L1Work/main/diagnose_stalled_cycle.py
python diagnose_stalled_cycle.py
```

`diagnosis_<timestamp>.json`이 생성되고 콘솔에 VERDICT가 출력된다.

---

## 2. VERDICT 코드별 조치

### `TASK_PATHS_STALE` — 가장 유력한 원인

예약 작업이 참조하는 실행 파일이 존재하지 않는다. canonical 이관 이후
`~/.claude/skills/<skill>/`에는 `SKILL.md`만 남고, `~/.claude/main/`은
retired 되기 때문에, 이관 **이전에 등록된 예약 작업**은 사라진 경로를 계속
가리킨다. 작업은 매 주기 트리거되지만 실행 파일을 못 찾아 즉시 실패한다.

증상이 조용한 것이 핵심이다. 스케줄러는 "실행했다"고 기록하지만
(`LastRunTime`이 갱신됨) 프로세스는 시작조차 못 하므로 **엔진 로그도, 원격
신호도 전혀 남지 않는다.** 결과적으로 "cycle 미실행"과 구별되지 않는다.

**조치** — 예약 작업을 현재 레이아웃 기준으로 재등록한다.

```text
skill-updater schedule install
```

`skillsilent`를 경유해야 하면:

```text
skillsilent run skill-updater schedule install
```

**확인 기준** — 재등록 후 진단 스크립트를 다시 실행해
`TASK_PATHS_STALE`이 사라지고 모든 참조 경로가 `[OK]`인지 본다.

재등록 명령이 없거나 실패하면, 기존 작업의 Action을 현재 경로로 직접 고친다.
현재 유효한 runner/YAML 위치는 진단 리포트의 `skills` 섹션에서
`canonical_root_exists=true`인 경로를 기준으로 찾는다.

### `TASK_LAUNCH_FAILED`

`LastTaskResult` 해석:

| 값 | 의미 | 조치 |
|---|---|---|
| `2` | 파일을 찾을 수 없음 | `TASK_PATHS_STALE`과 동일 |
| `267011` | 아직 실행된 적 없음 | 트리거 시각·활성 상태 확인 |
| `0x41301` | 현재 실행 중 | 정상, 완료 대기 |
| 기타 0 아님 | 실행은 됐으나 종료 코드 비정상 | 엔진 로그 확인 |

### `TASK_NOT_REGISTERED`

예약 작업 자체가 없다. `skill-updater schedule install`로 신규 등록한다.
등록 후 트리거 시각이 의도한 주기와 맞는지 확인한다.

### `TASK_DISABLED`

작업이 비활성 상태다. 스케줄러에서 활성화한다.

### `NETWORK_BLOCKED`

GitHub 호스트에 연결 자체가 안 된다. 사내망 프록시 정책 문제일 수 있다.
리포트의 `proxy_env`와 TLS 검증 결과를 함께 본다.
`TLS_UNVERIFIED`만 뜬 경우는 연결은 되는 상태이므로 차단이 아니다.

주의: HTTP 404 등 상태 코드가 돌아온 것은 **연결 성공**이다. 차단이 아니다.

### `TARGET_MISSING` / `CANARY_MISSING`

config의 `targets`에 해당 스킬이 없다. 등록되지 않은 스킬은 배포해도
처리되지 않으며, 그 스킬의 신호는 영구히 `0`이다. `CANARY_MISSING`이면
카나리아 기반 판정이 무효이므로 관측 결론을 다시 세워야 한다.

### `CONFIG_MISSING` / `CONFIG_UNREADABLE`

`skill-updater setup`으로 재구성한다. 기존 설정이 남아 있으면
보존되는지 먼저 확인한다.

---

## 3. 복구 후 검증

순서대로 수행한다.

1. **진단 재실행** — CRITICAL이 모두 해소됐는지 확인한다.

2. **수동 1회 실행** — 예약을 기다리지 않고 즉시 확인한다.

   ```text
   skillsilent run skill-updater update
   ```

   결과에서 확인할 것:
   - 대상 스킬이 `UPDATED` 또는 `SKIPPED`로 처리됐는가
   - `failed=0`인가
   - 카나리아 스킬도 목록에 포함됐는가

3. **로컬 evidence 확인** — 진단 리포트의 `job_list_evidence`가 비어 있지
   않은지, `updater_runs`에 방금 실행이 기록됐는지 본다.

4. **원격 신호 확인** — 전파 지연(최대 약 20분) 후 count를 읽는다.
   installer 단계가 증가했으면 체인 전체가 복구된 것이다.

5. **다음 예약 주기 대기** — 수동 실행이 아니라 **스케줄러 경유**로도
   동작하는지가 최종 확인이다. 수동은 되는데 예약은 안 되는 경우가
   바로 이 문제의 원래 증상이므로, 이 단계를 생략하지 않는다.

---

## 4. 관측 재개

복구 조치와 검증 실행은 모두 관측 구간을 오염시킨다.
모든 조치가 끝나고 전파가 완료된 뒤 baseline을 새로 잡는다. (§13.2)

이후 판정은 관측 문서 §13.5 판정표를 따른다.

---

## 5. 이 사례의 교훈

설치 레이아웃을 바꾸는 마이그레이션은 **그 레이아웃을 참조하는 외부 등록물**
(예약 작업, 서비스 등록, 바로가기)을 함께 갱신해야 한다. 갱신하지 않으면
마이그레이션 자체는 성공으로 보고되지만 자동화 체인은 조용히 끊긴다.

끊긴 자동화는 실패 신호를 내지 못한다. 실행 주체가 시작조차 못 하기 때문에
로그도 신호도 남기지 못하고, 원격에서는 "아무 일도 없었음"과 완전히 같아 보인다.
이런 종류의 고장은 정기적으로 **양성 확인**(성공 신호가 실제로 도착하는지)을
해야만 발견된다. 실패 신호가 없는 것을 정상으로 읽으면 안 된다.
