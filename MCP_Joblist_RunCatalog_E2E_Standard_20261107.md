# MCP–Job-list Run Catalog 등록·검증 표준 운영 절차

- 문서 버전: 1.0 / 기준일: 2026-11-07
- 적용 대상: Job-list One-shot 작업, MCP Wrapper/Registry/Allowlist, Run Catalog, `l1 analysis find`, LLM/Agent 조회 체인
- 목적: Job 실행 후 결과가 생성되었는데도 Agent가 증거를 발견하지 못하는 반복 장애 방지
- 상태: **운영 표준 제안안 — 실제 구현·상시 적용 미확인**. 다음 신규 Job에서 전체 E2E 검증 필요

## 1. 지금까지 확인된 사실과 한계

| 항목 | 최종 근거 | 상태 |
|---|---|---|
| 검증 증거 조회 | 최근 Agent 결과 A=1 | PASS |
| Job/Run/Result ID 정합성 | 최근 Agent 결과 B=1 | PASS |
| 기존·신규 Job 조회 | 최근 Agent 결과 C=1 | PASS |
| 전체 E2E 완료 | 최근 Agent 결과 D=3 | **미검증** |
| 반복 실패 원인 | LLM 분석 및 사용자 보고 | 검증 증거의 **Run Catalog 등록 누락**으로 `l1 analysis find` 체인에서 발견 불가; 복구 보고 후 Agent 증거 조회 성공 |

위 결과는 **특정 복구 사례의 조회 성공**을 뒷받침한다. 모든 후속 Job에 자동 등록이 이미 구현되었다거나 전체 E2E가 통과했다는 뜻은 아니다. 과거 v0.4.29·v0.4.30에서 발생한 여러 차례의 Queue/Receipt 성공은 비즈니스 작업 완료와 구분한다.

## 2. 역할 및 안전 경계

- **GPT:** 목표·완료 기준·실패 분류 설계, 결과 판정, 정본 관리
- **LLM:** 승인된 범위에서 구현·진단·회귀시험 수행, Run Catalog 게시 및 동일 API 재조회
- **Agent:** 실제 제공된 읽기 전용 MCP 도구로 독립적인 검색·원본 조회·ID 검증
- **MCP:** 등록/조회 계약, 권한 제어, Run Catalog와 Result API의 일관된 데이터 제공
- **Job-list:** 새 버전당 새 활성 One-shot Job 1개; 기존 Job 재실행 금지

금지: 인증 우회, Allowlist 전체 개방, 기존 Job/Run/Result ID 임의 생성·치환, 실행 이력 삭제, 허가 없는 운영 배포 또는 재시작, 민감한 코드·로그·경로·인증정보 외부 출력. 승인 경계를 넘는 작업은 `STAGED/APPROVAL_REQUIRED`로 멈춘다.

## 3. 모든 신규 Job에 적용할 등록·조회 계약

```text
새 Job 접수/등록
  → Queue / Receipt 생성
  → 실제 작업 실행과 완료 상태 판정
  → Result 및 검증 Evidence 저장
  → Run Catalog에 Job–Run–Result–Evidence 관계 등록
  → 등록 영수증과 인덱스 상태 확인
  → 'l1 analysis find'와 Result API에서 원본 재조회
  → Agent가 동일 식별자로 독립 조회
  → 최종 E2E 판정
```

필수 정책:

1. **단일 기준 키:** 발급된 `job_id`, `run_id`, `result_id`, `evidence_id`를 변형 없이 보관한다. 실제로 발급되지 않은 ID는 `UNKNOWN`으로 남기며 대체 생성하지 않는다.
2. **결과와 Catalog의 원자적 연결:** 구현이 허용하면 결과 작성 + Catalog 등록을 트랜잭션 또는 복구 가능한 outbox 작업으로 처리한다. 실패 시 등록 대기/오류 상태로 남기고 성공을 반환하지 않는다.
3. **멱등 등록:** 동일 식별자로 재시도하면 중복 Run이나 결과가 생기지 않아야 한다. 동일 ID에 다른 결과가 연결되면 자동 덮어쓰기 대신 충돌 처리한다.
4. **검색 가능성 확인:** 게시 성공만으로 완료하지 않는다. `l1 analysis find`의 **실제 실행되는 검색/조회 인터페이스**로 해당 등록 항목을 찾고, 원본 Result 및 Evidence로 이어지는지 확인한다. 대화 세션 검색은 증거가 아니다.
5. **권한 검증:** 정상 등록 Job은 조회되고 미승인 Job/권한 없는 호출은 거부되는지 확인한다. 접근할 수 없는 항목은 정상으로 추정하지 않는다.
6. **상태 분리:** `QUEUE_ACCEPTED`, `RUN_COMPLETED`, `RESULT_PERSISTED`, `CATALOG_REGISTERED`, `INDEX_DISCOVERABLE`, `AGENT_READBACK_PASS`, `E2E_PASS`를 서로 다른 사실로 관리한다.
7. **기존 호환성:** 과거 실패 Job과 성공 Job을 회귀시험에 함께 포함한다. 기존 Job 재실행 없이 저장 기록만 조회한다.
8. **민감정보 최소화:** 외부로 전달하는 증거는 상태 코드·참조 ID 및 비민감 요약에 한정한다. 실코드·원시 로그·토큰은 게시하지 않는다.

### 최소 결과 레코드(예시 스키마; 실제 MCP 지원 여부 검토 후 채택)

```json
{
  "schema_version": "1",
  "job_id": "<existing-id>",
  "run_id": "<existing-id-or-null>",
  "result_id": "<existing-id-or-null>",
  "evidence_id": "<existing-id-or-null>",
  "job_execution": "COMPLETED|FAILED|UNKNOWN",
  "catalog_registration": "PASS|FAIL|UNKNOWN",
  "find_readback": "PASS|FAIL|UNKNOWN",
  "agent_readback": "PASS|FAIL|UNKNOWN",
  "e2e": "PASS|PARTIAL|FAIL|UNVERIFIED",
  "error_code": "NONE|REGISTRY_MISSING|CATALOG_MISSING|ID_MISMATCH|INDEX_NOT_DISCOVERABLE|ACCESS_DENIED|SCHEMA_MISMATCH|UNKNOWN"
}
```

> 이 JSON은 **권장 계약 초안**이며 지원 API를 확인하기 전까지 실제 존재하는 MCP 스키마로 간주하지 않는다.

## 4. 자동 진단·복구 규칙

- `CATALOG_MISSING` / `INDEX_NOT_DISCOVERABLE`: 원본 Result·Run 식별자가 존재하는지 확인 → 등록/인덱스 지연 원인 분석 → 승인된 방식으로 **등록만 보정** → 동일 `l1 analysis find` 경로 재조회
- `ID_MISMATCH`: 실제 Job–Run–Result–Evidence 원본 관계를 비교 → 증거 기반으로만 매핑 수정 → 관련 기존 Job 회귀시험
- `REGISTRY_MISSING` / `SCHEMA_MISMATCH`: MCP 노출 도구·Registry·Allowlist·버전 계약 비교 → 최소 수정 → 미승인 Job 거부 시험
- `ACCESS_DENIED`: 우회하지 않고 권한·승인 책임자를 확인해 `APPROVAL_REQUIRED` 처리
- 판정 불가: `UNKNOWN` 기록 및 재현 가능한 비민감 오류 코드 게시. 추측성 코드 수정 금지

LLM은 동일 실패에 대해 승인된 범위에서 **최대 3회** 진단·수정·시험을 시도한다. 같은 오류가 반복되면 중단하여 원본 실패 근거를 고정한다. 무한 재시도 금지.

## 5. 완료 게이트

| 게이트 | 통과 조건 | 실패 시 |
|---|---|---|
| G1 실행 | 유효한 실행 근거 및 결과 상태 확인 | `EXECUTION_UNVERIFIED` |
| G2 등록 | Run Catalog에 Result/Evidence 등록 확인 | `CATALOG_MISSING` |
| G3 검색 | `l1 analysis find`로 실제 조회·원본 연결 확인 | `INDEX_NOT_DISCOVERABLE` |
| G4 정합성 | 발급된 Job/Run/Result/Evidence ID 연결 일치 | `ID_MISMATCH` 또는 `UNKNOWN` |
| G5 호환성 | 기존·신규 Job 조회 및 미승인 조회 차단 시험 | `COMPAT_FAIL` |
| G6 독립 검증 | Agent가 동일 대상·도구로 직접 원본 조회 | `AGENT_VERIFY_REQUIRED` |
| G7 전체 E2E | 해당 **신규 실제 Job**의 등록→실행→게시→검색→독립 조회 전체 확인 | `UNVERIFIED` |

**E2E PASS 규칙:** G1~G7 모두 실제 증거로 통과한 경우만. 등록·검색·ID·호환성 조회가 정상이어도 실제 신규 Job 전체 흐름을 수행·검증하지 않았다면 `E2E=UNVERIFIED`로 남긴다.

## 6. LLM용 One-shot 적용 지시문

다음 내용을 LLM에 한 번 전달한다. 이미 시행된 변경을 재수정하지 말고, 우선 현재 구현과 저장된 작업 기록을 조회한다.

> **[MCP–Job-list 표준 등록·검증 규칙 적용]**
>
> 기존 복구 사례의 마지막 Agent 결과는 `1 1 1 3`이다(증거 조회 PASS, ID PASS, 기존·신규 조회 PASS, 전체 E2E 미검증). 과거 문제는 검증 Evidence를 Run Catalog에 등록하지 않아 `l1 analysis find` 체인에서 발견할 수 없었던 것으로 보고됐다.
>
> 1. 기존 MCP 구현·Run Catalog·Result 등록·`l1 analysis find`·Job-list 실행 계약과 테스트를 조사한다. 대화 검색은 원본 증거로 인정하지 않는다.
> 2. 자동 등록·멱등성·원본 참조·검색 가능성·기존 Job 호환성·미승인 조회 차단이 이미 구현됐는지 먼저 확인한다. 구현이 부족한 항목만 승인된 범위에서 수정한다.
> 3. Result 저장→Run Catalog 등록→동일 find 인터페이스 재조회까지 하나의 완료 규약으로 만든다. 작업 자체 성공, 등록 성공, Agent 독립 조회, E2E 성공을 각각 구별한다.
> 4. 과거 실패 Job을 포함하여 단위·회귀·오류주입 시험을 수행한다. 수정·시험을 최대 3회까지 자체 반복하되 동일 결함 반복 시 차단 원인과 증거를 기록하고 중단한다.
> 5. 배포·서비스 재시작·권한 변경은 실제 승인 범위가 확인될 때만 실행한다. 미승인 변경은 STAGED 유지한다. 기존 Job 재실행/Job-list 재설치 금지.
> 6. 가능한 비민감 결과를 MCP 원본 결과 및 Run Catalog에 기록하고 **Agent가 호출할 동일 검색 도구**로 재조회한다. 재조회가 불가하면 성공이라 보고하지 않는다.
> 7. 검증 결과를 숫자 8개만 요약하되 상세 증거와 실패 항목은 MCP 작업 기록에 남긴다.
>
> 응답: A. 기존 구현 확인 `1=완료/2=미확인` B. 자동 Catalog 등록 `1=PASS/2=FAIL/3=미검증` C. find 재조회 `1=PASS/2=FAIL/3=미검증` D. ID 정합성 `1=PASS/2=FAIL/3=미검증` E. 기존 Job 호환성 `1=PASS/2=FAIL/3=미검증` F. 회귀시험 `1=PASS/2=FAIL/3=미실행` G. 운영 반영 `1=완료/2=STAGED/3=불필요` H. Agent 독립 검증 `1=PASS/2=FAIL/3=필요`.

## 7. Agent용 짧은 검증 지시(3,000자 이내)

Agent에는 별도 파일 `AGENT_MCP_Joblist_Standard_Verify_1107.md`의 내용만 전달한다. **새 실제 Job이 없는 경우 E2E를 PASS로 추정하지 않는다.**

## 8. 다음 한 동작

1. LLM에 **6절 지시문**으로 등록·검색 규칙의 상시 적용 여부 확인 및 누락 구현 보완을 수행한다.
2. 새로운 승인된 One-shot Job이 생성될 때 **7절 Agent 검증**을 실시하여 G1~G7의 실제 E2E를 확정한다.
3. 둘 중 어느 단계라도 실패 시 미해결 내용을 MCP 작업 기록에 저장하고, 기존 정상 경로를 다시 수정하지 않는다.
