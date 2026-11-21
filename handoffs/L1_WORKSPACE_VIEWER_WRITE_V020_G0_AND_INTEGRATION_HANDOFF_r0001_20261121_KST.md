# 업무 GPT 원샷 인계 — Linux Viewer 2차 Write 편집 연결 v0.2.0

- 작성: 2026-11-21 KST / Work: `L1-WORKSPACE-RAG-20261111-001`
- 대상: **기존 Linux Viewer** (새 서비스 생성 금지); GitHub PUBLIC `wonhwipark/L1Work`, branch `main`
- 인계 파일 상대 경로: **`handoffs/L1_WORKSPACE_VIEWER_WRITE_V020_G0_AND_INTEGRATION_HANDOFF_r0001_20261121_KST.md`**
- 기배송 1차 읽기 UI: [`l1-workspace-viewer-ui_v0_1_2_1121.zip`](../l1-workspace-viewer-ui_v0_1_2_1121.zip) / **74,940 bytes / SHA-256 `9be14c4c34c2a7d923d8b11c01fb0249d41e820861721f275001f0f7d499d9e3`**. 실제 Linux 설치는 이전 결과 기준 **NOT_RUN**.
- **이번 GPT 선행 구현물:** `l1-workspace-viewer-write-ui_v0_2_0_1121.zip`, 21,171 bytes / SHA-256 **`9f2df44348478eb44615bddef8f211645fa1c07ed71d43580b4fb324e376b6f9`**, 10 files CRC PASS, Node 30/30 + Python 8/8 자체시험 PASS, JS syntax PASS. **현재 대화 파일로 제공된 개발 후보이며 아직 L1Work/CoWork에 ZIP 바이너리로 게시된 것은 아님.** 다른 세션/업무 GPT가 이 GitHub 인계서만으로 해당 ZIP을 자동 수신한다고 가정하지 말 것. 사용자가 승인된 파일 전달 경로로 ZIP을 공급할 때만 정확한 SHA를 확인해 적용.
- Code Gate: **development_not_for_deployment**, 현장 인증·writer·B1~B3·E3/E4 모두 미실행. GitHub 인계 게시 자체는 Linux 구현/배포·계정 발급·쓰기 활성화 승인 아님.

## 1. 사용자 확정 요구

- **일반 열람은 무로그인 Read Only 유지**. 최초 Viewer의 실패했던 전체 로그인 기능 복원 금지; 동료에게 문서 열람용 ID/PW 요청 금지.
- **[수정] 누르면 편집 전용 ID/PW**. 인증 성공 뒤에도 **서버가 원본/문서별 편집 ACL과 세션·CSRF를 검증**해야만 초안·Diff/Preview·확정 저장 요청을 허용.
- 이슈 분석 본문·코멘트·MSC 설명 직접 편집을 지원하되, 원본 Work/Evidence/Knowledge 소유자는 기존 Workflow/Kernel/Updater writer로 재사용. 실제 Linux에서 지원 확인 전 새 writer/계정 DB/API를 사실로 가정하지 말 것.
- MSC **메시지·participant 수정/추가 의도**는 우측 편집 요청 UI에서 수집. 검증된 canonical anchors가 있으면 부모 DOM에서 선택하되, 별도 origin MSC iframe의 DOM·SVG를 직접 수정/저장/클릭으로 연동하지 않음. anchors 없으면 문서 수준 수정 요청 초안까지만 허용. MSC 구조 확정 저장 HOLD.
- 변경 후보 → 서버 재권한 검사 Diff/Preview → 명시적 초안 저장 또는 원본 revision/CAS 확인 후 확정 → 기존 writer readback. 저장 성공·렌더 실패는 **PARTIAL**, 불확실 저장은 **WRITE_UNCERTAIN**/임의 재시도 0. Knowledge 그룹 자동 게시/Agent 자동 실행 0.

## 2. 이미 만들어 둔 코드 — 교체할 필요 없이 그대로 활용

개발 ZIP 압축 해제 루트 `viewer-write-ui-v020/`:
- `assets/write-client.js`: 인증→편집 상태→원본 revision→서버 Diff/Preview→초안→한 번만 확정, SOURCE_STALE/WRITE_UNCERTAIN 단일 판단. server API 미연결은 fail-closed.
- `assets/write-ui.js`, `assets/write-ui.css`: 기존 `#doc-actions`에 [수정] 버튼 부착, 사용자 클릭 때만 인증 dialog, 승인 시 편집·MSC 요청 dialog, Ctrl 등 브라우저 저장 키 없이 메모리 초안. 서버가 `window.L1ViewerWriteHostAdapter`를 제공하지 않으면 [수정] 버튼은 보이지만 disabled. **실제 로그인 비밀번호 저장/전송 대상은 연결된 서버 owner만**, JS 지속 저장·URL·GitHub 게시 금지.
- `tools/apply_to_v012.py`: 위 정확한 v0.1.2 ZIP의 SHA-256·ZIP path/symlink/CRC를 검사하고 새 JS/CSS asset 3개를 추가한 `v0.2.0` **후보 ZIP 생성**. 단일 `index.html`의 세 anchor 개수 1일 때만 변경, 원본 v0.1.2 불변.
- `HOST_INTEGRATION.md`: 화면 UI에 필요한 논리 host adapter 계약, 서버 재검사·기존 writer 연결·B1~B3·EAuth/E3/E4.
- `tests/write-client.test.cjs`: Node 자체시험 30건 (인증 실패/권한 없음, base revision/CAS, draft readback, diff 권한, MSC anchor 및 COMMIT 금지, 불확실 write·중복 차단, logout/동시 요청 포함).
- `tests/test_patch.py`: Python 8건 (원본 ZIP SHA 고정, 중복 anchor·zip path/중복 파일 차단, manifest·재빌드).
- `preview.html`: **실제 계정/업무 데이터/저장 없는 가상 화면 목업**.

현재 v0.1.2 **원격 ZIP에서** `<link rel="stylesheet" href="assets/professional-theme.css">`, `<script defer src="assets/app.js"></script>`, `v0.1.2 · 합성 데이터` anchor 각각 1회 확인 PASS. 단, v0.2.0 전체 실제 ZIP 직접 생성/기존 브라우저 회귀는 **아직 NOT_RUN**(v0.1.2 전체 ZIP 로컬 복사 불가); 위 Python 모의 ZIP 시험과 실제 파일 적용은 구분.

## 3. 업무 GPT / Linux Agent 원샷 실행 순서

1. **READ_ONLY G0**: 이미 있는 업무 Viewer 실제 source/branch/revision, v0.1.2 적용 여부, 읽기 URL/handler/MSC origin/CSP, 동료 무로그인 유지, 편집자 인증 제공자(기존 로컬 OS·reverse proxy/내장 등), 문서별 edit ACL·CSRF·session rotate/TTL/rate-limit/계정 보호, 기존 Workflow/Kernel/Knowledge Updater 원본 writer/CAS/readback, canonical anchor provider를 설치 코드에서 확인. 확인한 항목만 REUSE/CONNECT/GAP/UNKNOWN.
2. **후보 패치와 격리시험**: 개발 ZIP이 사용자 대화 첨부에서 **실제로 전달된 경우에만** sha256 확인. 기배송 v0.1.2와 모두 준비됐으면 `python tools/apply_to_v012.py <v0.1.2 ZIP> <v0.2.0 candidate ZIP>`. 결과 manifest/CRC/소스 diff/Node/Python 시험. 제공되지 않았다면 `INPUT_ZIP=BLOCKED_NOT_TRANSFERRED`로만 보고하고 내용 추정·빈 파일 대체 금지.
3. **실제 backend 연결**: 설치된 서버의 검증된 인증자/안전한 writer로만 `window.L1ViewerWriteHostAdapter`를 구현. 이 이름은 **frontend 합성 계약**이지 이미 존재하는 Linux API가 아님. 서버는 각 login/draft/preview/commit와 writer 호출 직전 session·CSRF·ACL·revision 재확인. 별도 계정 DB/새 문서 writer·그룹 지식 자동 게시 기본 개발 금지. 현장 owner가 인증/Writer 정책을 충족하지 못하면 서버 adapter **미등록** 상태로 읽기만 계속.
4. **MSC**: canonical message/participant anchor의 서버 읽기 계약이 실제 있을 때만 selector 연결. 없으면 문서 단위 수정 요청 초안까지만. 실제 구조 수정/커맨드·LLM 자동 분석은 승인된 후속과 분리.
5. **시험**: Read Only 무로그인/읽기용 동료·편집자 2역할, 잘못된 PW/타이밍/권한 회수/세션 만료/CSRF/rate-limit/세션 고정, 문서별 edit ACL, draft/Diff/COMMIT 세 시점, stale/conflict/UNCERTAIN/retry0, B1/B2/B3, E3/E4, 1440/720/390/320, MSC 6/12, 원본 SHA/readback, 백업·rollback. 미실행은 PASS로 승격하지 않음.
6. **운영 적용**: 실제 Linux 운영 변경 유효 승인·B1~B3·EAuth·E3/E4·writer 게이트가 PASS이고 롤백 준비가 확인됐을 때만 기존 Viewer에 배포·브라우저·동료 실측. 이 인계·ZIP 작성만으로 운영 배포/쓰기 활성화 완료가 아님. 비용 발생 Agent 호출·호스트 계정 발급·설정/서비스 재시작은 승인 범위 밖이면 BLOCKED.
7. 업무 Workspace의 같은 Work에 실제 code diff·증거·승인 범위·리스크/영수증을 보존하고 사용자에게 아래 숫자 결과만 전달. 회사 코드·상세 MSC·계정·키·로그를 CoWork/L1Work PUBLIC으로 옮기지 않음.

## 4. 결과 숫자(객관식)

**1 PASS / 2 FAIL / 3 NOT_RUN / 4 BLOCKED / 5 UNKNOWN**. 적어도 `G0 / source_package_received / auth_session_CSRF_ACL / UI / draft_diff_commit / MSC_anchor / B1_B2_B3 / E3_E4 / host_deploy` 각각 숫자 제시. 마지막 한 줄 `현재=... | 변경=... | 실제시험=... | 미검증/차단=... | 정확한 업무 Work 근거 위치=... | 다음 한 행동=...`.

## 5. 리뷰·배포 상태

이전 편집 **설계** 독립 R1은 완료(ACCEPT_WITH_CHANGE)이고 상세 설계 r0004는 사용자 피드백 보완본. **본 v0.2.0 코드 독립 리뷰는 NOT_RUN**. 앞서 사용자가 생략한 것은 `Viewer STYLE-DESIGN R1`이며, 새 v0.2.0 실제 서버 쓰기 활성화에 대한 권한/보안/코드 게이트 면제 근거가 아님. 정확한 승인 범위가 없으면 정상적인 차단 상태로 종료하고 가능한 격리 구현/시험만 계속.

관련 기존 1차 인계: [v0.1.2 G0·배포](L1_WORKSPACE_VIEWER_FIRST_PHASE_V012_G0_DEPLOY_HANDOFF_r0001_20261121_KST.md). 이전 v0.1.2 패키지는 덮어쓰지 않음.
