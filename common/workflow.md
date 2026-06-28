# 5.x 상세화 워크플로우

## T0. 세션 부팅
- `README.md`, `WORKBOARD.md`, 대상 트랙 `HANDOFF.md`를 확인합니다.

## T1. 원천 식별
- 대상 트랙의 `source_refs.md`에 prompt, legacy, KG 등 원천을 매핑합니다.

## T2. 요구사항 추출
- 원천에서 목적, 입력, 출력, 제약, 완료 기준을 추출합니다.

## T3. 트랙 설계
- `spec/`에 상세 설계 초안을 작성하고 `contracts/`에 계약을 분리합니다.

## T4. 산출물 작성
- `prompt/`, `spec/`, `contracts/` 하위에 트랙 산출물을 작성합니다.

## T5. 자체 검토
- `review_logs/decision_log.md`에 결정과 근거를 기록합니다.

## T6. Staging 구성
- release 후보를 `release/staging/`에 모읍니다.

## T7. Current 승격
- 검증 기준을 충족하면 `release/current/`로 승격합니다.

## T8. 인수인계 및 종료
- `HANDOFF.md`에 다음 세션 시작점, 남은 작업, 주의사항을 남깁니다.
