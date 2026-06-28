# P5 — 자가점검 + 승인 정규화

목표: P4 case YAML 자가점검 후, 사람 승인 시 reviewed로 정규화.

입력: `p4.case_file` 우선. 없고 `p4.unresolved_file`만 있으면 unresolved 검토 모드. 둘 다 없으면 `{kg_root}/cases/`·`{kg_root}/cases/unresolved/` 최신 보여주고 번호만.

자가점검:
1. issue_type이 taxonomy active인지. 2. root_cause.category가 active이고 applies_to에 issue_type 포함인지. 3. confidence가 evidence 수준 대비 과하지 않은지. 4. fingerprint.signature_set이 keywords.yaml signature ID인지. 5. generic signature가 fingerprint에 안 들어갔는지. 6. sequence가 cptime 상대 순서인지. 7. line_range/time_range/raw_examples/related.jira 금지 위반 없는지. 8. recent_occurrences[].jira 위치 맞는지. 9. 미지 모듈 가드 필요한데 무시 안 했는지. 10. root_cause.summary가 증상 반복이 아니라 인과사슬인지. 11. 담당영역 밖이면 unresolved 형식 맞는지.

출력: 점검표. 자동 수정 가능한 건 수정, 불확실하면 한 줄로 질문. 승인 가능하면 "승인" 입력만 요청.

승인 시: review.status=reviewed, fingerprint.sequence_status=confirmed, `p5.approved=true`/approved_at_kst/review_status 갱신, NEXT_STEP을 P6로.
미승인 시: status=draft/rejected 유지, NEXT_STEP에 수정 항목.
[사람 확인] 승인 가능하면 "승인" 한 단어만.
