# RCA Standalone R2 — scripts/README.md v2 동기화

작성일: 2026-06-22 01:18 KST  
대상: `scripts/README.md`  
기준: `rca_kg/schema/rca_case.schema.yaml` v2, A안 crash 제거 반영본

---

## 1. 작업 목적

기존 `scripts/README.md`에는 v1 기준 운영 절차가 남아 있었다.
이 때문에 실 로그 검증 시 Claude Code 또는 Roo Code가 날짜 기반 case_id, `line_range`,
`raw_examples`, `related.jira` 등을 생성할 위험이 있었다.

이번 작업에서는 README를 schema v2 기준으로 전면 동기화했다.

---

## 2. 주요 변경 사항

1. 전체 흐름을 L1SW 1차 축소본 중심으로 재정의
   - `.sdm` → L1SW → `_l1sw.txt` → 선택적 signal → RCA YAML

2. active issue_type 명시
   - `rach_failure`
   - `scg_failure`
   - `tx_abnormal`
   - `l2_max_retransmission`

3. crash 제외 정책 명시
   - crash/dump 분석은 L1SW Log Analyzer 전담
   - 5.5 RCA KG에서는 신규 crash case 생성 금지

4. case_id 규칙 v2 반영
   - 날짜 기반 case_id 제거
   - `<fingerprint-slug>_<issue_type>_<3-digit-seq>` 사용

5. signal 파일명과 case_id 분리
   - signal 파일은 임시 분석 입력이므로 날짜 기반 파일명 허용
   - 정식 case_id는 분석 후 fingerprint 기반으로 부여

6. Claude Code 분석 요청 프롬프트 v2화
   - `fingerprint.signature_set`
   - `fingerprint.sequence`
   - `sequence_status`
   - `cptime_range`
   - `occurrence_count`
   - `recent_occurrences`
   - `unresolved` PENDING 처리 포함

7. v1 금지 필드 명시
   - `symptom.occurred_at`
   - `log_patterns.raw_examples`
   - `log_patterns.line_range`
   - `log_patterns.time_range`
   - `related.jira`
   - `issue_type: crash`

8. index.md 업데이트 기준을 fingerprint 중심으로 변경

9. unresolved 정의 보강
   - 원인 불명이 아니라 담당영역 밖 이관 상태로 설명

10. 다음 단계로 R3 `keywords.yaml` SSOT 설계 명시

---

## 3. 변경 파일

```text
scripts/README.md
HANDOFF_5.5.md
review_logs/rca_standalone_scripts_readme_v2_sync_20260622_0118_KST.md
```

---

## 4. 검증 결과

확인 항목:

```text
README 내 EXAMPLE_rach_failure_001.yaml 참조 제거
README 내 날짜 기반 case_id 생성 지시 제거
README 내 active crash case 생성 지시 제거
README 내 v2 분석 프롬프트 추가
README 내 사용 금지 필드 명시
```

주의:

```text
line_range, raw_examples, related.jira 같은 문자열은 README의 "사용 금지 필드" 또는 troubleshooting 설명에만 남아 있다.
실제 사용 지시로는 남아 있지 않다.
```

---

## 5. 남은 작업

다음 단계는 R3이다.

```text
R3. keywords.yaml SSOT 설계
```

R3에서 처리할 항목:

- issue_type별 signature ID 체계 정의
- confirmed / candidate / rejected 상태 정의
- ps1 키워드와 skills_seed 키워드 통합
- L1SW manifest fragment 생성 기준 정의
- `fingerprint.signature_set`과 `log_patterns[].signature` 네임스페이스 통일
