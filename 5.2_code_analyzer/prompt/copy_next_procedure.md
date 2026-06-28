# copy_next_procedure — 다음 procedure 분석 실행용 복사 프롬프트

아래 블록만 Claude Code/Roo Code에 복사해서 사용한다. `prompt/5.2_track_a_prompt.md` reference 문서는 런타임에 다시 읽지 않는다.

```text
Track A Phase 2..N을 수행해줘. 아직 DONE 아닌 procedure 하나만 분석해줘.

[입력]
- slug: (생략 가능 — 비우면 NEXT_STEP_5.2.md의 current_slug를 사용)

[자동 해석 규칙]
- slug를 비우면 NEXT_STEP_5.2.md의 current_slug를 읽어 쓴다.
- analysis_progress 경로는 output/5.2/<slug>/analysis_progress.md 로 자동 구성한다.
- 새로 만드는 파일의 <YYYYMMDD_HHMM_KST>는 사람이 적지 않는다. 도구가 현재 KST 시각으로 채운다.

[필수 규칙]
1. progress_cursor와 next를 먼저 읽는다.
2. DONE procedure는 다시 분석하지 않는다.
3. 이번에는 아직 DONE 아닌 procedure 하나만 분석한다.
4. procedure_runtime_index에서 이번 procedure_slug에 해당하는 slice만 읽는다.
5. index_status가 READY이면 structure_focused.json 또는 full structure 전체를 다시 읽지 않는다.
6. index_status가 INDEX_INCOMPLETE이거나 필요한 id/file 포인터가 없을 때만 structure json targeted fallback read를 허용한다.
7. entry point부터 HAL/PHY/IPC REQ boundary까지 call flow를 추적한다.
8. CNF handler는 단일 가정하지 않는다.
9. cnf_handler_candidate_ids에서 procedure와 매칭되는 handler를 확정한다.
10. 확정된 handler는 Global CNF Carry Map에 SELECTED로 기록하고 이후 재read하지 않는다.
11. 확정 불가 시 [RN] CNF side pending 또는 [RN] CNF handler ambiguous로 남긴다.
12. procedure MSC 1개를 별도 PlantUML 파일로 작성한다.
13. MSC 파일 경로는 output/5.2/<slug>/msc_<procedure_slug>_<YYYYMMDD_HHMM_KST>.puml 이다.
14. hld_<...>.md에는 PlantUML inline block을 넣지 않는다.
15. hld_<...>.md에는 procedure 동작 설명, call flow 요약, msc_ref 링크만 누적한다.
16. procedure별 call edge 본문은 해당 procedure 섹션 내부에만 기록한다.
17. 전역 confirmed call edges 누적 본문 블록은 만들지 않는다.
18. analysis_progress.md를 갱신하고 멈춘다.
19. overwrite 금지. 필요 시 새 timestamp 파일을 만든다.

[완료 진행줄]
진행줄 마지막에는 다음에 붙여넣을 파일명도 함께 안내한다.

다음 procedure가 있으면:
[진행: PROC_DONE:<procedure_slug> → 다음: PROC_NEXT:<next_procedure_slug>]
▶ 다음 붙여넣기: prompt/copy_next_procedure.md

마지막 procedure면:
[진행: PROC_DONE:<procedure_slug> → 다음: PHASEF_FINALIZE]
▶ 다음 붙여넣기: prompt/copy_phase_f.md
```
