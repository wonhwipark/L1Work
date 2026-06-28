# RCA Standalone v0.21 — kg_root user-configurable update

갱신: 2026-06-27 12:21 KST

## 변경 목적

v0.20에서 `workspace_root/rca_kg` anchor를 도입했지만, 반복 사용자가 패키지 버전을 교체할 때 KG가 버전 폴더별로 분산될 수 있었다. v0.21은 `workspace_root`와 `kg_root`를 분리하고, 사용자가 고정 KG 저장소를 지정할 수 있게 한다.

## 주요 변경

```text
- rca_config.yaml 추가
- configure_kg_root.ps1 추가
- KG_ROOT_GUIDE.md 추가
- current_run.yaml state_version 2 적용
- P0~P6 reference 경로 기준을 {kg_root}로 변경
- P1 format profile 저장 위치를 prompt/deepdive에서 kg_root/runtime_tool_generate/format_profiles로 변경
- run_next_step.ps1 skill-first 안내 및 kg_root 설정 인식
- validate_package.ps1 v0.21 정합성 검사 강화
```

## 권장 사용

```powershell
.\install_skill.ps1
.\validate_install.ps1
.\configure_kg_root.ps1 -KgRoot "D:\AI_Automation\RCA_KG"
```
