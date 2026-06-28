# Release Board

## Release 단계 기준
- `draft`: 아이디어, 요구사항, 원천 분석이 진행 중인 상태입니다.
- `staging`: 검토 가능한 산출물을 `release/staging/`에 배치한 상태입니다.
- `current`: 검증과 인수인계가 완료되어 현재 기준본으로 사용할 수 있는 상태입니다.
- `archive`: 이전 current 또는 폐기 후보를 보관하는 상태입니다.

## 현재 트랙별 release 상태
| 트랙 | staging 경로 | current 경로 | 현재 상태 | 메모 |
|---|---|---|---|---|
| 5.0 | `5.0_common_framework/release/staging/` | `5.0_common_framework/release/current/` | draft | 승격 전 |
| 5.1 | `5.1_jira_feedback_loop/release/staging/` | `5.1_jira_feedback_loop/release/current/` | draft | 승격 전 |
| 5.2 | `5.2_code_analyzer/release/staging/` | `5.2_code_analyzer/release/current/` | staging-source-ready | 원천 정리 가능 |
| 5.3 | `5.3_confluence_collection/release/staging/` | `5.3_confluence_collection/release/current/` | draft | 승격 전 |
| 5.4 | `5.4_hld_code_consistency/release/staging/` | `5.4_hld_code_consistency/release/current/` | draft | 승격 전 |
| 5.5 | `5.5_rca_kg/release/staging/` | `5.5_rca_kg/release/current/` | staging-source-ready | 원천 정리 가능 |
| 5.6 | `5.6_onboarding_knowledge_pack/release/staging/` | `5.6_onboarding_knowledge_pack/release/current/` | draft | 승격 전 |

## 승격 체크
- `source_refs.md` 원천 매핑 완료
- `TRACK_STATUS.md` 차단 항목 확인
- `review_logs/decision_log.md` 주요 결정 기록
- `release/RELEASE_CHECKLIST.md` 완료 기준 충족
- `HANDOFF.md` 다음 세션 재개 정보 최신화

## 2026-06-28 KST release 준비 메모
- 모든 5.x 트랙의 `prompt/`에 최소 1개 이상의 실제 `.md` 파일이 있도록 정렬했습니다.
- 5.2와 5.5는 release 승격 전 standalone 전체 이관 범위를 별도로 확정해야 합니다.

<!-- master-distribution-20260629:start -->
## 2026-06-29 KST release 준비 메모 - master 분배
- release 승격 전 원천 매핑 기준으로 각 트랙별 master v0.40 발췌본을 `master/` 하위에 배치했습니다.
- 본 작업은 source distribution 및 문서 최소 갱신이며, release 상태값 자체는 변경하지 않았습니다.
<!-- master-distribution-20260629:end -->
