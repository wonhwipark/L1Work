# Phase F — 블록 HLD 마무리

slug 자동 승계. 타임스탬프 도구가 채움.

규칙:
1. 선택된 procedure가 모두 DONE인지 확인. 누락 있으면 Phase F 수행하지 말고 다음 procedure 안내.
2. 블록 책임 1–2줄 작성.
3. 외부 인터페이스 목록 작성.
4. procedure 목록과 섹션 링크 작성. 각 procedure 섹션에 동작 설명과 msc_ref 링크 확인.
5. 각 msc_ref가 `output/5.2/<slug>/msc_<procedure_slug>_<ts>.puml`을 가리키는지 확인.
6. HLD .md에 PlantUML MSC inline 금지.
7. 남은 `[RN]` 목록을 별도 섹션에 정리.
8. `hld_<block>_<ts>.md` 최종본을 `output/5.2/<slug>/`에 저장. overwrite 금지.
9. `NEXT_STEP_5.2.md`를 WAIT_NEW_BLOCK 상태로 갱신. block_stack에 보류 중인 블록이 있으면 복귀를 안내한다(block_switch.md).

진행줄: `[진행: BLOCK_HLD_DONE:<slug> → 다음: WAIT_NEW_BLOCK]`.
