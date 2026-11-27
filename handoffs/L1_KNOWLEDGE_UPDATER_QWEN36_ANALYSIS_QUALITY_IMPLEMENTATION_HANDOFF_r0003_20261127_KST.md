# L1 Knowledge Updater 전용 통합 설계·구현 인계 r0003

- 2026-11-27 KST · 업무 GPT 설계/최종 판정 → 기존 업무 환경 OpenCode/Qwen3.6-27B 구현·실행.
- 기준: 11/25 Updater 분석 품질 r0002 전체 계약, 11/27 Source Map r0003, 11/27 Recovery·Source Map·Viewer 통합 r0001, 11/26 Viewer v0.5.6/v0.5.7 지식 문서 표시 역할.
- 목적: 기존 Updater의 코드 분석·지식 문서 생성·MSC·저장·갱신 품질 향상과 Source Map 공통 기반 추가. 기존 Updater가 실제로 무엇을 지원하는지 확인하고 누락된 지침/호출부만 최소 보완.
- 본 문서가 **Updater 전용 최신 단일 실행 기준**. 기존 Recovery·Source Map·Viewer 통합 인계는 해당 담당 범위에서 계속 유효. 동일 G0·대표 사례·Source Map 구축·Viewer 연결을 중복 수행하지 않음.
- 사용자 최신 확인: 실제 운영 Viewer v0.5.7; Source Map의 상위 폴더 l1-workspace/, knowledge/와 동등한 source-map/; 기존 Knowledge와 동일한 저장 방식 필수.
- 신규 독립 리뷰 없음. 문서 게시 자체는 제품 코드 변경·운영 설치/서비스 재시작·Job 예약/실행·그룹 게시 승인 아님. 실제 업무 구현 및 호스트 E2E는 미검증.

## 0. 업무 GPT 단일 요청문

> 기존 l1-knowledge-updater의 활성 SKILL.md/가이드/실행 entrypoint/실제 지원 action 및 기존 Work·Knowledge·Discovery 결과부터 확인해 주세요. 기존 Updater r0002의 분석 품질·실제 Code Analyzer/Doc Converter 호출·분류·근거·MSC·개인/그룹 지식 저장 계약을 유지하면서, 아래 r0003의 문서 작성 기준과 Source Map 생성/갱신/저장/조회 활용 요구를 통합해 주세요. Source Map은 반드시 기존 Knowledge와 동일한 Writer/저장·조회 방식으로 l1-workspace/source-map/에 저장하고, 별도 Writer/DB/저장 엔진을 새로 만들지 마세요. 기존 Discovery 7건과 유효 지식/MSC를 재사용하고 대표 NR L1 Tx → UL Tx Switching 시나리오 한 건으로 변경 전후 품질을 측정해 주세요. 신규 Knowledge 작성 시 유형별 표준 섹션 순서를 적용하되 기존 정본은 일괄 재작성하지 마세요. 실제 Code Analyzer와 Doc Converter를 호출하고 원본 근거·시나리오 의미·HTML/SVG를 검증해 주세요. Kernel/Workflow/Converter/Viewer/Analyzer의 별도 내부 변경을 Updater 작업에 포함하지 말고 입증된 결손만 해당 소유자에게 전달해 주세요. 이미 완료된 연계 시험을 재사용하고 단계별 근거/실패/재개점을 회신해 주세요. 추가 독립 리뷰는 하지 마세요.

## 1. 변경 범위·현재 운영 기준

| 구성 | 실제 확인/최신 게시 | Updater 작업 범위 |
|---|---|---|
| l1-knowledge-updater | 업무 GPT 관리, 활성 원문/version 미확인 | 기존 기능 유지, 가이드·오케스트레이션·지식/Map 관리 연결 |
| code-analyzer | v0.15.6 사용자 적용 확인, 최신 v0.15.7 게시 | 실제 활성 version/action 확인 및 재사용. 직접 호출·전처리 guard·coverage 근거 검증 |
| doc-converter | 최신 v0.2.26 | 검증된 Scenario IR→PUML/SVG/B형 HTML 실제 호출 |
| Viewer | **실제 운영 v0.5.7**, 최신 게시 v0.5.8 | 기존 표시/읽기 계약 소비. Source Map 전용 메뉴 및 실 adapter 연결은 별도 Viewer 담당 |
| work-ledger-kernel | 최신 v0.7.47 | 기존 Work/Evidence 및 export. 별도 지식/Map writer 구현 금지 |
| l1-fix-workflow | 최신 v1.6.75 | 기존 Work 선택/재개/조회·첨부, 개인 Knowledge/Map READ_ONLY. 같은 version 후보 hash 구분 |
| knowledge-analysis-preflight | v0.2.0 | 선택적 기존 입력/문맥/분류/근거 검사; 실제 호출·토큰/coverage 대체 아님 |
| 기존 Knowledge Writer / Reader | 실제 호스트 계약 확인 | knowledge/와 source-map/ 동일 저장/조회 방식 재사용 |
| Recovery | 별도 업무 GPT 관리 | 검증된 Map/Procedure 읽기 소비, 기존 Recovery 분석 계약 유지 |
| Skill Updater / Job List / MCP | 기존 관리 경로 | 자동 배포/Job/조회 경로 변경 없음; 입증된 읽기 결손만 별도 제안 |

최신 게시 ZIP과 활성본을 구분. Viewer 0.5.7은 현재 운영본이며 과거 기록으로만 취급하지 않음. Analyzer 0.15.6 사용자 적용 확인을 반영하되 0.15.7 실제 활성 여부는 확인. v0.5.8/v0.15.7 이전 개발 전달서의 development_not_for_deployment 표기와 자동 배포 원본 게시 정책이 충돌할 수 있음. 실제 Skill Updater 결과 및 서비스 경로를 확인하고 승인 범위 내에서 적용. 자동 설치/다운그레이드/구버전 재설치/운영 재시작을 이 문서에서 강제하지 않음. 비교 시험 중 도구/모델 버전 고정.

최신 개발 패키지: [Analyzer v0.15.7](../code-analyzer_v0_15_7_1127.zip) SHA-256 6a11cb8685c46d1ac22a1465968193a72708ca90bcfcf453b371c869abdfbeab; [Viewer v0.5.8](../l1-workspace-viewer-wiki-integrated_v0_5_8_1127.zip) SHA-256 5d7935edba33bf062d167c95f3a44c620c683c33accc9c7aadacb69561fa73de. 기존 개발자 격리 시험 Analyzer 85/85 PASS, Viewer 8/8 Node 프로그램 PASS는 현장 결과가 아님.

## 2. Updater 전체 동작 계약

| 순서 | 업무 | 핵심 결과 |
|---|---|---|
| U0 | 요청·기존 Work/Knowledge/Map 조회 및 source revision/build/범위 고정 | 기존 결과/영수증 재사용, 미확인 입력만 질문 |
| U1 | Discovery/Source Map exact lookup·방향별 1-hop, 필요한 경우 정상 Procedure 조회 | 관련 후보 및 누락/범위, Map 부재 시 기존 Analyzer 직접 탐색 |
| U2 | 기존 code-analyzer 실제 호출 | 호출/등록/분기/IPC/state/비동기 등 원본 근거 및 coverage |
| U3 | 원본 검증·의미 판정 | 실제 명제와 근거, UNKNOWN/CONFLICT, 필수 질문 누락 확인 |
| U4 | Module/Feature/Procedure/Scenario/Issue Knowledge 작성 | 유형별 표준 섹션, 기존 ID/variant/교차 참조, AS-IS/TO-BE 구별 |
| U5 | 필요한 시나리오의 검증 IR 및 doc-converter 실제 호출 | PUML/SVG/HTML/manifest/영수증 및 변환 전후 의미 대조 |
| U6 | 기존 Work/Evidence 기록 | 기존 승인 writer/Kernel 등록·SHA/revision/readback |
| U7 | 개인 Knowledge 저장 및 Map 갱신 | 기존 Knowledge Writer, 각 독립 경로/정본·검증·readback |
| U8 | 기존 그룹 Knowledge 비교·Preview | 승인 없으면 그룹 write 0; 승인 후 CAS·readback·역링크 정산 |
| U9 | Viewer/공통 읽기 연결 확인 | 동일 snapshot/문서 revision/ACL, 별도 담당 결과 |

U0~U9는 논리 실행 순서이며 신규 API/원장/schema가 아님. 단순 지식 편집, 기존 Work 지식화, Source Map 자체 갱신 등 요청 종류에 따라 필요한 단계만 실행. Map 구축은 기존 Knowledge나 Recovery 분석의 필수 선행 작업이 아님. U7의 Map 갱신은 발견된 실제 변경/결손 또는 사용자 요청에 한해 진행하며 모든 지식 작성마다 전체 Map 갱신/재분석 강제 금지. Source Map 작성 자체는 동작 설명/MSC 생성이 필요하지 않음. 기존 r0002의 실제 호출·품질·권한·재개 규칙은 부록 A 전체 유지.

## 3. 지식 분류 및 신규 문서 작성 표준

**기존 기술 분류를 유지**: Module→Feature→Scenario, Procedure는 Module 내 API/업무 절차와 관련 Feature/Scenario를 교차 연결. Issue Knowledge는 증상·원인·수정·검증 중심의 기존 지식 유형으로 사용하며 새 분류 계층/ID 강제 생성 금지. Source Map은 별도 공통 코드 관계 정본이지 Module/Procedure/Feature/Scenario 또는 MSC의 복제본이 아님.

Viewer v0.5.6의 다섯 유형 역할 및 v0.5.7 표시 순서를 기반으로 **신규/실제로 변경하는 Knowledge의 작성 가이드**를 이번 r0003에 추가. 기존 문서 형식·ID·제목·링크·개인/그룹 정본을 보존하며 기존 템플릿에 매핑. 다음 순서는 사용자가 검토하고 적용할 신규 작성 기준이며 과거 Viewer가 Updater 원문을 수정했다는 뜻이 아님.

| 지식 유형 | 권장 순서 (기존 verified 역할 대응) |
|---|---|
| Module | Functional Overview → Software Architecture → 구성 요소 → 인터페이스 → Features → 제약 → 코드 근거 |
| Feature | Functional Overview → 설계/동작 원리 → 동작 조건 → 상태/전이 → Scenarios → 예외 → 제약 → 코드 근거 |
| Scenario | Functional Overview → 동작 조건(Trigger/Precondition) → Software Architecture → Scenario Flow → MSC(본문 링크) → 예외 → 제약 → 코드 근거 |
| Procedure | Functional Overview → API → Caller/Callee → Parameters → 동작 조건 → Returns → Side Effects → 예외 → 코드 근거 |
| Issue Knowledge | 증상 → 원인 → 수정 → 영향 → 검증 → 코드 근거 |

모든 유형에 실제 목적/범위·RAT/variant·source revision/build·기존 지식 ID/문서 revision·근거 및 적용 상태를 기존 형식으로 연결. 실제 내용이 없는 섹션은 미확인/해당 없음과 이유를 필요한 범위에서 표시; 기술 사실을 채우기 위한 추정 금지. 기존 분류 규칙과 현장 템플릿이 다르면 차이와 매핑을 보고하고 ID·schema를 임의 변경하지 않음. 전체 기존 문서 일괄 재배열/재분석/MSC 재생성 금지. Viewer는 verified headingId/headingText/role와 문서/source revision 일치 시 표시를 재정렬할 수 있고, Updater는 DTO·UI를 직접 구현하지 않음. 별도 MSC 탭을 만들지 않고 기존 시나리오 본문에서 실제 HTML/SVG 링크 제공.

## 4. Source Map 생성·갱신·저장 계약 (최신 결정)

```text
l1-workspace/
├── works/       # Work/Evidence, 기존 Kernel
├── knowledge/   # 기술 지식, 기존 Knowledge Writer
├── recovery/    # Kernel 파생 Recovery 조회
├── source-map/  # Source Map, 동일 Knowledge Writer
└── index/       # 기존 Kernel 공통 index
```

- Updater가 Source Map의 발견/대조/정규화/검증/snapshot 생성·증분 갱신 및 저장 요청을 단독 담당. 실제 저장은 **기존 Knowledge Writer와 동일한 root/경로 해석·actor/권한·승인·Preview/CAS·이력·readback 방식**을 사용. 별도 Writer/DB/저장 엔진 금지.
- 실제 Knowledge Writer가 source-map/을 지원하지 않으면 기존 경로 매핑의 입증된 결손만 별도 최소 확장 제안. 쓰기 권한·원자적 전환을 확인할 수 없으면 후보와 이전 활성본을 보존하고 해당 저장 HOLD. Kernel/Workflow 수정이나 raw Git/shell 우회 금지.
- 기존 Reader/Adapter에서 같은 Workspace root와 읽기/ACL 정책 재사용. exact symbol/Message ID·방향별 1-hop·변경 영향 역조회에 필요한 실제 지원 기능 확인. Source Map 자체 write 기능은 Viewer에 추가하지 않음. 조회 미지원/stale/partial이면 Analyzer bounded probe로 독립 진행.
- 논리 후보 README.md/manifest.json/nr/lte/common/interfaces/index/history/gaps.md는 기존 파일 형식·Discovery 산출물에 매핑. 새 파일명/JSONL/DB/schema/API를 필수로 강제하지 않음. 구조화 정본과 MD/Viewer 표현은 동일 snapshot에서 파생. code anchor/관계/Evidence ID·기존 Knowledge 참조 중심, 제품 원문·상세 분석/MSC는 기존 Work/Evidence 및 Knowledge의 정본 유지.
- 동일 source revision/build/scope/hash 재사용. snapshot별 manifest·producer/version·coverage·predecessor, staging→무결성/권한 검증→기대 revision CAS→readback. 한 조회의 snapshot 고정, 경쟁/중단/응답 유실 시 기존 활성본 및 후보 보존. 변경/삭제/rename/등록 변경·공통 헤더·매크로·build config의 전후 역의존을 계산하여 영향 범위만 갱신. 삭제된 관계의 역참조 제거 또는 tombstone 및 stale 링크 검증. 전체 재구축은 국소 갱신이 불가능할 때만 평가.
- Analyzer는 기존 probe symbol/callers/callees/dispatch/callback/field 등으로 코드 사실 제공. Updater가 추출 명제·근거 수준 정규화. v0.15.7 condition_semantics_version=2의 sibling/nested guard 및 실제 활성 UNKNOWN/해석 불가 UNCERTAIN을 구분. legacy pending patch를 임의 덮어쓰지 않음. 정적 등록/도달 후보/실제 runtime 순서 각각 분리.
- Recovery·Analyzer·Updater·Viewer는 동일 Map의 읽기 소비. 소비자가 발견한 누락은 기존 Work에서 갱신 후보로 남기고 Updater가 수정. 별도 Source Map MSC/동작 설명 작성 금지.
- 그룹 l1sw-dev-knowledge는 기존 그룹 Writer/별도 승인/Preview/CAS/readback·역링크 정책을 적용. 개인 저장 성공≠그룹 게시 완료.

**최초 구축:** 기존 Discovery 7건을 D01~D07로 각 source/build/manifest/hash/coverage/관계별 매핑하여 재사용/부분 보완/충돌·미확인 구분. 전체 약 1,500개 파일 분모 및 빌드별 TU를 고정하고 대표 모듈 한 곳에서 P0 검증. 실제 파일 수는 현장 확인이며 과거 r0002의 2천 파일·215행(P120/F95)은 추정/검토 후보, 숫자를 합치거나 완료 범위로 사용하지 않음. 4개 기존 담당 모듈 범위는 r0002 유지. 이후 관계 정확도·비용·갱신 실측 후 확대.

P0: contains/include/declares/defines/calls/sends/receives/payload/registers/dispatches/guard/build. P1: read/write·모듈 인터페이스·Stack/Domain/Cell/CC·Timer/Event/callback·knowledge_ref. P2: data flow/alias(입증된 결손). 부록 B의 원문 추출표와 예시 참조. 새 파서/DB/외부 모델을 선행 도입하지 않음.

## 5. Map 소비 및 저사양 LLM 분석 품질

질문 한 개·source/build·scope 고정 → exact symbol/qualified signature/Message ID → 관계 유형·방향별 1-hop → 관련 기존 Knowledge/Procedure → 원본 Analyzer probe·근거 대조. 후보 이름/라인 일치로 실제 호출·런타임 순서·활성 빌드를 확정하지 않음. Map stale/없음/누락/충돌/권한 거절은 구분하고 허용된 범위의 독립 원본 탐색으로 대체. Map 밖 조사 없이 부재/안전/완료를 선언하지 않음.

Source Map pilot 상한: 4,096 실제 tokenizer tokens 및 50행, 기본 1-hop, 코드 20파일/step·60파일/task, 추가 probe 4단계, 총 입출력 32,768 tokens·20분/task. 실제 환경이 더 낮으면 낮은 값. Updater의 전체 시나리오 분석 예산은 r0002에서 실제로 고정하며 Map 질의 상한과 전체 분석 예산을 혼용하지 않음. 실제 파일/메타데이터 읽기·coverage·잘림·남은 범위·시간/토큰 기록. Qwen에는 한 시나리오 또는 한 근거 묶음씩 전달. 별도 신규 parser/index/멀티 Agent/전체 Source Map 구축을 필수 선행으로 하지 않음.

**분석 비교는 세 목적을 분리**:
- U-baseline/A/B/(실제 Analyzer 결손일 때만 C): 기존 Updater 분석 품질 개선 비교(r0002 §5.2).
- M-D0/D1/D2/D3: 현행 / 제한 Map / 정상 Procedure / Map+Procedure. M-D3−M-D2로 기존 정상 지식 위 Map의 추가 효과 평가.
- R-D0~D3 및 Recovery A/B/C: 별도 Recovery 담당의 코드 fact/Procedure 원인 분리와 선택적 위임 시험. M-D와 D1 의미가 다름. Updater에서 Recovery 전체 재실행 요구 금지.

기존 비교 결과는 동일 source/build/model/입력/예산/실험 목적과 유효 영수증 일치 시만 재사용. 기대 관계·정상 반례 정답은 입력에 넣지 않음. Updater 수락: 근거 없는 CONFIRMED 0, 확인된 필수 관계/분기 누락 0, 잘못된 MSC 방향·순서 0; UNKNOWN 별도 표시. Map 대표 pilot의 양성≥30/음성≥10, recall≥90%, stale/variant 탐지 100%, 근거 없는 확정 및 범위 밖 읽기 0은 기존 Map 시험 목표. 대표 1건의 결과를 전체 1,500개 소스 품질로 승격하지 않음.

## 6. 단계별 구현·회귀 및 업무 GPT 회신

| 차수 | 구현/확인 | 통과 근거 |
|---|---|---|
| 0 | 기존 Updater/Analyzer/Converter/Writer/Reader/Viewer 실제 계약 및 기존 사례/Discovery 7건 | 활성 version/hash/action/권한/기존 결과, REUSE/CONNECT/PROVEN_GAP/UNKNOWN |
| 1 | 대표 기존 NR L1 Tx → UL Tx Switching 1건 기준선과 Qwen 호출·근거 개선 | 원본 관계·파일 예산·분기·IPC·UNKNOWN 및 비교 지표 |
| 2 | 신규 유형별 Knowledge 작성 및 MSC 계약 | 실제 문서/Converter 영수증·PUML/SVG/HTML·의미/링크 검증 |
| 3 | 기존 Work/Evidence 및 개인 Knowledge 저장 | 기존 writer·revision/hash/readback·원본/분류/권한 보존 |
| 4 | 기존 Discovery 재사용 및 대표 모듈 Map 정규화 | 관계별 source/build/anchor·coverage·검증 상태 |
| 5 | 동일 Knowledge Writer로 source-map/ 저장·증분 갱신 | 실제 경로·actor/권한·CAS·snapshot/manifest hash·readback, 충돌/응답 유실 복구 |
| 6 | 기존 Reader/Map 조회 및 Updater 분석 소비 연결 | exact/1-hop·snapshot pin·stale/unknown·지도 밖 탐색, M-D 비교 가능한 범위 |
| 7 | 별도 Viewer 연동 확인 | 실제 활성 v0.5.7/v0.5.8·Map 조회·Knowledge/MSC·기존 기능 회귀, 실패 시 해당 담당만 재개 |
| 8 | 기존 그룹 비교·야간 확대 준비 | 별도 승인 게이트, 기존 Base/Ours/Theirs·Preview/복구/중복 방지, 실제 예약 미실행이면 NOT_RUN |

차수 1~3과 4~6은 독립 가능한 범위에서 진행. 이미 다른 통합 Work에서 완료한 항목은 유효 근거로 대체. 전체 Map/Viewer 설치를 Knowledge 분석의 선행 강제 조건으로 만들지 않음. 각 차수 실제 결과·변경 파일·근거·재개점·다음 조치를 보고하고 다음 차수 진행 범위를 사용자와 확인. 신규 독립 리뷰 없음.

기존 r0002 T01~T18 전체와 Source Map/Viewer의 해당 회귀 조건 재사용. 추가 수락:
- U19 신규 Knowledge 5유형 섹션 순서/기존 참조/필수 기술 정보 검증; 기존 문서 불필요 변경 0.
- U20 knowledge/와 source-map/ 동일 Writer 호출·경로 root·actor/권한·이력/readback 근거, 별도 Writer/DB 0.
- U21 기존 snapshot reader pin 및 CAS 경합/응답 유실·삭제/rename/헤더 영향·stale 링크 차단.
- U22 동일 활성 Map이 Updater/Viewer/Recovery에 일관된 snapshot ID를 반환; 접근 거절/미지원/없음 구분; Map 없이도 독립 분석 가능.
- U23 Kernel export 전후 Map/Knowledge 해시 보존, Workflow READ_ONLY, 기존 MSC/Work/Viewer 기능 회귀 및 타 스킬 임의 변경 0.

최초 회신: 기존 Work·활성 Updater/Analyzer/Converter·Knowledge Writer/Reader 실제 계약·기존 Discovery D01~D07·대표 사례와 기준선·변경 범위·차수별 수락 계획. 최종 회신: 분석/문서/MSC/Work/개인 Knowledge/Map 저장/Map 조회/Viewer/그룹/야간 각각 PASS/FAIL/SKIP/NOT_RUN/BLOCKED, 실제 evidence/receipt/hash/source/build/model/version·변경 파일·잔여 결손·다음 한 행동. 실제 업무 소스/상세 MSC/경로/로그는 업무 환경 내 보존.

## 7. 문서 우선순위와 기존 인계 참조

본문 0~6절이 최신 Updater 실행 기준. 부록 A는 r0002 전체 계약 보존용으로, 과거 버전/당시 시험/당시 적용 제한은 역사 기록이며 본문의 실제 사용자 확인 및 최신 버전 기준으로 해석. 부록 B는 Source Map 작성 및 증분 갱신 상세 예시. 부록 C는 Viewer의 원래 표시 역할/순서 계약이며 이번 본문 §3에서 신규 Updater 작성 가이드로 확장 적용. 기존 READ_ONLY G0/그룹 승인/제품 변경/운영 설치 제한 유지.

- [Updater 분석 품질 r0002](./L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0002_20261125_KST.md)
- [Source Map r0003](./L1_SOURCE_MAP_1500_UPDATER_INTEGRATED_HANDOFF_r0003_20261127_KST.md)
- [Recovery·Source Map·Viewer 통합 r0001](./L1_RECOVERY_SOURCE_MAP_VIEWER_INTEGRATED_IMPLEMENTATION_HANDOFF_r0001_20261127_KST.md) — 해당 공통 연동 및 Recovery의 별도 실행 기준. 동일 작업 중복 금지.
- [Viewer 기술 Knowledge 역할 v0.5.6](./L1_WORKSPACE_VIEWER_V056_TECHNICAL_KNOWLEDGE_READABILITY_COMPLETE_HANDOFF_r0001_20261126_KST.md)
- [Viewer 표준 섹션 순서 v0.5.7](./L1_WORKSPACE_VIEWER_V057_KNOWLEDGE_SECTION_ORDER_COMPLETE_HANDOFF_r0001_20261126_KST.md)
- [11/17 개인/그룹 동기화 R1](./L1_KNOWLEDGE_UPDATER_R1_G0_DETAILED_HANDOFF_r0002_20261117_KST.md)
- [11/11 Workflow r0005](./L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md)
- [11/23 야간 분석](./L1_KNOWLEDGE_UPDATER_NIGHTLY_MODULE_PROCEDURE_MSC_HANDOFF_r0001_20261123_KST.md)

**자체 검토 판정: 조건부 GO.** 새 Updater 작성 순서 및 동일 Knowledge 저장 계약을 명시했고 기존 r0002 요구를 보존함. 기존 Viewer는 v0.5.7(사용자 확인), v0.5.8 실서비스 전환/Writer·Reader 실제 지원/Updater 활성 원문/업무 E2E 미확인. 문서 게시 외 스킬 수정·설치·실행·그룹 게시·독립 리뷰 없음. 다음 한 행동: 업무 GPT에서 G0 및 대표 사례/기존 Discovery를 대조하여 실제 Updater 결손·재사용 범위를 회신.


---

# 부록 A. Updater 분석 품질 r0002 원문 전체 (기존 계약·시험·역사 보존)

※ 아래 원문의 기존 요청문을 별도 실행하지 않음. 버전/권한/새 작성 기준은 본문 우선.

# 업무 GPT 통합 실행 인계 — L1 Knowledge Updater 분석 품질 및 책임 경계 r0002

- 2026-11-25 KST / `wonhwipark/L1Work`, `main`, `handoffs/L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0002_20261125_KST.md`
- 대상: 업무 GPT 설계·최종 판정 → 허용된 Linux Agent/OpenCode/Qwen3.6-27B 구현·실행 → 기존 l1-knowledge-updater.
- 목적: 제품 코드의 정확하고 충분한 지식 분석, Module→Feature→Scenario 정본과 Procedure 교차 탐색, 근거 있는 AS-IS MSC, 개인 Knowledge 및 승인된 그룹 지식 연계. Viewer 화면 개선이나 공통 저장 엔진 개발이 목적이 아님.
- 본 문서는 11/25 Qwen 분석 품질 r0001의 실행 요구를 대체하는 최신 단일 Updater 개선 인계. 기존 파일·정책·독립 리뷰 이력은 보존. 실제 업무 설치본 확인·구현·실행·그룹 게시·운영 전환은 아직 완료를 주장하지 않음.

## 0. 업무 GPT 요청문 및 이번 변경 범위

> 위 repo/main의 r0002 문서를 기준으로 동일 목적 기존 Work를 재개해 주세요. 기존 Updater의 실제 SKILL.md, 가이드, 실행 entrypoint, 지원 action, 권한, 기존 결과를 대조하고 분석 품질 개선을 위한 Updater 가이드·호출부에서 입증된 결손만 보완해 주세요. 실제 소스 경로와 revision/build를 고정하고, NR L1 Tx → UL Tx Switching의 대표 시나리오 1건에서 기존 결과 재사용 여부, code-analyzer와 doc-converter 실제 호출, 근거의 정확성·탐색 범위·문서 및 MSC 의미를 검증해 주세요. Qwen에는 한 시나리오 또는 근거 묶음씩 짧고 명확한 단계 지시를 전달해 주세요.
>
> Kernel·Workflow·Viewer 및 Analyzer/Converter의 내부 구현·운영 설치는 이번 Updater 변경 대상이 아니에요. 필요한 기존 계약을 사용하고, 타 컴포넌트의 입증된 결손은 담당·근거·영향·재개 조건과 함께 별도 후속 항목으로 남겨 주세요. 분석·MSC·Work 저장·개인 Knowledge·Viewer·그룹 게시를 각각 판정하고 후속 실패만으로 분석을 재실행하지 마세요. 실제 권한이 있는 범위에서는 G0 조사만으로 종료하지 말고 최소 보완과 관련 회귀까지 진행해 주세요. 권한이 없거나 필요한 계약이 미확인인 단계는 보류하고 독립 가능한 단계만 이어가 주세요.

### 적용 우선순위와 승인 경계 (D1)

- 11/11 Workflow 인계 r0005와 11/17 개인/그룹 동기화 R1 r0002는 K5.8/K6 설치 사실 조사·분류/게시 계약을 위한 READ_ONLY 범위예요. 해당 조사에서는 원문의 쓰기·수정 금지 유지.
- 본 r0002는 별도 명시적으로 요청된 Updater 분석 품질 개선 범위에서만 r0001보다 우선해요. 조사와 구현 지시를 혼동하지 않고, 유효한 수정/시험 권한이 확인될 때만 Updater를 변경해요. 동기화 정책·그룹 게시 보호·기존 READ_ONLY 작업의 권한을 완화하지 않아요.
- 신규 유료 모델 비교/Job 등록·예약·운영 설치/설정 변경·그룹 write·제품 코드 수정은 기존 유효 승인 범위 밖이면 BLOCKED. 문서 게시 자체는 실행 승인이 아님. 업무 GPT나 실행 LLM은 자체 승인 권한을 부여하지 않아요.
- 기존 스킬 원문과 실제 호출·영수증, G0 사실과 G1 설계 가정, 합성 시험과 업무 소스 시험을 각각 구분. 확인하지 못한 기능을 결손 확정 또는 구현 완료로 보고하지 않아요.
- 업무 소스·상세 MSC·로그·원본 경로·인증·제한 자료는 허용된 업무 환경에 보존. 공개 인계 저장소를 업무 스킬 실행 의존성에 넣지 않으며 무승인 결과 외부 전송을 요구하지 않아요.

## 1. 책임 분리 — 변경 범위의 기준

| 구성요소 | 소유 책임 | Updater가 할 일 |
|---|---|---|
| 업무 GPT | 목적·범위·완료 기준·권한 및 최종 판정 | 설치 계약에 맞는 Qwen 단계 지시 작성 |
| l1-knowledge-updater | 기존 Knowledge/Work 검색, 분석 요청 구성, Analyzer/Converter 오케스트레이션, 근거 검증·지식 문서화, Module/Feature/Scenario 분류·Procedure 연결, 개인 knowledge/ 변경·기존 그룹 비교/Preview/승인 조정 | 이번 보완 대상. 기존 기능 충분 시 REUSE/NO_CHANGE |
| code-analyzer | 고정 source 기반 제한 탐색, entry/call/dispatch/callback/분기/상태/IPC/build 조건·근거·coverage 추출 | 실제 지원 action 호출, 출력과 원본 대조. 자체 C++ 파서·중복 분석기 개발 금지 |
| doc-converter | 지원 native Scenario IR 또는 변환 입력→PUML/SVG/HTML/manifest | 검증 입력 전달·변환 후 의미 대조. 자체 renderer/HTML writer 중복 구현 금지 |
| l1-fix-workflow | 요청·Work 선택/재개·기존 업무 흐름·첨부 연결 | 필요한 기존 인터페이스만 사용. Updater 직접 분석에 전체 Workflow 매회 실행 강제 금지 |
| work-ledger-kernel / 기존 승인 writer | Work/Evidence 원본·ID·revision·무결성·충돌·파생 export | 기존 등록·조회 요청/응답 확인. 별도 Work ID·원장·DB·schema·index 생성 금지 |
| Viewer/읽기 adapter | Work 및 Knowledge 탐색·권한 있는 artifact 링크·HTML/SVG 표시 | 올바른 문서와 참조를 제공. 직접 호출·UI·adapter 구현은 별도 담당 |
| 기존 Knowledge/Git writer | 허용 actor/path, 승인·expected HEAD/CAS, commit/readback, 충돌/중복 검사 | 검증된 지식 변경 요청·Preview 및 게시 후 정산 조정 |
| job-list/기존 OS 예약 수단 | 유효 Job/Runner·실행 영수증 및 별도 승인된 일정 | 기존 결과 소비. 신규 예약·재큐잉·스케줄 엔진 구현 금지 |

Updater는 개인 `knowledge/` 콘텐츠 및 해당 지식 탐색 분류의 유일한 WRITE 요청자이며 Workflow는 READ_ONLY라는 기존 정책 유지. 물리적 write는 실제 승인된 writer 및 기존 경로로만 수행. Kernel의 `works/`·공통 `index/`·root README/export 소유권과 분리해요. 문서 정책을 실제 ACL/credential/경로 보호가 강제된 증거로 취급하지 않아요.

REUSE → CONNECT → 입증된 gap만 최소 EXTEND. 다른 컴포넌트의 실제 결손이 확인돼도 이번 Updater 수정에 몰아서 구현하지 않아요. 승인된 별도 소유 컴포넌트 작업에 연결하고 기존 안전한 입력/출력·분석 결과를 보존해요. 추정 API, 새 필수 필드, RAG 엔진, 전용 DB/원장, 자동 로더를 신규 요구로 확정하지 않아요.

## 2. 두 진입 경로와 입력 고정

| 진입 | 처리 |
|---|---|
| A. 사용자 Module/Feature/Procedure/Scenario 직접 분석 | 기존 지식·Work·Evidence를 먼저 검색. 고정 revision/build와 범위가 유효하면 재사용, 필요한 부분만 분석/변환. 실제 코드 분석 Work가 필요하면 기존 Work 재개 또는 허용된 Kernel 생성 계약 사용 |
| B. Workflow/Recovery 등 기존 Work 지식화 | 원 Work의 실제 Code Facts/MSC/근거/시험/decision을 조회하고 유효성 검증. 누락된 근거만 보완. 전체 Workflow/Recovery나 모델 실행 반복 금지 |
| C. 단순 Knowledge 정리·편집 | 기존 지식과 목적/권한·근거가 충분하면 기존 Knowledge writer 경로. 불필요한 코드 분석, 새 Work 생성, MSC 호출을 강제하지 않음 |

사용자 필수 입력: target, purpose. 선택: 기존 Work/지식 항목, 코드 폴더·파일·메시지·인터페이스·entry·상태 변수·RAT/build 힌트. 실제 소스 탐색·분석이 필요한 경우만 아래 경로와 revision을 확인해요.

### 2.1 소스 폴더·revision 사전 확인

| 상황 | 처리 |
|---|---|
| 이번 요청에 경로 명시 | 실제 존재·읽기권한·제품/프로젝트 일치 확인. 잘못되면 저장값으로 자동 대체하지 않고 필요한 경로 확인 |
| 미지정 + 같은 호스트/프로젝트의 유효 저장 경로 1개 | 재검증 후 질문 없이 재사용 |
| 저장 경로 없음/이동/권한 오류/복수 후보 | 확인 가능한 이유·후보를 제시하고 이번 소스 경로를 한 번 질문 |
| 유효 경로, 요청 revision과 관찰 revision 일치 | 해당 revision/build 고정 |
| 유효 경로, revision 불일치 | 두 revision·불일치 이유를 보여주고 어느 revision인지 한 번 질문. 경로 재질문 금지 |
| revision 미지정 | 이번 관찰 revision을 고정. HEAD 변경이면 이전 근거 중 영향받은 부분만 무효화 |
| 무인 실행/답변 후에도 입력 미확정 | 기존 Work에 대기 조건·확보된 정보·재개 지점 보존. 임의 경로/checkout·제품 코드 읽기 시작 금지 |

Git은 canonical root, branch/commit, 요청 범위와 dirty/untracked 영향 및 실제 읽은 파일 버전을 구별. P4는 허용 client/view, stream/depot, 파일 revision 및 로컬 수정 여부 확인. commit과 실제 읽은 dirty bytes가 다르면 동일 source pin으로 보고하지 않음. 허용된 기존 snapshot/revision 근거가 없으면 영향 범위 보류. 경로와 revision 확인이 모두 필요하면 최초 질문 1회에 묶고 반복 질문하지 않아요. 입력 고정 전 본 분석 금지. 제품 소스·스킬 설치 폴더·Workspace는 구분해요.

### 2.2 범위와 분석 요청 계약 (A2·D3)

- 1차 담당: NR BCH(NR L1 Channel Controller), NR L1 Tx, LTE ChCfg, LTE L1 Tx. 215행(P120/F95)은 검토 후보, Layer1 약 2천 파일은 추정. 실제 모듈·소유자·경로/파일 수 및 시나리오 분모를 업무 환경에서 확인. 폴더=모듈로 추정하지 않음.
- SCell Procedure의 주관은 Channel Controller, Tx는 UL Tx 하위 참여. Search/Measurement, DRX 본체·Paging 독립 절차는 자동 포함하지 않음. 분석에 필요한 공통/HAL/PHY/IPC 경계는 근거와 함께 scope 포함. EN-DC·NRDC·Dual SIM·ULCA, RAT/Stack/domain/CC/build variant는 실제 조건으로 구분.
- 첫 사례: NR L1 Tx → UL Tx Switching의 단일 Trigger/Condition/State 경로. 동일 revision/build의 유효 기존 결과 우선. 기존 NR Init RACH Job의 미확인 결과를 임의 재큐잉하지 않음. 대표 사례 변경은 실제 목적·권한·기존 결과를 기준으로 기록.
- 필수 질문: trigger/precondition→entry/handler/dispatch→caller/callee→분기/guard→state write/read→REQ/CNF/IND·timer/callback·비동기→완료/실패·예외(존재 확인 시). 해당 시나리오에 없는 것은 이유와 함께 제외.
- 실행 입력: source pin/build, scope/exclusion, entry 후보 또는 제한 discovery 계획, 파일/심볼/메시지 후보, 필수 질문과 coverage 분모, 시간/토큰·파일 상한, 확대·종료 조건, 산출물·기존 저장 위치. 미확인 entry 때문에 제한 probe를 막지 않되 경로/revision/권한은 선확정.

## 3. G0: 실제 설치 계약과 OpenCode 실행 환경

G0는 설치 원문·권한 확인, G1은 실제 분석/실행 및 시험. 함수가 보이는 것, action이 노출되는 것, 실제 호출 영수증, 결과가 의미상 유효한 것을 각각 기록해요. 아래 항목은 확인 목록이며 새로운 API/필수 schema가 아니에요.

| 대상 | 확인할 사실 |
|---|---|
| Updater | 활성 SKILL.md·실행 파일·version/hash·가이드·직접/Work 진입·호출부, 기존 Knowledge 분류·Preview 경로 |
| Analyzer/Converter | 활성 버전 및 지원 action·실행 위치·I/O·권한, 실제 evidence/coverage·native IR·렌더러 지원 |
| Work/Knowledge writer | 이번 단계에 필요한 기존 Work 조회·등록·readback·허용 actor/path. Knowledge 변경/게시를 할 때만 해당 writer·보호 계약 확인 |
| 실행 환경 | 실제 Qwen 모델 ID, H 의미(확인된 경우), context/토큰/시간 한도, 기존 모델 호출 승인 |
| OpenCode (D2) | .claude/skills 등 실제 설치 경로·스킬 발견, 명시 action 호출/도구 이름과 worker 기능 parity, 입력 크기·단계 체크리스트, 기존 helper의 코드 게이트 유지 |

OpenCode v1/v2 및 parallel-extract-plan/check는 실제 설치본이 제공할 때만 사용. 스킬 description 자동 선택에 의존하지 않고 기존 action을 명시 호출. 이름만 해석되거나 LLM이 직접 유사 분석/PUML을 생성한 것은 도구 호출 PASS가 아님. 기존 helper의 may_invoke_doc_converter=false, may_publish_knowledge=false 등 보호는 변경하지 않아요. 별도 허용된 Converter/Writer 경로를 사용해요.

Kernel·Workflow의 실제 의존 인터페이스가 불명확하면 그 단계만 BLOCKED. Viewer 설치·버전·UI 전체 점검을 분석 선행 게이트로 강제하지 않아요. 공개 ZIP 버전과 업무 활성본은 별개예요.

## 4. Qwen 단계별 분석 및 명시 호출

한 시나리오를 순차 처리해요. 각 단위에 고정 입력·목적·허용 도구·기대 출력·중단/재개 조건을 주고 결과를 확인한 후 다음 단위로 이동. 2천 파일·다수 모듈의 내용을 한 프롬프트에 넣지 않아요.

| 단계 | 실제 작업 | 회수할 근거/실패 처리 |
|---|---|---|
| G1-A 요청 | 기존 Work/지식/영수증 검증·재사용, 필수 질문/기준 분모·범위 고정 | 기존 유효 결과·stale/미확인 구분 |
| G1-B 탐색 | Analyzer 지원 bounded scope/probe/feature/procedure/flow, caller/callee·dispatch·callback·timer·상태·IPC 등 실제 호출 | 실제 action/버전·입력/출력 참조·영수증, 읽은 범위·잘림·잔여 후보. 확장 한 조건씩 |
| G1-C 사실 검증 | 원본 문장·revision/build·심볼/조건·관계 대조, 아래 5절에 따라 확정 수준 정정 | fact 참조·지지/반대 근거·UNKNOWN·원본 출력 보존 |
| G1-D 서술 | 검증된 fact만으로 상세 문서·Scenario IR 작성. 필수 질문 answered/unknown/excluded 대조 | 검증된 문서·미해결 질문·다음 조회 한 건 |
| G1-E 변환 | 지원 native 입력으로 Converter 실제 호출, 의미·방향·순서 전후 검증 | PUML/SVG/HTML/manifest 실제 생성·hash/참조, 오류 시 영향 시나리오만 보완 |
| G1-F Work 보존 | 같은 Work에 기존 승인 writer로 분석·Evidence·source pin·artifact·영수증 등록 요청 | 기존 등록 응답/ID·revision/readback. 저장 실패만으로 분석 재실행 금지 |
| G1-G 개인 Knowledge | 기존 Module/Feature/Scenario ID·variant·Procedure·기존 지식 비교, 허용 경로로 후보/개인 변경 | 기존 origin·diff·지식 분류·검증 수준. 승인/권한 없는 write 금지 |
| G1-H 그룹 비교 | 기존 그룹 지식 Base/Ours/Theirs·Preview 및 검증/승인 후보 | 그룹 자동 write 0; 실제 게시 요청/승인 있을 때만 8절 |
| I-Viewer 별도 통합 | 실제 저장된 artifact의 read adapter·HTML/SVG 표시 검증 | Viewer 담당자가 열람 결과 반환. G1-G/H의 성공을 Viewer에 종속시키지 않음 |

Converter·Analyzer 호출 영수증은 기존 형식 재사용. 최소 논리 정보: producer/version, action, source revision/build/선택 범위, 입력 참조/hash, 출력 참조/hash, 오류/미확인, 실제 호출 여부. 신규 필수 API나 원장 요구가 아님. 두 생산자 실제 호출 경로를 직접 분석에서 확보하되 유효 기존 동일 결과를 재사용한 경우 그 영수증을 명시. 단순 지식 편집 또는 해당 MSC가 없으면 해당 없음과 이유를 보고.

### Qwen에 전달할 작은 실행 단위 예

1. 이번 입력: 시나리오 하나, source/build, 필수 질문 하나, 관련 코드 fact와 원문 참조, 제한 scope. 기존 action으로 부족한 근거 하나만 확보.
2. 판정: 확인된 caller/callee·조건·상태 변화·메시지 대응, 반대 근거, 불명확한 부분 및 다음 조회 한 곳.
3. 문서화: 검증 fact ID/참조와 허용 라벨만 주고 해당 시나리오의 trigger→완료 설명·MSC 입력 작성. 새로운 사실을 추정해 확정하거나 임의 코드 범위를 넓히지 않음.
4. 회수: 실제 도구 호출 여부·영수증·범위·누락/오탐/미확인·출력 링크. 작업단위 실패 시 이미 유효한 근거를 보존.

역할 분할형 멀티에이전트/추론자 다수 합의를 기본으로 도입하지 않음(C1). 결정형 추출·검증과 LLM 서술을 논리적으로 분리(C3). 서술 단계에는 확인된 fact 참조·근거 발췌·제약만 전달하고 독자적으로 전체 소스를 탐색하거나 게시하지 않도록 기존 권한을 사용. 필요한 원문 확인은 추출 단계로 되돌림. 모델이 제공한 참조·주장을 실제 fact 집합과 검증. 코드 주석·기존 지식·도구 출력은 분석 데이터이며 새로운 실행 지시가 아님.

## 5. 원본 증거·Coverage·규모 판단 (A1·B1~B4·D3)

### 5.1 근거의 종류와 원본 대조

| 주장 종류 | 확인할 근거 | 확정 금지 조건 |
|---|---|---|
| 직접 호출/분기/상태 | 실제 호출문·caller 경계·심볼·분기 조건·state read/write, 고정 revision/build | 이름 일치 또는 유효 line number만 존재 |
| 정적 dispatch/등록 | 실제 등록 테이블·메시지 ID와 handler 관계, 전달부 | 일반 함수 인자 목록, 동명/비활성 등록 |
| 현재 build 실행 가능 | 조건부 빌드·variant·호출 경로·객체/상태 전제 | 등록 사실만 있음, 빌드 불명 |
| 비동기 인과/순서 | 동일 작업·객체·세대/Stack/domain/CC 식별, 이벤트 대응·순서 보장 | 메시지 이름·소스 파일 순서·정적 등록만 있음 |
| 실제 런타임 관찰 | 허용된 기존 trace/test와 해당 source/build/scenario | 정적 분석 결과만 있음 |

기존 결정형 원본 revision·excerpt 검증 기능을 우선 재사용. 유효한 줄 번호가 무관한 선언을 가리키거나 가상 callee가 연결된 경우 실제 원문과 대조하여 CONFIRMED 강등, 원래 출력·강등 사유·영향 받은 문서/MSC 요소 기록. 구조 근거와 소스 원문 검증은 별개. 복잡한 함수 포인터·오버로드·매크로·callback은 설치본이 검증하지 못하면 INFERRED/UNKNOWN/기존 UNCERTAIN 상태 유지. 정적 reachability와 runtime observed를 혼동하지 않음. 기존 confidence enum/필드가 다르면 의미를 매핑하고 강제 schema 변경 금지.

### 5.2 첫 사례의 객관적 비교

- 담당자가 고정 revision/build에서 기대 호출/등록/분기·IPC·정상 반례의 기준표를 먼저 작성. 목표 표본은 함수 5개, 실제 등록 1~2건 및 시나리오 주요 분기; 해당 형태가 없으면 적용 가능한 경계와 실제 수 기록. 보정 입력과 별도 평가 사례 분리.
- 기존 활성 Analyzer의 양방향 callers/callees 및 지원 dispatch/callback 등을 기준표에 비교. 실제 내용 읽은 서로 다른 제품 소스 파일 수 ≤ N, 범위 밖 제품 소스 읽기 0을 확인. 설정/구조 메타데이터 읽기는 별도 집계. 실제 읽기 측정 기능이 없으면 NOT_VERIFIED 및 규모 확대 보류; 로그/계측 결손은 소유 컴포넌트에 인계. 상한 초과·잘림·미탐색을 숨기지 않음.
- 기대 관계 적중/누락, 비기대 관계 중 확인된 오탐, 미확인, 제외 이유를 각각 보고. 도구 결과 차집합은 추가 확인 후보이지 오탐/누락 자동 확정이 아님. 빈 결과는 부재 확정이 아님.
- 분모는 사전 정의한 적용 가능한 필수 질문/검증 관계 집합. coverage=근거로 확인된 항목/고정 분모. 필수 질문·관계별 각각 집계하고 제외 항목/사유를 별도 보고. 뒤늦게 발견한 신규 항목은 기준표 변경 이력과 새 분모로 기록; 분모를 줄여 coverage 향상 주장 금지.
- baseline과 A(요청 정규화)→B(기존 Analyzer 연결/단계 개선)→C(입증된 Analyzer 결손 수정이 있을 때만)를 동일 source pin/build/model·파일·시간/토큰 예산에서 비교. 기존 유효 결과 우선 사용. 승인 없는 새 모델 비교 호출 금지.
- 안전 게이트: 근거 없는 CONFIRMED, 확인된 필수 관계/분기의 문서 누락, 잘못된 MSC 방향·순서 각각 0. 적용 가능한 필수 질문 중 UNKNOWN은 반드시 표시하며 완전 분석으로 승격하지 않음. 실제 전체 coverage·시간·토큰·호출량 목표는 담당자가 첫 실측 후 합의(TBD). 불필요한 문서 줄 수 목표 금지.

### 5.3 Index-first와 확대 결정

- A1 ACCEPT_WITH_CHANGE: 활성본 실제 읽기 범위·상한 및 잘못된 확정 방지를 대규모 확대의 게이트로 적용. 특정 개발 ZIP 설치 자체를 선행 조건으로 강제하지 않음.
- B1 ACCEPT: dispatch/매크로/caller-callee 결손은 대표 사례 실측으로 확인. 실제 코드에서 자주 누락되는 관계를 재현한 뒤만 결손 판정.
- B3 CONDITIONAL: 특정 message→handler 등록 형태가 실제 존재하고 기존 추출이 놓치면 그 형식에 한정한 좁은 규칙·반례 검토. 기존 code-analyzer 담당 별도 수정; 일반 인자/동명/비활성 분기 오탐 검사.
- B2 DEFER: 좁은 기존 기능 개선으로도 필요한 관계를 반복 누락할 때만 tree-sitter/SQLite 등 소규모 결정형 파생 캐시를 별도 평가. 전체 AST/RAG/새 DB 도입이나 compile DB 생성 가능성을 가정하지 않음. 캐시는 원본 정본 아님. 입력 revision·build·규칙·scope 고정, 변경 무효화, 구축 시간/크기/재현성, 추가 적중·오탐·탐색 절감·기존 결과 무퇴행 측정 후 판정. 첫 사례에 파서 설치 불필요.
- C2 ACCEPT_CONDITIONAL: 대표 단일 시나리오의 품질·부분 실패 재개를 확인한 뒤 독립 시나리오 단위 병렬화를 검토. 동일 입력 중복 방지·작업별 산출물·전체 시간/토큰 budget·공유 writer 충돌/readback을 검증하기 전 다중 쓰기/야간 확대 금지. 파일 단위 worker 성적을 시나리오 동시 실행 수로 승계하지 않음. Viewer 미표시만으로 독립 분석 확대를 차단하지 않되 전체 통합 완료는 별도.

## 6. 지식 문서·MSC 의미 품질

Module→Feature→Scenario를 기준 탐색으로 유지. Procedure는 실제 관련 Feature/Scenario를 연결하는 교차 탐색이며 모든 절차를 동일 Feature 아래 강제하지 않아요. RAT별 variant/shared Tx 설명은 기존 지식 ID와 참조를 재사용해 중복 정본을 만들지 않아요. 분류 검토행을 실제 존재하는 ID 또는 지원 기능으로 승격하지 않아요.

문서에는 목적/범위/variant/source revision, 모듈 책임과 전체 동작, trigger/precondition, 시나리오 상세(조건·상태·호출·IPC·비동기), 분기/예외·제약·미확인, 검증된 MSC 및 실제 생성 참조, Code Facts/Evidence/영수증·Work/지식 후보를 기존 형식으로 작성. AS-IS 코드 사실·TO-BE 제안·가설·런타임 관찰은 구분. 모든 중요 주장과 메시지의 근거를 연결하고 확인된 필수 관계의 서술 누락을 검사해요. 내용의 깊이는 필수 질문·분기·인과관계의 검증 수준으로 판단.

### 6.1 변환 전후 의미 검증 (필수)

1. Updater가 검증된 fact를 기준으로 Scenario IR 또는 활성 Converter native 표현을 준비. participant/alias·stack_group·SOURCE_PARENT_DIR_V1 등 기존 규칙 사용. Analyzer가 이미 생성한 유효 MSC를 중복 생성하지 않되 필요한 HTML/SVG 변환은 지원 action으로 실제 수행.
2. 변환 전 각 메시지의 source/destination, 방향, 순서 또는 부분 순서, 조건/분기, 동일 이벤트 대응, evidence/revision을 대조. 비동기 이벤트의 임의 직렬화 금지. Edge나 다른 관계 정의가 미확정이면 해당 요소만 보류; 검증된 독립 요소는 부분 출력 가능하며 전체 시나리오 완전성은 주장하지 않음.
3. Converter 실제 호출 후 PUML/SVG/HTML/manifest 생성 상태, 파일 존재·hash·기존 상대 링크를 확인. 원본 시나리오와 메시지·방향·조건·순서·참조 의미를 대조. 형식 검증 PASS만으로 의미 PASS가 아님.
4. 잘못되거나 미검증인 MSC 요소/전체 artifact는 유효 산출물로 등록·링크하지 않아요. 실패 근거·원본 입력·기존 검증 fact는 허용 경로에 보존. 시나리오 입력/근거부터 보정하거나 Converter 담당에 전달. 필요한 변환만 재실행. 렌더러 누락은 코드 분석 실패가 아님. HTML/SVG가 없으면 없다고 표시하고 PUML/검증 입력의 실제 상태만 제공.
5. Viewer에서 HTML이 보이지 않는 것은 실제 Converter 호출/변환 여부의 증거가 아님. Work 등록·read adapter·Viewer 표시 경로를 별도 확인하고 소유자에게 전달. Viewer UI·안전 링크·CSP/ACL·렌더링 구현은 11/24 별도 통합 인계 책임.

## 7. Work 및 개인 Knowledge 보존 계약

- 분석 원본은 같은 개인 `l1-workspace/works/<work_id>/`의 기존 Work/Evidence 경로. Updater가 기존 승인 writer/Kernel 인터페이스로 전달하고 Work ID, evidence/artifact 참조·source revision·내용 hash·등록 응답/readback을 확인. 전체 Workflow 재실행은 요구하지 않음. 기존 원장·공통 export/index/root README·ID·schema는 Kernel/기존 제공자가 소유.
- 개인 `knowledge/`의 콘텐츠·분류·Procedure 연결·개인 수정/그룹 동기화 상태는 Updater의 지식 책임. 실제 WRITE는 기존 승인된 writer 및 actor/path 보호가 확인된 경우에만. Workflow READ_ONLY 유지. raw Git/shell로 권한 우회 금지. 권한·동시성 보호 미확인은 해당 write BLOCKED.
- 지식 자체에 Work ID를 무조건 강제하지 않음. Work 유래 지식은 기존 지원 표현에 복수 Work/Evidence/MSC/source revision 참조(N:M)를 연결. 근거 없는 신규 필드·alias/code_root 등 의미가 다른 ref_type 오용 금지. 원 Work → 지식 역링크가 기존 인터페이스에 없으면 PENDING_UNSUPPORTED; 별도 확인 후 보완. 기존 Work 삭제·이관 금지.
- 실제 writer 호출과 readback 성공을 구분. 실패한 등록/링크는 유효 원본과 입력을 보존하고 해당 단계만 재개. 공통 writer가 접근 불가하면 승인된 기존 보존 경로만 사용, 저장 미완료 명시. Viewer 표시 실패와 무관하게 유효한 지식 후보는 유지하되 존재하지 않는 링크를 쓰지 않음.
- Kernel exporter가 개인 knowledge/를 보존하는지, 기존 지원 권한을 침범하지 않는지는 별도 통합 시험으로 검증. 미확인 API로 Kernel/Workflow 변경을 자동 확정하지 않음.

## 8. 그룹 Knowledge 비교·승인·동기화 (기존 정책 유지)

그룹 `l1sw-dev-knowledge`는 검증된 기술 지식 정본(HLD·상세 설계·AS-IS MSC·승인 변경·재사용 가능한 이슈 지식). 개인 Workspace는 분석·가설·진행·수정/시험/리뷰·Evidence 원본 정본. 상세도만으로 저장 위치를 분류하지 않아요. 검증 원인은 수정 미완료 표시와 별도 검증/승인을 거쳐 그룹 후보 가능. 가설은 개인 보존. 기존 tier/K5.8/K6 이름·조건·ID/variant·저장 root는 실제 원문 확인; 임의 enum/metadata 변환 금지.

이번 분석 개선의 기본 범위는 개인 분석/후보 및 허용된 비교·Preview까지. 그룹 게시에는 별도 유효 승인·기존 보호된 writer가 필요해요.

| 상황 | 처리 |
|---|---|
| Base / Ours / Theirs | 실제 그룹 base commit·파일 base blob/hash·재현 내용, 개인 변경, 현재 그룹 HEAD/동일 ID·variant를 대조. base 복원 불가 시 임의 2-way overwrite 금지 |
| 비중첩 변경 | 기존 3-way merge는 Preview 후보만; 의미/링크 검증·새 승인·CAS 후 게시 |
| 중첩 변경 | CONTENT_CONFLICT, 개인·그룹 양쪽 보존, 자동 게시 0 |
| rename/move/delete/ID·variant·경로 변화 | STRUCTURAL_CONFLICT, 무조건 HOLD 및 사용자 선택·새 Preview/승인 |
| Preview 이후 HEAD 변경 | STALE_PREVIEW, 이전 승인으로 push 금지. 최신 비교·승인 |
| 개인 미게시 변경 | 보존, 일반 sync에서 자동 덮어쓰기 금지 |
| writer/actor/path/lock/CAS 미확인 | 해당 게시 BLOCKED; 새 엔진/스키마 기본 개발 금지 |

게시 전 실제 기존 writer의 canonical root/remote, actor·권한, 최종 changed-path allowlist, dirty/staged/untracked, rename old/new·symlink/path escape, checkout lock/경합, expected HEAD 및 승인된 write set을 확인. 프롬프트/CODEOWNERS/hook 또는 일반 push guard만으로 hard guard 입증 불가. 동일 계정/credential 우회 가능성이 미확인인 경우 write 보류. 기존 보호 수단 재사용 우선.

승인된 게시 후 commit/revision·실제 내용 hash/readback PASS와 영수증을 확인. 원래 Work/개인 Knowledge의 상태·역링크를 기존 지원 경로로 정산. 그룹 게시 성공 뒤 개인 상태/역링크 실패는 해당 정산만 재개하고 재게시 0. 게시 응답 유실/불확실은 원격 이력·영수증·내용 확인 전 UNKNOWN/HOLD, 자동 재시도 0. 기존 승인 retry 정책 우선; 기존 11/17 계약의 개인 상태/링크에 한정된 최대 3회 backoff 대안은 권한 확인 후만 사용. 신규 operation DB/원장/Job을 먼저 만들지 않음. 회사 제한 원본·개인 경로·미승인 파생물 자동 포함 금지.

## 9. 단계별 수락·실패 재개·회신

각 항목은 논리적 시험·보고 단위이며 신규 Kernel 필수 필드·FSM·schema가 아니에요. PASS/FAIL/SKIP/NOT_RUN 및 BLOCKED 원인(실행하지 못한 시험은 NOT_RUN)을 구분.

| 판정 단위 | 수락 근거 | 책임 |
|---|---|---|
| G0 / REQUEST_READY | 실제 활성 계약과 고정 입력, scope/기준표 | Updater |
| ANALYZER_CALL / FACT_COVERAGE / DOC_COMPLETENESS | 실제 호출 또는 유효 영수증, 원본 대조, 필수 질문·누락/오탐·미확인 | Updater/Analyzer |
| CONVERTER_CALL / MSC_SEMANTICS / MSC_HTML_SVG | 실제 호출·산출물·전후 의미 일치 및 실제 링크 참조 | Updater/Converter |
| WORK_READBACK | 승인 writer 등록·원본 hash/revision·재조회 | writer/Kernel, Updater 호출 연결 |
| PERSONAL_KNOWLEDGE | 기존 분류/중복/variant·origin·허용된 변경/readback | Updater/기존 Knowledge writer |
| VIEWER_LINK (별도 통합) | 저장 결과 실제 목록/문서/HTML/SVG 열람 | Viewer/읽기 adapter |
| GROUP_PREVIEW / GROUP_WRITE / GROUP_READBACK / BACKLINK | compare·Preview 및 실제 승인된 게시/정산만 판정 | Updater/그룹 writer |
| NIGHTLY_READY (별도 운영) | 대표 사례·저장/중복/권한·부하·실패 재개, 승인 | 기존 Job/예약 담당 |

분석 PASS는 지식 전체 완료·제품 런타임 검증·그룹 게시·Viewer E2E PASS가 아니에요. Viewer FAIL이어도 검증된 분석·MSC·저장/개인 Knowledge는 상태 유지. Work 저장 실패 시 결과 보존과 등록 재개. 근거가 무효화된 경우만 영향 분석·문서/MSC를 다시 검증. 실제 전체 통합 성공은 요청된 통합 단계 전부 검증된 경우에만 보고.

### 대표 수락 시험

| ID | 입력 / 기대 결과 | 담당 |
|---|---|---|
| T01 | 유효 지정 경로 우선, 저장 경로 재사용 시 질문 0, 미설정/복수/무효 지정은 질문 1회 및 분석 0 | Updater |
| T02 | 경로 유효·revision 불일치 → revision 선택만 1회, 고정 전 본 분석 0. 미지정 HEAD 변경 시 영향 근거 갱신 | Updater |
| T03 | 직접 분석/기존 Work/단순 편집 각각 적절한 진입, 유효 동일 결과 재사용. 전체 Workflow 반복 0 | Updater |
| T04 | N보다 많은 제품 파일에서 양방향 probe → 실제 파일 읽기 ≤ N 및 범위 밖 0, 미탐색/잘림 표시 | Analyzer/Updater |
| T05 | 무관한 선언 line에 가상 callee, 없는 fact 참조, 동명 함수/다른 build → 근거 없는 CONFIRMED 0, 실제 유효 관계 유지 | Analyzer/Updater |
| T06 | 직접 switch/case, 실제 메시지 등록 vs 일반 인자, callback/이전 세대/비동기 → 등록·도달·순서 구분, 기준표 누락/오탐/미확인 회수 | Analyzer/Updater |
| T07 | 확인된 필수 질문·branch·IPC·state 관계의 문서 누락 0. UNKNOWN·excluded·AS-IS/TO-BE 명시 | Updater |
| T08 | 순서를 뒤집거나 방향·조건이 다른 MSC, Converter 형식 PASS → 의미 FAIL 검출, 문제 artifact 등록/링크 0, 해당 입력/변환만 재개 | Updater/Converter |
| T09 | 렌더러/IR 지원 누락 → 변환 단계 보류, 분석·기존 PUML/근거 보존, 가짜 HTML 링크 0 | Converter/Updater |
| T10 | 실제 Work 등록 충돌/권한 거절/원본 변경 → writer에서 보류·재조회, 기존 분석 재실행 0, 원본·receipt 보존 | writer/Kernel 별도 통합 |
| T11 | Work에 유효 artifact 있음, Viewer는 링크 누락 → Viewer 별도 FAIL, 분석/MSC 재호출 0 | Viewer 별도 통합 |
| T12 | 기존 지식 ID/variant·Procedure 교차 링크·N:M origin, 기존 참조 경로 미지원 → 의미 다른 ref_type 오용 0·PENDING | Updater/writer |
| T13 | Workflow 개인 knowledge/ raw write 권한·same clone 경합·export 보호 미확인 → 해당 write 보류, 개인 변경 보존 | 기존 writer/Kernel 별도 통합 |
| T14 | Base/Ours/Theirs 중첩·rename·stale HEAD·승인 없음 → 자동 그룹 write 0; 승인된 비중첩 Preview만 허용 | Updater/그룹 writer |
| T15 | 그룹 게시 성공 후 개인 상태/역링크 실패 및 응답 유실 → 재게시 0, 원격 정산/해당 단계만 재개 | Updater/그룹 writer |
| T16 | OpenCode 명시 action 실패/도구 미노출/권한 없음 → 해당 단계 NOT_RUN/BLOCKED, helper 게이트 우회 0 | Updater |
| T17 | 대표 사례와 별도 평가 사례 동일 예산 baseline/A/B/(필요 시 C) 비교; 실제 파일 수·누락·오탐·UNKNOWN·시간/토큰·호출량 | 업무 GPT/Updater |
| T18 | 독립 시나리오 병렬 평가 시 공유 Work 충돌/중복/부분 실패 → 유효 결과 보존·중복 Job/모델 재호출 0. 미평가면 NOT_RUN | 별도 확대 검증 |

첫 회신: 기존 동일 목적 Work, 활성 Updater/Analyzer/Converter 지원 action, 실제 변경점과 REUSE/CONNECT/PROVEN_CODE_GAP/UNKNOWN 판정, 고정할 대표 사례·기준표·예산·시험 기대 결과. 공통 컴포넌트는 확인된 결손과 소유자만 제시.

실행 후 회신: 단계별 PASS/FAIL/SKIP/NOT_RUN, BLOCKED 사유, 실제 주체·revision/버전·근거/영수증·실제 수정 경로(업무 Work 내 참조)·다음 한 행동. 실제 읽은 제품 파일 수/N, 기대 관계 분모·적중/누락/오탐/미확인/제외, CONFIRMED 강등 수, 문서/MSC 생성·readback 및 Viewer 별도 결과, 개인 지식 변경·그룹 Preview/승인/게시 결과를 회수. 미실행을 완료로 표현하지 않음.

## 10. 야간 확대와 공개 패키지 경계

기존 야간 인계의 우선순위(사용자/담당자 선정 → source 변경 영향 → 오래된 근거/미분석 후보) 및 기존 유효 결과 건너뛰기 유지. 대표 1건의 실제 품질, 기준 대비 탐색·오탐/누락, MSC, Work 저장/readback·중복·권한·실패 복구가 확인된 후 별도 승인된 Job/Runner에서 점진 확대. 215행 일괄 실행 금지. 01:00 KST는 기존 설계 예시이지 예약 생성 지시가 아님. 스케줄·Job·모델 비용/부하·권한을 실제 계약으로 확인하고 승인 없으면 NOT_READY. Viewer 표시 자체는 예약 실행 엔진의 선행 조건 아님; 필요한 전체 서비스 통합은 별도 검증.

| 공개 개발/기준본 | 실제 근거 및 제한 |
|---|---|
| [Analyzer v0.15.4](../code-analyzer_v0_15_4_1119.zip) | 공개 기준본. 업무 활성본 동일성 미확인. 기존 callers/callees의 파일 budget 우회 및 불량 line/endpoint CONFIRMED 결손이 공개 원본에서 확인된 이력 |
| [Analyzer v0.15.5](../code-analyzer_v0_15_5_1125.zip) | 594,930 B, SHA-256 61099248ab0a4b2597ca8316e613f5987caaee671d735337eea1e0f70a6c2877. 격리 9 PASS; 후속 선별 61 PASS/1 FAIL(설치 버전 불일치). 무관한 선언과 가상 callee의 CONFIRMED 사례 남음. 운영 설치 보류 |
| [Analyzer v0.15.6](../code-analyzer_v0_15_6_1125.zip) | 611,206 B, SHA-256 bf1f369aed47e75c38fad3061041e720d5497953b0d90bcf4dc2fbf0d97b69ef. 버전 정합성 및 단순 직접 호출 근거 보완, 격리 harness 13/13 PASS(일부 대역). 전체 회귀·설치 self-check·독립 리뷰·업무 호스트 NOT_RUN. development_not_for_deployment |
| [Converter v0.2.26](../doc-converter_v0_2_26_1117.zip) | 공개 기준, 현장 활성 계약 확인. 기존 합성 평가에서 역순 입력도 형식 PASS: 의미 검증 별도 필요 |
| [preflight v0.2.0](../knowledge_analysis_preflight_v0_2_0_1121.zip) | 개발 보조, C++ parser·LLM runner·Writer 아님. 기존 fail-closed 보존 |

Updater는 실제 지원하는 probe_meta.coverage_partial, structure_files_analyzed, missing_structure_count, missing_source_count, unanchored_edge_count 및 RN 등 선택적 meta를 보존. v0.15.6의 anchor_kind/source_excerpt 등도 실제 제공 시만 사용. 구조·source 근거와 현재 실행을 별도 검증. 해당 필드 미지원이면 미확인으로 두고 새 필수 schema를 강제하지 않음.

v0.15.6은 기존 활성본 유지 상태에서 별도 격리 회귀·설치 self-check를 먼저 검증할 후보. 직접 호출 표기가 C++ target resolution·runtime·dispatch·MSC 순서를 확정하지 않음. 기존 공개 인계 및 업무 G0/승인/게이트 충족 전 자동 설치/운영 덮어쓰기 금지. Updater 자체 품질·호출부 개선은 신규 후보 설치와 독립 가능한 범위에서 진행.

## 11. 검토 판정·기존 계약 참조

11/25 Qwen 독립 설계 R1은 요약 입력 기준 검토(실제 업무 설치본 미확인). GPT 판정 ACCEPT_WITH_CHANGE: BLOCKING 2(입력/참조 한계), MAJOR 1(품질 기준), MINOR 2(승인 주체·입력). 해당 지적과 원본 r0001의 요청 생성, 실제 도구 호출, baseline 및 안전 게이트 유지. 별도 11/17 지식 동기화 R1의 BLOCKING 1/MAJOR 4/MINOR 2 반영 계약(권한·origin/역링크·CAS·충돌·부분 실패) 유지. r0002 신규 독립 리뷰는 NOT_RUN.

| 규모·Index 검토 항목 | 판정 및 적용 위치 |
|---|---|
| A1 / A2 | 수정 수용: 실제 읽기·근거 확대 게이트 / 4모듈 분모 구체화, 2·5절 |
| B1 / B4 | 수용: 기준표 측정·실제 원문 대조, 5절 |
| B2 / B3 | 보류 / 조건부: 전체 인덱스 즉시 도입 안 함, 재현된 좁은 결손만 별도 평가, 5절 |
| C1 / C2 / C3 | 역할 분할형 기본 미채택, 대표 실측 후 단위 병렬, 결정형 추출/서술 분리, 4·5절 |
| D1 / D2 / D3 | 수용: 문서 권한 범위 명확화·OpenCode parity·임계치 실측, 0·3·5절 |

기존 문서의 정책과 세부 시험은 다음 별도 범위에서 재사용하며 r0002가 이전 문서를 전부 폐기하거나 새 설치를 승인하지 않아요.

- [직전 Updater 분석 품질 r0001](./L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0001_20261125_KST.md) — 원본 보존, 이번 분석 개선 범위는 r0002 우선.
- [Recovery r0006](./L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0006_20261125_KST.md) — 원본 근거·MSC·책임 분리 원칙만 공통 적용. Seed 원인 규칙/timeout 제외 등 Recovery 전용 목표는 Updater 요구로 이식하지 않음.
- [규모·Index 제안](./CLAUDE_L1_KNOWLEDGE_SCALE_AND_INDEX_FIRST_PROPOSAL_FOR_GPT_r0001_20261125_KST.md) — A1~D3 판정 근거.
- [야간 분석](./L1_KNOWLEDGE_UPDATER_NIGHTLY_MODULE_PROCEDURE_MSC_HANDOFF_r0001_20261123_KST.md) — 별도 실행/예약 승인 유지.
- [개인/그룹 동기화 R1](./L1_KNOWLEDGE_UPDATER_R1_G0_DETAILED_HANDOFF_r0002_20261117_KST.md), [Workflow r0005](./L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md) — G0 READ_ONLY, K5.8/K6 조사·기존 권한/분류·게시 정책 유지.
- [저사양 분석 보조](./L1_KNOWLEDGE_UPDATER_NR_UL_TX_SWITCHING_MODIFICATION_REQUIREMENTS_r0002_20261121_KST.md), [Viewer·Updater·Converter 별도 통합](./L1_WORKSPACE_VIEWER_V052_MSC_UPDATER_CONVERTER_COMPLETE_HANDOFF_r0002_20261124_KST.md) — 실제 기존 계약·별도 컴포넌트 검증.
- [Analyzer v0.15.6 개발 전달](./CODE_ANALYZER_V0156_DEVELOPMENT_DELIVERY_r0001_20261125_KST.md) — 최신 후보, 별도 검증 및 운영 게이트.

현재 상태: r0002 문서 설계. 실제 업무 Updater 설치·호출·Qwen 구현/분석·Converter/Work/Knowledge/Viewer E2E·그룹 write·야간 예약/실행·신규 독립 리뷰 NOT_RUN. 다음 한 행동: 업무 GPT가 0절을 기준으로 실제 기존 Updater와 대표 1건의 유효 근거를 확인하여 권한 내 최소 보완·시험을 진행.

---

# 부록 B. Source Map r0003 상세 작성·예시·도구·시험 계약 (원문 발췌)

※ D0~D3는 본문 M-D에 대응. 저장 방식은 본문 §4의 동일 Knowledge Writer 필수 요구가 우선.

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

# 부록 C. 기존 Viewer 지식 문서 표시 역할·순서 계약 (원문 발췌)

## 3. 기술 Knowledge 포맷
| 유형 | 권장 표시 역할 |
| --- | --- |
| Module | overview, architecture, components, interfaces, features, constraints, evidence |
| Feature | overview, design, conditions, states, scenarios, exceptions, constraints, evidence |
| Scenario | overview, conditions(Trigger/Precondition), architecture, flow, msc, exceptions, constraints, evidence |
| Procedure | overview, api, calls(Caller/Callee), parameters, conditions, returns, side-effects, exceptions, evidence |
| Issue Knowledge | symptoms, cause, fix, impact, validation, evidence |

Module→Feature→Scenario 및 Procedure 교차 탐색 분류 유지. srsRAN/TI BLE/Nordic SoftDevice/DPDK의 기술 레퍼런스 구성 원칙 참고. 실제 섹션 순서 유지, 없는 내용 생성 금지, legacy fallback은 원문. 기술 예외·제약·원인·API·MSC·코드 근거는 펼침.

## 4. 업무 GPT의 실제 매핑
ZIP의 INTEGRATION_READABILITY_V055.md, assets/readability-v055.js, 합성 adapter를 참고. 이름은 v055 계승 파일명이며 VERSION=0.5.6. getReadabilityPresentation(docId)는 선택 표시 DTO 예시이지 신규 저장 API/schema 아님.
- Work root의 workTitle/displayTitle, issueKey, workId, 검증한 presentationRole을 매핑. 확정 결정에만 decision 부여.
- documentRevision(문서 snapshot)과 sourceRevision(코드 revision) 분리. DTO의 docId/workId/documentRevision/sourceRevision 일치 시만 사용.
- knowledgeSections: headingId/headingText/role/verified:true. workSummary: currentStatus/nextAction/blocker 각각 state(KNOWN 또는 명시 근거 있는 NONE_CONFIRMED), text, sourceDocId. 출처 없으면 미확인. 기존 ACL/resolver 사용.
- foldSections: 동일 headingId/headingText, verified:true, nonEssential:true, SYSTEM/LONG_METADATA 또는 Work의 DUPLICATE. 기술 섹션·유일한 정보·하위 heading/링크/표/코드 있는 섹션은 자동 접지 않음. 원문/TOC/deep link 접근 유지.
- Knowledge Updater는 내용 생산·분류, Analyzer는 코드 근거, Converter는 MSC, Kernel/기존 writer는 저장, Viewer는 표현. 기존 Knowledge/Work 및 Kernel/Workflow/Updater/Analyzer/Converter/Recovery 변경 없음. 새 지식 문서 생성 시 검증된 내용을 유형별 구성으로 표현 가능하되, 기존 문서 재작성/재분석 금지. 실제 생산 계약 gap 입증 시만 소유자에게 별도 최소 보완 제안.

## 변경 및 책임
- Scenario: Functional Overview → 동작 조건 → Software Architecture → Scenario Flow → MSC(본문 링크) → 예외 → 제약 → 코드 근거. Module/Feature/Procedure/Issue Knowledge도 기존 역할 목록 순서 적용.
- 기존 verified headingId/headingText/role, docId/workId/documentRevision/sourceRevision 일치 조건 그대로. 동일 계층의 연속된 검증 섹션만 화면에서 순서 조정; 미매핑 섹션은 경계, 하위 제목 및 표·코드·링크는 부모와 함께 이동. 불명확 구조/불일치/레거시 원문 순서 유지. 누락 내용을 생성하지 않음. 원문 보기와 원본 Markdown·ID·링크·권한·writer 불변.
- 설계 GPT: 합성 표시 로직만 변경. 업무 GPT: 기존 read adapter에 실제 제목·유형·섹션 역할을 매핑하고 기존 접근 계약 검증. 새 저장 schema/API/Kernel/Workflow/Updater/Analyzer/Converter/Recovery 변경 금지. 별도 MSC 탭 금지.
- 기존 v0.5.6의 Work 가독성, READ/WRITE/MSC/Recovery/업무 도우미/오늘의 업무/환경설정 기능 유지 대상.
