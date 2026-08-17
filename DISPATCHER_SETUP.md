# dispatcher 설치 (복구 완료 후에 진행)

## 먼저 확인

**`TOMORROW_START_HERE.md`의 복구가 끝난 뒤에 하세요.** 예약 실행이 아직 안 되는 상태에서 dispatcher를 얹으면 무엇이 문제인지 구분이 어려워집니다.

dispatcher는 개인 PC에서 5단계 검증을 통과했지만 사내 환경에서는 처음 도는 것입니다. 시간이 없으면 오늘은 건너뛰고 복구만 하셔도 됩니다.

---

## 1. 받기

```powershell
cd $env:USERPROFILE
mkdir l1sw-dispatcher-bin -Force
cd l1sw-dispatcher-bin
curl -sL -o l1sw_dispatcher.py https://raw.githubusercontent.com/wonhwipark/L1Work/main/l1sw_dispatcher.py
```

**스킬 트리 바깥에 두는 것이 중요합니다.** `~/.claude/skills/` 나 `~/l1sw-private-skills/` 안에 두면 canonical 이관 때 경로가 끊깁니다. 오늘 고치러 가시는 그 고장이 정확히 그것입니다.

---

## 2. 설치

```powershell
python l1sw_dispatcher.py install --interval-min 30
python l1sw_dispatcher.py status
```

`status`에서 확인할 것:

```text
registration    : 정상                      <- 이게 아니면 경로 문제
battery         : 안전 (배터리에서도 동작)   <- '위험'이면 아래 참고
next_run        : (30분 뒤)
```

### 이미 예전 버전으로 설치했다면 반드시 재설치하세요

초기 버전은 예약 작업을 만들 때 Windows 기본 전원 설정을 그대로 물려받았습니다.
그 설정은 **배터리 전원에서 작업 시작을 거부**하므로, 노트북에서 전원 케이블을
빼는 순간 dispatcher가 조용히 멈춥니다. 스케줄러는 실행 시각과 거부 코드
(`0x800710E0`)를 기록하지만 프로세스는 시작되지 않아 **로그도 신호도 남지
않습니다.** 이 도구가 잡아내려는 바로 그 유형의 고장입니다.

최신 스크립트로 아래를 다시 실행하면 해결됩니다.

```powershell
curl -sL -o l1sw_dispatcher.py https://raw.githubusercontent.com/wonhwipark/L1Work/main/l1sw_dispatcher.py
python l1sw_dispatcher.py install --interval-min 30
python l1sw_dispatcher.py status     # battery 항목이 '안전'인지 확인
```

`status`의 `battery`가 `위험`으로 남아 있으면 알려주세요.

---

## 3. 검증 (반드시)

### 3-1. 스케줄러 경유 실행

```powershell
schtasks /run /tn "l1sw-dispatcher"
```

30초 뒤:

```powershell
python l1sw_dispatcher.py status
Get-Content "$env:USERPROFILE\l1sw-dispatcher\dispatcher.log" -Tail 5 -Encoding UTF8
```

**`last_result`가 `0`이어야 합니다.** `2`면 경로 문제입니다.

수동 실행(`python l1sw_dispatcher.py run`)이 되는 것과 예약 실행이 되는 것은 다릅니다. 반드시 위 방식으로 확인하세요.

### 3-2. 창이 뜨는지

실행 중 cmd 창이나 PowerShell 창이 튀어나오면 안 됩니다. 뜨면 알려주세요.

---

## 4. 기존 예약 작업과의 관계

기존 `autotask-skill_update` 계열이 살아 있으면 **엔진을 호출하는 주체가 둘**이 됩니다. 동시에 돌면 겹칠 수 있습니다.

권장: 복구된 기존 작업을 당분간 그대로 두고 dispatcher를 관찰만 하세요. dispatcher가 안정적으로 도는 것이 확인되면 그때 기존 작업 정리를 검토합니다.

dispatcher에는 중복 실행 잠금이 있어 자기 자신끼리는 겹치지 않지만, 다른 경로로 실행된 엔진과는 겹칠 수 있습니다.

---

## 5. 사용법

### 사외에서 실행 걸기

개인 PC에서:

```powershell
python l1sw_dispatcher.py make-trigger --note "무슨 작업인지"
```

출력된 JSON을 `automation/trigger.json` 으로 업로드하면 됩니다.

사내 PC가 감지하기까지: **파일 반영 2~3분 + 최대 한 주기(30분)**

### 주기 바꾸기

```powershell
# 사내 PC에서
python l1sw_dispatcher.py install --interval-min 60

# 사외에서: trigger.json 에 "interval_min": 60 포함
```

허용 범위는 10~240분이며 벗어나면 자동으로 제한됩니다.

### 제거

```powershell
python l1sw_dispatcher.py uninstall
```

---

## 6. 원격에서 확인되는 것

| 신호 | 의미 |
|---|---|
| `dispatcher-heartbeat` | 살아 있음. **매 사이클 무조건** |
| `dispatcher-trigger-fired` | 요청을 감지해 실행 시작 |
| `dispatcher-engine-ok` / `-fail` | 엔진 결과 |
| `dispatcher-selfheal` | 등록이 깨져 자동 복구함 (원인 조사 대상) |

**heartbeat가 증가하는데 나머지가 0이면 정상입니다** (살아 있고 할 일 없음).
**heartbeat가 0이면 고장입니다.** 이 구분이 dispatcher를 만든 이유입니다.

주의: heartbeat 증가량을 사이클 수로 해석하지 마세요. 반영에 시간이 걸려 스냅샷 하나로는 판단할 수 없습니다. **증가했는지 여부만** 봅니다.

---

## 7. 문제 생기면

```powershell
python l1sw_dispatcher.py status
Get-Content "$env:USERPROFILE\l1sw-dispatcher\dispatcher.log" -Tail 30 -Encoding UTF8
```

이 두 출력을 알려주시면 진단해 드립니다. 급하면 `uninstall` 로 되돌리면 되고, 기존 예약 작업에는 영향이 없습니다.

상세 설계와 판정 기준은 `remote_trigger_and_liveness_mechanism.md` 에 있습니다.
