# 사내 LLM 구현 지시서 v1.1 — 기존 코드분석 요청 유지, MCP 결과·근거 읽기 도구 추가

> **사내 LLM은 3,000자 제한이 없다.** 아래 지시를 생략하지 말고 전체 적용하라. 모바일 Agent의 출력만 짧게 할 것.

## 역할과 확정 요구사항

사내 Linux `whpark-mcp` 담당 개발자 관점에서 실제 소스를 검토하고 최소 변경을 구현·테스트하라.

**사용자 최신 사실:** 사내 Agent를 통한 **코드분석 요청은 이미 가능**하다. 문제는 **MCP에서 기존 분석 상태·결과·분석 근거를 읽는 도구가 노출되지 않았다**는 것이다. 현재 개선의 **P0 우선순위는 조회 도구**, 신규 submit/Runner 개발이 아니다.

자료: `HANDOFF_L1_MCP_Freeform_Code_Analysis_Remote_v1_1.md`, 설치된 `whpark-mcp` 소스, 실제 호출 중인 코드분석 도구/`code-analyzer`, `work-ledger-kernel v0.7.27`, `job-list v0.4.22`, 필요 시 `issue-analyzer v0.11.48`.

**검증되지 않은 사실:** 기존 코드분석 요청의 실제 MCP 함수명, 분석기 실행 계약, `analysis_id`, 결과 파일 경로와 포맷, 기존 Work의 Evidence 연동, MCP read API 등록 상태. 추정 이름으로 도구를 호출하거나 결과를 만들어내지 말 것.

## 1단계. 소스 실사 (무변경)

1. 기존 코드분석 요청이 실제 성공한 Agent 사용 시나리오를 확인하고, **호출 도구/Skill/Runner 이름, 입력·출력 스키마, 인증 주체, 반환 ID, 결과 저장 위치**를 역추적한다. 가급적 저장된 호출 기록으로 확인하고 이 단계에서 분석을 재실행하지 않는다.
2. `whpark-mcp`의 tool registration/router, tool list, ACL, 허용 저장소/경로, 실행/조회 권한, service lifecycle, token·출력 마스킹을 코드 파일/함수 근거로 기록한다. 기존 요청 tool 변경 필요성이 없다면 **변경하지 않는다**.
3. 설치된 `code-analyzer`의 보고서(JSON/MD/HTML/TXT 등), 작업 상태 파일, 분석 종료 시 생성물, commit/revision, 출처·근거 파일/함수/라인 기록 여부, TTL/보존, fallback 경로를 확인한다. 결과가 없는 것과 Reader가 없는 것을 구분한다.
4. `work-ledger-kernel v0.7.27`에서 실제 제공하는 `work-find`, `work-refs`, `brief_resume`, `diagnostic_resume`, `record.evidence_index`, Evidence SHA·confidence 읽기 계약을 확인한다. **읽기만 허용**, `context`·`record`·`docs-export`·Git Push·binding 변경 호출 금지. Ledger storage constructor가 root directory를 만들 수 있으므로 원장 미존재 시 순수 조회 부작용 검증이 필요하다.
5. `job-list v0.4.22`의 상태/observer와 분석기 결과의 연결을 검토한다. 기존 `job_core.py status`에 레이아웃 생성/복구 같은 동작이 있다면 MCP GET에서 사용하지 않는다.
6. SOC/Jira key↔Work ID↔analysis ID가 실제 어떤 형태로 연결되는지 확인한다. 직접 링크가 없으면 분명히 `UNLINKED`로 표시하고 임의 추론을 하지 않는다.
7. 결과로 **현존 도구, 필요한 새 READ 도구, 결과 format, 소스 경로·상태 확인, 인증 요구, 변경 파일 후보, 남은 차단 원인**을 표로 보고한다.

## 2단계. 최소 구현 설계

기존 MCP에 동일 기능의 안전한 read tool이 있으면 그것을 재사용하고, 없다면 아래 계약을 MCP 명명규칙으로 추가하라. 도구명은 *제안명*이고 실제 등록 후 확인해야 한다.

- `l1_analysis_find(query, kind, limit, cursor)` : SOC/Work 기반 과거 코드분석 task 후보 목록. 분석 실행 금지.
- `l1_analysis_status_read(analysis_id)` : 현재 stage/state/error/result_available. 호출해도 복구/큐 수정/로그 append 없음.
- `l1_analysis_result_read(analysis_id, section, cursor, max_chars)` : 기존 완료 artifact의 summary/cause/callflow/variables/evidence/next 분할 반환. 없는 섹션은 `NO_SECTION`.
- `l1_analysis_evidence_read(work_id, evidence_id, section, cursor, max_chars)` : Ledger에 실제 등록된 immutable Evidence를 scope/해시/상태 확인 후 제한된 범위로 반환. 원본 불허 시 메타정보만 반환.
- `l1_work_summary_read(work_ref, view)` : Work 요약·최근 결정·다음 행동·실제 연결된 분석 ID만 반환. 사내 TL_PRIVATE 데이터 비노출.
- `l1_code_excerpt_read(repo_alias, revision, relative_path, line_start, line_count, analysis_id)` : 코드 발췌가 별도 승인된 경우에만 P1 구현. pinned Git SHA/P4 changelist 기준, 범위 제한, repo alias allowlist, secret/경로 탈출 차단. Git/P4 checkout·write 금지.

**두 가지 읽기 경로를 구별**: (1) 분석 보고서 읽기 = 저장 artifact, (2) 코드 파일 읽기 = 승인된 SCM snapshot. 둘 중 하나의 기능을 다른 하나로 대체하지 말 것. 기존 보고서를 읽는 데 신규 코드분석 Runner를 재실행하지 말 것.

세션/호스트가 달라도 Work ID와 분석 ID가 보존되어야 한다. 다중 결과·중복 ID·다른 브랜치/commit·작업 중 결과·부분 실패를 고려한다. `list` 결과는 principal+scope filter, 안정적 pagination, 최소 정보만 제공.

## 3단계. 구현 세부 요건

### 결과 발견·읽기

1. 기존 submit 도구가 반환하는 정식 ID 우선 사용. 없다면 **실제 저장 artifact를 기반**으로 안전한 레거시 조회 ID를 설계(근거와 수명 명시).
2. Job 상태의 `SUCCESS`와 artifact 존재/내용 유효성은 분리. 결과 파일이 없으면 `RESULT_NOT_FOUND`, 처리 중이면 `RESULT_NOT_READY`.
3. 결과 본문은 section별 최대 크기 제한과 `next_cursor`; UTF-8 등 실제 인코딩 검증, Markdown·HTML은 텍스트로 안전하게 출력. 외부 템플릿·스크립트·명령을 실행하지 않는다.
4. 파일 변조 여부·가용성·mtime/digest 고정 확인. ledger evidence에는 index metadata의 sha256을 검증하고 `AUTO_CANDIDATE`와 `HUMAN_CONFIRMED`를 명확하게 표시한다.
5. 근거가 없으면 LLM이 소스 함수명/라인/값을 생성하지 않게 응답 스키마에 `evidence_status`와 `confidence`를 포함. 실제 분석과 Work 서술 기록을 혼동하지 않는다.

### 권한·보안

- 인증 principal → work owner/tenant/repo alias/analysis id/특정 evidence ACL에 따라 접근 검증.
- 결과 존재 자체가 민감할 수 있다. 타 사용자 ID는 존재여부 유출 방지 정책에 맞춰 거부.
- 임의 디렉터리 경로, 사용자 제공 절대 경로, 범용 shell 실행, URL fetch, 무제한 grep/ls/find/read_file 노출 금지.
- 코드 발췌는 분석 근거의 파일/줄/버전 참조와 결합하고, 과다 응답·secret 파일·symlink traversal·파일 경계 초과 차단.
- 원본 코드, SDM, 사내 비밀정보, token, 내부 절대 경로를 모바일에 무단 출력하지 않는다.
- MCP read tool에서 `work-ledger-kernel` record/journal/evidence/bindings 수정 불가. 기존 작업 큐·Git 상태 불변.

### 후속 자연어 UX

- `SOC-420517 분석 결과 알려줘` → 분석 후보/최신 실제 분석 결과 조회.
- `왜 main_dac_path와 tx_dac_path가 달라?` → 실제 cause/variables/evidence 근거만 답변.
- `그 코드 보여줘` → 승인된 snippet reader로 고정 SHA, 해당 범위만 읽기.
- `지난번 분석 다시 설명해줘` → 새 분석 0회.
- `추가 분석해줘` → 사용자 명시 요청시에만 **기존 submit 경로**를 호출하고 새 분석 ID를 받아 기존 기록과 구분.
- 다중 Work·불명확 analysis ID는 후속 선택을 요구하되 숫자 객관식으로 간단히.

## 4단계. 구현·테스트

사내 승인된 수정 범위에서 실제 코드 수정 및 테스트를 진행하라. 승인되지 않은 배포·MCP 재시작·실제 분석 재실행·실로그 변환·소스/Work 쓰기는 분리하여 승인받는다.

필수 테스트:

- READ 도구 등록 후 실제 Agent tool 목록 가시성.
- **기존 코드분석 요청 기능 회귀**(기존 경로가 그대로 동작할 것).
- 실제 기존 분석 artifact 찾기 → 섹션 분할 → 근거 조회.
- 존재하지 않는 Work/analysis/evidence, 작업 중/실패한 분석, 미연결 Evidence의 정확한 상태.
- 동일 결과 100회 반복 조회 시 queue/Runner/파일 생성/복구/Git/원장 mutation **0회**(전후 상태·digest 비교).
- 타 사용자·미허가 저장소·traversal·secret·줄범위·Git/P4 revision mismatch 방어.
- MCP 서비스 반영 후 caller principal/ACL, 도구 호출, restart/rollback 검증.
- `work-ledger-kernel`의 기존 immutable Evidence/Work metadata/old migration job 및 `job-list` 실행 이력 보존.
- Linux 실환경 PASS와 Windows NOT TESTED, mock PASS와 실분석 결과 READ PASS 구분.
- SDM fixture가 확보된 별도 승인 시에만 `run_plus_sdm_to_txt` → TXT → issue-analyzer E2E 검증.

## 5단계. 산출물 (상세 보고 허용)

1. **사내 실소스 조사 보고서**: 실제 tool/파일/함수 근거, 기존 request 흐름, reader 누락 지점, result/Evidence 저장 경로(대외 노출 금지).
2. 변경 설계: 요청/응답 JSON schema, access scopes, pagination, 오류코드/상태도, 데이터 소유권 및 파일/클래스별 수정 계획.
3. 수정 코드 및 회귀 테스트, mock/사내 real 검증 결과 구분.
4. 변경한 패키지만 version bump 후 패키징(날짜 suffix 없음), install/rollback 설명과 서비스 적용 절차. 소스 변경이 없는 `work-ledger-kernel` ZIP을 불필요하게 재배포하지 말 것.
5. 사내 Agent용 자연어 요청·조회·근거 읽기 예제 및 사용 전제.
6. 부족한 자료·권한은 `BLOCKER`로 명시하며 미구현 기능의 PASS 허위 보고 금지.

**사내 결과 보고는 길이 제한 없음.** 원인·파일/심볼·테스트 로그 위치·보안과 회귀 영향을 상세히 기술해라. 단, 사외 모바일 전달용 단축 보고는 다음과 같이 제한:

```text
REQUEST_EXISTING=1/2/3 READ_TOOL=1/2/3 RESULT_READ=1/2/3
EVIDENCE_READ=1/2/3 CODE_EXCERPT=1/2/3 WORK_LINK=1/2/3
READ_ONLY=1/2/3 SDM_E2E=1/2/3 BLOCKER=... NEXT=...
```

**마지막 핵심:** 기존 코드분석 요청을 고치려 하지 말고, **그 요청이 생성한 결과를 MCP를 통해 안정적으로 검색·읽고, 원인 근거를 재분석 없이 확인하는 기능**을 우선 완성하라.
