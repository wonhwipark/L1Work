# 업무 GPT / Linux 로컬 Agent — L1 Workspace 로컬·웹 전환 G0 읽기 전용 확인

- 작성: 2026-11-18 KST / 공개용 비민감 인계 r0001
- 목적: **Linux 로컬 `l1-workspace`를 Work 원본으로 유지하고 웹에서 읽기 전용 열람**, 이후 승인된 그룹 Knowledge 게시를 계속할 수 있는지 실제 설치본 근거로 확인.
- 기존 CoWork Work: `L1-WORKSPACE-RAG-20261111-001`. 상세 설계는 CoWork PRIVATE `main`의 `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_LOCAL_FIRST_WEB_VIEWER_SAFE_TRANSITION_DESIGN_r0001_20261118_KST.md`.
- 이 문서는 실행·배포 승인서가 아님. 기존 MCP/Agent의 **허용된 읽기 전용 스킬·설치 상태 조회만** 수행. 새 Job/유료 LLM 호출, 외부 전송, Git commit/push/reset/stash/remote 변경, 폴더 이동/삭제, 웹 서버 실행·설치·포트 개방, ACL 변경, Knowledge 쓰기/승인/READY 요청 금지.

## 질문 / 답변 형식

각 항목은 실제 호스트 설치본 또는 설정/계약 원문을 확인해서 판정. `1=확인된 지원/조건 충족`, `2=확인된 미지원/조건 미충족`, `3=접근 불가·미확인`, `4=부분 지원·조건 있음`.

A. 설치된 Kernel에서 `.git`이 **없는 새 로컬 폴더**로 Work export 가능한가? (수행 말고 설치 코드·기존 시험 근거 조회)
B. Workflow의 `docs_sync`가 Git 등록 role/origin/clean tree 확인을 필수로 요구하는가?
C. Workflow의 `docs_push`가 원격 Git commit·push·readback을 필수로 수행하는가?
D. `l1-github repo-config`의 `work_docs` role과 **현재 로컬 root/remote/sync 정책**을 비민감 상태만으로 확인 가능한가?
E. 현장 Work 원장·Git 이력에 대해 오프호스트 백업 및 **복구 시험 근거**가 존재하는가?
F. 개인 `knowledge/`에 Updater 단독 WRITE/다른 스킬 READ_ONLY가 **실제 writer·권한 경계**에서 강제되는가?
G. Updater 직접 조사와 Workflow 분석 모두 같은 Work ID·Evidence/source revision을 보존·재사용 가능한가?
H. 기존 그룹 `l1sw-dev-knowledge` writer는 Preview/승인·CAS/readback·원래 Work 역링크를 지원하는가?
I. 설치본 Kernel의 Work-root `MSC_VIEW.md`에서 HTML로 연결되는 링크가 유효한가?
J. Converter의 **상세 원본** Markdown 안 상대 HTML 링크도 게시 후 유효한가? (I와 별개)
K. 현재 승인된 OpenCode Web/기존 내부 웹 서비스에서 정적 MD/HTML을 권한별 읽기 전용으로 제공할 수 있는가?
L. 새 서비스 설치 없이 본인 전용 localhost 뷰어를 기존 보안·인증 정책 아래에서 사용할 수 있는가?
M. 동료 2명 이상 웹 열람에 필요한 HTTPS/인증/ACL·감사 및 네트워크 승인이 이미 있는가?
N. Work 원본·Ledger 전체가 아니라 승인 파일만 **분리된 웹 문서 루트**에 발행하는 기능이 있는가?
O. 개인 임시 Work·제한 로그/코드/상세 MSC와 동료 공유 가능 Work를 **허용목록 기준**으로 구분할 수 있는가?
P. 기존 Skill·Writer·서비스 변경 없이 다음 단계의 비민감 합성 E3를 승인 조건 하에 시험 가능한가?

## 응답 (최소 타이핑)

**한 줄, A부터 P까지 순서대로 16개 숫자만:**

`A B C D E F G H I J K L M N O P`

예: `1 1 1 1 3 4 3 3 4 2 3 3 3 2 4 3` (샘플이며 실제 상태 추정 아님). `3` 또는 `4`가 있는 중요 항목의 이유는 선택적으로 **최대 두 항목, 각 12단어 이내**만 추가. 가능한 경우 스킬명·버전은 외부 회신이 허용되는 **비민감 식별자**로만 전달하고 회사 경로·repo·사람·문서/코드/토큰·IP·호스트 명칭·원본 텍스트는 회신하지 않음.

## Fail-closed

- 실제 설치본 미확인이면 **3**, 문서 설계/공개 ZIP을 읽었을 뿐이면 실제 지원 **1** 금지.
- 개인정보·민감 자료 판별이나 웹 권한 검증이 불가능하면 shared viewer 계획을 HOLD.
- 원격이 살아 있다는 이유만으로 로컬 단독 복구 가능하다고 보지 않음.
- 질문의 수락은 **조사 허용**만 의미, 실제 Linux 저장 정본 전환·웹 공개·그룹 지식 게시 명령으로 해석하지 않음.

## 회신 후 후속 결정

A~P 상태로 개인 SHADOW 웹 뷰어 가능성 / 원격 의존성 / 백업·보안 부족 / 그룹 writer API를 개별 판정. 현재 `docs_sync/docs_push`에 GitHub 전제 코드가 있어 GitHub를 즉시 끄지 않으며, 먼저 **기존 Git writer 유지 + 로컬 읽기 전용 뷰어**를 검증하고 저장 정본 이전은 독립 게이트로 진행.
