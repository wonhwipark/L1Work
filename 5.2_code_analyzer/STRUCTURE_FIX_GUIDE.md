# STRUCTURE_FIX_GUIDE — code-analyzer 설치 구조 복구 가이드

갱신: 2026-06-27 10:38 KST  
대상 버전: v0.8_manifest_guard

이 문서는 `install_skill.ps1` 실행 시 패키지 구조가 기대 구조와 맞지 않을 때 참고하는 복구 가이드다.

---

## 1. 원칙

설치 스크립트는 아무 폴더나 자동으로 추측해서 설치하지 않는다. 스킬 설치는 Claude Code가 읽어야 하므로 다음 조건을 만족해야 한다.

```text
<package root>/skills/code-analyzer/SKILL.md
```

이 위치가 맞지 않으면 설치는 중단된다. 대신 스크립트가 현재 발견한 `SKILL.md` 후보와 기대 구조를 보여주고, 사용자가 어떻게 맞춰야 하는지 안내한다.

---

## 2. 기대 구조

```text
<package root>/
├─ skill_manifest.yaml
└─ skills/
   └─ code-analyzer/
      ├─ SKILL.md
      └─ references/
         └─ ...
```

필수 파일:

- `skills/code-analyzer/SKILL.md`
- `skills/code-analyzer/references/index.md`
- `skills/code-analyzer/references/phase0.md`
- `skills/code-analyzer/references/phase1.md`
- `skills/code-analyzer/references/next_procedure.md`
- `skills/code-analyzer/references/resume.md`
- `skills/code-analyzer/references/block_switch.md`
- `skills/code-analyzer/references/track_b.md`
- `skills/code-analyzer/references/phase_f.md`

---

## 3. 자주 발생하는 구조 오류

### 3.1 스킬 폴더명이 바뀐 경우

잘못된 예:

```text
skills/code_analyzer/SKILL.md
```

또는

```text
skills/RCA/SKILL.md
```

맞춰야 하는 구조:

```text
skills/code-analyzer/SKILL.md
```

### 3.2 한 단계 더 깊게 풀린 경우

잘못된 예:

```text
skills/code-analyzer/code-analyzer/SKILL.md
```

맞춰야 하는 구조:

```text
skills/code-analyzer/SKILL.md
```

### 3.3 TargetSkillsDir를 잘못 지정한 경우

`-TargetSkillsDir`에는 스킬 폴더 자체가 아니라 상위 `skills` 폴더를 넣는다.

잘못된 예:

```powershell
.\install_skill.ps1 -TargetSkillsDir "C:\Users\<user>\.claude\skills\code-analyzer"
```

올바른 예:

```powershell
.\install_skill.ps1 -TargetSkillsDir "C:\Users\<user>\.claude\skills"
```

---

## 4. 복구 방법

가장 안전한 방법은 ZIP을 다시 푸는 것이다.

```text
1. ZIP을 새 폴더에 다시 압축 해제
2. 패키지 루트에서 skill_manifest.yaml 확인
3. skills/code-analyzer/SKILL.md 존재 확인
4. .\install_skill.ps1 실행
```

수동으로 폴더를 맞출 수도 있다.

```powershell
New-Item -ItemType Directory -Force -Path ".\skills" | Out-Null
Move-Item -Path "<현재-스킬-폴더>" -Destination ".\skills\code-analyzer"
```

단, `references` 폴더도 `SKILL.md`와 같은 스킬 폴더 아래에 있어야 한다.

---

## 5. 설치 후 검증

```powershell
.\validate_install.ps1
```

직접 위치를 지정한 경우:

```powershell
.\validate_install.ps1 -TargetSkillsDir "C:\Users\<user>\.claude\skills"
```
