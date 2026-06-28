# CodeAnalyzer v0.6 install script update

작성일: 2026-06-27 10:15 KST

## 변경 요약

- `install_skill.ps1` 추가
- `validate_install.ps1` 추가
- `INSTALL_SKILL.md` 추가
- `START_HERE_5.2.md`의 스킬 설치 절차를 수동 복사에서 설치 스크립트 방식으로 변경
- `HANDOFF_5.2.md`의 시작 문서 안내를 `START_HERE_5.2.md` 우선으로 정리
- `NEXT_STEP_5.2.md`에 설치 전 실행 안내 추가

## 설치 UX

```powershell
.\install_skill.ps1
.\install_skill.ps1 -TargetSkillsDir "C:\Users\<사용자>\.claude\skills"
.\install_skill.ps1 -Force
.\install_skill.ps1 -Backup
.\validate_install.ps1
```
