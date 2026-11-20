# 업무 GPT 실행 인계 — 기존 L1 Workspace Viewer 2단계 기능 통합 원샷

- 개정: r0001 / 2026-11-20 KST
- 저장소: GitHub PUBLIC **wonhwipark/L1Work**, branch **main**
- 파일 경로: **handoffs/L1_WORKSPACE_VIEWER_TWO_PHASE_IMPLEMENTATION_ONESHOT_HANDOFF_r0001_20261120_KST.md**
- 대상: 이미 사용 중인 별도 Linux Viewer. 신규 서비스 구축이 아니라 기존 UI·handler·스킬 연결의 최소 확장
- 목적: ① 이슈번호 SOC-xxx 등 선두 표시와 Work 제목 정리 → ② 수정 버튼 전용 인증과 이슈·MSC 편집 요청 및 안전한 writer 연동
- 실행 책임: 업무 GPT(현장 근거·설계/시험 판정) / 허용된 Linux 로컬 Agent 및 업무 LLM(현장 개발·시험). Linux MCP의 기존 허용 계약 확인 전 도구 호출을 가정하지 않음
- 권한 경계: 이번 PUBLIC 게시 자체는 **업무 GPT용 비민감 인계서 전달**. Linux 코드/서비스·계정·DB·Knowledge·Work 변경, 설치·재시작·공유·Job 실행·유료 리뷰의 승인이 아님. 실제 업무 호스트에 이미 유효한 승인/권한이 있는 부분만 진행하고 나머지는 BLOCKED로 분리

## 0. 이전 전달물 (이미 있으므로 중복 개발·전달 금지)

| 구분 | 정확한 PUBLIC main 경로 | 사용 방식 |
|---|---|---|
| 기존 UI ZIP | [l1-workspace-wiki-ui_v0_1_0_1119.zip](../l1-workspace-wiki-ui_v0_1_0_1119.zip) | 기존 HTML/CSS/JS·화면·INTEGRATION.md·합성 시험. **267,140 B / SHA-256 411553e74e76bb82237fd2ebef65169769e4dbe4cfd2231afb5afd38559b10a9** |
| 기존 Viewer 인계 | [Viewer UI 변경·연동 r0002](L1_WORKSPACE_VIEWER_UI_CHANGE_AND_MCP_VALIDATION_HANDOFF_r0002_20261120_KST.md) | 기존 사용성 P1, adapter I-01~I-07, G0·B1~B3·E3/E4·복구 게이트 |
| 개선 화면 참고 | [L1_Workspace_Wiki_Usability_Preview_20261120_KST.html](L1_Workspace_Wiki_Usability_Preview_20261120_KST.html) | 합성 HTML 시안, 기존 ZIP에는 미포함, 실제 Linux Viewer 적용 완료본 아님 |
| 기존 UI 개발 인계 | [L1_WORKSPACE_WIKI_UI_BUSINESS_GPT_REVIEW_AND_INTEGRATION_HANDOFF_r0001_20261119_KST.md](L1_WORKSPACE_WIKI_UI_BUSINESS_GPT_REVIEW_AND_INTEGRATION_HANDOFF_r0001_20261119_KST.md) | 이전 화면 구조·시험·INTEGRATION 지침 |
| Agent/MCP 구분 | [L1_MCP_AGENT_SKILL_ACCESS_AND_CAPABILITY_HANDOFF_r0002_20261120_KST.md](L1_MCP_AGENT_SKILL_ACCESS_AND_CAPABILITY_HANDOFF_r0002_20261120_KST.md) | Viewer는 별도 브라우저 UI. MCP는 별도의 Agent→업무 스킬 접근 |

- v0.1.0의 Chromium 합성 56 PASS/정적 19 PASS는 **실제 Linux 호스트 적용·설치·편집 PASS가 아님**.
- 이전 UI 독립 UX R1은 ACCEPT_WITH_CHANGE(P1 두 건: MSC 가로 넘침 안내, CSS 중복 정리). 기존 편집 설계 독립 R1도 ACCEPT_WITH_CHANGE(별도-origin MSC 선택 모순, 인증 하드 스톱, draft/diff/commit별 ACL 재검사 지적). 이후 사용자 의견으로 **전역 로그인 제거 이력, 수정 버튼만 인증, 이슈번호 선두, Work ID 표기**가 추가되었으며 이 추가분은 독립 재리뷰/실서비스 시험 완료가 아님.
- CoWork PRIVATE의 r0004 원문을 업무 GPT가 읽지 못하더라도 이 문서가 사용자 확정 요구·검증 조건을 완전히 전달하도록 작성. 회사 코드·상세 MSC·로그·내부 URL/경로·개인정보·인증 비밀을 PUBLIC/CoWork PRIVATE에도 전송 금지.

## 1. 변경 불가: 사용자 최신 결정

1. **Viewer 첫 접속·검색·문서/MSC 열람은 기존과 동일하게 로그인 없이 Read Only.** 초기 Viewer에서 ID/PW 입력이 반복 실패해 동료도 읽을 수 있도록 사용자가 전역 인증 제거를 요청했다는 사실을 우선. 과거 전역 로그인 화면/설정을 재활성화하거나 동료마다 ID/PW를 요구하지 말 것. 현재 접속 범위를 기존 업무망 밖으로 확대하지 말 것.
2. **[수정] 클릭 시에만 편집 전용 ID/PW 및 서버 edit ACL 확인.** 기존 Viewer에 전역 인증 서비스가 있다고 단정 금지. 기존 호스트의 실제 편집자 인증 제공자/계정 정책을 G0로 확인하고 REUSE; 없다면 최소 편집 전용 설계·보안 시험을 진행하되 승인 없이 계정/비밀번호를 발급하거나 호스트 설정을 변경하지 말 것. 인증 없으면 쓰기 0, 읽기는 유지.
3. **기존 Work ID·폴더명·Evidence SHA·역링크/원본 데이터 불변.** Viewer 표시용 이름만 정리. 새 title DB/스키마/대규모 rename 금지.
4. **해당 Work의 검증된 이슈번호가 있으면 제목 맨 앞에 한 번만 표시.** 합성 예: SOC-1234 — NR L1 Tx — UL Tx Switching 분석. 번호 없으면 NR L1 Tx — UL Tx Switching 분석. 제목 정보 없으면 기존 Work ID, 번호만 있으면 SOC-1234 — 기존 Work ID. 이름/번호 예시는 **가상**이며 업무 실데이터를 뜻하지 않음.
5. **MSC 원본과 파생 HTML/SVG 구분**. Viewer에서 렌더된 DOM/SVG를 직접 canonical로 저장하지 말 것. 업무 코드 분석·LLM 자동 호출이나 그룹 Knowledge 게시를 Viewer 열람 행동에 연결하지 말 것.

## 2. STEP G0 — 기존 Linux Viewer 실체/권한/데이터 읽기 조사

업무 GPT가 직접 확인할 수 없으면 허용된 Linux 로컬 Agent로 **읽기 전용** 조회. 기존 프로젝트/Work의 유효한 근거를 먼저 재사용. 이 확인 자체는 서버 재시작·데이터 재생성·LLM 분석·설치·Job 실행 0.

| 확인 대상 | 확인할 항목(모르면 UNKNOWN/NOT_VERIFIED) |
|---|---|
| 실제 Viewer | 소스 repo·branch·revision, 실제 서비스·빌드/asset 구조, 현재 UI/읽기 API·renderer·검색 handler, 기존 무로그인 상태와 과거 로그인 제거 이력 |
| 메타·Work 표시 | 목록의 Work ID, verified issue key/대표 이슈번호 출처, 제목/summary/module, 기존 인덱스/ISSUE_OVERVIEW/README의 허용 필드, pagination·권한·검색·동명이름 |
| 패키지 사용 현황 | 기존 ZIP UI 중 적용된 부분, 별도 개선 HTML이 실제 배포됐는지, 현재 화면과 source revision 차이 |
| 읽기 안전 | B1 root containment/path traversal/symlink/TOCTOU, B2 본문·title·raw·search·cache·download·관련 항목의 제한자료 차단, B3 실제 MSC 별도 origin/sandbox/CSP·세션 정보 격리 |
| 편집 인증 후보 | 안전한 기존 로그인/운영 계정 provider 실존 여부, 문서별 edit ACL, 세션 TTL·CSRF·rate-limit·계정 보호·session fixation 방어 및 정책 |
| 기존 writer | Workflow/Kernel의 Work/Evidence writer·SHA/CAS/충돌/복구/readback, Updater 개인 초안·그룹 승인 경계, doc-converter canonical MSC→B형 HTML/SVG |
| MSC 식별 계약 | 부모 Viewer가 기존 허용된 canonical message/participant anchor 목록을 조회할 수 있는지, anchor/source revision/권한 서버 재검증 방법 |
| 배포 권한 | 격리 개발·시험 허용 범위, 실제 서비스 설치/설정/재시작·동료 공유 승인, 사전 백업·롤백 기준 |

각 항목은 **REUSE / CONNECT / 확인된 PROVEN_GAP / UNKNOWN**으로 판정. 기존 UI adapter의 listRoots/listChildren/getDocument/getDocumentMeta/getMscTarget/search/getSummary는 **예시 계약**이고 실제 API 이름이 아님. 없는 API/필드·영속 schema를 가정해 만들지 말 것. 실제 소스·호스트가 접근 불가면 G0=BLOCKED인 부분만 보류하고 합성 UI 개발·테스트는 계속.

## 3. STEP A — 1차 Work 이슈번호·제목 표시 개선

### A1. 표시 규칙

- 대표 이슈번호는 기존 Viewer/Work/인덱스에 **실제로 연결된 값**만 사용. 업무 문서 안에 SOC 문자열이 우연히 등장해도 대표 번호라고 추론하지 않음. SOC 외 번호 체계도 기존 업무 메타 계약에 따라 지원.
- 우선순위: **이슈번호 — module/제목/분석 요약 → module/제목/요약 → 원본 Work ID**. 번호만 있으면 이슈번호 — Work ID. 제목에 동일 번호가 원래 포함돼 있으면 중복 출력 금지.
- 하나의 Work에 관련 이슈번호 복수이고 **대표 지정 근거가 없으면 임의로 하나를 고르지 않음**. 번호를 제목에 강제 추가하지 않고 기존 제목/ID를 표시, 상세 영역에서 관련 이슈번호를 권한 범위 내 보여주는 방안을 고려.
- **같은 formatter**를 Work 트리·검색 결과·breadcrumb·문서 헤더에 사용. 보조 영역의 원본 Work ID를 항상 정확히 유지하고 복사 가능. Work ID/이슈번호/제목 검색은 기존 API 범위 안에서 같은 Work로 연결. 잘못된 출처·비밀/제한자료가 title/index/cache에 새로 노출되지 않게 B2 유지.
- Work ID·폴더·원본 SHA·모든 기존 링크 불변. 표시용으로 전체 Work 문서를 무차별 재귀 스캔하거나 별도 DB/검색엔진을 만들지 않음. 제목·번호 metadata가 없으면 **기존 ID fallback** 처리.

### A2. 기존 화면 개선 결합

- 기존 Wiki UI v0.1.0의 Work/Knowledge/전체 파일·가운데 본문·우측 목차·모바일 드로어를 유지. 실제 Viewer framework가 다르면 기존 컴포넌트에 필요한 자산·UX만 좁게 이식.
- 기존 P1: 12명 MSC 가로 넘침 시 **방향 힌트 제공/불필요 시 제거**, 중복 CSS media query/Readability 충돌 최소 정리. 문서/검색/탭별 마지막 위치 복귀·집중 보기 개선 HTML은 이미 구현된 부분과 비교해 필요한 범위만 반영.
- 기존 개선 인계의 I-01~I-07을 모두 확인: 합성 fixture 의존성 제거, 실제 API와 CSP/frame 연결, placeholder MSC 대신 기존 doc-converter B HTML, 기존 Markdown/링크 handler, 실제 metadata 상태, pagination, 별도 origin 상태/스크롤.
- 정적/합성 시험 후 실서비스 적용은 **B1~B3 및 기존 유효 설치 승인**을 확인했을 때만. 아니면 화면/adapter 패치와 후보·회귀 근거만 보존하고 HOST_CHANGE=BLOCKED.

## 4. STEP B — 2차 수정 전용 인증·편집·원본 안전

### B1. 인증·UX

- 일반 열람은 무로그인 유지, **[수정] 버튼 클릭 때만** ID/PW 모달 → 서버에서 해당 사용자의 source별 EDIT 권한 확인 → 성공 시 현재 Viewer 우측 편집 패널을 활성화. 취소·실패·권한 회수/만료면 기존 읽기 화면 복귀.
- 비밀번호를 GPT 대화·GitHub·공개 ZIP·클라이언트 localStorage/URL·로그에 절대 넣지 않음. 기존 호스트 편집 인증 경로가 없다면 현장 계정 관리 승인 범위를 확인 후 최소 구조를 설계하되, 인증 서버 확인 전 쓰기 핸들러 활성화 0.
- 필수 HARD_STOP: 서버의 인증 세션·문서별 edit ACL·CSRF·rate-limit/계정 보호·session-fixation 방어(인증 성공 시 세션 교체), 쿠키 보호·TTL·권한 회수 중 미확인/부재인 항목이 있으면 **EDIT_AUTHORIZED의 실서비스 활성화 금지**. 단순 로그인 UI 성공이나 업무망 접속은 쓰기 승인 근거가 아님.
- **draft 저장, Diff/Preview 요청, 확정 commit, writer 진입 직전** 각각 세션·CSRF·ACL·source revision을 독립적으로 재검사.

### B2. 직접 편집과 MSC 구조 수정 요청의 구분

- 1차 편집 범위: 이슈 본문·코멘트·MSC 설명의 텍스트 수정, 사용자 Diff/Preview, 명시적 초안 저장 또는 개정본 확정. 실제 작성은 재사용 가능한 **기존 Workflow/Kernel/Updater writer**로만, 검증된 source에 한정.
- **MSC 메시지·participant 수정 요청 UI는 첫 구현부터 포함.** 부모 Viewer가 기존 서버에서 받은 권한 검증된 canonical anchor 목록을 자기 DOM에 표시, 해당 항목을 선택해 메시지 문구/순서·participant 이름/관계 수정 의도를 제출할 수 있게 설계.
- 별도 origin의 MSC iframe 내부 화살표를 부모가 직접 클릭해 수정한다고 가정하거나 임의 postMessage 전역 bridge를 열지 말 것. canonical anchor/원본 식별과 서버 재검증이 없다면 **문서 단위 수정 요청 메모만 허용**, 실제 구조 변경 저장 HOLD.
- 기술 사실/구조 변경에는 기존 Agent/code-analyzer의 근거 검증과 별도 실행 승인 확인. 단순 오탈자 변경마다 모델 호출 금지. 기본 후보: 사용자 명시 요청 1건당 최대 1회, 자동 재시도 0, 유효한 비용/호스트 정책 확인 전 자동 실행 비활성.
- 실제 canonical 원본 수정이 확정되고 writer readback에 성공한 뒤에만 기존 doc-converter B형 HTML/SVG 재생성. 렌더 실패 시 source 재저장·LLM 재실행 금지. Group Knowledge 게시/승인은 Updater의 별도 절차로 처리.

### B3. 안전 저장과 충돌

- base revision/hash → 후보 변경 → Diff/Preview → [초안 저장] 또는 [개정본 확정] 명시적 사용자 선택.
- 원본 revision이 변경됐으면 강제 덮어쓰기 0. 지원 확인된 CAS/3-way/멱등키만 활용, 충돌은 사용자 결정. 저장/변환/그룹 게시 상태 각각 별도 기록.
- 성공은 **실제 기존 writer의 revision/hash readback** 후만 표시. 실패/불확실 시 임의 Job/분석/저장을 재실행하지 않음. 기존 Work/Evidence 감사·버전 이력/복구 원본 보존. 새로운 Viewer 전용 영속 원장을 기본 추가 금지.

## 5. TEST & 운영 적용 게이트

| ID | 수락시험 — 실제 수행한 범위만 PASS |
|---|---|
| T01 | 무로그인 동료 첫 접속·검색·문서/MSC 열람, 첫 화면 ID/PW 0, 쓰기 API 직접 호출 거부 |
| T02 | 대표 이슈번호 확인됨 / 없음 / 번호만 / 복수 모호 / 제목에 번호 중복 / 동일 제목 / 제목 없음 및 안전 fallback |
| T03 | 목록·breadcrumb·문서 헤더·검색이 같은 이슈번호/제목/원본 Work ID를 표시/검색, 원본 폴더·링크·Evidence hash 불변 |
| T04 | 긴 제목·수백 Work/pagination·1440/720/390/320 및 MSC 6/12 participant, P1 스크롤 힌트·CSS 회귀·읽던 위치 복귀 |
| T05 | B1 경로 traversal·symlink/TOCTOU, B2 title/search/raw/cache/download/diff/preview 제한자료 차단, B3 iframe origin/sandbox/CSP/위조 anchor |
| T06 | 수정 버튼에서만 인증; 오입력·편집권한 없는 동료·만료·회수·session fixation·CSRF·rate-limit 각각 서버 차단 |
| T07 | draft/diff/commit 각 단계에서 권한 변경/세션 만료 주입, 원본 write 0 |
| T08 | 메시지/participant 검증된 anchor 선택과 부정 anchor 거부, 구조 변경 미확인 시 요청만 남고 원본 변경 0 |
| T09 | 변경 Diff/Preview, CAS/stale·동시 작업, 저장 성공·렌더 실패 분리, readback·rollback |
| E3 | 승인 범위 내 실제 Linux localhost 배포/화면·인증·원본 SHA/복구 시험 |
| E4 | 별도 공유 승인 하 동료 무로그인 Read Only + 편집자 두 역할 실제 접근 시험 |

- **B1/B2/B3 BLOCKING·G0 미확인·E3/E4 NOT_RUN**을 정적 UI 테스트로 해결했다고 선언 금지. 1차 읽기 기능도 실서비스 변경은 기존 안전 기준/운영 승인 충족 때만 가능.
- 호스트 운영 변경 승인과 보호 게이트가 유효할 경우에만 **기존 설치 baseline/SHA·백업/rollback → 좁은 적용 → 실제 URL/동료 브라우저 확인 → 새 revision readback/rollback 연습**. 권한 밖 설치/재시작/자격증명 생성/공유는 BLOCKED·NOT_RUN.
- 호스트 개발·합성시험은 가능하다면 먼저 완료해 후보/정확한 파일 diff·시험 보고를 기존 업무 Work에 보존. 과거 리뷰 자동 R2·새 유료 요청·Job/Knowledge 게시 자동 트리거 금지.

## 6. 업무 GPT 원샷 지시 — 아래 순서로 끝까지 처리

1. GitHub **wonhwipark/L1Work / main**에서 본 문서 **handoffs/L1_WORKSPACE_VIEWER_TWO_PHASE_IMPLEMENTATION_ONESHOT_HANDOFF_r0001_20261120_KST.md**를 열고 기존 UI ZIP, r0002 Viewer 인계, INTEGRATION.md 및 필요 시 MCP 구분 자료를 읽기. 전달 완료된 ZIP 중복 생성·재배포 금지.
2. 실제 업무 Linux Viewer의 소스 repo/branch/revision, 기존 UI 동작, 무로그인 Read Only/전역 인증 제거 이력, Work issue key/title 데이터, 보안/권한, 원본/Writer API를 **G0 읽기**로 확인. 접근 못하면 권한 허용된 로컬 Agent가 확인하고 근거를 업무 Work에 보존. 확인 안 된 API는 만들었다고 보고하지 말 것.
3. **1차**: Work 리스트·이슈번호 선두·제목/ID fallback·검색/깊은 링크, 기존 UX P1·필요한 개선만 최소 개발·관련 합성/현장 가능한 시험. Read Only·기존 문서·URL 보존.
4. **2차**: 수정 버튼 전용 인증·이슈/코멘트/MSC 텍스트·메시지/participant 수정 요청 UI·Diff/Preview·원본 CAS/편집 ACL 연동을 확인된 계약까지만 개발. 인증·writer·canonical anchor가 없으면 실쓰기 활성화는 BLOCKED로 유지하되 UI/합성 검증을 마무리.
5. 시험표 T01~T09 / B1~B3 / E3/E4에서 실제 PASS/FAIL/SKIP/NOT_RUN 증거를 개별 기록. 가능한 범위의 원인 보완과 관련 재시험을 같은 작업에 묶고 이미 완료된 리뷰/분석/Job을 재실행하지 말 것.
6. 유효한 실제 호스트 설치/운영 승인·백업/안전 게이트가 확인된 **경우에만** 기존 Viewer에 적용 및 실브라우저 점검. 승인 없으면 candidate source/patch/패키지·시험·롤백 계획을 해당 업무 Work에 보존하고 HOST_DEPLOY=BLOCKED. 임의 인증키·계정·운영 정책 변경 절대 금지.
7. 끝에 아래 숫자 표를 한 번에 보고. **제품 코드·상세 MSC·로그·실경로·서버 URL·계정·토큰은 업무 호스트 안에서만 보존하고 외부 공개/전달 금지.**

## 7. 사용자 보고 — 긴 주관식 설명 대신 숫자

표기: **1 PASS / 2 FAIL / 3 NOT_RUN / 4 BLOCKED / 5 UNKNOWN**. 실제 근거가 불충분하면 1 금지.

| 항목 | 값 |
|---|---|
| G0 실제 Viewer/권한/데이터 확인 | 숫자 |
| 1차 Work 이슈번호·제목 UI 구현/합성 시험 | 숫자 |
| 1차 실제 Linux E3 적용 | 숫자 |
| 2차 편집 전용 인증·UI 구현 | 숫자 |
| 2차 실제 원본 writer/MSC 안전 연결 | 숫자 |
| B1 / B2 / B3 | 숫자 3개 |
| E3 / E4 | 숫자 2개 |
| 원본 SHA 불변·충돌/롤백/readback | 숫자 |
| 운영 적용/동료 열람 | 숫자 |

통합 한 줄: **현재=... | 변경=... | 시험=... | 미확인/차단=... | 증거 보존=업무 Work 내부 | 다음 한 행동=...**.

이 파일 게시는 **업무 GPT에 대한 구현 인계 준비**일 뿐 자동 업무 GPT 메시지 수신, Linux Agent 작업 시작, 실제 Viewer 배포 완료를 의미하지 않음.
