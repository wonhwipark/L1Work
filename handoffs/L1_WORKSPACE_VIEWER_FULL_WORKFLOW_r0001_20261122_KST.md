# L1 Workspace Viewer v0.4.x — 결함 수정부터 운영 검증까지 전체 워크플로우

- 작성일: 2026-11-22 KST
- 기존 CoWork Work: `L1-WORKSPACE-RAG-20261111-001` (새 Work/DB/서비스 생성하지 않음)
- 협업 정본: `wonhwipark/CoWork-Skill-Collab`, branch `main`, `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md`
- 전달 저장소: `wonhwipark/L1Work`, branch `main` (실제 repo visibility 및 반출 허용 여부 매번 확인)
- 대상: Wiki 2안 UI + Write v0.2.0 + Preferences v0.3.0 통합 Viewer v0.4.0
- 현재 상태: PUBLIC 개발 ZIP 배송 PASS; 통합 E2E, 업무 Linux G0, 실제 Writer, 운영 적용 NOT_RUN. `development_not_for_deployment` 유지.

## 0. 변동 없는 기준 원본과 목적

| 입력 | L1Work/main 상대 경로 | SHA-256 |
|---|---|---|
| 단일 통합 Viewer v0.4.0 | `l1-workspace-viewer-wiki-integrated_v0_4_0_1121.zip` | `474db38255de06540b888241c0ee96f94feb09e48d9ee767768f50469d5ee7b3` |
| UI v0.1.2 | `l1-workspace-viewer-ui_v0_1_2_1121.zip` | `9be14c4c34c2a7d923d8b11c01fb0249d41e820861721f275001f0f7d499d9e3` |
| Write v0.2.0 | `l1-workspace-viewer-write-ui_v0_2_0_1121.zip` | `9f2df44348478eb44615bddef8f211645fa1c07ed71d43580b4fb324e376b6f9` |
| Preferences v0.3.0 | `l1-workspace-viewer-preferences_v0_3_0_1121.zip` | `228c60bada8a92591f7ae855dfabe206e018d9e59970cf2d1b773d4d00072812` |
| Workflow | `l1-fix-workflow_v1_6_75_1121.zip` | `fd337ee31e09c9f694146c9d159799ca7182af052c93121e73888a9ee367a0a1` |
| Kernel | `work-ledger-kernel_v0_7_43_1121.zip` | `9866ff7164884b0fb346bd31d37dbdf2013b5e5910e5857f8e35075624cf92f1` |

현재 미리보기: `handoffs/L1_Workspace_Viewer_Wiki_Integrated_Preview_v0_4_0_20261121.html`는 합성 데이터 기반 데모이며 운영 바이너리 아님. ChatGPT Space에만 있는 `l1-preview-responsive-visibility-fix` 추가 CSS는 GitHub 원본과 분리되어 있어 화면 차이가 생김.

## 1. 순서 / 담당 / 완료 게이트

| 순서 | 실행 | 담당 | 완료 조건 |
|---|---|---|---|
| G0 | CoWork CURRENT·이미 열린 메모·세 UI/Write/Preferences stream·기존 Linux 설치본·원본 revision·권한 확인 | GPT + 업무 GPT/Linux Agent | 원본 고정 SHA·현재 설치 버전·사용중인 서버/Writer 계약·승인 범위 기록 |
| G1 | UI·Write·Preferences 각 stream을 기존 Work `integration/streams/`에 등록. 요구사항/파일 소유권·동시 변경 충돌 해소 | GPT | 3 stream의 ZIP·SHA·필수 엔트리·변경 범위 모두 확인 |
| G2 | P1/P2 Viewer 수정 (아래 세부) | GPT 개발 | 코드 diff·단위시험·기존 동작 보존 |
| G3 | 세 stream 단일 ZIP 통합·검사 | GPT 개발 | 중복 엔트리 정합성·manifest·CRC·SHA·회귀/교차 시험 `INTEGRATION_PRECHECK_PASS` |
| G4 | 데스크톱/모바일/키보드 브라우저 E2E·기능별 회귀 | GPT 테스트 또는 허용된 테스트 호스트 | 1440/1040/760/390/320px·필터/설정/탐색/검색/MSC/Write disabled 테스트 PASS |
| G5 | 필요 독립 리뷰 1회, 결함 수용·재시험, 최종 개발 ZIP + HTML 미리보기 + HO 게시 | GPT + Windows Claude Code | 정식 요청/승인·READY·결과/영수증 확인 또는 `NOT_RUN`; 게시 commit 및 원격 byte readback PASS |
| G6 | 실제 Linux Viewer read adapter, CSP, 로그인/ACL, 기존 Workflow/Kernel/Writer G0 매핑 | 업무 GPT/Linux Agent | 설치본의 실제 API/버전/DOM·서버 소유자/신뢰 경계 확인; 모르면 Write disabled |
| G7 | Linux 격리 Read E2E·보안 B1~B3·기존 전체 Workflow/Kernel 회귀 | 업무 GPT/Linux Agent | 서버 검색/raw/다운로드 및 MSC sandbox 검증; 호스트 시험 결과·근거 기록 |
| G8 | 실제 Writer EAuth/E3/E4 + Work CAS/readback·실패 복구 E2E | 업무 GPT/Linux Agent | 원본 Work ID·SHA·revision 유지, 승인된 시험 데이터만 편집, 무단/중복 저장 차단, Evidence readback |
| G9 | 운영 설치/Write ON 여부 판정, 백업·롤백·원격 검증 | 운영 승인권자 + 업무 호스트 | 유효한 운영 승인, 관련 PASS, 단일 운영 버전·백업·되돌리기 실행 근거. 하나라도 미충족이면 HOLD |
| G10 | CURRENT·HO·공개 허용 비민감 결과·차단사유 갱신 | GPT + 업무 GPT | 사용자 관점 `현재 상태→변경→시험→차단/승인→산출물/SHA→다음 한 동작` 보고 |

## 2. 수정 요구사항 (새 기능 확장 금지)

**P1-A 문서 타입:** Viewer `doc.kind`의 한국어 표시값과 canonical 문서 분류값을 분리. 예: `이슈 분석→issue`, `상세 설계→design`, `MSC→msc`, `Evidence→other` 등 매핑 표를 명시하고 서버 canonical 종류와 실제 대응을 G0 확인. 모르는 종류는 `other`로 안전하게 표시하되 이때 필터의 동작을 명확히 안내. 제목 문자열만으로 권한/owner를 결정하지 않음.

**P1-B 필터의 의미:** `문서 유형 필터`는 목록/검색 결과의 **표시 필터**로 구현하고, 현재 보고 있는 문서의 본문 자체를 숨기는 부작용을 제거. 한편 섹션별 표시/숨기기는 `data-l1-section`의 실제 중앙 문서 블록에 적용하되 편집 버튼·인증·에러·원본 정보/필수 안전 경고를 숨기지 않음. 필터는 ACL이 아니므로 직접 링크/원문/API 서버 접근은 기존 ACL 별도 검증.

**P1-C 반응형 화면:** Space 미리보기의 탐색/목차 표시 CSS를 원본에 그대로 복사하지 말 것. Desktop 3영역 → Tablet 2영역/목차 버튼 → Mobile 본문 우선 + 열고 닫는 탐색/목차 드로어(접근성 aria-expanded/키보드/포커스 복원)로 정리. 320/390px에서 본문 첫 화면 확보. 우선순위는 사용자가 탐색·목차 존재를 발견하고 열 수 있는 것.

**P2-A 설정 UI:** theme/density/font가 중앙 본문·트리·메뉴·우측 패널·dialog에서 일관되게 변경되는지 computed style 검증. 강제색 대비/기본 글자 크기/Zoom 200%/접근성 준수. 설정은 저장/취소/초기화 및 새로고침 복구, 프로필 전환에만 영향. Write 데이터·권한 영향 금지.

**P2-B 프로필:** 서버가 제공하는 검증된 불투명 profile ID 연결 전에는 사용자별 분리 완료로 표기하지 말 것. 익명 모드는 현재 브라우저 저장으로만 표시. 프로필 변경/다른 탭 동시 변경/저장 실패/스토리지 불가를 각각 시험.

**P2-C MSC:** 기존 doc-converter의 실제 B형 HTML/SVG를 별도 origin·CSP/sandbox/권한 검증 후 읽기 전용으로 표시. 합성 6/12명 SVG Zoom PASS를 실제 MSC 검증 PASS로 취급하지 않음. canonical anchor 없는 구조 편집은 비활성.

## 3. 필수 시험표

| ID | 시험 조건 | 기대 결과 |
|---|---|---|
| T01 | 한국어 종류(`이슈 분석`,`상세 설계`,`MSC`,`Evidence`) 문서 이동 | 타입 매핑 정확, 전체 본문 사라지지 않음 |
| T02 | 문서 종류 필터 변경 후 검색·탐색·deep link | 필터는 UI 목록만 변경; 서버 ACL과 무관; 현재 문서의 본문 보존 |
| T03 | 섹션별 표시/숨김 | 해당 섹션만 변경; 편집/인증/핵심 안전 경고 불변 |
| T04 | 1440/1040/760/390/320px 해상도 | 탐색/목차 접근 가능, 본문 읽기 확보, 수평 overflow 통제 |
| T05 | 키보드 Tab/Shift+Tab/Escape, 패널 포커스/스크롤 | 포커스 트랩 및 복원, aria-expanded 동기화 |
| T06 | 설정 저장/취소/초기화/새로고침/타 탭/프로필 변경 | 명시된 상태 일치, 권한·원본문서 무변경 |
| T07 | 문서 3회 이상 이동 | 상단 환경설정 버튼과 Write 진입 가드 유지 |
| T08 | 검색 입력/링크 복사/뒤로가기/읽던 위치 | 정상 동작, Work/Knowledge 구분 유지 |
| T09 | 6명·12명 MSC Zoom/폭 맞춤, 실제 B형 MSC | 합성 UI와 실제 Converter 검증을 분리 표시 |
| T10 | 호스트 adapter 미설치·미로그인 | 무로그인 Read Only, Write disabled, 저장 0 |
| T11 | 기존 Writer 인증/CSRF/ACL·stale revision·중복 저장 | 서버에서 거부·멱등 처리; 불확실 상태 자동 재시도 금지 |
| T12 | Linux B1 경로/symlink, B2 검색/raw/cache/download, B3 iframe origin/CSP | 서버 보안 경계 우회 0 |
| T13 | 기존 Workflow+Kernel 전체 회귀·Work/Evidence readback | 유효한 source revision과 receipt 일치 |
| T14 | 백업/롤백 및 재시작 후 읽기 동작 | 승인된 배포만, 이전 상태로 복구 가능 |

시험은 각각 `PASS / FAIL / SKIP / NOT_RUN / BLOCKED`와 실행 주체·입력 버전·timestamp·Evidence 위치를 기록. 정적 코드검사 PASS를 Chromium 실동작 PASS로 대신하지 않음.

## 4. 표준 실행 제한·산출물

- 승인 전 수행 가능: 공개 가능한 UI 소스 개발/단위·브라우저 격리시험, ZIP 후보 패키징, 기존 Work 상태·비민감 근거 정리, 허용 범위 내 GitHub main 개발 후보 게시.
- 별도 유효 승인/접근 없이는 **하지 말 것**: 운영 Linux 설치/DB·키·CSP 설정 변경, 기존 LIVE watcher 변경, 실제 Write 활성화/원본 업무자료 수정, 신규 유료 리뷰/Job 자동 실행.
- 새 개발 ZIP: `l1-workspace-viewer-wiki-integrated_v<next_semver>_<MMDD>.zip`; 기존 v0.4.0 ZIP 보존. 버전은 최신 실제 main과 충돌 여부 확인 후 지정.
- L1Work 공개 전달: ZIP은 루트, 비민감 인계는 `handoffs/`, 단독 합성 미리보기는 **운영 불가** 표기. 모든 원격 파일은 commit/blob 및 size/SHA readback으로 확인.
- CoWork 동일 Work CURRENT에는 현재 상태/최신 근거/차단/다음 한 동작만. 상세 결과는 기존 근거/notes에 저장. 회사 제한 코드·실제 로그·상세 MSC·키·고객자료는 어떤 PUBLIC 저장소에도 반출 금지.
- 리뷰는 독립 리뷰 1회 필요 여부를 기존 유효 범위로 결정. REQUEST/PIN 게시·서명·READY·영수증/판정은 별개. 리뷰 창구를 새로 만들거나 임의 모델 비용을 발생시키지 않음.

## 5. 이 시점의 사실과 다음 실행

2026-11-22 현재 이 문서는 **검증·실행 설계**이며 신규 수정 ZIP이 이미 만들어지거나 Linux 호스트에 적용됐다는 뜻이 아님. 기존 v0.4.0는 PUBLIC 개발 후보, LIVE Read Only 및 Writer E2E 미검증 유지.

**NEXT_ONE_ACTION**: GitHub `L1Work/main` v0.4.0 단일 ZIP의 실제 바이트와 기존 `integration/streams` 등록 상태를 고정한 뒤 P1-A/B/C 변경을 최소 구현 → 테스트 → 신규 단일 개발 ZIP과 SHA/회귀 근거 작성. Linux 업무 GPT는 기존 G0/인증·Write 계약을 별도로 확인하며 호스트 반영은 보류.