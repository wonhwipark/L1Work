# RCA Standalone cleanup v0.7 — L1SW-first 정합성 정리

작성: 20260625_0024 KST
근거: RCA_L1SW_FIRST_CLEANUP_WORKFLOW_20260624_2353_KST.md (제안서) 리뷰 후 채택

## 변경 목적
L1SW 실행 결과인 `_l1sw.txt`를 RCA 5.5의 기준 입력으로 명확히 고정. RCA 기능 확장 아님 — 실행 흐름 정합성 정리.

## 변경 파일
| 파일 | 변경 요약 |
|---|---|
| rca_kg/indexes/index.md | signature alias(Msg1) → keywords.yaml ID(RACH_MSG1) 통일; 통계 표 실제/예시 case 분리 |
| USAGE_SCENARIO_5.5.md | 삭제된 `5_5_..._prompt.md` 참조 제거; RUNBOOK·MCP 참조로 트리 갱신 |
| HANDOFF_5.5.md | §0 L1SW-first 목적 + cleanup 상태표 추가; 트리의 stale TODO 3건을 현재 상태값으로 전환 |
| VERSION_5.5.md | 신규 — 패키지 버전/목적/상태(pre-E2E validation) 1장 요약 |

## 제안서 대비 처리 내역
- Step1(HANDOFF), Step3(USAGE), Step5(index alias), Step7(VERSION): 적용 완료
- Step6(schema unresolved case_id 예외): 이미 schema note(L26~27)에 명시돼 있어 추가 형식화 보류(동작상 충돌 없음)
- Step2(RUNBOOK 경로 예시화), Step4(P0~P6 문구): RUNBOOK은 이미 절대경로에 "P0/P1 결과를 따른다" 병기 + P3에 _l1sw 입력 명시돼 있어 현 상태 유지. 추가 강화는 차기 선택.

## 변경하지 않은 것
- keywords.yaml candidate/confirmed 상태: 실로그 근거 없이 변경 안 함
- 실제 case 승격 없음; 실로그 E2E 완료로 표기하지 않음 (현재 pre-E2E validation)
- 이력 문서(delta/, session_log)의 py_package 언급: 과거 사실 기록이므로 보존

## 검증
- 필수 파일 8종 존재 OK
- YAML 6종 파싱 OK
- index.md alias 잔존 0건
- 활성 운영 문서 py_package 참조 0건 (이력 문서만 잔존 — 허용)
