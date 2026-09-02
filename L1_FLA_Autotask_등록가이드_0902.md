# L1-FLA 무인 정시 실행 — Autotask-Builder 등록 가이드

대상 버전:

- `autotask-builder v0.4.23`
- `l1-fla v0.3.11`
- Linux PC
- Job-list 사용하지 않음

## 목표

지정한 시간에 OS Scheduler가 `l1-fla`를 직접 호출한다.

```text
Autotask-Builder
    ↓ 지정 시간
L1-FLA preflight
    ↓ 성공한 경우만
L1-FLA run --resume
    ↓
jira_list_tx_MMDD.md
    ↓
[FLA-SKIP] Jira 제외
    ↓
나머지 Jira만 분석
```

L1-FLA 입력 규칙은 다음과 같다.

```text
~/l1sw-private-skills/l1-fla/output/YYYYMMDD/jira_list_tx_MMDD.md
```

예:

```text
2026-09-02
→ ~/l1sw-private-skills/l1-fla/output/20260902/jira_list_tx_0902.md
```

Jira 제목이 아래처럼 시작하거나 `[FLA-SKIP]` 문자열을 포함하면 분석에서 제외한다.

```text
[FLA-SKIP] 테스트용 Jira
```

영구 skip 파일:

```text
~/l1sw-private-skills/l1-fla/data/config/exclude_jira_titles.md
```

---

# 1. 한 번에 등록

아래 블록에서 **`L1_FLA_TIME="02:00"` 한 줄만 원하는 시간으로 수정**한 뒤 Linux 터미널에 그대로 붙여넣는다.

```bash
set -e

# ============================================================
# 사용자 설정: L1-FLA 매일 실행 시간(HH:MM, 24시간제)
# ============================================================
L1_FLA_TIME="02:00"

AUTOTASK="$HOME/l1sw-private-skills/autotask-builder/bin/autotask"
TASK="$HOME/l1sw-private-skills/autotask-builder/data/config/tasks/task_l1_fla_daily.yaml"
L1_FLA="$HOME/l1sw-private-skills/l1-fla/bin/l1-fla-auto.py"

echo "============================================================"
echo "[1/7] 설치 상태 확인"
echo "============================================================"

test -x "$AUTOTASK" || {
    echo "ERROR: autotask-builder가 설치되어 있지 않습니다."
    echo "expected: $AUTOTASK"
    exit 1
}

test -f "$L1_FLA" || {
    echo "ERROR: l1-fla가 설치되어 있지 않습니다."
    echo "expected: $L1_FLA"
    exit 1
}

echo
echo "============================================================"
echo "[2/7] Autotask 환경 진단"
echo "============================================================"

"$AUTOTASK" doctor

echo
echo "============================================================"
echo "[3/7] L1-FLA daily task 생성/갱신"
echo "실행 시간: $L1_FLA_TIME"
echo "============================================================"

"$AUTOTASK" preset l1-fla-daily \
    --time "$L1_FLA_TIME" \
    --profile default \
    --force

echo
echo "============================================================"
echo "[4/7] 생성된 task 검증"
echo "============================================================"

"$AUTOTASK" check "$TASK"

echo
echo "============================================================"
echo "[5/7] L1-FLA 자체 preflight"
echo "※ 실제 Jira 분석은 시작하지 않음"
echo "============================================================"

python3 "$L1_FLA" \
    preflight \
    --profile default \
    --daily-issue-list \
    --json

echo
echo "============================================================"
echo "[6/7] OS Scheduler 등록"
echo "============================================================"

"$AUTOTASK" deploy "$TASK" --yes

echo
echo "============================================================"
echo "[7/7] 최종 상태 확인"
echo "============================================================"

"$AUTOTASK" status

echo
echo "============================================================"
echo "L1-FLA daily task 등록 완료"
echo "TIME : $L1_FLA_TIME"
echo "TASK : $TASK"
echo "============================================================"
```

---

# 2. 등록 후 기대 동작

등록된 task는 매일 지정 시간에 아래 순서로 실행된다.

```text
1. l1-fla preflight
2. preflight 성공 여부 확인
3. 실패/BLOCKED
   → 종료
   → 본 분석 시작하지 않음
4. preflight 성공
   → l1-fla run --resume
5. 당일 jira_list_tx_MMDD.md만 사용
6. Jira title skip 목록 적용
7. 대상 Jira만 분석
```

Autotask task의 실제 핵심 내용:

```yaml
steps:
  - kind: script
    name: l1-fla preflight
    run: "~/l1sw-private-skills/l1-fla/bin/l1-fla-auto.py"
    args:
      - preflight
      - --profile
      - default
      - --daily-issue-list
      - --json
    timeout_sec: 600

  - kind: script
    name: l1-fla unattended run
    run: "~/l1sw-private-skills/l1-fla/bin/l1-fla-auto.py"
    args:
      - run
      - --profile
      - default
      - --daily-issue-list
      - --resume
      - --json
    timeout_sec: 14400
```

따라서 Job-list는 이 정기 실행에 관여하지 않는다.

---

# 3. L1-FLA 입력 파일

매일 아래 파일만 분석 대상으로 사용한다.

```text
jira_list_tx_MMDD.md
```

예:

```text
09/02 → jira_list_tx_0902.md
09/03 → jira_list_tx_0903.md
09/04 → jira_list_tx_0904.md
```

파일 위치:

```text
~/l1sw-private-skills/l1-fla/output/YYYYMMDD/
```

예:

```text
~/l1sw-private-skills/l1-fla/output/20260902/jira_list_tx_0902.md
```

같은 폴더에 다른 `.md`가 있어도 `--daily-issue-list`에서는 위 패턴을 기준으로 선택한다.

---

# 4. Jira 분석 제외 규칙

표준 skip prefix:

```text
[FLA-SKIP]
```

영구 저장 파일:

```text
~/l1sw-private-skills/l1-fla/data/config/exclude_jira_titles.md
```

기본 예:

```markdown
# L1-FLA persistent Jira title skip list

- [FLA-SKIP]
```

추가 skip 문자열도 한 줄씩 넣을 수 있다.

```markdown
- [FLA-SKIP]
- automation dummy
- RF calibration
```

매칭 방식:

```text
대소문자 무시
+
부분 문자열 매칭
```

예:

```text
[FLA-SKIP] NR TX test issue
→ SKIP

NR automation dummy regression
→ SKIP
```

기존 영구 skip 목록은 autotask-builder task를 다시 등록해도 삭제되지 않는다.

---

# 5. 현재 등록 상태만 확인

```bash
"$HOME/l1sw-private-skills/autotask-builder/bin/autotask" status
```

---

# 6. Task YAML 확인

```bash
cat "$HOME/l1sw-private-skills/autotask-builder/data/config/tasks/task_l1_fla_daily.yaml"
```

---

# 7. 실행 시간 변경

예: 매일 `01:30`으로 변경.

```bash
AUTOTASK="$HOME/l1sw-private-skills/autotask-builder/bin/autotask"
TASK="$HOME/l1sw-private-skills/autotask-builder/data/config/tasks/task_l1_fla_daily.yaml"

"$AUTOTASK" preset l1-fla-daily \
    --time "01:30" \
    --profile default \
    --force

"$AUTOTASK" check "$TASK"
"$AUTOTASK" deploy "$TASK" --yes
"$AUTOTASK" status
```

---

# 8. 즉시 1회 시험 — 선택 사항

주의:

아래 명령은 단순 검증이 아니라 **preflight가 성공하면 실제 L1-FLA 분석까지 수행**한다.

```bash
AUTOTASK="$HOME/l1sw-private-skills/autotask-builder/bin/autotask"
TASK="$HOME/l1sw-private-skills/autotask-builder/data/config/tasks/task_l1_fla_daily.yaml"

"$AUTOTASK" run "$TASK"
```

등록만 확인하려면 이 명령은 수행할 필요 없다.

---

# 9. 문제 발생 시 최소 확인 명령

```bash
AUTOTASK="$HOME/l1sw-private-skills/autotask-builder/bin/autotask"
L1_FLA="$HOME/l1sw-private-skills/l1-fla/bin/l1-fla-auto.py"

"$AUTOTASK" doctor
"$AUTOTASK" check
"$AUTOTASK" status

python3 "$L1_FLA" \
    preflight \
    --profile default \
    --daily-issue-list \
    --json
```

Autotask 영구 저장 위치:

```text
~/l1sw-private-skills/autotask-builder/data/
```

Autotask 로그 위치:

```text
~/l1sw-private-skills/autotask-builder/output/log/
```

L1-FLA 영구영역:

```text
~/l1sw-private-skills/l1-fla/
```

---

# 최종 운영 구조

```text
Autotask-Builder
│
├─ 매일 지정 시간
│
└─ L1-FLA
    │
    ├─ preflight
    │    └─ 실패 시 여기서 종료
    │
    └─ run --resume
         │
         ├─ jira_list_tx_MMDD.md
         │
         ├─ Jira 조회
         │
         ├─ [FLA-SKIP] 제외
         │
         ├─ 로그 다운로드
         │
         ├─ issue-analyzer
         │
         └─ 결과 저장

Job-list: 사용하지 않음
Dispatcher: 필요 시 결과 관측용
```
