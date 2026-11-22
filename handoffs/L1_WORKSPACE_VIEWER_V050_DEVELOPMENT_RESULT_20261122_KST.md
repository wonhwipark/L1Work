# Viewer v0.5.0 개발·전달 결과

- Work: L1-WORKSPACE-RAG-20261111-001
- 2026-11-22 KST. 상태: 개발 후보. 운영 설치·실행 활성화 미수행.
- 요청: v0.4.1 기반 개발, 우측 업무 도우미·오늘 업무 탭, L1Work 개발 ZIP/미리보기/업무 GPT HO 전달.

## 변경

- v0.4.1의 필터 본문 보존, 전체 제목 확인, 너비 조절·설정 저장·모바일 탐색·가독성 개선 포함.
- 우측 목차/업무 도우미 전환·상단 도우미·크게 보기·오늘의 업무 화면·목록/대화·Work/문서/source revision 표시.
- Work별 대화/초안 메모리 분리, 문서/오늘 탭간 공유. 프로필 전환 시 메모리 대화 초기화. 재로딩 후 대화 복원은 미구현.
- 기본 합성 모드. 실제 LLM·Runner·업무 저장 0. 화면용 bridge와 실제 서버 기능을 구분.
- 실제 호스트 연결용 질문/실행 제안/실행/상태 조회 DTO·인증/권한 capability 검사·원본 revision 고정·영수증 필수·중복 전송 차단·불확실 응답 자동 재실행 금지.
- 결과 docId 링크만 인코딩하여 열기. 답변에 임의 HTML/URL 실행 없음.

## 실제 자체시험

기존 회귀 **10 PASS**, 신규 계약·상태 시험 **15 PASS**, 전 JS/inline JS 구문·중복 HTML ID·asset 연결·단독 HTML 동등성·Write 원본 해시·알려진 credential 패턴·ZIP SHA/CRC/manifest·2회 결정형 빌드 PASS. 시험은 source/순수 함수/DOM stub이며 브라우저 레이아웃과 실제 서비스 보안을 증명하지 않음.

## 미검증

사용자 요청대로 실제 브라우저/업무 데이터/API/LLM·Agent/권한·프로필/요청 복구/Writer/MSC/운영 E2E는 업무 환경에서 수행. 독립 리뷰 NOT_RUN, 신규 유료 요청 0. 기존 3 stream 원본 재고정/정식 통합 게이트 NOT_RUN. 새 stream은 같은 Work에 등록하며 다른 창 미등록 변경 자동 발견 보장 없음. 실제 설치 스킬 변경 0.

## 산출물

- `wonhwipark/L1Work`, `main`, 루트 `l1-workspace-viewer-wiki-integrated_v0_5_0_1122.zip`
- **117,897 bytes / 34 entries / SHA-256 `a133d8703cc36a7f74cce8de1fd37db757052ed6a44030bc05fea89a05c253fa`**
- `handoffs/L1_Workspace_Viewer_v0_5_0_20261122_KST.html`
- `handoffs/L1_WORKSPACE_VIEWER_V050_TODAY_ASSISTANT_HANDOFF_r0001_20261122_KST.md`
- `handoffs/L1_WORKSPACE_VIEWER_V050_SHA256SUMS_20261122_KST.txt`

개발물 공개 전달은 정식 운영 배포를 의미하지 않아요.

다음 한 동작: 업무 GPT가 인계서와 고정 ZIP을 받아 실제 Viewer G0 → 기존 read/실행/상태 writer 연결 → A01~A10 검증을 현재 승인 범위에서 진행. 운영 적용은 별도 현장 판정.
