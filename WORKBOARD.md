# L1Work Workboard

## 트랙 상태표
| 트랙 | 폴더 | 이름 | 현재 상태 | 비고 |
|---|---|---|---|---|
| 5.0 | `5.0_common_framework/` | 공통 자동화 프레임워크 | draft | 공통 구조와 운영 규칙 기준 |
| 5.1 | `5.1_jira_feedback_loop/` | Jira 피드백 루프 | draft | Jira 기반 피드백 자동화 |
| 5.2 | `5.2_code_analyzer/` | Code Analyzer | staging-source-ready | standalone 산출물 존재 |
| 5.3 | `5.3_confluence_collection/` | Confluence 수집 | draft | child page 및 weekly report 수집 |
| 5.4 | `5.4_hld_code_consistency/` | HLD-Code 일관성 점검 | draft | HLD와 코드 일관성 점검 |
| 5.5 | `5.5_rca_kg/` | RCA Knowledge Graph | staging-source-ready | standalone 및 KG 참조 존재 |
| 5.6 | `5.6_onboarding_knowledge_pack/` | Onboarding Knowledge Pack | draft | 온보딩 지식팩 |

## 상태 정의
- `draft`: 원천 확인 및 상세 요구사항 정리 단계입니다.
- `staging-source-ready`: 기존 원천과 산출물을 staging 후보로 정리할 수 있는 단계입니다.
- `staging`: release 후보를 `release/staging/`에 구성한 단계입니다.
- `current`: 검증 완료 후 현재 기준본으로 승격된 단계입니다.
- `archive`: 이전 기준본 또는 폐기된 후보를 보관하는 단계입니다.

## 2026-06-28 KST 작업 메모
- 5.x 트랙의 `prompt/` 폴더를 점검하고, L1Work 이전 목적의 복제/정렬본을 채웠습니다.
- 5.2와 5.5는 standalone prompt와 루트 prompt를 함께 보존하는 방식으로 정리했습니다.
- 5.2와 5.5에 누락된 표준 구조를 보완했습니다.

<!-- master-distribution-20260629:start -->
## 2026-06-29 KST 작업 메모 - master 분배
- 모든 5.x 트랙에 `master/` 폴더와 `master_v0.40_section_5.x.md` 발췌본을 생성했습니다.
- 기준 원본 `master/L1_AI_Automation_Roadmap_v0.40.md`는 수정하지 않았습니다.
- 5.3 트랙은 master 상의 `5.3-pre`와 `5.3 Weekly Report Collection`을 단일 5.3 트랙 발췌본에 함께 포함했습니다.
<!-- master-distribution-20260629:end -->
