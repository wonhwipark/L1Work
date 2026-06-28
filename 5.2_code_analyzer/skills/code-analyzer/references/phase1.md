# Phase 1 — procedure 발견 + procedure_runtime_index

slug는 `current_slug` 자동 승계. analysis_progress 경로 자동 구성. structure_json은 `output/5.2/<slug>/` 최신 `*_focused.json` 자동 선택(없으면 300KB 이하 최신 `*.json`).

규칙:
1. canonical path 확인. analysis_progress.md와 structure_json이 같은 canonical path 기준인지 확인.
2. structure_json은 이번 Phase 1에 필요한 만큼만 읽는다.
3. 블록 모드면 블록이 수신하는 외부 인터페이스를 열거. API 모드면 해당 API를 단일 procedure entry point로 확정.
4. procedure 후보를 procedure_slug와 함께 번호로 제시하고, 사용자가 전부/일부를 선택하도록 멈춘다.
5. `analysis_progress.md`에 procedure 목록과 next 기록.
6. 반드시 `procedure_runtime_index`를 생성한다. 항목별: entry_point, entry_file, entry_line, related_files, req_site_ids, cnf_handler_candidate_ids, call_edge_ids, hld_section_anchor, msc_file(`output/5.2/<slug>/msc_<procedure_slug>_<ts>.puml`), index_status(READY|INDEX_INCOMPLETE), rn.
7. 전역 confirmed call edges 누적 본문 블록 금지. 전역에는 edge id 요약만.

진행줄(완료): `[진행: PHASE1_DONE → 다음: PROC_NEXT:<procedure_slug>]` → next_procedure 자동 진행.
진행줄(선택 대기): `[진행: PHASE1_WAIT_SCOPE_SELECTION → 다음: USER_SELECT_PROCEDURES]` → 사용자 번호 선택 대기.
