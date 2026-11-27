# L1 Recovery · Source Map · Workspace Viewer 단일 통합 업무 GPT 인계 r0001

- 2026-11-27 KST · 기존 업무 Work 재사용 · 업무 GPT 설계/수락, Qwen3.6-27B 구현·실행
- 통합 기준: Recovery r0008, Source Map r0003, Viewer v0.5.8 / Analyzer v0.15.7 개발 인계.
- 사용자 최신 확정: **실제 운영 Viewer v0.5.7**, Source Map은 **기존 Knowledge와 동일한 저장 방식**, 상위 폴더 **l1-workspace/**, 독립 경로 **l1-workspace/source-map/**.
- 본 문서 하나를 전달하면 세 기존 인계서의 실행 지시를 중복 전달할 필요 없음. 상세 계약·관계 예시·회귀 조건은 본문과 부록에 포함. 기존 원문 및 과거 시험 이력은 보존.
- 제품 코드 변경, 운영 설치/서비스 재시작, Job 활성화, 그룹 게시 및 신규 독립 리뷰는 본 문서 게시 자체로 승인되지 않음. 기존 승인 범위를 확인하고 실제 변경은 그 범위에서만 수행.

## 0. 업무 GPT에 전달할 단일 요청

> 본 통합 인계서의 1~8절을 현재 실행 우선 기준으로 사용해 주세요. 기존 활성 스킬 및 Workspace의 Knowledge 저장·조회 구현을 먼저 대조하고 이미 있는 기능을 재사용해 주세요. Source Map은 Knowledge Updater가 생성/갱신하고 기존 Knowledge Writer와 동일한 방식으로 l1-workspace/source-map/에 저장해 주세요. 별도 Writer/DB/저장 엔진을 만들지 마세요. 현재 Viewer는 v0.5.7이므로 v0.5.8 최신 패키지와 실제 읽기 Adapter를 대조해 독립 Source Map 메뉴에 연결해 주세요. 기존 Kernel/Workflow/Converter는 수정하지 말고 실제 입증된 결손만 담당자에게 별도 제안해 주세요. Recovery는 Viewer 업데이트 또는 Source Map 전체 구축과 무관하게 대표 비-timeout Seed 1건부터 기존 분석 결과를 보존하고 V2 Cause Rule/V3 Search Plan을 단계적으로 개선해 주세요. 이미 검증된 Source Map/정상 Procedure는 선택 조회하고 원본 코드로 검증해 주세요. 단계별 결과·근거·차단 사유를 보고하고 사용자 확인 후 다음 단계로 진행해 주세요. 추가 독립 리뷰는 하지 마세요.

## 1. 기준 버전 및 영향 범위

| 대상 | 현재 확인/기준 | 조치 |
|---|---|---|
| Viewer | **실제 운영 v0.5.7 (사용자 확인)**, 최신 게시 v0.5.8 | Source Map 독립 메뉴 제공은 v0.5.8 대상. 실제 서비스 경로 및 Adapter 확인 후 승인 범위 내 연결/시험 |
| Code Analyzer | v0.15.6 사용자 적용 확인, 최신 게시 v0.15.7 | 실제 활성 version/hash/action 확인. 전처리 조건 보완본의 효과를 구버전에 소급하지 않음 |
| Knowledge Updater | 업무 GPT 관리 | Source Map 생성/저장/갱신 및 기존 Knowledge Writer 재사용 |
| Recovery | 업무 GPT 관리 | 기존 V0~V6 유지, V2/V3 집중 보완 |
| Kernel | 최신 v0.7.47 | 기존 Work/Evidence/export 보존, 변경 금지 원칙 |
| Fix Workflow | 최신 v1.6.75 | 기존 조회/Work/첨부 재사용. 동버전 후보 hash 구분 |
| Doc Converter | 최신 v0.2.26 | 기존 검증 Scenario IR→PUML/SVG/HTML |
| knowledge-analysis-preflight | v0.2.0 | 기존 제한 문맥/근거 검사 선택 재사용 |
| Job List / Skill Updater | 기존 관리 경로 | 신규 전용 Job/배포 로직 변경 없음 |
| Linux MCP / Read Adapter | 활성 계약 미확인 | 기존 Knowledge 조회와 권한 재사용, 필요한 읽기 경로 연결 |

최신 게시 ZIP을 기준으로 관리하되 실제 호스트 활성 상태는 별도 기록. Viewer v0.5.7을 구버전 역사 기록으로만 취급하면 안 됨: 사용자 확인된 현재 운영본. v0.5.8과 v0.15.7의 이전 개발 전달서에는 development_not_for_deployment 표기가 있음. 자동 배포 원본 게시와 실제 설치·서비스 전환은 다름. 해당 표기의 자동 선택 차단 여부를 추정하지 말고 기존 Skill Updater/설치 결과/실서비스 경로 확인. 사용자 승인과 기존 운영 정책에 따라 적용; 임의 롤백, 중복 설치, 강제 재시작 금지. 비교 시험 중 모델·도구·입력 버전 고정, 변경 시 새 기준선.

| 최신 패키지 | SHA-256 | 원격 고정 commit |
|---|---|---|
| [Viewer v0.5.8 ZIP](../l1-workspace-viewer-wiki-integrated_v0_5_8_1127.zip) | 5d7935edba33bf062d167c95f3a44c620c683c33accc9c7aadacb69561fa73de | e80cb844d4409b8b60ca212d2822bd91f1692891 |
| [Analyzer v0.15.7 ZIP](../code-analyzer_v0_15_7_1127.zip) | 6a11cb8685c46d1ac22a1465968193a72708ca90bcfcf453b371c869abdfbeab | d015c6c5c7d7e37ee93e3760ca3022cc48a0a3b8 |

구버전 ZIP 재설치 금지. 기존 11/27 격리 회귀 Analyzer 85/85, Viewer 8/8 Node 프로그램 PASS는 개발자 시험이며 실제 업무 호스트 E2E/실제 데이터 연결 PASS가 아님.

## 2. 확정 Workspace 저장·조회 아키텍처

```text
l1-workspace/
├── works/          # Work/Evidence: 기존 Kernel 및 승인 writer
├── knowledge/      # 기술 지식: Knowledge Updater + 기존 Knowledge Writer
├── recovery/       # 기존 Kernel 파생 Recovery 조회
├── source-map/     # Source Map 정본: Knowledge Updater + 동일 Knowledge Writer
└── index/          # 기존 Workspace 공통 인덱스: Kernel 소유권 유지
```

**저장 방식은 선택지가 아닌 필수 요구사항:** 기존 개인 Knowledge의 실제 저장 root, canonical 경로, Writer 호출, actor/권한, 승인, Preview/기대 revision, 이력, readback, 충돌/응답 유실 복구 절차를 Source Map에 재사용. Source Map은 knowledge/의 하위 폴더가 아니라 동일 계층. Workspace 자체의 실제 절대 경로는 기존 환경에서 확인. 기존 Knowledge Writer에 source-map/ 경로 지원이 없으면 기존 Writer의 승인된 경로 매핑만 최소 확장하는 안을 업무 GPT가 제시하고, 별도 Writer·DB·저장 엔진·새 Kernel schema는 만들지 않음. 안전한 저장/원자적 활성화가 미확인이면 후보 보존 후 해당 저장만 HOLD. 다른 분석을 차단하지 않음.

| 책임 | 변경 기준 |
|---|---|
| Knowledge Updater | Discovery→Analyzer fact→정규화·검증→기존 Writer 저장 요청·readback. Source Map 유일 write 요청자. Knowledge·Map은 각각 정본 |
| 기존 Knowledge Writer | 실제 source-map/ 파일 저장·승인·CAS·충돌 보호. 기존 경로/권한 재사용, 최소 경로 확장은 결손 입증 및 승인 후 |
| Ledger Kernel | Work/Evidence, 공통 index 및 export. Source Map 생성/갱신/저장 담당 아님. 기존 파일 보존만 검증 |
| 기존 Knowledge read 경로/Adapter | 같은 Workspace root의 인가·snapshot·ID/revision 확인 및 Map 검색/상세 연결. 승인 없는 경로/메타정보 노출 금지 |
| Viewer | 독립 Source Map 메뉴, 조회만. 기존 Knowledge/Recovery/Work/MSC/Write 기능 변경 금지 |
| Analyzer·Recovery | 검증된 Map의 읽기 소비; 오류/갱신 후보는 기존 Work에 남기고 Updater가 처리 |
| Workflow·Converter | 기존 Work·Evidence·MSC 계약 재사용. Source Map 전용 writer/renderer 구현 금지 |

저장 흐름: 기존 Discovery/Analyzer → Updater 검증·snapshot → **기존 Knowledge Writer** → l1-workspace/source-map/ → 기존 Knowledge 읽기 방식/필요한 제한 조회 연결 → Viewer/Analyzer/Recovery/Updater.

기존 통합 설계의 README.md·manifest.json·nr/·lte/·common/·interfaces/·index/·history/·gaps.md는 논리 후보. 하위 파일 형식은 기존 Knowledge 저장/조회와 실제 Discovery 산출물에 매핑. JSON/JSONL·DB·별도 API를 필수로 강제하지 않음. Source Map 정본은 검증된 구조화 snapshot이며 MD/Viewer 표시는 동일 snapshot에서 파생. Knowledge는 동작 의미 및 MSC, Work/Evidence는 분석 원본·영수증, Map은 심볼/관계/근거 참조만 유지.

Snapshot 단위 source revision/build/scope/producer/hash/coverage/predecessor, 기존 Writer의 staging→검증→기대 revision CAS→readback. 한 조회의 snapshot 고정, 충돌/중단 시 이전 활성본 유지, 변경 후보 보존. 기존 원자적 전환 방식이 없다면 새 DB를 먼저 만들지 않고 해당 저장을 보류·최소 보완 제안. 헤더·등록·rename/delete 등 변경의 전후 역의존 합집합으로 영향 범위 갱신. 동일 source/build/hash 재사용, stale/unknown·tombstone/역참조·문서 링크 재검증. 그룹 l1sw-dev-knowledge 게시/역링크는 기존 별도 Preview/승인/CAS/readback. 개인 저장과 그룹 게시 권한 구분.

## 3. G0 읽기 조사 및 최초 회신

| ID | 확인 내용 |
|---|---|
| G01 | 기존 Source Map Discovery 7건 D01~D07의 artifact/hash/source/build/coverage/gaps·관계 대응, 재사용/부분 보완/충돌 구분 |
| G02 | 실제 제품 source root/revision/build·모델/Analyzer/Updater/Recovery 활성 버전·지원 action·입출력·영수증 |
| G03 | 기존 Knowledge Writer 실제 actor/path·개인/그룹 G6 승인 범위·CAS/readback·기존 파일 보존 및 source-map/ 지원 |
| G04 | 기존 Knowledge read/adapter/MCP 실제 계약, exact/1-hop 및 Snapshot pin/인가, Viewer 실서비스 경로·v0.5.7 |
| G05 | Qwen 모델 ID/설정/tokenizer/예산, 대표 비-timeout Seed/정상 반례/기대 후보 고정 |
| G06 | 기존 그룹 저장·승인·Preview/충돌·역링크, 그룹 미승인 시 개인 이력 보존 |

G0 자체는 읽기 전용. 기존 자료를 재실행하지 않음. 기존 Work와 실패 로그/실행 영수증 우선 확보. 실제 분석 소스 경로가 명시되면 우선 검증, 미지정이면 같은 프로젝트의 유효한 저장 경로 재사용. 경로/revision 문제가 있으면 필요한 질문 최대 1회, 임의 경로 전환/checkout 금지. 업무 자료는 업무 환경에서만 보존. 각 항목은 PASS/FAIL/UNKNOWN 또는 NOT_RUN과 실제 계약/action/증거·다음 행동으로 회신. 미확인된 API를 추정 구현 금지.

## 4. 두 작업 흐름 (독립 진행)

**A. Source Map/Viewer:** G0 → 기존 Discovery 7건 재사용 → 대표 모듈 P0 관계 검증 → 동일 Knowledge Writer 개인 저장/readback → 기존 읽기 방식 연결 → 실제 Source Map 데이터·기존 Knowledge 링크 확인 → Viewer v0.5.8 회귀. Viewer 업데이트 전에도 승인된 저장 및 CLI/스킬 조회는 가능하면 독립 진행. 전체 1,500개 규모 확대는 대표 모듈의 정확도·비용·갱신 성능 확인 후.

**B. Recovery:** G0 → 기존 비-timeout Seed 1건 현행 기준선 → 코드 근거/Procedure 원인 분리 → V2 Cause Rule → V2 원문/반례 게이트 → V3 Search Plan/L1·L2 → 후보 coverage → L3 상태/자원 탐색 → V4~V6 기존 보호 판정/조치/MSC/Work 회귀. Viewer v0.5.8 설치나 Source Map 구축 완료는 선행 조건 아님. 이미 유효 Map이 있으면 사용. 없거나 stale/partial/conflict면 bounded Analyzer probe와 지도 밖 독립 탐색 수행. Map 누락을 안전 종결 근거로 사용 금지.

동일 Work/Seed/증거를 재사용할 수 있으면 재사용하되 두 업무의 저장 권한과 수락 기준은 구분. 각 차수별 변경·시험·사용자 확인. 분석 성공, MSC 성공, Work 저장, 개인 Map 저장, Viewer 조회, 제품 효과를 독립 판정. 후속 저장/Viewer 장애 때문에 완료 분석·변환·Job 재실행하지 않음.

## 5. Source Map 작성 및 분석 소비 핵심

P0 전체 경량 파일 목록/모듈·빌드별 관계: contains/include, declares/defines, calls, sends/receives/payload, registers/dispatches, guard/build. P1: read/write, L1C/HAL/RF/PHY 경계, Stack/Domain/Cell/CC 문맥, Timer/Event/callback, knowledge_ref. P2: data flow/alias는 실제 결손 시. 세부 방향, 명제와 신뢰도, 합성 완성 예시는 부록 A. 기존 Analyzer probe symbol/callers/callees/dispatch/callback/field 등 실제 지원 action만 사용. 정적 등록/호출 후보/빌드 활성/런타임 관찰 구분. v0.15.7의 condition_semantics_version=2 및 legacy 조건 근거 차단·보존 준수.

질문 하나·source/build·scope 고정 → exact qualified ID/symbol/Message ID → 관계 유형/방향별 기본 1-hop → 필요한 정상 Procedure/Feature → Analyzer 실제 원문/반례 확인. 각 답은 snapshot, evidence, 검증 수준, 누락/잘림, 다음 조회 포함. Source Map pilot 상한: 4,096 실제 tokenizer tokens/50행, 코드 20파일/step·60파일/task, 추가 probe 최대 4단계, 총 입출력 32,768 tokens·20분/task; 실제 환경이 더 낮으면 그 값. Recovery의 전체 Seed 예산은 별도 고정하고 모든 소비를 합산, Map 질의 예산이 전체 탐색 완전성을 뜻하지 않음. 기존 Knowledge/MSC 원본 중복 작성 금지.

## 6. Recovery V2/V3 및 비교 실험의 충돌 해소

부록 B의 r0008 V0~V6·Cause Rule·Search Plan·보호 판정·MSC·단계별 수락을 유지. V2의 원인 규칙은 수정 전 실패, 수정 후 보호, 정상 반례 모두 설명하고 실제 resource/object/owner/generation·preconditions·trigger·first_violation·ordering·invariant·fix_mechanism·anchors·evidence를 포함. V3의 L1 API, L2 caller/callee/wrapper, L3 상태/자원/메시지/handler, L4 의미 대체 API(후속) 단계 순서 유지. 후보/coverage/제외·미조사·잘림 관리. V4의 네 판정(이미 해결됨/발생 불가능/미해결 확인/추가 검증 필요), V5의 적시 보호/복귀 소유권, V6의 실제 Analyzer·Converter 영수증 및 기존 writer/Kernel 연동 유지.

**주의: 기존 두 인계서의 D0~D3에서 D1 의미가 다름.** 이 통합본에서는 명칭을 분리해 시험 혼용과 중복 실행을 방지.

| 비교 | Recovery 원인 분리 R-D | Source Map 기여 M-D |
|---|---|---|
| D0 | 현행 Recovery | 동일 조건의 현행 입력 |
| D1 | 검증된 코드 fact 추가 | 제한된 검증 Map 추가 |
| D2 | 검증된 정상 Procedure 추가 | 동일 정상 Procedure 추가 |
| D3 | fact + Procedure | Map + Procedure |

동일 Seed/source/build/model/tool/범위/예산/독립 맥락에서 비교. R-D는 코드 fact 획득/전달과 정상 맥락의 효과, M-D3−M-D2는 기존 지식 위 Map의 추가 효과. D0/D2는 실험 조건 및 실제 입력이 같고 유효한 경우에만 재사용. Map이 없는 단계에는 R-D를 먼저 수행 가능. 단일 시험으로 원인 확정 금지. 동일 정답셋(모델 입력에 노출 금지), 별도 holdout, 기대 후보/정상 반례·미조사·오탐·시간·토큰·근거 없는 확정 기록. Source Map pilot의 양성≥30/음성≥10, recall≥90% 및 근거 없는 확정 0/variant stale 탐지 100%/범위 밖 읽기 0은 기존 목표. Recovery 대표 수락의 핵심 원인 오류·알려진 직접 후보 누락·근거 없는 확정·MSC 역순 0건은 별도 목표. A/B/C 단일 Agent/선택적 위임 시험은 이 비교와 별개; 반복 실패 입증된 단계 하나만 분리.

## 7. Viewer v0.5.7 → v0.5.8 연결 및 회귀

1. 실제 프로세스/서비스 경로, VERSION, 정적 파일·manifest, 활성 adapter·권한 확인. 현재 사용자 확인 v0.5.7 기준. 최신 v0.5.8의 독립 Source Map 메뉴/route·assets/source-map.js/.css와 기존 Knowledge read 경로 비교.
2. 기존 Knowledge와 동일 Workspace 저장·조회 방식을 재사용. 실제 source-map/의 활성 snapshot을 읽기 전용으로 exact symbol/Message ID, module/build, max50, 상태 OK/EMPTY/PARTIAL/STALE/CONFLICT/DENIED/ERROR로 표시. 실제 adapter의 지원 capability 확인. 제공 searchSourceMap/resolveSourceMapKnowledge는 합성 예시이며 실 API 존재로 간주 금지. 미확인 시 fail-closed.
3. 기존 Work/Knowledge/Recovery/MSC/검색/Write/업무 도우미/오늘의 업무/환경설정/권한·CSP 및 v0.5.7 Knowledge 순서 보존. Source Map에서 별도 MSC/편집/Job/쓰기 금지. Map→Knowledge 링크는 문서 ID/revision·source/build·인가 일치 시에만. 기존 문서 원문/분류/ID/schema/권한 변경 금지.
4. 실제 Source Map 저장 readback 및 Viewer 조회 결과의 snapshot/hash/source/build 비교. 권한 밖 제목/건수, stale/혼합 snapshot, 미생성 링크, 404/변조/경로 이탈 차단. Desktop/mobile 화면 회귀. 실제 활성 버전의 서비스 전환은 기존 승인 범위 확인 후만. 기존 서비스/백업/rollback 경로 보존.
5. 기존 회귀는 §1의 개발 PASS를 현장 PASS로 복사하지 않음. Analyzer 실제 CLI/guard/legacy patch, Viewer 8개 Node 프로그램/통합 browser 및 기존 A/H/T/V56/V57 시험, 실제 host E2E를 각각 기록. 다른 스킬은 변경하지 않고 실제 결손 증빙만 해당 소유자에게 전달.

## 8. 단일 회신·완료 기준

| 단계 | 필수 증거 |
|---|---|
| G0 | 기존 Work, D01~D07, 실제 활성본·Writer/Reader 경로/action·권한·설치 결과 |
| A1 Map 생성 | 대표 모듈 source/build·관계·근거/coverage, 기존 결과 재사용 |
| A2 Map 저장 | 기존 Knowledge Writer 동일 경로·actor/승인/expected revision·실제 source-map/·snapshot/manifest hash·readback |
| A3 Map 조회 | 동일 snapshot exact/1-hop, stale/unknown·인가·기존 Knowledge 링크, Viewer 실제 v0.5.8 또는 차단 |
| B0~6 Recovery | 기준선/R-D, 단계별 V2/V3 품질/오류·탐색량·회귀 및 사용자 확인 |
| B7 통합 | Analyzer/Converter 실제 호출·MSC 의미/파일·Work/Evidence 등록·readback·Recovery 목록/HTML/SVG 열람 |
| 공통 영향 | Kernel export 전후 Map/Knowledge hash, 기존 Work/Knowledge/Recovery/MSC/Write 회귀, 기존 스킬/권한 보존 |
| 최종 | 각 항목 PASS/FAIL/SKIP/NOT_RUN/BLOCKED, 근거 ref/hash, 변경 파일/revision, 재개점 및 다음 한 행동 |

현재 결론: 문서 계약 기준 조건부 GO. 현재 Viewer v0.5.7은 Source Map 전용 메뉴 미지원이지만 Recovery 실행과 Map 저장 자체를 차단하지 않음. 최신 패키지·실제 Knowledge Writer 및 Adapter 동작/활성 Analyzer/기존 Discovery 원본은 업무 환경 G0 대상. 실제 구현/설치/Job/그룹 게시/제품 효과 미실행. 신규 독립 리뷰 없음. 다음 한 행동은 G0에서 실제 기존 Knowledge 저장·조회와 Source Map 경로 매핑 가능 여부 및 기존 Discovery 7건을 회신.

## 9. 원본·우선순위·부록 읽는 법

본문 0~8절의 최신 사용자 결정과 통합 실행 순서가 우선. 아래 부록은 세 원문에서 추출한 상세 계약/예시/시험 기준이며 기존 절 번호는 해당 원문의 번호. 과거 Viewer v0.5.7을 역사 기록으로만 보는 문구는 최신 사용자 확인으로 대체; 기존 개발 후보의 승인 게이트는 유지. 부록의 D0~D3는 본문 §6의 R-D/M-D로 해석. 원문의 별도 요청/버전 지시를 중복 수행하지 않음. 기존 세 인계서는 감사/이력 참고이며 별도 전달 필수 아님.

- [Recovery r0008](./L1_RECOVERY_POINT_ANALYSIS_INTEGRATED_IMPLEMENTATION_HANDOFF_r0008_20261127_KST.md)
- [Source Map r0003](./L1_SOURCE_MAP_1500_UPDATER_INTEGRATED_HANDOFF_r0003_20261127_KST.md)
- [Viewer/Analyzer 개발 전달 r0001](./L1_SOURCE_MAP_VIEWER_ANALYZER_DEVELOPMENT_DELIVERY_r0001_20261127_KST.md)
- [기존 Source Map 저장·책임 경계](./L1_SOURCE_MAP_KNOWLEDGE_UPDATER_VIEWER_SCOPE_HANDOFF_r0001_20261127_KST.md)
- [기존 Recovery/Kernel/Converter 연동 계약](./L1_CHANNEL_RECOVERY_VIEWER_KERNEL_CONVERTER_COMPLETE_HANDOFF_r0001_20261124_KST.md)


---

# 부록 A. Source Map r0003 상세 작성·샘플·시험 계약 (원문 발췌)

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

---

# 부록 B. Recovery r0008 상세 단계 및 회귀 계약 (원문 발췌)

## 4. G0 및 기준선 (변경 전)

1. 기존 Work/Seed와 실제 실행 실패 결과, 활성 Recovery/Analyzer/Converter/Workflow/Kernel/Viewer 버전·revision·action·권한·영수증을 확인. 필요한 의존 단계만 보류하며 독립 분석을 막지 않음.
2. 이번 요청의 명시 제품 소스 폴더를 우선 검증. 미지정이면 같은 프로젝트의 유효한 저장 경로 재사용. 경로 불명/권한 오류/복수 후보 또는 요청 revision 불일치 시 필요한 선택만 한 번 질문. 유효 경로와 revision 미지정이면 관찰 Git commit/P4 revision 고정. 경로 오류 시 임의 다른 경로 전환/checkout/전체 디스크 탐색 금지. 무인 실행이면 미확인과 재개 위치 보존.
3. PR/CL 수정 전·후·현재 source revision/build, 파일/확장/시간/토큰 예산, 모델/설정, 실제 조사 범위를 고정. 기존 Work의 비-timeout Seed 1건을 사용. 담당자가 원인·기대 후보·정상 반례를 평가용으로 별도 고정하고 정답은 모델 입력에 노출하지 않음.
4. 현행 결과(D0)를 보존. 동일 조건의 기존 영수증이 유효하면 재사용. 이전 r0006 비교 자료가 없거나 조건이 다르면 비교 불가로 표시하되 강화 단일 실행 자체의 수락 시험은 진행 가능.

## 5. V0~V6 전체 분석 계약

| 단계 | 실행·출력 | 통과/재개 |
|---|---|---|
| V0 입력 고정 | Work/Seed/경로/revision/build/예산 | 불명확하면 해당 입력만 보류 |
| V1 Seed 전후 | 실제 diff·주변 코드로 증상·실패 인과·Fix 효과·한계 검증 | Jira/PR 주장과 코드 사실 분리 |
| V2 Cause Rule | 객체·자원·세대·소유권·필수 전제·최초 위반·정상 불변조건 | 전/후/정상 반례 일치 시 V3 |
| V3 Search Plan | 명시 검색 조건·후보·coverage·잔여 범위 | 원본 대조, 미조사/잘림 보존 |
| V4 보호 판정 | 같은 작업의 첫 위반 전 보호 효력, 우회 분기·반례·빌드 | 4분류 및 종결 재검사 |
| V5 조치 | 검출·원인 수정·사전 검사·국소 복구·상위 이관 비교 | 소유권·부작용·복귀·실패 처리 |
| V6 산출 | 검증 Scenario IR·MSC·보고서·기존 writer | 두 생산자 호출, 의미/저장/열람 분리 |

### 5.1 V2 Cause Rule (최신 구현 계약)

V1→V2에서 관련 정상 Procedure의 시작/종료, 호출·메시지 순서, 모듈 책임, 상태 전이, 객체/세대/자원 소유권 및 비동기 경계를 확인. 필요한 기존 Knowledge를 revision/build 대조하여 재사용하고 부족한 경우 해당 정상 경로만 추가 분석.

필수 구조:
```yaml
cause_rule:
  rule_id: null
  resource: null
  object: null
  owner: null
  generation: null
  preconditions: []
  trigger: null
  first_violation: null
  ordering: []
  invariant: null
  fix_mechanism: null
  anchors: []
  evidence:
    before_fix: []
    after_fix: []
    normal_case: []
  confidence: UNKNOWN
  validation: UNVERIFIED
```
위 예시는 보고서/단계 산출물의 논리 구조이며 신규 저장 schema가 아님. evidence는 source revision/build/path/function/line 및 실제 참조. 하나의 if문/함수명으로 규칙을 대신하지 않음. 수정 전 최초 실패, 수정 후 적시 보호, 정상 반례를 동시에 설명해야 함. 규칙이 다수이면 분리. 형식 적합과 의미 정확도를 별도 검사. 근거 충돌/부족은 보류하고 다음 조회 명시. CONFIRMED/INFERRED/UNKNOWN과 시험 PASS/FAIL/NOT_RUN 구분.

### 5.2 V3 Search Plan (최신 구현 계약)

Cause Rule의 원본 확인 anchors를 검색 조건으로 변환. LLM은 의미 판단에 집중하고 후보 열거는 기존 Analyzer 및 허용된 결정론적 검색 사용.

| 수준 | 탐색 | 우선순위 |
|---|---|---|
| L1 | 동일 API 호출 위치 | 우선 |
| L2 | 직접 caller/callee·wrapper | 우선 |
| L3 | 동일 상태 read/write·자원·메시지·handler | L1/L2 검증 이후 |
| L4 | 다른 API의 의미적 동일 동작 | 후속 별도 설계 |

Search Plan 필수 항목: rule_id, source revision/build, scope, anchors, query 종류, 실제 지원 action/인자, 파일/확장/시간/토큰 상한, 제외 기준, 종료 및 재개 조건. 문자열 검색은 후보 열거이며 overload/macro/조건부 컴파일/간접 호출/비동기 dispatch는 원문 대조. Source Map은 검증된 정적 관계를 보조로 쓰되 실제 도달·순서의 증거로 단정하지 않음.

Candidate 필수 항목: candidate_id, rule_id, path/function/line, 발견 query, 객체/작업 관계, 근거, 관련/무관/미확인, 제외 이유, 조사 상태. 동일 위치라도 객체/빌드/경로가 다르면 일괄 합치지 않음. 전체 파일 분모, 실제 읽은 서로 다른 제품 파일, 메타데이터 별도, hit/중복/제외/조사 완료/미조사/잘림/잔여 범위/종료 이유 기록. 예산 도달 또는 추가 근거 없음에서 종료하고 재개점 남김. 후보 관련성은 결함 확정 아님. V3 누락을 V4 종결 검사로 대체하지 않음.

### 5.3 V4/V5 기존 판정·조치 유지

| 판정 | 필수 근거 |
|---|---|
| 이미 해결됨 | 현재 build·같은 작업의 관련 실패 분기에서 첫 위반 전에 동등 보호 |
| 발생 불가능 | 해당 후보에서 필수 전제가 성립하지 않는 build/객체/분기 근거 |
| 미해결 확인 | 같은 작업의 입력→실패 분기→최초 위반 및 보호 결손 |
| 추가 검증 필요 | 확인되지 않은 관련 분기/순서/소유권/빌드 또는 상충 근거 |

종결 전에 반대 근거, 보호 우회, 다른 작업 세대 callback을 재검사. HAL 실패 판단 뒤 정리하더라도 그 전에 잘못된 성공 통지가 나갔다면 적시 보호가 아님. V5는 검출 신호 → 정리 권한·실제 획득분 → 부분 SW/HW 부작용 → 종료 통지 → 복귀 확인 → 실패 시 상위 이관. 공유 RF/다른 Stack 영향과 소유권 불명 시 무조건 국소 복구 금지. 제품 변경은 별도 승인 및 실시간/고정 자원 제약(new/delete 금지). 상세 조치 분류는 r0007 §4 유지.

### 5.4 V6 MSC 및 Work/Viewer 통합

- Analyzer 실제 호출의 버전/action/revision/범위/결과/원본 근거/영수증 기록. 줄 번호나 양 끝 이름만으로 호출/등록/런타임 순서를 확정하지 않음.
- Seed 수정 전·후, 현재 후보 AS-IS, 제안 TO-BE를 분리. 검증된 Scenario IR의 발신/수신/순서/분기/비동기 대응 원본 대조. Edge 정의·근거는 Recovery 책임. 미확정 Edge 의존 요소만 보류하고 독립 검증 요소는 변환. 조치 없음은 해당 없음 사유 기록.
- Converter 실제 호출 후 입력 해시·영수증·PlantUML/SVG/B형 HTML·상대 링크·SHA 기록. 형식 PASS만으로 의미 PASS 금지. 역순/방향/메시지 불일치 또는 검증 불가 산출물은 등록·링크 차단. 실패 입력 보존 후 해당 IR/변환만 재개.
- 기존 승인 writer의 preview→source SHA/Evidence revision 고정→등록→readback 사용. 11/24 개발 계약: provider=l1-channel-recovery, kind=recovery_analysis, stage=utility; recovery_report_preview, record_recovery_report, work_recovery_reports는 실제 활성 action 대조 후에만 사용. UTF-8 MD/JSON 5 MiB 이하 조건도 설치본 확인. Work ID 유지, 등록 응답/Evidence ID/SHA/revision/재조회 기록. utility 첨부는 제품 효과 검증 완료 아님.
- Kernel이 기존 works/<work-id>/RECOVERY.md, state/recovery_reports.json, 루트 RECOVERY.md, index/recovery.json 및 recovery/README.md, recovery/index.json, recovery/works/<work-id>/<Evidence ID>.md 파생 보기 관리. Recovery가 직접 쓰거나 새 schema 생성 금지.
- Viewer의 Recovery 메뉴/목록/검색/상세 → 기존 Work → 검증된 MSC HTML/SVG 본문 링크 유지. 별도 MSC 탭은 만들지 않음. 실제 adapter/ACL/SHA/CSP/경로 확인. 합성 API/fixture를 운영 서비스에 덮어쓰지 않음. Source Map 메뉴는 별개 읽기 경로이며 Recovery 데이터를 재분류하거나 강제 이관하지 않음. 기존 Knowledge 섹션 순서/표시 변경은 Viewer 책임.
- 저장이나 열람 실패는 각 담당에게 근거와 재개점 전달. 분석·MSC 유효 결과는 그대로 보존.

## 6. 원인 분리 실험 및 최소 Knowledge

동일 Seed/revision/build/모델/도구/예산에서 독립 맥락으로 비교. 가능하면 반복하여 변동성 기록. 기존 결과 재사용은 입력과 영수증이 일치할 때만. D0는 변경 전 기준선으로 유지.

| 조건 | 제공 입력 | 판단 단서 |
|---|---|---|
| D0 | 현행 Recovery | 비교 기준 |
| D1 | 검증된 코드 fact 추가 | 사실 획득/전달 문제 |
| D2 | 검증된 정상 Procedure Knowledge 추가 | 정상 맥락 부족 |
| D3 | D1+D2 | 상호 보완 또는 잔여 오류 |

개선이 관찰돼도 단일 시험으로 원인 확정하지 않음. D3 실패 시 단계 지침/도구 사용/추론 한계를 추가 분리(필요시 동일 입력 강한 모델 비교, 별도 허용 범위). 정답 혼입·중복 입력 통제. 정상 Procedure 한 건만 기존 Updater로 조회/검증하거나 필요 시 생성. Module/Feature/Procedure/Scenario 교차 참조, 정상 MSC, 상태/소유권/순서 불변조건, revision/build/원문 포함. 오래되거나 충돌한 지식은 가설로 취급. 전체 지식 구축은 별도 결정.

## 7. 단계별 구현 순서 및 수락

| 차수 | 진행 | 수락 증거 |
|---|---|---|
| 0 | 활성 계약 G0, 현행 기준선/원인 분리 | 동일 Seed 기준 D0 및 D1~D3 비교 가능한 범위, 결손과 변경 지점 |
| 1 | V2 구조화 | 개발자 원인 판정 일치, 필수 필드 및 원본 참조 |
| 2 | V2 반례/원본 게이트 | 틀린 규칙의 V3 진입 차단 |
| 3 | Cause Rule→Search Plan | 실제 symbol/action, 범위/예산/재개 매핑 |
| 4 | V3 L1/L2 | 기대 직접 후보 누락·오탐 및 원문 대조 |
| 5 | 후보/coverage | 중복/제외/미조사/잘림 재현 및 재개 |
| 6 | V3 L3 | 상태·자원·메시지/handler 탐색, 실제 결손만 보완 |
| 7 | V4~V6 회귀·연동 | 기존 보호 판정/조치/MSC/등록/열람 계약 유지 |

차수마다 최소 변경·독립 시험·롤백 가능 상태·사용자 확인. D1~D3 수행에 필요한 자료가 없다면 진단 미확인과 제약을 기록하고, 확보한 기준선으로 독립 가능한 개선을 진행할지 사용자와 확인. 동일 Seed 전후 비교 및 별도 Seed 일반화 검증. V2 핵심 원인 오류, 알려진 직접 후보 누락, 근거 없는 확정, 잘못된 MSC 순서 각 0건을 대표 수락 목표로 설정. 전체 제품 코드 무결함을 보장하지 않음. V3 recall/precision은 분모와 함께, V4 오종결/보류, V5 조치 타당성, V6 의미 오류, 시간/토큰/실제 조사량을 보고.

**Agent 비교:** r0007 A(현행 r0006 또는 비교 가능한 기존 결과) / B(강화 단일 실행) / C(반복 결손 단계 하나 분리) 유지. D0~D3는 원인 분리 실험으로 A/B/C와 별개. B 충족 시 단일 실행 채택. 반복 오류의 위치가 입증된 경우만 seed-analyst 또는 candidate-checker 등 한 역할, 순차·깊이 1·읽기 전용으로 시험. 동일 전체 예산 합산, 프라이머리 최종 판정·등록 요청 책임 유지. 위임 불가 시 단일 경로 유지. 병렬화/전체 인덱스는 별도 실측 후 판단.

## 8. 최종 통합 시험 및 회신

| 시험 | 확인 |
|---|---|
| T01 | 명시/저장 경로·revision 분기, 질문 최대 1회, 입력 고정 전 분석 0 |
| T02 | Seed 전후·정상 반례 V2 원인 규칙 및 잘못된 규칙 차단 |
| T03 | V3 직접 호출/등록/상태/guard/빌드, 예산·미조사·누락/오탐 |
| T04 | V4 적시/늦은 보호·비활성 build·다른 세대 callback·종결 반대 근거 |
| T05 | V5 검출·소유권·부작용·복귀·금지 조건 |
| T06 | Analyzer 및 Converter 실제 영수증, MSC 네 관점·역순/방향 차단·미확정 Edge |
| T07 | Work/Evidence 등록·SHA/revision/CAS·readback·중복 방지 및 파생 Recovery 인덱스 |
| T08 | Viewer Recovery 목록→상세→Work→실제 HTML/SVG 본문 링크, ACL/CSP/404/변조/경로 이탈 차단, 데스크톱·모바일 |
| T09 | 기존 Viewer A01~A10/H01~H05/T1~T8 및 V56/V57과 최신 Source Map 변경 회귀(별도 Viewer 담당) |
| T10 | 단계별 실패/재개, 유효 결과 재사용, 중복 모델/Job/Analyzer 호출 0 |

최초 회신: ACTIVE_G0(버전/실행 action/권한/설치 결과), 기존 Work/Seed·기준선, 기존 구현 대비 gap·변경 파일·차수별 시험 계획. 이후 차수별 PASS/FAIL/SKIP/NOT_RUN/BLOCKED, 실제 결과·근거·지표(분자/분모)·변경 revision·재개점·다음 한 행동. 분석·MSC·Work 저장·Viewer 연동·제품 효과를 각각 판정. 실제 제품 시험 미실행이면 제품 효과 미검증. Viewer/Kernel/Converter 통합 결손은 독립 담당 작업으로 전달하고 Recovery 구현의 전체 선행 게이트로 만들지 않음.

---

# 부록 C. Viewer/Analyzer 개발 전달 및 당시 시험 기록 (원문 발췌)

※ 아래는 최초 개발 전달 당시 기록. 이후 격리 전체 시험은 부록 A 및 본문 §1 참조. 실제 업무 호스트 시험은 별도.

## 1. 패키지 및 고정 원본
| 대상 | 기존 원본 | 신규 ZIP | 크기(bytes) | 신규 SHA-256 | 게시 commit |
|---|---|---|---:|---|---|
| Viewer | v0.5.7 | [l1-workspace-viewer-wiki-integrated_v0_5_8_1127.zip](../l1-workspace-viewer-wiki-integrated_v0_5_8_1127.zip) | 301164 | 5d7935edba33bf062d167c95f3a44c620c683c33accc9c7aadacb69561fa73de | e80cb844d4409b8b60ca212d2822bd91f1692891 |
| Code Analyzer | v0.15.6 | [code-analyzer_v0_15_7_1127.zip](../code-analyzer_v0_15_7_1127.zip) | 627385 | 6a11cb8685c46d1ac22a1465968193a72708ca90bcfcf453b371c869abdfbeab | d015c6c5c7d7e37ee93e3760ca3022cc48a0a3b8 |

기준 main commit 7d2d59e4b23547598152850439291e84eb782025. 원본 ZIP SHA-256: Viewer 4a7a7ce742106cebbb4192c250a716ec303ac223ad31fb9673dfe61cb8332ddd; Analyzer bf1f369aed47e75c38fad3061041e720d5497953b0d90bcf4dc2fbf0d97b69ef. 기존 ZIP 보존. 신규 ZIP의 실제 원격 bytes 재조회 후 해시 일치. CRC·경로 및 manifest 전수 확인. 변경 파일 외 기존 원본 bytes 유지(Viewer 37개, Analyzer 214개). Viewer 변경된 파일은 재압축하여 크기가 감소했으며 내용 보존은 파일 해시로 확인.

## 2. 변경 범위
### Viewer
- index.html, assets/app.js: 독립 Source Map route, 메뉴, 기존 Knowledge 대상 route, 조회 취소 및 stale 응답 방지.
- assets/source-map.js/.css: 정확 심볼·Message ID 검색, Module/Build 필터, 최대 50개 결과, 증거·snapshot/revision/build, 상태(OK/EMPTY/PARTIAL/STALE/CONFLICT/DENIED/ERROR), 정적 후보와 실제 동작 순서 분리. 기존 Knowledge 링크는 권한 및 source/document revision, build 확인 가능한 경우에만 제공.
- fixtures/demo-data.js, adapters/adapter.js: 합성 데이터 및 읽기 adapter. 실제 업무 데이터 없음. 접근 불가 relation 제외. 기존 Knowledge·MSC·Recovery 문서와 storage schema 수정 없음.
- standalone-preview.html: 통합 자체 포함 미리보기, CSP inline 해시 재생성. tools/build_release.py, VERSION, README_INTEGRATED.md, manifest.sha256 및 개발 노트 갱신.
- tests/source-map.cjs, tests/source-map-fixture-tests.cjs 신규.

### Code Analyzer
- scripts/ca_core/probe_engine.py: 전처리 분기 frame, 이전 sibling 조건 배제, nested scope pop, 물리적 source anchor, line splice 후 lexical sanitize. #elif B → !A && B, #else → !A && !B, #endif 밖에는 해당 frame 조건 없음. 실제 build_activation은 UNKNOWN, 해석 불가 조건은 UNCERTAIN, 파일 budget 초과 aggregate는 partial.
- scripts/ca_core/patch_writer.py: condition_semantics_version=2 및 확정성 점검. 신규 incoming legacy 조건 근거 제외; 기존 legacy pending patch는 덮어쓰지 않고 명시적 오류로 보존, 새 scope에서 원본 재분석 필요.
- tests/test_compile_condition_v0157.py 신규. 버전/설치 메타 및 manifest 갱신.
- Analyzer는 근거 생성만 담당. Source Map 저장·지식 판단·게시, Viewer 렌더링 책임은 이 스킬에 추가하지 않음.

## 3. 실제 시험 및 미실행
| 항목 | 상태 | 범위 |
|---|---|---|
| Analyzer 기존 Outside 오류 재현 | PASS | 격리 harness에서 기존 원본 함수, 수정 후 해당 조건 사실 없음 |
| Analyzer 신규 집중시험 | 9 PASS / 1 SKIP | 격리 harness; 실제 패키지 CLI 1개 skip |
| C++ 전처리기 대조 | PASS | A/B 4조합 |
| Analyzer 기존 75 회귀·실제 CLI·설치 --home 자체점검 | NOT_RUN | 로컬 DNS/ZIP 반입 제한 |
| Viewer 신규 집중 Node 2개 프로그램 | PASS | 합성 분리 harness |
| Viewer Chromium 1280/360px | PASS | 합성 분리 화면: 검색/상세/Knowledge 링크/복귀/연속 조회/권한/키보드/overflow |
| Viewer 실제 ZIP fixture/adapter 보조검증 | PASS | JS parse, DemoTx 두 build 및 Knowledge 링크 |
| Viewer 기존 6개 Node 프로그램·통합 브라우저 | NOT_RUN | 원본 ZIP 로컬 반입 제한 |
| Viewer CRC/manifest/원격 SHA | PASS | 51/51, 50/50, 원격 전체 bytes |
| Analyzer CRC/manifest/원격 SHA | PASS | 224/224, 223/223, 원격 전체 bytes |
| 업무 실제 데이터·권한·호스트 adapter E2E | NOT_RUN | 업무 GPT 확인 필요 |

분리 harness의 PASS를 전체 설치본 검증으로 승격하지 않음. GitHub bytes 경로에서 원본 ZIP을 검증·수정·재패키징했으며 로컬 시험은 해당 신규 코드의 격리 실행에 한정.

## 4. 업무 GPT 실행 요청 (별도 승인 범위 내)
1. 위 두 ZIP의 실제 bytes SHA-256 대조. 기존 활성본과 백업 보존, 임시 디렉터리에서만 압축 해제·검증. Viewer standalone-preview.html 확인.
2. Analyzer 기존 75개 회귀 및 신규 test_compile_condition_v0157.py 전체, 실제 CLI와 임시 --home 설치 자체점검 수행. #if/#elif/#else/#endif, nested, splice, unsupported/UNCERTAIN, budget, legacy patch 거부 및 보존을 확인. 기존 legacy patch를 임의 삭제하지 않고 새 scope 재분석.
3. Viewer 기존 6개 Node 프로그램과 신규 2개, 전체 통합 브라우저 desktop/mobile 실행. Work/Knowledge/MSC/Recovery/검색/편집/도우미 회귀 확인.
4. 실제 기존 host adapter 및 권한·source snapshot/build/document revision 계약 확인. 합성 searchSourceMap/resolveSourceMapKnowledge는 UI 연결 예시이며 실제 API 존재를 주장하지 않음. 미확인 상태에서는 fail-closed. 업무 데이터는 업무 환경에만 유지.
5. 결과를 PASS/FAIL/SKIP/NOT_RUN, 원본/활성본 revision, Evidence 경로, 실제 연결 여부로 보고. 모두 통과 후에만 별도 운영 적용 판정. 추가 독립 리뷰 없음.

다음 한 행동: 업무 GPT에서 격리 전체 회귀 및 실제 adapter 계약 확인을 시작할 수 있도록 본 인계서와 두 ZIP을 전달.
