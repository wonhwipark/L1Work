# 5.3 Weekly Report Collection — Python Package 구현 프롬프트 기본틀

---

## 1. 목적

이 문서는 [`master/L1_AI_Automation_Roadmap_v0.38.md`](L1a/master/L1_AI_Automation_Roadmap_v0.38.md) 의 `5.3 Weekly Report Collection` 항목을 Python 패키지로 구현하기 위한 AI 작업 프롬프트 기본틀이다. 5.3은 Child Page 탐색을 직접 수행하지 않고, pre 단계가 생성한 `weekly_report_draft_<YYYYMMDD>_<HHMM>_KST.md`를 입력으로 받아 이전 주 양식을 적용한 final 보고서를 생성한다.

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

- GPT + 사용자는 Weekly Report Collection의 업무 흐름, 입력 profile, 결과물 품질 기준을 정한다.
- Roo Code / Claude Code는 현재 Confluence 접근 방식, 초안 생성 흐름, 저장 포맷을 최적화한다.
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
5.3-pre weekly_report_draft 입력
  ↓
Previous Week Page Confluence Link 기준 이전 주 양식 참조
  ↓
취합 원본 draft를 이전 주 양식에 맞춰 정리
  ↓
이번 주 TL 주간보고 final 작성
  ↓
Group Report
```

### 5.2 설명

Weekly Report Collection은 5.3-pre 단계에서 생성한 Child Page 본문 취합 원본 draft를 입력으로 받고, Previous Week Page Confluence Link를 통해 이전 주 주간보고 양식을 참조하여 이번 주 TL 주간보고 final을 작성하는 Workflow이다.
Child Page 탐색과 본문 취합은 pre 단계에서 수행하며, 5.3은 draft 내용을 이전 주 양식에 맞춰 정리하고 이번 주 보고서를 생성한다.
이 과정은 반복성이 높고 누락 가능성이 있으므로 자동화 가치가 크다.

### 5.3 Expected Benefit

```text
반복 업무 감소; 작성 누락 검출; 이전 주 양식 기반 일관성 유지; 주간보고 정리 시간 단축; 주차별 History 축적; TL 보고 초안 작성 시간 감소
```

### 5.4 Precondition

```text
Confluence MCP 인증 필요; Main Page와 Child Page 구조 확인 필요; 개인별 주간보고 Page Naming Rule 확인 필요; Group Report 형식 정의 필요
```

### 5.5 Storage / Reuse

```text
Weekly Report; Risk Trend; Action Item; History; 작성자; 주차; Confluence Link; 다음 주 Risk Trend 비교; 지연 Action Item 추적; 반복 Risk 검출
```

---

## 6. 연동 대상 시스템 기준

- Jira: 추출된 Action Item을 Jira로 생성하는 기능은 가능 범위에 포함하되 dry-run 우선으로 구현한다.
- Confluence: read는 가능 전제. 5.3에서는 Previous Week Page Confluence Link를 읽어 이전 주 양식 참조에 사용한다. Child Page 탐색/본문 취합은 pre 단계 산출물 draft를 사용한다.
- Confluence write/update: 아직 미확인이므로 TL final은 로컬 Markdown으로 생성하고, 업로드는 TODO 또는 옵션 처리한다.

---

## 7. Python Package 기본 구조

Roo Code 또는 Claude Code는 아래 구조를 기준으로 기본 패키지를 생성한다.

```text
weekly_report_collection/
├─ README.md
├─ requirements.txt
├─ .env.template
├─ examples/
│  ├─ sample_input.md
│  └─ sample_output.md
├─ src/
│  └─ weekly_report_collection/
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

매주 사용자가 제공하는 필수 입력:

```text
- Current Week (예: W23)
- Pre 단계 산출물 draft 경로: `%USERPROFILE%\artifacts\weekly_report_draft_<YYYYMMDD>_<HHMM>_KST.md`
- Previous Week Page Confluence Link
- dry-run (기본값: true)
```

선택 입력:

```text
- 이번 주 Parent Page Confluence Link (추적/메타데이터 기록용. Child Page 탐색에는 사용하지 않음)
```

팀원 목록은 사용하지 않는다.

```text
- members.yaml 없음
- missing member detection 없음
- pre 단계 draft에 취합된 실제 Child Page 내용만 사용
```

### 8.1 Pre 단계 draft 입력 로직

5.3은 Child Page 탐색을 직접 수행하지 않고, 5.3-pre가 생성한 `weekly_report_draft_<YYYYMMDD>_<HHMM>_KST.md`를 입력으로 사용한다.

우선순위:

```text
1. 사용자가 지정한 draft 파일 경로가 있으면 해당 파일 사용
2. 지정이 없으면 %USERPROFILE%\artifacts 아래의 최신 weekly_report_draft_<YYYYMMDD>_<HHMM>_KST.md 사용 여부를 사용자에게 확인
3. draft 파일이 없으면 5.3-pre Child Page Collection 수행이 필요하다고 안내하고 중단
4. 5.3 내부에서 Child Page discovery를 fallback으로 수행하지 않는다
```

**반드시** 적용된 draft 파일 경로와 Previous Week Page Confluence Link를 실행 로그에 출력한다.

```text
[INFO] Weekly report draft loaded: C:\Users\whpark\artifacts\weekly_report_draft_20260618_0030_KST.md
[INFO] Previous week page link: <previous_week_page_confluence_link>
```

이를 통해 사용자가 어느 pre 산출물과 이전 주 양식이 적용됐는지 확인할 수 있도록 한다.

---

## 9. 출력값 기본틀

5.3-pre의 `weekly_report_draft_<YYYYMMDD>_<HHMM>_KST.md`는 입력 산출물이다. 5.3의 필수 산출물은 아래 final Markdown이다.

```text
%USERPROFILE%\artifacts\weekly_report_final_<YYYYMMDD>_<HHMM>_KST.md
```

별도의 `weekly_report_source_<YYYYMMDD>_<HHMM>_KST.json` 산출물은 생성하지 않는다.

Artifact 기준 경로는 `config.py`의 `ARTIFACTS_BASE_DIR`에서 `%USERPROFILE%\artifacts`를 기본값으로 주입한다.  
(`5_0_common_automation_framework.md` §5.0.8 참조)

---

## 10. AI 구현 지시 프롬프트 초안

아래 프롬프트를 Roo Code 또는 Claude Code에 입력하여 구현을 시작한다.

```text
현재 작업은 MCP 설치나 MCP 설정 작업이 아니다.
ai-mcp-package-v1.0 기반 환경은 이미 준비되어 있다고 가정한다.

목표:
5.3 Weekly Report Collection 자동화 아이템을 Python 패키지 형태로 구현해줘.
5.3-pre 단계가 생성한 weekly_report_draft를 입력으로 받고, Previous Week Page Confluence Link에서 이전 주 양식을 참조하여 이번 주 TL 주간보고 final Markdown을 작성하는 것이 핵심이다.

기본 전제:
- Roo Code 또는 Claude Code에서 작업한다.
- Jira 생성은 가능하다.
- Confluence read는 가능하다. 단, 5.3에서는 Previous Week Page Confluence Link의 양식 참조에 사용하고, Child Page 탐색은 직접 수행하지 않는다.
- Confluence write/update는 아직 미확인이므로 실제 write는 구현하지 말고 TODO 또는 옵션 처리한다.
- 모든 외부 변경 작업은 기본적으로 dry-run을 먼저 제공한다.
- Child Page 탐색 및 naming rule 검증은 5.3-pre 단계 책임이며, 5.3은 pre 단계 draft를 입력으로 처리한다.

구현 요구사항:
1. `weekly_report_collection` Python 패키지 구조를 생성한다.
2. `README.md`에 목적, 실행 방법, 입력값, 출력값, dry-run 사용법을 작성한다.
3. `requirements.txt`를 작성한다.
4. `.env.template`에는 필요한 환경 변수 이름만 정의하고 실제 값은 넣지 않는다.
5. `config.py`에서 환경 변수와 실행 옵션을 로딩한다. pre 단계 draft 경로, Previous Week Page Confluence Link, artifacts 출력 경로를 파라미터로 포함한다.
6. `models.py`에 입력/출력 데이터 구조를 정의한다. pre draft에서 파싱한 개인별 주간보고 항목, 이전 주 양식, 이번 주 final 보고서를 포함한다.
7. `clients/jira_client.py`는 Jira create/read/update가 필요한 경우의 wrapper 기본틀만 만든다.
8. `clients/confluence_client.py`는 Confluence read wrapper 기본틀을 만든다. Previous Week Page Confluence Link 조회와 양식 추출을 포함한다.
9. Confluence write/update가 필요한 경우 실제 구현 대신 `NotImplementedError` 또는 명시적 TODO로 남긴다.
10. `workflow.py`에 업무 흐름을 함수 단위로 구현한다. pre draft 로딩 → Previous Week Page 양식 참조 → 이번 주 final 작성 순서로 구성한다.
11. `main.py`에서 CLI 또는 단순 실행 entry point를 제공한다.
12. `--dry-run` 옵션을 기본 동작으로 둔다.
13. 실제 Jira 생성이 필요한 경우 생성 전 preview를 출력한다.
14. `examples/sample_input.md`와 `examples/sample_output.md`를 작성한다.
15. `tests/test_dry_run.py`에 외부 시스템 변경 없이 실행 가능한 최소 테스트를 작성한다.

완료 조건:
- pre 단계 weekly_report_draft 로딩 및 파싱 가능
- Previous Week Page Confluence Link 기반 이전 주 양식 참조 및 이번 주 final 생성 가능
- dry-run 실행 가능
- Confluence read 호출부 분리(Previous Week Page 양식 참조 중심)
- Confluence write/update는 미확인 상태로 안전하게 분리
- README만 보고 다음 작업자가 이어서 구현 가능
```

---

## 11. 검증 기준

```text
- 패키지 구조가 생성되어야 한다.
- dry-run 실행 경로가 있어야 한다.
- 실제 Jira 생성 전 preview가 있어야 한다.
- Confluence read(Previous Week Page 양식 참조)와 write/update가 명확히 분리되어야 한다.
- Confluence write/update는 현재 미확인 상태로 표시되어야 한다.
- 외부 시스템 변경 없이 test_dry_run.py가 실행 가능해야 한다.
```

---

## 12. 추후 보완 항목

```text
- 이전 주 양식 참조 방식 확정 (Confluence URL vs 로컬 Markdown)
- Confluence write/update 가능 여부 검증 후 초안 업로드 기능 추가
- 사내 인증 방식별 예외 처리 추가
- final 결과물 저장 위치 확정
```
