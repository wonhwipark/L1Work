# SLTE Knowledge Manager v0.4.7 — 기존 지식 전체 취합 / Recall / Reconcile 실행 프롬프트

아래 작업을 순서대로 수행하라. 회사 Windows 환경 기준이며 **bash를 사용하지 않는다**. PowerShell 또는 Python을 직접 사용한다.

이 작업의 목적은 새로 학습하는 것이 아니다.

```text
기존 PC/작업공간에 이미 저장되어 있는 SLTE Knowledge를 최대한 찾아 inventory한다.
→ 승인/후보/reference/runtime를 구분한다.
→ 중복·충돌을 식별한다.
→ source를 삭제하거나 덮어쓰지 않고 canonical store로 안전하게 취합한다.
→ index를 재구축한다.
→ 과거 학습이 recall/query 되는지 검증한다.
```

---

# 0. 절대 정책

Canonical live Knowledge SSOT:

```text
~/l1sw-knowledge/
```

신규 학습/승인/query/index/history/run의 정상 read/write는 canonical root만 사용한다.

```text
NORMAL_READ_WRITE=~/l1sw-knowledge/**
```

`~/.claude/main/slte-knowledge-manager/`는 신규 active store가 아니다.

```text
LEGACY_MAIN_ACTIVE_STORE=NO
LEGACY_MAIN_WRITE=NO
LEGACY_MAIN_FALLBACK=NO
LEGACY_MAIN_MIGRATION_READ=YES
```

금지:

```text
Knowledge 재학습부터 시작 금지
candidate 자동 승인 금지
stale Knowledge 자동 current 승격 금지
충돌 파일 자동 overwrite 금지
legacy source 삭제/cleanup 금지
legacy main write 금지
Group/Common Skill 변경 금지
skill-updater 사용 금지
Git publish 금지
PRIVATE_KNOWLEDGE_PUBLISH는 이 작업 완료 전 금지
```

이번 작업에서 사용자가 개별 파일을 선택하게 하지 않는다.

```text
USER_FILE_SELECTION=NO
```

시스템이 저장소 단위로 inventory/분류/취합하고, 해결 불가능한 충돌만 그룹 단위로 보고한다.

---

# 1. 설치 버전 / Active Root 확인

실행:

```powershell
skillsilent run slte-knowledge-manager capabilities --
```

필수 확인:

```text
version=0.4.7
output_root=~/l1sw-knowledge/  # 또는 동일 경로의 Windows expand 결과
actions includes store-doctor
actions includes recall
```

다음이면 즉시 FAIL:

```text
version != 0.4.7
resolved active root가 protected legacy main
legacy main이 write target
```

Canary/test용 명시적 isolated override가 설정되어 있으면 운영 reconcile 전에는 제거하고 canonical root로 복귀한다.

---

# 2. 기존 Knowledge 저장소 전체 Inventory — READ ONLY

## 2.1 Known roots

아래 위치는 존재 여부를 모두 확인한다. 존재하지 않는 것은 정상이며 생성하지 않는다.

```text
A. ~/l1sw-knowledge/
   = canonical current store

B. ~/.claude/main/slte-knowledge-manager/
   = historical persistent store / legacy read-only source

C. ~/slte_knowledge/
   = older shared legacy store

D. ~/l1sw-skills/private/slte-knowledge-manager/
   = 과거 검토되었던 private persistent 후보 위치
   = 실제 Knowledge signature가 있을 때만 legacy candidate로 분류

E. 현재 설치된 slte-knowledge-manager package/runtime 내부의 과거 mutable Knowledge 흔적
   - knowledge/
   - current/
   - candidates/
   - history/
   - evidence/
   - indexes/
   - inventory/
   - block_context/
   - migration/
   - migration-backup/

F. 과거 branch-local store
   <working-branch-root>/output/slte-knowledge/
```

D/E는 **경로가 존재한다는 이유만으로 Knowledge store로 판정하지 않는다.** 아래 signature 중 하나 이상이 있을 때만 후보로 잡는다.

```text
knowledge_manifest.json
current/rules/*.json
candidates/pending/*.json
current/ut-structure/*.json
inventory/entities/*.json
responsibility_catalog.json
history/
evidence/
```

## 2.2 Historical branch store discovery

과거 버전에서 다음 경로를 사용했으므로 현재 알고 있는/접근 가능한 SLTE 작업 branch/worktree에서만 찾는다.

```text
<branch-root>/output/slte-knowledge/knowledge_manifest.json
```

탐색 우선순위:

```text
1. 현재 working directory 및 부모 repository root
2. 기존 Knowledge manifest/migration/history에서 참조된 branch root
3. 현재 도구가 이미 알고 있는 사용자의 SLTE workspace/worktree roots
```

금지:

```text
전체 회사 드라이브 무차별 recursive scan 금지
네트워크 드라이브 전체 scan 금지
사용자 홈 전체를 제한 없이 재귀 탐색 금지
```

필요한 경우 Python으로 **known workspace roots 아래에서만** `output/slte-knowledge/knowledge_manifest.json` signature를 탐색한다.

## 2.3 Migration/backup/history도 inventory

아래는 authoritative current Knowledge로 바로 merge하지 않고 먼저 inventory한다.

```text
*/migration-backup/
*/migration/
*/history/
*/evidence/
*/candidates/
*/providers/
*/wiki_mcp/
*/runs/
*/output/
```

분류:

```text
current/rules APPROVED       → APPROVED_KNOWLEDGE
current/rules stale=true     → STALE_APPROVED
candidates/*                 → PENDING_OR_CANDIDATE
current/ut-structure         → APPROVED_UT_KNOWLEDGE
inventory/*                  → INVENTORY_KNOWLEDGE
responsibility_catalog      → RESPONSIBILITY_KNOWLEDGE
history/evidence             → AUDIT_EVIDENCE
migration-backup             → RECOVERY_ONLY
providers/wiki_mcp           → REFERENCE_ONLY
runs/output/cache            → RUNTIME_OR_DERIVED
unknown                      → UNKNOWN
```

중요:

```text
REFERENCE_ONLY != APPROVED_KNOWLEDGE
RUNTIME_OR_DERIVED != APPROVED_KNOWLEDGE
RECOVERY_ONLY != APPROVED_KNOWLEDGE
```

## 2.4 Store Doctor

아직 migration/merge를 수행하지 말고 먼저:

```powershell
skillsilent run slte-knowledge-manager store-doctor --
```

기본 출력 외에 위에서 발견한 추가 candidate store를 함께 inventory하여 아래 표를 만든다.

```text
SOURCE_ID
ROOT
SOURCE_TYPE
EXISTS
KNOWLEDGE_SIGNATURE
APPROVED_RULES
STALE_RULES
PENDING_CANDIDATES
ACTIVE_INVENTORY
UT_PROFILES
HISTORY_FILES
EVIDENCE_FILES
REFERENCE_ONLY_FILES
RECOVERY_ONLY_FILES
MANIFEST_VERSION
MIGRATION_STATUS
READ_ONLY_SOURCE
COLLECT_ACTION
```

`COLLECT_ACTION` 값:

```text
CANONICAL_KEEP
AUTO_RECONCILE_SUPPORTED
BRANCH_LEGACY_STAGE_IMPORT
REFERENCE_ONLY_KEEP
RECOVERY_ONLY_KEEP
RUNTIME_IGNORE
UNKNOWN_REVIEW
EMPTY_IGNORE
```

---

# 3. 취합 전 Dedup / Conflict Preview — READ ONLY

모든 Knowledge source에 대해 canonical과 비교한다.

## 3.1 Exact duplicate

동일 relative path + 동일 SHA256:

```text
EXACT_DUPLICATE
→ 다시 copy할 필요 없음
```

서로 다른 파일명이더라도 기존 schema의 안정 ID를 사용할 수 있으면 아래 기준으로 추가 비교한다.

```text
identity_key
rule_id
candidate_id
entity_id
profile_id
responsibility_id
기타 schema에 정의된 stable identity
```

같은 stable identity + 동일 normalized content:

```text
SEMANTIC_DUPLICATE
```

자동 삭제는 하지 않는다.

## 3.2 Conflict

같은 relative path 또는 같은 stable identity인데 내용/SHA가 다르면:

```text
CONFLICT
```

정책:

```text
canonical current store 자동 overwrite 금지
legacy source 자동 overwrite 금지
한쪽 자동 삭제 금지
candidate 자동 승인 금지
```

Conflict는 다음과 같이 그룹화한다.

```text
APPROVED_VS_APPROVED
APPROVED_VS_STALE
APPROVED_VS_PENDING
INVENTORY_CONFLICT
UT_PROFILE_CONFLICT
RESPONSIBILITY_CONFLICT
UNKNOWN_CONFLICT
```

취합 전에 다음 수치를 산출한다.

```text
DISCOVERED_STORES=<n>
CONTENT_STORES=<n>
EXACT_DUPLICATES=<n>
SEMANTIC_DUPLICATES=<n>
MISSING_IN_CANONICAL=<n>
CONFLICT_GROUPS=<n>
UNKNOWN_ITEMS=<n>
```

---

# 4. Canonical Store 초기화 / 기본 Legacy Reconcile

먼저 v0.4.7이 공식 지원하는 기본 legacy source를 canonical에 missing-only 방식으로 reconcile한다.

```powershell
skillsilent run slte-knowledge-manager init --
```

기대 동작:

```text
[READ ONLY SOURCE]
~/.claude/main/slte-knowledge-manager/
~/slte_knowledge/
        ↓
missing-only merge
        ↓
~/l1sw-knowledge/
        ↓
index rebuild
```

정책:

```text
canonical target wins path conflicts
conflict copy는 canonical migration-backup에 보존
legacy external source retained
legacy source delete 금지
legacy main write 금지
candidate 상태 변경 금지
```

실행 후:

```powershell
skillsilent run slte-knowledge-manager store-doctor --
```

기본 legacy에 대해:

```text
migration_needed=false
```

이어야 한다.

`split_brain_detected`가 단순 legacy snapshot 존재 때문이 아니라 실제 missing/conflict/active override 때문에 true라면 원인을 계속 추적한다.

---

# 5. Historical Branch Store 취합

과거 `<branch-root>/output/slte-knowledge/` store가 발견된 경우 수행한다.

중요: 기존 `migrate-store`는 source manifest에 migration marker를 기록할 수 있으므로 **원본 branch store를 직접 migrate 대상으로 사용하지 않는다.**

각 branch legacy store별로:

```text
원본 = READ ONLY
        ↓
임시 staging copy
        ↓
supported migrate-store를 staging copy에 실행
        ↓
~/l1sw-knowledge/
```

Staging은 canonical Knowledge 밖의 임시 경로 또는 canonical의 명시적 migration staging 영역을 사용하되, 원본 source는 변경하지 않는다.

절차 개념:

```text
<original-branch>/output/slte-knowledge/
       ↓ read-only deterministic copy
<staging-branch>/output/slte-knowledge/
       ↓
skillsilent run slte-knowledge-manager migrate-store -- --from <staging-branch> --confirm
       ↓
~/l1sw-knowledge/
```

각 source 후 반드시:

```powershell
skillsilent run slte-knowledge-manager validate --
```

실패하면 해당 source만 BLOCK하고 다른 source를 덮어쓰지 않는다.

원본 branch store:

```text
SOURCE_CHANGED=NO
SOURCE_DELETED=NO
```

---

# 6. 추가 Legacy Candidate 취합

다음처럼 Knowledge signature는 있으나 v0.4.7 공식 기본 source가 아닌 위치가 발견될 수 있다.

예:

```text
~/l1sw-skills/private/slte-knowledge-manager/
과거 package/runtime 내부 mutable knowledge snapshot
기타 manifest/history가 명시적으로 가리키는 legacy store
```

원칙:

```text
UNKNOWN PATH를 자동 active store로 사용하지 않는다.
원본을 직접 수정하지 않는다.
파일별 사용자 선택을 요구하지 않는다.
```

가능하면 store layout/schema를 판정한다.

### A. v0.1.x branch-store layout

```text
STAGING COPY
→ migrate-store
```

### B. 현재/호환 persistent-store layout

```text
STAGING COPY
→ missing-only deterministic merge
→ canonical conflict backup
→ initialize/index rebuild
→ validate
```

단, 이 경우 기존 v0.4.7 코드의 안전한 missing-only primitive/공식 동작을 우선 사용하고 임의 overwrite 로직을 새로 만들지 않는다.

### C. schema/layout 불명

```text
COLLECT_ACTION=UNKNOWN_REVIEW
```

으로 남기고 자동 merge하지 않는다.

---

# 7. Canonical Consolidation Audit

모든 지원 가능한 source 취합 후 canonical을 다시 inventory한다.

최소 확인:

```text
~/l1sw-knowledge/current/rules/
~/l1sw-knowledge/candidates/
~/l1sw-knowledge/current/ut-structure/
~/l1sw-knowledge/inventory/
~/l1sw-knowledge/block_context/
~/l1sw-knowledge/responsibility_catalog.json
~/l1sw-knowledge/history/
~/l1sw-knowledge/evidence/
~/l1sw-knowledge/migration/
~/l1sw-knowledge/migration-backup/
```

취합 전/후 count를 비교한다.

```text
APPROVED_RULES_BEFORE / AFTER
PENDING_CANDIDATES_BEFORE / AFTER
UT_PROFILES_BEFORE / AFTER
INVENTORY_ENTITIES_BEFORE / AFTER
RESPONSIBILITY_ENTRIES_BEFORE / AFTER
HISTORY_FILES_BEFORE / AFTER
EVIDENCE_FILES_BEFORE / AFTER
```

지식 손실 판정:

```text
source에만 존재했던 non-conflicting Knowledge가 canonical에도 존재
→ COLLECTED

canonical conflict로 source 버전이 적용되지 않았지만 migration-backup/evidence에 보존
→ PRESERVED_CONFLICT

source에 있었는데 canonical/backup 어느 곳에도 없음
→ KNOWLEDGE_LOSS_RISK
```

`KNOWLEDGE_LOSS_RISK > 0`이면 FAIL.

---

# 8. Duplicate / Conflict Audit

취합 후 다시 stable identity/SHA 기준으로 중복과 충돌을 검사한다.

정책:

```text
exact duplicate 자동 삭제 금지
semantic duplicate 자동 삭제 금지
conflicting approved Knowledge 자동 선택 금지
pending 자동 승인 금지
```

단순 중복은 운영을 막지 않되 보고한다.

```text
DUPLICATE_STATUS=INFO
```

동일 stable identity의 서로 다른 APPROVED 지식이 현재 query 결과를 모호하게 만들 수 있으면:

```text
RESULT=PARTIAL
NEXT_STEP=KNOWLEDGE_CONFLICT_REVIEW
```

사용자에게 개별 파일을 고르게 하지 말고 다음처럼 **충돌 그룹 단위**로 요약한다.

```text
CONFLICT_GROUP_ID
IDENTITY
CATEGORY
CANONICAL_VERSION
OTHER_SOURCE_VERSION
APPLICABILITY_DIFFERENCE
RECOMMENDED_RESOLUTION
```

---

# 9. Store Validate / Index Rebuild

실행:

```powershell
skillsilent run slte-knowledge-manager validate --
```

PASS 조건:

```text
ok=true
errors=[]
```

index mismatch가 있을 때만:

```powershell
skillsilent run slte-knowledge-manager repair-index --
skillsilent run slte-knowledge-manager validate --
```

`validate` PASS인데 습관적으로 `repair-index`를 실행하지 않는다.

---

# 10. 기존 학습 Recall 검증

재학습하지 말고 기존 Knowledge를 회수한다.

대표 용어는 **inventory 결과에서 자동 선정**한다. 사용자가 일일이 용어를 입력하게 하지 않는다.

최소 5개, 가능하면 다음 category를 섞는다.

```text
Manager/Class
MSG/Procedure
Build option
Component
UT feature/scenario
Responsibility
MSC/procedure-related approved knowledge
```

우선 source별로 canonical에 새로 취합된 지식에서 대표 term을 하나 이상 포함한다.

각 term:

```powershell
skillsilent run slte-knowledge-manager recall -- `
  --term "<TERM>" `
  --branch "<TARGET_BRANCH>" `
  --scenario "<SCENARIO>" `
  --cl <CL>
```

branch/scenario/CL을 확실히 알 수 없는 지식은 억지 값을 만들지 말고 지원되는 최소 selector로 recall한다.

확인:

```text
approved_rule_matches
inventory_matches
ut_structure_matches
responsibility_matches
pending_candidate_matches
```

판정:

```text
FOUND_APPROVED
→ 기존 승인 학습 회수 성공

FOUND_ONLY_NON_USABLE / FOUND_NOT_CURRENTLY_APPLICABLE
→ 지식은 있으나 pending/stale/branch/CL/scenario 조건상 현재 authoritative 근거가 아님

NOT_FOUND
→ migration-backup/history/source inventory까지 대조 후에만 실제 miss 판정
```

---

# 11. Strict Query 재검증

Recall에서 찾은 승인 지식은 실제 분석 근거로 사용하기 전에 strict query로 다시 검증한다.

L1 domain 예:

```powershell
skillsilent run slte-knowledge-manager query-l1-domain-context -- `
  --term "<TERM>" `
  --branch "<TARGET_BRANCH>" `
  --scenario "<SCENARIO>"
```

일반 rule 예:

```powershell
skillsilent run slte-knowledge-manager query -- `
  --component "<COMPONENT>" `
  --class "<CLASS>" `
  --symbol "<SYMBOL>" `
  --branch "<TARGET_BRANCH>" `
  --scenario "<SCENARIO>" `
  --cl <CL>
```

의미:

```text
recall
= 과거 학습 존재/위치/상태 회수

strict query
= 현재 branch/CL/scenario에서 사용할 authoritative Knowledge 선택
```

---

# 12. 신규 학습 저장 경로 확인

이 작업에서는 새 학습을 강제로 수행하지 않는다.

향후 v0.4.7 정상 학습의 모든 mutable data는 아래에만 저장되어야 한다.

```text
~/l1sw-knowledge/
├─ candidates/pending/
├─ current/rules/
├─ candidates/ut-structure/
├─ current/ut-structure/
├─ inventory/
├─ block_context/
├─ responsibility_catalog.json
├─ indexes/
├─ msc-learning/runs/
├─ integrated_learning/runs/
├─ domain_bootstrap/runs/
├─ runs/
├─ history/
├─ evidence/
├─ migration/
└─ migration-backup/
```

검증 정책:

```text
NEW_LEARNING_WRITTEN_TO_CANONICAL=YES
NEW_LEARNING_WRITTEN_TO_LEGACY_MAIN=NO
MAIN_AS_ACTIVE_STORE=NO
MAIN_AS_FALLBACK=NO
```

---

# 13. 최종 결과 출력

긴 로그를 사용자에게 직접 분석하게 하지 말고 아래 machine-readable summary + 짧은 conflict summary만 출력한다.

```text
RESULT=PASS|PARTIAL|FAIL
MODE=KNOWLEDGE_FULL_CONSOLIDATE_RECALL_RECONCILE_V047

MANAGER_VERSION=0.4.7
CANONICAL_ROOT=~/l1sw-knowledge/
RESOLVED_ROOT=<path>

DISCOVERED_STORES=<n>
CONTENT_STORES=<n>
COLLECTED_STORES=<n>
SKIPPED_EMPTY_STORES=<n>
UNKNOWN_STORES=<n>

APPROVED_RULES_BEFORE=<n>
APPROVED_RULES_AFTER=<n>
PENDING_CANDIDATES_BEFORE=<n>
PENDING_CANDIDATES_AFTER=<n>
UT_PROFILES_BEFORE=<n>
UT_PROFILES_AFTER=<n>
INVENTORY_ENTITIES_BEFORE=<n>
INVENTORY_ENTITIES_AFTER=<n>

EXACT_DUPLICATES=<n>
SEMANTIC_DUPLICATES=<n>
CONFLICT_GROUPS=<n>
PRESERVED_CONFLICTS=<n>
KNOWLEDGE_LOSS_RISK=<n>

DEFAULT_LEGACY_RECONCILE=PASS|FAIL|NOT_NEEDED
BRANCH_LEGACY_COLLECT=PASS|PARTIAL|NOT_FOUND
ADDITIONAL_LEGACY_COLLECT=PASS|PARTIAL|NOT_FOUND
INDEX_VALIDATE=PASS|FAIL
INDEX_REPAIR_PERFORMED=YES|NO

RECALL_TERMS=<n>
RECALL_FOUND_APPROVED=<n>
RECALL_FOUND_NON_USABLE=<n>
RECALL_NOT_FOUND=<n>
STRICT_QUERY=PASS|PARTIAL|FAIL

LEGACY_MAIN_RETAINED=YES
LEGACY_MAIN_ACTIVE_STORE=NO
LEGACY_MAIN_WRITE=NO
LEGACY_SOURCES_DELETED=NO
CANDIDATE_AUTO_APPROVED=NO
KNOWLEDGE_RELEARN_FORCED=NO
SKILL_UPDATER_USED=NO
GROUP_COMMON_SKILL_TOUCHED=NO
PRIVATE_KNOWLEDGE_PUBLISHED=NO

UNRESOLVED_CONFLICT_GROUPS=<list or NONE>
UNRESOLVED_STORES=<list or NONE>
UNRESOLVED_TERMS=<list or NONE>
NEXT_STEP=<next>
```

NEXT_STEP:

```text
조건:
- KNOWLEDGE_LOSS_RISK=0
- UNKNOWN_STORES=0 또는 모두 명시적으로 NON_KNOWLEDGE 판정
- CONFLICT_GROUPS=0 또는 query 영향 없는 보존형 conflict만 존재
- INDEX_VALIDATE=PASS
- 대표 기존 Knowledge recall 성공
- strict query 정상

→ PRIVATE_KNOWLEDGE_PUBLISH_PRECHECK

동일 identity의 authoritative conflict가 남음
→ KNOWLEDGE_CONFLICT_REVIEW

미분류 store가 남음
→ KNOWLEDGE_STORE_CLASSIFICATION

recall NOT_FOUND가 남음
→ KNOWLEDGE_MISS_DIAGNOSIS

validate 실패
→ KNOWLEDGE_STORE_REPAIR

KNOWLEDGE_LOSS_RISK>0
→ FAIL / PRIVATE_KNOWLEDGE_PUBLISH 금지
```

---

# 14. 완료 Gate

최종 PASS는 단순히 `main`을 canonical로 복사했다는 의미가 아니다.

반드시:

```text
EXISTING_KNOWLEDGE_INVENTORIED=YES
KNOWN_LEGACY_STORES_SCANNED=YES
HISTORICAL_BRANCH_STORES_SCANNED=YES
SUPPORTED_STORES_CONSOLIDATED=YES
DUPLICATES_AUDITED=YES
CONFLICTS_AUDITED=YES
KNOWLEDGE_LOSS_RISK=0
INDEX_VALIDATE=PASS
RECALL_EXISTING_KNOWLEDGE=PASS
STRICT_QUERY=PASS
CANONICAL_ONLY_ACTIVE_STORE=YES
LEGACY_MAIN_WRITE=NO
LEGACY_SOURCES_RETAINED=YES
```

이어야 한다.

이 Gate가 PASS한 뒤에만 다음 단계로 이동한다.

```text
PRIVATE_KNOWLEDGE_PUBLISH_PRECHECK
```
