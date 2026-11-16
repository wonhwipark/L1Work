# 업무 GPT 검토 요청 — L1 Knowledge ③·④ 통합 설계

- 작성: 2026-11-16 KST / 개정 r0001
- 목적: 두 업무 스킬의 기존 기능(G0)을 확인하고 TO-BE 최소 보완안을 회신
- 참고: [③·④ 상세 설계 인계](L1_WORKSPACE_KNOWLEDGE_FOLDER_UPDATER_HANDOFF_r0001_20261116_KST.md)
- 이번 요청: **READ_ONLY 설치본 대조 + 설계 제안만**. 코드 수정·설치·실제 게시·Job 실행 금지.

## 1. 확정된 설계 방향

개인 업무용 l1-workspace에서 **works/**는 기존 Kernel Work·Evidence 원본으로 유지하고, **knowledge/**는 GitHub에서 사람이 Module → Feature → Scenario로 찾는 물리적 탐색 폴더로 사용합니다. 두 폴더는 서로 다른 정본을 만들지 않고 Work ID·Source Revision·Evidence·MSC 원본 경로로 연결합니다.

- **l1-fix-workflow**: works/ 기존 계약에 따라 기록 가능, knowledge/는 **READ_ONLY**.
- **l1-knowledge-updater**: knowledge/ 후보·인덱스·상태 **단독 WRITE**. 기존 Work 기록은 Kernel의 허용된 writer를 통해 추가하며 전체 Workflow 실행을 강제하지 않음.
- **l1sw-dev-knowledge**: 승인된 그룹 지식의 게시·revision/readback 정본. 개인 후보와 그룹 게시를 구분.
- code-analyzer·doc-converter의 기존 분석·MSC 원본을 재사용. 동일 입력이면 재분석하지 않고 Evidence 유효성을 확인.

## 2. 두 업무 스킬에 요구하는 TO-BE

### A. l1-knowledge-updater

1. Updater 직접 분석과 기존 Workflow Work 지식화, **두 진입점** 모두 기존 Work 검색·재개를 우선.
2. Source Revision/분석 범위·Evidence 해시·MSC 원본(PUML/MD)과 표시본(HTML/SVG)을 구분해 참조. 유효성 확인 전 재사용 금지.
3. knowledge/에 Module별 탐색 인덱스·후보·Preview·게시 상태를 관리하되 Work 원본 복제·덮어쓰기 금지.
4. 동일 Work에 후보 검토/결정/게시 결과를 Kernel의 **실제로 허용된 기록 계약**으로 추가. 미지원 API·ref_type은 임의 가정하지 말 것.
5. 그룹 정본 중복/대상 revision 대조 → Preview → 유효 승인 → 기존 그룹 writer 호출 → 원격 게시 revision/readback 확인 → 개인 knowledge 상태 갱신 → 원 Work 역링크 순서 준수.
6. 게시 응답 유실 시 원격 이력 먼저 정산. 그룹 게시 성공·역링크 실패 시 **링크만 복구**하고 중복 게시 금지.

### B. l1sw-dev-knowledge

1. 기존 지식 탐색·동일/유사 Knowledge 매칭, Module/Feature/Scenario·Procedure 교차 조회 지원 여부 확인.
2. 승인·대상 revision·소스 근거·AS-IS/TO-BE·정보 접근 범위 확인 후 기존 게시 writer로 반영.
3. 성공 시 Knowledge 식별자, commit/revision, readback 근거를 Updater에 반환. 충돌·중복·응답 유실 시 안전하게 중단·정산.

## 3. 우리 측 사전 확인 사항과 업무 GPT 검증 요청

- Kernel 정적 확인: exporter가 works/, index/, 루트 README를 생성. knowledge/ 보존·탐색 연계는 격리시험 필요.
- Kernel work_reference_add 허용 유형은 jira, alias, github_pr, p4_cl, code_root이며 **knowledge 전용 유형은 없음**. 기존 기록 경로를 먼저 확인.
- Workflow docs_sync는 dirty/untracked checkout에서 차단. GitHub Push Guard의 저장소 식별 검증은 **폴더별 쓰기 차단과 다름**.

**다음 네 질문에 실제 설치본 근거로 답변해 주세요.**

1. Workspace exporter/indexer가 knowledge/를 보존하거나 충돌하는가? 관련 API/검증 근거는?
2. Workflow의 knowledge/ 쓰기를 기존 writer·권한 정책에서 실제 차단할 수 있는가? 단순 프롬프트 금지와 구분.
3. Updater가 기존 Work ID에 이력을 추가할 수 있는 허용 Kernel 명령·입출력·승인 조건은?
4. 그룹 게시 후 개인 knowledge 상태·원 Work 역링크를 중복 게시 없이 갱신할 수 있는 기존 계약은?

## 4. 회신 형식·경계

각 질문별 **기존 기능/근거 파일·API/판정(REUSE·CONNECT·최소 EXTEND·미확인)/위험·최소 변경점/시험 필요 여부**를 표로 회신해 주세요. **G0 설치 확인, G1 설계 가정, 실제 E2E 시험**을 구분하고 설치 스킬 버전·확인 시점도 기재해 주세요.

회사 제한 코드·상세 MSC·로그·토큰은 이 공개 경로에 게시하지 마세요. 결과는 비민감 요약으로 전달해 주세요. 이번 인계만으로 스킬 코드 수정, knowledge/ 생성, 그룹 게시, 승인·설치·모델 유료 호출을 시작하지 않습니다.
