# CodeAnalyzer v0.8 manifest guard review log

생성: 2026-06-27 10:38 KST

## 변경

- `skill_manifest.yaml` 추가
- `STRUCTURE_FIX_GUIDE.md` 추가
- `install_skill.ps1` manifest 기반 구조 검증 추가
- `validate_install.ps1` manifest 기반 설치 검증 추가
- `references/index.md` 추가
- legacy skill folder 경고 추가
- TargetSkillsDir가 스킬 폴더 자체를 가리킬 때 경고 추가

## 사용자 효과

기대 구조와 다르면 설치 전 중단하고, 현재 감지된 `SKILL.md` 후보와 기대 구조, 복구용 PowerShell 예시를 출력한다.
