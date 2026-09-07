# [사내PC 실행용] MCD 보고서 확인 + code-analyzer 연결

소요 약 20분 · **읽기 전용** · 소스/CSV/P4 수정 없음

> 회신은 **`ANS` 줄 + 객관식 2문항**.

---

## 0. 왜 code-analyzer를 아직 연결하지 않았나

probe(`code-analyzer v0.14.0`)는 **fixer가 만든 `code_analysis_request.json` 의
`dependency_edges` 를 입력으로 받는다.**

직전 실행에서 그 edge 목록이 잘못돼 있었다.

```
fold=8  fe=0  intra=53  incyc=0  cov=PROXY_MODEL_MISMATCH  ncand=0
```

수동 분석은 같은 CSV에서 79 폴더 / 508 edge / 순환 46 이 나온다.
fixer가 물리 edge(`FromPath`/`ToPath`) 대신 모듈명을 쓰고 있었다는 뜻이다.

**잘못된 edge에 probe를 붙이면 잘못된 코드를 분석한다.**
그래서 "폴더 그래프가 정상인지 먼저 확인" 을 선행 조건으로 뒀다.

### 다만 지금 병렬로 확인할 수 있는 것이 있다

probe가 실제 소스를 못 찾으면 edge가 아무리 정확해도 무용지물이다.
`mcd_edge_probe.resolve_source()` 는 이렇게 동작한다.

```python
candidate = (branch_root / csv_path.lstrip("/")).resolve()
```

**접두사 처리가 없다.** CSV가 `ProjectX_Trunk/L1C/...` 형태이고
실제 트리가 `/home/whpark/Project/smp1900/SMPF/L1C/...` 라면
전부 `SOURCE_FILE_NOT_RESOLVED` 가 된다.

이 확인은 fixer와 무관하므로 **오늘 바로 할 수 있다.** STEP 2가 그것이다.

---

## STEP 1 — 보고서 상태 확인 (Track A)

`edge_source_health` 하나로 갈린다. v0.2.71에서 추가된 필드다.

```bash
python3 - <<'PY'
import json, glob, os
c = glob.glob(os.path.expanduser(
    "~/l1sw-private-skills/l1-sam-fixer/output/*/reports/mcd_edge_leverage.json"))
if not c:
    print("mcd_edge_leverage.json NOT FOUND"); raise SystemExit(1)
p = max(c, key=os.path.getmtime)
d = json.loads(open(p, encoding="utf-8").read())
g = d.get
print("file:", p)
for k in ("edge_source_health", "edge_source_degenerate", "folder_granularity",
          "folder_count", "folder_edge_count", "intra_folder_edge_dropped",
          "folders_in_cycle", "folder_cyclic_scc_count",
          "self_loop_edge_dropped", "candidate_coverage_status"):
    print("  %-28s = %s" % (k, g(k)))
cand = d.get("folder_demotion_candidates") or []
print("  %-28s = %s" % ("demotion_candidates", len(cand)))
for x in cand[:5]:
    print("      %-34s %s / %s / %s" % (x.get("target_folder"), x.get("folders_freed"),
                                        x.get("edges_to_cut"), x.get("file_refs_to_change")))
print("ANS12|health=%s|gran=%s|fold=%s|fe=%s|intra=%s|incyc=%s|scc=%s|sloop=%s|cov=%s|ncand=%s|top=%s" % (
    g("edge_source_health"), g("folder_granularity"), g("folder_count"),
    g("folder_edge_count"), g("intra_folder_edge_dropped"), g("folders_in_cycle"),
    g("folder_cyclic_scc_count"), g("self_loop_edge_dropped"),
    g("candidate_coverage_status"), len(cand),
    ";".join("%s:%s/%s/%s" % (x.get("target_folder"), x.get("folders_freed"),
                              x.get("edges_to_cut"), x.get("file_refs_to_change"))
             for x in cand[:3])))
PY
```

### `health` 별 의미

| 값 | 의미 | 다음 |
|---|---|---|
| `OK` + `incyc=46` | **정상. 개선안이 이미 나와 있다** | STEP 3 진행 |
| `OK` + `incyc` 다른 값 | 다른 스냅샷의 Run | artifact 경로 확인 |
| `NO_CROSS_FOLDER_EDGE` | 모든 edge가 폴더 내부. **입력이 잘못됨** | STEP 1-B |
| `NO_EDGE_INPUT` | edge 자체가 없음 | STEP 1-B |
| 필드 자체가 없음 | v0.2.71 미설치 | 스킬 버전 확인 |

**`ncand=0` 을 "고칠 것이 없음"으로 읽지 말 것.**
`health` 가 `OK` 가 아니면 입력이 잘못된 것이다.

### STEP 1-B — `OK` 가 아닐 때만

```bash
python3 - <<'PY'
import json, glob, os
c = glob.glob(os.path.expanduser(
    "~/l1sw-private-skills/l1-sam-fixer/output/*/baseline/inventory.json"))
p = max(c, key=os.path.getmtime)
def find(o, k):
    if isinstance(o, dict):
        if k in o: return o[k]
        for v in o.values():
            r = find(v, k)
            if r is not None: return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, k)
            if r is not None: return r
    return None
b = find(json.loads(open(p, encoding="utf-8").read()), "mcd_score_bridge") or {}
for k in ("status", "reason_code", "primary_file", "summary_file",
          "cycle_file", "relation_file", "relation_edge_row_count", "ambiguous_roles"):
    print("  %-26s = %s" % (k, b.get(k)))
sc = b.get("scanned_csvs") or []
print("  scanned_csvs (%d):" % len(sc))
for s in sc[:15]:
    name = os.path.basename(str(s.get("file", s))) if isinstance(s, dict) else os.path.basename(str(s))
    role = s.get("role") if isinstance(s, dict) else None
    print("     %-52s role=%s" % (name, role))
print("ANS13|st=%s|rc=%s|rel=%s|rows=%s|amb=%s|nscan=%s" % (
    b.get("status"), b.get("reason_code"),
    "Y" if b.get("relation_file") else "N", b.get("relation_edge_row_count"),
    ",".join(b.get("ambiguous_roles") or []) or "-", len(sc)))
PY
```

| 관측 | 원인 |
|---|---|
| `scanned` 에 `mfs_relations` 가 **있는데** `rel=N` | 헤더 판정 문제 |
| `scanned` 에 **없음** | 탐색 범위 문제. v0.2.71은 하위 1단계까지만 본다 |
| `amb=relation` | 같은 역할 후보가 2개 이상 |
| `nscan` 이 매우 작음 | `--file` 로 CSV 하나만 지정한 경우 |

---

## STEP 2 — 경로 매핑 확인 (Track B, Track A와 무관)

**이것이 code-analyzer 연결의 진짜 선행 조건이다.**

아래를 `probe_path_check.py` 로 저장한다. **UTF-8**, 전체 ASCII.

```python
#!/usr/bin/env python3
"""Find how SAM CSV paths map onto the real source tree.

Read-only.  The probe resolves a CSV path as ``branch_root / csv_path`` with no
prefix handling, so a CSV that ships paths like ``ProjectX_Trunk/L1C/x.hpp``
will never resolve under ``/home/.../SMPF``.  This reports the prefix to strip.

Usage:
    python3 probe_path_check.py <mfs_relations.csv> <branch_root> [sample]
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

ENC = ("utf-8-sig", "cp949", "utf-8", "latin-1")
FROM = ("frompath", "from", "src_path", "srcpath", "fromentity", "source_file")
TO = ("topath", "to", "dst_path", "dstpath", "toentity", "target_file")


def key(s):
    return re.sub(r"[^a-z0-9]", "", str(s or "").lower())


def load(p: Path, limit: int):
    for enc in ENC:
        try:
            with open(p, encoding=enc, newline="") as fh:
                rows = list(csv.reader(fh))
            break
        except UnicodeDecodeError:
            continue
    else:
        return [], None
    head = [key(c) for c in rows[0]]
    fi = next((i for i, c in enumerate(head) if c in FROM), None)
    ti = next((i for i, c in enumerate(head) if c in TO), None)
    if fi is None or ti is None:
        return [], rows[0]
    out = []
    for r in rows[1:]:
        if len(r) > max(fi, ti):
            for v in (r[fi], r[ti]):
                v = str(v or "").strip().replace("\\", "/").strip("/")
                if v:
                    out.append(v)
        if len(out) >= limit:
            break
    return out, rows[0]


def main(csv_path, root, sample=4000):
    root = Path(root).expanduser().resolve()
    paths, header = load(Path(csv_path), int(sample))
    if not paths:
        print("no from/to columns. header =", header)
        return 2
    uniq = sorted(set(paths))
    print("=" * 68)
    print(f"csv paths sampled : {len(uniq)}")
    print(f"branch root       : {root}")
    print("examples:")
    for x in uniq[:5]:
        print("   ", x)

    direct = sum(1 for x in uniq if (root / x).is_file())
    print("-" * 68)
    print(f"[1] direct  branch_root/<csv path>      -> {direct}/{len(uniq)} resolved")

    # try stripping leading segments
    best = (direct, 0)
    print("[2] strip N leading segments:")
    for n in range(1, 5):
        hit = 0
        for x in uniq:
            parts = x.split("/")
            if len(parts) > n and (root / "/".join(parts[n:])).is_file():
                hit += 1
        print(f"      strip {n}: {hit}/{len(uniq)}")
        if hit > best[0]:
            best = (hit, n)

    # basename search as a last resort
    index = Counter()
    by_base: dict[str, list[Path]] = {}
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".h", ".hpp", ".hxx", ".inl",
                                                ".c", ".cc", ".cpp", ".cxx"}:
            by_base.setdefault(p.name.casefold(), []).append(p)
    base_hit = sum(1 for x in uniq if Path(x).name.casefold() in by_base)
    print(f"[3] basename match anywhere under root  -> {base_hit}/{len(uniq)}")

    print("=" * 68)
    if best[0] >= len(uniq) * 0.8:
        if best[1] == 0:
            print("VERDICT: DIRECT_OK   -- probe works with --branch-root as is")
        else:
            print(f"VERDICT: STRIP_{best[1]}   -- csv paths carry {best[1]} extra leading segment(s)")
            ex = next(x for x in uniq if len(x.split("/")) > best[1])
            print(f"  example: {ex}")
            print(f"        -> {'/'.join(ex.split('/')[best[1]:])}")
    elif base_hit >= len(uniq) * 0.8:
        print("VERDICT: BASENAME_ONLY -- structure differs; only filenames match.")
        print("  A prefix rule is not enough; a path mapping profile is needed.")
    else:
        print("VERDICT: UNRESOLVED  -- neither prefix strip nor basename matches.")
        print("  Confirm branch_root is the right tree.")
    print(f"ANS11|direct={direct}|best_strip={best[1]}|best_hit={best[0]}"
          f"|base={base_hit}|total={len(uniq)}")
    print("=" * 68)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(*sys.argv[1:4]))
```

실행:

```
python3 probe_path_check.py \
    <sam_metrics_mcd_detail_mfs_relations.csv> \
    /home/whpark/Project/smp1900/SMPF
```

| VERDICT | 의미 | 조치 |
|---|---|---|
| `DIRECT_OK` | CSV 경로가 그대로 맞는다 | probe를 `--branch-root` 만으로 실행 가능 |
| `STRIP_N` | 앞 N개 세그먼트가 여분이다 | probe에 접두사 제거 필요 (STEP 4) |
| `BASENAME_ONLY` | 파일명만 일치, 구조가 다름 | 경로 매핑 프로파일이 필요 |
| `UNRESOLVED` | 어느 쪽도 아님 | `branch_root` 가 맞는 트리인지 확인 |

---

## STEP 3 — probe 실행 (STEP 1이 `OK` 이고 STEP 2가 `DIRECT_OK` 일 때만)

fixer가 만든 요청 파일을 찾는다.

```
find ~/l1sw-private-skills/l1-sam-fixer/output -name code_analysis_request.json -newermt today
```

probe 실행:

```
python3 ~/l1sw-private-skills/code-analyzer/scripts/mcd_edge_probe.py \
    --request-file <위 경로> \
    --branch-root /home/whpark/Project/smp1900/SMPF \
    --output /tmp/edge_facts.json --json
```

결과 요약:

```bash
python3 - <<'PY'
import json
from collections import Counter
d = json.loads(open("/tmp/edge_facts.json", encoding="utf-8").read())
wus = d.get("work_units") or [d]
facts = [e for w in wus for e in (w.get("edge_facts") or [])]
prop = Counter(e.get("edge_property") for e in facts)
cls = Counter(e.get("probe_class") for e in facts)
print("edges:", len(facts))
print("edge_property:", dict(prop))
print("probe_class  :", dict(cls))
for e in facts[:5]:
    print("   %-30s -> %-24s %s" % (str(e.get("from"))[-30:], str(e.get("to"))[-24:],
                                    e.get("edge_property")))
print("ANS14|n=%s|fwd=%s|unknown=%s|unresolved=%s" % (
    len(facts), prop.get("FORWARD_DECLARABLE", 0), prop.get("UNKNOWN", 0),
    cls.get("SOURCE_FILE_NOT_RESOLVED", 0)))
PY
```

`unresolved` 가 대부분이면 STEP 2 결과가 `DIRECT_OK` 가 아니었던 것이다.

그다음 fixer가 그 사실을 받는지 확인한다.

```
skillsilent run l1-sam-fixer improvement-points -- --top 5 --json
```

`evidence_level` 이 `ANALYSIS_REQUIRED` 에서 `CODE_ANALYZED` 로 올라가면
체인이 뚫린 것이다.

---

## STEP 4 — `STRIP_N` 이 나온 경우 (참고, 지금 실행하지 말 것)

`mcd_edge_probe.resolve_source()` 에 접두사 제거를 추가해야 한다.

```python
def resolve_source(branch_root, raw, strip=0):
    text = norm_rel(raw)
    parts = text.split("/")
    if strip and len(parts) > strip:
        text = "/".join(parts[strip:])
    ...
```

`--path-strip N` 인자로 노출하고, 값은 STEP 2의 `best_strip` 을 쓴다.
**자동 추정은 하지 않는다.** 잘못 추정하면 엉뚱한 파일을 읽는다.

---

## 회신 양식

```
ANS12|          (STEP 1)
ANS13|          (STEP 1-B, health가 OK가 아닐 때만)
ANS11|          (STEP 2, probe_path_check 마지막 줄)
ANS14|          (STEP 3, probe를 돌렸을 때만)
```

### Q1. STEP 2 VERDICT

```
[ ] DIRECT_OK   [ ] STRIP_N -> N =     [ ] BASENAME_ONLY   [ ] UNRESOLVED
```

### Q2. STEP 1 health

```
[ ] OK + incyc=46   [ ] OK + 다른 값   [ ] NO_CROSS_FOLDER_EDGE
[ ] NO_EDGE_INPUT   [ ] 필드 없음 (v0.2.71 미설치)
```

---

## 주의

- STEP 2는 STEP 1 결과와 **무관하게** 실행할 수 있다. 먼저 해도 된다
- `improvement-points` 가 `ANALYSIS_REQUIRED` 인 것은 실패가 아니다.
  **개선안은 `folder_demotion_candidates` 에서 나온다**
- STEP 1이 `OK` + `incyc=46` 이면 아래가 곧 1순위 수정 대상이며,
  이 수정은 probe 연결을 기다릴 필요가 없다

```
L1C/Common/Export   4 / 1 / 1
  ch_L1cAllocatorUtil.hpp -> Utility/MRA/Common/ch_MraUtilRadio.cpp
```
