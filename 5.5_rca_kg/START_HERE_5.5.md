# START_HERE_5.5 — RCA 정상 사용 시작점

마지막 갱신: 2026-06-27 12:21 KST  
대상 버전: convenience_v0.21_kg_root_config  
권장 방식: `/root-cause-analyzer` 스킬 사용

이 문서는 처음/평소 사용자가 보는 짧은 시작 안내다. 설치 상세는 `INSTALL_SKILL.md`, KG 저장소 설정은 `KG_ROOT_GUIDE.md`, 실제 사용 예시는 `USER_GUIDE_5.5.md`, 문제 해결은 `RUNBOOK_L1SW_TO_P6_5.5.md`를 본다.

---

## 1. 한 줄 요약

```text
ZIP 해제 → .\install_skill.ps1 → 필요 시 .\configure_kg_root.ps1 → VSCode/Claude Code 재시작 → _l1sw.txt 준비 → /root-cause-analyzer
```

---

## 2. 입력 파이프라인

```text
.sdm 원본
  → L1SW Log Analyzer
  → _l1sw.txt
  → /root-cause-analyzer
  → P0~P6 RCA
  → case YAML / keywords.yaml 후보
```

RCA는 `.sdm` 원본을 직접 분석하지 않는다. `_l1sw.txt`가 없으면 P0/C0에서 L1SW 실행 또는 준비 방법을 안내한다.

---

## 3. 최초 1회 설치

```powershell
.\install_skill.ps1
.\validate_install.ps1
```

반복 사용자는 KG 고정 저장소를 지정한다.

```powershell
.\configure_kg_root.ps1 -KgRoot "D:\AI_Automation\RCA_KG"
```

지정하지 않으면 기본값 `<패키지루트>\rca_kg`를 사용한다.

---

## 4. 분석 시작

```text
/root-cause-analyzer
C:\logs\ue01_20260627_l1sw.txt 원인 분석해줘
```

P0가 `workspace_root`와 `kg_root`를 확정한 뒤 P1~P6를 진행한다.

---

## 5. 이어하기

```text
/root-cause-analyzer
이어서 진행해줘
```

스킬은 `{kg_root}/runtime_tool_generate/current_run.yaml`과 `NEXT_STEP_5.5.md`를 기준으로 복귀한다.

---

## 6. 레거시 수동 모드

`prompt/` 폴더의 P0~P6 프롬프트는 스킬 설치가 불가능한 환경에서만 사용한다. 정상 흐름에서는 사용하지 않는다.
