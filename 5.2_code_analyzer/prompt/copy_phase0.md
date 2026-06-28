# copy_phase0 — Track A Phase 0 실행용 복사 프롬프트

아래 블록만 Claude Code/Roo Code에 복사해서 사용한다. `prompt/5.2_track_a_prompt.md` reference 문서는 런타임에 다시 읽지 않는다.

```text
code-analyzer 스킬로 Track A Phase 0을 수행해줘.

[입력]
- 코드 루트: <코드루트경로>
- 진입 모드: <블록명 또는 API명>
- target slug: <선택, 비우면 자동 생성>
- 분석 확장자: .c .cpp .h .hpp
- 제외 폴더: test/ third_party/ build/
- structure.json: 자동

[필수 규칙]
1. slug를 확정한다.
2. canonical path는 반드시 output/5.2/<slug>/ 이다.
3. %USERPROFILE%\artifacts\code_analyzer\<slug> 경로는 사용하지 않는다.
4. structure.json 자동 탐색 우선순위는 아래와 같다.
   a. output/5.2/<slug>/structure_*_focused.json 최신 파일
   b. output/5.2/<slug>/structure_*.json 중 파일 크기 300KB 이하인 최신 파일
   c. 300KB 초과 full structure는 자동으로 열지 않는다. 사용자가 명시한 경우에만 사용한다.
5. structure가 없으면 Phase 0 focused extraction으로 output/5.2/<slug>/structure_<YYYYMMDD_HHMM_KST>_focused.json을 생성한다. <YYYYMMDD_HHMM_KST>는 사람이 적지 않고 도구가 현재 KST 시각으로 채운다.
6. Phase 0에서는 source body 전체 read를 금지한다.
7. 파일 목록, LOC, 후보 함수명, 후보 line 중심으로만 구조맵을 만든다.
8. grep/검색 결과는 패턴별 최대 200줄까지만 1차 수집한다.
9. extraction_mode는 git | bash | powershell | internal_search | mixed 중 하나로 기록한다.
10. structure meta.root와 입력 코드루트가 다르면 경고하고 멈춘다.
11. output/5.2/<slug>/analysis_progress.md를 생성/갱신한다.
12. analysis_progress.md에는 structure 자동 선택 근거와 structure_size를 기록한다.
13. NEXT_STEP_5.2.md를 갱신한다. 이때 current_slug에 확정 slug를 기록한다. 이후 단계 prompt가 slug를 다시 입력받지 않고 이 값을 승계한다.

[완료 출력]
- slug
- canonical_path
- selected_structure_json
- structure_selection_reason
- extraction_mode
- structure_scope
- structure_size
- 다음 단계

마지막 진행줄은 반드시 아래 형식으로 출력한다. 다음에 붙여넣을 파일명도 함께 안내한다.
[진행: PHASE0_DONE → 다음: PHASE1_PROCEDURE_DISCOVERY]
▶ 다음 붙여넣기: prompt/copy_phase1.md
```
