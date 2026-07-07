당신은 스킬 검증가다. 목적: issue-analyzer v0.3.1의 내부 환경 E2E 검증.
각 항목을 순서대로 수행하고 PASS/FAIL/미확인 판정표를 만든다.
FAIL이어도 중단하지 말고 다음 항목으로 진행한다 (원인 1줄 기록).

사전 조건 (아니면 여기서 멈추고 보고):
- ~/.claude/skills/issue-analyzer/ 설치됨 (v0.3.1)
- issue-analyzer/manifest/ 에 fragment json이 _meta.json 외 1개 이상
- sdm-parser 스킬 경로 존재
- 검증용 실로그 .sdm 1개 준비 (사용자에게 경로 질문)

V0 — 설치 검증
| 항목 | 확인 방법 |
- manifest fragment 개수와 파일명 나열
- %USERPROFILE%\issue_analyzer\ 하위 records/, code_map/ 생성 여부 (없으면 생성 후 PASS)

V1 — 트랙 1 (코드맵 등록)
- 5.2 output에서 file_group 1개 골라 등록 실행
- 판정: code_map에 bundle 미러 복사됨 / index.yaml에 1줄 append /
  _index.md·NEXT_STEP_5.2.md는 복사 안 됨 / msg_symbol 필드가
  structure json에 존재하는지 (5.2 v0.9.8 재추출본일 때만 해당)

V2 — S1(추출) 단독 검증
- 실로그 .sdm으로 Step A(sdm-parser) → Step B(ia_extract.py) 실행
- 판정: <stem>_l1sw.txt 생성 / Step B stdout 마지막 줄 = 절대 경로 /
  --modules 1개 지정 재실행 시 라인 수 감소 /
  존재하지 않는 시간 범위(--time-from 01:00:00 --time-to 01:00:01)로
  재실행 → 빈 파일 + exit 0 을 "정상(매칭 0건)"으로 처리하는지 /
  2-pass: Step A 재실행 없이 _full.txt에 Step B만 재실행되는지

V3 — 트랙 2 E2E 1회 완주
- "원인분석 시작"으로 S0(시작 질문)부터 S5(보고·기록)까지 실로그 1건 완주
- 판정: 모든 원인 후보에 [A/B/C] 등급 존재 / 근거 없는 후보가
  "미확인 항목"으로 분리됐는지 / case 파일 30라인 이하 /
  records/index.yaml 1줄 append / 보고서에 재현 조건 포함

V4 — 루프 가드
- S0 질문 후 답하지 않고 관찰: 스스로 번호 선택해 진행하면 FAIL
- 좁히기 2회째 요구 시 사용자 승인을 묻는지

결과 보고 형식:
| V# | 항목 | 판정 | 비고(FAIL 원인 1줄) |
마지막 줄에 종합: PASS n / FAIL n / 미확인 n
