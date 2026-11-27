# LTE/NR L1 Source Map 구성안과 업무 GPT 통합 인계

**r0003 확정 구성 · R2 독립 리뷰 반영 · 2026-11-27 KST · L1-WORKSPACE-RAG-20261111-001 · 대상: 업무 GPT / l1-knowledge-updater 담당**

약 1,500개 파일에는 **전체 경량 목록 → 모듈·빌드별 정적 관계 → 질문별 원문 확인**의 세 단계를 권장해요. 기존 Discovery 7건과 Analyzer를 먼저 사용하고, 선택한 build에서 동일 이름·호출 대상을 구별하지 못한 사례가 반복될 때 로컬 Clang 계열을 시험해요. 제품 자료, 활성 도구, 실행 LLM 및 실제 품질 수치는 업무 환경 확인 대상이에요. 이 문서는 기존 통합 설계 r0002를 바탕으로 업무 GPT에 전달할 콘텐츠·운영 설계를 확정한 r0003예요. 첫 단계는 G0 읽기 확인이고, 제품 환경 확대는 §8 실측으로 판정해요.

## 1. 업무 GPT에 전달할 요청문

> 기존 Work L1-WORKSPACE-RAG-20261111-001에서 G01~G06부터 읽기 전용으로 확인해 주세요. 기존 NR/LTE Discovery 7건 각각을 3절의 표에 매핑해 주세요. 파일별 revision·build·조사 범위·추출 방식·원문 검증을 비교해 재사용, 부분 보완, 충돌·미확인으로 판정해 주세요. 이미 설정된 소스 위치와 권한을 먼저 확인하고, 실제 작업 위치가 식별되지 않을 때만 담당자에게 확인해 주세요. 전체 목록의 분모를 고정하고 대표 모듈 한 곳에서 직접 호출, 메시지 등록·송신, 빌드 분기 세 종류를 우선 검증해 주세요. 각 후보에는 양 끝 ID, 방향, guard, 원문 근거와 불확실성을 붙여 주세요. 5절의 예시와 6절의 절차를 사용하고 실제 결과와 제품 원문은 업무 Work에 보존해 주세요. 회신은 8절 형식으로 주세요.
>
> 기존 설계 저장소는 wonhwipark/CoWork-Skill-Collab, branch main, collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_SOURCE_MAP_LLM_FIRST_INTEGRATED_DESIGN_r0002_20261127_KST.md예요. 기존 업무 인계는 wonhwipark/L1Work, branch main, handoffs/L1_SOURCE_MAP_KNOWLEDGE_UPDATER_VIEWER_SCOPE_HANDOFF_r0001_20261127_KST.md예요. 이 자료들은 설계 전달용이에요. 스킬 실행 시 CoWork 접근·인증을 전제로 삼지 마세요.

**역할**　Updater가 발견·대조·정규화·갱신·승인된 Writer 저장 요청과 readback을 맡아요. Analyzer는 코드 근거, Recovery는 V2 정상 규칙·V3 후보 검증, Viewer/MCP는 승인된 읽기를 담당해요. Module에는 책임·구조, Feature에는 상태·조건의 의미, Procedure에는 API 계약, Scenario에는 정상/예외 흐름과 기존 MSC를 보존해요. Map은 관련 ID·문서 revision·참조 위치만 연결하고 분석 원문은 Work/Evidence에 둬요.

## 2. 기존 설계와 실제 배포 후보 대조

CoWork main 5abefaed2fb6 및 L1Work main 9134db8028f3 기준이에요. 사용자가 제공한 검토 요청 파일 L1_SOURCE_MAP_1500_FILES_LTE_NR_REVIEW_WORK_HANDOFF_r0002_20261127_KST.md의 SHA-256은 487c4a6c46cdc71a99c10f37a6d1c9d96e6a4afe80bd1d71c5cc2b96785abf62예요. 원격 패키지 다섯 개를 다시 읽어 ZIP CRC·경로와 원문을 확인했어요. §9 시험은 설계 GPT가 격리 Linux에서 실행했어요. Windows 리뷰어는 인계서 r0002 한 파일을 정적으로 읽었어요. 외부 URL·해시와 시험 결과의 독립 재현은 리뷰 범위 밖이었어요.

| 대상 | 실제로 확인한 기능·한계 | 판정 |
|---|---|---|
| 통합 설계 r0002와 업무 인계 3종 | 설계 §3~6에 데이터·조회·갱신·예산이 있음. 책임 경계 인계에는 일부 관계와 합성 조회 한 행, G0 인계에는 현장 질문, 패키지 인계에는 개발 회귀가 있음. 약 1,500개에서 사용할 방향별 추출표와 작성 완성 예시는 여러 문서만으로 조립해야 했음 | 이 문서 3~6절로 보완. 기존 상세 설계와 R1 지적·판정 보존 |
| 업무 GPT의 Updater·Discovery·Recovery | 기존 Updater r0002에 index-first, 분석 범위, Analyzer·Converter 사용, 그룹 비교·승인 절차가 있음. 활성 스킬 원문 및 7건 원본은 업무 환경에 있음 | **CONNECT**. 기존 결과와 물리 형식을 먼저 매핑. Recovery는 후보의 신뢰도와 지도 밖 검증 경로를 보존 |
| Analyzer v0.15.7 | bin/code-analyzer.py의 probe 및 scripts/ca_core/probe_engine.py 확인. symbol은 주석도 출현으로 반환. callers/callees는 기존 structure의 call_edges와 원문 호출 표기를 대조. dispatch 테이블 유사 패턴·callback 등록은 후보일 수 있음. compile-condition은 정적 분기와 실제 활성 여부를 분리 | 기존 probe를 사용. Updater에서 명제·범위·증거 수준을 변환. 구분할 수 없는 실제 사례가 남을 때만 Analyzer 확장 |
| Viewer v0.5.8 | assets/source-map.js, adapters/adapter.js에서 exact symbol/Message ID, module/build, 최대 50행, 오류·stale·권한, Knowledge 이동 확인. 현행 adapter는 합성 fixture | **표시 재사용**. 실제 호스트의 인가·snapshot·문서 revision 계약을 대조. UI의 50행 제한은 모델 토큰 또는 서버 인가 검증과 별개 |
| Kernel v0.7.47 | work_ledger_kernel/work_ux.py의 export_docs가 Work·index를 관리. 이전 합성 export에서 지도 표식과 지식 보존. 제품 Writer 검증 자료는 없음 | **REUSE**. 지도 생성기를 Kernel에 두지 않음. 현장 export 전후 hash와 경로 보존 검사 |
| Workflow v1.6.75 / Converter v0.2.26 | knowledge_input.py·msc_view.py의 인용·동일 Work 열람, msc_tool.py·scenario_ir_adapter.py의 기존 MSC 표현 확인 | **REUSE**. 분석 결과가 지식/MSC로 발전할 때 기존 경로 사용 |
| Writer / 업무 MCP | 활성 actor, 경로, 기대 revision 비교·읽기 권한은 미확인 | G03·G04에서 검증. 검증된 쓰기 경로가 없으면 후보와 기존 활성본 보존 |

[기존 상세 설계](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/3ee216ff501172a164958e91106053c1ed6cd1f9/collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_SOURCE_MAP_LLM_FIRST_INTEGRATED_DESIGN_r0002_20261127_KST.md) · [이전 독립 리뷰의 GPT 판정](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/5abefaed2fb6d6b9f28e1d0a34e1b36d8e08cde7/collab/projects/L1-WORKSPACE-RAG-20261111-001/GPT_SOURCE_MAP_R1_REVIEW_DISPOSITION_r0001_20261127_KST.md) · [책임 경계](https://github.com/wonhwipark/L1Work/blob/9134db8028f3d2acbf81e7067c5a7c6721e44351/handoffs/L1_SOURCE_MAP_KNOWLEDGE_UPDATER_VIEWER_SCOPE_HANDOFF_r0001_20261127_KST.md) · [G0](https://github.com/wonhwipark/L1Work/blob/9134db8028f3d2acbf81e7067c5a7c6721e44351/handoffs/L1_SOURCE_MAP_LLM_FIRST_G0_HANDOFF_r0001_20261127_KST.md) · [개발 전달](https://github.com/wonhwipark/L1Work/blob/9134db8028f3d2acbf81e7067c5a7c6721e44351/handoffs/L1_SOURCE_MAP_VIEWER_ANALYZER_DEVELOPMENT_DELIVERY_r0001_20261127_KST.md) · [기존 Updater 계약](https://github.com/wonhwipark/L1Work/blob/9134db8028f3d2acbf81e7067c5a7c6721e44351/handoffs/L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0002_20261125_KST.md)

## 3. 어떤 코드 정보를 어떤 방향으로 기록할지

P0 유형부터 기존 도구가 찾은 범위와 빈틈을 기록해요. **최초 작업 순서**는 전체 파일 분모와 build를 고정한 뒤, 공통 헤더와 복수 variant를 쓰는 대표 모듈 한 곳에서 표의 P0 여섯 분류를 작성하는 순서예요. 도구가 반환한 출현 행만 있는 경우에는 출현을 확인한 명제까지만 저장해요. P1은 대표 모듈에서 필요한 질문부터, P2는 P0/P1로 답할 수 없었던 질문을 보존한 후 선택해요. 같은 사실의 역방향 검색은 기존 간선을 반대로 조회해요. 별도 파일 11개나 신규 DB를 요구하는 분류가 아니에요.

| 우선 | 추출 대상 | 저장 방향과 관계 | 확인 근거와 보류 조건 |
|---|---|---|---|
| P0 | 파일·모듈·RAT·공유 헤더 | Module → File (contains), 포함한 File → 대상 File (include) | 정책상 허용된 상대 경로, include 위치, build별 해석. Common 파일의 ID를 유지하고 LTE/NR 사용처 연결. 동명 헤더나 생성 경로 미해소는 후보 |
| P0 | 함수·클래스·구조체·열거형·매크로 | File → Entity (declares/defines), 타입 → 필드 (contains) | qualified name, signature/qualifier, 정의·선언 anchor. C의 파일 정적 심볼, 익명 namespace는 TU/linkage, 템플릿은 원형/특수화, 매크로는 정의·사용 범위를 구별 |
| P0 | 직접 호출 | 호출자 → 피호출자 (calls) | 호출 위치와 양 끝 선언·정의를 대조. 철자 일치는 호출 표기. overload, virtual, 함수 포인터, 매크로 대상 미결정이면 개별 후보. 역조회로 callers 제공 |
| P0 | IPC·메시지 | 송신 함수 → Message ID (sends), 수신 Handler → Message ID (receives), Message ID → Payload 타입 (payload) | 송·수신 API의 실제 계약, enum/ID, typed payload와 소스 anchor. 동일 번호라도 인터페이스·방향·build가 다르면 분리. REQ/CNF/IND 대응은 등록·명시 매핑·기존 검증 근거가 있을 때만 연결 |
| P0 | 등록·분기 전달 | 메시지 키를 포함한 등록 슬롯 → Handler (registers), dispatch 지점 → Handler 또는 후보 (dispatches) | 테이블 타입·초기화, switch case, 조회 키와 간접 호출을 각각 증빙. 테이블 키 조회·단순 switch-case 모두 대상 전달이 있으면 dispatches로 기록하고 pattern을 table_lookup/switch_case로 구별해요. registers는 별도 등록 근거가 있을 때만 생성해요. 단순 인자 쌍은 후보. 등록·정적 도달·런타임 관찰을 분리 |
| P0 | 전처리·빌드 | 정의·호출·등록 관계에 guard 및 variant를 부착 | 분기 anchor와 앞선 형제 분기 배제. build 식별자, 플래그/생성 헤더/target 근거가 있으면 해당 build 활성 여부를 별도 기록. 미확인이면 UNKNOWN |
| P1 | 상태·구조체 필드 | 함수 → 상태 변수/필드 (read, write) | 선언·소유 인스턴스, 대입 또는 참조 위치. 읽기-수정-쓰기는 양쪽 근거. 동명 지역변수는 분리하고 alias를 통한 쓰기는 미해소 후보 |
| P1 | 인터페이스 경계 | send/receive/dispatch 양 끝에 L1C·HAL·RF·PHY 같은 확인된 모듈/인터페이스 ID 연결 | 소속 정의·실제 API/등록 계약. 디렉터리명·메시지명만으로 계층을 결정하지 않음 |
| P1 | Stack / Domain / Cell / CC | 접근 함수 → 문맥 키·매핑 변수/테이블 (read 등 기존 관계), 관계에 적용 인스턴스 범위 | 인덱스 계산 또는 테이블 정의와 guard·build, 값을 설정하는 근거. 숫자가 같아도 다른 RAT/인스턴스는 분리 |
| P1 | 비동기 Timer / Event / Callback | 등록·취소 지점 → 이벤트/콜백 슬롯, 호출 지점 → 가능한 대상 (callback, 세부 동작 구분) | 등록·교체·취소 anchor와 유효 범위. 여러 포인터 대상 미해소는 UNKNOWN. 실행 순서 및 timeout 원인 판정은 별도 |
| P1 | 기존 Knowledge·Work | Entity/관계 → 문서 ID·문서 revision·섹션/MSC (knowledge_ref), 근거 → 기존 Evidence ref | 소스 기준·문서 revision·서버 인가 일치 시 연결. 없는 링크는 비워 두고 Work의 기존 증빙 참조 |
| P2 | 데이터 전달·alias | 출발 필드/쓰기 → 도착 인자/읽기 후보, 중간 대입의 증빙 연결 | 명시 대입·타입·build에서 시작. 간접 경유·함수 간 alias는 후보와 반례 구분. 포인터 전체 추론은 구체적 실패 사례별로 판단 |

**모든 레코드가 갖춰야 할 의미**

| 단위 | 필수 의미 | 미확인·선택 처리 |
|---|---|---|
| Snapshot | ID, source identity/revision, build 또는 unknown, 범위/제외·coverage, producer/version·추출 방법, 내용 해시·이전 snapshot | build가 없으면 lexical 목록 이용 가능. build별 사실 확정은 보류. 최초 버전은 predecessor 없음 |
| Entity | ID, kind, 구별 가능한 이름, 소속·파일/심볼/범위 anchor, snapshot | signature는 함수에만 적용. 동일성 해소에 필요하면 TU·linkage·template/variant·생성 출처. 줄번호는 위치 힌트 |
| Relation | 고유 양 끝 ID 또는 식별된 미해소 슬롯, 방향·종류, snapshot, 적용 guard/build, evidence ref, 무엇이 확인됐는지 | 서로 다른 미해소 대상은 별개 후보. 정적 후보·확정된 코드 사실·관찰 Evidence를 구별. 확인된 리턴/ACK만 명시적 대응 |
| Evidence | 원본 revision/build, 상대 파일·심볼·범위 또는 기존 Work ref, hash·검증 방법과 검증 명제 | 제품 원문·절대 경로·로그는 업무 환경 보관. 미검증 행의 근거는 후보 생성 위치까지 표시 |
| 상태·Gap | 생성 방법(parser/tool/LLM/manual/unknown), 추출(EXTRACTED/INFERRED/UNKNOWN), 검증(VERIFIED/UNVERIFIED/CONFLICT), 소비 시 freshness, 조사/제외/잘림, 다음 확인 | 파일/관계 유형/variant별 분모 따로 기록. 추출과 원문 대조를 독립 보존. 인가된 범위에서만 gap 표시 |

## 4. 최초 구축·저장·증분 갱신

| 순서 | 입력 → 작업·담당 | 결과 / 실패 시 처리 |
|---|---|---|
| 1. 현황 고정 | Updater가 G01~06, 승인된 루트·source revision, 실제 build/config, 기존 manifest 7건·Work를 조회 | 7건 각각 재사용·부분 보완·충돌/미확인. 소스 기준 다른 두 행을 이름만으로 합치지 않음 |
| 2. 전체 경량 목록 | 기존 Discovery/도구로 허용 파일 목록, RAT·모듈, 소스/헤더/생성 파일, 선언/정의·include·메시지 후보 추출. 파일별 content hash | 승인된 대상 파일을 분모로 열거/제외/누락을 기록. 빌드별로 대상 TU와 성공적으로 해석된 TU 분리. generated 원본의 generator/config hash, scope 밖 참조는 gap |
| 3. 모듈별 관계 | 대표 모듈 하나에서 P0부터 기존 근거 재사용. Common 헤더·동명 심볼·두 variant를 비교. Updater는 검증한 명제만 정규화 | 모듈·variant별 레코드와 역방향 조회. 최초 구축의 wall time·최대 RSS·디스크/생성량·처리 파일/TU·오류를 별도 기록. 적정 작업 분할 크기는 현장 측정 |
| 4. 개인 snapshot | 구조화 정본에서 MD/Viewer 표현 파생. 기존 writer로 staging, 참조 무결성·hash·인가 검증, 기대 revision CAS, readback | 한 프로젝트·선택 build의 한 활성 snapshot을 조회 시작부터 끝까지 고정. 충돌/중단 시 이전 활성본 보존, 이미 반영된 응답 유실은 readback으로 정산 |
| 5. 변경분 갱신 | base↔new의 추가/변경/삭제/rename, 이전·신규 include 역의존, 생성 헤더/플래그/공통 매크로/메시지 등록표·도구 버전의 영향 TU를 합집합으로 계산 | 삭제된 정의·역참조를 함께 제거하거나 tombstone. rename은 근거로 이전 ID와 연결. 영향 범위를 좁힐 수 없는 모듈·variant는 stale/unknown 처리 후 해당 범위 재검증 |
| 6. 반복·복구 | 동일 source/build/입력 hash는 재사용. 변경 모듈의 레코드·파생물을 staging 후 새 snapshot으로 전환 | 전체 재구축은 공통 환경 변경 등 국소 무효화를 입증하기 어려울 때 비용 비교 후 선택. 혼합 snapshot, 오래된 역참조, 중복 쓰기 차단 |
| 7. 그룹 반영 | 개인 결과와 그룹 Base/Ours/Theirs 비교, Preview·별도 승인·기대 revision 저장·readback, Work 역링크 | 그룹 미승인도 개인 후보와 이력 보존. 역링크 실패 시 정산만 재개 |

물리 구현은 기존 저장 형식을 유지해요. 필요한 접근은 **심볼/메시지 exact lookup**, **유형·방향별 1-hop**, **변경 영향 역조회**예요. 기존 인덱스가 없다면 대표 모듈에서 deterministic lookup·역참조를 먼저 측정해요. 질의 지연·누락·갱신 비용이 관측돼야 별도 색인이나 DB를 비교할 근거가 생겨요. 두 build가 같은 헤더를 서로 다른 옵션으로 해석한 결과는 하나로 덮지 않아요.

## 5. 합성 완성 예시

가상 모듈 Demo의 단일 파일 demo.cpp예요. source revision은 아래 파일의 SHA-256 fe76dc4a6077e27d4a9be4fc61c61293a5d2856ee9e667b562d62bd8b61acf78로 고정했어요. 실제 모뎀 코드와 식별 관계가 없어요.

~~~cpp
enum class Key { ArmReq, ArmCnf };
struct Payload { int value; };
using Fn = void (*)(const Payload&);
struct Entry { Key key; Fn handler; };
static bool active = false;
extern void emit(Key, const Payload&);
static void apply(const Payload& p) { active = p.value != 0; }
static void onArm(const Payload& p) { apply(p); }
static const Entry routes[] = {{Key::ArmReq, &onArm}};
void submit(const Payload& p) { if (active) emit(Key::ArmReq, p); }
void dispatch(Key k, const Payload& p) {
  for (const Entry& e : routes) if (e.key == k) e.handler(p);
}
void after(Fn cb, const Payload& p) { if (cb) cb(p); }
#if OPT_A
void fastA() {}
#elif OPT_B
void fastB() {}
#else
void slow() {}
#endif
// OnlyTextToken appears in a comment.
~~~

**논리 레코드 한 세트.** 아래 간결한 표기는 기존 형식에 대응시키는 예시예요. 줄 번호는 위 코드 첫 줄을 1로 잡아요.

~~~yaml
snapshot: {id: demo-B, source: demo.cpp, revision: fe76dc4a6077e27d4a9be4fc61c61293a5d2856ee9e667b562d62bd8b61acf78, build: "OPT_A=0,OPT_B=1", coverage: "1/1 TU; runtime unobserved", producer: "manual + GCC 14.2.0", predecessor: null}
entities:
  - {id: E1, kind: function, name: "onArm(const Payload&)", linkage: internal, TU: demo.cpp, def: 8}
  - {id: E2, kind: function, name: "apply(const Payload&)", linkage: internal, TU: demo.cpp, def: 7}
evidence:
  - {id: V1, snapshot: demo-B, anchor: "demo.cpp:7-8", method: manual, proposition: "onArm body directly spells a call to the unique local apply declaration"}
relations:
  - {id: R1, snapshot: demo-B, from: E1, kind: calls, to: E2, guard: unconditional, evidence: V1, provenance: manual, extraction: EXTRACTED, validation: VERIFIED, semantics: static}
gaps: ["callback target at line 14", "send-to-dispatch transport", "ArmCnf pairing", "runtime order"]
~~~

| 같은 snapshot에서 작성할 행 | 근거 | 판정 |
|---|---|---|
| 등록 슬롯 routes[ArmReq] → onArm | 4, 8~9행. Entry 타입과 초기값에서 key와 함수 포인터가 함께 등장 | 정적 등록 VERIFIED. 11~12행은 key 검사와 간접 호출 위치. 특정 이벤트가 이 코드에 도착했다는 근거는 없음 |
| submit → ArmReq (sends 후보), ArmReq → Payload (이 호출 지점의 타입) | 6·10행 emit 선언 및 actual argument | 함수 호출·키·인자 타입 VERIFIED. 송신 API의 구현/계약은 이 파일 범위 밖이므로 실제 송신·수신 전달은 UNVERIFIED |
| apply → active (write), submit → active (read), apply → Payload.value (read) | 5·7·10행 | 직접 쓰기/읽기 VERIFIED. 특정 인스턴스의 상태 전이 시점은 미관찰 |
| fastB 정의 → 해당 build의 활성 여부 | 15~21행. OPT_A=0,OPT_B=1일 때만 전처리 출력에 남음 | 이 합성 build에서 VERIFIED. 다른 build의 snapshot을 받으면 먼저 STALE/variant mismatch. Analyzer 단독 정적 분기 출력에서는 build_activation=UNKNOWN |
| after → cb (callback), ArmReq ↔ ArmCnf 후보 | 14행은 포인터 경유 호출. 1행은 두 enum의 선언뿐 | 간접 호출 위치만 확인, cb의 실제 대상 UNKNOWN. 이름만 보고 대응 간선이나 MSC 순서를 만들지 않음 |

### 5.1 업무 GPT가 매핑할 관계 레코드

아래는 논리 샘플이에요. S0는 위 22행의 demo.cpp에 작은 보조 TU를 추가한 파일셋이에요. demo_support.hpp의 1행은 “void supportHook();”, support.cpp의 1행은 해당 헤더 include, 2행은 “void supportHook() {}”예요. procedure.md는 이 예시에서만 접근이 허가된 문서예요. 실제 호스트의 파일 형식과 ID 체계에 대응시켜 주세요. guard는 코드상 적용 조건이며 snapshot의 build와 구별해요. VERIFIED는 evidence의 명제에만 적용해요.

~~~yaml
snapshot: {"id": "S0", "source_revision": "6376d374471e7aad84857438dd7fa861cac440574f2c295ee12f3ebd2c016a3d", "build": "B:OPT_A=0,OPT_B=1", "scope": "2 TU + 1 header", "producer": "manual + GCC 14.2.0", "predecessor": null}
file_sha256: {"demo.cpp": "fe76dc4a6077e27d4a9be4fc61c61293a5d2856ee9e667b562d62bd8b61acf78", "demo_support.hpp": "f9cc298e39ce5d388233c54e7b61a05b58941705209899a72f0a896abc12af83", "support.cpp": "a8d0f676cd15fead650f204fc979912705a732f40ecafd36ebf85144908aec84", "procedure.md": "9d8e644e806f4257c29c9589537457f2fcd235150b8e3cff2ebc657fc1389c05"}
entities: {"M": "합성 Demo 모듈", "F": "demo.cpp", "H": "demo_support.hpp", "I": "support.cpp", "Hfn": "supportHook()", "Q": "Key::ArmReq", "C": "Key::ArmCnf", "P": "Payload", "A": "파일 정적 active", "Apply": "파일 정적 apply(const Payload&)", "On": "파일 정적 onArm(const Payload&)", "Submit": "submit(const Payload&)", "Slot": "routes[Key::ArmReq]", "Disp": "dispatch(Key,const Payload&)", "Late": "after(Fn,const Payload&)", "Cb": "after::cb, 실제 target 미해소", "K": "합성 문서 demo-procedure@rev1", "FastB": "fastB()"}
knowledge: {"K": {"doc_revision": "rev1", "authorized_demo": true, "source_revision": "6376d374471e7aad84857438dd7fa861cac440574f2c295ee12f3ebd2c016a3d", "build": "B", "section": "등록 표", "file": "procedure.md"}}
evidence:
  - {"id": "V01", "snapshot": "S0", "anchor": "file inventory", "method": "manual", "claim": "S0 허용 목록에 등재된 파일"}
  - {"id": "V02", "snapshot": "S0", "anchor": "support.cpp:1", "method": "tool", "claim": "GCC 로컬 dependency 출력으로 해소한 include"}
  - {"id": "V03", "snapshot": "S0", "anchor": "demo_support.hpp:1", "method": "manual", "claim": "함수 선언"}
  - {"id": "V04", "snapshot": "S0", "anchor": "support.cpp:2", "method": "manual", "claim": "동일 서명의 함수 정의"}
  - {"id": "V05", "snapshot": "S0", "anchor": "demo.cpp:7-8", "method": "manual", "claim": "같은 TU의 고유 정적 함수 직접 호출"}
  - {"id": "V06", "snapshot": "S0", "anchor": "demo.cpp:4,8-9", "method": "manual", "claim": "키 ArmReq의 테이블 초기값. pattern=table_lookup"}
  - {"id": "V07", "snapshot": "S0", "anchor": "demo.cpp:9,11-12", "method": "manual", "claim": "key가 일치할 때 가능한 포인터 대상. pattern=table_lookup"}
  - {"id": "V08", "snapshot": "S0", "anchor": "demo.cpp:6,10", "method": "manual", "claim": "emit 호출 표기. 송신 계약/전달 미확인"}
  - {"id": "V09", "snapshot": "S0", "anchor": "demo.cpp:9,11-12", "method": "manual", "claim": "등록에서 얻은 수신 후보. 런타임 도착 미관찰"}
  - {"id": "V10", "snapshot": "S0", "anchor": "demo.cpp:2,6,10", "method": "manual", "claim": "해당 호출 지점의 인자 타입. 전송 형식 미확인"}
  - {"id": "V11", "snapshot": "S0", "anchor": "demo.cpp:5,10", "method": "manual", "claim": "조건식에서 정적 상태 읽기"}
  - {"id": "V12", "snapshot": "S0", "anchor": "demo.cpp:5,7", "method": "manual", "claim": "함수 본문의 직접 대입"}
  - {"id": "V13", "snapshot": "S0", "anchor": "demo.cpp:3,14", "method": "manual", "claim": "인자 슬롯 간접 호출 위치. 구체 대상 UNKNOWN"}
  - {"id": "V14", "snapshot": "S0", "anchor": "procedure.md:1-3", "method": "manual", "claim": "아래 합성 인가 목록의 문서 rev1 링크. 업무 문서 권한 미검증"}
  - {"id": "V15", "snapshot": "S0", "anchor": "demo.cpp:15-21", "method": "tool", "claim": "GCC 전처리 출력에서 S0/B의 정의 확인"}
relations:
  - {"id": "R01", "snapshot": "S0", "from": "M", "kind": "contains", "to": "F", "guard": "true", "evidence": "V01", "provenance": "manual", "extraction": "EXTRACTED", "validation": "VERIFIED"}
  - {"id": "R02", "snapshot": "S0", "from": "I", "kind": "include", "to": "H", "guard": "true", "evidence": "V02", "provenance": "tool", "extraction": "EXTRACTED", "validation": "VERIFIED"}
  - {"id": "R03", "snapshot": "S0", "from": "H", "kind": "declares", "to": "Hfn", "guard": "true", "evidence": "V03", "provenance": "manual", "extraction": "EXTRACTED", "validation": "VERIFIED"}
  - {"id": "R04", "snapshot": "S0", "from": "I", "kind": "defines", "to": "Hfn", "guard": "true", "evidence": "V04", "provenance": "manual", "extraction": "EXTRACTED", "validation": "VERIFIED"}
  - {"id": "R05", "snapshot": "S0", "from": "On", "kind": "calls", "to": "Apply", "guard": "true", "evidence": "V05", "provenance": "manual", "extraction": "EXTRACTED", "validation": "VERIFIED"}
  - {"id": "R06", "snapshot": "S0", "from": "Slot", "kind": "registers", "to": "On", "guard": "true", "evidence": "V06", "provenance": "manual", "extraction": "EXTRACTED", "validation": "VERIFIED"}
  - {"id": "R07", "snapshot": "S0", "from": "Disp", "kind": "dispatches", "to": "On", "guard": "key==e.key", "evidence": "V07", "provenance": "manual", "extraction": "INFERRED", "validation": "UNVERIFIED"}
  - {"id": "R08", "snapshot": "S0", "from": "Submit", "kind": "sends", "to": "Q", "guard": "active", "evidence": "V08", "provenance": "manual", "extraction": "INFERRED", "validation": "UNVERIFIED"}
  - {"id": "R09", "snapshot": "S0", "from": "On", "kind": "receives", "to": "Q", "guard": "key==ArmReq", "evidence": "V09", "provenance": "manual", "extraction": "INFERRED", "validation": "UNVERIFIED"}
  - {"id": "R10", "snapshot": "S0", "from": "Q", "kind": "payload", "to": "P", "guard": "active", "evidence": "V10", "provenance": "manual", "extraction": "EXTRACTED", "validation": "VERIFIED"}
  - {"id": "R11", "snapshot": "S0", "from": "Submit", "kind": "read", "to": "A", "guard": "true", "evidence": "V11", "provenance": "manual", "extraction": "EXTRACTED", "validation": "VERIFIED"}
  - {"id": "R12", "snapshot": "S0", "from": "Apply", "kind": "write", "to": "A", "guard": "true", "evidence": "V12", "provenance": "manual", "extraction": "EXTRACTED", "validation": "VERIFIED"}
  - {"id": "R13", "snapshot": "S0", "from": "Late", "kind": "callback", "to": "Cb", "guard": "cb!=null", "evidence": "V13", "provenance": "manual", "extraction": "EXTRACTED", "validation": "VERIFIED"}
  - {"id": "R14", "snapshot": "S0", "from": "Slot", "kind": "knowledge_ref", "to": "K", "guard": "true", "evidence": "V14", "provenance": "manual", "extraction": "EXTRACTED", "validation": "VERIFIED"}
  - {"id": "R15", "snapshot": "S0", "from": "F", "kind": "defines", "to": "FastB", "guard": "!OPT_A && OPT_B", "evidence": "V15", "provenance": "tool", "extraction": "EXTRACTED", "validation": "VERIFIED"}
~~~

정적 이벤트는 질의별로 검증 대상을 좁혀요. 예를 들어 R06은 등록 완료, R07/R09는 후보, R08은 실제 송신 계약 확인 대기예요. 셋을 연결해 실행 순서나 ACK 수신을 확정하면 오류예요.

### 5.2 같은 코드가 바뀌었을 때

S1에서는 demo.cpp 9행의 등록 키 한 곳을 ArmReq에서 ArmCnf로 바꿔요. 바뀐 파일 SHA-256은 73fdc69a62a1ce5d2fac3ffb6038b6cc63456e720201f2d18deb5c7474a86002예요. 새 키의 등록 사실은 요청·응답의 짝이나 송신 경로를 확정하지 않아요. 아래 delta는 새 snapshot의 논리적 변경 기록이에요. S0의 immutable 레코드 자체를 수정하지 않아요.

~~~yaml
snapshot: {"id": "S1", "predecessor": "S0", "source_revision": "439a82f08bcd0738ad8f8d1daa8c3a586e1a1bb2534ce82c3d62c1ff260c0ae6", "build": "B:OPT_A=0,OPT_B=1"}
delta:
  - {"id": "R06", "before": "S0 active Slot(ArmReq) -> On", "after": "S1 tombstone", "reverse_lookup": "On -> Slot(ArmReq) removed", "evidence": "new line 9"}
  - {"id": "R16", "before": null, "after": "S1 active SlotC(ArmCnf) -> On", "kind": "registers", "guard": "true", "provenance": "manual", "extraction": "EXTRACTED", "validation": "VERIFIED", "evidence": "S1/demo.cpp:4,8-9", "new_entity": "SlotC = routes[Key::ArmCnf]"}
  - {"id": "R07/R09", "before": "S0 candidate for ArmReq", "after": "S1 withdrawn for ArmReq", "prior_evidence": "V07/V09 STALE for S1", "followup": "look up other authorized registrations before claiming absence"}
  - {"id": "R14", "before": "S0 verified link", "after": "S1 inactive link; document rev1 still pins S0", "followup": "revalidate doc scope and source revision"}
~~~

| 사건 | 기대되는 읽기·쓰기 결과 |
|---|---|
| Reader가 S0을 선택한 후 Writer A가 CAS(expected=S0, new=S1)에 성공 | 진행 중인 Reader는 S0의 양방향 관계만 읽고 다음 신규 조회는 S1만 사용 |
| Writer B가 같은 S0을 기준으로 S2를 활성화하려고 함 | 갱신 0건. S1 유지, 파생물도 S2로 노출하지 않음. B 후보를 보존하고 S1 기준 재대조 |
| Writer A가 커밋 후 응답을 잃음 | 활성 ID와 manifest hash를 읽어 S1과 일치하면 완료 정산. 조회 실패 시 결과 UNKNOWN으로 보존 |
| A/B 공통 헤더 변경과 B 전용 헤더 rename | 기존·신규 include 역의존의 합집합을 취함. 공통은 A/B 두 TU, B 전용의 이전·새 경로는 B만, 독립 TU는 제외 |

이 예시에서 두 build의 실제 GCC 의존 목록, 변경 전후 C++ 구문, 임시 SQLite로 구현한 CAS·reader pin 모형을 시험했어요. 업무 Writer·실제 인덱스는 G03·G04에서 별도 확인해요.

## 6. 저사양 LLM의 질문별 실행

1. **질문 하나**와 source/build, 허용 모듈·범위를 고정해요. ‘정의는 어디인가’와 ‘해당 build에서 누가 처리하는가’를 별도 질의로 취급해요.
2. qualified signature 또는 인터페이스를 포함한 Message ID로 정확 조회해요. 동명·variant 후보가 여러 개면 각각 표시하고, 묻는 관계와 방향의 직접 이웃만 받아요.
3. LLM에는 snapshot·build, 후보와 근거 위치, 검증 상태·빠진 범위, 다음 probe 한 개를 줘요. 모호할 때는 선언/등록 원문이나 지도 밖 대체 탐색을 한 단계 실행하고 분기해요. 미지원·오래됨·잘림·미권한·오류를 별도 처리하고 미권한 범위의 이름·건수도 노출하지 않아요.
4. Analyzer 원문과 빌드 조건이 뒷받침하는 범위까지 답해요. 예를 들어 ‘B에서 누가 ArmReq를 처리하는가’에는 등록된 onArm, dispatch의 포인터 호출 위치, 송신과 dispatch 사이의 미확인을 구분해요. 동작 이유는 기존 Procedure/Feature, 시퀀스는 검증된 Scenario/MSC로 연결해요.
5. 반환 한도는 Map **4,096 실제 tokenizer tokens 및 50행**, 기본 1-hop, 코드 **20파일/step·60파일/task**, 추가 probe 최대 4단계, 총 입출력 **32,768 tokens·20분/task**의 pilot 상한이에요. 활성 환경 상한이 더 낮으면 낮은 값을 적용해요. 모델 이름/컨텍스트 길이는 G05에서 실측 가능한 실제 호출 설정으로 고정해요. 초과 시 받은 부분·미조사·다음 위치를 반환하고 종료해요. 전체 인덱스 구축 비용은 따로 측정해요.
6. 지도 누락·충돌은 같은 Work에 갱신 후보로 남겨요. Recovery V2는 정상 Procedure와 수정 전후·반례, V3는 지도 후보와 지도 밖 독립 탐색, V4는 보호가 최초 위반 전에 실제 적용되는 근거를 확인해요. 없는 후보를 안전 종결의 근거로 쓰지 않아요.

## 7. 도구·라이선스·보안 결정

2026-11-27 KST 기준 아래 명시 버전의 공식 원문을 대조했어요. 특정 버전을 비교용으로 고정했으며 실제 업무 배포본·계약·승인 여부는 G0에서 확인해요.

| 도구와 확인 버전 | 이 작업에 유용한 범위와 비용 | 사용권·도입 판정 |
|---|---|---|
| 기존 승인 Discovery / Analyzer | 기존 7건·정확 이름 조회, 제한 probe와 코드 근거 재사용. lexical 출현·호출 표기·등록 후보를 구별. 재사용률·실제 읽기 수 측정 | **기본 경로**. G0에서 실제 설치와 허용 범위 확인. 도구 추가 없이 작성 표준과 비교 시험 진행 가능 |
| Aider aider-chat 0.86.1 | Repo Map의 토큰 예산과 관련 심볼 선택 방식을 참고. 전역 그래프 랭킹은 exact/1-hop에서 놓친 사례가 생기면 비교. 편집 agent 설치나 모델 호출은 설계에 필요하지 않음 | **개념 채택**. 프로젝트 LICENSE.txt는 Apache-2.0으로 상업적 내부 이용이 일반적으로 허용됨. 배포 시 적용되는 라이선스·저작권·NOTICE·수정 표시와 포함 의존성은 별도 확인. 설치 검토 시 모델 요청/업데이트 확인/analytics/자동 commit·히스토리·캐시 경로까지 확인. 기본 설계에서 외부 모델 비용 0 |
| LLVM/clangd·LibTooling 20.1.0 | 실제 compile command로 빌드별 symbol/refs·정의·타입 정밀화. clangd ref는 심볼→사용 위치로, L1 메시지 의미와 함수 간 호출 간선에는 별도 근거가 필요. 로컬 BackgroundIndex는 TU별 캐시, 일괄 static index는 재생성 비용을 따로 측정 | **선택적 로컬 pilot**. Apache-2.0 WITH LLVM-exception, 상업적 내부 이용 가능. 배포판 부속 고지/예외·종속성 대조. 생성 헤더·compiler/target/sysroot/include/defines를 대조하고 허용된 driver만 사용. 로컬 인덱스와 캐시만 승인 경로에 보존. 원격 인덱스 질의는 식별자 일부를 노출할 수 있음 |
| GitHub CodeQL CLI v2.22.0 / github/codeql 공개 쿼리 | 호출·데이터 흐름의 특정 결손을 검증할 때 후보. C/C++ none 모드는 플래그/include 추론, manual build는 실제 빌드 경로·비용을 수반. 어느 쪽도 업무 variant 정확성은 별도 검증 | **도입 제외, 명시적 사실·관계 질의 방식만 참고**. 기본 설계는 CodeQL CLI, 쿼리팩 또는 그 코드의 복사를 요구하지 않아요. 공개 표준 쿼리·라이브러리의 MIT와 CLI 이용약관은 별도. 일반 비공개 상업 제품 코드의 지도 구축은 공개 무료 조건만으로 허용됐다고 판단할 수 없음. GitHub Code Security/GHAS 등 실제 계약의 대상 repo·사용자·목적·자동 실행 범위나 별도 서면 허가를 확인한 뒤 검토. 가격 및 업무 계약 미확인 |

**업무 데이터 경계**　소스, 컴파일 DB, 전처리 산출물, 맵, 검색어, 프롬프트, 결과 캐시·로그는 코드와 같은 업무 경계에서 처리해요. 반입 시 artifact 출처·버전·SHA, 전이 의존성 고지, 허용 모델 endpoint·네트워크 경로, 캐시 위치·보존/삭제·접근자를 확인해요. 외부 네트워크가 차단된 읽기 전용 사본에서 실제 외부 요청과 Git 변경이 0인지 검증하고, 검증 전에는 기존 승인 도구 경로를 사용해요. 라이선스 파일만으로 회사 도입, 구독 가격, 모델 서비스 약관까지 확정할 수 없어요.

[공식 Aider v0.86.1 LICENSE](https://github.com/Aider-AI/aider/blob/b8b521f143f06be420e0c3ea4fe0a7fddc8db0da/LICENSE.txt) · [Repo Map](https://aider.chat/docs/repomap.html) · [Aider 설정](https://aider.chat/docs/config/options.html) · [LLVM 20.1.0 LICENSE](https://releases.llvm.org/20.1.0/LICENSE.TXT) · [LLVM 배포 정책](https://llvm.org/docs/DeveloperPolicy.html) · [clangd 인덱스](https://clangd.llvm.org/design/indexing) · [컴파일 명령](https://clangd.llvm.org/design/compile-commands) · [원격 인덱스와 정보 공개](https://clangd.llvm.org/guides/remote-index) · [CodeQL v2.22.0 CLI 약관](https://github.com/github/codeql-cli-binaries/blob/81e6755f40ec81a3583d4e2ba929819b0b0fc375/LICENSE.md) · [쿼리와 CLI 라이선스 구분](https://github.com/github/codeql#license) · [C/C++ build 방식](https://docs.github.com/en/code-security/reference/code-scanning/codeql/build-options-for-compiled-languages)

**연구·상용 적용 근거**　Zhang 외의 RepoCoder는 저장소 단위 코드 완성에서 검색과 생성을 반복하는 방식을 실험했어요. Liu 외의 Lost in the Middle은 긴 입력에서 근거 위치에 따라 QA/검색 성능이 달라짐을 관찰했어요. Anthropic의 JIT 문맥 사례는 가벼운 참조 후 필요 시 원문을 읽는 운영 예예요. LTE/NR의 Qwen 정확도 개선율은 이 연구들로 예측하지 않고 아래 D3−D2로 판단해요. [RepoCoder, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.151/) · [Lost in the Middle, TACL 2024](https://aclanthology.org/2024.tacl-1.9/) · [Anthropic의 context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

## 8. 현장 확인·평가·완료 기준

| G0 항목 | 업무 GPT가 돌려줄 확인 내용 |
|---|---|
| G01 기존 자료 | 7건 각각의 source/build·manifest/hash·범위·근거와 3절 관계 대응, 재사용/부분 보완/충돌. 실제 대상 파일/TU·헤더·생성 파일·제외 분모 |
| G02 추출 능력 | Updater/Analyzer 활성 version·hash·action·추출 방법, lexical/정적/빌드/관찰 구분. 동일 이름, 등록, 간접 호출, sibling guard, partial 반례 각 1건 |
| G03 개인 저장·권한 | G6의 개인/그룹 승인 범위, Writer actor/path·CAS·readback, Kernel export 전후 hash, 충돌·응답 유실·복구. 필요 시 도구별 반입/법무/보안 담당 판정 참조 |
| G04 소비자 | exact·방향별 1-hop·인가·snapshot 고정·권한 밖 건수 비공개·Knowledge 링크. Analyzer/Recovery/Viewer와 호스트에서 같은 ID·revision을 돌려주는지 |
| G05 모델·비교 | 실제 ID·토크나이저/툴·모델별 한도·정답셋/누출 방지, 실행별 토큰·파일·시간. 지연 공통 캐시/초기화·재사용 기준도 동일하게 적용 |
| G06 그룹 | 기존 그룹 형식·Base/Ours/Theirs·Preview·권한·readback·역링크 재개, 그룹 미승인 시 개인 이력 보존 |

G0 회신은 **ID / PASS·FAIL·UNKNOWN / 활성 version·action / 업무 Work의 증거 참조 / REUSE·CONNECT·재현한 GAP / 다음 행동**으로 기록해요. 각 PASS에는 시험명, 입력 package SHA·source/build, 실행 주체·환경, 명령, 실제 결과 로그 또는 CI artifact의 허용된 참조와 SHA-256을 붙여 주세요. 업무 데이터를 재실행할 권한이 없거나 로그가 없으면 NOT_RUN/미검증으로 표시해요. §9의 Linux 개발자 결과를 현장 PASS로 복사하지 않아요.

| 최초 회신 양식 | 업무 GPT 기록값 |
|---|---|
| G01 / D01…D07 각각 한 행 | 기존 artifact ID · hash · source/build · 조사한 분모/제외 · P0별 대응/공백 · 재사용/부분 보완/충돌 · 근거 ref |
| representative pilot 1건 | 대표 모듈 · build 2개 또는 1개인 사유 · 정확 심볼/메시지 · gold 근거 · 조회·반증 결과 · 다음 행동 |
| G02~06 각각 한 행 | 상태 · 활성 version/action · 실제 허용 권한 · 실행 주체 · 로그·SHA 또는 미확인 사유 · 후속 담당 |

| 비교군 | 입력 | 해석 |
|---|---|---|
| D0 | 현행 입력 | 기준선 |
| D1 | 현행 + 제한 Map | D1−D0, 탐색 단독 기여 |
| D2 | 현행 + 검증된 정상 Procedure | D2−D0, 동작 맥락 기여 |
| D3 | 현행 + 동일 Map + 동일 Procedure | **D3−D2**, 기존 지식 위에 더해진 Map의 가치 |

대표 모듈의 기존 비-timeout 실패 Seed와 별도 holdout을 독립 문맥에서 실행해요. 정답은 입력에서 제외하고 같은 source/build·model·허용 도구·총예산을 유지해요. 채점자는 미리 고정한 양성 ≥30, 음성/반례 ≥10을 call·message·build 및 모듈/variant별로 표시해요. recall=회수한 정답/전체 양성(미조사 포함), precision=올바른 확정/전체 확정 예측, 확정이 0건이면 precision은 N/A예요. pilot 목표는 **recall ≥90%, 근거 없는 확정 0, stale/variant 불일치 탐지 100%, 범위 밖 읽기 0**이에요. 전체 열거율, 해석 가능한 TU 비율, 관계별 누락·오탐, 잘림을 따로 기록해요.

동일 정확도에서 파일·토큰·시간이 줄거나 동일 예산에서 정답률이 높아지고 holdout에서도 재현될 때 확대해요. V2 규칙·최초 위반, V3 후보 recall/precision, V4 잘못된 종결을 별도 채점해요. 초기 구축 CPU/시간·메모리·디스크와 변경 1회 갱신 비용을 질의 비용과 분리해요. 손익분기 질의 수는 (구축비 + 기간 내 갱신비) / 질의당 절감비로 추정할 수 있어요. 비용 단위·품질이 같고 절감비가 양수일 때만 계산해요.

현장 회귀에는 공통 헤더/매크로 한 건 변경, 등록 삭제, rename, 같은 이름의 다른 TU/variant, snapshot 갱신 중 구버전 조회, CAS 경합·저장 후 응답 유실, 미권한/빈 결과, 구형 Knowledge 링크를 포함해요. 최종 보고는 현장 자체시험과 독립 설계 리뷰, 개발본과 운영 적용을 별도로 기록해요.

## 9. 이번 검토에서 직접 실행한 시험

| 시험 | 결과 | 확인한 범위 |
|---|---|---|
| Analyzer v0.15.7 실제 ZIP | **85/85 PASS** | 기존 직접 호출·coverage 13+9, 정확도/저장 25, 병렬 계약 28의 총 75건과 신규 전처리 10건. 신규에는 패키지 CLI 경유 시험 포함 |
| Viewer v0.5.8 실제 ZIP | **8/8 Node 프로그램 PASS** | 기존 6개와 Source Map 전용 2개. 상대 경로를 사용하는 2개는 tests 디렉터리에서 실행. 업무 브라우저·실제 adapter E2E는 NOT_RUN |
| 합성 C++ 4 build | **4/4 PASS** | GCC 14.2.0 구문 검사와 전처리 결과에서 (A,B)=(0,0)/(0,1)/(1,0)/(1,1)에 slow/fastB/fastA/fastA가 각각 한 개만 남음 |
| 합성 파일 1,500개 대상 CLI 범위 검사 | **PASS** | 실제 probe 입력에 1,500개 경로, 파일 예산 6으로 마지막 파일의 정의를 질의하면 NOT_ANALYZED/budget_exceeded. 해당 파일 하나를 입력으로 지정하면 symbol_occurrence 1건. 주석에만 있는 이름도 CONFIRMED 출현으로 반환되고 잘림은 rn에 표시. compile-condition은 잘린 범위·실제 활성 UNKNOWN을 보존 |
| 실제품·모델 품질·도구 반입 | **NOT_RUN** | 실제 1,500개 전체 색인, Qwen D0~D3·V2/V3/V4, 7건 재사용률, 업무 설치·권한·보안·법적 승인·그룹 게시. 합성 시험에서 제품 개선율/속도는 산출하지 않음 |

검토 패키지의 SHA-256은 Analyzer 6a11cb8685c46d1ac22a1465968193a72708ca90bcfcf453b371c869abdfbeab, Viewer 5d7935edba33bf062d167c95f3a44c620c683c33accc9c7aadacb69561fa73de, Kernel 5c1f73a09b2cd8c4ec93134f387ed7f80cec799b534f2d044978b66e6c38b20c, Workflow fd337ee31e09c9f694146c9d159799ca7182af052c93121e73888a9ee367a0a1, Converter b0ebd0aa4d771adc30648ab2bce23a3c1648e408984bedb36d0e3da45108312c예요. [L1Work 원본](https://github.com/wonhwipark/L1Work/tree/9134db8028f3d2acbf81e7067c5a7c6721e44351)

**보강 시험**　같은 합성 파일에서 dispatch(Key::ArmReq)는 실제 테이블 9행 대신 10행의 인자 쌍을 UNCERTAIN으로 반환했고, field(active)는 5행·10행만 반환해 7행 대입을 놓쳤어요. callers(apply)는 structure 미제공 시 NOT_ANALYZED였고, 8행 후보를 제공하자 static_direct_call_spelling을 확인했어요. 그러므로 출현·후보·누락을 실제 소스와 대조해야 해요.

**시험 증거**　L1_SOURCE_MAP_1500_VALIDATION_EVIDENCE_20261127_KST.zip의 SHA-256은 c4f938fe0df840eebf07b6e38770994428f8712bb8881f56e62a0d24a6e0e1a9예요. README에 원본 ZIP 고정 링크·실행 절차가 있고 logs/analyzer 및 logs/viewer에는 5개와 8개 시험 프로그램의 출력, logs/check_design.txt에는 GCC 4조합과 1,500파일 검사 결과, logs/check_delta.txt에는 헤더 및 CAS 모형, logs/probe_examples.txt에는 합성 probe 결과가 있어요. SHA256SUMS는 개별 파일의 해시예요.

## 10. 독립 리뷰 반영과 적용 범위

Windows Claude Code의 정적 리뷰 대상은 이전 **업무 GPT용 통합 인계서 r0002**였어요. 요청 rev 1, ZIP 14,106 bytes, ZIP SHA-256 138af88da296a738d48f86636724f71ec72f3c9c84d2d7fd900a652eb4ed38db, 그 안의 MD SHA-256 909447e4ec91cf4d8567e89d66076eb5c9b8dc48e4dcf7844ed7dfd54ac62a55예요. 이는 §2에 표시한 사용자 첨부 파일과 별개예요. r0003은 GPT가 지적을 보완하고 자체 검증한 전달본이에요.

| 독립 리뷰 지적 | 반영 |
|---|---|
| M1 관계별 형식화 | §5.1의 14개 관계 종류·15개 레코드에 양 끝, 근거, 방향, 조건, 검증 상태를 명시 |
| M2 변경 반례 | §5.2에 등록 삭제·새 등록·후보 철회·역참조·문서 stale, 두 Writer 경합과 고정 Reader를 명시 |
| M3 해시 식별 | 사용자 첨부, 리뷰한 MD, 리뷰 ZIP, 샘플·시험 증거의 파일별 해시를 대조. r0003 자체 해시는 별도 Work 판정에 기록 |
| M4 시험의 독립성 | §8~9에 개발자/리뷰어/현장 시험을 구분하고 증거와 G0 회신 양식 제공 |
| m1, m2 | §3에 switch/table의 공통 전달 관계와 별도 등록 기준, §2·7에 외부 원문을 확인한 주체·범위를 표시 |

[독립 리뷰 원문](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/d55513db3c8a7b3a92e6a5d77df83dc270792d30/collab/reviews/REQ-L1-SOURCE-MAP-DESIGN-R2-20261127/REVIEW_RESULT_1.md) · [실행 영수증](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/d55513db3c8a7b3a92e6a5d77df83dc270792d30/collab/receipts/REQ-L1-SOURCE-MAP-DESIGN-R2-20261127/RECEIPT_1.md)

**다음 한 행동**　업무 GPT에서 기존 7건을 3절과 대조해, 대표 모듈에 이미 있는 관계와 처음 원문 확인이 필요한 관계를 한 표로 회신해 주세요.
