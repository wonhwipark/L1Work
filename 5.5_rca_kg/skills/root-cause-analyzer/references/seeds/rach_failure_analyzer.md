# rach_failure_analyzer

최종 업데이트: 2026-06-19  
누적 케이스: 0건 (실습 전)

---

## Trigger Signatures

아래 중 하나 이상 로그에 등장하면 RACH failure 분석 시작.

```
PHY_TIMER_EXPIRY    # 확인됨
RACH                # 추정
rach_fail           # 추정
msg2 timeout        # 추정
RAR timeout         # 추정
preamble            # 추정
RA-RNTI             # 추정
```

---

## Required Evidence (분석 시 반드시 확인)

1. RACH attempt 시작 시점 (msg1 전송)
2. msg1 → msg2 → msg3 → msg4 진행 단계 중 최초 실패 지점
3. RAR 수신 여부 및 timeout 발생 여부
4. 동일 UE/session/correlation_id 기준 직전/직후 이벤트
5. 동일 cell 내 다른 UE의 RACH 성공 여부 (단일 UE 이슈 vs cell 이슈 구분)
6. 재시도 횟수 및 backoff 동작 여부

---

## Root Cause Categories

| category | 설명 | 주요 단서 |
|---|---|---|
| radio_access_timeout | RAR/msg2 응답 없음 | msg2 timeout 반복 |
| preamble_collision | 동일 preamble 충돌 | 재시도 시 동일 preamble 사용 |
| scheduler_grant_missing | UL grant 미수신 | msg3 미전송 |
| config_parameter_mismatch | 타이머/파라미터 오류 | 비정상 짧은 timeout |
| api_contract_mismatch | 계층간 파라미터 불일치 | REQ/CNF 파라미터 불일치 |

---

## Analysis Checklist

- [ ] signal 파일에서 `PHY_TIMER_EXPIRY` 첫 등장 라인 확인
- [ ] msg1 ~ msg4 중 어느 단계에서 실패했는지 특정
- [ ] 동일 UE 기준 RACH 재시도 횟수 카운트
- [ ] RAR timeout 연속 발생 여부 확인
- [ ] 동일 cell 내 다른 UE의 RACH 성공 여부 확인
- [ ] 관련 API/IPC (REQ, CNF) 파라미터 확인
- [ ] 직전 이벤트에서 scheduling 이상 징후 확인

---

## Prevent Rule Candidates

- msg2 timeout 3회 이상 연속 발생 시 RACH parameter 점검
- 동일 cell 다수 UE에서 RACH failure 발생 시 cell load 및 scheduler 확인
- PHY_TIMER_EXPIRY 후 fallback 동작이 없으면 연결 해제 가능성 경고

---

## 누적 패턴 (케이스 추가 시 업데이트)

| 날짜 | case_id | root_cause | confidence |
|------|---------|------------|------------|
| -    | -       | -          | -          |
