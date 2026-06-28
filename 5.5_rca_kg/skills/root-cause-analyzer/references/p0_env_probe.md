# P0 — 환경 자가 진단 + 상태 파일 초기화

가장 먼저 1회. 추측하지 말고 실제 파일시스템을 확인해 `workspace_root`와 `kg_root`를 확정하고 current_run.yaml에 저장한다.

## P0-0. workspace_root / kg_root 절대경로 확정 — 다른 무엇보다 먼저

이 단계가 P0의 첫 작업이다. 여기서 확정한 `kg_root` 아래에만 RCA KG 산출물을 쓴다. cwd(현재 작업 디렉토리)가 로그 파일 폴더로 잡혀 있어도, 그 폴더에 `rca_kg/`를 만들지 않는다.

1. `workspace_root`를 찾는다: **`skill_manifest.yaml`과 `rca_config.yaml`이 함께 있는 RCA_standalone 패키지 루트.**
2. 탐색 순서:
   a. cwd부터 상위로 거슬러 올라가며 마커를 찾는다.
   b. 못 찾으면 기존 current_run.yaml의 `workspace_root`가 있으면 확인한다.
   c. 그래도 없으면 사용자에게 RCA_standalone 패키지 루트의 절대경로를 1회 묻는다.
3. `{workspace_root}/rca_config.yaml`을 읽는다.
4. `kg_root` 결정:
   - `rca_config.yaml`의 `kg_root`가 절대경로이면 그 값을 사용한다.
   - `kg_root`가 null이면 기본값 `{workspace_root}/rca_kg`를 사용한다.
   - 사용자가 고정 저장소를 원하면 `configure_kg_root.ps1 -KgRoot "D:\AI_Automation\RCA_KG"`를 안내한다.
5. 검증:
   - `{workspace_root}/skill_manifest.yaml` 존재
   - `{kg_root}/keywords.yaml` 존재 또는 생성 가능
   - `{kg_root}/runtime_tool_generate/` 존재 또는 생성 가능
   - `kg_root`가 `.claude/skills/` 아래가 아닌지 확인
6. `current_run.yaml` 위치는 `{kg_root}/runtime_tool_generate/current_run.yaml`이다. 없으면 패키지 기본 template에서 생성하고 `workspace_root`, `kg_root`, `kg_root_source`를 기록한다.
7. 안전장치 — cwd ≠ `workspace_root`이고 cwd 아래에 `rca_kg/`가 이미 있으면 잘못 생성된 KG일 수 있다. 경고하고, `STRUCTURE_FIX_GUIDE.md`의 "KG 병합 절차"를 안내한다. 자동 삭제·자동 이동은 하지 않는다.

이후 단계의 모든 KG 경로는 `{kg_root}/...`로 해석한다.

## P0-1. 환경 진단

조사:
1. `workspace_root`와 `kg_root`가 P0-0에서 확정됐는지 재확인한다.
2. `workspace_root`, `kg_root`, 일반 로그 후보 경로에서 `.sdm`과 `_l1sw.txt`를 찾는다(경로·크기·수정시각 표). `_l1sw.txt`가 1개면 `input.selected_l1sw_txt`에 자동 저장(절대경로 권장), 여러 개면 번호 목록 + next_step=C0_SELECT_L1SW_TXT, 없고 `.sdm`만 있으면 next_step=C0_RUN_L1SW.
3. L1SW Log Analyzer 접근성 확인: parse.ps1 후보, manifest 디렉토리·fragment JSON. `l1sw` 블록에 저장.
4. PowerShell 실행 가능 여부 + `scripts/*_prefilter.ps1` 파라미터 구조 확인(이 단계에서 prefilter 실행 안 함).
5. `{kg_root}/cases/` 아래 EXAMPLE 외 실제 case 수.
6. `{kg_root}/signals_tool_generate/`, `{kg_root}/indexes_tool_generate/` 상태.
7. START_HERE_5.5.md, NEXT_STEP_5.5.md, `{kg_root}/runtime_tool_generate/current_run.yaml` 존재 확인.

출력:
- 화면: `| 항목 | 상태(OK/없음/확인불가) | 근거 경로 | 다음 조치 |` 표. 맨 위 행에 `workspace_root`, `kg_root` 절대경로를 명시.
- `{workspace_root}/review_logs/p0_env_probe_<YYYYMMDD>_<HHMM>_KST.md` 생성(타임스탬프 도구가 채움).
- `{kg_root}/runtime_tool_generate/current_run.yaml`을 실제 값으로 갱신(`workspace_root`, `kg_root` 포함). NEXT_STEP_5.5.md 갱신.

next_step 판정: `_l1sw.txt` 1개 선택가능→P1 / 여러 개→C0_SELECT_L1SW_TXT / 없고 .sdm+parse.ps1→C0_RUN_L1SW / parse.ps1 못 찾음→P0_NEEDS_L1SW_PATH.

마지막에 "지금 P1부터 시작 가능한가?"를 yes/no로 판정. no면 사람이 먼저 할 최소 작업만 1~3줄.
[사람 확인] `workspace_root`와 `kg_root`가 맞는지, P0 표의 "다음 조치"와 NEXT_STEP만 확인.
