# Phase 0 — 구조맵 (Track A 시작)

입력: 코드 루트, 진입 모드(블록명 또는 API명). slug 비우면 자동 생성.

규칙:
1. slug를 확정한다.
2. canonical path는 반드시 `output/5.2/<slug>/`.
3. 폐기 경로(`artifacts/...`) 사용 금지.
4. structure.json 자동 탐색 우선순위: (a) `structure_*_focused.json` 최신 → (b) 300KB 이하 `structure_*.json` 최신 → (c) 300KB 초과 full은 자동으로 열지 않음(사용자 명시 시만).
5. structure가 없으면 focused extraction으로 `structure_<ts>_focused.json` 생성. `<ts>`는 도구가 현재 KST로 채움.
6. Phase 0에서 source body 전체 read 금지.
7. 파일 목록·LOC·후보 함수명·후보 line 중심으로만 구조맵 작성.
8. grep/검색은 패턴별 최대 200줄.
9. `extraction_mode` enum 기록.
10. structure meta.root와 입력 코드루트가 다르면 경고하고 멈춤.
11. `analysis_progress.md` 생성/갱신. structure 자동 선택 근거와 structure_size 기록.
12. `NEXT_STEP_5.2.md` 갱신 — `current_slug`에 확정 slug 기록(이후 단계 자동 승계).

진행줄: `[진행: PHASE0_DONE → 다음: PHASE1_PROCEDURE_DISCOVERY]` → Phase 1 자동 진행.
