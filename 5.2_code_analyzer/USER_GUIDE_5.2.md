# USER_GUIDE_5.2 — code-analyzer 사용 가이드

버전: v0.7  
갱신: 2026-06-27 10:38 KST  
대상: L1 블록/API 분석 → HLD성 문서 + MSC PlantUML 생성

---

## 1. 이 스킬이 하는 일

`code-analyzer`는 코드 루트와 분석 대상만 받아 다음 산출물을 만든다.

```text
output/5.2/<slug>/analysis_progress.md
output/5.2/<slug>/structure_<KST>_focused.json
output/5.2/<slug>/msc_<procedure_slug>_<KST>.puml
output/5.2/<slug>/hld_<slug>_<KST>.md
```

일반 사용자는 `prompt/` 폴더를 열 필요가 없다.

---

## 2. 설치 확인

설치가 아직이면 먼저 `INSTALL_SKILL.md`를 따른다.

```powershell
.\install_skill.ps1
.\validate_install.ps1
```

설치 후 Claude Code 또는 VSCode를 재시작한다.

---

## 3. 블록 기준 분석

Claude Code에서 호출한다.

```text
/code-analyzer
```

요청 예시:

```text
C:\work\modem\l1 에서 TxSwitchMngr 블록 분석해줘
```

스킬 진행:

```text
1. 코드 루트 확인
2. 블록/API명으로 관련 파일 후보 탐색
3. 코드 규모 판별
4. 필요한 경우 focused structure 생성
5. procedure 목록 생성
6. procedure별 call flow 분석
7. MSC .puml 및 HLD md 생성
```

---

## 4. API 기준 분석

특정 함수 또는 메시지를 기준으로 볼 수도 있다.

```text
C:\work\modem\l1 에서 ProcPeriodicTxSwitch API 기준으로 full call flow와 MSC 만들어줘
```

API 기준 분석은 블록 분석의 부분집합이다. 결과는 동일하게 `output/5.2/<slug>/` 아래에 생성한다.

---

## 5. 대형 코드 처리

코드가 크면 사용자가 Track을 직접 고르지 않아도 된다. 스킬이 다음 기준으로 자동 선택한다.

| 상황 | 처리 |
|---|---|
| 작은 블록/API | 바로 focused 분석 |
| 20파일 이상 또는 5천 LOC 이상 | structure 추출 선행 |
| 수백~수천 파일 | 후보 파일 축소 후 분석 |

---

## 6. 이어하기

세션이 끊겼거나 멈췄으면 다시 호출한다.

```text
/code-analyzer
이어서 진행해줘
```

스킬은 아래 상태를 기준으로 복귀한다.

```text
NEXT_STEP_5.2.md
output/5.2/<slug>/analysis_progress.md
```

---

## 7. 분석 중 다른 블록을 잠깐 확인할 때

요청 예시:

```text
잠깐 AitMngr 쪽으로 전환해서 관련 call flow만 확인하고, 끝나면 원래 TxSwitchMngr 분석으로 돌아와줘
```

스킬은 기존 slug/cursor를 보존하고 새 블록을 분석한 뒤 복귀한다.

---

## 8. 결과 확인

| 파일 | 의미 |
|---|---|
| `analysis_progress.md` | 현재 진행 상태와 procedure별 요약 |
| `structure_*_focused.json` | 분석 대상 중심 구조맵 |
| `msc_*.puml` | procedure별 PlantUML MSC |
| `hld_*.md` | 최종 HLD성 설명 문서 |

---

## 9. 막혔을 때

증상별 조치는 `RUNBOOK_BLOCK_TO_HLD_5.2.md`를 본다.

대표 조치:

```text
- 설치 문제: INSTALL_SKILL.md
- 현재 다음 단계 불명확: NEXT_STEP_5.2.md
- structure/slug/path 문제: RUNBOOK_BLOCK_TO_HLD_5.2.md
- 설계 배경 확인: HANDOFF_5.2.md
```

---

## 10. 레거시 수동 모드

`prompt/` 폴더는 스킬 설치가 불가능한 환경의 하위 호환용이다. 새 사용자는 기본적으로 사용하지 않는다.
