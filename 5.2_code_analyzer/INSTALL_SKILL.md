# INSTALL_SKILL — CodeAnalyzer 설치 가이드

갱신: 2026-06-27 10:38 KST  
대상 스킬: `code-analyzer`  
대상 버전: `v0.8_manifest_guard`

이 문서는 설치만 설명한다. 설치 후 사용법은 `START_HERE_5.2.md`와 `USER_GUIDE_5.x.md`를 본다.

---

## 1. 기본 설치

패키지 루트에서 PowerShell을 열고 실행한다.

```powershell
.\install_skill.ps1
```

스크립트는 먼저 `skill_manifest.yaml`을 읽고 패키지 구조를 검증한다. 구조가 맞으면 기본 Claude skills 위치를 보여주고 사용할지 묻는다.

기본 대상 위치:

```text
C:\Users\<사용자>\.claude\skills
```

Enter 또는 `Y`를 누르면 설치한다.

---

## 2. 설치 위치 직접 지정

회사 PC 계정명, 테스트 폴더, 별도 Claude 설정 위치가 다르면 직접 지정한다.

```powershell
.\install_skill.ps1 -TargetSkillsDir "C:\Users\<사용자>\.claude\skills"
```

`TargetSkillsDir`에는 `code-analyzer` 폴더 자체가 아니라 그 상위의 `skills` 폴더를 넣는다.

정상 설치 구조:

```text
C:\Users\<사용자>\.claude\skills\code-analyzer\SKILL.md
```

만약 `code-analyzer` 폴더 자체를 지정하면 스크립트가 경고하고 상위 `skills` 폴더를 쓰도록 안내한다.

---

## 3. 기존 설치가 있을 때

기존 스킬을 바로 교체한다.

```powershell
.\install_skill.ps1 -Force
```

기존 스킬을 백업하고 새로 설치한다.

```powershell
.\install_skill.ps1 -Backup
```

경로 지정과 함께 사용할 수 있다.

```powershell
.\install_skill.ps1 -TargetSkillsDir "C:\Users\<사용자>\.claude\skills" -Backup
```

---

## 4. 구조가 맞지 않을 때

설치 스크립트는 아래 구조를 기대한다.

```text
<package root>\skills\code-analyzer\SKILL.md
```

기대 구조와 맞지 않으면 설치를 중단하고 다음 정보를 출력한다.

```text
- 누락된 필수 파일
- 현재 발견된 SKILL.md 후보
- 맞춰야 하는 기대 위치
- 복구용 PowerShell 예시
```

상세 가이드는 `STRUCTURE_FIX_GUIDE.md`를 본다.

---

## 5. legacy 폴더 경고

이전 이름 또는 임시 이름의 스킬 폴더가 설치 대상에 남아 있으면 스크립트가 경고한다. 스크립트는 legacy 폴더를 자동 삭제하지 않는다.

---

## 6. 설치 검증

```powershell
.\validate_install.ps1
```

직접 지정한 경로를 검증한다.

```powershell
.\validate_install.ps1 -TargetSkillsDir "C:\Users\<사용자>\.claude\skills"
```

성공 기준:

```text
C:\Users\<사용자>\.claude\skills\code-analyzer\SKILL.md 존재
manifest의 required_files가 설치 위치에 모두 존재
```

---

## 7. 설치 후 조치

Claude Code 또는 VSCode에서 스킬 목록이 바로 갱신되지 않으면 재시작한다.

호출:

```text
/code-analyzer
```
