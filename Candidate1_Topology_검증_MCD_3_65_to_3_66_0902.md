# Candidate #1 Topology 검증 프롬프트 — MCD 3.65 → 3.66

## 목적

현재 `l1-sam-fixer v0.2.61` 기준으로 Candidate #1의 코드 수정안은 `PATCH_READY_FOR_REVIEW` 상태다.

하지만 MCD 효과는 아직 검증되지 않았다.

현재 상태:

- Current Official MCD: **3.65**
- Target MCD: **3.66**
- Code Proposal: **PATCH_READY_FOR_REVIEW**
- Topology Status: **TOPOLOGY_GAIN_UNVERIFIED**
- Expected Gain: **null**
- Predicted MCD: **미확정**
- 3.65 → 3.66: **NOT VERIFIED**

이번 작업에서는 **실제 C++ 코드를 수정하지 말고**, Candidate #1의 break edge 제거가 실제 cycle 소멸로 이어지는지만 먼저 검증한다.

---

# Candidate #1 정보

## Repository Path

`HAL/MODEM/CmdHdlr/NR/SLEEP_BLOCK/ch_HalSleepProcLte.cpp`

## Absolute Path

`/home/whpark/Project/smp1900/SMPF/Protocol/Channel/L1/HAL/MODEM/CmdHdlr/NR/SLEEP_BLOCK/ch_HalSleepProcLte.cpp`

## Class / Symbol

`GET_DRXLTEDBGETTER().GetDrxStateDb()->GetActiveResumeState()`

## Break Edge

`ch_HalSleepProcLte.cpp -> ch_L1cDrxLteDbState.cpp`

## Fix Pattern

`PROXY_METHOD_ON_GETTER`

의도:

- `DbGetter`에 proxy method 추가
- `ch_HalSleepProcLte.cpp`에서 `ch_L1cDrxLteDbState.cpp`로 향하는 직접 dependency 제거
- 직접 include 제거

## Risk

`MEDIUM`

---

# 수행 요청

현재 최신 MCD 분석 결과를 재사용하라.

가능하면 아래 기존 결과를 먼저 찾는다.

- `mcd_target_plan.json`
- `mcd_improvement_points.json`
- 최신 MCD cycle/topology 데이터
- 최신 기본 MCD report
- Candidate #1이 포함된 cycle/work_unit 정보

과거 run과 최신 run을 섞지 않는다.

---

# STEP 1. Candidate #1이 속한 Cycle 확인

Candidate #1의 아래 정보를 찾는다.

- cycle ID
- work_unit
- cycle 전체 dependency chain
- cycle에 포함된 node 목록
- cycle에 포함된 edge 목록
- Candidate #1 break edge가 실제 cycle 구성 edge인지
- 동일 두 node 사이의 대체 edge가 존재하는지

결과를 추측하지 않는다.

---

# STEP 2. Break Edge 제거 Simulation

다음 edge를 graph에서 제거했다고 가정한다.

`ch_HalSleepProcLte.cpp -> ch_L1cDrxLteDbState.cpp`

그 후 **동일 cycle이 실제로 소멸하는지 topology simulation을 수행**한다.

단순히 해당 edge가 cycle에 포함되어 있다는 이유만으로 cycle 해결로 판단하지 않는다.

다음을 반드시 확인한다.

1. 동일 node들 사이에 다른 경로가 남아 있는가
2. alternative path로 cycle이 유지되는가
3. 해당 edge 제거 후 strongly connected component가 분리되는가
4. 동일 work_unit에서 다른 cycle이 남는가
5. Candidate #1 수정으로 실제 scored cycle penalty가 제거되는가

---

# STEP 3. Topology 판정

아래 중 하나로만 판정한다.

## A. EDGE_RESOLVES_CYCLE

조건:

- break edge 제거 후 해당 cycle이 실제로 소멸
- alternative cycle/path가 남지 않음
- scored cycle penalty 제거 근거가 있음

이 경우:

- expected_gain 계산
- predicted MCD 계산
- 3.65 → 3.66 도달 여부 계산

## B. EDGE_DOES_NOT_RESOLVE_CYCLE

조건:

- break edge 제거 후에도 동일 cycle 또는 alternative cycle이 유지
- 해당 edge 하나만 제거해서 penalty가 사라지지 않음

이 경우:

- expected_gain = 0
- Candidate #1을 단일-edge quick-win에서 제외
- 다음 topology-resolvable candidate를 추천

## C. TOPOLOGY_GAIN_UNVERIFIED

조건:

- cycle/work_unit graph 데이터 부족
- edge 정보 불완전
- simulation 수행 불가
- topology 근거 부족

이 경우:

- expected_gain = null 유지
- predicted MCD = 미확정
- 무엇이 부족한지 정확히 1~3개 항목으로 제시

---

# STEP 4. Expected Gain 계산

`EDGE_RESOLVES_CYCLE`인 경우에만 계산한다.

현재 공식 점수:

`3.65`

목표 점수:

`3.66`

아래를 계산한다.

- cycle penalty
- 제거 가능한 verified penalty
- expected_gain
- predicted MCD after fix
- target reachability

예:

```text
Current Official MCD = 3.650
Verified Expected Gain = +0.012
Predicted MCD After Fix = 3.662
Target = 3.660
Result = TARGET REACHABLE
```

주의:

- `TOPOLOGY_GAIN_UNVERIFIED` 후보에 gain을 임의 부여하지 않는다.
- `EDGE_DOES_NOT_RESOLVE_CYCLE`이면 expected_gain은 0으로 본다.
- predicted MCD는 공식 확정 점수가 아니다.
- 최종 점수는 실제 코드 수정 후 SAM 재측정으로 확정한다.

---

# STEP 5. 코드 수정 여부 결정

이번 작업에서는 실제 코드를 수정하지 않는다.

Topology 검증 결과에 따라 다음 액션만 결정한다.

## EDGE_RESOLVES_CYCLE

다음 액션:

`Candidate #1 실제 코드 수정 -> Build/UT -> SAM 재측정`

## EDGE_DOES_NOT_RESOLVE_CYCLE

다음 액션:

`Candidate #1 제외 -> 다음 topology-resolvable candidate 분석`

## TOPOLOGY_GAIN_UNVERIFIED

다음 액션:

`부족한 cycle/work_unit/topology evidence 보완`

---

# 최종 출력 형식

아래 형식을 그대로 사용한다.

```text
[Candidate #1 Topology 검증 결과]

Candidate:
ch_HalSleepProcLte.cpp -> ch_L1cDrxLteDbState.cpp

Cycle ID:
Work Unit:

Topology Status:
EDGE_RESOLVES_CYCLE / EDGE_DOES_NOT_RESOLVE_CYCLE / TOPOLOGY_GAIN_UNVERIFIED

Cycle Before:
-

Edge Removed:
ch_HalSleepProcLte.cpp -> ch_L1cDrxLteDbState.cpp

Cycle After:
-

Alternative Path:
YES / NO / UNKNOWN

Verified Cycle Resolved:
YES / NO / UNKNOWN

Expected Gain:
Predicted MCD:
Target 3.66:
REACHABLE / NOT REACHABLE / NOT VERIFIED

Code Proposal:
PATCH_READY_FOR_REVIEW

실제 코드 수정:
NOT EXECUTED

[판정]
1. Candidate #1을 실제 수정 대상으로 진행 가능한가:
2. 근거:
3. 다음 1개 Action:
```

---

# 금지사항

- 이번 단계에서 실제 C++ 코드를 수정하지 말 것.
- break edge가 cycle에 있다는 이유만으로 `EDGE_RESOLVES_CYCLE`로 판정하지 말 것.
- topology 검증 없이 expected_gain을 계산하지 말 것.
- `simulated_resolved = 0`인데 cycle penalty 전체를 gain으로 사용하지 말 것.
- 과거 run과 최신 run을 혼합하지 말 것.
- 현재 공식 점수 3.65와 목표 3.66을 임의 변경하지 말 것.
- Candidate #1이 `PATCH_READY_FOR_REVIEW`라는 이유만으로 MCD 효과까지 검증됐다고 판단하지 말 것.

---

# 최종 목적

이번 단계의 목적은 하나다.

**`ch_HalSleepProcLte.cpp -> ch_L1cDrxLteDbState.cpp` dependency를 제거하면 실제로 MCD cycle이 소멸하는지 확인하고, 그 결과가 검증된 경우에만 expected_gain과 3.65 -> 3.66 도달 가능성을 계산한다.**
