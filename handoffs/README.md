# 업무용 GPT 인계 문서

## 관리 스킬 기능 요약 (공개용 · 업무용 GPT 인계)

| 문서 | 용도 | 검증 범위 |
|---|---|---|
| [L1_SKILL_CAPABILITY_SUMMARY_INHOUSE_HANDOFF_r0001_20261113.md](L1_SKILL_CAPABILITY_SUMMARY_INHOUSE_HANDOFF_r0001_20261113.md) | 관리 스킬 **18개 + 별도 업무용 연동 1개**의 역할·재사용 판단·현재 코드 MSC 활용 요약 | 기존 정적 카탈로그를 비민감 범위에서 요약. 작업 PC 설치·실호출·독립 리뷰 미검증 |

상세 기능 카탈로그와 검증 결과의 정본은 접근 권한이 필요한 CoWork PRIVATE에 있으며, 이 공개 인계에는 회사 코드·운영자료·인증정보를 포함하지 않는다. 스킬 설치·Job 실행·공개 배포를 승인하는 문서가 아니다.

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
| **현재 인계 r0005** | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md) | G0 설치 사실 / G1 가정 분리, K5.8 설계표만, 기존 기능 우선 재사용 |
| 이전 r0004 | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0004_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0004_1111.md) | 이전 보완 계약, 과거 기록 보존 |
| 과거 r0002 | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0002_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0002_1111.md) | 이전 통합 인계, 과거 기록 보존 |

저장소 `wonhwipark/L1Work`, branch `main`. 현재 인계는 G0 READ_ONLY와 G1 설계표 작성이며 기존 knowledge/metadata·Work/Evidence·record/schema를 변경하지 않는다. SourceSnapshot·CAS·N:M·복구는 기존 Kernel/Updater/Git 제공자를 우선 재사용하고 미확인 API/record는 추가 확인 또는 BLOCKED로 남긴다.

r0005의 G0 전체 미수행 표기는 작성 당시 상태로 보존한다. 2026-11-14에는 일부 기존 기능의 호스트 확인 보고를 확보한 상태이며, 원본 설치/API·독립 리뷰·통합 전체 PASS를 뜻하지 않는다. 실제 저장·MSC/source/Evidence·게시/역링크·AI 본문 활용은 첫 승인된 분석 후속으로 확인한다. 신규 엔진·schema 확장은 확인된 gap의 최소 후보로만 검토하며, 이 목록은 구현·그룹 write·설치·모델 호출·외부 전송을 승인하지 않는다. 파일을 내려받아 업무용 GPT에 첨부해 해당 문서의 리뷰 요청을 사용한다.

## 용어·접근 지침

신규 안내에서는 저장소·작업 PC·실행 호스트·접근 권한으로 대상을 지칭한다. 기존 파일명(예: `_INHOUSE_` 포함)은 링크 호환성을 위해 유지한다. 이 인계 목록은 공개 허용 설명만 포함하며 PRIVATE 기록, 회사 코드, 제한 정보의 공개를 승인하지 않는다.
