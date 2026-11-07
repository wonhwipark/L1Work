# L1 Knowledge — 기존 MCP Wrapper 최소 확장·실호출 검증 원샷 프롬프트 v1.0

- 작성: 2026-11-07
- 대상: **사내 Agent** (기존 MCP Wrapper 코드·등록·테스트에 접근 가능한 실행 환경)
- 기준 입력: `L1_Fix_Workflow_Knowledge_Usecase_Inhouse_Review_v1_3_20261106.md`, `L1_Workflow_Knowledge_MCP_Interface_Integrated_OneShot_v1_4_1107.md`, 사내에 저장된 해당 진단 상세 MD
- 기존 Agent 숫자 진단: `2 1 1 3 2 2 2 1` (설계 조사), `2 3 3 1 3 1` (실제 MCP 호출 조사)
- **주의:** 숫자 진단은 Agent의 보고이며 이 문서 작성자가 MCP 등록부·응답을 직접 확인한 것이 아니다. 실제 함수·경로·스키마는 사내 소스로 확인한다.

## 0. 이번 작업 목표와 권한 경계

기존 MCP Wrapper에서 **(1) U01~U15 통합 기능 진단, (2) 개인/그룹 지식 원문 조회**를 실제 MCP 호출 가능한 읽기 전용 도구로 연결하고, **(3) 기존 정상 동작하는 결과 재조회 도구**로 진단 결과를 다시 조회할 수 있게 한다. 새로운 MCP 서버·독립 스킬·별도 DB를 만들지 않는다.

**허용:** 기존 코드/설정의 읽기, 변경 영향 분석, 기존 Wrapper 내 최소 코드·등록·스키마·단위/회귀 테스트 수정, 격리된 로컬 테스트, 변경 후보·diff·시험 기록 생성. **금지:** 운영 등록/배포·서비스 재시작·운영 allowlist/권한 변경, 사내외 Git push, Work 생성/수정, 지식 정본 수정, 인덱스 재구축, 실제 제품 E2E, 민감 자료 반출. 운영 적용이 별도 승인 대상이면 `STAGED_APPROVAL_REQUIRED`로 멈춘다. 개발용 등록·격리 시험은 기존 승인 범위에서만 한다. 허가되지 않은 코드 수정도 승인 대기 상태로 설계·패치안까지만 작성한다.

## 1. 먼저 실제 MCP 계약 확인 — 추측 금지

1. 실제 MCP Wrapper의 등록 목록, tool ID, 입력·출력 JSON Schema, dispatcher, allowlist, 결과 보존/재조회, 인증·접근 범위, 실행/테스트 명령을 코드에서 확인한다. 문서상 명령명과 실제 등록 도구를 구분한다.
2. `l1-fix-workflow`, `work-ledger-kernel`, `l1sw-dev-knowledge`, `l1-github`의 실제 설치본과 read-only 함수/CLI/Controller 진입점을 매핑한다. `v1.6.64` 설치를 가정하지 않는다.
3. 기존 `workflow_audit_result_get`과 동등한 **정상 재조회 인터페이스**를 확인하고 재사용한다. 기존 Job ID/Receipt/Registry 및 보존 정책을 우회·복제하지 않는다.
4. 앞선 진단의 `통합 진단 미등록`, `지식 조회 미등록`, `RAG 주입 미확인`을 **실제 MCP 등록 목록과 부작용 없는 호출 응답**으로 재확인한다. 다른 이름의 동등 도구가 있다면 중복 생성하지 않는다.
5. 각 U01~U15별로 기존 도구·필요 데이터·실제 호출 가능 여부·미지원 원인을 표로 기록한다. 구현 범위는 아래 두 읽기 인터페이스와 기존 재조회 연결에 한정한다.

## 2. 최소 MCP 계약 — 기존 이름/스키마 우선

아래 도구명은 **논리 제안명**이다. 기존 동등 도구가 있으면 해당 도구를 확장한다. Agent에게 임의의 미등록 도구 호출을 시도하게 하지 않는다.

### A. `workflow_capability_audit` (READ_ONLY)

**입력:** `usecase_ids` (기본 U01~U15), `include_work_git` (기본 true), `include_rag` (기본 true), `evidence_mode=existing_only`, `max_items` (기본 15). 입력값 제한·형식 검증 필수.

**반환:** `schema_version`, `audit_id`(기존 결과 저장 규칙과 호환), `run_status`, `installed_versions`, `registered_tools`, `items[]`(U ID, 기능 지원 `FULL|PARTIAL|NONE|UNKNOWN`, 증거 `E0..E3`, MCP 등록/호출 상태, 기존 tool ID, 누락 입력/출력, `REUSE|CONNECT|BUILD|DEFER`, GAP), `total_count`, `returned_count`, `has_more`, `not_run`, `errors`, `summary_ref_internal`.

- **15개 항목의 존재와 순서 보장**. 개별 기능의 증거가 부족해도 누락하지 말고 `UNKNOWN/E0` 반환.
- 기존 등록/코드/시험 기록을 **읽어서 판정**한다. 실행 불가능한 분석·게시·호스트 연속성은 `NOT_RUN`; 근거 없이 E3/FULL로 승격하지 않는다.
- 진단 실행 결과는 기존 결과 저장소의 **허용된 기록 API**를 통해서만 보존한다. 저장 API가 읽기 전용 계약과 충돌하면 `NOT_PERSISTED`로 반환하고 재조회 성공을 주장하지 않는다. 진단 생성 시의 제한된 결과 저장과 업무 데이터 수정은 명확히 분리한다.
- 과거 `total_count/has_more` 문제를 회귀 시험한다.

### B. `knowledge_context_probe` (READ_ONLY)

**입력:** `query`(필수), `module`, `feature`, `scenario`, `rat`, `stack`, `branch`, `source_revision`, `source_scope=personal|group|both`, `max_sections`, `max_excerpt_chars`, `verify_injection=false`.

**반환:** `schema_version`, `probe_id`, `retrieval_status`, `sources[]`(제공자 종류, 문서 ID/절 ID, 상대 경로 또는 내부 전용 참조, **실제 원문 절**, 문서/코드 revision, scope 일치 판정, 검증 수준, 관련 Work, hash), `excluded_reasons`, `staleness`, `conflicts`, `injection_status`, `injection_evidence_internal`, `errors`.

- 기존 module-library, 기존 개인 문서 조회, 그룹 지식 제공자의 **실제 사용 가능한 읽기 경로**를 연결한다. 그룹 전용 API가 없다면 허용된 로컬 Markdown 범위 검색을 `LOCAL_FALLBACK`으로 표기하며 전용 API 성공으로 표시하지 않는다.
- 단순 제목·snippet 검색을 **원문 절 반환**으로 오인하지 않는다. 문서가 없는 경우 `NO_MATCH`, 권한 부족 `PERMISSION_DENIED`, 범위 불일치 `SCOPE_MISMATCH`, 오래된 인덱스 `STALE_INDEX`, 제공자 장애 `PROVIDER_UNAVAILABLE`를 구분한다.
- `retrieved`와 `injected`를 구분한다. Agent/LLM 실제 입력에 근거가 들어간 관찰 가능한 시험 증거가 없으면 `injection_status=NOT_VERIFIED`; 임의로 모델 프롬프트/세션을 열거나 주입 성공으로 선언하지 않는다.
- 요청당 문서 수/발췌 길이/시간 제한, 경로 정규화·접근 제어, 악성 지식 문서의 지시문 무시, 개별 문서 오류 격리를 적용한다. 검색 결과는 도구 권한을 변경할 수 없다.

### C. 기존 결과 재조회 도구 (REUSE)

기존 정상 도구에 새 진단 결과가 연결되는지 확인한다. 입력은 기존 `audit_id`/`result_id` 등 **실제 식별자 계약**을 유지하고 `summary|items|internal`, 페이지네이션을 지원할 수 있는 범위에서만 확장한다. 조회는 기존 저장 결과만 읽으며 **재진단·모델 재호출·Work 재실행 금지**. `NOT_FOUND/EXPIRED/PERMISSION_DENIED`를 구분하고 권한에 따라 원문을 마스킹한다.

## 3. 구현 절차 — 중간 질문 최소화

1. **BASELINE:** 변경 전 버전/등록 도구/테스트 결과/dirty 상태 기록. 기존 변경사항을 덮어쓰지 않는다.
2. **GAP:** A/B가 미등록인지, 내부 함수가 없는지, Wrapper 등록/allowlist/응답 매핑만 빠졌는지 분리. 재조회 C는 기존 함수 재사용.
3. **PATCH:** 승인된 범위에서 최소 파일만 수정. 기존 tool ID·응답 필드·호출자와 하위호환, 신규 필드 additive 원칙. 소스·설정·원본 근거를 보고서에 외부 공개하지 않는다.
4. **TEST:** 격리된 환경에서 실제 MCP 등록 목록 재조회 → A/B 각각 정상 호출 → 스키마 검증 → A 결과의 C 재조회 → 동일 ID/페이지/건수 비교. 실제 서버 연결이 불가하면 `NOT_RUN`으로 남긴다.
5. **REGRESSION:** 기존 Work 검색/조회, MCP read-only plan, `total_count/has_more`, 기존 C 재조회, CLI/Controller/MCP 응답 일치, 오류·권한·타임아웃·scope·stale·그룹 fallback·주입 미확인, 지식/Work/Git 무변경 검사.
6. **STAGE:** 변경 파일·diff·시험 증거·미해결/승인 필요 사항을 사내 상세 MD로 보존. 운영 배포/재시작/권한 변경은 별도 승인 전 중지.

## 4. 필수 검증 케이스

| ID | 검증 | 합격 조건 |
|---|---|---|
| M01 | Wrapper 등록 | A/B가 실제 도구 목록에 나타남 (격리 환경) |
| M02 | 통합 진단 | U01~U15 15개 반환, UNKNOWN 허용, 누락 0 |
| M03 | 응답 스키마 | 필수 필드/enum/형식 유효, 민감 데이터 출력 정책 준수 |
| M04 | 개인 지식 | 허용 문서 원문 절과 출처·revision 반환 |
| M05 | 그룹 지식 | 제공자 또는 `LOCAL_FALLBACK` 정확히 표기 |
| M06 | 범위/실패 | scope mismatch/stale/no match/permission/timeout 구분 |
| M07 | RAG 상태 | 조회 성공을 주입 성공으로 오인하지 않음 |
| M08 | 기존 결과 재조회 | 동일 진단 ID로 C 호출해 저장 결과 확인; 불가 시 원인 명시 |
| M09 | 호환성 | 기존 Work 조회·건수·has_more·C 조회 회귀 통과 |
| M10 | 부작용 | Work/지식 정본/인덱스/Git 변경 0, 운영 서비스 무변경 |
| M11 | 권한·보안 | 경로 탈출·무권한 원문·과도한 응답·프롬프트 인젝션 차단 |
| M12 | 실호출 증거 | 호출 도구 ID·환경·시점·요청/응답 스키마·PASS/FAIL/NOT_RUN 기록 |

## 5. 사내 산출물과 최종 응답

**사내 전용** `L1_MCP_WRAPPER_EXTENSION_IMPLEMENTATION_AUDIT.md`: 기준 설치본, 실제 도구 ID/함수/파일, 변경 diff, U01~U15 매핑, M01~M12 결과, 등록·실호출 증거, 재조회 결과, 운영 승인/배포 미실시, 알려진 결함/미검증.

**공유 허용 시에만** `L1_MCP_WRAPPER_EXTENSION_DECISION_SUMMARY.md`: 민감 코드·내부 경로·URL·토큰·소스/로그·Evidence 원문 없는 상태 요약. 반출 허용 여부를 확인하지 못하면 작성만 사내에서 하고 외부 전달 금지.

최종 사용자 응답은 **숫자 8개만** 출력한다. 각 자리는 다음과 같다.

| 자리 | 값 |
|---|---|
| A 코드 수정 | 1=완료 / 2=승인대기 / 3=실패 / 4=불필요(기존 재사용) |
| B A 도구 등록(격리 시험) | 1=등록·실호출 정상 / 2=등록만 / 3=미등록 / 4=시험불가 |
| C B 도구 등록(격리 시험) | 1=등록·실호출 정상 / 2=등록만 / 3=미등록 / 4=시험불가 |
| D 기존 C 재조회 연동 | 1=새 진단 ID 재조회 성공 / 2=기존 C만 정상 / 3=실패 / 4=시험불가 |
| E U01~U15 응답 | 1=15개 구조화 / 2=일부 / 3=불가 |
| F RAG 주입 | 1=실제 입력 주입 검증 / 2=조회만 검증 / 3=미검증 |
| G M01~M12 시험 | 1=모두 PASS / 2=일부 PASS/미실행 / 3=FAIL 있음 / 4=전체 NOT_RUN |
| H 운영 적용 | 1=기존 승인 범위 내 적용·검증 / 2=미적용·승인대기 / 3=실패 / 4=적용 불필요 |

**주의:** `A=1`은 로컬 코드 수정 완료이지 운영 설치 완료가 아니다. `B/C=1`도 격리 환경 실호출 성공이지 운영 MCP E2E 통과가 아니다. `H=1`은 실제 적용 증거가 있을 때만 선택한다.

**다음 한 동작:** 실제 등록/호출 결과를 바탕으로 운영 적용 승인 또는 누락 기능 보완 중 하나를 제시하되, 사용자에게는 위 숫자만 전달해도 후속 판정 가능하게 한다.
