# output/5.2/_example_slug

이 폴더는 **canonical output layout의 단일 권위 문서**다. 산출물 폴더 구조는 스킬 `code-analyzer`가 소유하며, 다른 문서는 이 layout을 복제하지 않고 여기를 참조한다. 실제 실행 시 `_example_slug` 대신 확정 slug를 사용한다.

```text
output/5.2/<slug>/
├── analysis_progress.md
├── structure_<YYYYMMDD_HHMM_KST>_focused.json
├── structure_<YYYYMMDD_HHMM_KST>_full.json              # 선택, 300KB 초과 시 자동 read 대상 아님
├── hld_<block_or_proc>_<YYYYMMDD_HHMM_KST>.md
└── msc_<procedure_slug>_<YYYYMMDD_HHMM_KST>.puml
```

실제 산출물은 실행 중 생성되므로 이 패키지에는 예시 README만 포함한다.

핵심 runtime 규칙:

```text
- Phase 1이 analysis_progress.md에 procedure_runtime_index를 생성한다.
- Phase 2..N은 procedure_runtime_index의 해당 procedure slice만 읽는다.
- structure json 전체 반복 read는 금지한다. INDEX_INCOMPLETE일 때만 targeted fallback read한다.
- MSC는 HLD md에 inline하지 않고 별도 .puml 파일로 저장한다.
```
