# 회사 PC에서 여기부터 시작

아무것도 기억하지 않아도 됩니다. 위에서부터 그대로 따라 하세요.

---

## 배경 (30초)

skill-updater 예약 작업이 매 주기(00:07 / 04:07 / 08:07 / 12:07 / 16:07)
트리거되지만 **아무 일도 일어나지 않고 있습니다.** 로그도, 설치도, 원격 신호도
전혀 없습니다.

원인 후보 1순위는 이겁니다. 개인 PC에서 **같은 증상을 재현하고 실제로 확인했습니다.**

> 예약 작업이 `~/.claude/skills/<skill>/runners/...` 같은 경로를 가리키는데,
> canonical 이관 이후 그 경로에는 `SKILL.md`만 남아 실행 파일이 사라졌습니다.
> 작업은 매번 트리거되지만 프로세스가 시작조차 못 하고 즉시 죽습니다.
> (Windows 작업 결과 코드 `2` = 파일을 찾을 수 없음)

**조용히 실패하는 게 핵심입니다.** 실행 주체가 시작을 못 하니 로그도 신호도
안 남고, 원격에서는 "아무 일도 없었음"과 완전히 똑같이 보입니다.

---

## 1단계. 진단 (2분)

PowerShell을 열고 그대로 붙여넣으세요.

```powershell
curl -sL -o diagnose_stalled_cycle.py https://raw.githubusercontent.com/wonhwipark/L1Work/main/diagnose_stalled_cycle.py
python diagnose_stalled_cycle.py
```

- 읽기 전용입니다. 설치·설정·예약작업을 **바꾸지 않습니다.**
- 화면 맨 아래 `VERDICT` 부분을 보세요.
- `diagnosis_<시각>.json` 파일이 같은 폴더에 저장됩니다. **이 파일을 보관하세요.**

---

## 2단계. VERDICT 코드별 조치

### `TASK_PATHS_STALE` 또는 `TASK_LAUNCH_FAILED` (가장 유력)

예약 작업을 현재 레이아웃 기준으로 재등록합니다.

```
skillsilent run skill-updater schedule install
```

위 명령이 안 되면 이것도 시도해 보세요.

```
skill-updater schedule install
```

**확인**: 진단을 다시 실행해서 모든 참조 경로가 `[OK]`로 바뀌었는지 봅니다.

```powershell
python diagnose_stalled_cycle.py
```

### `TASK_NOT_REGISTERED`

예약 작업 자체가 없습니다. 위와 같은 `schedule install`로 신규 등록합니다.

### `TASK_DISABLED`

작업 스케줄러에서 해당 작업을 활성화합니다.

### `NETWORK_BLOCKED`

GitHub 접근이 사내망에서 막혀 있습니다. 프록시 설정 확인이 필요합니다.
(주의: HTTP 404 같은 응답은 **차단이 아닙니다.** 연결은 성공한 것입니다.)

### `CONFIG_MISSING` / `CONFIG_UNREADABLE`

```
skill-updater setup
```

### 그 외 / 판단이 안 설 때

`diagnosis_<시각>.json` 내용을 복사해 두었다가 붙여넣어 주시면 판독해 드립니다.
더 자세한 절차는 아래에서 받을 수 있습니다.

```powershell
curl -sL -o STALLED_CYCLE_PLAYBOOK.md https://raw.githubusercontent.com/wonhwipark/L1Work/main/STALLED_CYCLE_PLAYBOOK.md
```

---

## 3단계. 복구 확인 (가장 중요 — 생략하지 마세요)

**수동 실행이 되는 것과 예약 실행이 되는 것은 다릅니다.**
어제 개인 PC에서도 수동은 잘 됐지만 예약은 계속 죽어 있었습니다.
그게 이 문제의 원래 증상입니다.

### 3-1. 수동으로 1회 실행

```
skillsilent run skill-updater update
```

결과에서 볼 것:
- `failed=0` 인가
- job-list가 `UPDATED` 또는 `SKIPPED`로 처리됐는가
- l1_fla도 목록에 있는가

### 3-2. 다음 예약 주기까지 기다린 뒤 확인

예약 주기는 00:07 / 04:07 / 08:07 / 12:07 / 16:07 입니다.
해당 시각이 지난 뒤 진단을 다시 실행해서, 예약 작업의
`last_result`가 `0`이고 실행 시각이 갱신됐는지 확인합니다.

```powershell
python diagnose_stalled_cycle.py
```

---

## 하지 말아야 할 것

**브라우저로 아래 주소의 파일들을 직접 열거나 다운로드하지 마세요.**

```
https://github.com/wonhwipark/Fail/releases/tag/signal-v1
```

이 파일들의 다운로드 횟수가 원격 판정의 근거입니다. 수동으로 열면 카운터가
올라가서 "실제로 실행됐는지"를 구분할 수 없게 됩니다. 페이지를 보는 것은
괜찮지만, **파일을 클릭해서 받지 마세요.**

---

## 돌아와서 알려주실 것

아래 세 가지를 확인해 주시면 나머지 미해결 건까지 정리됩니다.

1. `diagnosis_<시각>.json` 파일 내용 (또는 VERDICT 부분만이라도)
2. **사내 PC의 job-list 설치 버전** — 진단 리포트의 `skills` 섹션에 나옵니다
3. **job_sync 활성 여부** — 진단 리포트의 `updater_config.job_sync_enabled`

참고로 job-list 최신 버전(어제 배포)에는 job_sync가 꺼져 있으면 자동으로
켜주는 기능이 들어갔습니다. 개인 PC에서 실제로 동작을 확인했습니다.
