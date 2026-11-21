# 업무 GPT 실행 HO — L1 Workspace Viewer 2안 Wiki 통합 v0.4.0

- 작성: 2026-11-21 KST
- 기존 Work: `L1-WORKSPACE-RAG-20261111-001`. 같은 목적의 신규 Work·DB·스키마/서비스 생성 금지, 기존 Linux Work/분석·시험·리뷰 결과를 먼저 재개.
- 정확한 저장소: PUBLIC `wonhwipark/L1Work`, branch `main`
- 정확한 인계 파일: `handoffs/L1_WORKSPACE_VIEWER_WIKI_INTEGRATED_V040_G0_AND_E2E_HANDOFF_r0001_20261121_KST.md`
- **신규 단일 전체 UI ZIP**: `l1-workspace-viewer-wiki-integrated_v0_4_0_1121.zip` (루트), **236,326 bytes** / SHA-256 **`474db38255de06540b888241c0ee96f94feb09e48d9ee767768f50469d5ee7b3`** / Git blob `f20fcc97d14afad2274d35fba620727cd78b2aa9`
- 합성 단독 미리보기: `handoffs/L1_Workspace_Viewer_Wiki_Integrated_Preview_v0_4_0_20261121.html` / 114,175 bytes / Git blob `1a378141e37ecbddc17144192e7e697ca8a98858`; 이 HTML은 인라인 스크립트 합성 DEMO로 운영 서비스에 배포 금지.
- GitHub 업로드 commit `0cd3b2d36a79d939babfe73b3e7be716d47e1069`; remote ZIP Base64 전체 byte/size/SHA 및 HTML 원격 본문 readback PASS.
- **판정**: `PUBLIC_INTEGRATED_DEVELOPMENT_ZIP=PASS`; `REAL_LINUX_VIEWER_G0/BROWSER_E2E/WRITE_WRITER/B1/B2/B3/E3/E4/DEPLOY=NOT_RUN`, `development_not_for_deployment`. 사용자 요청은 공개 전달까지이며 실제 Linux 서비스 설치/새 인증·Writer 활성화·Job·유료 모델 호출 승인은 별도 유효 범위 확인.

## 1. 세 입력 고정 및 현재 버전 정합성

| 기준 UI/기능 | 변동 없는 기존 ZIP | SHA-256 | 통합 사용 |
|---|---|---|---|
| **2안 팀 위키형 + Blue Gray** | `l1-workspace-viewer-ui_v0_1_2_1121.zip` | `9be14c4c34c2a7d923d8b11c01fb0249d41e820861721f275001f0f7d499d9e3` | 3단 Wiki 레이아웃·Work 제목/검색/MSC overflow 안내 |
| Write UI | `l1-workspace-viewer-write-ui_v0_2_0_1121.zip` | `9f2df44348478eb44615bddef8f211645fa1c07ed71d43580b4fb324e376b6f9` | [수정]·편집자 인증·Diff/Preview·Draft/Commit 요청 UI |
| 환경설정 UI | `l1-workspace-viewer-preferences_v0_3_0_1121.zip` | `228c60bada8a92591f7ae855dfabe206e018d9e59970cf2d1b773d4d00072812` | 화면/문서 필터·테마/크기/밀도·프로필 저장/초기화 |

위 세 ZIP은 각각 별도 원본으로 보존. 이번 **v0.4.0 전체 통합 ZIP을 단일 프런트 소스로 사용**하며 다시 v0.2.0/0.3.0 patch utility를 중복 적용하지 말 것. 기존 Workflow `l1-fix-workflow_v1_6_75_1121.zip`/Kernel `work-ledger-kernel_v0_7_43_1121.zip` 관련 스킬 전체 ZIP도 기존 HO r0003에 따라 별도 관리.

## 2. 이전 디자인 불일치 보완

- 사용자 확정 **2안 Confluence 계열 팀 위키 정보구조** 보존: 상단 제품명/검색, 좌측 Work·Knowledge·전체 파일 탐색, 중앙 제목·문서·MSC, 우측 목차/근거/원본 ID. Blue Gray theme CSS v0.1.2를 이어받으며 신규 UI는 추가 CSS로 좁게 보완.
- 기존 환경설정 v0.3.0은 **재그리는 `#doc-actions` 안에 버튼을 삽입**해 문서 변경 후 버튼이 사라질 수 있음. 이번 통합에서 **고정 `.topbar`**로 이동해 연속 표시.
- 사용자 표시 정책: Work/Knowledge 기본 표시, **전체 파일 메뉴 기본 감춤**(사용자 설정에서 복원). `index`, `transfers` 폴더 기본 가림 및 추가 폴더명 쉼표 구분 입력. 화면·문서 필터·localStorage 저장/취소/초기화 기능 유지. DOM 자료의 표시 필터이며 **원본 삭제·서버 접근 제한이 아님**. 직접 deep link, 검색/raw/download/API는 Linux 서버의 ACL과 보호 정책으로 별도 통제.
- 소규모 UX 개선: 탭별 마지막 문서, 이동 전 읽던 위치, 검색어 유지, 합성 MSC 상단 링크 `msc-six` 하드코딩 대신 실제 관련 ID(데모 내) 사용. 실제 Linux canonical 문서 분류/MSC HTML anchor/source revision 연결과 별도 origin 보안은 G0 이후.
- v0.3.0 원래 화면 영역 분류 9종·문서종류 6종은 보존. 업무 Linux 문서 kind/source 매핑은 설치본 기준 확인(미확인 모델의 `data-l1doc-type` 존재를 가정하지 않음).
- 스킬과 기술 원본은 변경 0, 정본 Work ID/Evidence SHA 불변. 기존 Write UI는 `window.L1ViewerWriteHostAdapter` 부재 시 **수정 버튼 disabled**, 서버 저장 0.
- **유보**: 기존 CSS 파일의 중복 규칙 전량 재정리, 실제 computed-style/접근성·Chromium 1440/720/390/320 E2E 및 실제 Doc Converter B형 MSC 연결은 이번 통합 패키징에서 독립 완료되지 않음. 합성 단독 HTML 시연으로 운영 PASS를 주장하지 말 것.

## 3. 업무 GPT / Linux Agent 원샷 실행 지시

1. CoWork `main/collab/CONTEXT_BRIEF.md` → `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md` → 본 HO, 그리고 이미 유효한 업무 Linux 기존 Work/결과를 먼저 읽어 실제 서비스/브랜치/revision/템플릿·버전·UI·CSP·기존 DOM·읽기 API·권한/승인 범위 G0 확인. 기존 소스/공유용 Linux URL을 추측하여 보고하지 말 것.
2. 다운로드된 신규 v0.4.0 ZIP의 SHA-256/size/CRC/manifest 전체 검사, path traversal/symlink/민감정보/필수 파일 확인. `viewer-wiki-ui/index.html`은 분리 asset을 쓰는 **합성 UI**로, `viewer-wiki-ui/standalone-preview.html`은 현장 배포용이 아닌 단독 인라인 DEMO.
3. 실제 Linux Viewer는 **기존 서비스 재사용**. 업무 제한 자료인 `window.WikiFixtures`의 가상 데이터 대신 호스트의 승인된 읽기 Adapter/문서 종류/검색/raw/Knowledge/Work·Evidence/MCS 핸들러로 최소 CONNECT. Workspace root를 미검증 웹 document root로 직접 공개하지 말 것.
4. Write 서버는 기존 문서별 session/CSRF/ACL/source revision/CAS·writer/Evidence/receipt/readback/rollback을 검증. `l1-fix-workflow`의 기존 Work 선택/재개와 Kernel 원장·Evidence 기록, Updater Knowledge source owner를 구분. 합성 프런트 adapter 이름을 Linux API 실존으로 가정 금지. 미구현/미권한이면 `EDIT_DISABLED`.
5. 보안/회귀: 동료 무로그인 Read Only, Write 인증/권한 회수/stale/중복 저장/실패, Work/Knowledge/전체파일 메뉴·폴더별 숨김/복원/문서/화면 필터 저장·초기화/프로필 전환, **문서 이동 3회 뒤 상단 환경설정 버튼과 [수정] 버튼 둘 다 존재**, 이동 후 스크롤/MSC 복귀/검색 유지, 긴 제목·1440/720/390/320·6/12 participant, B1 path canonical/symlink, B2 제한정보·검색/raw/cache/download, B3 격리 HTML iframe origin/sandbox/CSP, EAuth/E3 localhost/E4 동료 2계정.
6. 운영 설치/Write ON은 실제 호스트 승인·동일 Writer CAS/readback·backup/rollback 및 관련 게이트 PASS 이후만. 미통과는 해당 단계 BLOCKED/NOT_RUN, 나머지 개발·시험 계속. 실서비스나 DB, 토큰, PUBLIC 게시 확대 금지.
7. 업무 Work/Evidence에 실제 diff/시험 결과/호스트 source SHA/다음 한 행동 저장. 제한 코드·상세 MSC/로그·키/개인 정보는 CoWork/L1Work PUBLIC 게시하지 말 것. 업무 GPT 실행 결과는 검증된 비민감 상태만 설계 GPT에게 회신.

## 4. 테스트 및 보고

- 설계 GPT 직접 확인: 공개 입력 ZIP 3종 SHA-256 및 압축 내 각 파일 CRC PASS; 새 통합 ZIP 20 entries 전체 CRC+SHA manifest 검증 PASS; GitHub main 원격 ZIP/HTML byte readback PASS.
- 설계 GPT 직접 **미수행**: JavaScript 새 통합본 브라우저 실행·상호작용·키보드/모바일, 기능별 Node 테스트 재실행/독립 코드 리뷰, 실제 Linux G0/보안/B1~B3/E3/E4/Writer E2E/운영 설치.
- 숫자 보고: `1 PASS / 2 FAIL / 3 NOT_RUN / 4 BLOCKED / 5 UNKNOWN`. 반환 필드 `G0/UI_WIKI/READ_ONLY/PREFS_MENU/FOLDER_HIDE/PROFILE/NAV_RESUME/WRITE_WF_KERNEL/MSC/B1_B2_B3/E3_E4/REAL_WRITE/HOST_DEPLOY` 및 근거 위치+다음 한 행동.

**다음 한 동작:** 업무 GPT가 본 통합 단일 ZIP과 HO를 수신하여 기존 Linux Viewer 현장 UI·Adapter G0와 대조하고, 코드/브라우저 회귀·보안/Writer E2E를 허용된 범위에서 진행.
