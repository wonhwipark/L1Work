# 사내 MCP 검증 프롬프트 — Skill-Updater v0.5.43

사내 LLM에 아래 블록을 복사해서 사용한다. **우선 읽기 전용 진단**이며 설정 변경·업데이트 실행·Jira 쓰기·Git/P4 쓰기·빌드·UT는 금지한다.

## 프롬프트 A — 사내 상태 확인

현재 skill-updater를 **실제 설치 기준으로** 진단해줘. 기대 후보는 `skill-updater v0.5.43`, `work-ledger-kernel v0.7.13`, `l1-fix-workflow v1.6.21`이야. 읽기 전용 조회만 허용해.

1. skill-updater 실제 로드 버전과 canonical `VERSION` 확인.
2. `~/l1sw-bootstrap/l1sw_bootstrap.py` 독립 설치 여부, 파일 해시·실행 가능 여부 확인.
3. updater canonical config의 `self_update_policy` 확인. 기본 `manual_canary`면 승인 없이 변경하지 마.
4. `skill-updater`가 `targets`에 활성화됐는지 확인.
5. `~/l1sw-bootstrap/pending_self_update.json`이 있다면 state, from/to, policy_ref, SHA256 일치만 확인. 패키지 설치 금지.
6. 사내 MCP의 `run_skill_updater`가 외부 CLI 프로세스를 실행하는지, 아니면 Updater `main()`을 같은 서버 프로세스에서 호출하는지 확인.
7. Linux cron/Autotask 경로에서 `skill_updater_auto.py --yes` 또는 외부 Bootstrap이 사용되는지 **조회만** 확인.
8. Kernel과 Workflow 설치 버전 확인.
9. 신규 ZIP v0.5.43의 신뢰된 원격 배포 목록 존재 여부 확인. 접근 불가하면 확인불가로 표시.

출력: 순서대로 **숫자 9개를 한 줄**로 보고. `1=기대대로 정상`, `2=미준비/불일치`, `3=승인 대기`, `4=조회 불가`. 그 다음 최대 2개의 짧은 오류 코드. 원문 로그·경로 덤프 금지. 변경/설치/원격 Job-list 실행 금지.

## 프롬프트 B — 사내 소유자 승인 이후에만 사용

아래 작업은 **소유자가 외부 Bootstrap 배포와 자동 적용 정책을 별도로 명시 승인한 경우에만** 수행한다. 기존 파일 백업 후 승인된 v0.5.43 ZIP에서 Bootstrap을 독립 배포하고, `self_update_policy=automatic_after_exit`를 설정해. 기존 MCP Tool 3개·Job-list 스케줄링 정책·기타 설정은 변경하지 마. 그 뒤 Updater 1회 정상 동작을 실행해 STAGED 선적용 → 신규 Updater 탐색 → 새 Updater 설치 → 일반 Skill 업데이트 순서를 검증해. 예상치 못한 단계 실패 시 즉시 중단하고 현행 버전 보존 또는 롤백해.

출력은 `PREAPPLY / POSTAPPLY / EXECUTED_VERSION / KERNEL_VERSION / WORKFLOW_VERSION / JOB_LIST_UNEXPECTED` 6개만 짧게 제시해. MCP에서 보고서 경로만 출력하지 말고 결과를 직접 요약해.
