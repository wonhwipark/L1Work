# Private Skill / Knowledge Final Close — Integrated Master Workflow
## 기준일: 2026-08-12

> 목적: Storage/SSOT Refactor 이후 Final Validate → Reconcile → Private Hub/Knowledge Reproducibility까지 하나의 흐름으로 통합 처리한다.
> PASS는 자동 연속 진행하고, FAIL/CONFLICT/Git write/파괴적 변경에서만 멈춘다.

---

# 0. 현재 상태

```text
STORAGE_SSOT_REFACTOR=COMPLETE
ACTIVE_PRIVATE_SKILLS=12
RETIRED_SKILLS=2

RETIRED_SKILLS:
- issue-fix-implement v0.3.1
- slte-port-impact-analyzer v0.8.23

RETIRED_SKILL_STORAGE_REFACTOR=NO
RETIRED_SKILL_REPUBLISH=NO
RETIRED_SKILL_INSTALL_VALIDATE=NO
RETIRED_SKILL_AUTO_DELETE=NO
```

최신 Active-12:

```text
1. code-analyzer            v0.13.20
2. code-fix                 v0.4.6
3. doc-converter            v0.2.1
4. hld-code-compare         v0.10.5
5. hld-code-implement       v0.5.10
6. hld-composer             v0.4.14
7. issue-analyzer           v0.11.6
8. l1_fla                   v0.2.1
9. l1-sam-fixer             v0.2.19
10. p4-code-owner           v0.6.1
11. p4-fix-kb               v0.2.3
12. slte-knowledge-manager  v0.4.8
```

---

# 1. Canonical Storage Contract

```text
PACKAGE_ROOT=~/.claude/skills/<skill>/
IMPLEMENTATION_ROOT=~/l1sw-skills/private-skills/<skill>/
SKILL_PERSISTENT_ROOT=~/l1sw-data/<skill>/    # 실제 필요한 Skill만
SHARED_KNOWLEDGE_ROOT=~/l1sw-knowledge/
BRANCH_OUTPUT_ROOT=<branch>/output/<skill>/

MAIN_AS_ACTIVE_STORE=NO
MAIN_AS_FALLBACK=NO
MAIN_NEW_WRITE=NO
LEGACY_READ_ONLY=YES
LEGACY_AUTO_DELETE=NO
LEGACY_AUTO_OVERWRITE=NO
```

Shared Knowledge:

```text
승인 전  : ~/l1sw-knowledge/candidates/
승인 후  : ~/l1sw-knowledge/current/
검색 파생: ~/l1sw-knowledge/indexes/
```

---

# 2. 통합 실행 원칙

```text
PASS     → 다음 Phase 자동 진행
FAIL     → 즉시 STOP + 실패 단계/검사/원인/복구법 출력
CONFLICT → 즉시 STOP + 자동 overwrite 금지
```

사용자 확인 없이 가능한 동작:

```text
read-only inventory
version/hash validation
contract validation
self-check/UT
legacy read-only scan
missing-only reconcile
index rebuild
read-only smoke
isolated canary
isolated restore test
local package/checksum 생성
```

사용자 확인이 필요한 동작:

```text
1. 사내 Git 실제 write/push/publish
2. Naming 변경
3. Group/Common Promote
4. Legacy 삭제
5. Retired Skill 실제 삭제
6. conflict overwrite/merge
```

---

# 3. Master Flow

```text
PHASE 0  PREFLIGHT
    ↓
PHASE 1  INSTALL / VERSION ALIGN
    ↓
PHASE 2  ACTIVE-12 FINAL_VALIDATE_V2
    ↓
PHASE 3  LOCAL RECONCILE / ADOPTION WAVE
    ↓
PHASE 4  KNOWLEDGE RECALL / RECONCILE CLOSE
    ↓
PHASE 5  PRIVATE HUB LOCAL REPACKAGE / PRECHECK
    ↓
USER GATE A: PRIVATE HUB GIT PUBLISH?
    ↓ YES
PHASE 6  PRIVATE HUB PUBLISH / REMOTE VERIFY
    ↓
PHASE 7  ISSUE-ANALYZER INSTALLER CANARY
    ↓
PHASE 8  ACTIVE-12 FULL INSTALL VALIDATE
    ↓
PHASE 9  PRIVATE HUB REPRODUCIBILITY CLOSE
    ↓
PHASE 10 PRIVATE KNOWLEDGE PUBLISH PRECHECK
    ↓
USER GATE B: PRIVATE KNOWLEDGE GIT PUBLISH?
    ↓ YES
PHASE 11 PRIVATE KNOWLEDGE PUBLISH / REMOTE VERIFY
    ↓
PHASE 12 PRIVATE KNOWLEDGE RESTORE CANARY
    ↓
PHASE 13 PRIVATE KNOWLEDGE REPRODUCIBILITY CLOSE
    ↓
PHASE 14 NAMING AUDIT
    ↓
PHASE 15 RETIRED-2 REFERENCE AUDIT
    ↓
USER GATE C: NAMING / PROMOTE / RETIRE / CLEANUP
    ↓
PHASE 16 STEADY STATE
```

---

# 4. PHASE 0 — PREFLIGHT

자동 확인:

```text
OS / HOME
Python availability
Git availability
skillsilent availability
package roots
implementation roots
persistent roots
knowledge root
branch root
repository roots
write permission
symlink/reparse/path escape
```

절대 조건:

```text
INTERNAL_GIT_USE_SKILL_UPDATER=NO
GROUP_COMMON=NO_TOUCH
UNLISTED_SKILL=NO_TOUCH
LEGACY_DELETE=NO
LEGACY_MODIFY=NO
```

---

# 5. PHASE 1 — INSTALL / VERSION ALIGN

Remaining-4 최신 버전:

```text
hld-composer v0.4.14
doc-converter v0.2.1
p4-code-owner v0.6.1
p4-fix-kb v0.2.3
```

각 Skill 확인:

```text
~/.claude/skills/<skill>/VERSION
SKILL.md version
~/l1sw-skills/private-skills/<skill>/ implementation marker
```

설치 직후 legacy source 삭제 금지.

PASS:

```text
ACTIVE12_VERSION_ALIGN=PASS
```

---

# 6. PHASE 2 — ACTIVE-12 FINAL_VALIDATE_V2

Active-12만 Full Validate 한다.
Retired-2는 dependency/reference read-only audit만 한다.

Active-12 검사:

```text
VERSION
SKILL.md
skillsilent manifest
skillsilent contract
package hash
implementation route
implementation marker
write roots
persistent root
branch output root
main active/fallback absence
dependency references
self-check / UT
```

필수 Storage Gate:

```text
PACKAGE_ROOT=~/.claude/skills/<skill>/
IMPLEMENTATION_ROOT=~/l1sw-skills/private-skills/<skill>/
MAIN_ACTIVE_STORE=NO
MAIN_FALLBACK=NO
MAIN_NEW_WRITE=NO
LEGACY_ACTIVE_WRITE=NO
PATH_ESCAPE=0
SYMLINK_ESCAPE=0
```

PASS:

```text
PRIVATE14_STORAGE_REFACTOR=PASS
ACTIVE12_FINAL_VALIDATE_V2=PASS
RETIRED2_READ_ONLY_AUDIT=PASS
```

FAIL이면 Phase 3 금지.

---

# 7. PHASE 3 — LOCAL RECONCILE / ADOPTION WAVE

권장 순서:

```text
1. slte-knowledge-manager  v0.4.8
2. issue-analyzer          v0.11.6
3. code-analyzer           v0.13.20
4. l1-sam-fixer            v0.2.19
5. l1_fla                  v0.2.1
6. hld-code-compare        v0.10.5
7. hld-code-implement      v0.5.10
8. code-fix                v0.4.6
9. hld-composer            v0.4.14
10. doc-converter          v0.2.1
11. p4-code-owner          v0.6.1
12. p4-fix-kb              v0.2.3
```

원칙:

```text
설치 버전과 reconcile 문서 버전 일치
legacy read-only
missing-only adoption
conflict fail-closed
automatic overwrite NO
original delete NO
original modify NO
```

한 Skill FAIL 시:

```text
STOP
다른 Skill production store 자동 수정 금지
```

전체 PASS:

```text
ACTIVE12_LOCAL_RECONCILE=PASS
```

---

# 8. PHASE 4 — KNOWLEDGE RECALL / RECONCILE CLOSE

## 8.1 Knowledge 역할

`slte-knowledge-manager`가 학습하여 승인된 장기 L1 지식의 authoritative live SSOT:

```text
~/l1sw-knowledge/
```

대상 예:

```text
L1 Domain Knowledge
Procedure
Architecture
MSG
UT
Responsibility
approved branch-scoped Knowledge
approved CL-scoped Knowledge
rules
UT structure
indexes
catalogs
mappings
```

중요:

```text
Skill package != Knowledge data
Skill Git repo != Knowledge Git repo
```

## 8.2 Scope 보존

```text
COMMON < BRANCH < BRANCH + CL RANGE
BRANCH_SCOPE_PRESERVE=YES
CL_SCOPE_PRESERVE=YES
CL_SCOPE_GUESSED=NO
```

금지:

```text
branch 이름으로 임의 CL 추정
SLTE 문자열로 CL 추정
branch conflict 자동 병합
CL conflict 자동 병합
```

## 8.3 Close Gate

```text
CANONICAL_ROOT=~/l1sw-knowledge/
LEGACY_STORES_INVENTORIED=YES
LEGACY_BRANCH_STORES_SCANNED=YES
BRANCH_SCOPE_AUDIT=PASS
CL_SCOPE_AUDIT=PASS
BRANCH_SCOPE_LOSS=0
CL_SCOPE_GUESSED=0
UNRESOLVED_SCOPE_CONFLICTS=0
CANONICAL_MERGE=PASS
INDEX_REBUILD=PASS
VALIDATE=PASS
RECALL_EXISTING_KNOWLEDGE=PASS
STRICT_BRANCH_QUERY=PASS
STRICT_BRANCH_CL_QUERY=PASS
LEGACY_SOURCE_DELETED=NO
LEGACY_SOURCE_MODIFIED=NO
MAIN_WRITE=NO
```

PASS:

```text
KNOWLEDGE_STORE_RECALL_RECONCILE=PASS
```

---

# 9. PHASE 5 — PRIVATE HUB LOCAL REPACKAGE / PRECHECK

Repository:

```text
l1sw-private-skills/
├─ README.md
├─ registry.json
├─ skills/
├─ tools/
│  ├─ private-skill-installer/
│  └─ private-skill-publisher/
└─ manifests/
   ├─ repository-manifest.json
   └─ checksums.json
```

Active-12만 최신 패키징.
Retired-2는 republish/install/full validate 대상 제외.

Precheck:

```text
SECRET_SCAN=PASS
PACKAGE_SHA=PASS
MANIFEST_VERIFY=PASS
REGISTRY_VERIFY=PASS
ACTIVE_SKILLS=12
RETIRED_SKILLS_EXCLUDED=YES
SKILL_UPDATER_USED=NO
```

PASS 후 사용자에게 한 번만 질문:

```text
사내 l1sw-private-skills repository에 publish할까요?
1. YES — publish 후 자동 계속
2. NO — local package까지만 종료
```

---

# 10. PHASE 6 — PRIVATE HUB PUBLISH / REMOTE VERIFY

사용자 YES인 경우에만 Git write.

```text
private-skill-publisher 사용
skill-updater 사용 금지
credential URL 금지
PAT/password 저장 금지
Git Credential Manager 또는 SSH
API/HTTP 호출 최소화
```

Remote verify:

```text
registry
manifest
checksums
12 skill versions
package digests
managed_assets
```

PASS:

```text
PRIVATE_HUB_PUBLISH=PASS
REMOTE_VERIFY=PASS
```

---

# 11. PHASE 7 — INSTALLER CANARY

```text
CANARY_SKILL=issue-analyzer
EXPECTED_VERSION=0.11.6
```

Production 보호:

```text
~/.claude/skills/issue-analyzer/
~/l1sw-skills/private-skills/issue-analyzer/
~/l1sw-data/issue-analyzer/
~/l1sw-knowledge/
```

isolated target 검증:

```text
REGISTRY_LOAD
VERSION_VERIFY
CHECKSUM_VERIFY
INSTALLER_LIST
PACKAGE_INSTALL
PACKAGE_SHA_VERIFY
IMPLEMENTATION_SYNC
IMPLEMENTATION_SHA_VERIFY
EXECUTION_ROOT_CONTRACT
READ_ONLY_FUNCTIONAL_SMOKE
```

필수:

```text
PRODUCTION_PACKAGE_CHANGED=NO
PRODUCTION_RUNTIME_CHANGED=NO
PRODUCTION_PERSISTENT_CHANGED=NO
KNOWLEDGE_CHANGED=NO
SKILL_UPDATER_USED=NO
```

PASS:

```text
PRIVATE_HUB_INSTALLER_CANARY=PASS
READY_FOR_FULL_INSTALL_VALIDATE=YES
```

---

# 12. PHASE 8 — ACTIVE-12 FULL INSTALL VALIDATE

isolated clean root에서 Active-12 전체 재설치.

```text
REGISTRY_ENTRY
VERSION
CHECKSUM
PACKAGE_INSTALL
PACKAGE_SHA
MANAGED_ASSETS
RUNTIME_SHA
IMPLEMENTATION_MARKER
EXECUTION_ROOT
WRITE_ROOT_CONTRACT
READ_ONLY_SAFE_SMOKE
PERSISTENT_ROOT_EXPECTED
BRANCH_OUTPUT_ROOT_EXPECTED
MAIN_ACTIVE_STORE=NO
MAIN_FALLBACK=NO
LEGACY_WRITE=NO
```

PASS:

```text
PRIVATE_HUB_FULL_INSTALL_VALIDATE=PASS
FAILED=0
```

---

# 13. PHASE 9 — PRIVATE HUB REPRODUCIBILITY CLOSE

```text
PUBLISH_FROM_LOCAL=PASS
REMOTE_VERIFY=PASS
INSTALL_FROM_REMOTE=PASS
PACKAGE_SHA=PASS
RUNTIME_SHA=PASS
CANARY=PASS
FULL_INSTALL_VALIDATE=PASS
INTERNAL_GIT_USE_SKILL_UPDATER=NO
GROUP_COMMON=NO_TOUCH
```

최종:

```text
PRIVATE_HUB_REPRODUCIBILITY=PASS
PRIVATE_HUB_OPERATIONAL=YES
```

---

# 14. PHASE 10 — PRIVATE KNOWLEDGE PUBLISH PRECHECK

## 14.1 Repository 관계

```text
~/l1sw-knowledge/
= authoritative live Knowledge SSOT

l1sw-private-knowledge
= versioned backup / internal distribution / restore source
```

즉 Git repository 자체가 runtime SSOT가 아니다.

## 14.2 Publish 후보

포함 후보:

```text
current/
inventory/
indexes/
history/
evidence/
catalogs/
mappings/
responsibility*
manifest*
```

실제 파일 의미를 검사해 publish-safe한 것만 포함한다.

제외:

```text
candidates/
runs/
cache/
wiki_mcp/
providers/
migration/
migration-backup/
runtime/
output/
logs/
temp/
backup/
```

## 14.3 Secret / Local-data Gate

검색:

```text
password
PAT
token
api key
private key
credential
cookie
authorization header
machine-local auth
```

추가 확인:

```text
absolute machine-local path
user-specific temporary path
download cache
raw credential config
unapproved candidate knowledge
```

필수:

```text
KNOWLEDGE_RECONCILE_PASS=YES
SECRET_SCAN=PASS
UNAPPROVED_CANDIDATE_INCLUDED=NO
RUNTIME_DATA_INCLUDED=NO
MACHINE_LOCAL_AUTH_INCLUDED=NO
```

PASS 후 사용자에게 한 번 질문:

```text
사내 l1sw-private-knowledge repository에 승인 Knowledge snapshot을 publish할까요?
1. YES — publish 후 restore canary까지 자동 계속
2. NO — precheck 결과만 저장하고 종료
```

---

# 15. PHASE 11 — PRIVATE KNOWLEDGE PUBLISH / REMOTE VERIFY

사용자 YES인 경우:

```text
~/l1sw-knowledge/
→ publish-safe snapshot
→ l1sw-private-knowledge
```

주의:

```text
live Knowledge를 Git checkout으로 직접 덮어쓰지 않는다.
Git repo는 backup/distribution/restore source다.
```

Remote verify:

```text
manifest
checksums
approved knowledge
scope metadata
indexes/catalog metadata
excluded directories absence
secret absence
```

PASS:

```text
PRIVATE_KNOWLEDGE_PUBLISH=PASS
PRIVATE_KNOWLEDGE_REMOTE_VERIFY=PASS
```

---

# 16. PHASE 12 — PRIVATE KNOWLEDGE RESTORE CANARY

Production:

```text
~/l1sw-knowledge/
```

는 NO_TOUCH.

격리 root에 remote snapshot으로 복원.

검증:

```text
STORE_LOAD
KNOWN_QUERY
FILTER_QUERY
BRANCH_QUERY
BRANCH_CL_QUERY
RELOAD_QUERY
INDEX_LOAD
```

필수:

```text
PRODUCTION_KNOWLEDGE_CHANGED=NO
BRANCH_SCOPE_LOSS=0
CL_SCOPE_GUESSED=0
```

PASS:

```text
PRIVATE_KNOWLEDGE_RESTORE_CANARY=PASS
```

---

# 17. PHASE 13 — PRIVATE KNOWLEDGE REPRODUCIBILITY CLOSE

```text
LIVE_STORE_VALIDATE=PASS
PUBLISH_PRECHECK=PASS
PUBLISH=PASS
REMOTE_VERIFY=PASS
RESTORE_FROM_REMOTE=PASS
RESTORE_CANARY=PASS
KNOWN_QUERY=PASS
BRANCH_QUERY=PASS
BRANCH_CL_QUERY=PASS
RELOAD_QUERY=PASS
```

최종:

```text
PRIVATE_KNOWLEDGE_REPRODUCIBILITY=PASS
PRIVATE_KNOWLEDGE_OPERATIONAL=YES
```

---

# 18. PHASE 14 — NAMING AUDIT

자동 rename 금지. 검토만 수행:

```text
canonical skill name
folder name
SKILL.md name/id
VERSION
registry id
Git path
skillsilent identity
contract identity
dependency references
CLI aliases
output folder name
documentation
cross-skill references
```

현재 후보:

```text
l1_fla
l1_sam_fix / l1-sam-fixer
underscore / hyphen consistency
```

---

# 19. PHASE 15 — RETIRED-2 REFERENCE AUDIT

대상:

```text
issue-fix-implement v0.3.1
slte-port-impact-analyzer v0.8.23
```

READ ONLY 검사:

```text
dependency reference
cross-skill invocation
registry entry
manifest entry
documentation reference
job-list reference
installer reference
publisher reference
legacy persistent data
rollback need
```

실제 삭제 금지.

---

# 20. USER GATE C — 정책 결정

모든 reproducibility PASS 후에만 질문:

```text
1. Naming normalization 진행
2. Group/Common promote 후보 검토
3. Retired-2 실제 제거
4. Legacy cleanup
5. 모두 보류하고 Steady State 진입
```

기본 권장:

```text
5. 모두 보류하고 Steady State 진입
```

Cleanup 조건:

```text
Private Hub reproducibility PASS
Private Knowledge reproducibility PASS
Naming stable
rollback window elapsed
explicit user approval
```

---

# 21. PHASE 16 — STEADY STATE

## Skill 변경

```text
source 수정
→ UT/self-check
→ semantic version bump
→ validation
→ secret scan
→ private-skill-publisher
→ l1sw-private-skills
→ remote verify
```

## Skill 설치

```text
l1sw-private-skills
→ private-skill-installer
→ registry/checksum verify
→ install/update
→ implementation sync
→ skillsilent
→ smoke
```

사내:

```text
SKILL_UPDATER_USED=NO
```

## Shared Knowledge Learning

```text
source / HLD / code / UT / Wiki / issue evidence
        ↓
candidate knowledge
        ↓
~/l1sw-knowledge/candidates/
        ↓
validation / scope / conflict check
        ↓
approval
        ↓
~/l1sw-knowledge/current/
        ↓
index rebuild
        ↓
recall validation
```

승인된 Knowledge의 사내 Private repository 반영:

```text
~/l1sw-knowledge/                 [authoritative live SSOT]
        ↓
Knowledge publish precheck
        ↓
secret / candidate / runtime exclusion
        ↓
publish-safe snapshot
        ↓
l1sw-private-knowledge            [versioned backup/distribution/restore]
        ↓
remote verify
```

중요:

```text
Git에서 학습하는 것이 아니다.
slte-knowledge-manager의 live learning 결과가 먼저 canonical Knowledge가 된다.
Git repository는 backup/distribution/restore/version history 역할이다.
```

---

# 22. Machine-readable 결과 형식

PASS:

```text
RESULT=PASS
MODE=<phase>
CHECKS=<summary>
FAILED_CHECKS=0
NEXT_STEP=<next phase>
AUTO_CONTINUE=YES/NO
```

FAIL:

```text
RESULT=FAIL
MODE=<phase>
FAILED_CHECKS=<list>
BLOCK_REASON=<reason>
PRODUCTION_CHANGED=YES/NO
ROLLBACK_PERFORMED=YES/NO
NEXT_STEP=<repair/retry phase>
AUTO_CONTINUE=NO
```

CONFLICT:

```text
RESULT=BLOCKED
MODE=<phase>
CONFLICTS=<list>
AUTO_OVERWRITE=NO
USER_DECISION_REQUIRED=YES
```

---

# 23. 최종 완료 Gate

```text
ACTIVE12_FINAL_VALIDATE_V2=PASS
ACTIVE12_LOCAL_RECONCILE=PASS
KNOWLEDGE_STORE_RECALL_RECONCILE=PASS
PRIVATE_HUB_PUBLISH=PASS
PRIVATE_HUB_INSTALLER_CANARY=PASS
PRIVATE_HUB_FULL_INSTALL_VALIDATE=PASS
PRIVATE_HUB_REPRODUCIBILITY=PASS
PRIVATE_KNOWLEDGE_PUBLISH=PASS
PRIVATE_KNOWLEDGE_RESTORE_CANARY=PASS
PRIVATE_KNOWLEDGE_REPRODUCIBILITY=PASS
RETIRED2_REFERENCE_AUDIT=PASS
INTERNAL_GIT_USE_SKILL_UPDATER=NO
GROUP_COMMON_TOUCHED=NO
LEGACY_AUTO_DELETE=NO
```

최종:

```text
RESULT=PASS
MODE=PRIVATE_SKILL_KNOWLEDGE_FINAL_CLOSE
PRIVATE_HUB_OPERATIONAL=YES
PRIVATE_KNOWLEDGE_OPERATIONAL=YES
STEADY_STATE_READY=YES
```

---

# 24. 새 작업창에서 바로 실행할 프롬프트

```text
이 MD를 최신 Master Workflow로 사용해서 Private Skill / Knowledge Storage/SSOT 후속 작업을 통합 진행해줘.

운영 방식:
- PASS이면 다음 Phase로 자동 진행
- FAIL/CONFLICT이면 즉시 STOP하고 실패 Phase와 원인/복구법 출력
- Git write, Naming mutation, Group Promote, Legacy/Retired 삭제에서만 사용자 확인
- legacy source는 read-only
- missing-only reconcile
- conflict overwrite 금지
- ~/.claude/main 신규 active/fallback/write 금지
- Group/Common/Unlisted NO_TOUCH
- 사내 Git에서 skill-updater 사용 금지

현재 Storage/SSOT refactor는 완료 상태다.

Active-12 최신 버전:
1. code-analyzer v0.13.20
2. code-fix v0.4.6
3. doc-converter v0.2.1
4. hld-code-compare v0.10.5
5. hld-code-implement v0.5.10
6. hld-composer v0.4.14
7. issue-analyzer v0.11.6
8. l1_fla v0.2.1
9. l1-sam-fixer v0.2.19
10. p4-code-owner v0.6.1
11. p4-fix-kb v0.2.3
12. slte-knowledge-manager v0.4.8

Retired:
- issue-fix-implement v0.3.1
- slte-port-impact-analyzer v0.8.23

먼저 PHASE 0 PREFLIGHT부터 시작하고 가능한 단계는 자동으로 연속 수행해.
실제 사내 Git write가 필요한 시점에는 딱 한 번 선택지를 제시해.

Knowledge 정책:
- ~/l1sw-knowledge/ = authoritative live Knowledge SSOT
- l1sw-private-knowledge = versioned backup/distribution/restore source
- 승인되지 않은 candidates는 publish 금지
- runtime/cache/log/temp/migration/auth data publish 금지
- Restore Canary는 isolated root에서 수행하고 production Knowledge NO_TOUCH
- Branch/CL scope를 보존하고 CL을 추정하지 말 것
```
