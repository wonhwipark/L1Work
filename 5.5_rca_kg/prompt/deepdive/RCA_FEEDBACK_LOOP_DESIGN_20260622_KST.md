# RCA 피드백 루프 전체 구조 — 2026-06-22 세션 설계

근거 세션: 2026-06-22 (claude.ai), 직전 문서: `L1SW_AND_FLOW_20260620.md`
이 문서는 "L1SW manifest 보강" 아이디어부터 "case 용량 통제", "unresolved 이관/통합
워크플로", "case 스키마 v2" 까지 한 세션에서 합의된 전체 설계를 하나로 묶은 기록이다.
스키마 자체의 필드 정의는 `rca_kg/schema/rca_case.schema.yaml` 이 SSOT이며, 이 문서는
**왜 그렇게 설계했는지**(설계 의도·결정 이력)를 보존하는 용도다.

---

## 1. 출발점 — "pre-filter가 결국 모듈별 키워드 아니냐?"는 질문

`L1SW_AND_FLOW_20260620.md`에서 확정된 사실 두 가지가 이 세션의 전제였다.

- L1SW manifest regex는 **모듈명(prefix)만** 매핑한다. 증상 키워드(`PHY_TIMER_EXPIRY` 등)는
  매핑하지 않는다 (§1.2, §1.4).
- L1SW의 지식 누적 경로 중 하나가 **manifest 갱신**(`manifest/<part>.json`에 regex 한 줄
  추가)이다 (§1.5). 이는 L1SW가 원래 의도한 정상적인 확장 경로다.

여기서 실제 pre-filter 스크립트(`rach_failure_prefilter.ps1`, `scg_failure_prefilter.ps1`)를
열어보니, 키워드는 모듈명이 아니라 **증상/프로토콜 용어**(`Msg1~4`, `RAR`, `T310`,
`beamFail` 등)였다. 즉 L1SW의 모듈 축과 5.5의 증상 축은 **다른 축**이며, pre-filter는
L1SW의 `-Modules` 옵션으로 대체되지 않는다는 점이 1차로 확인되었다.

### 1.1 결론 — manifest fragment 확장 (L1SW 무수정)

L1SW를 수정하지 않고, **issue_type 전용 fragment JSON**을 추가하는 방식으로 결론지었다.

```json
// rca_rach.json (5.5가 생성·관리, 피드백으로 채워짐)
{
  "RACH_module":  "\\[PHY_RACH\\]|\\[MAC_RA\\]",
  "RACH_symptom": "PHY_TIMER_EXPIRY|RAR|Msg[1-4]|RA-RNTI"
}
```

이 방식이 성립하는 전제 조건은 `parse.ps1`의 `Select-String`이 **줄 전체 매칭**인지
여부였다. **본 세션에서 "줄 전체 매칭"으로 확인됨** → manifest fragment에 증상 키워드를
그대로 넣어도 동작한다. 이로써 다음이 확정되었다.

- L1SW 코드 0줄 수정으로 issue-aware `_l1sw.txt` 생성 가능
- 5.5의 별도 grep 2차 패스가 (최소한 1차 필터링 단계에서는) 불필요해질 수 있음
- 피드백 루프의 출력처가 명확해짐: 분석자가 confirmed로 전환할 때 결정적이었던 키워드가
  바로 이 fragment JSON의 `*_symptom` 엔트리로 들어간다

---

## 2. 전체 순환 구조

```text
.sdm 원본
   │
   ▼
L1SW 필터 (manifest: 모듈 + issue_type별 증상 fragment) ──┐
   │                                                        │ ②
   ▼                                                        │ manifest 보강
_l1sw.txt (issue-aware 축소본)                              │
   │                                                        │
   ▼                                                        │
5.5 분석 (유형판정 + root_cause 추정)                       │
   │                                                        │
   ▼                                                        │
case 생성 ── fingerprint 매칭 ──┬─ 일치 → occurrence_count++ │
   │                            └─ 불일치 → 신규 case        │
   │                                                        │
   ├─ 담당영역 내, 원인 불확실 → status: analyzed            │
   │                              (confidence: low/medium…)  │
   │                                                        │
   └─ 담당영역 밖 → status: unresolved                       │
        (cases/unresolved/, handoff 블록, root_cause=null)   │
              │                                              │
              ▼ 분석자(이관받은 담당자) 입력                  │
        root_cause / fix / review 직접 채움                  │
        status → confirmed                                  │
              │                                              │
              ▼ 통합(merge)                                  │
        fingerprint 재매칭 → 기존 case 병합 또는 cases/ 승격  │
              │                                              │
              ▼ ① 자산 갱신                                   │
   ┌──────────────────────────────────────────┐              │
   │ keywords.yaml (confirmed/candidate)        │──────────────┘
   │ skills_seed/*.md (issue_type 분석지식)     │
   │ indexes_tool_generate/index.md (fingerprint 검색)        │
   └──────────────────────────────────────────┘
              │
              ▼ ③ 다음 분석에 자동 주입
        (다음 5.5 분석 프롬프트 강화 / 유사사례 즉시 매칭)
```

순환의 핵심은 세 화살표다.

- **① 피드백 → 자산 갱신**: 분석자가 unresolved를 confirmed로 바꾸며 입력한 결정적
  키워드/패턴이 keywords.yaml·skills_seed에 반영된다.
- **② 자산 → L1SW manifest 보강**: 갱신된 키워드가 `*_symptom` fragment에 들어가 다음
  입력(`_l1sw.txt`) 자체가 더 정확해진다.
- **③ 자산 → 다음 분석 강화**: 갱신된 skills_seed/index가 다음 5.5 분석 프롬프트와
  유사사례 검색에 자동 반영된다.

---

## 3. case 용량 비대화 방지 설계

누적되는 자산이 case YAML이라, "무엇을 case 안에 담고 무엇을 밖으로 빼는가"가 핵심
설계축이었다. 원칙은 **"case는 포인터, 데이터는 한 곳에"**.

| 데이터 | 저장 위치 | case에는 |
|---|---|---|
| 로그 본문 | `_l1sw.txt` (항상 보존) | 경로 + cptime_range 참조만 |
| signature 정의 | keywords.yaml | ID 참조만 |
| 검색 메타 | indexes_tool_generate/index.md | — |
| 원인·해결법 | case 본문 | 요약형으로 직접 보유 |

`raw_examples`(로그 원문 인라인)를 스키마에서 제거하고, `log_patterns[].signature` +
`cptime_range`로 대체한 이유가 이것이다.

### 3.1 동일 원인 재발 — time_range로 묶을 수 없는 이유

통신 프로토콜 로그는 단말 시험마다 wall-clock이 다르므로, **시각 기반으로는 "같은
장애"를 식별할 수 없다.** 이를 해결하기 위해 두 층으로 식별 키를 분리했다.

- **파일-로컬 포인터** (`log_patterns[].cptime_range`): 한 파일 안에서만 유효, 증거 위치용
- **시간 불변 핑거프린트** (`fingerprint.signature_set` + `sequence`): case 간 동일성
  판정용. 절대 시각을 모두 제거하고 시그니처 집합과 **상대 순서**만 남긴다.

순서 추출 기준 시각은 **cptime**(캡처/칩 기준 단조 증가 시각)으로 통일했다. wall-clock은
시험마다 다르고 드리프트 가능성이 있지만, cptime은 이벤트 선후 관계가 시험 간에도
안정적으로 보존되기 때문이다. 다만 cptime은 절대값 자체는 fingerprint에 포함하지 않고
**정렬에만** 사용한다.

```yaml
fingerprint:
  signature_set: [Msg1, Msg2, Msg3, PHY_TIMER_EXPIRY]
  sequence: "Msg1→Msg2→Msg3→(PHY_TIMER_EXPIRY)"   # cptime 정렬 결과, 절대값 미포함
  sequence_status: draft | confirmed
```

매칭 키는 `signature_set + sequence` 두 가지로 확정했다 (module_set은 매칭 키에서
제외 — 참고 정보로만 `symptom.module`에 유지).

#### sequence 자동 초안의 동작 방식

5.5는 별도 파서가 아니라 LLM 기반 분석이므로, "자동 초안"은 규칙 스크립트가 아니라
**분석 단계에서 모델이 cptime 순으로 줄을 정렬해 시그니처만 추출**하는 방식이다.

```
입력: _l1sw.txt 구간 (각 줄에 cptime 포함)
처리: 모델이 cptime으로 정렬 → issue_type 시그니처만 추출 → 절대값 제거, 순서만 표기
출력 초안: "Msg1 → Msg2 → Msg3 → (PHY_TIMER_EXPIRY)"
```

초안 단계에서는 노이즈(무관한 모듈 로그 혼입)나 인과관계 오판 가능성이 있어
`sequence_status: draft`로 표시되고, 분석자가 노이즈를 제거하고 **정규형**으로 확정하면
`confirmed`로 전환된다. 확정된 정규형이 이후 매칭의 기준이 된다.

### 3.2 재발 시 case 본체 미증식 — occurrence_count

동일 fingerprint가 재발할 때마다 새 case를 만들지 않고 카운터만 올린다.

```yaml
occurrence_count: 7
recent_occurrences:     # 최근 5건만 유지, 초과분은 순환 폐기
  - { date: ..., signal_file: ..., cptime_range: ..., jira: ... }
first_seen: 2026-05-30
last_seen:  2026-06-21
```

**트레이드오프**: `recent_occurrences`가 최근 5건만 유지하므로, 6번째 재발부터는 가장
오래된 발생의 Jira 참조가 자연 소실된다. 전체 이력이 아니라 "최근 동향" 추적이 목적이라는
것을 의도적으로 받아들였다. `related.jira`는 폐기하고 `recent_occurrences[].jira`로
단일화했다 (Single Source of Truth).

---

## 4. unresolved — "원인 불명"과 "담당 밖"의 구분

핵심 정의: `unresolved` ≠ "원인을 모른다". 원인 불확실은 `status: analyzed` +
`root_cause.confidence: low`로 이미 표현 가능하다. `unresolved`는 **"이건 내 담당
모듈/도메인 문제가 아니다"라는 판단 결과**이며, 타 담당자 이관이 필요한 상태다.

### 4.1 파일 분리 + null 신호

```
rca_kg/cases/unresolved/<date>_<issue_type>_<seq>_PENDING.yaml   ← 이관 대기
rca_kg/cases/<fingerprint-slug>_<issue_type>_NNN.yaml             ← 확정 자산
```

`unresolved/` 파일은 `root_cause`, `fix`, `skill_seed`, `review`가 **명시적으로 null**이다.
이 null 자체가 "분석자가 아직 입력하지 않았다"는 신호이며, 폴더 위치와 status 필드 두
군데서 동시에 확인할 수 있다.

```yaml
status: unresolved
handoff:
  reason: "..."
  suspected_domain: "..."
  suspected_owner: "..."
  handed_off_at: 2026-06-22
root_cause: null
fix: null
review: null
```

### 4.2 통합(merge) 절차

1. **이관**: `cases/unresolved/`에 PENDING 파일 생성. fingerprint는 가능한 범위까지만
   기록(미완성 허용, `sequence_status: draft` 가능).
2. **분석자 입력**: 이관받은 담당자가 같은 파일을 열어 `root_cause`/`fix`/`review`를
   직접 채우고 `status`를 `confirmed`(또는 `rejected`)로 변경, `sequence_status`를
   `confirmed`로 정규화.
3. **통합**: fingerprint(`signature_set`+`sequence`) 기준으로 `cases/` 내 기존 case와
   매칭.
   - 일치 → 기존 case의 `occurrence_count++`, `recent_occurrences`에 추가(5건 초과 시
     가장 오래된 항목 폐기). PENDING 파일은 폐기.
   - 불일치 → 정식 `case_id`를 fingerprint 기준으로 부여, `cases/`로 승격(파일 이동).
4. `indexes_tool_generate/index.md` 갱신.

---

## 5. 5.0/5.2 연결 — TODO로 분리

5.0(common framework)/5.2(Code Analyzer) 산출물이 RCA의 root_cause 단계에 도움을 줄 수
있는 영역(모듈→코드 위치 매핑)은 인정하나, 5.2 산출물 구조가 아직 확인되지 않았다.

**결정**: RCA 스키마에 `root_cause.code_ref` 옵션 필드만 비워두고, 자동 연결은 5.2 산출물
구조 확인 후 TODO로 분리한다. RCA 본 피드백 루프를 5.2 진행 상황에 의존시키지 않는다.

---

## 6. 이번 세션 결정 이력 요약

| # | 주제 | 결정 |
|---|---|---|
| 1 | pre-filter의 정체 | 모듈 키워드 아님, 증상/프로토콜 키워드. L1SW와 축이 다름 |
| 2 | L1SW 보강 방식 | manifest fragment 추가 (L1SW 코드 무수정) |
| 3 | parse.ps1 매칭 방식 | 줄 전체 매칭 (확인 완료) → fragment 방식 성립 |
| 4 | 5.0/5.2 연결 | RCA 의존성으로 묶지 않음, `code_ref` 필드만 두고 TODO |
| 5 | 피드백 루프 핵심 | 분석자 입력 → keywords/skills_seed 자동 갱신 → 다음 분석 강화 |
| 6 | line_range 사용 불가 | 단말 시험 wall-clock 비교 불가 → cptime 기반 sequence로 전환 |
| 7 | fingerprint 매칭 키 | signature_set + sequence (module_set 제외) |
| 8 | sequence 채움 방식 | LLM 자동 초안(cptime 정렬) + 분석자 정규형 확정 |
| 9 | 재발 처리 | occurrence_count + recent_occurrences(최근 5건만) |
| 10 | jira 추적 | related.jira 폐기, recent_occurrences[].jira로 단일화 |
| 11 | unresolved 정의 | "담당영역 밖 이관"으로 한정 (원인불명=analyzed+confidence:low와 구분) |
| 12 | unresolved 저장 | cases/unresolved/ 별도 폴더 + 명시적 null 필드 |
| 13 | 통합 절차 | 분석자 입력 완료 후 fingerprint 매칭 → 병합 또는 cases/ 승격 |

---

## 7. 다음 세션 연결 지점

- `keywords.yaml` 실제 구현 시 `signature` ID 체계가 본 문서의 `fingerprint.signature_set`,
  `log_patterns[].signature`와 동일 네임스페이스를 공유해야 함 (SSOT 일관성).
- `taxonomy.yaml`에 fingerprint 관련 신규 개념(예: signature 사전) 반영 필요 여부 확인.
- `indexes_tool_generate/index.md` 포맷을 fingerprint 기준 검색에 맞춰 재설계 필요.
- manifest fragment(`rca_rach.json` 등) 실제 작성은 사내 L1SW 환경에서 진행.
- 실 로그 1건으로 end-to-end 검증 시, 이번에 설계한 schema v2 전체(특히 fingerprint
  자동 초안 정확도)를 함께 검증.
