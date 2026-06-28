# 5.5 RCA — Claude Code 자율 실행 프롬프트 모음 (E2E v2, stateful convenience)

작성일: 2026-06-25 01:38 KST  
목적: 사람이 경로와 단계 상태를 반복 입력하지 않도록 `current_run.yaml`과 `NEXT_STEP_5.5.md`를 중심으로 P0~P6를 연결한다.

---

## 공통 운영 규칙 — 모든 P0~P6에 적용

아래 규칙은 모든 프롬프트에서 반드시 지킨다.

```text
@START_HERE_5.5.md
@NEXT_STEP_5.5.md
@rca_kg/runtime_tool_generate/current_run.yaml
```

1. 작업 시작 시 `rca_kg/runtime_tool_generate/current_run.yaml`을 먼저 읽는다.
2. 이전 단계 산출물이 있으면 사용자가 다시 경로를 입력하지 않아도 자동 사용한다.
3. 여러 후보가 있으면 전체 경로를 타이핑하게 하지 말고 번호만 묻는다.
4. 각 단계 종료 시 `current_run.yaml`의 `current_step`, `next_step`, `last_updated_kst`, 해당 P단계 블록을 갱신한다.
5. 각 단계 종료 시 `NEXT_STEP_5.5.md`를 갱신한다.
6. 각 단계 종료 시 필요한 경우 `review_logs/*_<YYYYMMDD>_<HHMM>_KST.md`를 생성한다. 이때 `<YYYYMMDD>`와 `<HHMM>`은 사람이 적지 않는다. 도구가 현재 KST 시각으로 채운다. 파일명 안의 모든 타임스탬프 placeholder도 동일하다.
7. 모든 응답 맨 끝에 진행 한 줄을 붙이고, 바로 다음 줄에 사용자가 다음에 붙여넣을 프롬프트 블록을 한 줄로 안내한다.

진행 줄 형식:

```text
[진행: <방금 끝낸 단계> 완료 → 다음: <다음 단계와 할 일>. <생성/변경 요약>]
▶ 다음 붙여넣기: prompt/CLAUDE_CODE_PROMPTS_e2e_v1.md 의 <다음 P단계> 블록
```

예:

```text
[진행: P0 완료 → 다음: C0 또는 P1. current_run.yaml/NEXT_STEP 갱신]
▶ 다음 붙여넣기: prompt/CLAUDE_CODE_PROMPTS_e2e_v1.md 의 C0 블록 (또는 _l1sw.txt가 있으면 P1 블록)
```

사용자가 "지금 어느 블록을 붙여넣지"를 스스로 판단하지 않게 한다. 다음 블록 판단 기준이 모호하면 `NEXT_STEP_5.5.md`의 next_step을 따른다.

`_tool_generate` 폴더 의미:

```text
_tool_generate = 도구(Claude Code/스크립트)가 생성·갱신하는 산출물 영역. 사람은 직접 편집하지 않는다.
```

도구가 쓰지만, 승인/원인 판단은 여전히 사람이 한다.

---

## P0 — 환경 자가 진단 + 상태 파일 초기화

> 가장 먼저 1회 실행한다. 기존처럼 보고만 하지 않고, 이후 단계가 읽을 `current_run.yaml`과 `NEXT_STEP_5.5.md`를 갱신한다.

```text
@START_HERE_5.5.md
@NEXT_STEP_5.5.md
@HANDOFF_5.5.md
@scripts/README.md
@rca_kg/runtime_tool_generate/current_run.yaml
@rca_kg/keywords.yaml
@rca_kg/schema/rca_case.schema.yaml

너는 지금 사내 RCA_standalone 작업 폴더 안에서 동작하고 있다.
추측하지 말고 실제 파일 시스템을 확인해서 환경을 진단하고, 그 결과를 상태 파일에 저장해줘.

조사 항목:
1. 현재 작업 루트가 RCA_standalone 폴더인지 확인한다.
2. 이 폴더 아래와 일반 로그 후보 경로에서 .sdm 파일과 _l1sw.txt 파일을 찾는다.
   - 찾은 후보는 경로, 크기, 수정시각을 표로 정리한다.
   - _l1sw.txt 후보가 하나면 current_run.yaml의 input.selected_l1sw_txt에 자동 저장한다.
   - 후보가 여러 개면 번호 목록을 만들고 next_step을 C0_SELECT_L1SW_TXT로 둔다.
   - 후보가 없고 .sdm만 있으면 next_step을 C0_RUN_L1SW로 둔다.
3. L1SW Log Analyzer 스킬 접근성을 확인한다.
   - parse.ps1 후보 경로를 찾는다.
   - manifest 디렉토리와 fragment JSON 파일을 찾는다.
   - 찾은 값은 current_run.yaml의 l1sw 블록에 저장한다.
4. PowerShell 실행 가능 여부를 확인한다.
   - scripts/rach_failure_prefilter.ps1 와 scripts/scg_failure_prefilter.ps1의 파라미터 구조를 확인한다.
   - 이 단계에서는 prefilter를 실행하지 않는다.
5. rca_kg/cases/ 아래 EXAMPLE 외 실제 case 파일 수를 센다.
6. rca_kg/signals_tool_generate/ 와 rca_kg/indexes_tool_generate/ 상태를 확인한다.
7. START_HERE_5.5.md, NEXT_STEP_5.5.md, rca_kg/runtime_tool_generate/current_run.yaml 존재 여부를 확인한다.

출력:
1. 화면에는 아래 표를 보여준다.
   | 항목 | 상태(OK/없음/확인불가) | 근거 경로 | 다음 조치 |
2. review_logs/p0_env_probe_<YYYYMMDD>_<HHMM>_KST.md 를 생성한다.
3. rca_kg/runtime_tool_generate/current_run.yaml 을 실제 값으로 갱신한다.
4. NEXT_STEP_5.5.md 를 다음 단계 기준으로 갱신한다.

next_step 판정:
- _l1sw.txt가 1개 선택 가능하면: P1
- _l1sw.txt 후보가 여러 개면: C0_SELECT_L1SW_TXT
- _l1sw.txt가 없고 .sdm과 parse.ps1이 있으면: C0_RUN_L1SW
- parse.ps1을 못 찾으면: P0_NEEDS_L1SW_PATH

마지막에 "지금 P1부터 시작 가능한가?"를 yes/no로 판정한다.
no면 사람이 먼저 해줘야 할 최소 작업만 1~3줄로 알려준다.
```

`[사람 확인]` P0 표의 "다음 조치"와 `NEXT_STEP_5.5.md`만 확인한다.

---

## C0 — `_l1sw.txt` 확보 분기

> C0는 별도 프롬프트라기보다 P0/P1이 사용하는 분기다. `_l1sw.txt`가 없을 때만 실행한다.

```text
@START_HERE_5.5.md
@NEXT_STEP_5.5.md
@rca_kg/runtime_tool_generate/current_run.yaml
@scripts/README.md

목표: P1에 사용할 _l1sw.txt를 확보해줘.

상태 파일을 읽고 아래 중 하나로 처리해줘.

1. current_run.yaml에 selected_l1sw_txt가 있으면:
   - 파일 존재/크기 확인 후 next_step을 P1로 갱신한다.
   - NEXT_STEP_5.5.md에 P1 실행 안내를 쓴다.

2. l1sw_txt_candidates가 여러 개면:
   - 후보 번호 목록을 보여준다.
   - 사용자가 번호만 입력하면 selected_l1sw_txt에 저장한다.
   - next_step을 P1로 갱신한다.

3. selected_l1sw_txt가 없고 selected_sdm 또는 sdm 후보가 있으면:
   - L1SW parse.ps1 실제 경로와 후보 .sdm을 사용해 실행 명령을 제시한다.
   - parse.ps1 파라미터명이 확실하면 실행해도 된다.
   - 파라미터명이 확실하지 않으면 명령어 후보를 제시하고 멈춘다.
   - 생성된 _l1sw.txt 경로를 selected_l1sw_txt에 저장한다.

4. .sdm도 없으면:
   - next_step을 WAIT_INPUT_LOG로 둔다.
   - NEXT_STEP_5.5.md에 사용자가 배치해야 할 파일 형식과 위치 예시를 적는다.

각 경우 current_run.yaml과 NEXT_STEP_5.5.md를 갱신하고 진행 줄을 출력해줘.
```

`[사람 확인]` `_l1sw.txt` 경로가 맞는지만 확인한다.

---

## P1 — L1SW 출력 형식 역설계

```text
@START_HERE_5.5.md
@NEXT_STEP_5.5.md
@rca_kg/runtime_tool_generate/current_run.yaml
@scripts/README.md

목표: L1SW가 생성한 _l1sw.txt의 실제 줄 형식을 역설계하고, 그 결과를 다음 단계가 자동으로 읽게 저장해줘.

지시:
1. current_run.yaml의 input.selected_l1sw_txt를 우선 사용한다.
   - 비어 있으면 이 작업 폴더에서 최신 _l1sw.txt를 찾는다.
   - 후보가 여러 개면 번호만 묻는다.
   - 없으면 C0_RUN_L1SW 절차로 넘어가고 멈춘다.
2. _l1sw.txt 앞부분 50줄과 파일 전체의 무작위 구간 30줄을 확인한다.
   - 사내 민감정보로 보이는 토큰은 <MASK> 처리한다.
3. 아래 형식 명세를 작성한다.
   - cptime이 줄 어디에 어떤 포맷으로 찍히는가
   - module/component 이름이 줄 어디에 찍히는가
   - severity/log level 표기가 있는가
   - UE/session/correlation id로 쓸 수 있는 필드가 있는가
   - 한 줄의 필드 순서가 대략 어떤 구조인가
   - cptime_range 추출 시 사용할 정규식 후보
4. 결과를 아래 파일명으로 저장한다.
   - prompt/deepdive/L1SW_OUTPUT_FORMAT_PROBED_<YYYYMMDD>_<HHMM>_KST.md
5. 파일 맨 위에 아래 문구를 넣는다.
   - "이 문서는 실제 _l1sw.txt 샘플에서 역설계한 형식 명세다."
6. 확인된 내용은 "확인됨", 추정은 "추정"으로 표시한다.
7. current_run.yaml의 p1.output_format_doc, p1.cptime_format, p1.module_field_format을 갱신한다.
8. NEXT_STEP_5.5.md를 P2 안내로 갱신한다.

이 결과는 P2 manifest fragment 후보와 P4 cptime_range 추출 기준으로 사용한다.
```

`[사람 확인]` cptime 포맷 한 줄만 실제 로그와 맞는지 확인한다.

---

## P2 — L1SW manifest fragment 후보 자동 생성

```text
@START_HERE_5.5.md
@NEXT_STEP_5.5.md
@rca_kg/runtime_tool_generate/current_run.yaml
@rca_kg/keywords.yaml
@scripts/README.md

목표: keywords.yaml 기반으로 L1SW manifest fragment 후보 JSON을 issue_type별로 자동 생성해줘.

입력 찾기:
1. current_run.yaml의 p1.output_format_doc를 우선 사용한다.
2. 비어 있거나 파일이 없으면 prompt/deepdive/L1SW_OUTPUT_FORMAT_PROBED_*_KST.md 중 가장 최신 파일을 자동으로 사용한다.
3. 여러 개이고 최신 판단이 애매하면 번호 목록만 보여준다.

규칙:
1. keywords.yaml을 단일 출처로 사용한다. 키워드를 새로 지어내지 않는다.
2. 각 issue_type에서 use_for.l1sw_manifest_fragment == true 인 signature만 포함한다.
3. use_for.fingerprint == false 인 generic context signature는 manifest fragment에서도 제외한다.
4. P0가 찾은 기존 L1SW fragment JSON을 1개 열어 키 구조를 확인하고 가능한 한 같은 구조로 만든다.
5. 기존 fragment 구조를 못 찾으면 잠정 구조로 만들고 status에 "structure_unverified"를 기록한다.
6. 각 signature의 status(confirmed/candidate)를 fragment 안에 보존한다.

출력 파일:
- rca_kg/manifest_fragments/rca_rach.json
- rca_kg/manifest_fragments/rca_scg.json
- rca_kg/manifest_fragments/rca_tx.json
- rca_kg/manifest_fragments/rca_l2.json

리뷰 로그:
- review_logs/rca_standalone_R4_manifest_fragments_<YYYYMMDD>_<HHMM>_KST.md

리뷰 로그에 포함할 표:
| issue_type | signature_id | 포함/제외 | status | 사유 |
|---|---|---|---|---|

완료 후:
1. current_run.yaml의 p2.generated_fragments와 p2.review_log를 갱신한다.
2. NEXT_STEP_5.5.md를 "실로그마다 L1SW 실행 후 P3" 안내로 갱신한다.
3. keywords.yaml 자체는 수정하지 않는다.
```

`[사람 확인]` review_log의 "기존 구조 일치 여부"만 확인한다.

---

## P3 — issue_type 추천 + signal 생성

```text
@START_HERE_5.5.md
@NEXT_STEP_5.5.md
@rca_kg/runtime_tool_generate/current_run.yaml
@scripts/README.md
@rca_kg/keywords.yaml

목표: 분석할 issue_type을 추천하고 signal 파일을 만들어줘.

사용자 입력은 선택사항이다.
- 이번 대상 issue_type: <비워두면 자동 추천 / 또는 rach_failure | scg_failure | tx_abnormal | l2_max_retransmission>
- 입력 _l1sw.txt 경로: <비워두면 current_run.yaml의 selected_l1sw_txt 사용>

지시:
1. 입력 경로가 비어 있으면 current_run.yaml의 input.selected_l1sw_txt를 사용한다.
2. selected_l1sw_txt가 없으면 최신 _l1sw.txt를 찾고, 여러 개면 번호만 묻는다.
3. issue_type이 비어 있으면 4개 issue_type 대표 signature 등장 횟수를 센다.
   - rach_failure
   - scg_failure
   - tx_abnormal
   - l2_max_retransmission
4. 추천 결과를 아래 형식으로 보여준다.
   | issue_type | 대표 signature hit 수 | 근거 signature 상위 5개 | 판단 |
5. 최다 hit issue_type을 추천하되, 사람에게 전체 경로 입력을 요구하지 말고 "이 issue_type으로 진행할까요?"만 묻는다.
6. 확정된 issue_type 기준으로 signal 파일을 만든다.
   - 가능하면 기존 scripts/*_prefilter.ps1을 사용한다.
   - 해당 issue_type용 ps1이 없으면 keywords.yaml 기반 Select-String/grep으로 임시 signal을 만든다.
7. 출력 파일명:
   - rca_kg/signals_tool_generate/<YYYYMMDD>_<issue_type>_<source-slug>_signal.txt
8. signal 보고에 아래를 포함한다.
   - signal 줄 수
   - signature별 hit 수
   - cptime 범위
   - 시간창 내 module/component 전체 목록
   - 미지 모듈 가드 관점에서 "보이는 모듈이 너무 좁은지" 1차 판단
9. current_run.yaml의 p3 블록을 갱신한다.
10. NEXT_STEP_5.5.md를 P4 안내로 갱신한다.

주의:
- signal은 자동 생성 산출물이므로 사람이 직접 편집하지 않는다.
- 원인 분석은 P4에서 한다. P3에서는 원인을 단정하지 않는다.
```

`[사람 확인]` 추천 issue_type과 signal 줄 수만 확인한다.

---

## P4 — 원인분석 7단계 + case 생성/갱신

```text
@START_HERE_5.5.md
@NEXT_STEP_5.5.md
@HANDOFF_5.5.md
@rca_kg/runtime_tool_generate/current_run.yaml
@rca_kg/schema/rca_case.schema.yaml
@rca_kg/schema/taxonomy.yaml
@rca_kg/keywords.yaml
@rca_kg/indexes_tool_generate/index.md
@rca_kg/cases/EXAMPLE_v2_rach_failure_001.yaml
@rca_kg/cases/unresolved/EXAMPLE_unresolved.yaml
@prompt/deepdive/RCA_ANALYSIS_METHODOLOGY.md

목표: P3 signal을 기준으로 원인분석 7단계를 수행하고, schema v2 기준 case YAML을 생성 또는 갱신해줘.

입력 자동 선택:
1. current_run.yaml의 p3.signal_file을 우선 사용한다.
2. p3.selected_issue_type을 우선 사용한다.
3. 없으면 rca_kg/signals_tool_generate/*_signal.txt 중 최신 파일을 찾고 번호만 묻는다.

PART A — 원인분석 7단계:
1. 증상 anchor를 잡는다.
2. cptime 시간창을 정한다.
3. 정상경로 대비 최초 이탈 지점을 찾는다.
4. 미지 모듈 가드를 적용한다.
   - 원인 줄이 _l1sw.txt/signal에 없고 주변이 비어 있으면 원인을 단정하지 않는다.
   - 추가 추출이 필요하면 시간창/모듈/명령 후보를 제시하고 멈춘다.
   - 추가 추출 누적은 current_run.yaml의 p4.extraction_attempt_count로 관리한다.
   - 누적 2회 후에도 원인 줄이 없으면 analyzed + confidence: low + 원인 미상으로 정직하게 종료한다.
5. 최소 2개, 최대 4개 가설을 세운다.
6. 가설을 가르는 단서만 추가 확인한다.
7. 단말/환경/계층/API/설정 문제를 분리한다.
8. root_cause.summary는 "A 때문에 B가 발생했고, 그 결과 C가 실패했다" 형태의 인과사슬로 작성한다.
9. confidence는 methodology 기준으로 산정한다. 근거 부족 시 low를 유지한다.

PART B — case YAML 생성/갱신:
1. case_id는 날짜 기반으로 만들지 말고 fingerprint 기반으로 만든다.
   - 형식: <fingerprint-slug>_<issue_type>_<3-digit-seq>
2. fingerprint 블록을 반드시 생성한다.
   - signature_set: 등장한 signature ID 목록
   - sequence: cptime 기준 상대 순서
   - sequence_status: 자동 초안이면 draft
3. line_range/raw_examples/time_range는 사용하지 않는다.
4. 위치 정보는 cptime_range만 사용한다.
5. Jira 참조는 recent_occurrences[].jira에만 기록한다.
6. 신규 case 생성 전 rca_kg/cases/ 아래 기존 case와 fingerprint(signature_set + sequence)를 비교한다.
7. fingerprint가 기존 case와 일치하면 신규 YAML을 만들지 말고 기존 case의 occurrence_count, recent_occurrences, last_seen만 갱신한다.
8. 담당영역 밖 문제로 판단되면 rca_kg/cases/unresolved/<YYYYMMDD>_<issue_type>_<seq>_PENDING.yaml 로 생성하고 root_cause/fix/review는 null로 둔다.
9. crash/dump 분석은 5.5 RCA KG 대상이 아니므로 crash case를 생성하지 않는다.
10. 사람이 이미 원인을 직접 알려준 경우에는 methodology의 [E] 경로를 따른다.
    - 사람 입력 최소: 원인 인과사슬, 근거 로그 유무
    - 자동: confidence 산정, status=reviewed 후보, keywords candidate 추가 후보 기록

완료 후:
1. rca_kg/indexes_tool_generate/index.md를 fingerprint 기준으로 갱신한다.
2. current_run.yaml의 p4 블록을 갱신한다.
   - case_file 또는 unresolved_file
   - root_cause_category
   - confidence
   - candidate_signatures_for_p6
   - extraction_attempt_count
   - unknown_module_guard
3. NEXT_STEP_5.5.md를 P5 안내로 갱신한다.
4. 변경 내용 요약을 답변에 포함한다.
```

`[사람 확인]` 인과사슬 1줄, confidence, case 파일 경로만 확인한다.

---

## P5 — 자가점검 + 승인 정규화

```text
@START_HERE_5.5.md
@NEXT_STEP_5.5.md
@rca_kg/runtime_tool_generate/current_run.yaml
@rca_kg/schema/rca_case.schema.yaml
@rca_kg/schema/taxonomy.yaml
@rca_kg/keywords.yaml

목표: P4가 만든 case YAML을 자가점검하고, 사람이 승인하면 reviewed 상태로 정규화해줘.

입력 자동 선택:
1. current_run.yaml의 p4.case_file을 우선 사용한다.
2. case_file이 없고 p4.unresolved_file만 있으면 unresolved 검토 모드로 진행한다.
3. 둘 다 없으면 cases/와 unresolved/ 최신 파일을 보여주고 번호만 묻는다.

자가점검 항목:
1. issue_type이 taxonomy active issue_type인지 확인한다.
2. root_cause.category가 taxonomy active category이고 applies_to에 해당 issue_type이 포함되는지 확인한다.
3. confidence가 evidence 수준보다 과하지 않은지 확인한다.
4. fingerprint.signature_set이 keywords.yaml의 signature ID인지 확인한다.
5. generic signature가 fingerprint에 들어가지 않았는지 확인한다.
6. sequence가 cptime 기준 상대 순서인지 확인한다.
7. line_range/time_range/raw_examples/related.jira 금지 규칙 위반이 없는지 확인한다.
8. recent_occurrences[].jira 위치가 맞는지 확인한다.
9. 미지 모듈 가드가 필요한데 무시하지 않았는지 확인한다.
10. root_cause.summary가 증상 반복이 아니라 인과사슬인지 확인한다.
11. 담당영역 밖이면 unresolved 형식이 맞는지 확인한다.

출력:
- 점검표를 보여준다.
- 문제가 있으면 자동 수정 가능한 것은 수정하고, 불확실한 것은 사람에게 한 줄로 묻는다.
- 승인 가능하면 사람에게 "승인" 입력만 요청한다.

사람이 "승인"하면:
1. review.status를 reviewed로 갱신한다.
2. fingerprint.sequence_status를 confirmed로 갱신한다.
3. current_run.yaml의 p5.approved=true, approved_at_kst, review_status를 갱신한다.
4. NEXT_STEP_5.5.md를 P6 안내로 갱신한다.

사람이 승인하지 않으면:
1. review.status=draft 또는 rejected를 유지한다.
2. NEXT_STEP_5.5.md에 필요한 수정 항목을 적는다.
```

`[사람 확인]` 승인 가능하면 `승인` 한 단어만 입력한다.

---

## P6 — keywords.yaml candidate → confirmed 승격

```text
@START_HERE_5.5.md
@NEXT_STEP_5.5.md
@rca_kg/runtime_tool_generate/current_run.yaml
@rca_kg/keywords.yaml
@rca_kg/schema/keywords.schema.yaml
@rca_kg/schema/taxonomy.yaml

목표: P5에서 승인된 case의 근거 signature를 keywords.yaml에 반영하고, candidate를 confirmed로 승격해줘.

입력 자동 선택:
1. current_run.yaml의 p5.approved가 true인지 확인한다.
2. current_run.yaml의 p4.case_file과 p4.candidate_signatures_for_p6를 우선 사용한다.
3. 없으면 reviewed case 중 최신 파일을 찾고 번호만 묻는다.

규칙:
1. 사람이 승인하지 않은 case의 signature는 confirmed로 승격하지 않는다.
2. P4/P5에서 근거가 확인된 signature만 승격한다.
3. generic/noise signature는 confirmed 승격 대상에서 제외한다.
4. 새 signature가 필요하면 status=candidate로 추가하고, confirmed는 다음 검증 후로 미룬다.
5. keywords.yaml의 version 또는 changelog가 있으면 갱신한다.
6. 승격 전/후 표를 반드시 보여준다.

출력:
1. keywords.yaml 갱신
2. review_logs/rca_standalone_P6_keywords_promotion_<YYYYMMDD>_<HHMM>_KST.md 생성
3. current_run.yaml의 p6 블록 갱신
4. NEXT_STEP_5.5.md를 "완료 / 다음 로그는 P3부터" 안내로 갱신

검증:
- 가능하면 scripts/validate_package.ps1을 실행하거나, 실행 명령을 안내한다.
```

`[사람 확인]` before/after 표에서 승격 대상이 과하지 않은지만 확인한다.
