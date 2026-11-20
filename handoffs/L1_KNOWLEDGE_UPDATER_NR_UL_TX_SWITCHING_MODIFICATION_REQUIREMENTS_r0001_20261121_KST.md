# 업무 GPT 수정 요청 — l1-knowledge-updater Module→Feature→Scenario 및 코드 기반 MSC 개선

- r0001 / 2026-11-21 KST
- **전달 정본:** GitHub PUBLIC `wonhwipark/L1Work` / `main` / `handoffs/L1_KNOWLEDGE_UPDATER_NR_UL_TX_SWITCHING_MODIFICATION_REQUIREMENTS_r0001_20261121_KST.md`
- **기존 CoWork Work:** `L1-WORKSPACE-RAG-20261111-001` (동일 목적의 기존 분석·설계·개발 흐름을 재개)
- **수행 주체:** 업무 GPT(실제 스킬 설계·변경 지시) + 허용된 업무 Linux Agent·LLM(원본 코드/스킬 조회·개발·시험)
- **요구 성격:** 설치 원본 확인과 구현 요청을 하나로 묶음. 이 문서 자체는 설치·모델 호출·작업 자동 실행·그룹 게시 승인 아님.

## 0. 배경과 이번 우선순위 변경

설계 GPT는 업무 Linux의 `l1-knowledge-updater` 설치 원본과 업무 C++ 소스를 직접 열 수 없다. 따라서 설계 GPT가 Updater 전체를 추측해 ZIP으로 교체하지 않는다. 대신 **기존 기능 비교 + 필요한 최소 변경 + 직접 시험**의 요구사항을 먼저 확정하여 업무 GPT가 실제 설치본에서 재사용/연결/결손을 판단하도록 요청한다. 단순 G0 현황 보고만으로 종료하지 말고, 현장 기존 권한·기능 내에서 구현·자체시험·후속 패키징 후보까지 연속 진행한다.

최종 목표는 **NR L1 Tx → UL Tx Switching** 코드 기반 지식 1건을 Updater가 정확하게 판별·검토하고, 허용된 **개인 `l1-workspace`**에 근거·Knowledge 변경 초안·MSC 링크를 갱신하고 실제 readback으로 입증하는 것. 이 기능이 검증된 다음 Agent→MCP 노출을 진행하며, Viewer는 관련 없음.

이전에 전달한 아래 문서를 취소하지 않되, **이번 구현 요청을 더 구체적인 최신 지시로 우선 적용**한다.
- [G0 저사양/MSC 검증 r0001](L1_KNOWLEDGE_UPDATER_LOW_RESOURCE_LLM_MSC_G0_AND_INTEGRATION_HANDOFF_r0001_20261121_KST.md)
- [NR L1 TX 1건 실사용·Workspace readback](NR_L1TX_UL_TX_SWITCHING_KNOWLEDGE_AGENT_MCP_ONE_SHOT_HANDOFF_r0001_20261120_KST.md)
- [일반 Agent/MCP 스킬 연결](L1_MCP_AGENT_SKILL_ACCESS_AND_CAPABILITY_HANDOFF_r0002_20261120_KST.md)

## 1. 업무 GPT에 요청하는 실제 수정 항목과 완료 기준

| ID | 요구·기대 결과 | 소유 스킬 및 최소 수정 원칙 |
|---|---|---|
| R1 | **Module 후보 식별:** 사용자 입력 NR L1 Tx/UL Tx Switching → 기존 분류표/Knowledge·Work 우선 조회 → 코드 디렉터리/클래스/함수 후보 식별. 실제 책임 소유자와 참여 모듈을 구분 | Updater 오케스트레이션, 기존 Analyzer/Git 조회 REUSE. Module·Feature ID는 분류 검토행과 실제 정본 ID를 혼동 금지 |
| R2 | **Feature 후보 정밀화:** 자연어 검색만 사용하지 않고 candidate 파일→클래스→함수→호출/상태/분기 등 구조적 근거에 따라 기능 경계를 판정. TxSwitchMngr 등 명칭만으로 소유·실행 확정 금지 | `code-analyzer` 기존 CODE FACT/심볼·관계/근거 우선 REUSE. Updater가 중복 C++ parser/검색 엔진 구현 금지 |
| R3 | **Scenario 추출:** trigger·precondition·guard·state transition·실제 호출 순서·RF/HAL/PHY IPC·결과·release/exception의 코드 근거를 추적하고 CONFIRMED/INFERRED/UNKNOWN·미확인 경로 구분 | Analyzer facts → Updater 검증·분류. call edge만으로 branch feasibility/실제 실행 증명 금지. 잘못 연결된 코드 경로는 MSC/PUBLISH BLOCK |
| R4 | **저사양 LLM 최적화:** 범위별 계층 검색과 결정형 context slicing; 후보 1개 또는 Scenario 1개씩 제한된 코드 근거만 LLM 전달. 검색 누락과 잘림은 별도 표시하고 필요한 범위만 재조회 | 기존 스킬 검색·Python 활용. whole repo prompt, GraphRAG DB 신규 설치, CodeQL CLI 실행, 외부 모델/구현 소스 복사 금지 |
| R5 | **기존 Knowledge와 충돌·중복 대조:** 동일 Module/Feature/Scenario 및 Procedure 교차 참조, existing revision/source pin에 대해 변경·유지·추가 제안/미확인 결정. 편집/수동 문서 불변 | Updater 단일 owner; 기존 Work/Kernel writer, CAS·readback 등 기존 제공자 REUSE. 검증되지 않은 metadata/schema 추가 금지 |
| R6 | **실제 code-based MSC 연계:** 코드 근거가 검증된 Scenario만 `doc-converter` **기존 canonical IR**로 전달해 PUML/SVG/B형 HTML 생성·검증. source pin, `SOURCE_PARENT_DIR_V1`, `stack_group`, participant aliases, 기존 manifest·output path 보존 | 최신 PUBLIC `doc-converter_v0_2_26_1117.zip` 참고. 업무 설치 SHA·입력 action/allowed flags/IR를 실제 확인한 뒤 REUSE. 필요한 연결만 최소 수정; converter 자체 변경은 검증된 결손 없으면 없음 |
| R7 | **저장·회수:** Updater 직접 진입으로 분석한 내용, 선택적 MSC, Evidence·source revision·미확인·기존 내용과 차이를 개인 `l1-workspace`에 저장하고 revision·본문 readback 확인 | Updater + 기존 workspace writer. 이슈 Workflow 전체 실행을 전제하지 않음. 기존 Work가 있으면 그 Work 재개, 지식 편집에 새 Work 발급 강제 금지 |
| R8 | **결과 보고:** 실제 수행 run·스킬 버전/소스 SHA, 사용한 근거 범위·오류/누락, 토큰/메모리/시간, 기존 vs 개선 정확도, MSC 파일·링크 존재/재조회 상태를 사용자에게 표 형식으로 반환 | 업무 GPT/Agent. 검증 안 된 수치는 추정 금지; 확인된 근거만 공유. 제품 코드·상세 MSC·비밀·회사 제한 로그는 PUBLIC/PRIVATE 반출 금지 |

※ R1~R8은 **요구사항**이지 설치된 기능 부재의 단정이 아니다. 먼저 실제 구현에서 `REUSE` / `CONNECT` / `EXTEND_PROVEN_GAP` / `BLOCKED`로 매핑. 이미 구현된 기능을 중복 작성하지 말 것.

## 2. 업무용 1개 사례 수락시험

- **시험 대상**: `NR L1 Tx → UL Tx Switching`. 우선 검토행 `NT-F09`(Switching 결정·상태), `NT-F11`(Tx Path Switching)는 정본 Knowledge ID로 가정하지 않는다.
- **source pin**: 실제 접근 가능한 코드 commit/CL/P4 revision과 원본 크기·hash 기록. 같은 revision의 기존 Knowledge·기준 보고서 비교.
- **필수 성공 예**: (A) Module/Feature 후보와 근거 파일·클래스·함수 확인 (B) 대표 2~3 Scenario의 trigger/조건/상태/종료 경로 근거 확인 (C) 부정 사례에서 잘못된 호출·분기 단정 차단 (D) doc-converter native 입력으로 실제 MSC 1건 생성·검사 및 링크/manifest 확인 (E) 개인 Workspace 저장·readback (F) 저사양 LLM 실행 토큰·시간·메모리 실제 측정.
- **필수 회귀**: 소스 revision 불일치, 증거 누락·truncation, 모듈 소유 혼동, 중복 Feature 생성, MSC 호출 순서 불일치, HTML 실패 시 깨진 성공 링크, 수동 Knowledge/기존 Work 덮어쓰기, 그룹 미승인 게시 방지.
- **MSC 분리**: Converter는 실제 확인된 scenario facts를 표현하는 도구이며 코드 분기 실행 가능성을 새로 증명하지 않는다. 상세 MSC는 업무 환경 허용 저장소에만 보관한다.
- **평가**: precision/recall 또는 표본별 오탐·누락, 근거 추적 커버리지, 문서 중복률, MSC source/participant/flow 재현성, 모델 토큰·평균 지연. 해당되는 실제 측정값만 기록.

## 3. 구현·리뷰·배포 절차

1. 업무 GPT가 **현재 설치** `l1-knowledge-updater`, `code-analyzer`, `doc-converter`, 기존 Kernel/Writer의 SKILL·action/실제 코드·version·policy를 현장 READ_ONLY 확인한 다음 요구 R1~R8을 매핑한다. `l1-knowledge-manager` 구버전으로 대체 금지.
2. 기존 권한 내 개발환경에서 이미 입증된 부족분만 수정·자체시험. 필요한 최소 코드/설계만 변경하고 기존 설치본과 이전 이력을 보존한다. 실제 분석/지식 쓰기 권한이 없다면 가능한 정적 수정·시험까지만 수행하고 쓰기는 BLOCKED.
3. **외부 전달 허용 범위**: 소스·상세 MSC·업무 로그·회사 제한 코드 불포함. `PRIVATE wonhwipark/CoWork-Skill-Collab`의 `collab/projects/L1-WORKSPACE-RAG-20261111-001/`에 비민감 구현 변경표, 통과/실패 표, 버전·SHA·권한·차단 이유·리뷰용 안전한 후보를 연결한다. 실제 업무 제한 원본은 업무 `l1-workspace`에 보존. **사용자 제공 기준에 맞지 않는 수정 패키지는 PUBLIC/PRIVATE에 반출하지 말 것**.
4. 고정된 비민감 후보에 대해 Windows Claude Code 독립 리뷰 REQUEST/SOURCE_PIN/승인·서명/READY 절차 준수, 독립 결과+영수증 수집. 사용자 기존 승인·위임이 유효한 경우 중복 승인 요청 금지. 리뷰 입력을 만들 수 없거나 자동 유료 리뷰 자격이 확인되지 않으면 `INDEPENDENT_REVIEW=NOT_RUN/PENDING`으로 기록하고 가능한 개발·시험은 계속한다.
5. GPT가 리뷰와 실제 시험을 판정하고 적합한 새 버전 ZIP에 대해서만 SHA-256·size·CRC·경로 이탈·민감정보·구버전 보존 검사. **승인된 PUBLIC `L1Work/main` 루트 게시** 후 원격 실바이트 확인. ZIP 전달과 업무 Linux 설치/실행을 구분한다. 설치·운영 전환은 별도 유효 승인에 따름.
6. 제품 소스 수정·자동 그룹 `l1sw-dev-knowledge` 게시·MCP 서버 운영 변경·새 유료 모델 호출은 이 수정 요구서만으로 승인되지 않는다.

## 4. 의존성·원본 근거

- L1Work 최신 PUBLIC 참조 ZIP: [doc-converter v0.2.26](https://github.com/wonhwipark/L1Work/blob/main/doc-converter_v0_2_26_1117.zip), [code-analyzer v0.15.4](https://github.com/wonhwipark/L1Work/blob/main/code-analyzer_v0_15_4_1119.zip). 이는 설치 확인이 아니라 공개 원본 참조다.
- CoWork 기존 정본: `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_WORKSPACE_KNOWLEDGE_UPDATER_OWNERSHIP_AND_VIEWER_UX_DELTA_r0004_20261118_KST.md`; `L1_MSC_DUAL_ENTRY_DOCUMENT_DESIGN_r0001_20261117_KST.md`; `LOW_RESOURCE_LLM_RESEARCH_LICENSE_MSC_AND_CANDIDATE_QA_r0001_20261121_KST.md`.
- 코드/논문 차용은 아이디어만. 외부 라이브러리·라이선스 포함 코드·상용 CodeQL CLI 사용 없이 기존 구현 우선.

## 5. 업무 GPT 회신 형식과 한 번에 복사할 요청

| 단계 | 상태(필수) | Evidence 또는 사유 |
|---|---|---|
| 설치 계약 확인 | PASS/NOT_RUN/BLOCKED | 실제 스킬 버전·source pin |
| 수정 범위 확정 | REUSE/CONNECT/EXTEND/DEFER | R1~R8 매핑표 |
| 실제 개선/자체시험 | PASS/FAIL/NOT_RUN | 테스트 수·실측 값 |
| NR Switching 사례 분석 | PASS/FAIL/NOT_RUN | Source pin·Scenario 수·근거 |
| MSC / Workspace readback | PASS/FAIL/NOT_RUN | 내부 위치·revision; 외부 허용 요약 |
| 독립 리뷰 요청·결과 | NOT_RUN/PENDING/PASS/FAIL | REQUEST ID·영수증, 비용(있는 경우) |
| 후보/최종 ZIP | DEV_ONLY/RELEASED/BLOCKED | 해시·위치·배포/호스트 상태 별도 |
| 다음 한 동작 | 1개 | 남은 최초 차단 단계만 |

> 업무 GPT는 `wonhwipark/L1Work` `main`의 `handoffs/L1_KNOWLEDGE_UPDATER_NR_UL_TX_SWITCHING_MODIFICATION_REQUIREMENTS_r0001_20261121_KST.md`에 따라, 실제 `l1-knowledge-updater`의 R1~R8 지원·결손을 먼저 확인하고, 해당 권한 내에서 기존 Analyzer·Converter를 재사용해 NR L1 Tx UL Tx Switching Module/Feature/Scenario 분석과 코드 근거 MSC·개인 Workspace 결과 검증이 가능하도록 필요한 부분만 수정·자체시험해 주세요. 단순 G0 보고에서 멈추지 말고 가능한 수정·검증·비민감 결과 인계까지 이어 주세요. 제한 자료 반출/미승인 운영 설치·그룹 게시·유료 호출은 하지 말고 BLOCKED를 분리해 보고해 주세요.
