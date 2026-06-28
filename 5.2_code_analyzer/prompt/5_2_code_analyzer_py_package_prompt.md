⛔ **[DEPRECATED — v0.41부터 제거 예정]**

이 프롬프트는 **폐기 예정** 상태입니다.

- **신규 분석:** `5_2_code_analyzer_track_a_prompt.md` (권장) 또는 `5_2_code_analyzer_track_b_prompt.md` (사전 단계) 사용
- **현재 상태:** Historical record로 보존 (참고용만 사용)
- **제거 일정:** v0.41 (다음 마이너 버전) 이후

---

# 5.2 Code Analyzer — Python Package 구현 프롬프트 기본틀

---

## 1. 목적

이 문서는 [`master/L1_AI_Automation_Roadmap_v0.38.md`](L1a/master/L1_AI_Automation_Roadmap_v0.38.md) 의 `5.2 Code Analyzer` 항목을 Python 패키지로 구현하기 위한 AI 작업 프롬프트 기본틀이다.

HLD 문서 없이 코드만 존재하는 기존 구현을 분석하여, HLD(또는 구현문서) 초안과 업데이트 항목 목록을 자동으로 생성하는 것이 목표이다.

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

- GPT + 사용자는 Code Analyzer의 분석 목적, 산출물 범위, HLD 연계 방향을 정한다.
- Roo Code / Claude Code는 현재 환경 기준으로 분석 파이프라인, AST/정적분석 도구, 출력 포맷을 최적화한다.
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

## 5. 항목 정의

### 5.1 Workflow

```text
코드 루트 경로 + 분석 대상 지정
  ↓
코드 구조 분석 (함수/클래스/호출 관계/Branch 조건)
  ↓
Call Flow 추출
  ↓
HLD 업데이트 항목 목록 생성
  ↓
HLD 문서 초안 생성
  ↓
(선택) Confluence 업로드 또는 로컬 저장
```

### 5.2 설명

Code Analyzer는 HLD 없이 코드만 존재하는 기존 구현을 분석하여 HLD(또는 구현문서)를 문서화하는 Workflow이다.
개별 담당자가 자신의 담당 코드를 대상으로 직접 실행하며, 분석 결과로 HLD 업데이트 항목 목록과 HLD 문서 초안을 생성한다.
출력은 업데이트 항목 목록(항목 단위 정리)과 HLD 문서 초안(섹션 구조 포함) 두 가지를 모두 제공한다.

5.4 HLD ↔ Code Consistency Check와의 역할 구분:
- 5.2(Code Analyzer): HLD가 없는 상태 → 코드에서 HLD를 새로 만든다.
- 5.4(HLD ↔ Code Consistency Check): HLD가 이미 있는 상태 → 코드와 불일치를 찾는다.
두 항목의 Trigger 주체는 모두 개별 담당자이며 독립적으로 실행한다.

### 5.3 Expected Benefit

```text
HLD 미작성 코드의 문서화 부채 해소; 신규 인원 온보딩 지원; 코드 리뷰 품질 향상;
HLD 작성 시간 단축; Call Flow 가시화; 구현 의도 복원
```

### 5.4 Precondition

```text
분석 대상 코드 경로 지정 필요; 분석 언어/확장자 지정 필요; HLD 출력 템플릿 정의 필요;
독립 착수 가능 (다른 항목 선행 불필요)
```

### 5.5 Storage / Reuse

```text
HLD 업데이트 항목 목록; HLD 문서 초안; Call Flow MSC(PlantUML);
함수/클래스 구조 분석 결과; Branch 조건 목록;
5.4 Consistency Check 입력으로 재사용 가능;
5.5 RCA Knowledge Graph의 API 연결 정보로 재사용 가능;
5.6 Onboarding Knowledge Pack의 HLD 링크로 활용 가능
```

---

## 6. 연동 대상 시스템 기준

- Jira: 기본 구현 범위에서 실제 호출 없음. 향후 문서화 task 생성이 필요한 경우 확장 후보.
- Confluence: HLD 초안 업로드는 write/update 미확인 상태이므로 로컬 Markdown 파일로 우선 생성. 업로드는 TODO/옵션 처리.
- Perforce/코드 저장소: local path scan 기반으로 시작. 코드 파일은 로컬 경로 입력으로 처리.

---

## 7. Python Package 기본 구조

Roo Code 또는 Claude Code는 아래 구조를 기준으로 기본 패키지를 생성한다.

```text
code_analyzer/
├─ README.md
├─ requirements.txt
├─ .env.template
├─ examples/
│  ├─ sample_input.md
│  └─ sample_output.md
├─ src/
│  └─ code_analyzer/
│     ├─ __init__.py
│     ├─ config.py
│     ├─ models.py
│     ├─ clients/
│     │  ├─ __init__.py
│     │  └─ confluence_client.py
│     ├─ analyzer/
│     │  ├─ __init__.py
│     │  ├─ code_parser.py
│     │  ├─ call_flow_extractor.py
│     │  └─ hld_generator.py
│     ├─ workflow.py
│     └─ main.py
└─ tests/
   └─ test_dry_run.py
```

---

## 8. 입력값 기본틀

```text
- 코드 루트 경로
- 분석 대상 파일 확장자 (예: .c, .cpp, .h)
- 제외 폴더 목록
- 분석 시작점 함수 또는 모듈명 (선택)
- HLD 출력 템플릿 경로 (선택)
- 출력 폴더 경로
```

---

## 9. 출력값 기본틀

```text
- HLD 업데이트 항목 목록 Markdown
- HLD 문서 초안 Markdown (섹션 구조 포함)
- Call Flow MSC(PlantUML)
- 함수/클래스 구조 분석 결과 JSON
```

---

## 10. AI 구현 지시 프롬프트 초안

아래 프롬프트를 Roo Code 또는 Claude Code에 입력하여 구현을 시작한다.

```text
현재 작업은 MCP 설치나 MCP 설정 작업이 아니다.
ai-mcp-package-v1.0 기반 환경은 이미 준비되어 있다고 가정한다.

목표:
5.2 Code Analyzer 자동화 아이템을 Python 패키지 형태로 구현해줘.
HLD 없이 코드만 존재하는 기존 구현을 분석하여 HLD 업데이트 항목 목록과 HLD 문서 초안을 생성하는 것이 핵심이다.

기본 전제:
- Roo Code 또는 Claude Code에서 작업한다.
- Jira 연동은 기본 구현에서 제외한다.
- Confluence read는 가능하나 기본 구현에서는 사용하지 않는다.
- Confluence write/update는 아직 미확인이므로 HLD 초안은 로컬 Markdown으로 생성한다.
- 모든 분석 작업은 로컬 코드 경로 기반으로 동작한다.
- --dry-run 옵션은 분석만 수행하고 파일 출력을 생략하는 모드로 사용한다.

구현 요구사항:
1. `code_analyzer` Python 패키지 구조를 생성한다.
2. `README.md`에 목적, 실행 방법, 입력값, 출력값, dry-run 사용법을 작성한다.
3. `requirements.txt`를 작성한다.
4. `.env.template`에는 필요한 환경 변수 이름만 정의하고 실제 값은 넣지 않는다.
5. `config.py`에서 환경 변수와 실행 옵션을 로딩한다.
6. `models.py`에 입력/출력 데이터 구조를 정의한다. HLD 항목, Call Flow MSC(PlantUML), 함수 구조를 포함한다.
7. `analyzer/code_parser.py`는 코드 파일에서 함수/클래스/호출 관계를 추출하는 기본틀을 만든다.
8. `analyzer/call_flow_extractor.py`는 추출된 구조에서 Call Flow MSC(PlantUML)를 생성하는 기본틀을 만든다.
9. `analyzer/hld_generator.py`는 Call Flow MSC(PlantUML)와 구조 분석 결과를 기반으로 HLD 업데이트 항목 목록과 HLD 문서 초안을 생성하는 기본틀을 만든다.
10. `clients/confluence_client.py`는 Confluence read wrapper 기본틀을 만든다. write/update는 NotImplementedError 또는 명시적 TODO로 남긴다.
11. `workflow.py`에 전체 흐름(코드 분석 → Call Flow MSC(PlantUML) 생성 → HLD 항목 생성 → HLD 초안 생성)을 함수 단위로 구현한다.
12. `main.py`에서 CLI entry point를 제공한다.
13. `--dry-run` 옵션은 분석 결과를 콘솔에만 출력하고 파일 저장을 생략한다.
14. `examples/sample_input.md`와 `examples/sample_output.md`를 작성한다.
15. `tests/test_dry_run.py`에 외부 시스템 변경 없이 실행 가능한 최소 테스트를 작성한다.

완료 조건:
- 로컬 코드 경로를 입력받아 분석 가능
- HLD 업데이트 항목 목록 출력 가능
- HLD 문서 초안 Markdown 생성 가능
- dry-run 실행 가능
- README만 보고 다음 작업자가 이어서 구현 가능
```

---

## 11. 검증 기준

```text
- 패키지 구조가 생성되어야 한다.
- 로컬 코드 경로 입력으로 분석이 시작되어야 한다.
- HLD 업데이트 항목 목록이 Markdown으로 생성되어야 한다.
- HLD 문서 초안이 Markdown으로 생성되어야 한다.
- dry-run 실행 시 파일 저장 없이 콘솔 출력만 제공되어야 한다.
- 외부 시스템 변경 없이 test_dry_run.py가 실행 가능해야 한다.
```

---

## 12. 추후 보완 항목

```text
- 실제 분석 대상 언어별 파서 확정 (C/C++ 우선)
- HLD 출력 템플릿 확정 (팀 표준 양식 반영)
- Call Flow MSC(PlantUML) 출력 품질 고도화
- Confluence write/update 가능 여부 검증 후 업로드 기능 추가
- 사내 인증 방식별 예외 처리 추가
- 분석 결과 저장 위치 확정
```
