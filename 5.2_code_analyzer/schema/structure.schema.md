# schema — structure.json v0.2

이 문서는 Track B 또는 Track A Phase 0이 생성하는 `structure_<YYYYMMDD_HHMM_KST>_focused.json` 또는 `structure_<YYYYMMDD_HHMM_KST>_full.json`의 최소 계약이다.

저장 위치는 반드시 아래 canonical 경로다.

```text
output/5.2/<slug>/
```

권장 파일명:

```text
focused structure: structure_<YYYYMMDD_HHMM_KST>_focused.json
full structure:    structure_<YYYYMMDD_HHMM_KST>_full.json
```

---

## 1. Top-level schema

```json
{
  "meta": {},
  "modules": [],
  "call_edges": [],
  "ipc_req_sites": [],
  "ipc_cnf_handlers": [],
  "domain_branches": [],
  "limits": {},
  "rn": []
}
```

---

## 2. meta

```json
{
  "root": "<input code root>",
  "slug": "<slug>",
  "canonical_path": "output/5.2/<slug>/",
  "extracted_at": "YYYYMMDD_HHMM_KST",
  "extraction_mode": "git | bash | powershell | internal_search | mixed",
  "file_count": 0,
  "total_loc": 0,
  "structure_scope": "full | focused",
  "target": "<block_or_api>",
  "target_type": "block | api | mixed",
  "auto_read_policy": "focused_first; full_auto_only_if_<=300KB"
}
```

`extraction_mode`은 반드시 아래 중 하나다.

```text
git | bash | powershell | internal_search | mixed
```

---

## 3. modules[]

```json
{
  "file": "<relative path>",
  "loc": 0,
  "functions": [
    {
      "id": "FUNC001",
      "name": "<function>",
      "line": 0,
      "signature": "<short signature>",
      "confidence": "HIGH | MEDIUM | LOW"
    }
  ]
}
```

---

## 4. call_edges[]

`call_edges[]`는 Phase 1이 procedure_runtime_index로 가져갈 수 있도록 안정적인 `id`를 가져야 한다.

```json
{
  "id": "EDGE001",
  "from": "<caller>",
  "to": "<callee>",
  "file": "<relative path>",
  "line": 0,
  "type": "CALL | IPC_REQ | IPC_CNF | DISPATCH | UNKNOWN",
  "confidence": "HIGH | MEDIUM | LOW",
  "note": "<optional, [RN] allowed>"
}
```

---

## 5. ipc_req_sites[]

```json
{
  "id": "REQ001",
  "caller": "<caller function>",
  "ipc_call": "<send/post/request call>",
  "file": "<relative path>",
  "line": 0,
  "pattern": "<matched pattern>",
  "confidence": "HIGH | MEDIUM | LOW"
}
```

---

## 6. ipc_cnf_handlers[]

v0.2부터 CNF handler는 단일 객체가 아니라 후보 배열이다.

```json
{
  "id": "CNF001",
  "function": "<handler function>",
  "file": "<relative path>",
  "line": 0,
  "scope": "NR | LTE | COMMON | UNKNOWN",
  "confidence": "HIGH | MEDIUM | LOW",
  "branches": [
    {
      "condition": "<domainType/stackId/RAT branch>",
      "calls": ["<callee>"]
    }
  ],
  "status": "CANDIDATE | SELECTED | REJECTED"
}
```

검증 기준:

```text
1개 후보: Phase 1/2에서 확인 후 SELECTED 가능
2개 이상 후보: candidates 유지, procedure별 Phase에서 확정
확정 불가: [RN] CNF handler ambiguous
```

---

## 7. limits

```json
{
  "grep_result_limit_per_pattern": 200,
  "structure_soft_limit_kb": 300,
  "structure_hard_limit_kb": 1024,
  "raw_ast_allowed": false,
  "runtime_repeated_full_read_allowed": false
}
```

---

## 8. 크기 정책과 자동 탐색 정책

```text
300KB 이하: 자동 탐색 대상 가능
300KB~1MB: modules 요약, target 관련 call_edges 유지. focused 저장 권장
1MB 초과: focused structure 생성. block/API 관련 subgraph만 유지
```

Track A Phase 0 자동 탐색 우선순위:

```text
1. structure_*_focused.json 최신 파일
2. structure_*.json 중 300KB 이하인 최신 파일
3. 300KB 초과 full structure는 사용자가 명시한 경우에만 사용
```

raw AST와 전체 symbol table 덤프는 금지한다.

---

## 9. Phase 1 인계 계약

Phase 1은 structure json을 읽은 뒤 `analysis_progress.md`에 `procedure_runtime_index`를 생성해야 한다. Phase 2..N은 이 index slice만 읽고 진행한다.

```text
structure json → Phase 1 → procedure_runtime_index → Phase 2..N
```

따라서 structure json은 반복 read 대상이 아니라 Phase 1의 인덱스 생성 source다.
