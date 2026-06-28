# schema — analysis_progress.md v0.2

저장 위치는 반드시 아래 canonical 경로다.

```text
output/5.2/<slug>/analysis_progress.md
```

이 파일은 resume의 주 입력이다. 따라서 누적 로그처럼 계속 커지면 안 된다. Phase 2..N이 매번 큰 structure json을 다시 읽지 않도록 Phase 1에서 만든 `procedure_runtime_index`를 중심으로 유지한다.

---

## 1. 필수 필드

```text
slug
block_or_api
mode
canonical_path
selected_structure_json
structure_selection
created
updated
progress_cursor
extraction_mode
root
file_count
total_loc
structure_size
structure_scope
runtime_read_policy
Global CNF Carry Map
procedure 목록 / 진행
procedure_runtime_index
procedure별 결과 요약
Global Edge ID Summary (ids only, optional)
[RN] 미확인 목록
next
```

폐기 필드:

```text
전역 call edge 누적 본문 블록   # procedure별 local_call_edges로 대체
```

---

## 2. mode

```text
A = 블록 기준
B = API 기준
```

---

## 3. extraction_mode

반드시 아래 enum 중 하나만 사용한다.

```text
git | bash | powershell | internal_search | mixed
```

폐기 표현:

```text
shell_mode
git_bash
unknown
fallback_mode
```

---

## 4. progress_cursor

진행줄과 동일한 token cursor를 저장한다.

```text
[진행: PHASE0_DONE → 다음: PHASE1_PROCEDURE_DISCOVERY]
```

사용 가능한 대표 상태:

```text
INIT
TRACKB_DONE
PHASE0_DONE
PHASE1_WAIT_SCOPE_SELECTION
PHASE1_DONE
PROC_DONE:<procedure_slug>
BLOCK_HLD_DONE:<slug>
```

사용 가능한 대표 next:

```text
TRACK_A_PHASE0
PHASE1_PROCEDURE_DISCOVERY
USER_SELECT_PROCEDURES
PROC_NEXT:<procedure_slug>
PHASEF_FINALIZE
WAIT_NEW_BLOCK
```

---

## 5. selected_structure_json / structure_selection

`selected_structure_json`은 Phase 0에서 확정한 구조 파일이다.

```text
selected_structure_json: output/5.2/<slug>/structure_<YYYYMMDD_HHMM_KST>_focused.json
structure_selection: focused_latest | small_structure_latest | explicit_user_path | phase0_generated_focused
```

자동 탐색 우선순위:

```text
1. structure_*_focused.json 최신 파일
2. structure_*.json 중 300KB 이하인 최신 파일
3. 300KB 초과 full structure는 명시 지정 시에만 사용
```

---

## 6. runtime_read_policy

```text
runtime_read_policy: progress_index_first; structure_targeted_fallback_only
```

규칙:

```text
1. Phase 2..N은 structure json 전체를 반복 read하지 않는다.
2. Phase 2..N은 procedure_runtime_index에서 해당 procedure slice만 읽는다.
3. index_status가 READY이면 structure read 금지.
4. index_status가 INDEX_INCOMPLETE이면 필요한 파일/id 범위만 targeted fallback read.
5. resume도 동일 규칙을 따른다.
```

---

## 7. Global CNF Carry Map

단일 CNF handler를 가정하지 않는다.

```text
status: PENDING | PARTIAL | RESOLVED
handlers[]:
  id
  function
  file
  line
  scope
  confidence
  status
  branches
```

SELECTED handler는 이후 procedure에서 재read하지 않는다.

---

## 8. procedure_runtime_index

Phase 1이 반드시 생성한다.

```text
procedure_runtime_index:
  - procedure_slug: <procedure_slug>
    entry_point: <function/message/api>
    entry_file: <relative path>
    entry_line: <line 또는 UNKNOWN>
    related_files:
      - <relative path>
    req_site_ids:
      - <REQ001 또는 UNKNOWN>
    cnf_handler_candidate_ids:
      - <CNF001 또는 UNKNOWN>
    call_edge_ids:
      - <EDGE001 또는 UNKNOWN>
    hld_section_anchor: <anchor>
    msc_file: output/5.2/<slug>/msc_<procedure_slug>_<YYYYMMDD_HHMM_KST>.puml
    index_status: READY | INDEX_INCOMPLETE
    rn:
      - <필요 시>
```

`index_status` 기준:

```text
READY: Phase 2가 structure json 없이 시작 가능
INDEX_INCOMPLETE: Phase 2에서 필요한 범위만 structure targeted fallback read 필요
```

---

## 9. procedure별 결과 요약

procedure 결과는 각 procedure 섹션에만 누적한다.

```text
procedure: <procedure_slug>
status: DONE
hld_section: hld_<...>.md#<anchor>
msc_ref: output/5.2/<slug>/msc_<procedure_slug>_<YYYYMMDD_HHMM_KST>.puml
local_call_edges:
  - <from> -> <to> [CALL|IPC_REQ|IPC_CNF] (file:line)
rn:
  - <설명>
```

전역 누적 call edge 본문 블록은 금지한다. 필요 시 아래처럼 id만 남긴다.

```text
EDGE_IDS_DONE: EDGE001, EDGE002
REQ_IDS_DONE: REQ001
CNF_IDS_SELECTED: CNF001
```

---

## 10. MSC 저장 규칙

MSC는 HLD md 안에 inline PlantUML 코드블록으로 넣지 않는다.

```text
msc_ref: output/5.2/<slug>/msc_<procedure_slug>_<YYYYMMDD_HHMM_KST>.puml
```

HLD .md에는 `msc_ref` 링크와 산문 설명만 기록한다.

---

## 11. resume 규칙

1. `progress_cursor`를 먼저 읽는다.
2. `canonical_path`가 `output/5.2/<slug>/`인지 확인한다.
3. `selected_structure_json`은 확인만 한다.
4. DONE procedure는 재분석하지 않는다.
5. `Global CNF Carry Map`의 SELECTED handler는 재read하지 않는다.
6. `next`가 `PROC_NEXT:<procedure_slug>`이면 `procedure_runtime_index`의 해당 slice만 읽는다.
7. `index_status: READY`이면 structure json을 읽지 않는다.
8. `index_status: INDEX_INCOMPLETE`이면 필요한 범위만 targeted fallback read한다.
9. 다음 작업은 `next` 필드 기준으로 하나만 수행한다.
