# RCA Standalone Phase 1-A 정합성 패치 — crash 제거

작성일: 2026-06-22 KST  
대상 패키지: RCA_standalone  
작업 의도: 5.5 RCA Knowledge Graph v2 기준에서 crash/dump 분석을 active issue_type에서 제거하고 L1SW Log Analyzer 전담 영역으로 분리한다.

---

## 변경 요약

1. `rca_kg/schema/taxonomy.yaml`
   - active `issue_types`에서 `crash` 제거
   - active `root_cause_categories`에서 `null_pointer_crash`, `assertion_failure` 제거
   - `api_contract_mismatch`, `unknown`의 `applies_to`에서 `crash` 제거
   - `deprecated_external_issue_types.crash` 섹션 추가

2. `rca_kg/schema/rca_case.schema.yaml`
   - `root_cause.category.values`에서 `null_pointer_crash`, `assertion_failure` 제거
   - header 변경 이력에 v2-A crash root cause active enum 제거 사항 추가

3. `rca_kg/indexes/index.md`
   - fingerprint 기준 index 구조로 최소 재설계
   - 통계 요약에서 `crash` 제거
   - `Deprecated / External` 섹션 추가

4. `rca_kg/skills_seed/crash_analyzer.md`
   - 파일을 삭제하지 않고 최상단에 deprecated banner 추가
   - 신규 5.5 case 생성에는 사용하지 않도록 명시

---

## 적용 후 기준

```text
active issue_type:
- rach_failure
- scg_failure
- tx_abnormal
- l2_max_retransmission

external/deprecated:
- crash → L1SW Log Analyzer 전담
```

---

## 남은 작업

- `scripts/README.md`는 아직 v1 잔재가 많으므로 별도 v2 동기화 필요
- `keywords.yaml` SSOT 작성 전, README/index/taxonomy/schema 기준을 최종 확인할 것
- 실 로그 1건으로 fingerprint 생성 및 occurrence_count 갱신 경로 검증 필요
