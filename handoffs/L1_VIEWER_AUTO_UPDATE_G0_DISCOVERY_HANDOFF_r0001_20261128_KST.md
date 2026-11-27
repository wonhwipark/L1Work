# L1 Viewer 자동 업데이트 — G0 현장 조사 인계 r0001
- 상태: 조사 요청 / 구현·배포 미승인
- 대상: 업무 GPT (필요 시 Qwen 또는 Linux MCP의 읽기 전용 조사)
- 목표: 설계 GPT가 공통 Viewer 개발을 유지하고, 기존 Linux cron(사용자 확인: 3시간마다 실행)을 활용해 승인된 Viewer만 LLM 없이 자동 적용.
- 기준: [Skill Updater v0.5.44](../skill-updater_v0_5_44_1027.zip), [Viewer v0.5.8](../l1-workspace-viewer-wiki-integrated_v0_5_8_1127.zip), [통합 개발 인계](L1_SOURCE_MAP_VIEWER_ANALYZER_DEVELOPMENT_DELIVERY_r0001_20261127_KST.md). 게시본과 실제 설치본은 구분. v0.5.8은 개발 후보이며 운영 배포 승인 아님.

## 1. G0 필수 조사
| ID | 확인 대상 | 제출 근거 |
|---|---|---|
| G01 | cron 실제 호출 명령, 실행 계정, 주기, 작업 디렉터리, 중복 실행 방지, 로그 | 비밀값 제거한 설정·최근 실행 결과 |
| G02 | Updater 실제 버전/경로, auto→engine 호출 흐름, GitHub 탐색·버전 선택·다운로드·검증·설치·결과 기록 | 파일:라인, 함수명, 설정 키 |
| G03 | lifecycle.json, preserve 정책, release manifest, skillsilent, staged preinstall, 설치 hook 및 rollback 지원 여부 | 실제 코드 근거, 재사용 가능/불가/미확인 |
| G04 | Viewer 활성 버전, 서비스 종류·실행 경로·document root·포트·재시작 필요 여부 | 읽기 전용 서비스 상태 및 버전 근거 |
| G05 | Viewer 배포 ZIP 대비 운영 파일 차이, 공통 HTML/CSS/JS와 Host Adapter·환경설정·로컬 수정 분류 | 상대경로·해시·차이 유형; 원본 코드 외부 게시 금지 |
| G06 | Adapter API 계약, Kernel/Knowledge/Recovery/MSC/Source Map 의존성, 최소 호환 버전 | 인터페이스 목록 및 호환성 근거 |
| G07 | 기존 설치/백업/복구 방식, 권한, 디스크, 원자적 전환 가능성, 동시 요청·캐시 영향 | 현재 구조 및 제약; 변경 없이 확인 |
| G08 | 실제 배포 승인 신호, 개발 후보 제외 방법, 패키지 SHA-256 및 신뢰 기준, 실패/재시도/알림 경로 | 현재 정책과 부족한 항목 |
| G09 | 자동 smoke test 가능 범위: HTTP, JS/CSS, Work/Knowledge/MSC/Recovery/Source Map, Adapter 읽기 API | 기존 시험 명령/fixture 및 실행 가능 여부; 이번 조사에서는 실행하지 않음 |

## 2. 설계 후보 (확정 아님)
기존 cron → Skill Updater 탐색/검증 → Viewer 설치 hook 또는 격리된 handler → staging → 호환성 및 smoke test → 원자적 활성화 → 상태 확인 → 실패 시 이전 버전 복구 → 영수증.
기존 lifecycle/preserve/hook으로 충분하면 신규 엔진 금지. 부족하면 최소 handler만 제안. 기존 스킬 처리 및 Job-list 동작을 변경하지 않음. Viewer 공통 UI만 교체하고 Host Adapter, 설정, 사용자 데이터, Workspace/Knowledge/Work ledger는 보존. Adapter 변경이 필요한 릴리스는 자동 적용 차단 후 별도 인계. 승인된 manifest와 고정 digest가 없으면 적용 금지. 실패 시 기존 활성 버전 유지, 동일 실패 반복 방지. 브라우저 캐시 및 전환 중 요청 일관성도 검토.

## 3. 회신 계약
업무 GPT는 G01~G09별 PASS(근거 확보)/PARTIAL/BLOCKED/UNKNOWN, 실제 관측값, 파일:라인 또는 비밀 제거한 명령 출력, 차단 사유를 표로 회신. 추정은 별도 표시. 추가로 (1) 현재 호출 흐름 (2) 운영/배포 파일 책임 분류 (3) 기존 기능 재사용 매트릭스 (4) 최소 수정 후보 파일·이유 (5) 권장 방식 A: 기존 hook / B: 최소 handler / C: 별도 updater 중 근거 있는 선택 (6) 후속 G1 설계 입력을 제출.
회신 권장 파일명: L1_VIEWER_AUTO_UPDATE_G0_DISCOVERY_RESULT_r0001_YYYYMMDD_KST.md. 업무 GPT가 승인된 경로로 비민감 요약만 전달; 원본 소스·토큰·내부 주소·사용자 데이터 공개 금지.

## 4. 작업 경계
G0는 읽기 전용 조사만. 코드 수정, 설치, cron 변경, 서비스 재시작, Job 실행, 운영 전환, 독립 리뷰 요청 금지. 실제 경로/권한 부족 시 BLOCKED로 보고하고 추정 구현 금지. 설계 GPT가 회신 검토 후 G1 설계 및 구현 범위를 확정. 기존 Viewer 개발 후보를 자동 적용 대상으로 등록하지 않음.
