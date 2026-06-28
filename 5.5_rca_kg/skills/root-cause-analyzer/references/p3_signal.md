# P3 — issue_type 추천 + signal 생성

목표: 분석할 issue_type을 추천하고 signal 파일 생성. 사용자 입력은 선택(비우면 자동).

지시:
1. 입력 경로 비면 `input.selected_l1sw_txt` 사용. 없으면 최신 `_l1sw.txt`(여러 개면 번호만).
2. issue_type 비면 4개(rach_failure, scg_failure, tx_abnormal, l2_max_retransmission) 대표 signature 등장 횟수를 센다. seeds/<issue_type>_analyzer.md의 trigger signature를 참조.
3. 추천 표: `| issue_type | 대표 signature hit 수 | 근거 signature 상위 5 | 판단 |`. 최다 hit 추천하되 전체 경로 입력 요구 말고 "이 issue_type으로 진행할까요?"만.
4. 확정 issue_type으로 signal 생성: 기존 `scripts/*_prefilter.ps1` 우선, 없으면 keywords.yaml 기반 Select-String/grep으로 임시 signal.
5. 출력: `{kg_root}/signals_tool_generate/<YYYYMMDD>_<issue_type>_<source-slug>_signal.txt`.
6. signal 보고: signal 줄 수, signature별 hit, cptime 범위, 시간창 내 module 전체 목록, 미지 모듈 가드 관점 "보이는 모듈이 너무 좁은지" 1차 판단.
7. `p3` 블록 갱신. NEXT_STEP을 P4로.

주의: signal은 자동 산출물(사람이 직접 편집 안 함). P3에서 원인 단정 금지(원인은 P4).
[사람 확인] 추천 issue_type과 signal 줄 수만.
