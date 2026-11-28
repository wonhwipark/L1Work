<!-- BEGIN HANDOFF_CURRENT_INDEX: managed by scripts/build_handoff_current_index.py -->
# 인계서 최신 정본 인덱스

> 최신 정본은 명시적으로 검토·등록합니다. 새 인계서 게시와 업무 GPT 실제 적용·운영은 구분합니다. 업데이트 날짜는 등록된 정본·보완 문서의 마지막 Git 커밋 일시 중 최신값(KST)입니다.

| 관리 영역 | 최신 정본 및 보완 문서 | 마지막 문서 업데이트 (KST) | 현재 확인 상태 | 다음 조치 |
|---|---|---|---|---|
| Knowledge Updater | [r0005](L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0005_20261128_KST.md) · [실행 참조](L1_KNOWLEDGE_UPDATER_QWEN36_EXECUTION_REFERENCE_r0005_20261128_KST.md) | 2026-11-28 01:53 | 인계 / G0 대기 | 실제 진입점·SHA 확인 |
| Source Map | [통합 r0003](L1_SOURCE_MAP_1500_UPDATER_INTEGRATED_HANDOFF_r0003_20261127_KST.md) · [파일럿 r0001](L1_SOURCE_MAP_EXTRACTION_PILOT_HANDOFF_r0001_20261128_KST.md) | 2026-11-28 12:20 | 인계 / 파일럿 대기 | 대표 모듈 근거 대조 |
| Viewer · Code Analyzer | [Viewer v0.5.8 / Analyzer v0.15.7](L1_SOURCE_MAP_VIEWER_ANALYZER_DEVELOPMENT_DELIVERY_r0001_20261127_KST.md) | 2026-11-27 02:22 | 개발 패키지 게시 / 운영 미확인 | 회귀·활성본 검증 |
| Channel Recovery | [통합 r0008](L1_RECOVERY_POINT_ANALYSIS_INTEGRATED_IMPLEMENTATION_HANDOFF_r0008_20261127_KST.md) | 2026-11-27 16:09 | 인계 / 실행 미확인 | Seed 1건 V2·V3 회귀 |
| Viewer 자동 업데이트 · Job-list | [검증된 ZIP 배포 r0004](L1_VIEWER_AUTO_UPDATE_JOBLIST_PUBLIC_RELEASE_AND_RECOVERY_HANDOFF_r0004_20261128_KST.md) · [G0 조사](L1_VIEWER_AUTO_UPDATE_G0_DISCOVERY_HANDOFF_r0001_20261128_KST.md) · [장애 복구 r0002](L1_VIEWER_AUTO_UPDATE_JOBLIST_RECOVERY_HANDOFF_r0002_20261128_KST.md) | 2026-11-28 14:39 | 배포 완료 / Linux 설치·실행 미확인 | cron·Updater 영수증 및 G01~G09 결과 확인 |
| Job-list · Agent MCP | [통합 r0001](L1_JOBLIST_KNOWLEDGE_UPDATER_RECOVERY_MCP_EXECUTION_RESULT_HANDOFF_r0001_20261128_KST.md) | 2026-11-28 01:51 | 인계 / 호스트 G0 대기 | 기존 Run·Result 조회 확인 |
| Project Control Center | [구축 r0001](L1_PROJECT_CONTROL_CENTER_WORK_GPT_HANDOFF_r0001_20261128_KST.md) | 2026-11-28 10:39 | 인계 / 업무 적용 미확인 | 권한·환경 G0 조사 |

## 신규·변경 인계서 (정본 미분류)

현재 정본 인덱스 생성 기준 이후 신규·변경 미분류 문서는 없습니다. 새 문서는 정본 자동 승격 대신 이곳에 표시됩니다.

기존 인계서와 검증 기록은 아래의 작성 당시 이력을 보존합니다.
<!-- END HANDOFF_CURRENT_INDEX -->

---

## 기존 인계서 이력 (작성 당시 기준)

## Knowledge Updater r0005 · 업무 GPT 실행 인계 (2026-11-28)

[통합 인계서 r0005](L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0005_20261128_KST.md) · [Qwen 실행 참조서](L1_KNOWLEDGE_UPDATER_QWEN36_EXECUTION_REFERENCE_r0005_20261128_KST.md) · Work `L1-WORKSPACE-RAG-20261111-001`

업무 GPT는 G0-1에서 실제 호출 진입점의 SHA-256을 먼저 확인하세요. Source Map, Procedure G-2, 기존 Knowledge 문서의 실행 순서와 확대·중단 기준은 통합 인계서 첫 페이지에서 확인할 수 있어요.

---

## LTE/NR L1 Source Map · 업무 GPT 통합 인계 (2026-11-27)

[최신 통합 인계서 r0003](L1_SOURCE_MAP_1500_UPDATER_INTEGRATED_HANDOFF_r0003_20261127_KST.md) · Work `L1-WORKSPACE-RAG-20261111-001`

업무 GPT는 1절 요청문으로 시작해 기존 Discovery 7건을 3절의 관계표와 대조하고, 8절 양식으로 회신해 주세요. 5절에는 합성 레코드와 변경·삭제 전후 예시가 있어요.

---

## Source Map 책임 경계와 Viewer·관리 스킬 수정 범위 (2026-11-27)

- [기존 책임 경계 인계 r0001](L1_SOURCE_MAP_KNOWLEDGE_UPDATER_VIEWER_SCOPE_HANDOFF_r0001_20261127_KST.md) · 기존 Work `L1-WORKSPACE-RAG-20261111-001`. 기존 Knowledge·MSC 역할, Analyzer의 빌드 분기 반례, Viewer 최소 표시 범위와 자체 회귀·현장 수락 기준을 담았어요.
- 다음은 업무 GPT의 활성 Updater·Discovery 7건·G6 범위 확인이에요. [기존 읽기 전용 G0 인계](L1_SOURCE_MAP_LLM_FIRST_G0_HANDOFF_r0001_20261127_KST.md)

---

## Source Map LLM-first — 업무 GPT 읽기 전용 G0 (2026-11-27)

- [G0 인계 r0001](L1_SOURCE_MAP_LLM_FIRST_G0_HANDOFF_r0001_20261127_KST.md) · [통합 상세 설계 r0002](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/3ee216ff501172a164958e91106053c1ed6cd1f9/collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_SOURCE_MAP_LLM_FIRST_INTEGRATED_DESIGN_r0002_20261127_KST.md)
- 기존 Discovery 결과, 추출 신뢰도, G6 승인 범위, 저장/조회/Viewer/MCP 계약 및 모델 예산 확인. 사용자 지시로 추가 독립 리뷰 생략. 코드 수정·실행·설치·게시 승인 아님.

---

## Viewer v0.5.7 — Knowledge 표준 섹션 순서 (2026-11-26)

- [업무 GPT 단일 인계](./L1_WORKSPACE_VIEWER_V057_KNOWLEDGE_SECTION_ORDER_COMPLETE_HANDOFF_r0001_20261126_KST.md) · [전체 ZIP](../l1-workspace-viewer-wiki-integrated_v0_5_7_1126.zip)
- 검증된 동일 계층 섹션 순서 정렬·목차 동기화, 원문·MSC 링크·기존 스킬 유지. 457657 bytes / SHA-256 `4a7a7ce742106cebbb4192c250a716ec303ac223ad31fb9673dfe61cb8332ddd`. V8 대역 및 ZIP 검증 PASS; 실제 Node/브라우저/업무 호스트/독립 리뷰/운영 설치 NOT_RUN. development_not_for_deployment.

---

## Viewer v0.5.6 — 기술 Knowledge·Work 가독성 통합 개발 인계 (2026-11-26)

- [업무 GPT 단일 인계 r0001](./L1_WORKSPACE_VIEWER_V056_TECHNICAL_KNOWLEDGE_READABILITY_COMPLETE_HANDOFF_r0001_20261126_KST.md) · [Viewer v0.5.6 전체 ZIP](../l1-workspace-viewer-wiki-integrated_v0_5_6_1126.zip)
- 기술 레퍼런스 유형별 표현, Work 업무명·상단 상태 요약, 문서 내 MSC 링크 유지. 실제 업무 필드 매핑은 업무 GPT 담당. 원본·기존 스킬 변경 없음.
- ZIP 446,659 bytes / SHA-256 `147c414777e6fd368520e7a7e7b9c8298c9fa047f2411d8525191e7b91c77343`. V8 대역 5개 시험 프로그램·제한 DOM 단언 7개·패키지 검증 PASS. 실제 Node/브라우저/업무 통합·독립 리뷰·운영 설치 NOT_RUN. development_not_for_deployment.

---

## Job-list PcellTxPathOnOff API 프로시저 MSC — 단일 실행 프롬프트 (2026-11-25)

- **[업무 GPT 실행 프롬프트](JOBLIST_PCELL_TX_PATH_ON_OFF_PROCEDURE_MSC_PROMPT_r0001_20261125_KST.md)** — 실제 활성 `job-list`의 one-shot 경로에서 `code-analyzer`로 정확한 심볼의 caller/guard/callee/상태·비동기 흐름을 코드 근거로 분석하고 Procedure MSC 생성. 지원되는 경우 `doc-converter` PUML/SVG/HTML로 변환해 동일 Work/Evidence에 저장·재조회.
- 공개 문서 업로드만 수행. 실제 제품 소스 접근·Job 등록·실행·모델 호출·MSC 생성·Linux MCP 검증·운영 설치 **NOT_RUN**. Analyzer v0.15.6 공개 ZIP은 개발 후보이며 강제 설치하지 않음.

---

## L1 Channel Recovery 통합 설계·구현 인계 r0007 (2026-11-25)

- **[업무 GPT 최신 단일 인계 r0007](./L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0007_20261125_KST.md)**. V2는 수정 전·후·정상 반례, V3는 탐색 상한과 실제 조사량, V4는 첫 위반 전 보호와 종결 반대 근거를 대조해요. 현행 기준선과 보강한 단일 실행을 비교한 뒤 반복 오류가 남은 단계만 선택적으로 분리해요.
- 원격 확인용 SHA-256 `12f3f1274a766c01ebac31007ab75a6c8e228fb9afbd433437685eca920f4e18`, 54,103 B. 업무 GPT에 전달할 요청문은 1절에 있어요. 신규 정식 독립 리뷰·업무 호스트 G0·Qwen 비교·실제 Work/Viewer 통합·제품 효과 시험은 `NOT_RUN`이에요.

## L1 Channel Recovery 통합 설계 가이드 r0006 — 이전 버전 보존 (2026-11-25)

- **[업무 GPT 이전 단일 인계 r0006](./L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0006_20261125_KST.md)** — r0005 분석·MSC 의미 검증을 유지하고 Recovery, 기존 Work writer/Kernel, Viewer의 구현 책임·완료 판정을 분리해요. Viewer/Kernel 내부 수정·설치는 Recovery 구현 범위에서 제외하고, 기존 인터페이스 재사용과 실패 단계별 재개만 요구해요.
- 원격 확인용 SHA-256 `291c675185fe5ab7e0c6561f8ec823ac38586968b9fa42e7b1bdbf48857c4518`, 43,073 B. Analyzer v0.15.6은 별도 개발 후보로 전체 회귀·설치 자체검사 전 운영 설치 금지. r0006 독립 리뷰·업무 호스트·실제 분석/MSC/저장/Viewer 및 제품 시험은 NOT_RUN이에요.

## L1 Channel Recovery 통합 설계 가이드 r0005 — 이전 버전 보존 (2026-11-25)

- **[업무 GPT 이전 단일 인계 r0005](./L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0005_20261125_KST.md)**. 비-timeout Seed 1건에서 활성 Analyzer의 탐색 범위와 코드 근거를 대조해요. 호출·등록·보호 순서의 누락과 오탐을 측정하고, 검증된 MSC를 같은 Work에서 HTML/SVG로 열람해요.
- 원격 확인용 SHA-256 `7564af19bcdba3aeaa25c951826b80e7cf179284aea2f37c99da4df931693ae8`, 37,084 B. 공개 Analyzer v0.15.5는 격리 설치 자체검사가 실패해 설치 보류예요. r0005 신규 독립 리뷰, 업무 호스트 G0·Qwen 실행·제품 및 MSC/Viewer 통합 시험은 `NOT_RUN`이에요.
- [직전 단일 인계 r0004](./L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0004_20261125_KST.md)에는 [r0003 설계 심사 원본](./L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0003_20261125_KST.md)의 독립 리뷰 M1·N1·N2·N3가 반영됐어요. r0004는 25,780 B, SHA-256 `ab8b98c5a99a83011f76b1e9068e75a155c26873f4dbefdff63290eaf656661d`예요.

---

## Qwen 기반 Knowledge Updater 분석 품질 및 책임 경계 — 최신 r0002 (2026-11-25)

- **[업무 GPT 최신 통합 인계 r0002](./L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0002_20261125_KST.md)** — 기존 Updater 분석·지식 관리 책임 유지, Kernel/Workflow/Viewer 내부 구현 제외. 원본 근거 검증·실제 탐색 상한·MSC 의미 대조·개인 Knowledge/그룹 Preview 및 게시 보호·단계별 검증·OpenCode 실행 환경을 통합. A1~D3 및 대표 수락 시험 18개 포함.
- 원격 확인용 SHA-256 `365816fc1b502562fed353968f75471495fedc521531ede2955f755b092a2fbe`, 41,286 B. 기존 활성 Analyzer 유지, v0.15.6은 별도 개발 후보로 전체 회귀·설치 self-check 전 운영 설치 금지. 신규 독립 리뷰·업무 호스트·실제 Updater/MSC/Work/Knowledge/Viewer·그룹 게시/야간 실행 NOT_RUN.
- 11/11 Workflow r0005와 11/17 동기화 R1의 READ_ONLY 조사·권한 보호는 유지. 이번 Updater 분석 품질 개선 범위만 r0002 우선이며 인계 자체는 설치·실행·write 승인이 아님.

## Qwen 기반 Knowledge Updater 분석 품질 개선 + Code Analyzer 개발 후보 — 이전 r0001 보존 (2026-11-25)

- **[업무 GPT 이전 구현 인계 r0001](./L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0001_20261125_KST.md)** — 실제 Analyzer·Converter 호출, 분석 준비/근거·커버리지·MSC/Work/Viewer 단계별 검증, 현장 최소 보완·회귀·회신 요구.
- **[Code Analyzer v0.15.5 전체 개발 ZIP](../code-analyzer_v0_15_5_1125.zip)** — 594,930 bytes / SHA-256 `61099248ab0a4b2597ca8316e613f5987caaee671d735337eea1e0f70a6c2877`. callers/callees scope 제한 및 anchor/partial coverage 개선. v0.15.4 보존.
- 상태: 격리 9 PASS, ZIP CRC/manifest PASS; 전체 suite·독립 코드 리뷰·실제 업무 Linux/LLM E2E NOT_RUN. development_not_for_deployment; 자동 설치 금지.

---

## Recovery Viewer v0.5.3 + Kernel v0.7.47 — 신규 통합 인계 (2026-11-24)

- **[업무 GPT 단일 통합 HO](L1_CHANNEL_RECOVERY_VIEWER_KERNEL_CONVERTER_COMPLETE_HANDOFF_r0001_20261124_KST.md)** — 업무 GPT의 Recovery Seed 전후/AS-IS·TO-BE doc-converter HTML/SVG 생성, 기존 Work/Evidence 등록·Kernel recovery/ 파생 탐색·Viewer MSC 연결. v0.5.2 기존 UI/Write/도우미 계약 전체 보존.
- **[Viewer 전체 ZIP v0.5.3](../l1-workspace-viewer-wiki-integrated_v0_5_3_1124.zip)** — 399,993 bytes / SHA-256 `9fe5d6cce9ac7064152099e183cdeee21421a0cefe9044ce48d39db686b67411`. 기존 v0.5.2 기능 보존, Recovery 읽기·상세·MSC artifact callback.
- **[Kernel 전체 ZIP v0.7.47](../work-ledger-kernel_v0_7_47_1124.zip)** — 406,507 bytes / SHA-256 `5c1f73a09b2cd8c4ec93134f387ed7f80cec799b534f2d044978b66e6c38b20c`. Recovery v0.7.46 + Viewer Write guard v0.7.43 병합, 물리적 recovery/ 파생 보기.
- 상태: 개발용 PUBLIC ZIP 배송과 업무 Linux 실제 설치·독립 리뷰·Browser/Converter E2E는 구분. 개발 패키지는 development_not_for_deployment.

---

# 업무용 GPT 인계 문서

## Viewer 최신 통합 인계 — v0.5.2 + Updater/Converter MSC HTML 연결 (2026-11-24)

- **[업무 GPT 최신 단일 인계 r0002](./L1_WORKSPACE_VIEWER_V052_MSC_UPDATER_CONVERTER_COMPLETE_HANDOFF_r0002_20261124_KST.md)** — 실제 Updater→doc-converter 호출·HTML/SVG 생성·Workspace artifact/Evidence 등록·Viewer 링크 표시를 단계별 조사. r0001의 전체 UI·Write·도우미 계약과 A01~A10/H01~H05, MSC T1~T8 보존. 최신 현장 회신 양식 포함.
- **[Viewer v0.5.2 전체 ZIP](../l1-workspace-viewer-wiki-integrated_v0_5_2_1124.zip)** — 374,930 bytes / SHA-256 `15e83f136fa10ef680619602b55d74c4cd4c0c86a6cc470c1bec9cac250239ba`; **이번 Viewer 구현 입력은 r0002 + 이 ZIP 하나**. [기존 v0.5.2 가독성 완결 인계 r0001](./L1_WORKSPACE_VIEWER_V052_READABILITY_COMPLETE_HANDOFF_r0001_20261124_KST.md)은 r0002에 원문 보존.
- **시험 상태 분리:** v0.5.1 게시본의 [후속 Node 재검증](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/51c436e96821aa3d86fb4c8adf978f63b140773e/collab/projects/L1-WORKSPACE-RAG-20261111-001/VIEWER_V051_POST_UPLOAD_VERIFICATION_r0001_20261123_KST.md)은 **25 PASS(10+15)**. **v0.5.2 Node 3개·브라우저 E2E·실제 업무 Linux G0·MSC HTML 링크·Write/LLM/Agent/운영 적용은 NOT_RUN**; 과거 버전 PASS를 최신 버전에 대입하지 않음.
- **운영 경계:** `development_not_for_deployment`. 인계/ZIP 공개 게시는 실제 설치·Converter 호출·현장 적용 완료가 아님. 실제 원본 코드·MSC·로그·인증정보는 업무 Work에만 보존. 기존 승인 범위에서 현장 G0→최소 연결·회귀시험→비민감 상태 회신.

---

## Viewer v0.5.1 — 2026-11-23 (단일 완결 인계)

- [v0.5.1 신규 통합 ZIP](../l1-workspace-viewer-wiki-integrated_v0_5_1_1123.zip) — 349332 bytes / SHA-256 `0bc0240261e29c863c541e9650e9f99271b2b924ffd52be753598889f66cf290`, 기존 v0.5.0 불변
- [업무 GPT 최종 인계서](./L1_WORKSPACE_VIEWER_V051_TODAY_ASSISTANT_HANDOFF_r0001_20261123_KST.md) — v0.5.0 계약 전체 포함, 이전 문서 별도 전달 불필요
- [미리보기](./L1_Workspace_Viewer_v0_5_1_20261123_KST.html) · [개발 결과](./L1_WORKSPACE_VIEWER_V051_DEVELOPMENT_RESULT_20261123_KST.md) · [체크섬](./L1_WORKSPACE_VIEWER_V051_SHA256SUMS_20261123_KST.txt)


## L1 Knowledge Updater — 야간 모듈·Procedure·MSC 분석 설계 (2026-11-23)

- **[업무 GPT 실행 인계 r0001](L1_KNOWLEDGE_UPDATER_NIGHTLY_MODULE_PROCEDURE_MSC_HANDOFF_r0001_20261123_KST.md)** — 기존 Updater/Code Analyzer/Converter를 우선 재사용하고 NR UL Tx Switching 1건의 근거·MSC·개인 Work readback 검증 후 야간 예약 가능 여부 판정. **문서 게시 완료, Linux 실행·야간 예약·그룹 지식 게시 NOT_RUN**.
- **Code Analyzer 판정:** 기존 공개 `code-analyzer v0.15.4`에 bounded probe/State·IPC·Callback/Procedure·MSC·revision 검증 기능이 있으므로 이 단계에서 **불필요한 코드 수정·신규 ZIP 발행 없음**. 현장 시나리오에서 재현된 실제 gap만 후속 최소 수정 검토.

---

## Viewer v0.5.0 — 오늘의 업무·우측 업무 도우미 (2026-11-22)

- **[업무 GPT 인계서](L1_WORKSPACE_VIEWER_V050_TODAY_ASSISTANT_HANDOFF_r0001_20261122_KST.md)** · [전체 개발 ZIP](../l1-workspace-viewer-wiki-integrated_v0_5_0_1122.zip) · [단독 HTML 미리보기](L1_Workspace_Viewer_v0_5_0_20261122_KST.html)
- v0.4.1의 제목·너비·필터 개선 포함. 우측 목차/도우미, 오늘 업무 탭, Work별 대화·상태·영수증·결과 연결. **기본 합성 예시, 실제 LLM/Agent 호출·운영 적용 없음.**
- 자체시험 25 PASS / 실제 브라우저·호스트 검증은 사용자 지시대로 업무 환경에서 진행. development_not_for_deployment. [개발 결과](L1_WORKSPACE_VIEWER_V050_DEVELOPMENT_RESULT_20261122_KST.md) · [SHA-256](L1_WORKSPACE_VIEWER_V050_SHA256SUMS_20261122_KST.txt)

---

## Viewer 2안 Wiki 통합 UI v0.4.0 (2026-11-21)

- **[업무 GPT 통합 Viewer v0.4.0 G0/E2E 인계](L1_WORKSPACE_VIEWER_WIKI_INTEGRATED_V040_G0_AND_E2E_HANDOFF_r0001_20261121_KST.md)** · [통합 20파일 ZIP](../l1-workspace-viewer-wiki-integrated_v0_4_0_1121.zip) · [단독 HTML 미리보기](L1_Workspace_Viewer_Wiki_Integrated_Preview_v0_4_0_20261121.html)
- 팀 위키형 Blue Gray + Write UI v0.2.0 + 환경설정 v0.3.0 + 메뉴·폴더 숨김/탐색 복원 통합. **공개 개발 패키지 전달 PASS / 실제 Linux 브라우저·쓰기 E2E·운영 적용 NOT_RUN**. 기존 r0001~r0003, 이전 ZIP·리뷰·영수증 보존.

---

## Viewer Write — Workflow v1.6.75 / Kernel v0.7.43 전체 스킬 개발 패키지 (2026-11-21)

- **[업무 GPT 우선 실행 인계 r0003](L1_WORKSPACE_VIEWER_WRITE_WORKFLOW_KERNEL_FULL_SKILLS_HANDOFF_r0003_20261121_KST.md)** — 기존 [r0002 통합 연동 HO](L1_WORKSPACE_VIEWER_WRITE_V020_WORKFLOW_KERNEL_E2E_ONESHOT_HANDOFF_r0002_20261121_KST.md) 보완. 최신 두 스킬의 **수정된 전체 ZIP**과 원본 ZIP SHA·단위/모의시험·기존 전체 회귀/실제 Linux Write E2E 미검증 경계 명시. **실제 호스트 사용은 별도 G0·보안/운영 승인 게이트**.
- **[l1-fix-workflow v1.6.75 전체 ZIP](../l1-fix-workflow_v1_6_75_1121.zip)** — **832,039 B**, SHA-256 `fd337ee31e09c9f694146c9d159799ca7182af052c93121e73888a9ee367a0a1`, 315 entries; Viewer Write canonical Work ID/document/revision routing, SDK/README/release/manifest/단위시험 포함.
- **[work-ledger-kernel v0.7.43 전체 ZIP](../work-ledger-kernel_v0_7_43_1121.zip)** — **379,642 B**, SHA-256 `9866ff7164884b0fb346bd31d37dbdf2013b5e5910e5857f8e35075624cf92f1`, 166 entries; 기존 잠금 CAS writer 위임·세션/ACL/원본 재검사·영수증/readback helper, 단위시험·manifest 포함.
- **판정:** GitHub 원격 바이트·전체 ZIP CRC/manifest PASS, 기존 모듈 시험 Workflow 8/8+Kernel 13/13+교차 4/4+staging 5/5 PASS. **전체 기존 스킬 suite/실 Linux G0·B1~B3·E3/E4·운영 WRITE ON=NOT_RUN**. 신규 버전은 `development_not_for_deployment`, 승인된 최종 배포/운영 설치본 아님. 기존 v1.6.74/v0.7.42 불변 보존.

---

## Viewer Write v0.2.0 × Workflow/Kernel — 업무 GPT E2E 인계 r0002 (2026-11-21)

- **[업무 GPT 우선 실행 HO: Write v0.2.0 + l1-fix-workflow + work-ledger-kernel 통합](L1_WORKSPACE_VIEWER_WRITE_V020_WORKFLOW_KERNEL_E2E_ONESHOT_HANDOFF_r0002_20261121_KST.md)** — 실제 업무 Linux 설치본 G0 확인 후 기존 Work 선택·Workflow/Kernel/CAS·writer 연동→초안·Diff·저장·Evidence/revision readback→Viewer 반영을 원샷으로 실행. Workflow/Kernel은 필수 연결, **수정은 입증된 gap에만 최소 범위**. 설정 v0.3.0 공존/Read Only·보안/MSC 별도 게이트. **HO 게시만으로 업무 GPT 수신·호스트 E2E/운영 설치 완료 아님**.
- 실행 입력: [Viewer Write UI v0.2.0 개발 ZIP](../l1-workspace-viewer-write-ui_v0_2_0_1121.zip), [Viewer v0.1.2 UI ZIP](../l1-workspace-viewer-ui_v0_1_2_1121.zip), [환경설정 v0.3.0 ZIP](../l1-workspace-viewer-preferences_v0_3_0_1121.zip). 기존 [Write HO r0001](L1_WORKSPACE_VIEWER_WRITE_V020_G0_AND_INTEGRATION_HANDOFF_r0001_20261121_KST.md)은 이력으로 유지.

---

## Viewer 환경설정 v0.3.0 개발용 전달 (2026-11-21)

- **[환경설정 v0.3.0 소스·패치·시험 ZIP](../l1-workspace-viewer-preferences_v0_3_0_1121.zip)** — 20,661 B / SHA-256 `228c60bada8a92591f7ae855dfabe206e018d9e59970cf2d1b773d4d00072812`. 기존 Viewer v0.1.2/Write v0.2.0 유지, 사용자별(익명은 브라우저별) 표시·숨김/문서 유형 필터/화면 설정/로컬 저장·초기화 추가. Node 16/16 + Python 14/14 PASS, ZIP CRC PASS, **실 Linux DOM/CSP/브라우저·운영 설치 NOT_RUN**, `development_not_for_deployment`.
- **[환경설정 Linux G0 연동·조건부 적용 인계](L1_WORKSPACE_VIEWER_PREFERENCES_V030_G0_INTEGRATION_HANDOFF_r0001_20261121_KST.md)** — 화면 매핑/사용자 식별·저장 정책/기존 Write 공존과 원본 무변경 확인, 재현 시험·안전 배포 조건.

---

## Viewer 2차 Write 기능 — 개발 후보·업무 GPT 연결 (2026-11-21)

- **[Viewer Write UI v0.2.0 개발 ZIP](../l1-workspace-viewer-write-ui_v0_2_0_1121.zip)** — L1Work/main 루트 21,171 B, SHA-256 `9f2df44348478eb44615bddef8f211645fa1c07ed71d43580b4fb324e376b6f9`, 10-file CRC PASS, 원격 bytes PASS. **개발용 전달 예외**, Linux Write 활성화·운영 배포 NOT_RUN.
- **[Viewer v0.2.0 편집 UI 연결 및 실제 Linux G0 인계](L1_WORKSPACE_VIEWER_WRITE_V020_G0_AND_INTEGRATION_HANDOFF_r0001_20261121_KST.md)** — 기존 동료 무로그인 Read Only 유지, [수정] 전용 인증·이슈 본문/MSC 변경 요청·Diff/Preview·초안/저장 흐름의 프런트엔드 개발 후보와 서버 보안·원본 writer 재사용 게이트를 정리. **UI 개발 자체시험 30+8 PASS**이나 실제 Linux 인증·CSRF·ACL·Writer·B1~B3/E3/E4 및 운영 Write는 NOT_RUN. v0.2.0 개발 ZIP은 **L1Work/main 루트에 PUBLIC 배송·SHA 검증 PASS**. 기존 1차 v0.1.2 ZIP/운영 보존.

---

## L1 Workspace Viewer 1차 v0.1.2 배송 (2026-11-21)

- **[Viewer v0.1.2 ZIP](../l1-workspace-viewer-ui_v0_1_2_1121.zip)** — 74,940 B / SHA-256 `9be14c4c34c2a7d923d8b11c01fb0249d41e820861721f275001f0f7d499d9e3`. 이슈번호 선두·Work ID 보조 표시, 블루그레이 색감·MSC 방향 안내. **사용자 최신 지시로 독립 스타일 리뷰 생략 후 PUBLIC 전달 완료**. 합성 정적 UI 포함, Linux 현장 적용·보안·실동료 시험은 미실행.
- **[업무 GPT 1차 Linux Viewer 이식·시험·조건부 배포 원샷](L1_WORKSPACE_VIEWER_FIRST_PHASE_V012_G0_DEPLOY_HANDOFF_r0001_20261121_KST.md)** — 기존 로그인 없는 Read Only, B1~B3·E3/E4·백업/rollback 필수. 실제 설치가 끝났다고 보고하지 않음.

---

> **2026-11-21 전달 예외(사용자 최신 지시):** `knowledge_analysis_preflight_v0_2_0_1121.zip`가 L1Work/main 루트에 **개발용 분석 보조 ZIP**으로 공개 전달됨. 독립 리뷰 R2는 미실행(사용자 지시로 리뷰·별도 GPT 판정 생략). 실제 Updater 연동·C++/MSC/Workspace E2E 검증은 아직 안 됐으며 **자동 설치/운영 사용 승인 아님**. 후속 작업은 [업무 GPT Updater 통합 인계 r0002](L1_KNOWLEDGE_UPDATER_NR_UL_TX_SWITCHING_MODIFICATION_REQUIREMENTS_r0002_20261121_KST.md)를 우선 적용. 기존 r0001은 보존/HOLD.

## NR L1 Tx UL Tx Switching — 분석 보조 ZIP 공개 전달 및 업무 GPT 통합 r0002 (2026-11-21)

- **[분석 보조 ZIP: knowledge_analysis_preflight_v0_2_0_1121.zip](../knowledge_analysis_preflight_v0_2_0_1121.zip)** — 16,138B / SHA-256 `90a0d55842138d4c813f0dbc3a5c8e4625e84a110afe68035348297ffedad1f3`. 리뷰/별도 판정 사용자 생략에 따른 개발용 전달 예외, 호스트 설치용 검증본 아님.
- **[업무 GPT 통합 구현 요구 r0002](L1_KNOWLEDGE_UPDATER_NR_UL_TX_SWITCHING_MODIFICATION_REQUIREMENTS_r0002_20261121_KST.md)** — 설치 Updater/Analyzer/Converter 실제 계약 대조 후 NR L1 Tx UL Tx Switching의 bounded evidence·MSC·개인 Workspace write/readback을 검증. 기존 r0001 HOLD.

---

> **2026-11-21 최신 우선순위 정정:** NR L1 Tx 지식 개선은 **설계 GPT의 분석 보조 구현·자체시험 → CoWork Claude 독립 리뷰 → GPT 판정 → L1Work 최종 ZIP 배포 → 그 후 업무 GPT Updater 연동 요구(r0002)** 순서다. 현재 [기존 Updater 우선 수정 요청 r0001](L1_KNOWLEDGE_UPDATER_NR_UL_TX_SWITCHING_MODIFICATION_REQUIREMENTS_r0001_20261121_KST.md)은 **HOLD/이력 보존**이며 업무 GPT의 수정 시작 트리거가 아니다. PRIVATE 리뷰 `REQ-L1-KNOWLEDGE-PREFLIGHT-V020-R1-20261121` 제출. ZIP은 아직 PUBLIC 배송되지 않았다.


## NR L1 Tx UL Tx Switching — 업무 GPT Updater 실제 수정 요구 (2026-11-21)

- **[최신 구현 요청 R1~R8: 설치 Updater 확인 → 기존 Analyzer/Converter 재사용 → 부족분 수정·시험 → 협업 독립 리뷰 → 승인된 ZIP 배포](L1_KNOWLEDGE_UPDATER_NR_UL_TX_SWITCHING_MODIFICATION_REQUIREMENTS_r0001_20261121_KST.md)** — G0 보고에서 종료하지 말고 허용된 변경·회귀시험까지 연속 진행. 실제 업무 GPT 수신·호스트 실행·리뷰·최종 ZIP 배송은 아직 `NOT_VERIFIED/NOT_RUN`.

---


## NR L1 Tx UL Tx Switching — 저사양 LLM·라이선스·MSC 검증 인계 (2026-11-21)

- **[실제 Updater/Code Analyzer/doc-converter 계약 G0 및 저사양 LLM·코드 MSC 호환 검증](L1_KNOWLEDGE_UPDATER_LOW_RESOURCE_LLM_MSC_G0_AND_INTEGRATION_HANDOFF_r0001_20261121_KST.md)** — 논문·상용의 아이디어 차용(외부 코드 포함 0), bounded code evidence, 기존 Converter native Scenario IR/PUML/SVG/B형 HTML 재사용. 독립 합성 후보 12 PASS이나 **실제 설치 스킬 수정·업무 Linux E2E·PUBLIC ZIP 배포는 미실행/차단**. 기존 NR Switching 단일 사례 실행 인계와 동일 Work로 연결.

---


## Viewer 2단계 개선 — 업무 GPT 원샷 구현 인계 (2026-11-20)

- **[최신 Viewer 통합 인계: 이슈번호 SOC-xxx 선두·Work 제목 통일 → 수정 버튼 전용 인증·이슈/MSC 편집](L1_WORKSPACE_VIEWER_TWO_PHASE_IMPLEMENTATION_ONESHOT_HANDOFF_r0001_20261120_KST.md)** — 기존 PUBLIC `l1-workspace-wiki-ui_v0_1_0_1119.zip`과 앞선 Viewer UI 변경서 r0002를 재사용. 동료 무로그인 Read Only 유지, Work ID/폴더/근거 불변, canonical MSC/Writer 보안 게이트와 Linux G0 확인을 분리. **인계서 PUBLIC 게시 완료 / 실제 업무 GPT 수신·Linux 구현·호스트 배포 NOT_VERIFIED/NOT_RUN**.

---

## NR L1 Tx UL Tx Switching — Agent MCP 지식 검토→개인 Workspace 갱신 1건 (2026-11-20)

- **[실행 인계: l1-knowledge-updater 실제 분석 → l1-workspace 동일 Work 저장 → readback → 사용자 결과 표시](NR_L1TX_UL_TX_SWITCHING_KNOWLEDGE_AGENT_MCP_ONE_SHOT_HANDOFF_r0001_20261120_KST.md)** — 범용 MCP 기능 연결의 대표 실사용 시나리오. 제품 코드/그룹 Knowledge 변경은 제외. **문서 전달만 완료**, 실제 Linux MCP 호출·분석·개인 Workspace 저장/재조회는 아직 `NOT_RUN`.

---


## Linux MCP 업무 스킬 접근 — Viewer 진단과 분리 (2026-11-20)

- **[최신 업무 GPT 인계: 기존 L1 스킬 기능의 MCP 연결·호출 계약·P0 실호출 검증](L1_MCP_AGENT_SKILL_ACCESS_AND_CAPABILITY_HANDOFF_r0002_20261120_KST.md)** — 사용자 결정: Viewer는 브라우저용 별도 UI이며 MCP의 상시 업무 접근 경로가 아님. 모바일 Agent → Linux MCP → 기존 Workflow/Kernel/Analyzer/Knowledge Updater/Job의 실제 허용 인터페이스를 G0 조회하고 REUSE/CONNECT/최소 EXTEND. 조회와 분석·게시·설치·실행 승인을 구분하며 업무 GPT가 현장 실호출 근거로 판정.
- 기존 [Viewer 중심 MCP r0001](L1_MCP_AGENT_READONLY_CAPABILITY_AND_VIEWER_PROBE_HANDOFF_r0001_20261120_KST.md)은 당시 진단 요청 이력으로 보존. [Viewer UI 인계 r0002](L1_WORKSPACE_VIEWER_UI_CHANGE_AND_MCP_VALIDATION_HANDOFF_r0002_20261120_KST.md)는 별도 작업으로 계속 유효. **이 게시만으로 MCP 설치/개발·Job 실행·지식 게시가 시작되지 않음.**

---

## Recovery 분석 설계 보완 + Workspace 연결 — 최신 추가 인계 r0002 (2026-11-20)

- **[업무 GPT 최종 HO: 차용 판단·원인 규칙·추적/판정 근거·평가 계획·저장/조회 계약](L1_RECOVERY_WORKSPACE_IMPLEMENTED_CONTRACT_HANDOFF_r0002_20261120_KST.md)** — 기존 11/19 기준 분석 r0002를 유지하며 사용자가 제공한 확장 설계 요청에서 필요한 네 항목만 보완. CodeQL 설치 없이 기존 분석 재사용, 후보별 순차 대조·반대 근거·근거 부족 보류, **CNF 미수신 timeout 및 이미 구현된 해당 recovery 제외** 유지.
- 이번 업무 요청은 **스터디·설계/현장 계약 매핑**. 관리 스킬 Kernel 0.7.46·Workflow 1.6.75는 별도 지시로 개발한 저장·조회 후보이며 분석 정확도/제품 효과의 검증 결과가 아님. **이번에는 MD만 전달**, 후보 ZIP 공개·설치·코드 수정·Job·유료 리뷰를 포함하지 않음.
- MCP 설치본 자료를 사용자에게 다시 요구하지 않으며, 업무 GPT가 접근 가능한 기존 원문으로 설계를 이어감. 원문·로그·상세 MSC·요약의 외부 회신을 완료 조건으로 요구하지 않음.

---

## Agent/MCP 상태 확인 확장 + Viewer UI 변경 인계 (2026-11-20 최신)

- **[MCP 읽기 전용 진단 확장 요청서](L1_MCP_AGENT_READONLY_CAPABILITY_AND_VIEWER_PROBE_HANDOFF_r0001_20261120_KST.md)** — 실제 대상 호스트·설치/로드·Viewer API·기존 문서/MSC·현재성·권한을 한 번에 조회하고 모바일 Agent가 짧은 판정을 전달하도록 기존 기능 재사용/최소 확장. MCP 실제 구현·설치·활성은 아직 NOT_RUN.
- **[Viewer UI 변경·연동 인계 r0002](L1_WORKSPACE_VIEWER_UI_CHANGE_AND_MCP_VALIDATION_HANDOFF_r0002_20261120_KST.md)** — P1 두 건·사용성 개선, 실제 연동 전 I-01~I-07, B1~B3/E3~E4·복구·업무 GPT 복사 지시문. 기존 v0.1.0 UX 독립 리뷰는 이후 ACCEPT_WITH_CHANGE로 완료; 아래 과거 NOT_RUN 표기는 당시 기록.
- **[개선 HTML 시안](L1_Workspace_Wiki_Usability_Preview_20261120_KST.html)** / [기존 구현 ZIP](../l1-workspace-wiki-ui_v0_1_0_1119.zip) — 개선 시안은 별도 합성 자료이며 ZIP에 미포함. PUBLIC 자료 전달과 실제 업무 서비스 설치/동작 검증을 구분.

---

## PEC·ACE 두 스킬 최종 ZIP 실제 배포 완료 (2026-11-19)

- **[최신 업무 GPT 인계 §15](L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md)** — `code-analyzer v0.15.4` PEC-HOP [최종 ZIP](../code-analyzer_v0_15_4_1119.zip) · `l1-fix-workflow v1.6.74` ACE [최종 ZIP](../l1-fix-workflow_v1_6_74_1119.zip). **L1Work/main 실제 배송·원격 SHA256 PASS**, 자체 패키지 12+10 PASS; 독립 코드 리뷰는 **사용자 명시 생략**으로 PASS 아님. 업무 Linux 설치/활성·효용 시험은 업무 환경 자체 책임, 외부 전송 요구 없음. 아래 “최종 ZIP 미게시”는 당시에만 유효한 과거 기록.

## PEC-HOP·ACE 상위 2개 스킬만 수정 — 22건 실패 없는 개발 CI (2026-11-19)

- **[업무 GPT 2스킬 수정 결과·최종 배송 상태 — 기존 인계서 §14](L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md)**: `code-analyzer v0.15.4` PEC-HOP (12 PASS), `l1-fix-workflow v1.6.74` ACE (10 PASS) 개발 ZIP 생성·source 보존/CRC/2회 빌드 동일. ACON 제외. 이 ZIP들은 PRIVATE CI artifact의 `development_not_for_deployment`이며 **L1Work/main 루트 최종 ZIP은 아직 미게시**. Windows 신규 코드 독립 리뷰/배포 게이트 충족 후만 공개·설치 가능; 현장 결과는 외부 반출 없음.

## PEC-HOP 우선·ACE 최소 적용: 반출 없는 현장 평가 (2026-11-19)

- **[최신 범위 및 현장 평가 §13](L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md)** — **PEC-HOP P1 / ACE P2만 최소 적용·ACON 보류**. 업무 Linux 설치·코드/Evidence·시험 결과는 업무 환경 내부에서 보존하며 **반출 승인 없는 “비민감 결과 회신”도 요구하지 않음**. 현장 자체 G0→대표 사례 1건 기존/개선 비교→확대 판단. 현재 최종 ZIP 배송·현장 시험은 완료 아님.

## 수정 CL 기반 미커버 유사 결함 탐색·검사·Recovery 판단 — 기준 분석 r0002 (2026-11-19)

- **[이전 recovery 상황·배경 논리·Seed 패턴·현재 보호 커버·조치 선별을 포함한 업무 GPT 인계 r0002](L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0002_20261119_KST.md)** — 기존 11-17 분석 프롬프트와 11-19 r0001 설계·진행 기록을 조회한 뒤 개정. 수정 CL을 Seed로 원인 구조·Fix 효과를 배우고 현재 관련 경로의 미커버 유사 문제를 탐색. Seed가 이미 수정됐어도 다른 후보 탐색을 계속하며, 정적 유사 결함 발견·런타임 검출·안전한 복귀를 각각 판단.
- 호출자/callee/wrapper/상위 보호·정상 반례·빌드/수명 차이를 대조하고, 직접 Fix 누락·미커버 변형·이미 보호됨·전제 불성립·보류·미분석을 구분. V0~V6 절차, 필수 근거 9항목, 저사양 순차 탐색·범위 보고, 규칙/연결 시험 16항목과 제품 효과 검증 계획 포함. **CNF 미수신 timeout 제외 유지.** 기존 문서는 보존하며 목적·탐색 판정은 r0002 우선. 이 문서 게시 자체는 업무 코드 변경·설치·Job·유료 호출 승인이 아님.

## L1 Workspace 모던 팀 위키 UI — 업무 GPT 검토·현장 연동 (2026-11-19 최신)

- **[화면 구성·가독성·스타일·시인성 검토 및 Linux Viewer 최소 연동 인계](L1_WORKSPACE_WIKI_UI_BUSINESS_GPT_REVIEW_AND_INTEGRATION_HANDOFF_r0001_20261119_KST.md)** — 사용자 요청에 따라 Claude 토큰 만료 보고 후 업무 GPT로 전달. 이번 구현물의 독립 시각·코드 리뷰는 NOT_RUN. 과거 리뷰 대기보다 이 최신 전달 지시 우선.
- **[UI 코드·설계·시험·캡처·INTEGRATION 전체 ZIP](../l1-workspace-wiki-ui_v0_1_0_1119.zip)** / [단일 HTML](L1_Workspace_Wiki_UI_v0_1_0_20261119_KST.html). 합성 UI v0.1.0, 브라우저 자체시험 56/56·정적 19/19·CRC/해시 PASS. **개발·검토용 전달물이며 정식 설치 배포 아님**, 실제 API·B1~B3·E3/E4 미검증.

## 이전 Recovery 포인트 상세 설계 r0001 — 보존 (2026-11-19)

- **[필수 근거 9항목·단계별 입출력·후보 판정·최소 구현·검증을 포함한 상세 인계 r0001](L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0001_20261119_KST.md)** — CL→Jira/merged PR의 Problem/Cause/Solution과 실제 source revision을 대조하고, 정상/실패 시나리오·최초 불일치·검출부·런타임 자원 소유자의 복구 경계를 구분. 기존 스킬 재사용, G01~G10 기능 대조, S0~S6 분석 계약, E0~E5 적용·최소 구현·회수, T01~T20 연결 시험과 R01~R08 제품 효과 검증 계획 포함.
- **CNF 미수신 timeout·기존 recovery 커버 범위 제외**, 저사양 모델 순차 처리·기존 Work/Evidence 보존·미확인 API/스키마 가정 금지 유지. 분석 흐름 구현과 실제 제품 recovery 코드 변경을 구분. 업무 GPT의 현장 대조·구현에 사용할 설계 인계이며, 게시 자체는 호스트 실행·제품 코드 변경·설치·운영 전환 승인이 아님. 기존 [사례 분석 프롬프트](L1_CL_JIRA_RECOVERY_ANALYSIS_PROMPT_r0001_20261117_KST.md) 보존.

## ACE·PEC-HOP·ACON — Workflow v1.6.73 개발 ZIP CI 검증 결과 (2026-11-19)

- **[ACE·PEC-HOP·ACON Workflow 통합 개발 ZIP 실제 CI 20 PASS / 최종 ZIP은 릴리스 게이트 미충족 — 기존 인계서 최신 12절](L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md)** — PRIVATE Actions에서 기존 MSC 계보를 보존한 `l1-fix-workflow v1.6.73` 개발 ZIP 실제 빌드·전파일 해시/CRC·재현성 PASS. 미완료 코드 독립 리뷰/실호스트 G0·Writer 권한을 건너뛴 자동 배포 금지; 배포 승인된 최종 ZIP만 L1Work 루트에 게시 가능. 업무 전용 Updater 원본 반출 없이 업무 GPT의 비민감 기능 판정 회수.

## ACE·PEC-HOP·ACON 신규 코드 후보·최종 ZIP 배포 게이트 (2026-11-19)

- **[ACE·PEC-HOP·ACON 실제 적용 현황: 비민감 순수 후보 19건 PASS / 최종 스킬 ZIP 배포 차단 — 기존 인계서 최신 11절](L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md)** — PRIVATE 구현 후보·정적 근거는 원래 CoWork Work에 보존. `development_not_for_deployment`/실설치 소스 미확인·Writer 보호/전체 회귀·코드 독립 리뷰 미충족으로 `PUBLIC_SKILL_ZIP=BLOCKED_NOT_POSTED`. 업무 GPT가 필요한 설치 기능의 비민감 델타만 READ_ONLY 회신, Gate 완료 후 신규 ZIP만 L1Work/main 루트로 전달. 문서 게시 자체는 설치나 Job 실행이 아님.

## L1 Workspace 최신 책임 변경·가독성 개선 논의 (2026-11-18)

- **[개인 Knowledge 관리 및 그룹 Knowledge 연계: 업무 GPT 현장 설계 / Knowledge Updater 전담, 웹 뷰어 UX 문제 OPEN — 최신 15절](L1_WORKSPACE_LOCAL_VIEWER_R0002_BUSINESS_GPT_DETAILED_REVIEW_AND_G0_HANDOFF_r0001_20261118_KST.md#15-최신-사용자-결정--knowledge-updater-전담업무-gpt-현장-설계-및-viewer-ux-별도-논의-2026-11-18)**. 기존 13·14절 유지. 메타정보·실제 스킬/G0는 업무 GPT가 조사, UI 화면 변경은 사용자 논의 후. 인계 문서 게시만 수행; Linux 운영·Knowledge WRITE 미실행.

## L1 Workspace r0002 업무 GPT 직접 상세 검토 인계 (2026-11-18)

- **[전체 Workspace 트리·형식별 렌더링·보안/기존 스킬/G0 A~S/수락시험 T01~T34 상세 검토·작업 지시서](L1_WORKSPACE_LOCAL_VIEWER_R0002_BUSINESS_GPT_DETAILED_REVIEW_AND_G0_HANDOFF_r0001_20261118_KST.md)** — **최신 사용자 결정: Claude 독립 리뷰 생략, 업무 GPT 직접 검토.** 기존 r0002 설계의 요구·리스크·근거·19개 현장 질문과 단계별 Gate를 단독 검토 가능한 수준으로 수록. **13절 추가: 개인 Linux PC의 실제 웹 서비스 구축을 위한 업무 GPT→업무 LLM/Agent E0~E5 단계별 구현·시험·승인·롤백 지시문 포함.** **14절 추가: 사용자·업무 GPT의 개인 Knowledge 축적/탐색 TO-BE 합의(D-1~D-4, Module→Feature→Scenario, Work/Evidence/Revision/Coverage, 그룹 포맷 변환/승인 게시, Workflow knowledge/ WRITE 차단) 및 PK-G01~G08 인계.** `INDEPENDENT_REVIEW=NOT_RUN`, Linux G0·서비스/원본 전환·그룹 Knowledge 게시 `NOT_RUN`. 지금은 허용된 읽기 전용 G0·설계 검토에 한정; Linux 운영 변경은 별도 승인.

## L1 Workspace 웹 뷰어 안전 중지 인계 (2026-11-18)

- **[Linux Workspace 전체 URL 뷰어 — 중지 시점·재개 조건 인계](L1_WORKSPACE_LOCAL_VIEWER_SAFE_STOP_HANDOFF_r0001_20261118_KST.md)** — 전체 업무 폴더 열람 및 Markdown 즉시 렌더 설계 r0002, Claude 리뷰 입력·$1.50 단일 승인·미등록 REQUEST/READY, 운영 설정 미변경, 안전 중지 상태와 추후 재개 경계를 정리. **읽기 전용 상태 공유이며 실행 트리거가 아님.**

## L1 Workspace Linux 로컬 웹 뷰어 안전 전환 G0 (2026-11-18)

- **[로컬 Workspace·웹 열람 전환 G0 읽기 전용 16항목 인계](L1_WORKSPACE_LOCAL_WEB_VIEWER_LINUX_G0_READONLY_HANDOFF_r0001_20261118_KST.md)** — Kernel·Workflow 실제 원격 의존성, 로컬 백업·기존 웹/인증·공유 ACL·그룹 Knowledge writer 확인. A~P 숫자 회신. 신규 설치·Git 변경·웹 공유·Knowledge 쓰기·Job/모델 호출 없이 읽기 전용 상태 검토.

## MSC 두 진입 writer G0 읽기 전용 확인 (2026-11-18)

- **[MSC 두 진입 Updater·Kernel writer G0 숫자 확인 인계 r0001](L1_MSC_DUAL_ENTRY_WRITER_G0_READONLY_HANDOFF_r0001_20261118_KST.md)** — 업무 GPT/허용된 Linux Agent에서 기존 설치본·writer/HTML published_path·수동 편집 보호 계약을 **READ_ONLY**로 확인. 회신은 A~J 10개 숫자. 현재 개발 ZIP은 최종 PUBLIC 배포 게이트 미충족으로 게시하지 않음. 스킬 설치·Job 실행·지식 쓰기 승인 아님.

## ACE·PEC-HOP·ACON: 업무 스킬 실제 사용·모바일 수정 요청 협업 (2026-11-19)

- **[실사용 패키지·업무 전용 Updater 원본 비반출·모바일 오류 수정 요청의 책임/회신 경계 — 기존 인계서 최신 10절](L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md#10-2026-11-19-kst--실제-업무-사용업무-전용-updater모바일-수정-요청-협업-경계)** — 사용자 확인: 스킬 패키지는 업무 환경에 전달되어 실제 사용 중. Updater 원본 코드는 GitHub 제공 불필요, 업무 GPT의 비민감 기능/실행 판정만 회수. 문제가 생기면 모바일 Agent로 기존 Work에 수정 요청 → 소유 스킬별 개발·시험·유효 승인/배포 Gate → 실제 업무 적용 확인. 설치 활성 버전과 HOST E2E는 별도 증빙, 문서 게시 자체는 실행·설치 트리거 아님.

## ACE·PEC-HOP·ACON 지식 Updater 설계 적용 제안 (2026-11-18)

- **[업무 GPT 검토용 설계 적용 제안서 r0001 + 실제 Linux 설치본 READ_ONLY G0 원샷(9절)](L1_KNOWLEDGE_UPDATER_ACE_PEC_HOP_ACON_DESIGN_APPLICATION_PROPOSAL_r0001_20261118_KST.md#9-2026-11-18-kst--acepec-hopsafe-실제-linux-설치본-g0-읽기-전용-원샷)** — ACE 최신 Work 결정·PEC-HOP Evidence 원문 바이트·SAFE 무변경을 **실제 설치본에서 읽기 전용**으로 확인하기 위한 AST/SHA-256 점검 스니펫·synthetic fixture 경계·단일 비민감 결과 양식 포함. 업무 GPT/허용된 Linux Agent가 실행하는 절차이며 현재 **호스트 미실행**. 스킬 수정·설치·Knowledge 게시·Job·유료 호출 승인 아님. 기존 11-17 Knowledge 동기화 R1 리뷰와 구분.

## CL·Jira 기반 이슈 시나리오·복구 지점 분석 (2026-11-17)

- **[CL·Jira 복구 지점 분석 프롬프트 r0001](L1_CL_JIRA_RECOVERY_ANALYSIS_PROMPT_r0001_20261117_KST.md)** — CL 번호 1개로 시작해 description의 Jira 연결, Problem/Cause/Solution·코멘트·diff/revision 대조, 정상/실패 시나리오와 검출 지점·소유자 복구 경로를 분석하는 업무 LLM 전달용 문서. p4-code-owner·l1-github·code-analyzer, 로그가 있을 때 issue-analyzer와 기존 Workflow/Kernel·doc-converter를 재사용.
- **REQ→CNF 미수신 timeout은 기존 recovery 구현 범위로 제외.** 저사양 모델은 이슈·실패 절차별 순차 처리. 업무 소스는 읽기 전용이며 코드 변경·설치·실제 HW/오류 주입 시험·Job·그룹 지식 게시는 포함하지 않음. 입력란을 채워 문서 전체를 업무 GPT 또는 허용된 실행 LLM·로컬 Agent에 전달.

## L1 Knowledge Updater — Claude R1 완료, 업무 GPT 상세 G0 인계 (2026-11-17)

- **[Knowledge Updater R1 판정 반영·개인/그룹 동기화 상세 인계 r0002](L1_KNOWLEDGE_UPDATER_R1_G0_DETAILED_HANDOFF_r0002_20261117_KST.md)** — 사용자 확정 ①~④, Claude R1 독립 설계 리뷰 `ACCEPT_WITH_CHANGE`(BLOCKING 1/MAJOR 4/MINOR 2)와 GPT 보완, G01~G16 실제 설치본 READ_ONLY 검증 질문, Base/Ours/Theirs·CAS·부분실패 복구, T01~T10 후속 수락 기준. 설계 정적 검토 완료, 코드/호스트/Knowledge 쓰기는 미실행. **기존 11-16 인계의 미수신 표기보다 최신**.


## 관리 스킬 기능 요약 (공개용 · 업무용 GPT 인계)

| 문서 | 용도 | 검증 범위 |
|---|---|---|
| [L1_SKILL_CAPABILITY_SUMMARY_INHOUSE_HANDOFF_r0001_20261113.md](L1_SKILL_CAPABILITY_SUMMARY_INHOUSE_HANDOFF_r0001_20261113.md) | 관리 스킬 **18개 + 별도 업무용 연동 1개**의 역할·재사용 판단·현재 코드 MSC 활용 요약 | 기존 정적 카탈로그를 비민감 범위에서 요약. 작업 PC 설치·실호출·독립 리뷰 미검증 |

상세 기능 카탈로그와 검증 결과의 정본은 접근 권한이 필요한 CoWork PRIVATE에 있으며, 이 공개 인계에는 회사 코드·운영자료·인증정보를 포함하지 않는다. 스킬 설치·Job 실행·공개 배포를 승인하는 문서가 아니다.

## MSC 링크 5종 스킬 G0 확인 (2026-11-16)

- **[L1 MSC 링크 5종 스킬 G0 읽기 전용 검토 인계 (2026-11-16)](L1_MSC_LINK_SKILL_G0_REVIEW_HANDOFF_r0001_20261116_KST.md)** — 공개 4종 재사용/수정 후보와 실제 설치된 Knowledge Updater·그룹 writer·호스팅의 I/O 차이 확인 Q1~Q8. 문서 게시가 업무 검토 실행이나 스킬 수정·배포 완료를 의미하지 않음.

## MSC B 뷰어 — 생성·축적·게시·열람 컨셉 리뷰

| 상태 | 문서 | 범위 |
|---|---|---|
| **설계 리뷰 인계 r0001** | [L1_KNOWLEDGE_MSC_B_VIEWER_GPT_REVIEW_HANDOFF_r0001_20261114_KST.md](L1_KNOWLEDGE_MSC_B_VIEWER_GPT_REVIEW_HANDOFF_r0001_20261114_KST.md) | doc-converter의 HTML+SVG 생성, Workflow/Kernel/Updater 연결, 사람의 보기 URL과 AI의 원문 재사용. 모듈·Feature 목록 검토는 1단계 유지 |

공개 가상 샘플을 참고한 컨셉 리뷰 입력. 실제 스킬 변경·코드 분석·Job 실행·지식 게시·호스팅 변경을 요청하지 않는다. B 자동 생성·연결과 첫 실제 분석 E2E는 아직 미검증이며 후속 확인으로 구분한다.

## CL/PR 이슈 분석 → Workspace 축적 — 구현·회귀시험

| 상태 | 문서 | 범위 |
|---|---|---|
| **기존 구현 원샷 지침 (보존)** | [L1_CLPR_ISSUE_ANALYSIS_IMPLEMENTATION_AND_REGRESSION_ONESHOT_r0001_20261114.md](L1_CLPR_ISSUE_ANALYSIS_IMPLEMENTATION_AND_REGRESSION_ONESHOT_r0001_20261114.md) | 기존 스킬 5종 최소 수정·회귀·ZIP 배포 게이트 요구사항 |
| **2026-11-14 실제 수정 후보 5종, 최종 배포 차단** | [L1_CLPR_IMPLEMENTATION_STATUS_r0001_20261114.md](L1_CLPR_IMPLEMENTATION_STATUS_r0001_20261114.md) | PRIVATE 후보 ZIP 5종 원격 SHA/CRC PASS. Python 회귀/E3 NOT_RUN, PUBLIC 루트 최종 ZIP 미게시 |

이 문서는 기존 스킬을 재사용해 분석·축적하는 **실행 인계**이며, 수정된 스킬 ZIP 또는 실제 회귀시험 완료 결과가 아니다. 추가 독립 리뷰 요청은 포함하지 않으며, 코드 변경·시험·PUBLIC 루트 스킬 ZIP 게시에는 각각 실증된 안전·호환·릴리스 게이트가 적용된다.

## L1 Knowledge Updater × Workflow

| 상태 | 문서 | 범위 |
|---|---|---|
| **업무 GPT G0 검토 요청 (2026-11-16)** | [L1_WORKSPACE_KNOWLEDGE_34_BUSINESS_GPT_REVIEW_REQUEST_r0001_20261116_KST.md](L1_WORKSPACE_KNOWLEDGE_34_BUSINESS_GPT_REVIEW_REQUEST_r0001_20261116_KST.md) | ③·④: Knowledge 폴더 Updater 단독 WRITE / Workflow READ_ONLY, Work 이력, 그룹 게시·readback·역링크. **2,702자, 읽기 전용 G0 확인·TO-BE 제안**, 구현/운영 쓰기 지시 아님 |
| **최신 ③·④ 설계 검토 인계 (2026-11-16)** | [L1_WORKSPACE_KNOWLEDGE_FOLDER_UPDATER_HANDOFF_r0001_20261116_KST.md](L1_WORKSPACE_KNOWLEDGE_FOLDER_UPDATER_HANDOFF_r0001_20261116_KST.md) | `works/` 원본 유지 · 물리적 `knowledge/` 탐색 제안 · Updater만 WRITE / Workflow READ_ONLY · 공통 Evidence 인계 · 승인된 그룹 게시·역링크. 독립 설계 리뷰 미수신, 실제 설치·E2E 미검증. **READ_ONLY G0 점검용** |
| **현재 인계 r0005** | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md) | G0 설치 사실 / G1 가정 분리, K5.8 설계표만, 기존 기능 우선 재사용 |
| 이전 r0004 | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0004_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0004_1111.md) | 이전 보완 계약, 과거 기록 보존 |
| 과거 r0002 | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0002_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0002_1111.md) | 이전 통합 인계, 과거 기록 보존 |

저장소 `wonhwipark/L1Work`, branch `main`. 현재 인계는 G0 READ_ONLY와 G1 설계표 작성이며 기존 knowledge/metadata·Work/Evidence·record/schema를 변경하지 않는다. SourceSnapshot·CAS·N:M·복구는 기존 Kernel/Updater/Git 제공자를 우선 재사용하고 미확인 API/record는 추가 확인 또는 BLOCKED로 남긴다.

r0005의 G0 전체 미수행 표기는 작성 당시 상태로 보존한다. 2026-11-14에는 일부 기존 기능의 호스트 확인 보고를 확보한 상태이며, 원본 설치/API·독립 리뷰·통합 전체 PASS를 뜻하지 않는다. 실제 저장·MSC/source/Evidence·게시/역링크·AI 본문 활용은 첫 승인된 분석 후속으로 확인한다. 신규 엔진·schema 확장은 확인된 gap의 최소 후보로만 검토하며, 이 목록은 구현·그룹 write·설치·모델 호출·외부 전송을 승인하지 않는다. 파일을 내려받아 업무용 GPT에 첨부해 해당 문서의 리뷰 요청을 사용한다.

## 용어·접근 지침

신규 안내에서는 저장소·작업 PC·실행 호스트·접근 권한으로 대상을 지칭한다. 기존 파일명(예: `_INHOUSE_` 포함)은 링크 호환성을 위해 유지한다. 이 인계 목록은 공개 허용 설명만 포함하며 PRIVATE 기록, 회사 코드, 제한 정보의 공개를 승인하지 않는다.
