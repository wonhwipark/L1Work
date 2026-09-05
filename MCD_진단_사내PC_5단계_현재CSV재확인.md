# [사내PC 실행용 · 5단계] 현재 CSV 재확인 — fixer 파싱 결함 여부 확정

소요 약 3분 · **읽기 전용** · 스킬 설치 불필요

> 회신은 `ANS4|` **한 줄**이면 된다.

---

## 0. 무엇을 확인하는가

4단계에서 **0811 시점 CSV**를 직접 읽었더니 순환이 나왔다.

```
r1=CYC   scc=2   sl=27   cyc0=29
```

그런데 fixer의 1단계 진단은 **판정 C (`INPUT_GRAPH_GENUINELY_ACYCLIC`)** 였다.
두 결과가 배치된다. 다만 스냅샷 시점이 달라 아직 확정이 아니다.

**그래서 판정 C를 냈던 그 CSV를 같은 방식으로 직접 읽어본다.**

| 결과 | 결론 |
|---|---|
| `r1=CYC`, `cyc0>0` | **fixer 파싱 결함 확정.** 원본에 순환이 있는데 `inventory.json`에서 사라짐 |
| `r1=ACY`, `cyc0=0` | 현재 스냅샷은 실제로 비순환. 판정 C가 맞음 |

어느 쪽이든 **include graph 구축은 답이 아니다.** fixer를 고칠지 말지를 가르는 확인이다.

---

## 1. 준비물

| 항목 | 주의 |
|---|---|
| **판정 C를 냈던 그 run의 원본 CSV 폴더** | `import-artifact`에 넣었던 바로 그것. 다른 스냅샷이면 비교가 성립하지 않는다 |
| 4단계에서 쓴 `cl_*.diff` | **그대로 재사용.** 형식상 필요할 뿐이다 |
| `mcd_cl_impact.py` | 4단계에서 저장한 것 그대로. 없으면 아래 STEP 1 |
| Python 3.9+ | 표준 라이브러리만. **스킬 설치 불필요** |

---

## 2. STEP 1 — 스크립트 (4단계에서 이미 저장했으면 건너뛴다)

`mcd_cl_impact.py`로 저장. **UTF-8**, 내용은 전부 ASCII.

```python
#!/usr/bin/env python3
"""Cross a P4 CL against the pre-fix SAM MCD artifact.

Read-only. Parses the raw SAM CSV directly (NOT inventory.json, so the fixer's
own parsing cannot influence the result) and answers:

  R-1  Does the RAW pre-fix CSV graph contain directed cycles at all?
  R-2  Which dependency edges did the CL actually remove?
  R-3  Were those edges on a directed cycle?
  R-4  How many cycles did each removed edge participate in (leverage)?

R-3 is the decision. If a CL that demonstrably improved the official MCD score
removed edges that were NOT on any directed cycle, the current
"prove it resolves a directed cycle" gate rejects what actually works.

Usage:
    python mcd_cl_impact.py <csv-file-or-folder> <cl-diff-file>
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

FROM_COLS = ("frompath", "from", "fromentity", "src_path", "srcpath",
             "source_file", "sourcefile", "sourcepath", "from_path")
TO_COLS = ("topath", "to", "toentity", "dst_path", "dstpath",
           "target_file", "targetfile", "targetpath", "to_path")
CYCLE_COLS = ("cycleindex", "cycle_index", "cycle", "cycleid", "cycle_id", "mfscycleindex")
ENCODINGS = ("utf-8-sig", "cp949", "utf-8", "latin-1")


def key(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(s or "").lower())


def norm(v: object) -> str:
    return str(v or "").strip().replace("\\", "/")


def base(p: str) -> str:
    return norm(p).rsplit("/", 1)[-1].casefold()


def read_rows(path: Path):
    for enc in ENCODINGS:
        try:
            with open(path, encoding=enc, newline="") as fh:
                rows = list(csv.reader(fh))
            return rows, enc
        except UnicodeDecodeError:
            continue
        except OSError:
            return None, None
    return None, None


def load_edges(target: Path):
    files = [target] if target.is_file() else sorted(target.glob("*.csv"))
    edges: set[tuple[str, str]] = set()
    cyc_of: dict[tuple[str, str], set[str]] = defaultdict(set)
    used: list[str] = []
    total_rows = 0
    for f in files:
        rows, enc = read_rows(f)
        if not rows or len(rows) < 2:
            continue
        head = [key(c) for c in rows[0]]
        fi = next((i for i, c in enumerate(head) if c in FROM_COLS), None)
        ti = next((i for i, c in enumerate(head) if c in TO_COLS), None)
        if fi is None or ti is None:
            continue
        ci = next((i for i, c in enumerate(head) if c in CYCLE_COLS), None)
        n = 0
        for r in rows[1:]:
            if len(r) <= max(fi, ti):
                continue
            a, b = norm(r[fi]), norm(r[ti])
            if not a or not b:
                continue
            edges.add((a, b))
            n += 1
            if ci is not None and len(r) > ci and str(r[ci]).strip():
                cyc_of[(a, b)].add(str(r[ci]).strip())
        if n:
            used.append(f"{f.name} [{enc}] rows={n} from='{rows[0][fi]}' to='{rows[0][ti]}'")
            total_rows += n
    return edges, cyc_of, used, total_rows


def tarjan(nodes, edges):
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
    idx, low, on, st, out, c = {}, {}, set(), [], [], 0
    for root in sorted(nodes):
        if root in idx:
            continue
        frames = [(root, iter(adj.get(root, ())))]
        idx[root] = low[root] = c
        c += 1
        st.append(root)
        on.add(root)
        while frames:
            v, it = frames[-1]
            moved = False
            for w in it:
                if w not in idx:
                    idx[w] = low[w] = c
                    c += 1
                    st.append(w)
                    on.add(w)
                    frames.append((w, iter(adj.get(w, ()))))
                    moved = True
                    break
                if w in on:
                    low[v] = min(low[v], idx[w])
            if moved:
                continue
            frames.pop()
            if low[v] == idx[v]:
                comp = set()
                while st:
                    w = st.pop()
                    on.discard(w)
                    comp.add(w)
                    if w == v:
                        break
                out.append(comp)
            if frames:
                low[frames[-1][0]] = min(low[frames[-1][0]], low[v])
    return out


def reaches(adj, src, dst) -> bool:
    seen, stack = {src}, [src]
    while stack:
        cur = stack.pop()
        if cur == dst:
            return True
        for nxt in adj.get(cur, ()):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return False


FILE_PAT = re.compile(r"(//[^\s#]+|[ab]/\S+|\S+\.(?:h|hpp|hxx|inl|c|cc|cpp|cxx))", re.I)
INC_PAT = re.compile(r'^[-+]\s*#\s*include\s*[<"]([^">]+)[">]')
FWD_PAT = re.compile(r"^\+\s*(?:class|struct|enum\s+class)\s+\w+\s*;")


def parse_cl(path: Path):
    text = None
    for enc in ENCODINGS:
        try:
            text = path.read_text(encoding=enc)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        return [], [], 0, []
    cur = ""
    removed, added, fwd = [], [], []
    touched = set()
    for line in text.splitlines():
        s = line.rstrip()
        if s.startswith("====") or s.startswith("--- ") or s.startswith("+++ ") or s.startswith("Index:"):
            m = FILE_PAT.search(s)
            if m:
                cur = norm(m.group(1)).split("#")[0]
                if re.search(r"\.(h|hpp|hxx|inl|c|cc|cpp|cxx)$", cur, re.I):
                    touched.add(cur)
            continue
        m = INC_PAT.match(s)
        if m and cur:
            (removed if s.startswith("-") else added).append((cur, norm(m.group(1))))
            continue
        if FWD_PAT.match(s) and cur:
            fwd.append(cur)
    return removed, added, len(touched), fwd


def main(csv_target: str, cl_file: str) -> int:
    tgt, clp = Path(csv_target), Path(cl_file)
    if not tgt.exists() or not clp.is_file():
        print("path not found")
        return 2

    edges, cyc_of, used, rows_read = load_edges(tgt)
    nodes = {x for e in edges for x in e}
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)

    comps = tarjan(nodes, edges)
    cyclic = [c for c in comps if len(c) > 1]
    selfl = sum(1 for a, b in edges if a == b)

    print("=" * 72)
    print("[R-1] RAW pre-fix CSV graph  (parsed directly, fixer not involved)")
    for u in used:
        print("   ", u)
    if not used:
        print("    no CSV with recognizable from/to columns found")
        return 0
    print(f"    rows={rows_read}  nodes={len(nodes)}  unique edges={len(edges)}")
    print(f"    cyclic SCCs={len(cyclic)}  self-loops={selfl}"
          f"   largest SCC={max((len(c) for c in cyclic), default=0)}")
    print("    -> RAW_CSV_HAS_DIRECTED_CYCLES" if (cyclic or selfl)
          else "    -> RAW_CSV_IS_ACYCLIC")

    removed, added, touched, fwd = parse_cl(clp)
    print("-" * 72)
    print("[R-2] CL content")
    print(f"    files touched={touched}  includes removed={len(removed)}  "
          f"added={len(added)}  forward-decls added={len(fwd)}")
    for src, inc in removed[:8]:
        print(f"      - {base(src)}  ->  {inc}")

    by_base = defaultdict(list)
    for a, b in edges:
        by_base[(base(a), base(b))].append((a, b))

    print("-" * 72)
    print("[R-3] were the removed edges on a directed cycle?")
    verdict = Counter()
    detail = []
    for src, inc in removed:
        cands = by_base.get((base(src), base(inc)), [])
        if not cands:
            verdict["EDGE_NOT_IN_CSV"] += 1
            detail.append((base(src), base(inc), "EDGE_NOT_IN_CSV", 0))
            continue
        for a, b in cands:
            rest = defaultdict(list)
            for x, y in edges:
                if (x, y) != (a, b):
                    rest[x].append(y)
            on = reaches(rest, b, a)
            verdict["ON_DIRECTED_CYCLE" if on else "NOT_ON_DIRECTED_CYCLE"] += 1
            detail.append((base(a), base(b),
                           "ON_DIRECTED_CYCLE" if on else "NOT_ON_DIRECTED_CYCLE",
                           len(cyc_of.get((a, b), ()))))
    for k, v in verdict.most_common():
        print(f"    {v:4}  {k}")

    on = verdict.get("ON_DIRECTED_CYCLE", 0)
    off = verdict.get("NOT_ON_DIRECTED_CYCLE", 0) + verdict.get("EDGE_NOT_IN_CSV", 0)
    print("-" * 72)
    if not detail:
        print("    VERDICT: NO_INCLUDE_REMOVAL_FOUND")
        print("    The CL changed something other than include edges"
              " (moved code, new class, etc.).")
    elif off > on:
        print("    VERDICT: CYCLE_MODEL_NOT_SUPPORTED")
        print("    A CL that improved the score removed mostly off-cycle edges.")
        print("    The current directed-cycle gate would have rejected this fix.")
    elif on and not off:
        print("    VERDICT: CYCLE_MODEL_SUPPORTED")
        print("    The fix was a genuine cycle break; the gate's model is right.")
    else:
        print("    VERDICT: MIXED")

    print("-" * 72)
    print("[R-4] per-edge detail (cycles = CycleIndex values this edge appears in)")
    print(f"    {'from':28} {'to':28} {'on-cycle?':22} {'cycles':>6}")
    for a, b, v, n in detail[:30]:
        print(f"    {a[:28]:28} {b[:28]:28} {v[:22]:22} {n:>6}")
    if len(detail) > 30:
        print(f"    ... {len(detail)-30} more")

    r1 = "CYC" if (cyclic or selfl) else "ACY"

    # [R-5] Counterfactual: apply every removal in this CL at once and recount.
    removed_pairs = set()
    for src, inc in removed:
        removed_pairs.update(by_base.get((base(src), base(inc)), []))
    after_edges = edges - removed_pairs
    after_nodes = {x for e in after_edges for x in e}
    after_cyclic = [c for c in tarjan(after_nodes, after_edges) if len(c) > 1]
    after_self = sum(1 for a, b in after_edges if a == b)
    before_tot = len(cyclic) + selfl
    after_tot = len(after_cyclic) + after_self
    resolved = before_tot - after_tot

    print("-" * 72)
    print("[R-5] counterfactual: apply the WHOLE CL to the baseline graph")
    print(f"    edges removed from graph = {len(removed_pairs)}")
    print(f"    cyclic units before = {before_tot}   after = {after_tot}   "
          f"resolved = {resolved}")
    if resolved == 0 and removed_pairs:
        print("    -> ZERO cycles resolved by this CL.")
        print("       If the official MCD score improved, that is a direct")
        print("       counterexample to the cycle-resolution gate. One CL suffices.")

    if not detail:
        r3 = "NOINC"
    elif off > on:
        r3 = "NOTSUP"
    elif on and not off:
        r3 = "SUP"
    else:
        r3 = "MIXED"
    top = ";".join(f"{a}>{b}:{'Y' if v == 'ON_DIRECTED_CYCLE' else 'N'}"
                   for a, b, v, _ in detail[:5])
    print("=" * 72)
    print("COPY THE LINE BELOW AND SEND IT BACK. Nothing else is needed.")
    print(
        f"ANS4|r1={r1}|n={len(nodes)}|e={len(edges)}|scc={len(cyclic)}|sl={selfl}"
        f"|rows={rows_read}|files={touched}|rm={len(removed)}|add={len(added)}|fwd={len(fwd)}"
        f"|r3={r3}|on={on}|off={verdict.get('NOT_ON_DIRECTED_CYCLE', 0)}"
        f"|nocsv={verdict.get('EDGE_NOT_IN_CSV', 0)}"
        f"|cut={len(removed_pairs)}|cyc0={before_tot}|cyc1={after_tot}|res={resolved}"
        f"|top={top}"
    )
    print("=" * 72)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
```

---

## 3. STEP 2 — 실행

```
python mcd_cl_impact.py <판정C를_냈던_CSV폴더> cl_483920.diff
```

CL 인자는 자리를 채우는 용도다. `rm=0`이라 결과에 영향이 없다.

---

## 4. 회신

출력 맨 아래 `ANS4|` 로 시작하는 줄을 **그대로** 복사.

```
CSV 경로 = 
ANS4|
```

**`r1` 과 `cyc0` 두 필드만 보면 된다.** 나머지는 무시해도 된다.

---

## 5. 주의

- CSV 폴더가 여러 개 후보면, **판정 C가 나온 run의 `state.json` 에 기록된 경로**를 쓴다.
  찾는 법: `dir /s /b state.json` 후 해당 run의 `state.json` 안 `artifacts` 항목 확인.
- 4단계와 **다른 CSV**를 넣는 것이 이 단계의 요점이다. 같은 걸 또 넣으면 의미가 없다.
- 순환 수가 0811(29개)보다 줄어 있으면 그것도 유의미한 정보다. 그 사이 실제로 순환이 해소됐다는 뜻이다.
