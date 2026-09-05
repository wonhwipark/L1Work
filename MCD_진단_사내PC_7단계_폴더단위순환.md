# [사내PC 실행용 · 7단계] 파일 단위 vs 폴더 단위 순환 비교

소요 약 3분 · **읽기 전용** · 스킬 설치 불필요

> 회신은 `ANS7|` **한 줄**이면 된다.

---

## 0. 배경 — 팀이 이미 검증한 방법

기존 MCD 개선은 **별도 DB 폴더를 만들고, 다른 폴더들이 그 한 방향으로만 참조**하게 하는
방식이었다. `A <-> B` 를 `A -> DB <- B` 로 바꾸는 것이다.
DB 폴더가 아무 데도 되참조하지 않으므로 순환이 원천적으로 생기지 않는다.
(Lakos의 demotion, Martin의 공통 패키지와 같은 원리)

이 방법이 성립한다는 것 자체가 **MCD가 폴더 단위 지표**라는 강한 증거다.
파일 단위 지표라면 폴더를 새로 만드는 것으로 점수가 움직일 이유가 없다.

이 단계는 그것을 데이터로 확인하고, **다음 demotion 대상을 찾는다.**

---

## 0-1. 검증할 가설

**MCD는 파일이 아니라 모듈(폴더) 간 순환을 센다. 폴더 내부 참조는 순환에 포함되지 않는다.**

이게 맞으면 지금까지의 모순이 한 번에 풀린다.

```
folderA/a1.cpp -> folderB/b1.h
folderB/b2.cpp -> folderA/a2.h
```

- **파일 단위**: 순환 없음. a1->b1, b2->a2, 서로 연결도 안 된다
- **폴더 단위**: A->B, B->A = **순환**

즉 판정 C(`INPUT_GRAPH_GENUINELY_ACYCLIC`)와 SAM이 penalty를 매기는 것이
**동시에 참일 수 있다.** 누락 edge도, 파서 버그도 필요 없다.

### 코드 확인 결과

순환을 판정하는 두 모듈에 `folder` 라는 단어가 **0회**다.

| 모듈 | 역할 | folder 언급 |
|---|---|---|
| `mcd_edge_leverage.py` | 순환 판정 / break 후보 | **0** |
| `mcd_measurement_model.py` | proxy mismatch 판정 | **0** |
| `mcd_worst_report.py` | 보고서 롤업 | 있음 (순환을 다 찾은 **뒤** 집계용) |

동일 폴더 edge를 제외하는 로직도 없다.
**fixer는 파일 단위로, 모든 edge를 포함해 순환을 찾는다.**

---

## 1. 준비물

| 항목 | 비고 |
|---|---|
| SAM MCD CSV 폴더 또는 파일 | 어느 스냅샷이든 됨. 최신 것 권장 |
| Python 3.9+ | 표준 라이브러리만 |

---

## 2. STEP 1 — 스크립트 저장

`mcd_folder_cycles.py` 로 저장. **UTF-8**, 내용은 전부 ASCII.

```python
#!/usr/bin/env python3
"""Compare FILE-level and FOLDER-level cycles in the same SAM MCD CSV.

Read-only. Tests one hypothesis:

    MCD counts cycles between MODULES (folders), not between files, and
    references inside one folder are internal so they never form a cycle.

If that is right, the folder graph can be cyclic while the file graph is
acyclic -- which would explain VERDICT C and SAM's penalty at the same time,
with no missing edges and no parser bug.

Folder depth is unknown, so every depth is reported:
  leaf   = the file's own directory
  d1..d5 = first N path segments from the root

Usage:
    python mcd_folder_cycles.py <csv-file-or-folder>
"""
from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

FROM_COLS = ("frompath", "from", "fromentity", "src_path", "srcpath",
             "source_file", "sourcefile", "sourcepath", "from_path")
TO_COLS = ("topath", "to", "toentity", "dst_path", "dstpath",
           "target_file", "targetfile", "targetpath", "to_path")
ENCODINGS = ("utf-8-sig", "cp949", "utf-8", "latin-1")


def key(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(s or "").lower())


def norm(v: object) -> str:
    return str(v or "").strip().replace("\\", "/").strip("/")


def load(target: Path):
    files = [target] if target.is_file() else sorted(target.glob("*.csv"))
    edges: set[tuple[str, str]] = set()
    used: list[str] = []
    rows_read = 0
    for f in files:
        rows = None
        for enc in ENCODINGS:
            try:
                with open(f, encoding=enc, newline="") as fh:
                    rows = list(csv.reader(fh))
                break
            except UnicodeDecodeError:
                continue
            except OSError:
                rows = None
                break
        if not rows or len(rows) < 2:
            continue
        head = [key(c) for c in rows[0]]
        fi = next((i for i, c in enumerate(head) if c in FROM_COLS), None)
        ti = next((i for i, c in enumerate(head) if c in TO_COLS), None)
        if fi is None or ti is None:
            continue
        n = 0
        for r in rows[1:]:
            if len(r) <= max(fi, ti):
                continue
            a, b = norm(r[fi]), norm(r[ti])
            if a and b:
                edges.add((a, b))
                n += 1
        if n:
            used.append(f"{f.name} rows={n}")
            rows_read += n
    return edges, used, rows_read


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


def leaf_dir(p: str) -> str:
    return p.rsplit("/", 1)[0] if "/" in p else "ROOT"


def depth_dir(p: str, d: int) -> str:
    parts = p.split("/")[:-1]
    return "/".join(parts[:d]) if parts else "ROOT"


def analyse(edges, mapper):
    """Collapse nodes with mapper, DROP intra-group edges, return cycle stats."""
    coll = set()
    dropped = 0
    for a, b in edges:
        ga, gb = mapper(a), mapper(b)
        if ga == gb:
            dropped += 1
            continue
        coll.add((ga, gb))
    nodes = {x for e in coll for x in e}
    comps = [c for c in tarjan(nodes, coll) if len(c) > 1]
    pairs = sum(1 for a, b in coll if (b, a) in coll) // 2
    return {
        "groups": len(nodes), "edges": len(coll), "intra_dropped": dropped,
        "cyclic": len(comps),
        "in_cycle": sum(len(c) for c in comps),
        "largest": max((len(c) for c in comps), default=0),
        "bidir_pairs": pairs,
        "comps": sorted(comps, key=len, reverse=True),
    }


def main(target: str) -> int:
    p = Path(target)
    if not p.exists():
        print("path not found:", target)
        return 2
    edges, used, rows_read = load(p)
    if not edges:
        print("no CSV with recognizable from/to columns")
        return 2

    fnodes = {x for e in edges for x in e}
    fcomps = [c for c in tarjan(fnodes, edges) if len(c) > 1]
    fself = sum(1 for a, b in edges if a == b)

    print("=" * 72)
    for u in used:
        print("   ", u)
    print(f"    rows={rows_read}  files={len(fnodes)}  edges={len(edges)}")
    print("-" * 72)
    print(f"[FILE level]   cyclic SCC = {len(fcomps)}   self-loops = {fself}"
          f"   largest = {max((len(c) for c in fcomps), default=0)}")

    print("-" * 72)
    print("[FOLDER level] intra-folder edges dropped, then cycles recounted")
    print(f"    {'gran':6}{'groups':>8}{'edges':>8}{'intra':>8}"
          f"{'cyclicSCC':>11}{'inCycle':>9}{'largest':>9}{'A<->B':>7}")
    results = {}
    grans = [("leaf", leaf_dir)] + [(f"d{d}", (lambda d: lambda x: depth_dir(x, d))(d))
                                    for d in range(1, 6)]
    for name, fn in grans:
        r = analyse(edges, fn)
        results[name] = r
        print(f"    {name:6}{r['groups']:>8}{r['edges']:>8}{r['intra_dropped']:>8}"
              f"{r['cyclic']:>11}{r['in_cycle']:>9}{r['largest']:>9}{r['bidir_pairs']:>7}")

    best = max(results.items(), key=lambda kv: kv[1]["cyclic"])
    print("-" * 72)
    print(f"largest folder-level cycle set at granularity '{best[0]}':")
    for comp in best[1]["comps"][:5]:
        members = sorted(comp)
        print(f"    [{len(members)}] " + " <-> ".join(m or "ROOT" for m in members[:4])
              + (" ..." if len(members) > 4 else ""))

    # ---- folder-level break candidates + demotion targets ----
    mapper = dict(grans)[best[0]]
    fedges = {(mapper(a), mapper(b)) for a, b in edges if mapper(a) != mapper(b)}
    fnodes2 = {x for e in fedges for x in e}
    base_cyc = len([c for c in tarjan(fnodes2, fedges) if len(c) > 1])
    incyc = {x for c in tarjan(fnodes2, fedges) if len(c) > 1 for x in c}

    cand = []
    for e in sorted(fedges):
        if e[0] not in incyc or e[1] not in incyc:
            continue
        rest = fedges - {e}
        left = len([c for c in tarjan({x for f in rest for x in f}, rest) if len(c) > 1])
        if base_cyc - left > 0:
            cand.append((base_cyc - left, e))
    cand.sort(reverse=True)

    print("-" * 72)
    print("[BREAK] folder edges whose removal collapses folder cycles")
    if cand:
        for gain, (a, b) in cand[:8]:
            print(f"    -{gain}  {a or 'ROOT'}  ->  {b or 'ROOT'}")
    else:
        print("    no single folder edge resolves a cycle alone"
              " (dense coupling; demotion is the lever)")

    indeg = defaultdict(int)
    outdeg = defaultdict(int)
    for a, b in fedges:
        outdeg[a] += 1
        indeg[b] += 1
    demote = sorted(((indeg[n], outdeg[n], n) for n in incyc),
                    key=lambda t: (-t[0], t[1]))
    print("-" * 72)
    print("[DEMOTE] DB-folder candidates: many depend on it, it depends on few")
    for i, o, n in demote[:6]:
        print(f"    in={i:4} out={o:4}  {n or 'ROOT'}"
              + ("   <<< already sink-like" if o == 0 else ""))

    fcyc = len(fcomps) + fself
    gcyc = best[1]["cyclic"]
    print("-" * 72)
    if fcyc == 0 and gcyc > 0:
        verd = "FOLDER_ONLY"
        print("VERDICT: FOLDER_ONLY_CYCLES")
        print("  File graph is acyclic; the FOLDER graph is not.")
        print("  VERDICT C and SAM's penalty are both true. The fixer analyses")
        print("  the file graph, so it can never see these cycles.")
    elif gcyc == 0 and fcyc > 0:
        verd = "FILE_ONLY"
        print("VERDICT: FILE_ONLY_CYCLES")
        print("  Every cycle lives inside one folder. If MCD is module-level,")
        print("  none of them is an MCD violation.")
    elif gcyc and fcyc:
        verd = "BOTH"
        print("VERDICT: BOTH_LEVELS_CYCLIC")
        print("  Folder-level count is the one to target if MCD is module-level.")
    else:
        verd = "NONE"
        print("VERDICT: NO_CYCLES_AT_EITHER_LEVEL")

    print("=" * 72)
    print("COPY THE LINE BELOW AND SEND IT BACK. Nothing else is needed.")
    print(
        f"ANS7|verd={verd}|files={len(fnodes)}|edges={len(edges)}"
        f"|fcyc={len(fcomps)}|fself={fself}|best={best[0]}"
        + "".join(f"|{n}={results[n]['groups']}/{results[n]['cyclic']}"
                  f"/{results[n]['largest']}/{results[n]['intra_dropped']}"
                  for n, _ in grans)
        + f"|brk={len(cand)}"
        + "|top=" + ";".join(f"{a}>{b}:-{g}" for g, (a, b) in cand[:3])
        + "|db=" + ";".join(f"{n}:{i}/{o}" for i, o, n in demote[:3])
    )
    print("(each gran = groups/cyclicSCC/largest/intraDropped)")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
```

---

## 3. STEP 2 — 실행

```
python mcd_folder_cycles.py <CSV폴더>
```

폴더 깊이 기준을 모르므로 **6가지 granularity를 전부** 계산한다.
`leaf`(파일의 직속 폴더)와 `d1`~`d5`(루트로부터 N단계).

---

## 4. 회신

### (1) 필수 — `ANS7|` 줄 그대로 복사

```
CSV 경로 = 
ANS7|
```

### (2) 객관식 — 기존 DB 폴더 위치

기존에 만든 DB 폴더가 `ANS7` 의 `db=` 목록이나 `[DEMOTE]` 출력에 보이는가?

```
[ ] 보인다  -> 폴더명 = 
[ ] 안 보인다 (이미 순환 밖으로 완전히 빠져 있음)
[ ] 해당 DB 폴더가 이 CSV scope 밖이다
```

### (3) 객관식 — SAM 리포트의 순환 표기 단위

`sam-result.html` 이나 MCD 리포트에서 순환이 무엇들 사이로 표시되는가?

```
[ ] 파일 이름 사이   (예: HudPanel.h <-> HudModel.h)
[ ] 폴더/모듈 이름 사이 (예: l1/phy <-> l1/mac)
[ ] 둘 다 표시됨
[ ] 확인 못 함
```

**(3)이 판정의 핵심 근거다.** SAM이 무엇 사이의 순환이라고 부르는지가 답이다.

---

## 5. `verd` 해석 (참고, 회신 시 불필요)

| 값 | 의미 | 다음 |
|---|---|---|
| `FOLDER_ONLY` | 파일은 비순환, 폴더는 순환 | **가설 확정.** fixer가 잘못된 그래프를 봄. 폴더 단위 분석으로 전환 |
| `BOTH` | 양쪽 다 순환 | 폴더 단위 수치를 목표로 삼음 |
| `FILE_ONLY` | 폴더 단위로는 순환 없음 | 모든 순환이 폴더 내부. MCD가 모듈 단위라면 위반이 아님 |
| `NONE` | 양쪽 다 없음 | 이 CSV에는 순환이 없음 |

`ANS7` 의 각 granularity 항목은 `groups/cyclicSCC/largest/intraDropped` 순이다.
`intraDropped` 가 크면 폴더 내부 참조가 많다는 뜻이고, 그만큼 파일 단위 분석이
MCD와 동떨어져 있었다는 신호다.

### 추가 출력 두 가지

**`[BREAK]`** — 폴더 edge 하나를 지우면 폴더 순환이 몇 개 없어지는지.
`brk=0` 이면 단일 edge로는 안 깨진다는 뜻이고, 그 경우 **demotion이 유일한 지렛대**다.

**`[DEMOTE]`** — DB 폴더 후보. `in`(자기를 참조하는 폴더 수)이 크고 `out`(자기가 참조하는 폴더 수)이
작을수록 좋은 후보다. `out=0` 이면 이미 싱크라서 그대로 두면 된다.
`db=` 필드에 상위 3개가 `폴더:in/out` 형식으로 들어간다.

기존 DB 폴더 방식을 그대로 적용할 다음 대상을 여기서 고르면 된다.

---

## 6. 주의

- 읽기 전용이다. CSV를 수정하지 않는다.
- `d1=0/0/0/N` 처럼 groups가 0으로 나오는 깊이는 정상이다. 그 깊이에서는 모든 파일이 한 그룹이라 edge가 전부 내부로 처리된 것이다.
- 이 결과는 6단계(고정 base A/B 측정)와 독립이다. 순서 상관없다.
