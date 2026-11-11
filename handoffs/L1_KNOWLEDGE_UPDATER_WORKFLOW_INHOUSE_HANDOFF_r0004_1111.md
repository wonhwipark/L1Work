# L1 Knowledge Updater K5.8/K6 × Workflow — 사내 G0 인계 r0004

- 작성: 2026-11-11 KST / 문서 버전 r0004
- 문서 위치: GitHub PUBLIC `wonhwipark/L1Work`, branch `main`, `handoffs/L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0004_1111.md`
- 용도: 사내 GPT에 첨부하여 독립적으로 읽는 G0 READ_ONLY + 최소 연동 설계 인계. 취득 후 오프라인 문서 입력으로 사용할 수 있으며 실행 시 외부 계정·인증·저장소 조회에 의존하지 않는다.
- 현재 준비도: READY_FOR_INHOUSE_G0. 실제 K5.8/K6 원문·설치 API 호환성은 AS_IS_NOT_VERIFIED이고 구현 착수/운영 게시 명세 확정은 BLOCKED_AT_G0이다.
- 이번 개정: 검증 상태축, 원인만 검증된 이슈, MSC 주장 근거, source 입력, N:M/부분 갱신, 승인/CAS·응답 유실 복구, legacy mapping, RAG 자격 조건을 보완했다. 이는 설계 보완이며 검증된 구현이라는 뜻이 아니다.
- 범위: 실제 설치 원문·계약 확인, AS-IS→목표 매핑, REUSE/CONNECT/EXTEND/DEFER, 변경 파일 후보와 시험·롤백 계획 작성만.
- 금지: 소스/설치 스킬 수정, 실제 Work/Evidence 생성·갱신, 운영 DB/작업 설정 변경, 그룹 정본 write, 모델/Job 유료 호출, 자료 외부 전송. 보고 파일은 승인된 사내 작업 공간에만 작성한다.
- 상태: G0_K58_K6_SOURCE=NOT_VERIFIED / INHOUSE_E3=NOT_RUN / TEST_T01_T24=NOT_RUN / RAG_M1=BLOCKED / INDEPENDENT_REVIEW=NOT_RUN / GROUP_WRITE=NOT_RUN / SKILL_RELEASE=NOT_RUN.
- 문서 공개는 설계 인계만 허용한 것이며 설치·자동 실행·그룹 게시·스킬 배포 승인이 아니다. 기존 r0002 인계는 과거 기록으로 보존한다. 이번 범위의 충돌 조건은 이 r0004를 우선한다.

증거 수준: E0=전제/미확인, E1=문서/계약, E2=실제 소스·격리시험, E3=사내 설치본/실환경의 해당 항목 실측. G0 설치본 원문 확인과 실제 API/통합 성공은 별도로 보고한다. 공개 개발 후보 근거를 사내 E3로 승계하지 않는다.

## 1. 정책 범위와 정본

사용자 전달 그룹 합의의 목표 정책: 그룹 `l1sw-dev-knowledge`는 현재 코드 기준 HLD·상세 설계·확인된 AS-IS MSC·승인된 설계 변경과 재사용 가능한 기술 이슈 히스토리를 관리한다. 개인 `l1-workspace`는 Work ID·진행 상태·가설/초안·수정·시험·리뷰·Evidence 원장의 정본이다. 그룹 게시 뒤에도 Work/Evidence를 삭제·이관하지 않고 게시 revision을 연결한다.

상세도는 GROUP/PERSONAL routing 조건이 아니다. 그룹 내용 범위 허용은 자동 write·overwrite 승인과 다르다. 모듈/피처/시나리오 기존 ID와 구조를 우선 사용한다. 현행 K5.8 tier 이름·번호·우선순위는 아직 확인하지 못했으며 임의로 발명·교체하지 않는다.

정책 우선순위: 이전 인계의 S01을 ‘진행 중 ISSUE는 항상 그룹 미게시’로 해석하는 부분은 이 문서의 원인 지식 조건으로 대체한다. 미검증 메모·가설은 개인 Work에 유지한다. 검증된 원인은 수정 미완료 표시와 별도 검증·승인을 거쳐 그룹 후보가 될 수 있다. 기존 Work 및 원본 설계의 과거 기록은 보존한다.

## 2. 책임과 호출 방향

| 구성요소 | 소유 책임 | 경계 |
|---|---|---|
| Workflow (`l1-fix-workflow`) | 요청 intent·Work 선택/재개·분석 호출·후보 인계 | 그룹 본문 임의 write 금지; Work 분류를 Kernel profile로 자동 전환 금지 |
| Kernel (`work-ledger-kernel`) | 실제 Work ID·Work 상태·허용 Evidence·원장 및 파생 export | 기존 record/schema/registry/export 소유권 유지 |
| code-analyzer 및 Git/P4 보조 | 고정 입력의 코드 사실·분석 근거·AS-IS MSC 후보 | 분석 성공은 승인·수정 완료·런타임 검증이 아님 |
| 기존 Knowledge Updater | K5.8/K6·기술 분류·후보·중복/충돌·Preview·승인/기존 writer 조정 | Work 원장 대체·Work ID 별도 발급 금지 |
| 기존 설계/HLD/변환 기능 | TO-BE 설계와 표현 변환 | 실제 작성·승인 책임은 G0 확인; analyzer가 TO-BE 승인 권한을 얻는 것으로 해석 금지 |
| 기존 RAG driver/Job 경계 | 접근·source/owner/root·최종 본문/payload 검증 | 링크 검색 또는 게시 성공만으로 M1 PASS 금지 |

Updater에서 코드·이슈 분석으로 진입해도 Workflow의 기존 Work 선택 기능을 통과한다. Workflow에서 진입하면 Work/Evidence를 먼저 보존하고 기존 ArtifactRef를 Updater에 전달한다. Updater가 같은 분석을 다시 호출해 새 Work를 만들지 않는다.

두 진입점은 공통 operation/request 상관키를 전달하고 기존 Work 소유자에서 원자적으로 resolve/resume한다. 실제 구현에 원자적 생성 기능이 없으면 승인된 기존 직렬화 경로를 확인한다. 새 Work 엔진은 만들지 않는다. 기존 순수 스터디·문서 편집에 Work를 강제할지는 설치본 조사 후 정하며 모든 요청에 새 Work를 만들지 않는다.

## 3. K5.8 분류·검증·게시 축

`knowledge_kind`, Work 목적, artifact 종류, 기술 탐색 분류, 기존 실행 profile/work_purpose는 독립 축이다. 논리 예시를 현재 설치 enum 또는 Kernel Evidence kind로 취급하지 않는다.

`validation_state`를 단일 상호배타 enum으로 저장하지 않는다. 다음 의미를 각각 증거와 scope에 연결한다. 필드명·enum은 현행 계약에 매핑한다.

| 독립 축 | 필요한 의미 | 근거 |
|---|---|---|
| 원인 | 가설/근거로 지지됨/반증/불명 | 주장·방법·조건·반례·Evidence |
| 설계 | 초안/승인/승인 철회 | 설계 revision·승인 영수증 |
| 구현 | 미반영/반영/revert/불명 | 제품·브랜치·variant별 소스 snapshot |
| 시험 | PASS/FAIL/SKIP/NOT_RUN | 시험 버전·대상 snapshot·환경·범위 |
| 현재성 | 적용 일치/불일치/불명 | 요청 scope와 검증 기준 비교 |
| 지식 생명주기 | active/superseded/retracted | 대체 revision·정정 이유 |
| 게시 | 후보/Preview/승인/게시 진행/게시 확인 등 | 게시 operation·승인·원격 영수증 |
| 역링크 | 미연결/일부 연결/전부 확인 | Work별 LinkReceipt |

예를 들어 원인 검증됨 + 수정 미반영 + 시험 NOT_RUN을 동시에 표현한다. 시험 FAIL이 원인 검증 이력을 지우지 않으며, 과거 snapshot의 PASS를 새 snapshot의 PASS로 승계하지 않는다. STALE은 현재 요청과의 적용 관계이고 과거 검증 사실 자체를 삭제하지 않는다. UNCLASSIFIED는 Work 목적 미확정이며 artifact 검증 상태와 다르다.

원인만 검증된 이슈의 그룹 후보 조건: 원인 주장, 고정 소스/관측 근거, 검증 방법·검증자·시점, 적용 조건, 미확인 사항·반례, 수정·시험의 독립 상태를 명시한다. 정적 증명과 런타임 재현은 구분한다. 코드와 조건으로 충분히 입증한 원인은 그 범위에서 게시 후보가 될 수 있지만 관측하지 않은 런타임 동작까지 확정하지 않는다. 회피책의 효과도 별도 검증하며 원인 검증만으로 자동 승인하지 않는다.

원인 검증/설계 승인/수정 통합/시험 확인을 하나의 RESOLVED로 합치지 않는다. FIX_INTEGRATED는 해당 적용 브랜치·제품에서 실제 통합이 확인된 사실이며 다른 브랜치·제품으로 전파하지 않는다.

## 4. typed SourceSnapshot과 실제 입력

SourceSnapshot은 SCM revision과 analyzer가 실제 읽은 입력을 함께 고정한다. 모든 회사 근거·원문·내부 경로는 인가된 사내 공간에만 보관한다.

- 공통: `snapshot_id`, `source_authority_ref/root_ref`, 제품/RAT/release/build 조건, module/feature/scenario 및 파일 scope, 실제 입력 manifest/digest, tree state, capture 시점, 일관성 확인 근거.
- Git: full commit SHA, requested branch/ref는 계보·표시 정보, 필요한 경우 tree/submodule/dependency pin. committed tree와 materialized 파일·generated 설정·분석 조건의 차이를 확인한다. 같은 SHA만으로 다른 제품/build 입력의 동일성을 주장하지 않는다.
- P4: 실제 파일별 file#rev/haveRev 집합, 로컬 content digest·opened 상태, client/CL은 단서. haveRev/단일 CL만으로 실제 로컬 바이트 또는 모든 파일 revision을 대표하지 않는다.
- 변경 분석은 `before`, `after`, `design_target` 등 역할별 snapshot refs를 보존한다. 존재하지 않는 미래 구현 SHA를 만들지 않는다.
- capture 전후의 소스·scope 일관성 확인이 실패하거나 dirty/untracked/입력 불명확 상태이면 현재 코드 VERIFIED 게시를 차단한다. 과거 고정 snapshot 근거는 보존하되 현재 적용성은 별도 평가한다.
- 같은 SHA·동등 입력·scope가 검증되면 여러 branch의 분석을 재사용할 수 있다. 동일 SHA라도 설정·의존성·권한·적용 범위가 다르면 불가하다. 다른 SHA의 backport도 별도 통합·동등성 근거가 필요하다.
- 기존 source-root containment·symlink/범위·owner/권한·버전 가드를 유지하고 scoped manifest를 재사용한다. 수만 파일 전체 재해시를 매 호출에 무조건 수행하지 않는다.

## 5. K6 AS-IS / TO-BE 및 participant

AS-IS MSC는 고정 소스에 존재하는 코드 흐름의 파생 설명이다. 중요한 메시지·조건·상태 변화마다 `claim_id`, `source_anchor_ref`, snapshot, Evidence, 확인 방식, 제한을 연결한다. 필수 메시지 coverage와 추론 메시지를 구분해 전체 문서의 VERIFIED 배지가 미확인 메시지를 숨기지 못하게 한다.

정적 분석의 호출/조건/상수 확인과 실제 task 간 순서·지연·타이밍 보장은 다르다. 런타임 확인이 없는 주장은 INFERRED/UNVERIFIED로 표시한다. 필수 코드 anchor가 누락된 현재 AS-IS 주장은 VERIFIED 게시하지 않는다. 선택적 추론 overlay를 보존해도 사실 근거 RAG 입력과 구분한다.

TO-BE는 설계 revision·승인 상태를 근거로 별도 게시 후보가 될 수 있다. 아직 코드가 없으면 미구현 설계임을 표시한다. 구현 뒤 kind만 바꾸어 AS-IS로 승격하지 않고 실제 소스·근거로 새 AS-IS artifact를 생성·검증하여 `implements/derived_from`으로 연결한다. AS-IS는 코드 검증 게이트, TO-BE는 설계·승인 게이트를 적용한다.

participant는 논리 stable ID와 표시 alias를 분리한다. 가독형 alias 예: TxCfgMngr/TxCmdMngr → TxMngr, BCH_CTRLR → BCH, DRX_CTRLR → DRX, RF_BLOCK → RF_BLOCK. 원시 절대 경로를 stable ID로 고정하지 않고 기존 module ID를 우선 재사용한다. 여러 source를 한 actor로 합치는 것은 명시된 alias map으로만 수행한다. map 버전·동명 충돌·rename과 doc-converter 왕복에서 ID·상태·anchor를 보존한다. participant ID는 담당 owner와도 다르다.

Work에서 생성한 원본 분석·Evidence는 보존하고 그룹의 고정 게시 revision에 연결한다. 그룹과 개인에 독립적인 ‘최신 기술 정본’ 두 개를 만들지 않는다.

## 6. 논리 메시지·참조 계약

아래는 필수 의미이며 새 사내 API/스키마가 이미 존재한다는 뜻이 아니다. 설치본의 허용 필드·기존 연결 기능에 먼저 매핑한다.

| 객체 | 필수 의미 필드 |
|---|---|
| 공통 envelope | contract_version, operation_id, request_id, request_digest, actor_ref, producer_contract_version |
| WorkContext | ledger_instance_id, 실제 Kernel work_id, work_revision, 요청 scope, source_snapshot_refs[] |
| EvidenceRef | ledger_instance_id + work_id + evidence_id, 실제 producer/등록 slot, content_digest |
| SourceSnapshot | snapshot_id, authority/root ref, 기술·build scope, SCM pins, 실제 입력 manifest/digest, tree state, captured_at, capture_guard_ref |
| ArtifactRef | artifact_id, origin_work_refs[], producer/version, artifact_kind, content_digest, evidence_refs[], claim/anchor refs, 역할별 snapshot refs, retention_ref |
| KnowledgeCandidate | candidate_id/revision, knowledge_id, variant_id, origin_work_refs[], artifact_refs[], scope_before/after, 역할별 source refs, target_store_id, operation, expected_base_revision, write_set[], manifest_digest |
| ApprovalReceipt | candidate revision/manifest_digest, target/scope/expected base, source·근거 집합, 승인자·허용 동작·정책 revision·유효성 조건 |
| PublicationReceipt | publication_id, operation_id, candidate revision/digest, knowledge_id/variant_id, approval_ref, 실제 writer, publication_revision/write_commit, 최종 원격 content_digest, readback_ref/status |
| WorkLinkReceipt | Work ref + knowledge/variant ID + 고정 publication_revision, 연결 writer 영수증, Work별 링크 상태 |

work_id는 Kernel이 발급한 불변 opaque ID를 그대로 사용한다. 요청 해석 단계만 optional이며 코드/이슈 분석과 후보 인계 전 확정한다. primary Work를 유지하더라도 후보의 복수 origin Work와 namespace Evidence refs는 손실 없이 보존한다.

content digest에는 hash algorithm과 canonicalization 계약이 필요하다. approval은 diff digest뿐 아니라 실제 최종 본문·참조·scope·정책을 포함하는 불변 manifest를 식별한다. renderer/metadata 추가가 승인 대상 결과를 바꾸면 재검토한다.

server가 나중에 반환하는 write_commit/publication_revision은 candidate digest 밖의 receipt 필드로 관리해 자기 참조 해시를 만들지 않는다. 본문에 자동 metadata를 넣는다면 승인된 템플릿·허용 필드·canonicalization 범위를 사전에 명시하고 승인 본문 변경을 숨기지 않는다.

같은 request/operation 키의 같은 payload 재시도는 기존 결과를 반환한다. 같은 키·다른 payload는 거부한다. 분석 재사용 키는 Work·snapshot·scope·producer 계약 버전으로 구분한다. 유사한 자연어만으로 서로 다른 분석을 합치지 않는다.

기존 Evidence registry 밖의 kind/provider를 가장하지 않는다. `code_review`, `issue_review`, `p4-code-owner` direct provider가 지원된다고 가정하지 않는다. 공개 개발 후보의 허용 슬롯 근거는 사내 설치본 지원 증거가 아니므로 G0에서 대조한다. record.json·Evidence 객체에 임의 필드를 넣거나 생성형 README/index/문서안내를 직접 덮어쓰지 않는다.

연결 manifest/sidecar를 사용할 경우 기존 Updater 또는 허용 connector의 writer·CAS·보존·revision 소유권을 정한다. 이 manifest는 Work 상태 SSOT가 아니다. 링크를 저장·노출할 허용 계약이 없으면 INTEGRATION_BLOCKED이며 원장을 임의 확장하지 않는다.

## 7. 지식 단위·N:M·부분 갱신·정정

stable knowledge_id는 제목·경로 rename에도 유지한다. 제품/RAT/release/source 계열이 다른 동시 유효 지식은 variant로 구분한다. branch 이름만으로 전역 최신본을 선택하지 않는다. 한 Work→여러 지식, 여러 Work→한 지식의 N:M 계보와 승인자·정보등급·읽기 권한을 보존한다.

기술 이슈 단위에는 scope, symptom(관측/추정 분리), root_cause, design_change, fix, verification, reusability, provenance가 필요하다. design-change는 제안/승인/실제 적용 범위를 구분한다. fix/verification은 variant별 source에 연결한다.

write_set 각 항목은 document_id, section_or_scenario_id, expected_base_revision, patch_digest, resulting_content_digest를 가진다. 변경 영향은 기존 관계를 재사용하여 describes/implements/derived_from/verified_by/supersedes 등으로 추적한다. 기존 문서 전체를 무심사 overwrite하지 않는다.

같은 저장소면 관련 HLD·상세설계·MSC·이슈 변경을 기존 원자적 commit으로 묶는다. 여러 저장소이면 승인된 게시 집합의 부분 적용 상태를 기록하고 불완전 조합을 일관된 현재 정본으로 활성화하지 않는다. 새 분산 트랜잭션 엔진을 앞서 만들지 않고 기존 writer 보장을 G0에서 확인한다.

원인 반증/지식 정정/승인 철회/코드 revert 시 과거 Work·Evidence·게시 영수증은 보존한다. 잘못된 현재 주장에는 정정/철회 revision과 이유를 남기고 의존 지식을 재평가한다. 과거 시험 PASS는 그 snapshot의 이력으로 유지하며 현재 구현 상태만 재판정한다. 현재 포인터·인덱스·검색 캐시의 회수 반영을 확인한다.

## 8. 승인·CAS 게시·응답 유실·역링크 복구

1. 권한 있는 기존 writer의 게시 operation과 불변 후보 manifest를 원격 write 전에 영속 보존한다. 원격 게시에도 같은 operation을 식별할 정보를 남겨 commit 응답 또는 로컬 receipt 유실 후 재조회할 수 있어야 한다.
2. 승인은 후보 revision/digest·목적지·variant·expected base·source/근거 집합·허용 동작·정책/유효성 조건에 묶는다. writer 경계에서 권한·승인 철회/만료와 조건 일치를 재검증한다. 실제 원자적 권한/정책 보장 방식은 기존 writer 계약으로 확인하며 불가능하면 BLOCKED로 둔다.
3. source snapshot은 보존하되 CURRENT 적용 주장이 승인 후 drift하면 재검토한다. 명시적으로 승인한 과거 pinned 지식은 과거 상태로만 게시/조회한다. 대상 revision만 같다는 이유로 source·근거·정책 변경을 무시하지 않는다.
4. UPDATE는 expected base를 CAS로 대조한다. CREATE는 expected=ABSENT를 확인한다. 충돌 시 기존 승인을 무조건 재사용하지 않고 Preview/조건을 다시 검증해 필요한 승인을 재취득한다.
5. 원격 write 성공 후 승인한 결과 manifest·바이트/digest와 원격 revision을 readback한다. 불일치면 거짓 완료로 기록하지 않는다.
6. timeout·프로세스 재시작·응답 유실은 새 후보/operation을 만드는 이유가 아니다. 원격 operation과 내용/commit 이력을 대조해 같은 게시가 확인되면 receipt를 복구한다. authoritative no-write가 확인되고 조건이 유효한 경우에만 같은 operation의 통제된 재시도를 허용한다. 확정 불가면 HOLD/RECONCILIATION_REQUIRED이며 임의 재게시하지 않는다.
7. 게시 확인과 Work 역링크는 독립 상태다. 복수 origin Work의 LinkReceipt를 각각 정산한다. 일부 실패는 PUBLISHED_LINK_PENDING이고 그룹 재게시 없이 링크만 복구한다. 지원되지 않는 Kernel 필드/README 직접 편집으로 복구하지 않는다.

게시 상태(논리 예): CANDIDATE → PREVIEWED → APPROVED → WRITE_PENDING → PUBLISHED_READBACK. 실패 분기는 REVIEW_REQUIRED / CONFLICT / RECONCILIATION_REQUIRED / HOLD로 남긴다. 링크 상태는 별도로 NONE / PARTIAL / ALL_CONFIRMED이다. 두 상태를 한 enum으로 덮어쓰지 않는다.

## 9. RAG 및 정보 보호

GROUP_PUBLISHED는 게시 사실이지 현재성·코드 확인·런타임 검증·수정 완료가 아니다. 권한 → 제품/RAT/release/build/source scope → 주장 종류·상태 → 현재성을 순서대로 판정한다. 그룹 최신 문서라는 이유로 질문에 맞는 branch 근거보다 우선하지 않는다.

| 질의 목적 | 허용 근거 |
|---|---|
| 현재 코드 동작 | 해당 source 적용성과 코드 주장 근거가 확인된 지식 |
| 설계 의도/계획 | 승인·미구현 여부가 표시된 설계 |
| 이슈 원인 | 검증 범위·수정 미완료가 표시된 원인 주장 |
| 진행 상태 | 접근 가능한 개인 Work/Evidence |
| 과거 동작 | 과거 source와 publication revision에 고정된 지식 |

UNKNOWN/STALE 또는 적용 불명 근거를 현재 사실로 사용하지 않는다. 적합 근거가 없으면 불충분함을 표시하고 자동으로 새 분석/모델 호출을 시작하지 않는다. 그룹 reader가 개인 Work 원문을 볼 권한이 없으면 승인된 그룹 설명만 제공한다.

RAG M1은 실제 retrieved body/anchor/digest → trusted driver → Provider 최종 입력의 동일성, source/owner/root/권한/버전·Job gate와 receipt가 확인되기 전 BLOCKED이다. body·payload hash를 Provider 자기 보고만으로 신뢰하지 않는다. 검색/게시/본문 소비 게이트는 독립이다. 권한 철회·지식 정정·cache 변경은 최종 입력 전에도 반영한다.

회사 소스·내부 MSC·고객 자료·내부 경로/로그·토큰은 인가된 사내 경계에 보관한다. 공개 가능한 일반화 설계와 내부 구체 근거를 분리한다. 그룹 게시 승인과 외부 반출 승인은 별개이며 private 여부·링크·해시만으로 반출 권한을 얻지 않는다. 문서 변환·인덱스·sidecar·HTML 내장 데이터·역링크도 같은 정보 분류를 적용한다. 조사 결과는 기본 NO_EXPORT이고 별도 승인 없이 외부 서비스로 보내지 않는다.

## 10. 호환성·단계 이행·완료 게이트

G0에서 실제 tier 규칙과 reader/writer/viewer/exporter를 먼저 조사한다. 기존 tier 값·경로·Work ID·Evidence·수동 문서를 보존한다. 새 metadata는 기존 허용 계약 또는 관리된 sidecar로 점진 도입한다. 구 reader가 중요한 상태를 무시해 현재 사실로 오표시한다면 노출을 제한하거나 PREVIEW_ONLY로 두며 silent fallback하지 않는다.

이행 순서는 읽기 전용 매핑 → 호환 가능한 선택적 metadata 설계 → 승인된 격리 왕복·동시 writer·rollback 검증 → 승인된 범위별 활성화이다. rollback은 새 기능의 노출/쓰기 경로를 중지하고 이전 승인 reader 경로로 복귀하는 설계이며 Work/Evidence/게시 계보를 삭제하지 않는다. 실제 운영 migration·파일 이동·rollback 실행은 이 인계 범위가 아니다.

필요한 최소 변경은 기존 스킬의 REUSE / CONNECT / EXTEND / DEFER로 판정한다. 신규 vector DB·별도 RAG skill·새 Work SSOT·독립 오케스트레이터를 선행 도입하지 않는다. G0 완료는 기능 구현·독립 리뷰·그룹 게시·운영 승인·RAG M1 PASS가 아니다.
## 11. G0 읽기 전용 확인표

아래 항목은 조사 전 모두 AS_IS_NOT_VERIFIED이다. 실제 설치본과 원문을 근거로 항목별 CONFIRMED/GAP/AS_IS_NOT_VERIFIED/BLOCKED를 판정한다. 설치본을 읽은 사실과 API/통합 실행 성공을 구분한다.

| ID | 실제 확인할 내용 | 해소 대상 |
| --- | --- | --- |
| G01 | 실제 설치 버전·release 상태·entrypoint 및 읽기 명령의 쓰기 부작용 | 설치본 기준·조사 범위 |
| G02 | K5.8 전체 tier 원문·우선순위·예외·routing·reader/viewer | KR-01·04 |
| G03 | K6 AS-IS/TO-BE/승인 설계/런타임 확인 규칙과 예외 | KR-11 |
| G04 | 두 진입점의 Work 탐색·재개·동시 생성 차단·상관키 | KR-07 |
| G05 | 설치 Kernel registry·schema/validator parity·exporter 소유권 | KR-08 및 임의 필드 금지 |
| G06 | analyzer 출력 snapshot/anchor·영구 ArtifactRef·Run 보존 정책 | KR-08·10·11 |
| G07 | TO-BE 작성/승인 책임자, converter의 ID·상태·근거 왕복 | KR-11·12 |
| G08 | Git/P4 실제 입력 바이트·build 조건·의존성 고정 방식 | KR-10 |
| G09 | 그룹 stable ID·variant·section·N:M·영향 관계의 현행 저장 계약 | KR-09·13 |
| G10 | 기존 writer CAS·CREATE 충돌·operation 조회·원격 readback 보장 | KR-05·06 |
| G11 | 승인 철회·만료·권한 변경을 writer 경계에서 검증하는 방식 | KR-05 |
| G12 | 구 reader/writer·tier 매핑·메타데이터 보존·점진 이행·롤백 | KR-04 |
| G13 | 정정·철회·revert의 현재 포인터·연관 지식·캐시 처리 | KR-13·14 |
| G14 | 실제 RAG source/owner/root/Job·body/driver/payload 검증 경로 | 기존 M1 차단 유지 |

K5.8/K6 전체 원문·설치 경로·상세 I/O 증거는 사내에만 보관한다. ‘재분류’는 재분류 설계표 작성이며 파일/데이터 이동이 아니다. 자연어 진입점을 호출하면 Work 생성·DB 갱신이 일어날 수 있으므로 G0는 원문·소스·기존 계약의 읽기 전용 확인을 우선한다. 읽기 부작용을 보장할 수 없는 명령은 실행하지 않고 한계를 남긴다. 운영 DB의 WAL/SHM을 포함해 쓰기 영향이 없어야 한다. Work 생성·Evidence 등록·그룹 writer·Job/Provider 호출은 G0에서 실행하지 않는다.

## 12. 부정·회귀시험 계획 T01~T24

다음은 시험 계획이다. 이번 문서 작성·게시 과정에서 상태 전이/스킬/실 API/호스트 시험은 수행하지 않았다. 모든 항목의 현재 상태는 NOT_RUN이다. 기존 문서의 시험 PASS를 이 표로 승계하지 않는다. G0 뒤 명세 확정 → 승인된 격리 구현·시험 → 별도 운영 판정 순서다.

| ID | 시험 | 수용 기준 | 현재 상태 |
| --- | --- | --- | --- |
| T01 | 상세 HLD/MSC와 기존 tier | 상세도만으로 개인-only 강제 0, 기존 tier 보존 | NOT_RUN |
| T02 | 원인만 검증되고 수정 미완료 | 원인/수정/시험/회피책 독립, 미확인·반례 명시 | NOT_RUN |
| T03 | 설계 승인·코드 미반영 | 승인과 구현·시험 별도, AS-IS 승격 0 | NOT_RUN |
| T04 | 새 코드 수정 없는 정적 AS-IS MSC | 고정 근거로 후보 가능, 런타임 추론 메시지 별도 | NOT_RUN |
| T05 | 미구현 TO-BE 및 승인 설계 | 설계 게시와 현행 AS-IS 구분, 자동 승격 0 | NOT_RUN |
| T06 | Branch A/B 상이·동일 SHA 및 build 조건 | 다른 적용 scope 거부, 검증된 동등 scope 재사용 허용 | NOT_RUN |
| T07 | 동시 두 진입점·서로 다른 호출 ID·재시작 | Work/후보/동일 분석 중복 0 | NOT_RUN |
| T08 | CAS 변경·승인 철회/만료·source/Evidence 변경 | 쓰기 0, 조건 재검증·재승인 | NOT_RUN |
| T09 | 게시 성공 후 복수 Work 일부 링크 실패 | 영수증 보존, 링크별 복구, 재게시 0 | NOT_RUN |
| T10 | 구 tier·구 viewer/exporter 왕복 | 원장·tier·새 메타데이터 무손실 또는 안전한 격리 | NOT_RUN |
| T11 | 미등록 slot·schema/runtime 차이·producer 위장 | 등록 계약 준수, 허용 필드 가장/임의 삽입 0 | NOT_RUN |
| T12 | 링크만 전달·다른 본문·payload 변조·권한 변경 | 검색과 M1 분리, 미검증 M1 PASS 0 | NOT_RUN |
| T13 | N:M·variant·section 동시 개정 | 출처 보존, CAS, 관련 문서의 일관된 게시 | NOT_RUN |
| T14 | 승인 후 drift·P4 로컬 변경·anchor 유실 | 현재 VERIFIED 게시 차단, 상태 표시 유지 | NOT_RUN |
| T15 | 게시 원인의 후속 반증 | 정정 계보·현재 주장 회수·의존 재평가 | NOT_RUN |
| T16 | Branch A만 수정·다른 snapshot 시험 | Branch B 수정 완료 및 해당 수정 시험 PASS 오인 0 | NOT_RUN |
| T17 | 원격 commit 후 응답·로컬 영수증 유실 | 동일 operation 게시 복구, 불명확 HOLD, 중복 0 | NOT_RUN |
| T18 | 동일 멱등키·다른 후보/본문/대상 | 요청 거부, 이전 영수증 오재사용 0 | NOT_RUN |
| T19 | 철회·권한 변경 후 검색 캐시 | 최종 Provider 입력에서 자격·접근 차단 | NOT_RUN |
| T20 | participant 충돌·rename·converter 왕복 | stable ID·표시·상태·근거 보존 | NOT_RUN |
| T21 | Run 정리로 artifact/anchor 유실 | 근거 보존 또는 검증 불가 명시, 무근거 재승격 0 | NOT_RUN |
| T22 | HLD/detail/MSC write set 일부 게시 | 원자 적용 또는 명시적 부분 상태, 불완전 현재화 0 | NOT_RUN |
| T23 | 그룹 reader에 개인 Evidence 권한 없음 | 승인된 설명만 제공, 개인 본문·경로 누출 0 | NOT_RUN |
| T24 | legacy mapping 후 구 writer 실행·롤백 | Work 원장·tier·출처·게시 계보 무손실 | NOT_RUN |

각 시험 기록은 종류(정적/합성/격리 통합/실호스트), 명령·입력 revision·환경·수정 파일·실제 PASS/FAIL/SKIP/NOT_RUN·Evidence를 구분한다. 위 시험을 G0 요청에 포함했다고 실제 실행 승인이 된 것은 아니다.
## 13. 사내 결과 문서와 비민감 요약 형식

사내 상세 결과 파일명 제안: `L1_KNOWLEDGE_UPDATER_K58_K6_WORKFLOW_G0_INTERNAL_RESULT_r0004.md`. 경로는 사내 승인된 작업 공간으로 정하고 Work 원장/운영 정본을 덮어쓰지 않는다.

1. 현재 조사 범위·실제 설치 버전·원문 식별 근거. K5.8/K6 원문은 사내에서만 관리.
2. K5.8 tier별 AS-IS 의미·우선순위·예외·routing·reader와 목표 정책 매핑. 실제 값은 원문 그대로 보존.
3. K6의 현재 생성/검증/저장/승격·participant·설계 승인·변환 규칙과 차이.
4. producer/consumer·Work/Evidence/기술 지식 소유권 및 두 진입점 호출 그래프.
5. G01~G14 결과와 근거 수준, 기존 기능의 REUSE/CONNECT/EXTEND/DEFER.
6. KR-01~KR-14별 수용/수정 수용/거절/보류/추가 정보 필요, 최소 변경 파일·호환성·rollback·시험 계획. ID는 설계 추적용이며 Kernel Evidence kind가 아니다.
7. T01~T24 실제 상태와 실행 증거. 미실행은 NOT_RUN.
8. 승인/CAS·operation 복구·역링크·정보등급·RAG M1에서 남는 차단과 다음 한 동작.

이 문서만으로 추적할 설계 점검 ID:

| ID | 점검 내용 | 관련 절 |
|---|---|---|
| KR-01 | 독립 검증·게시·링크 상태 | §3 |
| KR-02 | 수정 전 원인 검증 조건 | §3 |
| KR-03 | 기존 S01 해석과 정책 우선순위 | §1 |
| KR-04 | 현행 tier·reader·이행/롤백 | §10 |
| KR-05 | 승인 바인딩·게시 직전 권한/source 재검증 | §6·8 |
| KR-06 | 영속 operation·응답 유실 정산 | §8 |
| KR-07 | 두 진입점 Work·분석 중복 차단 | §2·6 |
| KR-08 | namespace·N:M·before/after 근거 | §4·6·7 |
| KR-09 | section/variant·관련 문서 일관 갱신 | §7 |
| KR-10 | 실제 입력·build·P4 로컬 상태 | §4 |
| KR-11 | MSC 주장별 근거·설계/코드 게이트 | §5 |
| KR-12 | participant stable ID·변환 왕복 | §5 |
| KR-13 | 반증·정정·revert·cache 회수 | §7·9 |
| KR-14 | RAG 검색 자격·현재 코드 오인 방지 | §9 |

비민감 추상 후보는 다음 범주형 형식으로만 별도 작성할 수 있다. 이것도 기본 사내 보관이며 외부 전송을 요구하지 않는다.

```text
review_kind: INHOUSE_G0_READ_ONLY
overall: CONFIRMED_WITH_GAPS | AS_IS_NOT_VERIFIED | BLOCKED
checks:
  - check_id: G02
    result: COMPATIBLE | CHANGE_REQUIRED | AS_IS_NOT_VERIFIED
    basis: INSTALLED_SOURCE | HOST_READ_ONLY | NOT_RUN
    conclusion_code: LEGACY_MAPPING_REQUIRED
    detailed_evidence: INTERNAL_ONLY
next_gate: SPEC_REVISION | ISOLATED_TEST_DESIGN
export_status: NO_EXPORT
```

요약에 실제 tier 원문·내부 경로·Work ID·CL·MSC·코드·로그·토큰을 넣지 않는다. 필요 시 별도 정보 분류/승인으로 허용 범위를 결정한다.

## 14. 사내 GPT 원샷 요청

> 첨부된 이 r0004 인계서만으로 작업을 시작해 줘. 현재 설치된 l1-knowledge-updater의 K5.8 tier 전체 원문과 K6 MSC 정책 전체 원문을 사내에서 먼저 읽고, Workflow·Kernel·analyzer·Git/P4·기존 writer/reader의 실제 I/O와 소유권을 G01~G14에 따라 읽기 전용으로 조사해 줘. 필요한 인가된 사내 OpenCode/Agent에는 같은 G0 읽기 전용 범위만 위임하고, 실제 설치 원문을 보지 않은 기능은 AS_IS_NOT_VERIFIED로 남겨 줘. 기존 tier·사용자 경로·원장·Evidence·생성 문서·그룹 정본을 바꾸지 말고 AS-IS→목표 정책의 재분류 설계표만 작성해 줘. 그룹은 현재 코드 HLD/상세 설계/AS-IS MSC/승인된 설계 변경/재사용 가능한 기술 이슈 히스토리를, 개인은 Work/진행·수정·시험·리뷰/Evidence 원장을 소유한다는 목표를 검토하되 실제 기능을 재사용하고 최소 수정으로 조정해 줘. 원인 검증/수정 통합/시험 PASS를 분리하고, N:M 출처·실제 SourceSnapshot·승인 바인딩·CAS·응답 유실·역링크 복구·legacy mapping·RAG 자격 조건을 확인해 줘. REUSE/CONNECT/EXTEND/DEFER, 최소 변경 파일 후보, T01~T24 격리시험·rollback 계획과 남은 블로커를 사내 결과 문서에 한 번에 정리해 줘. 조사 중 Work 생성/Evidence 등록/그룹 write/스킬 설치·수정/운영 DB·작업 변경/모델·Job 호출/외부 전송은 하지 마. 읽기 명령의 부작용이 불명확하면 실행하지 말고 근거와 한계를 기록해 줘. 미확인은 NOT_VERIFIED, 미실행은 NOT_RUN으로 보고해 줘.

완료 조건은 실제 설치본에 근거한 매핑·최소 변경/시험 계획·차단 판정이다. 조사 완료를 구현 완료·그룹 게시·독립 리뷰 PASS·운영 승인·RAG M1 해제로 올리지 않는다. 다음 한 동작은 G0 결과로 명세를 확정하는 것이다.
