# 업무용 GPT 인계 문서

## L1 Workspace 모던 팀 위키 UI — 업무 GPT 검토·현장 연동 (2026-11-19 최신)

- **[화면 구성·가독성·스타일·시인성 검토 및 Linux Viewer 최소 연동 인계](L1_WORKSPACE_WIKI_UI_BUSINESS_GPT_REVIEW_AND_INTEGRATION_HANDOFF_r0001_20261119_KST.md)** — 사용자 요청에 따라 Claude 토큰 만료 보고 후 업무 GPT로 전달. 이번 구현물의 독립 시각·코드 리뷰는 NOT_RUN. 과거 리뷰 대기보다 이 최신 전달 지시 우선.
- **[UI 코드·설계·시험·캡처·INTEGRATION 전체 ZIP](../l1-workspace-wiki-ui_v0_1_0_1119.zip)** / [단일 HTML](L1_Workspace_Wiki_UI_v0_1_0_20261119_KST.html). 합성 UI v0.1.0, 브라우저 자체시험 56/56·정적 19/19·CRC/해시 PASS. **개발·검토용 전달물이며 정식 설치 배포 아님**, 실제 API·B1~B3·E3/E4 미검증.

## Recovery 포인트 분석 — 업무 GPT 상세 설계·구현 인계 (2026-11-19)

- **[필수 근거 9항목·단계별 입출력·후보 판정·최소 구현·검증을 포함한 상세 인계 r0001](L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0001_20261119_KST.md)** — CL→Jira/merged PR의 Problem/Cause/Solution과 실제 source revision을 대조하고, 정상/실패 시나리오·최초 불일치·검출부·런타임 자원 소유자의 복구 경계를 구분. 기존 스킬 재사용, G01~G10 기능 대조, S0~S6 분석 계약, E0~E5 적용·최소 구현·회수, T01~T20 연결 시험과 R01~R08 제품 효과 검증 계획 포함.
- **CNF 미수신 timeout·기존 recovery 커버 범위 제외**, 저사양 모델 순차 처리·기존 Work/Evidence 보존·미확인 API/스키마 가정 금지 유지. 분석 흐름 구현과 실제 제품 recovery 코드 변경을 구분. 업무 GPT의 현장 대조·구현에 사용할 설계 인계이며, 게시 자체는 호스트 실행·제품 코드 변경·설치·운영 전환 승인이 아님. 기존 [사례 분석 프롬프트](L1_CL_JIRA_RECOVERY_ANALYSIS_PROMPT_r0001_20261117_KST.md) 보존.

## ACE·PEC-HOP·ACON — Workflow v1.6.73 개발 ZIP CI 검증 결과 (2026-11-19)

- **[ACE·PEC-HOP·ACON Workflow 통합 개발 ZIP 실제 CI 20 PASS / 최종 ZIP은 릴리스 게이트 미충족 — 기존 인계서 최신 12절](L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md)** — PRIVATE Actions에서 기존 MSC 계보를 보존한 `l1-fix-workflow v1.6.73` 개발 ZIP 실제 빌드·전파일 해시/CRC·재현성 PASS. 미완료 코드 독립 리뷰/실호스트 G0·Writer 권한을 건너뛴 자동 배포 금지; 배포 승인된 최종 ZIP만 L1Work 루트에 게시 가능. 업무 전용 Updater 원본 반출 없이 업무 GPT의 비민감 기능 판정 회수.

## ACE·PEC-HOP·ACON 신규 코드 후보·최종 ZIP 배포 게이트 (2026-11-19)

- **[ACE·PEC-HOP·ACON 실제 적용 현황: 비민감 순수 후보 19건 PASS / 최종 스킬 ZIP 배포 차단 — 기존 인계서 최신 11절](L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md)** — PRIVATE 구현 후보·정적 근거는 원래 CoWork Work에 보존. `development_not_for_deployment`/실설치 소스 미확인·Writer 보호/전체 회귀·코드 독립 리뷰 미충족으로 `PUBLIC_SKILL_ZIP=BLOCKED_NOT_POSTED`. 업무 GPT가 필요한 설치 기능의 비민감 델타만 READ_ONLY 회신, Gate 완료 후 신규 ZIP만 L1Work/main 루트로 전달. 문서 게시 자체는 설치나 Job 실행이 아님.

## L1 Workspace 최신 책임 변경·가독성 개선 논의 (2026-11-18)

- **[개인 Knowledge 관리 및 그룹 Knowledge 연계: 업무 GPT 현장 설계 / Knowledge Updater 전담, 웹 뷰어 UX 문제 OPEN — 최신 15절](L1_WORKSPACE_LOCAL_VIEWER_R0002_BUSINESS_GPT_DETAILED_REVIEW_AND_G0_HANDOFF_r0001_20261118_KST.md#15-최신-사용자-결정--knowledge-updater-전담업무-gpt-현장-설계-및-viewer-ux-별도-논의-2026-11-18)**. 기존 13·14절 유지. 메타정보·실제 스킬/G0는 업무 GPT가 조사, UI 화면 변경은 사용자 논의 후. 인계 문서 게시만 수행; Linux 운영·Knowledge WRITE 미실행.

## L1 Workspace r0002 업무 GPT 직접 상세 검토 인계 (2026-11-18)

- **[전체 Workspace 트리·형식별 렌더링·보안/기존 스킬/G0 A~S/수락시험 T01~T34 상세 검토·작업 지시서](L1_WORKSPACE_LOCAL_VIEWER_R0002_BUSINESS_GPT_DETAILED_REVIEW_AND_G0_HANDOFF_r0001_20261118_KST.md)** — **최신 사용자 결정: Claude 독립 리뷰 생략, 업무 GPT 직접 검토.** 기존 r0002 설계의 요구·리스크·근거·19개 현장 질문과 단계별 Gate를 단독 검토 가능한 수준으로 수록. **13절 추가: 개인 Linux PC의 실제 웹 서비스 구축을 위한 업무 GPT→업무 LLM/Agent E0~E5 단계별 구현·시험·승인·롤백 지시문 포함.** **14절 추가: 사용자·업무 GPT의 개인 Knowledge 축적/탐색 TO-BE 합의(D-1~D-4, Module→Feature→Scenario, Work/Evidence/Revision/Coverage, 그룹 포맷 변환/승인 게시, Workflow knowledge/ WRITE 차단) 및 PK-G01~G08 인계.** `INDEPENDENT_REVIEW=NOT_RUN`, Linux G0·서비스/원본 전환·그룹 Knowledge 게시 `NOT_RUN`. 지금은 허용된 읽기 전용 G0·설계 검토에 한정; Linux 운영 변경은 별도 승인.

## L1 Workspace 웹 뷰어 안전 중지 인계 (2026-11-18)

- **[Linux Workspace 전체 URL 뷰어 — 중지 시점·재개 조건 인계](L1_WORKSPACE_LOCAL_VIEWER_SAFE_STOP_HANDOFF_r0001_20261118_KST.md)** — 전체 업무 폴더 열람 및 Markdown 즉시 렌더 설계 r0002, Claude 리뷰 입력·$1.50 단일 승인·미등록 REQUEST/READY, 운영 설정 미변경, 안전 중지 상태와 추후 재개 경계를 정리. **읽기 전용 상태 공유이며 실행 트리거가 아님.**

## L1 Workspace Linux 로컬 웹 뷰어 안전 전환 G0 (2026-11-18)

- **[로컬 Workspace·웹 열람 전환 G0 읽기 전용 16항목 인계](L1_WORKSPACE_LOCAL_WEB_VIEWER_LINUX_G0_READONLY_HANDOFF_r0001_20261118_KST.md)** — Kernel·Workflow 실제 원격 의존성, 로컬 백업·기존 웹/인증·공유 ACL·그룹 Knowledge writer 확인. A~P 숫자 회신. 신규 설치·Git 변경·웹 공유·Knowledge 쓰기·Job/모델 호출 없이 읽기 전용 상태 검토.

## MSC 두 진입 writer G0 읽기 전용 확인 (2026-11-18)

- **[MSC 두 진입 Updater·Kernel writer G0 숫자 확인 인계 r0001](L1_MSC_DUAL_ENTRY_WRITER_G0_READONLY_HANDOFF_r0001_20261118_KST.md)** — 업무 GPT/허용된 Linux Agent에서 기존 설치본·writer/HTML published_path·수동 편집 보호 계약을 **READ_ONLY**로 확인. 회신은 A~J 10개 숫자. 현재 개발 ZIP은 최종 PUBLIC 배포 게이트 미충족으로 게시하지 않음. 스킬 설치·Job 실행·지식 쓰기 승인 아님.

## ACE·PEC-HOP·ACON: 업무 스킬 실제 사용·모바일 수정 요청 협업 (2026-11-19)

- **[실사용 패키지·업무 전용 Updater 원본 비반출·모바일 오류 수정 요청의 책임/회신 경계 — 기존 인계서 최신 10절](L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md#10-2026-11-19-kst--실제-업무-사용업무-전용-updater모바일-수정-요청-협업-경계)** — 사용자 확인: 스킬 패키지는 업무 환경에 전달되어 실제 사용 중. Updater 원본 코드는 GitHub 제공 불필요, 업무 GPT의 비민감 기능/실행 판정만 회수. 문제가 생기면 모바일 Agent로 기존 Work에 수정 요청 → 소유 스킬별 개발·시험·유효 승인/배포 Gate → 실제 업무 적용 확인. 설치 활성 버전과 HOST E2E는 별도 증빙, 문서 게시 자체는 실행·설치 트리거 아님.

## ACE·PEC-HOP·ACON 지식 Updater 설계 적용 제안 (2026-11-18)

- **[업무 GPT 검토용 설계 적용 제안서 r0001 + 실제 Linux 설치본 READ_ONLY G0 원샷(9절)](L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md#9-2026-11-18-kst--acepec-hopsafe-실제-linux-설치본-g0-읽기-전용-원샷)** — ACE 최신 Work 결정·PEC-HOP Evidence 원문 바이트·SAFE 무변경을 **실제 설치본에서 읽기 전용**으로 확인하기 위한 AST/SHA-256 점검 스니펫·synthetic fixture 경계·단일 비민감 결과 양식 포함. 업무 GPT/허용된 Linux Agent가 실행하는 절차이며 현재 **호스트 미실행**. 스킬 수정·설치·Knowledge 게시·Job·유료 호출 승인 아님. 기존 11-17 Knowledge 동기화 R1 리뷰와 구분.

## CL·Jira 기반 이슈 시나리오·복구 지점 분석 (2026-11-17)

- **[CL·Jira 복구 지점 분석 프롬프트 r0001](L1_CL_JIRA_RECOVERY_ANALYSIS_PROMPT_r0001_20261117_KST.md)** — CL 번호 1개로 시작해 description의 Jira 연결, Problem/Cause/Solution·코멘트·diff/revision 대조, 정상/실패 시나리오와 검출 지점·소유자 복구 경로를 분석하는 업무 LLM 전달용 문서. p4-code-owner·l1-github·code-analyzer, 로그가 있을 때 issue-analyzer와 기존 Workflow/Kernel·doc-converter를 재사용.
- **REQ→CNF 미수신 timeout은 기존 recovery 구현 범위로 제외.** 저사양 모델은 이슈·실패 절차별 순차 처리. 업무 소스는 읽기 전용이며 코드 변경·설치·실제 HW/오류 주입 시험·Job·그룹 지식 게시는 포함하지 않음. 입력란을 채워 문서 전체를 업무 GPT 또는 허용된 실행 LLM·로컬 Agent에 전달.

## L1 Knowledge Updater — Claude R1 완료, 업무 GPT 상세 G0 인계 (2026-11-17)

- **[Knowledge Updater R1 판정 반영·개인/그룹 동기화 상세 인계 r0002](L1_KNOWLEDGE_UPDATER_R1_G0_DETAILED_HANDOFF_r0002_20261117_KST.md)** — 사용자 확정 ①~④, Claude R1 독립 설계 리뷰 `ACCEPT_WITH_CHANGE`(BLOCKING 1/MAJOR 4/MINOR 2)와 GPT 보완, G01~G16 실제 설치본 READ_ONLY 검증 질문, Base/Ours/Theirs·CAS·부분실패 복구, T01~T10 후속 수락 기준. 설계 정적 검토 완료, 코드/호스트/Knowledge 쓰기는 미실행. **기존 11-16 인계의 미수신 표기보다 최신**.


## 관리 스킬 기능 요약 (공개용 · 업무용 GPT 인계)

| 문서 | 용도 | 검증 범위 |
|---|---|---|
| [L1_SKILL_CAPABILITY_SUMMARY_INHOUSE_HANDOFF_r0001_20261113.md](L1_SKILL_CAPABILITY_SUMMARY_INHOUSE_HANDOFF_r0001_20261113.md) | 관리 스킬 **18개 + 별도 업무용 연동 1개**의 역할·재사용 판단·현재 코드 MSC 활용 요약 | 기존 정적 카탈로그를 비민감 범위에서 요약. 작업 PC 설치·실호출·독립 리뷰 미검증 |

상세 기능 카탈로그와 검증 결과의 정본은 접근 권한이 필요한 CoWork PRIVATE에 있으며, 이 공개 인계에는 회사 코드·운영자료·인증정보를 포함하지 않는다. 스킬 설치·Job 실행·공개 배포를 승인하는 문서가 아니다.

## MSC 링크 5종 스킬 G0 확인 (2026-11-16)

- **[L1 MSC 링크 5종 스킬 G0 읽기 전용 검토 인계 (2026-11-16)](L1_MSC_LINK_SKILL_G0_REVIEW_HANDOFF_r0001_20261116_KST.md)** — 공개 4종 재사용/수정 후보와 실제 설치된 Knowledge Updater·그룹 writer·호스팅의 I/O 차이 확인 Q1~Q8. 문서 게시가 업무 검토 실행이나 스킬 수정·배포 완료를 의미하지 않음.

## MSC B 뷰어 — 생성·축적·게시·열람 컨셉 리뷰

| 상태 | 문서 | 범위 |
|---|---|---|
| **설계 리뷰 인계 r0001** | [L1_KNOWLEDGE_MSC_B_VIEWER_GPT_REVIEW_HANDOFF_r0001_20261114_KST.md](L1_KNOWLEDGE_MSC_B_VIEWER_GPT_REVIEW_HANDOFF_r0001_20261114_KST.md) | doc-converter의 HTML+SVG 생성, Workflow/Kernel/Updater 연결, 사람의 보기 URL과 AI의 원문 재사용. 모듈·Feature 목록 검토는 1단계 유지 |

공개 가상 샘플을 참고한 컨셉 리뷰 입력. 실제 스킬 변경·코드 분석·Job 실행·지식 게시·호스팅 변경을 요청하지 않는다. B 자동 생성·연결과 첫 실제 분석 E2E는 아직 미검증이며 후속 확인으로 구분한다.

## CL/PR 이슈 분석 → Workspace 축적 — 구현·회귀시험

| 상태 | 문서 | 범위 |
|---|---|---|
| **기존 구현 원샷 지침 (보존)** | [L1_CLPR_ISSUE_ANALYSIS_IMPLEMENTATION_AND_REGRESSION_ONESHOT_r0001_20261114.md](L1_CLPR_ISSUE_ANALYSIS_IMPLEMENTATION_AND_REGRESSION_ONESHOT_r0001_20261114.md) | 기존 스킬 5종 최소 수정·회귀·ZIP 배포 게이트 요구사항 |
| **2026-11-14 실제 수정 후보 5종, 최종 배포 차단** | [L1_CLPR_IMPLEMENTATION_STATUS_r0001_20261114.md](L1_CLPR_IMPLEMENTATION_STATUS_r0001_20261114.md) | PRIVATE 후보 ZIP 5종 원격 SHA/CRC PASS. Python 회귀/E3 NOT_RUN, PUBLIC 루트 최종 ZIP 미게시 |

이 문서는 기존 스킬을 재사용해 분석·축적하는 **실행 인계**이며, 수정된 스킬 ZIP 또는 실제 회귀시험 완료 결과가 아니다. 추가 독립 리뷰 요청은 포함하지 않으며, 코드 변경·시험·PUBLIC 루트 스킬 ZIP 게시에는 각각 실증된 안전·호환·릴리스 게이트가 적용된다.

## L1 Knowledge Updater × Workflow

| 상태 | 문서 | 범위 |
|---|---|---|
| **업무 GPT G0 검토 요청 (2026-11-16)** | [L1_WORKSPACE_KNOWLEDGE_34_BUSINESS_GPT_REVIEW_REQUEST_r0001_20261116_KST.md](L1_WORKSPACE_KNOWLEDGE_34_BUSINESS_GPT_REVIEW_REQUEST_r0001_20261116_KST.md) | ③·④: Knowledge 폴더 Updater 단독 WRITE / Workflow READ_ONLY, Work 이력, 그룹 게시·readback·역링크. **2,702자, 읽기 전용 G0 확인·TO-BE 제안**, 구현/운영 쓰기 지시 아님 |
| **최신 ③·④ 설계 검토 인계 (2026-11-16)** | [L1_WORKSPACE_KNOWLEDGE_FOLDER_UPDATER_HANDOFF_r0001_20261116_KST.md](L1_WORKSPACE_KNOWLEDGE_FOLDER_UPDATER_HANDOFF_r0001_20261116_KST.md) | `works/` 원본 유지 · 물리적 `knowledge/` 탐색 제안 · Updater만 WRITE / Workflow READ_ONLY · 공통 Evidence 인계 · 승인된 그룹 게시·역링크. 독립 설계 리뷰 미수신, 실제 설치·E2E 미검증. **READ_ONLY G0 점검용** |
| **현재 인계 r0005** | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md) | G0 설치 사실 / G1 가정 분리, K5.8 설계표만, 기존 기능 우선 재사용 |
| 이전 r0004 | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0004_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0004_1111.md) | 이전 보완 계약, 과거 기록 보존 |
| 과거 r0002 | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0002_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0002_1111.md) | 이전 통합 인계, 과거 기록 보존 |

저장소 `wonhwipark/L1Work`, branch `main`. 현재 인계는 G0 READ_ONLY와 G1 설계표 작성이며 기존 knowledge/metadata·Work/Evidence·record/schema를 변경하지 않는다. SourceSnapshot·CAS·N:M·복구는 기존 Kernel/Updater/Git 제공자를 우선 재사용하고 미확인 API/record는 추가 확인 또는 BLOCKED로 남긴다.

r0005의 G0 전체 미수행 표기는 작성 당시 상태로 보존한다. 2026-11-14에는 일부 기존 기능의 호스트 확인 보고를 확보한 상태이며, 원본 설치/API·독립 리뷰·통합 전체 PASS를 뜻하지 않는다. 실제 저장·MSC/source/Evidence·게시/역링크·AI 본문 활용은 첫 승인된 분석 후속으로 확인한다. 신규 엔진·schema 확장은 확인된 gap의 최소 후보로만 검토하며, 이 목록은 구현·그룹 write·설치·모델 호출·외부 전송을 승인하지 않는다. 파일을 내려받아 업무용 GPT에 첨부해 해당 문서의 리뷰 요청을 사용한다.

## 용어·접근 지침

신규 안내에서는 저장소·작업 PC·실행 호스트·접근 권한으로 대상을 지칭한다. 기존 파일명(예: `_INHOUSE_` 포함)은 링크 호환성을 위해 유지한다. 이 인계 목록은 공개 허용 설명만 포함하며 PRIVATE 기록, 회사 코드, 제한 정보의 공개를 승인하지 않는다.
