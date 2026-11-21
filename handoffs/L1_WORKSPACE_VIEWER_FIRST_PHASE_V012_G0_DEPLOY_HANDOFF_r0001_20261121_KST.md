# 업무 GPT 실행 인계 — 기존 Linux Viewer 1차 v0.1.2 적용 원샷

- 개정: r0001 / 2026-11-21 KST
- 정본 배포 저장소: GitHub PUBLIC `wonhwipark/L1Work` / branch `main`
- 정확한 인계 상대 경로: `handoffs/L1_WORKSPACE_VIEWER_FIRST_PHASE_V012_G0_DEPLOY_HANDOFF_r0001_20261121_KST.md`
- 이전 패키지: `l1-workspace-wiki-ui_v0_1_0_1119.zip` (267140 B, SHA-256 `411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9`), 기존 Linux 서비스 설치 여부 미확인
- **이번 전달 ZIP:** [`l1-workspace-viewer-ui_v0_1_2_1121.zip`](../l1-workspace-viewer-ui_v0_1_2_1121.zip), **74,940 B**, SHA-256 **`9be14c4c34c2a7d923d8b11c01fb0249d41e820861721f275001f0f7d499d9e3`**, Git blob **`6b9b3cb718044565e0b99aea8ba38a2ed3fa29de`**, PUBLIC commit **`4abf877a75d36388f1f4409edaaca1822f019cec`**. GitHub remote base64 바이트 readback PASS.
- **사용자 최신 지시:** 기존 정식 STYLE-DESIGN R1의 완료를 기다리지 않고 **독립 리뷰 생략 후 1차 배송·가능한 배포까지 진행**. 기존 완료 리뷰 이력·요청/영수증 불변. 2차 ID/PW·편집은 이번 범위 밖.
- **게이트 구분:** `PUBLIC_ZIP_DELIVERY=PASS` / `INDEPENDENT_STYLE_R1=USER_WAIVED` / `ACTUAL_HOST_G0/B1/B2/B3/E3/E4=NOT_RUN` / `LINUX_HOST_DEPLOY=NOT_RUN`; 이 문서로 호스트 설치 사실을 주장하지 않는다.

## 1. 기존 Viewer 재사용 및 변경 범위

**업무 GPT/허용된 Linux 로컬 Agent**가 아래 순서대로 처리. 업무 Host 실제 repo/branch/revision/서비스 ID가 확인되지 않으면 정확하지 않은 경로를 지어내지 말 것.

| 구분 | 1차 필수 내용 | 지켜야 할 불변식 |
|---|---|---|
| 시각 스타일 | 보라색 위주 → 업무용 `#1E40AF` 포인트 + 블루그레이 `#EFF6FF` 선택 배경, 저대비 보조 텍스트 보완 | 기존 좌측 트리·중앙 본문·우측 목차·모바일 우선 레이아웃 유지 |
| Work 제목 | **검증된 대표 이슈번호가 있을 때만** 번호를 제목 맨 앞에 1회 표시. 가상 예: `SOC-1234 — NR L1 Tx — UL Tx Switching 분석`. 없으면 검증된 제목/원래 Work ID 폴백 | 실제 Work ID·폴더·링크·Evidence/SHA 불변; 본문 문자열에서 이슈번호 임의 추정 금지 |
| 탐색·검색 | 목록·현재 문서·breadcrumb·검색 결과에 공통 표시 함수. 보조 행에 `Work ID` 원문 표시, 검색에서 이슈번호·제목·Work ID 검색 지원(기존 API 범위) | 신규 필수 DTO/DB·Index 스키마·업무 원본 writer 생성 금지 |
| MSC | 합성 MSC placeholder 가로 overflow일 때만 방향 안내. 실제 B형 MSC는 기존 격리된 `doc-converter` 결과와 현재 handler 재사용 | 렌더된 SVG/HTML을 기술 원본으로 저장 금지 |
| 열람 정책 | 기존 동료 무로그인 Read Only 보존 | 첫 화면 ID/PW 추가 금지, [수정]/인증/쓰기 UI 및 API는 이번 ZIP에서 아예 제외 |

**핵심:** PUBLIC ZIP에는 현재 v0.1.0을 바탕으로 수정한 HTML/CSS/JS·가상 fixture가 포함되어 있음. 그 자체가 업무 Linux Viewer 서버 코드/권한/API를 포함한 것은 아님. `viewer-wiki-ui/fixtures/` 합성 자료는 실제 서비스 data root·검색 인덱스에 연결하지 말 것. `issueKey` 필드는 UI 입력 **예시**이므로 실제 업무 Work 필드의 이름/존재를 단정하지 말 것.

## 2. 업무 GPT 원샷 실행 지시

1. **기존 업무 Linux Viewer 설치본 G0:** 현행 Viewer's 저장소·브랜치·revision, 실제 서비스 asset/CSP, 기존 읽기 handler/Work 목록/검색/MSC B형 renderer, 사용 권한·백업/rollback, 무로그인 Read Only 동작을 읽기 확인. 기존 Work 최신 근거가 있으면 재사용. 직접 접근 못 하면 유효한 Linux 로컬 Agent를 통한 기존 승인된 읽기 조회.
2. **ZIP 다운로드·안전 확인:** PUBLIC main의 위 정확한 파일 및 SHA-256/크기/CRC/manifest 검사. 기존 v0.1.0 소스·실제 설치본과 차이 확인. 원본 설치본/DB/Knowledge/Work/Evidence SHA 백업.
3. **기존 Viewer 코드에 최소 이식:** ZIP `viewer-wiki-ui/assets/work-labels.js`·`professional-theme.css` 및 필요한 `app.js`·adapter diff를 기존 해당 UI 프레임워크에만 이식. 기존 허용된 index/metadata에서 대표 이슈번호·Work title·Work ID를 연결하고 미확인 필드는 null fallback. 운영에서는 fixture/합성 PUBLISHED/fixture-r1/미검증 상태를 제거 또는 미확인으로 표시. 신규 서비스·정본 metadata DB 만들지 말 것.
4. **실제 기능 시험:** 열람 무로그인(동료 1명 이상), 기존 Work ID/링크/원본 SHA 불변, SOC 번호 있음/없음/복수/중복, 검색·breadcrumb·선택 상태, 모바일 1440/720/390/320, 키보드, MSC 6/12 overflow, 대비·색상만으로 상태 전달하지 않음을 확인. Test=PASS/FAIL/NOT_RUN, 개별 SHA/revision 근거는 업무 Work에 보존.
5. **보안·운영 게이트:** B1 canonical path containment, B2 Work title/search/raw/cache/download 제한정보 보호, B3 MSC 별도-origin sandbox/CSP, E3 localhost 실제 서비스 UI/롤백, E4 기존 동료 공유 범위 실제 열람 시험을 해당 revision에서 확인. 무로그인 정책이 자격증명 없이 **쓰기 허용**으로 변하지 않았는지도 점검.
6. **배포:** 위 게이트가 충족되고 실제 서비스 설치·재시작·공유 권한 및 기존 유효 승인 범위가 확인된 경우에만 백업→좁은 파일 변경→서비스 반영→브라우저와 동료 사용 확인→원격 revision/SHA readback 및 rollback 검증. **이번 사용자 지시는 1차 Viewer 배포 진행 의도**지만, 업무 호스트 권한을 확인하는 단계를 생략하거나 안전 검증 실패를 무시하는 허가가 아님.
7. Linux 설치까지 못 하면 가능 범위의 후보 코드·diff·시험·원본 SHA와 정확한 BLOCKED 사유를 **기존 업무 Work**에 기록하고 사용자가 다시 요구사항을 입력하게 하지 말 것. 이 공개 인계서 게시가 자동으로 업무 GPT/로컬 Agent를 실행하지 않음.

## 3. 1차 수락 보고 (숫자 중심)

코드: **1 PASS / 2 FAIL / 3 NOT_RUN / 4 BLOCKED / 5 UNKNOWN**.

| 구분 | 값 |
|---|---|
| 실제 Linux Viewer G0/권한 확인 | 숫자 |
| Work 이슈번호·제목/검색 연결 | 숫자 |
| 블루그레이 UI/접근성/MSC 안내 | 숫자 |
| 기존 동료 무로그인 Read Only·원본 ID/SHA 불변 | 숫자 |
| B1 / B2 / B3 | 숫자 3개 |
| E3 / E4 | 숫자 2개 |
| 기존 Viewer 운영 적용 및 rollback/readback | 숫자 |

통합 1행: `현재=... | 변경=... | 실제시험=... | 미검증/차단=... | 결과=업무 Work 내부 | 다음 한 행동=...`.

회사 제한 코드·상세 MSC·로그·계정·토큰/서버 내부 절대경로는 L1Work/CoWork GitHub로 반출하지 않음. 이번 1차에는 2차 인증/편집, 스킬 변경, 그룹 Knowledge 자동 게시, 유료 Claude 독립 리뷰를 연결하지 않음.

## 4. 요청 리뷰 이력·사용자 생략 결정

이전 `REQ-L1-WORKSPACE-VIEWER-STYLE-DESIGN-R1-20261121`은 2026-11-21 오전 확인 기준 REQUEST/SOURCE_PIN만 원격에 있었고, 보호 서명·READY·결과/영수증은 미관측. **사용자가 그 리뷰 없이 진행하라고 정정했으므로, 보호된 signer/watcher는 이 ID에 대해 새 승인·서명·READY·모델 호출을 시작하지 말 것.** 기존 원본·고정 PIN·기존 영수증을 삭제·수정해 재요청하지 말 것. 이 문서만으로 Windows watcher의 실행 차단이 물리적으로 검증된 것은 아니므로 실제 Windows 승인/디스패치 담당자의 확인이 남음.
