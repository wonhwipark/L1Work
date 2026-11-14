# L1 CL/PR 이슈 분석 → l1-workspace 축적: 구현·회귀시험·최종 ZIP 전달 원샷

- Date: 2026-11-14 KST
- PUBLIC source: `wonhwipark/L1Work` / `main` / `handoffs/L1_CLPR_ISSUE_ANALYSIS_IMPLEMENTATION_AND_REGRESSION_ONESHOT_r0001_20261114.md`
- Scope: 사용자가 P4 submitted CL 목록·GitHub merged PR 목록만 제공해도 기존 Work 검색/재개 → 안전한 이슈별 수집·그룹핑 → 문제/원인/수정 분석 → `l1-workspace` 저장·재조회가 가능한 최소 기능.
- Authority: 기존 `l1-fix-workflow`, `p4-code-owner`, `l1-github`, `code-analyzer`, `work-ledger-kernel` 재사용. `issue-analyzer`는 로그·증상 입력 있을 때만 선택.
- Public documents contain no corporate code, path, token, internal MCP identity, customer data, logs or detailed MSC.
- This handoff is implementation guidance, **not** skill ZIP or completed host result. It does not authorize a new paid review, automatic Job, Knowledge publishing, or installed-skill replacement.

## 원샷 사용자 지시

현재 승인된 실행 환경에서 정확히 **PUBLIC `wonhwipark/L1Work` `main` `handoffs/L1_CLPR_ISSUE_ANALYSIS_IMPLEMENTATION_AND_REGRESSION_ONESHOT_r0001_20261114.md`**를 읽고, 기존 배포 ZIP과 현재 설치본·최신 설치 계약을 구분하여 아래 A~G를 중간 핑퐁 없이 가능한 범위에서 끝까지 수행한다.

**추가 Claude 독립 설계/코드 리뷰는 요청하지 않는다.** 개발·자체시험·회귀시험은 자기 시험 `SELF_TEST`로 기록한다. 이미 완료된 설계 리뷰는 보존하지만 수정된 코드의 독립 리뷰 PASS로 소급하지 않는다. 특정 코드·호스트·권한에 접근할 수 없는 경우 해당 부분만 `BLOCKED/NOT_RUN` 처리하고 다른 부분을 이어서 수행한다.

## A. 입력 및 소스 확인

1. PUBLIC 루트의 기존 패키지 실제 바이트·SHA-256·ZIP CRC·내부 버전·license/manifest/skillsilent 정책·기능을 확인. 작업 대상 초기 기준:
   - `p4-code-owner_v0_6_7_1012.zip`
   - `l1-github_v0_3_56_1110.zip`
   - `l1-fix-workflow_v1_6_67_1110.zip`
   - `code-analyzer_v0_15_2_1107.zip`
   - `work-ledger-kernel_v0_7_37_1103.zip`
   현재 공개 최신본·실제 설치본/원본이 다르면 최신 CURRENT/변경 diff 기준으로 충돌을 기록하고 무단 덮어쓰지 않는다.
2. 승인된 비운영 작업복사본에서만 개발. 현재 운영 설치본, L1 코드 repo, 운영 DB/WAL, 사용자 Work 원본, Job-list/Skill-Updater/워처/예약작업은 불변.
3. 실제 Python 최소 지원 버전(3.10/3.11/3.12) 및 P4 접근 허용 방식(Mango MCP 제공 여부, CLI 금지 정책), GitHub PR 조회 action과 결과 계약을 확인. API/권한이 미확인이면 구현 가정으로 메우지 않음.

## B. 우선 수정 — 기존 스킬 최소 확장

| ID | 대상 | 필수 구현·차단 조건 |
|---|---|---|
| B1 | `p4-code-owner` | Jira 키 없이 CL 목록만으로 시작하는 **CL Evidence 소비 경로** 추가. Agent가 인가된 Mango MCP를 통해 취득한 submitted CL/describe/files/integration 근거를 입력받아 기존 validation/L1-scope allowlist 재사용. 미제공/불완전/원본 추적 불가 → PENDING, Jira 가상 생성 금지. |
| B2 | `l1-github` | `pr-code-analysis`에서 merged 여부, merged_at, merge_commit_sha, target/base, head를 구분. PR diff head vs 실제 target 적용 commit의 일치/불일치. Closed-unmerged는 merged가 아님. |
| B3 | `l1-fix-workflow` 연결 | CL reference는 `p4:<server_alias>:<cl>`로, PR은 정규 절대 URL로. 기존 Work reference find/resume 재사용, 중복 Work 금지. 그룹핑은 Jira·공식 integration·명시적 상호 링크의 근거가 있는 **후보**만 제시; 근거 없으면 UNLINKED 단독, CL/PR N:M 허용, 자동 병합 금지. |
| B4 | `code-analyzer` 연계 | Git SHA, P4 file#rev/from_rev, source scope와 before/after를 분리. P4 과거 snapshot 없을 때는 diff-based INFERENCE. 불일치→CODE_CONFIRMED 금지. 사내 정책이 Mango MCP 전용이면 local `p4` subprocess 호출 금지, 인가된 Evidence file 경로 우선. |
| B5 | `work-ledger-kernel` / 연결 | 기존 허용 Evidence slots만 사용. 과거 PR/P4 근거를 `delivery`·`change_provenance` 또는 다른 provider 명의로 위장 금지. 이슈 서술과 source refs는 허용된 Work doc/artifact 경로 확인 후 저장. record.json·README/index/문서안내 파생 파일 직접 수정 금지. |
| B6 | Python 호환 | `work_ux.py` 및 `share_export.py`의 Python 3.12 의존 f-string 문법을 선언한 최소 지원 버전에서 구동 가능한 표현으로 변경, 최소 버전 구문 검사와 작동 시험. |
| B7 | 실행 안전 | 동일 저장소 PR 분석은 직렬화: head 기준 준비 상태 확인 → Analyzer Run/근거 정착 → 다음 PR. Runtime branch drift·dirty/untracked/missing commit은 거짓 PASS 금지. |
| B8 | claim state | `Problem`, `RootCause`, `FixMechanism`, `Impact`, `Verification`, `CurrentApplicability`를 독립 표시. CODE_CONFIRMED/INFERENCE/UNKNOWN을 본문·Evidence anchor와 묶고 분석/merged를 실제 test PASS로 자동 전환 금지. |

## C. 회귀시험 필수 (PASS/FAIL/SKIP/NOT_RUN 실측)

- C01: Jira 없이 합성 P4 CL 리스트 3개 → 요청 생성·증거 소비; 가짜 Jira 키 0, 미인가 L1 scope 실패 차단.
- C02: merged/closed-unmerged/squash/rebase/target drift PR 메타데이터 → 각각 올바른 landing 및 applicability.
- C03: 합성 CL 2개+PR 1개 공식 공통 근거 → 후보 이슈, 링크/원본 손실 0; 같은 모듈의 다른 이슈는 병합 0.
- C04: CL 원본 미확인, P4 혼합 revision, 누락된 PR object, dirty workspace, 미확정 merge → CODE_CONFIRMED=0.
- C05: 동일 CL/PR 목록 순서/표기 달라도 같은 Work, 참조 중복 0; 다른 Work에 걸쳐 참조가 충돌하면 임의 merge 0.
- C06: 미등록 Kernel evidence provider/kind·`delivery` 우회 시도 → 거부, 운영 registry 수정 0.
- C07: Python 3.10/3.11 `py_compile` + Work create/find/resume/Export·Code Analyzer module import. 지원하지 않는 Python 버전은 명시하고 가짜 PASS 금지.
- C08: 동일 repo PR 2개 순차 분석에서 먼저 분석한 source snapshot·Run/Evidence 보존.
- C09: 원인 확인·수정 미반영·시험 NOT_RUN → 상태 분리, VERIFIED_CLOSED 거짓값 0.
- C10: 기존 Work exporter, source retention, 기존 Repo Role/Push Guard, 임시 worktree 원본 불변, 스킬 기존 공개 단위시험. 변경 관련 회귀 전체 재실행.
- C11: ZIP 경로 이탈/중복 이름/심링크/민감정보·구 버전 파일 덮어쓰기 0. 패키지 안의 실제 VERSION/manifest/skillsilent 계약 일치.
- C12: 외부 게시 예제/결과에 회사 코드·개인정보·로그·상세 MSC 0. 실 사내 호스트 접근 불가면 E3=NOT_RUN.

테스트는 실제 사용된 Python interpreter, 명령, 커밋, PASS/FAIL/SKIP/NOT_RUN, 아티팩트/해시를 기록. 기존 PASS 주장만 복사하지 않는다.

## D. 배포와 결과 분리

1. 수정 파일·diff·회귀시험 뒤 스킬별 신규 ZIP 파일명 규칙 `<skill>_v<major>_<minor>_<patch>_<MMDD>.zip`(예: 1114)를 적용. 이미 존재하는 원본/최종본을 덮어쓰지 않는다.
2. ZIP 실제 SHA-256/size/CRC, 스킬별 필수파일·민감정보 검사, Python 버전·기존 호환/롤백 지침을 기록.
3. **독립 리뷰 추가 요청 0**. 사용자 승인된 PUBLIC 대상은 `wonhwipark/L1Work/main` **루트 최종 ZIP**. 단 현재 `PUBLIC_RELEASE_GATE.md`/최신 계약상 호스트 호환·배포 필수 확인 미충족이면 `development_not_for_deployment`·`PUBLIC_RELEASE=BLOCKED/NOT_POSTED`를 유지하고 PUBLIC 배송본으로 오보고하지 않는다. PRIVATE ZIP으로 배송을 대체하지 않는다.
4. 실제 배포 게이트 충족한 최종 ZIP만 PUBLIC root에 신규 별도 파일로 업로드, 원격 다시 내려받아 **바이트 SHA-256/크기/ZIP CRC 일치** 확인. 실패 시 PUBLIC 완료 표기 금지.
5. `skill-updater` 설치, `job-list` 활성화·실행, `l1-workspace` 업무 원장 write, `l1sw-dev-knowledge` 게시 및 Provider RAG 입력은 자동 실행되지 않으며 개별 승인·실측 게이트를 따름.

## E. 비민감 결과 MD 보고 항목

```text
WORK_ID: L1-WORKSPACE-RAG-20261111-001 / CLPR implementation
SOURCE_BASELINE: [zip name / content hash / path]
GPT_DISPOSITION: ACCEPT_WITH_CHANGE
IMPLEMENTATION: PASS|PARTIAL|BLOCKED|NOT_RUN
MODIFIED_FILES: [...]
SELF_TEST: PASS|FAIL|SKIP|NOT_RUN (tests, commands, actual counts)
INDEPENDENT_DESIGN_REVIEW: REPORTED_COMPLETE (past design)
POST_PATCH_INDEPENDENT_REVIEW: NOT_RUN (no additional review requested)
HOST_E3: PASS|PARTIAL|NOT_VERIFIED
PUBLISH_GATE: PASS|BLOCKED
PACKAGES: [name, version, bytes, sha256, crc/path checks]
PUBLIC_RELEASE: [POSTED_VERIFIED|BLOCKED|NOT_POSTED]
PUBLIC_COMMIT / READBACK_SHA256: actual only
SKILL_UPDATER_INSTALLED / JOB_ACTIVATED / WORKSPACE_WRITE / KNOWLEDGE_PUBLISHED: separately
UNVERIFIED/APPROVAL_REQUIRED: [...]
NEXT_ONE_ACTION: ...
```

## F. 협업 구조 최종 점검

- GPT 판정은 PRIVATE `wonhwipark/CoWork-Skill-Collab` `main`, `collab/projects/L1-WORKSPACE-RAG-20261111-001/GPT_CLPR_DESIGN_REVIEW_DISPOSITION_r0001_20261114.md`를 정본으로 사용.
- READ/WRITE 역할: PUBLIC L1Work root(최종 검증 ZIP만), PUBLIC handoffs(업무 실행 인계), PRIVATE CoWork(판정·비민감 결과·영수증). 현재 README·CURRENT·TRACKER에서 실제 상태를 확인.
- GitHub 신규 MD 게시 자체는 Claude Code, Linux MCP, Job-list, watcher, 자동 유료 리뷰를 실행하지 않음. `REQUEST/READY` 생성/추가 리뷰 호출 금지.
- 정상 작업 경로는 **요청 1회 → 기존 패키지 검토 → 수정·시험 반복 → ZIP 생성·안전/호환 판정 → 가능한 최종 배포·원격 검증 → 비민감 결과 기록 → GPT 통합 판정**.
- 회사 제한자료 반출 0, 운영 DB/Job/Watcher/신뢰키/LIVE 변경 0, 승인 범위 외 추가 유료 호출 0.
- 차단된 항목만 `BLOCKED`, 나머지 실제 수행분은 이력·근거를 남기고 완료. **추가 리뷰 미실시를 리뷰 PASS로 기록하지 않음**.

## G. 단일 완료 조건

외부 GitHub README 링크나 인계 MD의 존재만으로 개발 성공·PUBLIC ZIP 배포·호스트 기능 확인을 추정하지 않는다. 실제 파일 바이트·시험 증거와 원격 readback 기준으로 개별 판정한다.
