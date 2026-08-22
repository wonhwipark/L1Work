# L1SW Linux One-shot 시험 준비 + 실행 통합 프롬프트

아래 내용을 회사 Linux PC의 OpenCode / Claude Code 등에 **그대로 한 번에 붙여넣어 실행**한다.

---

## 실행 프롬프트

너는 L1SW 야간 무인 자동화의 **Linux one-shot 시험 준비 및 검증 수행자**다.

현재 상황:

- 회사 PC OS: **Linux**
- Skill-Updater로 Job-list 업데이트는 성공함
- 하지만 Study Runner가 실행되지 않음
- 기존 시험 Job `JOB-20260822-TEST001`은 `platform: windows`였으므로 Linux에서 실행되지 않는 것이 정상
- 다음 시험은 Linux용 새 Job ID를 사용해야 함
- Job-list의 `l1-study` profile은 기본적으로 disabled일 수 있음
- 현재 profile의 `base_dir: "%L1_CODE_ROOT%"` 표기는 Linux에서 정상 expand되지 않을 수 있으므로 실제 Linux 절대경로를 사용한다

이번 작업의 목적:

```text
회사 Linux PC 환경 준비
    ↓
l1-study profile 활성화
    ↓
실제 smp1900 코드 경로 연결
    ↓
Job-list validate
    ↓
다음 Linux one-shot Job을 받을 준비 완료
```

이번 단계에서는 기존 processed/receipt/state를 임의 삭제하지 않는다.

---

# 1. 현재 설치 경로 확인

기준 경로:

```text
~/l1sw-private-skills/
```

다음 Skill의 존재 여부와 VERSION을 확인한다.

```text
skill-updater
job-list
l1-study-runner
l1sw-dispatcher 또는 dispatcher
```

기대 버전:

```text
skill-updater      0.5.25
job-list           0.3.44 이상
l1-study-runner    0.2.4
dispatcher         0.3.3
```

버전이 다르더라도 바로 변경하지 말고 먼저 현재 상태를 보고한다.

---

# 2. Linux 코드 checkout 경로 찾기

현재 사용 중인 `smp1900` checkout root를 확인한다.

가능하면 기존 환경변수부터 확인한다.

```bash
echo "$L1_CODE_ROOT"
```

비어 있으면 아래처럼 실제 checkout 후보를 찾는다.

```bash
find "$HOME" -maxdepth 4 -type d -name smp1900 2>/dev/null | head -20
```

또는 기존 개발 환경/설정에서 checkout root를 확인한다.

최종적으로 반드시 아래 target이 존재해야 한다.

```text
<실제 smp1900 root>/SMPF/LTE_TX
```

검증:

```bash
test -d "<실제 smp1900 root>/SMPF/LTE_TX" && echo PASS || echo FAIL
```

FAIL이면 임의의 다른 target으로 바꾸지 말고:

```text
BLOCKED
Reason: SMPF/LTE_TX target not found
```

로 보고하고 중단한다.

---

# 3. L1_CODE_ROOT 영구 설정

실제 smp1900 root가 예를 들어:

```text
/home/user/github/smp1900
```

이라면 현재 shell에 먼저 설정한다.

```bash
export L1_CODE_ROOT="/home/user/github/smp1900"
```

그리고 shell 재접속 후에도 유지되도록 현재 shell 환경에 맞는 startup file에 저장한다.

bash 사용 시 예:

```bash
grep -q 'export L1_CODE_ROOT=' ~/.bashrc \
  && sed -i 's|^export L1_CODE_ROOT=.*|export L1_CODE_ROOT="/home/user/github/smp1900"|' ~/.bashrc \
  || echo 'export L1_CODE_ROOT="/home/user/github/smp1900"' >> ~/.bashrc
```

단, **실제 경로로 치환해서 사용**한다.

설정 후:

```bash
echo "$L1_CODE_ROOT"
test -d "$L1_CODE_ROOT/SMPF/LTE_TX" && echo TARGET_PASS || echo TARGET_FAIL
```

---

# 4. Job-list `l1-study` profile 활성화

파일:

```text
~/l1sw-private-skills/job-list/data/config/overnight-profiles.json
```

백업은 1회만 만든다.

```bash
cp ~/l1sw-private-skills/job-list/data/config/overnight-profiles.json \
   ~/l1sw-private-skills/job-list/data/config/overnight-profiles.json.bak_0822
```

이미 백업이 있다면 덮어쓰지 않는다.

현재 `l1-study` profile을 확인한다.

```bash
python - <<'PY'
import json
from pathlib import Path

p = Path.home() / "l1sw-private-skills/job-list/data/config/overnight-profiles.json"
data = json.loads(p.read_text(encoding="utf-8"))
print(json.dumps(data.get("l1-study"), indent=2, ensure_ascii=False))
PY
```

다음 두 조건을 만족하도록 최소 수정한다.

```text
enabled = true
base_dir = 실제 smp1900 Linux 절대경로
```

중요:

```text
"%L1_CODE_ROOT%"
```

를 그대로 사용하지 않는다.

Linux에서는 실제 절대경로를 넣는다.

예:

```json
"l1-study": {
  "enabled": true,
  "parameters": {
    "target": {
      "flag": "--target",
      "type": "relative_path",
      "required": true,
      "base_dir": "/home/user/github/smp1900",
      "must_exist": true,
      "max_length": 240
    }
  }
}
```

기존 profile의 다른 필드는 임의 삭제하거나 변경하지 않는다.

Python으로 안전하게 필요한 값만 수정해도 된다.

수정 후 다시 출력해서 확인한다.

---

# 5. Job-list validation

실행:

```bash
python ~/l1sw-private-skills/job-list/scripts/job_core.py validate
```

기대:

```text
status = PASS
errors = []
```

FAIL이면 다음 단계로 진행하지 않는다.

보고:

```text
BLOCKED
Component: Job-list profile validation
Cause: ...
```

---

# 6. Study Runner preflight

경로 이동:

```bash
cd ~/l1sw-private-skills/l1-study-runner
```

현재 제공되는 Linux용 preflight/help를 먼저 확인한다.

```bash
ls
```

가능한 preflight Python 또는 shell entrypoint가 있으면 그것을 사용한다.

Windows 전용 `.ps1`은 Linux에서 실행하지 않는다.

SKILL.md / README / `--help`를 확인해서 Linux에서 지원하는 실제 preflight 방법을 사용한다.

최소한 다음은 확인한다.

```text
Study Runner entrypoint 존재
Code Analyzer 접근 가능
Knowledge Manager 접근 가능
target root 접근 가능
```

실제 학습은 아직 실행하지 않는다.

---

# 7. 기존 TEST001 상태 확인

기존 시험 Job:

```text
JOB-20260822-TEST001
```

은 `platform: windows`였으므로 Linux에서:

```text
TARGET_MISMATCH
```

처리되는 것이 정상이다.

아래 상태를 확인한다.

```bash
python ~/l1sw-private-skills/job-list/scripts/job_core.py status
```

그리고 필요하면:

```bash
cat ~/l1sw-private-skills/job-list/data/state/activation/latest.json
tail -20 ~/l1sw-private-skills/job-list/data/state/core/processed.jsonl
cat ~/l1sw-private-skills/job-list/data/state/observer/latest_result.json
```

중요:

- TEST001을 억지로 다시 실행하지 않는다
- processed/state 파일을 삭제하지 않는다
- TEST001을 재사용하지 않는다

---

# 8. 다음 Linux 시험 Job 규칙

다음 시험은 새 Job ID를 사용한다.

권장:

```text
JOB-20260822-TEST002
```

Job 내용:

```json
{
  "job_id": "JOB-20260822-TEST002",
  "platform": "linux",
  "profile": "l1-study",
  "params": {
    "target": "SMPF/LTE_TX"
  }
}
```

Linux PC에서는:

```text
platform = linux
→ enqueue 허용
```

Windows PC에서는:

```text
platform mismatch
→ TARGET_MISMATCH
→ queue에 넣지 않음
→ consumed 처리하지 않음
```

---

# 9. 다음 Job-list update 후 기대 동작

다음 Linux 시험용 Job-list 새 버전이 GitHub에 올라오면:

```text
Skill-Updater
    ↓
Job-list 새 버전 설치
    ↓
TEST002 감지
    ↓
platform=linux 확인
    ↓
l1-study enabled 확인
    ↓
target 존재 확인
    ↓
PENDING
    ↓
detached worker
    ↓
Study Runner
    ↓
SMPF/LTE_TX
    ↓
CONSUMED + receipt
```

Skill-Updater는 Study Runner 완료까지 기다리면 안 된다.

---

# 10. 퇴근 전 최종 확인

아래 항목만 확인되면 회사 PC 준비 완료로 판정한다.

```text
[ ] Linux PC 확인
[ ] L1_CODE_ROOT 실제 smp1900 root로 설정
[ ] $L1_CODE_ROOT/SMPF/LTE_TX 존재
[ ] l1-study enabled = true
[ ] l1-study target.base_dir = 실제 Linux 절대경로
[ ] job_core.py validate PASS
[ ] 기존 TEST001 state 삭제하지 않음
[ ] 다음 Job ID는 TEST002 사용
[ ] 다음 Job platform은 linux 사용
```

---

# 11. 최종 보고 형식

작업 후 아래 형식으로 결과를 출력한다.

```text
============================================================
L1SW LINUX ONE-SHOT PREP RESULT
============================================================

Overall: READY / BLOCKED

1. OS
- Platform: Linux

2. Versions
- Skill-Updater:
- Job-list:
- Study Runner:
- Dispatcher:

3. Code Root
- L1_CODE_ROOT:
- SMPF/LTE_TX exists: YES / NO

4. Job-list Profile
- l1-study enabled:
- target.base_dir:
- validate:

5. Existing TEST001
- status:
- expected TARGET_MISMATCH confirmed: YES / NO / NOT FOUND

6. Next Test
- job_id: JOB-20260822-TEST002
- platform: linux
- profile: l1-study
- target: SMPF/LTE_TX

7. Changes Made
- ...

8. Blocker
- NONE
또는
- Component:
- Cause:
- Recommended action:

============================================================
```

`Overall: READY`이면 추가 변경 없이 퇴근해도 된다.

전체 구조를 임의 변경하지 말고, 이번 작업에서는 **Linux one-shot 실행에 필요한 로컬 준비만 최소 변경**하라.
