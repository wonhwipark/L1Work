# 업무 GPT 설계 적용 검토 제안서 — ACE × PEC-HOP × ACON / L1 Knowledge Updater

- 문서: r0001 / 2026-11-18 KST
- 대상: 업무 GPT와 실제 설치된 l1-knowledge-updater의 담당자
- 목적: 기존 L1 지식 업데이트 기능에 장기 맥락·근거 보존·실패 기반 입력 개선을 최소 변경으로 적용 가능한지 설계 검토
- 단계: DESIGN_PROPOSAL_FOR_BUSINESS_GPT_REVIEW / READ_ONLY_G0_REQUIRED
- 범위: 설계·실제 설치본 읽기 전용 조사·피드백 회신. 코드 변경·설치·저장소/지식 쓰기·그룹 게시·모델 유료 호출·Job 실행·승인 변경 지시가 아님.
- 선행 연결: [기존 Knowledge Updater 개인/그룹 동기화·충돌 상세 인계](L1_KNOWLEDGE_UPDATER_R1_G0_DETAILED_HANDOFF_r0002_20261117_KST.md). 이전 설계 R1의 ACCEPT_WITH_CHANGE는 해당 선행 주제에만 적용, 이번 새 설계의 독립 리뷰/실제 적용 완료 근거가 아님.

## 1. 배경과 검토 방향

지금의 지식 업데이트 목표는 기존 업무 Work와 Evidence의 원본을 보존하고, 개인 Knowledge 후보를 검토한 다음 검증되고 승인된 내용만 그룹 정본에 반영하는 것. 새 지식 DB/원장/자동 검색 엔진을 추가하기보다 기존 Updater·Workflow·Kernel·Analyzer·Converter·Git/P4 writer를 REUSE → CONNECT → 입증된 gap만 최소 EXTEND 순서로 검토.

- ACE(Agentic Context Engineering): 전체 지침 재요약 대신 Work·지식 항목별로 결정/실패/최신 상태를 선별하고 갱신 이력을 보존하는 원리
- PEC-HOP(MCE-Compass): 압축된 입력에서도 증거의 원문·근거 식별자·적용 문맥을 보존하는 원리
- ACON: 원본은 성공했지만 압축 입력에서 실패한 사례를 재현하고 보존 규칙을 개선하는 원리

위 세 기술의 특정 논문 성능을 현재 한국어 L1 환경 성능으로 가정하지 않음. 논문 알고리즘의 전면 구현 요청이 아닌 기존 기능에 대한 설계 적용성 평가.

## 2. 수정하지 않아야 할 기존 책임

| 구성 | 유지할 책임 | 이번 검토에서 확인할 점 |
|---|---|---|
| l1-fix-workflow | 기존 Work 선택/재개·업무 결과 조정; 개인 knowledge/는 READ_ONLY | Work 재개 입력에 기존 결정/근거를 선택할 수 있는가 |
| work-ledger-kernel | Work/Evidence·결정/이력 정본 및 허용 writer | 추가 자료를 기존 Work 기록으로 보존 가능한가; Knowledge ref_type을 임의 발명하지 않는가 |
| code-analyzer, issue-analyzer | 현재 코드 사실·실제 로그 근거·원인 가설과 확인 분리 | source revision, file:line, 함수/IPC, 분석 범위와 증거 신뢰도 반환 가능 여부 |
| doc-converter, hld-composer | 근거가 확인된 fact/semantic input을 HLD/MSC로 변환·표현 | 원본 PUML/MD와 HTML/SVG, source trace 및 AS-IS/TO-BE 분리 |
| l1-github, P4 provider | Git commit/PR·P4 CL·origin/landed revision 조회, 승인된 writer | 검증된 source pin 및 원격 readback; 직접 Git 우회와 권한 실제 보호 |
| l1-knowledge-updater | 독립 Procedure/Feature 조사 또는 기존 Work 지식화, 개인 후보·Preview/그룹 writer 조정 | 실제 설치본 I/O/호출/권한 및 어느 단계에만 얇은 연결이 필요한가 |
| 그룹 Knowledge writer | 검증·승인된 그룹 정본 변경, 기준 revision·중복·충돌/게시 확인 | 실제 계약/권한이 있는지 확인하기 전 신규 구현 금지 |

## 3. 제안 A — ACE 원리: 기존 Work와 Knowledge 지침의 선택적 갱신

제안 흐름: 요청 범위/실제 source revision 확인 → 기존 Work와 Knowledge의 관련 기록만 읽기 → 최신 승인된 결정·예외·미해결·근거/검증 등급을 작은 읽기 전용 패킷으로 묶음 → 분석/검토 후 검증된 교훈만 원래 Work/후보에 연결 → 기존 writer와 승인 절차를 통해 필요한 결과만 갱신.

- Work 없는 순수 Knowledge 조회/편집에 새 Work ID를 강제하지 않음.
- 코드 분석 등 실제 Work가 있을 때는 기존 ID와 Evidence를 재사용. 새 원장/Kernel Profile/metadata enum 추가 금지.
- 과거 결정/교훈을 자동 확정하지 않고, 폐기 결정과 최신 결정이 충돌하면 최신 실제 근거와 사용자 판정이 우선.
- 기존 개인 knowledge/ 내용을 Workflow가 직접 수정하지 않음. Updater가 유일한 지식 WRITE 요청자이며 실제 하드 권한은 G0로 따로 확인.
- 수용 기준: 동일 Work 5회 갱신 중 필수 규칙 누락 0·폐기된 결정 부활 0·무승인 write 0.

## 4. 제안 B — PEC-HOP 원리: 증거 보존형 업무 GPT 입력 묶음

별도 지식 API·데이터베이스 신설 대신 기존 producer의 결과에서 선택된 증거만 텍스트 표현으로 연결.

| 전달 내용 | 필요한 실제 확인 |
|---|---|
| 업무 요청의 정확한 의미 | Module/Procedure/Feature/Scenario, Work ID가 있을 때만 origin |
| 근거 식별자 | 기존 Evidence/Fact ID, 파일·함수/IPC·라인 또는 정확한 문서 절 |
| 고정 source | Git commit/P4 CL·실제 revision, branch·scope, 미검증 dirty 여부 |
| 원문 발췌 및 문맥 | 권한 내 최소 발췌·주변 적용 조건·부정/예외 조건, 해석과 구별 |
| 주장 상태 | 현재 코드/로그 관측·원인 가설·검증 사실·TO-BE 설계를 구분 |
| 후보/게시 연결 | 개인 Knowledge 후보 ID, 그룹 기존 ID·variant, 승인·게시 revision |
| 미확인 항목 | stale revision, 접근/원문 누락, 증거 불충분, 충돌/정보등급 |

- 원문 발췌는 실제 업무 호스트/업무 GPT에서만 허용된 소스 사용. 공개 전달 문서에는 코드·고객 로그·상세 MSC 원문을 담지 않음.
- 링크만 있고 업무 GPT가 접근하지 못하는 경우 자료를 읽은 척하지 않음. 전달 가능한 비민감/승인된 원문 발췌를 포함하거나 미확인 표시.
- source pin이 다르면 기존 Evidence를 현재 코드 사실로 승격하지 않음.
- 증상→원인→해결에서 원인 추론·코드 diff·시험은 서로 다른 Evidence로 표시. 기존 Group Knowledge의 예상 정상 흐름만으로 실제 장애 원인을 확정하지 않음.
- 수용 기준: 실제 함수/API/IPC/수치/branch/부정 조건 변형 0, 근거 없는 Cause 확정 0, 미접근 자료 읽었다는 주장 0.

## 5. 제안 C — ACON 원리: 실패 사례에 한정한 압축 개선

원본 입력·기존 압축 입력·개선 압축 입력의 결과를 비교. 원본은 성공했지만 압축본에서만 증거가 소실되어 실패했다는 사실이 재현된 경우에 한해 보존 규칙 개선 후보 작성.

- 모델 설정·소스 revision·업무 환경 변화로 발생한 실패를 압축 실패로 오인하지 않음.
- 기존 Work의 피드백·결정/시험 이력을 사용하고 새로운 상시 학습/자동 프롬프트 수정 시스템을 만들지 않음.
- 개선에 사용하지 않은 별도 사례로 재검증. 정확성·근거 보존 PASS 후 토큰 수 감소를 평가.
- 기존 source pin/승인/게시/중복 차단은 결정형 검증을 유지하고 모델 출력으로 대체 금지.

## 6. 반드시 보존할 기존 L1 지식 처리 계약

A. Updater 직접 조사: 관련 Work가 필요할 때만 기존 선택/재개·허용 생성 경로 → 기존 Analyzer/Converter 분석 또는 유효 Evidence 재사용 → 원본/분석 이력은 기존 Kernel 허용 Work writer로 기록 → 개인 knowledge/ 후보·Preview.

B. Workflow 기존 Work 지식화: 현재 Work ID/Evidence/source revision 사용 → Updater는 후보만 생성·기존 그룹 지식과 대조 → 승인된 경우에만 그룹 writer를 통하여 게시 → 그룹 원격 revision/readback → 지원되는 범위에서 원 Work 연결.

그룹 Base/Ours/Theirs·latest HEAD/CAS·rename/move/delete 구조 충돌 HOLD, 사용자 승인, 응답 유실 시 재게시 금지, 이미 게시된 건의 상태/Work 역링크만 선택적 복구는 기존 선행 설계를 그대로 유지. Work-side Knowledge backlink의 기존 Kernel API는 정적 검토상 미확인이므로 임의 ref_type 확장 금지. 업무 GPT의 실제 G0 검증이 먼저.

## 7. 업무 GPT에 요청하는 READ_ONLY G0 설계 리뷰

실제 설치된 l1-knowledge-updater 및 기존 연결 스킬의 SKILL.md/구현/허용 action/출력 sample/그룹 writer 계약을 확인해 다음 항목을 수행해 주세요.

1. 최신 설치본 버전·실제 source path·주요 action/호출 계약을 표기. 가정과 실제 확인을 구별.
2. ACE context packet에 필요한 결정/미해결/기존 기록·중복 정리 기능의 재사용 가능성과 gap 판단.
3. PEC 근거 packet의 원문 보존에 사용 가능한 현재 Fact/Evidence ID, source hash/revision, 검색/원문 접근·추출 함수/출력과 한계 확인.
4. ACON 회귀 비교를 기존 시험/피드백 경로에서 구현 없이 수행 가능한지 확인.
5. 기존 개인 knowledge/ Updater 단독 writer·Workflow read-only, raw Git·동일 credential 우회·동시 실행 lock/CAS의 실제 보호 범위 확인.
6. 그룹 지식 Base/Ours/Theirs·승인 Preview·원격 readback·부분 실패 복구 기능을 기존 원문에서 확인. 이번 설계만으로 그룹 쓰지 않기.
7. 새 API/새 필드/별도 Prompt Memory DB 없이 해결 가능한 최소 변경안을 파일·함수·입력/출력 단위로 비교.
8. 변경이 불필요한 스킬은 명확하게 NO_CHANGE/REUSE로 판정. 검증할 수 없는 것은 BLOCKED/NOT_VERIFIED.

## 8. 회신 형식과 리뷰 수락 조건

한국어로 다음 표를 작성:
| 항목 | 설치본 경로/버전·근거 | 현재 구현 사실 | REUSE/CONNECT/EXTEND/NOT_VERIFIED | 최소 설계 제안 | 시험/위험 |
그리고 ACE / PEC-HOP / ACON 각각에 대해 **수용/수정 수용/보류/거절** 및 실제 근거·잠재 반례·단순화 가능성, 추가 확인 하나를 기록.

검증 기준: 기존 근거/결정·Source Revision 무손실, 미승인 쓰기 0, 과거 사례를 현재 fact로 승격 0, 기존 Knowledge 원격 충돌·다른 담당자 변경 무손실, 업무 GPT 텍스트 전달시 근거 위치 소실 0. 설계 리뷰 PASS는 설치/실행/Knowledge 게시 PASS가 아님.

**이번 요청은 검토·회신만입니다.** 실제 코드 변경/시험 실행/그룹 Knowledge 게시/운영 설치/Job/새 유료 모델 리뷰·승인/키·토큰 변경은 여기서 시작하지 마세요. 기존 업무 인계 r0002의 실제 G0 점검과 중복 조사하지 말고 확인된 항목은 근거를 재사용하세요.


## 9. 2026-11-18 KST — ACE·PEC-HOP·SAFE 실제 Linux 설치본 G0 읽기 전용 원샷

### 상태·책임 및 적용 경계

- 최신 사용자 지시: ACE/PEC-HOP/SAFE 합성 설계시험과 CoWork PRIVATE 개발 후보의 실제 소스 정적 G0 이후, **업무 GPT/허용된 Linux Agent의 실제 설치본 G0**를 이어서 수행. 이 항목은 앞의 7~8절 G0에 추가되는 **한정된 확인 절차**이며 새 Work/스킬/Writer를 만들지 않는다.
- 선행 증거: CoWork 기존 Work `COWORK-SKILL-DISCOVERY-20261112-001`의 `GPT_ACE_PEC_SAFE_SOURCE_G0_INTERFACE_MAPPING_r0001_20261118_KST.md`. 개발 후보 `l1-fix-workflow 1.6.70`, `work-ledger-kernel 0.7.43`, `code-analyzer 0.15.3`의 일부 소스는 GPT가 직접 열어 **SOURCE_CANDIDATE_G0=PASS_SCOPE_LIMITED** 확인. 이는 설치/활성 버전 확인이 아니며 실제 함수 실행 결과도 아니다.
- CoWork 합성 계약 26/26 PASS는 **순수 함수 oracle**의 결과일 뿐 실제 업무 스킬 통합 시험 결과가 아니다. `UPDATER_HOST_G0`는 별도로 업무 GPT가 확인한다.
- 이번 수행 허용 범위: 실제 설치 경로·버전·원본 파일 digest·함수 정의·기존 reader/검증기 권한·적합한 **이미 존재하는 승인된 비민감 synthetic fixture**의 무변경 여부를 읽기 전용으로 조사. 스킬/지식 수정, `apply=True`, 모듈 재설치, Git/P4 push, Group Knowledge 쓰기, 예약/Job/모델 실행, 서비스 개방, 신규 유료 리뷰, CoWork REQUEST/READY 생성 **금지**. 만약 기존 fixture/허용 registry가 없으면 실제 호출 시험을 강행하지 않고 `NOT_RUN`.
- 여기의 `python -B`는 실제 설치 Python 모듈을 **import하지 않고 AST로 읽기만 하는 1차 점검용**. 이 문서의 게시나 GPT 응답 자체는 Linux Agent를 시작하지 않으며 실제 호스트 실행/인증은 업무 GPT가 기존 허용된 Linux MCP/Agent 경로로 수행해야 한다.

### 9.1 업무 GPT가 먼저 수행할 설치본 READ_ONLY 원샷

1. 실제 Linux 환경의 허용된 스킬 발견/설치 상태 조회 기능으로 `l1-fix-workflow`, `work-ledger-kernel`, `code-analyzer`, `l1-knowledge-updater`의 **활성 설치본** 디렉터리·SKILL.md 버전/원본 revision/설치 해시/호출 가능 provider를 확인. 공개 릴리스와 PRIVATE 개발 후보 번호를 현재 설치 버전으로 추정하지 않음. Agent에 업무 폴더 전체 검색이나 민감 파일 출력 요청 금지.
2. 아래 probe의 `WORKFLOW_ROOT`, `KERNEL_ROOT`, `ANALYZER_ROOT`에는 **각 스킬의 실제 설치 root**(예: 하위 `l1_fix_workflow/`, `work_ledger_kernel/`, `scripts/ca_core/`가 존재하는 부모)만 입력. stdout에 절대 경로·회사 코드·Evidence 원문은 출력하지 말고 별칭/상대 경로·SHA만 회신. 설치본 경로 또는 스킬 이름을 확인할 수 없으면 `NOT_VERIFIED`로 보고하고 자동 설치/탐색 범위 확대 금지.
3. 다음 코드는 stdlib AST와 SHA-256만 사용하고 **실제 설치 모듈을 import하거나 실행하지 않는다**. UTF-8 파일을 검사하는 동안 pycache 쓰기를 피하기 위해 `-B` 사용. 원본이 symlink/누락/파싱 불가면 FAIL_CLOSED/`NOT_VERIFIED`.

```bash
# 실제 설치 root는 업무 GPT/허용된 Agent가 확인한 값으로만 지정
: "${WORKFLOW_ROOT:?verified workflow skill root required}"
: "${KERNEL_ROOT:?verified kernel skill root required}"
: "${ANALYZER_ROOT:?verified analyzer skill root required}"
PYTHONDONTWRITEBYTECODE=1 python3 -B - "$WORKFLOW_ROOT" "$KERNEL_ROOT" "$ANALYZER_ROOT" <<'PY'
import ast
import hashlib
import json
import pathlib
import sys

CHECKS = {
    "workflow": [
        ("l1_fix_workflow/work_inspection.py", "inspect_work"),
        ("l1_fix_workflow/feature_evidence.py", "attach_evidence"),
        ("l1_fix_workflow/work_router.py", "DeterministicWorkRouter.handle"),
    ],
    "kernel": [
        ("work_ledger_kernel/continuity.py", "TLContinuity.resume"),
        ("work_ledger_kernel/work_refs.py", "WorkReferences.read"),
        ("work_ledger_kernel/validation.py", "validate_evidence_meta"),
        ("work_ledger_kernel/storage.py", "LedgerStorage.__init__"),
    ],
    "analyzer": [
        ("scripts/ca_core/reuse_validator.py", "validate"),
        ("scripts/ca_core/provenance_resolver.py", "resolve"),
    ],
}
def symbols(tree):
    found = {}
    for item in tree.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            found[item.name] = item
        elif isinstance(item, ast.ClassDef):
            for child in item.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    found[item.name + "." + child.name] = child
    return found

results = []
for role, value in zip(CHECKS, sys.argv[1:]):
    root = pathlib.Path(value).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise SystemExit("HOLD: verified root is not a directory")
    for relative, symbol in CHECKS[role]:
        candidate = root / relative
        row = {"role": role, "module": relative, "symbol": symbol}
        if candidate.is_symlink() or not candidate.is_file():
            row["status"] = "NOT_VERIFIED"
        else:
            try:
                raw = candidate.read_bytes()
                tree = ast.parse(raw, filename=relative)
                found = symbols(tree)
                row["sha256"] = hashlib.sha256(raw).hexdigest()
                row["status"] = "PRESENT" if symbol in found else "NOT_VERIFIED"
                if symbol == "LedgerStorage.__init__" and symbol in found:
                    row["calls_mkdir"] = any(
                        isinstance(n, ast.Call) and
                        isinstance(n.func, ast.Attribute) and
                        n.func.attr == "mkdir"
                        for n in ast.walk(found[symbol])
                    )
            except (OSError, SyntaxError, UnicodeError):
                row["status"] = "NOT_VERIFIED"
        results.append(row)
print(json.dumps(results, ensure_ascii=False, indent=2))
if any(r["status"] != "PRESENT" for r in results):
    raise SystemExit(2)
PY
```

**주의:** `PRESENT`는 함수 정의가 소스에 있다는 사실만 확인하며, 실제 runtime import/호출 가능 또는 권한/무변경 보증이 아니다. `calls_mkdir=true`면 이미 소스에서 확인된 Kernel 초기화 부수효과 위험을 보여준다. 결과에 출력되지 않는 writer/Agent 자동 작업이나 하위 호출까지 검증한 것으로 취급하지 않는다.

### 9.2 실제 읽기 전용 fixture 시험 — 전제 통과 때만

- 업무 GPT가 **이미 존재하며 사용이 승인된 비민감 synthetic Work/Evidence fixture**와 기존 provider registry/profile을 확인한 뒤, 실제 설치 모듈을 이용한 `inspect_work`, `TLContinuity.resume`, `attach_evidence(..., apply=False)`를 순서대로 실행할 수 있는지 판정. 미확인 API/빈 Work에 새로운 Work ID를 임의 생성하거나 실제 회사 Work를 fixture로 쓰지 않음.
- 호출 전·후 **해당 fixture 전체**의 상대 파일/디렉터리 목록·파일 크기·SHA-256·mtime/ctime을 비교. 생성·수정·삭제가 하나라도 있으면 `FAIL_SIDE_EFFECT`, 비교/권한 불가면 `NOT_RUN`. atime은 읽기만 해도 파일시스템에 따라 변할 수 있으므로 무변경 판정의 유일한 기준으로 삼지 않음. 업무 Workspace 원본/시스템 설정에는 실행하지 않음.
- `LedgerStorage.__init__`은 `root.mkdir(parents=True, exist_ok=True)` 가능성이 확인됐으므로, **기존 fixture root가 실제 존재할 때만** 시험. root 미존재로 인한 자동 디렉터리 생성은 읽기 전용 PASS가 아니다.
- **ACE-02:** 원본 결정 append/revision·승인 범위·철회 이력이 실제 reader 출력/정본에서 보존되는지 비교. `brief.decisions`의 `ref/date=None` 요약값만 있으면 최신 결정 확정 불가 → `HOLD`.
- **PEC-01/03:** 기존 Evidence `sha256`이 **전체 파일 digest**인지 확인한 뒤, 발췌의 `byte_offset/length`가 원본 provider 출력에 존재하는지 확인. 명확한 바이트 범위와 동일 revision이 있으면 원문 raw bytes와 발췌 raw bytes의 SHA-256을 fixture에서만 대조하고 1바이트 오염의 FAIL/HOLD를 확인. byte range/인코딩/원본 권한 불명확하면 `NOT_VERIFIED/HOLD`; 원본 속성을 새 Kernel 필드로 추가하지 않음.
- **SAFE-01/03:** `apply=True` 금지, 검증 작업 중 파일/디렉터리 변경·Group write·Git/P4 publish·Watcher REQUEST/READY·모델 호출·Job/Agent 자동 시작 모두 0 확인. 기존 R1 완료 리뷰는 재큐잉하지 않음. 실행중 부수효과 감시 근거가 없으면 단순 파일 diff만으로 watcher/모델 호출 0을 보증했다고 주장 금지.
- 위 중 하나라도 설치 경로·함수 존재·fixture·권한 경계가 미확인이면 **거기서 중단**하여 해당 항목만 `NOT_RUN/BLOCKED`로 기록. 이미 가능한 정적 G0 조사·비민감 회신은 계속.

### 9.3 단일 비민감 회신(동일 기존 Work에 연결)

업무 GPT는 기존 검토 7~8절과 중복 수행하지 말고 실제 이번에 확인된 델타만 다음 표로 한 번 회신:

| 항목 | 요구 회신 |
|---|---|
| 설치본/활성 provider | 스킬 4종별 실제 버전·설치 경로 **별칭**·SKILL/기능 파일 SHA/실행 인터페이스; 코드·절대 경로 본문 금지 |
| ACE-02 | `SOURCE_STATIC/ACTUAL_FIXTURE=PASS/FAIL/NOT_RUN`, 결정 원본 순서·승인 근거 보존, HOLD 반례 |
| PEC-01/03 | preview`(apply=False)` 결과, 전체 파일 SHA vs byte-range SHA 경계, 1-byte 오염/누락 시 결과 |
| SAFE-01/03 | fixture 사전/사후 트리 digest 동일성·측정 대상/확인 불가 항목; 신규 모델/Job/READY 발생 여부는 **실제 로그 확인 여부**와 함께 보고 |
| Updater/그룹 | 실제 Knowledge Updater 설치/Writer 및 그룹 게시 계약 **읽기 전용 G0**; 최신 개인 Knowledge 관리 전담 결정(기존 15절) 유지 |
| 판정 | 항목별 `PASS/FAIL/SKIP/NOT_RUN`, REUSE/CONNECT/입증된 gap만 EXTEND 후보, 잔여 차단·최소 다음 동작 |

현재 이 문서 추가는 `HANDOFF_UPDATED`일 뿐 `LINUX_HOST_G0=NOT_RUN`. 업무 GPT 회신 전에는 실제 통합 기능의 PASS/배포 가능 판정을 내리지 않는다. 리뷰 R1은 **CLOSED_NO_AUTOMATIC_REREVIEW**, ACON 모델 3+3 시험은 별도 유효 권한·예산 확인 전 **NOT_RUN**.
