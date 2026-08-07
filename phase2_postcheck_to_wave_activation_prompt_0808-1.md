# Phase 2 Activation — Post-check부터 Wave 1~4까지 통합 실행 프롬프트

- 기준일: 2026-08-08 KST
- 적용 대상: `job-list v0.3.0` Activation Plan 수행 이후
- 목적: **Post-check → Wave 1~4 staged Activation → 각 Wave validation → Phase 2 최종 검증**을 하나의 프롬프트로 수행한다.
- 핵심: 각 단계가 PASS일 때만 다음 단계로 이동한다.
- 실패 시 즉시 중단하고 **정확히 어느 단계/어느 Skill에서 실패했는지** 반환한다.
- 이 프롬프트는 **Phase 3 Knowledge Migration을 수행하지 않는다.**

---

# 회사 Claude Code 실행 프롬프트

```text
job-list v0.3.0 Activation Plan 수행 이후의 Phase 2 Activation을 진행해줘.

이번 요청은 하나의 staged workflow로 실행한다.

순서:

POST_CHECK
→ WAVE_1_PREFLIGHT
→ WAVE_1_APPLY
→ WAVE_1_VALIDATE
→ WAVE_2_PREFLIGHT
→ WAVE_2_APPLY
→ WAVE_2_VALIDATE
→ WAVE_3_PREFLIGHT
→ WAVE_3_APPLY
→ WAVE_3_VALIDATE
→ WAVE_4_PREFLIGHT
→ WAVE_4_APPLY
→ WAVE_4_VALIDATE
→ PHASE_2_FINAL_VALIDATE
→ PHASE_2_COMPLETE

각 단계가 PASS일 때만 다음 단계로 진행해라.

어느 단계에서든 FAIL / BLOCKED / CRITICAL / 결과 불명확이 발생하면:

1. 즉시 다음 단계 진행 중단
2. 필요한 rollback 수행
3. 실패 단계와 실패 Skill을 정확히 기록
4. 원인을 증거 파일/경로와 함께 출력
5. Phase 3로 절대 이동하지 않음

사용자에게 중간 확인 질문을 요구하지 말고,
확실하게 안전한 범위 내에서 자동 수행하되
안전 Gate가 만족되지 않으면 fail-closed로 종료해라.

==================================================
0. CURRENT BASELINE
==================================================

Claude Skill Entry:

~/.claude/skills/<skill>/SKILL.md

위치는 유지한다.

NEW Skill implementation root:

~/l1sw-skills/private-skills/<skill>/

OLD runtime / rollback source:

~/.claude/main/<skill>/

OLD runtime은 이번 Phase에서 삭제/이동/cleanup하지 않는다.

현재 실행 엔진:

skill-updater v0.5.11
skillsilent v0.2.36

이번 Phase에서 고정 엔진으로 취급한다.

Activation target에서 반드시 제외:

- job-list
- skill-updater
- skillsilent
- autotask-builder

이번 Workflow에서 금지:

- ~/.claude/main/<skill>/ 삭제
- ~/.claude/main/<skill>/ move
- OLD runtime cleanup
- Skill rename
- GitHub push
- skillsilent v0.2.37 적용
- skillsilent update
- skill-updater update/self-update
- job-list self-update
- autotask-builder activation/update
- Knowledge Store migration
- ~/l1sw-knowledge/ 전환
- source code 임의 리팩토링
- plan에 없는 Python/config 수정
- dependency 임의 추가
- Wave 순서 임의 변경
- 하나의 Wave 검증 실패 후 다음 Wave 진행

==================================================
1. RESULT / LOG ROOT 확인
==================================================

job-list output의 실제 최신 결과를 찾아라.

우선 탐색:

~/.claude/main/job-list/output/last_run.json

~/.claude/main/job-list/output/runs/<run_id>/summary.json

~/.claude/main/job-list/output/actions/activation_plan_*.json

~/.claude/main/job-list/output/actions/*activation*.json

~/.claude/main/job-list/output/actions/migration_*_r*_*.json

~/.claude/main/job-list/output/compatibility_review.md

파일명이 조금 다르다면 output 폴더 내부에서
가장 최근 job-list v0.3.0 실행과 직접 연결된 결과를 탐색해라.

이전 v0.2.x 결과나 오래된 v0.3.0 결과를
최신 실행 결과로 오인하지 마.

가능하면 다음을 서로 연결해서 확인:

- run_id
- timestamp
- plan file
- plan SHA256
- compatibility result
- Wave definition
- rollback metadata

==================================================
2. 공통 FAIL 반환 규칙
==================================================

어느 단계에서든 실패하면 최종 출력 맨 위에 반드시:

PHASE_2_ACTIVATION = FAILED

FAILED_STAGE =
FAILED_WAVE =
FAILED_SKILL =
FAILURE_TYPE =
FAILURE_REASON =

ROLLBACK_REQUIRED = YES / NO
ROLLBACK_ATTEMPTED = YES / NO
ROLLBACK_RESULT = SUCCESS / FAILED / PARTIAL / NOT_REQUIRED

LAST_SAFE_STATE =

NEXT_STEP =

를 출력해라.

FAILED_STAGE는 아래 값 중 하나를 사용:

POST_CHECK
WAVE_1_PREFLIGHT
WAVE_1_APPLY
WAVE_1_VALIDATE
WAVE_2_PREFLIGHT
WAVE_2_APPLY
WAVE_2_VALIDATE
WAVE_3_PREFLIGHT
WAVE_3_APPLY
WAVE_3_VALIDATE
WAVE_4_PREFLIGHT
WAVE_4_APPLY
WAVE_4_VALIDATE
PHASE_2_FINAL_VALIDATE

FAILURE_TYPE은 가능한 경우 아래 중 선택:

NOT_FOUND
AMBIGUOUS
COMPATIBILITY_BLOCKED
COMPATIBILITY_CRITICAL
PLAN_INTEGRITY_FAIL
MANIFEST_MISMATCH
SOURCE_CHANGED
UNEXPECTED_WRITE
ROLLBACK_NOT_READY
LEGACY_RUNTIME_DEPENDENCY
INVALID_TARGET
APPLY_FAIL
VALIDATION_FAIL
CROSS_SKILL_FAIL
SKILLSILENT_FAIL
UPDATER_COMPAT_FAIL
IDEMPOTENCY_FAIL
KNOWLEDGE_MIGRATION_MIXED
ROLLBACK_FAIL
OTHER

실패한 증거도 반드시 출력:

EVIDENCE:
- file:
- path:
- field:
- expected:
- actual:

확실하지 않은 결과를 PASS로 추정하지 마.

==================================================
3. POST_CHECK
==================================================

먼저 job-list v0.3.0 Plan 결과를 다시 검증해라.

필수:

V0_3_EXECUTION = PASS
RUN_MODE = PLAN
PHASE_2_COMPATIBILITY = PASS
PLAN_RESULT = GO
PLAN_INTEGRITY_VERIFIED = YES
ROLLBACK_READY = YES

가능하면 모든 Activation 대상 Skill에서:

activation_readiness = READY
manifest_match = true
blocking_reasons = []
source_changed = false
write_performed = false
activation_performed = false

를 확인해라.

schema의 필드명이 다르면
동일 의미의 필드와 실제 파일 상태로 판정해라.

특히 plan 단계에서:

- SKILL.md 변경
- runtime control 변경
- source 변경
- Activation 수행

이 발생하지 않았는지 확인해라.

다음 경로가 존재한다는 사실만으로 blocker 처리하지 말고,
실제 runtime dependency인지 구분해라:

~/.claude/main/<skill>
.claude/main/<skill>
~/l1sw-skills/private/<skill>
~/l1sw-skills/private/skills/<skill>

용도 구분:

runtime
rollback-reference
document
test-fixture
comment
unknown

runtime dependency로 남아 있고 Activation 후에도 OLD가 필요하면 BLOCKED.

POST_CHECK 결과가 PASS가 아니면 즉시 종료.

성공 시 기록:

STAGE_RESULT.POST_CHECK = PASS

==================================================
4. Activation Plan / Wave 정의 고정
==================================================

가장 최근 검증된 activation plan에서:

PLAN_FILE =
PLAN_SHA256 =
PLAN_RUN_ID =

ACTIVATION_TARGETS =
EXCLUDED_TARGETS =

WAVE_1 =
WAVE_2 =
WAVE_3 =
WAVE_4 =

를 읽어라.

Wave가 4개보다 적다면 존재하는 Wave만 사용하되
임의로 Wave를 새로 만들지 마.

Wave가 4개보다 많거나 plan 구조가 예상과 다르면
plan의 실제 Wave 정의를 보존하면서
각 Wave 번호를 정확히 출력해라.

아래 Skill이 Activation target/Wave에 들어 있으면 실패:

job-list
skill-updater
skillsilent
autotask-builder

Failure:

FAILED_STAGE = POST_CHECK
FAILURE_TYPE = INVALID_TARGET

==================================================
5. 각 Wave 공통 PREFLIGHT
==================================================

각 Wave N 시작 전에 반드시 다음을 수행해라.

예:
WAVE_1_PREFLIGHT
WAVE_2_PREFLIGHT
...

Wave N 대상 Skill에 대해 각각:

1. ENTRY 존재

~/.claude/skills/<skill>/SKILL.md

2. OLD rollback source 존재

~/.claude/main/<skill>/

3. NEW implementation 존재

~/l1sw-skills/private-skills/<skill>/

4. compatibility READY

5. manifest match

6. blocking reason 없음

7. plan 생성 이후 OLD source의 예상치 않은 변경 없음

8. plan 생성 이후 NEW implementation의 예상치 않은 변경 없음

9. PLAN_SHA256 현재 plan과 일치

10. rollback metadata 존재/생성 가능

11. plan에 정의되지 않은 파일 수정 필요 없음

12. Knowledge migration이 포함되지 않음

13. skillsilent v0.2.36으로 실행 가능

14. skill-updater v0.5.11 자체 변경 불필요

15. 이전 Wave가 있다면 이전 Wave validation = PASS

하나라도 실패하면 해당:

FAILED_STAGE = WAVE_N_PREFLIGHT

로 중단한다.

==================================================
6. 각 Wave 공통 Rollback 준비
==================================================

실제 APPLY 전에 Wave N의 각 Skill별 rollback metadata를 확인하거나 생성해라.

최소:

skill
wave
plan_file
plan_sha256
entry/control path
pre-activation SHA256
old_runtime
new_runtime
expected activation change
rollback operation
timestamp

원칙:

OLD runtime tree 자체는 이동/삭제하지 않는다.

rollback metadata를 만들 수 없으면:

FAILURE_TYPE = ROLLBACK_NOT_READY

로 중단한다.

==================================================
7. 각 Wave 공통 APPLY
==================================================

각 Wave에서 job-list v0.3.0이 실제로 제공하는
deterministic activation apply mechanism만 사용해라.

중요:

CLI/action 이름이나 인자를 추정해서 만들지 마.

필요하면 먼저:

- job-list SKILL.md
- job_list.py --help
- v0.3.0 activation plan
- action schema/config

를 읽어서 실제 지원되는 apply 호출법을 확인해라.

반드시 고정:

PLAN_SHA256 = 현재 검증된 값
WAVE = 현재 Wave 번호
TARGETS = plan의 해당 Wave 대상만

허용:

- plan에 정의된 entry/runtime routing 변경
- plan에 정의된 deterministic control metadata 변경

금지:

- source code 의미 변경
- Python 리팩토링
- 새로운 fallback 로직 임의 추가
- plan에 없는 config 변경
- plan에 없는 Skill 추가
- 현재 Wave 밖 Skill 변경

각 Skill 적용 직후 확인:

- expected file write 성공
- post-write SHA 확인
- NEW runtime routing 활성화
- OLD runtime 존재
- NEW implementation tree 보존
- source delete 없음
- source move 없음
- plan 밖 파일 변경 없음

실패하면 즉시 현재 Wave를 중단한다.

==================================================
8. APPLY 실패 시 rollback 규칙
==================================================

APPLY 중 실패한 경우:

A. v0.3.0 plan이 Wave atomic transaction을 정의한 경우:

현재 Wave 전체 rollback.

B. per-skill staged transaction을 정의한 경우:

실패 Skill은 반드시 rollback.

이미 성공한 같은 Wave의 앞선 Skill은
plan이 명시한 rollback policy를 따른다.

정책이 불명확하면 안전 우선으로:

- 더 이상 다음 Skill 진행하지 않음
- 이미 성공한 Skill 상태를 변경하지 않고 고정
- 실패 Skill rollback
- PARTIAL 상태를 명시
- 사용자 검토 대상으로 종료

임의로 전체 rollback 정책을 만들어 적용하지 마.

rollback 후 반드시 확인:

- entry/control pre-activation SHA 복구 여부
- OLD runtime 존재
- NEW implementation tree 손상 없음

rollback 실패 시:

FAILURE_TYPE = ROLLBACK_FAIL
ROLLBACK_RESULT = FAILED 또는 PARTIAL

다음 Wave 진행 금지.

==================================================
9. 각 Wave 공통 VALIDATE
==================================================

Wave N APPLY가 성공하면
즉시 Wave N validation을 수행해라.

각 Skill에서 가능한 범위 내 최소 검증:

1. direct invocation

2. help / self-check

3. read-only workflow

4. output path 확인

5. cross-skill invocation
   - 실제 dependency가 있는 경우

6. skillsilent v0.2.36 실행

가능한 기존 contract:

skillsilent run <skill> ...

실제 Skill contract를 확인해서 사용하고
명령을 추정하지 마.

7. updater 설치/재설치 후 runtime route 유지 여부
   - updater 자체를 수정하지 않음
   - 불필요한 updater write를 유발하지 않음
   - 현재 운영 환경에서 안전하게 검증 가능한 경우만 실행

8. 동일 명령 재실행 / idempotency

9. OLD runtime은 rollback source로 계속 존재

10. 실행 시 NEW implementation이 실제 사용되는지

11. 예상 output/data path 유지

12. legacy OLD runtime이 실제 실행 root로 다시 선택되지 않는지

validation에서 write workflow가 불필요하면
read-only test를 우선한다.

한 Skill이라도 validation 실패하면:

FAILED_STAGE = WAVE_N_VALIDATE
FAILED_SKILL = <skill>
FAILURE_TYPE = VALIDATION_FAIL 또는 세부 유형

다음 Wave 진행 금지.

validation 실패 시 rollback 여부:

- Activation 자체가 원인으로 명확하고
- rollback procedure가 검증되어 있으면
  해당 Skill/Wave를 plan rollback policy에 따라 rollback.

원인이 외부 시스템/일시 장애 등으로 Activation 문제인지 불명확하면
무리하게 rollback하지 말고:

ROLLBACK_REQUIRED = REVIEW

에 준하는 의미를 FAILURE_REASON에 기록하고,
ROLLBACK_ATTEMPTED = NO

로 종료할 수 있다.

단 최종 enum 출력이 YES/NO만 허용되면:
ROLLBACK_REQUIRED = NO
그리고 FAILURE_REASON에
"activation-caused failure not proven; manual review required"
를 명시해라.

==================================================
10. Wave 진행 규칙
==================================================

반드시:

POST_CHECK PASS
→ Wave 1

WAVE_1_PREFLIGHT PASS
→ WAVE_1_APPLY

WAVE_1_APPLY PASS
→ WAVE_1_VALIDATE

WAVE_1_VALIDATE PASS
→ Wave 2

동일 방식으로 Wave 4까지 진행.

이전 단계가 PASS가 아니면
다음 단계로 절대 넘어가지 마.

각 단계 성공 시 누적 기록:

STAGE_RESULT:
POST_CHECK = PASS
WAVE_1_PREFLIGHT = PASS
WAVE_1_APPLY = PASS
WAVE_1_VALIDATE = PASS
...

==================================================
11. slte-knowledge-manager 특별 Gate
==================================================

slte-knowledge-manager가 어느 Wave에 포함되어 있든
Skill implementation Activation만 허용한다.

허용 대상:

~/l1sw-skills/private-skills/slte-knowledge-manager/

이번 Phase에서 금지:

~/l1sw-knowledge/

Knowledge Store migration.

또한 기존 Knowledge Store 위치를
Skill Activation과 동시에 강제로 변경하지 마.

Skill implementation Activation과
Knowledge migration이 하나의 operation에 섞여 있으면:

FAILURE_TYPE = KNOWLEDGE_MIGRATION_MIXED

즉시 중단.

==================================================
12. PHASE_2_FINAL_VALIDATE
==================================================

모든 Wave validation이 PASS한 경우에만 실행.

전체 Activation 대상 Skill에 대해 다시 확인:

1. Skill entry는 계속:

~/.claude/skills/<skill>/SKILL.md

2. 실제 implementation runtime은:

~/l1sw-skills/private-skills/<skill>/

3. OLD:

~/.claude/main/<skill>/

는 rollback source로 존재.

4. OLD runtime 삭제/이동 없음

5. source tree 손상 없음

6. Wave별 rollback metadata 존재

7. 모든 Wave validation PASS

8. cross-skill dependency 정상

9. skillsilent v0.2.36 contract 정상

10. skill-updater v0.5.11 자체 변경 없음

11. job-list self-change 없음

12. autotask-builder 변경 없음

13. Knowledge migration 없음

14. activation plan 밖 예상하지 않은 변경 없음

15. 전체 idempotency 이상 없음

가능하면 activation 전후
entry/control file의 SHA와 runtime target을
표로 정리해라.

하나라도 실패하면:

FAILED_STAGE = PHASE_2_FINAL_VALIDATE

로 종료.

==================================================
13. Phase 2 성공 판정
==================================================

모든 단계 PASS일 때만:

PHASE_2_ACTIVATION = PASS
PHASE_2_STATUS = COMPLETE

를 출력한다.

중요:

Phase 2 COMPLETE는
Knowledge Migration 완료를 뜻하지 않는다.

다음 Phase는 별도:

PHASE_3 = KNOWLEDGE_MIGRATION

이지만 이번 요청에서는 Phase 3를 실행하지 않는다.

==================================================
14. 성공 시 최종 출력 형식
==================================================

모두 성공하면 아래 형식으로 출력:

PHASE_2_ACTIVATION = PASS
PHASE_2_STATUS = COMPLETE

PLAN_FILE =
PLAN_SHA256 =
PLAN_RUN_ID =

STAGE_RESULT:
- POST_CHECK = PASS
- WAVE_1_PREFLIGHT = PASS
- WAVE_1_APPLY = PASS
- WAVE_1_VALIDATE = PASS
- WAVE_2_PREFLIGHT = PASS
- WAVE_2_APPLY = PASS
- WAVE_2_VALIDATE = PASS
- WAVE_3_PREFLIGHT = PASS
- WAVE_3_APPLY = PASS
- WAVE_3_VALIDATE = PASS
- WAVE_4_PREFLIGHT = PASS
- WAVE_4_APPLY = PASS
- WAVE_4_VALIDATE = PASS
- PHASE_2_FINAL_VALIDATE = PASS

ACTIVATED_SKILLS:
- skill
  - wave:
  - entry:
  - new_runtime:
  - old_rollback_source:
  - validation: PASS

ROLLBACK_READY = YES

OLD_RUNTIME_PRESERVED = YES
NEW_RUNTIME_ACTIVE = YES
SKILL_ENTRY_LOCATION_PRESERVED = YES

SKILLSILENT_VERSION = 0.2.36
SKILLSILENT_COMPATIBILITY = PASS

SKILL_UPDATER_VERSION = 0.5.11
SKILL_UPDATER_CHANGED = NO

KNOWLEDGE_MIGRATION_PERFORMED = NO

UNEXPECTED_CHANGES = NO

FINAL = PHASE_2_COMPLETE

NEXT_PHASE = PHASE_3_KNOWLEDGE_MIGRATION
NEXT_PHASE_EXECUTED = NO

==================================================
15. 실패 시 최종 출력 형식
==================================================

실패하면 설명보다 아래를 먼저 출력:

PHASE_2_ACTIVATION = FAILED

FAILED_STAGE =
FAILED_WAVE =
FAILED_SKILL =
FAILURE_TYPE =
FAILURE_REASON =

STAGE_RESULT:
- POST_CHECK =
- WAVE_1_PREFLIGHT =
- WAVE_1_APPLY =
- WAVE_1_VALIDATE =
- WAVE_2_PREFLIGHT =
- WAVE_2_APPLY =
- WAVE_2_VALIDATE =
- WAVE_3_PREFLIGHT =
- WAVE_3_APPLY =
- WAVE_3_VALIDATE =
- WAVE_4_PREFLIGHT =
- WAVE_4_APPLY =
- WAVE_4_VALIDATE =
- PHASE_2_FINAL_VALIDATE =

ROLLBACK_REQUIRED = YES / NO
ROLLBACK_ATTEMPTED = YES / NO
ROLLBACK_RESULT = SUCCESS / FAILED / PARTIAL / NOT_REQUIRED

LAST_SAFE_STATE =

EVIDENCE:
- file:
- path:
- field:
- expected:
- actual:

BLOCKERS:
1.
2.
3.

FINAL = PHASE_2_STOPPED

NEXT_STEP =
- 실패 원인 수정
- 필요한 경우 해당 Wave 재검증
- Phase 3 진행 금지

==================================================
16. 최우선 안전 원칙
==================================================

1. Gate PASS 없이는 다음 단계 금지.

2. plan SHA가 다르면 APPLY 금지.

3. Wave N validation PASS 없이는 Wave N+1 금지.

4. OLD runtime은 Phase 2 전체 동안 rollback source로 유지.

5. plan에 없는 파일/Skill을 AI 판단으로 수정하지 않음.

6. job-list / skill-updater / skillsilent / autotask-builder는
   Activation target에서 제외.

7. Knowledge migration은 Phase 3로 분리.

8. 실패 시 가장 중요한 출력은
   "어느 단계에서 실패했는가"이다.

9. 단계 결과가 불명확하면 PASS가 아니라 중단.

10. 모든 Wave가 성공해도 Phase 3는 자동 실행하지 않는다.
```

---

# 실패 위치 해석 예시

예를 들어 Wave 2의 `code-analyzer`를 활성화한 뒤
self-check에서 실패하면 다음처럼 반환해야 한다.

```text
PHASE_2_ACTIVATION = FAILED

FAILED_STAGE = WAVE_2_VALIDATE
FAILED_WAVE = 2
FAILED_SKILL = code-analyzer
FAILURE_TYPE = VALIDATION_FAIL

LAST_SAFE_STATE = WAVE_1_VALIDATE_PASS

ROLLBACK_REQUIRED = YES
ROLLBACK_ATTEMPTED = YES
ROLLBACK_RESULT = SUCCESS

FINAL = PHASE_2_STOPPED
```

즉 Wave 3/4는 수행하지 않는다.

---

# 전체 성공 시 의미

최종:

```text
FINAL = PHASE_2_COMPLETE
NEXT_PHASE = PHASE_3_KNOWLEDGE_MIGRATION
NEXT_PHASE_EXECUTED = NO
```

가 나오면 Skill implementation Activation Phase가 종료된 것이다.

그 다음에 별도 Phase 3 프롬프트로 Knowledge Migration을 시작한다.

---

# 단계 요약

```text
POST_CHECK
   ↓ PASS
WAVE 1 PREFLIGHT
   ↓
WAVE 1 APPLY
   ↓
WAVE 1 VALIDATE
   ↓ PASS
WAVE 2 PREFLIGHT
   ↓
WAVE 2 APPLY
   ↓
WAVE 2 VALIDATE
   ↓ PASS
WAVE 3 PREFLIGHT
   ↓
WAVE 3 APPLY
   ↓
WAVE 3 VALIDATE
   ↓ PASS
WAVE 4 PREFLIGHT
   ↓
WAVE 4 APPLY
   ↓
WAVE 4 VALIDATE
   ↓ PASS
PHASE 2 FINAL VALIDATE
   ↓ PASS
PHASE_2_COMPLETE

어느 위치에서든 FAIL
   ↓
STOP
   ↓
FAILED_STAGE 반환
   ↓
필요시 rollback
   ↓
Phase 3 진행 금지
```
