# NEXT_STEP_5.5 — RCA 다음 행동

마지막 갱신: 2026-06-27 12:21 KST  
상태 파일: `{kg_root}/runtime_tool_generate/current_run.yaml` + `NEXT_STEP_5.5.md`

---

## 1. 현재 상태

```text
package_version: convenience_v0.21_kg_root_config
current_step: INIT
next_step: INSTALL_OR_RUN_SKILL
primary_input: _l1sw.txt
kg_root: 기본값 <패키지루트>\rca_kg 또는 사용자 지정 고정 저장소
progress_cursor: [진행: INIT → 다음: INSTALL_OR_RUN_SKILL]
```

---

## 2. 다음 한 걸음

```powershell
.\install_skill.ps1
.\validate_install.ps1
```

반복 사용을 위한 KG 고정 저장소 지정:

```powershell
.\configure_kg_root.ps1 -KgRoot "D:\AI_Automation\RCA_KG"
```

분석 시작:

```text
/root-cause-analyzer
C:\logs\ue01_l1sw.txt 원인 분석해줘
```

진행 중 이어하기:

```text
/root-cause-analyzer
이어서 진행해줘
```

---

## 3. 완료 후 기대 결과

```text
{kg_root}/runtime_tool_generate/current_run.yaml 갱신
{kg_root}/runtime_tool_generate/format_profiles/*.md 생성
{kg_root}/signals_tool_generate/*_signal.txt 생성
{kg_root}/cases/*.yaml 생성 또는 갱신
{kg_root}/indexes_tool_generate/index.md 갱신
{kg_root}/keywords.yaml candidate/confirmed 갱신 후보 생성
```
