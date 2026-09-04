# [사내PC 실행용 · 2단계] 판정 C 이후 — MCD penalty 실제 동인 확인

전제: 1단계 판정 = **C `INPUT_GRAPH_GENUINELY_ACYCLIC`**
소요 약 10분 · **읽기 전용 (코드/데이터 수정 없음)**

---

## 0. 왜 아직 include graph가 아닌가

판정 C는 **`inventory.json`에 들어간 edge들이 비순환**이라는 뜻이다.
CSV 원본이 비순환이라는 뜻은 아니다. 아직 확인 안 된 것이 셋 남아 있다.

| # | 확인할 것 | 사실이면 |
|---|---|---|
| A | 파서가 CSV 행을 잃었나 | CSV 열 매핑 수정 — include graph 불필요 |
| B | SAM 순환 경로에 edge가 안 잡힌 파일이 있나 | **누락 edge가 이름으로 특정됨** — 전수 조사 불필요 |
| C | 방향만 안 닫히나, 연결 자체가 없나 | 방향 문제면 파서, 연결 없으면 진짜 누락 |
| D | penalty가 애초에 순환이 아닌 다른 것에 좌우되나 | **순환 끊기 전략 자체를 폐기** |

**D가 가장 중요하다.** MCD가 cycle이 아니라 coupling/density 지표라면 판정 C는 이상 현상이 아니라 정상이고, 지금까지의 순환 중심 접근이 처음부터 어긋나 있었다는 뜻이 된다.

---

## 1. 준비물

| 항목 | 예시 |
|---|---|
| inventory.json | `<run-dir>\\baseline\\inventory.json` |
| SAM MCD CSV | `sam_metric_mcd_detail.csv` (선택, 있으면 A 확인 가능) |
| Python | 3.9+ (표준 라이브러리만) |

---

## 2. STEP 1 — 스크립트 저장

아래 블록 전체를 `mcd_stage2_driver.py`로 저장한다. **UTF-8**, 내용은 전부 ASCII.

```python
#!/usr/bin/env python3
"""Stage-2 triage after VERDICT C (INPUT_GRAPH_GENUINELY_ACYCLIC).

Read-only. Answers three questions the stage-1 script could not:

  Q-A  Did the parser lose CSV rows on the way into inventory.json?
  Q-B  Does SAM's own cycle path name files the edge list never connects?
  Q-C  Is MCD penalty driven by something other than directed cycles?

Usage:
    python mcd_stage2_driver.py <inventory.json> [<sam_metric_mcd_detail.csv>]
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict


def norm(v: object) -> str:
    return str(v or "").strip().replace("\\", "/")


def edge_of(item: object) -> tuple[str, str] | None:
    if not isinstance(item, dict):
        return None
    a = norm(item.get("from") or item.get("source"))
    b = norm(item.get("to") or item.get("target"))
    return (a, b) if a and b else None


def undirected_has_cycle(nodes: set[str], edges: set[tuple[str, str]]) -> bool:
    """Union-find over the underlying undirected graph (ignores self loops)."""
    parent = {n: n for n in nodes}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    seen: set[frozenset[str]] = set()
    for a, b in edges:
        if a == b:
            return True
        key = frozenset((a, b))
        if key in seen:
            continue
        seen.add(key)
        ra, rb = find(a), find(b)
        if ra == rb:
            return True
        parent[ra] = rb
    return False


def rank(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            out[order[k]] = avg
        i = j + 1
    return out


def spearman(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3:
        return None
    rx, ry = rank(xs), rank(ys)
    n = len(rx)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def main(inv_path: str, csv_path: str | None) -> int:
    data = json.loads(open(inv_path, encoding="utf-8").read())
    units = data.get("work_units") or data.get("units") or []
    if not units:
        print("work_units not found")
        return 2

    all_nodes: set[str] = set()
    all_edges: set[tuple[str, str]] = set()
    member_source = Counter()
    uncovered_units: list[tuple[str, list[str]]] = []
    total_uncovered = 0
    feats: list[dict] = []

    for u in units:
        if not isinstance(u, dict):
            continue
        members = {norm(x) for x in (u.get("cycle_members") or []) if norm(x)}
        edges = set()
        for it in u.get("dependency_edges") or []:
            k = edge_of(it)
            if k:
                edges.add(k)
        endpoints = {x for e in edges for x in e}
        all_nodes |= members | endpoints
        all_edges |= edges
        member_source[str(u.get("cycle_member_source") or "NONE")] += 1

        uncovered = sorted(m for m in members if m not in endpoints)
        if uncovered:
            total_uncovered += len(uncovered)
            uncovered_units.append((str(u.get("work_unit_id") or "?"), uncovered))

        pen = None
        for f in ("score_penalty", "penalty", "mcd_penalty", "penalty_score"):
            if u.get(f) is not None:
                try:
                    pen = abs(float(u.get(f)))
                    break
                except (TypeError, ValueError):
                    pass
        nodes_u = members | endpoints
        n, e = len(nodes_u), len(edges)
        outd, ind = defaultdict(int), defaultdict(int)
        for a, b in edges:
            outd[a] += 1
            ind[b] += 1
        feats.append({
            "penalty": pen,
            "node_count": float(n),
            "edge_count": float(e),
            "density": (e / (n * (n - 1)) if n > 1 else 0.0),
            "avg_degree": (2.0 * e / n if n else 0.0),
            "max_fan_in": float(max(ind.values()) if ind else 0),
            "max_fan_out": float(max(outd.values()) if outd else 0),
            "member_count": float(len(members)),
        })

    print("=" * 64)
    print(f"units={len(units)}  nodes={len(all_nodes)}  edges={len(all_edges)}")
    print(f"cycle_member_source: {dict(member_source)}")

    print("-" * 64)
    print("[Q-A] parser loss")
    if csv_path:
        try:
            enc_used = None
            for enc in ("utf-8-sig", "cp949", "utf-8"):
                try:
                    with open(csv_path, encoding=enc, newline="") as fh:
                        rows = list(csv.reader(fh))
                    enc_used = enc
                    break
                except UnicodeDecodeError:
                    continue
            if enc_used is None:
                print("  CSV unreadable with utf-8-sig/cp949/utf-8")
            else:
                body = max(0, len(rows) - 1)
                ratio = (len(all_edges) / body * 100.0) if body else 0.0
                print(f"  CSV data rows = {body}   (encoding {enc_used})")
                print(f"  ingested edges = {len(all_edges)}   -> {ratio:.1f}% of rows became edges")
                print("  LOSS_SUSPECTED" if ratio < 60.0 else "  ROW_COVERAGE_OK")
        except OSError as exc:
            print("  csv read failed:", exc)
    else:
        print("  csv path not supplied - skipped")

    print("-" * 64)
    print("[Q-B] SAM cycle members not connected by any edge")
    print(f"  units with uncovered members = {len(uncovered_units)}")
    print(f"  uncovered member occurrences = {total_uncovered}")
    for wid, items in uncovered_units[:5]:
        print(f"    {wid}: {items[:4]}")
    if total_uncovered:
        print("  -> SAM names files the CSV edge list never links. MISSING_EDGE_EVIDENCE")
    else:
        print("  -> every member is an edge endpoint. NO_MISSING_EDGE_EVIDENCE")

    print("-" * 64)
    print("[Q-C] direction vs absence")
    und = undirected_has_cycle(all_nodes, all_edges)
    print(f"  undirected cycle in merged graph = {und}")
    print("  -> loop exists but directions do not close it. DIRECTION_SUSPECT"
          if und else
          "  -> not even an undirected loop. EDGES_GENUINELY_ABSENT")

    print("-" * 64)
    print("[Q-D] penalty driver correlation (Spearman, |r|>=0.5 notable)")
    scored = [f for f in feats if f["penalty"] is not None]
    print(f"  scored units = {len(scored)}")
    if len(scored) >= 3:
        ys = [f["penalty"] for f in scored]
        ranked = []
        for key in ("node_count", "edge_count", "density", "avg_degree",
                    "max_fan_in", "max_fan_out", "member_count"):
            r = spearman([f[key] for f in scored], ys)
            if r is not None:
                ranked.append((abs(r), key, r))
        for a, key, r in sorted(ranked, reverse=True):
            mark = " <<<" if a >= 0.5 else ""
            print(f"    {key:14} r = {r:+.3f}{mark}")
    else:
        print("  too few scored units for correlation")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None))
```

---

## 3. STEP 2 — 실행

```
python mcd_stage2_driver.py <run-dir>\\baseline\\inventory.json sam_metric_mcd_detail.csv
```

CSV 경로는 생략 가능하지만, **넣으면 A 확인까지 된다.** 넣는 것을 권장.

---

## 4. 답변지

**아래만 채워서 회신. 서술 불필요.**

### Q1. 헤더 3줄

```
units =        nodes =        edges = 
cycle_member_source = 
```

### Q2. [Q-A] 파서 손실 — 택1

```
[ ] ROW_COVERAGE_OK
[ ] LOSS_SUSPECTED
[ ] CSV 미지정으로 건너뜀
```

```
CSV data rows =        ingested edges =        비율 =      %
```

### Q3. [Q-B] SAM 순환 멤버 중 edge 미연결 — 택1

```
[ ] MISSING_EDGE_EVIDENCE      (누락 edge가 이름으로 특정됨)
[ ] NO_MISSING_EDGE_EVIDENCE
```

```
uncovered 있는 unit 수 =        uncovered 총 개수 = 
```

출력에 찍힌 예시 파일명 그대로 붙여넣기 (최대 5줄):

```

```

### Q4. [Q-C] 방향 문제 vs 연결 부재 — 택1

```
[ ] DIRECTION_SUSPECT      (무방향으로는 루프가 있음)
[ ] EDGES_GENUINELY_ABSENT (무방향으로도 루프 없음)
```

### Q5. [Q-D] penalty 동인 상관 — 출력 표 그대로 붙여넣기

```
scored units = 

    node_count     r = 
    edge_count     r = 
    density        r = 
    avg_degree     r = 
    max_fan_in     r = 
    max_fan_out    r = 
    member_count   r = 
```

### Q6. 미해결 항목 (1단계에서 답 못 받은 것)

CSV 열 목록 — 해당 항목 체크:

```
[ ] cycle_path / dependency_path / loop_path / 순환경로
[ ] cycle_index / cycle_id / CycleIndex
[ ] dependency_type / reference_type / edge_type / 의존유형
[ ] 위 셋 다 없음
```

SAM 의존 그래프 단위 (SAM 도구 담당자 확인):

```
[ ] 헤더 단위   [ ] TU 단위   [ ] 모름
```

공식 SAM MCD 점수:

```
현재 =        목표 = 
```

---

## 5. 결과별 다음 단계 (참고용, 지금 실행하지 말 것)

| 관측 | 결론 | 다음 |
|---|---|---|
| Q2 = `LOSS_SUSPECTED` | 파서가 행을 버림 | `parse_sam_csv` 열 매핑 수정 → 재실행 |
| Q3 = `MISSING_EDGE_EVIDENCE` | SAM은 아는 파일을 CSV edge가 안 연결 | **그 파일들만** include 확인. 전수 조사 불필요 |
| Q4 = `DIRECTION_SUSPECT` | 연결은 있는데 방향이 안 닫힘 | CSV의 from/to 열 의미 재확인 (caller/callee vs includes/included-by) |
| Q5에 \|r\| >= 0.5 인 항목 있음 | **penalty 동인이 순환이 아님** | 순환 끊기 중단. 해당 지표를 줄이는 전략으로 전환 |
| 전부 음성 | 그때 include graph 구축 | 설계문서 Phase 1 착수 |

---

## 6. 주의

- 읽기 전용이다. 소스, CSV, run-dir 어느 것도 수정하지 않는다.
- Q5에서 `edge_count`나 `node_count`의 상관이 높게 나오면, **MCD 개선 방향은 "순환을 끊는다"가 아니라 "컴포넌트를 작게 쪼갠다 / 결합 수를 줄인다"** 가 된다. 이 경우 기존 fix rule 5종의 적용 우선순위가 통째로 바뀐다.
- 상관은 인과가 아니다. Q5 결과는 가설 순위를 정하는 용도이며, 확정은 공식 SAM 재측정으로만 한다.
