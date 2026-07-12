# GATE — flow 스키마 v0 확정용 실측 프롬프트 (code-analyzer 5.2 / v0.9.8)

목적: flow 취합(flows 섹션 + flow MSC) 스키마를 확정하기 전에, 5.2가 실제로 산출한
`structure_*_focused.json` / `analysis_progress.md`가 어떤 필드를 갖고 있는지 실측한다.

**출력 규칙 (중요)**
- 이 프롬프트는 **심볼명·함수명·파일경로·코드 본문을 출력하지 않는다.**
- 판정 결과는 **객관식 번호 한 줄**로만 낸다. 그 한 줄만 밖으로 옮겨 적으면 된다.
- 스크립트는 **읽기 전용**이다. 어떤 파일도 만들지 않고 고치지 않는다.

---

## STEP 0 — 선행 확인 (이걸 먼저 한다)

프로브는 **스킬이 아니라 스킬이 뱉은 산출물**을 잰다. 산출물이 옛 버전으로 만들어졌으면
`Q1=3`(msg_symbol 없음)이 나오는데, 이건 "5.2 확장 필요"가 아니라 "output이 낡음"이다.
두 경우를 구분하려면 설치 버전을 먼저 확인해야 한다.

```
python -c "import io,glob,os;p=os.path.expanduser('~/.claude/skills/code-analyzer/SKILL.md');s=io.open(p,encoding='utf-8').read() if os.path.exists(p) else '';print('Q0=1 (v0.9.8)' if 'version: v0.9.8' in s else ('Q0=2 (older, no version marker)' if s else 'Q0=3 (SKILL.md not found)'))"
```

- `Q0=1` → STEP 1로 진행
- `Q0=2` → **v0.9.8을 먼저 설치**한다. 그 뒤, 기존 `code_analyzer_output`이 옛 버전 산출이면
  refresh mode(§0-4)로 재분석한다: `refresh 해줘` / `수정된 코드 갱신해줘`
- `Q0=3` → 스킬 설치 경로가 다름. 실제 경로를 찾아 같은 방식으로 `version:` 라인 확인

**분석 대상 조건**: `structure_*_focused.json`이 **서로 다른 소스 파일 2개 이상**에서 나와야
Q3(파일 간 edge)·Q5(REQ/CNF 페어)·Q7이 의미를 갖는다. 가급적 **REQ 송신 파일 + CNF 처리 파일**
한 쌍을 5.2로 분석한 뒤 STEP 1을 실행한다. 파일이 1개뿐이면 Q7=2가 나오고 flow 취합의
핵심 근거(파일 경계를 넘는 flow)를 실측할 수 없다.

---

## STEP 1 — 실행

Claude Code에서 `code_analyzer_output`이 있는 폴더(= 5.2를 돌렸던 cwd)로 이동한 뒤,
아래 스크립트를 `gate_probe.py`로 저장하고 실행한다.

```
python gate_probe.py
```

경로가 다르면: `python gate_probe.py <code_analyzer_output 경로>`

```python
# gate_probe.py  (read-only. prints numbers only, no code identifiers)
import sys, os, json, glob, re

root = sys.argv[1] if len(sys.argv) > 1 else "code_analyzer_output"

def ans(d, k, v):
    d[k] = v

Q = {}

# ---- collect structure files
sfiles = glob.glob(os.path.join(root, "**", "structure_*_focused.json"), recursive=True)
sfull  = glob.glob(os.path.join(root, "**", "structure_*_full.json"), recursive=True)

# Q7: structure 파일 수
if len(sfiles) >= 2:   ans(Q, "Q7", 1)
elif len(sfiles) == 1: ans(Q, "Q7", 2)
else:                  ans(Q, "Q7", 3)

reqs, cnfs, edges = [], [], []
for p in sfiles:
    try:
        j = json.load(open(p, encoding="utf-8"))
    except Exception:
        continue
    reqs  += j.get("ipc_req_sites", []) or []
    cnfs  += j.get("ipc_cnf_handlers", []) or []
    edges += j.get("call_edges", []) or []

ipc = reqs + cnfs
FIELDS = ["id", "msg_symbol", "api", "file", "line"]

# Q1: ipc 항목 필드 구성
if not (reqs or cnfs):
    ans(Q, "Q1", 4)
elif not any("msg_symbol" in e for e in ipc):
    ans(Q, "Q1", 3)
elif all(all(f in e for f in FIELDS) for e in ipc):
    ans(Q, "Q1", 1)
else:
    ans(Q, "Q1", 2)

# Q2: msg_symbol 채움률
syms = [e.get("msg_symbol") for e in ipc]
nn = [s for s in syms if s]
if not syms:
    ans(Q, "Q2", 4)
else:
    r = len(nn) / len(syms)
    ans(Q, "Q2", 1 if r >= 0.9 else 2 if r >= 0.5 else 3 if r > 0 else 4)

# Q3: call_edges + cross-file edge
def efile(e):
    for k in ("file", "from_file", "caller_file", "src_file"):
        if e.get(k): return e[k]
    return None
def tfile(e):
    for k in ("to_file", "callee_file", "dst_file", "target_file"):
        if e.get(k): return e[k]
    return None
if not edges:
    ans(Q, "Q3", 3)
else:
    cross = any(efile(e) and tfile(e) and efile(e) != tfile(e) for e in edges)
    ans(Q, "Q3", 1 if cross else 2)

# Q4: REQ 수신 표현 (cnf_handlers 배열에 _REQ 심볼이 들어오는가)
csyms = [e.get("msg_symbol") or "" for e in cnfs]
if not [s for s in csyms if s]:
    ans(Q, "Q4", 3)
elif any(s.upper().endswith("_REQ") for s in csyms):
    ans(Q, "Q4", 1)
else:
    ans(Q, "Q4", 2)

# Q5: REQ/CNF 접미 페어링 실재 여부
def base(s):
    return re.sub(r"_(REQ|CNF|IND|RSP|RESP)$", "", s.upper())
up = [s.upper() for s in nn]
has_suffix = any(re.search(r"_(REQ|CNF|IND|RSP|RESP)$", s) for s in up)
rq = {base(s) for s in up if s.endswith("_REQ")}
cf = {base(s) for s in up if s.endswith(("_CNF", "_RSP", "_RESP"))}
if not has_suffix:
    ans(Q, "Q5", 3)
elif rq & cf:
    ans(Q, "Q5", 1)
else:
    ans(Q, "Q5", 2)

# Q6: procedure_runtime_index 필드
progs = glob.glob(os.path.join(root, "**", "analysis_progress.md"), recursive=True)
need = ["entry_point", "entry_file", "entry_line", "req_site_ids", "cnf_handler_candidate_ids"]
txt = ""
for p in progs:
    try: txt += open(p, encoding="utf-8", errors="ignore").read()
    except Exception: pass
if "procedure_runtime_index" not in txt:
    ans(Q, "Q6", 3)
elif all(f in txt for f in need):
    ans(Q, "Q6", 1)
else:
    ans(Q, "Q6", 2)

# Q8: ipc file 필드가 상대경로인가
fpaths = [e.get("file") or "" for e in ipc if e.get("file")]
def is_abs(p):
    return p.startswith("/") or bool(re.match(r"^[A-Za-z]:[\\/]", p))
if not fpaths:
    ans(Q, "Q8", 4)
else:
    a = sum(1 for p in fpaths if is_abs(p))
    ans(Q, "Q8", 2 if a == len(fpaths) else 1 if a == 0 else 3)

# ---- print: numbers only
print("GATE: " + " ".join("%s=%s" % (k, Q[k]) for k in sorted(Q)))
print("N: structure=%d full=%d req=%d cnf=%d edge=%d proc_md=%d"
      % (len(sfiles), len(sfull), len(reqs), len(cnfs), len(edges), len(progs)))
```

---

## STEP 2 — 결과 보고 (이 두 줄만 옮겨 적으면 됨)

```
Q0=?
GATE: Q1=? Q2=? Q3=? Q4=? Q5=? Q6=? Q7=? Q8=?
N: structure=? full=? req=? cnf=? edge=? proc_md=?
```

`Q0`은 STEP 0의 출력이다. Q0 없이 GATE만 오면 Q1=3의 해석이 갈리므로 반드시 함께 적는다.

두 번째 줄은 개수뿐이라 코드 정보가 아니다. 안 적어도 되지만 있으면 판정이 정확해진다.

---

## 객관식 문항 정의 (해석표 — 보고할 필요 없음)

**Q1. ipc 항목 필드 구성**
1. 모든 항목이 `{id, msg_symbol, api, file, line}` 5필드를 다 가짐
2. `msg_symbol`은 있으나 일부 항목에서 다른 필드가 빠짐
3. `msg_symbol` 필드 자체가 없음 (v0.9.8 미적용 output)
4. `ipc_req_sites` / `ipc_cnf_handlers` 배열 자체가 없음

**Q2. msg_symbol 채움률 (non-null 비율)**
1. 90% 이상 2. 50~90% 3. 50% 미만 4. 전부 null 또는 없음

**Q3. call_edges 와 파일 간 edge**
1. `call_edges[]` 있고 **서로 다른 파일을 잇는 edge 존재**
2. `call_edges[]` 있으나 전부 같은 파일 내부
3. `call_edges[]` 없음

**Q4. REQ 수신(recv) 지점 표현**
1. `ipc_cnf_handlers[]`에 `_REQ` 심볼도 포함됨 (수신 핸들러가 REQ까지 커버)
2. `ipc_cnf_handlers[]`엔 `_CNF/_IND`만. REQ 수신은 `entry_point`로만 표현됨
3. 심볼이 비어 판별 불가

**Q5. REQ/CNF 접미 페어링 실재**
1. `_REQ`/`_CNF` 접미가 있고 **prefix를 공유하는 페어가 1쌍 이상 실재**
2. 접미는 있으나 공유 페어 0쌍 (분석 파일이 1개뿐이면 정상)
3. `_REQ`/`_CNF` 접미 규칙 자체가 코드 명명과 안 맞음

**Q6. procedure_runtime_index**
1. 있고 `entry_point/entry_file/entry_line/req_site_ids/cnf_handler_candidate_ids` 전부 존재
2. 있으나 일부 필드 누락
3. 없음

**Q7. structure_*_focused.json 개수**
1. 2개 이상 (여러 file_group) 2. 1개뿐 3. 0개 (경로가 다름 → 인자로 경로 지정 후 재실행)

**Q8. ipc `file` 필드 경로 형식**
1. code_root 상대경로 2. 절대경로/드라이브레터 포함 3. 혼재 4. file 필드 없음

---

## 각 답이 flow 스키마에 미치는 영향 (설계 측 대응 — 참고용)

| 문항 | 답 | flow_composer 설계 대응 |
|---|---|---|
| Q1 | 1 | 그대로 진행 |
| Q1 | 2/3/4 | 5.2 추출 단계 확장 필요 → **작업 大**, 별도 버전업 |
| Q2 | 1 | 심볼 축 페어링 신뢰 |
| Q2 | 2/3 | null 항목은 `[RN] symbol uncaptured`로 flow에서 제외 |
| Q3 | 1 | `evidence: call-chain` 사용 가능 (순서 근거 확보) |
| Q3 | 2/3 | `evidence: symbol-pairing`만 사용, seq는 REQ→CNF 2단계로 제한 |
| Q4 | 2 | flow step의 recv는 `procedure_runtime_index.entry_point`에서 조달 → composer가 progress도 읽어야 함 (확정) |
| Q5 | 1 | 페어링 규칙을 **코드 근거로 확정** (임의 창작 아님) |
| Q5 | 2 | 규칙은 유지하되 이번 샘플로는 검증 불가 → `confidence: MEDIUM` |
| Q5 | 3 | 접미 휴리스틱 폐기. 페어링은 call-chain 근거만 허용 |
| Q6 | 1 | composer 입력 확정 |
| Q7 | 1 | cross-file flow 실측 가능 |
| Q7 | 2 | 파일 1개 → flow 취합 의미 검증 불가. **파일 2개 이상 분석 후 재실행 권장** |
| Q8 | 1 | flow step `file`을 그대로 사용 |
| Q8 | 2/3 | composer가 `meta.root` 기준 상대경로로 정규화 (SSOT 유지) |

---

## 주의

- 이 프롬프트는 **읽기 전용**이다. 파일을 만들거나 고치지 않는다.
- `python3`가 아니라 `python`으로 실행한다.
- structure가 아직 없다면 5.2로 **서로 다른 소스 파일 2개 이상**(가급적 REQ 송신 파일과 CNF 처리 파일)을 먼저 분석한 뒤 실행해야 Q3/Q5/Q7이 의미를 갖는다.
