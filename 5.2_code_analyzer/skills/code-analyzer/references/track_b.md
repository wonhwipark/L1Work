# Track B — 정적 구조 추출 (대형 코드 선행)

대형 코드에서 토큰 절감을 위해 structure_*.json을 먼저 만든다. Phase 0이 이 파일을 자동으로 찾는다.

입력: 코드 루트, 블록/API 이름. (slug는 비우면 자동 생성)
기본 IPC 패턴: REQ = `HAL_ _REQ SendMsg PostMsg`, CNF = `_CNF CnfHandler MsgDispatch`.

규칙:
1. 산출물 경로는 `output/5.2/<slug>/`로 통일한다.
2. 기본 저장은 `output/5.2/<slug>/structure_<ts>_focused.json`. (`<ts>`=현재 KST, 도구가 채움)
3. full을 만들면 `structure_<ts>_full.json`. full이 300KB 초과면 Phase 0 자동 read 대상이 아니므로 focused를 별도 생성한다.
4. `extraction_mode`는 enum 하나만. fallback `git → bash → powershell → internal_search → mixed`.
5. CNF handler는 단일 가정 금지. `ipc_cnf_handlers[]` 후보 배열로 기록.
6. `ipc_req_sites[]`, `ipc_cnf_handlers[]`, `call_edges[]`에 안정적 id 부여.
7. grep/검색은 패턴별 최대 200줄까지만 1차 수집. raw AST·전체 symbol table 덤프 금지.
8. 300KB 초과 시 요약, 1MB 초과 시 focused로 축소.
9. `NEXT_STEP_5.2.md`를 canonical path 기준으로 갱신.

완료 출력: structure_json, slug, canonical_path, extraction_mode, file_count, total_loc, ipc_req_sites 수, ipc_cnf_handlers 수, structure_scope, structure_size.
진행줄: `[진행: TRACKB_DONE → 다음: TRACK_A_PHASE0]` → Phase 0 자동 진행.
