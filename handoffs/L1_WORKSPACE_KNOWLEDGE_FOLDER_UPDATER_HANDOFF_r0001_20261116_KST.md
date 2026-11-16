# 업무 GPT 인계 — L1 Workspace `works/`·`knowledge/` 분리와 Workflow × Knowledge Updater 연결 설계

- 작성일: 2026-11-16 KST
- 문서 개정: r0001
- 목적: 사용자와 합의한 ③ 분석 근거 공통 인계 및 ④ 그룹 Knowledge 반영·역링크 설계를 업무 GPT의 **실제 설치본 기능 대조(G0)와 최소 보완 판단**에 전달
- 설계 상태: **GPT 조건부 권고 / 사용자 구조·권한 방향 합의 / 독립 설계 리뷰 미수신**
- 실행 상태: `DESIGN_HANDOFF_ONLY`; `HOST_E2E=NOT_RUN`; `GROUP_KNOWLEDGE_WRITE=NOT_RUN`; `WORKSPACE_KNOWLEDGE_DIR_CREATE=NOT_RUN`
- 범위: 업무용 개인 `l1-workspace` 및 그룹 `l1sw-dev-knowledge`. 동일 이름의 GitHub.com 저장소만으로 실제 업무 정본 위치·권한을 추정하지 말 것
- 중요: 이 문서는 **업무 GPT의 판단·조사용 인계**. 설치·스킬 변경·새 폴더 생성·실제 Work/Knowledge 쓰기·배포·유료 호출·Job 실행 승인 문서가 아님

## 0. 리뷰 선조회 결과와 증거 등급

2026-11-16 KST 기준 독립 Claude Code 설계 리뷰 결과·실행 근거는 **미수신**. 따라서 아래 방안을 **독립 리뷰 승인 설계 또는 E2E 검증 완료**라고 표현하지 말 것. 이후 결과가 접수되면 지적별로 검토해 필요한 설계 보완만 진행하고 기존 승인·실행 이력을 임의 변경하지 말 것.

근거 분류:

| 구분 | 현재 판단 | 근거 한계 |
|---|---|---|
| Workflow/Kernel 개발 패키지 | 기존 Work ID/프로파일 구조 및 공통 기록 경로의 정적 검토 근거 있음 | 업무 호스트 설치본과 동일성 미확인 |
| Updater 두 진입·분류/Preview | 기존 설계 및 업무 GPT 일부 기능 보고 | Updater 실제 설치 코드·정확한 writer API·호출 성공 미확인 |
| 개인 Workspace `knowledge/` | **신규 TO-BE 권장 구조** | 실제 폴더 존재, GitHub 탐색 인덱스/권한 강제 기능 미확인 |
| 그룹 writer·승인·원격 readback·역링크 | 기존 기능 우선 재사용하도록 설계 | 실제 writer/권한/동시성/E2E 미검증 |
| Claude 독립 설계 리뷰 | 결과/영수증 미수신 | 다른 주제의 Claude 리뷰 완료를 본 건의 승인으로 대체 금지 |

## 1. 사용자 요구와 핵심 결정

1. GitHub에서 수많은 Work ID 사이에 지식이 묻히지 않아야 하므로, `l1-workspace` 최상위에서 사람이 쉽게 찾는 **물리적 `knowledge/` 폴더 및 Module→Feature→Scenario 탐색 인덱스**를 우선 설계.
2. `works/`는 기존 `l1-fix-workflow`·`work-ledger-kernel`의 Work/Evidence·개발·시험·리뷰 이력 정본으로 유지. 기존 원본을 이동·삭제·재작성하지 않음.
3. `knowledge/`의 **유일한 업무 쓰기 주체는 `l1-knowledge-updater`**. `l1-fix-workflow`는 해당 경로 **READ_ONLY**이며 파일·인덱스·상태를 직접 변경할 수 없어야 함.
4. Updater는 `knowledge/`만 쓸 수 있는 단순 viewer가 아님. Updater 직접 분석 및 지식화 검토/결과를 **기존 Kernel 허용 기록 경로를 통해 `works/<work_id>/`에도 추가 기록할 수 있어야** 함. 단 원래 Workflow 산출물 덮어쓰기 금지.
5. Work Profile과 Knowledge 분류는 **서로 다른 축**. 별도의 `KNOWLEDGE` Kernel Profile 또는 새 Work ID 발급기를 기본 도입하지 않음. 기존 관련 Work가 있으면 그 ID를 재사용하며, 순수 독립 조사에서 필요한 신규 Work는 실제 기존 생성 계약을 사용.
6. `knowledge/`는 **개인 후보·검토·GitHub 탐색의 출처 연결 공간**이지 그룹 검증 지식의 대체 정본이 아님. 그룹 확정본은 권한·승인 후 `l1sw-dev-knowledge` 기존 writer로 반영.
7. `KNOWLEDGE`라는 카테고리 명칭을 제안한다는 이유로 기존 Kernel profile enum, 기존 metadata/schema/registry, 실제 지식 tier를 임의 변경하지 않음.

## 2. 목표 저장 구조 — 예시이며 실제 경로 확인 전 변경 금지

```text
l1-workspace/                          # 업무 정본의 실제 root는 호스트에서 확인
├── works/                             # 기존 Work/Evidence 원본: 위치와 생성 규칙 유지
│   ├── <work_id-A>/
│   └── <work_id-B>/
├── knowledge/                         # TO-BE: Updater만 WRITE / Workflow READ_ONLY
│   ├── README.md                      # 사람 중심 탐색: 모듈·상태·최근 후보
│   ├── NR-L1-Tx/
│   │   ├── README.md                  # Feature 목록
│   │   └── Init-RACH.md               # 탐색/후보 요약, 출처 Work·Evidence 링크
│   ├── NR-BCH/
│   └── LTE-ChCfg/
└── (기존 인덱스/문서·기타 파일 유지)     # 기존 인덱스/정본 경로 변조 금지
```

- `knowledge/NR-L1-Tx/Init-RACH.md`는 **설명용 경로 예시**이며 실제 Feature·Scenario 식별자·대상 path는 현행 스킬과 기존 Knowledge ID를 확인해 결정.
- 권장 내용: 읽기 쉬운 제목·Module/Feature/Scenario·절차/피처 구분·현재 상태(개인 후보/보완/승인 대기/그룹 게시)·출처 Work 링크(복수 가능)·Evidence/MSC/source revision 참조·게시된 그룹 지식 ID/고정 revision·미확인/다음 검증.
- `knowledge/`의 목록·요약은 Updater가 소유한 **탐색/후보 표현**. 코드 사실 원본, 원본 PUML/MD, Work 원장, 그룹 확정 지식 본문을 원칙 없이 복제하거나 두 번째 '최신 정본'으로 운영하지 않음.
- 링크는 상대경로·권한·대상 존재성을 GitHub 뷰와 실제 reader에서 검증. GitHub README만 보인다는 이유로 임의 자동 인덱스/호스팅 엔진을 추가하지 않음.
- 기존 Kernel `README`/`문서안내`/machine index 등 자동 생성 파일의 소유권을 침범하지 않을 것. 기존 exporter의 산출물·인덱스와 충돌하는 경로는 먼저 조사.

## 3. 권한·단일 writer 계약 (가장 중요한 신규 설계 경계)

| 기능/경로 | l1-fix-workflow | l1-knowledge-updater | 기록·게시 제공자 |
|---|---|---|---|
| 기존 Work 검색·조회/재개 | 허용 | 기존 선택/재개 기능 재사용 | Workflow/Kernel 계약 |
| `works/` 기록 | 기존 승인 경로로 WRITE | 지식 분석·검토/그룹 반영 이력에 한해 Kernel 허용 경로로 WRITE | **Kernel + 기존 Workspace writer** |
| `knowledge/` 읽기·탐색 | **READ_ONLY** | READ | 기존 reader/검색 |
| `knowledge/` 문서·인덱스 생성/갱신/삭제 | **DENY** | **유일한 WRITE 주체** | 검증된 Updater 경유 단일 writer |
| 그룹 `l1sw-dev-knowledge` 본문 | 직접 WRITE 금지 | 기존 승인·writer 조정 | **그룹 기존 writer만** |
| 승인·게시 readback·원 Work 역링크 | 조회 가능, 지식 경로는 변경 금지 | 조정·상태 갱신 | 그룹 writer + Kernel writer 각각 검증 |

**강제 수단 확인:** 단순 Markdown 역할 선언이나 GitHub `CODEOWNERS`만으로 folder-level 기술적 WRITE 금지가 보장되지 않음. 동일 repo write token이 공유되면 Workflow의 직접 Git 쓰기가 여전히 가능할 수 있음. 업무 GPT는 실제 실행 주체/자격·스킬 허용경로/명령 가드·Git writer 중앙화·commit path diff 검증·기존 정책 강제와 우회 경로를 확인해야 함. 분리 계정/추가 Git 정책은 기존 수단으로 충족하지 못하는 gap이 입증된 경우에만 제안. 여러 Updater 실행의 **동시 WRITE도 별개로 직렬화/CAS 필요**.

## 4. ③ 분석 결과 인계 — 두 진입을 연결하되 원본 불변

### 경로 A: Updater에서 직접 조사

`Module/Procedure/Feature 분석 요청 → 관련 기존 Work 조회/유일 매칭 → 필요 시 기존 Kernel 계약으로 Work 생성 → 유효한 기존 Evidence 재사용 또는 기존 code-analyzer 분석 → Kernel 허용 방식으로 Work/Evidence 기록 + readback → Updater가 knowledge/에 후보·인덱스 기록 + readback`

- 단순 질의·메모마다 신규 Work를 강제하지 않음. 맞는 기존 Work가 없을 때 생성 조건·Profile 정책을 실제 설치본과 확인.
- Updater가 `works/`에 기록할 때 전체 Workflow 파이프라인을 반복 실행할 필요 없음. 허용되는 공통 writer/API를 통해 기록하되, 그 존재와 입력 형식은 설치 원본으로 증명.

### 경로 B: Workflow 결과를 Updater가 지식화

`Workflow의 기존 Work ID 지정 → Source Revision과 분석 범위에 맞는 Code Evidence·MSC 원본 조회 → 재분석 적합성 판정 → Updater 지식 후보/기존 그룹 지식 대조 → knowledge/에 출처 링크·후보 기록 → 승인 전 Preview`

- **원래 Work ID는 바꾸지 않음.** 새로운 지식 후보 ID와 원본 Work ID는 서로 다른 식별자.
- 같은 Knowledge 항목이 여러 Work를 근거로 가질 수 있고, 하나의 Work가 여러 지식 후보를 낼 수 있음(N:M). 이름 유사도만으로 Work/Knowledge 자동 병합 금지.
- 유효한 Evidence를 재사용할 때 `code-analyzer`/Job을 단지 지식화를 위해 재실행하지 않음. 유효하지 않거나 누락된 경우만 필요한 분석 범위를 다시 판정.

| 인계 의미 | 유지·검증할 정보 | 주의 사항 |
|---|---|---|
| Work reference | Kernel 실제 opaque Work ID + 올바른 ledger/저장 경계 | 같은 이름/제목이더라도 동일 Work로 단정 금지 |
| Code Evidence | 기존 Evidence ID, 생산자, 원본 위치, 내용 해시, 근거 신뢰 수준 | 요약/CL·PR 후보를 증명된 코드 사실로 승격 금지 |
| MSC 원본 | PUML/MD·Artifact ID/해시·근거, HTML/SVG는 별도 표현 산출물 | 생성 표현물을 원본에 덮어쓰지 않음; AS-IS/TO-BE 구별 |
| Source Revision | Git/P4 실제 고정 revision + 파일/제품/build/scope·dirty 조건 | 같은 Work ID라도 revision이 다르면 현재 사실로 자동 재사용 금지 |
| 후보 출처 | origin Work들, Knowledge 대상 기존 ID/variant, 근거 범위 | 지식 후보의 현재본과 Work 분석 이력의 정본 구별 |

이 표의 정보는 **논리적 인계 요구**이며 신규 Kernel 필드/enum/API/DB 스키마 추가 지시가 아님. 기존 Work/Artifact/Evidence/SCM 참조로 매핑할 것.

## 5. ④ 그룹 Knowledge 반영 — 승인·게시·링크는 분리된 상태

1. Updater가 `knowledge/` 후보를 만들고 그룹 기존 `Module→Feature→Scenario`·Knowledge ID·variant 및 중복/충돌/Tier·대표 MSC 정책을 대조. Procedure는 별도 정본 복제보다 교차 탐색으로 활용.
2. Preview에는 지식 제목·대상·실제 변경 diff/범위·원본 Work/Evidence·고정 source revision·대상 기준 revision·민감정보 분류와 승인 필요 항목 표시.
3. 승인받은 후보 **특정 revision/digest/대상/적용 조건**에 대해서만 유효 권한과 target revision guard를 writer 경계에서 재확인. 만료·철회·기준 변경·권한 부족이면 그룹 쓰기 `BLOCKED`; 승인 자동 확대 금지.
4. 기존 `l1sw-dev-knowledge`의 실제 게시 writer가 쓰기 수행. 그룹에 상세 설계/확인된 AS-IS MSC를 포함할 수 있으나, 콘텐츠 허용 정책과 쓰기 승인/정보 반출 허가는 서로 다름.
5. 실제 remote commit/revision 및 내용 readback이 일치해야 **PUBLISHED_CONFIRMED**. 게시된 내용이 현재 코드 검증·수정 완료·RAG 사용 완료를 자동 의미하지 않음.
6. Updater가 개인 `knowledge/`에 게시 결과·그룹 고정 revision 링크를 기록하고, **기존 Kernel 허용 경로로 원래 Work(복수인 경우 각 Work)에 역링크**. 이 두 write의 성공 여부는 각각 확인.
7. Work 역링크만 실패했다면 그룹 재게시 금지. 기존 게시 revision/영수증을 확인하여 **링크만 복구**. 게시 성공 여부 불확실하면 원격 commit/history/기존 receipt부터 정산하고 무조건 재시도 금지.
8. 그룹 반영을 보류·실패한 경우에도 개인 Work 원본과 `knowledge/` 후보는 보존. 승인 전 후보는 Workflow에서 **검증된 그룹 사실로 오용 금지**.

## 6. 충돌·꼬임 케이스와 기대 안전 동작 (미실행 설계 시험)

| 번호 | 반례 | 반드시 성립할 안전 결과 |
|---|---|---|
| C01 | Workflow가 `knowledge/`에 직접 쓰기 시도 | 실제 가드/권한에서 차단, 변경 파일 0 |
| C02 | Updater A/B 두 실행이 같은 `knowledge/` 파일 동시 수정 | 직렬/CAS로 충돌 탐지, 한쪽의 변경 손실 0 |
| C03 | Workflow가 Work를 갱신하는 동안 Updater가 Work에 이력 추가 | Kernel writer 충돌 보호, 업무 원본/지식 링크 모두 무손실 |
| C04 | 기존 Work 검색에서 복수 매칭/부분 응답 | 자동 선택·신규 중복 생성 차단, 사용자/기존 계약으로 해소 |
| C05 | 같은 Work ID이나 source revision/scope 다름 | 기존 Evidence를 현행 코드 증명으로 재사용 금지 |
| C06 | Evidence 원본 누락·해시 불일치·권한 불가 | 후보에 확인 필요 표시, 거짓 CODE_VERIFIED/그룹 쓰기 금지 |
| C07 | MSC 원본과 렌더링 HTML/SVG가 불일치 | 원본·표현계보 확인 전 현재 사실 확정 차단 |
| C08 | 여러 Work의 동일 Knowledge 후보 생성 | 기존 Knowledge ID·variant 대조 후 출처 병합 또는 충돌 보류 |
| C09 | AS-IS 코드 사실과 승인 TO-BE 설계 혼재 | 상태·적용 revision 구별, 현재 동작으로 자동 승격 금지 |
| C10 | Preview 이후 대상 지식/승인조건 변경 | 재검토/재승인 필요, 예전 승인으로 덮어쓰기 0 |
| C11 | 그룹 게시 성공 후 API 응답 유실 | 원격 history/receipt 정산; 확정 전 재게시 0 |
| C12 | 그룹 게시 성공, 개인 `knowledge/` 상태 갱신 실패 | 게시 revision 보존·확인 후 해당 상태 갱신만 복구 |
| C13 | 그룹 게시 성공, 원 Work 역링크 일부 실패 | 성공한 그룹 글 재게시 0; 실패한 Work 링크만 보완 |
| C14 | GitHub README/index의 링크 단절·rename·구버전 링크 | 기존 원본/그룹 revision은 보존; 탐색 링크만 정상화 |
| C15 | 그룹 reader가 개인 Workspace 원본에 접근 불가 | 개인 내용/경로 누출 금지, 승인된 그룹 본문만 제공 |
| C16 | 승인/권한/정보등급 미확인인데 폴더가 PRIVATE | PRIVATE만으로 허가 간주하지 않음; 그룹/외부 반출 차단 |
| C17 | 기존 exporter/indexer 또는 다른 스킬이 `knowledge/`를 수정 | 단일 소유자 우회 경로 차단 또는 실제 gap으로 판정 |
| C18 | 운영 중 rollback 또는 updater 재실행 | 기존 Work/지식 정본 보존, 고정 operation·기존 history로 중복 방지 |

각 케이스는 `PASS/FAIL/SKIP/NOT_RUN`으로 구분하되 **현재 모두 NOT_RUN**. 단일 writer 소유 선언 자체는 C01/C02/C17의 실행 시험 PASS가 아님.

## 7. 업무 GPT의 요청 작업 — 이번에는 READ_ONLY G0 및 G1 차이 판정만

기존 설치 원본·기존 시험·반영 결과를 먼저 확인하고 아래 **미확인 항목만** 조사. 충분히 검증된 항목은 재조사하지 말 것.

| 체크 | 실제 확인 질문 | 출력 |
|---|---|---|
| G01 | 최신 설치 `l1-fix-workflow`·`work-ledger-kernel`·`l1-knowledge-updater` 버전 및 `l1sw-dev-knowledge` writer의 실제 소유/호출 계약은? | 설치 확인 사실·근거/미확인 |
| G02 | Work ID 검색·재개·신규 생성/기본 Profile, 기존 Work 조회·Evidence writer/readback 계약은? | REUSE/CONNECT 지도 |
| G03 | Workspace의 실제 `works/`·인덱스/export/docs-sync 소유권과 `knowledge/` 기존 존재/지원 여부는? | 기존 경로 보존/충돌 위험 |
| G04 | Workflow의 `knowledge/` 변경을 실제로 막는 **권한/실행 가드**가 있는가? Updater만 쓰도록 보장 가능한가? | 우회 경로·최소 보완 필요성 |
| G05 | Updater의 직접 분석 결과가 Kernel Work/Evidence에 기록 가능하며 원본 Workflow 근거를 읽을 수 있는가? | 두 진입별 producer/consumer I/O |
| G06 | Code Evidence/PUML·MD/HTML·SVG/Source Revision을 기존 ID·해시·scope로 참조할 수 있는가? | 근거 보존/미지원 확정 금지 |
| G07 | `knowledge/` 탐색 목록(README/Module별 파일)의 생성/갱신을 기존 writer·indexer로 할 수 있는가? | GitHub 탐색성/링크 보장 |
| G08 | Updater의 기존 Preview·승인·중복/충돌/Tier·Knowledge ID·variant 기능은 어디까지 실제 지원되는가? | 현재 동작 vs 설계 가정 |
| G09 | 그룹 writer의 permission, expected revision/CAS, readback, 응답 유실/중복 게시 방지 보장은? | 최소 실제 게시 게이트 |
| G10 | 그룹 게시→`knowledge/` 상태 반영→원래 Work 역링크를 중복 없이 회수할 기존 기록/복구 수단은? | 각 단계별 확정/미확인 |
| G11 | `knowledge/` 읽기가 미승인 후보를 RAG/코드 사실로 승격시키지 않도록 적용성/권한 필터가 있는가? | reader 경계 |
| G12 | 과거 개발 패키지와 현재 설치본 차이, 회귀·호스트 실제 E3 미검증 범위는? | G0/G1/E3 분리 보고 |

### 출력 양식

1. **현재 상태:** G0 설치 사실 확인 범위 / Updater 실제 함수·기록/그룹 writer 미확인 및 제약.
2. **기능 대응표:** `요구 ID | 실제 설치 스킬·기존 기능 | 확인 방식/근거 | REUSE/CONNECT/입증된 최소 EXTEND/추가 확인 | 위험/다음 검증`.
3. **경로·권한 표:** Workflow가 `knowledge/`를 실제로 쓰지 못하도록 강제할 수 있는지와 Updater가 `works/`에 안전하게 기록하는 경로를 구분.
4. **③/④ 검토 판정:** 제안 수용/수정 수용/보류/거절, 근거 및 가장 작은 수정안. 새 API·새 원장·schema·RAG 엔진이 기본적으로 필요하다고 전제하지 않음.
5. **다음 한 행동:** 현재 허용된 범위 내에서 가능한 첫 검증 하나. 실제 코드 분석·격리 통합 시험·그룹 게시 등은 승인 범위에 맞춰 별도로 수행.

사실 표시는 `INSTALLED_SOURCE_CONFIRMED`, `EXISTING_CONTRACT_READ`, `USER_REPORTED`, `DESIGN_PROVISIONAL`, `NOT_VERIFIED`, `NOT_RUN` 등을 정확히 구분. 실제 코드 경로·회사 자료/상세 MSC/로그·비밀·토큰은 인가된 업무 경계에만 보관하고, 허용되지 않은 외부 전송은 수행하지 말 것.

## 8. 이번 인계의 금지·유지 사항

- 새로운 Kernel `KNOWLEDGE` Profile / 별도 Work 발급기 / 지식 전용 원장 / 새로운 RAG·동기화·CAS·복구 엔진 선제 도입 금지.
- `works/` 원본 이관·삭제, 기존 생성 README/index 직접 덮어쓰기, 기존 knowledge/metadata/tier/schema/registry 강제 변경 금지.
- Workflow의 `knowledge/` 쓰기 허용 또는 Updater 우회 writer를 임의 용인하지 말 것.
- 기존 유료 리뷰의 REQUEST/SOURCE_PIN/ZIP/승인/영수증을 재사용·수정하거나 별도 모델 호출하지 말 것. 이번 문서는 독립 리뷰 실행 요청이 아님.
- 실제 폴더 생성·권한 정책 변경·운영 Work/Knowledge writer 호출·스킬 설치·Job/LLM 실행·PUBLIC 배포는 **별도 유효 실행 승인 및 해당 게이트 확인 전 NOT_RUN** 유지.
- 공개 저장소 또는 접근 제한된 협업 저장소에 회사 제한 코드·원문 MSC·고객 자료·로그·토큰을 게시하지 말 것. `l1-workspace`가 PRIVATE라는 사실만으로 자료 이동/그룹 게시 권한이 생기지 않음.

## 9. 다음 단계 수락 기준 (후속 시험 계획, 아직 PASS 아님)

- `knowledge/`가 GitHub에서 **최상위 진입점으로 탐색 가능**, Module→Feature→Scenario 링크가 실제 Work·게시 고정 revision으로 이어지고 링크 유실 0.
- Workflow가 `knowledge/` write를 시도할 때 권한/경로 정책으로 차단되고 파일 변경 0. 기존 Workflow `works/` 수행/회귀는 그대로 유지.
- Updater는 `knowledge/` 단일 writer이며, 승인된 Kernel API로 기존 Work에 자기 검토/게시 기록을 더하고 기존 원본 손상 0.
- 기존 Work 지식화에서 Work 중복 생성 0·유효 Evidence 중복 재분석 0; 원본/Evidence/MSC/revision 일치·readback.
- revision·source·권한·승인 충돌 시 안전 차단, 미승인 후보의 그룹 게시 0.
- 게시 성공/응답 유실/역링크 실패 상황에서 실제 remote readback, 중복 그룹 게시 0, 기존 Work·이력 보존.
- 검증된 그룹 지식 정본과 개인 후보를 reader가 구별하고, 업무 권한/정보분류/AS-IS·TO-BE 및 source 적용 조건을 보존.

**이번 업무 GPT에 요청하는 즉시 작업은 G01~G12의 기존 기능 대조 및 설계 적합성 판정뿐**. C01~C18의 합성/실제 시험은 설치 계약·실행 승인 및 격리된 테스트 범위가 확인된 후 단계적으로 검증.
