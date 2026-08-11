# issue-analyzer v0.11.6 Existing Data Inventory / Reconcile Prompt

> 목적: 과거 `issue-analyzer`의 재사용 가치가 있는 데이터를 삭제 없이 취합해
> `~/l1sw-data/issue-analyzer/`를 유일한 branch-independent persistent SSOT로 만든다.
>
> 이 작업은 **기존 branch output을 cleanup하는 작업이 아니다.** 모든 legacy source는 read-only로 유지한다.

## 0. 고정 정책

```text
ISSUE_ANALYZER_VERSION=0.11.6
CANONICAL_PERSISTENT_ROOT=~/l1sw-data/issue-analyzer

NEW_MAIN_WRITE=NO
MAIN_AS_ACTIVE_STORE=NO
MAIN_AS_FALLBACK=NO

NEW_BRANCH_RECORD_WRITE=NO
BRANCH_OUTPUT_AS_RUNTIME=YES
BRANCH_OUTPUT_AS_PERSISTENT_SSOT=NO

LEGACY_SOURCE_DELETE=NO
LEGACY_SOURCE_MODIFY=NO
AUTO_OVERWRITE_CONFLICT=NO
```

신규 저장 역할:

```text
~/l1sw-data/issue-analyzer/
├─ log_manifest/        # 승인된 base + branches/<branch> overlay regex
├─ records/             # case/report/index/recall_index/handoff
├─ migration/
└─ migration-backup/
```

branch output 역할:

```text
<branch>/output/issue-analyzer/
├─ work/<run_id>/       # pipeline/resume/conversion/current analysis
├─ code_map/            # branch-local derived CodeAnalyzer mirror
└─ code_analysis_manifest.json  # legacy v1 fallback only
```

## 1. 절대 금지

- bash 사용 금지. PowerShell 또는 Python/skillsilent만 사용한다.
- 기존 source file/dir을 delete/move/rename/edit하지 않는다.
- `~/.claude/main/issue-analyzer/`에 신규 파일을 쓰지 않는다.
- 과거 `<branch>/output/issue-analyzer/records/`를 신규 SSOT로 계속 사용하지 않는다.
- 서로 다른 내용의 동일 파일명을 자동 덮어쓰지 않는다.
- branch를 경로 문자열만 보고 임의 추정하지 않는다.
- case가 branchless이고 source branch도 검증하지 못했다면 import하지 않는다.
- `index.yaml`, `recall_index.jsonl`은 legacy 내용을 그대로 이어붙이지 않는다. canonical case 기준으로 재생성한다.

## 2. 설치 버전 확인

먼저 `issue-analyzer v0.11.6`이 설치/활성화되어 있어야 한다.

확인:

```text
skillsilent run issue-analyzer help -- --action analyze --json
```

또는 package의 `VERSION.md`, `skillsilent/manifest.json`을 read-only 확인한다.

필수:

```text
VERSION=0.11.6
```

다르면 즉시 중단한다.

## 3. 현재 canonical store doctor

```text
skillsilent run issue-analyzer store-doctor --
```

기록:

```text
CANONICAL_ROOT
CANONICAL_LOG_MANIFEST_FILES
CANONICAL_CASES
CANONICAL_REPORTS
LEGACY_MAIN_SOURCE
```

## 4. Legacy source inventory

다음 후보를 **존재할 때만** read-only inventory한다.

### 4.1 Legacy main

```text
~/.claude/main/issue-analyzer/
```

주요 대상:

```text
log_manifest/
migration/
migration-backup/
records/   # 존재하는 구버전에서만
```

### 4.2 과거 branch-local output

알려진/접근 가능한 각 working branch에 대해:

```text
<branch-root>/output/issue-analyzer/
```

주요 대상:

```text
records/
  case_*.md
  report_*.md
  index.yaml
  recall_index.jsonl
  handoffs/
```

`work/`, conversion log/state, `code_map/`은 현재 단계에서 중앙 persistent로 취합하지 않는다.
이들은 branch-local runtime/derived artifact다.

### 4.3 기타 과거 root

실제로 존재할 때만 다음도 확인한다.

```text
~/issue_analyzer/
<old workspace>/issue_analyzer/
```

단, 파일 구조가 `issue-analyzer` persistent signature와 일치할 때만 source 후보로 등록한다.
임의 폴더를 자동 분류하지 않는다.

각 source에 대해:

```text
SOURCE_ID
SOURCE_ROOT
SOURCE_TYPE=LEGACY_MAIN|BRANCH_OUTPUT|LEGACY_RECORD_ROOT
SOURCE_BRANCH=<verified branch or UNKNOWN>
CASE_COUNT
REPORT_COUNT
LOG_MANIFEST_JSON_COUNT
SOURCE_DIGEST_BEFORE
SYMLINK_FINDINGS
```

을 기록한다.

## 5. Branch provenance 판정

과거 branch output은 path 자체가 branch context 역할을 했으므로 중앙화 전에 branch를 보존해야 한다.

우선순위:

```text
1. case 본문의 branch:
2. source의 code_analysis_manifest / pipeline_state에 기록된 단일 branch
3. 실제 P4/Git working branch 확인
4. 사용자/기존 inventory가 명시한 branch
5. 폴더명은 보조 evidence만 사용
```

판정:

```text
CASE_BRANCH=EXPLICIT
CASE_BRANCH=SOURCE_BRANCH_FALLBACK
CASE_BRANCH=UNKNOWN
CASE_BRANCH=CONFLICT
```

규칙:

- case에 branch가 이미 있으면 그대로 보존한다.
- case가 branchless이고 `SOURCE_BRANCH`가 검증되었으면 canonical copy에만 branch를 추가한다.
- case branch와 `SOURCE_BRANCH`가 다르면 `CONFLICT`이며 자동 import 금지.
- 둘 다 모르면 import 금지.
- legacy source 원문은 절대 수정하지 않는다.

## 6. Legacy main reconcile

존재하면:

```text
skillsilent run issue-analyzer reconcile-store -- \
  --source "~/.claude/main/issue-analyzer"
```

기대:

```text
legacy log_manifest missing-only import
source unchanged
canonical conflict auto-overwrite 없음
```

`issue-analyzer v0.11.6`의 정상 startup도 legacy main `log_manifest`를 missing-only로 읽을 수 있지만,
이 단계에서는 명시적인 migration evidence를 남긴다.

## 7. Branch output records reconcile

각 검증된 branch source에 대해 한 번씩 수행한다.

예:

```text
skillsilent run issue-analyzer reconcile-store -- \
  --source "D:/workspace/SMP1900/output/issue-analyzer" \
  --source-branch "1900"
```

```text
skillsilent run issue-analyzer reconcile-store -- \
  --source "D:/workspace/SMP1800/output/issue-analyzer" \
  --source-branch "1800"
```

동작:

```text
records preflight
→ branch provenance audit
→ filename/content conflict check
→ source read-only digest capture
→ canonical case/report missing-only copy
→ branchless case는 verified source branch만 canonical copy에 보강
→ report pointer는 canonical report path로 정규화
→ canonical index.yaml rebuild
→ canonical recall_index.jsonl rebuild
→ migration evidence 저장
→ source digest after 확인
```

### Conflict 시

다음 중 하나라도 있으면 해당 source reconcile은 FAIL:

```text
same target filename + different content
case branch != verified source branch
branch-local case branchless + source branch UNKNOWN
symlink finding
source path invalid
```

다른 파일로 덮어쓰거나 자동 rename하지 않는다.
충돌 목록만 반환한다.

## 8. Canonical records 검증

모든 정상 source 취합 후:

```text
skillsilent run issue-analyzer store-doctor -- \
  --source "<legacy-source-1>" \
  --source "<legacy-source-2>"
```

확인:

```text
CANONICAL_CASES >= 취합 전
CANONICAL_REPORTS >= 취합 전
index.yaml exists
recall_index.jsonl exists
```

### 대표 과거 이슈 recall

기존 case 3~5건에서 실제 symptom/API/code symbol을 선정해 다음 내부 동작을 확인한다.
정식 사용자 분석을 새로 만들 필요는 없다.

```text
ia_recall.py --records ~/l1sw-data/issue-analyzer/records --query-terms <term> --branch <branch>
```

가능하면 skillsilent 등록 action/정식 pipeline을 우선 사용한다.

검증:

```text
RECALL_OLD_CASE=PASS
SAME_BRANCH_RANKING=PASS
CROSS_BRANCH_REFERENCE_AVAILABLE=PASS
SUPERSEDED_CASE_EXCLUDED=PASS
```

과거 case는 현재 root-cause 증거가 아니라 precedent다. 현재 로그/코드에서 반드시 재검증한다.

## 9. log_manifest 검증

확인:

```text
~/l1sw-data/issue-analyzer/log_manifest/
├─ *.json
└─ branches/
   ├─ 1800/
   └─ 1900/
```

기존 branch overlay가 있으면 branch 이름을 유지한다.
base와 branch overlay를 한 파일로 flatten하지 않는다.

검증:

```text
LOG_MANIFEST_BASE_PRESERVED=YES
LOG_MANIFEST_BRANCH_OVERLAY_PRESERVED=YES
LOG_MANIFEST_SOURCE_MODIFIED=NO
```

## 10. 신규 저장 경계 smoke

격리 테스트 또는 안전한 sample 분석으로 다음을 확인한다.

```text
NEW_RUN_WORK_ROOT=<branch>/output/issue-analyzer/work/<run_id>
NEW_CODE_MAP_ROOT=<branch>/output/issue-analyzer/code_map

NEW_CASE_ROOT=~/l1sw-data/issue-analyzer/records
NEW_REPORT_ROOT=~/l1sw-data/issue-analyzer/records
NEW_RECALL_INDEX=~/l1sw-data/issue-analyzer/records/recall_index.jsonl
NEW_LOG_MANIFEST=~/l1sw-data/issue-analyzer/log_manifest
```

반드시:

```text
NEW_MAIN_WRITE=NO
NEW_BRANCH_RECORD_WRITE=NO
BRANCH_RUNTIME_WRITE=YES
CENTRAL_PERSISTENT_WRITE=YES
```

## 11. 최종 PASS Gate

```text
RESULT=PASS
MODE=ISSUE_ANALYZER_STORE_RECONCILE
VERSION=0.11.6

CANONICAL_PERSISTENT_ROOT=~/l1sw-data/issue-analyzer
LEGACY_MAIN_SCANNED=YES
KNOWN_BRANCH_OUTPUTS_SCANNED=YES

LOG_MANIFEST_RECONCILE=PASS
LEGACY_CASE_RECONCILE=PASS
BRANCH_PROVENANCE_PRESERVED=YES
BRANCH_GUESSED=NO

INDEX_REBUILD=PASS
RECALL_INDEX_REBUILD=PASS
RECALL_OLD_CASE=PASS
SAME_BRANCH_RANKING=PASS

SOURCE_MODIFIED=NO
SOURCE_DELETED=NO
AUTO_OVERWRITE_CONFLICT=NO
NEW_MAIN_WRITE=NO
NEW_BRANCH_RECORD_WRITE=NO

RUNTIME_OUTPUT_ROOT=<branch>/output/issue-analyzer
PERSISTENT_ROOT=~/l1sw-data/issue-analyzer

READY_FOR_NORMAL_OPERATION=YES
```

FAIL:

```text
RESULT=FAIL
MODE=ISSUE_ANALYZER_STORE_RECONCILE
FAILED_CHECKS=<list>
CONFLICTS=<list>
SOURCE_MODIFIED=NO
NEXT_STEP=REPAIR_ONLY_FAILED_SOURCE
```

## 12. Cleanup

이 단계에서는 cleanup하지 않는다.

삭제 금지:

```text
~/.claude/main/issue-analyzer/
<legacy branch>/output/issue-analyzer/records/
legacy migration evidence
```

다음 조건 이후 별도 승인으로 cleanup한다.

```text
reconcile PASS
신규 run smoke PASS
과거 recall PASS
rollback window elapsed
explicit user approval
```
