# L1 Workspace — 2안 모던 팀 위키 UI 업무 GPT 전달·검토·현장 연동 r0001

> **2026-11-20 최신 보완:** [L1_WORKSPACE_VIEWER_UI_CHANGE_AND_MCP_VALIDATION_HANDOFF_r0002_20261120_KST.md](L1_WORKSPACE_VIEWER_UI_CHANGE_AND_MCP_VALIDATION_HANDOFF_r0002_20261120_KST.md)와 [MCP 진단 확장 요청서](L1_MCP_AGENT_READONLY_CAPABILITY_AND_VIEWER_PROBE_HANDOFF_r0001_20261120_KST.md)를 우선 읽어 주세요. 아래 Claude NOT_RUN은 11/19 전달 당시 이력이며, 이후 v0.1.0 독립 시각 UX R1은 ACCEPT_WITH_CHANGE로 완료됐어요. 새 개선 HTML의 독립 리뷰·실제 Linux 연동은 미실행이에요. 기존 원문·ZIP은 보존해요.

2026-11-19 KST · UI v0.1.0 · 개발·검토용 전달물 / development_not_for_deployment

## 1. 최신 사용자 지시와 현재 상태

사용자가 Claude 토큰 만료를 보고하고, Claude 사전 리뷰를 기다리지 않고 완성 UI 자료를 업무 GPT에 전달하도록 요청했어요. 이 인계는 그 최신 전달 지시에 따른 것으로, **이번 UI 구현물의 Claude 독립 시각·코드 리뷰는 NOT_RUN**이에요. 과거 설계 리뷰와 이번 구현물 검토를 구분해 주세요.

업무 GPT가 화면 구성·가독성·스타일·사용자 관점의 시인성을 먼저 검토하고, 실제 Linux의 **기존 별도 Viewer 서비스** 구조를 확인해 최소 연동을 진행해 주세요. 업무 LLM/Agent는 UI 재설계보다 좁은 adapter 연결·필요 보완·현장 시험에 집중해요.

이번 PUBLIC 전달은 사용자가 승인한 **개발·검토용 UI 자료 전달**이에요. 정식 스킬 릴리스, 호스트 설치·서비스 재시작·네트워크 공유·그룹 Knowledge 쓰기 완료나 승인을 의미하지 않아요.

## 2. 전달 자료와 실제 검증

저장소 **wonhwipark/L1Work**, branch **main**:

| 자료 | 정확한 상대 경로 |
|---|---|
| UI 코드·설계·시험·화면·연동 가이드 ZIP | `l1-workspace-wiki-ui_v0_1_0_1119.zip` |
| 이 인계서 | `handoffs/L1_WORKSPACE_WIKI_UI_BUSINESS_GPT_REVIEW_AND_INTEGRATION_HANDOFF_r0001_20261119_KST.md` |
| 바로 열어볼 단일 HTML | `handoffs/L1_Workspace_Wiki_UI_v0_1_0_20261119_KST.html` |

- [ZIP 다운로드](../l1-workspace-wiki-ui_v0_1_0_1119.zip)
- [단일 HTML](L1_Workspace_Wiki_UI_v0_1_0_20261119_KST.html)
- ZIP: **267140 bytes**, SHA-256 `411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9`.
- 단일 HTML: **65344 bytes**, SHA-256 `119be5e0104fbcc22d0daa89b42c418eefd8f00cdb94534a6f3518c79de4ed9d`.
- 합성 Chromium 자체시험 **56 PASS / 0 FAIL**, 정적 검사 **19 PASS / 0 FAIL**. ZIP CRC·경로·파일별 해시 및 공개 내용 검사 PASS.
- 1920/1440/1024/720/390/320 CSS px, 문서/원문·검색·TOC·deep link·뒤로가기·XSS·모바일 초점·합성 MSC 검증. 200%는 720 CSS px 상당 reflow 시험.
- 실제 Linux API·인증·권한·서비스 revision·동료 계정·실제 doc-converter MSC는 **NOT_VERIFIED / NOT_RUN**.

압축 해제 루트는 `viewer-wiki-ui/`예요. 23개 파일, `manifest.sha256`은 자기 자신을 제외한 22개 파일을 확인해요. **모든 문서·인물·Work/revision·MSC는 합성 예시**로 실제 L1 소스 사실이 아니에요.

## 3. 먼저 읽을 파일

1. `README.md`, `DESIGN.md`: 화면 구조·상태·책임·렌더 정책.
2. `screenshots/wiki-1440.jpg`, `wiki-390.jpg`, `wiki-320.jpg`, `msc-12.jpg`: 실제 합성 브라우저 화면.
3. `L1_Workspace_Wiki_UI_v0_1_0_20261119_KST.html`: 다운로드 후 브라우저로 열어 탐색. GitHub 파일 페이지는 HTML 앱을 직접 실행하지 않아요.
4. `TEST_REPORT.md`, `tests/results.json`, `tests/static-results.json`: 수행 범위와 한계.
5. **`INTEGRATION.md`**: 실제 서비스 G0·adapter 매핑·기존 renderer 재사용·현장 게이트·rollback.

업무 GPT가 직접 이미지·ZIP을 읽을 수 없다면, 허용된 업무 LLM·Linux Agent/MCP가 압축 해제·해시 확인·문서 추출·브라우저 관찰을 수행하고 업무 GPT에 근거를 반환해요. 이미지나 화면을 직접 확인하지 못했으면 시각 평가를 PASS로 표시하지 않아요.

## 4. 업무 GPT의 화면 검토 — 4축

| 축 | 검토 질문 | 필요한 결과 |
|---|---|---|
| 화면 구성 | 동료가 Work/Knowledge/전체 파일과 현재 위치·다음 탐색을 쉽게 찾는가? | 트리/M→F→S/Procedure·breadcrumb·본문/목차·모바일 배치의 문제와 최소 수정 |
| 가독성 | 긴 기술 문서·표·코드·경로·메타정보를 오래 읽기 편한가? | 글자/줄간격/본문 폭·위계·대비·정보 밀도·320px 가림 평가 |
| 화면 스타일 | 모던하고 일관적이며 공동 업무 위키에 적합한가? | 색·아이콘·버튼·배지·여백·선택/초점의 일관성·피로도 |
| 사용자 시인성·사용성 | 상태·핵심 내용·주요 행동이 바로 눈에 들어오는가? | 초안/게시 예시/미확인 구분, 검색·원문·MSC·복귀·닫기·읽기 전용 인지 |

검토 순서는 PC→390px→320px→MSC예요. 처음 보는 담당자가 이슈 개요에서 문제·원인·해결을 파악하고 MSC로 이동하는 흐름, Knowledge에서 Scenario와 Work/Evidence를 찾는 흐름을 확인해요.

결과는 **수용 / 최소 보완 후 수용 / 재검토 / 미확인**으로 판정하고, 확인된 문제마다 화면/viewport·사용자 영향·근거·우선순위·최소 수정안·확인 방법을 적어 주세요. 결함 개수를 강제하지 않고 취향과 재현 가능한 문제를 구분해요. 자체시험 56개 PASS를 사용자의 시인성 수락이나 독립 리뷰 완료로 바꾸지 않아요.

## 5. 실제 Linux Viewer 연결

**실제 소스 저장소·브랜치·revision·서비스·프레임워크·읽기 API·권한은 미확인**이에요. 기존 업무 Work와 허용된 호스트 접근에서 G0로 확정해 현장 실행 지시에 정확히 기재해 주세요. 미확인 경로·API를 추측하지 않아요.

1. 기존 Viewer 소스/현재 UI·시작/빌드 방법·인증·service identity·파일 root·renderer·검색·캐시·공유 범위를 읽기 전용으로 확인.
2. 기존 서비스가 정적 UI 교체를 지원하는지, template/component의 스타일·구조만 이식해야 하는지 판정. 새 서비스·새 프레임워크·DB 도입을 기본 요구하지 않아요.
3. `adapters/adapter.js`의 `listRoots/listChildren/getDocument/getDocumentMeta/getMscTarget/search/getSummary`는 **UI용 예시 계약**일 뿐 실제 API/영구 메타 스키마가 아니에요. 기존 읽기 계약에 매핑.
4. 기존 Markdown renderer·링크 mapper·파일 handler와 doc-converter B형 HTML+SVG를 우선 재사용. 합성 MSC SVG를 실제 converter로 배포하지 않아요.
5. 개인 Knowledge 메타·후보 저장·그룹 선별/승인 게시·readback/고정 revision 역링크는 기존 Knowledge Updater 책임. Viewer 적용을 이유로 Updater/Workflow/Kernel/doc-converter·Work/Evidence·그룹 정본을 함께 수정하지 않아요.
6. 실제 연동할 때만 합성 표기·검색 범위·fixture 상태를 검증된 원천값에 매핑. 모르는 값은 미확인. `fixtures/`, `tests/`와 합성 보안 입력을 실제 업무 서비스 제공 경로에 노출하지 않아요.
7. UI asset·adapter의 변경 전 버전과 rollback을 보존. 설치/재시작/공유가 필요하면 **해당 호스트의 기존 유효 승인 범위**를 확인하고 범위 밖 단계만 보류해요.

## 6. 보안·현장 시험 게이트

| 항목 | 현장 확인 | 현재 |
|---|---|---|
| B1 | canonical root·경로 이탈·encoded/absolute·symlink/hardlink·TOCTOU·보호 파일 차단 | 미검증 BLOCKING |
| B2 | 본문·검색·raw·download·캐시의 비밀/제한자료 fail-closed | 미검증 BLOCKING |
| B3 | 실제 MSC HTML 별도 origin·쿠키/토큰 격리·sandbox/CSP·asset 정책 | 미검증 BLOCKING |
| E3 | 기존 Linux localhost·인증·문서/원문/MSC·원본 SHA 불변·rollback | NOT_RUN |
| E4 | 유효 공유 승인·동료 2계정 읽기 권한·검색/deep link·동시 접근 | NOT_RUN |

데모 CSP는 네트워크/iframe을 차단해요. 실제 API 연결에 필요한 정책은 기존 서비스 보안 계약에 맞게 최소 조정·검증해야 해요. 임의 wildcard·같은 origin의 비신뢰 HTML 실행은 금지해요.

합성 UI 성공을 B1~B3 해결이나 동료 공유 가능으로 판정하지 않아요. 코드·기술 문서·상세 MSC/로그·호스트 절대 경로·인증정보는 업무 환경에 보존해요.

## 7. 업무 GPT에 바로 전달할 실행 요청

> `wonhwipark/L1Work`의 `main`에서 `handoffs/L1_WORKSPACE_WIKI_UI_BUSINESS_GPT_REVIEW_AND_INTEGRATION_HANDOFF_r0001_20261119_KST.md`와 루트 `l1-workspace-wiki-ui_v0_1_0_1119.zip`을 기준으로 이어가 주세요. Claude 토큰 만료로 이번 UI의 독립 리뷰는 미실행인 상태이며, 사용자 지시에 따라 업무 GPT 검토로 전달받았어요. 먼저 화면 구성·가독성·스타일·시인성 4축을 확인하고 필요한 최소 보완을 판정해 주세요. 이어서 허용된 업무 LLM/Agent로 기존 Linux 별도 Viewer의 실제 소스·브랜치·revision·읽기 API·권한·renderer를 G0 확인하고, ZIP의 INTEGRATION.md에 따라 adapter와 기존 UI의 최소 연결·현장 시험을 진행해 주세요. 기존 Work/Evidence·Knowledge writer·converter는 보존하고, 미확인 API를 새로 정의하지 말아 주세요. 실제 실행/미실행·보안 B1~B3·E3/E4·rollback·원본 SHA를 구분해 기록하고, 범위 밖 호스트 설치/재시작/공유는 기존 승인 확인 후 필요한 단계만 보류해 주세요.

업무 환경에 상세 근거를 남기고, 필요 회신은 `화면검토=수용/보완/미확인 | G0=PASS/NOT_RUN | API=REUSE/CONNECT/GAP/UNKNOWN | B1/B2/B3=PASS/FAIL/NOT_RUN | E3/E4=PASS/NOT_RUN | 원본변경=0/확인필요 | 다음=...`처럼 짧게 전달해요.
