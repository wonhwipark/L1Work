# job-list v0.2.0 Remote Queue 복구/배포 프롬프트

## 목적

현재 사내 PC에서 `job-list v0.2.0` 설치는 완료되었으나,
`skill-updater`의 `job_sync` 단계에서 원격:

```text
main/automation/job-list.json
```

이 존재하지 않아 queue merge가 수행되지 않았고,
`job-list` runner도 호출되지 않았다.

이번 작업의 목표는:

```text
1. updater가 실제 참조하는 GitHub repository / main branch 확인
2. 현재 PC의 실제 Skill source inventory 확인
3. job-list v0.2.0의 Phase 2-A용 remote queue 작성
4. JSON/schema/path/safety 검증
5. 검증 성공 시에만 GitHub의 automation/job-list.json에 반영
6. 실제 updater/job-list 재실행은 하지 않음
```

이다.

---

# 0. 현재 확정 조건

현재:

```text
skill-updater = v0.5.11
job-list = v0.2.0
skillsilent = v0.2.36
```

이번 작업에서:

```text
skill-updater 수정 금지
job-list 수정/버전업 금지
skillsilent 수정/업데이트 금지
migration 실행 금지
job_sync 실행 금지
Activation 금지
기존 source 삭제/이동/rename 금지
```

한다.

이번 작업은 **remote queue를 안전하게 준비하는 작업**이다.

---

# 1. 목표 경로

## Skill Entry

유지:

```text
~/.claude/skills/<skill>/SKILL.md
```

이 위치는 migration 대상이 아니다.

## Skill implementation target

```text
~/l1sw-skills/private-skills/<skill>/
```

금지된 과거 target:

```text
~/l1sw-skills/private/<skill>/
~/l1sw-skills/private/skills/<skill>/
```

## Knowledge target

```text
~/l1sw-knowledge/
```

단, Skill implementation migration과 Knowledge migration을 같은 job으로 섞지 않는다.

이번 queue에서는 **Skill implementation pre-stage만 우선**한다.

---

# 2. STEP 1 — Updater가 참조하는 원격 위치 확인

`skill-updater v0.5.11`의 실제 config/manifest/source 정보를 읽어서 다음을 확인해.

```text
repository
branch/ref
automation path
job-list.json expected path
```

반드시 실제 updater 설정/코드 근거로 판단하고 추측하지 마.

기대되는 논리 위치:

```text
<updater-source-repository>
└─ main
   └─ automation/
      └─ job-list.json
```

실제 repository 또는 branch가 다르면 실제 값을 사용한다.

확인할 수 없으면 이후 작업을 중단한다.

판정 코드:

```text
STEP1 = 1  # PASS
STEP1 = 2  # FAIL
STEP1 = 9  # UNKNOWN
```

---

# 3. STEP 2 — 기존 remote queue 존재 여부 확인

GitHub remote에서 실제:

```text
automation/job-list.json
```

존재 여부를 확인해.

## 존재하지 않음

```text
REMOTE_QUEUE = MISSING
```

→ 신규 생성 후보.

## 존재함

내용을 읽고 다음을 확인:

```text
schema
현재 jobs
job id
revision
완료되지 않은 기존 one-shot job
```

기존 queue가 있으면 **무조건 overwrite하지 마.**

병합 가능 여부를 먼저 판단한다.

기존 job을 삭제하지 않는다.

판정:

```text
STEP2 = 1  # missing 또는 안전하게 merge 가능
STEP2 = 2  # 충돌/기존 queue 때문에 자동 진행 불가
STEP2 = 9  # 확인 불가
```

---

# 4. STEP 3 — 현재 PC source inventory

현재 설치된 개인 Skill의 실제 implementation/runtime source를 기계적으로 조사해.

우선 확인 후보:

```text
~/.claude/main/<skill>/
~/.claude/skills/<skill>/
```

하지만 source를 임의로 추정하지 마.

다음 기준으로 각 Skill을 분류해.

```text
SKILL.md만 있는 entry 위치
실제 scripts/config/implementation이 있는 위치
runtime/output/data만 있는 위치
```

`~/.claude/skills/<skill>/SKILL.md` 자체는 target으로 COPY하지 않는다.

migration 대상은 실제 implementation asset이다.

각 대상 Skill마다 최소:

```text
name
source
target
source_exists
source_kind
```

를 만든다.

target:

```text
~/l1sw-skills/private-skills/<skill>/
```

source가 불명확한 Skill은 migration job에 포함하지 마.

판정:

```text
STEP3 = 1  # 모든 포함 대상 source 확인
STEP3 = 2  # 일부 source 불명확
STEP3 = 3  # migration 대상 없음
STEP3 = 9  # inventory 실패
```

STEP3이 1이 아니면 GitHub 반영 금지.

---

# 5. STEP 4 — job-list v0.2.0 template 확인

현재 설치된 `job-list v0.2.0` package에서 Phase 2-A template을 찾아.

우선 후보:

```text
templates/job-list.private-skill-prestage.json
```

실제 template이 있으면 해당 schema를 그대로 기준으로 사용한다.

template이 없거나 schema가 불명확하면 임의 schema를 만들지 말고 중단한다.

판정:

```text
STEP4 = 1  # template/schema 확인
STEP4 = 2  # template/schema 없음
STEP4 = 9  # 확인 불가
```

---

# 6. STEP 5 — Remote queue 작성

STEP1~4가 모두 PASS인 경우에만 작성한다.

Job의 목적:

```text
Phase 2-A / PRE-STAGE
inventory
COPY
verify
report
STOP
```

허용 mode:

```text
copy-verify
```

금지:

```text
activation
delete
move
rename
cleanup
source write
GitHub push from migration job
Knowledge migration
Skill rename
```

가능하면 기존 template의 job id를 사용한다.

새 job id를 만들어야 한다면 명확하게:

```text
PRIVATE-SKILL-PRESTAGE
```

계열로 사용한다.

revision은 remote에 동일 job id가 없다면:

```text
revision = 1
```

기존 동일 id가 있으면 기존 revision을 읽고:

```text
revision = previous + 1
```

로 한다.

revision을 추측하지 마.

---

# 7. STEP 6 — Safety 검증

GitHub 반영 전에 반드시 아래를 모두 검사해.

## 필수

```text
JSON parse = PASS
schema/template compatibility = PASS
source exists = PASS
target root allowlist = PASS
duplicate job id/revision = NONE
DELETE/MOVE/RENAME = NONE
activation = false / absent
source-write = false / absent
```

## Target allowlist

Skill target은 반드시:

```text
~/l1sw-skills/private-skills/
```

하위여야 한다.

다른 target이면 즉시 FAIL.

## Source protection

queue에 source delete/rename/move/overwrite 의미가 있는 field가 있으면 FAIL.

---

# 8. STEP 7 — GitHub 반영

STEP1~6이 모두 PASS인 경우에만:

```text
automation/job-list.json
```

을 updater가 실제 참조하는 remote repository/branch에 반영한다.

기존 queue가 있다면 안전하게 병합하고,
기존 미완료 job을 임의 삭제하지 않는다.

반영 후 remote 파일을 다시 읽어서
작성한 내용과 동일한지 검증한다.

중요:

```text
GitHub queue 반영까지만 수행
skill-updater 재실행 금지
job_sync 재실행 금지
job-list runner 실행 금지
migration 실행 금지
```

즉 실제 migration은 다음 별도 단계에서 실행한다.

---

# 9. GitHub 반영 금지 조건

다음 중 하나라도 발생하면 commit/push/remote update를 하지 마.

```text
updater remote 위치 UNKNOWN
기존 queue 충돌
source path 불명확
template/schema 불명확
target allowlist 위반
duplicate revision
destructive operation 발견
unexpected Knowledge migration 포함
```

---

# 10. 최종 숫자 판정

첫 줄에는 반드시 숫자 하나만 출력한다.

```text
1 = SUCCESS
    remote automation/job-list.json 생성/병합 및 검증 완료
    실제 updater 재실행은 아직 하지 않음

2 = REMOTE_PATH_FAIL
    updater가 참조하는 repository/branch/path 확인 실패

3 = QUEUE_CONFLICT
    기존 automation/job-list.json과 안전하게 병합할 수 없음

4 = INVENTORY_FAIL
    실제 source path를 안전하게 확정하지 못함

5 = TEMPLATE_FAIL
    job-list v0.2.0 template/schema 확인 실패

6 = VALIDATION_FAIL
    JSON/schema/path/safety/revision 검증 실패

7 = GITHUB_WRITE_FAIL
    로컬 queue 작성/검증은 성공했으나 GitHub 반영 실패

8 = PARTIAL
    일부 단계만 성공하여 remote 반영하지 않음

9 = UNKNOWN
    객관적 판단에 필요한 정보 부족
```

---

# 11. 답변 형식

첫 줄:

```text
<1~9 숫자 하나>
```

그 아래는 최대 10줄만 출력:

```text
REMOTE_REPO=<value|UNKNOWN>
REMOTE_BRANCH=<value|UNKNOWN>
REMOTE_QUEUE=<CREATED|MERGED|EXISTS|MISSING|NOT_WRITTEN|UNKNOWN>
JOB_ID=<value|UNKNOWN>
REVISION=<number|UNKNOWN>
SKILL_COUNT=<number>
TEMPLATE=<PASS|FAIL|UNKNOWN>
VALIDATION=<PASS|FAIL|UNKNOWN>
GITHUB_WRITE=<PASS|FAIL|NOT_RUN>
NEXT_STEP=<RUN_UPDATER_POSTCHECK|STOP_AND_ANALYZE>
```

`1`일 때만:

```text
NEXT_STEP=RUN_UPDATER_POSTCHECK
```

그 외에는:

```text
NEXT_STEP=STOP_AND_ANALYZE
```

로 출력한다.

---

# 12. 중요한 실행 원칙

1. 추가 질문하지 않는다.
2. 현재 PC와 repository에서 확인 가능한 정보로 최대한 끝까지 수행한다.
3. 경로는 추측하지 않는다.
4. Python을 이용한 JSON/schema/path 검증을 우선한다.
5. 정상 source를 찾지 못한 Skill은 queue에 넣지 않는다.
6. 기존 remote job을 임의 삭제하지 않는다.
7. destructive operation은 절대 생성하지 않는다.
8. 이번 작업에서는 migration을 실제 수행하지 않는다.
9. updater/job-list 재실행은 하지 않는다.
10. `skillsilent v0.2.36`은 변경하지 않는다.
11. `skill-updater v0.5.11`도 변경하지 않는다.
12. 최종 답변은 숫자 판정을 최우선으로 한다.

---

# 13. 성공 후 다음 단계

결과가:

```text
1
```

이면 다음 단계는:

```text
skill-updater를 명시적으로 1회 실행
→ job_sync
→ job-list v0.2.0
→ Phase 2-A COPY+VERIFY
→ v0.2.0 Post-Check
```

이다.

Post-Check PASS 이후에만:

```text
job-list v0.2.1 compatibility-check
```

로 진행한다.
