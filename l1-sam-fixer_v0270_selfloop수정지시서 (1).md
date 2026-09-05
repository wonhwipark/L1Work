# l1-sam-fixer 수정 지시서 (3차) — self-loop을 의존 순환으로 취급하지 않기

- 대상 버전: **v0.2.69** → v0.2.70
- 성격: **P0 잔여 항목 1건.** 2차 지시서의 P0-3만 미반영
- 범위: 작음. `mcd_edge_leverage.py` 중심, 회귀 테스트 추가

---

## 1. v0.2.69 검증 결과 — 대부분 완료

| 항목 | 상태 | 확인 방법 |
|---|---|---|
| P0-1 헤더 기반 companion 판정 | **완료** | 비표준 파일명(`zz_summary_custom.csv`)으로도 정확히 분류 |
| P0-2 relation 단독 허용 | **완료** | relation만 있을 때 `EDGE_READY_SCORE_UNRESOLVED` 반환 |
| **P0-3 self-loop 금지** | **미반영** | 아래 §2 |
| P1-1 demotion 호출 연결 | **완료** | `folder_demotion_candidates` payload 적재 확인 |
| P1-2 `mcd_report` 소비 | 반영됨 | 참조 4건 |
| P1-3 `improvement_points` | 반영됨 | 참조 4건 |
| P2 `--folder-depth` 정책 등록 | **완료** | `allowed_flags` / `value_flags` 양쪽 |
| 회귀 | **239 tests PASS** | |
| `mcd_folder_graph.py` | 정상 | intra edge 제외, `edge_provenance` 보존 확인 |

**`mcd_folder_graph.py` 는 건드리지 말 것.** 정상 동작한다.

---

## 2. 남은 결함 — self-loop이 검증된 수정 후보로 올라온다

### 재현

```python
units = [{
    "work_unit_id": "S1", "cycle_index": "9", "score_penalty": -0.3,
    "cycle_members": ["src/m/x.cpp"],
    "dependency_edges": [{"from": "src/m/x.cpp", "to": "src/m/x.cpp"}],
}]
mcd_edge_leverage.build(units, top=5)
```

결과:

```
candidate_coverage_status = COMPLETE
verified_edge_count       = 1
topology_eligible_edge_count = 1
edge: src/m/x.cpp -> src/m/x.cpp   simulated_resolved_cycle_count = 1
folders_in_cycle          = 0        <- 폴더 계층은 올바르게 걸러냄
```

**파일이 자기 자신을 참조하는 것은 모듈 간 의존 순환이 아니다.**
그런데 `resolved=1` 로 계산되어 "검증된 MCD 수정 후보"가 된다.

`folders_in_cycle=0` 인 것이 오히려 정상 신호다. 폴더 계층은 intra edge를
제외하므로 self-loop을 걸러내는데, **파일 계층에는 같은 방어가 없다.**

### 실측 영향

실제 artifact 실행에서 **topology fallback 후보 53건이 전부 self-loop**이었다.
담당자에게 존재하지 않는 위반 53건이 제시된다.

### 지금이 더 위험하다

v0.2.69에서 `mcd_report` 에 demotion 배선이 들어갔다.
따라서 보고서에 **진짜 demotion 후보와 self-loop 허위 후보가 섞여서** 나간다.
분리되어 있을 때보다 판단이 어렵다.

---

## 3. 원인

2차 지시서의 P0-1/P0-2로 companion 결합 문제는 해결됐다.
그러나 **이미 만들어진 self-loop을 걸러내는 방어**는 들어가지 않았다.

결합이 정상화되면 self-loop이 생기지 않을 수도 있으나,
**입력이 무엇이든 물리 의존 그래프에 `(a, a)` 가 들어가서는 안 된다.**
방어는 입력 품질과 무관하게 존재해야 한다.

---

## 4. 수정

### 4-1. 그래프 구성 시 self-loop 제외

`mcd_edge_leverage.py` `_build_scope_graphs()` (`:107` 부근)

```python
key = _edge_key(item)
if not key:
    continue
if key[0] == key[1]:                 # 추가
    self_loop_dropped += 1           # 카운트만 하고 그래프에 넣지 않는다
    continue
graph["edges"].add(key)
```

### 4-2. self-loop을 순환으로 인정하는 분기 제거

`mcd_edge_leverage.py:259` `_cyclic_components()`

```python
# 현재
def _cyclic_components(nodes, edges):
    comps = _tarjan(nodes, edges)
    self_loops = {a for a, b in edges if a == b}
    return [set(c) for c in comps if len(c) > 1 or (len(c) == 1 and c[0] in self_loops)]

# 수정
def _cyclic_components(nodes, edges):
    # self-loop은 4-1에서 이미 제외되므로 다중 노드 SCC만 순환이다
    return [set(c) for c in _tarjan(nodes, edges) if len(c) > 1]
```

`mcd_edge_leverage.py:283` `_unit_is_cyclic()` 의 단일 노드 분기도 함께 제거한다.

```python
# 제거 대상
if any(len(comp) == 1 and bool(members & comp) for comp in cyclic):
    return True
```

이 분기는 self-loop을 순환으로 인정하기 위해 존재했다. 4-1 이후 도달 불가능하며,
남겨두면 단일 노드 컴포넌트를 순환으로 오인할 여지가 남는다.

### 4-3. 투명성 — 버린 것을 보고한다

조용히 버리지 않는다. payload에 추가:

```
self_loop_edge_dropped        int    그래프에서 제외된 (a,a) 수
self_loop_source_files        list   상위 10건 (진단용)
```

`self_loop_edge_dropped > 0` 이면 리포트에 한 줄 표기한다.

> 참고: `mcd_folder_graph.py:69` 의 `self_loops` 처리는 intra edge를 이미
> 제외하므로 도달하지 않는 죽은 코드다. 정리해도 좋으나 필수는 아니다.

---

## 5. 사전 확인 1건 (수정 전)

**SAM이 진짜 self-cycle을 보고하는 경우가 있는가?**

| 답 | 처리 |
|---|---|
| 없다 | §4 그대로 진행. 단순 필터로 충분 |
| 있다 | `dependency_edges` 에서만 제외하고 `self_referential_edges` 별도 필드로 보존. MCD 후보로는 올리지 않는다 |

확인 방법: SAM CSV의 `FromPath == ToPath` 행이 존재하는지, 존재한다면
`sam-result.html` 에서 그것이 순환으로 표시되는지.

불확실하면 **보존하는 쪽(있다)** 으로 처리한다. 정보를 지우는 것보다 안전하다.

---

## 6. 검증 기준

- [ ] self-loop만 있는 입력 → `verified_edge_count = 0`, 후보 0건
- [ ] `_cyclic_components()` 가 단일 노드 컴포넌트를 반환하지 않을 것
- [ ] `self_loop_edge_dropped` 가 payload에 노출될 것
- [ ] 정상 순환(다중 노드 SCC) 입력의 결과가 **v0.2.69와 동일**할 것 — 회귀 없음
- [ ] `folder_demotion_candidates` 결과가 변하지 않을 것 (폴더 계층은 이미 self-loop 제외)
- [ ] 신규 회귀 테스트: self-loop 전용 입력 / self-loop + 진짜 순환 혼합 입력
- [ ] 기존 239 tests 전체 통과
- [ ] 기존 액션·인자 제거 없음, 기존 payload 키 삭제 없음

---

## 7. 하지 말 것

- **`mcd_folder_graph.py` 수정** — 정상이다. intra edge를 이미 제외하고 있다
- **companion 판정 로직 재수정** — v0.2.69에서 검증 완료
- **self-loop 정보를 흔적 없이 제거** — 최소한 카운트는 남긴다 (§4-3)

---

## 8. 이후 절차 (수정 완료 후)

1. **실제 artifact로 재실행** — 기대값:
   - `folders_in_cycle` = **46**
   - `L1C/Common/Export` → freed 4 / cut 1 / refs 1
   - `Utility/MRA/Common` → freed 6 / cut 3 / refs 9
   - self-loop 후보 **0건** (현재 53건)
   - `mcd_report.md` 에 demotion 섹션 포함
2. **`L1C/Common/Export` 되참조 1건 수정** — 참조 1개로 폴더 4개.
   목적은 점수가 아니라 **"폴더 4개 해소 = MCD 몇 점"** 캘리브레이션
3. **고정 base 프로토콜로 재측정** — M0 / M0'(재현성) / M1.
   자동 빌드가 base를 올리므로 이것 없이는 효과를 확인할 수 없다

---

## 9. 여전히 미해결

| # | 항목 | 비고 |
|---|---|---|
| 1 | SAM scoring node가 leaf 폴더인지 논리 모듈인지 | `sam-result.html` 순환 표기 단위로 확인. `folder_of` 는 교체 가능하게 유지 |
| 2 | MCD 점수가 순환 소속 폴더 수에 비례하는지 | §8-2로 캘리브레이션 |
| 3 | 고정 base 측정 프로토콜 | §8-3 |
