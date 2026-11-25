# Viewer v0.5.6 기술 Knowledge·Work 가독성 통합 인계 r0001

- 2026-11-26 KST / 기존 Work L1-WORKSPACE-RAG-20261111-001.
- 저장소 wonhwipark/L1Work, main. 신규 단일 입력: [l1-workspace-viewer-wiki-integrated_v0_5_6_1126.zip](../l1-workspace-viewer-wiki-integrated_v0_5_6_1126.zip), 446,659 bytes, 44 files, SHA-256 `147c414777e6fd368520e7a7e7b9c8298c9fa047f2411d8525191e7b91c77343`, commit `1064f12c9c387612f3dc603bdec939bbefc7c810`. v0.5.3 원본·v0.5.5 후보 보존, 미게시 v0.5.4 요구 포함.
- development_not_for_deployment. 실제 업무 호스트 설치·Write ON·Job·그룹 게시 승인 아님.

## 1. 업무 GPT 원샷 요청

본 인계와 위 ZIP 하나만 신규 Viewer 입력으로 사용. SHA/CRC/manifest, 실제 활성 Viewer revision·read adapter·ACL·기존 기능 G0 확인 후 표시 계층만 통합. 합성 adapter를 운영 서비스에 덮어쓰지 않음. 실제 Knowledge/Work 원본·파일명·ID·순서·schema·저장 엔진 및 기존 스킬 변경 금지. 실제 필드와 문서 섹션은 업무 GPT가 기존 읽기 계약에 매핑. 미확인 값·동작 추정 금지. 아래 수락 시험 이후 별도 승인 범위에서 운영 적용.

## 2. 변경 기능
| 영역 | 표시 기준 |
| --- | --- |
| Knowledge | 정확히 같은 첫 H1만 중복 제거, 문단·표·코드·목록 여백 축소, 기존 안전 Markdown 포맷터·원문·링크 보존, 상세 메타정보 기본 접힘. 실제 섹션 기반 유형별 빠른 이동 및 강조. |
| Work 목록 | 실제 업무명 우선, 검증된 SOC/ID 접두 중복 제거, SOC/ID 보조 표시 및 검색·route 보존. |
| Work 폴더 | READ/README→업무 개요, 확인된 확정 decision→확정된 결정(혼재/미확인은 결정 기록), state 기본 접힘·선택 접근 유지. |
| Work 본문 | 현재 상태·다음 행동·Blocker 상단 요약과 근거. 미확인≠차단 없음. 원문·기존 이슈 상세 요약 유지. 확인된 비핵심 중복/시스템정보만 접기. |
| MSC | 별도 MSC 탭 금지. 본문 시나리오 설명→기존 HTML/SVG 링크 및 권한 handler→그림 열람·확대/복귀. 임의 URL/HTML 금지. 합성 MSC는 실제 Converter 출력 아님. |
| 기존 기능 | READ/WRITE/MSC/Recovery/오늘의 업무/업무 도우미/환경설정/검색/필터/목차/원문/ACL·writer 유지. |

## 3. 기술 Knowledge 포맷
| 유형 | 권장 표시 역할 |
| --- | --- |
| Module | overview, architecture, components, interfaces, features, constraints, evidence |
| Feature | overview, design, conditions, states, scenarios, exceptions, constraints, evidence |
| Scenario | overview, conditions(Trigger/Precondition), architecture, flow, msc, exceptions, constraints, evidence |
| Procedure | overview, api, calls(Caller/Callee), parameters, conditions, returns, side-effects, exceptions, evidence |
| Issue Knowledge | symptoms, cause, fix, impact, validation, evidence |

Module→Feature→Scenario 및 Procedure 교차 탐색 분류 유지. srsRAN/TI BLE/Nordic SoftDevice/DPDK의 기술 레퍼런스 구성 원칙 참고. 실제 섹션 순서 유지, 없는 내용 생성 금지, legacy fallback은 원문. 기술 예외·제약·원인·API·MSC·코드 근거는 펼침.

## 4. 업무 GPT의 실제 매핑
ZIP의 INTEGRATION_READABILITY_V055.md, assets/readability-v055.js, 합성 adapter를 참고. 이름은 v055 계승 파일명이며 VERSION=0.5.6. getReadabilityPresentation(docId)는 선택 표시 DTO 예시이지 신규 저장 API/schema 아님.
- Work root의 workTitle/displayTitle, issueKey, workId, 검증한 presentationRole을 매핑. 확정 결정에만 decision 부여.
- documentRevision(문서 snapshot)과 sourceRevision(코드 revision) 분리. DTO의 docId/workId/documentRevision/sourceRevision 일치 시만 사용.
- knowledgeSections: headingId/headingText/role/verified:true. workSummary: currentStatus/nextAction/blocker 각각 state(KNOWN 또는 명시 근거 있는 NONE_CONFIRMED), text, sourceDocId. 출처 없으면 미확인. 기존 ACL/resolver 사용.
- foldSections: 동일 headingId/headingText, verified:true, nonEssential:true, SYSTEM/LONG_METADATA 또는 Work의 DUPLICATE. 기술 섹션·유일한 정보·하위 heading/링크/표/코드 있는 섹션은 자동 접지 않음. 원문/TOC/deep link 접근 유지.
- Knowledge Updater는 내용 생산·분류, Analyzer는 코드 근거, Converter는 MSC, Kernel/기존 writer는 저장, Viewer는 표현. 기존 Knowledge/Work 및 Kernel/Workflow/Updater/Analyzer/Converter/Recovery 변경 없음. 새 지식 문서 생성 시 검증된 내용을 유형별 구성으로 표현 가능하되, 기존 문서 재작성/재분석 금지. 실제 생산 계약 gap 입증 시만 소유자에게 별도 최소 보완 제안.

## 5. 수락 시험
V56-01 실제 제목·SOC/ID·검색/route·폴더 역할.
V56-02 요약 3필드 근거/revision, 미확인/없음 구분.
V56-03 Knowledge 5유형·H1·섹션/표/코드·기술정보·원문/목차 보존.
V56-04 별도 MSC 탭 없음, 실제 본문 링크→HTML/SVG 그림·확대·복귀·ACL/CSP/artifact SHA.
V56-05 revision 불일치·legacy·비정상 유형·경로 이탈·위험 링크·기술정보 숨김 방지.
V56-06 Chromium/Firefox 1440/760/390/320px 및 키보드·deep link·원문 복원.
V56-07 tests에서 node regression.cjs, readability.cjs, assistant-client.cjs, recovery.cjs, readability-v055.cjs 실제 실행; 기존 A01~A10/H01~H05/T1~T8와 Write/Recovery/도우미/설정 회귀. 승인 격리 Work/모의 writer만 사용.
V56-08 실제 Work/Knowledge 각 1건·Recovery 사례 readback, 원본·기존 스킬 불변 확인.

개발 검증: v0.5.3/v0.5.5 SHA pin, 최종 44 CRC/43 manifest/경로/roundtrip/원격 SHA 및 Write 3파일·기존 렌더러/Recovery/도우미/설정 바이트 보존 PASS. V8 구문 19개, 실제 파일 기반 시험 프로그램 5개(V8 표준 라이브러리 대역, Node 아님), fixture 매핑 6건·제한 DOM 단언 7개·standalone CSP PASS. v0.5.3/0.5.5의 readability.cjs 빈 text node 단언 실패 재현 후 실제 링크 요소 검사로 수정(허용/차단 단언 유지); 비정상 kind/role fallback·합성 업무명 일치 보완. 실제 Node/브라우저/업무 호스트 G0/E2E/독립 리뷰/설치 NOT_RUN.

## 6. 기존 계약과 회신
[기존 v0.5.3 통합 인계](./L1_CHANNEL_RECOVERY_VIEWER_KERNEL_CONVERTER_COMPLETE_HANDOFF_r0001_20261124_KST.md)의 A/H/T·Recovery/Kernel/Converter, [Write 계약](./L1_WORKSPACE_VIEWER_WRITE_WORKFLOW_KERNEL_FULL_SKILLS_HANDOFF_r0003_20261121_KST.md), [Updater 품질 인계](./L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0002_20261125_KST.md) 유지. 활성 스킬 재사용, 동일 Workflow v1.6.75 후보 충돌 확인 전 덮어쓰기 금지. 구버전 ZIP 재설치 금지. 표시 실패만으로 분석/변환/Job 재실행 금지.
회신: INPUT_SHA, ACTIVE_G0, 매핑 근거, V56-01~08별 PASS/FAIL/SKIP/NOT_RUN/BLOCKED, 실제 MSC 링크, 변경 경로·revision, 원본/기능 보존, 다음 한 행동. 업무 원문·상세 MSC·로그는 업무 Work에 보존.
