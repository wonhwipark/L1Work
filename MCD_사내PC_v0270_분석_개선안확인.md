# [사내PC 실행용] v0.2.70 MCD 분석 + 개선안 제안 확인

소요 약 10분 · **읽기 전용** (소스/CSV 수정 없음)

> 회신은 **객관식 6문항 + 표 1개**.

---

## 0. 확인하려는 것

v0.2.70은 MCD를 **파일 단위가 아니라 상위 경계(폴더) 단위**로 본다.
수동 분석에서는 다음이 나왔다. **도구가 같은 답을 내는지** 확인한다.

| 항목 | 수동 분석값 |
|---|---|
| 순환에 묶인 폴더 | **46** (전체 79 중) |
| 1순위 개선안 | `L1C/Common/Export` — 폴더 4개 해소 / edge 1개 / 파일참조 1개 |
| 2순위 | `Utility/MRA/Common` — 폴더 6개 / edge 3개 / 파일참조 9개 |
| 제외 대상 | `HAL/.../SLEEP_BLOCK` — 파일참조 1218개로 폴더 4개 (비용 대비 최악) |

---

## STEP 0 — 버전 확인

```
skillsilent run l1-sam-fixer version --
```

**`0.2.70` 이 아니면 여기서 중단한다.** 이후 결과가 무의미하다.

---

## STEP 1 — 분석 실행

19:10 job이 이미 돌았으면 STEP 2로 건너뛰어도 된다.
아니거나 확실치 않으면 순서대로 실행한다.

```
skillsilent run l1-sam-fixer mcd-report -- --view all --format all --json
skillsilent run l1-sam-fixer mcd-edge-leverage -- --top 20 --json
```

**순서가 중요하다.** `mcd-report` 는 MCD Run이 없으면 스스로 부트스트랩하지만
`mcd-edge-leverage` 는 Run이 없으면 `MCD_RUN_NOT_FOUND` 로 즉시 실패한다.

`MCD_RUN_NOT_FOUND` 가 나오면 artifact 폴더를 지정한다.

```
skillsilent run l1-sam-fixer mcd-report -- --artifact-dir <SAM artifact 폴더> --view all --format all --json
```

artifact 폴더를 모르면:

```
find ~ -name "sam_metrics_mcd_detail_mfs_relations.csv" 2>/dev/null
```

그 파일이 들어 있는 **폴더**가 `--artifact-dir` 값이다.

---

## STEP 2 — 결과 파일 위치 확인

```
ls -1 <run-dir>/reports/
```

`mcd_edge_leverage.json`, `mcd_report.md` 가 있어야 한다.
run-dir 을 모르면:

```
find ~/l1sw-private-skills/l1-sam-fixer/output -name mcd_edge_leverage.json -newermt today 2>/dev/null
```

---

## STEP 3 — 핵심 수치 추출

아래를 그대로 실행한다. 출력 마지막 `ANS9|` 한 줄이 회신 내용이다.

```bash
python3 - <<'PY'
import json, sys, pathlib
p = sys.argv[1] if len(sys.argv) > 1 else None
if not p:
    c = sorted(pathlib.Path.home().glob(
        "l1sw-private-skills/l1-sam-fixer/output/*/reports/mcd_edge_leverage.json"),
        key=lambda x: x.stat().st_mtime)
    p = c[-1] if c else None
if not p:
    print("mcd_edge_leverage.json NOT FOUND"); raise SystemExit(1)
d = json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
g = lambda k: d.get(k)
cand = d.get("folder_demotion_candidates") or []
print("file:", p)
print("-"*66)
for k in ("folder_granularity","folder_count","folder_edge_count",
          "intra_folder_edge_dropped","folders_in_cycle","folder_cyclic_scc_count",
          "self_loop_edge_dropped","candidate_coverage_status","verified_edge_count",
          "folder_model_authority"):
    print(f"  {k:28} = {g(k)}")
print("-"*66)
print(f"  {'target':34}{'freed':>6}{'cut':>5}{'refs':>7}{'eff':>8}")
for c in cand[:8]:
    print(f"  {str(c.get('target_folder'))[:34]:34}{c.get('folders_freed',0):>6}"
          f"{c.get('edges_to_cut',0):>5}{c.get('file_refs_to_change',0):>7}"
          f"{c.get('cost_efficiency',0):>8.3f}")
print("="*66)
top = ";".join(f"{c.get('target_folder')}:{c.get('folders_freed')}/"
               f"{c.get('edges_to_cut')}/{c.get('file_refs_to_change')}" for c in cand[:3])
print("ANS9|gran=%s|fold=%s|fe=%s|intra=%s|incyc=%s|scc=%s|sloop=%s|cov=%s|ncand=%s|top=%s" % (
    g("folder_granularity"), g("folder_count"), g("folder_edge_count"),
    g("intra_folder_edge_dropped"), g("folders_in_cycle"), g("folder_cyclic_scc_count"),
    g("self_loop_edge_dropped"), g("candidate_coverage_status"), len(cand), top))
PY
```

경로가 자동으로 안 잡히면 파일 경로를 인자로 붙인다.

---

## STEP 4 — 보고서 반영 확인

**담당자에게 배포되는 것은 `mcd_report.md` 다.** 여기 없으면 실무에 전달되지 않는다.

```
grep -ci "demotion" <run-dir>/reports/mcd_report.md
grep -i "Upper-boundary" <run-dir>/reports/mcd_report.md | head -3
```

---

## STEP 5 — 개선안 제안 확인

```
skillsilent run l1-sam-fixer improvement-points -- --top 5 --json
```

여기서 나오는 `evidence_level` 이 무엇인지 본다.

| 값 | 의미 |
|---|---|
| `ANALYSIS_REQUIRED` | 코드 사실이 없어 패턴을 못 고름 (**현재 예상값**) |
| `TOPOLOGY_INFERRED` | 위상만으로 후보 제시 |
| `CODE_ANALYZED` | code-analyzer 사실 반영됨 |

`ANALYSIS_REQUIRED` 가 나와도 정상이다. code-analyzer probe(v0.14.0)를
아직 연결하지 않았기 때문이며, **폴더 demotion 제안은 STEP 3에서 이미 나온다.**

---

## 회신 양식

### Q1. 버전

```
[ ] 0.2.70   [ ] 그 외 -> 값 = 
```

### Q2. `ANS9|` 줄 그대로 복사

```
ANS9|
```

### Q3. `folders_in_cycle` 판정

```
[ ] 46  (수동 분석과 일치)
[ ] 다른 값 -> 값 = 
```

### Q4. demotion 후보 표 — STEP 3 출력의 상위 5행 그대로

```

```

### Q5. `mcd_report.md` 에 demotion 섹션

```
[ ] 있음   [ ] 없음
```

### Q6. `improvement-points` 의 `evidence_level`

```
[ ] ANALYSIS_REQUIRED   [ ] TOPOLOGY_INFERRED   [ ] CODE_ANALYZED
[ ] 목록이 비어 있음
```

---

## 판정 기준

| 관측 | 의미 |
|---|---|
| `incyc=46`, 후보에 Export 4/1/1 | **도구가 수동 분석을 재현했다.** 이후 개선안은 도구로 받으면 된다 |
| `incyc` 이 46이 아님 | 다른 스냅샷의 Run이거나 granularity 차이. `intra`, `gran` 값을 함께 본다 |
| `intra=0` | SAM CSV가 폴더 내부 참조를 이미 제외했다는 확인 (수동 분석과 동일) |
| `sloop>0` | v0.2.70 self-loop 필터가 실제로 동작했다는 증거 |
| `ncand=0` | 폴더 순환 미검출. `cov`(`candidate_coverage_status`) 확인 |
| `HAL/.../SLEEP_BLOCK` 이 상위 | **정렬 결함.** `cost_efficiency` 기준이 안 먹은 것 |

---

## 주의

- 읽기 전용이다. 소스, CSV, P4 어느 것도 건드리지 않는다.
- `improvement-points` 가 `ANALYSIS_REQUIRED` 여도 실패가 아니다.
  근거 없이 C++ 패턴을 강행하지 않는다는 정상 종료다.
- 이번 확인의 성패는 **Q3 하나**로 갈린다. 나머지는 보조 지표다.
