# Review Log — signature 정합성 통일 + 원인분석 방법론 신설

작성: 2026-06-23 00:23 KST
세션: claude.ai (HANDOFF 확인 → deepdive 검토 → 방법론 강화)

---

## 1. 배경

HANDOFF 확인 후 5.5 deepdive(E2E P0~P6) 동작 가능성을 검토한 결과,
실행은 가능하나 fingerprint signature 표기가 keywords.yaml ID와 alias로 갈려 있어
P4 규칙(#2: ID 사용)과 예시 파일이 모순되는 결함 1건을 발견했다.
추가로 사용자가 "L1SW 원인분석 방법·접근법을 파악하게 하고, 분석/원인파악 성공률을
높이는 효율적·효과적 방법"을 프롬프트에 반영해 달라고 요청했다.

---

## 2. 변경 — signature 네임스페이스 통일 (1번)

| 파일 | before | after |
|---|---|---|
| `rca_case.schema.yaml` L74,78 | `["Msg1",...,"PHY_TIMER_EXPIRY"]` | `["RACH_MSG1",...,"RACH_PHY_TIMER_EXPIRY"]` |
| `EXAMPLE_v2_rach_failure_001.yaml` | `Msg1/Msg2/Msg3/PHY_TIMER_EXPIRY` | `RACH_MSG1/.../RACH_PHY_TIMER_EXPIRY` |
| `EXAMPLE_unresolved.yaml` | `SCG-Config/beamFail` | `SCG_CONFIG/SCG_BEAM_FAIL` |

검증: 3개 파일 `yaml.safe_load` OK. 모든 signature_set / sequence / log_patterns[].signature
참조가 keywords.yaml 의 실재 ID로 resolve됨(미해결 0건).

---

## 3. 변경 — deepdive 폴더 정리

| 파일 | 조치 |
|---|---|
| `L1SW_AND_FLOW_20260620.md` | 깨진 근거 파일명 `L1SW_CHECKLIST_OBJECTIVE_20260620.md` → `_v2.md` 수정 |
| `L1SW_VERIFICATION_QUESTIONS_v2.md` | 상단 "✅ 사용 완료 / 빈 양식 이력보존용" 마커 추가 |
| `L1SW_CHECKLIST_OBJECTIVE_v2.md` | 동일 마커 추가 |

빈 답변란을 미완성으로 오인하지 않도록 의도 명시. 내용 삭제 없음.

---

## 4. 신설 — RCA_ANALYSIS_METHODOLOGY.md

기존 공백: 워크플로(root_cause 위치/confidence 표기/unresolved 분리)는 있었으나
**원인 도출 추론 방법**이 없었다. issue_type 공통 7단계 엔진으로 채움.

- S1 증상 anchor 고정(가장 이른 failure_event cptime)
- S2 시간창(anchor 앞=원인, 뒤=fallback)
- S3 정상경로 대조 → 최초 이탈 지점 특정(원인에 가장 가까움)
- S4 가설 2~4개(skills_seed Root Cause Categories, 1개 즉단 금지)
- S5 가르는 단서만 grep(전체 정독 금지)
- S6 단말 vs 환경 분리 → 환경이면 unresolved+handoff
- S7 인과사슬 + confidence(증거 충족도 §3 표)

부가: 효율 규칙(§4), 안티패턴(§5: 증상=원인 금지, 첫가설 확증 금지 등), case 매핑(§6).

설계 의도: 성공률(과신·확증편향 차단) + 효율(가설이 부르는 grep만, anchor부터 바깥).

---

## 5. 변경 — E2E 프롬프트 P4/P5 강화

- **P4**: METHODOLOGY 문서 첨부. PART A(7단계 추론, 근거 cptime 제시) → PART B(YAML 매핑)
  2부 구조로 재편. root_cause.summary=인과사슬 강제, confidence=§3 표 강제,
  sequence/signature ID 표기 명시.
- **P5**: 자가점검에 4개 항목 추가 — ID 표기 위반 / 인과사슬 vs 증상나열 / confidence 정합 /
  환경원인을 low로 보유 금지.

---

## 6. 영향 범위 / 비파괴성

- schema 구조·필드 정의 자체는 변경 없음(example 값과 note만). 기존 case 호환 유지.
- 방법론은 신규 문서 + 프롬프트 참조로만 작동. 실행 파이프라인(P0~P3,P6) 불변.
- keywords.yaml / taxonomy / scripts 미변경.

버전: 패키지 v0.2 → v0.3 (methodology 반영본).
