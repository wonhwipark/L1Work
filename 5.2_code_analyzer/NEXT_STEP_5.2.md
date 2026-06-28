# NEXT_STEP_5.2 — CodeAnalyzer 다음 행동

마지막 갱신: 2026-06-27 10:38 KST  
상태 파일: `NEXT_STEP_5.2.md` + `output/5.2/<slug>/analysis_progress.md`

---

## 1. 현재 상태

```text
current_block:             (없음)
current_slug:              (없음)
block_stack:               []
current_step:              INIT
next_step:                 INSTALL_OR_RUN_SKILL
canonical_path:            output/5.2/<slug>/
progress_cursor:           [진행: INIT → 다음: INSTALL_OR_RUN_SKILL]
```

---

## 2. 다음 한 걸음

### 스킬 미설치

```powershell
.\install_skill.ps1
.\validate_install.ps1
```

설치 후 Claude Code 또는 VSCode를 재시작한다.

### 스킬 설치 완료

```text
/code-analyzer
C:\path\to\source 에서 <블록명 또는 API명> 분석해줘
```

### 진행 중 이어하기

```text
/code-analyzer
이어서 진행해줘
```

---

## 3. 완료 후 기대 결과

```text
output/5.2/<slug>/analysis_progress.md
output/5.2/<slug>/structure_<YYYYMMDD_HHMM_KST>_focused.json
output/5.2/<slug>/msc_<procedure_slug>_<YYYYMMDD_HHMM_KST>.puml
output/5.2/<slug>/hld_<slug>_<YYYYMMDD_HHMM_KST>.md
```

---

## 4. 고정 규칙

```text
경로: output/5.2/<slug>/
진행줄: [진행: ... → 다음: ...]
structure: focused 우선, full은 명시 지정 시만
runtime read: procedure_runtime_index 우선
MSC: HLD md에 inline으로 넣지 않고 별도 .puml 생성
```

---

## 5. 막히면

`RUNBOOK_BLOCK_TO_HLD_5.2.md`를 본다.
