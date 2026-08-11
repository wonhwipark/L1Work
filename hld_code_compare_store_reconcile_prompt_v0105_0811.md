# hld-code-compare v0.10.5 Storage Reconcile / Legacy Output Adoption Prompt

아래 절차를 회사 PC의 OpenCode/Claude Code에서 수행하라.
Windows 환경이므로 **bash를 사용하지 말고 PowerShell 또는 등록된 skillsilent action만 사용**한다.

## 목표

`hld-code-compare`는 장기 Persistent Store를 만들지 않는다.

```text
LONG_TERM_PERSISTENT=NONE
CANONICAL_OUTPUT=<working_branch_root>/output/hld-code-compare/
LEGACY_OUTPUT=<working_branch_root>/hld_compare_output/
LEGACY_OUTPUT_MODE=READ_ONLY
MAIN_ACTIVE_STORE=NO
L1SW_DATA_STORE=NO
```

과거 `hld_compare_output/`에 진행 중이거나 보존할 Gap run이 있을 때만 원본을 유지한 채 canonical output으로 missing-only adoption한다.

## 절대 금지

- `~/.claude/main/hld-code-compare/`를 신규 저장소로 만들지 않는다.
- `~/l1sw-data/hld-code-compare/`를 만들지 않는다.
- legacy source를 수정/삭제/rename/move 하지 않는다.
- conflicting file을 자동 overwrite 하지 않는다.
- 다른 branch의 output을 현재 branch에 합치지 않는다.
- Code Analyzer output을 복사하지 않는다.

## STEP 1 — 현재 스킬 확인

```text
EXPECTED_VERSION=0.10.5
```

`skillsilent run hld-code-compare help -- --json`으로 등록 action과 version을 확인한다.

실패하면 중단:

```text
RESULT=FAIL
FAILED_STEP=VERSION_CHECK
```

## STEP 2 — 현재 branch storage doctor

현재 working branch root를 `<BRANCH_ROOT>`로 확정한다.

```powershell
skillsilent run hld-code-compare store-doctor -- --cwd "<BRANCH_ROOT>" --json
```

확인:

```text
LONG_TERM_PERSISTENT=NONE
CANONICAL_OUTPUT_ROOT=<BRANCH_ROOT>/output/hld-code-compare
LEGACY_WRITE_ALLOWED=FALSE
MAIN_ACTIVE_STORE=FALSE
CENTRAL_PERSISTENT_STORE=FALSE
```

## STEP 3 — Legacy 존재 여부 판정

`LEGACY_FILES=0`이면 adoption은 수행하지 않는다.

```text
LEGACY_ADOPTION=NOT_NEEDED
```

`LEGACY_FILES>0`이면 다음으로 진행한다.

## STEP 4 — Read-only legacy adoption

```powershell
skillsilent run hld-code-compare adopt-legacy-output -- --cwd "<BRANCH_ROOT>" --json
```

필수 조건:

```text
SOURCE_UNCHANGED=TRUE
LEGACY_DELETE=FALSE
LEGACY_WRITE=FALSE
CONFLICTS=0
```

충돌 발생 시 자동 해소하지 않는다.

```text
RESULT=FAIL
FAILED_STEP=LEGACY_ADOPTION
BLOCK_REASON=LEGACY_OUTPUT_CONFLICT
```

## STEP 5 — Resume routing 확인

기존 HLD slug 중 하나를 `<HLD_SLUG>`로 선택한다.

```powershell
skillsilent run hld-code-compare output-resolve -- --cwd "<BRANCH_ROOT>" --hld-slug "<HLD_SLUG>" --intent resume --json
```

PASS 조건:

```text
ACTIVE_OUTPUT_ROOT=<BRANCH_ROOT>/output/hld-code-compare
PATH_MODE=PRIMARY_RESUME
LEGACY_ADOPTION_REQUIRED=FALSE
```

legacy root가 active output으로 반환되면 FAIL.

## STEP 6 — Artifact 무결성 확인

canonical output에서 아래를 inventory한다.

```text
gap_report_*.yaml
gap_summary_*.md
_ca_v2/
_ownership/
confluence publish state (존재 시)
legacy adoption manifest (adoption 수행 시)
```

이 데이터는 **branch/source-specific run evidence**이며 중앙 Persistent로 이동시키지 않는다.

## STEP 7 — 최종 결과

PASS 출력:

```text
RESULT=PASS
MODE=HLD_CODE_COMPARE_STORAGE_RECONCILE
SKILL_VERSION=0.10.5
LONG_TERM_PERSISTENT=NONE
CANONICAL_OUTPUT_ONLY=YES
LEGACY_SOURCE_READ_ONLY=YES
LEGACY_SOURCE_CHANGED=NO
LEGACY_SOURCE_DELETED=NO
CONFLICTS=0
MAIN_ACTIVE_STORE=NO
L1SW_DATA_STORE=NO
READY_FOR_NORMAL_USE=YES
```

FAIL은 정확한 단계와 이유를 출력하고 중단한다.
