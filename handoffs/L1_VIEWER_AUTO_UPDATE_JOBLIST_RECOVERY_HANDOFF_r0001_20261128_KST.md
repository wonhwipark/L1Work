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
