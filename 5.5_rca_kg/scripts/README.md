# scripts/README — RCA 보조 스크립트 안내

갱신: 2026-06-27 12:21 KST  
상태: 보조/수동 도구 설명서

정상 사용자는 이 문서를 먼저 보지 않는다. 정상 흐름은 아래 문서와 스킬 호출을 따른다.

```text
README.md → START_HERE_5.5.md → /root-cause-analyzer
```

이 폴더의 PowerShell 스크립트는 RCA 스킬이 실행 중 필요할 때 호출하거나, 스킬 설치가 불가능한 환경에서 수동으로 signal을 만들 때만 사용한다.

---

## 1. 스크립트 목록

| 파일 | 역할 | 일반 사용자 직접 실행 |
|---|---|---|
| `validate_package.ps1` | 패키지 구조 정합성 검사 | 선택 |
| `run_next_step.ps1` | `current_run.yaml` 기준 다음 단계 표시 | 선택 |
| `rach_failure_prefilter.ps1` | RACH failure signal 후보 생성 | 보통 불필요 |
| `scg_failure_prefilter.ps1` | SCG failure signal 후보 생성 | 보통 불필요 |
| `compare_kg_cases.ps1` | 잘못 생긴 KG ↔ 정본 KG case 대조·병합 계획 출력 (읽기 전용) | KG 위치 복구 시만 |

---

## 2. 정상 사용자 권장 흐름

```powershell
# 패키지 루트에서
.\install_skill.ps1
.\validate_install.ps1
```

그 다음 Claude Code에서 실행한다.

```text
/root-cause-analyzer
C:\logs\ue01_l1sw.txt 원인 분석해줘
```

---

## 3. 패키지 구조 검증

배포 ZIP이 깨졌는지 확인하고 싶을 때 실행한다.

```powershell
.\scripts\validate_package.ps1
```

---

## 4. 현재 다음 단계 확인

```powershell
.\scripts\run_next_step.ps1
```

기준 파일:

```text
rca_kg/runtime_tool_generate/current_run.yaml
NEXT_STEP_5.5.md
```

---

## 5. signal prefilter 수동 실행

스킬이 자동으로 처리하는 것이 기본이다. 수동 실행은 디버깅 또는 레거시 환경에서만 사용한다.

예시:

```powershell
.\scripts\rach_failure_prefilter.ps1 -InputPath "C:\logs\ue01_l1sw.txt" -OutputPath ".\rca_kg\signals_tool_generate\ue01_rach_signal.txt"
```

출력 위치는 반드시 아래를 사용한다.

```text
rca_kg/signals_tool_generate/
```

---

## 6. KG 위치 복구 — case 대조·병합 계획

`rca_kg/`가 분석한 `_l1sw.txt`의 상위 폴더에 잘못 생긴 경우, 그 안의 case를 정본 KG로 병합하기 전에 두 폴더를 대조한다. 이 스크립트는 **읽기 전용**이다 — 어떤 파일도 옮기거나 지우지 않고 계획만 출력한다.

```powershell
.\scripts\compare_kg_cases.ps1 `
  -SourceCasesDir "C:\logs\block_x\rca_kg\cases" `
  -TargetCasesDir "C:\work\RCA_standalone\rca_kg\cases"
```

unresolved 까지 함께 보고, NEW 케이스 이동 명령(실행 안 함)도 출력하려면:

```powershell
.\scripts\compare_kg_cases.ps1 `
  -SourceCasesDir "C:\logs\block_x\rca_kg\cases" `
  -TargetCasesDir "C:\work\RCA_standalone\rca_kg\cases" `
  -IncludeUnresolved -MovePlan
```

출력 분류:

```text
NEW    : 정본에 없음          → 그대로 이동
DUP    : fingerprint 겹침     → occurrence_count 합산 수동 병합
SAMEID : case_id 동일         → 수동 확인
```

NEW만 이동하고, DUP/SAMEID는 `STRUCTURE_FIX_GUIDE.md` §6.3 대로 사람이 합산 병합한다.

---

## 7. 주의

```text
- RCA의 주 입력은 _l1sw.txt다.
- .sdm 원본은 L1SW Log Analyzer에서 먼저 처리한다.
- scripts/는 정상 시작 문서가 아니다.
- prompt/ 폴더는 legacy only다.
```
## configure_kg_root.ps1

사용자 지정 RCA KG 저장소를 설정한다.

```powershell
.\configure_kg_root.ps1 -KgRoot "D:\AI_Automation\RCA_KG"
```
