# copy_track_b — Track B 실행용 복사 프롬프트

아래 블록만 Claude Code/Roo Code에 복사해서 사용한다. `prompt/5.2_track_b_prompt.md` reference 문서는 런타임에 다시 읽지 않는다.

```text
code-analyzer Track B로 정적 구조를 추출해줘.

[입력값]
- 코드 루트: <코드루트경로>
- block/API 이름: <블록명 또는 API명>
- target slug: <선택, 비우면 자동 생성>
- 분석 확장자: .c .cpp .h .hpp
- 제외 폴더: test/ third_party/ build/
- IPC REQ 패턴: HAL_ _REQ SendMsg PostMsg
- IPC CNF 패턴: _CNF CnfHandler MsgDispatch

[필수 규칙]
1. 산출물 경로는 반드시 output/5.2/<slug>/ 로 통일한다.
2. 기본 structure 저장 경로는 output/5.2/<slug>/structure_<YYYYMMDD_HHMM_KST>_focused.json 이다.
3. full structure를 생성할 경우 output/5.2/<slug>/structure_<YYYYMMDD_HHMM_KST>_full.json 으로 저장한다.
4. full structure가 300KB를 초과하면 Track A 자동 탐색 대상이 아니므로 focused structure를 별도로 생성한다.
5. %USERPROFILE%\artifacts\code_analyzer\<slug> 경로는 사용하지 않는다.
6. extraction_mode는 git | bash | powershell | internal_search | mixed 중 하나만 사용한다.
7. fallback 순서는 git → bash → powershell → internal_search → mixed 이다.
8. CNF handler는 단일로 가정하지 말고 ipc_cnf_handlers[] 후보 배열로 기록한다.
9. ipc_req_sites[], ipc_cnf_handlers[], call_edges[]에는 안정적인 id를 부여한다.
10. grep/검색 결과는 패턴별 최대 200줄까지만 1차 수집한다.
11. raw AST와 전체 symbol table 덤프는 금지한다.
12. 300KB 초과 시 요약, 1MB 초과 시 focused structure로 줄인다.
13. NEXT_STEP_5.2.md를 canonical path 기준으로 갱신한다.

[완료 출력]
- structure_json
- slug
- canonical_path
- extraction_mode
- file_count
- total_loc
- ipc_req_sites 수
- ipc_cnf_handlers 수
- structure_scope
- structure_size
- auto_read_policy: focused 우선, full은 300KB 이하만 자동 사용

마지막 진행줄은 반드시 아래 형식으로 출력한다. 다음에 붙여넣을 파일명도 함께 안내한다.
[진행: TRACKB_DONE → 다음: TRACK_A_PHASE0]
▶ 다음 붙여넣기: prompt/copy_phase0.md
```
