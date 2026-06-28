# tx_abnormal_analyzer

최종 업데이트: 2026-06-19  
누적 케이스: 0건 (실습 전)

---

## Trigger Signatures

```
TX abnormal         # 추정
tx fail             # 추정
ul grant            # 추정
harq                # 추정
HARQ                # 추정
UL_FAIL             # 추정
```

---

## Required Evidence (분석 시 반드시 확인)

1. TX abnormal 최초 발생 시점
2. UL grant 수신 여부 및 직전/직후 grant 간격
3. HARQ fail/retry 흐름 (몇 번 retry 후 fail?)
4. 동일 bearer/session/correlation_id 기준 burst 구간
5. Downlink 측 이상 여부 (DL 정상 → UL만 이상인지)
6. 스케줄러 측 로그와 PHY 측 로그 시간 비교

---

## Root Cause Categories

| category | 설명 | 주요 단서 |
|---|---|---|
| scheduler_grant_missing | UL grant 미수신 | grant 간격 비정상 |
| harq_retx_exceeded | HARQ 재전송 한계 초과 | retx 횟수 급증 |
| config_parameter_mismatch | 파라미터 설정 오류 | power/timing 비정상 |
| api_contract_mismatch | 계층간 불일치 | PHY/MAC 파라미터 불일치 |

---

## Analysis Checklist

- [ ] TX abnormal 첫 발생 라인 및 타임스탬프 확인
- [ ] UL grant 수신 간격 이상 여부 확인
- [ ] HARQ retry 횟수 카운트 (정상 범위 이내인지)
- [ ] burst 구간 동안 동일 UE/bearer 집중 여부 확인
- [ ] DL 측 로그 동시 이상 여부 확인
- [ ] 문제 구간 전후 스케줄러 로그 확인

---

## Prevent Rule Candidates

- HARQ fail 연속 N회 이상 발생 시 alert 추가
- UL grant 미수신 구간 발생 시 스케줄러 상태 로그 추가
- TX abnormal burst 구간 자동 캡처 TC 시나리오 추가

---

## 누적 패턴 (케이스 추가 시 업데이트)

| 날짜 | case_id | root_cause | confidence |
|------|---------|------------|------------|
| -    | -       | -          | -          |
