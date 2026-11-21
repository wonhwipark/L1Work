# Viewer 환경설정 v0.3.0 — 업무 GPT/Linux Agent G0·최소 연결·검증 인계

- Work: `L1-WORKSPACE-RAG-20261111-001`, 2026-11-21 KST
- 원본: GitHub PUBLIC `wonhwipark/L1Work`, branch `main`
- 정확한 인계 경로: `handoffs/L1_WORKSPACE_VIEWER_PREFERENCES_V030_G0_INTEGRATION_HANDOFF_r0001_20261121_KST.md`
- 소스·시험 ZIP: `main/l1-workspace-viewer-preferences_v0_3_0_1121.zip`, **20,661 B**, SHA-256 `228c60bada8a92591f7ae855dfabe206e018d9e59970cf2d1b773d4d00072812`.
- 선행 Write v0.2.0: `main/l1-workspace-viewer-write-ui_v0_2_0_1121.zip`, 21,171 B / SHA-256 `9f2df44348478eb44615bddef8f211645fa1c07ed71d43580b4fb324e376b6f9`; 선행 v0.1.2 SHA `9be14c4c34c2a7d923d8b11c01fb0249d41e820861721f275001f0f7d499d9e3`.
- **판정:** 개발용 PUBLIC ZIP 전달. 기존 설치본 재사용 필수. **실 Linux 운영 반영/브라우저 E2E/Write 활성화 NOT_RUN**. ZIP 다운로드가 자동 설치·Job 수행·유료 리뷰 승인 아님.

## 구현된 부분

사용자·브라우저별 표시 설정(localStorage), 화면 영역 표시/숨김 9종, 문서 필터 6종, 테마·밀도·글자크기, 저장/초기화/취소, 다른 탭 반영, 없는 저장소 안전 실패. [수정] 인증/세션/CSRF/ACL/CAS, 기존 writer, MSC iframe은 수정하지 않음. 기본 READ_ONLY 유지. 익명 사용자는 **브라우저 프로필만** 식별하며 기기간 사용자 동기화는 지원한다고 주장하지 않음.

## 실제 Linux 수행 순서

1. READ ONLY G0: 기존 Viewer 실제 소스 경로/branch/revision·운영 여부, `#doc-actions`, DOM 섹션/문서 목록/스타일 토큰/CSP/MSC origin, 현재 Write v0.2.0 설치 여부·권한/백업·rollback, 현재 화면 1440/720/390/320 확인. 미확인값 추정 금지.
2. 고정 SHA로 1차 v0.1.2 + Write v0.2.0 + 환경설정 v0.3.0 세 ZIP을 검증. 기존 Write 패키지의 `tools/apply_to_v012.py`로 **조립된 v0.2.0 Viewer 후보**를 만든 뒤 환경설정 ZIP의 `tools/apply_to_viewer.py`로 새 후보를 작성. 기존 ZIP/운영 원본 불변. 출력 실패/체크섬 manifest 발견이면 **BLOCKED**로 멈추고 수동 원본 훼손 금지.
3. 실제 Viewer의 표시 영역과 문서 카드 중 검증된 곳에만 `data-l1-section` / `data-l1doc-type`을 연결. 현재 Viewer DOM을 추측한 셀렉터 강제 적용 금지. 필요한 경우 호스트의 불투명 non-secret 사용자 ID를 `window.L1ViewerPrefsIdentity={id:'opaque_id'}`로 제공하고 사용자 전환 시 `l1viewer:profile-changed` 이벤트. 계정 DB/토큰/비밀번호 저장 금지.
4. 테스트: 익명 Read Only, 계정 전환/공유 PC/새 탭/재접속, 초기화·취소·저장 실패·필터 복원, 검색/문서 목록/MSC·HLD 정상, Write 버튼/로그인/초안/preview·commit 영향 0, CSP/접근성/반응형/백업·롤백. **B1~B3/EAuth/E3/E4의 기존 운영 쓰기 게이트는 별도 유지**.
5. 사용자에게 `G0/DOM_FILTER/PROFILE_STORAGE/WRITE_COMPAT/BROWSER/SECURITY/HOST_DEPLOY` 각각 PASS/FAIL/NOT_RUN/BLOCKED와 Work Evidence·rollback 위치를 보고. 운영 승인/실제 G0 및 게이트 통과 전 **운영 적용하지 말 것**.

## 개발자 자체시험 범위

Node `node --test tests/preferences.test.cjs` **16/16 PASS**, Python `python -m unittest discover -s tests -p 'test_*.py'` **14/14 PASS**. JS syntax, Python compile, ZIP CRC/path/manifest PASS. Linux 실제 빌드/브라우저 자동화/운영 Writer 통합/독립 코드리뷰 **NOT_RUN**. 패키지는 `development_not_for_deployment`.

비민감 G0/시험 결과만 같은 Work에 회신. 회사 코드/로그/고객정보/인증·키를 L1Work/CoWork PUBLIC으로 옮기지 않음.
