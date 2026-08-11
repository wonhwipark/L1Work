# hld-code-implement v0.5.10 Storage Reconcile / Legacy Output Adoption Prompt

회사 PC의 OpenCode/Claude Code에서 수행하라.
Windows 환경이므로 **bash를 사용하지 말고 PowerShell 또는 skillsilent action만 사용**한다.

## 목표

`hld-code-implement`의 run 상태와 diff/rollback/shelve/HLD amendment는 branch/source/approval에 종속된 실행 증거다.
따라서 장기 Persistent Store로 중앙화하지 않는다.

```text
LONG_TERM_PERSISTENT=NONE
CANONICAL_OUTPUT=<working_branch_root>/output/hld-code-implement/
LEGACY_OUTPUT=<working_branch_root>/output/hld-implementation/
LEGACY_OUTPUT_MODE=READ_ONLY
MAIN_ACTIVE_STORE=NO
L1SW_DATA_STORE=NO
```

## 절대 금지

- `~/.claude/main/hld-code-implement/`에 신규 state를 쓰지 않는다.
- `~/l1sw-data/hld-code-implement/`를 만들지 않는다.
- legacy output을 수정/삭제하지 않는다.
- run manifest/G2 snapshot/diff를 다른 branch와 합치지 않는다.
- source code 변경은 기존 G1/G2 승인 계약을 우회하지 않는다.
- P4 submit은 수행하지 않는다.

## STEP 1 — Version / action 확인

```text
EXPECTED_VERSION=0.5.10
```

skillsilent 등록 action에서 `store-doctor`, `adopt-legacy-output`, 기존 HCI action을 확인한다.

## STEP 2 — 현재 branch doctor

`<BRANCH_ROOT>`를 현재 working branch root의 절대경로로 확정한다.

```powershell
skillsilent run hld-code-implement store-doctor -- --root "<BRANCH_ROOT>" --json
```

확인:

```text
LONG_TERM_PERSISTENT=NONE
CANONICAL_OUTPUT_ROOT=<BRANCH_ROOT>/output/hld-code-implement
LEGACY_WRITE_ALLOWED=FALSE
MAIN_ACTIVE_STORE=FALSE
CENTRAL_PERSISTENT_STORE=FALSE
```

## STEP 3 — Legacy output 판정

`<BRANCH_ROOT>/output/hld-implementation/`에 파일이 없으면:

```text
LEGACY_ADOPTION=NOT_NEEDED
```

파일이 있으면 다음 단계 수행.

## STEP 4 — Read-only adoption

```powershell
skillsilent run hld-code-implement adopt-legacy-output -- --root "<BRANCH_ROOT>" --json
```

PASS 조건:

```text
SOURCE_UNCHANGED=TRUE
LEGACY_DELETE=FALSE
LEGACY_WRITE=FALSE
CONFLICTS=0
```

conflict 시 자동 overwrite/merge 금지.

## STEP 5 — Canonical run inventory

`<BRANCH_ROOT>/output/hld-code-implement/` 하위에서 다음을 확인한다.

```text
run_manifest.yaml
_run_baseline/
_g2/
g2/
impl_records/
run.diff
impl_log.md
shelve_ledger.json
cl_handoff.json
hld/
hld_amendments/
build_recovery/
```

존재 여부는 run 단계에 따라 다를 수 있다.
이들은 모두 branch/run evidence이며 중앙 persistent로 옮기지 않는다.

## STEP 6 — Run root boundary smoke

새로운 synthetic/read-safe 준비 테스트를 수행할 수 있으면 canonical run dir만 사용한다.

```text
<BRANCH_ROOT>/output/hld-code-implement/<run-id>/
```

canonical 밖의 `--run-dir`이 차단되는지 확인한다. 실제 source edit/P4 write 승인은 수행하지 않는다.

PASS:

```text
OUTSIDE_CANONICAL_RUN_DIR_BLOCKED=YES
```

## STEP 7 — Compare legacy dependency 확인

Implement가 gap report를 읽을 때 구 `<BRANCH_ROOT>/hld_compare_output/`을 read-only fallback으로 발견할 수 있다.
가능하면 먼저 `hld-code-compare v0.10.5`의 reconcile/adoption을 수행해서:

```text
<BRANCH_ROOT>/output/hld-code-compare/
```

를 canonical Gap source로 만든다.
Implement가 compare legacy root에 쓰면 FAIL.

## STEP 8 — 최종 결과

```text
RESULT=PASS
MODE=HLD_CODE_IMPLEMENT_STORAGE_RECONCILE
SKILL_VERSION=0.5.10
LONG_TERM_PERSISTENT=NONE
CANONICAL_OUTPUT_ONLY=YES
LEGACY_SOURCE_READ_ONLY=YES
LEGACY_SOURCE_CHANGED=NO
LEGACY_SOURCE_DELETED=NO
CONFLICTS=0
OUTSIDE_CANONICAL_RUN_DIR_BLOCKED=YES
MAIN_ACTIVE_STORE=NO
L1SW_DATA_STORE=NO
SOURCE_EDIT_POLICY=UNCHANGED_G1_G2_APPROVAL
READY_FOR_NORMAL_USE=YES
```
