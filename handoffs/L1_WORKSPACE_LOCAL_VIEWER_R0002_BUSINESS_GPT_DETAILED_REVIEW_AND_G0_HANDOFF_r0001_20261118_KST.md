# 업무 GPT 상세 검토·실행 게이트 인계 — L1 Workspace 전체 트리 로컬 웹 뷰어 r0002

- 문서 개정: r0001 / 2026-11-18 KST
- 기존 협업 Work ID: `L1-WORKSPACE-RAG-20261111-001` (같은 Work 재개, 신규 Work 생성 금지)
- 작업 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, `main`, `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md`
- 인계 위치: GitHub PUBLIC `wonhwipark/L1Work`, `main`, `handoffs/`
- **최신 사용자 지시:** 이번에는 Windows Claude **독립 리뷰 생략**, 업무 GPT가 r0002 설계를 직접 상세 검토. 기존 리뷰 REQUEST/READY/유료 호출을 새로 발행하거나 재실행하지 말 것. Linux 운영 변경은 별도 승인 Gate.
- **현재 판정:** `GPT_DESIGN_DISPOSITION=ACCEPT_WITH_GATES` (아래 조건부 정적 설계 방향 승인), `INDEPENDENT_REVIEW=NOT_RUN / USER_WAIVED_FOR_THIS_HANDOFF`, `LINUX_HOST_G0=NOT_VERIFIED`, `VIEWER_DEPLOYED=NOT_RUN`, `LOCAL_AUTHORITY_CUTOVER=NOT_RUN`, `GROUP_KNOWLEDGE_WRITE=NOT_RUN`.
- **문서의 실제 효력:** 업무 GPT가 추가 설계·G0 판단을 내릴 수 있도록 제공하는 상세 검토용 작업 지시. 문서 게시 자체는 실행 호스트 승인, 스킬 설치, 서비스 기동, 원본 이관, 그룹 게시 또는 비용 승인이 아님. **현재 즉시 허용된 범위는 기존 승인 도구를 이용한 읽기 전용 상태·계약 확인과 비민감 설계 검토**에 한정.

## 1. 최종 목표·r0002 확정 요구

**목표:** Linux 업무 환경의 실제 `l1-workspace` **업무 콘텐츠 전체 폴더 트리**를 업무 네트워크의 **하나의 웹 URL**에서 탐색하고, 권한 있는 동료가 폴더/Work ID/파일을 읽기 전용으로 열람. 파일 형식에 맞게 브라우저에서 렌더링하되 원본 및 Work/Evidence 이력은 보존.

1. Work별 선택 공개 목록과 문서별 승인을 **기본 UX의 필수 절차에서 제거**. 승인된 업무망 사용자에게 전체 **업무 콘텐츠**를 탐색·검색할 수 있도록 한다. 단, 네트워크 접근 승인·인증 및 시스템 비밀/제한 자료 차단은 필수. “전체”가 Linux OS 전체·인터넷 익명 공개·토큰/개인키/제한 자료 공개를 뜻하지 않음.
2. 실제 루트의 폴더/Work 구조를 유지하여 `works/<work_id>/`, `index/`, 기존 `knowledge/` 등이 **존재하는 경우** 탐색. 실경로·실제 Knowledge 저장 위치·쓰기 주체는 G0 확인 전 추정 금지. 동명 GitHub.com 저장소가 업무 `l1-workspace`의 실체라고 가정 금지.
3. **Markdown 전량을 HTML 파일로 사전 변환하지 않음**. 원본 `.md`를 보존한 채 열 때 renderer가 HTML 표시(또는 안전한 갱신 캐시). 기존 B형 MSC HTML+SVG 인터랙션, PDF·이미지·JSON·TXT·CSV·YAML 등은 형식별 뷰어로 처리.
4. Work 원본·Kernel Ledger/Evidence·source revision·해시·결정·시험·리뷰·그룹 지식 반영 이력은 그대로 유지. 웹 화면은 **읽기 전용 표현 계층**이며 독립 Knowledge writer 또는 새 정본이 아님.
5. Linux 웹 뷰어 도입과 **GitHub writer 폐지/로컬 원본 authority 전환**은 완전히 다른 작업. 후자를 당장 시행하지 않으며 복구·단일 writer·백업·호환 게이트와 별도 명시적 승인 필요.

## 2. 이미 알려진 근거와 미확인 항목

| 구분 | 확인된 내용(정확한 범위) | 이 인계에서 확정하지 않는 항목 |
|---|---|---|
| `work-ledger-kernel` 개발 후보 | v0.7.45 개발 패키지의 격리 합성 시험에서 **비Git 새 폴더로 12개 문서 export** 및 재export 바이트 동일성 PASS. 관련 pytest 5 PASS. Legacy TL_REVIEW 공유 차단 관련 시험 포함 | Linux **실제 설치본** 동일 기능·버전, 운영 Work에 안전하게 호출 가능한지 |
| `l1-fix-workflow` 개발 후보 | v1.6.72 코드 검토상 `docs_sync`에 Git origin/registered role/clean tree, `docs_push`에 commit/push/remote readback 의존 존재 | 현재 Linux 설치 버전, 별도 local mode·기존 우회 경로 제공 여부 |
| MSC 링크 | 합성 Work-root `MSC_VIEW.md` → 실제 `published_path` HTML 링크 검증. Converter **상세 원본 Markdown**의 일부 기존 상대 HTML 링크는 BROKEN 보고 | 현장 전체 MSC·상대 자산·브라우저 호환성 |
| r0002 설계 입력 | CoWork PRIVATE의 r0002 검토 ZIP **91,324 bytes**, SHA-256 `6a013a104ebfefeae6dc452965ce99ce5a3f9637ed538c778d8cb5189d5a7e5f`; 9개 입력·CRC/원격 조회 검증 기록 | 설치 가능한 스킬 ZIP·Linux Viewer 바이너리 또는 운영 실행 완료 여부 |
| Claude 독립 리뷰 | 해당 로컬 뷰어 설계에 대한 **리뷰 결과·영수증 없음**. 과거 Windows 비용 정책 불일치로 사전검증 차단 기록. | Claude PASS·review 완료·비용 청구를 추정하지 않음. **최신 사용자 지시로 이번 인계에서는 생략** |
| 실제 Linux 환경 | G0/웹서버·URL/실제 root·파일 수·보안 정책·동료 접근·백업/복구·그룹 writer E3 | **NOT_VERIFIED/NOT_RUN**. 설계·격리 시험을 현장 PASS로 승격 금지 |

**GPT 자체 정적 판정:** ① 원본/뷰어/그룹 정본을 분리하고 ② 기존 Git Writer를 보존하며 ③ 전체 업무 트리 read-only UX를 G0→합성 시험→별도 승인된 호스트 시험으로 진행하는 **방향은 수용**. 다만 보안 격리·기존 서비스 적합성·실제 수용 테스트가 미검증이므로 운영 배포는 **HOLD**. 이는 Claude 독립 리뷰 PASS 대체가 아님.

## 3. 목표 아키텍처와 책임 경계

```text
업무 GPT / 허용된 Linux Agent·MCP
  ├─ Updater 직접 Procedure·Feature 분석
  └─ Workflow의 ISSUE·FEATURE·REFACTOR·DESIGN 분석
       └─ 동일 기존 Work ID·Kernel Ledger·Work/Evidence·source revision
             ├─ 원본 l1-workspace (기존 writer/Git/복구 유지)
             │    ├─ works/ · index/ · 존재하는 knowledge/
             │    └─ 개인 Knowledge 후보: 기존 Updater writer만 쓰기
             ├─ READ_ONLY 파일 조회 / 안전한 격리 snapshot·projection
             │    ├─ 경로 루트 제한·비밀 제외·MIME/크기 검사
             │    ├─ 파일별 Markdown/MSC/텍스트/PDF/이미지 renderer
             │    └─ 업무망 인증/권한 하의 단일 URL 트리 탐색
             └─ 기존 Updater 후보→그룹 baseline 대조/Preview→승인/CAS
                   →기존 l1sw-dev-knowledge writer→readback/revision
                   →원 Work 역링크
```

- **영역 1: Workspace 원본.** Kernel Ledger, Work별 변경·결정·Evidence·MSC·원문 MD·원본 SHA와 Writer 유지. 브라우저나 웹 프로세스는 수정 권한 없음.
- **영역 2: Viewer.** 읽기 전용 표시/검색/캐시/격리 사본은 교체·재생성 가능하며 원본 정본이 아님. 원본 root 전체를 미검증 HTTP 서버 document root에 직접 연결하지 않음.
- **영역 3: 그룹 Knowledge.** 검증된 HLD·상세 설계·AS-IS MSC·재사용 이슈 등은 기존 `l1sw-dev-knowledge`의 승인된 writer에만 게시. Viewer URL 공개를 그룹 지식 게시 또는 검증으로 오해 금지.
- 기존 스킬 우선순위: **REUSE → CONNECT → 실제 미지원이 입증된 최소 GAP만 EXTEND**. 신규 DB, RAG 엔진, 사이트 생성기, 양방향 동기화, 새로운 Work schema·승인 스키마를 선제 도입하지 말 것.

## 4. 웹 UX·파일 형식·링크/검색 요구

| 화면/형식 | 필수 동작 | 유의사항 |
|---|---|---|
| 단일 업무망 진입 URL | 루트 폴더 탐색→Work ID/폴더→파일; 검색, 최근 갱신·원본 revision 표시 | 도메인/URL/포트는 G0·네트워크 승인 후 확정 |
| Markdown `.md` | 선택 시 HTML 렌더(표·한글·코드블록·링크·원문 보기) | XSS sanitization, 상대 경로 정규화, UTF-8 |
| B형 MSC `.html` + `.svg` | 단계 이동·확대·스크롤 등 기존 인터랙션 유지 | 격리 origin/iframe sandbox/엄격 CSP 및 asset 동작 실증 |
| JSON·TXT·CSV·YAML 등 | 안전한 코드/테이블·텍스트 뷰어 | 크기·라인·MIME·escape/다운로드 제한 |
| PDF·이미지 | 안전한 브라우저/기존 뷰어로 미리보기 | 위험한 포함 리소스·외부 fetch 차단 |
| 바이너리/대용량/미지원 | 통제된 다운로드 또는 미리보기 불가 안내 | 무조건 inline 실행 금지; 크기·쿼터·timeout |
| Work 안내 및 상세 MD | `MSC_VIEW.md`의 `published_path`→HTML **및** Converter 상세 원본 MD→HTML 상대 링크 각각 확인 | 이전 BROKEN 링크는 viewer 매핑으로만 최소 보정 또는 개별 링크 HOLD. 원본 MD/Evidence 임의 수정 금지 |
| 신규·변경 문서 | 새 Work/파일 자동 발견, 캐시·검색 색인 갱신, 원문/렌더 최신 revision 일치 | 전량 사전 HTML 재생성 강제 없음; 인덱스에도 인증·보호 적용 |
| 장애 시 | 부분 파일 실패가 전체 Work/원본 훼손으로 확대되지 않음 | 마지막 정상 snapshot 복귀/알림, 장애 중 Git·Group 변경 0 |

**실제 UI 검토 포인트:** 폴더 트리/Work ID/Module→Feature→Scenario와 Procedure 교차 탐색, Work 개요→설계·결정→Evidence/MSC→시험·그룹 게시 revision, 직접 URL 복사, 여러 동료 열람, Markdown과 MSC 가독성. 고급 검색 기능의 존재는 G0에서 확인하고, 없으면 구현 요구 확정 전 최소 대안을 제안할 것.

## 5. 접근·보안·공유 경계(필수 차단 조건)

1. 업무망의 인증된 사용자에게 **업무 Workspace 콘텐츠 전체**를 열람하는 UX를 목표로 한다. r0001의 Work별 선택 allowlist/공유 요청 프로세스를 기본 필수 조건으로 복원하지 말 것. 다만 조직 정책에 따라 제한해야 하는 자료는 G0에서 구별·차단하며, 권한이 불명확하면 **공유 HOLD**.
2. `.git/`, `.ssh/`, `.env`, 토큰·키·credential cache·세션·DB 인증정보, OS 경로, 백업/임시 작업·제한 자료와 문서 본문에 포함된 비밀이 검색·파일·asset·원문 보기·다운로드·브라우저 캐시에 드러나지 않아야 함.
3. 정규화된 루트 containment와 **fail-closed**: `../`, URL 인코딩·이중 인코딩, 절대경로, symlink/hardlink, 숨김 파일, Unicode NFC/NFD·casefold, 특수 파일·상대 asset·redirect·`file:`/`data:`/`javascript:` 우회 경로 전부 차단/격리.
4. HTML/SVG의 inline script·iframe·외부 CDN·외부 이미지·네트워크 fetch를 검사. 필요한 MSC JS도 **원본 서버의 인증 쿠키/토큰과 분리된 origin**, sandbox, CSP 하에서만 허용하고 브라우저 부정시험이 실패하면 열람 보류. Markdown의 HTML injection도 무해화.
5. 기존 승인된 인증/SSO·VPN/VLAN·HTTPS·방화벽·감사·read-only identity를 우선 활용. 실제 host/포트·운영 계정·권한은 G0 확인 전 발명·개방 금지.
6. 원본 직접 mount가 허용되지 않거나 권한 필터를 보장할 수 없으면 **검증된 READ_ONLY snapshot/staging** 선택. snapshot writer도 원본 Work writer가 아니며 원본에 역쓰기하지 않는다.
7. 사용자 PC 전원·슬립·네트워크 단절 시 동료 URL 가용성은 보장되지 않음. 상시 가용성이 필요하면 **별도 승인된** 공용 읽기전용 사본 호스트 검토. 자동 미러·전송 또는 새 운영 서비스 설치를 지금 시작하지 말 것.
8. `python -m http.server` 등 검증되지 않은 임시 파일 서버를 업무 콘텐츠 전체 공개용 운영 서버로 사용하지 말 것.

**즉시 STOP:** 시스템/업무 비밀 노출, root 이탈, 무인증 인터넷 접근, 웹 API 쓰기 가능, HTML active content 격리 실패, 원본 SHA 변경, 기존 writer/Knowledge 쓰기 의심 또는 유효 네트워크 승인 없음.

## 6. 구현 후보와 선택 기준 — G0 전에는 확정하지 않음

| 후보 | 적용 조건 | 장점 | 차단 위험 |
|---|---|---|---|
| A. 기존 승인된 웹 서비스의 **읽기 전용 디렉터리/파일 핸들러 연결** | 실호스트에서 root containment, denylist, 인증, on-demand 렌더, 격리 origin 지원 검증 | 기존 서비스/renderer 재사용·구성 최소 | 원본 root 과노출·쓰기 API·HTML/쿠키 위험이면 불가 |
| B. **격리 READ_ONLY snapshot → 기존 웹 서비스** | 직접 mount 안전성을 입증할 수 없거나 원본 접근과 공개 범위를 분리해야 할 때 | 비밀 검사·원자적 발행·롤백 쉬움 | 파일 수·증분·검색 갱신·성능과 보관 주기 확인 필요 |
| C. 승인된 상시 호스트에 **읽기 전용 복제 뷰어** | 동료 상시 가용성 필요, 조직 네트워크·보안·운영 승인이 있을 때만 | 개인 PC 중단과 분리 | 업무 자료 이동/보존·접근 정책·소유권 재검증 |
| D. **로컬 authority로 Work 원본 전환** | **이 뷰어 작업의 즉시 범위 아님**. G5 독립 승인, 단일 writer·백업 복원·기존 Git 호환·코드 리뷰 필요 | 원격 필수 게시 완화 가능 | 이중 writer/이력·복구 손상; 절대 뷰어 성공으로 자동 실행 금지 |

최초 판단 순서: 기존 OpenCode Web/승인 서비스 등 기능 확인 → **A가 안전하면 A**, 위험하면 **B**, 기존 서비스로도 실현 불가함이 입증된 때만 최소 기능 보완 제안. 새 서버 구축을 기본안으로 정하지 말 것.

## 7. 업무 GPT 첫 작업: **읽기 전용 G0 조사 A~S (19항목)**

**지시:** 실제 Linux 설치 스킬/웹 호스트/설정·권한의 **기존 근거만 읽고** 수치와 판정 보고. 기존 A~P 응답·증거가 있으면 재조사하지 않고 필요한 미확인만 채운다. `1=설치본/원문으로 확인`, `2=근거로 미충족/미지원`, `3=미확인·접근 불가`, `4=부분 지원·조건부`. 미확인을 2나 1로 채우지 말 것.

| ID | 실제 점검 질문 |
|---|---|
| A | 설치된 Kernel의 non-Git 로컬 문서 export 기능·원본 보존 계약은? |
| B | 설치된 Workflow `docs_sync`의 registered `work_docs`/origin·clean-tree 의존은? |
| C | `docs_push` commit/push/원격 readback 의존·기존 분리 모드는? |
| D | 실제 `work_docs` root/host/role, Work ID·Ledger 출처·source revision을 확인 가능한가? |
| E | Git/Work history·single writer 보호, 오프호스트 백업과 **복구 시험** 증거는? |
| F | 개인 `knowledge/`의 Updater 단독 WRITE/Workflow READ_ONLY가 실제 강제되는가? |
| G | Updater 직접 분석/Workflow 분석이 같은 Work·Evidence를 기록·재사용하는가? |
| H | 그룹 writer의 Preview→승인→CAS/readback→원 Work 역링크는 실지원되는가? |
| I | Work-root `MSC_VIEW.md`→`published_path` HTML 링크는 정상인가? |
| J | Converter 상세 MD 내부 상대 HTML 링크·asset은 정상인가? (I와 별개) |
| K | **수정**: 기존 승인 서비스가 **전체 업무 root 탐색**, Markdown 동적 렌더, HTML/SVG/JSON/PDF 등을 읽기 전용으로 제공 가능한가? |
| L | **수정**: 개인 localhost 및 기존 인증 경계의 현 상태는? |
| M | **수정**: 업무망 동료가 단일 URL로 전체 업무 트리를 읽는 데 필요한 승인/SSO·TLS·접속·감사 수단은? |
| N | **수정**: 원본 read-only mount(A)와 안전한 격리 snapshot(B) 중 어떤 방식이 실제 보안 요구에 적합한가? |
| O | **수정**: Work별 allowlist가 아니라 **root containment·비밀 denylist·숨김/링크/identity 권한**이 보장되는가? |
| P | 기존 Writer/Skill/서비스 변경 없이 비민감 synthetic 호스트 시험을 제안할 수 있는가? |
| Q | Markdown 실시간 렌더, B형 MSC 인터랙티브 HTML, JSON/PDF/이미지 핸들러의 구체 지원 조건은? |
| R | 신규·변경 파일 자동 발견, 검색 색인·캐시 갱신, revision 일치 방식은? |
| S | 동료 2계정의 읽기 범위·동시 접근, PC 꺼짐/재시작/주소 변경 시 가용성 요건은? |

**주의:** 과거 r0001 G0의 K/N/O를 그대로 “정적 MD만 제공/선택 파일 공개/Work별 allowlist”로 판정하지 말 것. 위 최신 r0002 질문이 우선. **응답은 A~S 순서 19개 숫자 + 근거 종류/미확인/차단 사유**. 호스트 실경로·내부 주소·실제 코드·문서/로그·인증정보는 업무 환경 로컬 Evidence로만 유지하고 PUBLIC/CoWork로 전송하지 말 것.

## 8. 단계별 진행 / Gate / 허용 범위

| 단계 | 구체 결과물 | 진입·승인 조건 | 실패 처리 |
|---|---|---|---|
| **P0/G0** 현장 읽기 전용 확인 | A~S 상태, 설치버전/owner/기존 서비스/파일 유형·개수·백업/네트워크·보안 제약(비민감 요약) | 기존 권한 내 읽기 전용 조회만. **지금 업무 GPT에게 요청할 1차 작업** | 근거 없으면 NOT_VERIFIED; 구현·서비스 실행 보류 |
| **P1/G1** 합성 export·형식별 렌더 후보 | 완전히 격리된 synthetic 문서·원본 해시/멱등성·새 문서 발견·읽기만 시험 및 렌더 설계 | G0로 기능 확인 + 합성 시험 실행이 허용된 범위 확인. 운영 원본 수정 금지 | 실패 시 viewer 후보만 수정; Git/Work 불변 |
| **P2/G2** 보안/링크 검증 | traversal·secret·MIME/HTML/SVG/CSP, Work-root와 상세 MD **두 링크**, 검색/캐시 부정시험 | 충분한 보안 테스트 환경. 업무 원본 무변조 | 노출·XSS/경계 탈출·깨진 링크면 해당 공개 HOLD |
| **P3/G3** 개인 localhost viewer | URL·문서 트리/renderer/읽기전용/롤백의 실제 브라우저 E3 | 별도 Linux **프로세스/서비스·설정 실행 승인** 및 G0/G2 결과 | 개인 뷰어 OFF, 기존 Git/원본 유지 |
| **P4/G4** 동료 업무망 viewer | 2계정 전체 업무 콘텐츠 탐색, 인증/네트워크/동시 접근·안전성 | 별도 **업무 네트워크 공유 및 보안/운영 승인**, G3+G2 실증 | 공유 HOLD; 개인 시험 결과와 원본 불변 |
| **P5/G5** local authority 전환 | 기존 Git 원격·Writer 전환 가능성, 백업 복구·이중 writer 방지·코드 독립 리뷰 | **별개의 사용자 명시 승인**. 이번 인계에서 **착수 금지** | 기존 Git remote/Workflow 그대로 |
| **P6/G6** 그룹 Knowledge 게시 | 기존 Updater 승인된 Preview/CAS/readback/원 Work 역링크 | 별도의 지식 게시 승인·실제 설치 계약 | 그룹 재게시 금지, Work/Evidence 보존 |

**Gate 정의:** PASS=실제 실행과 재현 가능한 Evidence, FAIL=검증된 결함, SKIP=범위 불해당, NOT_RUN=미실행. `G0 설치 사실`/`G1 설계 가정`/`합성 자체시험`/`Linux E3`/`독립 리뷰`는 서로 대체 불가. 별도 승인 전에는 신규 서비스·패키지 설치, 포트/방화벽/OS 권한 변경, Git push/pull/reset·원본 쓰기, DB/Job·자동화, 유료 리뷰·모델 호출, 그룹 Knowledge 변경을 시작하지 말 것.

## 9. 상세 수락·부정시험 목록 (기존 T01~T26 + r0002 T27~T34)

시험 아래의 **기대**는 검증 계획이며 PASS 이력 아님. 이미 수행된 합성 T01/T02와 관련 pytest의 확인 범위만 2절에 기록.

| ID | 시험 시나리오·기대 |
|---|---|
| T01 | 비Git 격리 폴더 synthetic Work export/파일·index 정상 |
| T02 | 재export byte/SHA 일치·멱등 |
| T03 | Legacy TL_REVIEW가 공유 export에서 차단됨 |
| T04 | 수동 편집 Work 안내 문서 덮어쓰기 없음 |
| T05 | 두 writer 동시 접근의 lock/revision·stale 차단 |
| T06 | dirty tree/소스 SHA 변경 시 구버전 근거 최신화 금지 |
| T07 | Work-root `MSC_VIEW.md` → 게시 HTML 경로/해시 |
| T08 | Converter **상세 MD** → 상대 HTML 링크; BROKEN이면 안전한 매핑/HOLD |
| T09 | `../`/인코딩/절대 URL root traversal 차단 |
| T10 | symlink/hardlink/hidden/Knowledge alias 외부 접근 차단 |
| T11 | 비인가 사용자/보호 파일·지원 불가 형식 403/404 또는 안내 |
| T12 | 토큰/비밀/제한 로그/고객자료 본문·검색·캐시 누출 없음 |
| T13 | HTML/SVG JS·iframe·외부 fetch 격리/CSP 동작 |
| T14 | 승인된 계정/비승인 계정의 직접 URL·검색 접근 통제 |
| T15 | index/브라우저 cache/ETag로 타 권한 내용 노출 없음 |
| T16 | Unicode NFC/NFD·casefold·경로 충돌 fail-closed |
| T17 | 긴 MSC participant/asset·확대·스크롤·문서 가독성 |
| T18 | 1000+ Work / 대용량 Evidence 시 누락·잘림 탐지 |
| T19 | staging/프로세스 중단 시 부분 파일 미노출, 마지막 정상본 |
| T20 | viewer 장애·재부팅에도 Work/Group 원본 불변 |
| T21 | Git dirty/diverged/untracked 복구 가능·auto-reset/rebase 금지 |
| T22 | 오프호스트 복원 실패 시 local authority cutover 금지 |
| T23 | Group CAS 충돌 시 overwrite 금지·Preview 재대조 |
| T24 | Group 게시 성공 + Work 역링크 실패 시 **재게시 금지**, 링크만 복구 |
| T25 | Group write 불확실/중복 응답 시 영수증/readback 우선 |
| T26 | rollback 시 local-only 신규 이력 무손실 보존·대조 |
| **T27** | **전체 Workspace tree**·새 Work 발견·검색 자동 갱신, 원본 0변경 |
| **T28** | **Markdown** 즉석 렌더/Raw, 한글·표·상대링크, XSS 무해화 |
| **T29** | **기존 B형 MSC HTML/JS/SVG** sandbox/origin/CSP, 확대·단계이동 유지, 쿠키/토큰 접근 불가 |
| **T30** | **JSON/TXT/이미지/PDF/바이너리** 형식별 preview 또는 안전한 fallback/크기 제한 |
| **T31** | **root 이탈/비밀 경로** 이중 인코딩·symlink·absolute·hidden·casefold 모두 거부 |
| **T32** | **업무망 2계정** 전체 업무 콘텐츠 보기·검색/직접 URL 일치, 쓰기·삭제·rename 불가 |
| **T33** | **업무 PC offline/재시작/주소 변동** 시 안내·재접속, Work/Group 불변 |
| **T34** | **전량 HTML 사전 변환 없이** on-demand vs 증분 캐시의 지연/메모리/색인·갱신 비용 비교 |

각 테스트는 `PASS/FAIL/SKIP/NOT_RUN`, 실행 환경, 검증 근거 식별자, 원본 SHA 변화 여부를 개별 기록. 계획을 제시한 것만으로 T27~T34 PASS 금지.

## 10. 업무 GPT에 요청하는 실제 리뷰·판정 항목

업무 GPT는 다음 질문에 **근거 수준을 표시해 조건부 판정**할 것:

1. r0002 사용자 요구가 r0001의 Work별 선택 공개 의존성을 모두 제거하면서도 조직 보안/원본 분리 요구를 충족하는가?
2. `A: 안전한 기존 서비스 mount` vs `B: 격리 snapshot` 중 무엇이 **실제 G0**에서 지지되는가? 미확인 기능/API·설정·URL을 가짜로 쓰지 않았는가?
3. Markdown·MSC·JSON/PDF·검색·신규 파일 발견/권한·캐시와 상대 링크가 기존 승인된 도구로 가능한가? 미지원이 **실증**된 경우에만 확장 후보를 제안했는가?
4. B형 MSC의 작동성과 XSS/CSP/iframe/외부 fetch·검색 색인의 비밀 보호가 함께 만족되는가?
5. 기존 Workflow `docs_sync/docs_push` Git 의존성과 Kernel export를 정확히 분리해 **Viewer는 Writer를 바꾸지 않는가**?
6. Updater의 직접 분석/Workflow의 Work 진입과 개인 `knowledge/` Writer, 그룹 Knowledge 승인·CAS/readback·역링크를 유지하는가?
7. Linux 호스트·데이터 분류·동료 공유 정책이 불명확할 때 **fail-closed**와 필요한 승인만 제시하는가?
8. 남은 위험을 차단(Blocker)/후속 권고/선택 옵션으로 분리하고, 요구사항의 범위 확대·추가 유료 독립 리뷰를 기본 요청하지 않는가?

**GPT 판단 기록:** 항목별 `수용 / 수정수용 / 보류 / 추가확인 / 거절`, 근거·보완안·완료 판정 기준. 통합 상태는 `DESIGN_ACCEPT_WITH_GATES` 또는 `DESIGN_HOLD` 중 실제 근거로 선택. 부족한 근거는 BLOCKED/NOT_VERIFIED로 분리하고, 그 이유로 새 스킬이나 구조를 임의 확정하지 말 것.

## 11. 보고 형식과 데이터 이동 제한

업무 GPT가 현재 즉시 회수할 보고서는 아래 틀로 충분하되 **A~S 전체를 실제 근거로 채우고 상세 위험/반례 판정을 별도 부록으로 작성**. 출력 범위는 허용된 비민감 상태·분류/숫자/결론만. 실제 원본/상세 MSC·로그·코드·보안 파일·주소·토큰·호스트/개인 식별자·내부 URL·자격정보를 PRIVATE/PUBLIC GitHub 또는 대화에 옮기지 말 것.

```text
WORK_ID: L1-WORKSPACE-RAG-20261111-001
BASELINE: r0002 latest / r0001 history preserved
INDEPENDENT_REVIEW: NOT_RUN (USER_WAIVED_THIS_HANDOFF)
GPT_DESIGN_DISPOSITION: ACCEPT_WITH_GATES | HOLD | NEED_EVIDENCE
HOST_G0_A_TO_S: A=... B=... ... S=...  (1/2/3/4)
EVIDENCE_LEVEL: ACTUAL_INSTALLED | SOURCE_READ | CANDIDATE_ONLY | USER_REPORT | UNKNOWN
EXISTING_VIEWER: REUSE_AVAILABLE | PARTIAL | NOT_VERIFIED | UNSUITABLE
A_VS_B: A | B | HOLD ; reasons and measured constraints
DOC_LINKS: WORK_ROOT=... / CONVERTER_DETAIL=... (separate)
SECURITY: ROOT_CONTAINMENT=... ; SECRET_DENY=... ; HTML_ISOLATION=... ; AUTH=...
GATES: G0=... G1=... G2=... G3=... G4=... G5=... G6=...
TESTS: PASS=# FAIL=# SKIP=# NOT_RUN=# ; evidence IDs
SOURCE_MUTATION: NONE_VERIFIED | UNKNOWN | CHANGED
SKILL_CHANGES: NONE | MINIMUM_GAP_PROPOSAL_ONLY
LINUX_OPERATING_CHANGES: NOT_RUN
GROUP_WRITE: NOT_RUN
BLOCKERS_AND_REQUIRED_APPROVALS: ...
LOCAL_EVIDENCE_IDS: ... (no sensitive source content)
NEXT_ONE_ACTION: 정확히 1개
```

- **문서·비민감 상태 결과**는 기존 Work에 연결. 회사 업무 원본/정밀 로그/MSC는 업무 Linux의 허용된 Work/Evidence로 보존.
- 기존 리뷰 요청 `REQ-L1-WORKSPACE-LOCAL-VIEWER-DESIGN-R1-20261118` 관련 REQUEST/READY/watchers/유료 실행을 생성·재큐잉하지 않음. 이전 예산 USD 1.50 승인을 이번 업무 GPT 단계의 유료 모델 실행/보안 설정 변경 승인으로 확대하지 않음.
- 리뷰 생략 사실은 명시적으로 유지: `INDEPENDENT_REVIEW=NOT_RUN`. 이 문서에서의 GPT 검토는 독립 코드 리뷰·호스트 E3·보안 운영 인증을 대체하지 않는다.
- **다음 한 동작:** 업무 GPT가 이 문서의 **r0002 정적 상세 검토 + 읽기 전용 G0 A~S**를 기존 설치 근거로 수행하고, 차단 항목·가장 작은 후속 시험/승인 범위를 한 번에 판정. Linux 서비스 기동·네트워크 공유·writer 전환·Group Knowledge 게시 등은 이후 별도 승인 전까지 수행하지 않는다.

## 12. 참고 정본 경로(접근 가능한 경우에만 조회; 이 문서 단독으로도 1차 검토 가능)

- CoWork PRIVATE `main`: `collab/CONTEXT_BRIEF.md`
- 같은 Work `CURRENT.md` (상태·승인·중복·최신 결과 원장)
- 같은 Work `L1_WORKSPACE_LOCAL_FIRST_WEB_VIEWER_SAFE_TRANSITION_DESIGN_r0001_20261118_KST.md` (보존한 이전 설계·T01~T26)
- 같은 Work `L1_WORKSPACE_FULL_TREE_WEB_RENDER_VIEWER_DESIGN_DELTA_r0002_20261118_KST.md` (**최신 요구 우선**, T27~T34)
- 같은 Work `L1_WORKSPACE_LOCAL_VIEWER_LINUX_PROPOSAL_AND_WORK_ORDER_DRAFT_r0001_20261118_KST.md` (과거 초안·이 문서로 업데이트)
- L1Work PUBLIC `handoffs/L1_WORKSPACE_LOCAL_VIEWER_SAFE_STOP_HANDOFF_r0001_20261118_KST.md` (이전 안전 중지 이력)
- L1Work PUBLIC `handoffs/L1_WORKSPACE_LOCAL_WEB_VIEWER_LINUX_G0_READONLY_HANDOFF_r0001_20261118_KST.md` (이전 A~P 질문·r0002 A~S가 우선)

**이 상세 인계는 운영 배포·설치 명령이 아니라 사용자가 선택한 ‘Claude 리뷰 없이 업무 GPT로 직접 설계 검토’의 정본 작업 자료다.**
