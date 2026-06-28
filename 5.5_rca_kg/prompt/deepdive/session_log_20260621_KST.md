# Session Log — 2026-06-21 KST (claude.ai 방향성 검토)

**환경:** claude.ai 채팅 (모바일)
**입력 패키지:** `RCA_standalone_20260619_1233_KST.zip`
**작업:** pre-filter와 5.5의 방향성 검토 + L1SW 추가 질문 리스트 작성

---

## 1. 이번 세션에서 확인된 것

### 1.1 Pre-filter의 정체성 재정립

기존 분석에서는 "Option A(역할 분리) 채택 시 5.5의 pre-filter 스크립트 폐기"를
검토했으나, 이번 세션에서 **pre-filter 자체가 폐기 대상이 아님**을 확인했다.

**핵심 인식 전환:**

```
기존 이해:
  L1SW가 1차 필터 → 5.5 pre-filter는 불필요 → scripts/ 폐기

수정된 이해:
  L1SW = 범용 필터 (모듈/시간 기반, issue_type 무관)
  5.5 pre-filter = issue_type 특화 필터 (_l1sw.txt 위에서 2차 grep)
  → pre-filter는 유지하되, 입력을 raw log → _l1sw.txt로 변경
  → 핵심 자산은 grep 스크립트가 아니라 "issue_type별 키워드 사전"
```

### 1.2 키워드 사전이 5.5의 핵심 자산

현재 패키지에서 키워드가 **3곳에 분산**되어 있고, 동기화가 안 됨:

| 위치 | 내용 | 문제 |
|---|---|---|
| `scripts/*.ps1` `$keywords` | grep 실행용 | 추정 태그만, 실검증 없음 |
| `skills_seed/*.md` Trigger Signatures | 분석 트리거 | ps1과 미묘하게 다름 |
| `prompt/5_5_...md` §10 #17 | 키워드 초안 | 또 다른 사본 |

**결론:** issue_type별 키워드 사전의 **Single Source of Truth** 파일이 필요.
제안된 위치: `rca_kg/schema/keywords.yaml`

### 1.3 키워드 누적 개선 루프 필요

키워드는 고정 자산이 아니라 분석 케이스가 쌓이면서 진화해야 함:

```
분석 1건 완료
  → Case YAML의 log_patterns에서 실제 hit한 키워드 확인
  → confirmed 승격 / rejected 처리 / 신규 candidate 추가
  → keywords.yaml 업데이트
  → scripts/*.ps1, skills_seed Trigger Signatures 자동 동기화
```

### 1.4 5.5의 진짜 가치는 "분석 후" 단계

패키지 전체를 읽은 결과, 설계 비중이 pre-filter(입력 축소)에 과도하게 쏠려 있음.
L1SW에 1차 필터를 위임한 뒤, 5.5의 설계 중심을 아래로 이동해야 함:

- `_l1sw.txt` → issue_type 자동 분류 로직
- 분석 결과 → Case YAML 생성 품질
- skills_seed checklist 실검증 + 강화 루프
- keywords.yaml 누적 관리

### 1.5 프롬프트 구조 문제

`5_5_..._prompt.md`가 두 가지 역할을 혼합하고 있음:
- A) Python 패키지 구현 명세 (Step 2용)
- B) Claude Code 분석 운영 가이드 (Step 1 현재 운영용)

→ 분리가 필요하지만, 이번 세션에서는 실행하지 않음.

---

## 2. 이번 세션에서 생성한 파일

| 파일 | 내용 |
|---|---|
| `L1SW_VERIFICATION_QUESTIONS_v2.md` | 기존 5개(블록A) + 신규 키워드 구조 6개(블록B) + 누적 메커니즘 4개(블록C) = 총 15개 질문 |
| `session_log_20260621_KST.md` | 이 파일 (세션 논의 요약) |
| `HANDOFF_5.5.md` | 업데이트 (§4 다음 세션 액션 전면 개정) |

---

## 3. 다음 세션에서 할 것

**최우선 (질문 답변 수집):**
1. 사내 Claude Code에서 L1SW 스킬 파일을 읽어 `L1SW_VERIFICATION_QUESTIONS_v2.md`의
   블록 A/B/C 15개 질문에 답변 채우기

**답변 수집 후 (설계 확정):**
2. 답변 기반으로 Option A/B/C 최종 선택
3. `keywords.yaml` SSOT 파일 초안 작성
4. 키워드 누적 개선 루프 설계 확정
5. 5.5 입력 소스를 `_l1sw.txt`로 재정의 (Option A 채택 시)
6. `5_5_..._prompt.md` 분리 여부 결정

**이후 (검증):**
7. 실 로그 1건으로 end-to-end 시범 운영
8. skills_seed "추정" 키워드 실검증
