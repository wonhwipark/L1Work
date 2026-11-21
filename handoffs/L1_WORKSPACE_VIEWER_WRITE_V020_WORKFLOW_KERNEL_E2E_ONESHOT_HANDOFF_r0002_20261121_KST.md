# 업무 GPT 실행 인계 r0002 — Viewer Write v0.2.0 × l1-fix-workflow × work-ledger-kernel E2E

- 작성: 2026-11-21 KST
- 정본 위치: **GitHub PUBLIC `wonhwipark/L1Work` / branch `main` / `handoffs/L1_WORKSPACE_VIEWER_WRITE_V020_WORKFLOW_KERNEL_E2E_ONESHOT_HANDOFF_r0002_20261121_KST.md`**
- 기존 CoWork Work: `L1-WORKSPACE-RAG-20261111-001` (새 Work 생성 금지; 업무 Linux에서 진행 중인 동일 목적의 기존 Work·분석·결정 이력 먼저 재개)
- 사용자 요청: **Write UI만으로 끝내지 말고, `l1-fix-workflow`와 `work-ledger-kernel`까지 실제 저장 E2E를 확인하여 필요한 경우 최소 수정 후 시험·후속 적용**. 업무 GPT가 검토/조정하고 허용된 Linux Agent·실행 LLM이 실제 구현·시험 수행. G0만 확인하고 무조건 종료하지 말되, 미권한·보안 위험·미확인 API에는 fail-closed.
- 이 문서는 **기존 r0001 Write HO를 보완하는 우선 실행 인계**. r0001/기존 ZIP/Work/영수증은 불변 보존. 파일 게시 자체로 업무 GPT가 자동 실행되거나 호스트에 설치되는 것은 아님.

## 1. 실제 읽을 원본·SHA 고정

| 기존 자산 | L1Work/main의 정확한 파일 | 확인된 공개 ZIP/경계 |
|---|---|---|
| Viewer 읽기·색감 | `l1-workspace-viewer-ui_v0_1_2_1121.zip` | 74,940 B / SHA-256 `9be14c4c34c2a7d923d8b11c01fb0249d41e820861721f275001f0f7d499d9e3` |
| Viewer 편집 UI **v0.2.0** | `l1-workspace-viewer-write-ui_v0_2_0_1121.zip` | 21,171 B / SHA-256 `9f2df44348478eb44615bddef8f211645fa1c07ed71d43580b4fb324e376b6f9` (Git blob `aed05a83e70efbe32f28bf494b6bf7b984f3f09b`) |
| Viewer 사용자 환경설정 **v0.3.0** | `l1-workspace-viewer-preferences_v0_3_0_1121.zip` | 20,661 B / SHA-256 `228c60bada8a92591f7ae855dfabe206e018d9e59970cf2d1b773d4d00072812` — Write와 독립된 표시·숨김 |
| Workflow 공개 참조 | `l1-fix-workflow_v1_6_74_1119.zip` | 760,324 B / SHA-256 `b810ce0cf072609431737c58b0ef2b7a0a8ec0701a0746e6a94283c374224989` |
| Kernel 공개 참조 | `work-ledger-kernel_v0_7_42_1116.zip` | 320,083 B / SHA-256 `ece2bce143ef35a1c8cc3bc12ddf6a73e27e0f218fc69fec87844759d9dfc164` |
| MSC Converter 참조 | `doc-converter_v0_2_26_1117.zip` | 공개 v0.2.26, 업무 Linux 실제 설치·호출 미검증 |

- 위 파일명은 2026-11-21 L1Work `main` Git tree 직접 조회(전체 tree `truncated=false`)로 확인. **공개 최신 ZIP ≠ 업무 Linux 활성 설치본**. 설치 스킬의 실제 위치·branch/revision/사용 중인 API는 G0에서 별도 확인.
- 참고 r0001: `handoffs/L1_WORKSPACE_VIEWER_WRITE_V020_G0_AND_INTEGRATION_HANDOFF_r0001_20261121_KST.md`.
- 설계 근거: CoWork `main/collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_VIEWER_AUTH_EDIT_DETAILED_DESIGN_r0004_20261120_KST.md`, `WIKI_UI_SKILL_INTEGRATION_COMPATIBILITY_REVIEW_r0001_20261120_KST.md`. 기존 설계 독립 R1 판정 ACCEPT_WITH_CHANGE이며 **Write v0.2.0 실제 코드 독립 리뷰/호스트 E2E는 NOT_RUN**.

## 2. 업무 GPT·실행 LLM/Agent 책임과 Write 기능 소유권

| 계층 / 주체 | 반드시 확인하고 재사용할 책임 | 수정 필요 조건 |
|---|---|---|
| 설계 GPT | Write r0004 / 본 r0002의 요구·수락 기준, 결과 판정·CoWork 상태 관리 | UI/원본 소유권 변경 지시하지 않음 |
| 업무 GPT | 업무 Linux G0, 실제 설치 스킬/원본 읽기 계약·권한 확인, 실행 LLM에게 좁은 범위 구현·시험 요청, 증거 검수 | 실제 지원/결손 구분하여 수정 최소화 |
| Linux Agent·실행 LLM | 허용된 Linux 개발 작업, 코드 변경, 격리시험, 필요한 현장 보고서/승인 범위 내 적용 | GitHub 문서만으로 신규 서비스·계정·원장/DB 생성 금지 |
| **Viewer Read/Write UI** | 무로그인 Read Only 유지, [수정] 클릭 때만 인증 dialog, 편집 입력·Diff/Preview·저장 상태 표시. `L1ViewerWriteHostAdapter`는 **합성 프런트엔드 계약**, 존재하는 Linux API라고 단정 금지 | 실제 Viewer의 읽기 handler와 세션·ACL 보호된 host adapter 사이에 좁게 CONNECT |
| **`l1-fix-workflow`** | 기존 Work 선택/재개, 이슈 분석·기술 결정/코멘트의 작성 주체·개정 작업 연결·Work 진행/Evidence 관계 유지 | 기존 workflow에 **Viewer 수정 요청 → 같은 Work 개정** 진입이 실제로 없다면 검증된 gap에만 최소 EXTEND |
| **`work-ledger-kernel`** | Work ID·Evidence ID·revision/hash·기존 원장·source pin, 안전한 artifact/write 경계·이력/영수증/readback. Kernel의 export 기능을 실제 canonical writer와 혼동하지 않음 | 개정본 쓰기/CAS 또는 stale·충돌/복구/readback/근거 기록의 기존 지원이 부족함이 입증될 때만 최소 EXTEND |
| **기존 Git/P4 writer·API** | 실제 보존·commit/revision/readback, 권한/충돌/롤백 계약 | Kernel만이 유일한 실파일 writer라고 가정하지 않음 |
| `l1-knowledge-updater` | 개인 Knowledge source의 쓰기 owner, Preview·승인 후 그룹 게시·역링크 | Knowledge 대상에만 CONNECT. **모든 Knowledge 수정에 전체 Workflow를 강제하지 않음** |
| `doc-converter` | 확정된 canonical MSC에서 B형 HTML/SVG 파생 렌더 | 구조적 MSC 변경 근거·canonical anchor·writer가 확인되기 전에는 재생성/확정 금지 |

**판정 규칙**: Workflow·Kernel은 Write E2E의 **필수 연동 대상**이지만 ZIP 코드를 **선제적으로 무조건 수정할 대상은 아님**. `REUSE → CONNECT → 입증된 GAP만 최소 EXTEND`; 미확인 API·스키마를 만들어 구현 지시하지 않음. 기존 Kernel export/MSC_VIEW 읽기를 수정 writer 지원으로 허위 PASS 판정 금지.

## 3. E2E 시퀀스 — Write 진입부터 원본 확인까지

`READ_ONLY(동료 무로그인)` → **[수정] 클릭** → 편집 전용 ID/PW 및 서버 세션·CSRF·rate-limit·계정 보호·해당 source의 ACL 검사 → `GET canonical source+sourceRevision/hash+owner+Work ID/Evidence ref` → UI 수정 의도/초안 입력 → **서버 재권한 검사 후 Diff/Preview** → **서버 재권한 검사 후 초안 저장 + readback** 또는 **최종 저장 직전 서버 권한·원본 revision/CAS·대상 owner 재검사** → **기존 Workflow(Work 대상)/Updater(Knowledge 대상)와 Kernel·검증된 writer의 해당 owner 경로 단일 저장** → receipt/actual bytes hash/revision/readback → 원래 Work 연결·사용자 저장 상태 표시.

- Work 원본은 기존 Work ID/폴더·원본 Evidence 불변을 기본으로 **새 개정 이력·확정 revision을 연결**. 파일 직접 overwrite·이력 손실·동명이인 Work 새 생성 금지.
- **문서 종류/owner 분기:** 이슈/결함 Work 분석 문서이면 Workflow의 기존 Work 및 Kernel 기록 경로; 개인 Knowledge 원본이면 Updater의 기존 쓰기 경로; 변환된 B형 MSC HTML/SVG는 **원본이 아니라 파생물**. 실제 owner·수정 가능한 canonical field가 확인 안 되면 EDIT_DISABLED/HOLD.
- 수정 요청의 대상에 기존 작성 결과·CODE_FACTS/Evidence 등 확정 사실/읽기 전용 원본이 섞이면 **문서별 수정 가능 범위를 먼저 확인**, 원본 사실 파일이나 그룹 정본 직접 수정 금지.
- 초안 저장, Diff 생성, Commit 각 **호출 시점마다** 인증 세션·CSRF·문서별 write ACL 재검사. Commit은 실제 writer 직전에도 재검사. 권한 회수/만료/원본 stale·CAS 충돌이면 원본 변경 0.
- 실패 구분: `AUTH_DENIED`, `PERMISSION_CHANGED`, `SOURCE_STALE`, `CONFLICT`, `WRITE_FAILED`, `WRITE_UNCERTAIN`, `RENDER_FAILED`, `READBACK_FAILED`. 모델/작업 자동 재실행·강제 덮어쓰기 0. **원본 저장 성공·렌더 실패는 PARTIAL**로 별도 복구하고 writer 재실행하지 않음.
- MSC 메시지/participant 수정·추가 **요청 UI**는 유지. canonical anchor 제공자가 검증되면 부모 Viewer가 받은 ID만 사용. 별도 origin iframe DOM/SVG를 편집 정본으로 다루지 않음. 구조적 순서/방향 변경의 확정은 **anchor·근거 검증·CAS·writer·converter 연동이 입증될 때까지 HOLD**.
- Knowledge 그룹 공용 게시와 Viewer의 초안/Work 개정 저장은 **별개 승인·revision/readback**. 한 단계 성공을 다른 단계 성공으로 승격하지 않음.

## 4. 원샷 실행 절차 — G0 뒤 가능한 범위까지 계속

1. **G0 READ-ONLY 조사(업무 GPT 승인된 기존 Agent):** 현재 업무 Linux Viewer 실제 repository/branch/commit/설치 위치/asset·읽기 handler·CSP/MSC origin, 로그인 제거 이력, 기존 auth provider/ACL/CSRF/session/credential handling, 로컬 설치된 `l1-fix-workflow`·`work-ledger-kernel` 원문/버전/entrypoint·실 writer 호출·업무 Workspace 구조, `l1-knowledge-updater`/Converter의 필요 범위, 현재 Write 설치 여부 및 설정 v0.3.0 공존을 **이미 존재하는 Work 보고를 우선 재사용**하여 조회. 회사 제한 원본·토큰·계정·실 MSC/로그 GitHub 반출 금지.
2. **기존 함수/원본 매핑표 확정:** `Viewer [수정]`의 owner/source type/Work ID/revision→`Workflow` 진입/개정 경로→`Kernel` Work/Evidence/원본 고정→실제 Git/local writer→diff/commit/readback/rollback을 **실제 설치 함수·입력/출력/소스 위치**로 연결. `WORKFLOW=REUSE/CONNECT/GAP/UNKNOWN`, `KERNEL=REUSE/CONNECT/GAP/UNKNOWN`를 각각 독립 판정. 소스 파일명이 없거나 함수 미확인이면 가상의 API를 구현한다고 단정하지 않음.
3. **안전한 부분부터 연결·구현:** 1차 v0.1.2·Write v0.2.0 고정 SHA/CRC/manifest로 격리 조립. 실제 host adapter가 부족하면 현장 인증 owner가 허용하는 최소 프런트–서버 연결만 구현; 기존 writer가 부족하면 **그 부족한 부분에 한정하여** Workflow 또는 Kernel의 사전 호환성을 보존하며 개발·자체시험·새 패키지 후보를 생성. **서버 인증 보호나 canonical writer가 미검증이면 Write API 활성화 금지하고 개발·시험 결과만 정리**.
4. **환경설정 v0.3.0 공존:** 별도 설정 창의 localStorage/표시·숨김은 **사용자 화면용**이며 Work 쓰기 권한·비밀번호·source ACL·Evidence와 무관. `#doc-actions` 환경설정 버튼과 [수정] 버튼 둘 다 유지, 설정 숨김 후에도 서버 write ACL 우회 0. v0.3.0 실제 DOM 매핑 전에는 해당 설정을 우회하지 말고 읽기 동작을 보존. 세 ZIP을 수정 없는 원본 상태로 두고 후보 조립 및 회귀 결과를 남김.
5. **격리 E2E 시험:** 기존 Work의 **허용된 무민감 샘플 또는 승인된 테스트 Work** 1건으로 초안→Diff/Preview→저장/revision/readback, 동료 Read Only 사용자·편집자 두 역할 분리, 이전 Evidence SHA 불변, Work ID 동일, Viewer 반영 확인. 미확인/금지 상태면 **합성 드라이런**을 대신 수행하고 실제 통합/실쓰기 PASS로 말하지 않음. 직전 호스트 허용 범위 외 유료 모델/Job 자동 실행 0.
6. **실제 시험·보안/복구:** B1 canonical containment/symlink·경로 이탈, B2 문서/제목/검색/raw/download/cache 권한, B3 MSC iframe origin/sandbox/CSP, 편집 세션 CSRF/TTL/회전/rate-limit/세션 고정·권한 회수, 2회 클릭/timeout 뒤 중복/WRITE_UNCERTAIN retry0, CAS 동시 변경/3-way/conflict, 실패 후 rollback/readback, 1440/720/390/320·키보드·MSC 6/12와 저장 UX. 상태는 `PASS/FAIL/SKIP/NOT_RUN` 각각 증거와 함께.
7. **후보 패키지/동작 경계:** Workflow/Kernel 변경이 입증되면 **해당 스킬의 기존 이름·새 버전**과 diff/테스트를 별도 보존, ZIP 이름 `<skill>_v<major>_<minor>_<patch>_<MMDD>.zip`·SHA/크기/CRC·경로/민감정보 검사. 변경 없으면 **WORKFLOW_REUSE / KERNEL_REUSE** 명시하고 새 ZIP 만들지 않음. 회사 제한 코드는 허용된 **업무 Linux Work 내부**에만 보존; L1Work/CoWork PUBLIC에 코드를 게시하지 않음. 공개 허용 가능한 비민감 인계·집계 결과만 별도.
8. **호스트 설치/Write ON:** 유효한 운영 설치/설정 권한과 B1~B3/EAuth/E3/E4·백업/롤백·기존 writer readback이 모두 확인됐을 때만 **허용 범위 내** 기존 Viewer/스킬 적용. 권한 없는 서비스/DB/계정 변경·자동 공개 게시 금지. 실제 운영 승인이 없으면 해당 단계 `BLOCKED`로 표기하되 개발 후보·시험·인계는 마무리. 신규 유료 Claude 리뷰 자동 요청 0.
9. **같은 Work에 통합 결과**: 업무 GPT가 실제 스킬 source revision·수정 필요 판정·각 테스트·호스트 권한/차단·증거 위치·실행 영수증·rollback·변경 내용·다음 한 행동을 기존 업무 `l1-workspace` Work 및 CoWork 관련 Work의 **비민감 요약**에 기록. 설치 미확인/실호출 미실행을 완료로 승격하지 않음.

## 5. 필수 수락 조건 / 회귀 반례

| ID | 시험 시나리오 / 검증 포인트 | 성공 조건 |
|---|---|---|
| W01 | 동료 무로그인 열람/검색/MSC | 기존 Read Only 지속; 편집 API 접근 0 |
| W02 | 로그인 실패·Read Only 사용자·권한 없는 문서 | [수정] 통한 save 0, 원본 변형 0 |
| W03 | [수정] 후 workflow가 **같은 Work ID**를 재개 | 별도 목적의 새 Work 생성 0, 문서·Evidence 소속 정확 |
| W04 | Kernel/실 writer의 초안→Diff→명시적 COMMIT | 실제 revision+영수증+readback, 원본 SHA/이력 보존 |
| W05 | 세 시점(초안·Diff·Commit) 세션 만료/권한 회수 | 호출 모두 재검사, 무허가 write 0 |
| W06 | stale revision·2인 동시 편집·중복 클릭/타임아웃 | CAS/충돌 fail-closed, 중복 write 0, 불확실성 보고 |
| W07 | 저장 성공 후 MSC 변환 실패 | 저장/렌더 결과 분리, writer 재호출 0 |
| W08 | MSC participant/message 수정 요청 | 부모 DOM canonical anchor 확인, structural 확정은 검증 전 HOLD |
| W09 | Knowledge source에 Write 요청 | Updater 단일 owner, 무승인 그룹 게시 0 |
| W10 | 환경설정 v0.3.0과 Write v0.2.0 공존 | [환경설정]/[수정] 모두 정상, 숨김으로 ACL 변화 0 |
| W11 | B1/B2/B3 + E3/E4 | 각 게이트의 **실제 호스트 증거** 존재 |
| W12 | 실제 Work/기술 원문 범위 준수 | 회사 제한 자료 PUBLIC 반출 0, 소스·Evidence hash 보존 |

## 6. 업무 GPT → 설계 GPT 반환 양식 (숫자 최소 입력)

상태 코드 `1=PASS, 2=FAIL, 3=NOT_RUN, 4=BLOCKED, 5=UNKNOWN`.

```text
Viewer source/G0: [1~5]
Write v0.2.0 & Preferences v0.3.0 조립: [1~5]
l1-fix-workflow: [REUSE | CONNECT | GAP | UNKNOWN] / 수정:[YES | NO | HOLD]
work-ledger-kernel: [REUSE | CONNECT | GAP | UNKNOWN] / 수정:[YES | NO | HOLD]
실제 writer/Work ID·Evidence SHA/CAS/readback: [1~5]
AUTH/CSRF/ACL/SESSION: [1~5]
MSC canonical anchor/변환기: [1~5]
B1 B2 B3: [1~5] [1~5] [1~5]
E3 E4: [1~5] [1~5]
Linux Write 활성화: [1~5]
변경된 실제 스킬 ZIP/버전/설치: [각 NONE 또는 검증된 항목]
업무 Work ID/근거 위치: [제한정보 비반출 요약]
다음 한 행동: [한 문장]
```

**핵심 완료 기준:** 단순 프런트 v0.2.0 설치가 아니라 **Viewer → 실제 허용된 Workflow/Kernel/기존 writer → 기존 Work revision·Evidence 이력 → readback → Viewer 반영** 경로를 입증하는 것. 이 경로가 막히면 어떤 단계가 왜 차단됐는지 구체화하고, 같은 범위의 개발·시험은 계속해 사용자에게 중복 지시를 요구하지 않을 것.
