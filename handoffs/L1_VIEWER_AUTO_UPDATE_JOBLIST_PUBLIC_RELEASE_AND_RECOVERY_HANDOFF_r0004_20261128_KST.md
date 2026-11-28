# Viewer G0 Job-list v0.4.39 — 검증된 공개 배포 및 업무 GPT 실행·복구 인계 r0004

- 기준일: 2026-11-28 KST
- **실제 게시 ZIP:** [job-list_v0_4_39_1128.zip](../job-list_v0_4_39_1128.zip)
- **GitHub 릴리스 커밋:** [9ba5c2697c2e08d010154a919bcbd545b3571c9e](https://github.com/wonhwipark/L1Work/commit/9ba5c2697c2e08d010154a919bcbd545b3571c9e)
- ZIP bytes: **314,842** / SHA-256: **`9d4fd7c31555080df50ce0b7fda728f81f37ad9ca26baf1fd52faf5c0ce03d84`**
- Git Blob SHA: `ff2d4273d41ae9b1c5501da1b95f6bc5cfe25154`
- 기준 원본: [v0.4.38 ZIP](../job-list_v0_4_38_1115.zip), 원본 SHA-256 `0cdda16fe214f86811d4df25cc04f3453ec93789ddc9bc2b0769e730bb9c16e0`
- Job ID: `JOB-20261128-VIEWER-AUTOUPDATE-G0-01` / Profile: `viewer-autoupdate-g0-linux`
- 만료: 2026-12-15 23:59:59 KST, 재시도 0회
- 관련 문서: [G0 조사 항목](L1_VIEWER_AUTO_UPDATE_G0_DISCOVERY_HANDOFF_r0001_20261128_KST.md), [전달·복구 이력 r0003](L1_VIEWER_AUTO_UPDATE_JOBLIST_DELIVERY_AND_RECOVERY_HANDOFF_r0003_20261128_KST.md), [복구 상세 r0002](L1_VIEWER_AUTO_UPDATE_JOBLIST_RECOVERY_HANDOFF_r0002_20261128_KST.md), [PUBLIC 운영 계약](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/ops/CONTRACTS/JOBLIST_PUBLIC_DELIVERY_V1.md)

## 1. 이번 게시와 원래 목표 구분

**원래 목적:** Linux 3시간 주기 cron과 기존 Skill Updater를 이용하여, 승인된 Viewer 공통 UI 업데이트를 LLM 없이 자동 적용하도록 설계하기 위한 **G0 현장 조사 1건**. 이번 배포는 Viewer 자동 설치/교체를 수행하지 않음.

**한 번 수행할 조사:** G01 cron/예약 계정, G02 Updater 엔트리포인트·버전, G03 lifecycle/preserve/release 정책, G04 Viewer 설치본·서비스 후보, G05 배포본/설치본 파일 지문, G06 Adapter/관련 스킬, G07 backup/release/current, G08 승인·digest·후보 제외, G09 smoke test 준비 상태. Worker는 승인된 read-only 범위의 **정형 증거만 수집**, 원본 코드·비밀·운영 로그를 PUBLIC에 게시하지 않음. **Qwen/OpenCode 자동 호출은 미구현**이며 제품 코드 의미 분석·API 호환성은 G0 결과 이후 업무 GPT의 추가 근거 검토 필요.

## 2. 무엇을 경량화했는가

| 범위 | 배포본 처리 |
|---|---|
| 실행 엔진·설치기·Profile·SkillSilent·lifecycle | 유지 |
| `requests/one-shot-jobs.json` | 이번 고유 Job ID **1건**만 |
| `scripts/viewer_autoupdate_g0_linux_job.py` | G01~G09 제한적 사실 조사 |
| 옛 Job 결과·대화 로그·영수증·`data/state/**` Queue | **신규 ZIP에서 제외** |
| 과거 리뷰, Bootstrap/다른 스킬 ZIP, 예전 연구 보관 문서 | 신규 ZIP에서 제외 |
| 실제 Linux `data/**`, `output/**`, Queue/Receipt/processed | **기존 설치본에서 삭제·초기화 금지** |

패키지 크기는 v0.4.38의 1,570,759 bytes에서 **314,842 bytes**로 감소(약 80%). ZIP 내부 58개 파일, 중복/CRC 및 상대 경로 정책 검증.

## 3. 단계별 실제 상태

| 단계 | 상태 | 근거 |
|---|---|---|
| 소스 pin/안전한 재패키징 | PASS | 원본 SHA 고정, 58개 파일 목록, 역사적 상태 제외 |
| ZIP CRC/문법/manifest/버전/Profile | PASS | 격리 Python 검증, `job_core validate` 27 profiles / 오류 0 |
| GitHub Actions 빌드·게시 | PASS | [Run 46112960782](https://github.com/wonhwipark/L1Work/actions/runs/46112960782) success |
| **GitHub ZIP 실제 바이트 SHA-256 재조회** | **PASS** | Base64 응답 재디코딩하여 314,842 bytes, 위 SHA-256과 정확히 일치 |
| Linux Skill Updater 감지·설치 | NOT_VERIFIED | 호스트 영수증 미확인 |
| One-shot 활성화 / Worker 실행 | NOT_VERIFIED | Job/Run ID 실제 영수증 미확인 |
| G0 G01~G09 전체 조사 완료 | NOT_VERIFIED | Linux 결과·상세 코드 분석 미확인 |
| Viewer 자동 업데이트 구현/운영 전환 | NOT_RUN | G0 종료 후 별도 설계 |

참고: 과거 인계 r0003의 `NOT_POSTED`는 **당시 이력**이며, 이 문서의 원격 검증된 **PUBLIC_POSTED=PASS**가 최신 상태. 공개 게시가 운영 설치/활성화/실행 성공을 의미하지 않음.

## 4. 업무 GPT가 실패 시 확인할 순서

| 단계 | 조회 근거 | 복구 정책 |
|---|---|---|
| D01 공개 ZIP | 위 커밋·원격 SHA·크기 | 배송 PASS; 같은 이름 덮어쓰기 금지 |
| D02 cron/Skill Updater | 실제 예약 계정·버전 감지 로그 | 임의 cron 수정, 재실행, 키 변경 금지 |
| D03 설치 | 설치 version, manifest, 영수증, 보존 데이터 | 설치/활성화 분리, Queue·Receipt 보존 |
| D04 활성화 | 예약 hook, 단일 요청, profile, expiry, consumed 확인 | Update-only는 실행 아님; 이전 Job 재큐잉 금지 |
| D05 Worker | Job ID·Run ID·권한·최초 실패 코드 | Linux non-root / canonical root / identity 확인 |
| D06 결과 | `output/viewer_autoupdate_g0/latest_result.json`, per-run evidence·report | 결과 조회 장애는 Worker 재실행 사유 아님 |
| D07 MCP | 같은 ID의 Queue·Catalog·Receipt readback | `RESULT_UNSUPPORTED`와 실행 실패 구분 |
| D08 결과 품질 | G01~09 실측 증거/추정/UNKNOWN 구분 | 정형 지문을 설치 호환성 PASS로 오인 금지 |
| D09 후속 설계 | Updater 기존 lifecycle/hook/rollback 재사용 우선 | 개발 후보 v0.5.8 자동 적용 금지, 변경 별도 승인 |

**즉시 실행 요청:** GitHub 공개 배송 확인 후 업무 GPT는 실제 Linux에 설치된 Job-list 및 최근 cron 영수증을 읽기 전용으로 확인하고, 자동 One-shot이 활성화되어 실행되었는지 확인. 미실행이면 **최초 실패 단계·근거·필요한 한 조치**를 보고하고 승인 없는 수동 재발행/재실행을 하지 말 것. 기존 상태/운영/Knowledge/Kernel/Viewer 코드를 수정하지 말 것. 독립 리뷰 신규 요청 없음.

**회신:** `L1_VIEWER_AUTO_UPDATE_G0_DISCOVERY_RESULT_r0001_YYYYMMDD_KST.md`에 G01~G09 근거, 단계별 PASS/PARTIAL/BLOCKED/UNKNOWN, 기존 기능 재사용 매트릭스, 최소 변경 범위와 G1 입력을 포함. 원본/개인 경로/민감 로그 공개 반출 금지.
