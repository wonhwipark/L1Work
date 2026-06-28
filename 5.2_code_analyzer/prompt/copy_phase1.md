# copy_phase1 — Track A Phase 1 실행용 복사 프롬프트

아래 블록만 Claude Code/Roo Code에 복사해서 사용한다. `prompt/5.2_track_a_prompt.md` reference 문서는 런타임에 다시 읽지 않는다.

```text
Track A Phase 1을 수행해줘.

[입력]
- slug: (생략 가능 — 비우면 NEXT_STEP_5.2.md의 current_slug를 사용)

[자동 해석 규칙]
- slug를 비우면 NEXT_STEP_5.2.md의 current_slug를 읽어 쓴다.
- analysis_progress 경로는 output/5.2/<slug>/analysis_progress.md 로 자동 구성한다.
- structure_json은 사람이 파일명을 적지 않는다. output/5.2/<slug>/ 에서 최신 *_focused.json을 자동 선택한다(없으면 300KB 이하 최신 *.json).

[필수 규칙]
1. canonical path가 output/5.2/<slug>/ 인지 먼저 확인한다.
2. analysis_progress.md와 structure_json이 같은 canonical path 기준인지 확인한다.
3. structure_json은 이번 Phase 1에서만 필요한 만큼 읽는다.
4. 블록 기준 모드면 블록이 수신하는 외부 인터페이스를 열거한다.
5. API 기준 모드면 해당 API를 단일 procedure entry point로 확정한다.
6. procedure 후보를 procedure_slug와 함께 번호로 제시한다.
7. 사용자가 전부/일부를 선택할 수 있게 멈춘다.
8. analysis_progress.md에 procedure 목록과 next를 기록한다.
9. 반드시 procedure_runtime_index를 생성한다.
10. procedure_runtime_index에는 procedure별 entry_point, related_files, req_site_ids, cnf_handler_candidate_ids, call_edge_ids, msc_file, index_status를 기록한다.
11. 전역 confirmed call edges 누적 본문 블록은 만들지 않는다.
12. 필요한 경우 전역에는 edge id 요약만 남긴다.
13. 진행줄은 token cursor로 출력한다.

[procedure_runtime_index 최소 형식]
- procedure_slug: <procedure_slug>
  entry_point: <function/message/api>
  entry_file: <relative path>
  entry_line: <line 또는 UNKNOWN>
  related_files:
    - <relative path>
  req_site_ids:
    - <REQ_EDGE_ID 또는 UNKNOWN>
  cnf_handler_candidate_ids:
    - <CNF_HANDLER_ID 또는 UNKNOWN>
  call_edge_ids:
    - <EDGE_ID 또는 UNKNOWN>
  hld_section_anchor: <anchor>
  msc_file: output/5.2/<slug>/msc_<procedure_slug>_<YYYYMMDD_HHMM_KST>.puml
  index_status: READY | INDEX_INCOMPLETE
  rn:
    - <필요 시>

진행줄 마지막에는 다음에 붙여넣을 파일명도 함께 안내한다.

[블록 기준 완료 진행줄]
[진행: PHASE1_DONE → 다음: PROC_NEXT:<procedure_slug>]
▶ 다음 붙여넣기: prompt/copy_next_procedure.md

[사용자 선택이 필요한 경우]
[진행: PHASE1_WAIT_SCOPE_SELECTION → 다음: USER_SELECT_PROCEDURES]
▶ procedure 번호를 선택해 회신. 선택 후 다음 붙여넣기: prompt/copy_next_procedure.md
```
