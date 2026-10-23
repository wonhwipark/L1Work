# 사내 OpenCode CLI / LLM 실행용 원샷 프롬프트 — MSC 접근·라우팅·Evidence 복구

- 버전: v1.1 / 2026-10-23
- 우선순위: P0 — **기존 Work MSC 조회만 정상화**
- 대상 Work: `20261007-SOC-411668` (Jira `SOC-411668`)
- 실행 위치: 사내 Linux PC의 **실제 권한 있는 OpenCode CLI / 사내 LLM**
- 범위: `Agent → whpark-mcp → 기존 Wrapper/Runner → l1-fix-workflow CLI → work-ledger-kernel → Evidence`의 장애 위치 확인, 사용자 소유·허용 범위 내 최소 복구, 실제 E2E 검증
- 기준 코드: 제공된 `l1-fix-workflow v1.6.45` (단, **실제 설치본/호출본 버전을 우선 확인**)
- 참고 설계: `HANDOFF_L1_Workflow_MSC_VIEW_TL_Summary_Weekly_Final_Fix_v1_0.md`의 **A. MSC_VIEW / P0**
- 이번 작업 제외: TL Summary·주간보고 구현, SDM 파서 연동, Code Analyzer 재분석, MSC 신규 생성·업로드

---

## 사내 LLM에 전달할 실행 지시 (전체를 한 번에 실행)

당신은 사내 개인 MCP(`whpark-mcp`) 및 L1 Workflow MSC 조회 실행 경로를 진단·복구하는 엔지니어다. **아래 작업을 처음부터 끝까지 연속 수행**하라. 수동으로 이미 수행된 숫자 진단을 반복하지 말고, 실제 실행 근거를 확보하라. 프롬프트 글자 수 제한은 없다. 다만 사외 사용자에게 전달할 최종 결과는 **숫자 6개**로 제한한다.

### 0. 목적과 판정 기준

**목표:** Agent에 `20261007-SOC-411668 MSC 보여줘`를 요청했을 때 이미 Work에 저장된 검증 가능한 MSC 원본을 **Phase별 `A → B : API/Message`, alt/else/loop, Note 흐름**으로 Agent 본문에서 조회하도록 만든다. 읽기 전용 조회이며 코드 분석, 새 MSC 생성, Work 변경, 승인 요청의 대리 수행이 아니다.

다음은 성공이 아니다: `view=brief` 응답, Evidence ID만 표시, 메시지 수만 표시, `.svg`/`render_output`만 표시, CLI exit code 0, 테스트 fixture만 PASS, `SKILL_NOT_FOUND`가 사라진 상태만 확인, `tl_summary_status=READY`.

**완료는 실제 Work의 Agent 경유 조회에서 `MSC_VIEW_READ_ONLY`, `ok=true`, `provider_executed=false`, `user_summary`에 검증된 원본의 실제 메시지 흐름이 포함될 때만 인정**한다. Agent 자체가 제공되지 않거나 인증·접근 권한이 부족하면 실제 E2E를 미검증/차단으로 기록한다.

### 1. 출발점: 이미 확인된 사실과 아직 모르는 사실

**코드 확인 사실(배포 ZIP v1.6.45):**

- `l1_fix_workflow/cli.py`에는 `resume --view {brief,diagnostic,msc}`가 있고, 기본값은 `brief`다. `resume --mode context --view msc`가 별도 `view_work_msc()` 분기로 들어간다.
- `l1_fix_workflow/msc_view.py`는 정확한 Work의 `asis_msc`/`hld_msc` Evidence를 선택하고, Work-local `evidence/` 아래 경로·symlink·파일 크기·SHA-256을 확인한 뒤 `.puml`, fenced PlantUML `.md/.txt`, 특정 Converter JSON을 Flow 텍스트로 투영한다.
- 읽기 전용 구현은 분석 Provider를 호출하지 않는다.
- 기본 출력 길이 제한이 있고, **현재 배포 CLI에 `--detail`이나 `--page` 옵션이 있다고 가정하지 말 것**. 반드시 설치본 `--help`로 확인한다.

**사내 사용자 보고/핸드오프:**

- Agent에서 MSC를 요청했으나 `view=brief`가 반환되거나 원본 접근 실패가 보고됐다.
- 메타데이터 수준에서 `asis_msc` 두 건(`E-a938171c8c87`, `E-562d100a45b9`)과 `render_output` 두 건(`E-ce98f79d48da`, `E-0b8425828a34`)이 확인됐다고 보고됐다.
- 이전 숫자 진단은 경로·권한 차단을 가리켰으나 **실제 CLI와 MCP 경유 실행의 차단 지점은 확정되지 않았다**.
- 과거 `SKILL_NOT_FOUND`가 제시한 `/home/whpark/l1sw-private-skills/l1-fix-workflow`는 **실패한 Runner가 기대한 경로**일 뿐, 진짜 설치 경로라고 단정할 근거가 없다.

실제 현장 결과로 이 보고를 독립 검증하라. 원인으로 이미 확정됐다고 가정하지 말라.

### 2. 실행 전 불변조건·보호 범위

1. 사내 보안 정책과 기존 allowlist를 준수한다. 접근 제어 우회, sudo/ACL/chmod/chown 변경, 타 사용자 경로 탐색, 비밀값 출력, 승인되지 않은 외부 전송 금지.
2. **기존 Work, Ledger/Journal, Evidence 원본과 SHA, Git/P4 저장소, GitHub/Jira/Confluence, Work focus 및 분석 상태를 수정하지 않는다.** Read-only 조회만 수행한다.
3. 자동 수정은 **사용자 소유의 기존 `whpark-mcp` 설정·Runner 경로·인자 매핑 중 이미 정책상 허용된 항목**에 한정한다. 수정 전 사용자 소유 위치에 백업과 digest를 남기며, 실패 시 원복한다. 기존 인가 범위를 확장하거나 새 임의 Runner를 만들어 우회하지 않는다.
4. Workflow 스킬 소스 변경, 공용 스킬 설치, Kernel 스키마/Guard 수정, MSC Evidence 재연결/재등록/복구, 권한 부여가 필요하다고 판단되면 **해당 단계는 변경하지 말고 `APPROVAL_OR_IMPLEMENTATION_REQUIRED`로 분리 보고**한다. 다른 허용된 진단은 계속 수행한다.
5. `/home/whpark/Project/smp1900` 등 코드 저장소를 Work Evidence 탐색 대용으로 사용하거나 worktree를 생성하지 않는다. `code-analyzer`, `doc-converter`, 로그 분석기를 실행하지 않는다.
6. 확인을 위한 테스트 로그·임시 결과는 보안 정책이 허용한 사용자 개인 진단 디렉터리에만 보관하고, Work 경로나 외부 저장소에 자동 저장하지 않는다. 민감한 본문 대신 status/경로 분류/해시/호출 trace만 남긴다.

### 3. S0 — 동일 실행 환경과 실제 설치본 식별

사내에서 실제로 **Agent가 호출하는 동일 MCP 서버/Runner**와 **OpenCode CLI 프로세스**를 식별한다.

- 개인 MCP의 서비스 실행 주체(user/euid/gid), 현재 작업 디렉터리, Python/CLI 실행 파일, `PATH` 등 **필요 최소 환경 차이**, MCP allowlist·도구 등록 상태, 기존 Wrapper의 action과 인자 schema 확인.
- `skill-updater`의 설치 성공 표시만 믿지 말고, Agent→MCP가 **실제로 호출하는 스킬 entrypoint**와 그 `--version`/`--help`/설치 manifest를 대조한다.
- 실제 설치된 `l1-fix-workflow`에 `resume --view msc`가 노출되는지 검사. ZIP의 동일 코드인지 revision/manifest/digest가 있으면 비교. 여러 설치본의 혼선(stale shim, 실행 PATH 우선순위, 잘못된 current directory)을 구분.
- `/home/whpark/l1sw-private-skills/l1-fix-workflow`는 과거 오류의 관찰값으로만 다루고, 유효 설치 위치는 등록된 configuration/manifest/실행 trace로 확인한다.
- `work-ledger-kernel` 실제 읽기 API 버전/ledger-root를 확인하되 Work를 새로 생성하거나 focus를 바꾸지 않는다.

**산출물:** 실행 주체·호출 entrypoint·실효 버전·MCP 등록/allowlist·설치본 불일치 여부. 확인 불가 항목은 UNKNOWN.

### 4. S1 — CLI 직접 조회 / Agent→MCP 경유 조회의 차이 분리

먼저 **실제 설치본에서 도움말로 확인한 동일한 인자**를 사용해 정확한 Work로 아래 두 read-only 경로를 각각 수행한다.

- CLI 직접 실행: `resume --work-id 20261007-SOC-411668 --mode context --view msc`
- 자연어 분류 대조: `plan --read-only '20261007-SOC-411668 MSC 보여줘'`

위는 **서브커맨드 이하 인자 예시**다. 앞에 붙는 실제 launcher, `--ledger-root`, `--kernel-path` 등의 전역 인자·Python module 경로는 설치 manifest/`--help`에서 확인된 값으로만 구성한다. 임의 경로 추측 금지.

각 요청에서 다음을 기록한다: `action`, `ok`, `view` 또는 실효 view, `work_id`, `evidence_id`, `phase_count`, `message_count`, `user_summary`의 Flow 유무, `read_only`, `provider_executed`, 반환 오류 유형. **CLI 프로세스 종료 코드 0만으로 성공 취급 금지**.

그다음 기존 사내 Agent에서 동일 Work의 `MSC 보여줘`를 호출하여 실제 MCP 도구 요청의 **typed `view=msc` → Wrapper 매핑 → CLI argv → 반환 JSON → Agent 표시 본문**을 단계별로 비교한다. 파라미터가 누락되어 `brief`가 기본값으로 적용됐는지, 구버전 CLI가 호출됐는지, Wrapper가 `user_summary` 대신 일반 TL 요약을 노출했는지 분리한다.

- CLI 성공 / Agent 실패 = MCP 라우팅·arg 전달·응답 표시 문제 우선.
- CLI 실패 / Agent 실패 = Evidence 접근·정확 Work 식별·Kernel 사용·실행 환경 문제 우선.
- CLI도 `brief` = 실제 설치 버전·CLI 명령 구성·잘못된 진입점부터 확인.
- CLI 성공 / Agent 검사 불가 = **CLI만 검증, Agent E2E 미완료**로 표시.

### 5. S2 — 해당 Work의 Evidence 실체와 안전한 접근 확인

정확한 Work `20261007-SOC-411668`의 Work Ledger API를 통해 `evidence_index`를 **읽기만** 수행한다. 동일 Jira 번호를 가진 다른 Work를 병합·임의 선택하지 않는다.

1. 위의 두 `asis_msc` Evidence ID 및 `hld_msc`가 있으면 함께, 현재 `kind`, 등록 순서/버전, `path`, `sha256`, `code_rev` 존재 여부를 확인한다. **메타데이터의 존재는 파일 존재/SHA 정상과 별개**임을 지킨다.
2. Work-local 등록 경로만 확인한다. 실제 소유 사용자/실행 계정이 각 상위 디렉터리를 통과할 수 있는지, 파일을 읽을 수 있는지, symlink/경로 탈출이 있는지 비파괴적으로 확인한다.
3. 파일 존재·접근 가능·크기·SHA256 일치·지원 원본(`.puml`, fenced `.md/.txt`, 지원 Converter Spec JSON)·파서 Flow 추출을 각각 별도로 기록한다.
4. `render_output`의 `.svg`나 `MSC_VIEW.md`, 기존 AS-IS 15건/TO-BE 17건 요약 숫자만으로 메시지 API를 재구성하지 않는다. 실제 원본을 찾지 못하면 `MSC_CANONICAL_PUML_REQUIRED` 또는 `MSC_SOURCE_UNAVAILABLE`로 분류한다.
5. AS-IS/TO-BE 식별·선택은 실제 메타데이터에 근거한다. 최신 Evidence가 실패하고 과거 것을 읽으면 **OLDER_VERSION/STALE 표기를 명시**하며 최신을 읽은 것처럼 보고하지 않는다.
6. 예전 보고의 ‘원본 SHA 정상’은 어느 정확한 Evidence에 대해, 어느 호스트·계정에서 확인한 것인지 증명되지 않았다면 미확정으로 취급한다.

### 6. S3 — 원인 확정·허용된 범위 내 최소 복구

원인을 다음 **서로 독립적인 층**으로 귀속하라. 둘 이상이면 복합 원인으로 처리한다.

A. MCP/Agent 자연어 라우팅 또는 `view` 인자 전달 누락 (`MSC_ROUTE_NOT_APPLIED`)
B. 서로 다른 스킬 설치본/실행 entrypoint/Runner 등록 불일치 (`SKILL_ENTRYPOINT_MISMATCH`)
C. 실제 실행 계정·작업 디렉터리·등록 ledger-root·파일 읽기 권한·허용 경로 불일치 (`MSC_FILE_UNAVAILABLE` 등)
D. Evidence 메타데이터만 존재, 원본 손실, SHA 불일치, 지원되지 않는 source, Flow 추출 실패 (`MSC_SOURCE_UNAVAILABLE` / `EVIDENCE_INTEGRITY_UNVERIFIED` / `MSC_CANONICAL_PUML_REQUIRED` / 실제 코드 오류)
E. 원인 미확정 또는 둘 이상

**복구 원칙:**

- 허용된 기존 개인 MCP 설정의 경로 오기·인자 누락·환경변수 전달 오류는 실제 근거를 확인한 뒤 변경 전 백업, 최소 수정, config validation, 재기동 필요 여부 확인, 재시험 순으로 진행한다. 이미 허용된 `view` 값을 올바르게 전달하는 것은 가능하지만 허용되지 않은 옵션을 억지로 통과시키거나 정책을 변경하지 않는다.
- CLI에서 버전이 뒤섞인 경우 설치된 승인 버전과 등록 entrypoint의 정합성만 맞춘다. 무단 패키지 업데이트·파일 복사·실행 권한 변경 금지.
- 파일이 존재하지만 회사 정책상 접근 권한이 없다면 ACL을 바꾸지 말고 소유자/보안 담당자 승인 필요로 보고한다.
- canonical MSC 원본 자체가 없거나 손상됐으면 **설정 변경으로 해결된다고 주장하지 않는다**. Evidence 복구/재등록은 별도 승인 필요.
- v1.6.45 Workflow 코드 자체의 결함이 증명됐다면 함수/테스트/재현 조건을 남기고 별도 구현 트랙으로 이관한다. **이번 작업에서 Workflow/Kernel 소스를 임의 수정하지 않는다.**
- 개인 MCP 변경 후 이상/회귀 확인 시 백업으로 즉시 원복하고 실패 사유 분류.

### 7. S4 — 실제 E2E 재검증 및 회귀 Gate

복구가 가능한 경우 반드시 **동일 실제 Work**를 대상으로 순서대로 검증한다.

**MSC 성공 Gate**

1. CLI `resume ... --view msc`가 정상 호출되고 결과의 `action=MSC_VIEW_READ_ONLY`, `ok=true`.
2. 검증된 원본에서 실제 한 개 이상의 `A → B : API/Message`가 추출되고, 실제 Phase/분기·Note가 있다면 원본과 동일한 순서로 표시. 전체 메시지 수는 파싱 결과 기준이며 과거 캡처 숫자 15/17을 그대로 재사용 금지.
3. Agent 경유에서도 **effective MSC view**가 유지되고 `brief`로 떨어지지 않으며, `user_summary`에 실제 Flow가 표시.
4. 읽기 전용 플래그, `provider_executed=false`, `code_analysis_executed=false`, `converter_executed=false`. Work/Journal/Evidence/Repo의 전후 무결성 동일.
5. MSC가 길어 잘릴 때 `display_truncated`를 확인하며, 원본 일부만 보이는 결과를 완전 조회라고 주장하지 않는다. 현재 CLI에서 paging 미지원이면 **별도 코드 개선 필요**로 분리하되 핵심 조회 여부는 따로 판정한다.

**부정/회귀 Gate**

- MSC 요청인데 `view=brief`면 FAIL.
- `.svg`만 있고 canonical source 없으면 안전하게 차단되고 임의 Flow 생성 0.
- SHA 불일치, `../` 경로, symlink 이탈은 차단되어야 한다.
- 정확한 Work ID를 주면 다른 Jira Work를 합치지 않아야 한다.
- 기존 `resume --view brief`, `diagnostic`는 기존 동작 유지.
- read-only MSC 조회는 BUG `ANALYSIS_EVIDENCE_REQUIRED`를 우회하거나 분석 작업을 시작하지 않아야 한다.
- 기존 코드분석·로그분석 provider 전체 실행은 금지하며, 변경된 MCP 라우트·설정에 의존하는 일반 smoke만 가능한 범위에서 수행한다.
- 개인 MCP 설정 변경 전에 측정한 baseline과 동일 환경에서 비교하고, 기존에 있던 실패를 신규 회귀라고 허위 보고하지 않는다.

**테스트 범위 분리:** fixture PASS, 설치본 CLI PASS, **실제 Work CLI PASS**, **실제 Agent/MCP PASS**는 별도 상태다. 마지막 항목이 없으면 E2E 완료라고 말하지 않는다.

### 8. S5 — 현장 보고와 후속 구분

사내에서 내부적으로 확인할 수 있는 **간결한 검증 보고서**를 제공하라. 보안 정책상 허용된 경우에만 개인 작업영역에 결과를 보존하며 Work/원본은 건드리지 않는다.

보고서 내용: 실제 호출한 entrypoint와 확인된 버전(민감 경로는 마스킹), CLI 대 MCP의 route/argv 유무, 검사한 Evidence ID별 `metadata/file/access/sha/parser` 결과, 변경한 사용자 소유 설정 키(민감 값 제외), 백업/원복 여부, 실제 MSC Phase/Message 개수, 사전·사후 상태, 회귀, 미해결 승인·구현 과제. 사내 코드·로그·원본 PlantUML 전체를 외부로 출력하거나 복사하지 않는다.

**최종 Agent 사용자 응답은 아래 Q1~Q6 숫자 6개만 한 줄로 반환**하라. 각 문항은 실제 검증 근거에서 선택하고 예시 숫자를 복사하지 마라. 사내 상세 보고서는 사용자 사외 재타이핑이 필요하지 않도록 한다.

- **Q1 주된 장애층:** 1 라우팅/인자 / 2 설치본·Runner / 3 경로·접근권한 / 4 Evidence 원본·무결성 / 5 복합·미확정
- **Q2 직접 CLI의 실제 Work MSC 조회:** 1 Flow 성공 / 2 MSC 실패·brief / 3 CLI 실행 불가·미검증
- **Q3 Agent→MCP 실제 Work MSC 조회:** 1 Flow 성공 / 2 brief 오분류 / 3 실행·원본·응답 실패 / 4 실행 권한 없어 미검증
- **Q4 canonical MSC Evidence:** 1 등록 원본 파일·SHA·파싱 검증 / 2 메타데이터만 확인 / 3 원본 존재하나 접근 차단 / 4 원본 부재·SHA/형식 오류 / 5 미확인
- **Q5 복구 상태:** 1 허용 설정 최소 수정·재검증 성공 / 2 수정 불필요(기존 정상) / 3 추가 승인·스킬 구현 필요 / 4 수정 실패·원복
- **Q6 보호·회귀:** 1 PASS(Work/Evidence 무쓰기·기존 동작 유지) / 2 FAIL / 3 미검증

**형식:** `Q1 Q2 Q3 Q4 Q5 Q6` 순서로 공백 구분 숫자만. 예: `5 2 3 2 3 1`은 형식 예시일 뿐 진단 결과가 아니다. 근거 불충분 시 반드시 미확정·미검증 선택을 사용할 것.

### 9. 종료 기준과 범위 밖 후속 작업

- **완료:** 실제 Work에서 사내 Agent→MCP→Workflow CLI→canonical MSC Evidence→Phase/Message Flow가 한 번에 정상 출력되고, read-only·회귀 Gate를 통과.
- **부분 완료:** CLI 직접 성공이나 Agent 경유 실패/미검증. 이 경우 Wrapper 계약/Agent 표시 경로 작업만 별도 이관.
- **차단:** 회사 접근 승인, canonical Evidence 복구·재등록, Workflow 자체 수정 필요. 승인 없이 임의 조치하지 않으며, 필요한 담당/정확 차단 계층을 보고.
- **이번 요청의 외부 작업 제외:** TL 한눈에 보기와 주간보고 개선은 핸드오프 문서의 P1 트랙에서 추후 독립 구현. `issue-analyzer`의 SDM 파서는 별도 설계·구현 작업창에서 처리.

추가 주관식 질문이나 다회차 진단은 하지 말고 허용된 확인·복구·재검증을 한 차례에 이어서 마무리하라.
