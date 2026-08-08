# Private Skill Phase 2 Activation — 새 대화 Handoff

- 기준일: 2026-08-08 KST
- 목적: `job-list v0.2.1 compatibility-check` 이후, 새 대화에서 **Activation 설계 → 실행 여부 판단 → 안전한 전환**을 이어서 진행하기 위한 전달 문서
- 중요: 기존 `private_skill_knowledge_migration_handoff_0807.md`의 경로/보안/rollback 원칙을 그대로 계승한다.

## 0. 현재 확정 구조

### Claude Skill Entry
`SKILL.md` 위치는 유지한다.

```text
~/.claude/skills/<skill>/SKILL.md
```

### 개인 Skill implementation 목표 경로
```text
~/l1sw-skills/private-skills/<skill>/
```

사용하지 않는 과거 경로:
```text
~/l1sw-skills/private/<skill>/
~/l1sw-skills/private/skills/<skill>/
```

### Knowledge 목표 경로
```text
~/l1sw-knowledge/
```

Knowledge와 Skill implementation은 분리한다.

## 1. 현재 사내 실행 엔진 상태

```text
skill-updater v0.5.11
skillsilent v0.2.36
```

운영 규칙:
- 새벽 unattended 실행에서 `skill-updater` 자체는 update target에서 제외
- `skillsilent`도 update target에서 제외
- 따라서 두 구성은 새벽 실행의 고정 엔진으로 취급

`skillsilent v0.2.37` 개선본은 준비되어 있으나 현재 GitHub에 올리지 않고, 이번 Activation 흐름에서도 의존하지 않는다.

## 2. Job-list 현재 단계

```text
job-list v0.2.0
- Phase 2-A
- inventory
- COPY
- SHA256/file-count verify
- source unchanged
- FAILED_SAFE

job-list v0.2.1
- Phase 2-B
- compatibility-check
- READY / BLOCKED / CRITICAL 판정
- 실제 path 수정 없음
- Activation 없음
```

`job-list v0.2.0 / v0.2.1`은 현재 `skillsilent v0.2.36`의 기존 `job-list/run` contract를 유지하는 방향이다.

Migration 동작은 별도 `safe-skill-migration` Skill을 호출하지 않고 `job_list.py` 내부 built-in Python action으로 수행한다.

## 3. 새 대화 시작 시 가장 먼저 받을 입력

회사 Claude Code에서 수행한 `job-list v0.2.1 compatibility-check` 결과를 사용한다.

가능하면 다음 중 하나를 제공한다.

```text
~/.claude/main/job-list/output/compatibility_review.md
```

또는 가장 최근 report JSON:

```text
~/.claude/main/job-list/output/actions/migration_*_r*_<timestamp>.json
```

필요시:
```text
~/.claude/main/job-list/output/last_run.json
~/.claude/main/job-list/output/runs/<run_id>/summary.json
```

## 4. Activation 진행 Gate

### PASS
다음 조건을 만족해야 한다.

```text
PHASE_2_COMPATIBILITY = PASS
```

그리고 모든 Activation 대상 Skill에서:

```text
activation_readiness = READY
manifest_match = true
blocking_reasons = []
source_changed = false
write_performed = false
activation_performed = false
```

이면 Activation 설계 단계로 이동한다.

### BLOCKED
하나라도 `activation_readiness = BLOCKED`이거나 runtime legacy path가 남아 있으면 Activation을 진행하지 않는다.

대표 blocker:
```text
~/.claude/main/<skill>
.claude/main/<skill>
~/l1sw-skills/private/<skill>
~/l1sw-skills/private/skills/<skill>
```

이 경로가 Python/script/config의 runtime path로 사용되는 경우.

### CRITICAL
다음 중 하나라도 확인되면 즉시 중단한다.

```text
source_changed = true
write_performed = true
activation_performed = true
source delete/rename 흔적
```

판정:
```text
PHASE_2_COMPATIBILITY = CRITICAL
NEXT_STEP = STOP_AND_REVIEW
```

## 5. 새 대화의 1차 목표

Compatibility가 PASS인 경우에도 바로 Activation job을 실행하지 않는다.

먼저 **Activation 설계**를 확정한다.

목표:
```text
OLD runtime을 rollback source로 그대로 유지하면서
새 implementation root를 실제 runtime으로 전환하는 방법 설계
```

## 6. Activation 설계 시 반드시 확인할 것

각 Skill별로 아래를 확인한다.

```text
1. 현재 실제 실행 entrypoint
2. SKILL.md 내부 실행 경로
3. Python/script 내부 root resolver
4. config/data path
5. cross-skill 호출 경로
6. skillsilent contract
7. skill-updater target/manifest 경로
8. runtime output/data path
9. rollback 방법
```

특히 `~/.claude/skills/<skill>/SKILL.md` 위치는 유지하지만, SKILL.md 내부에 implementation script 경로가 hard-coded되어 있다면 Activation 시 새 root를 가리키도록 수정이 필요할 수 있다.

## 7. 권장 Activation 구조

```text
~/.claude/skills/<skill>/SKILL.md
        │
        │ discovery / entry
        ▼
~/l1sw-skills/private-skills/<skill>/
        │
        ├─ scripts/
        ├─ config/
        ├─ schemas/
        └─ implementation assets
```

OLD:
```text
~/.claude/main/<skill>/
```

은 즉시 삭제하지 않고 rollback source로 유지한다.

## 8. Root Resolver 권장 원칙

가능하면 각 Skill에서 절대 경로 hard-coding을 제거한다.

우선:
```python
Path(__file__).resolve()
```

기반 상대 경로를 사용하거나 공통 root resolver를 사용한다.

전환 기간에는 필요한 경우:
```text
NEW root
~/l1sw-skills/private-skills/<skill>/
        ↓ validation failure / unavailable
OLD root
~/.claude/main/<skill>/
```

fallback을 둘 수 있다.

## 9. Activation은 Skill별 staged rollout 권장

한 번에 모든 Skill을 활성화하지 않는다.

예시:
```text
Wave 1
- 단순/독립 Skill

Wave 2
- cross-skill dependency가 있는 Skill

Wave 3
- issue-analyzer / code-analyzer / code-fix 계열

Wave 4
- slte-knowledge-manager
- slte-port-impact-analyzer
```

실제 순서는 compatibility 결과와 dependency를 보고 확정한다.

## 10. Activation 시 검증 항목

각 Skill 전환 후 최소:

```text
1. direct invocation
2. help/self-check
3. read-only workflow
4. output path 확인
5. cross-skill invocation
6. skillsilent 실행
7. updater 설치 후 실행
8. 재실행/idempotency
```

문제가 있으면:
```text
NEW deactivate
→ OLD runtime 재활성화
```

로 rollback한다.

## 11. Job-list 다음 버전 방향

Activation 기능을 job-list에 추가한다면 `v0.3.0` 수준의 별도 버전으로 분리하는 것을 우선 검토한다.

```text
v0.2.x = PRE-STAGE / compatibility 검증
v0.3.x = 실제 runtime Activation
```

다만 `job-list v0.3.0`이 수행할 수 있는 것은 **이미 검증된 deterministic activation operation**으로 제한한다.

job-list가 AI로 Skill source를 임의 수정하면 안 된다.

## 12. Activation job Safety Gate

최소:

```text
compatibility result = PASS
manifest_match = true
source_changed = false
target verified
OLD source exists
rollback metadata created
```

위 조건이 하나라도 없으면 Activation 거부.

추가 금지:
```text
NO source delete
NO source move
NO cleanup
NO GitHub push
NO Skill rename
NO Knowledge migration 동시 수행
```

## 13. Knowledge migration은 별도 Phase로 유지

`slte-knowledge-manager`는 두 축을 분리한다.

```text
A. Skill implementation activation
   → ~/l1sw-skills/private-skills/slte-knowledge-manager/

B. Knowledge Store migration
   → ~/l1sw-knowledge/
```

두 작업을 동시에 수행하지 않는다.

Knowledge migration 시에는 가능하면:
```text
SLTE_KNOWLEDGE_HOME=~/l1sw-knowledge
```

override 기반 전환을 우선 검토한다.

## 14. Silent 관련 현재 정책

이번 Activation에서는:

```text
skillsilent v0.2.36
```

을 기준으로 한다.

`skillsilent v0.2.37` 개선본은 별도 보류한다.

Activation 설계가 새 Silent action/flag를 요구하지 않도록 한다.

가능하면 기존:
```text
skillsilent run <skill> run ...
```

contract를 유지하고, 세부 routing은 Skill 내부 Python에서 처리한다.

## 15. 새 대화에서 금지할 것

Compatibility 결과 확인 전에:
```text
Activation 실행 금지
```

또한:
```text
기존 ~/.claude/main 삭제 금지
기존 SKILL.md 이동 금지
Skill rename 금지
skillsilent 업데이트 금지
skill-updater 업데이트 금지
GitHub push 자동 수행 금지
Knowledge Store 동시 전환 금지
```

## 16. 새 대화 첫 요청문

아래 내용을 새 대화에 그대로 입력한다.

```text
첨부한 Phase 2 Activation Handoff를 현재 확정 기준으로 사용해줘.

회사 Claude Code에서 job-list v0.2.1 compatibility-check 결과를 확인했다.
먼저 내가 제공하는 compatibility_review.md 또는 migration report JSON을 분석해줘.

최우선 조건:
1. PHASE_2_COMPATIBILITY가 PASS인지 먼저 확인
2. BLOCKED/CRITICAL이 있으면 Activation 설계/실행을 진행하지 않음
3. Skill entry는 ~/.claude/skills/<skill>/SKILL.md에 유지
4. 새 Skill implementation root는 ~/l1sw-skills/private-skills/<skill>/
5. 기존 ~/.claude/main/<skill>/는 rollback source로 유지
6. MOVE/DELETE/CLEANUP 금지
7. 현재 skillsilent v0.2.36 기준으로 설계
8. skillsilent v0.2.37은 이번 흐름에서 사용하지 않음
9. skill-updater v0.5.11 자체도 이번 흐름에서 수정하지 않음
10. Knowledge migration은 Skill Activation과 분리

compatibility 결과가 PASS이면
먼저 Skill dependency와 path 구조를 분석해서
Activation wave와 rollback 전략을 설계해줘.

그 다음 job-list v0.3.0으로 deterministic Activation을 구현하는 것이 적절한지 판단해줘.

실제 Activation을 수행하기 전에 반드시 아래를 먼저 제시해줘:

- Activation 대상 Skill 목록
- Wave 순서
- Skill별 변경 파일/경로
- rollback 방법
- validation 항목
- 위험 요소
- GO / NO-GO 판정

BLOCKED Skill이 있으면
해당 Skill 수정이 먼저 필요한지 정확히 구분해줘.
```

## 17. 새 대화에서 기대하는 출력

Compatibility PASS인 경우:

```text
PHASE_2_COMPATIBILITY = PASS

ACTIVATION_DESIGN
- Wave 1:
- Wave 2:
- Wave 3:
- Wave 4:

ROLLBACK_READY = YES/NO

JOB_LIST_V0_3_0_RECOMMENDED = YES/NO

ACTIVATION_GO_NO_GO = GO / CONDITIONAL / NO-GO
```

BLOCKED인 경우:

```text
PHASE_2_COMPATIBILITY = BLOCKED

BLOCKED_SKILLS:
- ...

REQUIRED_FIX:
- ...

ACTIVATION_GO_NO_GO = NO-GO
```

CRITICAL이면:

```text
PHASE_2_COMPATIBILITY = CRITICAL
ACTIVATION_GO_NO_GO = NO-GO
NEXT_STEP = STOP_AND_REVIEW
```

## 18. 핵심 원칙

```text
Activation은 "새 경로가 존재한다"가 아니라
"새 경로가 검증되었고, 기존 runtime으로 즉시 rollback 가능하다"는
두 조건이 동시에 만족될 때만 수행한다.
```
