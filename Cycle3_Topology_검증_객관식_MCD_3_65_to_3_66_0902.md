# Cycle #3 Topology 검증 프롬프트 — MCD 3.65 → 3.66

## 목적

현재 `l1-sam-fixer v0.2.61` 기준으로 Candidate #1은 MCD 개선 후보에서 제외되었다.

이유:
- break edge가 directed SCC 내부 cycle edge가 아님
- `ch_L1cDrxLteDbState.cpp`는 outgoing edge 0인 leaf node
- `simulated_resolved_cycle_count = 0`
- 따라서 expected gain = 0
- 코드 품질 개선 후보일 수는 있으나 MCD score 개선 근거는 없음

이번 단계에서는 **다음 topology 후보인 Cycle #3**을 검증한다.

---

# 대상 후보

## Cycle

`Cycle #3`

## Break Edge

`ch_HalGapProcLte.cpp -> ch_L1cCpuClkMngr.cpp`

## 알려진 정보

- Edge count: **8**
- Node count: **3**
- Penalty: **-3.0**
- Current Official MCD: **3.65**
- Target MCD: **3.66**
- Required Gain: **+0.01**

---

# 수행 원칙

1. 실제 C++ 코드는 수정하지 않는다.
2. 최신 MCD run만 사용한다.
3. 과거 run과 최신 run을 혼합하지 않는다.
4. topology 검증 전에는 expected gain을 확정하지 않는다.
5. Cycle penalty `-3.0`을 그대로 MCD gain으로 간주하지 않는다.
6. break edge가 cycle에 포함된다는 이유만으로 `EDGE_RESOLVES_CYCLE`로 판정하지 않는다.
7. 가능하면 답변은 **객관식**으로 한다.
8. 객관식으로 표현할 수 없는 실제 수치/경로/근거만 짧은 주관식으로 추가한다.

---

# STEP 1. 최신 Cycle #3 데이터 확인

최신 MCD 결과에서 Cycle #3의 실제 topology 정보를 찾는다.

확인:

- cycle ID
- work_unit
- node 목록
- edge 목록
- SCC 구성
- scored cycle 여부
- penalty
- 관련 파일/클래스
- 해당 break edge 존재 여부

## Q1. Cycle #3 최신 topology 데이터는 존재하는가?

A. 존재하며 node/edge/SCC 모두 확인 가능  
B. 일부만 존재  
C. Cycle #3 데이터 없음  
D. 최신 run 여부 확인 불가

## Q2. `ch_HalGapProcLte.cpp -> ch_L1cCpuClkMngr.cpp` edge는 최신 Cycle #3에 실제 존재하는가?

A. 존재  
B. 존재하지 않음  
C. 유사 edge만 존재  
D. 확인 불가

---

# STEP 2. Directed SCC 내부 edge 여부 확인

다음 break edge가 **실제 directed SCC 내부 edge인지** 확인한다.

`ch_HalGapProcLte.cpp -> ch_L1cCpuClkMngr.cpp`

## Q3. 이 edge는 directed SCC 내부에 포함되는가?

A. YES — source/target 모두 동일 SCC 내부  
B. NO — SCC 외부/경계 edge  
C. SCC 자체를 계산할 수 없음  
D. 확인 불가

## Q4. 이 edge가 directed cycle 형성에 실제 참여하는가?

A. YES — 해당 edge를 포함한 directed cycle 확인  
B. NO — cycle에 직접 참여하지 않음  
C. 간접적으로만 연결됨  
D. 확인 불가

---

# STEP 3. Edge 제거 Simulation

다음 edge를 graph에서 제거했다고 가정한다.

`ch_HalGapProcLte.cpp -> ch_L1cCpuClkMngr.cpp`

그 후 동일 work_unit / SCC / cycle 상태를 다시 계산한다.

확인:

- remaining path
- alternative path
- SCC 크기 변화
- cycle 수 변화
- scored cycle 수 변화
- resolved cycle count

## Q5. edge 제거 후 alternative path가 남는가?

A. 없음  
B. 있음  
C. 일부 topology 정보 부족  
D. 확인 불가

## Q6. edge 제거 후 SCC가 실제 분리되는가?

A. YES — SCC 분리  
B. NO — 동일 SCC 유지  
C. 일부만 변화  
D. 확인 불가

## Q7. `simulated_resolved_cycle_count` 결과는?

A. 0  
B. 1  
C. 2 이상  
D. 계산 불가 / 필드 없음

## Q8. scored cycle penalty가 실제 제거되는가?

A. YES  
B. NO  
C. 일부만 제거  
D. 확인 불가

---

# STEP 4. Topology 최종 판정

다음 기준으로 판정한다.

## EDGE_RESOLVES_CYCLE

아래를 만족:

- SCC 내부 edge
- directed cycle에 실제 참여
- edge 제거 후 SCC 또는 cycle 구조가 깨짐
- `simulated_resolved_cycle_count > 0`
- scored penalty 제거 근거 있음

## EDGE_DOES_NOT_RESOLVE_CYCLE

아래 중 하나:

- SCC 외부 edge
- directed cycle 미참여
- edge 제거 후 SCC 유지
- alternative path 유지
- `simulated_resolved_cycle_count = 0`

## TOPOLOGY_GAIN_UNVERIFIED

다음 중 하나:

- graph 데이터 부족
- SCC 계산 불가
- simulation 불가
- 최신 run 확인 불가

## Q9. 최종 topology status는?

A. `EDGE_RESOLVES_CYCLE`  
B. `EDGE_DOES_NOT_RESOLVE_CYCLE`  
C. `TOPOLOGY_GAIN_UNVERIFIED`

---

# STEP 5. Expected Gain / Predicted MCD

`Q9 = A`인 경우에만 계산한다.

현재:

- Current Official MCD = **3.65**
- Target MCD = **3.66**
- Required Gain = **+0.01**

확인:

- verified removable penalty
- score model 적용 결과
- expected gain
- predicted MCD

## Q10. expected gain 계산 가능 여부는?

A. 가능 — topology + score model 모두 검증됨  
B. topology는 통과했으나 score model 근거 부족  
C. topology 미통과로 계산 불가  
D. 확인 불가

## Q11. 계산된 expected gain은 +0.01 이상인가?

A. YES  
B. NO  
C. expected gain 미확정  
D. 계산 불가

## Q12. predicted MCD는 3.66 이상인가?

A. YES  
B. NO  
C. predicted MCD 미확정  
D. 계산 불가

---

# STEP 6. 실제 코드 수정 후보 승격 여부

## Q13. Cycle #3 후보를 실제 MCD 수정 대상으로 진행 가능한가?

A. 가능 — topology 검증 통과 + gain 근거 있음  
B. 조건부 가능 — topology는 통과했으나 gain/score model 보완 필요  
C. 불가 — edge 제거해도 cycle 미해결  
D. 불가 — topology 검증 자체가 불가능

## Q14. Candidate 상태는?

A. `MCD_FIX_READY`  
B. `PATCH_READY_FOR_REVIEW`만 가능  
C. MCD 후보 제외  
D. 추가 분석 필요

---

# STEP 7. 다음 1개 Action 결정

## Q15. 다음 액션은?

A. 실제 코드 Before/After 상세 수정안 작성  
B. 실제 코드 수정 → Build/UT → SAM 재측정  
C. 다음 topology 후보 분석  
D. Cycle #3 topology evidence 보완  
E. score model / expected gain 계산 보완

판정 기준:

- Q13=A이고 코드 수정안이 이미 충분하면 → B
- Q13=A지만 코드 Before/After가 아직 없으면 → A
- Q13=B이면 → E
- Q13=C이면 → C
- Q13=D이면 → D

---

# 최종 답변 형식

아래 형식을 그대로 사용한다.

```text
[Cycle #3 Topology 검증 결과]

Q1.  A/B/C/D
Q2.  A/B/C/D
Q3.  A/B/C/D
Q4.  A/B/C/D
Q5.  A/B/C/D
Q6.  A/B/C/D
Q7.  A/B/C/D
Q8.  A/B/C/D
Q9.  A/B/C
Q10. A/B/C/D
Q11. A/B/C/D
Q12. A/B/C/D
Q13. A/B/C/D
Q14. A/B/C/D
Q15. A/B/C/D/E

[핵심 수치]
Cycle ID:
Work Unit:
Node Count:
Edge Count:
Penalty:
SCC Size Before:
SCC Size After:
simulated_resolved_cycle_count:
Expected Gain:
Predicted MCD:

[최종 판정]
1. Topology Status:
2. MCD_FIX_READY 여부:
3. 3.65 → 3.66 가능성:
4. 다음 1개 Action:

[필요 시 주관식 — 최대 5줄]
- 객관식만으로 설명할 수 없는 핵심 근거만 작성
```

---

# 금지사항

- 실제 C++ 코드를 이번 단계에서 수정하지 말 것.
- Cycle #3 penalty `-3.0`을 expected gain으로 직접 환산하지 말 것.
- SCC 내부 여부 확인 없이 quick-win으로 승격하지 말 것.
- `simulated_resolved_cycle_count = 0`이면 MCD gain을 부여하지 말 것.
- topology 미검증 상태에서 predicted MCD를 생성하지 말 것.
- 최신 run과 과거 run을 섞지 말 것.
- 현재 공식 MCD 3.65 / 목표 3.66을 임의 변경하지 말 것.

---

# 최종 목적

이번 검증 목적은 단순히 Cycle #3가 문제인지 확인하는 것이 아니다.

**`ch_HalGapProcLte.cpp -> ch_L1cCpuClkMngr.cpp` edge를 제거했을 때 실제 directed SCC/cycle이 해소되는지 검증하고, 검증된 경우에만 MCD expected gain과 3.65 → 3.66 도달 가능성을 계산하여 실제 코드 수정 후보로 승격할지 결정하는 것**이다.
