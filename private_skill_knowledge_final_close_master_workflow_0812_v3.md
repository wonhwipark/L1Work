# Private Skill / Knowledge Final Close Master Workflow v3
## 기준일: 2026-08-12
## Mode: RESUME / DELTA FIRST
## 목적: 기존 v1 수행 결과를 재사용하고, 이후 추가된 변경사항만 안전하게 이어서 처리

> 이 문서는 기존 `private_skill_knowledge_final_close_master_workflow_0812.md`를 이미 수행한 환경을 기본 전제로 한다.
> **처음부터 전체를 재실행하지 않는다.**
>
> 핵심:
> - 기존 PASS 단계는 READ-ONLY 증빙 확인 후 `SKIP_ALREADY_PASS`
> - FAIL / BLOCKED / NOT_RUN / 증빙 없는 단계만 재수행
> - v1 이후 추가된 `skillsilent v0.2.39` 정합을 Delta Gate로 처리
> - `l1sw-private-knowledge` Repository 생성/검증 프롬프트를 본 문서에 내장
> - 실제 Git write / destructive action만 사용자 승인
> - 사내 Git에서는 `skill-updater` 사용 금지

---

# 0. 현재 기준 상태

## 0.1 Active Private Skills

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

## 0.2 Fixed Engine

```text
skillsilent v0.2.39
```

v1 수행 이후 최신 Storage/SSOT 정책에 맞게 갱신된 버전이다.

핵심 계약:

```text
~/.claude/main
→ active discovery NO
→ registration NO
→ execution NO
→ fallback NO
→ write NO
→ legacy read-only inventory only

~/.claude/skills/<skill>/
→ Package / Declaration

~/l1sw-skills/private-skills/<skill>/
→ Implementation

~/.skillsilent/
→ skillsilent registry / approval / audit state

~/l1sw-skills/
→ Group/Common automatic mutation NO
```

## 0.3 Retired

```text
issue-fix-implement v0.3.1
slte-port-impact-analyzer v0.8.23
```

정책:

```text
STORAGE_SSOT_REFACTOR=NO
REPUBLISH=NO
INSTALL_VALIDATE=NO
AUTO_DELETE=NO
REFERENCE_AUDIT_ONLY=YES
```

---

# 1. Canonical Storage / SSOT Contract

```text
PACKAGE_ROOT=~/.claude/skills/<skill>/
IMPLEMENTATION_ROOT=~/l1sw-skills/private-skills/<skill>/

SKILL_PERSISTENT_ROOT=~/l1sw-data/<skill>/
ONLY_IF_ACTUALLY_NEEDED=YES

SHARED_KNOWLEDGE_ROOT=~/l1sw-knowledge/
APPROVED_KNOWLEDGE_ROOT=~/l1sw-knowledge/current/
CANDIDATE_KNOWLEDGE_ROOT=~/l1sw-knowledge/candidates/
KNOWLEDGE_INDEX_ROOT=~/l1sw-knowledge/indexes/

BRANCH_OUTPUT_ROOT=<branch>/output/<skill>/

MAIN_AS_ACTIVE_STORE=NO
MAIN_AS_FALLBACK=NO
MAIN_NEW_WRITE=NO

LEGACY_READ_ONLY=YES
LEGACY_AUTO_DELETE=NO
LEGACY_AUTO_OVERWRITE=NO

GROUP_COMMON=NO_TOUCH
UNLISTED_SKILL=NO_TOUCH

INTERNAL_GIT_USE_SKILL_UPDATER=NO
```

---

# 2. v3 실행 방식 — Resume / Delta

## 2.1 절대 기본값

```text
RESUME_MODE=YES
FULL_REPLAY=NO
```

이전 Workflow의 PASS 결과를 무조건 재실행하지 않는다.

먼저 local evidence를 READ ONLY로 확인한다.

확인 가능한 evidence 예:

```text
VERSION
SKILL.md
manifest
validation result
reconcile result
package SHA
runtime SHA
Git commit / remote state
local report
machine-readable PASS marker
restore-canary result
```

## 2.2 상태 판정

각 Phase를 다음 중 하나로 판정한다.

```text
PASS
FAIL
NOT_RUN
BLOCKED
UNKNOWN
```

동작:

```text
PASS
→ SKIP_ALREADY_PASS
→ mutation NO
→ next

FAIL
→ repair 가능한 경우 해당 Phase만 재수행
→ 다음 Phase 자동 진행 금지

NOT_RUN
→ 수행

BLOCKED
→ block 원인 해결 후 해당 Phase resume

UNKNOWN
→ READ ONLY validation
→ PASS 입증 시 SKIP
→ 아니면 NOT_RUN 취급
```

## 2.3 금지

```text
PASS 단계의 reinstall 금지
PASS reconcile 재수행 금지
PASS Git publish 중복 금지
PASS canary 중복 수행 금지
legacy 자동 overwrite 금지
```

---

# 3. v3 Master Flow

```text
[START]
        ↓
R0. EXISTING V1 RESULT INVENTORY
        ↓
R1. SKILLSILENT v0.2.39 DELTA GATE
        ↓
R2. RESUME POINT DECISION
        ↓
A. Active-12 Final Validate V2       [기존 PASS면 SKIP]
        ↓
B. Active-12 Local Reconcile         [기존 PASS면 SKIP]
        ↓
C. Knowledge Recall/Reconcile Close  [기존 PASS면 SKIP]
        ↓
D. Private Hub Repackage/Publish     [기존 PASS면 SKIP]
        ↓
E. Installer Canary                  [기존 PASS면 SKIP]
        ↓
F. Full Install Validate             [기존 PASS면 SKIP]
        ↓
G. Private Hub Reproducibility       [기존 PASS면 SKIP]
        ↓
H. PRIVATE KNOWLEDGE REPOSITORY INITIALIZE / VERIFY
        ↓
I. Private Knowledge Publish Precheck
        ↓
USER GATE: 실제 Knowledge Git publish?
        ↓ YES
J. Private Knowledge Publish / Remote Verify
        ↓
K. Private Knowledge Restore Canary
        ↓
L. Private Knowledge Reproducibility Close
        ↓
M. Naming Audit
        ↓
N. Retired-2 Reference Audit
        ↓
USER POLICY GATE
        ↓
O. Steady State
```

---

# 4. R0 — 기존 v1 수행 결과 Inventory

먼저 기존 Final Workflow의 수행 흔적을 READ ONLY로 찾는다.

목표:

```text
V1_RESULT_INVENTORIED=YES
```

아래 항목별 상태를 만든다.

```text
ACTIVE12_FINAL_VALIDATE_V2
ACTIVE12_LOCAL_RECONCILE
KNOWLEDGE_STORE_RECALL_RECONCILE

PRIVATE_HUB_PUBLISH
PRIVATE_HUB_INSTALLER_CANARY
PRIVATE_HUB_FULL_INSTALL_VALIDATE
PRIVATE_HUB_REPRODUCIBILITY

PRIVATE_KNOWLEDGE_REPOSITORY_READY
PRIVATE_KNOWLEDGE_PUBLISH_PRECHECK
PRIVATE_KNOWLEDGE_PUBLISH
PRIVATE_KNOWLEDGE_RESTORE_CANARY
PRIVATE_KNOWLEDGE_REPRODUCIBILITY

NAMING_AUDIT
RETIRED2_REFERENCE_AUDIT
```

출력:

```text
MODE=RESUME_INVENTORY

<phase>=PASS/FAIL/NOT_RUN/BLOCKED/UNKNOWN
...

NEXT_RESUME_POINT=<phase>
```

중요:

```text
R0에서 production mutation 금지
Git write 금지
reconcile 금지
install 금지
```

---

# 5. R1 — skillsilent v0.2.39 Delta Gate

## 5.1 목적

v1 이후 Storage/SSOT 정책에 맞게 갱신된 `skillsilent v0.2.39`가
실제 사내 PC에 설치 및 정합되어 있는지 확인한다.

## 5.2 확인

```text
skillsilent VERSION=0.2.39

main active discovery=NO
main registration=NO
main execution=NO
main fallback=NO
main write=NO

group/common auto-organize=NO
package auto mutation=NO

canonical declaration:
~/.claude/skills/<skill>/

canonical implementation:
~/l1sw-skills/private-skills/<skill>/

skillsilent state:
~/.skillsilent/
```

## 5.3 이미 PASS인 경우

```text
SKILLSILENT_V0239_DELTA=PASS
ACTION=SKIP_ALREADY_PASS
```

## 5.4 미설치 / 구버전인 경우

사용자가 제공한:

```text
skillsilent_v0_2_39_storage_ssot_bundle_0812.zip
```

기준으로 설치하고 bundle 안의:

```text
skillsilent_store_reconcile_prompt_v0239_0812.md
```

를 수행한다.

원칙:

```text
legacy main DELETE=NO
legacy main MODIFY=NO
legacy registry state-only rebind
canonical 대상 없으면 BLOCKED_LEGACY_ROOT
package 자동 수정 금지
```

PASS:

```text
SKILLSILENT_V0239_DELTA=PASS
```

FAIL이면 전체 Workflow 중단.

---

# 6. R2 — Resume Point Decision

R0 + R1 결과로 실제 재개 위치를 계산한다.

예:

```text
ACTIVE12_FINAL_VALIDATE_V2=PASS
ACTIVE12_LOCAL_RECONCILE=PASS
KNOWLEDGE_STORE_RECALL_RECONCILE=PASS
PRIVATE_HUB_REPRODUCIBILITY=PASS

PRIVATE_KNOWLEDGE_REPOSITORY_READY=NOT_RUN
```

이면:

```text
NEXT_RESUME_POINT=PRIVATE_KNOWLEDGE_REPOSITORY_INITIALIZE
```

즉 앞 단계는 다시 실행하지 않는다.

---

# 7. A — Active-12 Final Validate V2

기존 PASS evidence가 있으면:

```text
ACTION=SKIP_ALREADY_PASS
```

PASS evidence가 없을 때만 수행.

검사:

```text
VERSION
SKILL.md
skillsilent manifest/contract
package SHA
implementation route
runtime marker
write root
persistent root
branch output root
main active/fallback absence
dependency references
self-check / UT
```

필수:

```text
MAIN_ACTIVE_STORE=NO
MAIN_FALLBACK=NO
MAIN_NEW_WRITE=NO
LEGACY_ACTIVE_WRITE=NO
```

PASS:

```text
ACTIVE12_FINAL_VALIDATE_V2=PASS
```

---

# 8. B — Active-12 Local Reconcile / Adoption

기존 PASS면 SKIP.

필요 시 권장 순서:

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
missing-only
legacy read-only
conflict fail-closed
overwrite NO
delete NO
modify original NO
```

PASS:

```text
ACTIVE12_LOCAL_RECONCILE=PASS
```

---

# 9. C — Knowledge Recall / Reconcile Close

기존 PASS면 SKIP.

Canonical:

```text
~/l1sw-knowledge/
```

검증:

```text
legacy inventory
branch/CL scope audit
missing-only canonical reconcile
index rebuild
known recall
branch query
branch + CL query
```

필수:

```text
BRANCH_SCOPE_LOSS=0
CL_SCOPE_GUESSED=0
UNRESOLVED_SCOPE_CONFLICTS=0

LEGACY_SOURCE_DELETED=NO
LEGACY_SOURCE_MODIFIED=NO

MAIN_WRITE=NO
BRANCH_OUTPUT_WRITE_AS_KNOWLEDGE=NO
```

PASS:

```text
KNOWLEDGE_STORE_RECALL_RECONCILE=PASS
```

---

# 10. D~G — Private Hub Resume

Repository:

```text
l1sw-private-skills
```

이전 v1에서 아래가 PASS이면 모두 SKIP:

```text
PRIVATE_HUB_PUBLISH=PASS
PRIVATE_HUB_INSTALLER_CANARY=PASS
PRIVATE_HUB_FULL_INSTALL_VALIDATE=PASS
PRIVATE_HUB_REPRODUCIBILITY=PASS
```

PASS evidence 없는 단계부터만 resume한다.

사내 정책:

```text
skill-updater 사용 금지
private-skill-publisher 사용
private-skill-installer 사용
Active-12만 대상
Retired-2 제외
Group/Common NO_TOUCH
```

Canary:

```text
issue-analyzer v0.11.6
```

최종:

```text
PRIVATE_HUB_REPRODUCIBILITY=PASS
PRIVATE_HUB_OPERATIONAL=YES
```

---

# 11. H — Private Knowledge Repository Initialize / Verify

## 11.1 목적

다음 사내 Private GitHub Repository를 준비한다.

```text
REPOSITORY=l1sw-private-knowledge
VISIBILITY=PRIVATE
```

역할:

```text
~/l1sw-knowledge/
= authoritative live Knowledge SSOT

l1sw-private-knowledge
= versioned backup
+ distribution
+ restore source
```

**Git Repository 자체가 live runtime SSOT가 아니다.**

## 11.2 먼저 존재 여부 확인

READ ONLY:

```text
repository exists?
visibility private?
remote reachable?
current scaffold state?
```

이미 존재하면:

```text
REMOTE_RECREATE=NO
REMOTE_OVERWRITE=NO
→ 구조/visibility만 검증
```

정상:

```text
PRIVATE_KNOWLEDGE_REPOSITORY_READY=PASS
```

없을 경우에만 아래 **내장 생성 프롬프트**를 실행한다.

---

# 12. [내장 프롬프트] l1sw-private-knowledge Repository 최초 생성

아래 블록은 Repository가 **없을 때만** 실행한다.

```text
[BEGIN PRIVATE_KNOWLEDGE_REPOSITORY_INITIALIZE_PROMPT]

목표:
사내 GitHub에 다음 Private Repository를 생성한다.

Repository:
l1sw-private-knowledge

Visibility:
PRIVATE

역할:
~/l1sw-knowledge/
= authoritative live Knowledge SSOT

l1sw-private-knowledge
= versioned backup / internal distribution / restore source

이번 단계에서는 실제 Knowledge를 업로드하지 않는다.
Repository + empty scaffold만 생성한다.

절대 원칙:

REPOSITORY=l1sw-private-knowledge
VISIBILITY=PRIVATE

LIVE_KNOWLEDGE_ROOT=~/l1sw-knowledge/
LIVE_KNOWLEDGE_NO_TOUCH=YES

KNOWLEDGE_UPLOAD_IN_THIS_PHASE=NO
CANDIDATE_UPLOAD=NO
RUNTIME_UPLOAD=NO

INTERNAL_GIT_USE_SKILL_UPDATER=NO
GROUP_COMMON_SKILL_POLICY=NO_TOUCH

LEGACY_DELETE=NO
LEGACY_MODIFY=NO

CREDENTIAL_IN_URL=NO
PAT_IN_FILE=NO
PASSWORD_IN_FILE=NO
TOKEN_IN_FILE=NO

Preflight:
- git --version
- gh 사용 가능 여부
- 현재 GitHub Enterprise host
- 현재 인증 상태
- user / organization namespace
- l1sw-private-knowledge 존재 여부

credential/token 값 자체는 출력하지 않는다.

namespace가 환경에서 결정되지 않을 때만 사용자에게 질문:
1. 현재 개인 계정
2. 사내 Organization

Repository 이름은 다시 묻지 않는다.

중복 보호:
이미 l1sw-private-knowledge가 존재하면 생성하지 않는다.

REMOTE_DELETE=NO
REMOTE_RECREATE=NO
REMOTE_OVERWRITE=NO

존재하지 않는 경우에만 PRIVATE Repository를 생성한다.

Git 인증:
- 이미 인증된 gh CLI 또는 사내 공식 Git client 우선
- credential 포함 URL 금지
- PAT/token script 저장 금지
- token echo/log 금지

Local work root 권장:
~/l1sw-private-knowledge-repo/

최초 scaffold:

l1sw-private-knowledge/
├─ README.md
├─ current/
│  └─ .gitkeep
├─ inventory/
│  └─ .gitkeep
├─ indexes/
│  └─ .gitkeep
├─ history/
│  └─ .gitkeep
├─ evidence/
│  └─ .gitkeep
├─ catalogs/
│  └─ .gitkeep
├─ mappings/
│  └─ .gitkeep
└─ manifests/
   ├─ repository-manifest.json
   └─ checksums.json

이번 단계에서 복사 금지:
~/l1sw-knowledge/current/*
~/l1sw-knowledge/candidates/*
~/l1sw-knowledge/indexes/*
legacy knowledge
runtime/cache/log/output

즉 empty directory scaffold만 만든다.

README 최소 계약:

# l1sw-private-knowledge

Private repository for approved L1 Knowledge backup, distribution, and restore.

Authoritative live store:
~/l1sw-knowledge/

This repository is NOT the runtime SSOT.

Publish flow:
slte-knowledge-manager learning
→ candidates
→ validation / scope / conflict check
→ approval
→ ~/l1sw-knowledge/current/
→ index / recall validation
→ publish precheck
→ l1sw-private-knowledge

Do not publish:
- unapproved candidates
- runtime/cache/log/temp
- migration backup
- credential/auth data

manifests/repository-manifest.json:

{
  "schema_version": 1,
  "repository": "l1sw-private-knowledge",
  "status": "initialized",
  "knowledge_snapshot_present": false
}

manifests/checksums.json:

{
  "schema_version": 1,
  "files": {}
}

Secret / local-data scan:
- password
- passwd
- PAT
- token
- api key
- api_key
- private key
- BEGIN PRIVATE KEY
- credential
- authorization
- cookie
- machine-local auth
- *.pem
- *.key
- .env
- auth cache
- temporary dump
- user-specific temporary path

실제 secret 의심 값 발견 시:
COMMIT=NO
PUSH=NO
RESULT=FAIL

Safety Gate PASS 후 initial commit:

Commit message:
Initialize private knowledge repository

Initial commit에는 scaffold만 포함.

필수:
APPROVED_KNOWLEDGE_UPLOADED=NO
CANDIDATES_UPLOADED=NO
LIVE_KNOWLEDGE_CHANGED=NO

Push 후 검증:
REMOTE_EXISTS=YES
VISIBILITY_PRIVATE=YES
README=PASS
MANIFEST=PASS
CHECKSUM_SCAFFOLD=PASS
EMPTY_KNOWLEDGE_SCAFFOLD=PASS

이번 단계에서 하지 않을 것:
- 실제 Knowledge publish
- ~/l1sw-knowledge/ 변경
- candidate 승인
- index rebuild
- restore canary
- private-skill publish
- skill-updater 사용
- Group/Common 변경
- legacy 삭제

성공 출력:

RESULT=PASS
MODE=PRIVATE_KNOWLEDGE_REPOSITORY_INITIALIZE

REPOSITORY=l1sw-private-knowledge
VISIBILITY=PRIVATE
REMOTE_CREATED=YES
INITIAL_COMMIT=PASS
INITIAL_PUSH=PASS

EMPTY_SCAFFOLD=PASS
SECRET_SCAN=PASS

APPROVED_KNOWLEDGE_UPLOADED=NO
CANDIDATES_UPLOADED=NO
LIVE_KNOWLEDGE_CHANGED=NO

SKILL_UPDATER_USED=NO
GROUP_COMMON_TOUCHED=NO
LEGACY_TOUCHED=NO

PRIVATE_KNOWLEDGE_REPOSITORY_READY=PASS

[END PRIVATE_KNOWLEDGE_REPOSITORY_INITIALIZE_PROMPT]
```

---

# 13. I — Private Knowledge Publish Precheck

전제:

```text
KNOWLEDGE_STORE_RECALL_RECONCILE=PASS
PRIVATE_KNOWLEDGE_REPOSITORY_READY=PASS
```

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

Secret Gate:

```text
password
PAT
token
api key
private key
credential
cookie
authorization
machine-local auth
```

필수:

```text
SECRET_SCAN=PASS
UNAPPROVED_CANDIDATE_INCLUDED=NO
RUNTIME_DATA_INCLUDED=NO
MACHINE_LOCAL_AUTH_INCLUDED=NO
```

PASS:

```text
PRIVATE_KNOWLEDGE_PUBLISH_PRECHECK=PASS
```

---

# 14. USER GATE — 실제 Knowledge Publish

Precheck PASS 후에만 사용자에게 한 번 질문한다.

```text
사내 l1sw-private-knowledge Repository에
현재 승인된 Knowledge snapshot을 publish할까요?

1. YES
2. NO
```

YES일 때만 Git write.

NO이면:

```text
RESULT=BLOCKED
REASON=USER_DEFERRED_KNOWLEDGE_PUBLISH
```

production Knowledge는 변경하지 않는다.

---

# 15. J — Knowledge Publish / Remote Verify

Flow:

```text
~/l1sw-knowledge/
    ↓
publish-safe snapshot
    ↓
l1sw-private-knowledge
```

원칙:

```text
live store 직접 git checkout overwrite 금지
candidate publish 금지
runtime/cache/log publish 금지
credential publish 금지
```

검증:

```text
manifest
checksums
approved Knowledge
Branch/CL scope metadata
indexes/catalog metadata
excluded directory absence
secret absence
```

PASS:

```text
PRIVATE_KNOWLEDGE_PUBLISH=PASS
PRIVATE_KNOWLEDGE_REMOTE_VERIFY=PASS
```

---

# 16. K — Private Knowledge Restore Canary

production:

```text
~/l1sw-knowledge/
```

NO_TOUCH.

isolated root에 remote snapshot 복원.

검사:

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

# 17. L — Knowledge Reproducibility Close

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

# 18. M — Naming Audit

READ ONLY 우선.

검토:

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

자동 rename 금지.

결과:

```text
NAMING_CHANGE_REQUIRED=YES/NO
```

실제 rename은 사용자 승인 필요.

---

# 19. N — Retired-2 Reference Audit

대상:

```text
issue-fix-implement
slte-port-impact-analyzer
```

READ ONLY:

```text
dependency reference
cross-skill invocation
registry
manifest
documentation
job-list
installer
publisher
legacy persistent
rollback need
```

실제 삭제 금지.

출력:

```text
RETIRED_SKILL=<name>
REFERENCES=<count>
SAFE_TO_REMOVE=YES/NO
DELETE_PERFORMED=NO
```

---

# 20. USER POLICY GATE

다음은 자동 수행하지 않는다.

```text
1. Naming normalization
2. Group/Common promote
3. Retired-2 실제 제거
4. Legacy cleanup
5. 모두 보류
```

기본 권장:

```text
5. 모두 보류
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

# 21. O — Steady State

## 21.1 Skill

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

설치:

```text
l1sw-private-skills
→ private-skill-installer
→ checksum / registry
→ install
→ implementation sync
→ skillsilent
→ smoke
```

사내:

```text
SKILL_UPDATER_USED=NO
```

## 21.2 Knowledge

새 학습:

```text
source / code / HLD / UT / Wiki / issue evidence
        ↓
slte-knowledge-manager
        ↓
~/l1sw-knowledge/candidates/
        ↓
validation / scope / conflict
        ↓
approval
        ↓
~/l1sw-knowledge/current/
        ↓
index rebuild / recall validate
        ↓
publish precheck
        ↓
l1sw-private-knowledge
        ↓
remote verify
```

관계:

```text
~/l1sw-knowledge/
= authoritative live SSOT

l1sw-private-knowledge
= versioned backup / distribution / restore
```

Git에서 직접 학습하지 않는다.

---

# 22. Machine-readable 공통 결과

PASS:

```text
RESULT=PASS
MODE=<phase>
ACTION=EXECUTED/SKIP_ALREADY_PASS
FAILED_CHECKS=0
NEXT_STEP=<next>
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
NEXT_STEP=<repair/retry>
AUTO_CONTINUE=NO
```

BLOCKED:

```text
RESULT=BLOCKED
MODE=<phase>
BLOCK_REASON=<reason>
AUTO_OVERWRITE=NO
USER_DECISION_REQUIRED=YES/NO
```

---

# 23. v3 최종 완료 Gate

아래를 확인한다.

```text
SKILLSILENT_V0239_DELTA=PASS

ACTIVE12_FINAL_VALIDATE_V2=PASS
ACTIVE12_LOCAL_RECONCILE=PASS
KNOWLEDGE_STORE_RECALL_RECONCILE=PASS

PRIVATE_HUB_REPRODUCIBILITY=PASS
PRIVATE_HUB_OPERATIONAL=YES

PRIVATE_KNOWLEDGE_REPOSITORY_READY=PASS
PRIVATE_KNOWLEDGE_PUBLISH_PRECHECK=PASS
PRIVATE_KNOWLEDGE_PUBLISH=PASS
PRIVATE_KNOWLEDGE_RESTORE_CANARY=PASS
PRIVATE_KNOWLEDGE_REPRODUCIBILITY=PASS
PRIVATE_KNOWLEDGE_OPERATIONAL=YES

RETIRED2_REFERENCE_AUDIT=PASS

INTERNAL_GIT_USE_SKILL_UPDATER=NO
GROUP_COMMON_TOUCHED=NO
LEGACY_AUTO_DELETE=NO
```

이 중 v1에서 이미 PASS한 것은
READ-ONLY evidence 확인 후 `SKIP_ALREADY_PASS`로 인정한다.

최종:

```text
RESULT=PASS
MODE=PRIVATE_SKILL_KNOWLEDGE_FINAL_CLOSE_V3

RESUME_MODE=YES
DUPLICATE_MUTATION=NO

PRIVATE_HUB_OPERATIONAL=YES
PRIVATE_KNOWLEDGE_OPERATIONAL=YES
STEADY_STATE_READY=YES
```

---

# 24. 새 작업창에서 바로 사용할 실행 프롬프트

```text
이 문서를 최신 Final Close Master Workflow v3로 사용해줘.

중요한 현재 상황:
- 이전 `private_skill_knowledge_final_close_master_workflow_0812.md`는 이미 수행했다.
- 따라서 처음부터 재실행하지 말고 반드시 RESUME/DELTA 방식으로 수행한다.
- 기존 PASS Phase는 READ-ONLY evidence로 확인 후 SKIP_ALREADY_PASS 처리한다.
- 기존 PASS install/reconcile/Git publish/canary를 중복 실행하지 않는다.
- FAIL/BLOCKED/NOT_RUN/UNKNOWN 중 PASS 입증이 안 되는 Phase만 수행한다.

v1 이후 변경:
- skillsilent 최신 버전은 v0.2.39다.
- 먼저 skillsilent v0.2.39 Delta Gate를 확인한다.
- 미설치/미정합이면 최신 bundle + reconcile 절차로 정합한다.
- main은 active/fallback/write/execution 경로로 사용하지 않는다.

Knowledge Repository:
- l1sw-private-knowledge가 아직 없을 수 있다.
- 존재 여부부터 확인한다.
- 없으면 이 문서의 내장 `PRIVATE_KNOWLEDGE_REPOSITORY_INITIALIZE_PROMPT`를 사용한다.
- Repository 생성 단계에서는 empty scaffold만 생성한다.
- 실제 Knowledge는 절대 이 단계에서 업로드하지 않는다.
- 실제 승인 Knowledge publish는 Publish Precheck PASS 후 사용자 승인 시 수행한다.

Storage:
- Package = ~/.claude/skills/<skill>/
- Implementation = ~/l1sw-skills/private-skills/<skill>/
- Persistent = 필요한 Skill만 ~/l1sw-data/<skill>/
- Shared Knowledge SSOT = ~/l1sw-knowledge/
- Branch evidence = <branch>/output/<skill>/
- ~/.claude/main 신규 active/fallback/write 금지

Safety:
- legacy read-only
- missing-only reconcile
- conflict overwrite 금지
- Group/Common/Unlisted NO_TOUCH
- 사내 Git에서 skill-updater 사용 금지
- Git write와 destructive action에서만 사용자 확인

먼저 R0 EXISTING V1 RESULT INVENTORY부터 시작하고,
그 결과를 기준으로 최소한의 Delta만 연속 수행해줘.
```
