# Viewer G0 One-shot Job-list v0.4.39 — 배송·실행·실패 복구 인계 (r0003)

- 기준일: 2026-11-28 KST
- 수신: 업무 GPT / Linux MCP / Job-list 및 Skill Updater 담당
- JOB ID: `JOB-20261128-VIEWER-AUTOUPDATE-G0-01`
- Profile: `viewer-autoupdate-g0-linux`
- 기준 배포: `wonhwipark/L1Work` / `main` / 루트 / 신규 유일 ZIP
- 원본: `job-list_v0_4_38_1115.zip` (SHA-256 `0cdda16fe214f86811d4df25cc04f3453ec93789ddc9bc2b0769e730bb9c16e0`)
- 관련 인계: [G0 조사 r0001](L1_VIEWER_AUTO_UPDATE_G0_DISCOVERY_HANDOFF_r0001_20261128_KST.md), [장애 복구 r0002](L1_VIEWER_AUTO_UPDATE_JOBLIST_RECOVERY_HANDOFF_r0002_20261128_KST.md)
- [전달·안전 계약](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/ops/CONTRACTS/JOBLIST_PUBLIC_DELIVERY_V1.md)

## A. 현재 확인된 배포 단계 — 혼동 금지

| 단계 | 상태 | 확인 증거 |
|---|---|---|
| 후보 생성 | PASS | `job-list_v0_4_39_1128.zip` |
| 로컬 ZIP 검사 | PASS | 338,284 bytes, SHA-256 `95b47949bac62cfa15cdfeeaac73395a46669f297aec231f1ff2599644edbe1f`, CRC/목록 검증 |
| 실행 Profile 검사 | PASS | `job_core validate`: profiles 27, errors 0 |
| 추가 보안·회귀 단위검사 | PASS | 6 tests, 6 PASS (단일 요청·중복 Run·신원·Linux/Nonroot·파일 무결성) |
| Linux 설치 통합검증 | NOT_RUN | 실제 호스트 정보 및 안전한 격리 환경 미확인 |
| **GitHub L1Work 루트 ZIP 게시** | **NOT_POSTED** | 연결된 GitHub 파일 쓰기 기능이 UTF-8 파일 또는 직접 인코딩 문자열을 요구. 현재 세션의 ZIP 로컬 바이트를 그대로 넘기는 연결 경로 미확인 |
| GitHub 원격 ZIP bytes/SHA readback | NOT_RUN | 게시 미완료 |
| Skill Updater 설치 | NOT_RUN | 호스트 영수증 없음 |
| One-shot 활성화·Worker 실행 | NOT_RUN | 실행 영수증 없음 |
| MCP/Catalog 결과 조회 | NOT_RUN | 실행 확인 전 재실행 금지 |

**주의:** 위 SHA는 본 세션에서 재생성한 ZIP의 로컬 바이트 기준이며, 이전 r0002의 309,393-byte 후보와 *같은 파일이 아니다*. 혼용·덮어쓰기 금지. 원격 게시 전에는 Linux Skill Updater가 새 버전을 설치한 것으로 간주하지 않는다.

## B. 포함된 작업과 안전 경계

- 기존 Job-list 실행 엔진과 `install.py`, `.skill-main.json`, lifecycle/preserve, Skillsilent 계약 유지.
- 과거 리뷰 산출물·테스트 fixture·Bootstrap/타 스킬 ZIP 및 과거 One-shot 요청은 신규 배포 ZIP에서 제외. 기존 호스트 `data/**`, `output/**`, Queue·Receipt·processed 기록을 삭제하지 않음.
- `requests/one-shot-jobs.json`에는 Linux `JOB-20261128-VIEWER-AUTOUPDATE-G0-01` 단 1건. Retry 0, supersede false, expiry 2026-12-15 23:59:59 KST.
- `scripts/job_core.py`에 새 Profile, `scripts/viewer_autoupdate_g0_linux_job.py`에 G01~G09 읽기 전용 관측 구현.
- 관측: G01 사용자 crontab의 Updater 표시 존재·개수, G02 Updater 스크립트·AST·해시, G03 lifecycle/Preserve, G04 Viewer 설치 후보, G05 Viewer 파일 지문, G06 Adapter 후보, G07 backup/release 디렉터리, G08 release manifest, G09 테스트 디렉터리. 비밀값·원문·절대 경로는 공개로 전송하지 않음.
- **Qwen/OpenCode 모델 호출 미구현/미실행.** 정상 산출은 `ANALYSIS_PARTIAL`이며 G0 완료나 Viewer 자동 업데이트 적용 PASS가 아님.
- Viewer 서비스/cron/Updater/Knowledge/Kernel 정본 변경·외부 코드 전송·기존 Job 재큐잉 금지.

## C. 출력 계약

설치 호스트의 기존 canonical Job-list 루트 아래:
- `output/viewer_autoupdate_g0/latest_result.json`
- `output/viewer_autoupdate_g0/runs/<run_id>/evidence.json`
- `output/viewer_autoupdate_g0/runs/<run_id>/G0_REPORT.md`

실패 시에도 latest_result에 실제 reason_codes를 보존. 실제 Runner Receipt와 Run Catalog가 존재하는지 별도 판정. 동일 Run ID가 이미 있으면 재실행 차단.

## D. 업무 GPT 디버깅 D01~D09

| 단계 | 우선 확인할 근거 | 복구 원칙 |
|---|---|---|
| D01 공개 ZIP 배송 | L1Work/main 루트의 실제 신규 파일, SHA·크기·커밋 | 기존 ZIP 덮어쓰기 금지. 업로드 실패를 설치 실패와 구분 |
| D02 cron 호출 | 예약 계정·주기·최근 호출 로그 | 읽기 전용. 임의 설정 변경 금지 |
| D03 Updater 감지/설치 | 설치 영수증·manifest·설치 버전·Installer | 먼저 실제 Updater가 >=0.5.43인지 확인, 기존 data/output 보존 |
| D04 활성화 | 단일 요청, Profile, 기존 pending/running/processed/expiry | 다른 Job 대기 시 신규 활성화 차단. 소비 Job 재큐잉 금지 |
| D05 Worker | Job ID/Run ID/권한/종료코드/원인코드 | 정확히 첫 실패 단계만 진단. Qwen 성공으로 추정 금지 |
| D06 증거 파일 | latest_result, per-run JSON/MD, 로컬 SHA | 결과 조회 실패를 이유로 Worker 재실행 금지 |
| D07 Catalog/MCP readback | 동일 Job·Run ID 영수증, Queue/Catalog | 조회 실패와 실행 실패 분리 |
| D08 G01~G09 품질 | 관측값, 원문 위치, UNKNOWN/PARTIAL 사유 | 정형 지문만으로 코드 호출·호환성 확정 금지 |
| D09 최소 복구 | 버전·패치·후속 격리시험·롤백 | 운영 수정·재큐잉·유료 호출은 추가 승인 필요 |

## E. 재개 조건과 다음 한 조치

**최우선 미완료:** 승인된 ZIP을 L1Work/main 루트에 신규 파일 `job-list_v0_4_39_1128.zip`으로 게시하고 **원격 파일 실제 bytes/SHA-256 일치**를 확인. 공개 배송 전에 로컬 ZIP의 서명된 검증 상태, 공개금지 데이터·경로·기존 Job 보존을 다시 확인.

업로드 이후 Linux Skill Updater의 다음 기존 스케줄에서 **설치·활성화·실행 상태를 별도 증빙**하되, 새 스케줄 생성·강제 Job 실행은 금지. 실제 Worker가 부분 보고서를 생성하면 업무 GPT가 원본 근거로 코드를 추가 분석하여 G1 설계를 확정. 독립 리뷰는 새로 요청하지 않음.

### 주의 사항

ZIP 로컬 제작과 L1Work 공개 게시는 다른 작업이다. **본 r0003 Markdown의 GitHub 게시는 ZIP의 PUBLIC_POSTED 증거가 아니다.** 이전 r0002 링크는 보존하되 본 문서의 최신 배포상태/새 SHA를 우선 사용.
