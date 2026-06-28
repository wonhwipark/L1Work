# RCA Knowledge Graph — Case Index

> **자동 전용 (_tool_generate).** 이 표는 P4/P5가 case 등록·검토 시 갱신한다.
> 사람이 직접 행을 편집하지 않는다(승인은 P5에서, 표 갱신은 도구가 수행).
> v2-A 기준으로 fingerprint 검색과 active issue_type만 사용한다.
> crash/dump 분석은 L1SW Log Analyzer 전담이므로 이 index의 active issue_type 통계에서 제외한다.

---

## 사용법

새 케이스 분석 완료 시 아래 표에 한 줄 추가한다.

```text
| case_id | issue_type | signature_set | sequence | occurrence_count | first_seen | last_seen | status |
```

유사 케이스 검색 시 `issue_type`으로 1차 필터링한 뒤,
`signature_set + sequence` fingerprint가 일치하는지 확인한다.

- fingerprint 일치: 신규 case를 만들지 않고 기존 case의 `occurrence_count++`, `recent_occurrences` 추가
- fingerprint 불일치: 신규 `case_id`를 부여하고 `cases/`에 YAML 생성
- 담당영역 밖 이관: `cases/unresolved/`에 PENDING 파일 생성

---

## Case 목록

| case_id | issue_type | signature_set | sequence | occurrence_count | first_seen | last_seen | status |
|---------|------------|---------------|----------|------------------|------------|-----------|--------|
| EXAMPLE_v2_rach_failure_001 | rach_failure | RACH_MSG1, RACH_MSG2, RACH_MSG3, RACH_PHY_TIMER_EXPIRY | RACH_MSG1→RACH_MSG2→RACH_MSG3→(RACH_PHY_TIMER_EXPIRY) | 7 | 2026-05-30 | 2026-06-21 | confirmed |

---

## 통계 요약 (수동 업데이트)

| issue_type | 실제 case | 예시 case | 합계 |
|------------|----------:|----------:|-----:|
| rach_failure | 0 | 1 | 1 |
| scg_failure | 0 | 0 | 0 |
| tx_abnormal | 0 | 0 | 0 |
| l2_max_retransmission | 0 | 0 | 0 |
| **합계** | **0** | **1** | **1** |

> 실제 case = 실로그 분석으로 생성된 case. 예시 case = EXAMPLE_* (구조 참고용, 통계 분리).

---

## Deprecated / External

| 항목 | 처리 |
|------|------|
| crash | 5.5 RCA KG 신규 case 생성 대상 아님. L1SW Log Analyzer 산출물을 경로로만 참조 |

---

## 디렉토리 구조

```text
rca_kg/
  ├─ cases/           ← 분석 1건당 YAML 1개. 단, 동일 fingerprint 재발은 기존 case 갱신
  │   └─ unresolved/  ← 담당영역 밖 이관 PENDING 파일
  ├─ signals_tool_generate/         ← L1SW 출력 또는 issue_type signal 파일
  ├─ skills_seed/     ← 문제 유형별 분석 가이드. crash_analyzer.md 는 deprecated
  ├─ indexes_tool_generate/
  │    └─ index.md    ← 이 파일
  └─ schema/
       ├─ rca_case.schema.yaml   ← 필드 정의
       └─ taxonomy.yaml          ← active issue_type / root_cause / confidence 기준
```
