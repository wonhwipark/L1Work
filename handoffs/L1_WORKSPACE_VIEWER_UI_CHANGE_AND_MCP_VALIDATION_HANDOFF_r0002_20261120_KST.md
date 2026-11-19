# 업무 GPT 요청 — 위키 Viewer UI 변경 및 MCP 확인 연계

r0002 / 2026-11-20 KST / 개발·현장 연동 변경서

## 1. 이번 변경과 입력

현재 업무 GPT에서 실동작을 직접 확인할 수 없어, 현장 확인 수단을 [Agent/MCP 읽기 진단 확장](L1_MCP_AGENT_READONLY_CAPABILITY_AND_VIEWER_PROBE_HANDOFF_r0001_20261120_KST.md)과 연결해요. 기존 Linux 별도 Viewer를 유지하고 아래 화면과 연결 변경을 좁게 적용할 수 있도록 검토·설계·개발해 주세요.

전달 저장소는 wonhwipark/L1Work, branch main이에요. 이 문서의 상대 경로는 handoffs/L1_WORKSPACE_VIEWER_UI_CHANGE_AND_MCP_VALIDATION_HANDOFF_r0002_20261120_KST.md예요. 실제 Viewer 구현 저장소·브랜치·설치 revision은 미확인이므로 현장 읽기 조사에서 확정한 뒤 실행 지시에 정확히 적어 주세요.

| 전달물 | 상대 경로·용도 |
|---|---|
| 기존 구현 ZIP | [l1-workspace-wiki-ui_v0_1_0_1119.zip](../l1-workspace-wiki-ui_v0_1_0_1119.zip): 코드·설계·자체시험·INTEGRATION 포함 |
| 이번 개선 HTML | [L1_Workspace_Wiki_Usability_Preview_20261120_KST.html](L1_Workspace_Wiki_Usability_Preview_20261120_KST.html): 사용성 확인용 별도 합성 시안 |
| 기존 상세 인계 | [2026-11-19 UI 인계](L1_WORKSPACE_WIKI_UI_BUSINESS_GPT_REVIEW_AND_INTEGRATION_HANDOFF_r0001_20261119_KST.md): 과거 상태는 이력, 이번 변경서 우선 |
| MCP 확장 요청 | [L1_MCP_AGENT_READONLY_CAPABILITY_AND_VIEWER_PROBE_HANDOFF_r0001_20261120_KST.md](L1_MCP_AGENT_READONLY_CAPABILITY_AND_VIEWER_PROBE_HANDOFF_r0001_20261120_KST.md) |

기존 ZIP은 267140 bytes, SHA-256 411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9예요. 이번 개선 HTML은 69919 bytes, SHA-256 7c9ab930bedf0f2cf59834c66d3598a920a95d9215993788b9ca80f125de237c예요. 개선 HTML은 v0.1.0 ZIP 안에 들어 있지 않으며 새 정식 버전 ZIP도 아니에요. 두 입력의 상태를 구분해 주세요.

## 2. 리뷰·시험 현재 상태

- 기존 v0.1.0 자체시험: 합성 Chromium 56 PASS, 정적 검사 19 PASS. 실제 Linux 연동·실기기·동료 계정 검증은 아님.
- 기존 v0.1.0 독립 시각 UX R1은 이후 완료되어 ACCEPT_WITH_CHANGE: P0 없음, P1 두 건(MSC 넘침 신호, CSS 중복), P2 두 건 보류. 과거 인계의 Claude NOT_RUN은 당시 기록이며 현행 리뷰 상태로 반복하지 않아요.
- 독립 리뷰는 이미지/소스 정적 검토이며 실제 Linux 런타임·독립 코드 실행 시험 PASS가 아니에요.
- 이번 개선 HTML은 GPT가 브라우저에서 문서 복귀·탭별 마지막 문서·검색어 유지·집중 보기·MSC 안내를 확인한 별도 합성 시안이에요. 추가 코드의 독립 리뷰·전체 56건 재회귀·실제 API 연동은 NOT_RUN.
- 실제 설치 소스·API·계정·revision은 NOT_VERIFIED. B1/B2/B3 BLOCKING, E3/E4 NOT_RUN 유지. 문서/시안 전달은 실사용 배포 완료가 아니에요.

## 3. 화면 변경 범위

| 순서 | 변경 | 완료 기준 |
|---|---|---|
| 필수 P1 | MSC 가로 넘침 안내 | 실제 넘침/이동 방향에 맞춰 표시·제거, 확대/폭 맞춤/화면 크기 변경 후 갱신. participant를 가리지 않음 |
| 필수 P1 | CSS 중복 정리 | 기본·Readability·화면 폭별 중복을 합치고 본문 16px/H2 22px/H3 17px·현행 여백 보존. 시안에는 이 정식 리팩터 미완료 |
| 우선 | 읽던 위치 복귀·탭별 문서 기억 | 문서→MSC→복귀 및 Work/Knowledge 전환에서 원래 문서·읽던 위치 유지. 명시적 section 주소는 해당 절 우선 |
| 후속 후보 | 현재 위치·검색 유지·집중 보기 | 선택 문서 경로 찾기, 같은 창 검색어 유지, 패널 접어 본문 공간 확보. 실제 권한/문서 revision 변경 시 재검증 |
| 보류 | 320px 메타정보·깊은 트리 | 실제 긴 제목·담당자 사용 근거로 필요한 부분만 보완 |

위키형 좌측 탐색·중앙 본문·우측 목차, 보라색 강조·16px 본문을 유지해요. 신규 검색엔진/DB·지식 writer·스키마 개편을 UI 도입의 선행 조건으로 만들지 않아요.

## 4. 실제 연결 전에 고쳐야 하는 지점

| ID | 현재 시안의 한계 | 필요한 연동 변경 |
|---|---|---|
| I-01 | documentView가 WikiFixtures.trees를 직접 참조, adapter도 합성 데이터 기반 | fixture 직접 참조 제거. 실제 분류/읽기 목록으로 문서 소속을 결정. 문서 ID의 msc- 접두사 대신 실제 종류/관계 사용 |
| I-02 | connect-src none, frame-src none인 데모 CSP | 승인된 실제 API·MSC origin에 맞춰 운영 asset의 meta와 서버 헤더 정책을 함께 구성. 제한 정책을 헤더 추가만으로 해제하려 하지 않음 |
| I-03 | renderMsc는 synthetic-placeholder만 표시 | 기존 doc-converter B형 HTML을 허용된 격리 handler로 연결. 텍스트 MSC_VIEW 응답을 HTML URL로 간주 금지 |
| I-04 | 제한된 Markdown/JSON/BINARY 및 doc: 링크 | 기존 safe renderer·상대 링크 resolver·SVG/PDF/이미지 handler 재사용, 원본 링크/문서 일괄 수정 금지 |
| I-05 | 합성 문구·fixture-r1·고정 상태 분기 | 실제 Updater/Kernel 원천을 매핑. 원인 확인/수정/시험/게시를 구분하고 미확인은 그대로 표시 |
| I-06 | 전체 하위 트리 재귀 조회와 pagination 없는 예시 | 실제 API pagination·권한·크기 제한 확인, 측정 후 필요한 lazy load만 보완 |
| I-07 | 부모 문서와 같은 창 메모리에만 위치·배율 보존 | 별도 origin MSC 내부 DOM 직접 접근 금지. 우선 부모 읽기 위치 복귀; child 상태 보존은 검증된 별도 계약 없으면 제외 |

운영 경로에서는 fixture/tests/합성 standalone HTML을 실제 업무 자료 제공 경로에서 제외해요. 브라우저에 token/cookie를 새로 저장하거나 임의 URL/srcdoc를 삽입하지 않아요.

## 5. 관련 스킬 책임과 재사용

- Viewer 서비스: UI asset·읽기 adapter·기존 인증/renderer/handler·검색·권한을 연결하는 직접 대상.
- l1-knowledge-updater: 개인 Knowledge 분류·관리·그룹 Preview/승인 게시·readback/역링크 관리. 현장 설치 원문 확인 후 기존 메타정보만 읽기 매핑.
- l1-fix-workflow: Work 조회/연속성. 기존 MSC_VIEW는 저장된 canonical 원본의 메시지 텍스트 조회이며 HTML 호스팅이 아니에요.
- work-ledger-kernel: Work/Evidence/export·published artifact mapping·SHA 보호 재사용.
- doc-converter: 기존 B형 HTML+내장 SVG 생성 재사용. 합성 그림을 실제 MSC로 바꾸거나 새로운 변환기를 만들지 않아요.

2026-11-20 정적 대조한 PUBLIC 입력은 Workflow 1.6.74, Kernel 0.7.42, doc-converter 0.2.26이에요. 공개본 존재와 실제 설치/로드 동일성을 구분해 MCP 진단으로 확인해요. UI 연결을 위해 스킬·Work/Evidence·그룹 Knowledge 구조를 일괄 변경하지 않아요.

## 6. 현장 진행·수락·복구

1. 기존 Work에서 실제 소스/브랜치/revision·권한·현재 UI/asset·원본 SHA를 보존하고 기존 API 매핑을 확정해요. 업무 GPT가 직접 접근할 수 없으면 허용된 로컬 Agent가 수행하고 MCP 조회로 근거를 회수해요.
2. 실제 읽기 API/handler에 연결할 adapter와 UI asset만 개발해요. 기존 프레임워크면 화면·동작만 이식하고 새 서비스로 교체하지 않아요.
3. B1 경로 containment/탈출·symlink·TOCTOU, B2 제한자료/비밀 차단의 raw·검색·캐시·download 일관성, B3 별도 origin/sandbox/CSP·인증정보 격리를 각각 확인해요. 정적 정책 검사와 실제 부정시험을 구분해요.
4. 허용된 개발/격리 환경에서 1440/720/390/320, 긴 표/코드/문서 링크·검색·키보드·복귀, 실제 B형 MSC 6/12명·긴 phase·확대/단계 이동 시험을 수행해요. 원본 SHA 불변과 UI/adapter rollback을 확인해요.
5. 유효 권한 내 E3 localhost 적용/브라우저 시험, 별도 공유 범위의 E4 동료 2계정 시험을 구분해요. 범위 밖 설치·재시작·공유 단계만 BLOCKED로 남기고 가능한 개발·시험·패키징은 완료해요.
6. 결과를 MCP 진단/기존 결과 조회에서 읽을 수 있게 기존 보고 경로에 연결해요. HTTP 200·파일 존재만으로 UI 렌더/보안/공유 PASS를 표시하지 않아요.

기존 승인·writer 경계와 원본 Work/Evidence/Knowledge는 유지해요. 중복 Job/분석·변환·유료 리뷰를 자동 실행하지 않아요. 현장 원문·절대 경로·상세 MSC·토큰·코드의 PUBLIC/PRIVATE 업로드는 요구하지 않아요.

## 7. 업무 GPT용 복사 지시문

> wonhwipark/L1Work main의 handoffs/L1_MCP_AGENT_READONLY_CAPABILITY_AND_VIEWER_PROBE_HANDOFF_r0001_20261120_KST.md와 handoffs/L1_WORKSPACE_VIEWER_UI_CHANGE_AND_MCP_VALIDATION_HANDOFF_r0002_20261120_KST.md를 함께 읽고 기존 현장 Work를 재개해 주세요. 직접 실동작 확인이 불가능하므로 허용된 Linux 로컬 Agent로 기존 whpark-mcp·Viewer·설치 스킬과 읽기 API를 대조하고, Agent에서 실제 상태를 답할 수 있는 최소 read-only 진단 확장을 설계·개발·시험해 주세요. 이어 Viewer는 기존 ZIP과 별도 개선 HTML을 구분해 필요한 asset/adapter/격리 handler만 보완해 주세요. 실제 대상 저장소·브랜치·revision은 현장에서 확정하고 기존 기능을 우선 재사용해 주세요. 개발/합성 시험·MCP 연결·Agent 응답·실제 문서/MSC·B1~B3/E3~E4의 결과를 각각 기록하고, 미실행/접근 불가는 정확한 상태와 다음 한 행동으로 반환해 주세요. 문서 작성만으로 완료하지 말고 허용 범위의 개발·시험·후보 패키징까지 진행해 주세요.
