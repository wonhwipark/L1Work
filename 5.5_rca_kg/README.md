# RCA Standalone — 새 사용자 빠른 시작

버전: convenience_v0.21_kg_root_config  
갱신: 2026-06-27 12:21 KST  
스킬: `root-cause-analyzer` (`/root-cause-analyzer`)

이 패키지는 L1SW Log Analyzer가 만든 `_l1sw.txt`를 입력으로 받아 L1 장애의 근본 원인 분석(RCA), case YAML 생성, keywords.yaml 후보 승격을 수행하는 Claude Code 스킬 패키지다.

---

## 1. 처음이면 이 순서만 따른다

```powershell
cd .\RCA_standalone
.\install_skill.ps1
.\validate_install.ps1
```

설치 후 Claude Code 또는 VSCode를 재시작한다.

```text
/root-cause-analyzer
C:\logs\ue01_l1sw.txt 원인 분석해줘
```

`.sdm`만 있으면 먼저 L1SW Log Analyzer로 `_l1sw.txt`를 만들어야 한다. RCA는 `.sdm` 원본을 직접 분석하지 않는다.

---

## 2. KG 저장소 선택

기본값은 패키지 내부다.

```text
kg_root = <RCA_standalone>\rca_kg
```

반복 사용자는 고정 KG 저장소를 지정하는 것을 권장한다.

```powershell
.\configure_kg_root.ps1 -KgRoot "D:\AI_Automation\RCA_KG"
```

스킬 설치 폴더 아래에 `rca_kg`를 두지 않는다. 스킬은 교체 가능하고, KG는 계속 보존되어야 한다. 자세한 내용은 `KG_ROOT_GUIDE.md`를 본다.

---

## 3. 문서 역할

| 문서 | 언제 보는가 |
|---|---|
| `README.md` | ZIP을 처음 받은 사람이 가장 먼저 본다. |
| `START_HERE_5.5.md` | 정상 사용 흐름을 짧게 확인한다. |
| `INSTALL_SKILL.md` | 스킬 설치 옵션, 경로 직접 지정, 재설치를 확인한다. |
| `KG_ROOT_GUIDE.md` | 누적 RCA KG 저장소 위치를 정한다. |
| `USER_GUIDE_5.5.md` | 설치 후 P0~P6 사용법을 확인한다. |
| `NEXT_STEP_5.5.md` | 현재 상태와 다음 한 걸음을 확인한다. |
| `RUNBOOK_L1SW_TO_P6_5.5.md` | 실행 중 막혔을 때 증상별 조치를 확인한다. |
| `VERSION_5.5.md` | 변경 이력을 확인한다. |
| `HANDOFF_5.5.md` | 설계 이력/유지보수용이다. 일반 사용자는 보통 보지 않는다. |

`prompt/` 폴더는 스킬 설치가 불가능한 환경의 레거시 수동 모드다. 정상 사용자는 열지 않는다.

---

## 4. 대표 결과물 위치

`kg_root` 기준:

```text
runtime_tool_generate/current_run.yaml
runtime_tool_generate/format_profiles/*.md
signals_tool_generate/*_signal.txt
cases/*.yaml
cases/unresolved/*.yaml
indexes_tool_generate/index.md
keywords.yaml
```
