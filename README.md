# L1Work

L1 업무용 스킬 패키지 및 별도 승인된 공개 자료를 제공하는 GitHub PUBLIC 저장소입니다.

## 바로가기

- [업무용 GPT 인계 문서](handoffs/README.md) — 관리 스킬 요약, 기존 도구 재사용 방법 및 역할·접근 권한 표기 기준
- **[CoWork Executive v4 · 업무 진행·검증·남은 일 한눈에 보기](https://wonhwipark.github.io/L1Work/cowork-dashboard/)**  
  **기본 대시보드(사용자 선택 1번)**입니다. 화면 상단에서 **업무 목적–현재까지 확인된 기록–남은 작업**을 한눈에 보고, **업무별 상세 보기**를 누르면 담당·목표 산출물·자체시험과 독립 리뷰 상태를 확인합니다. 시스템 운영·REQUEST/REVIEW/RECEIPT 지표는 하단 접힘형 진단 영역으로 분리했습니다. 공개 허용된 작업 범주 요약만 포함하며 PRIVATE 원문·Work ID·영수증은 게시하지 않습니다. **PRIVATE 변경 → 공개 허용 상태 자동 게시 → Pages 배포 E2E 확인 완료(2026-11-13)**. 상태 생성시각, 전체/공개 Work 차이, 내 조치·리뷰 대기·차단 필터와 검색을 지원합니다. 페이지를 열어둔 동안 2분마다 공개 상태를 재확인하며 탭 복귀 시 다시 확인합니다.
- **[최근 핸드오프 이력 3건 보기](https://wonhwipark.github.io/L1Work/cowork-dashboard/#handoff-status)** — `handoffs/`에 게시된 공개 인계서를 최초 Git 게시일 기준 최신 3건으로 표시하고 각 원문으로 연결합니다. 문서가 추가되면 PUBLIC GitHub Actions가 `docs/cowork-dashboard/handoffs.json`을 갱신하며, 대시보드가 페이지 열기·2분 주기 재확인 시 표시합니다. **다른 GPT에 전달한 사실·피드백 접수·리뷰 완료는 자동 탐지하거나 추정하지 않습니다.** 오래된 문서는 [전체 인계 목록](handoffs/README.md) 또는 [GitHub 폴더](handoffs/)에서 확인합니다.
- **[대시보드 리디자인 시안 3개 비교하기](https://wonhwipark.github.io/L1Work/cowork-dashboard/concepts/)** — Executive / System Topology / Process Journey. **기존 2·3번 시안은 비교용으로 보존**.
- [CoWork HTML 원본 보기](docs/cowork-dashboard/index.html) — GitHub 파일 화면에서는 HTML 소스 표시
- [L1Work 전체 파일·스킬 ZIP 보기](https://github.com/wonhwipark/L1Work) — 기존 배포 파일 및 자료

## 공개 범위

스킬 ZIP은 별도 승인된 파일만 사용합니다. 공개 대시보드에는 PRIVATE 기록에서 선별·검증한 **상위 수준 상태 요약**만 표시합니다. 요청 ID·리뷰 원문·영수증·비밀정보·내부 상세 작업 파일은 공개하지 않습니다. 상태 JSON은 사전에 허용된 공개용 범주·정형 상태·집계 값만 자동 게시하며, 내부 Work ID·원문·고객자료는 전송하지 않습니다. PRIVATE 상태와 PUBLIC에 공개된 상태는 의도적으로 구분됩니다. 자세한 협업 자료는 GitHub PRIVATE에서 관리합니다.
