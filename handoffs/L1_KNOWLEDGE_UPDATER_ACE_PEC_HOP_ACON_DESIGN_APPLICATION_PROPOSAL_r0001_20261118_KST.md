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
if len(sys.argv) != 4:
    raise SystemExit("HOLD: exactly three verified skill roots required")
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
    try:
        root = pathlib.Path(value).expanduser().resolve(strict=True)
        if not root.is_dir():
            raise ValueError("not a directory")
    except (OSError, ValueError, RuntimeError):
        raise SystemExit("HOLD: verified skill root unavailable (path redacted)")
    for relative, symbol in CHECKS[role]:
        candidate = root / relative
        row = {"role": role, "module": relative, "symbol": symbol}
        at = root
        symlink_in_path = False
        for component in pathlib.Path(relative).parts:
            at = at / component
            if at.is_symlink():
                symlink_in_path = True
                break
        if symlink_in_path or not candidate.is_file():
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

**점검 스니펫 자체 QA(업무 호스트가 아닌 격리 합성 환경):** GitHub 본문 내 Python 코드 3,027 B, SHA-256 `9fc117c5754b096f01f98d9130461aa0d92bd469b46b98ae280c63cda2fd024b`; 동일 실제 바이트를 대상으로 구문 파싱/정상 9개 함수/`mkdir` 탐지/모듈 누락/루트 누락 시 경로 비노출/인수 누락/symlink 거부를 실행해 **PASS**. 실제 업무 설치본 함수 실행·권한·부수효과 검증은 **NOT_RUN**.

현재 이 문서 추가는 `HANDOFF_UPDATED`일 뿐 `LINUX_HOST_G0=NOT_RUN`. 업무 GPT 회신 전에는 실제 통합 기능의 PASS/배포 가능 판정을 내리지 않는다. 리뷰 R1은 **CLOSED_NO_AUTOMATIC_REREVIEW**, ACON 모델 3+3 시험은 별도 유효 권한·예산 확인 전 **NOT_RUN**.

## 10. 2026-11-19 KST — 실제 업무 사용·업무 전용 Updater·모바일 수정 요청 협업 경계

### 10.1 사용자 최신 운영 사실과 검증 등급

- **사용자 확인(2026-11-19):** 스킬 패키지는 업무 환경으로 전달되어 실제 업무에 사용되고 있음. 문제 발생 시 사용자는 **모바일에서 수정 요청**하여 기존 협업으로 후속 보완하는 운용 방식을 사용.
- 이는 **USER_CONFIRMED_IN_USE**이며, 개별 스킬별 실제 설치/활성 버전·SHA-256·적용 날짜·호스트 영수증이 자동으로 입증됐다는 뜻은 아님(`ACTIVE_REVISION=NOT_VERIFIED`). GitHub PUBLIC ZIP, CoWork PRIVATE 개발 후보 ZIP, Linux 호스트 설치본을 계속 구별. 스킬이 실제 사용 중이라는 이유로 전체 기능/E2E PASS를 선언하지 않음.
- **`l1-knowledge-updater`는 업무 환경 전용 스킬.** 구현 코드·SKILL.md·업무 Knowledge·로그·경로·회사 소스 원문을 CoWork PRIVATE 또는 L1Work PUBLIC에 옮기지 않음. 원본을 GPT에 제공하는 것을 G0/설계 수락의 필수 조건으로 삼지 않음.
- 업무 GPT와 허용된 Linux Agent/MCP가 현재 환경에서 내부 원본·설치 계약·실제 실행 근거를 확인할 수 있음. GPT는 **업무 GPT의 비민감 결과 요약을 HOST_REPORTED로 수용**해 REUSE/CONNECT/검증된 최소 EXTEND 여부를 판정할 수 있으나, 원본을 직접 검증했다고 소급 보고하지 않음.
- 기존 7~9절의 실제 설치본 G0 요청은 **필요한 미확인 부분만** 수행. 업무 전용 Updater의 raw package/SKILL.md/코드 제출은 요구하지 않음. 이미 실행 중인 정상 스킬을 조사 때문에 재설치하거나 기존 Job을 재실행하지 않음. 확인 불가 항목은 BLOCKED/NOT_VERIFIED로 유지하되 나머지 설계·후속 처리는 진행.

### 10.2 업무 GPT의 최소 회신 — 원본 반출 없이 충분한 범위

| 항목 | 비민감 회신만 허용 | 실제 검증 경계 |
|---|---|---|
| 스킬 사용 | 관련 스킬명, 실제 사용 중 여부(USER_CONFIRMED/HOST_VERIFIED 구분), 버전·SHA는 **알려진 경우만** | 설치본 추정 금지. 외부 GPT가 이미 확인한 PUBLIC/PRIVATE 스냅샷과 호스트 활성본은 별개 |
| Knowledge Updater | Work 직접 분석/기존 Work 지식화, 후보·Preview, 개인/그룹 지식 연결 등 **지원/미지원/미확인**과 책임 스킬 | 구현/스킬 원문·회사 자료·상세 코드/로그/절대 경로 반출 불필요 |
| ACE | 최신 유효 Work 결정/이력·다음 액션을 기존 reader에서 찾을 수 있는지, HOLD 반례 | 사용자 결정/승인 범위와 원본 기록에 대한 **호스트 자체 판정 요약** |
| PEC-HOP | Source Revision·Evidence ID·전체 파일 SHA·근거 발췌 검증의 지원 범위 및 누락 | 실제 파일/함수/IPC/원문 bytes를 CoWork로 반출하지 않음 |
| ACON | 기존 실패·수정 피드백 기록과 baseline 비교 가능성, 모델 호출 없이 수행 가능한 부분 | 유료 모델 반복 시험이나 신규 모델 호출 자동 시작 금지 |
| 안전·수정 | `REUSE / CONNECT / GAP_VERIFIED / BLOCKED`, 증상·원인·수정 소유자, 사전/사후 시험 등급 | 로컬 실제 시험 상세는 업무 환경에 보존, 공유본에는 요약만 |

**실제 버전이나 내부 함수 시그니처 확보가 불가능해도** 사용 기능의 관측·입출력·제약·실패 조건을 확인한 범위에서 설계 검토 가능. 단 내부 구현의 미확인 항목은 확정 구현이나 코드 검증 PASS로 승격하지 않음.

### 10.3 사용 중 문제 발생 시 모바일 수정 요청 경로

```text
업무 Linux 스킬 사용 중 문제 확인
  → 모바일 Agent에서 문제·기대 결과·재현 조건의 비민감 요약을 전달
  → 기존 CoWork Work/기존 스킬 책임과 중복 확인
  → GPT가 원인/범위와 REUSE·CONNECT·필요한 최소 수정 판정
  → (GitHub 관리 스킬) 허용된 개발·시험 → 필요한 독립 리뷰 → 배포 Gate 충족 시 최종 L1Work ZIP
  → (업무 전용 Updater) 업무 GPT/허용된 업무 Agent에서 원본 보존·허용된 수정·시험, 비민감 결과만 회신
  → 기존 유효 승인·skill-updater/전달 계약에 따라 업무 Linux 적용
  → 실제 설치 해시·시험/영수증·오류 해결 여부를 확인하고 동일 Work 정산
```

- 모바일 수정 요청은 **이슈 접수**이며 자동 설치·호스트 시작·유료 리뷰·원격 게시·REQUEST/READY 트리거가 아님. 해당 행위는 그때의 유효한 승인·권한·비용·배포 게이트를 별도 확인.
- 모바일 회신에 필요한 최소 내용: **대상 스킬/Work ID(알 때만), 관측 증상, 기대 동작, 문제가 발생한 단계, 비민감 재현 조건, 활성 버전(확인된 경우), 오류 분류·Evidence 식별자(공유 가능한 경우)**. 민감 코드/로그/토큰/고객정보 복사 금지.
- 동일 목적의 기존 Work를 우선 재개. 수정된 ZIP이 기존 공개본보다 높거나 후보 이름이 같아도 설치됐다고 보고하지 않음. 새로운 최종 ZIP은 기존 ZIP 보존·SHA/CRC·보안·호환/시험·필요 리뷰 게이트 후 허용된 PUBLIC 배송을 수행. 업무 환경 설치/사용 결과는 **별도 HOST_VERIFIED**.
- 운영 문제를 접수했다고 ACE/PEC-HOP/ACON의 새로운 서브에이전트·상시 watcher·압축 엔진·지식 원장까지 신설하지 않음.

### 10.4 현재 판정·다음 한 행동

`DESIGN_R1=ACCEPT_WITH_CHANGE/CLOSED` (기존 완료 리뷰 재사용), `SYNTHETIC_CONTRACT=26_PASS`, `USER_CONFIRMED_SKILLS_IN_USE=YES`, `ACTIVE_INSTALLED_REVISIONS=NOT_VERIFIED`, `UPDATER_SOURCE_EXPORT=NOT_REQUIRED`, `UPDATER_RUNTIME_CONTRACT=HOST_REPORTED_OR_PENDING`, `NEW_HOST_TEST/MODEL_CALL/INSTALL/KNOWLEDGE_WRITE=NOT_RUN_BY_THIS_DOC`.

**NEXT_ONE_ACTION:** ACE·PEC-HOP·ACON을 실제 업무에 연결할 때 또는 모바일 오류 수정 요청이 들어올 때, 업무 GPT가 **문제와 관련된 미확인 기능만** 읽기 전용으로 확인하여 10.2 표의 비민감 결과를 회신. GPT는 기존 Work/공개 스킬 근거와 대조해 최소 변경·검증·배송 여부를 판정. 현재 정상 사용 중인 스킬에 대한 일괄 재설치·전체 기능 재조사 요구 없음.

## 11. 2026-11-19 KST — GPT 순수 읽기 전용 구현 후보·L1Work ZIP 배포 게이트 판정

- **사용자 실행 지시:** ACE·PEC-HOP·ACON을 기존 스킬에 적용하고 L1Work에 최종 ZIP까지 배포 요청. 이번 단계에서 실제 수행 가능한 비민감 순수 연결 후보와 합성 단위시험은 완료했으나, **최종 스킬 ZIP은 L1Work에 게시하지 않음(`PUBLIC_SKILL_ZIP=BLOCKED_NOT_POSTED`)**.
- GPT가 GitHub PRIVATE CoWork 기존 Work에 새 스킬/영속 원장 없이 READ_ONLY 순수 연결 후보 1개를 작성함. ACE: 동일 Work 결정 원문·append/유효 근거가 없으면 HOLD. PEC-HOP: pinned raw bytes/발췌 위치·SHA-256 비교, 1-byte 변조 FAIL. ACON: *이미 있는* 고정 모델·revision의 baseline/compressed 결과만 비교하며 신규 모델 호출 없음. Python 합성 단위시험 **19 PASS/0 FAIL**. 기존 메모리 내 합성 계약시험 26 PASS와 실제 업무 스킬 E2E는 구별.
- **아직 수행하지 않은 것:** 후보를 활성 `l1-fix-workflow` / `work-ledger-kernel` / `code-analyzer` ZIP에 편입하거나 실제 Linux 설치본의 기존 함수와 연결하는 작업. 업무 전용 `l1-knowledge-updater`의 코드/SKILL.md를 GitHub로 제공할 필요 없음. 새로운 서브에이전트, 학습/압축 엔진, 유료 모델 호출, Knowledge write, REQUEST/READY/Job, Windows/업무 호스트 변경 모두 없음.
- **배포 차단 사유:** GitHub PRIVATE의 관련 개발 ZIP은 `development_not_for_deployment`. 기존 업무용 Git/Knowledge writer의 raw Git·credential·동시성/충돌 방어, 전체 회귀, 신규 코드 독립 리뷰, 실제 설치/연결 계약 등이 통합 배포 PASS로 입증되지 않았음. 최신 활성 설치 버전을 확인하지 않고 낮은 공개 ZIP을 기반으로 새 버전을 만들면 과거 변경을 덮을 수 있음. 따라서 “단순 ZIP 재패키징 → L1Work 공개 → 업무 환경 자동 설치”를 실행하면 안 됨. 공개된 구버전 ZIP을 변경하지 않음.
- **업무 GPT의 최소 후속:** 기존 §§9~10의 전체 재조사 대신, 실제 활성 **Workflow/Kernel/Analyzer 버전 또는 source hash(확인 가능한 항목만)**, 기존 Work 결정의 원문 순서/권한 검증 가능성, 기존 Evidence 발췌의 byte range 제공 여부, Knowledge Updater의 **지원 기능/제약/호스트 시험 등급에 대한 비민감 요약**만 읽기 전용으로 회신. 내부 코드·원문 로그·회사 자료·상세 MSC는 업무 환경에 유지. 접근/권한이 없으면 `NOT_VERIFIED`.
- **다음 수행의 완료 기준:** 현재 버전과 호환되는 기존 스킬 경로에 필요한 순수 연결만 추가 → 기존 기능·보안·호환 전체 회귀 및 독립 코드 리뷰 → 필수 릴리스 게이트 PASS → 새 최종 스킬 ZIP을 L1Work/main **루트**에 게시해 바이트/SHA 원격 검증. 업무 환경의 설치/활성화·동작 시험은 그 후 별도 HOST 결과로 정산. 조건 미달이면 계속 `BLOCKED_NOT_POSTED`.

**현재 분리 판정:** `DEV_SOURCE=POSTED_PRIVATE_READBACK_PASS`; `SYNTHETIC_UNIT_TESTS=19_PASS`; `SOURCE_SKILL_INTEGRATION=NOT_RUN`; `INDEPENDENT_CODE_REVIEW=NOT_RUN`; `PUBLIC_FINAL_ZIP=BLOCKED_NOT_POSTED`; `BUSINESS_HOST_INSTALL=NOT_RUN`; `DESIGN_REVIEW_R1=CLOSED`. 이 공개 문서는 **실제 ZIP 배포/자동 업데이트/업무 호스트 적용 신호가 아님**.

## 12. 2026-11-19 KST — Workflow v1.6.73 실제 패키지 내 통합·20단위시험 PASS·최종 배포 대기

**업무 GPT 인계용 최신 사실(2026-11-19 KST):**

- CoWork PRIVATE `COWORK-SKILL-DISCOVERY-20261112-001`에서 기존 Workflow v1.6.70 원본과 MSC v1.6.72 패치 계보를 재사용해 **v1.6.73 개발 ZIP을 실제 생성**. `l1_fix_workflow/ace_pec_acon_readonly.py`에 ACE 결정 후보/HOLD, PEC 원문 raw byte+SHA 검증, ACON 기존 반복 결과 비교 함수를 포함.
- [실제 GitHub Actions 개발 CI 44422077963](https://github.com/wonhwipark/CoWork-Skill-Collab/actions/runs/44422077963): **SUCCESS**, `l1-fix-workflow_v1_6_73_1119.zip` 760,970 B / SHA256 `4e435a165a692f9c77c816067d6dd7d11f920def4c808d4ecb06b44b613a5c77`. 패키지의 실제 모듈을 import한 비민감 Python 단위시험 **20 PASS/0 FAIL**, MSC 기존 계약 3 PASS, ZIP 311 members/manifest 310, CRC/버전/두 번 빌드 바이트 동일 PASS.
- **중요한 미완료:** 이 ZIP의 release channel은 `development_not_for_deployment`. Windows Claude Code **신규 코드 독립 리뷰 미완료**, 업무 Linux **실제 설치/권한/G0 미확인**, Git writer의 raw Git credential·동시 writer/충돌 보호와 전체 호환/보안 게이트 미검증. ZIP은 **현재 L1Work main 루트에 게시하지 않았음(`PUBLIC_FINAL_SKILL_ZIP=BLOCKED_NOT_POSTED`)**. 기존 L1Work 구버전 ZIP은 그대로 유지. 사용자 공개 배송 지시는 유효하게 보존.
- 비민감 현장 협업: 업무 GPT/허용된 Linux Agent는 실제 활성 Workflow/Kernel/Analyzer 버전·read-only 호출 가능성, Knowledge Updater 기능(지원/미지원/미확인), Writer 권한/충돌 보호의 **관련 G0 델타만** 회신. Updater 원본·SKILL.md·회사 코드/로그/MSC를 CoWork 또는 L1Work에 반출하지 않음.
- Windows Claude Code 독립 코드 리뷰는 CoWork PRIVATE 동일 Work의 `ACE_PEC_ACON_WORKFLOW_V1673_INDEPENDENT_CODE_REVIEW_AND_RELEASE_GATES_r0001_20261119_KST.md`에 범위·고정 소스·CI·LIVE 사전승인 Gate를 기록. 실제 호스트 정책/보호 위임 합치지 않는 한 REQUEST/READY/유료 리뷰 호출 0; 기존 완료된 디자인 R1은 CLOSED.
- **최종 다음 행동:** 관련 업무 G0와 독립 코드 리뷰/릴리스 Gate PASS 후, 검증된 신규 최종 채널 패키지만 `wonhwipark/L1Work/main` 루트에 게시하여 실제 바이트 SHA-256 readback. 공개 ZIP 전달과 `skill-updater` Linux 설치·실업무 결과는 각각 별도 판정.

`HOST_INSTALL=NOT_RUN`; `WORKFLOW_V1673_DEV_CI=PASS`; `INDEPENDENT_CODE_REVIEW=NOT_RUN`; `PUBLIC_SKILL_ZIP=BLOCKED_NOT_POSTED`; `BUSINESS_UPDATER_SOURCE_EXPORT=NOT_REQUIRED`.

## 13. 2026-11-19 KST — 최종 범위 축소: PEC-HOP 우선·ACE 최소, ACON 보류 / 업무 환경 내부 완결형 실증

**가장 최근 적용 판단(앞선 §§1~12의 G0 회수·ACON 배포 계획보다 우선):** 사용자 확인에 따라 *업무 환경에서 생성된 코드·분석/Evidence/로그·실험 및 설치 결과는 외부 GitHub/개발 GPT로 반출하지 않음*. “비민감 G0 요약 회신”도 **별도 명시적 반출 승인 없이는 요구하지 않음**. 기존 문서의 회신 문장은 현장 내부 확인·보존으로 대체.

### 13.1 실제 실행 구조

```text
개발 GPT / Windows Claude Code
  비민감 스킬 코드·합성 시험·독립 코드 리뷰·릴리스 심사
  → 승인된 새 최종 ZIP만 L1Work/main 루트
  → 기존 skill-updater가 허용된 업무 Linux에서 설치/검증
     └─ 업무 GPT / Linux Agent / MCP
          ├─ PEC-HOP(P1): 원본 source revision·Evidence/raw bytes 대조
          ├─ ACE(P2): 기존 Workflow/Kernel의 결정·미해결·중단 Work 재개
          ├─ ACON: DEFER
          └─ 현장 전용 baseline 비교/시험 결과/영수증 보존
                  X 회사 자료·실행 판정 외부 회신
```

실제 업무 데이터와 함수/IPC/MSC/Work ID/로그, 호스트 버전·경로·평가 결과는 모두 승인된 업무 환경에만 보존. 기능을 현장에서 사용하기 위해 외부 GPT가 이 정보를 읽을 필요는 없음. 하지만 외부 GPT는 현장 PASS를 직접 확인할 수 없으므로 `HOST_VERIFIED_EXTERNAL=NOT_OBSERVABLE`로 유지.

### 13.2 스킬 연결 범위

| 우선 | 담당 | 필요한 최소 기능 | 금지/미확인 |
|---|---|---|---|
| P1 PEC-HOP | Code Analyzer의 근거·Workflow/Kernel 기존 reader | 실제 고정 source revision·해당 byte-range와 발췌 일치 검증, stale/missing/1-byte 변조 시 FAIL/HOLD | 기존 원본·근거를 L1Work로 내보내지 않음; raw range 미지원이면 임의 PASS 금지 |
| P2 ACE | Workflow/Kernel 기존 Work/decision | 같은 scope/유효 출처·권한/append 결정 중 최신 선택, 불명확 시 HOLD, Work 재개 시 미해결·다음 행동 보존 | 새 Work/DB/Agent/재실행/자동 승인 없음 |
| 보류 ACON | 기존 코드 후보는 보존 | **실제 현장 효과가 확인된 후에만** 별도 재평가 | 3+3 유료 모델 시험·새 압축 엔진·자동 프롬프트 수정·이번 ZIP 범위에 자동 포함 금지 |
| 변경 제외 Knowledge Updater | 업무 GPT/허용 Agent | 기존 관리·승인/게시 기능과 권한 유지 | 업무 전용 스킬 SKILL.md/구현 제공 불필요, writer 변경 없음 |

기존 `l1-fix-workflow_v1_6_73_1119.zip`의 **20 PASS는 과거 합성 개발시험**일 뿐 현장 기능·신규 범위 PASS 아님. 패키지는 `development_not_for_deployment`이고 **최종 ZIP은 아직 L1Work에 미게시**. 과거 개발 바이트와 리뷰 영수증은 무손실 보존; 향후 P1/P2만 포함할 최종 패키지는 실제 소스·호환성을 먼저 고정해 새 고유 버전으로 검증/게시.

### 13.3 업무 환경 내부에서만 수행하는 소규모 평가

업무 GPT는 실제 설치본의 read-only G0(Workflow·Kernel·Code Analyzer·Updater 역할/권한/원본 조회 가능 여부)를 **현장에서 자체 확인**. 데이터 쓰기·호스트 재설치 없이 합성 fixture부터 확인하고 허용된 경우 대표 사례 1개(예: NR L1 Tx Recovery 업무)를 선택. 기존 결과 baseline과 개선 결과를 같은 입력·설정·판정 기준으로 비교. 효과가 보이면 3~5개 사례로 확대. **현장 결과의 외부 회신은 요구하지 않음**.

| ID | 합격 기준(기본 상태 전부 NOT_RUN) |
|---|---|
| PEC-P1 | 원본 권한/source revision/raw byte-range/digest 실제 일치만 PASS; 원본 미접근·위치 미확인 HOLD |
| PEC-P2 | **합성** 1-byte 변조, stale revision, 누락 범위 입력이 하나도 잘못 PASS되지 않을 것 |
| PEC-P3 | 선택 사례의 핵심 IPC/상태/조건/근거 누락·변형 0, 근거 없는 원인 확정 0 |
| ACE-P1 | 유효 최신 결정/철회 처리 정확, 승인 범위·순서 모호 시 HOLD, 권한 잘못 적용 0 |
| ACE-P2 | 중단 Work 재개 시 원 Work/결정/미해결/다음 행동 보존; 중복 Work·중복 Job 0 |
| SAFE-P1 | 무단 업무/Git/Knowledge/운영 WRITE·모델 호출·외부 데이터 전송 0 |
| VALUE-P1 | baseline 대비 근거 오류·재개 누락·수동 확인 횟수·경과 시간을 **내부에서 실측**해 실제 개선 여부 판단. 향상이 없으면 `BENEFIT_NOT_DEMONSTRATED` |

안전·정확성 결함 하나라도 있으면 해당 사례 FAIL. 제한된 표본의 통과는 `LOCAL_PILOT_PASS_SCOPE_LIMITED`로 표시하고 다른 모듈·업무 환경 전체 PASS로 확대하지 않음. 현장 호스트의 실제 영수증은 업무 환경에서만 정산.

### 13.4 책임과 다음 한 행동

- **외부 개발 담당:** PEC·ACE에 필요한 공개 가능한 공통 코드·합성 테스트·독립 코드 리뷰·패키지 RELEASE 품질·PUBLIC GitHub 게시까지만 판단. 실제 업무 원본이 없으면 기능 연결 G0를 추정하거나 현장 검증 PASS로 보고하지 않음.
- **업무 GPT/허용 Linux Agent:** 실제 설치본 read-only 기능을 확인하고, 기존 Work/Evidence로 파일럿 1건의 baseline과 P1/P2 개선판을 **현장 내부에서만** 비교·기록·판정. 설치·운영 변경은 실제 기존 승인/호스트 계약 하에서만.
- **본 인계서의 게시**는 스킬 설치/호스트 실행/자동 모델 호출/Knowledge writer/외부 피드백 승인이 아님. 내부 검증 결과가 외부에서 관찰되지 않더라도 기존 개발·PUBLIC ZIP 무결성 검증은 독립적으로 계속 가능.

`LATEST_SCOPE=PEC_P1_ACE_P2_ACON_DEFER`, `NO_EXPORT=DEFAULT`, `WORKFLOW_V1673_DEV=20_SYNTHETIC_PASS`, `CURRENT_PILOT=NOT_RUN`, `PUBLIC_FINAL_ZIP=BLOCKED_NOT_POSTED`, `EXTERNAL_HOST_E2E=NOT_OBSERVABLE`.
