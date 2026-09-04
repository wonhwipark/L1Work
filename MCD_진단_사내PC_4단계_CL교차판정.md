# [사내PC 실행용 · 4단계] 수정 전 artifact x P4 CL 교차 판정

목적: **점수를 올렸던 그 수정이 실제로 순환을 끊은 것이었는지** 확정한다.
소요 약 10분 · **읽기 전용** (P4 서버에 쓰지 않음, 소스 수정 없음)

> **회신은 스크립트가 찍어주는 `ANS4|...` 한 줄 + 객관식 2문항이 전부다.**
> 표를 옮겨 적을 필요 없다.

---

## 0. 이 단계가 결정적인 이유

지금까지의 진단은 전부 `inventory.json`을 봤다. 그건 **fixer가 CSV를 파싱한 결과**다.
이 스크립트는 **SAM CSV를 직접 읽는다.** fixer를 거치지 않는다.

| 출력 | 확인되는 것 |
|---|---|
| **R-1** RAW CSV에 directed cycle이 있는가 | 판정 C가 **fixer 파싱 탓인지 데이터 탓인지** 독립 검증 |
| **R-3** CL이 제거한 edge가 순환 위였는가 | 현재 게이트가 **실제로 되는 걸 막고 있는지** 확정 |
| **R-5** CL 전체를 적용하면 순환이 몇 개 없어지는가 | **반례 성립 여부.** CL 1건으로 판정 가능 |

### CL이 한 건뿐이어도 되는 이유

현재 게이트의 주장은 "gain을 얻으려면 directed cycle이 해소돼야 한다"는 **전칭 명제**다.
전칭 명제는 **반례 하나로 무너진다.** 표본 수 문제가 아니다.

- `res=0` 인데 공식 점수가 올랐다  ->  주장 반증 완료
- 증거 단위는 CL이 아니라 **edge**다. CL 하나가 include를 여러 개 지우면 그만큼 데이터가 나온다
- `r1`(RAW CSV 순환 유무)은 표본이 아니라 **데이터 자체의 성질**이라 CL 수와 무관하다

R-1이 `CYC`인데 앞선 판정이 C였다면, **CSV에는 순환이 있고 fixer가 잃어버린 것**이다.
그 순간 include graph 구축은 불필요해진다.

---

## 1. 준비물

| 항목 | 준비 방법 |
|---|---|
| 수정 **전** SAM MCD CSV | `mfs_relations.csv` 등이 든 **폴더** 또는 파일 하나 |
| P4 CL diff | 아래 명령으로 생성 |
| Python 3.9+ | 표준 라이브러리만 |

```
p4 describe -du <CL번호> > cl_<CL번호>.diff        (submit된 CL)
p4 describe -du -S <CL번호> > cl_<CL번호>.diff     (shelve 상태)
```

둘 다 읽기 전용 명령이다.

---

## 2. STEP 1 — 스크립트 저장

아래 블록 전체를 `mcd_cl_impact.py`로 저장한다. **UTF-8**, 내용은 전부 ASCII.

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
python mcd_cl_impact.py <수정전CSV폴더> cl_<CL번호>.diff
```

CL이 여러 개면 CL마다 한 번씩 돌린다. **1건만 있어도 판정에는 충분하다** (아래 R-5 참조).

---

## 4. 회신 양식

### (1) 필수 — 출력 맨 아래 `ANS4|` 로 시작하는 줄을 **그대로** 복사

```
CL 번호 = 
ANS4|
```

CL이 여러 건이면 줄을 반복한다.

```
CL 번호 =            ANS4|
CL 번호 =            ANS4|
CL 번호 =            ANS4|
```

### (2) 필수 — 공식 MCD 점수

**`res=0`일 때 이 값이 있어야 반례가 성립한다. 가장 중요한 항목이다.**

```
[ ] 있다  -> 수정 전 =        수정 후 = 
[ ] 없다  -> 재측정 가능한가?  [ ] 가능  [ ] 불가
```

### (3) 객관식 — 위 결과가 `r3=NOINC` 인 경우에만

그 CL은 include 제거가 아니었다. 무엇을 바꿨나?

```
[ ] 코드/클래스를 다른 파일로 이동
[ ] 새 클래스/인터페이스 신설
[ ] 함수 호출 구조 변경
[ ] 기타
```

**끝. 이 외에는 아무것도 적지 않아도 된다.**

---

## 5. `ANS4` 줄 읽는 법 (참고, 회신 시 불필요)

| 필드 | 뜻 |
|---|---|
| `r1=CYC` / `ACY` | RAW CSV에 순환 있음 / 없음 |
| `n` `e` `scc` `sl` | 노드, edge, 순환 SCC, 자기루프 |
| `rows` | CSV에서 읽은 관계 행 수 |
| `files` `rm` `add` `fwd` | CL이 건드린 파일 / 제거된 include / 추가된 include / 추가된 전방선언 |
| `r3=SUP` | 진짜 순환 끊기였음 |
| `r3=NOTSUP` | **순환 밖 edge를 지웠는데 점수가 올랐음** |
| `r3=MIXED` / `NOINC` | 혼재 / include 제거 아님 |
| `on` `off` `nocsv` | 순환 위 / 순환 밖 / CSV에 없던 edge 수 |
| `cut` | CL 적용으로 그래프에서 빠진 edge 수 |
| `cyc0` `cyc1` `res` | 적용 전 순환 수 / 적용 후 / **해소된 수** |
| `top=a>b:Y` | 상위 5개 edge와 순환 위 여부 |

**`res=0` + 점수 상승 = 반례 성립.** 이 조합이면 다른 근거가 필요 없다.

---

## 6. 결과 조합별 다음 단계 (참고용, 지금 실행하지 말 것)

| r1 | r3 | 결론 | 다음 |
|---|---|---|---|
| CYC | NOTSUP | **penalty 동인이 순환이 아님** | 게이트를 억제→순위로 되돌림. include graph **불필요** |
| CYC | SUP | 게이트 모델은 옳고 **fixer 파싱이 순환을 잃음** | `parse_sam_csv` 수정. include graph **불필요** |
| ACY | NOTSUP | 순환은 원래 없고 개선은 결합 감소에서 옴 | 전략을 결합 감소로 전환 |
| ACY | SUP | 모순 | 입력 CSV가 수정 전 것이 맞는지 재확인 |
| - | NOINC | 그 CL은 include 수정이 아님 | 다른 CL로 재시도 |

---

## 7. 주의

- CSV는 반드시 **수정 전(baseline)** 것이어야 한다. 수정 후 것을 넣으면 지워진 edge가 이미 없어 전부 `nocsv`로 집계된다.
- edge 매칭은 **파일명 기준**이다. 동명 파일이 여러 폴더에 있으면 한 항목이 여러 줄로 나올 수 있다. 정상이다.
- `p4 describe`는 서버 상태를 바꾸지 않는다.
