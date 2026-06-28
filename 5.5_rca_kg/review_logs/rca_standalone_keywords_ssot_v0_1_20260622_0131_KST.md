# RCA Standalone R3 — keywords.yaml SSOT v0.1 생성

작성일: 2026-06-22 01:31 KST  
대상: RCA Standalone  
기준 패키지: `RCA_standalone_20260622_0118_KST_scripts_readme_v2_sync.zip`

---

## 1. 작업 목적

RCA 분석에서 사용하는 keyword/signature가 `scripts/*.ps1`, `skills_seed/*.md`, `prompt/*.md`에 분산되어 있었다.
이번 작업에서는 이를 `rca_kg/keywords.yaml`로 통합하여 RCA Signature Registry의 SSOT를 만들었다.

---

## 2. 생성 파일

```text
rca_kg/keywords.yaml
rca_kg/schema/keywords.schema.yaml
review_logs/rca_standalone_keywords_ssot_v0_1_20260622_0131_KST.md
```

수정 파일:

```text
HANDOFF_5.5.md
scripts/README.md
```

---

## 3. 설계 컨셉

`keywords.yaml`은 단순 keyword list가 아니라 RCA Signature Registry다.

```text
keyword = 로그에 실제 찍히는 문자열 또는 regex 후보
signature = RCA 분석에서 쓰는 표준화된 의미 ID
alias = 하나의 signature로 정규화 가능한 원문 표현 목록
```

`fingerprint.signature_set`과 `log_patterns[].signature`는 반드시 `keywords.yaml`의 signature ID를 참조한다.

---

## 4. 초기 등록 결과

| issue_type | signature 수 | confirmed | candidate |
|---|---:|---:|---:|
| rach_failure | 11 | 1 | 10 |
| scg_failure | 12 | 0 | 12 |
| tx_abnormal | 5 | 0 | 5 |
| l2_max_retransmission | 6 | 0 | 6 |
| **합계** | **34** | **1** | **33** |

현재 confirmed는 `RACH_PHY_TIMER_EXPIRY` 하나다.
나머지는 실 로그 검증 전이므로 candidate로 둔다.

---

## 5. 중요한 정책 결정

1. `crash`는 active issue_type에 포함하지 않았다.
   - crash/dump 분석은 L1SW Log Analyzer 전담이다.

2. Generic keyword는 fingerprint 기본 후보에서 제외했다.
   - 예: `RACH`, `SCG`, `RLC`, `HARQ`
   - 이유: 너무 넓어 동일 원인 판정 fingerprint를 오염시킬 수 있음

3. Candidate signature를 fingerprint에 넣을 수는 있지만, 그 경우 `sequence_status: draft` 유지가 권장된다.

4. R3에서는 scripts/*.ps1을 수정하지 않았다.
   - R4 이후 `keywords.yaml` 기준으로 prefilter script 또는 L1SW manifest fragment 동기화 여부를 판단한다.

---

## 6. 다음 단계

다음 단계는 R4다.

```text
R4. L1SW manifest fragment 후보 설계
```

R4에서는 `keywords.yaml`에서 아래 조건을 만족하는 signature를 추출한다.

```text
use_for.l1sw_manifest_fragment: true
status: confirmed 또는 candidate
noise_risk: low 또는 medium 우선
role: context 는 기본 제외 또는 별도 검토
```

그 결과로 아래 파일 후보를 만들 수 있다.

```text
rca_kg/l1sw_fragments/rca_rach.fragment.json
rca_kg/l1sw_fragments/rca_scg.fragment.json
rca_kg/l1sw_fragments/README.md
```
