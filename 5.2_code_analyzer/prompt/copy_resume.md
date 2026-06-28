# copy_resume — 이어하기 실행용 복사 프롬프트

아래 블록만 Claude Code/Roo Code에 복사해서 사용한다. `prompt/5.2_track_a_prompt.md` reference 문서는 런타임에 다시 읽지 않는다.

```text
CodeAnalyzer Track A를 이어서 수행해줘.

[입력]
- slug: (생략 가능 — 비우면 NEXT_STEP_5.2.md의 current_slug를 사용)

[자동 해석 규칙]
- slug를 비우면 NEXT_STEP_5.2.md의 current_slug를 읽어 쓴다.
- analysis_progress 경로는 output/5.2/<slug>/analysis_progress.md 로 자동 구성한다.
- 새로 만드는 파일의 <YYYYMMDD_HHMM_KST>는 사람이 적지 않는다. 도구가 현재 KST 시각으로 채운다.

[필수 규칙]
1. analysis_progress.md의 progress_cursor를 먼저 읽는다.
2. canonical_path가 output/5.2/<slug>/ 인지 확인한다.
3. selected_structure_json 경로는 확인만 하고, next가 PROC_NEXT이면 구조 파일 전체를 바로 읽지 않는다.
4. extraction_mode가 git | bash | powershell | internal_search | mixed 중 하나인지 확인한다.
5. DONE procedure는 다시 분석하지 않는다.
6. Global CNF Carry Map의 SELECTED handler는 재read하지 않는다.
7. next가 PROC_NEXT:<procedure_slug>이면 procedure_runtime_index에서 해당 procedure slice만 읽는다.
8. index_status가 READY이면 structure json 재read 없이 해당 procedure 하나만 수행한다.
9. index_status가 INDEX_INCOMPLETE이면 필요한 범위만 targeted fallback read한다.
10. next가 PHASEF_FINALIZE이면 .puml 파일 링크와 HLD 섹션만 확인한다.
11. 응답 마지막은 token progress cursor로 출력한다.

[진행줄 예]
진행줄 마지막에는 다음에 붙여넣을 파일명도 함께 안내한다.
[진행: PROC_DONE:<procedure_slug> → 다음: PROC_NEXT:<next_procedure_slug>]   ▶ 다음 붙여넣기: prompt/copy_next_procedure.md
[진행: PROC_DONE:<procedure_slug> → 다음: PHASEF_FINALIZE]                  ▶ 다음 붙여넣기: prompt/copy_phase_f.md
[진행: BLOCK_HLD_DONE:<slug> → 다음: WAIT_NEW_BLOCK]                        ▶ 다음 붙여넣기: prompt/copy_phase0.md (새 블록)
```
