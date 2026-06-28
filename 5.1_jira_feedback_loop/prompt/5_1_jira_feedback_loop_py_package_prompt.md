# 5.1 Jira Feedback Loop — Python Package 구현 프롬프트 기본틀

---

## 1. 목적

이 문서는 [`master/L1_AI_Automation_Roadmap_v0.38.md`](L1a/master/L1_AI_Automation_Roadmap_v0.38.md) 의 `5.1 Jira Feedback Loop` 항목을 Python 패키지로 구현하기 위한 AI 작업 프롬프트 기본틀이다.

현재 문서는 완성형 구현 명세가 아니라, 추후 Roo Code 또는 Claude Code에서 구체 구현을 이어가기 위한 기본 골격이다.

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

- GPT + 사용자는 Jira Feedback Loop의 업무 목적과 성공 기준을 정한다.
- Roo Code / Claude Code는 현재 환경 기준으로 구현 방식, 연동 방식, dry-run 범위를 최적화한다.
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
(1) Critical Defect Detection
      ↓
(2) AI Root Cause Analysis
      ↓
(3) AI Patch Proposal
      ↓
(4) P4 Shelve Creation  ← AI가 p4 CLI 또는 Perforce MCP로 직접 생성
      ↓
(5) Jira Creation
    (Shelve Number + Root Cause Summary + Patch Proposal Summary 포함)
      ↓
(6) Review & Discussion
      ↓
(7) Resolution Decision
    ├─ Reject → False Positive Rule 정리 → Skill Update
    └─ Resolve → Prevent Rule 정리 → Skill Update
```

### 5.2 설명

Jira Feedback Loop는 Critical Defect Workflow의 후속 단계이다.
AI가 결함 후보의 Root Cause를 분석하고 Patch를 제안한 후, p4 CLI 또는 Perforce MCP를 통해 P4 Shelve를 직접 생성한다.
Jira 등록 시 Shelve Number, Root Cause Summary, Patch Proposal Summary를 포함하여 Reviewer가 즉시 수정 후보를 확인할 수 있도록 한다.
Review 결과는 Reject와 Resolve로 분기한다. Jira Close 상태는 Jira MCP 폴링(JQL)으로 감지하고 Resolution 필드로 Reject/Resolve를 분류한다.
Reject 사례는 False Positive Rule로, Resolve 사례는 Prevent Rule로 정리하여 각각 Skill에 반영한다.
목적은 Jira 처리 결과를 Rule, Skill, Prompt, Workflow 개선으로 연결하는 것이다.

### 5.3 Expected Benefit

```text
False Positive 감소; 경험 축적; Rule 강화; Review 결과 재사용; Critical Defect 검출 정확도 향상; Jira Close 이후 지식 손실 방지
```

### 5.4 Precondition

```text
4.1 Critical Defect Workflow 완성 필요; Jira 상태 조회 또는 Jira MCP 연동 필요; Review Comment 수집 방식 필요; Jira Close 기준 정의 필요
```

### 5.5 Storage / Reuse

```text
Rule DB; False Positive History; Prevent Rule; Review Feedback; Rule Version; Prompt / Skill DB; 다음 Branch Scan에서 Prevent Rule 재사용; 유사 Defect 검출 시 기존 Jira와 RCA 연결
```

---

## 6. 연동 대상 시스템 기준

- Jira: search/read/update/create 가능 범위 사용. Jira 등록 시 Shelve Number, Root Cause Summary, Patch Proposal Summary를 포함하고, review comment, status transition 정보를 읽는다. Jira MCP 폴링(JQL)으로 Close 상태를 감지하고 Resolution 필드로 Reject/Resolve를 분류한다. 필요한 경우 후속 Jira 또는 개선 task를 생성한다.
- Confluence: read가 필요한 경우 RCA/HLD 링크 조회에 한정한다. write/update는 기본 구현에서 제외하거나 TODO 처리한다.
- Perforce: AI가 p4 CLI 또는 Perforce MCP를 통해 P4 Shelve를 직접 생성한다. 모든 shelve 생성 전 dry-run preview를 필수로 제공한다. Shelve Number는 Jira Creation 시 attach 정보로 사용한다.

---

## 7. Python Package 기본 구조

Roo Code 또는 Claude Code는 아래 구조를 기준으로 기본 패키지를 생성한다.

```text
jira_feedback_loop/
├─ README.md
├─ requirements.txt
├─ .env.template
├─ examples/
│  ├─ sample_input.md
│  └─ sample_output.md
├─ src/
│  └─ jira_feedback_loop/
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

```text
- Jira project key 또는 JQL
- Critical Defect Jira key 목록
- AI Root Cause Analysis 결과 (결함 원인, 영향 범위)
- AI Patch Proposal 결과 (수정 방향, 코드 변경안)
- P4 Shelve 생성 대상 파일 및 변경 내용
- Jira MCP 폴링 주기
- Resolution 필드 기준 (Reject/Resolve 분류 기준)
- Rule/Skill 저장 위치
```

---

## 9. 출력값 기본틀

```text
- P4 Shelve 생성 dry-run preview (Shelve Number 포함)
- Jira Creation dry-run preview (Shelve Number + Root Cause Summary + Patch Proposal Summary)
- Jira Feedback 분석 JSON (Resolution 기준 Reject/Resolve 분류)
- [Reject 경로] False Positive Rule 후보 Markdown
- [Resolve 경로] Prevent Rule 후보 Markdown
- Skill Update 대상 항목 요약
- 필요 시 후속 Jira 생성 dry-run preview
```

---

## 10. AI 구현 지시 프롬프트 초안

아래 프롬프트를 Roo Code 또는 Claude Code에 입력하여 구현을 시작한다.

```text
현재 작업은 MCP 설치나 MCP 설정 작업이 아니다.
ai-mcp-package-v1.0 기반 환경은 이미 준비되어 있다고 가정한다.

목표:
5.1 Jira Feedback Loop 자동화 아이템을 Python 패키지 형태로 구현해줘.

기본 전제:
- Roo Code 또는 Claude Code에서 작업한다.
- Jira MCP 연동이 가능하다.
- Perforce MCP 또는 p4 CLI 연동이 가능하다.
- Confluence read는 가능하다.
- Confluence write/update는 아직 미확인이므로 실제 write는 구현하지 말고 TODO 또는 옵션 처리한다.
- 모든 외부 변경 작업은 기본적으로 dry-run을 먼저 제공한다.

구현 요구사항:
1. `jira_feedback_loop` Python 패키지 구조를 생성한다.
2. `README.md`에 목적, 실행 방법, 입력값, 출력값, dry-run 사용법을 작성한다.
3. `requirements.txt`를 작성한다.
4. `.env.template`에는 필요한 환경 변수 이름만 정의하고 실제 값은 넣지 않는다.
5. `config.py`에서 환경 변수와 실행 옵션을 로딩한다.
6. `models.py`에 입력/출력 데이터 구조를 정의한다.
   - AI Root Cause Analysis 결과 필드를 포함한다.
   - AI Patch Proposal 결과 필드를 포함한다.
   - P4 Shelve Number 필드를 포함한다.
   - Resolution 필드 (Reject/Resolve 분류 기준)를 포함한다.
7. `clients/jira_client.py`는 Jira MCP 기반 create/read/update wrapper 기본틀을 만든다.
   - Jira 등록 시 Shelve Number, Root Cause Summary, Patch Proposal Summary attach 필드를 포함한다.
   - JQL 폴링으로 Close 상태 감지 및 Resolution 필드 조회 기능을 포함한다.
8. `clients/perforce_client.py`는 p4 CLI 또는 Perforce MCP 기반 Shelve 생성 wrapper 기본틀을 만든다.
   - Shelve 생성 전 반드시 dry-run preview를 출력한다.
9. `clients/confluence_client.py`는 Confluence read wrapper 기본틀을 만든다.
   - Confluence write/update가 필요한 경우 `NotImplementedError` 또는 명시적 TODO로 남긴다.
10. `workflow.py`에 업무 흐름을 함수 단위로 구현한다.
    - Critical Defect Detection → AI Root Cause Analysis → AI Patch Proposal → P4 Shelve Creation → Jira Creation → Review & Discussion → Resolution Decision 순서로 구성한다.
    - Resolution Decision에서 Reject/Resolve 분기를 명확히 구현한다.
    - Reject 경로: False Positive Rule 정리 → Skill Update
    - Resolve 경로: Prevent Rule 정리 → Skill Update
11. `main.py`에서 CLI 또는 단순 실행 entry point를 제공한다.
12. `--dry-run` 옵션을 기본 동작으로 둔다.
13. P4 Shelve 생성 및 Jira 생성 전 각각 preview를 출력한다.
14. `examples/sample_input.md`와 `examples/sample_output.md`를 작성한다.
15. `tests/test_dry_run.py`에 외부 시스템 변경 없이 실행 가능한 최소 테스트를 작성한다.
    - Reject/Resolve 분기 실행 경로를 각각 테스트한다.

완료 조건:
- dry-run 실행 가능
- 입력값 validation 가능
- P4 Shelve 생성 전 preview 가능
- Jira 생성 전 preview 가능 (Shelve Number + Root Cause Summary + Patch Proposal Summary 포함)
- Reject/Resolve 분기 실행 경로 각각 동작
- False Positive Rule / Prevent Rule 각각 출력
- Confluence read와 write/update가 명확히 분리
- README만 보고 다음 작업자가 이어서 구현 가능
```

---

## 11. 검증 기준

```text
- 패키지 구조가 생성되어야 한다.
- dry-run 실행 경로가 있어야 한다.
- P4 Shelve 생성 전 preview가 있어야 한다.
- Jira 생성 전 preview가 있어야 한다 (Shelve Number + Root Cause Summary + Patch Proposal Summary 포함).
- Reject/Resolve 분기 실행 경로가 각각 있어야 한다.
- False Positive Rule과 Prevent Rule이 각각 별도 출력으로 구분되어야 한다.
- Confluence read와 write/update가 명확히 분리되어야 한다.
- Confluence write/update는 현재 미확인 상태로 표시되어야 한다.
- 외부 시스템 변경 없이 test_dry_run.py가 실행 가능해야 한다.
```

---

## 12. 추후 보완 항목

```text
- 실제 Jira field mapping 확정
- 실제 Confluence page 구조 확정
- Confluence write/update 가능 여부 검증
- 사내 인증 방식별 예외 처리 추가
- 운영 로그 저장 방식 확정
- 결과물 저장 위치 확정
```
