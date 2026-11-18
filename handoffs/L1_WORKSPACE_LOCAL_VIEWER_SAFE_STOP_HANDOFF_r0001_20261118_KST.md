# L1 Workspace 전체 URL 웹 뷰어 — 안전 중지·재개 인계 r0001

- 작성: 2026-11-18 KST
- Work ID: `L1-WORKSPACE-RAG-20261111-001`
- 현재 판정: **PAUSED_SAFE / REVIEW_NOT_RUN / HOST_NOT_CHANGED**
- 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`, `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md`
- 이 문서는 **상태 인계 전용**. 게시·열람만으로 REQUEST/READY·유료 리뷰·Linux 설치·Job·지식 업로드를 시작하지 않는다.

## 1. 최종 목표와 확정 요구

Linux 업무 PC의 `l1-workspace` 전체 **업무 문서 트리**를 업무 네트워크의 단일 URL에서 폴더별·Work ID별로 찾아보고, 사용자와 동료가 읽기 전용으로 열람하도록 설계한다. 특정 Work마다 별도 공개 승인·allowlist를 필수로 두지 않는 **전체 업무 트리 탐색**을 기본 UX로 한다.

**모든 원본을 별도 HTML 파일로 변환할 필요는 없다.** 원본 파일을 유지하면서 웹에서 열 때 형식별 화면 뷰어를 적용한다.

| 원본 | 웹 열람 방식 | 전량 HTML 사전 변환 |
|---|---|---|
| Markdown(`.md`) | HTML 실시간 렌더 또는 캐시 | 불필요 |
| 기존 MSC(`.html`) | 기존 HTML·SVG 인터랙션 재사용 | 불필요 |
| `.svg` / 이미지 / PDF | 형식별 브라우저·검증된 뷰어 | 불필요 |
| JSON / TXT / CSV / YAML | 구조화된 텍스트·테이블 표시 | 불필요 |
| 기타 바이너리 | 허용된 다운로드/미리보기 불가 처리 | 불필요 |

호스트 OS 전체 공개나 인터넷 익명 공개가 아니라 **업무 네트워크의 Workspace 업무 콘텐츠 공유**이다. `.git`, 자격정보, 토큰·개인키, Workspace root 탈출, HTML/JS 취약점은 차단한다. 조직 보안 정책·실제 접근 권한은 Linux G0에서 확인한다.

Work 원본·Evidence·Kernel 이력과 그룹 `l1sw-dev-knowledge`의 승인된 게시 정본을 구분한다. 웹 뷰어는 **읽기 전용 표현 계층**이고, 웹 화면 도입만으로 기존 Git writer를 폐지하거나 로컬로 완전 이행하지 않는다.

## 2. 실제 완료/미실행

| 항목 | 최신 확인 상태 |
|---|---|
| 안전 전환 설계 r0001, 전체 트리·on-demand 렌더 변경 r0002 | **설계 문서 게시 완료** |
| 기존 Kernel non-Git synthetic export 시험 | **PASS** — 합성 Work 문서 12개, 재출력 SHA 일치 |
| 기존 Kernel 관련 pytest | **PASS** — 5건 |
| Claude 리뷰용 고정 입력 ZIP r0002 | **PRIVATE 게시·CRC/원격 readback PASS** — 9개 파일, 91,324 B |
| 이번 Claude 리뷰 1회 비용 | 사용자가 **최대 USD 1.50 승인**, 실제 호출 0 (해당 세션 근거) |
| 정식 REQUEST.md / SOURCE_PIN.json / 승인 서명 / READY | **NOT_POSTED** (검증 초안·Windows 인계서만 게시) |
| Windows 실호스트 $1.50 select/check·수동 서명 검증 | **NOT_RUN** |
| Claude 독립 리뷰·결과·영수증 | **NOT_RUN / NOT_RECEIVED** |
| Linux 설치본 G0·웹서버·실제 URL·동료 접속 | **NOT_VERIFIED / NOT_RUN** |
| 업무 Workspace 원본 전환·그룹 Knowledge 쓰기 | **NOT_RUN** |
| 운영 승인/비용 한도 설정 변경·삭제 | **NOT_RUN** |
| 업무 GPT 최종 구현 작업 지시서 / 정식 스킬 배포 | **리뷰 후 단계, NOT_POSTED** |

운영 Windows의 과거 비용 검증은 `POLICY_COST_MISMATCH`로 차단되었다. 정책상 최소 리뷰 등급 USD 1.50과 보호 자동 위임 한도 USD 1.00이 달랐다. 이후 사용자는 **이번 리뷰 1회 $1.50**을 승인했지만, 승인만으로 유효 서명·READY 또는 리뷰 실행이 성립하지 않는다.

## 3. 중지 지시와 보존 사항

사용자 최신 지시: **“추가확장하지말고 안전하게 중지해줘.”** 이에 따라 이 Work의 추가 구현·GitHub 정본 변경·정식 리뷰 등록·모델 호출·운영 설치 및 설정 변경을 **중지**한다. 사용자가 이번에 명시적으로 요청한 이 **PUBLIC 핸드오프 문서 작성·게시만 예외 범위**이며, 기존 중지 상태를 해제하지 않는다.

- 설계·r0001/r0002 ZIP·리뷰 인계·기존 영수증·CURRENT 이력은 손대지 않고 보존.
- 요청당 비용 보호·서명·READY·중복·만료 검증을 임의 삭제하지 않음.
- “요청 후 한도 관련 설정 삭제”는 **아직 실행되지 않음**. 이번 요청 전용 임시 override가 실제 생성되었는지 확인되지 않았으며, 생성되지 않았다면 삭제 대상 없음. 전역 자동 위임 최대 금액 삭제는 이번 1회 승인으로 추정하지 않음.
- PRIVATE 설계 문서의 링크를 제공하는 것이 업무 Linux 설치·지식 게시·Windows 원샷 실행 승인은 아님.

## 4. 재개 시 참고할 정본 (접근 권한 필요)

모두 GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab/main`:

1. [Work CURRENT — 최신 상태](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md)
2. [전체 업무 트리/형식별 웹 뷰어 설계 r0002](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_FULL_TREE_WEB_RENDER_VIEWER_DESIGN_DELTA_r0002_20261118_KST.md)
3. [고정 Claude 리뷰 입력 ZIP r0002](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/packages/l1-workspace-local-viewer-design_r0002_1118_REVIEW_INPUT.zip)
4. [USD 1.50 정식 요청 사전검증 **초안**](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/L1-WORKSPACE-RAG-20261111-001/REQUEST_PREFLIGHT_DRAFT_LOCAL_VIEWER_R0002_150USD_20261118.md)
5. [Windows 원샷 **실행 인계서** — 아직 실행하지 않음](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/requests/REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118/HOST_SUBMIT_ONESHOT_150USD_AND_LIMIT_CLEANUP_20261118.md)
6. [업무 GPT Linux 제안·작업지시 **초안**](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_LOCAL_VIEWER_LINUX_PROPOSAL_AND_WORK_ORDER_DRAFT_r0001_20261118_KST.md)

리뷰 입력 ZIP 무결성 식별자: SHA-256 `6a013a104ebfefeae6dc452965ce99ce5a3f9637ed538c778d8cb5189d5a7e5f`, 크기 91,324 bytes. 이는 **리뷰용 고정 입력**이지 설치 패키지가 아니다.

## 5. 다음 한 행동 (사용자가 명시적으로 재개 요청한 경우에만)

그 시점의 PRIVATE `CURRENT.md`와 Windows 실제 호스트 상태를 다시 읽고 동일 요청의 중복·UNCERTAIN·정책·서명/금액 검증부터 확인한다. 유효한 승인과 사전검증 PASS일 때만 **리뷰 1회 → GPT 판정 → 업무 GPT 최종 구현 MD → 별도 승인된 Linux G0·구현·시험** 순서로 재개한다.

현재는 **안전 중지 유지**. 기존 Windows 원샷 지시서를 자동으로 수행하거나 새 READY를 발행하지 않는다.

---

비민감 상태 공유용 PUBLIC 문서. 회사 코드·상세 MSC·실제 로그·키·토큰·원본 업무 자료를 포함하지 않는다.
