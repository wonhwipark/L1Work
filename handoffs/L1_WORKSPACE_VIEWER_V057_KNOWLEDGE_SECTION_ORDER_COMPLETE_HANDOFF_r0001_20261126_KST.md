# Viewer v0.5.7 Knowledge 표준 섹션 순서 통합 인계 r0001

- 2026-11-26 KST / L1-WORKSPACE-RAG-20261111-001 / wonhwipark/L1Work main
- 단일 신규 Viewer ZIP: [l1-workspace-viewer-wiki-integrated_v0_5_7_1126.zip](../l1-workspace-viewer-wiki-integrated_v0_5_7_1126.zip), 457657 bytes, 46 files, SHA-256 `4a7a7ce742106cebbb4192c250a716ec303ac223ad31fb9673dfe61cb8332ddd`. v0.5.6 원본 보존, 이전 [v0.5.6 완결 인계](./L1_WORKSPACE_VIEWER_V056_TECHNICAL_KNOWLEDGE_READABILITY_COMPLETE_HANDOFF_r0001_20261126_KST.md)의 V56-01~08 및 전체 보호/매핑/설치 게이트 유지. 이전 ZIP 재설치 금지.
- development_not_for_deployment. 이번 전달은 운영 설치·Write ON·Job·그룹 게시 승인이 아님.

## 변경 및 책임
- Scenario: Functional Overview → 동작 조건 → Software Architecture → Scenario Flow → MSC(본문 링크) → 예외 → 제약 → 코드 근거. Module/Feature/Procedure/Issue Knowledge도 기존 역할 목록 순서 적용.
- 기존 verified headingId/headingText/role, docId/workId/documentRevision/sourceRevision 일치 조건 그대로. 동일 계층의 연속된 검증 섹션만 화면에서 순서 조정; 미매핑 섹션은 경계, 하위 제목 및 표·코드·링크는 부모와 함께 이동. 불명확 구조/불일치/레거시 원문 순서 유지. 누락 내용을 생성하지 않음. 원문 보기와 원본 Markdown·ID·링크·권한·writer 불변.
- 설계 GPT: 합성 표시 로직만 변경. 업무 GPT: 기존 read adapter에 실제 제목·유형·섹션 역할을 매핑하고 기존 접근 계약 검증. 새 저장 schema/API/Kernel/Workflow/Updater/Analyzer/Converter/Recovery 변경 금지. 별도 MSC 탭 금지.
- 기존 v0.5.6의 Work 가독성, READ/WRITE/MSC/Recovery/업무 도우미/오늘의 업무/환경설정 기능 유지 대상.

## 확인 및 수락
- 원격 v0.5.6 실제 bytes SHA 및 44 CRC/43 manifest 검증. 변경 이외 기존 36개 파일 SHA 동일. v0.5.7 46 CRC 및 파일별 roundtrip PASS, JS 14개 구문 검사 및 standalone CSP 재생성. 기존 readability-v055와 신규 11개 순서 시험 V8 대역 PASS (실 Node/브라우저 아님).
- V57-01 5유형 역순 원문을 권장 순서로 표시, 본문/목차/빠른 이동 동일.
- V57-02 미매핑 경계·중첩·동일 역할·잘못된 revision·다중 H1 fallback 및 내용 손실 0.
- V57-03 실제 MSC 링크/권한/확대/복귀, 하위 제목·표·코드·deep link·원문 토글 검증.
- V57-04 기존 V56-01~08 및 전체 Node suite(신규 tests/readability-v057.cjs 포함), Chromium/Firefox 320~1440px, 실제 Work/Knowledge/Recovery 사례 확인. 원본 및 권한/스킬 불변.
- 실제 Node/브라우저/업무 호스트/독립 리뷰/운영 설치 NOT_RUN. 업무 GPT는 G0에서 실제 활성 revision/adapter 확인 후 허용 범위 내 시험, 결과·차단·원본 hash/readback과 다음 행동 회신. 실제 문서 원문/MSC는 업무 환경 내 보존.
