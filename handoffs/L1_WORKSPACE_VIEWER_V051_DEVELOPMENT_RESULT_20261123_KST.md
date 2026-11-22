# Viewer v0.5.1 개발/검증/전달 결과 — 2026-11-23 KST

- Work: `L1-WORKSPACE-RAG-20261111-001`
- 기존 ZIP 보존: `l1-workspace-viewer-wiki-integrated_v0_5_0_1122.zip` / 117897 bytes / `a133d8703cc36a7f74cce8de1fd37db757052ed6a44030bc05fea89a05c253fa`.
- 신규 ZIP: `l1-workspace-viewer-wiki-integrated_v0_5_1_1123.zip` / **349332 bytes / 34 entries / SHA-256 `0bc0240261e29c863c541e9650e9f99271b2b924ffd52be753598889f66cf290`**.
- v0.5.0 34개 소스 전체 계승, assistant.js/CSS/index/standalone/version/source-pin/manifest/README만 기본 숨김과 metadata 갱신. Write v0.2.0 3개 파일 SHA 불변.
- 동작: 문서 목차 기본, 도우미 상단 명시적 버튼; 오늘 업무 기본 목록 전체폭, 채팅 버튼/상단 버튼으로만 열기; ESC/닫기; Work별 초안 유지; 크게 보기 명시적 진입. Demo 모드 유지.
- 실제 정적 확인: 원본 SHA PASS, deflate 34개 decode PASS, 변경 anchor PASS, Write hash PASS, 생성 ZIP 34개 전체 roundtrip hash PASS, SHA-256 표준 벡터 PASS, standalone CSP 재산출 PASS.
- 기존 v0.5.0 Node 25 PASS는 **과거 버전 근거**. 신규 v0.5.1 Node/browser E2E/Linux G0/LLM·Agent/Writer/운영 설치는 **NOT_RUN**.
- 독립 리뷰: 사용자 결정에 따라 SKIP_BY_USER. 재요청 0. 배포 상태: `development_not_for_deployment`.
- 업무 GPT 신규 단일 완결 인계 `handoffs/L1_WORKSPACE_VIEWER_V051_TODAY_ASSISTANT_HANDOFF_r0001_20261123_KST.md`(기존 v0.5.0 인계 내용 모두 내장). 이전 ZIP/HO는 업무 GPT에 전달 불필요.
- 다음 한 동작: 업무 GPT가 새 ZIP과 완결 인계만으로 실제 Viewer G0와 A01~A10/H01~H05 검증. 무단 운영 적용 금지.
