# TRACK_STATUS - 5.5 RCA Knowledge Graph

## 현재 단계
- 현재 상태: `staging-source-ready`
- release 단계: draft
- 관리 정책: `L1Work/5.5_rca_kg/` 내부 prompt는 기존 원본의 복제/정렬본으로 관리하고, 원본은 읽기 전용으로 보존합니다.

## 완료 항목
- [x] `RCA_standalone/prompt/` 하위 prompt/deepdive 복제 상태 확인
- [x] 루트 `prompt/5_5_rca_knowledge_graph_py_package_prompt.md` 복사
- [x] 루트 `prompt/5_5_rca_knowledge_graph_py_package_prompt_v1_backup.md` 복사
- [x] 표준 구조 보완: `TRACK_STATUS.md`, `HANDOFF.md`, `source_refs.md`, `CHANGELOG.md`, `review_logs/decision_log.md`, `release/RELEASE_CHECKLIST.md`, `spec/`, `contracts/`, `release/staging/`, `release/current/`

## 진행 항목
- [ ] standalone 전체 이관 범위와 KG release 승격 기준 확정

## 대기 항목
- [ ] 대규모 RCA KG/스킬/스크립트 동기화 필요 여부 검토

## 차단 항목
- 현재 등록된 차단 항목 없음

<!-- master-distribution-20260629:start -->
## Master 분배 상태 - 2026-06-29 KST
- [x] `master/` 하위 폴더 생성
- [x] `L1Work/5.5_rca_kg/master/master_v0.40_section_5.5.md` 생성
- [x] 기준 원본 `master/L1_AI_Automation_Roadmap_v0.40.md` 참조 기록
- [x] section 경계 검토: 명확함
<!-- master-distribution-20260629:end -->
