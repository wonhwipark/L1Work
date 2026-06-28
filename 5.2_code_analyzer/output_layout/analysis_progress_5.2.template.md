# analysis_progress — <slug> (템플릿)

> 이 파일은 Track A가 자동 갱신한다. 사람은 직접 편집하지 않는다.  
> 실제 사용 시 반드시 아래 canonical 경로에 생성한다.  
> 이 파일은 resume의 주 입력이다. 따라서 무한히 커지는 누적 로그가 아니라 작은 실행 인덱스와 procedure별 포인터 중심으로 유지한다.

```text
output/5.2/<slug>/analysis_progress.md
```

---

## 메타

```text
slug:                    <slug>
block_or_api:            <블록명 또는 API명>
mode:                    A | B
canonical_path:          output/5.2/<slug>/
selected_structure_json: output/5.2/<slug>/structure_<YYYYMMDD_HHMM_KST>_focused.json
structure_selection:     focused_latest | small_structure_latest | explicit_user_path | phase0_generated_focused
created:                 <YYYYMMDD_HHMM_KST>
updated:                 <YYYYMMDD_HHMM_KST>
progress_cursor:         <token cursor>
```

---

## 추출 정보

```text
extraction_mode:    git | bash | powershell | internal_search | mixed
root:               <입력 코드루트>
file_count:         <N>
total_loc:          <N>
structure_size:     <bytes 또는 KB>
structure_scope:    full | focused
runtime_read_policy: progress_index_first; structure_targeted_fallback_only
```

---

## Global CNF Carry Map

```text
status: PENDING | PARTIAL | RESOLVED
handlers:
  - id: <handler_slug>
    function: <함수명>
    file: <경로>
    line: <line>
    scope: NR | LTE | COMMON | UNKNOWN
    confidence: HIGH | MEDIUM | LOW
    status: CANDIDATE | SELECTED | REJECTED
    branches: <domainType/stackId/RAT 분기 요약>
```

---

## procedure 목록 / 진행

| # | procedure | procedure_slug | entry point | stage(s) | 상태 | 산출 섹션 | msc_ref |
|---:|---|---|---|---|---|---|---|
| 1 | <SCell configuration> | <scell_configuration> | <TxCfgScellConfigReq> | S1 | TODO/DOING/DONE | hld_<...>.md#... | msc_<...>.puml |
| 2 | ... | ... | ... | S2 | TODO | ... | ... |

---

## procedure_runtime_index

> Phase 1이 생성한다. Phase 2..N은 이 섹션에서 해당 procedure slice만 읽고 시작한다.  
> structure json 전체 재read는 `index_status: INDEX_INCOMPLETE`일 때만 fallback으로 허용한다.

```text
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

---

## procedure별 결과 요약

> call edge 본문은 전역 누적 블록이 아니라 procedure별 결과 안에만 기록한다.

```text
procedure: <procedure_slug>
status: TODO | DOING | DONE
hld_section: hld_<...>.md#<anchor>
msc_ref: output/5.2/<slug>/msc_<procedure_slug>_<YYYYMMDD_HHMM_KST>.puml
local_call_edges:
  - <from> -> <to> [CALL|IPC_REQ|IPC_CNF] (file:line)
rn:
  - <설명>
```

---

## Global Edge ID Summary (ids only)

> 선택 사항이다. 전역에는 본문을 누적하지 않는다. resume 키가 필요한 경우 id만 남긴다.

```text
EDGE_IDS_DONE: <EDGE001>, <EDGE002>
REQ_IDS_DONE: <REQ001>
CNF_IDS_SELECTED: <CNF001>
```

---

## [RN] 미확인 목록

```text
- <설명> (file:line 또는 사유)
```

---

## 다음

```text
next: <TRACK_A_PHASE0 | PHASE1_PROCEDURE_DISCOVERY | PROC_NEXT:<procedure_slug> | PHASEF_FINALIZE | WAIT_NEW_BLOCK>
```
