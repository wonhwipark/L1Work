# L1 Source Map 책임 경계와 수정 범위 · 업무 GPT 인계

2026-11-27 KST · r0001 · 기존 Work `L1-WORKSPACE-RAG-20261111-001` · 단계 **인계**

**설계 판정**　Source Map은 LLM이 현재 소스에서 확인할 파일·심볼·메시지 관계를 고르는 공통 인덱스로 확정해요. 동작 설명은 기존 Knowledge, 분석 근거는 Work/Evidence, 시퀀스는 기존 MSC를 참조해요. 효과 판정은 정상 Procedure Knowledge를 이미 제공한 상태에서 Map이 더해 주는 정확도 또는 비용 개선으로 해요.

**업무 GPT에 전달할 요청문**

> 기존 Work에서 업무 GPT가 관리하는 `l1-knowledge-updater`의 활성 원본과 기존 Discovery 7개를 읽기 전용으로 대조해 주세요. 7개 각각의 revision/build·근거·범위·재사용 여부와 개인/그룹 G6 승인 범위를 먼저 회신해 주세요. 현재 Analyzer의 분기 조회가 아래 합성 반례를 통과하는지도 확인해 주세요. 일치하는 원본 근거를 확보하면 대표 모듈 한 곳에서 기존 조회·검증 단계를 연결할 최소 변경과 시험 대상을 제시해 주세요. 제품 소스와 결과 원문은 업무 Work에 보존하고, 회신에는 버전·판정·허용된 증빙 참조·다음 행동을 적어 주세요.

| 우선순위 | 확정 사항 | 소유자와 시점 |
|---|---|---|
| P0 | Analyzer v0.15.6의 전처리 조건 오판을 최소 수정할 근거가 있음. 활성본에서 동일 반례를 확인하고, 수정·회귀 전 해당 출력을 빌드 조건 확정에 사용하지 않음 | 설계 GPT가 관리하는 Analyzer. 업무 GPT는 현장 대조와 소비 제한 |
| P0 | 기존 7개 결과를 기존 형식에 매핑하고 필요한 관계만 조회. 증거 수준이 낮은 결과는 다음 코드 탐색 후보로 전달 | 업무 GPT의 Updater. 첫 작업은 G01~G06 |
| P1 | 독립 Source Map 진입점과 읽기 전용 검색·상세를 제공하려면 Viewer v0.5.7 후보에 소규모 수정이 필요함 | 설계 GPT는 표시, 업무 GPT는 실제 read adapter. 품질 시험에 UI 개발을 선행 조건으로 두지 않음 |
| 재사용 | 기존 Knowledge 분류, MSC 본문, Converter, Workflow, Kernel은 이번 목적 때문에 일괄 변경할 이유가 없음 | 현장 계약에서 실패한 동작만 소유자에게 환류 |

이번 인계는 11월 27일 통합 설계 r0002의 품질·권한·예산 기준을 이어받아요. 기존 R1 판정의 지적을 재사용하며 이후 검증은 자체 회귀와 현장 비교로 진행해요. G6, 현장 설치, Job, 그룹 게시의 승인 상태는 별도예요. [통합 설계 r0002](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/3ee216ff501172a164958e91106053c1ed6cd1f9/collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_SOURCE_MAP_LLM_FIRST_INTEGRATED_DESIGN_r0002_20261127_KST.md) · [기존 R1 판정](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/dc2e782c1ca909ead6232e59ff5a605de6191529/collab/projects/L1-WORKSPACE-RAG-20261111-001/GPT_SOURCE_MAP_R1_REVIEW_DISPOSITION_r0001_20261127_KST.md) · [기존 Work CURRENT](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/dc2e782c1ca909ead6232e59ff5a605de6191529/collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md)

## 1. Knowledge와 Source Map이 각각 보관할 내용

| 기존 정본 | Knowledge·Work에 한 번만 유지 | Source Map이 반환할 최소 정보 |
|---|---|---|
| Module | 책임, Architecture, 구성요소, 인터페이스 계약 | 모듈·구성요소 ID, 소속, 진입 심볼·정의 위치, 문서 참조 |
| Feature | 설계 원리, 적용 조건, 상태와 예외, 관련 Scenario | 관련 심볼, guard·상태 변수의 위치, 읽기·쓰기 근거 |
| Procedure | API 의미, 호출 이유, 인자·반환·부작용, 필요한 정상 절차와 기존 MSC | 정확한 시그니처·정의/선언, 방향이 있는 직접 호출 또는 미확정 후보, 타입 참조 |
| Scenario | Trigger, 전제, 정상·예외 경로, 비동기 부분 순서, 검증된 MSC | 해당 메시지·Handler·Payload의 근거, 기존 문서·그림 참조 |
| Issue Knowledge / Recovery | 증상·원인 규칙·수정·검증, Edge/AS-IS/TO-BE의 의미 | 관련 심볼과 후보 위치, 조사·제외 범위. 후보의 종결은 Recovery가 판정 |
| Work/Evidence | 소스 대조 기록·분석 영수증·기존 그림과 이력 | 해당 Evidence ID·revision·anchor·hash. 같은 원문을 다시 저장할 필요가 있는지 기존 권한·보존 계약으로 판단 |

기술 지식의 기본 탐색은 **Module → Feature → Scenario**, Procedure는 여러 Feature·Scenario를 잇는 교차 참조예요. 같은 API가 여러 화면에 보여도 설명과 MSC의 원본은 하나예요. 정적 호출·등록은 코드에 있는 관계를 뜻해요. 실행 여부와 메시지 순서를 설명하려면 현재 코드·조건 또는 관찰 근거가 필요해요. Map 갱신 후 기존 문서와 코드 기준이 다르면 재검토 대상으로 표시해요. [기존 분류표 v0.9, 담당자 검토 후보](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/L1_NR_LTE_Confluence_Module_Procedure_Feature_Table_v0_9_20261113_KST.md) · [Updater r0002, 6~8절](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/handoffs/L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0002_20261125_KST.md) · [Viewer v0.5.6 역할표](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/handoffs/L1_WORKSPACE_VIEWER_V056_TECHNICAL_KNOWLEDGE_READABILITY_COMPLETE_HANDOFF_r0001_20261126_KST.md)

**r0002 대비 결정.** 독립 논리 영역 `source-map/`과 Viewer의 독립 접근은 수용해요. 구체 하위 디렉터리·DB·전역 랭킹·새 API는 G0의 기존 형식에 맞춰요. 화면은 검색 결과와 근거 상세로 축소하고 Architecture 설명·Scenario 흐름·Map 전용 MSC는 기존 Knowledge로 연결해요. 처음에는 Map → Knowledge 이동만 연결하며, 역방향은 기존 문서 재작성 없이 읽기 측에서 제공할 수 있을 때 추가해요.

## 2. 최신 원본에서 발견한 수정 근거

검토 기준은 L1Work `f167325d7bfb`와 CoWork `dc2e782c1ca9`예요. L1Work 개발 ZIP 7개에서 Git blob·크기·ZIP CRC를 대조했고, Viewer는 내부 manifest 45개 항목도 검증했어요. 분류표·Updater/Recovery 최신 인계·합성 Knowledge 5유형·공개 Work MSC 샘플과 배포 후보 코드를 읽었어요. 업무 Knowledge 정본, 활성 Updater/Recovery 및 Discovery 7개 원문은 현장 G0 확인 대상이에요. [L1Work 검토 시점](https://github.com/wonhwipark/L1Work/tree/f167325d7bfb33a314e52cdc97f2dce6cc996eb5) · [CoWork 관리 스킬 카탈로그](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/dc2e782c1ca909ead6232e59ff5a605de6191529/collab/knowledge/SKILL_CAPABILITY_CATALOG.md) · [공개 합성 Work/MSC](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/sample/msc-workspace/works/DEMO-MSC-001/CODE_FACTS.md)

### 2.1 Code Analyzer에서 고칠 한 곳

v0.15.6의 `scripts/ca_core/probe_engine.py::compile_condition_probe`는 `#elif`를 새 중첩 조건으로 push하고 `#else`에서 현재 분기를 바꾸지 않아요. `#endif`가 한 번만 pop하면서 바깥 선언에 조건이 남아요. 패키지의 `probe compile-condition` 진입점과 C++ 전처리기(GCC 14.2) 네 가지 A/B 조합으로 확인했어요.

| 합성 fixture에서 심볼이 놓인 위치 | 전처리기의 기대 활성 조건 | v0.15.6 원본 응답 |
|---|---|---|
| `#if A` 안 | A | `[#if A]`, `CONFIRMED` |
| 뒤따르는 `#elif B` 안 | `!A && B` | `[#if A, #elif B]`, `CONFIRMED` |
| 같은 블록 `#else` 안 | `!A && !B` | 앞 행과 같은 조건 목록, `CONFIRMED` |
| `#endif` 뒤 독립 선언 | 네 조합 모두 포함, 이 블록 조건 없음 | `[#if A]`, `CONFIRMED`. 해당 사실이 `patch_writer.merge_results`에서 `PATCH_PENDING`에도 포함 |

**최소 수정 범위**는 조건 블록별 현재 분기·앞선 형제 분기·중첩 종료 처리와 전용 회귀예요. 실제 build 정의가 없으면 정적 분기 위치까지만 확인하고 활성 여부는 미확인으로 남겨요. 정상 중첩, `#elif` 연속, `#else`, 종료 뒤 선언, 주석·문자열·연속행, 처리 불가 지시문을 검사하고, 모호한 사실이 확정 patch에 들어가지 않도록 검증해요. 기존 probe 명칭·출력 호환과 직접 호출 검증은 유지해요. 활성본이 같은 반례를 이미 처리하면 해당 버전을 재사용해요. [Analyzer v0.15.6 원본 ZIP](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/code-analyzer_v0_15_6_1125.zip) · [기존 개발 전달 기록](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/handoffs/CODE_ANALYZER_V0156_DEVELOPMENT_DELIVERY_r0001_20261125_KST.md)

현행 `symbol` probe는 주석·문자열에만 있는 이름도 `symbol_occurrence / CONFIRMED`로 반환했어요. 이는 텍스트 출현에 대한 결과예요. `feature-scope-probe`의 상위 후보 점수 0.55 이상도 aggregate `CONFIRMED`가 될 수 있어요. `callers/callees`의 `static_direct_call_spelling`은 소스 직접 호출 표기까지만 보증해요. Updater는 `fact_type`·근거·대상 명제를 함께 읽고 정의·overload 해소·실행 순서로 승격하지 않아요. 이 세 경우는 소비 규칙과 원문 대조로 처리 가능해요.

### 2.2 Viewer에서 고칠 한 곳

v0.5.7의 `assets/app.js::route`는 Work·Knowledge·전체 파일과 Today·Recovery를 구분해요. 배포된 fixture에서 `listRoots('source-map')`은 `VIEW_NOT_FOUND`였고, `adapters/adapter.js::resolveDocumentLink`는 같은 Work 안의 Markdown 상대 경로만 해석했어요. `search`는 합성 문서 본문의 부분 문자열 검색이에요. `href`와 일반 검색 결과 이동은 현재 view를 기본값으로 사용해요. 기존 검색에 Map 레코드만 섞으면 정확 심볼 검색과 올바른 대상 화면 이동을 보장할 수 없어요. [Viewer v0.5.7 원본 ZIP](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/l1-workspace-viewer-wiki-integrated_v0_5_7_1126.zip) · [v0.5.7 통합 인계](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/handoffs/L1_WORKSPACE_VIEWER_V057_KNOWLEDGE_SECTION_ORDER_COMPLETE_HANDOFF_r0001_20261126_KST.md)

| 최소 화면 | 처음 보이는 것 | 선택 후에만 보이는 것 |
|---|---|---|
| Source Map 읽기 화면 | 독립 진입점, 심볼/Message ID 검색, RAT·모듈 또는 build 필터, 이름·종류·검증 상태 | 정의/등록/호출 후보, source pin·build·anchor, 근거·누락 범위, 유효한 기존 Knowledge 링크 |
| 기존 Knowledge | 기존 유형별 제목·섹션·본문 MSC | 기존 HTML/SVG 확대와 원문·목차·뒤로가기. 미매핑 문서는 원문 순서 |

대상은 `index.html`의 메뉴, `assets/app.js`의 라우팅·선택·대상 view를 지정한 문서 이동, `adapters/adapter.js`의 합성 읽기 예시와 대응하는 실제 호스트 read adapter예요. 검색·목록·표·본문 렌더러를 재사용해요. 서버가 권한과 문서 ID·revision을 확인한 경우에만 기존 Knowledge 화면으로 이동해요. 같은 Work 상대 경로 제한을 풀지 않아요. 긴 JSON·근거는 기본 접힘이며 미등록·오래됨·부분 결과·충돌·권한 실패를 구분해요. 승인 없는 문서의 이름·경로·건수도 노출하지 않아요. 호스트 조회가 실패하면 그 상태를 표시해요. Map 화면에서 편집·Job·MSC 생성은 제공하지 않아요.

## 3. 스킬별 변경 판정

| 담당과 구성 | 판정 | 적용 단위 |
|---|---|---|
| 업무 GPT · `l1-knowledge-updater` | **CONNECT 우선** | 기존 조회/중복 비교/원본 대조 단계에 선택 조회, 증거 강도 변환, 기존 지식 ID와 연결, 누락·충돌의 갱신 후보를 추가. Map 생성·갱신과 개인 저장·그룹 게시 **요청**의 단일 소유자. 실제 파일명·action은 활성 원본 확인 후 지목 |
| 설계 GPT · `code-analyzer` | **REUSE + 최소 EXTEND** | `probe`의 symbol/callers/callees/dispatch/callback/field, 기존 manifest·reuse 검증을 재사용. 2.1절의 조건 오류만 우선 수정. Map 후보는 기존 scope·target resolution에 허용된 경로로 제한해 전달 |
| 설계 GPT · Viewer / 업무 GPT · MCP·read adapter | **표시 EXTEND / 조회 CONNECT** | 2.2절의 메뉴·라우팅·근거 표시만 확장. 활성 adapter에 기존 exact lookup·ID 이동이 있으면 연결. 승인된 capability로 필요한 조회가 안 될 때만 해당 읽기 동작 보완 |
| 업무 GPT · `l1-channel-recovery` | **CONNECT** | V1→V2는 정상 Procedure·수정 전/후·정상 반례로 규칙 확인. V3는 Map 후보와 지도 밖 독립 탐색으로 보호 누락 검사. V4~V6 최초 위반 전 보호·반증·복귀·MSC는 기존 r0007. 기존 비-timeout 범위 유지 |
| 업무 GPT · 개인/그룹 Writer | **REUSE, 현장 확인** | 승인 actor/path·기존 CAS(기대 revision)·readback을 재사용. 경로 권한 또는 원자적 전환 미확인은 해당 저장만 보류 |
| 설계 GPT · `work-ledger-kernel` v0.7.47 | **REUSE** | `work_ledger_kernel/work_ux.py`의 실제 export가 Knowledge와 Map 표식 파일을 보존. Work/Evidence·공통 index 역할 유지. 현장 export가 이를 훼손할 때만 재검토 |
| 설계 GPT · `l1-fix-workflow` v1.6.75 | **REUSE** | `knowledge_input.py`의 검증된 기존 지식 인용, `msc_view.py`의 동일 Work·SHA 확인 열람 경로 재사용. Map을 기존 Module 문서 입력으로 위장하지 않음. 동버전 후보는 ZIP hash로 대조 |
| 설계 GPT · `doc-converter` v0.2.26 | **REUSE** | `msc-scenario-adapt/build`와 `msc-package`가 검증된 시나리오 입력에서 기존 PUML/SVG/HTML을 제공. 유효 기존 MSC를 참조. Map 전용 렌더러는 제외 |
| `knowledge-analysis-preflight` v0.2.0 | **선택 재사용** | `preflight.py`·`hierarchy.py`의 제한 문맥·근거 ID·분류/Procedure 교차 참조 검사. 문자 한도·근거 연결 통과만으로 토큰 예산·실행 경로·Converter 호출을 승인하지 않음 |
| `job-list` / `skill-updater` | **변경 범위 밖** | 기존 실행·인계·패키지 검증 경로 유지. 이번 설계에 전용 Job이나 배포 변경 요구 없음 |

[Recovery r0007](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/handoffs/L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0007_20261125_KST.md) · [Recovery V2/V3 진단](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/handoffs/L1_RECOVERY_V2_V3_PROCEDURE_KNOWLEDGE_DIAGNOSTIC_DESIGN_HANDOFF_r0001_20261126_KST.md) · [Kernel 원본](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/work-ledger-kernel_v0_7_47_1124.zip) · [Workflow 원본](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/l1-fix-workflow_v1_6_75_1121.zip) · [Converter 원본](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/doc-converter_v0_2_26_1117.zip) · [Preflight 원본](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/knowledge_analysis_preflight_v0_2_0_1121.zip) · [기존 Job 인계](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/handoffs/JOBLIST_PCELL_TX_PATH_ON_OFF_PROCEDURE_MSC_PROMPT_r0001_20261125_KST.md)

## 4. LLM 조회·갱신 계약

| 단위 | 기존 형식에서 대응시킬 최소 의미 |
|---|---|
| Snapshot | 원본 식별자·revision, build/variant, 범위/제외, producer/version, manifest/hash·이전 snapshot, 조사량/gap. 한 조회는 동일 snapshot으로 고정 |
| Entity와 관계 | qualified name, signature/qualifier, 필요 시 TU/linkage·template·variant, 선언/정의 anchor. 양 끝 ID·관계 종류·방향·guard·evidence ref. 행 번호 단독으로 동일성을 정하지 않음 |
| 신뢰도 | 생성 방식 `parser/tool/LLM/manual/unknown`, `EXTRACTED/INFERRED/UNKNOWN`, 원문 대조 `VERIFIED/UNVERIFIED/CONFLICT`, 소비 시 `freshness`를 독립 보존. 정적 관계·실행 관찰은 종류와 근거를 분리 |
| Knowledge 참조 | 기존 문서 ID·문서 revision·섹션 또는 MSC artifact, 참조한 소스 revision/build. 확인 안 된 링크는 미연결. Map 변경만으로 문서·MSC를 자동 갱신하지 않음 |

1. 요청마다 source/build, 허용 scope, 질문 하나를 고정해요. 예를 들어 ‘API 정의 위치’는 Map, ‘해당 API가 특정 상태에서 실행되는 이유’는 Procedure/Feature와 원문으로 답해요.
2. 기존 조회로 정확한 ID·qualified signature 또는 메시지 키를 찾고, 관계 종류와 방향을 지정해 기본 1-hop만 받아요. 동명·overload·간접 호출이 남으면 후보를 각각 반환해요. 응답에는 snapshot, 후보·근거·검증 수준, 조사/제외 범위, partial/truncated와 다음 조회 한 건을 넣어요.
3. 결과가 없거나 stale이면 허용된 현재 코드에 대한 기존 bounded probe로 이어가요. Map 누락은 부재·보호 완료의 근거가 될 수 없어요. 원문 검증 후 Updater는 기술 문서, Recovery는 후보 판정을 담당해요. 소비자가 발견한 오류는 같은 Work에 갱신 후보로 남겨요.
4. Updater는 같은 revision의 유효 결과·MSC를 재사용하고 바뀐 범위만 대조해요. 개인 Workspace의 논리적 `source-map/`, Knowledge 및 Work의 정본은 각자 유지해요. 한 snapshot에서 Markdown 표를 파생하고 기존 Writer의 staging·기대 revision·readback이 확인된 경우에만 활성 참조를 전환해요. 충돌·불확실 응답은 이전 버전과 후보를 보존해요.
5. 그룹은 Base/Ours/Theirs 비교와 별도 Preview·승인·CAS·readback 후 연결해요. 게시 후 역링크 정산만 실패하면 정산만 재개해요. Viewer·링크 실패로 분석·Discovery·변환·Job을 반복하지 않아요.

**조회 응답 예시.** 2.1절의 합성 fixture에서 빌드 A=0, B=1로 `OnlyB`를 조회하고 선언 위치만 요청한 경우예요. 아래 한 행은 논리 응답 예시이며 업무 API 이름이나 실제 제품 결과를 뜻하지 않아요.

| 질의·범위 | 돌려줄 사실 | 검증 상태와 후속 조회 |
|---|---|---|
| `OnlyB`, 선언, 합성 snapshot 1건 | 합성 파일 4행의 선언. 전처리 출력으로 이 빌드에서 선언이 남은 것을 확인 | 선언·해당 build만 검증. 정의·호출자·런타임 실행은 미조사, 기존 Knowledge 링크는 미연결. 다음 질문이 ‘정의’일 때만 정의 후보 조회 |


## 5. 자체 회귀 결과와 현장 수락 기준

| 구분 | 이번에 실제 실행한 범위 | 판정 |
|---|---|---|
| Analyzer v0.15.6 | 직접 호출/coverage 22건, 정확도·저장 25건, 병렬 계약 28건 | 기존 75/75 PASS. 별도 분기 정확도 반례는 2.1절처럼 FAIL |
| Viewer v0.5.7 | Node 24에서 배포본의 `regression`, `readability`, `readability-v055`, `readability-v057`, `assistant-client`, `recovery` | 기존 6/6 프로그램 PASS. 추가 fixture 검사에서 Map root 부재, Work 밖 상대 링크 거부 재현. 실브라우저 회귀는 이 검토 환경에 실행 가능한 Chromium이 없어 미실행 |
| Kernel / Workflow | Kernel Recovery 2건·Write guard 13건, 별도 합성 Work 두 번 export. Workflow Knowledge 입력은 실제 v0.15.6 후보와 연결해 23건 | 15/15, 23/23 PASS. export 후 Knowledge 1개·Map 2개 바이트 동일, 두 번째 export 변경 파일 0. 운영 Writer 권한은 미확인 |
| Preflight / Converter | Preflight 원본 unittest 38건. Converter는 원본 HTML·MSC 합성 시험 함수 6건 직접 실행, 추가로 원본 SVG 내장 바이트·누락 phase 보류 확인 | 선별 범위 PASS. v0.2.26 전체 pytest는 실행 환경의 pytest 부재로 미실행. 실제 제품 MSC 의미·브라우저·호스트 연동은 미확인 |

**현장 비교.** 소스/build·모델 ID/설정·도구·총예산·질의·정답 분모를 고정해요. 대표 모듈 하나의 기존 실패 비-timeout Seed와 별도 평가 사례를 독립 문맥으로 비교해요. 정상 Procedure에 정답·수정 정답지가 새지 않게 하고, 자동으로 들어가는 기존 Knowledge와 실제 전송된 데이터를 기록해요.

| 시험군 | 기준선에 추가하는 입력 | 확인할 차이 |
|---|---|---|
| D0 | 없음 | 현행 분석 |
| D1 | 제한된 Map 조회 결과 | D1−D0, 코드 탐색 효과 |
| D2 | 검증된 정상 Procedure Knowledge | D2−D0, 동작 맥락 효과 |
| D3 | 동일 Map과 동일 Procedure | **D3−D2**, 기존 지식에 Map을 더한 가치 |

11/26 Recovery 진단에서 D1은 **검증된 코드 fact**를 투입한 군이에요. 여기의 D1은 **지도 후보를 주고 현재 코드를 다시 확인하는 군**이에요. 두 결과는 실험 입력 이름을 구별해 기록해요.

- r0002 pilot 예산은 Map 4,096 tokenizer tokens·50 records, 실제 코드 최대 20파일/step·60파일/task, 추가 probe 최대 4단계, 총 입출력 32,768 tokens·20분/task예요. 더 낮은 활성 제한을 우선하고 시험 시작 전 한도를 고정해요. 문자 수·반환 행 수와 실제 토큰 수·읽은 파일 수를 따로 계측해요.
- 담당자 검증 양성 관계 ≥30개, 음성·반례 ≥10개. recall ≥90%(30개면 27개 이상), 누락·UNKNOWN도 양성 분모에 포함. precision은 전체 확정 예측을 분모로 계산해요. 근거 없는 확정 0, stale/variant 불일치 탐지 100%, 범위 밖 읽기 0이 수락 기준이에요.
- V2 규칙·최초 위반 정확도, V3 후보 recall/precision, V4 잘못된 종결, 필요한 경우 V6 MSC 방향·분기·순서를 별도 채점해요. Map 비용까지 포함한 시간·토큰·실제 파일 수와 최초 구축/변경분 갱신 비용을 따로 기록해요. 동일 예산에서 정확도가 높아지거나, 동일 정확도에서 탐색 비용이 줄어드는 효과가 별도 사례에서도 재현되면 확대해요. 허위 확정 발생 또는 추가 가치 미확인은 해당 확대를 보류해요.

| 남은 회귀 묶음 | 합격 조건 |
|---|---|
| 정본·재사용 (B01~03, B05, B11) | 동일 snapshot 재분석·MSC 재생성 0, 기본 분류·기존 링크·원문 보존, 정적 등록에서 런타임 시퀀스 추론 0, 오래된 Knowledge 자동 확정 0 |
| 탐색·예산 (B04, B06) | 분기 반례와 overload·TU·variant·간접 호출을 구별, 한도 도달 시 누락과 후속 조회 기록. 실제 읽기와 토큰 측정 |
| Viewer (B07~09, B12) | 검색→선택→권한 있는 Knowledge/MSC→복귀. ID·문서 rev·소스 rev 불일치, 없는 링크, 미권한, 조회 오류를 분리. 기존 Work/검색/목차/원문/편집 보호·도우미·Recovery와 모바일·키보드 회귀. 표시 실패로 재실행 0 |
| 권한·동시성 (B10, 기존 T06~08/T12) | 경쟁 갱신 시 한 snapshot만 활성, 권한 밖 쓰기·혼합 revision·중복 게시 0, 충돌/중단 후 기존 스냅샷과 readback 일치 |

## 6. 업무 GPT가 회신할 항목

| 기존 G0 | 현장에서 확인할 원본 | 회신할 판정 |
|---|---|---|
| G01 | 7개 산출물 각각의 manifest·hash·source/build·coverage | 그대로 재사용 / 일부 보완 / 충돌·미확인 및 근거 |
| G02 | 활성 Updater·Analyzer의 version/hash/action과 추출 방식, 2.1절 분기 fixture | 재현/해결/미확인, 어떤 사실까지 검증 가능한지 |
| G03 | G6 승인 대상, 개인 Writer actor/path·CAS/readback, 활성 Kernel export | 개인/그룹별 범위와 보존 여부 |
| G04 | 기존 조회·MCP·Viewer adapter와 Analyzer/Recovery의 읽기 입력 | exact/1-hop·예산·권한·ID 이동, 재사용 위치 또는 결손 사례 |
| G05 | 실제 모델·도구·토큰 계측, 고정 평가셋과 정상 Procedure | 동일 예산 D0~D3 가능 여부·상한·분모 |
| G06 | 기존 그룹 형식, 비교·Preview·충돌·게시 후 정산 계약 | 그룹 연계 가능 범위·남은 조건 |

회신은 `G0 ID / PASS·FAIL·UNKNOWN / 활성 version·action / 업무 Work 내 근거 ref / REUSE·CONNECT·입증된 GAP / 다음 행동` 한 행씩이면 충분해요. G0 후 업무 GPT가 Updater의 실제 변경 지점을 결정하고, 설계 GPT는 Analyzer 결함의 회귀와 필요한 Viewer 변경을 맡아요. 대표 모듈 실측과 기존 기능 회귀를 통과한 개발 후보만 해시와 함께 인계해요. 운영 적용·그룹 반영은 해당 권한과 수락 결과에 따라 별도로 판정해요. [기존 G0 인계](https://github.com/wonhwipark/L1Work/blob/f167325d7bfb33a314e52cdc97f2dce6cc996eb5/handoffs/L1_SOURCE_MAP_LLM_FIRST_G0_HANDOFF_r0001_20261127_KST.md)
