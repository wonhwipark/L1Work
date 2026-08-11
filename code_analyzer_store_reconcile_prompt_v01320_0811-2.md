# Code Analyzer v0.13.20 기존 상태 정리 / Reconcile 실행 프롬프트

> 목적: `code-analyzer v0.13.20` 설치 후, 과거 branch별 `output/code-analyzer/`에 섞여 있던 **장기 사용자 상태만** 중앙 persistent store로 안전하게 취합한다.
>
> 분석 산출물 자체를 중앙화하지 않는다.

---

# 0. 절대 원칙

```text
CODE_ANALYZER_VERSION=0.13.20

PACKAGE_ROOT=~/.claude/skills/code-analyzer/
IMPLEMENTATION_ROOT=~/l1sw-skills/private-skills/code-analyzer/

PERSISTENT_ROOT=~/l1sw-data/code-analyzer/
BRANCH_OUTPUT=<branch>/output/code-analyzer/

CENTRAL_PERSISTENT_SCOPE=USER_INTENT_AND_CONFIG_ONLY
BRANCH_OUTPUT_SCOPE=SOURCE_DERIVED_ANALYSIS

LEGACY_SOURCE_WRITE=NO
LEGACY_SOURCE_DELETE=NO
AUTO_CONFLICT_OVERWRITE=NO
ANALYSIS_ARTIFACT_CENTRAL_COPY=NO

BASH_USE=NO
POWERSHELL_OR_PYTHON_ONLY=YES
```

중앙 persistent에 취합하는 대상은 오직:

```text
1. inventory inclusion policy
   ACTIVE / EXCLUDED / PURGED

2. explicit build-option source registration
   option_source_config.json
```

중앙화하지 않는 것:

```text
code_analysis_manifest.json
scopes/
patches/
structure_*.json
procedure_runtime_index.json
analysis_progress.md
HLD
MSC
flows_*.json
features/
inventory session JSON
inventory events/backups
branch_build_context.json
cmake_inventory.json
path_build_contexts.json
build_context_matrix.json
UT profile
knowledge_bundle.json
knowledge export
request routes
issue handoff
resume state
```

위 항목은 branch/source revision/baseline CL/build context에 종속되므로 기존 branch output에 그대로 둔다.

---

# 1. 설치 버전 확인

먼저 설치된 `code-analyzer`가 정확히 `0.13.20`인지 확인한다.

가능하면 다음 순서로 확인한다.

```text
~/.claude/skills/code-analyzer/VERSION
~/l1sw-skills/private-skills/code-analyzer/
skillsilent manifest
```

기대:

```text
CODE_ANALYZER_VERSION=0.13.20
```

다르면 즉시 중단한다.

---

# 2. 현재 저장 경계 확인

정상 신규 구조:

```text
~/l1sw-data/code-analyzer/
└─ branches/
   ├─ 1800/
   │  └─ preferences/
   │     ├─ inventory_management.json
   │     └─ option_source_config.json
   │
   └─ 1900/
      └─ preferences/
         ├─ inventory_management.json
         └─ option_source_config.json
```

각 branch의 분석 결과는 계속:

```text
<branch>/output/code-analyzer/
```

에 존재해야 한다.

`~/.claude/main/code-analyzer/`는 v0.13.19의 정상 active store가 아니므로 신규 write/active/fallback 대상으로 만들지 않는다.

---

# 3. 기존 branch root Inventory

전체 디스크를 무차별 검색하지 않는다.

우선순위:

```text
1. 현재 working branch root
2. 현재 branch root의 부모 아래 sibling branch
3. 사용자가 이미 운용해온 알려진 L1 branch root
4. 기존 code-analyzer output이 실제 존재하는 root
```

각 후보 branch에 다음 중 하나가 있는지 확인한다.

```text
<branch>/output/code-analyzer/
<branch>/code_analyzer_output/
```

branch별 Inventory를 작성한다.

```text
SOURCE_ID
BRANCH_ROOT
SOURCE_BRANCH
SOURCE_BRANCH_EVIDENCE
PRIMARY_OUTPUT_EXISTS
LEGACY_OUTPUT_EXISTS
INVENTORY_STATE_EXISTS
BUILD_OPTION_CONFIG_EXISTS
ANALYSIS_ARTIFACT_EXISTS
```

`SOURCE_BRANCH`는 v0.13.20의 `store-doctor.branch_scope_key`를 canonical key로 사용하고 아래 근거로 교차 검증한다.

```text
1. branch root의 명확한 4자리 branch token (예: SMP1900 → 1900)
2. 명시적 P4 stream/branch 정보
3. 기존 manifest/scope의 branch metadata
```

`store-doctor.branch_scope_key`와 P4/manifest 근거가 충돌하면 자동으로 다른 값을 선택하지 않는다. `CODE_ANALYZER_BRANCH_KEY`를 장기 운영 환경에 명시적으로 고정할 사유가 있는 경우에만 별도 설정 검토 대상으로 보고, 이 reconcile에서는 BLOCK한다.

불명확하면:

```text
SOURCE_BRANCH=UNKNOWN
RECONCILE=BLOCKED
```

추측 금지.

---

# 4. store-doctor

확인된 각 branch에 대해:

```text
skillsilent run code-analyzer store-doctor -- --branch-root <branch_root>
```

를 실행한다.

확인할 필드:

```text
canonical_root
branch_scope_key
central.inventory_state_exists
central.build_option_config_exists
legacy.inventory_state_exists
legacy.build_option_config_exists
branch_analysis_artifacts_remain_local=true
analysis_artifacts_migrated=false
```

branch key가 예상 branch와 다르면 해당 branch reconcile을 중단한다.

예:

```text
SMP1900 → branch_scope_key=1900
```

---

# 5. Legacy Durable State 분류

과거 branch output에서 다음 두 파일만 migration 대상으로 본다.

```text
<branch>/output/code-analyzer/inventory/inventory_management.json
<branch>/output/code-analyzer/build-context/option_source_config.json
```

구 legacy output에 동일 목적 파일이 실제 존재하면 별도 SOURCE로 inventory하되 자동 추정하지 않는다.

그 외 파일은:

```text
CLASS=BRANCH_LOCAL_ANALYSIS_ARTIFACT
MIGRATE=NO
```

로 분류한다.

특히:

```text
procedure_runtime_index
HLD
MSC
flow
manifest
scope
patch
build-context derived JSON
knowledge bundle
```

을 `~/l1sw-data/code-analyzer/`로 복사하지 않는다.

---

# 6. Source SHA Baseline

migration 대상 파일이 존재하면 실행 전 SHA256을 기록한다.

```text
SOURCE_INVENTORY_STATE_SHA_BEFORE
SOURCE_BUILD_OPTION_CONFIG_SHA_BEFORE
```

Reconcile 이후 동일 SHA인지 검증한다.

```text
SOURCE_CHANGED=NO
```

가 필수다.

---

# 7. Dry-run Reconcile

각 branch별로 먼저:

```text
skillsilent run code-analyzer reconcile-store -- \
  --source <branch_root> \
  --source-branch <verified_branch> \
  --dry-run
```

Windows corporate environment에서는 bash syntax를 그대로 실행하지 말고 PowerShell/직접 argv 형태로 실행한다.

Dry-run 기대:

```text
status=DRY_RUN_READY
source_modified=false
analysis_artifacts_migrated=false
```

다음이면 실제 reconcile 금지:

```text
SOURCE_BRANCH_CONFLICT
INVENTORY_STATUS_CONFLICT
BUILD_OPTION_SOURCE_CONFLICT
ERROR
```

충돌은 자동으로 최신 timestamp를 선택하거나 덮어쓰지 않는다.

---

# 8. 실제 Reconcile

Dry-run PASS branch만:

```text
skillsilent run code-analyzer reconcile-store -- \
  --source <branch_root> \
  --source-branch <verified_branch>
```

수행한다.

취합 대상:

```text
inventory management policy
→ ~/l1sw-data/code-analyzer/branches/<branch>/preferences/inventory_management.json

option source registration
→ ~/l1sw-data/code-analyzer/branches/<branch>/preferences/option_source_config.json
```

분석 산출물:

```text
<branch>/output/code-analyzer/**
```

은 이동하지 않는다.

---

# 9. Inventory Identity 검증

과거 `inventory_management.json`은 procedure identity에 절대 `source_root`가 들어 있었을 수 있다.

v0.13.20 canonical durable identity는:

```text
file_group
+ procedure_slug
```

중심이며 branch는 상위:

```text
branches/<branch_key>/
```

로 분리한다.

따라서:

```text
D:\clientA\SMP1900\...
D:\clientB\SMP1900\...
```

처럼 workspace root가 변경돼도 동일:

```text
branch=1900
file_group=L1/Tx/Tx.cpp
procedure_slug=tx_config
```

이면 동일 durable user policy로 인식되어야 한다.

절대 workspace path를 canonical identity로 다시 넣지 않는다.

---

# 10. Build Option Source 검증

`option_source_config.json`은 중앙 persistent로 이동하지만 options 원문은 복사하지 않는다.

예:

```text
1900.options
```

는 원래 branch 내 상대경로 그대로 유지한다.

중앙에는:

```text
path
digest
enabled
precedence
registered metadata
```

만 저장한다.

실제 build context 계산 결과는:

```text
<branch>/output/code-analyzer/build-context/
```

에 유지한다.

즉:

```text
OPTION_SOURCE_REGISTRATION=PERSISTENT
BUILD_CONTEXT_DERIVATION=BRANCH_LOCAL
```

이다.

---

# 11. Branch / CL 검증

Code Analyzer에서는 분석 결과를 중앙 장기 memory로 통합하지 않는다.

각 분석 산출물의:

```text
branch
baseline_cl
build_context_digest
source provenance
source digest
scope_id
```

를 기존 branch output에서 그대로 보존한다.

1900의 특정 CL 이후 SLTE 변화 등은:

```text
Code Analyzer
→ 해당 branch/CL source 분석

Knowledge Manager
→ 승인 Knowledge의 Branch + CL applicability 관리
```

역할 분리를 유지한다.

따라서 서로 다른 branch output의 분석 결과를 하나의 canonical Code Analyzer Fact DB로 merge하지 않는다.

---

# 12. 기능 검증

각 대표 branch에 대해 최소 다음을 확인한다.

## 12.1 inventory policy

기존 EXCLUDED 항목이 있으면:

```text
inventory
→ EXCLUDED 상태가 중앙 policy를 통해 유지되는지 확인
```

필요하면 restore 후 다시 exclude하는 식의 destructive 검증은 하지 않는다.

read-only inventory 표시를 우선한다.

## 12.2 build option registration

```text
skillsilent run code-analyzer build-option-source-show -- --branch-root <branch>
```

가 중앙 registration을 읽는지 확인한다.

실제 options 파일이 변경된 경우 `CHANGED` 판정은 정상이며 자동 overwrite하지 않는다.

## 12.3 신규 분석 output

작은 read-only 분석/scope smoke를 실행하고 신규 분석 산출물이:

```text
<branch>/output/code-analyzer/
```

에 생성되는지 확인한다.

절대:

```text
~/l1sw-data/code-analyzer/scopes/
~/l1sw-data/code-analyzer/HLD/
~/l1sw-data/code-analyzer/MSC/
```

등을 생성하면 안 된다.

---

# 13. Source NO_TOUCH 재검증

reconcile 전후 SHA를 비교한다.

```text
SOURCE_INVENTORY_STATE_SHA_AFTER
SOURCE_BUILD_OPTION_CONFIG_SHA_AFTER
```

필수:

```text
SOURCE_INVENTORY_STATE_SHA_BEFORE
=
SOURCE_INVENTORY_STATE_SHA_AFTER

SOURCE_BUILD_OPTION_CONFIG_SHA_BEFORE
=
SOURCE_BUILD_OPTION_CONFIG_SHA_AFTER
```

그리고:

```text
LEGACY_SOURCE_MODIFIED=NO
LEGACY_SOURCE_DELETED=NO
```

---

# 14. 최종 결과

PASS 형식:

```text
RESULT=PASS
MODE=CODE_ANALYZER_STORE_RECONCILE

CODE_ANALYZER_VERSION=0.13.20
PERSISTENT_ROOT=~/l1sw-data/code-analyzer

BRANCHES_INVENTORIED=<n>
BRANCHES_RECONCILED=<n>
UNKNOWN_BRANCHES=0

INVENTORY_POLICY_RECONCILE=PASS
BUILD_OPTION_CONFIG_RECONCILE=PASS

ABSOLUTE_WORKSPACE_IDENTITY_REMOVED=YES
SOURCE_BRANCH_PRESERVED=YES

ANALYSIS_ARTIFACTS_MIGRATED=NO
BRANCH_OUTPUT_RETAINED=YES

LEGACY_SOURCE_MODIFIED=NO
LEGACY_SOURCE_DELETED=NO
CONFLICTS=0

INVENTORY_READ_SMOKE=PASS
BUILD_OPTION_SHOW_SMOKE=PASS
BRANCH_OUTPUT_SMOKE=PASS

MAIN_AS_ACTIVE_STORE=NO
OUTPUT_AS_LONG_TERM_MEMORY=NO
CENTRAL_PERSISTENT_SCOPE=USER_INTENT_AND_CONFIG_ONLY

READY_FOR_NEXT_PRIVATE_SKILL=YES
```

FAIL:

```text
RESULT=FAIL
MODE=CODE_ANALYZER_STORE_RECONCILE
FAILED_CHECKS=<list>
BLOCK_REASON=<reason>
LEGACY_SOURCE_MODIFIED=YES/NO
ANALYSIS_ARTIFACTS_MIGRATED=YES/NO
NEXT_STEP=REPAIR_CODE_ANALYZER_STORE_RECONCILE
```

---

# 15. Cleanup 금지

이 단계에서 삭제하지 않는다.

```text
old output/code-analyzer
code_analyzer_output
legacy inventory state
legacy option source config
old HLD/MSC/flow
migration evidence
```

Cleanup은 별도 승인 단계에서만 수행한다.

---

# 16. 최종 운영 구조

```text
[Package]
~/.claude/skills/code-analyzer/

[Implementation]
~/l1sw-skills/private-skills/code-analyzer/

[Durable user state]
~/l1sw-data/code-analyzer/
└─ branches/<branch_key>/preferences/
   ├─ inventory_management.json
   └─ option_source_config.json

[Branch/source-derived analysis]
<branch>/output/code-analyzer/
├─ code_analysis_manifest.json
├─ scopes/
├─ patches/
├─ source-relative analysis folders/
├─ features/
├─ inventory sessions/events/backups/
├─ build-context derived data/
├─ ut-structure/
└─ knowledge export bundles
```

핵심:

```text
USER_INTENT_AND_CONFIG
→ CENTRAL

SOURCE_DERIVED_ANALYSIS
→ BRANCH OUTPUT

APPROVED_DOMAIN_KNOWLEDGE
→ SLTE KNOWLEDGE MANAGER
```
