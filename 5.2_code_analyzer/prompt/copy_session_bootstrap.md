# copy_session_bootstrap — 세션 시작 시 1회만 붙여넣는 공통 규칙

새 Claude Code/Roo Code 세션을 열면 **이 블록을 가장 먼저 1회만** 붙여넣는다. 이후 `copy_phase0` / `copy_phase1` / `copy_next_procedure` / `copy_resume` / `copy_phase_f`는 같은 세션 안에서 아래 규칙이 이미 적용된 상태로 실행된다. 같은 규칙을 매 단계 다시 길게 붙여넣지 않아도 되므로 입력 토큰이 줄어든다.

reference 문서(`prompt/5.2_track_a_prompt.md`, `prompt/5.2_track_b_prompt.md`)는 런타임에 읽지 않는다.

```text
지금부터 CodeAnalyzer 5.2 세션이다. 이 세션 동안 아래 고정 규칙을 항상 적용한다.
다음 메시지부터는 단계별 copy prompt만 짧게 붙여넣겠다.

[경로]
1. 모든 산출물 경로는 output/5.2/<slug>/ 로 통일한다.
2. artifacts/code_analyzer, %USERPROFILE%\artifacts\code_analyzer, artifacts/5.2 경로는 사용하지 않는다.
3. NEXT_STEP_5.2.md는 항상 canonical path 기준으로 갱신한다.
4. overwrite 금지. 재생성이 필요하면 새 KST timestamp 파일을 만든다.

[추출/상태]
5. extraction_mode는 git | bash | powershell | internal_search | mixed 중 하나만 쓴다.
6. fallback 순서는 git → bash → powershell → internal_search → mixed 이다.
7. 응답 마지막은 항상 token progress cursor로 끝낸다. 예: [진행: PHASE0_DONE → 다음: PHASE1_PROCEDURE_DISCOVERY]
8. 산문형 진행줄은 쓰지 않는다.

[런타임 토큰 절감]
9. structure 자동 탐색은 focused 우선, full은 300KB 이하만 자동 사용한다.
10. Phase 1은 analysis_progress.md에 procedure_runtime_index를 반드시 생성한다.
11. Phase 2..N은 procedure_runtime_index의 해당 procedure slice만 읽는다.
12. index_status가 READY이면 structure json을 다시 읽지 않는다. INDEX_INCOMPLETE일 때만 targeted fallback read.
13. 전역 confirmed call edges 누적 본문 블록은 만들지 않는다. procedure별 local_call_edges + 전역 id 요약만 쓴다.
14. MSC는 HLD md에 inline하지 않고 별도 msc_<procedure_slug>_<ts>.puml 파일로 저장한다. HLD md에는 msc_ref 링크와 산문만 남긴다.

[분석 안전]
15. 한 번에 procedure 하나만 분석한다. DONE procedure는 재분석하지 않는다.
16. CNF handler는 단일로 가정하지 않는다. ipc_cnf_handlers[] 후보로 두고 procedure별로 확정한다.
17. 미확인 flow는 추측하지 말고 [RN]으로 남긴다.

[입력 편의 — 사람이 적을 값 최소화]
18. slug는 Phase 0에서 한 번 확정하면 NEXT_STEP_5.2.md의 current_slug에 기록한다. 이후 단계 prompt에서 slug가 비어 있으면 current_slug를 자동 승계한다. 사람이 매번 다시 적지 않는다.
19. <YYYYMMDD_HHMM_KST> 같은 타임스탬프는 사람이 적지 않는다. 새 파일을 만들 때 도구가 현재 KST 시각으로 채운다.
20. structure_json은 사람이 파일명을 적지 않는다. output/5.2/<slug>/ 에서 최신 *_focused.json을 자동 선택한다.
21. 매 응답의 진행줄 다음 줄에 "▶ 다음 붙여넣기: prompt/<파일>.md"로 다음에 붙여넣을 copy prompt를 한 줄 안내한다. 사용자가 어느 파일을 열지 스스로 판단하지 않게 한다.

이 규칙을 이해했으면 "세션 규칙 적용 완료"라고만 답하고, 내가 다음에 붙여넣을 단계 prompt를 기다려라.
[진행: SESSION_READY → 다음: TRACK_B_OR_PHASE0]
▶ 다음 붙여넣기: 대형 코드면 prompt/copy_track_b.md, 아니면 prompt/copy_phase0.md
```
