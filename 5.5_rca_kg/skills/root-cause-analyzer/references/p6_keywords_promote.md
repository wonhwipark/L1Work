# P6 — keywords.yaml candidate → confirmed 승격

목표: P5 승인 case의 근거 signature를 keywords.yaml에 반영, candidate→confirmed 승격.

입력: `p5.approved`가 true인지 확인. `p4.case_file`과 `p4.candidate_signatures_for_p6` 우선. 없으면 reviewed case 최신(번호만).

규칙:
1. 사람이 승인 안 한 case signature는 승격 금지.
2. P4/P5에서 근거 확인된 signature만 승격.
3. generic/noise signature는 제외.
4. 새 signature는 status=candidate로 추가, confirmed는 다음 검증 후로.
5. keywords.yaml version/changelog 있으면 갱신.
6. 승격 전/후 표를 반드시 표시.

출력: `{kg_root}/keywords.yaml` 갱신, `{workspace_root}/review_logs/rca_standalone_P6_keywords_promotion_<YYYYMMDD>_<HHMM>_KST.md` 생성, `p6` 블록 갱신, NEXT_STEP을 "완료 / 다음 로그는 P3부터"로.
검증: 가능하면 `scripts/validate_package.ps1` 실행 또는 명령 안내.
[사람 확인] before/after 표에서 승격 대상이 과하지 않은지만.
