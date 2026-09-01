# Dispatcher v0.3.9 — MCD Detail Observer 배포 및 검증

작성일: 2026-09-01

## 1. 목표

회사 Linux의 MCD 분석 진행 상황을 사외에서 GitHub Release asset `download_count` 변화로 더 자세히 관측한다.

Dispatcher의 역할은 끝까지 다음으로 제한한다.

```text
OBSERVER_ONLY
READ local state/artifacts
GET pre-created GitHub Release signal assets
```

하지 않는 것:

```text
Job 실행/중지/retry
Skill 호출
Code Analyzer 호출
GitHub POST/PUT/PATCH/DELETE/push
Remote Queue
MCD 실행 gate
```

## 2. v0.3.9 추가 관측 정보

로컬에서 다음 6개 차원을 읽는다.

```text
stage
root_layer
analysis_required
pending_cycles
report_state
resumable
```

외부 signal은 고정 enum만 사용하며 코드/로그/Jira/경로/자유형 LLM 문장을 보내지 않는다.

## 3. 사외 GitHub 선작업

먼저 `signal-v1` Release에 제공된 21개 Linux MCD signal asset을 **추가만** 한다.

사용 파일:

```text
dispatcher_mcd_detail_signal_assets_v0_3_9_0901.zip
```

기존 heartbeat / FLA / Job-list / skill signal은 삭제/overwrite하지 않는다.

대표 GET 3개 정도를 확인하고, GET 후 download_count를 BASELINE으로 기록한다.

MCD detail asset이 없거나 GET에 실패해도 MCD Job은 실행된다. v0.3.9는 실패한 MCD detail signal을 durable retry backlog에 남기지 않아 기존 coarse signal을 방해하지 않는다.

## 4. 회사 Linux Dispatcher 업데이트

사외 signal asset 준비가 끝난 뒤 Dispatcher v0.3.9를 설치한다.

```bash
unzip l1sw-dispatcher-bundle_v0_3_9_0901.zip
cd l1sw-dispatcher
python3 install.py
```

기존 `state.json`, `config.json`, monitor/log runtime은 installer에서 보존한다. `cmd install`은 observer-only known config key만 다시 기록하므로 legacy/unknown key는 제거한다.

설치 확인:

```bash
python3 ~/l1sw-dispatcher/l1sw_dispatcher.py --version
python3 ~/l1sw-dispatcher/l1sw_dispatcher.py status
```

기대:

```text
version = 0.3.9
mode = OBSERVER_ONLY
mcd_checkpoint = ~/l1sw-private-skills/l1-study-runner/data/state/mcd_study_checkpoint.json
mcd_detail_signal_os_families = [linux]
```

## 5. 강제 cycle 불필요

운영 중에는 autotask-builder가 관리하는 기존 자연 Dispatcher cycle을 기다린다.

필요한 경우 회사에서 read-only 확인만 한다.

```bash
python3 ~/l1sw-dispatcher/l1sw_dispatcher.py status
python3 ~/l1sw-dispatcher/l1sw_dispatcher.py report
```

`cycle`을 실행해야만 설치가 완료되는 구조가 아니다.

## 6. 사외에서 해석하는 방법

예를 들어 자연 cycle 사이 download count 변화가 다음이면:

```text
mcd-stage-code-analyzer  +1
mcd-analysis-remains     +1
mcd-pending-6-20         +1
mcd-report-stale         +1
mcd-resumable-yes        +1
```

해석:

```text
현재 Code Analyzer 단계
ANALYSIS_REQUIRED 남음
pending 6~20 cycle
최종 report 아직 stale
checkpoint 재개 가능
```

정상 완료 예:

```text
mcd-stage-complete +1
mcd-analysis-zero  +1
mcd-pending-zero   +1
mcd-report-fresh   +1
mcd-resumable-no   +1
```

## 7. Root signal

실패/주의 원인을 로컬 evidence로 특정할 수 있을 때만 다음 중 하나가 증가한다.

```text
job-list
study-runner
code-analyzer
knowledge-manager
sam-fixer
```

정상 상태에서 `root-none` signal은 만들지 않는다. 근거가 불충분한 root도 외부로 추측해서 보내지 않는다.

## 8. ANALYSIS_REQUIRED 의미

```text
ANALYSIS_REQUIRED / REVIEW_REQUIRED = 실제 분석이 아직 필요한 항목
UNRESOLVED = 실제 분석은 수행했지만 자동 개선 결론 확정 불가
```

따라서 `UNRESOLVED`는 `mcd-analysis-remains`에 포함하지 않는다.

## 9. 기존 coarse observer 유지

v0.3.9에서도 기존 항목은 변경하지 않는다.

```text
heartbeat
FLA
Job-list
SAM Fixer
Study Runner
Skill-Updater
Autotask
```

Study Runner producer가 `quality_status=PASS/FAIL`을 쓰는 경우 Dispatcher가 각각 `OK/INVALID_OUTPUT`으로 호환 매핑한다.

## 10. 검증 완료 기준

```text
1. Dispatcher version 0.3.9
2. OBSERVER_ONLY 유지
3. 기존 heartbeat count 계속 증가
4. 기존 FLA/job-list signal 계속 증가
5. 실제 MCD 수행 시 MCD detail signal 증가
6. signal GET 실패가 Job/Skill 실행에 영향 없음
7. monitor_snapshot에 내부 path/code/log 내용 없음
```

## 11. 문제 발생 시

MCD detail count가 움직이지 않아도 먼저 Job 실패로 판단하지 않는다.

확인 순서:

```text
1. Dispatcher 자연 cycle 수행 여부
2. ~/l1sw-dispatcher/state.json 의 mcd_detail
3. mcd_study_checkpoint.json 존재 여부
4. checkpoint.sam_run_dir 유효 여부
5. GitHub signal asset 이름 정확 일치 여부
6. signal_flush failed 수
```

Dispatcher를 실행 제어기로 변경하거나 새로운 gate를 추가하지 않는다.
