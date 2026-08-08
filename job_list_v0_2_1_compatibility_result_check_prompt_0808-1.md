# Job-list v0.2.1 Compatibility Check 결과 확인 프롬프트

## 목적

`job-list v0.2.1`의 `compatibility-check` 수행 결과를 확인하고,
각 Skill이 새 implementation 경로로 Activation 가능한 상태인지 판정한다.

이번 작업은 **검증 전용**이다.

절대로 다음 작업을 수행하지 않는다.

- 기존 Skill/Knowledge 파일 수정
- 기존 경로 삭제/이동/rename
- 새 경로 Activation
- `SKILL.md` 이동
- 환경변수 변경
- GitHub push
- Skill rename
- legacy path 자동 수정
- skillsilent 변경/업데이트
- skill-updater 변경/업데이트

---

# 1. 현재 확정 경로

## Claude Skill Entry

다음 위치는 유지한다.

```text
~/.claude/skills/<skill>/SKILL.md
```

이 경로를 새 implementation root로 이동하지 않는다.

---

## 개인 Skill implementation 목표 경로

```text
~/l1sw-skills/private-skills/<skill>/
```

과거 제안 경로인 아래 위치는 사용하지 않는다.

```text
~/l1sw-skills/private/<skill>/
~/l1sw-skills/private/skills/<skill>/
```

---

## Knowledge 목표 경로

```text
~/l1sw-knowledge/
```

Knowledge와 Skill implementation은 분리한다.

---

# 2. 사전 조건 확인

먼저 현재 설치된 `job-list` 버전을 확인한다.

기대:

```text
job-list v0.2.1
```

버전이 다르더라도 파일이나 설정을 수정하지 말고 현재 확인 결과에 기록한다.

그 다음 `job-list v0.2.1`의 compatibility-check 결과 파일을 탐색한다.

우선 확인 위치:

```text
~/.claude/main/job-list/output/actions/
```

예상 파일 형태:

```text
migration_*_r*_<timestamp>.json
```

추가 확인 위치:

```text
~/.claude/main/job-list/output/last_run.json
~/.claude/main/job-list/output/runs/
~/.claude/main/job-list/history/job_history.jsonl
```

가장 최근 수행 결과를 기준으로 분석한다.

동일 시각대 결과가 여러 개 있으면 다음 우선순위를 사용한다.

```text
1. compatibility-check 결과
2. 가장 최신 revision
3. 가장 최신 timestamp
```

결과 파일을 찾지 못하면 임의로 생성하거나 compatibility-check를 재실행하지 않는다.

다음과 같이 판정하고 종료한다.

```text
RESULT = NOT_FOUND
reason = compatibility-check 결과 파일을 찾지 못함
```

---

# 3. 각 Skill에서 반드시 확인할 항목

각 migration item / Skill마다 다음 항목을 확인한다.

## A. activation_readiness

정상:

```text
READY
```

문제:

```text
BLOCKED
```

`BLOCKED`이면 Activation 금지 대상으로 판정한다.

---

## B. manifest_match

정상:

```text
true
```

다음이면 BLOCKED 처리한다.

```text
false
missing
unknown
```

source와 target의 manifest/checksum 일치가 확인되지 않은 상태에서는
Activation 가능으로 판정하지 않는다.

---

## C. blocking_reasons

정상:

```text
[]
```

내용이 하나라도 있으면 모두 수집한다.

특히 다음 유형을 구분한다.

```text
legacy runtime path
missing target
manifest mismatch
source/target inconsistency
unsafe path
symlink
verification failure
기타
```

---

## D. source_changed

정상:

```text
false
```

`true`이면 즉시 중요 오류로 분류한다.

Compatibility Check는 source를 변경하면 안 된다.

---

## E. write_performed

정상:

```text
false
```

`true`이면 중요 오류로 분류한다.

---

## F. activation_performed

정상:

```text
false
```

`true`이면 중요 오류로 분류한다.

이번 단계에서는 Activation이 발생하면 안 된다.

---

# 4. Legacy Path 분석

Compatibility report에 legacy path 참조가 있으면
각 항목의 실제 파일과 line을 확인한다.

가능하면 다음 정보를 수집한다.

```text
Skill
파일 경로
line number
발견 문자열
분류
```

## BLOCKER로 취급할 경로

실행 코드, script, config 등에 아래 경로가 runtime path로 사용되면 BLOCKER다.

```text
~/.claude/main/<skill>
.claude/main/<skill>

~/l1sw-skills/private/<skill>
~/l1sw-skills/private/skills/<skill>
```

문자열 표현 방식이 조금 달라도 같은 legacy root 의미이면 동일하게 분류한다.

예:

```python
Path.home() / ".claude" / "main" / "issue-analyzer"
```

도 legacy runtime path로 간주한다.

---

## BLOCKER가 아닌 경로

다음 경로 자체는 현재 유지 대상이다.

```text
~/.claude/skills/<skill>/SKILL.md
```

따라서 `.claude/skills` 참조만 있다는 이유로 BLOCKED 처리하지 않는다.

단, 해당 참조가 implementation/data storage 위치로 잘못 사용되고 있다면
별도 WARNING으로 기록한다.

---

# 5. 데이터 파일 오탐 방지

Knowledge, report, history, sample, test fixture 등에
과거 경로 문자열이 단순 데이터로 포함되어 있을 수 있다.

다음과 같이 구분한다.

```text
실행/runtime/config에서 사용
→ BLOCKER 후보

문서/로그/history/example/test fixture에 단순 문자열로 존재
→ WARNING 또는 INFORMATION
```

단순 문자열 검색 결과만으로 Skill을 BLOCKED 처리하지 않는다.

실제 runtime path 의존 여부를 확인한다.

---

# 6. 최종 Skill별 판정 규칙

## READY

다음 조건을 모두 만족해야 한다.

```text
activation_readiness == READY
manifest_match == true
blocking_reasons == []
source_changed == false
write_performed == false
activation_performed == false
```

추가 legacy path 분석에서도 runtime BLOCKER가 없어야 한다.

---

## BLOCKED

다음 중 하나라도 해당하면 BLOCKED다.

```text
activation_readiness == BLOCKED
manifest_match != true
blocking_reasons가 비어 있지 않음
runtime legacy path 발견
target 검증 실패
source/target 불일치
unsafe path 발견
```

---

## CRITICAL

다음 중 하나라도 해당하면 일반 BLOCKED보다 높은 `CRITICAL`로 표시한다.

```text
source_changed == true
write_performed == true
activation_performed == true
기존 source 삭제/rename 흔적
```

이 경우 추가 작업을 수행하지 말고 즉시 분석만 종료한다.

---

# 7. 전체 단계 판정

모든 대상 Skill이 READY이면:

```text
PHASE_2_COMPATIBILITY = PASS
NEXT_STEP = ACTIVATION_DESIGN
```

단, 여기서 Activation을 실제 수행하지 않는다.

하나라도 BLOCKED이면:

```text
PHASE_2_COMPATIBILITY = BLOCKED
NEXT_STEP = FIX_BLOCKED_SKILLS
```

하나라도 CRITICAL이면:

```text
PHASE_2_COMPATIBILITY = CRITICAL
NEXT_STEP = STOP_AND_REVIEW
```

결과 자체를 찾지 못하면:

```text
PHASE_2_COMPATIBILITY = NOT_FOUND
NEXT_STEP = CHECK_JOB_LIST_EXECUTION
```

---

# 8. 출력

분석 결과를 화면에 요약하고,
가능하면 다음 파일에도 저장한다.

```text
~/.claude/main/job-list/output/compatibility_review.md
```

단, 이 결과 보고서 외의 기존 파일은 수정하지 않는다.

보고서 형식:

```markdown
# Job-list v0.2.1 Compatibility Review

## 1. Overall

- Job-list version:
- Compatibility result:
- Checked report:
- PHASE_2_COMPATIBILITY:
- NEXT_STEP:

## 2. Skill Summary

| Skill | Result | Manifest | Legacy Runtime Path | Source Changed | Activation | Reason |
|---|---|---|---|---|---|---|
| code-analyzer | READY | PASS | NONE | false | false | - |
| issue-analyzer | BLOCKED | PASS | FOUND | false | false | legacy runtime path |

## 3. BLOCKED Details

### <skill>

- Result:
- Blocking reason:
- File:
- Line:
- Legacy path/reference:
- Recommended correction concept:

주의:
Recommended correction concept만 제시하고 실제 파일은 수정하지 않는다.

## 4. Warnings

- `.claude/skills` entry reference
- history/sample/test-only legacy strings
- 기타 non-blocking warning

## 5. Safety Validation

- source_changed:
- write_performed:
- activation_performed:
- source delete/rename detected:

## 6. Final Decision

PHASE_2_COMPATIBILITY = PASS | BLOCKED | CRITICAL | NOT_FOUND
NEXT_STEP = ACTIVATION_DESIGN | FIX_BLOCKED_SKILLS | STOP_AND_REVIEW | CHECK_JOB_LIST_EXECUTION
```

---

# 9. 실행 원칙

이 작업은 저사양 모델에서도 안정적으로 끝까지 수행할 수 있도록 다음 원칙을 따른다.

1. 추가 질문하지 않는다.
2. 먼저 기계적으로 결과 파일을 찾는다.
3. JSON parsing과 path/reference 분석은 Python을 우선 사용한다.
4. 가능하면 하나의 Python 실행 흐름으로 분석한다.
5. 분석 대상이 많아도 중간에 사용자 승인을 요청하지 않는다.
6. 파일 수정은 `compatibility_review.md` 보고서 생성만 허용한다.
7. Activation은 절대 수행하지 않는다.
8. BLOCKED Skill의 소스 자동 수정도 하지 않는다.
9. 결과가 불명확하면 READY로 추정하지 말고 BLOCKED 또는 NOT_FOUND로 판정한다.
10. 마지막에 다음 단계만 명확히 표시한다.

---

# 10. 최종 요청

위 기준으로 현재 사내 PC의 `job-list v0.2.1 compatibility-check` 수행 결과를 분석해줘.

가장 중요한 목표는:

```text
각 Skill이
~/l1sw-skills/private-skills/<skill>/
경로를 실제 runtime implementation root로 사용하도록
Activation해도 되는 상태인지 사전에 검증하는 것
```

이다.

하지만 이번 작업에서는 **Activation을 수행하지 않는다.**

최종 답변 마지막에는 반드시 아래 형태로 출력해줘.

```text
PHASE_2_COMPATIBILITY = <PASS|BLOCKED|CRITICAL|NOT_FOUND>
READY_SKILLS = <count>
BLOCKED_SKILLS = <count>
CRITICAL_SKILLS = <count>

NEXT_STEP = <ACTIVATION_DESIGN|FIX_BLOCKED_SKILLS|STOP_AND_REVIEW|CHECK_JOB_LIST_EXECUTION>
```

`BLOCKED`가 있으면 Skill 이름과 수정이 필요한 파일/line/path를 함께 요약해줘.
