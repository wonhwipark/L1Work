# [사내 Claude Code 실행용] MCD 검토 및 개선 제안 수령 절차

전제: `MCD_handoff_20260908_v2.zip` 압축 해제 완료
소요: 설치 1분 + 정답 확보 3분 + 도구 수리(가변)

> **경로는 `<...>` 로 표시했다. 실행 전에 실제 값으로 바꿀 것.**

---

## 채워 넣을 값

| 이름 | 설명 | 값 |
|---|---|---|
| `<BUNDLE>` | 번들 압축 해제 위치 | `.../MCD_handoff_20260906` |
| `<REL_CSV>` | `*mfs_relations*.csv` **파일** 절대경로 | |
| `<BRANCH_ROOT>` | C++ 소스 루트 | `/home/whpark/Project/smp1900/SMPF/...` |

`<REL_CSV>` 를 모르면:

```
find ~ -name "*mfs_relations*.csv" 2>/dev/null
```

> `<BRANCH_ROOT>` 는 이전 확인에서 `.../SMPF/Protocol/Channel/L1` 로 92개 경로가
> 모두 직접 매칭(`DIRECT_OK`)되었다. 다만 그것이 SAM 의 scope 인지는 미확정이며,
> scope 가 다르면 STEP 2 의 수치도 달라진다.

---

## STEP 1 — 설치

```
cd <BUNDLE>
python3 install_all.py --required-only
```

`l1-sam-fixer 0.2.71` + `code-analyzer 0.14.0` 만 설치한다.
이미 같은 버전이면 `SKIP_CURRENT` 로 건너뛴다. 여러 번 실행해도 안전하다.

전부 설치하려면 `--required-only` 를 뺀다.
`job-list`(스케줄러)와 `l1sw-dispatcher`(사외 원격 관측)는 선택이며,
사내에서 직접 실행한다면 필요 없다.

확인:

```
skillsilent run l1-sam-fixer version --
```

---

## STEP 2 — 정답 먼저 확보 ★ 순서가 중요하다

```
python3 <BUNDLE>/scripts/mcd_folder_cycles.py <REL_CSV>
```

**도구를 고치기 전에 정답을 잡는다.** 이 스크립트는 `l1-sam-fixer` 를 거치지 않고
CSV 를 직접 파싱한다. 설치도 run 디렉터리도 보지 않는다.

반대 순서로 하면 도구의 오류를 정답으로 착각하게 된다.

파일 대신 폴더를 줘도 되지만, `mfs_relations` 계열이 여러 개면 합쳐지므로
**파일 하나를 직접 지정하는 쪽을 권한다.** 열 이름(`FromPath`/`ToPath`)으로
판정하므로 다른 CSV 는 자동으로 건너뛴다.

### 확인할 것

첫 줄에서 어떤 파일을 몇 행 읽었는지 나온다.

```
mfs_relations.csv rows=...
rows=...  files=...  edges=...
```

그리고 세 가지를 기록한다. **이후 모든 판단의 기준선이다.**

```
파일 단위 순환 (cyclic SCC)     =
폴더 단위 (leaf): 폴더 수        =
                  폴더 edge      =
                  intra dropped  =
                  순환 폴더 수    =
```

`intra dropped = 0` 이면 SAM CSV 가 폴더 내부 참조를 이미 제외했다는 뜻이며,
MCD 가 파일이 아니라 상위 경계 단위임을 뒷받침한다.

### 여기서 이미 개선 후보가 나온다

출력의 `[DEMOTE]` 섹션이 DB 폴더 후보다.
`in`(자기를 참조하는 폴더 수)이 크고 `out`(자기가 참조하는 폴더 수)이 작을수록 좋다.

더 자세한 작업 목록:

```
python3 <BUNDLE>/scripts/mcd_demotion_plan.py <REL_CSV> --focus Export
python3 <BUNDLE>/scripts/mcd_demotion_plan.py <REL_CSV> --focus Utility
```

`[P-3]` 섹션에 **되참조 하나하나와 그 뒤의 실제 파일 참조**가 나온다.
이것이 코드 수정 지시서 역할을 한다. **도구 수리를 기다리지 않아도 된다.**

---

## STEP 3 — 도구 수리 (`NO_EDGE_INPUT`)

직전 실행에서 `l1-sam-fixer` 가 `edge_source_health=NO_EDGE_INPUT` 을 냈다.
STEP 2 결과와 대조하면 도구가 무엇을 놓치는지 드러난다.

절차: `docs/MCD_사내PC_NO_EDGE_INPUT_반복추적.md` 의 R1~R6.

핵심 확인 지점:

```
<run-dir>/baseline/inventory.json  ->  mcd_score_bridge
    status, reason_code, relation_file, scanned_csvs, ambiguous_roles
```

| 관측 | 원인 |
|---|---|
| `scanned_csvs` 에 `mfs_relations` **있는데** `relation_file` 이 빔 | 헤더 판정 문제 |
| `scanned_csvs` 에 **없음** | 탐색 범위 문제 (v0.2.71은 하위 1단계까지) |
| `ambiguous_roles` 에 `relation` | 같은 역할 후보가 2개 이상 |

**`mcd_folder_graph.py` 는 정상이므로 건드리지 않는다.** 입력이 문제다.
`PROXY_MODEL_MISMATCH` 로직도 삭제하지 않는다. 정확한 진단이었다.

---

## STEP 4 — 개선 제안 수령

```
skillsilent run l1-sam-fixer mcd-report -- --view all --format all --json
```

생성물:

```
<run-dir>/reports/mcd_report.html
<run-dir>/reports/mcd_edge_leverage.json
```

### HTML 최상단 판정 배너를 먼저 읽는다

| 배너 | 의미 | 다음 |
|---|---|---|
| **먼저 이것을 고치십시오** | 정상 | 대상 폴더 · 해소 폴더 수 · 실제 코드 참조가 제시된다 |
| **이 보고서는 아직 신뢰할 수 없습니다** | 수집이 깨짐 | STEP 3 으로 |
| **개선 후보가 만들어지지 않았습니다** | 순환 0 이면 정상 | `candidate_coverage_status` 확인 |

**후보 0건을 "고칠 것이 없다" 로 읽지 말 것.**
배너가 정상이 아니면 "읽지 못했다" 는 뜻이다.

그 아래 **섹션 D — 폴더 단위 개선 후보(demotion)** 가 작업 목록이다.
`고칠 코드` 대비 `해소 폴더` 순으로 정렬된다.

### STEP 2 와 대조

`folder_demotion_candidates` 가 STEP 2 결과와 일치해야 한다.
다르면 도구가 아직 다른 데이터를 보고 있는 것이다.

---

## STEP 5 — 병렬 작업 (STEP 3 을 기다리지 않는다)

### P0-A. 재발 방지 게이트

개선 투입이 0건인 채 코드가 계속 들어와 지표가 악화 중이다.
유입을 막지 않으면 폴더를 다 풀어도 제자리다.

`mcd_folder_cycles.py` 가 CSV 하나로 순환 폴더 수를 내므로
**스킬 설치 없이 게이트를 만들 수 있다.**

```
CL 제출 전 또는 정기 빌드 시
  순환 폴더 수를 직전 기준선과 비교
  증가하면 경고  ->  안정화 후 차단
```

### P0-B. `L1C/Common/Export` 되참조 1건

```
ch_L1cAllocatorUtil.hpp  ->  Utility/MRA/Common/ch_MraUtilRadio.cpp
```

참조 1개로 폴더 4개. 이미 확정된 값이라 도구가 다시 뽑을 필요가 없다.

`.hpp` 가 `.cpp` 를 참조하는 형태이므로 헤더의 인라인/템플릿 정의가
그 .cpp 함수를 호출할 가능성이 높다. 해법은 둘이다.

1. 인라인 정의를 `.cpp` 로 내린다
2. 필요한 기능을 `Export` 안으로(또는 더 하위로) 옮긴다 ← 팀의 DB 폴더 방식

**목적은 점수가 아니라 환산율이다.** 반드시 고정 base 에서 측정한다.

```
동일 base 리비전 고정 (중간 sync 금지)
  M0   수정 전                -> S0
  M0'  코드 변경 없이 재측정   -> S0r     <- 재현성 검사. 생략 금지
  M1   수정 후                -> S1
```

```
python3 <BUNDLE>/scripts/mcd_ab_verify.py \
    --before <snap_before> --after <snap_after> \
    --s0 <S0> --s0r <S0r> --s1 <S1>
```

`S0 != S0r` 이면 SAM 이 비결정적이라는 뜻이고, **그 경우 다른 작업을 멈추고**
SAM 설정·캐시·scope 부터 확인한다. 재현성이 없으면 어떤 개선도 검증할 수 없다.

`S1 - S0` 이 **폴더 4개 해소의 실제 점수**다. 이 값이 나와야
나머지 폴더 작업의 가치와 3.77 도달 가능성을 계산할 수 있다.

---

## 두 artifact 비교가 필요할 때

수정 전/후 artifact 폴더가 각각 있으면:

```
skillsilent run l1-sam-fixer mcd-compare -- \
    --ref-artifact-dir <ref 폴더> \
    --after-artifact-dir <fix 폴더> \
    --folder-depth leaf --json
```

`folder_comparison` 에 순환 폴더 증감, 해소된 폴더, **새로 순환에 들어간 폴더(회귀)**,
남은 demotion 후보가 나온다.

한쪽이라도 cross-folder edge 가 없으면 숫자 대신 `UNCOMPARABLE` 을 낸다.
깨진 수집 위에서 잰 delta 를 개선으로 제시하지 않기 위함이다.

---

## 최종 목표와의 관계

| 층위 | 내용 | 이 절차에서 |
|---|---|---|
| 1. 어디를 | 어느 폴더의 어느 참조 | **STEP 2, 4 에서 나온다** |
| 2. 어떻게 | 어떤 C++ 기법으로 | probe 연결 후 (P2) |
| 3. 몇 점 | MCD 가 얼마나 오르나 | **STEP 5 의 P0-B 실험으로만** |

**최종 목표는 공식 SAM MCD 3.77 이다.** 도구가 제안을 내는 것 자체는 목표가 아니라
폴더를 반복 처리하기 위한 수단이다.

개선 확정은 **공식 SAM 재측정으로만** 한다. 도구의 예상 gain 은 예상치다.

---

## 하지 말 것

| 항목 | 이유 |
|---|---|
| include graph 구축 | edge 는 이미 CSV 에 있다. 집계 단위가 문제였다 |
| `mcd_folder_graph.py` 수정 | 정상이다. 입력이 문제다 |
| `PROXY_MODEL_MISMATCH` 로직 삭제 | 정확한 진단이었다 |
| `HAL/.../SLEEP_BLOCK` 착수 | 참조 1218개로 폴더 4개. 비용 대비 최악 |
| base 고정 없는 개선 검증 | 결과를 해석할 수 없다 |
| 도구 완성을 기다리며 개선 보류 | **현재 악화의 직접 원인이다** |
