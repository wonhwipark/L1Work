# 업무 GPT 통합 인계 r0002 — Viewer v0.5.2 + Updater 직접 분석 MSC HTML 연결 진단·보완

- 개정: 2026-11-24 KST / 기존 CoWork Work `L1-WORKSPACE-RAG-20261111-001` 재사용
- **입력 저장소/브랜치**: `wonhwipark/L1Work` / `main`
- **이번 단일 인계 파일**: `handoffs/L1_WORKSPACE_VIEWER_V052_MSC_UPDATER_CONVERTER_COMPLETE_HANDOFF_r0002_20261124_KST.md`
- **기존 Viewer 전체 소스 ZIP(변경 없음)**: 루트 `l1-workspace-viewer-wiki-integrated_v0_5_2_1124.zip` / 374,930 bytes / SHA-256 `15e83f136fa10ef680619602b55d74c4cd4c0c86a6cc470c1bec9cac250239ba` / Git blob `6dc79e44dbb209a6cf2b437fcd0672649a772a10`
- **참조할 기존 Updater 연결 인계**: `handoffs/L1_KNOWLEDGE_UPDATER_NR_UL_TX_SWITCHING_MODIFICATION_REQUIREMENTS_r0002_20261121_KST.md`, `handoffs/L1_KNOWLEDGE_UPDATER_NIGHTLY_MODULE_PROCEDURE_MSC_HANDOFF_r0001_20261123_KST.md`
- 목적: 사용자가 실제 Viewer에서 **PlantUML 원문만 보고 MSC HTML 링크는 보지 못한 현상**의 소유 단계 판정 후, 확인된 범위에서 최소 연결·시험
- **기술 상태**: 위 현상은 사용자 관찰. 실제 `l1-knowledge-updater → doc-converter` 호출 여부, HTML/SVG 생성 여부, Work writer/Viewer 연결 여부 모두 **UNKNOWN / 업무 Linux G0 미검증**. ZIP 전달 자체는 호스트 적용 완료가 아님.
- 실행 경계: `development_not_for_deployment`. 업무 제품 코드·로그·상세 MSC는 원래 업무 Work에만 저장. 이 공개 HO에 붙이지 않음. 설치/서비스 재시작/새 Job·자동 예약/새 유료 모델 호출/Write ON/그룹 지식 게시에는 기존 유효 승인 또는 별도 승인 필요.

## 0. 가장 먼저 확인할 결손 — Converter 실제 호출 증거

사용자가 Viewer에서 PlantUML 소스만 봤다는 이유로 Converter가 실행됐거나 실패했다고 **둘 다 단정하지 말 것**. 코드 Analyzer가 직접 PUML을 남겼을 수도 있고, Converter가 HTML을 만들었지만 저장 또는 링크가 누락됐을 수도 있음.

1. **실제 설치본과 기존 결과 조사(G0, 읽기 전용)**: 업무 Linux의 `l1-knowledge-updater`, `code-analyzer`, `doc-converter`, `work-ledger-kernel`, Workspace writer, Viewer read adapter의 실제 버전·source revision·파일 위치·실제 지원 action/입출력 계약을 확인. 공개 `doc-converter_v0_2_26_1117.zip`은 참고용이며 설치본 동일성 가정 금지.
2. **재실행 전에 기존 결과 확인**: 문제를 본 정확한 Work ID·문서·원본 revision·분석 Run/Job ID·기존 분석 결과·로그/영수증·`.puml` 존재 위치를 찾는다. 실행 이력·영수증이 없으면 `CONVERTER_INVOKED=UNKNOWN`으로 보고. `.puml` 파일 존재만으로 호출 PASS 금지.
3. **Converter 실제 사용 확인**: 동일 실행 ID에서 호출 주체, 허용된 action/명령, converter version, 입력 canonical Scenario IR/source revision, 호출 시각/상태 및 성공·실패 영수증을 연결. 콜 체인이 없으면 Updater의 호출/연동 gap으로 분류. 기존 지원 API 미확인 시 임의 호출 생성·게이트 무단 해제 금지.
4. **변환 산출물 존재/형식 확인**: PUML 원문 외에 HTML 또는 SVG가 실제 생성되었는지, 출력 위치·manifest·source/parent/variant·상대 경로·내용 무결성을 확인. `doc-converter`의 native Scenario IR·`SOURCE_PARENT_DIR_V1`·`stack_group`·participant alias를 유지. 출력이 PUML만인 경우 converter 실행 옵션·입력 호환성·실패 증거를 먼저 판정.
5. **Workspace 저장/등록/재조회 확인**: HTML/SVG가 있다면 동일 Work의 승인된 기존 writer/Kernel 경로로 artifact/Evidence와 정확히 연결됐는지, 실제 file bytes·Work revision/readback을 확인. Updater는 직접 분석 후에도 이 공통 writer를 사용해야 하며 전체 `l1-fix-workflow` 실행을 강제하지 않음.
6. **Viewer 표시 확인**: Work의 실제 read model이 HTML/SVG artifact와 권한 검증된 링크/docId를 전달하는지 확인. 링크가 있어도 Viewer 미표시라면 실제 Viewer adapter/render/UI를 수정. 없을 때는 링크·그림이 있다고 꾸미지 않고 `HTML_NOT_AVAILABLE`/미확인 안내 및 PUML 원문을 유지.

### 단계별 책임 판정

| 확인된 결과 | 책임 후보 | 우선 조치 |
|---|---|---|
| Updater 결과만 있고 Converter 호출 이력 없음 | `l1-knowledge-updater` 호출 연결 | 기존 Analyzer/Converter 지원 인터페이스를 연결. 실제 gap 확인 전 신규 API·중복 변환기 작성 금지 |
| Converter 호출 확인, HTML/SVG 산출 없음 | Updater 입력 IR / `doc-converter` 변환 경계 | native IR 호환·검증/옵션/실패 원인 대조. Converter 자체 결함이 입증될 때만 최소 수정 |
| HTML/SVG 생성은 확인, 개인 Work에 파일·Evidence 링크 없음 | Updater → 기존 Workspace writer/Kernel | 원래 Work에 artifact 경로·source revision·근거 등록하고 revision/readback |
| Work에 파일과 링크 있음, Viewer에 PUML만 표시 | Viewer 실제 읽기 adapter / 표시 UI | 실제 저장 경로와 허용 docId/HTML render 경로 매핑, Read Only 권한·CSP·sandbox 검증 |
| HTML이 없는 과거 Work | 변환·재등록 여부 추가 판정 | 근거가 유효한 기존 결과부터 재사용; 분석/Job 재실행 없이 가능한 변환/링크 복원, 불가하면 BLOCKED |
| 증거/권한 없음 | 미확인/차단 | UNKNOWN/BLOCKED와 필요한 근거를 명시; 빈 결과를 PASS로 표시하지 않음 |

## 1. 목표 화면/산출물 계약

사용자가 `NR L1 Tx → UL Tx Switching`과 같은 분석 Work를 열면, 같은 Work 문서의 MSC 섹션에서 **(a) 근거 있는 AS-IS MSC HTML 보기, (b) SVG 가능 시 그림 보기/확대, (c) PlantUML 원문, (d) 분석 근거·source revision**을 분리하여 연결한다. 실제 존재·권한 확인된 산출물만 링크 노출. 파일명·디렉터리·docId·URL은 호스트 G0 결과를 우선하며 이 문서만 보고 고정하지 않는다.

```text
l1-knowledge-updater [직접 분석 진입, 또는 기존 Workflow 결과 재사용]
    └─ code-analyzer / 기존 CODE FACT (근거·source revision 고정)
        └─ doc-converter (실제 지원 IR·호출 증거 있을 때 HTML/SVG)
            └─ 기존 writer + work-ledger-kernel (같은 Work의 artifact/Evidence 연결·readback)
                └─ 실제 Viewer read adapter (권한·Work 경계 검증)
                    └─ [MSC HTML 보기] [SVG 보기] [PlantUML 원문] (실재하는 출력만)
```

기존 스킬 또는 데이터에 이미 HTML/SVG가 있으면 **코드 분석·LLM/Job을 재실행하지 않는다**. 누락된 연결만 복구한다. `work-ledger-kernel`을 공통 기록/검증 경로로 쓰되 Converter를 직접 호출하는 주체는 분석을 조정하는 Updater/기존 Analyzer 계약과 대조하여 확정한다. 그룹 `l1sw-dev-knowledge` 자동 게시와 개인 Workspace 업데이트를 혼동하지 않는다.

## 2. 업무 GPT 원샷 통합 실행 지시

이 **r0002 HO + 기존 Viewer v0.5.2 ZIP 하나만** Viewer 구현 입력으로 사용. 아래는 사용자가 보고한 실제 MSC 문제를 조사하는 추가 계약이며, 이전 r0001의 UI/Write/도우미 안전 계약·시험 A01~A10/H01~H05 전체를 그대로 승계한다.

- 먼저 대표 기존 Work 한 건에서 `Updater → Converter` **실제 호출 영수증 → HTML/SVG 산출물 → Work artifact/Evidence 등록 → Viewer read/링크 노출**을 각각 추적.
- 이미 확인된 파일·해시·원본 근거·권한을 재사용하고, 입증된 연결 결손이 있으면 해당 스킬 또는 View adapter에만 최소 패치를 적용. 업무 Linux 설치본 실제 action/경로를 확인하기 전 구현용 API·schema·파일명·새 writer를 추정하지 않는다.
- 기존 v0.5.2 Viewer ZIP에는 합성 `WikiAdapter`만 있으며 업무 HTML artifact reader 실연동이 없음. 브라우저에서 `<iframe>`을 임의로 직접 열거나 원본 파일시스템 경로 노출, 임의 URL 프록시, JS 실행/unsafe HTML 삽입은 하지 않는다. 기존 승인된 same-origin/전용 보호 렌더 경로와 세션/ACL/CSP/sandbox 검증을 우선.
- 개발물·새 ZIP은 실제 변경 스킬만 별도 버전/manifest/SHA를 만들고 필요한 검증을 수행; **Viewer 수정이 필요 없으면 Viewer ZIP 버전을 올리지 않는다.** 승인 범위 내 개발·시험만 수행하고, 운영 설치·모델/Job 실행·보안 경계 확대는 별도 게이트를 지킨다.
- **수락 시험**: T1 Converter 미호출 시 거짓 호출 PASS 금지; T2 호출 성공+HTML 존재는 manifest/SHA로 확인; T3 HTML→Work artifact/Evidence/readback; T4 Work 링크→Viewer 클릭→HTML 시퀀스 다이어그램 실제 화면 렌더(모바일/데스크톱); T5 권한 없는 Work/경로 이탈/악성 HTML·CSP 차단; T6 기존 PUML 원문/근거 링크 정상; T7 Updater 직접 분석과 Workflow 재사용 두 진입에서 동일 Work 경로; T8 기존 Viewer Node/브라우저·Write 안전 회귀.
- 수락 기준은 **실제 업무 Work 하나에서 HTML 그림 열람 + source/Work revision·근거 일치 + 권한 검증**까지. 문서/ZIP 정적 시험 또는 합성 HTML 표시만으로 통합 PASS 판정 금지.

### 최종 반환 표 (모두 필수, 상태 PASS/FAIL/SKIP/NOT_RUN/BLOCKED/UNKNOWN 구분)

| 필드 | 회신 내용 |
|---|---|
| `WORK_ID / SOURCE_REV / RUN_RECEIPT` | 기존 Work·실제 분석 실행 ID/영수증·코드 revision. 없으면 UNKNOWN |
| `CONVERTER_INVOKED` | 호출 증거(action/입력 IR/시각·출력 영수증) 또는 미호출·미확인 사유 |
| `CONVERTER_HTML_SVG` | 실제 HTML/SVG 파일 위치·manifest/SHA/실패 원인 |
| `WORKSPACE_ARTIFACT_READBACK` | 동일 Work artifact·Evidence 등록·revision/내용 readback |
| `VIEWER_HTML_LINK / BROWSER_E2E` | 링크 매핑/권한 검증·실제 화면 렌더 근거 |
| `CODE_CHANGE / REGRESSION` | 변경한 정확한 파일·스킬 버전/ZIP SHA·시험 결과. 변경 없으면 NO_CHANGE |
| `HOST_DEPLOY / INDEPENDENT_REVIEW` | 운영 설치·독립 리뷰 수행 사실(기본 NOT_RUN)과 승인·미검증 |
| `NEXT_ONE_ACTION` | 남은 가장 작은 연결 결손과 한 행동 |

상세 업무 코드·호스트 경로·MSC 내용은 업무 Work에만 보존. 공개 저장소에는 비민감 상태/패키지 식별자만 기록. **인계 파일 게시 자체는 실제 업무 GPT 수신·호스트 실행·진단 PASS를 뜻하지 않는다.**

---

## 3. 기존 Viewer v0.5.2 완결 인계 원문 전량 보존

이하 내용은 기존 `handoffs/L1_WORKSPACE_VIEWER_V052_READABILITY_COMPLETE_HANDOFF_r0001_20261124_KST.md` 원문이며 기존 A01~A10/H01~H05, Write/도우미/Read Only/권한·회귀 계약을 변경하지 않는다. 이번 실행의 입력 인계 문서만 새 r0002로 변경한다.

---

# 업무 GPT 최종 단일 인계 — Viewer v0.5.2 문서 읽기/가독성 보완

- 일자: 2026-11-24 KST
- Work: `L1-WORKSPACE-RAG-20261111-001` (신규 Work 생성 없음)
- 정본: GitHub PUBLIC `wonhwipark/L1Work`, branch `main`
- **유일한 신규 입력 ZIP**: 저장소 루트 `l1-workspace-viewer-wiki-integrated_v0_5_2_1124.zip`
- ZIP SHA-256: `15e83f136fa10ef680619602b55d74c4cd4c0c86a6cc470c1bec9cac250239ba`
- ZIP bytes: **374,930**, entries: **36**, Git blob `6dc79e44dbb209a6cf2b437fcd0672649a772a10`
- standalone 데모 HTML: `handoffs/L1_Workspace_Viewer_v0_5_2_20261124_KST.html`
- 패키지 내부: `viewer-wiki-ui/INTEGRATION_READABILITY.md`, `tests/readability.cjs`
- 상태: **development_not_for_deployment**. 실제 Linux 운영 설치·브라우저 E2E·LLM/Agent·Write ON/호스트 read adapter=NOT_RUN. 독립 리뷰=NOT_RUN.
- 기존 v0.5.1 ZIP/인계의 역사는 유지하지만 업무 GPT에 이전 ZIP을 별도 전달하지 않음.

## 1. 이번 수정 — Viewer에 한정

| 파일 | 수정 |
|---|---|
| `assets/markdown.js` | `FOLLOW_UP.md` 같은 상대 링크는 adapter에 전달; `\\|`, `&#124;`, `CFG\\_REQ`, `&lt;`를 원문 의미로 표시. 비허용 링크는 plain text로 차단 |
| `adapters/adapter.js` | 동일 Work 내 상대경로를 canonical docId로 해석하는 합성 예시 `resolveDocumentLink`, Work snapshot과 테스트 데이터의 읽기 계약 |
| `assets/app.js` | Work 진행/코드 수정/시험 결과를 별도로 표시. PASS/FAIL/NOT_RUN/기록 없음 구분, 개별 시험 근거 링크·revision. 근거형 snapshot을 반환하는 이슈에서 현상→원인 수준→조치·검증→다음 행동 4칸. 전체 원문은 접어 보존 |
| `assets/viewer-integrated.css` | 글자 크기(본문/표/표제/코드/목차) 동기화, 긴 ID/경로 줄바꿈, 반응형 이슈 요약 |
| `fixtures/demo-data.js` | 합성 FOLLOW_UP.md 및 가설·미실행·근거 문서 데모 추가 |
| `tools/build_release.py`, `standalone-preview.html`, `manifest.sha256` | 버전 갱신·같은 변경 소스 미리보기 재생성·해시 명세 갱신 |
| 기타 | `VERSION=0.5.2`, `source-pin.json`, 새 호스트 인계와 회귀시험 코드 |

**수정하지 않은 스킬:** `l1-fix-workflow v1.6.75`, `work-ledger-kernel v0.7.43`. 지금은 저장된 값과 문서를 소비하는 Viewer의 읽기 경로를 먼저 개선. 실제 출력에 필수 값이 없다면 그때만 원본 생성 스킬 검토.

## 2. 시험·안전 판정

| 시험/검증 | 결과 |
|---|---|
| v0.5.1 원본 349,332B SHA 고정 | PASS (연결된 원격 ZIP 대조) |
| v0.5.2 ZIP local/central 구조, 36 entries, CRC | PASS (격리 패키저의 바이트 검사) |
| v0.5.2 manifest 및 기존 Write 3개 SHA | PASS (격리 패키저 검증) |
| Markdown 링크/표/상태의 실제 Node 회귀 | **NOT_RUN**. `node tests/readability.cjs` 포함, 업무 호스트에서 실행할 것 |
| 기존 Node 25개 회귀 | **NOT_RUN (v0.5.2 기준)**. 과거 v0.5.1 25 PASS를 재사용하지 말 것 |
| Chrome/Firefox 브라우저 및 Linux 설치본 G0 | **NOT_RUN** |
| 실제 읽기 adapter, ACL, LLM/Agent, Write | **NOT_RUN** |
| 독립 리뷰, 운영 설치/정식 통합 | **NOT_RUN** |

## 3. 업무 GPT 원샷 진행

1. `wonhwipark/L1Work/main`의 **본 인계 + v0.5.2 ZIP만** 입력으로 읽고 SHA/CRC/manifest 및 기존 Write 해시 확인. v0.5.1을 다시 설치하거나 덮어쓰지 말 것.
2. 실제 Linux Viewer의 실행 source/branch·읽기 root/adapter 모듈/API·인증/ACL과 기존 Work revision을 **G0에서 확인**. ZIP의 `WikiAdapter`는 합성 fixture이며 실제 서비스 API가 아님.
3. `INTEGRATION_READABILITY.md`에 따라 실제 read adapter에서 동일 Work·권한이 확인된 .md 문서만 상대 링크 → docId로 매핑. UI의 `getIssueSnapshot`은 실제 TL 요약/체크포인트/후속·수정·시험 기록에서 확인된 값만, 소스 revision과 함께 제공. 레거시 Work에 데이터가 없으면 원문 보기 유지.
4. 설치본과 별개 격리 환경에서 `cd viewer-wiki-ui/tests && node regression.cjs && node assistant-client.cjs && node readability.cjs`를 실행. 미성공 시험과 별개로 패키징·안전한 읽기 UI 작업은 계속하되, 회귀 미검증을 PASS로 보고하지 말 것.
5. 실제 Work 3건(수정·시험 있음/원인 가설만 있음/레거시 문서)에서 링크 이동, 5열 후속표, 실패·미실행·기록 없음, 근거 출처, 목차·원문/확대/모바일, 악성 링크 차단 확인.
6. 아래 기존 **A01~A10, H01~H05 및 Write 안전/복구 계약 전체**를 계속 검증. 백업/롤백·ACL·승인/Writer·실호출 권한 확인 이전 운영 설치, Write ON, 모델/Job 자동호출 금지.
7. 실제 근거/결과는 업무 l1-workspace Work에 기록하고 공개 저장소에는 비민감 판정·링크만 반환. 정확한 실제 adapter 파일 경로와 성공/차단 판정 포함해 보고.

## 4. 기존 v0.5.1 완결 인계 계약의 전량 보존

다음 내용은 **계약·검증 항목의 누락 방지용 역사적 원문**입니다. 아래 역사 절의 v0.5.1 ZIP/파일명/해시는 과거 기준을 뜻하며 이번 실행 입력은 **위 1~3절에 명시한 v0.5.2 하나**입니다. 기존 사용자 결정, 오늘의 업무·숨김 도우미 및 A01~A10, H01~H05, 권한/실행/영수증 계약은 그대로 승계합니다.

---

# 업무 GPT 단일 완결 인계 — L1 Workspace Viewer v0.5.1

- 2026-11-23 KST / Work: `L1-WORKSPACE-RAG-20261111-001`
- L1Work `main` 루트 **단일 신규 ZIP**: `l1-workspace-viewer-wiki-integrated_v0_5_1_1123.zip`
- **ZIP 정확한 크기: 349,332 bytes / SHA-256: `0bc0240261e29c863c541e9650e9f99271b2b924ffd52be753598889f66cf290` / 34 entries**
- 완결 인계서 경로: `handoffs/L1_WORKSPACE_VIEWER_V051_TODAY_ASSISTANT_HANDOFF_r0001_20261123_KST.md`
- 단독 미리보기: `handoffs/L1_Workspace_Viewer_v0_5_1_20261123_KST.html`
- **업무 GPT는 이 v0.5.1 인계서 + v0.5.1 ZIP만 수령**. v0.5.0 인계서와 ZIP은 별도 전달하지 않음(원격 이전 버전은 보존).
- 상태: `development_not_for_deployment`. 실제 브라우저/업무 Linux/LLM·Agent·Write/운영 적용 NOT_RUN, 독립 리뷰 사용자 생략(새 요청 없음).

## v0.5.1 추가 변경 (기존 v0.5.0 기능 전부 포함)

1. 문서 화면에서 **본문+목차를 기본 표시**, 도우미 탭/패널은 기본 숨김.
2. 상단 **업무 도우미** 버튼으로만 열기·닫기. 좁은 화면은 우측 overlay, ESC/닫기 시 접힘.
3. **오늘의 업무** 탭에서는 목록 전체폭으로 표시하고 대화 컬럼은 기본 숨김. 상단 버튼 또는 `이 업무로 대화` 버튼을 눌러 표시.
4. 닫아도 Work별 대화/초안은 메모리에 유지. 새로고침·프로필 전환 시 기존 계약대로 소멸.
5. `크게 보기`는 사용자 명시 클릭에 한해 오늘의 업무 화면에서 대화를 바로 열기.
6. 실제 LLM/Agent/Writer 연결이 없으므로 Demo 표시와 미실행 안전 경계 유지, 실제 저장/모델 호출 0.

## 업무 GPT에게 바로 전달할 지시

`wonhwipark/L1Work/main`의 `handoffs/L1_WORKSPACE_VIEWER_V051_TODAY_ASSISTANT_HANDOFF_r0001_20261123_KST.md` 및 루트 `l1-workspace-viewer-wiki-integrated_v0_5_1_1123.zip`만 입력으로 기존 `L1-WORKSPACE-RAG-20261111-001` Work를 재개. 입력 ZIP CRC/manifest/SHA 확인→실제 Viewer source/branch·auth/read/adapter G0 확인→최소 UI 이식→아래 **기존 전체 계약 A01~A10과 신규 H01~H05** 검증. 원래 Workflow/Kernel/Updater/analyzer/converter/Write를 재사용. 미확인 API·새 서버·DB·자동 실행을 만들지 말고, 실제 호스트 권한/승인 범위 내에서 진행. 운영 설치·Write ON·LLM/Agent 실행 활성화는 별도 검증·승인 전 보류.

## 검증 판정

기존 원본 ZIP SHA 일치 PASS, 전체 34엔트리 복원 PASS, 변경 코드/화면 앵커 확인 PASS, Write 원본 3파일 SHA 불변 PASS, 신규 ZIP 전 파일 해시 왕복 검사 PASS, standalone CSP inline SHA 재생성 PASS. **신규 v0.5.1 Node·브라우저 E2E·업무 Linux G0=NOT_RUN**, v0.5.0의 25 PASS를 v0.5.1 결과로 치환하지 않음.

---

## 기존 v0.5.0 인계 계약 전량 내장 (v0.5.1 파일명·검증상태에 맞춰 계승)

# 업무 GPT 인계 — Viewer v0.5.1 오늘의 업무·우측 업무 도우미

- 작성: 2026-11-23 KST
- Work: `L1-WORKSPACE-RAG-20261111-001` (기존 Work 재사용)
- 전달 저장소: GitHub PUBLIC `wonhwipark/L1Work`, branch `main`.
- 정확한 인계 상대 경로: `handoffs/L1_WORKSPACE_VIEWER_V051_TODAY_ASSISTANT_HANDOFF_r0001_20261123_KST.md`
- 입력 ZIP: 루트 `l1-workspace-viewer-wiki-integrated_v0_5_1_1123.zip`
- 입력 bytes: **349,332** / SHA-256: `0bc0240261e29c863c541e9650e9f99271b2b924ffd52be753598889f66cf290`
- 미리보기: `handoffs/L1_Workspace_Viewer_v0_5_1_20261123_KST.html`
- 개발 결과: `handoffs/L1_WORKSPACE_VIEWER_V051_DEVELOPMENT_RESULT_20261123_KST.md`

## 사용자 결정 및 현재 범위

사용자 지시: “검증은 업무 환경에서, 설계와 개발을 미리 진행” 및 “마지막 버전 기준 Viewer 개발·배포·업무 GPT 핸드오프 게시”. 따라서 이 전달은 **개발물 PUBLIC 전달 예외**이며 정식 통합 PASS·운영 설치·실행 활성화 승인이 아님. 기존 v0.4.0 원격본과 v0.4.1 전달본을 보존하고, v0.4.1의 개선을 포함한 v0.5.1 전체 소스를 제공.

## 업무 GPT에게 그대로 전달할 실행 요청

> GitHub `wonhwipark/L1Work`의 `main`에서 `handoffs/L1_WORKSPACE_VIEWER_V051_TODAY_ASSISTANT_HANDOFF_r0001_20261123_KST.md`와 루트 `l1-workspace-viewer-wiki-integrated_v0_5_1_1123.zip`을 읽고 기존 Viewer Work에서 이어가 주세요. ZIP의 bytes/SHA/CRC/manifest를 확인한 뒤 실제 사용 중인 Viewer 구현 저장소·브랜치·활성 source revision·읽기 root·인증·기존 LLM/Agent 및 실행/상태 조회 인터페이스를 G0에서 확인해 주세요. 새 UI를 재설계하지 말고 제공한 소스를 기존 서비스에 최소 이식하세요. `WikiAdapter`는 합성 전용이므로 실제 문서 조회에 연결하고, `L1ViewerAssistantHostAdapter`는 아래 화면용 계약을 기존 서버 API/Runner에 매핑하세요. 미확인 API·새 DB·임의 filesystem/shell 실행을 먼저 만들지 마세요. 기존 Workflow/Kernel/Updater/analyzer/converter의 실제 책임·writer를 재사용하세요. 이 문서 제공 자체가 업무 GPT 자동 실행은 아니며 실제 변경·호출은 현재 호스트 권한과 승인 범위 안에서 수행하세요. 권한/실행 미지원 부분만 BLOCKED로 남기고 가능한 UI 이식·격리 개발·아래 A01~A10 검증과 복구 준비를 이어가 주세요. 운영 설치/Write ON/실행 활성화는 현장 승인·보안·rollback 게이트 이후에만 진행하세요. 결과와 근거는 업무 Work에 보존하며 반출 미승인 자료의 회신은 요구하지 않아요.

## 실제 개발·자체시험과 미검증

- 기존 v0.5.0 기준 Node 10+15=**25 PASS(과거 버전 시험 근거)**. v0.5.1 신규 Node/브라우저/업무 Linux 시험은 NOT_RUN.
- v0.5.0 기준 JS/standalone inline JS 구문 PASS(과거 시험 근거). v0.5.1 실제 JS runtime/브라우저 시험은 업무 환경에서 실행 필요. HTML 중복 ID/asset 연결·미리보기 동등성·기존 Write 3파일 해시 보존·알려진 키 패턴 검사 PASS.
- ZIP CRC/manifest/중복·경로 검사 PASS. 동일 소스 2회 빌드 SHA 일치 PASS.
- **BROWSER_E2E/FORMAL_INTEGRATION_GATE/INDEPENDENT_REVIEW/LINUX_G0/REAL_LLM_AGENT/REAL_WRITE/HOST_DEPLOY=NOT_RUN.** 실제 검증은 사용자 지시대로 업무 환경 담당. 합성 답변을 실제 LLM 응답·업무 완료로 취급하지 않음.
- 배포 상태: `development_not_for_deployment`. 공개 전달과 실제 운영 적용을 구분.

---

# Viewer v0.5.1 — 업무 GPT 개발물 인계·현장 연결 계약

- 작성: 2026-11-23 KST. Work: `L1-WORKSPACE-RAG-20261111-001`.
- 제공물: UI 개발 소스. 실제 브라우저·업무 데이터·LLM/Agent 실행·운영 적용은 업무 환경에서 검증.
- GitHub 전달: `wonhwipark/L1Work`, branch `main`, 루트 `l1-workspace-viewer-wiki-integrated_v0_5_1_1123.zip`.
- 인계 정본: 동일 저장소 `handoffs/L1_WORKSPACE_VIEWER_V051_TODAY_ASSISTANT_HANDOFF_r0001_20261123_KST.md`.
- 실제 구현 저장소·브랜치·활성 서비스 경로·API: NOT_VERIFIED. 업무 GPT가 G0에서 설치본 원문으로 확정할 항목. CoWork 경로·인증에 업무 런타임이 의존하지 않음.

## 1. 사용자 요청과 구현

v0.4.1의 필터·긴 제목·너비 조절·글자/설정 개선을 포함한 전체 개발 ZIP에 우측 `목차 / 업무 도우미`와 `오늘의 업무` 전용 화면 추가. 같은 Work의 대화·입력 초안은 두 화면에서 이어짐. 문서 이동 시 대상 Work·문서·revision 표시, 이미 제안된 실행 대상은 원래 revision에 고정. 문서 없는 전역 요청은 오늘의 업무 범위로 읽기 질문 가능, 실행은 Work/revision 선택 전 보류.

대화는 메모리에만 유지되며 새로고침/프로필 전환 시 소멸. 대화 장기 보관은 이번 범위 밖. 장기 결과·진행 기록은 기존 Work/Evidence writer에 남겨야 함. 브라우저 저장소에 대화·토큰·키를 넣지 않음. 프로필 전환은 실제 서버 identity와 해당 이벤트 연결이 선행되어야 하며 설치본의 실제 사용자 격리 완료를 주장하지 않음.

`fixtures/demo-data.js` + `WikiAdapter`는 합성 전용. 기본 도우미는 명시적 합성 답변과 실행 연결 전 안내만 제공. 임의 프롬프트에 실제 LLM 응답을 흉내 내지 않으며 실제 호출/저장 0. `assistant-client.js`는 실제 호스트 연결을 위한 화면용 bridge 계약이며 서버 API/설치 기능의 사실이 아님.

## 2. 기존 기능 재사용·스킬 책임

| 역할 | 기존 경로 | 현장 확인 |
|---|---|---|
| Work 목록·상태·진행·근거 | Workflow + Kernel 기존 조회/export | 오늘 날짜(KST) 의미·권한·갱신 시각·지원 상태 매핑 |
| Work 재개·분석 실행 의도 | 기존 업무 LLM/Agent → `l1-fix-workflow` | canonical Work/revision·기존 실행 승인·Runner/Job 유무 |
| 상태·중복·원본·결과 | `work-ledger-kernel`·기존 검증 writer | 요청 식별·진행 이력·CAS·readback·영수증 |
| 분석·설계·MSC | 기존 issue/code analyzer·hld-composer·doc-converter | 기존 스킬 산출물을 Workspace에 보존 후 문서 링크로 반환 |
| 지식 반영 | `l1-knowledge-updater` 및 기존 그룹 writer | 별도 owner·Preview·승인·revision/readback 유지 |

이번 ZIP은 Viewer만 변경. 위 스킬들의 새 버전/실제 Runner·MCP 서버·인증 서버는 포함하지 않음. Viewer에 직접 filesystem·shell·임의 스킬명 실행·API 키 입력·외부 ChatGPT iframe을 추가하지 않음. 모바일 Agent → Linux MCP 기존 경로와 Viewer 서버 경로는 허용된 공통 업무 기능을 재사용하되, Viewer를 MCP 상시 필수 경로로 만들지 않음.

## 3. UI bridge — 설치 API에 매핑할 예시 계약

서버가 허용된 방식으로 `window.L1ViewerAssistantHostAdapter`를 공급. 설치본에 존재하는 인증·API·LLM/Agent 호출·Job 조회 경로에 좁게 매핑. 새 서버/DB/REST URL을 아래 이름만 보고 만들지 말 것. `getCapabilities`의 true는 실제 서버 검증 결과일 때만 공급하며 프런트엔드 값은 보안 권한의 근거가 아님. 모든 요청에서 서버가 재인증·ACL/CSRF·범위·한도를 재검사.

| 메서드 | UI 요청 | 서버 측 의미/응답 |
|---|---|---|
| `getCapabilities()` | 없음 | `{readVerified,authVerified,scopeVerified,executeVerified}`. read/auth/scope 세 가지 true 전 모델/업무 호출 차단 |
| `listToday({date,timezone})` | KST YYYY-MM-DD, Asia/Seoul | `{items:[{workId,title,docId,revision,status}]}`. 권한 범위 조회. 날짜 필터·대기/진행의 의미는 기존 Work 필드에 매핑하고 미지원은 UNKNOWN/보류 |
| `send({clientRequestId,scope,message,mode:'ask'})` | scope=`{date,timezone,workId,docId,revision}` | 질문/의도 해석·읽기·요청 미리보기. 이 단계에서 변경·실행 자동 시작 금지. 실행 제안은 `proposalId/proposalLabel`로 반환 |
| `execute({clientRequestId,proposalId,scope})` | 사용자 실행 버튼, 제안 당시 Work/revision | 서버 보관 proposal·사용자·기존 승인·한도 재검사 → 기존 Runner/스킬에 1회 위임. 임의 모델 tool arguments를 신뢰하지 않음 |
| `getRequest({clientRequestId,scope})` | 기존 요청 번호 | 상태/이력/영수증만 조회. 재큐잉·재분석·재실행 금지 |

공통 응답: `{status, requestId?, receiptId?, text, proposalId?, proposalLabel?, links?:[{docId,label}]}`.

허용 상태: `RECEIVED / RUNNING / COMPLETED / NEEDS_INPUT / BLOCKED / FAILED / UNCERTAIN`. COMPLETED에는 영수증 ID 필수. 실제 작업 완료·새 revision·Evidence readback 여부는 서버 영수증으로 증명. 직접 URL 대신 권한 검증된 opaque docId를 반환하고 Viewer 기존 resolver가 원문을 열도록 연결. canonical docId와 route 형식은 설치본에 맞게 변환.

전송 중 중복 버튼 차단. 응답 불명확/연결 단절 시 UNCERTAIN으로 보존하고 자동 재시도 없음. 처리 중 목록은 수동 상태 조회 방식. 현재 클라이언트의 불확실 요청은 새로고침 시 소멸하므로 **서버의 사용자별 요청 이력 조회·중복 실행 방지·영수증 보존을 필수로 연결**. 호스트/브라우저 재시작 후 미정산 요청을 확인하지 않고 같은 실행을 새 요청으로 다시 보내지 말 것. 기존 승인 자동 위임이 유효하면 서버 계약을 재사용하고 불필요한 재승인을 추가하지 않음.

## 4. 기존 읽기/쓰기·UI 이식

기존 `WikiAdapter` read 메서드를 실제 문서 root·읽기 API에 연결. 합성 fixtures/standalone은 운영 제공 경로에서 제외. UI만 이식하고 Work/Evidence 원본·파일명·폴더 구조·정본 schema는 보존. v0.4.1 Write v0.2.0 파일은 바이트 그대로 유지하며 `L1ViewerWriteHostAdapter`와 도우미 bridge는 별개. 인증 안 된 독자는 현재 허용된 문서 읽기를 계속하며 도우미 실행은 서버 인증/검증 전 보류. 숨김 설정은 ACL 아님.

CSP `connect-src 'none'`은 합성 데모 정책. 실제 승인된 same-origin 서버 세션·요청 계약 확인 후 서버에서 최소 허용. 임의 CORS `*`, iframe ChatGPT, 브라우저 키 저장 금지. assistant 답변은 textContent, 결과 링크는 docId 인코딩. 기존 HTML/MSC 별도 origin·sandbox/권한 게이트 유지.

## 5. 업무 환경에서 수행할 확인표

| ID | 확인 | 완료 기준 |
|---|---|---|
| A01 | 1440/1300/1040/760/390/320px | 본문·목차·탐색·도우미 접근, 수평 overflow/패널 겹침 통제 |
| A02 | 우측↔오늘 탭↔문서 3회 이동 | 같은 Work 대화·초안 유지, 다른 Work 분리, 전역/Knowledge 문서 혼선 없음 |
| A03 | Tab/Shift+Tab/Escape/좌우키/IME | 패널 닫기·포커스 복원, 탭 전환, 입력 중 원치 않는 실행 없음 |
| A04 | 오늘 날짜·KST 자정·상태·현재 source | 실제 원천 필드와 일치, 조회 실패를 업무 0건으로 오인하지 않음 |
| A05 | 미연결·읽기만·권한 실패 | 실제 호출/원본 쓰기 0, UI만으로 실행 권한 상승 불가 |
| A06 | 실제 질문/분석 제안→실행→결과 | 기존 허용 LLM/Agent/스킬, Work ID·원본 revision·영수증·문서 readback 일치 |
| A07 | 네트워크 단절·중복·새로고침·재시작 | 중복 실행 0, 기존 요청/영수증 조회로 복구. 무단 재큐잉 0 |
| A08 | 계정·프로필·문서 ACL·CSRF | 다른 사용자/Work의 대화·목록·결과·검색 내용 노출 0 |
| A09 | 기존 필터/설정/너비/MSC/Write | v0.4.1 관련 시험 + v0.2.0 실제 Write/기존 Workflow·Kernel 회귀 |
| A10 | 백업·rollback | Viewer asset/entry/adapter만 복구 가능, 원본 Work/Evidence/DB 불변 |

상태는 PASS/FAIL/NOT_RUN/BLOCKED로 업무 Work에 보존. 운영 설치/도우미 실호출·Write ON은 실제 승인 범위 내에서 수행. 회사 제한 원문·로그·MSC·토큰 및 반출 승인 없는 결과는 외부 전송하지 않음.


## v0.5.1 추가 현장 화면 검증

- H01: 최초 문서 표시 시 목차 노출, 도우미 숨김, 상단 버튼 `aria-expanded=false`.
- H02: 상단 버튼 2회, ESC, 닫기로 접기/펼치기, focus 복귀, 1440/1300/1040/760/390/320px 회귀.
- H03: 오늘의 업무 최초 진입 대화 컬럼 숨김/목록 전체 폭, 명시적 버튼 후에만 열림.
- H04: Work A→B→A 대화/초안 분리 유지, 크게 보기 전환 후 이어짐.
- H05: Demo에서 LLM/Agent/업무 원본 쓰기·실행 0. 실제 운영 활성화 불가.
