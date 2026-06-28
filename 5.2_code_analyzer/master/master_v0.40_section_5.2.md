# Master v0.40 Extract - 5.2 Code Analyzer

- 원본: `master/L1_AI_Automation_Roadmap_v0.40.md`
- 추출 기준: `### 5.2 Code Analyzer`부터 `### 5.3-pre Confluence Child Page Collection` 직전까지
- 경계 검토: 명확함

---

### 5.2 Code Analyzer

Code Analyzer는 HLD 없이 코드만 존재하는 기존 구현을 분석하여 **Call Flow의 가시화(Call Graph + MSC) 및 간단한 모듈 설명 문서**를 생성하는 Workflow이다.

특히 대용량 폴더(30분 이상의 분석 시간)를 처리할 때, §5.0.10 Staged Analysis 메커니즘을 사용하여 분석을 단계별로 나누고, Global CNF Carry를 통해 CNF 파일 분석 결과를 모든 단계에서 재사용한다.

#### 5.2.1 실행 옵션 (Execution Tracks)

Code Analyzer는 두 가지 Track으로 운영된다:

**Track A: Skill-based Staged Analysis (권장 — 메인 경로)**

```text
코드 루트 경로 + 분석 대상 폴더 + 단계 범위 지정
  ↓
[Phase 0] 전체 폴더 인벤토리 (함수/클래스/호출 계수)
  ↓
[Phase 1..N] 단계별 분석 (각 단계별 REQ-site 파일 그룹 분석)
  │  각 단계:
  │  - 대상 폴더 코드 구조 분석 (함수/클래스/호출 관계/Branch 조건)
  │  - Call Flow 추출 (IPC REQ 사이트 중심)
  │  - Global CNF Carry 체크포인트 적용 (CNF 처리 파일 재사용)
  │  - review_progress_<YYYYMMDD>_<HHMM>_KST.md 저장
  │
[Phase F] 전 Stage 결과 통합
  ↓
Call Flow MSC (PlantUML) 생성
  ↓
간단한 모듈 설명 문서 + JSON 메타데이터
  ↓
(선택) Confluence 업로드 또는 로컬 저장
```

**특징:**
- `staged-code-analyzer` Skill로 구현 (§5.0.9 Skill Layer)
- `5_2_code_analyzer_track_a_prompt.md`로 실행
- 대용량 폴더(30분+) 분석 시 문맥 초과 위험 방지
- Global CNF Carry: CNF 파일(IPC 응답)은 모든 Stage에서 동일하므로, 1회 분석 후 다음 Stage에서 재사용

**Track B: Static Extraction (선택적 — 사전 단계)**

```text
코드 루트 경로 지정
  ↓
Bash 프롬프트 기반 정적 구조 추출
  (find / wc / ctags / grep 등 기존 환경 활용)
  ↓
구조 JSON 생성 (module layout, function inventory, include hierarchy)
  ↓
Track A 입력으로 활용 (선택적)
```

**특징:**
- §5.0.5 "Prefer Existing Environment" 원칙 준수
- Python 패키지 불필요; bash 프롬프트 기반 실행
- `5_2_code_analyzer_track_b_prompt.md`로 실행
- Track A 진입 전 "코드 구조 전체 파악" 필요 시 사용 (선택적)
- 시간 효율: 구조 추출만 ~5분, HLD 산문 생성은 미단축

#### 5.2.2 Global CNF Carry 메커니즘

L1 모뎀 구현에서 IPC REQ/CNF는 다음과 같은 구조를 가진다:

- **IPC REQ 사이트:** 여러 파일에서 발생 (브랜치별로 다름)
- **IPC CNF 처리:** 특정 1개 파일에서만 처리 (모든 REQ의 응답 처리)

따라서 대용량 폴더를 Stage로 분할할 때:
1. **[Phase 1]** CNF 파일 포함 Stage에서 CNF 처리 로직을 완전히 분석 → review_progress_<YYYYMMDD>_<HHMM>_KST.md 체크포인트에 저장
2. **[Phase 2..N]** 이후 Stage에서는 CNF 분석 결과를 재사용 (CNF 파일 재분석 불필요)
3. **[Phase F]** 모든 Stage의 REQ + 공유 CNF 결과 통합 → 최종 Call Flow MSC 생성

#### 5.2.3 간단한 모듈 설명 문서 (Module Overview)

각 모듈당 50~100줄 분량의 Markdown 문서:
- **모듈 개요** (2~3줄): 모듈의 역할 한 문단
- **주요 책임** (bullet 2~3개): "REQ 처리", "CNF 응답", "타이밍 관리" 등
- **주요 함수/API** (리스트): 함수명 + 1줄 설명
- **주요 IPC 호출** (옵션): REQ/CNF 구분, 호출 순서

#### 5.2.4 Expected Benefit

- Call Flow 가시화 (MSC): 대용량 코드에서도 IPC 호출 흐름 시각화
- 구현 의도 복원: 간단한 모듈 설명으로 신규 인원 빠른 이해
- 문맥 초과 방지: Staged Analysis로 30분+ 분석도 완료
- 코드 리뷰 품질: Call Flow 이해 → 리뷰 포인트 명확화
- 후속 항목 입력: 5.4/5.5/5.6의 기반 자료 제공

#### 5.2.5 Precondition

- 분석 대상 코드 루트 경로, 단계별 폴더 범위(예: Phase 1: TxSwitchMngr/, Phase 2: TxCfgMngr/), 분석 대상 파일 확장자(.c, .h 등) 사전 확정 필요
- Track A 사용 시: Claude Code 또는 Roo Code 사용 가능
- Track B 사용 시: bash 환경 + find/wc/ctags/grep 기본 도구

#### 5.2.6 Storage / Reuse

- Call Flow MSC (PlantUML) — 5.4 Gap Detection, 5.5 RCA Knowledge Graph에 입력으로 재사용 가능
- 간단한 모듈 설명 문서 — 신규 인원 온보딩, 코드 리뷰 가이드, 5.6 Onboarding Knowledge Pack의 기반
- 구조 분석 메타데이터 (JSON) — 5.4 Consistency Check, 5.5 RCA Knowledge Graph의 API 연결 정보로 재사용 가능
- review_progress.md (Stage 체크포인트) — 재개 또는 다시 실행 시 Skip 지점 명시
