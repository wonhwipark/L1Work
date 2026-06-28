# RCA Standalone Package Version

- package_version: convenience_v0.21_kg_root_config
- generated_at: 2026-06-27 11:43 KST
- base_package: RCA_standalone_20260627_1038_KST_manifest_guard_bundle.zip
- track: RCA 5.5 standalone
- operating_model: L1SW-first + stateful convenience + skill-first
- current_status: pre-E2E validation
- primary_input: `_l1sw.txt`
- raw_log_policy: `.sdm` is input to L1SW only; RCA P3~P6 uses `_l1sw.txt` or signal files
- primary_entry: `README.md` → `START_HERE_5.5.md`
- install_entry: `INSTALL_SKILL.md`
- skill_call: `/root-cause-analyzer`

---## v0.21 변경 요약 (2026-06-27 12:21 KST)

v0.21은 `workspace_root`와 `kg_root`를 분리한 릴리스다. 기본값은 `<패키지루트>/rca_kg`이지만, 반복 사용자는 `D:\AI_Automation\RCA_KG` 같은 고정 저장소를 지정할 수 있다.

주요 변경:

```text
- rca_config.yaml 추가: package root와 kg_root 설정 SSOT
- configure_kg_root.ps1 추가: 사용자 지정 KG 저장소 생성/초기화/상태 반영
- KG_ROOT_GUIDE.md 추가: 스킬 위치와 KG 위치 분리 원칙 설명
- current_run.yaml state_version 2: workspace_root와 kg_root 필드 분리
- P0-0 갱신: workspace_root 확인 후 rca_config.yaml에서 kg_root 결정
- P1 산출물 위치 변경: prompt/deepdive → {kg_root}/runtime_tool_generate/format_profiles
- P2~P6 산출물 기준 변경: {workspace_root}/rca_kg → {kg_root}
- run_next_step.ps1 skill-first 안내 및 kg_root config 인식
- validate_package.ps1 v0.21 정합성 검사 추가
```

금지 원칙:

```text
rca_kg를 .claude/skills/root-cause-analyzer 아래에 두지 않는다.
```


## v0.20 변경 요약 (2026-06-27 11:43 KST)

v0.20은 KG 누적 위치 버그를 고친 릴리스다. 이전에는 산출물 경로가 상대경로 `rca_kg/`였고 Claude Code의 cwd가 분석 대상 `_l1sw.txt`의 폴더로 잡히면 그 폴더에 `rca_kg/`가 잘못 생성됐다. KG가 분산되어 패턴 재발 감지·signature 승격이 깨지는 문제였다.

- P0에 P0-0 단계 추가: 패키지 마커(`skill_manifest.yaml` + `rca_kg/`)로 `workspace_root`를 절대경로로 확정.
- SKILL.md §1에 KG 루트 불변 규칙(0a~0d) 추가. 모든 `rca_kg/...`는 `{workspace_root}/rca_kg/...`로 해석.
- P1~P6 reference의 모든 산출물 경로를 `{workspace_root}` 기준으로 변경.
- cwd ≠ workspace_root인데 cwd 아래 `rca_kg/`가 있으면 경고하는 안전장치 추가.
- STRUCTURE_FIX_GUIDE.md §6에 잘못 생긴 KG의 case YAML 병합 절차 추가.
- current_run.yaml / example: `workspace_root` 의미 주석화, 예시에 절대경로 표기.

---

## v0.18 변경 요약 (2026-06-27 10:22 KST)

v0.18은 새 사용자가 ZIP 다운로드 후 쉽게 사용할 수 있도록 설명 문서를 정리한 릴리스다.

### 1. README 추가

`README.md`를 추가해 ZIP을 처음 받은 사용자의 첫 진입점을 명확히 했다.

### 2. 문서 역할 분리

```text
README.md                    최초 진입
START_HERE_5.5.md            정상 사용 시작
INSTALL_SKILL.md             설치 전용
USER_GUIDE_5.5.md            설치 후 사용법
NEXT_STEP_5.5.md             현재 다음 한 걸음
RUNBOOK_L1SW_TO_P6_5.5.md    문제 해결
USAGE_SCENARIO_5.5.md        전체 운영 시나리오
HANDOFF_5.5.md               설계 이력/유지보수
VERSION_5.5.md               변경 이력
```

### 3. 설치 설명 중복 제거

설치 상세는 `INSTALL_SKILL.md`로 모으고, `START_HERE_5.5.md`와 `USER_GUIDE_5.5.md`에는 설치 상세를 반복하지 않도록 정리했다.

### 4. 스킬 우선 UX 명확화

정상 사용은 `/root-cause-analyzer` 호출로 고정했다. `prompt/` 폴더는 스킬 설치가 불가능한 환경의 레거시 수동 모드로만 설명한다.

### 5. 구방식 수동 설치 안내 제거

정상 사용자 문서에서 직접 파일 복사 방식의 설치 절차를 제거했다. 설치는 `install_skill.ps1`과 `validate_install.ps1` 기준으로 안내한다.

### 6. 입력 파이프라인 재강조

`.sdm → L1SW Log Analyzer → _l1sw.txt → RCA` 흐름을 모든 사용자 문서에서 동일하게 정리했다.

---

## v0.17 변경 요약 (2026-06-27 10:16 KST)

v0.17은 v0.16 스킬화 구조를 유지하면서 설치와 재설치 편의성을 보강했다.

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

## v0.16 핵심 요약

`root-cause-analyzer` 스킬을 도입했다.

```text
skills/root-cause-analyzer/SKILL.md
skills/root-cause-analyzer/references/*
```

주요 효과:

```text
- 별도 부트스트랩 프롬프트 불필요
- P0~P6 단계 자동 복귀
- current_run.yaml 기반 stateful 진행
- _l1sw.txt 유무에 따른 C0/P1 분기
- issue_type 추천 및 signal 생성
```

---

## 고정 규칙

```text
RCA 입력: _l1sw.txt
.sdm 처리: L1SW Log Analyzer에서 먼저 수행
상태 파일: rca_kg/runtime_tool_generate/current_run.yaml
signal 위치: rca_kg/signals_tool_generate/
case 위치: rca_kg/cases/
legacy prompt: prompt/ 폴더, 비권장
```
