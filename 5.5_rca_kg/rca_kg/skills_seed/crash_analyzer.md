# crash_analyzer

> **DEPRECATED — do not use for 5.5 RCA KG 신규 case 생성.**  
> Crash/dump 분석은 L1SW Log Analyzer 전담이다. 이 파일은 v1 이력 보존용이며, 필요한 경우 L1SW 산출물 경로를 참조하는 보조 자료로만 사용한다.

최종 업데이트: 2026-06-19  
누적 케이스: 0건 (실습 전)

---

## Trigger Signatures

```
ASSERT              # 추정
FATAL               # 추정
crash               # 추정
backtrace           # 추정
PC=                 # 추정
LR=                 # 추정
stack               # 추정
Segmentation fault  # 추정
abort               # 추정
```

---

## Required Evidence (분석 시 반드시 확인)

1. ASSERT/FATAL/crash 최초 발생 라인 (타임스탬프 포함)
2. call stack / backtrace 전체
3. PC (Program Counter) / LR (Link Register) 값
4. symbol 정보 (함수명, 파일명, 라인번호) — 있는 경우
5. crash 직전 동일 모듈의 error burst 여부
6. crash 전후 N라인 evidence window 전체
7. 재현 여부 (동일 조건에서 반복 발생?)

---

## Root Cause Categories

| category | 설명 | 주요 단서 |
|---|---|---|
| null_pointer_crash | Null pointer 역참조 | PC= 주소 0x0 근방 |
| assertion_failure | ASSERT 조건 실패 | ASSERT 메시지 내 조건식 |
| api_contract_mismatch | 계층간 파라미터 불일치 | crash 직전 IPC 수신 |
| config_parameter_mismatch | 설정값 범위 초과 | 비정상 파라미터로 함수 진입 |

---

## Analysis Checklist

- [ ] crash/FATAL 최초 라인 타임스탬프 확인
- [ ] backtrace 전체 수집 및 call stack depth 확인
- [ ] PC/LR 값 기록 (symbol 변환 가능 시 변환)
- [ ] crash 직전 5~10초 구간 동일 모듈 error 여부 확인
- [ ] crash 이전 어떤 IPC/API 가 마지막으로 수신되었는지 확인
- [ ] 재현 조건 특정 (특정 UE 수? 특정 트래픽? 특정 시나리오?)

---

## Prevent Rule Candidates

- ASSERT 발생 전 error burst 구간 자동 경보 추가
- 동일 PC/LR 주소에서 재현 시 즉시 에스컬레이션
- crash 직전 N초 로그 자동 보존 메커니즘 TC 추가

---

## 누적 패턴 (케이스 추가 시 업데이트)

| 날짜 | case_id | root_cause | confidence | PC/LR |
|------|---------|------------|------------|-------|
| -    | -       | -          | -          | -     |
