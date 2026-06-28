# Phase 2..N — procedure 하나 분석 (반복)

slug 자동 승계. 타임스탬프 도구가 채움. 한 번에 아직 DONE 아닌 procedure **하나만** 분석한다.

규칙:
1. progress_cursor와 next를 먼저 읽는다. DONE procedure는 재분석 금지.
2. `procedure_runtime_index`에서 이번 procedure_slug slice만 읽는다.
3. index_status가 READY이면 structure json 전체를 다시 읽지 않는다.
4. INDEX_INCOMPLETE이거나 필요한 id/file 포인터가 없을 때만 structure json targeted fallback read.
5. entry point부터 HAL/PHY/IPC REQ boundary까지 call flow 추적.
6. CNF handler 단일 가정 금지. `cnf_handler_candidate_ids`에서 procedure 매칭 handler 확정. 확정 handler는 Global CNF Carry Map에 SELECTED로 기록하고 재read 안 함. 확정 불가 시 `[RN] CNF side pending` 또는 `[RN] CNF handler ambiguous`.
7. procedure MSC 1개를 별도 `output/5.2/<slug>/msc_<procedure_slug>_<ts>.puml`로 작성.
8. `hld_*.md`에 PlantUML inline 금지. 동작 설명·call flow 요약·msc_ref 링크만 누적. call edge 본문은 해당 procedure 섹션 내부에만. 전역 누적 본문 금지.
9. `analysis_progress.md` 갱신하고 멈춘다. overwrite 금지(필요 시 새 timestamp).

진행줄(다음 있음): `[진행: PROC_DONE:<slug> → 다음: PROC_NEXT:<next_slug>]` → 자동 반복.
진행줄(마지막): `[진행: PROC_DONE:<slug> → 다음: PHASEF_FINALIZE]` → Phase F 자동 진행.

블록 전환 요청이 들어오면 `block_switch.md`로 처리(현재 cursor 보존 후 전환).
