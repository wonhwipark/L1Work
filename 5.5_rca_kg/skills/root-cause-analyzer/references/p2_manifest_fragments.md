# P2 — L1SW manifest fragment 후보 자동 생성

목표: keywords.yaml 기반으로 issue_type별 manifest fragment 후보 JSON 자동 생성.

입력: `p1.output_format_doc` 우선. 비면 `{kg_root}/runtime_tool_generate/format_profiles/L1SW_OUTPUT_FORMAT_PROBED_*_KST.md` 최신. 애매하면 번호만.

규칙:
1. `{kg_root}/keywords.yaml`을 단일 출처로. 키워드를 지어내지 않는다.
2. 각 issue_type에서 `use_for.l1sw_manifest_fragment == true` signature만 포함.
3. `use_for.fingerprint == false` generic context signature는 제외.
4. P0가 찾은 기존 L1SW fragment JSON 1개를 열어 키 구조 확인, 같은 구조로 작성. 못 찾으면 잠정 구조 + status `structure_unverified`.
5. signature status(confirmed/candidate)를 fragment에 보존.

출력: `{kg_root}/manifest_fragments/rca_{rach,scg,tx,l2}.json`.
리뷰 로그: `{workspace_root}/review_logs/rca_standalone_R4_manifest_fragments_<YYYYMMDD>_<HHMM>_KST.md`, 표 `| issue_type | signature_id | 포함/제외 | status | 사유 |`.

완료: `p2.generated_fragments`, `p2.review_log`, `p2.manifest_fragment_dir_resolved` 갱신. NEXT_STEP을 "실로그마다 L1SW 실행 후 P3"로. keywords.yaml 자체는 수정 안 함.
[사람 확인] review_log의 "기존 구조 일치 여부"만.
