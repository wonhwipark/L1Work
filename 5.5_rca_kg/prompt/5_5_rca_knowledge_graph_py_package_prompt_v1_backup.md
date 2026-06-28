# 5.5 RCA Knowledge Graph — Python Package 구현 프롬프트 기본틀

---

## 1. 목적

이 문서는 [`master/L1_AI_Automation_Roadmap_v0.40.md`](L1a/master/L1_AI_Automation_Roadmap_v0.40.md) 의 `5.5 RCA Knowledge Graph` 항목을 구현하기 위한 AI 작업 프롬프트 기본틀이다.

현재 문서는 완성형 구현 명세가 아니라, 추후 Roo Code 또는 Claude Code에서 구체 구현을 이어가기 위한 기본 골격이다.

구현은 두 단계로 진행한다.

- **Step 1 (현재)**: 파일 기반 Knowledge Graph — pre-filter + YAML 저장 + Claude Code 자동 업데이트
- **Step 2 (향후)**: Python 패키지 — streaming parser / timeline reconstruction / Jira 연동

---

## 2. 선행 전제

`ai-mcp-package-v1.0_workflow_todo` 기반 환경 준비가 선행된 이후의 상황을 전제로 한다.

```text
- Roo Code 사용 가능
- Claude Code 사용 가능
- Jira 생성 가능
- Confluence read 가능
- Confluence write/update는 아직 미확인
- Local MCP 기반 사내 연동 환경은 이미 준비된 상태
```

---


## 3. 공통 설계 원칙

이 항목의 공통 설계 원칙은 [`prompt/5_0_common_automation_framework.md`](L1a/prompt/5_0_common_automation_framework.md) 를 단일 출처로 참조한다.

이 프롬프트에서는 아래만 추가로 유지한다.

- GPT + 사용자는 RCA Knowledge Graph의 연결 대상, 우선 관계, 활용 목적을 정한다.
- Roo Code / Claude Code는 현재 저장 방식, 그래프 표현 방식, 질의/탐색 방식을 최적화한다.
- 구현 중 개선점은 [`delta/`](L1a/delta) 또는 [`review_logs/`](L1a/review_logs) 에 기록한다.

---

## 4. 이 프롬프트에서 제외할 내용

아래 항목은 선행 작업에서 다루는 영역이므로 이 구현 프롬프트에 포함하지 않는다.

```text
- Node.js 설치 여부 확인
- npm/npx MCP 패키지 설치
- Jira MCP 등록
- Confluence MCP 등록
- claude mcp add 명령어 안내
- .mcp.json 생성
- Roo Code mcp_settings.json 생성
- MCP 서버 설정 절차
- MCP 연결 자체를 위한 초기 환경 구성
```

---

## 5. Master 5장 원문 요약

### 5.1 Workflow

```text
Issue
  ↓
Log
  ↓
Root Cause
  ↓
Fix
  ↓
Jira
  ↓
HLD
  ↓
TC
  ↓
API
  ↓
Knowledge Layer
```

### 5.2 설명

RCA Knowledge Graph는 Issue, Log, Root Cause, Fix, Jira, HLD, TC, API를 연결하는 구조화된 지식 그래프이다.
RCA를 Graph 형태로 저장하면 특정 API, 특정 Root Cause, 특정 Log Pattern, 특정 Jira, 특정 TC를 기준으로 과거 사례를 재사용할 수 있다.

### 5.3 Expected Benefit

```text
분석 시간 감소; 경험 재사용; 신규 인원 지원; 유사 Issue 검색; Root Cause Pattern 축적; Prevent Rule 생성; TC 보강 근거 확보
```

### 5.4 Precondition

```text
5.2 API Call Flow DB 구축 필요; Jira와 RCA 문서 연결 필요; Log Pattern 저장 기준 필요; Root Cause 분류 기준 필요
문제 유형별 pre-filter keyword/signature 기준 필요; RCA YAML 저장 템플릿 필요; signal 파일에 포함할 line number/timestamp/module/severity/UE-session-correlation id 기준 필요
```

### 5.4.1 Step 1 대용량 로그 처리 방침

대용량 로그(100MB~1GB txt)는 원문 전체를 AI Context에 직접 입력하지 않는다.
Step 1에서는 문제 유형별 pre-filter 로 `signal_<issue_type>.txt` 를 먼저 생성한다.

```text
현재:
log.txt (100MB~1GB) → Claude/Roo 분석 요청 → 결과 휘발

Step 1 개선:
log.txt → issue-type pre-filter → signal_<issue_type>.txt → Claude/Roo 분석 → RCA YAML 저장
```

signal 파일에는 가능한 경우 원본 line number, timestamp, module/component, severity, UE/session/correlation id 를 포함한다.
분석 결과는 `rca_kg/cases/YYYY-MM-DD_<issue_type>_<seq>.yaml` 로 저장하여 향후 Skill Seed 및 Knowledge Graph Seed 로 재사용한다.

### 5.5 Storage / Reuse

```text
Issue; Log; Root Cause; Fix; Jira; HLD; TC; API; Known Defect; Prevent Rule; 신규 Issue 분석 시 유사 RCA 검색; Critical Defect Rule 생성
```

---

## 6. 연동 대상 시스템 기준

- Jira: issue key, status, comment, fix version, close 정보 조회/연결에 사용한다.
- Confluence: RCA/HLD 문서 read에 사용한다.
- Confluence write/update: 기본 구현에서 제외하고 Knowledge Graph export 파일을 생성한다.
- Perforce: fix changelist 연결은 향후 확장 후보로 둔다.

---

## 7. Python Package 기본 구조

Roo Code 또는 Claude Code는 아래 구조를 기준으로 기본 패키지를 생성한다.

```text
rca_knowledge_graph/
├─ README.md
├─ requirements.txt
├─ .env.template
├─ examples/
│  ├─ sample_input.md
│  └─ sample_output.md
├─ src/
│  └─ rca_knowledge_graph/
│     ├─ __init__.py
│     ├─ config.py
│     ├─ models.py
│     ├─ clients/
│     │  ├─ __init__.py
│     │  ├─ jira_client.py
│     │  └─ confluence_client.py
│     ├─ workflow.py
│     └─ main.py
└─ tests/
   └─ test_dry_run.py
```

---

## 8. 입력값 기본틀

**Step 1 (파일 기반 KG):**
```text
- Large log txt file path
- Issue type (rach_failure, scg_failure, tx_abnormal, l2_retx, crash)
- Pre-filter keyword/signature rule (scripts/rach_failure_prefilter.ps1 등)
- Signal file 저장 경로 (rca_kg/signals/<case_id>_signal.txt)
- RCA YAML 저장 경로 (rca_kg/cases/<case_id>.yaml)
```

**Step 2 (Python 패키지, 향후):**
```text
- Jira issue key
- RCA 문서 링크 또는 markdown
- Log pattern 입력
- API/TC/HLD 연결 기준
- Knowledge graph 저장 경로
```

---

## 9. 출력값 기본틀

**Step 1 (파일 기반 KG):**
```text
- rca_kg/signals/<case_id>_signal.txt        ← pre-filter 출력
- rca_kg/cases/<case_id>.yaml                ← RCA 분석 결과 (schema/rca_case.schema.yaml 준수)
- rca_kg/indexes/index.md 업데이트           ← Case 목록 한 줄 추가
- skills_seed/<issue_type>_analyzer.md 업데이트 후보  ← 새 패턴 발견 시
```

**Step 2 (Python 패키지, 향후):**
```text
- RCA Graph JSON (초기는 JSON flat 구조 사용; 향후 graph DB 전환 시 models.py에서 포맷만 교체 가능하도록 interface 분리 권장)
- 유사 이슈 검색용 index 초안
- Prevent Rule 후보
- TC 보강 후보
```

---

## 10. AI 구현 지시 프롬프트 초안

아래 프롬프트를 Roo Code 또는 Claude Code에 입력하여 구현을 시작한다.

```text
현재 작업은 MCP 설치나 MCP 설정 작업이 아니다.
ai-mcp-package-v1.0 기반 환경은 이미 준비되어 있다고 가정한다.

목표:
5.5 RCA Knowledge Graph 자동화 아이템을 Python 패키지 형태로 구현해줘.

기본 전제:
- Roo Code 또는 Claude Code에서 작업한다.
- Jira 생성은 가능하다.
- Confluence read는 가능하다.
- Confluence write/update는 아직 미확인이므로 실제 write는 구현하지 말고 TODO 또는 옵션 처리한다.
- 모든 외부 변경 작업은 기본적으로 dry-run을 먼저 제공한다.
- 5.2 Code Analyzer의 Call Flow / 구조 분석 산출물은 완성 전제이나,
  기본틀에서는 local JSON 파일 또는 stub 데이터로 대체하여
  Knowledge Graph 패키지 구조를 먼저 완성한다.

구현 요구사항:
1. `rca_knowledge_graph` Python 패키지 구조를 생성한다.
2. `README.md`에 목적, 실행 방법, 입력값, 출력값, dry-run 사용법을 작성한다.
3. `requirements.txt`를 작성한다.
4. `.env.template`에는 필요한 환경 변수 이름만 정의하고 실제 값은 넣지 않는다.
5. `config.py`에서 환경 변수와 실행 옵션을 로딩한다.
6. `models.py`에 입력/출력 데이터 구조를 정의한다.
7. `clients/jira_client.py`는 Jira create/read/update가 필요한 경우의 wrapper 기본틀만 만든다.
8. `clients/confluence_client.py`는 Confluence read wrapper 기본틀을 만든다.
9. Confluence write/update가 필요한 경우 실제 구현 대신 `NotImplementedError` 또는 명시적 TODO로 남긴다.
10. `workflow.py`에 업무 흐름을 함수 단위로 구현한다.
11. `main.py`에서 CLI 또는 단순 실행 entry point를 제공한다.
12. `--dry-run` 옵션을 기본 동작으로 둔다.
13. 실제 Jira 생성이 필요한 경우 생성 전 preview를 출력한다.
14. `examples/sample_input.md`와 `examples/sample_output.md`를 작성한다.
15. `tests/test_dry_run.py`에 외부 시스템 변경 없이 실행 가능한 최소 테스트를 작성한다.
16. Step 1 대용량 로그 pre-filter 경로를 제공한다.
    - 원본 `log.txt` 전체를 AI Context에 직접 입력하지 않는다.
    - 입력으로 large log txt file path 와 issue type 을 받는다.
    - issue type 별 keyword/signature rule 을 적용해 `signal_<issue_type>.txt` 를 생성한다.
    - signal 에는 가능한 경우 원본 line number, timestamp, module/component, severity, UE/session/correlation id 를 포함한다.
    - signal 파일 생성은 dry-run 에서도 preview 가능해야 한다.
17. 기본 issue type 별 keyword/signature rule 초안을 README 또는 config 예시에 포함한다.
    - rach_failure: RACH, rach_failure, msg1~msg4, RAR, preamble, PHY_TIMER_EXPIRY
    - scg_failure: SCG, scgFailure, PSCell, secondary, B1, B2, handover
    - tx_abnormal: TX abnormal, tx fail, ul grant, harq
    - l2_retx: max retransmission, RLC, HARQ, retx
    - crash: ASSERT, FATAL, crash, backtrace, PC=, LR=, stack
18. RCA 분석 결과를 `rca_kg/cases/<case_id>.yaml` 로 저장할 수 있게 한다.
    - 파일명: `YYYY-MM-DD_<issue_type>_<3-digit-seq>.yaml`
    - `rca_kg/schema/rca_case.schema.yaml` 필드 구조를 준수한다.
    - 정식 Skill 파일이 없을 때는 `rca_kg/skills_seed/<issue_type>_analyzer.md` 를 참조한다.

완료 조건:
- dry-run 실행 가능
- 입력값 validation 가능
- Jira 생성 전 preview 가능
- Confluence read 호출부 분리
- Confluence write/update는 미확인 상태로 안전하게 분리
- README만 보고 다음 작업자가 이어서 구현 가능
```

---

## 11. 검증 기준

**Step 1 검증:**
```text
- 샘플 로그에서 issue type 별 signal 파일을 생성할 수 있어야 한다.
- signal 파일에는 가능한 경우 line number 와 핵심 log line 이 포함되어야 한다.
- rca_kg/cases/<case_id>.yaml 출력이 rca_case.schema.yaml 필드를 준수해야 한다.
- rca_kg/indexes/index.md 에 새 케이스 한 줄이 추가되어야 한다.
- 외부 시스템 변경 없이 dry-run 으로 pre-filter 경로를 검증할 수 있어야 한다.
```

**Step 2 검증 (향후):**
```text
- 패키지 구조가 생성되어야 한다.
- dry-run 실행 경로가 있어야 한다.
- 실제 Jira 생성 전 preview가 있어야 한다.
- Confluence read와 write/update가 명확히 분리되어야 한다.
- Confluence write/update는 현재 미확인 상태로 표시되어야 한다.
- 외부 시스템 변경 없이 test_dry_run.py가 실행 가능해야 한다.
```

---

## 12. 추후 보완 항목

**Step 1 보완:**
```text
- Python streaming parser 로 pre-filter 고도화
- UE/session/correlation id 기반 timeline reconstruction
- masking/normalization rule 고도화
- rca_kg/cases/ 10건 이상 누적 후 by_issue_type.yaml, by_root_cause.yaml, by_log_pattern.yaml index 추가
- RCA YAML 누적 기반 정식 Skill 파일 생성
- Knowledge Graph node/edge 자동 적재
- SCG failure 확인된 keyword 업데이트 (현재 전체 추정)
```

**Step 2 보완 (향후):**
```text
- 실제 Jira field mapping 확정
- 실제 Confluence page 구조 확정
- Confluence write/update 가능 여부 검증
- 사내 인증 방식별 예외 처리 추가
- 운영 로그 저장 방식 확정
- Graph 저장 포맷 확정 (JSON flat vs embedded graph DB vs external graph DB)
```

---

## 13. rca_kg/ 업데이트 주체 — Claude Code 자동 운영

### 13.1 업데이트 주체

`rca_kg/` 디렉토리는 **Claude Code** 가 분석 세션 내에서 직접 읽고 쓴다.
사용자는 pre-filter 실행과 분석 요청만 하면 된다.

```text
사용자:
  1. pre-filter 스크립트 실행 (PowerShell)
  2. Claude Code 에 분석 요청

Claude Code:
  3. signal 파일 읽기 (@rca_kg/signals/...)
  4. skills_seed 참조 (@rca_kg/skills_seed/...)
  5. cases/ 에 YAML 작성 (새 파일 생성)
  6. indexes/index.md 업데이트 (한 줄 추가)
  7. skills_seed 업데이트 후보 제안 (직접 수정 또는 제안)
```

### 13.2 Claude Code 에 분석 요청하는 표준 프롬프트

```text
@rca_kg/signals/YYYY-MM-DD_<issue_type>_001_signal.txt
@rca_kg/skills_seed/<issue_type>_analyzer.md
@rca_kg/cases/EXAMPLE_rach_failure_001.yaml

위 signal 파일을 분석해줘.
분석 기준은 skills_seed 의 checklist 를 따라줘.
결과를 EXAMPLE yaml 의 형식에 맞춰 아래 파일로 저장해줘:
  rca_kg/cases/YYYY-MM-DD_<issue_type>_001.yaml
저장 후 rca_kg/indexes/index.md 에 한 줄 추가해줘.
```

### 13.3 Claude Code 가 직접 쓰는 파일 목록

| 파일 | 작업 | 시점 |
|------|------|------|
| `rca_kg/cases/<case_id>.yaml` | 신규 생성 | 분석 완료 시 |
| `rca_kg/indexes/index.md` | 한 줄 추가 | case YAML 생성 직후 |
| `rca_kg/skills_seed/<type>_analyzer.md` | 누적 패턴 표 추가 | 새 패턴 발견 시 (제안 또는 직접) |

### 13.4 Claude Code 가 읽는 파일 목록

| 파일 | 용도 |
|------|------|
| `rca_kg/signals/<case_id>_signal.txt` | 분석 대상 |
| `rca_kg/skills_seed/<type>_analyzer.md` | 분석 기준 checklist |
| `rca_kg/cases/EXAMPLE_rach_failure_001.yaml` | 출력 형식 참조 |
| `rca_kg/schema/rca_case.schema.yaml` | 필드 정의 확인 |
| `rca_kg/schema/taxonomy.yaml` | confidence / root_cause 기준 |
| `rca_kg/indexes/index.md` | 유사 케이스 선별 (500건 이후) |

### 13.5 사람이 직접 해야 하는 것

```text
- pre-filter 스크립트 실행 (PowerShell)
- review.status 를 draft → reviewed → confirmed 로 승인
- skills_seed 내 # 추정 키워드를 # 확인됨 / # 삭제 로 업데이트
- Jira, HLD, TC 연결 정보 입력
```
