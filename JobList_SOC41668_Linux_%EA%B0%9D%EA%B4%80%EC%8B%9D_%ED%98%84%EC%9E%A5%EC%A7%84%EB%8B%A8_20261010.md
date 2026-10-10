# Job List / SOC-41668 Linux 무인 원복 — 사내 LLM용 객관식 진단 프롬프트

> **사내 Linux PC의 LLM에 이 문서를 입력하고, 실제 파일/로그를 조회해서 답변하라.** 질문을 사용자에게 다시 던지지 말 것. **읽기 전용 진단만 수행**하고, 최종 답은 숫자 코드 1~2줄만 표시할 것.

## A. 진단 목적과 대상

- 진단 대상: `skill-updater` → `job-list` → `l1-github` → 기본 저장소 브랜치 원복.
- 기대 Job: `JOB-20261010-WT-SOC41668-AUTO-01` / Profile: `l1-github-worktree-auto-linux` / OS: Linux.
- 기대 버전: `job-list >= 0.4.13`, `l1-github >= 0.3.40`.
- 기본 저장소: `/home/whpark/Project/smp1900`.
- 이전 linked Worktree: `/home/whpark/Project/smp1900/.worktrees/fix-SOC-41668`.
- 원복 후 기대 브랜치: `fix-SOC-41668` (기본 저장소 안에서 작업; 신규 Worktree 생성 아님).
- 정기 실행 설정(사용자 설명): **01:00부터 3시간 주기**, cron → Skill-Updater → Job List. *실제 cron과 실행 여부는 반드시 현장에서 확인.*
- 주의: ChatGPT가 ZIP을 생성한 것만으로 사내 설치·외부 GitHub 게시·Job 실행이 완료된 것은 아니다.

## B. 절대 안전 규칙

1. **조회만 수행.** `git status`, `git branch --show-current`, `git worktree list --porcelain`, `git rev-parse`, `crontab -l`, 파일 존재/버전/mtime/JSON 필드 읽기만 허용.
2. 다음은 **금지**: `activate --launch`, Job 수동 실행, `git switch`, `git checkout`, `git worktree remove/move/prune`, `git reset`, `git clean`, `git stash pop/drop`, `git fetch/push`, `--apply`, 스케줄 재시작, ZIP 설치·업데이트, 변경·삭제·재시도.
3. 비밀키·토큰·내부 주소·소스·로그 원문·커밋 SHA·사용자 ID·개인 정보는 **외부 전송용 답변에 포함 금지**. 확인 근거는 사내에서만 유지한다.
4. 로컬 읽기 권한이나 파일이 없으면 추측하지 않고 `9=확인 불가`로 기록한다. 최신 실행 기록이 다른 Job 것이면 성공으로 오판하지 않는다. 필요한 경우 해당 Job ID가 포함된 `history/processed` 기록까지 조회한다.
5. 기존 Worktree나 기본 저장소에 수정사항이 있어도 건드리지 않는다. **실패 원인 확정 전 재실행 금지.**

## C. 조회 위치 — 있는 것만 읽어라

- 설치 파일:
  - `~/l1sw-private-skills/job-list/VERSION`, `~/l1sw-private-skills/job-list/bin/job-list-core.py`
  - `~/l1sw-private-skills/l1-github/VERSION`, `~/l1sw-private-skills/l1-github/scripts/l1_github.py`
  - `~/l1sw-private-skills/skill-updater/VERSION` (없으면 실제 설치 위치 탐색)
- Job 정의: `~/l1sw-private-skills/job-list/requests/one-shot-jobs.json`
- Job 접수·활성화: `~/l1sw-private-skills/job-list/data/state/activation/latest.json`, `history.jsonl`
- 작업 큐/처리 이력: `~/l1sw-private-skills/job-list/data/state/core/queue.json`, `processed.jsonl`, `running.json`
- Job 실행 결과: `~/l1sw-private-skills/job-list/output/core/last_run.json`, `output/core/runs/`, `data/state/observer/latest_result.json`
- 원복 결과: `~/l1sw-private-skills/job-list/output/github_worktree_recovery/latest_result.json`
- 1회 실행 보호: `~/l1sw-private-skills/job-list/data/state/github_worktree_recovery/*.auto.json`
- Updater 실행: 실제 `skill-updater` 설치 폴더와 최신 실행 리포트의 `job_sync` / `activate --launch` 수행 기록 확인. **업데이터에서 `job_sync`가 SKIP이어도 원인을 구분.**
- Linux cron: `crontab -l` 및 가능한 경우 cron 실행 흔적(로그/실행결과 파일의 최근 수정 시각). **cron 등록 ≠ 실제 실행.**
- Dispatcher (참고): `~/l1sw-dispatcher/` 내의 로컬 상태/스냅샷만 조회. Dispatcher의 원격 신호는 실제 Job 완료의 직접 증거가 아니며, Job List 로컬 기록을 우선한다.

설치 경로가 다른 경우 `~/.claude/skills/`, `~/l1sw-skills/`, 해당 스킬의 `SKILL.md` 등에서 실제 canonical 설치 위치를 **읽기 전용으로** 확인한다. 파일이 존재한다는 것만으로 설치 버전이나 실행 여부를 단정하지 않는다.

## D. 객관식 10문항 — 사내 LLM이 직접 판정

**Q1. Linux에 설치된 Job List 버전?**
- `1` = 0.4.13 이상 및 실행 파일 존재
- `2` = 0.4.12 이하
- `3` = 설치 파일이 없음 / 진입점 없음
- `9` = 확인 불가

**Q2. `l1-github` 설치 상태?**
- `1` = 0.3.40 이상 + 실행 파일 존재
- `2` = 0.3.39 이하
- `3` = 설치되지 않았거나 진입점 없음
- `9` = 확인 불가

**Q3. 최근 예정 시간(01/04/07시 등)에 Linux Skill-Updater가 실제 실행됐나?**
- `1` = 해당 주기 실행 완료 증거 있음
- `2` = 실행 시작 흔적은 있으나 오류/중단
- `3` = cron 등록은 있으나 해당 주기 실행 증거 없음
- `4` = cron 자체가 없음 / 주기 설정이 다름
- `9` = 확인 불가

**Q4. Skill-Updater → Job List 자동 호출(`activate --launch`) 결과?**
- `1` = 호출 성공 증거 있음
- `2` = 호출 SKIP / 대상 미설치 등으로 생략
- `3` = 호출 실패 또는 타임아웃
- `4` = 호출 시도 기록 없음
- `9` = 확인 불가

**Q5. 정확한 Job ID가 현장 요청 파일에 있는가?**
- `1` = ID·Profile·Linux·브랜치 모두 일치
- `2` = ID 없음 (과거 PREVIEW Job만 있으면 2)
- `3` = ID 있으나 Profile/OS/브랜치 불일치
- `4` = 요청 파일 자체가 없음
- `9` = 확인 불가

**Q6. 해당 Job이 Job List에 접수됐나?**
- `1` = 활성화 이력/큐/처리 이력에서 접수 확인
- `2` = 접수 시도했지만 거절/만료/중복/OS 필터
- `3` = 요청 파일에는 있지만 접수 이력 없음
- `4` = 처리 기록에 이미 완료됨(후속 결과 검증 필요)
- `9` = 확인 불가

**Q7. 해당 Job worker의 실제 실행 상태?**
- `1` = worker 실행 완료
- `2` = worker 실행 시작 후 실패/타임아웃/중단
- `3` = 큐에 대기만 있음
- `4` = worker 시작 기록 없음
- `9` = 확인 불가

**Q8. `github_worktree_recovery`의 해당 Job 원복 결과?**
- `1` = `RESTORED` 및 작업 시각·대상 일치
- `2` = `BLOCKED` (사전 점검에서 차단)
- `3` = `NEEDS_MANUAL_REVIEW` 또는 auto 상태가 `STARTED`로 남음 (재시도 금지)
- `4` = 결과 파일 없음 / 해당 Job 결과가 아님
- `5` = 기타 실패 상태
- `9` = 확인 불가

**Q9. 현재 기본 저장소 `/home/whpark/Project/smp1900`의 실제 Git 상태?**
- `1` = 기본 저장소 브랜치 `fix-SOC-41668`; 원복 후 조건 확인됨
- `2` = 기본 저장소는 다른 브랜치, 대상은 아직 linked Worktree에 있음
- `3` = 기본 저장소는 다른 브랜치, 대상 Worktree도 찾을 수 없음
- `4` = 기본 저장소 브랜치는 대상이지만 HEAD/복원 결과 확인 불가 또는 불일치
- `9` = 확인 불가

**Q10. Dispatcher 상태(향후 사외 진단 대비)?**
- `1` = Linux Dispatcher 동작·최근 관측 기록 확인
- `2` = 설치됐지만 관측 갱신 안 됨 / 오류
- `3` = 설치되지 않음
- `9` = 확인 불가

## E. 최초 실패 단계(F) 판단

다음 중 **가장 앞에서 확인된 장애 하나**만 선택한다. `Q1`부터의 실행 체인과 증거를 기준으로 하며, 정상 완료가 충분히 입증되지 않으면 `0`을 선택하지 않는다.

- `F=0` 원복 성공: Job 성공 + 기본 저장소 브랜치/HEAD 확인
- `F=1` Job List 미설치/버전 미달 또는 새 패키지가 사내 PC에 도착하지 않음
- `F=2` cron/Skill-Updater 실행 문제
- `F=3` Updater → Job List 연계 문제
- `F=4` Job 요청 미수신·불일치
- `F=5` Job List 접수·큐 처리 문제
- `F=6` worker 실행 문제
- `F=7` l1-github 설치/진입점 문제
- `F=8` Git 안전 점검 거부·경로/수정사항 충돌
- `F=9` 원복 도중 실패/중단, 복구 상태 불확실
- `F=10` 원복 성공이나 VS Code/CLion에서 다른 폴더를 연 경우
- `F=99` 증거 부족으로 판단 불가

**추가 판정 지침:** Q1=2/3이면 F=1을 우선 고려한다. Q2=2/3이어도 Q1~Q7의 선행 실패가 있으면 선행 단계를 우선한다. Q8=1이라도 Q9가 충족되지 않으면 F=0은 금지한다. Q9=1만으로 Job 성공을 추정하지 않는다. Q10은 별도 관측 상태이며 원복 실패의 선행 원인으로 취급하지 않는다.

## F. 출력 — **복사 가능한 숫자 1~2줄만**

다른 설명, 상세 파일 경로, SHA, 로그, JSON, 내부 호스트명은 출력하지 않는다.

```text
Q1=_,Q2=_,Q3=_,Q4=_,Q5=_,Q6=_,Q7=_,Q8=_,Q9=_,Q10=_
F=_
```

예시(**임의 예시이며 현장 판정이 아님**):

```text
Q1=2,Q2=1,Q3=1,Q4=2,Q5=2,Q6=9,Q7=9,Q8=4,Q9=2,Q10=1
F=1
```

사내에서는 객관식 판정에 대한 근거를 로컬 화면에서 확인하되, **사외로는 위 코드 2줄만 직접 입력**한다. 외부 반출이 허용되지 않는 정보는 코드 형태로도 반출하지 말고 사내 보안정책을 따른다.
