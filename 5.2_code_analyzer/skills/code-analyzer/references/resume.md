# Resume — 중단 후 이어하기

slug 자동 승계. 타임스탬프 도구가 채움.

규칙:
1. `analysis_progress.md`의 progress_cursor를 먼저 읽는다.
2. canonical_path가 `output/5.2/<slug>/`인지 확인.
3. selected_structure_json은 확인만. next가 PROC_NEXT이면 구조 파일 전체를 바로 읽지 않는다.
4. extraction_mode enum 확인. DONE procedure 재분석 금지. Global CNF Carry Map SELECTED handler 재read 금지.
5. next가 PROC_NEXT이면 procedure_runtime_index에서 해당 slice만. index READY이면 structure 재read 없이 procedure 하나만 수행. INCOMPLETE이면 필요한 범위만 targeted fallback.
6. next가 PHASEF_FINALIZE이면 .puml 링크와 HLD 섹션만 확인.
7. 응답 마지막은 token progress cursor.

cursor에 따라 next_procedure / phase_f로 자동 진행한다.
