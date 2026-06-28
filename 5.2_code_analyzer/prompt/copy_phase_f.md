# copy_phase_f — Phase F HLD 마무리 실행용 복사 프롬프트

아래 블록만 Claude Code/Roo Code에 복사해서 사용한다. `prompt/5.2_track_a_prompt.md` reference 문서는 런타임에 다시 읽지 않는다.

```text
Track A Phase F를 수행해서 블록 HLD성 md를 마무리해줘.

[입력]
- slug: (생략 가능 — 비우면 NEXT_STEP_5.2.md의 current_slug를 사용)

[자동 해석 규칙]
- slug를 비우면 NEXT_STEP_5.2.md의 current_slug를 읽어 쓴다.
- analysis_progress 경로는 output/5.2/<slug>/analysis_progress.md 로 자동 구성한다.
- 새로 만드는 파일의 <YYYYMMDD_HHMM_KST>는 사람이 적지 않는다. 도구가 현재 KST 시각으로 채운다.

[필수 규칙]
1. 선택된 procedure가 모두 DONE인지 확인한다.
2. 누락 procedure가 있으면 Phase F를 수행하지 말고 다음 procedure를 안내한다.
3. 블록 책임 1–2줄을 작성한다.
4. 외부 인터페이스 목록을 작성한다.
5. procedure 목록과 섹션 링크를 작성한다.
6. 각 procedure 섹션에 동작 설명과 msc_ref 링크가 있는지 확인한다.
7. 각 msc_ref가 output/5.2/<slug>/msc_<procedure_slug>_<YYYYMMDD_HHMM_KST>.puml 파일을 가리키는지 확인한다.
8. HLD .md 안에 PlantUML MSC inline block을 넣지 않는다.
9. 남아 있는 [RN] 목록을 별도 섹션에 정리한다.
10. hld_<block>_<YYYYMMDD_HHMM_KST>.md 최종본을 output/5.2/<slug>/에 저장한다.
11. overwrite 금지.
12. NEXT_STEP_5.2.md를 WAIT_NEW_BLOCK 상태로 갱신한다.

[완료 진행줄]
진행줄 마지막에는 다음에 붙여넣을 파일명도 함께 안내한다.
[진행: BLOCK_HLD_DONE:<slug> → 다음: WAIT_NEW_BLOCK]
▶ 다음 블록을 분석하려면 다음 붙여넣기: prompt/copy_phase0.md
```
