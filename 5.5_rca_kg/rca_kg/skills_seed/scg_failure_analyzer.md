# scg_failure_analyzer

최종 업데이트: 2026-06-19  
누적 케이스: 0건 (실습 전)

---

## Trigger Signatures

```
scgFail             # 추정
SCG                 # 추정
PSCell              # 추정
B1Event, B2Event    # 추정
measReport          # 추정
RLF                 # 추정
T310, T311          # 추정
beamFail            # 추정
dualConn            # 추정
SCG-Config          # 추정
```

※ 실제 로그 확인 후 `# 확인됨` / `# 삭제` 로 업데이트 필요

---

## Required Evidence (분석 시 반드시 확인)

1. SCG add/modify 요청 시작 시점
2. B1/B2 measurement event 발생 여부 및 측정값
3. PSCell 또는 secondary cell 관련 이벤트 흐름
4. RLF 발생 시점 및 타이머 (T310/T311) 동작 여부
5. SCG failure 후 fallback (SCG release) 또는 재시도 여부
6. 동일 UE의 MN(Master Node) 측 로그와 시간 비교

---

## Root Cause Categories

| category | 설명 | 주요 단서 |
|---|---|---|
| nr_reconfig_timeout | SCG 재설정 타임아웃 | SCG-Config 후 응답 없음 |
| radio_access_timeout | PSCell 무선 접속 실패 | B2 event 후 접속 실패 |
| api_contract_mismatch | MN/SN 간 파라미터 불일치 | measReport 파라미터 오류 |
| config_parameter_mismatch | 측정 임계값 오류 | B1/B2 threshold 비정상 |

---

## Analysis Checklist

- [ ] SCG add/modify 최초 요청 라인 확인
- [ ] B1/B2 이벤트 발생 시점 및 RSRP/RSRQ 값 확인
- [ ] T310/T311 타이머 동작 여부 확인
- [ ] SCG failure 직전 PSCell 측 에러 확인
- [ ] MN 측 로그와 타임스탬프 비교 (비동기 이슈 확인)
- [ ] fallback 또는 SCG release 이후 복구 여부 확인

---

## Prevent Rule Candidates

- B2 event threshold 값 검토 (너무 민감하게 설정 시 불필요한 SCG add/remove 반복)
- T310 만료 후 recovery 절차 정상 동작 여부 TC 추가
- SCG-Config 적용 후 응답 timeout 발생 시 로그 레벨 상향

---

## 누적 패턴 (케이스 추가 시 업데이트)

| 날짜 | case_id | root_cause | confidence |
|------|---------|------------|------------|
| -    | -       | -          | -          |
