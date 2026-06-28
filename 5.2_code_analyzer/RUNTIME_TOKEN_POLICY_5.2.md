# RUNTIME_TOKEN_POLICY_5.2 — CodeAnalyzer 토큰 운영 정책

갱신: 2026-06-27 10:38 KST  
대상: `/code-analyzer` 스킬 실행

---

## 1. 원칙

스킬 방식에서는 세션 불변 규칙이 `skills/code-analyzer/SKILL.md`에 내장되어 있으므로, 사용자가 공통 프롬프트를 반복해서 붙여넣지 않는다.

토큰 절감의 핵심은 다음이다.

```text
- 전체 reference를 매 단계 다시 읽지 않음
- structure 전체 반복 read 금지
- procedure_runtime_index slice 우선 사용
- procedure별 local_call_edges 유지
- 전역 call edge 본문 누적 금지
- MSC는 HLD md와 분리해 .puml로 저장
```

---

## 2. 런타임 read 정책

| 단계 | 읽는 것 | 피하는 것 |
|---|---|---|
| 시작 | `NEXT_STEP_5.2.md`, 현재 slug의 `analysis_progress.md` | 모든 reference 전문 재읽기 |
| structure 확보 | focused structure | 큰 full structure 자동 read |
| procedure 분석 | `procedure_runtime_index[procedure_slug]` | structure 전체 반복 read |
| 마무리 | procedure 요약, msc_ref | PlantUML 전체 inline 누적 |

---

## 3. 레거시 prompt 폴더

`prompt/` 폴더는 스킬 설치가 불가능한 환경의 하위 호환용이다. 정상 사용에서는 `/code-analyzer`만 호출한다.

---

## 4. 사용자 입력 최소화

사용자가 반복 입력하지 않아야 하는 값:

```text
- slug
- Track A/B 선택
- 다음 phase prompt 선택
- output 경로
- KST timestamp
```

사용자가 제공해야 하는 값:

```text
- 코드 루트
- 분석 대상 블록명 또는 API명
```
