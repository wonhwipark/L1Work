# CodeAnalyzer Standalone — 새 사용자 빠른 시작

버전: v0.8 manifest guard 릴리스  
갱신: 2026-06-27 10:38 KST  
스킬: `code-analyzer` (`/code-analyzer`)

이 패키지는 L1 코드의 특정 블록/API를 분석해 HLD성 문서와 MSC PlantUML 파일을 생성하기 위한 Claude Code 스킬 패키지다.

---

## 1. 처음이면 이 순서만 따른다

```powershell
# 1) ZIP 압축 해제 후 이 폴더로 이동
cd .\CodeAnalyzer_standalone

# 2) 스킬 설치
.\install_skill.ps1

# 3) 설치 확인
.\validate_install.ps1
```

설치 후 Claude Code 또는 VSCode를 재시작한다.

Claude Code에서 호출한다.

```text
/code-analyzer
```

그 다음 아래처럼 요청한다.

```text
C:\path\to\source 에서 <블록명 또는 API명> 분석해줘
```

사용자가 준비할 값은 **코드 루트**와 **분석 대상**뿐이다.

---

## 2. 문서 역할

| 문서 | 언제 보는가 |
|---|---|
| `README.md` | ZIP을 처음 받은 사람이 가장 먼저 본다. |
| `START_HERE_5.2.md` | 정상 사용 흐름을 짧게 확인한다. |
| `INSTALL_SKILL.md` | 설치 옵션, 경로 직접 지정, 재설치를 확인한다. |
| `USER_GUIDE_5.2.md` | 설치 후 실제 분석 요청 방법을 확인한다. |
| `NEXT_STEP_5.2.md` | 현재 상태와 다음 한 걸음을 확인한다. |
| `RUNBOOK_BLOCK_TO_HLD_5.2.md` | 실행 중 막혔을 때 증상별 조치를 확인한다. |
| `VERSION_5.2.md` | 변경 이력을 확인한다. |
| `HANDOFF_5.2.md` | 설계 이력/유지보수용이다. 일반 사용자는 보통 보지 않는다. |

`prompt/` 폴더는 스킬 설치가 불가능한 환경의 레거시 수동 모드다. 정상 사용자는 열지 않는다.

---

## 3. 결과물 위치

분석 결과는 항상 아래에 저장한다.

```text
output/5.2/<slug>/
```

대표 결과물:

```text
analysis_progress.md
structure_<YYYYMMDD_HHMM_KST>_focused.json
procedure_runtime_index
msc_<procedure_slug>_<YYYYMMDD_HHMM_KST>.puml
hld_<slug>_<YYYYMMDD_HHMM_KST>.md
```
