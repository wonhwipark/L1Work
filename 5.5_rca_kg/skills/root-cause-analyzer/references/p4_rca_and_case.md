# P4 — 원인분석 7단계 + case YAML 생성/갱신

목표: P3 signal 기준으로 원인분석을 수행하고 schema v2 case YAML을 생성/갱신. 추론 규칙은 methodology.md를 따른다.

입력 자동 선택: `p3.signal_file` 우선, `p3.selected_issue_type` 우선. 없으면 `signals_tool_generate/*_signal.txt` 최신(번호만).

## PART A — 원인분석 7단계
1. 증상 anchor를 잡는다.
2. cptime 시간창을 정한다(wall-clock 아님, cptime 기준).
3. 정상경로 대비 최초 이탈 지점을 찾는다. issue_type seed(seeds/<issue_type>_analyzer.md)의 정상경로·required evidence 참조.
4. 미지 모듈 가드 적용: 원인 줄이 signal/_l1sw.txt에 없고 주변이 비면 단정 금지. 추가 추출(시간창/모듈/명령 후보) 제시하고 멈춤. 누적은 `p4.extraction_attempt_count`. 2회 후에도 없으면 analyzed + confidence: low + 원인 미상으로 정직 종료.
5. 가설 최소 2개, 최대 4개.
6. 가설을 가르는 단서만 추가 확인.
7. 단말/환경/계층/API/설정 문제를 분리.
8. root_cause.summary는 "A 때문에 B가 발생했고 그 결과 C가 실패했다" 인과사슬로.
9. confidence는 methodology 기준 산정. 근거 부족 시 low 유지.

## PART B — case YAML 생성/갱신

모든 case YAML은 `{kg_root}/cases/`(미해결은 `{kg_root}/cases/unresolved/`)에만 생성·갱신한다. cwd가 로그 폴더여도 그 폴더에 만들지 않는다.
1. case_id는 날짜가 아니라 fingerprint 기반: `<fingerprint-slug>_<issue_type>_<3-digit-seq>`.
2. fingerprint 블록 필수: signature_set(등장 signature ID), sequence(cptime 상대 순서), sequence_status(자동 초안=draft).
3. line_range/raw_examples/time_range 사용 금지.
4. 위치 정보는 cptime_range만.
5. Jira 참조는 recent_occurrences[].jira에만.
6. 신규 생성 전 기존 case와 fingerprint(signature_set+sequence) 비교.
7. fingerprint 일치하면 신규 YAML 만들지 말고 기존 case의 occurrence_count/recent_occurrences/last_seen만 갱신.
8. 담당영역 밖이면 `{kg_root}/cases/unresolved/<YYYYMMDD>_<issue_type>_<seq>_PENDING.yaml` 생성, root_cause/fix/review는 null.
9. crash/dump는 RCA KG 대상 아님 — crash case 생성 금지.
10. 사람이 원인을 직접 알려준 경우 methodology의 [E] 경로(사람 입력 최소: 인과사슬·근거 로그 유무 / 자동: confidence 산정, status=reviewed 후보, keywords candidate 후보 기록).

완료: `{kg_root}/indexes_tool_generate/index.md`를 fingerprint 기준 갱신. `p4` 블록 갱신(case_file 또는 unresolved_file, root_cause_category, confidence, candidate_signatures_for_p6, extraction_attempt_count, unknown_module_guard). NEXT_STEP을 P5로. 변경 요약을 답변에 포함.
[사람 확인] 인과사슬 1줄, confidence, case 파일 경로만.
