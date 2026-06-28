# l2_max_retransmission_analyzer

최종 업데이트: 2026-06-19  
누적 케이스: 0건 (실습 전)

---

## Trigger Signatures

```
max retransmission  # 추정
RLC                 # 추정
HARQ                # 추정
retx                # 추정
MAX_RETX            # 추정
rlc_fail            # 추정
```

---

## Required Evidence (분석 시 반드시 확인)

1. max retransmission 발생 시점
2. RLC 재전송 burst 구간 (시작~종료 타임스탬프)
3. HARQ retransmission 횟수 및 패턴 (연속인지 간헐적인지)
4. 동일 UE/RB/session 기준 반복 발생 횟수
5. 무선 링크 품질 (RSRP/SINR) 로그 직전 상태
6. 스케줄러 측 grant 할당 상태

---

## Root Cause Categories

| category | 설명 | 주요 단서 |
|---|---|---|
| rlc_max_retransmission | RLC 최대 재전송 도달 후 RLF | RLC retx 카운터 max |
| harq_retx_exceeded | HARQ 한계 초과 | HARQ retx 급증 |
| radio_access_timeout | 무선 환경 열화 | RSRP/SINR 급락 직전 |
| config_parameter_mismatch | 재전송 횟수 설정 오류 | max retx count 비정상 |

---

## Analysis Checklist

- [ ] max retransmission 최초 발생 라인 확인
- [ ] RLC retransmission burst 구간 타임스탬프 범위 확인
- [ ] HARQ retry 횟수 추이 확인 (급증 구간 특정)
- [ ] 동일 UE/RB 에서 반복 발생 횟수 확인
- [ ] 무선 환경 로그 (RSRP/SINR) 동시 열화 여부 확인
- [ ] max retransmission 이후 RLF 발생 여부 및 타임라인 확인

---

## Prevent Rule Candidates

- RLC retx 카운터 N회 이상 시 사전 경고 로그 추가
- 무선 환경 열화 구간에서 자동 retx 파라미터 조정 TC 추가
- max retransmission 후 RLF 전환 여부 모니터링 TC 추가

---

## 누적 패턴 (케이스 추가 시 업데이트)

| 날짜 | case_id | root_cause | confidence |
|------|---------|------------|------------|
| -    | -       | -          | -          |
