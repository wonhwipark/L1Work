# Reference — L1a Master v0.40 §5.2 Code Analyzer 요약

이 파일은 원본 L1a Master §5.2에서 Code Analyzer standalone에 필요한 핵심만 보존한 참조 문서다.  
v0.2에서는 standalone 실행 규칙을 아래 기준으로 보정했다.

---

## 1. 목적

L1 C/C++ 코드에서 특정 블록 또는 특정 API를 기준으로 동작 flow를 복원하고, HLD성 markdown 문서를 생성한다.

```text
입력: 코드루트 + 블록명/API명
출력: HLD성 md + procedure별 PlantUML MSC .puml
```

---

## 2. 실행 원칙

```text
1 블록 = HLD성 md 1개
1 procedure = MSC .puml 1개
한 번에 procedure 하나만 분석
미확인은 [RN]
overwrite 금지
KST timestamp 사용
```

---

## 3. v0.2 standalone 보정

```text
canonical path: output/5.2/<slug>/
extraction_mode: git | bash | powershell | internal_search | mixed
progress cursor: [진행: PHASE0_DONE → 다음: PHASE1_PROCEDURE_DISCOVERY]
structure auto-read: focused first; full only if <=300KB or explicitly specified
runtime read: procedure_runtime_index first; structure targeted fallback only
MSC storage: separated .puml, HLD md has msc_ref only
```

---

## 4. Track 구성

```text
Track A: staged 분석 메인 경로
Track B: 선택적 structure.json 정적 추출
```

Track B는 필수가 아니다. 단, 대형 코드에서는 Track B를 먼저 실행하는 것이 토큰 절감에 유리하다.

---

## 5. Phase별 인계 계약

```text
Track B / Phase 0
  → selected_structure_json 확보

Phase 1
  → structure json을 한 번 읽어 procedure_runtime_index 생성

Phase 2..N
  → procedure_runtime_index의 해당 procedure slice만 읽고 진행
  → structure json은 INDEX_INCOMPLETE일 때만 targeted fallback read

Phase F
  → HLD md에 msc_ref 링크와 산문 설명만 유지
  → MSC 본문은 .puml 파일에 유지
```

---

## 6. RCA 연계 후보

향후 RCA 5.5와 연결할 때는 아래 정보를 `root_cause.code_ref` 후보로 사용할 수 있다.

```text
hld_ref: output/5.2/<slug>/hld_<block>_<ts>.md#procedure-<procedure_slug>
msc_ref: output/5.2/<slug>/msc_<procedure_slug>_<ts>.puml
structure_ref: output/5.2/<slug>/structure_<ts>_focused.json
file_line_ref: <file>:<line>
confidence: HIGH | MEDIUM | LOW
```

이 연결 계약은 아직 확정 전이다.
