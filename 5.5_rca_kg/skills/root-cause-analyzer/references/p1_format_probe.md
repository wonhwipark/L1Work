# P1 — L1SW 출력 형식 역설계

목표: `_l1sw.txt`의 실제 줄 형식을 역설계해 다음 단계가 자동으로 읽게 저장.

입력: `input.selected_l1sw_txt` 우선. 비면 최신 `_l1sw.txt` 탐색(여러 개면 번호만). 없으면 C0_RUN_L1SW로 넘기고 멈춤.

지시:
1. 앞부분 50줄 + 전체 무작위 30줄 확인. 사내 민감 토큰은 `<MASK>`.
2. 형식 명세 작성: cptime 위치·포맷, module/component 위치, severity/log level 유무, UE/session/correlation id 후보 필드, 줄 필드 순서, cptime_range 추출용 정규식 후보.
3. `{kg_root}/runtime_tool_generate/format_profiles/L1SW_OUTPUT_FORMAT_PROBED_<YYYYMMDD>_<HHMM>_KST.md`에 저장(타임스탬프 도구가 채움). 맨 위 문구: "이 문서는 실제 _l1sw.txt 샘플에서 역설계한 형식 명세다."
4. 확인된 내용 "확인됨", 추정 "추정" 표시.
5. `{kg_root}/runtime_tool_generate/current_run.yaml`의 `p1.output_format_doc`, `p1.cptime_format`, `p1.module_field_format` 갱신. NEXT_STEP을 P2 안내로.

이 결과는 P2 manifest fragment와 P4 cptime_range 추출 기준으로 쓰인다.
[사람 확인] cptime 포맷 한 줄만 실제 로그와 맞는지.
