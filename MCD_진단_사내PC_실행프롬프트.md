# [사내PC 실행용] MCD `PROXY_MODEL_MISMATCH` 원인 판별 프롬프트

버전 대상: `l1-sam-fixer v0.2.66` · 소요 약 10분 · **읽기 전용 (코드/데이터 수정 없음)**

---

## 0. 이 작업의 목적

현재 MCD 개선 후보가 0개로 나오고 `PROXY_MODEL_MISMATCH`가 뜬다.
원인 후보는 4가지이고, **어느 쪽이냐에 따라 다음 작업이 5분짜리와 몇 주짜리로 갈린다.**

| 원인 | 후속 작업 규모 |
|---|---|
| A. fixer의 scope 분할이 순환을 자름 | 패치 수십 줄 |
| B. fixer의 경로 대소문자 처리 불일치 | 패치 수 줄 |
| C. CSV 그래프가 실제로 비순환 | include graph 구축 (수 주) |
| D. edge가 아예 안 읽힘 | CSV 열 매핑 수정 |

**이 문서는 A~D 중 어느 것인지만 판별한다.** 판별 전에는 include graph 작업에 착수하지 않는다.

---

## 1. 준비물

| 항목 | 예시 경로 |
|---|---|
| inventory.json | `<run-dir>\\baseline\\inventory.json` |
| SAM MCD CSV | `sam_metric_mcd_detail.csv` |
| Python | 3.9+ (표준 라이브러리만 사용, 설치 불필요) |

경로를 모르면:

```
dir /s /b inventory.json
dir /s /b sam_metric_mcd_detail.csv
```

---

## 2. STEP 1 — 진단 스크립트 생성

아래 블록 전체를 `mcd_proxy_diagnose.py`로 저장한다. **인코딩은 UTF-8**, 내용은 전부 ASCII라 cp949 환경에서도 안전하다.

```python
#!/usr/bin/env python3
"""PROXY_MODEL_MISMATCH root-cause triage for l1-sam-fixer.

Read-only. Answers one question: is the missing directed cycle caused by the
input graph, or by how the fixer partitions and normalizes that graph?

Usage:
    python mcd_proxy_diagnose.py <run-dir>/baseline/inventory.json
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict


def norm(value: object) -> str:
    return str(value or "").strip().replace("\\", "/")


def edge_of(item: object) -> tuple[str, str] | None:
    if not isinstance(item, dict):
        return None
    a = norm(item.get("from") or item.get("source"))
    b = norm(item.get("to") or item.get("target"))
    return (a, b) if a and b else None


def scope_of(unit: dict) -> tuple[str, str]:
    for field in ("cycle_index", "cycle_id"):
        text = str(unit.get(field) or "").strip()
        if text:
            return "SAM_CONNECTED_COMPONENT", f"CYCLE_INDEX:{text}"
    wid = str(unit.get("work_unit_id") or unit.get("cycle_signature") or "").strip()
    return "WORK_UNIT_FALLBACK", f"WORK_UNIT:{wid}"


def tarjan(nodes: set[str], edges: set[tuple[str, str]]) -> list[set[str]]:
    adj: dict[str, list[str]] = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
    idx: dict[str, int] = {}
    low: dict[str, int] = {}
    on: set[str] = set()
    stack: list[str] = []
    out: list[set[str]] = []
    counter = 0
    for root in sorted(nodes):
        if root in idx:
            continue
        frames = [(root, iter(adj.get(root, ())))]
        idx[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on.add(root)
        while frames:
            v, it = frames[-1]
            advanced = False
            for w in it:
                if w not in idx:
                    idx[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on.add(w)
                    frames.append((w, iter(adj.get(w, ()))))
                    advanced = True
                    break
                if w in on:
                    low[v] = min(low[v], idx[w])
            if advanced:
                continue
            frames.pop()
            if low[v] == idx[v]:
                comp: set[str] = set()
                while stack:
                    w = stack.pop()
                    on.discard(w)
                    comp.add(w)
                    if w == v:
                        break
                out.append(comp)
            if frames:
                low[frames[-1][0]] = min(low[frames[-1][0]], low[v])
    return out


def cyclic(nodes: set[str], edges: set[tuple[str, str]]) -> int:
    loops = sum(1 for a, b in edges if a == b)
    return sum(1 for c in tarjan(nodes, edges) if len(c) > 1) + loops


def main(path: str) -> int:
    data = json.loads(open(path, encoding="utf-8").read())
    units = data.get("work_units") or data.get("units") or []
    if not units:
        print("work_units not found in", path)
        return 2

    all_nodes: set[str] = set()
    all_edges: set[tuple[str, str]] = set()
    scopes: dict[str, dict] = {}
    node_scope: dict[str, set[str]] = defaultdict(set)
    id_source = Counter()
    fallback_units = 0

    for unit in units:
        if not isinstance(unit, dict):
            continue
        id_source[str(unit.get("identity_source") or "MISSING")] += 1
        stype, sid = scope_of(unit)
        if stype == "WORK_UNIT_FALLBACK":
            fallback_units += 1
        sc = scopes.setdefault(sid, {"nodes": set(), "edges": set()})
        members = {norm(x) for x in (unit.get("cycle_members") or []) if norm(x)}
        sc["nodes"] |= members
        all_nodes |= members
        for m in members:
            node_scope[m].add(sid)
        for item in unit.get("dependency_edges") or []:
            key = edge_of(item)
            if not key:
                continue
            sc["nodes"] |= set(key)
            sc["edges"].add(key)
            all_nodes |= set(key)
            all_edges.add(key)
            for m in key:
                node_scope[m].add(sid)

    scoped_cycles = sum(cyclic(s["nodes"], s["edges"]) for s in scopes.values())
    global_cycles = cyclic(all_nodes, all_edges)

    fold: dict[str, set[str]] = defaultdict(set)
    for n in all_nodes:
        fold[n.casefold()].add(n)
    case_collisions = {k: v for k, v in fold.items() if len(v) > 1}

    folded_edges = {(a.casefold(), b.casefold()) for a, b in all_edges}
    folded_nodes = {n.casefold() for n in all_nodes}
    folded_cycles = cyclic(folded_nodes, folded_edges)

    cross = sum(1 for a, b in all_edges if node_scope[a].isdisjoint(node_scope[b]))

    print("=" * 62)
    print(f"units={len(units)}  scopes={len(scopes)}  nodes={len(all_nodes)}  edges={len(all_edges)}")
    print(f"identity_source: {dict(id_source)}")
    print(f"WORK_UNIT_FALLBACK units (no cycle_index/cycle_id): {fallback_units}")
    print("-" * 62)
    print(f"[1] directed cycles WITHIN fixer scopes ..... {scoped_cycles}   <- what the fixer sees")
    print(f"[2] directed cycles in ONE merged graph ..... {global_cycles}")
    print(f"[3] directed cycles after casefold ......... {folded_cycles}")
    print(f"    nodes differing only by case ........... {len(case_collisions)}")
    print(f"    edges whose endpoints share no scope ... {cross}")
    print("=" * 62)

    if scoped_cycles == 0 and global_cycles > 0:
        print("VERDICT: SCOPE_PARTITION_DESTROYS_CYCLES")
        print("  The CSV does contain directed cycles. Per-scope graph building hides them.")
        print(f"  Fix the scope key (cycle_index) before any include-graph work.")
    elif scoped_cycles == 0 and folded_cycles > 0:
        print("VERDICT: PATH_CASE_NORMALIZATION_DESTROYS_CYCLES")
        print("  Casefolding node names alone recovers directed cycles.")
        print("  mcd_edge_leverage/_edge_key does not casefold; the rest of the tool does.")
        for k, v in list(case_collisions.items())[:5]:
            print(f"    {sorted(v)}")
    elif global_cycles == 0 and folded_cycles == 0 and all_edges:
        print("VERDICT: INPUT_GRAPH_GENUINELY_ACYCLIC")
        print("  Even one merged, casefolded graph has no directed cycle.")
        print("  Only now is include-graph enrichment the right next step.")
    elif not all_edges:
        print("VERDICT: NO_EDGES_INGESTED  (dependency_edges empty -> check CSV column mapping)")
    else:
        print("VERDICT: CYCLES_PRESENT_IN_SCOPE  (look elsewhere: gain function, simulation limit)")
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
python mcd_proxy_diagnose.py <run-dir>\\baseline\\inventory.json
```

출력이 `==========` 로 둘러싸인 블록 하나로 나온다. **그 블록 전체를 그대로 복사해 둔다.**

---

## 4. STEP 3 — CSV 열 이름 확인

```
python -c "import csv,sys;print(next(csv.reader(open(sys.argv[1],encoding='utf-8-sig'))))" sam_metric_mcd_detail.csv
```

UnicodeDecodeError가 나면 `encoding='cp949'`로 바꿔 재시도한다.

---

## 5. 답변지

**아래 양식만 채워서 회신하면 된다. 서술 불필요.**

### Q1. 판정 — 출력 마지막 `VERDICT:` 줄 하나 선택

```
[ ] A. SCOPE_PARTITION_DESTROYS_CYCLES
[ ] B. PATH_CASE_NORMALIZATION_DESTROYS_CYCLES
[ ] C. INPUT_GRAPH_GENUINELY_ACYCLIC
[ ] D. NO_EDGES_INGESTED
[ ] E. CYCLES_PRESENT_IN_SCOPE
```

### Q2. 숫자 — 출력에서 그대로 옮기기

```
units    = 
scopes   = 
nodes    = 
edges    = 

[1] scope 내부 directed cycle = 
[2] 통합 그래프 directed cycle = 
[3] casefold 후 directed cycle = 

대소문자만 다른 노드 쌍 = 
scope 공유 안 하는 edge  = 
WORK_UNIT_FALLBACK unit = 
```

### Q3. identity_source 분포 — 출력의 dict 한 줄 그대로

```
identity_source = 
```

### Q4. CSV 열 — STEP 3 출력에서 해당하는 것 모두 체크

```
[ ] cycle_path / dependency_path / loop_path / 순환경로
[ ] cycle_index / cycle_id / CycleIndex
[ ] dependency_type / reference_type / edge_type / 의존유형
[ ] 위 셋 다 없음
```

전체 열 목록(그대로 붙여넣기):

```

```

### Q5. SAM 의존 그래프 단위 — SAM 도구 담당자 확인 (스크립트로는 알 수 없음)

```
[ ] 헤더 단위 (.h/.hpp include 관계)
[ ] TU 단위 (.cpp 포함 전체 번역단위)
[ ] 모름 / 확인 불가
```

### Q6. 공식 SAM MCD 점수

```
현재 =         목표 = 
```

---

## 6. 판정별 다음 단계 (참고용, 지금 실행하지 말 것)

| Q1 | 다음 작업 | include graph 필요? |
|---|---|---|
| **A** | `_scope_identity` 패치 → `mcd-edge-leverage` 재실행 | **불필요** |
| **B** | 해당 경로가 실제 동일 파일인지 확인 → `_edge_key` 정렬 | **불필요** |
| **C** | 첨부 설계문서 Phase 1 착수 | 필요 |
| **D** | `parse_sam_csv` 열 매핑 수정 | 불필요 |
| **E** | gain 함수 / simulation limit 쪽 재조사 | 불필요 |

A·B는 **C++ 코드를 한 줄도 고치지 않고** 후보가 되살아나는지 먼저 확인할 수 있다.

---

## 7. 주의

- 이 절차는 읽기 전용이다. 소스, CSV, run-dir 어느 것도 수정하지 않는다.
- 판정이 나오기 전까지 기존 candidate #1/#2를 폐기하지 않는다. `REVALIDATION_REQUIRED` 상태로 둔다.
- `[1]=0` 자체는 "개선점 없음"의 근거가 아니다. `[2]` 또는 `[3]`이 0보다 크면 **데이터가 아니라 도구가 원인**이다.
