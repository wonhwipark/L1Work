# 업무 GPT 인계 — 모바일 Agent의 기존 L1 업무 스킬 접근을 위한 Linux MCP 기능 연결

- 문서: r0002 / 2026-11-20 KST
- 전달 위치: `wonhwipark/L1Work` / `main` / `handoffs/L1_MCP_AGENT_SKILL_ACCESS_AND_CAPABILITY_HANDOFF_r0002_20261120_KST.md`
- 대상: 기존 Linux MCP(`whpark-mcp`로 알려진 프로젝트), 업무 GPT, 허용된 실행 LLM/로컬 Agent
- 목적: **Viewer 접근 진단이 아닌, 기존 L1 업무 스킬의 기능을 모바일 Agent가 실제로 조회·요청·결과 확인할 수 있도록 연결**
- 상태: **설계/현장 확인 요청서**. 이 문서의 게시만으로 MCP 확장·호스트 설치·서비스 재시작·스킬 실행·Job 등록·Knowledge 게시가 일어나지 않음. 실제 호출 가능 여부는 업무 호스트에서 검증 필요.

## 1. 사용자 결정과 기존 인계의 범위 정정

설계 GPT가 L1 스킬의 책임·입출력·연계 방향을 정리하고, 업무 GPT가 실제 실행 환경의 설치본·MCP 도구·호출 계약을 대조한 뒤 필요한 연결을 구현·검증하는 협업 흐름이 목적이다. 모바일 Agent는 사용자 자연어 요청을 Linux MCP의 **실제로 등록되고 권한이 허용된 기능**으로 전달한다.

기존 [MCP 읽기 진단/Viewer Probe r0001](L1_MCP_AGENT_READONLY_CAPABILITY_AND_VIEWER_PROBE_HANDOFF_r0001_20261120_KST.md)은 Viewer 설치·API·MSC 화면 진단을 중심으로 작성되어 MCP의 상시 업무 경로로 오해될 수 있었다. **이번 r0002가 MCP의 업무 스킬 접근 목적에 대한 최신 지시**이며, 그 범위에서 r0001보다 우선한다. 기존 문서와 시험/결과는 이력으로 보존하고 재작성·삭제하지 않는다.

[Viewer UI 변경 인계 r0002](L1_WORKSPACE_VIEWER_UI_CHANGE_AND_MCP_VALIDATION_HANDOFF_r0002_20261120_KST.md)는 **별도 웹 UI 개발/검증 작업**으로 유지한다. 이번 MCP 기능 연결의 선행 조건·완료 조건에 Viewer API 연결, 브라우저 렌더링, MSC 화면 검증을 넣지 않는다. Viewer의 별도 개선을 중지·완료 처리한다는 뜻도 아니다.

### 경로 분리

```text
[업무 요청·결과]
사용자 → 모바일 Agent → Linux MCP → 기존 업무 도구/스킬의 허용된 호출 인터페이스
                                      ├─ l1-fix-workflow → work-ledger-kernel → Work/Evidence
                                      ├─ code-analyzer / issue-analyzer → 코드·이슈 분석 기능
                                      ├─ l1-knowledge-updater → 개인 분석·후보/Preview
                                      ├─ l1sw-dev-knowledge → 승인된 그룹 지식 조회
                                      ├─ l1-github / P4 조회 도구 → revision·이력 근거
                                      └─ job-list / 승인 Runner → 실행·영수증/결과 (승인 시)

[별도 사용자 UI]
사용자 → 웹 브라우저 → Viewer → 허용된 Work/Knowledge 문서·MSC 표시
```

이 그림은 **설계상 역할/후보 경로**다. 해당 MCP 도구가 이미 등록·실행 가능하거나 각 스킬에 원격 callable API가 있다는 증거는 아니다. 실제 `l1-workspace`, `l1sw-dev-knowledge`의 저장/호스트/권한은 업무 환경의 계약으로 확인하며 동명 GitHub.com 저장소를 정본으로 가정하지 않는다.

## 2. 업무 GPT에 요청하는 우선 작업: 기존 기능 실측

새 MCP 서버·조회 엔진·스킬별 재구현부터 시작하지 않는다. 기존 업무 Work와 진단 결과를 재사용하고 다음을 한 번에 읽기 조사한다.

1. **동일 대상 확인:** 실제 MCP 서비스 등록 저장소·브랜치/revision, 소스·실행 호스트, 대상 호스트 라우팅·호출 identity/권한을 대조한다. Agent 컨테이너의 로컬 상태를 대상 호스트 증거로 대체하지 않는다.
2. **노출 도구 확인:** Agent가 검색·호출 가능한 현재 MCP tool 이름/설명/input-output schema/READ·PLAN·EXECUTE 권한, 오류 계약, 예산·timeout·감사·승인 게이트를 확인한다. 없는 tool 이름·API·CLI·필드를 만들어 쓰지 않는다.
3. **스킬/실행기 대조:** 아래 기능별로 공개 ZIP 존재, 실제 설치 manifest, 실행 프로세스 로드 버전, 호출 가능한 CLI/함수/서비스·Job/Runner·현행 writer를 별도 확인한다. 스킬 문서에 기능이 적혀 있어도 MCP 호출 보장은 아니다.
4. **기존 연결 재사용:** 사용 가능한 Work 조회, Knowledge 검색, Work/Job 결과·영수증 조회, 기존 공통 Workflow/Kernel/Updater/Git/P4 연계부터 매핑한다. 실제 미지원만 `REUSE / CONNECT / 최소 EXTEND / DEFER`로 분류한다.
5. **관측의 의미 구분:** 이전 Agent 조회에서 `LOCAL_FALLBACK`, Provider 미호출, 모듈 라이브러리 `LIBRARY_NOT_CONFIGURED` 사례가 보고되었다. 일반 문서 검색 결과와 Provider/모듈 라이브러리 구성, 개인 문서 읽기, 실제 호스트 로드·실호출은 별개다. 재확인 전 현재도 동일하다고 단정하지 않는다.

읽기 확인이 불가능한 구간은 `NOT_VERIFIED`/`BLOCKED`와 이유를 남기고, 확인된 기존 계약으로 나머지 설계·격리 시험을 계속한다. 사용자에게 운영 스킬 ZIP·manifest·회사 소스/로그 원문을 대신 전달해 달라고 요청하지 않는다.

## 3. 기능별 MCP 연결 우선순위

| 우선 | 사용자가 모바일 Agent에 요청할 실제 용례 | 연결 대상과 업무 책임 | 첫 단계/경계 |
|---|---|---|---|
| P0 | “진행 중인 Work와 마지막 판정·다음 조치를 보여줘” | `l1-fix-workflow` + `work-ledger-kernel` | 기존 Work/Evidence 조회·revision/상태 요약. 새 Work 생성/수정과 구분 |
| P0 | “특정 모듈의 검증된 지식·문서를 찾아줘” | `l1sw-dev-knowledge`, 허용된 개인/그룹 Knowledge 조회 제공자 | source_scope·권한·revision·Provider vs fallback 확인. 검색 hit와 실제 본문 읽기 분리 |
| P0 | “지금 어떤 분석 도구를 사용할 수 있고, 마지막 Job이 어디까지 갔어?” | Linux MCP capability, `job-list`, `skill-updater` 상태, 기존 결과/영수증 도구 | 등록/권한/설치/로드/결과 조회. Job DONE만으로 분석 성공 판정 금지 |
| P1 | “이 블록/파일의 현재 동작을 코드 기준으로 분석해줘” | `code-analyzer` + 필요한 `l1-github`/P4 근거 | 고정 source revision·범위·승인된 분석 실행 경로 확인. 분석/LLM·산출물 생성은 단순 READ probe 아님 |
| P1 | “이 블록의 Procedure/Feature를 스터디하고 Knowledge 후보를 보여줘” | `l1-knowledge-updater` + `code-analyzer` + `doc-converter` + Workflow/Kernel | Updater 직접 진입과 기존 Work 진입 구분. 개인 Work에 분석·초안·Evidence 보존 → 후보/중복 대조/Preview. 그룹 게시 별도 승인 |
| P1 | “이슈 원인과 관련 CL/PR을 조사해줘” | `issue-analyzer`, `code-analyzer`, `p4-code-owner`, `l1-github` | 근거 수집 READ와 LLM 분석 실행·결과 저장 분리. 변경·submit 없음 |
| P2 | “기존 승인된 분석 요청을 실행하고 결과를 확인해줘” | 기존 `job-list`/Runner, 필요할 때 `skill-updater` | 등록·설치·활성·실행·영수증·완료를 단계별 검증. 유효 승인 없이 enqueue/retry/재호출 금지 |

스킬의 실제 이름/실행 인터페이스는 현장 원문을 우선한다. 표는 최소 연결 대상의 탐색 순서이며 모든 기능의 즉시 노출을 지시하지 않는다. 코드/이슈 분석이나 Updater ‘스터디’는 모델 비용·출력 파일·Workspace 갱신이 수반될 수 있으므로 **조회 도구가 존재한다는 이유로 자동 실행하지 않는다**.

## 4. 요청→응답 계약과 권한 경계

- Agent의 자연어 요청을 **지원 기능 발견 → 입력 scope/revision 검증 → 권한/승인 확인 → 기존 provider 호출 → Work/Job/Evidence 근거 포함 결과 반환** 순서로 연결한다.
- MCP는 **기존 스킬의 공통 호출·상태 조회 경계**이지 각 스킬 엔진을 복제하는 신규 아키텍처가 아니다. 처음부터 범용 shell/임의 filesystem·URL 실행, 자유 형식 코드 패치, 자동 Knowledge writer를 추가하지 않는다.
- 읽기 전용 상태/검색과, 스킬 실행(코드 분석·문서 변환·LLM/Job·Work 원본 변경), 코드 수정·지식 게시·설치·서비스 설정을 구분한다. 실제 기존 승인 범위 안에서만 실행하고 범위 밖 항목은 별도 승인 대상으로 반환한다.
- 허용된 식별자/상태/비민감 요약만 모바일 응답에 포함한다. 회사 코드·상세 MSC·로그·고객자료·토큰·절대 경로 등 제한 원본을 공개 저장소·Agent 응답·로그에 자동 복사하지 않는다.
- `PASS / FAIL / SKIP / NOT_RUN` 시험 판정, `UNKNOWN/NOT_VERIFIED/BLOCKED` 관측 상태와 시각·대상·원인을 명확히 유지한다. FALLBACK/합성 결과, 설치/로드, 검색 hit/본문, Job 성공/실제 분석, Preview/게시/readback을 혼합하지 않는다.
- 현행 스킬에서 직접 호출이 어려우면 허용된 기존 Job/Runner·Workflow/Updater 호출을 **CONNECT**하고, 입증된 공백만 좁은 tool/adaptor로 **EXTEND**한다. 스키마/DB/원장/권한 모델의 중복 확장은 요구하지 않는다.
- 현재 별도 진행 중인 `l1-channel-recovery` 분석 개선의 범위·우선순위를 자동 변경하거나 그 Workspace 연동을 선행 조건으로 만들지 않는다.

## 5. 단계적 개발·시험 요청

**G0 — 읽기 실측/기능 매핑:** 등록 tool, 호스트 identity, 설치·로드, provider/Runner/권한·상태 조회 계약을 확인한다. 기능별 지원/부분 지원/미지원/미확인을 분리한 표와 실제 입력·응답의 안전한 요약을 만든다.

**G1 — 최소 연결 설계:** P0부터 기존 기능 재사용/adapter 연결/입증된 결손 최소 개발을 확정한다. 각 동작의 required input, source revision·Work ID, 제한 권한, 결과와 reason code, timeout/size/개수 상한, 멱등성·중복 방지·rollback을 기존 계약에 맞춘다.

**G2 — 허용된 개발/격리 시험:** 중복 tool 등록, 권한 없음, 잘못된 ID·경로 탈출, 미연결 provider, 대상 호스트 불일치, timeout/부분 응답, stale revision, 개인정보/비밀 누출, 모델/Job 이중 실행 0을 회귀 시험한다. 자체시험과 독립 리뷰는 분리 기록한다.

**G3 — 실호스트/Agent E2E:** 유효한 호스트 적용 승인 후 P0 대표 세 요청(Work 검색·Knowledge 검색/본문·capability/Job 상태)을 Agent가 실제 MCP를 통해 호출하고 응답을 받는지 확인한다. P1의 코드 분석/Knowledge 후보 생성은 **별도 실행 승인과 고정 입력**이 확인된 경우에만 대표 한 건으로 검증한다. 설치·재시작·실제 그룹 게시 등 범위 밖 단계는 `BLOCKED/NOT_RUN`으로 남긴다.

**수락 기준:** P0는 실제 대상 동일성, tool 발견, 기존 원천 조회, 권한·revision·reason code, 모바일 응답을 각각 증명해야 한다. 특정 기능이 차단됐다면 차단 자체를 명확히 보고하고 다른 기능의 PASS를 전체 PASS로 확대하지 않는다. P1/P2가 아직 미검증이어도 G0/G1/격리 시험 진행을 막지 않는다.

## 6. 업무 GPT의 결과 보고 형식

| 항목 | 요구 결과 |
|---|---|
| 대상 | 실제 MCP 소스/브랜치/revision, 검증한 실행/관측 호스트와 시간 |
| 기능 매핑 | 요청별 기존 tool/스킬/Provider·호출 방식·필요 권한, REUSE/CONNECT/EXTEND/DEFER |
| 구현 | 변경 파일·공통 adapter 여부·입력 고정·안전 제한·rollback |
| 시험 | 합성·개발 자체·MCP 연결·Agent E2E·독립 리뷰를 각각 PASS/FAIL/SKIP/NOT_RUN |
| 상태 | 공개 패키지/설치/로드·실호출·Job 결과·Knowledge Preview/게시와 근거를 분리 |
| 제약 | 미검증/차단 원인, 현장에만 남긴 근거, 필요한 승인, 다음 한 행동 |

실행 상세·회사 제한 자료는 업무 Work/Evidence의 기존 허용 저장 경로에 보존한다. 공개 회신은 제한 범위를 넘지 않는 판정과 참조만 사용한다. 업무 GPT가 직접 접근할 수 없는 부분은 허용된 로컬 Agent가 실측하도록 연결하되, 실제 호출하지 않은 결과를 성공으로 쓰지 않는다.

## 7. 업무 GPT가 바로 적용할 지시

> `wonhwipark/L1Work`의 `main`, `handoffs/L1_MCP_AGENT_SKILL_ACCESS_AND_CAPABILITY_HANDOFF_r0002_20261120_KST.md`를 최신 업무 MCP 목적 인계로 확인해 주세요. Viewer 진단을 이번 MCP 확장 목표에서 제외하고, 기존 Linux MCP의 실제 tool/권한/host routing과 설치·로드된 L1 업무 스킬·Workflow/Kernel/Updater/Analyzer/Job 결과 조회 계약부터 G0로 대조해 주세요. 기존 기능은 REUSE/CONNECT, 근거로 확인된 결손만 최소 EXTEND하고 우선 P0의 Work/Knowledge/capability 상태 조회를 모바일 Agent에서 실호출 검증해 주세요. 코드 분석·스터디·Job 실행·지식 게시·설치·재시작 등 변경/비용/운영 작업은 실제 승인 범위를 확인한 뒤 별도 실행하고, Viewer 웹 UI 검증은 기존 별도 인계로 유지해 주세요. 기존 업무 Work에서 결과·시험·차단·다음 한 행동을 기록하되 회사 원문·로그·상세 MSC·토큰을 공개 저장소로 올리지 마세요.

## 8. 참조 및 상태 유지

- [이전 MCP Viewer 중심 r0001 — 이력](L1_MCP_AGENT_READONLY_CAPABILITY_AND_VIEWER_PROBE_HANDOFF_r0001_20261120_KST.md)
- [Viewer UI 별도 작업 r0002 — 계속 유효](L1_WORKSPACE_VIEWER_UI_CHANGE_AND_MCP_VALIDATION_HANDOFF_r0002_20261120_KST.md)
- [관리 업무 스킬 기능 요약](L1_SKILL_CAPABILITY_SUMMARY_INHOUSE_HANDOFF_r0001_20261113.md)
- 이 문서는 **설계·진단·최소 연결 작업 요청**이며 설치·호출·E2E·업무 GPT 수신을 이미 완료했다는 선언이 아니다.
