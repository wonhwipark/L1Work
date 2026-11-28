# Viewer 자동 업데이트 G0 — Job-list v0.4.39 경량 패키지·실패 복구 인계 r0002

- 일자: 2026-11-28 KST
- 대상: 업무 GPT, Linux MCP, Job-list/Skill Updater 담당
- Job ID: `JOB-20261128-VIEWER-AUTOUPDATE-G0-01`
- Profile: `viewer-autoupdate-g0-linux` / Linux One-shot / Priority 65 / Retry 0 / Supersede false
- 만료: `2026-12-15T23:59:59+09:00`
- 기준: [G0 상세조사 인계](L1_VIEWER_AUTO_UPDATE_G0_DISCOVERY_HANDOFF_r0001_20261128_KST.md), [기존 실패 복구 인계](L1_VIEWER_AUTO_UPDATE_JOBLIST_RECOVERY_HANDOFF_r0001_20261128_KST.md), [Job-list PUBLIC 전달 계약](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/ops/CONTRACTS/JOBLIST_PUBLIC_DELIVERY_V1.md).

## 목적과 금지 범위

최종 목표는 승인된 Viewer 공통 UI 업데이트를 Linux cron 3시간 주기 및 기존 Skill Updater로 안전하게 자동화하는 것이다. 이번 Job은 **그 전 단계 G0 읽기 전용 조사 한 건만** 수행한다. Viewer/Updater/cron/서비스/Repository/Knowledge/Work/Kernel 수정, 서비스 재시작, 설치, 동작 시험, 외부 소스 반출을 금지한다.

## 신규 경량 패키지 내용

| 항목 | 정해진 내용 |
|---|---|
| 후보 ZIP | `job-list_v0_4_39_1128.zip` (새 버전, 기존 v0.4.38 덮어쓰기 금지) |
| 고정 요청 | `requests/one-shot-jobs.json`의 위 Job ID 단 1건 |
| 실행 Profile | `scripts/job_core.py`의 `viewer-autoupdate-g0-linux` |
| Worker | `scripts/viewer_autoupdate_g0_linux_job.py` |
| 결과 | `output/viewer_autoupdate_g0/latest_result.json`, `runs/<run_id>/evidence.json`, `G0_REPORT.md` |
| 설치 | 기존 `install.py`, `.skill-main.json`, lifecycle/preserve, SkillSilent 계약 보존 |
| 경량화 | 과거 리뷰/스냅샷/타 스킬 테스트 ZIP 및 Bootstrap payload 제외 |
| 이력 | 기존 `data/**`, `output/**`, `.git/**`, Queue·Receipt·processed 기록 보존 |
| 안전 | 실행 ID 검증, Linux non-root, 다른 Job 대기/실행 시 차단, 중복 요청 SKIP |

작업자 구현 범위는 G01~G09 정형 증거 취합이다. **실제 Qwen/OpenCode 호출은 포함되지 않는다.** 모델 라우팅·호출 권한이 확인되지 않은 상황에서 암묵적 모델 호출은 금지하며, 부족한 코드 해석은 업무 GPT가 근거를 바탕으로 후속 진행한다. 결과 `ANALYSIS_PARTIAL`은 정상적인 부분 관측으로서 G0 완료, Viewer 배포 가능 또는 Qwen 실행 성공을 의미하지 않는다.

## G01~G09 조사 증거

| ID | 조회 대상 | 한계 |
|---|---|---|
| G01 | 사용자 crontab의 Updater 매칭 스케줄; 명령/비밀값 제거 | 실제 예약 사용자·다른 크론/서비스 가능성 |
| G02 | 설치 Updater 버전·Python 엔트리포인트·AST 함수와 라인·SHA | 함수 목록만으로 호출 관계 확정 불가 |
| G03 | lifecycle/preserve/release 정책 키 및 해시 | 실제 설치 보존 시험 미실행 |
| G04 | 고정 후보 Viewer 경로, systemd user 서비스 명칭 | 실제 활성 document root 미확인 가능 |
| G05 | 설치 Viewer HTML/CSS/JS/Adapter 파일 지문 | GitHub 기준 ZIP의 해시 대조 별도 필요 |
| G06 | Adapter 파일 지문, 관련 스킬 설치 버전 | API/Knowledge/Source Map 호환성 추가 조사 |
| G07 | releases/backups/current 구조 존재 여부 | 원자성/롤백 실제 검증 미실행 |
| G08 | 배포 manifest/Updater 지문 | 승인 신호 및 candidate 제외 규칙 확인 필요 |
| G09 | test/scripts/fixture 존재 여부 | HTTP/브라우저/smoke 실행 금지 |

## 수행·배포 상태를 반드시 분리

`CANDIDATE_BUILT`, `SELF_TESTED`, `PUBLIC_POSTED`, `UPDATER_INSTALLED`, `JOB_ACTIVATED`, `WORKER_EXECUTED`, `RESULT_READBACK`, `G0_COMPLETE`는 서로 독립이다. 작성 환경 자체 검증: 신규 6 PASS, 기존 Worker 격리·버전 회귀 3 PASS, `job_core validate` 27 profiles / errors 0 / PASS, CRC·manifest·버전·파일경로 검사 PASS. 실제 Linux 설치·Worker·MCP readback·Qwen 분석은 NOT_RUN이다.

현 단계의 로컬 검증 ZIP 바이트: 309,393 bytes, SHA-256 `fa81fc0ef06dfe91e4faea163f3df09506de40184e4500785f4e8ac59c620da1`. **이 값은 로컬 ZIP 증거이며 GitHub 원격 readback 증거가 아니다.** GitHub 바이너리 게시 여부와 최종 원격 commit은 별도 확인 후 `PUBLIC_POSTED`를 판정한다.

## 장애 디버깅 D01~D09 (업무 GPT 담당)

| 단계 | 확인 | 실패 시 대응 |
|---|---|---|
| D01 GitHub | L1Work/main 루트에 실제 ZIP 존재, bytes/SHA 일치 | 미게시면 `PUBLIC_NOT_POSTED`; 동일 ZIP 이름 덮어쓰기 금지 |
| D02 cron/탐색 | 실제 cron 로그·실행 계정·Updater 감지 버전 | 조회로 근거 수집, cron 및 인증정보 임의 수정 금지 |
| D03 설치 | canonical 디렉터리, installer/Manifest/Updater >=0.5.43 | 설치와 활성화 실패 분리, 기존 data/output 보존 |
| D04 One-shot 활성화 | 예약 hook, Job ID/Profile, Queue/processed/만료/중복 | 다른 Job 차단 원인 확인, 기존 Job 재큐잉 금지 |
| D05 Worker | 실행 Run ID, Profile, 권한, 종료코드, stdout/stderr | `JOB_RUNNER_IDENTITY_UNVERIFIED` 등 첫 실패만 분석 |
| D06 로컬 결과 | latest_result 및 per-run Evidence/MD/해시 | 결과 조회 장애를 재실행 사유로 쓰지 않음 |
| D07 Catalog/MCP | 동일 Job/Run ID로 Queue·Receipt·Catalog 조회 | READBACK 장애는 Worker 실행 실패와 구분 |
| D08 G0 품질 | G01~G09 PASS/PARTIAL/UNKNOWN과 증거·추론 분리 | 실제 코드 위치 미확인이면 UNKNOWN 유지 |
| D09 최소 복구 | 새 버전·설정 계약·테스트·롤백 | 운영 변경/모델 재호출/Job 재발급은 추가 승인 필요 |

## 승인된 조회 예 (실제 설치 경로가 일치할 때만)

```bash
JOB_ROOT="$HOME/l1sw-private-skills/job-list"
JOB_ID='JOB-20261128-VIEWER-AUTOUPDATE-G0-01'
python3 "$JOB_ROOT/scripts/job_core.py" job-queue-read --root "$JOB_ROOT" --job-id "$JOB_ID"
python3 "$JOB_ROOT/scripts/job_core.py" job-result-read --root "$JOB_ROOT" --job-id "$JOB_ID"
python3 "$JOB_ROOT/scripts/job_core.py" job-catalog-read --root "$JOB_ROOT" --job-id "$JOB_ID"
```

이 명령은 읽기 전용 결과 조회용이다. `activate --launch`, `run`, 수동 재큐잉 또는 서비스 재시작 명령으로 바꾸지 않는다. 업무 GPT의 회신은 실제 최초 실패 단계, ID, 근거, 보존된 결과 위치, 최소 수정안 및 다음 한 조치로 구성한다. 독립 리뷰 신규 요청은 하지 않는다.

---

## 참고: 기존 r0001 복구 규칙 보존

# Viewer 자동 업데이트 G0 — Job-list 실행 실패 복구 및 디버깅 인계
상태: 실행 요청 설계 / 실제 ZIP 배포 및 호스트 실행 별도 확인.
대상: 업무 GPT, Linux MCP, Job-list/Skill Updater 담당.
기준: [G0 조사](L1_VIEWER_AUTO_UPDATE_G0_DISCOVERY_HANDOFF_r0001_20261128_KST.md), [기존 실행·조회 계약](L1_JOBLIST_KNOWLEDGE_UPDATER_RECOVERY_MCP_EXECUTION_RESULT_HANDOFF_r0001_20261128_KST.md), [공개 배포 계약](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/ops/CONTRACTS/JOBLIST_PUBLIC_DELIVERY_V1.md).
## 실행 요청
Viewer G0 G01~G09를 기존 승인된 Linux one-shot으로 한 번 수행. 정형 관측은 기존 허용 read-only 도구, 코드 호출 구조 분석은 Qwen/OpenCode 사용. 실제 등록기/Profile/스키마 확인 후 고유 ID 발급. 신규 활성 요청 최대 1건, 만료 및 중복 방지, 기존 영수증·data/output 보존. 기존 활성 요청이 있으면 대기. 일반 MCP update-only 호출로 활성화하지 말고 기존 예약 hook 사용. 운영 Viewer/Updater/cron/서비스/DB/Knowledge 수정 금지. 조사 결과는 승인된 로컬 결과 경로에 저장, 공개 게시 금지(비민감 상태 요약만 별도 승인).
## 실패 진단 및 복구
| 단계 | 확인 | 최소 복구 |
|---|---|---|
| D1 배송 | 신규 ZIP/manifest/hash/원격 readback | 배송 결손만 복구, 동일 이름 덮어쓰기 금지 |
| D2 탐색·설치 | 실제 cron 로그, 버전 선택, 설치 영수증, 실제 로딩 경로 | 경로/정책/인증 오류 식별; 운영 변경은 유효 승인 필요 |
| D3 활성화 | scheduled hook, profile, expiry, 기존 활성/소비 기록 | update-only와 구분; 기존 요청 중복 활성화 금지 |
| D4 Worker | Job/Run ID, 시작/종료, CLI/권한/모델 상태 | 최초 실패 확정, 격리 시험; 불확실 호출 재실행 금지 |
| D5 결과 | G01~G09 근거, 결과 파일/hash, 영수증 | 기존 결과 보존, 누락 단계만 분석 |
| D6 조회 | Catalog 등록, 동일 ID MCP readback | RESULT_UNSUPPORTED 원인 분리, 기존 결과 경로 우회, 등록/조회만 재개 |
## 복구 권한
읽기 조사, 기존 로그 조회, 비운영 후보 패치 및 무모델 격리 회귀는 기존 승인 범위 내 수행. 운영 설치/설정/서비스 변경, 키 교체, 추가 유료 호출, 소비 Job 재큐잉은 별도 유효 승인 없이는 금지. 승인된 운영 복구만 백업→최소 변경→검증→필요시 롤백. Viewer 자동 업데이트 자체 구현은 이번 범위 아님.
## 회신
배송/설치/활성화/Worker/결과 저장/Catalog/MCP readback 각각 PASS/FAIL/BLOCKED/NOT_RUN; 실제 ID·버전·시각·근거·최초 실패·복구 diff·회귀·다음 한 행동. G01~G09 결과와 재사용 매트릭스 포함. 미발급 ID 생성 금지. 결과 조회 실패로 모델 재호출 금지. 기존 정상 Job 및 스킬 회귀 확인. 독립 리뷰 신규 요청 없음.
