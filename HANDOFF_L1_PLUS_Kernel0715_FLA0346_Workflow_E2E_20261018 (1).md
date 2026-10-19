# HANDOFF — PLUS 분석기 정합성 감사 및 SOC-417698 Workflow E2E 마무리

- 작성일: 2026-10-18 (KST)
- 상태: **첨부 ZIP 2개 소스 검토 완료 / 후속 개선 작업은 미적용 / 사내 실제 실행 검증 미완료**
- 검토 대상:
  1. `work-ledger-kernel_v0_7_15 (1).zip` — v0.7.15
  2. `l1-fla_v0_3_46_1015.zip` — v0.3.46
- 기본 분석기 정확한 이름: **`l1sw-dev-log-analyzer-plus`** (과거 오기 `l1sw-dev-analyzer-plus` 사용 금지)
- 요청 의도: 두 스킬이 PLUS를 올바르게 사용하는지 실물 소스로 검증하고, 미완료된 **SOC-417698 / Work `20261014-1C167F69`** 메신저 Agent → MCP → Workflow → PLUS → Ledger E2E 문제를 해결하기 위한 **구현용 인계**를 남긴다.

> **중요: `l1-fla`는 복수 이슈 분석용 별도 오케스트레이터다. 단일 Work의 기본 경로에 끼워 넣거나, FLA의 성공을 Workflow E2E 성공으로 간주하지 않는다.** 이번에 제공된 두 ZIP에는 `l1-fix-workflow` 최신 설치본과 사내 `l1sw-dev-log-analyzer-plus` 원본/MCP Wrapper가 없다. 이들 내부 동작은 첨부 ZIP만으로 확정할 수 없다.

---

## 1. 결론 요약 / 변경 우선순위

| 구성 | PLUS 지원 판정 | 실제 실행 판정 | 권장 조치 |
|---|---|---|---|
| **Kernel v0.7.15** | **지원 확인**: BUG/BUG-NR `analyze-issue` Provider Registry에 PLUS 명시 | Kernel은 실행기가 아니므로 적용 대상 아님 | PLUS 등록 관련 운영 코드 변경 불필요. 오래된 설명/테스트 정책 충돌만 별도 정리 |
| **FLA v0.3.46** | **지원 확인**: `plus` 기본 preset, 설치 프로필 마이그레이션, 런타임 위임 경로 존재 | **실제 PLUS headless Run 성공은 미검증** | 과거 기본 분석기 명칭이 남은 문서/라우팅 설명 정합성 보완. 사내 실제 OpenCode CLI 계약 확인 |
| **단일 Work Workflow** | 이전 사내 진단에서 PLUS 라우팅/Kernel/Result Adapter 정상 보고 | SOC-417698 Provider 미실행 및 Confluence 차단 이력 존재 | **최우선: 설치된 Workflow·MCP·Agent의 실제 첫 차단 지점 조사**. FLA 필수 경유 금지 |

**판정:** 두 ZIP에서 PLUS 선택·등록 자체는 이미 구현되어 있다. **PLUS를 기본 분석기로 다시 교체하는 대규모 코드 수정은 필요하지 않다.** 남은 본질적 문제는 실제 사내 호출 경계·로그 Scope·Agent Confluence 라우팅과 E2E 결과 검증이다.

---

## 2. 정확한 아키텍처 / 책임 분리

```text
A. 단일 Jira Work 후속 분석 (이번 사용 사례)
사외 모바일 → 사내 메신저 Agent → Linux MCP run_l1_fix_workflow
    → l1-fix-workflow (Work/Jira/Scope/승인/intent)
    → Provider Manifest → OpenCode Shim → l1sw-dev-log-analyzer-plus
    → Workflow Result Adapter → work-ledger-kernel (Evidence 원본 보존 + 신규 append)
    → MCP TL Summary
    └─ GitHub work_docs Push는 사용자 명시 요청 시에만

B. 다중 Jira/정기 분석 (별도 실행 경로)
LLM/Agent/Job → l1-fla v0.3.46 → plus preset
    → Headless OpenCode 사전 가용성 검사
    → l1sw-dev-log-analyzer-plus (Jira 조회·로그 취득·분석 소유)
    → l1-fla-delegated-result/2 검증 → FLA 자체 Run/통합 보고서
    └─ Work Ledger Evidence 자동 append를 의미하지 않음

C. 공통 근거 Registry
work-ledger-kernel v0.7.15: PLUS Provider가 남긴 issue_analysis 등
등록 가능한 출처인지 검증 / 자체적으로 스킬을 호출하지 않음.
```

**입출력 계약을 혼용하지 말 것:** FLA delegated JSON (`l1-fla-delegated-result/1|2`)과 Workflow Runner 결과 (`request.json`/`provider_result.json` 및 receipt)는 서로 다른 계약이다. 자동 호환이라고 추정하지 않는다.

---

## 3. Kernel v0.7.15 소스 검증

### 3.1 확인된 구현

- `contracts/registry_v1.json`: BUG/BUG-NR `analyze` / `analyze-issue`의 허용 Provider에 `issue-analyzer`, `l1-log-analysis`, **`l1sw-dev-log-analyzer-plus`**가 함께 등록되어 있다.
- `work_ledger_kernel/contracts/registry_v1.json`: 동일 등록이 패키지 내부에도 존재한다. 설치본에서는 두 사본의 정합성을 유지해야 한다.
- `tests/test_plus_registry_v0714.py`: PLUS 출처로 `issue_analysis` + 실제 테스트용 `repro_attempt`를 기록한 뒤 `ANALYZED` 전이를 확인한다.
- `README.md`, `SKILL.md`는 PLUS 허용을 "provenance/registry 확장"으로 설명하고 **Runner를 설치하지 않는다**고 명시한다.
- 기존 Provider `l1-log-analysis` 및 `issue-analyzer`는 과거 분석 Evidence의 출처 보존을 위해 계속 유지한다.

### 3.2 주의할 사항

- Registry에서 PLUS를 허용해도 `configured_runner()`나 OpenCode 실행 파일이 자동 생성되는 것은 아니다. 실행 소유권은 Workflow/Provider 설정에 있다.
- `ANALYZED` 단계의 필수 Evidence 종류를 완화하지 말 것. `repro_attempt`를 실제 재현 시도 없이 만들어서는 안 된다. Evidence **append**와 FSM **전이**는 서로 별개로 검증한다.
- 전체 Kernel 테스트 로컬 실행: `130 tests / failures=3 / errors=5`. PLUS 전용 테스트는 **1/1 통과**. 전체 실패 중 Linux launcher 실행 비트 미보존에 따른 2건과, 새 `JIRA_WRITE_DEFAULT_DENY` 보안 게이트와 과거 테스트 기대값 충돌 등이 확인되었다. 이를 PLUS 결함으로 오인해서는 안 되며, Jira 쓰기 차단 정책을 완화해 테스트를 통과시키면 안 된다. ZIP 추출 도구에 따른 실행비트 보존 여부도 별도 검증한다.
- 대응: 테스트 코드/픽스처가 최신 승인 계약을 반영하도록 개선하되, 운영 Jira 쓰기는 기본 OFF 유지. PLUS Registry 자체는 수정 불필요.

---

## 4. L1-FLA v0.3.46 소스 검증

### 4.1 PLUS 기본 분석기가 실제 등록·선택되어 있음

- `templates/default_profile.json`: `analysis.default_analyzer="plus"`.
- 같은 파일 `analysis.analyzers.plus.skill="l1sw-dev-log-analyzer-plus"`, `invocation="natural_language"`, `input_mode="jira"`, `acquisition_owner="analyzer"`, `fallback_analyzer_id=""`.
- `install.py` (PLUS 등록/마이그레이션 구간): 이전 내장 기본값 `l1log` 또는 `l1sw`는 PLUS로 이전. **사용자가 설정한 custom named default는 변경하지 않음**.
- `scripts/l1-fla.py`의 `resolve_analyzer_config()`는 프로필·라우팅 override를 기준으로 Analyzer를 선택하며, `probe_delegated_analyzer()` / `run_natural_language_jira_analyzer()`는 실제 모델 CLI 실행 경로를 갖는다.
- `scripts/low_spec_route.py`는 명시적인 `l1sw-dev-log-analyzer-plus` 요청을 `--analyzer-id plus`로 라우팅한다.
- `skillsilent/contract.json`, `RELEASE_NOTES_v0_3_46_1015.md`도 PLUS 기본값, 자동 fallback OFF를 명시한다.

### 4.2 실행과 검증 계약

- FLA는 Run 시작 시 headless provider에서 선택 분석기의 가용성을 1회 probe 한다. 확인 불가 시 기본 PLUS preset에서 자동으로 legacy analyzer로 전환하지 않고 **BLOCKED** 처리한다.
- Delegated 실행은 PLUS에 Jira 조회/로그 취득/실제 RCA 수행을 위임하고, 최종 응답을 `l1-fla-delegated-result/2` (레거시 `/1` 허용) 계약으로 검증한다.
- 실제 선택된 `analyzer`·`jira`·`status`·`failure_kind`를 검사하며 임의 stdout을 완료로 인정하지 않는다.
- FLA 결과 `analysis_complete`와 FLA 자체 `DELEGATED_VALIDATED`는 **Work Ledger Evidence 자동 등록을 의미하지 않는다**.
- OpenCode CLI는 내부 `_provider_command()`에서 `opencode run -m <model> --auto <prompt>` 형태로 구성한다. **실제 사내 OpenCode 버전에서 이 호출 계약이 유효한지 / 모델·권한·정책이 실제 작동하는지는 이번 로컬 검증에 포함되지 않았다.** 미확인 인자를 임의로 추가하지 말 것.

### 4.3 문서 정합성 결함 (수정 권장)

아래 파일에 예전 기본값(`l1-log-analysis` / `l1log`)을 **현재형으로** 기술한 문구가 남아 있다.

- `README.md` (v0.3.46 공지 바로 아래 기존 "기본 Jira Analyzer=l1-log-analysis" 등)
- `SKILL.md` (문서 서두는 v0.3.46이나 이후 옛 기본 분석기 설명 잔존)
- `references/FULL_SKILL_GUIDE.md`, `references/input_and_output_contract.md`, `references/FLA_FAILURE_ROOT_CAUSE_PROMPT.md`
- `scripts/low_spec_route.py`의 구 명시 분석기 선택 설명 "default analyzer-owned Jira path"는 실제로는 legacy override이므로 표현 수정
- `skillsilent/contract.json`의 결과 설명은 `/1`을 필수처럼 표현하지만 런타임은 `/2`를 우선하고 `/1`을 허용하므로 문서 계약 설명 동기화 권장

**수정 원칙:** 현행 동작을 설명하는 부분만 변경하고, 역사적 릴리스 노트·기존 evidence의 provider ID는 일괄 치환하지 않는다. 프로필 사용자 지정 default는 존중한다. 문서 수정만으로 실제 실행 문제를 해결했다고 주장하지 않는다.

### 4.4 Confluence와의 관계

- 이번 두 ZIP의 주요 `scripts/` 및 Kernel 런타임 코드 검색에서는 **Confluence API를 직접 호출하는 코드가 확인되지 않았다**.
- `l1-fla/references/L1_FLA_OPERATION_CONFLUENCE.html`은 설명 자료로 존재한다. **파일명에 Confluence가 있다는 이유만으로 메신저의 보안 차단 주체라고 판단하지 않는다.**
- 메신저 정책 메시지의 호출 주체는 실제 Agent 도구 라우팅 기록 또는 OpenCode 이벤트 스트림을 봐야만 특정할 수 있다.

---

## 5. 수행한 로컬 검증 / 미검증 경계

| 검증 | 결과 | 의미 |
|---|---|---|
| 두 ZIP 파일 무결성 (`ZipFile.testzip`) | 양쪽 정상 | 압축 파일 내부 CRC 오류 없음 |
| FLA PLUS 기본값 테스트 | **3/3** | 기본 preset, 설치 마이그레이션, custom default 보존 |
| FLA PLUS 구 경로/위임 테스트 | **7/7** | delegated 실행 로직의 모의 검증 |
| FLA delegated 계약 테스트 | **8/8** | 가용성 probe 및 완료/차단 계약 모의 검증 |
| Kernel PLUS Evidence 테스트 | **1/1** | PLUS 출처의 Registry 허용 및 분석 단계 전이 테스트 |
| Python 주요 런타임 `py_compile` | 통과 | 소스 구문 검사 |
| Kernel 전체 단위 테스트 | 130건 중 3 실패/5 오류 | PLUS 외 테스트 환경·Jira 기본 차단 계약 관련 미정리 |
| FLA 전체 단위 테스트 | 제한시간 초과, **전체 통과 판정 불가** | 대상 선별 테스트만 통과 확인 |
| 사내 설치 프로필·OpenCode 실제 실행 | **미검증** | 로컬 ZIP에는 사내 실행 계정/환경 없음 |
| 메신저 Agent → Workflow → PLUS 실제 SOC-417698 분석 | **미검증/기존 차단** | 이번 두 ZIP으로 E2E 성공 주장 금지 |

---

## 6. 미완료 SOC-417698 E2E 사고 인계 (중요)

### 대상 및 기대 동작

- Jira: **SOC-417698** (기존 SOC-414798 표기는 오기)
- Work ID: **`20261014-1C167F69`** (영문 대문자 그대로 사용)
- 제목: RF MIPI error 이슈 분석 및 해결
- 기본 분석기: `l1sw-dev-log-analyzer-plus`
- 목표: 기존 RCA/Evidence 보존 → 새 분석 Run **실제 실행** → 결과 검증 → 신규 Evidence만 append → 메신저에서 TL 요약 제공

### 이전 대화에서 확인된 사실 (이번 ZIP에서 독립 검증한 내용 아님)

1. 운영 OpenCode Shim에서 PATH 문제로 `opencode`를 찾지 못해 `exit 4`가 발생했다. `~/.opencode/bin`을 PATH에서 찾는 방식 대신, 검증된 `/home/whpark/.opencode/bin/opencode` 절대경로로 수정했고 Smoke Test 성공 및 기존 Work 9032 보존이 보고됐다.
2. 후속 SOC-417698 시도에서는 Provider **미실행·exit code 없음**. 사내 조사에서는 `LOG_SOURCE_NOT_FOUND` (`/home/whpark/log/SOC-417698/` 미존재)와 요청 문구 `EXPLICIT_PATTERN` 불일치를 **서로 독립적인 호출 전 차단**으로 확인했다.
3. `"추가 분석 실행해줘"`처럼 실제 실행 의도가 분명한 문장으로 Mock Route→Queued→Result/Evidence 테스트는 통과했다고 보고됐다. **Mock은 실제 PLUS 실행의 증거가 아니다.**
4. 사용자 보고: 메신저 Agent에 재요청하자 약 20분 후 **"보안정책상 Confluence 기능은 메신저에서 사용할 수 없음"** 응답. 무엇이 Confluence를 호출했고 어느 단계까지 분석됐는지는 미확인.
5. 마지막으로 사내 LLM에 요청한 **Confluence 차단 원인 조사 프롬프트 결과는 아직 제공되지 않았다**. 분석기 실행 성공/신규 Evidence append도 확인되지 않았다.
6. 이전 설치본 보고에서 Workflow **v1.6.22**가 언급됐지만 사내 최신 버전은 추가 검증 필요. 이번 첨부 두 ZIP은 Workflow/MCP 실설치본을 포함하지 않는다.

### 해서는 안 되는 추정

- Confluence 차단 = FLA가 호출됐음 (근거 없음)
- Kernel Registry에 PLUS 있음 = Agent에서 PLUS 실제 실행 가능 (성립하지 않음)
- FLA PLUS 기본값 정상 = Workflow가 PLUS를 실행 (별도 경로)
- log source가 없으므로 다른 Jira 로그를 대신 사용 (금지)
- E2E 실증 없이 `SUCCESS`, 신규 Evidence, RCA 변경을 가정 (금지)

---

## 7. 후속 구현 지침 / 권장 우선순위

### P0 — **단일 Work 실제 차단 원인부터 조사 (필수)**

1. 사내 **실제 설치된** Workflow, 메신저 MCP Wrapper, PLUS Shim/Manifest, PLUS 결과 포맷을 확인한다. 이번 ZIP 두 개만 수정해 끝낼 문제가 아니다.
2. SOC-417698 요청에 대해 `MCP called? → Workflow route/action? → scope? → Provider started? → OpenCode started? → PLUS status? → evidence append?`를 시점별로 **하나의 Run ID**에 맞춰 대조한다.
3. 메신저의 Confluence 정책 차단 메시지 호출 주체가 `Agent 도구 선택`, `Workflow`, `OpenCode/PLUS`, `후처리` 중 어디인지 기록으로 식별한다. **보안정책 우회 금지**; 필요하지 않은 Confluence 연동은 실행 경로에서 제외한다.
4. 로그 source가 계속 미존재라면 승인된 실제 로그 위치를 사용자에게 요구하거나 `BLOCKED / LOG_SOURCE_NOT_FOUND`로 끝낸다. 분석기를 기동시키기 위한 가짜/타 이슈 로그 사용 금지.
5. 진단용 실행은 이전 실패 Run의 receipt/이벤트만 읽고 **자동 재시도 및 실제 분석 실행 금지**. 원인이 해결되고 실행 승인이 확보된 경우에만 E2E **1회** 수행한다.
6. TL 응답은 Run ID, 분석 실행 여부, RCA 보존, 신규 Evidence 건수, 로그·코드 근거와 최초 실패 지점을 직접 출력한다.

### P1 — FLA 문서/계약 정합성 (작은 패치 후보)

- `README.md`, `SKILL.md`, `references/*`의 **현재 기본값 설명**을 `plus`로 정리.
- `low_spec_route.py`의 명시적 `l1log` override 설명 수정.
- 계약 설명을 delegated v2 우선/v1 호환으로 정리.
- 오해 방지: FLA 결과가 Work Ledger에 자동 누적되는 것으로 표현하지 않는다.
- 실설치 OpenCode 버전에서 기존 실행 인자와 provider path가 정상인지 확인. 실행 명령을 추측해서 바꾸지 않는다.
- 기존 FLA 사용자의 custom default와 legacy 명시 선택 테스트 유지.

### P2 — Kernel 테스트/문서 회귀 정리 (PLUS 기능과 독립)

- ZIP 설치·실행 비트 검증 및 테스트 압축 해제 시 모드 보존.
- `JIRA_WRITE_DEFAULT_DENY`에 부합하도록 테스트 시나리오/예상 에러 순서를 업데이트한다.
- 운영 Jira 쓰기 플래그 활성화를 일반적인 테스트 해결책으로 사용하지 않는다.
- PLUS Registry 원본 및 사본 동기화, 레거시 Evidence 보존 회귀 테스트 유지.

### P3 — E2E가 성공할 때만 최종 판정

- 메신저 Agent가 실제 `run_l1_fix_workflow` 호출
- 연결 Jira = SOC-417698 / Work ID = `20261014-1C167F69`
- 실제 `l1sw-dev-log-analyzer-plus` 프로세스/Run ID/결과 JSON 및 근거 확인
- 기존 RCA/Evidence ID 불변 + 검증된 신규 `issue_analysis` Evidence append (실제 재현 시도 없는 `repro_attempt` 허위 생성 금지)
- 승인 없이 Jira Create/Comment, Git Push, 코드 수정/빌드, branch/worktree 변경 없음
- Confluence 정책 우회 없이 메신저 TL 요약 결과 확인

---

## 8. 새 대화 시작 프롬프트

> 첨부 `HANDOFF_L1_PLUS_Kernel0715_FLA0346_Workflow_E2E_20261018.md`를 기준으로 계속 진행해줘. Kernel v0.7.15와 FLA v0.3.46의 PLUS 지원 여부는 ZIP 소스 검토에서 확인됐다. Kernel은 출처 Registry만, FLA는 다중 Jira 오케스트레이터로 유지한다. **단일 SOC-417698 / Work 20261014-1C167F69 후속 분석은 Workflow 직접 호출**이며 FLA를 필수 경유시키지 마. 사내 메신저 Confluence 정책 차단과 LOG_SOURCE/요청 패턴 문제의 실제 최신 원인을 먼저 확인하고, 그 원인에만 최소 수정·검증을 진행해줘. 구현된 기능을 다시 만들거나 사내 미제공 실행 계약/JSON 스키마를 지어내지 마. 사내 조사 프롬프트는 3,000자 이내, 최종 응답은 숫자 객관식 + 오류 한 줄만 요구해줘. Git Push, Jira 생성/Comment, 빌드와 실 Work 변경은 명시 승인 전 금지.

### 사내 Linux LLM에 보낼 **원샷 읽기 전용 조사 프롬프트** (3,000자 이내)

```text
SOC-417698 / Work 20261014-1C167F69의 미완료 Workflow E2E를 1회에 걸쳐 읽기 전용으로 조사해줘.

기준: l1sw-dev-log-analyzer-plus (정확한 스킬명). Kernel v0.7.15는 PLUS Evidence provider 허용, FLA v0.3.46은 별도 다중 이슈 오케스트레이터이며 이번 Work의 필수 실행기가 아님.

최근 메신저 Agent 요청은 약 20분 뒤 "보안정책상 Confluence 기능은 메신저에서 사용할 수 없음"으로 종료. 과거 LOG_SOURCE_NOT_FOUND, EXPLICIT_PATTERN 불일치, Shim opencode PATH 문제는 보고됐지만 새 원인을 추정하지 마.

실제 사내 설치본과 최근 실패 Run만 조사해 다음을 한 번에 확인해줘:
1) 메신저의 MCP 호출 여부·실제 선택 도구·전달 인자
2) Workflow intent/action/Scope/실행 차단 조건
3) PLUS Shim/OpenCode 실제 실행 여부·최초 오류 및 events JSONL
4) Confluence 호출 주체와 20분 지연 원인
5) 실제 LOG_SOURCE 존재 여부, 연결 Work/Jira 정합성
6) RCA/Evidence 보존 및 신규 Evidence 유무
7) FLA profile default=plus 여부(별도 참고만), Kernel Registry 허용 여부
8) 최소 개선 대상: Agent / Workflow / Shim / PLUS / 경로·환경 / 불필요

제약: 사내 운영 스킬/Manifest/MCP 변경 금지, 새 분석 실행 금지, Confluence 우회 금지, Git Push/Jira 쓰기/빌드 금지. 실제 실패 기록 없으면 0=미확인. 화면 캡처·긴 출력 금지. 중간 질문 금지.

응답 형식:
Q1 MCP: 0 미확인 / 1 호출 / 2 미호출
Q2 Provider: 0 미확인 / 1 기동 / 2 미기동
Q3 최초 차단: 0 미확인 / 1 Agent / 2 Scope / 3 Workflow 실행 패턴 / 4 Runner / 5 분석기 / 6 후처리
Q4 Confluence 주체: 0 미확인 / 1 Agent / 2 Workflow / 3 OpenCode·PLUS / 4 후처리
Q5 지연: 0 미확인 / 1 분석 / 2 큐 / 3 재시도 / 4 timeout / 5 기타
Q6 로그: 0 미확인 / 1 존재 / 2 없음 / 3 정책 차단
Q7 Evidence: 0 미확인 / 1 기존 보존·신규 0 / 2 기존 보존·신규 1이상 / 3 변형 우려
Q8 조치: 0 미확인 / 1 Agent / 2 Workflow / 3 Runner / 4 PLUS / 5 로그 준비 / 6 정상 재실행 가능

첫 줄 숫자 8개, 둘째 줄 BLOCKER=오류 코드 또는 UNKNOWN, 셋째 줄 FIX=30자 이내 핵심 조치. 내부 보고서는 자체 저장 가능하지만 사외 전달 응답에 경로·원문·상세문장 출력 금지.
```

---

## 9. 다음 창에 추가로 있으면 좋은 파일 (실제 수정 판단용)

1. 이 핸드오프 MD와 이 두 ZIP (이번 ZIP은 제공됨)
2. **사내 최신 `l1-fix-workflow` 설치 소스/ZIP** (v1.6.22 이후 실제본) — 수집이 가능할 때
3. 사내 Linux MCP 기존 Wrapper `whpark-mcp`의 진단 요약 또는 관련 설정·라우팅 코드 (보안상 원문 반출 불가 시 객관식 진단만)
4. PLUS 실제 실행 계약의 **비밀정보 없는 최소 인터페이스 요약** (OpenCode 명령, receipt/status/report 포맷)
5. 기존 실패 Run의 **오류 코드만**, 보고서 원본/소스 로그 외부 반출 불필요

**종료 기준:** 두 스킬에서 PLUS가 명칭상 등록된 사실이 아니라, **SOC-417698에 대해 실제 PLUS 실행 완료 + Work의 RCA 보존 + 신규 Evidence 누적 + 메신저 요약**이 관측되어야 최종 E2E `SUCCESS`다.
