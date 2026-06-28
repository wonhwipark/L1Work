# Review Log — CodeAnalyzer Standalone v0.5 (code-analyzer 스킬화)

생성: 2026-06-26 08:13 KST  
기준 패키지: CodeAnalyzer_standalone v0.4

---

## 1. 배경 — 사용자 4개 질문

```text
1. prompt/ 폴더를 ~/.claude/skills/code-analyzer 로 이동 가능한가?
2. 최초 시작 프롬프트가 뭔가? /code-analyzer 바로 못 쓰나? 부트스트랩 자동실행 안 되나?
3. 작은 블록/대형 코드 자동 구분 안 되나?
4. next 반복 중 다른 블록/API를 새로 시작하고, 확인 후 이전 상태로 복귀 가능한가?
```

근본 원인: v0.4까지는 copy prompt가 "사내 설치된 staged-code-analyzer 스킬을 사람이 자연어로 호출"하는 대본 묶음이었다. 자동화 한계가 여기서 왔다. v0.5에서 **copy prompt 묶음을 실제 스킬로 승격**해 4개를 한 번에 해결했다.

---

## 2. 질문 1 — 스킬화 (단순 이동이 아니라 패키징)

`prompt/`를 그대로 옮기면 안 된다(`SKILL.md` 진입점이 없어 Claude Code가 스킬로 인식 못 함). copy prompt들의 규칙을 흡수해 정식 스킬로 만들었다.

```text
skills/code-analyzer/
├── SKILL.md                       # 세션 불변 규칙 + 호출/자동판별/워크플로우/블록전환 (158줄)
└── references/
    ├── track_b.md                 # copy_track_b 흡수
    ├── phase0.md                  # copy_phase0 흡수
    ├── phase1.md                  # copy_phase1 흡수 (procedure_runtime_index)
    ├── next_procedure.md          # copy_next_procedure 흡수
    ├── phase_f.md                 # copy_phase_f 흡수
    ├── resume.md                  # copy_resume 흡수
    └── block_switch.md            # 신규 — 블록 전환/복귀
```

스킬 이름: 기존 `staged-code-analyzer` → **`code-analyzer`**로 개명·승격. 사용자 요청대로, 작은 단위(단일 API)부터 큰 단위(다파일 모듈)까지 전부 커버하는 이름이다. 패키지 전 문서의 `staged-code-analyzer` 참조도 `code-analyzer`로 갱신(review_logs history 제외).

설치는 패키지가 스킬을 **포함**하므로 복사 1회로 끝난다(START_HERE §5).

```powershell
Copy-Item -Recurse -Force ".\skills\code-analyzer\*" "$env:USERPROFILE\.claude\skills\code-analyzer"
```

## 3. 질문 2 — 즉시 호출 + 부트스트랩 자동

```text
- /code-analyzer 로 바로 호출 가능(이제 그 이름의 스킬이 존재).
  또는 자연어 "이 코드루트의 <블록/API> 분석해줘".
- copy_session_bootstrap 규칙 21개를 SKILL.md §0 "세션 불변 규칙"으로 내장.
  → 세션 시작 시 부트스트랩 붙여넣기 불필요. 스킬 활성화 시 자동 적용.
```

## 4. 질문 3 — Track A/B 자동 판별 (토큰 0)

코드 본문을 읽지 않고 **파일 수·LOC만 메타 스캔**으로 결정한다. 카운트는 컨텍스트에 코드를 올리지 않으므로 토큰 비용 사실상 0, 1초 미만.

스캔은 환경별 fallback(`git → bash → powershell → internal_search/p4 → mixed`)으로 **사용 가능한 첫 방법**을 쓴다. 현재 사내는 Perforce(d)이고 추후 git(a)으로 전환 예정이라 두 경로를 모두 지원한다. Windows에서 git만 있고 coreutils(wc)가 없는 경우를 위해 git+PowerShell 하이브리드도 둔다.

```text
a. git         : git ls-files + wc  (권장 1순위, git 전환 후 기본)
   git(win)    : git ls-files + PowerShell Measure-Object  (Windows에 wc 없을 때)
b. bash        : find + wc  (Git Bash/WSL/Linux, git 아님)
c. powershell  : Get-ChildItem + Measure-Object -Line  (Windows, git 아님)
d. p4          : p4 files + PowerShell 보조 집계  (현재 사내, internal_search/mixed)
```

어떤 방법을 썼는지 extraction_mode로 기록. 어느 경로로도 못 세면 자동 판별을 포기하고 사용자에게 직접 묻는다.

```text
파일 ≤10 또는 단일 API     → Track A 바로
파일 ≥20 또는 LOC ≥5,000   → Track B 선행
11~19 구간 / 단일 거대파일  → 추천 + 한 줄 확인(경계 오판 방지)
```

자동 단정이 위험한 경계값에서만 사람을 한 번 거치므로 오판 비용이 낮다. 상세 SKILL.md §2.

## 5. 질문 4 — 블록/API 전환 + 복귀

각 블록 상태가 `output/5.2/<slug>/`에 폴더로 분리되어 쌓이는 구조를 활용. `NEXT_STEP_5.2.md`에 `block_stack`(LIFO) 필드를 추가했다.

```text
A→B→C 분석 중 "T 먼저 봐줘"
  → push C(cursor=PROC_NEXT:proc_c), current_slug=T, Phase 0 시작   [BLOCK_SWITCH_PUSH]
T 확인 끝 → "원래대로"
  → pop → current_slug=C, cursor=PROC_NEXT:proc_c 에서 이어감        [BLOCK_SWITCH_POP]
```

핵심 안전장치: 전환·복귀로 어떤 블록의 DONE procedure도 재분석하지 않는다. 이미 분석한 블록으로 재진입하면 저장된 cursor에서 이어간다(처음부터 X). 상세 references/block_switch.md.

---

## 6. 수정/추가 파일

추가:

```text
skills/code-analyzer/SKILL.md
skills/code-analyzer/references/{track_b,phase0,phase1,next_procedure,phase_f,resume,block_switch}.md
review_logs/codeanalyzer_v0_5_skill_20260626_0813_KST.md
```

수정:

```text
VERSION_5.2.md             # v0.5 헤드라인
START_HERE_5.2.md          # §3 스킬 기반 순서표, §5 스킬 설치(포함본 복사), staged→code-analyzer
NEXT_STEP_5.2.md           # block_stack 필드, §2 스킬 호출 우선, 블록전환 상태전이
output/5.2/_example_slug/README.md  # 스킬명 갱신
prompt/copy_phase0.md, copy_track_b.md, 5.2_track_*.md  # 스킬명 staged→code-analyzer
HANDOFF_5.2.md             # 스킬명 갱신
```

미변경(하위 호환 + history):

```text
prompt/copy_session_bootstrap.md, copy_phase1.md, copy_next_procedure.md, copy_resume.md, copy_phase_f.md
  → 레거시 수동 경로로 그대로 유지(스킬 미설치 환경 대비)
RUNTIME_TOKEN_POLICY_5.2.md, schema/*, reference/*, output_layout/*
review_logs/ 기존 항목
```

---

## 7. 완료 기준

```text
- skills/code-analyzer/SKILL.md 존재, frontmatter 유효, 158줄(<500 목표 충족).
- references 7개 존재. 모든 copy prompt 규칙이 흡수됨.
- /code-analyzer 호출 + 부트스트랩 자동 적용이 SKILL.md에 명문화됨.
- Track A/B 자동 판별(메타 스캔, 경계 확인)이 SKILL.md §2에 정의됨.
- block_stack 기반 전환/복귀가 NEXT_STEP + block_switch.md에 정의됨.
- staged-code-analyzer 참조가 active 문서에 없음(전부 code-analyzer).
- 제어문자 0개. 레거시 copy prompt는 하위호환으로 보존.
```

---

## 8. 남은 미결 / 권장 다음 작업

```text
1. 실제 사내 L1 블록으로 스킬 E2E 검증(메타 스캔 판정, 블록 전환/복귀 동작 확인).
2. skill-creator의 eval로 /code-analyzer 트리거율 측정 후 description 튜닝(선택).
3. 보조 스킬(api-callflow-analysis, plantuml-msc)과의 호출 계약을 SKILL.md에 더 구체화할지 검토.
4. RCA 5.5 root_cause.code_ref 연결 계약(첫 HLD 산출물 이후).
```
