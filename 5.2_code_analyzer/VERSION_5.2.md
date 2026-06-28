# CodeAnalyzer Standalone Package Version

- package_version: v0.8_manifest_guard
- generated_at: 2026-06-27 10:38 KST
- base_package: CodeAnalyzer_standalone_20260627_1022_KST_v0_7_doc_cleanup.zip
- track: Code Analyzer 5.2 standalone
- operating_model: skill-first + focused structure + procedure_runtime_index
- current_status: pre-E2E validation
- primary_entry: `README.md` → `START_HERE_5.2.md`
- install_entry: `INSTALL_SKILL.md`
- skill_call: `/code-analyzer`

---

## v0.8 변경 요약 (2026-06-27 10:38 KST)

v0.8은 설치 구조 안정성을 강화한 릴리스다.

- `skill_manifest.yaml` 추가
- `STRUCTURE_FIX_GUIDE.md` 추가
- 설치 전 manifest required_files 검증
- 구조 불일치 시 누락 파일, 감지 후보, 복구 PowerShell 예시 출력
- legacy skill folder 경고
- `validate_install.ps1` manifest 기반 설치 검증

---

## v0.7 변경 요약 (2026-06-27 10:22 KST)

v0.7은 새 사용자가 ZIP 다운로드 후 쉽게 사용할 수 있도록 설명 문서를 정리한 릴리스다.

### 1. README 추가

`README.md`를 추가해 ZIP을 처음 받은 사용자의 첫 진입점을 명확히 했다.

### 2. 문서 역할 분리

```text
README.md                 최초 진입
START_HERE_5.2.md         정상 사용 시작
INSTALL_SKILL.md          설치 전용
USER_GUIDE_5.2.md         설치 후 사용법
NEXT_STEP_5.2.md          현재 다음 한 걸음
RUNBOOK_BLOCK_TO_HLD_5.2.md 문제 해결
HANDOFF_5.2.md            설계 이력/유지보수
VERSION_5.2.md            변경 이력
```

### 3. 설치 설명 중복 제거

설치 상세는 `INSTALL_SKILL.md`로 모으고, `START_HERE_5.2.md`와 `USER_GUIDE_5.2.md`에는 설치 상세를 반복하지 않도록 정리했다.

### 4. 스킬 우선 UX 명확화

정상 사용은 `/code-analyzer` 호출로 고정했다. `prompt/` 폴더는 스킬 설치가 불가능한 환경의 레거시 수동 모드로만 설명한다.

### 5. 구방식 수동 설치 안내 제거

정상 사용자 문서에서 직접 파일 복사 방식의 설치 절차를 제거했다. 설치는 `install_skill.ps1`과 `validate_install.ps1` 기준으로 안내한다.

---

## v0.6 변경 요약 (2026-06-27 10:16 KST)

v0.6은 v0.5 스킬화 구조를 유지하면서 설치 편의성을 보강했다.

```text
install_skill.ps1
validate_install.ps1
INSTALL_SKILL.md
```

지원 기능:

```text
- 기본 Claude skills 위치 자동 탐색
- TargetSkillsDir 직접 지정
- Force 덮어쓰기
- Backup 후 설치
- 설치 후 SKILL.md 검증
```

---

## v0.5 핵심 요약

`code-analyzer` 스킬을 도입했다.

```text
skills/code-analyzer/SKILL.md
skills/code-analyzer/references/*
```

주요 효과:

```text
- 별도 부트스트랩 프롬프트 불필요
- Track A/B 자동 판별
- slug 자동 승계
- block_switch 지원
- procedure_runtime_index 기반 반복 read 절감
```

---

## 고정 규칙

```text
산출물 경로: output/5.2/<slug>/
MSC: 별도 .puml
HLD: msc_ref만 기록
진행줄: [진행: ... → 다음: ...]
legacy prompt: prompt/ 폴더, 비권장
```
