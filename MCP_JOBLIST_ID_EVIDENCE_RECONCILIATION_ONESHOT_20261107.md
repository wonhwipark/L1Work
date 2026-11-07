# MCP–Job-list ID 불일치 증거 통합·복구 One-shot 지시서

- 작업 키: `MCP-JOBLIST-ID-RECONCILIATION-20261107`
- 대상: **LLM(진단·수정·시험)** → **Agent(읽기 전용 독립 검증)**
- 목적: 동일 Job에 대해 LLM은 ID 정합성 PASS, Agent는 FAIL을 보고한 **검증 대상·증거·판정 기준의 차이**를 확정하고, 확인된 결함만 수정한다.
- 원칙: 기존 기록 재사용, 무증거 수정 금지, 기존 Job 재실행 금지, 승인 범위 내 변경만 수행, 운영 반영과 Agent 검증 분리.

## 1. 현재 알려진 사실 및 미확인 사항

| 출처 | 최근 결과 | 의미 |
|---|---|---|
| LLM | `1 1 1 1 1 2` | ID·Catalog/Registry·기존 Job·회귀시험 PASS, 운영 반영 완료 **보고**, Agent 검증 필요 |
| Agent | `2 1 1 1 3` | **신규 Job ID 정합성 FAIL**, 기존 Job PASS, MCP 기능 PASS, 운영 반영 확인, 전체 E2E 미확인 |

**중요:** 두 결과가 동일 Job/Run/Result 레코드를 검증했는지 확인되지 않았다. 실패 유형도 확정되지 않았다. `Result 조회 성공`과 `Job ID ↔ Run ID ↔ Result ID 연결 성공`은 서로 다른 판정이다.

비교 대상:
- `JOB-20261107-L1-MCP-E2E-PILOT-01` (v0.4.29)
- `JOB-20261107-MCP-WRAPPER-REGISTRY-RECOVERY-01` (v0.4.30)
- 실제 운영 기록에서 확인되는 **최신 복구 작업**과 이전 Agent 실패 대상(발견되면 추가). 임의 Job/Run/Result ID 생성 금지.

## 2. LLM에 전달할 통합 실행 프롬프트

> 아래 본문을 LLM에 한 번 전달한다. 중간 보고나 반복 객관식 질의 없이 허용 범위의 모든 단계를 연속 수행한다.

### 역할 및 완료 목표

당신은 MCP Wrapper/Job-list 통합 복구의 책임 실행자이다. 위 작업 키와 대상 Job을 기준으로 이미 존재하는 실행·검증 기록을 조사하고, **Agent FAIL과 LLM PASS가 갈린 정확한 증거**를 우선 확보하라. 추측성 코드 수정은 금지한다.

### 단계 A — 같은 증거에 정렬

1. 기존 MCP 작업 기록, Agent 조회 실패 이력, LLM 회귀시험 이력, Catalog·Queue·Receipt·Result 데이터를 **기존 조회 기능으로 먼저 검색**하라.
2. 두 검증에 사용된 **실제 Job ID, Run ID, Result ID**, Job-list 버전, 데이터 소스·스냅샷/캐시, 사용한 MCP 도구·조회 인자, 관측 시점을 비교하라. 값 자체는 승인된 내부 기록에만 보관하라.
3. 실제 스키마에서 Run/Result ID가 의무 필드인지부터 확인하라. 의무가 아닌 경우 `NOT_APPLICABLE`과 `MISSING`을 구분하고, 스키마에 없는 키를 강제하지 말라.
4. 비교 대상마다 아래 레코드를 **있는 그대로** 기록하라(민감값은 외부 출력 금지):
   - `job_id` / `run_id` / `result_id` (존재·연결 근거 포함)
   - `catalog_ref` / `queue_ref` / `receipt_ref` / `result_ref`
   - `lookup_tool`, `lookup_key`, `version_or_schema`, `source_snapshot`, `observed_at`
   - `join_rule`, `join_evidence`, `observed_status`, `failure_code`
5. `Queue DONE`/`Receipt SUCCESS`만으로 수정 실행 성공이나 ID 일치로 간주하지 말라. ID는 **신뢰할 수 있는 원천 참조 관계**로 확인하고, 시간순 정렬·이름 유사성만으로 결합하지 말라.
6. Agent의 상세 실패 증거가 남아 있지 않다면, 해당 사실을 `AGENT_EVIDENCE_MISSING`으로 기록하고 가능한 범위의 독립 재조회·비교까지만 수행하라. 동일한 실패를 재현하지 못하면 임의로 원인을 확정하지 말라.

### 단계 B — 불일치 분류와 최소 수정

아래 중 실제 근거가 있는 유형만 판정하라.
- `SCOPE_MISMATCH`: Agent와 LLM이 서로 다른 Job/Run/Result를 조회
- `LINK_MISSING`: 실재 레코드 간 참조 누락
- `CROSS_JOB_LINK`: 다른 Job의 Run/Result에 잘못 연결
- `PROJECTION_MISMATCH`: 서로 다른 MCP 도구가 ID/필드를 다르게 노출
- `SNAPSHOT_MISMATCH`: 버전·캐시·데이터 소스 차이
- `SCHEMA_MISMATCH`: ID 필수 여부·스키마 버전 차이
- `ACCESS_VIEW_MISMATCH`: 역할별 노출·필터 차이
- `NO_REPRO` / `EVIDENCE_INSUFFICIENT`: 재현 불가 / 판단 근거 부족

원인 확정 시 기존 승인 범위에서 최소한으로 수정하라. Registry/Catalog/Result 조회의 단일 정본 관계, 조회 키 정규화, 스키마별 필드 판정을 우선 검토하라. 이미 정상인 기존 Job과 조회 기능은 보존하라. 무단 Allowlist 확장·인증 우회·이력 변경은 금지한다.

### 단계 C — 같은 사례 기반 회귀시험

변경 전에 실패한 **정확한 Job/Run/Result 사례**를 재현 시험에 고정하고, 수정 후 동일한 조회 인터페이스·키·기준으로 재시험하라.
- T1 신규 Job의 ID 연결과 참조 원천 확인
- T2 기존 Job의 Catalog/Queue/Receipt/Result 호환성
- T3 미등록 Job 조회 거부 및 권한 유지
- T4 Registry/Allowlist/Capabilities/도구 노출 정합성
- T5 `NOT_APPLICABLE`과 실제 ID 누락 구분
- T6 캐시/버전 차이에 따른 잘못된 연결 부재
- T7 기존 이력 무변경, Job 재실행 없음
- T8 **LLM과 Agent의 판정 조건을 같은 명세로 비교** (Agent 관측 자체는 독립 검증 전까지 미확인 처리)

실패했으면 승인 범위에서 원인 기반 수정·재시험을 **최대 3회** 반복한다. 같은 증상으로 무작정 코드를 변경하지 말 것. 회귀시험 PASS는 실제 Agent 검증 PASS를 대신하지 못한다.

### 단계 D — 반영·증거 보존·재발 방지

1. 승인 범위가 충분한 경우에만 운영 반영하고, 필요한 추가 승인·재시작이 있다면 `STAGED/APPROVAL_REQUIRED`에서 중단하라.
2. **최종 근거 레코드**를 기존 승인된 MCP 작업 결과 저장 기능이 있을 때만 게시하라. 작업 키 `MCP-JOBLIST-ID-RECONCILIATION-20261107` 아래 최신 버전과 시험 범위, 원인 코드, 미해결 사항, 조회 가능한 결과 참조를 남겨라.
3. 작업 결과 게시 기능이 없거나 권한이 없다면 **게시 성공이라고 보고하지 말고** `EVIDENCE_NOT_PUBLISHED`로 표시하라. 신규 쓰기 API나 권한을 임의 생성하지 말라.
4. 앞으로 같은 오류가 반복되지 않도록 **신규 Job 등록 시 ID 조인 무결성 검사**와 기존 실패 사례 회귀시험을 자동 체크에 포함하라(수정 권한이 있을 때만).
5. 원천 코드, 실제 Run/Result 식별자, 인증정보, 내부 경로, 원시 로그 등은 승인된 경계 밖으로 출력하지 말라.

### LLM 최종 응답 — 숫자 7개만

- **A. LLM/Agent 대상 정합성:** `1=동일 2=불일치 확인 3=증거 부족`
- **B. ID 실패 원인:** `1=연결누락 2=타 Job 연결 3=도구/스키마 차이 4=캐시/조회범위 차이 5=기타 6=미확정`
- **C. 코드·설정 조치:** `1=수정완료 2=수정불필요 3=승인대기 4=실패/보류`
- **D. 고정 실패 사례 회귀시험:** `1=PASS 2=FAIL 3=미실행/근거부족`
- **E. 기존 Job 보호 시험:** `1=PASS 2=FAIL 3=미검증`
- **F. 운영 반영:** `1=확인 2=STAGED/승인대기 3=실패 4=미확인`
- **G. Agent가 읽을 결과 증거:** `1=MCP 게시·조회확인 2=미게시/조회불가 3=게시 여부 불명`

상세 증거는 MCP 작업 기록에 남긴다(지원·권한이 있을 경우). 숫자만 답변하고 내부 내용을 장문으로 출력하지 않는다.

---

## 3. 이후 Agent에 전달할 최종 독립 검증 프롬프트

> **LLM의 작업 종료 후 한 번만** 전달한다. LLM 결과 A~G를 다시 타이핑할 필요 없다. MCP 기록을 직접 조회한다.

```text
[MCP–Job-list 동일 증거 기반 최종 검증]

작업 키: MCP-JOBLIST-ID-RECONCILIATION-20261107

LLM과 Agent가 같은 Job/Run/Result 레코드를 검증했는지 확인하고,
읽기 전용 MCP로 다음을 검사하라.

1. 작업 키로 최신 증거·시험 결과·적용 상태 조회
2. 이전 FAIL 사례의 Job ID/Run ID/Result ID 연결 직접 재조회
3. 신규 Job과 기존 Job의 Catalog/Queue/Receipt/Result 조회 확인
4. Registry·도구·Capabilities 정상 여부 확인
5. LLM의 PASS 기준과 실제 Agent 관측이 같은지 비교
6. 해결되지 않은 불일치가 있으면 결과 기록(쓰기 기능이
   승인된 경우에만). 없으면 임의 기록했다고 보고하지 말 것

금지: Job 재실행, 코드 수정, 설정 변경, 권한 확대, 민감정보 출력.
기록이 없거나 읽을 수 없다면 성공으로 추정하지 말 것.

응답(숫자 6개만):
A 동일 Job/Run/Result 검증: 1=PASS 2=불일치 3=근거부족
B 신규 Job ID 정합성: 1=PASS 2=FAIL 3=미확인
C 기존 Job 호환성: 1=PASS 2=FAIL 3=미확인
D MCP 조회 기능: 1=PASS 2=FAIL 3=미확인
E 증거 게시·열람: 1=성공 2=실패 3=미확인
F 전체 E2E: 1=PASS 2=FAIL 3=미확인
```

## 4. 최종 판정 규칙

- **완료:** Agent 최종 응답 `1 1 1 1 1 1`이고, 대상은 기존 실패 사례를 포함하며, 승인 범위/실제 반영도 확인됨.
- **부분 복구:** 기존 Job/일부 MCP는 정상이지만 신규 Job ID FAIL 또는 증거 미확보.
- **차단:** 수정에 필요한 승인·권한·증거가 없으면 현재 상태를 유지하고 별도 승인/근거 확보를 요청.
- **재발 방지:** 다음 개선에서는 Job-list 단위 시험뿐 아니라 **동일 Job/Run/Result를 실제 조회하는 계약 시험**을 필수화.

## 5. 사용자가 할 일

1. **LLM에 이 MD의 2절을 한 번 전달** → 숫자 7개만 확인.
2. 완료되면 **Agent에 3절을 한 번 전달** → 숫자 6개만 확인.
3. 중간에 승인 요청이 발생하지 않는 한 추가 대화 없이 진행한다. 두 주체 간 자동 전달 기능은 현재 검증되지 않았으므로 자동 연결을 전제하지 않는다.
