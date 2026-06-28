# 5.4 HLD ↔ Code Consistency Check — Python Package 구현 프롬프트 기본틀

---

## 1. 목적

이 문서는 [`master/L1_AI_Automation_Roadmap_v0.38.md`](L1a/master/L1_AI_Automation_Roadmap_v0.38.md) 의 `5.4 HLD ↔ Code Consistency Check` 항목을 Python 패키지로 구현하기 위한 AI 작업 프롬프트 기본틀이다.

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

- GPT + 사용자는 Consistency Check의 비교 기준, 우선 탐지할 Gap 유형, 승인 기준을 정한다.
- Roo Code / Claude Code는 현재 코드베이스/HLD 형식 기준으로 파서, 비교 로직, 리포트 형식을 최적화한다.
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
HLD
  ↓
Code 분석
  ↓
Gap Detection
  ↓
누락 Branch 발견
  ↓
HLD 수정안
  ↓
Confluence Update
```

### 5.2 설명

HLD ↔ Code Consistency Check는 HLD 문서와 실제 Code 구현이 일치하는지 확인하는 Workflow이다.
기능 변경 후 Code는 업데이트되었지만 HLD가 갱신되지 않거나, HLD에는 설계가 존재하지만 실제 구현에서 누락되는 경우를 검출한다.

### 5.3 Expected Benefit

```text
설계 최신화; 문서 품질 향상; Code와 HLD 간 불일치 감소; Review 품질 향상; 신규 인원 이해도 향상; 기능 변경 이력 추적 강화
```

### 5.4 Precondition

```text
HLD 형식 표준화 필요; 5.2 Code Analyzer 구축 권장; Confluence Update 권한 필요 (현재 미확인 — 기본 구현에서는 로컬 출력으로 대체); Code 분석 범위 지정 필요
```

### 5.5 Storage / Reuse

```text
HLD Section; Code Path; API; Branch Condition; Gap Type; Suggested HLD Update; Confluence Link; Review Status; 다음 HLD 작성 시 Gap Pattern 재사용; Code Review 시 HLD 누락 검출
```

---

## 6. 연동 대상 시스템 기준

- Jira: 발견된 gap을 이슈화할 때 create 가능 범위로 사용한다. 기본은 dry-run preview이다.
- Confluence: HLD read는 가능 전제. HLD 문서 조회와 section 추출에 사용한다.
- Confluence write/update: 아직 미확인이므로 Suggested HLD Update를 로컬 Markdown으로 생성하고 실제 update는 TODO/옵션 처리한다.
- 코드 저장소: local path scan 기반으로 시작한다.

---

## 7. Python Package 기본 구조

Roo Code 또는 Claude Code는 아래 구조를 기준으로 기본 패키지를 생성한다.

```text
hld_code_consistency_check/
├─ README.md
├─ requirements.txt
├─ .env.template
├─ examples/
│  ├─ sample_input.md
│  └─ sample_output.md
├─ src/
│  └─ hld_code_consistency_check/
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
- HLD Confluence page URL 또는 exported markdown
- 코드 루트 경로
- 분석 대상 API/Module
- Gap detection 기준
- Jira 생성 여부
```

---

## 9. 출력값 기본틀

```text
- HLD-Code Gap Report Markdown
- Suggested HLD Update Markdown
- Jira 생성 preview
- Gap JSON
```

---

## 10. AI 구현 지시 프롬프트 초안

아래 프롬프트를 Roo Code 또는 Claude Code에 입력하여 구현을 시작한다.

```text
현재 작업은 MCP 설치나 MCP 설정 작업이 아니다.
ai-mcp-package-v1.0 기반 환경은 이미 준비되어 있다고 가정한다.

목표:
5.4 HLD ↔ Code Consistency Check 자동화 아이템을 Python 패키지 형태로 구현해줘.

기본 전제:
- Roo Code 또는 Claude Code에서 작업한다.
- Jira 생성은 가능하다.
- Confluence read는 가능하다.
- Confluence write/update는 아직 미확인이므로 실제 write는 구현하지 말고 TODO 또는 옵션 처리한다.
- 모든 외부 변경 작업은 기본적으로 dry-run을 먼저 제공한다.

구현 요구사항:
1. `hld_code_consistency_check` Python 패키지 구조를 생성한다.
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

```text
- 실제 Jira field mapping 확정
- 실제 Confluence page 구조 확정
- Confluence write/update 가능 여부 검증
- 사내 인증 방식별 예외 처리 추가
- 운영 로그 저장 방식 확정
- 결과물 저장 위치 확정
```
