# Review Log — CodeAnalyzer Standalone v0.2 런타임 토큰 누수 수정

생성: 2026-06-26 01:16 KST

---

## 1. 반영 배경

v0.2에서 copy prompt 분리로 reference prompt 반복 입력 비용은 줄었다. 그러나 procedure가 늘어날수록 아래 런타임 반복 read 누수가 남아 있었다.

```text
1. analysis_progress.md의 confirmed call edges 누적 블록이 procedure 수에 비례해 계속 커짐
2. copy_next_procedure / copy_resume가 progress 전체를 매번 읽으면서 이전 edge를 반복 처리함
3. structure_focused.json을 Phase 2..N마다 반복 read할 가능성이 있음
4. Track A reference는 MSC inline, copy prompt는 별도 .puml로 서로 모순됨
5. structure 자동 탐색이 1MB full structure를 우발적으로 집을 수 있음
6. reference prompt가 런타임에 다시 read될 여지가 있음
```

---

## 2. 핵심 수정

### 2.1 전역 call edge 누적 본문 제거

제거 대상:

```text
## confirmed call edges (누적)
- <from> -> <to> ...
```

대체 방식:

```text
procedure별 결과 요약.local_call_edges
Global Edge ID Summary (ids only)
```

효과:

```text
8개 procedure 중 8번째 procedure를 분석할 때 1~7번 procedure의 edge 본문을 전부 다시 읽는 문제를 차단한다.
```

---

### 2.2 procedure_runtime_index 도입

Phase 1이 아래 작은 인덱스를 만든다.

```text
procedure_runtime_index:
  - procedure_slug
  - entry_point
  - related_files
  - req_site_ids
  - cnf_handler_candidate_ids
  - call_edge_ids
  - msc_file
  - index_status
```

Phase 2..N은 이 인덱스의 해당 procedure slice만 읽는다.

---

### 2.3 structure json 반복 read 차단

수정 후 정책:

```text
index_status: READY              → structure json 재read 금지
index_status: INDEX_INCOMPLETE   → 필요한 범위만 targeted fallback read
```

`structure_focused.json`은 Phase 1 인덱스 생성 source이고, Phase 2..N의 반복 입력이 아니다.

---

### 2.4 MSC 분리 .puml 통일

수정 전 모순:

```text
Track A reference: HLD md 안에 PlantUML inline 가능
copy prompt: 별도 msc_*.puml 생성
```

수정 후:

```text
MSC는 artifacts/5.2/<slug>/msc_<procedure_slug>_<YYYYMMDD_HHMM_KST>.puml 로 저장
HLD md에는 msc_ref 링크와 산문 설명만 기록
```

효과:

```text
HLD md 비대화 방지
Phase F / resume에서 큰 inline MSC 반복 처리 방지
산출물 정합성 확보
```

---

### 2.5 structure 자동 탐색 우선순위 고정

수정 후 우선순위:

```text
1. structure_*_focused.json 최신 파일
2. structure_*.json 중 300KB 이하인 최신 파일
3. 300KB 초과 full structure는 명시 지정 시에만 사용
```

효과:

```text
1MB full structure를 자동으로 열어 토큰을 소모하는 우발 read를 차단한다.
```

---

### 2.6 reference prompt 런타임 차단 표식 추가

아래 두 파일 상단에 런타임 read 불필요 문구를 추가했다.

```text
prompt/5.2_track_a_prompt.md
prompt/5.2_track_b_prompt.md
```

실행은 copy prompt만 사용한다.

---

## 3. 수정 파일

```text
VERSION_5.2.md
START_HERE_5.2.md
NEXT_STEP_5.2.md
HANDOFF_5.2.md
RUNBOOK_BLOCK_TO_HLD_5.2.md
reference/master_v0.40_section_5_2.md
prompt/5.2_track_a_prompt.md
prompt/5.2_track_b_prompt.md
prompt/copy_track_b.md
prompt/copy_phase0.md
prompt/copy_phase1.md
prompt/copy_next_procedure.md
prompt/copy_resume.md
prompt/copy_phase_f.md
artifacts_layout/analysis_progress_5.2.template.md
schema/analysis_progress.schema.md
schema/structure.schema.md
```

---

## 4. 완료 기준

```text
- confirmed call edges (누적) 블록이 템플릿/schema/prompt에서 제거됨
- procedure_runtime_index가 Phase 1 필수 산출물로 정의됨
- copy_next_procedure가 structure json 전체를 반복 read하지 않도록 수정됨
- copy_resume도 procedure_runtime_index 우선으로 수정됨
- MSC가 별도 .puml 파일로 통일됨
- HLD md inline PlantUML MSC 정책이 제거됨
- structure 자동 탐색이 focused 우선 / full 300KB 이하로 제한됨
- reference prompt 상단에 runtime read 차단 문구가 있음
```
