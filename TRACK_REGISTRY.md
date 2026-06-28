# Track Registry

| 트랙 번호 | 폴더 | 원천 prompt / 참조 | 현재 상태 | 비고 |
|---|---|---|---|---|
| 5.0 | `5.0_common_framework/` | `prompt/5_0_common_automation_framework.md` | draft | 공통 프레임워크 |
| 5.1 | `5.1_jira_feedback_loop/` | `prompt/5_1_jira_feedback_loop_py_package_prompt.md` | draft | Jira 피드백 루프 |
| 5.2 | `5.2_code_analyzer/` | `prompt/5_2_code_analyzer_py_package_prompt.md`<br>`prompt/5_2_code_analyzer_track_a_prompt.md`<br>`prompt/5_2_code_analyzer_track_b_prompt.md`<br>`CodeAnalyzer_standalone/README.md` | staging-source-ready | legacy source 포함 |
| 5.3 | `5.3_confluence_collection/` | `prompt/5_3_pre_confluence_child_page_collection_prompt.md`<br>`prompt/5_3_weekly_report_collection_py_package_prompt.md` | draft | Confluence 수집 |
| 5.4 | `5.4_hld_code_consistency/` | `prompt/5_4_hld_code_consistency_check_py_package_prompt.md` | draft | 일관성 점검 |
| 5.5 | `5.5_rca_kg/` | `prompt/5_5_rca_knowledge_graph_py_package_prompt.md`<br>`RCA_standalone/README.md`<br>`rca_kg/indexes/index.md` | staging-source-ready | KG refs 포함 |
| 5.6 | `5.6_onboarding_knowledge_pack/` | `prompt/5_6_onboarding_knowledge_pack_py_package_prompt.md` | draft | 온보딩 지식팩 |

## 관리 규칙
- 신규 원천이 추가되면 해당 트랙의 `source_refs.md`와 이 문서를 함께 갱신합니다.
- L1Work 이전/상세화 목적의 prompt는 각 트랙의 `prompt/` 아래에 원본 파일명 그대로 복제/정렬본으로 보관할 수 있습니다.
- 원본 `prompt/`, `CodeAnalyzer_standalone/`, `RCA_standalone/` 파일은 삭제/이동/수정하지 않습니다.
- 상태값은 `WORKBOARD.md`와 일치해야 합니다.

## 2026-06-28 KST prompt 정렬 상태
| 트랙 | L1Work prompt 상태 | 비고 |
|---|---|---|
| 5.0 | 채움 완료 | 루트 5.0 prompt 복사 |
| 5.1 | 채움 완료 | 기존 L1Work 복제본 확인, 루트 원천 `prompt/5_1_jira_feedback_loop_py_package_prompt.md`는 현재 작업공간에 없음 |
| 5.2 | 채움 완료 | standalone prompt 및 루트 5.2 prompt 3종 포함 |
| 5.3 | 채움 완료 | 루트 5.3 prompt 2종 포함 |
| 5.4 | 채움 완료 | 루트 5.4 prompt 포함 |
| 5.5 | 채움 완료 | standalone prompt/deepdive 및 루트 5.5 prompt 2종 포함 |
| 5.6 | 채움 완료 | 루트 5.6 prompt 포함 |

<!-- master-distribution-20260629:start -->
## 2026-06-29 KST master 분배 상태
| 트랙 | master 발췌본 | 상태 | 경계 검토 |
|---|---|---|---|
| 5.0 | `5.0_common_framework/master/master_v0.40_section_5.0.md` | 분배 완료 | 명확함 |
| 5.1 | `5.1_jira_feedback_loop/master/master_v0.40_section_5.1.md` | 분배 완료 | 명확함 |
| 5.2 | `5.2_code_analyzer/master/master_v0.40_section_5.2.md` | 분배 완료 | 명확함; 기존 `reference/master_v0.40_section_5_2.md` 및 standalone 참조 기록 |
| 5.3 | `5.3_confluence_collection/master/master_v0.40_section_5.3.md` | 분배 완료 | 명확함; 5.3-pre와 5.3 Weekly Report를 함께 포함 |
| 5.4 | `5.4_hld_code_consistency/master/master_v0.40_section_5.4.md` | 분배 완료 | 명확함 |
| 5.5 | `5.5_rca_kg/master/master_v0.40_section_5.5.md` | 분배 완료 | 명확함; 기존 RCA 보조 참조 기록 |
| 5.6 | `5.6_onboarding_knowledge_pack/master/master_v0.40_section_5.6.md` | 분배 완료 | 명확함 |
<!-- master-distribution-20260629:end -->
