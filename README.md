# L1Work

## Job-list v0.4.39 경량 One-shot 공개 배포 (2026-11-28 KST)

- **[검증된 최종 패키지](job-list_v0_4_39_1128.zip)** — 314,842 bytes / SHA-256 `9d4fd7c31555080df50ce0b7fda728f81f37ad9ca26baf1fd52faf5c0ce03d84`, GitHub 원격 바이트 재조회 PASS.
- Viewer 자동 업데이트를 위한 **G0 읽기 전용 Linux 현장 조사 One-shot 1건**만 활성화. 과거 Job 결과·Queue·다른 스킬 ZIP 제외, 기존 실행 엔진과 persistent 이력 보존 계약 유지.
- **[최신 업무 GPT 실행·실패 복구 인계 r0004](handoffs/L1_VIEWER_AUTO_UPDATE_JOBLIST_PUBLIC_RELEASE_AND_RECOVERY_HANDOFF_r0004_20261128_KST.md)** — 공개 게시 PASS, **Linux Skill Updater 설치·Job 실행·Viewer 자동 업데이트 적용은 미확인/미실행**. 확인은 기존 예약 실행 영수증으로 별도 진행.


## l1-cleanup v0.13.7 릴리스 (2026-11-20 KST)

- **[최종 패키지 l1-cleanup_v0_13_7_1120.zip](l1-cleanup_v0_13_7_1120.zip)** — SHA-256 `a1a2daf42bb079bd7531ce73376f014dff9a2b4218bbd73c99a64be50d90f2f2` (216,672 bytes), GitHub Actions 원격 게시 확인.
- 기존 v0.13.6 기반 최소 개선: P0 Linux 프로세스 FD/maps/cwd 보호 검사(기존 운영 동작 유지를 위해 **`L1_CLEANUP_PROCESS_GUARD_STRICT=1` 명시 설정 시 강화 검사 적용**; `UNKNOWN`이면 차단), P1 기존 HTML 보고서의 폴더·소스별 크기 탐색, P2 읽기 전용 `system-health` 진단.
- **검증:** 신규 2건 + OS 안전 19건 + 기존 안전 82건 + 산출물 6건 = 109건 PASS, ZIP CRC/manifest 전 파일 SHA-256/크기·PACKAGE_CONTENTS 정합성 PASS. Windows 실환경 및 업무 Linux 설치/운영 E2E는 별도 확인 필요. 스킬 설치·LIVE 정책 변경은 수행하지 않음.
- [CI 릴리스 검증 기록](https://github.com/wonhwipark/L1Work/actions/runs/44578645761) · 기존 버전과 정책은 보존.

L1 업무용 스킬 패키지 및 별도 승인된 공개 자료를 제공하는 GitHub PUBLIC 저장소입니다.

## 최신 스킬 ZIP 배포 (2026-11-19)

- **PEC-HOP** — [`code-analyzer_v0_15_4_1119.zip`](code-analyzer_v0_15_4_1119.zip), SHA-256 `11e1da15ee12e750c3652190c348a7fc8e31aa1741876e3c06bc0af3413b16af`
- **ACE** — [`l1-fix-workflow_v1_6_74_1119.zip`](l1-fix-workflow_v1_6_74_1119.zip), SHA-256 `b810ce0cf072609431737c58b0ef2b7a0a8ec0701a0746e6a94283c374224989`
- 두 ZIP 모두 **PUBLIC 게시·원격 바이트 검증 완료**. 코드 독립 리뷰는 이번 두 스킬에 한해 **사용자 요청으로 생략**했으며 자체/패키지 시험 22건 PASS. 실제 업무 Linux `skill-updater` 설치·호스트 기능 검증은 별도. 자세한 인계: [업무 GPT 적용·검증 §15](handoffs/L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md).

## 바로가기

- **[분석 문서 → HTML → MSC 열람 샘플](https://wonhwipark.github.io/L1Work/sample/msc-workspace/)** — [GitHub sample 폴더](sample/README.md). 가상 Work의 분석 문서·MSC 미리보기·확대/단계 이동 뷰어를 연결한 공개 예시예요.
- [업무용 GPT 인계 문서](handoffs/README.md) — 관리 스킬 요약, 기존 도구 재사용 방법 및 역할·접근 권한 표기 기준
- **[CoWork Executive v4 · 업무 진행·검증·남은 일 한눈에 보기](https://wonhwipark.github.io/L1Work/cowork-dashboard/)**  
  **기본 대시보드(사용자 선택 1번)**입니다. 화면 상단에서 **업무 목적–현재까지 확인된 기록–남은 작업**을 한눈에 보고, **업무별 상세 보기**를 누르면 담당·목표 산출물·자체시험과 독립 리뷰 상태를 확인합니다. 시스템 운영·REQUEST/REVIEW/RECEIPT 지표는 하단 접힘형 진단 영역으로 분리했습니다. 공개 허용된 작업 범주 요약만 포함하며 PRIVATE 원문·Work ID·영수증은 게시하지 않습니다. **PRIVATE 변경 → 공개 허용 상태 자동 게시 → Pages 배포 E2E 확인 완료(2026-11-13)**. 상태 생성시각, 전체/공개 Work 차이, 내 조치·리뷰 대기·차단 필터와 검색을 지원합니다. 페이지를 열어둔 동안 2분마다 공개 상태를 재확인하며 탭 복귀 시 다시 확인합니다.
- **[최근 핸드오프 이력 3건 보기](https://wonhwipark.github.io/L1Work/cowork-dashboard/#handoff-status)** — `handoffs/`에 게시된 공개 인계서를 최초 Git 게시일 기준 최신 3건으로 표시하고 각 원문으로 연결합니다. 문서가 추가되면 PUBLIC GitHub Actions가 `docs/cowork-dashboard/handoffs.json`을 갱신하며, 대시보드가 페이지 열기·2분 주기 재확인 시 표시합니다. **다른 GPT에 전달한 사실·피드백 접수·리뷰 완료는 자동 탐지하거나 추정하지 않습니다.** 오래된 문서는 [전체 인계 목록](handoffs/README.md) 또는 [GitHub 폴더](handoffs/)에서 확인합니다.
- **[대시보드 리디자인 시안 3개 비교하기](https://wonhwipark.github.io/L1Work/cowork-dashboard/concepts/)** — Executive / System Topology / Process Journey. **기존 2·3번 시안은 비교용으로 보존**.
- [CoWork HTML 원본 보기](docs/cowork-dashboard/index.html) — GitHub 파일 화면에서는 HTML 소스 표시
- [L1Work 전체 파일·스킬 ZIP 보기](https://github.com/wonhwipark/L1Work) — 기존 배포 파일 및 자료

## 공개 범위

스킬 ZIP은 별도 승인된 파일만 사용합니다. 공개 대시보드에는 PRIVATE 기록에서 선별·검증한 **상위 수준 상태 요약**만 표시합니다. 요청 ID·리뷰 원문·영수증·비밀정보·내부 상세 작업 파일은 공개하지 않습니다. 상태 JSON은 사전에 허용된 공개용 범주·정형 상태·집계 값만 자동 게시하며, 내부 Work ID·원문·고객자료는 전송하지 않습니다. PRIVATE 상태와 PUBLIC에 공개된 상태는 의도적으로 구분됩니다. 자세한 협업 자료는 GitHub PRIVATE에서 관리합니다.

