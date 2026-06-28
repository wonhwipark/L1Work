---
name: code-analyzer
description: Analyze C/C++ telecom L1 (LTE/NR) source code into HLD-style markdown with PlantUML MSC, at any scale — a single API, one block, or a large multi-file module. Covers staged structure extraction, per-procedure call-flow tracing across IPC REQ/CNF boundaries, and MSC generation. Use this whenever the user wants to understand, document, reverse-engineer, or produce an HLD/MSC for L1 code, mentions a block name or API to analyze, refers to "Track A/B", "Phase 0/1/F", "structure.json", "call flow", "IPC REQ/CNF", "slug", or asks to resume or switch a code-analysis run. Prefer this skill over ad-hoc code reading for any block-to-HLD or API-to-call-flow task, even if the user does not say the word "skill".
---

# code-analyzer

L1 채널 모뎀 C/C++ 코드를 작은 단위(단일 API)부터 큰 단위(다파일 모듈)까지 일관된 방식으로 분석해 HLD성 markdown + PlantUML MSC를 만든다. 이 스킬 하나로 전 규모를 커버한다.

이 문서는 워크플로우 전체를 담는다. 사용자는 `/code-analyzer`로 호출하거나 자연어로 "이 블록 분석해줘"라고 말하면 된다. 별도의 부트스트랩 붙여넣기는 필요 없다 — 아래 "세션 불변 규칙"이 항상 적용된다.

---

## 0. 세션 불변 규칙 (항상 적용 — 별도 붙여넣기 불필요)

이 스킬이 활성화되면 아래 규칙이 자동으로 적용된다. 과거에는 `copy_session_bootstrap.md`를 수동으로 붙여넣어야 했지만, 이제 스킬 본문에 내장되어 자동 적용된다.

경로
1. 모든 산출물 경로는 `output/5.2/<slug>/` 로 통일한다.
2. `artifacts/code_analyzer`, `%USERPROFILE%\artifacts\code_analyzer`, `artifacts/5.2` 경로는 사용하지 않는다.
3. `NEXT_STEP_5.2.md`는 항상 canonical path 기준으로 갱신한다.
4. overwrite 금지. 재생성이 필요하면 새 KST timestamp 파일을 만든다.

추출/상태
5. `extraction_mode`는 `git | bash | powershell | internal_search | mixed` 중 하나만 쓴다.
6. fallback 순서는 `git → bash → powershell → internal_search → mixed`.
7. 모든 응답 마지막은 token progress cursor로 끝낸다. 산문형 진행줄은 금지.
8. 진행줄 다음 줄에 다음 행동을 한 줄로 안내한다(스킬이 자동 진행하므로 "다음 단계 자동 실행" 형태로 안내).

런타임 토큰 절감
9. structure 자동 탐색은 focused 우선, full은 300KB 이하만 자동 사용.
10. Phase 1은 `analysis_progress.md`에 `procedure_runtime_index`를 반드시 생성한다.
11. Phase 2..N은 `procedure_runtime_index`의 해당 procedure slice만 읽는다.
12. `index_status`가 READY이면 structure json을 다시 읽지 않는다. INDEX_INCOMPLETE일 때만 targeted fallback read.
13. 전역 confirmed call edges 누적 본문 블록은 만들지 않는다. procedure별 local_call_edges + 전역 id 요약만.
14. MSC는 HLD md에 inline하지 않고 별도 `msc_<procedure_slug>_<ts>.puml`로 저장. HLD md에는 msc_ref 링크와 산문만.

분석 안전
15. 한 번에 procedure 하나만 분석한다. DONE procedure는 재분석하지 않는다.
16. CNF handler는 단일로 가정하지 않는다. `ipc_cnf_handlers[]` 후보로 두고 procedure별로 확정한다.
17. 미확인 flow는 추측하지 말고 `[RN]`으로 남긴다.

입력 편의 (사람이 적을 값 최소화)
18. slug는 Phase 0에서 한 번 확정하면 `NEXT_STEP_5.2.md`의 `current_slug`에 기록하고, 이후 단계는 자동 승계한다.
19. `<YYYYMMDD_HHMM_KST>` 타임스탬프는 사람이 적지 않는다. 새 파일 생성 시 도구가 현재 KST로 채운다.
20. structure_json은 사람이 파일명을 적지 않는다. `output/5.2/<slug>/`에서 최신 `*_focused.json`을 자동 선택한다.

---

## 1. 호출과 자동 진입 판단

사용자가 `/code-analyzer` 또는 "이 블록/이 API 분석해줘"로 진입하면:

1. **상태 먼저 확인** — `NEXT_STEP_5.2.md`와 `current_run` 성격의 진행 상태를 읽는다. 진행 중인 블록이 있으면 "이어하기(resume)"인지 "새 분석"인지 사용자 의도로 판별한다(모호하면 한 줄로 묻는다).
2. **새 분석이면 입력 확인** — 코드 루트와 분석 대상(블록명 또는 API명)만 받으면 된다. 나머지(slug, structure 경로, 타임스탬프)는 자동.
3. **자동 규모 판별(§2)로 Track A/B를 결정**하고 곧바로 실행한다.

사용자에게 필요한 최소 입력은 **코드 루트 + 분석 대상** 둘뿐이다. slug를 직접 주고 싶으면 줄 수 있으나 선택이다.

---

## 2. Track A/B 자동 판별 (코드 내용을 읽지 않는 메타 스캔)

대형 코드에서 토큰을 아끼려면 Track B(정적 구조 추출) 선행이 유리하다. 어느 쪽인지는 **파일 수·LOC만 세어** 자동 결정한다. **이 카운트는 코드 본문을 컨텍스트에 올리지 않으므로 토큰 비용이 사실상 0이다.**

스캔 방법 (분석 확장자 `.c .cpp .h .hpp`, 제외 폴더 `test/ third_party/ build/`). 환경에 따라 아래 fallback 순서(`git → bash → powershell → internal_search → mixed`)로 **사용 가능한 첫 번째 방법**을 쓴다. 어느 방법을 썼는지 `extraction_mode`로 기록한다. 모든 방법은 파일 목록·줄 수만 세고 코드 본문은 읽지 않는다.

현재 사내 코드 관리는 Perforce(d)이고, 추후 git(a)으로 전환 예정이다. 두 경로를 모두 지원하므로 전환 전후 어느 환경에서도 자동 판별이 동작한다.

a. git 저장소인 경우 (`extraction_mode: git`) — **권장 1순위**

향후 코드 관리가 Perforce에서 git으로 전환되면 이 경로가 기본이 된다. coreutils(`wc`/`xargs`)가 함께 있으면(Git Bash/WSL/Linux):

```bash
git -C "<root>" ls-files '*.c' '*.cpp' '*.h' '*.hpp' | grep -vE '(^|/)(test|third_party|build)/' > /tmp/ca_files.txt
wc -l < /tmp/ca_files.txt                  # 파일 수
xargs wc -l < /tmp/ca_files.txt | tail -1   # 총 LOC
```

Windows에서 `git`은 PATH에 있으나 `wc`/`xargs`가 없을 수 있다(Git for Windows의 coreutils는 Git Bash 안에서만 동작). 이때는 **파일 목록만 `git ls-files`로 받고 LOC는 PowerShell로 집계**한다(`extraction_mode: git` 유지, 집계 보조만 powershell):

```powershell
$root = "<root>"
$files = git -C $root ls-files '*.c' '*.cpp' '*.h' '*.hpp' |
  Where-Object { $_ -notmatch '(^|/)(test|third_party|build)/' }
$fileCount = $files.Count
$totalLoc  = ($files | ForEach-Object { Join-Path $root $_ } | Get-Content | Measure-Object -Line).Lines
"files=$fileCount loc=$totalLoc"
```

b. bash/coreutils가 있고 git이 아닌 경우 (`extraction_mode: bash`)

```bash
find "<root>" -type f \( -name '*.c' -o -name '*.cpp' -o -name '*.h' -o -name '*.hpp' \) \
  -not -path '*/test/*' -not -path '*/third_party/*' -not -path '*/build/*' > /tmp/ca_files.txt
wc -l < /tmp/ca_files.txt
xargs wc -l < /tmp/ca_files.txt | tail -1
```

c. Windows PowerShell만 있고 git도 아닌 경우 (`extraction_mode: powershell`)

git도 coreutils(find/wc)도 없고 git 저장소도 아닌 경우, PowerShell 네이티브 파일시스템 스캔으로 센다.

```powershell
$root = "<root>"
$exclude = '\\(test|third_party|build)\\'
$files = Get-ChildItem -Path $root -Recurse -File -Include *.c,*.cpp,*.h,*.hpp |
  Where-Object { $_.FullName -notmatch $exclude }
$fileCount = $files.Count
$totalLoc  = ($files | Get-Content | Measure-Object -Line).Lines
"files=$fileCount loc=$totalLoc"
```

참고: `Get-Content`은 줄 수만 세고 본문을 분석 컨텍스트로 끌어오지 않는다. 매우 큰 트리(수천 파일)에서 LOC 합산이 느리면, 파일 수만 먼저 보고(`$fileCount`) 대형이 명백하면 LOC 합산을 생략한 채 Track B로 진행해도 된다.

d. Perforce(p4) 작업공간인 경우 (`extraction_mode: internal_search` 또는 `mixed`)

git 전환 전까지의 현재 사내 환경이다. p4 메타데이터로 파일 목록을 받고 LOC는 PowerShell로 보조 집계한다.

```powershell
# 대상 경로 하위의 관리 파일 목록 (depot 동기화된 워크스페이스 기준)
$files = (p4 files "<root>/...") -split "`n" |
  Where-Object { $_ -match '\.(c|cpp|h|hpp)#' -and $_ -notmatch '(test|third_party|build)/' }
$fileCount = $files.Count
"files=$fileCount (LOC는 필요 시 PowerShell c 방법으로 보조 집계)"
```

p4가 인증/티켓 문제로 막히면 c 방법(PowerShell 파일 시스템 스캔)으로 폴백한다. 어떤 경로로도 셀 수 없으면 자동 판별을 포기하고 사용자에게 Track A/B를 직접 묻는다.

판정 기준 (START_HERE §4와 동일):

| 측정 결과 | 결정 |
|---|---|
| 특정 API 하나만 분석 | **Track A 바로** (규모 무관) |
| 파일 ≤ 10 | **Track A 바로** |
| 파일 ≥ 20 또는 LOC ≥ 5,000 | **Track B 선행** |
| 코드루트 전체가 수백~수천 파일 | **Track B 선행** |
| 어느 블록인지 모름 | **Track B**로 후보 구조 먼저 |

경계 처리 (중요): **파일 수가 11~19 구간이거나, 파일 수는 적지만 단일 파일이 매우 큰 경우(예: 한 파일 LOC ≥ 2,000)에는 자동 단정하지 말고** 추천 + 한 줄 확인을 한다. 예: "파일 14개·LOC 6.1k → Track B 선행을 권장합니다. 그대로 진행할까요, Track A로 바로 갈까요?" 명확한 구간에서는 묻지 않고 자동 진행한다.

자동 판별이 안전한 이유: 메타 스캔은 0토큰·1초 미만이고, 경계값에서만 사람을 한 번 거치므로 오판 비용이 낮다.

---

## 3. 단계 워크플로우

각 단계의 상세 규칙은 `references/`에 있다. 스킬은 현재 progress_cursor에 따라 **다음 단계를 자동으로 이어서 실행**한다(사용자가 매번 다음 프롬프트를 붙여넣을 필요 없음). 단, 사용자 판단이 필요한 지점(procedure 범위 선택, 경계값 Track 결정, 블록 전환)에서는 멈추고 묻는다.

```text
(자동 규모 판별)
  → [대형] Track B 정적추출  → references/track_b.md
  → Phase 0 구조맵          → references/phase0.md
  → Phase 1 procedure 발견 + procedure_runtime_index → references/phase1.md
  → Phase 2..N procedure별 call flow + MSC (한 번에 하나) → references/next_procedure.md
  → Phase F 블록 HLD 마무리  → references/phase_f.md
(중단/이어하기)                → references/resume.md
(블록 전환/복귀)               → references/block_switch.md
```

진행 상태 키:

```text
SESSION_READY → TRACKB_DONE → PHASE0_DONE → PHASE1_DONE
→ PROC_NEXT:<slug> (반복) → PHASEF_FINALIZE → BLOCK_HLD_DONE:<slug>
```

---

## 4. 블록/API 전환과 복귀 (v0.5 신규)

실사용에서 A→B→C procedure를 분석하던 중 다른 블록 T를 급히 봐야 할 수 있다. T 확인 후 원래 자리(C→D)로 돌아와야 한다. 각 블록 상태는 `output/5.2/<slug>/`에 폴더로 분리되어 쌓이므로, 전환은 **slug 전환 + 복귀 스택**으로 안전하게 처리된다. 상세는 `references/block_switch.md`.

핵심 동작:
- 전환 시 현재 블록의 progress_cursor를 그 블록의 `analysis_progress.md`에 보존하고, `NEXT_STEP_5.2.md`의 `block_stack`에 push한 뒤 새 slug로 분기한다.
- 새 블록 분석이 끝나거나 사용자가 "원래대로"라고 하면 `block_stack`에서 pop해 이전 slug·cursor로 복귀한다.
- 이미 분석된 블록은 output에 남아 있으므로, 같은 블록으로 다시 들어가면 처음부터가 아니라 저장된 cursor에서 이어간다.

---

## 5. 산출물 레이아웃 (스킬 소유)

```text
output/5.2/<slug>/
├── analysis_progress.md                         # 진행 상태 + procedure_runtime_index
├── structure_<ts>_focused.json                  # focused 구조 (자동 read 대상)
├── structure_<ts>_full.json                     # 선택, 300KB 초과 시 자동 read 제외
├── hld_<block_or_proc>_<ts>.md                  # HLD성 md (MSC inline 금지, msc_ref만)
└── msc_<procedure_slug>_<ts>.puml               # procedure별 MSC (별도 파일)
```

`analysis_progress.md`는 사람이 직접 편집하지 않는다. 단, procedure 범위 선택과 머지 판단은 사용자가 결정한다.

---

## 6. reference 파일 안내

필요한 단계의 파일만 읽는다(progressive disclosure).

| 파일 | 언제 읽나 |
|---|---|
| `references/track_b.md` | 대형 코드 정적 구조 추출 |
| `references/phase0.md` | 구조맵 생성 (Track A 시작) |
| `references/phase1.md` | procedure 발견 + runtime index |
| `references/next_procedure.md` | procedure 하나 분석 (반복) |
| `references/phase_f.md` | 블록 HLD 마무리 |
| `references/resume.md` | 중단 후 이어하기 |
| `references/block_switch.md` | 블록/API 전환·복귀 |

`prompt/5.2_track_a_prompt.md` / `prompt/5.2_track_b_prompt.md`(reference 원문)는 런타임에 읽지 않는다.
