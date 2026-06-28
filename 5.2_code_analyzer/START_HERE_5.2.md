# START_HERE_5.2 — CodeAnalyzer 정상 사용 시작점

마지막 갱신: 2026-06-27 10:38 KST  
대상 버전: v0.8  
권장 방식: `/code-analyzer` 스킬 사용

이 문서는 처음/평소 사용자가 보는 짧은 시작 안내다. 설치 상세는 `INSTALL_SKILL.md`, 실제 사용 예시는 `USER_GUIDE_5.2.md`, 문제 해결은 `RUNBOOK_BLOCK_TO_HLD_5.2.md`를 본다.

---

## 1. 한 줄 요약

```text
ZIP 해제 → .\install_skill.ps1 → VSCode/Claude Code 재시작 → /code-analyzer → 코드 루트와 분석 대상 입력
```

---

## 2. 최초 1회 설치

패키지 루트에서 실행한다.

```powershell
.\install_skill.ps1
.\validate_install.ps1
```

다른 위치에 설치해야 하면 `INSTALL_SKILL.md`의 `-TargetSkillsDir` 옵션을 사용한다.

---

## 3. 분석 시작

Claude Code에서 호출한다.

```text
/code-analyzer
```

요청 예시:

```text
C:\work\modem\l1 에서 TxSwitchMngr 블록 분석해줘
```

또는 특정 API 기준으로 요청한다.

```text
C:\work\modem\l1 에서 ProcPeriodicTxSwitch API 기준 call flow 분석해줘
```

스킬이 자동으로 처리하는 항목:

```text
- 코드 규모 판별
- Track A/B 선택
- slug 생성/승계
- output/5.2/<slug>/ 생성
- structure focused 추출 또는 탐색
- procedure 목록 생성
- procedure별 분석
- MSC .puml 분리 생성
- HLD md 생성
- 이어하기 상태 관리
```

---

## 4. 이어하기

진행 중 세션이 끊기면 다시 호출한다.

```text
/code-analyzer
이어서 진행해줘
```

스킬은 `NEXT_STEP_5.2.md`와 `output/5.2/<slug>/analysis_progress.md`를 기준으로 복귀한다.

---

## 5. 문서 지도

| 목적 | 문서 |
|---|---|
| 처음 시작 | `README.md`, `START_HERE_5.2.md` |
| 설치 상세 | `INSTALL_SKILL.md` |
| 사용 예시 | `USER_GUIDE_5.2.md` |
| 현재 다음 단계 | `NEXT_STEP_5.2.md` |
| 문제 해결 | `RUNBOOK_BLOCK_TO_HLD_5.2.md` |
| 설계/유지보수 | `HANDOFF_5.2.md`, `VERSION_5.2.md`, `RUNTIME_TOKEN_POLICY_5.2.md` |

---

## 6. 레거시 수동 모드

`prompt/` 폴더의 copy prompt는 스킬 설치가 불가능한 환경에서만 사용한다. 정상 흐름에서는 사용하지 않는다.
