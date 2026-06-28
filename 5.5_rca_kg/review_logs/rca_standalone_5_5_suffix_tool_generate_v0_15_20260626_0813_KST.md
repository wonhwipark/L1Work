# Review Log — RCA Standalone v0.15 (_5.5 접미사 + tool_generate 리네이밍 + 편의 점검)

생성: 2026-06-26 08:13 KST  
기준 패키지: RCA_standalone convenience_v0.14 (stateful)

---

## 1. 반영 배경

5.2 CodeAnalyzer 패키지를 v0.4까지 편의 개선한 것과 동일 컨셉으로 5.5 RCA 패키지를 점검했다. 추가로 두 가지 요청을 반영했다.

```text
1. 5.2 패키지와 충돌하지 않도록 최상위 문서에 _5.5 접미사를 붙인다.
2. no_human 표기를 tool_generate로 바꾼다.
```

점검 중 5.2와 동일 계열의 제어문자 깨짐 버그도 1건 발견해 고쳤다.

---

## 2. _5.5 접미사 (충돌 방지)

5.2 패키지는 이미 `START_HERE_5.2.md` 식으로 최상위 문서에 `_5.2`를 쓴다. RCA는 bare 이름(`START_HERE.md`)이라, 두 폴더를 같이 열거나 "START_HERE"로 지칭할 때 모호했다. 동일 규칙으로 맞췄다.

```text
START_HERE.md          → START_HERE_5.5.md
NEXT_STEP.md           → NEXT_STEP_5.5.md
HANDOFF.md             → HANDOFF_5.5.md
VERSION.md             → VERSION_5.5.md
USAGE_SCENARIO.md      → USAGE_SCENARIO_5.5.md
RUNBOOK_L1SW_TO_P6.md  → RUNBOOK_L1SW_TO_P6_5.5.md
```

범위 결정:

```text
- 최상위 네비게이션 문서만 접미사를 붙인다 (5.2와 동일 범위).
- rca_kg/ · prompt/ · scripts/ 내부 파일은 폴더로 네임스페이스가 분리되어 그대로 둔다.
- 모든 md/ps1/yaml의 상호 참조 경로를 일괄 갱신.
- 이중 접미사(_5.5_5.5) 없음 확인.
- scripts/validate_package.ps1의 required 목록도 _5.5로 갱신, 실재 파일과 일치 확인.
```

---

## 3. no_human → tool_generate

의미상 "사람이 안 한다(no_human)"보다 "도구가 생성한다(tool_generate)"가 정확하다. 폴더 3개 + 인라인 표기를 모두 바꿨다.

```text
rca_kg/runtime_no_human/  → rca_kg/runtime_tool_generate/
rca_kg/signals_no_human/  → rca_kg/signals_tool_generate/
rca_kg/indexes_no_human/  → rca_kg/indexes_tool_generate/
인라인 _no_human          → _tool_generate
```

설명 문구도 손봤다.

```text
변경 전: "_no_human = 사람이 직접 편집하지 않는 자동 산출물 영역. 사람의 승인/판단이 없다는 뜻이 아니다."
변경 후: "_tool_generate = 도구(Claude Code/스크립트)가 생성·갱신하는 산출물 영역. 도구가 쓰고, 사람이 판단한다."
```

전 파일(md/ps1/yaml)에서 `no_human` 문자열 잔존 0개 확인. case YAML의 signal_file 경로, 스크립트의 OutputTxt 경로 포함 모두 갱신.

---

## 4. 편의 점검 (5.2 v0.4와 동일 컨셉)

RCA는 이미 `current_run.yaml` 기반 stateful 구조라 5.2의 slug 자동승계에 해당하는 마찰은 없다. 적용 가능한 2가지만 반영했다.

### 4.1 다음 붙여넣을 블록 안내

공통 운영 규칙 7번을 보강해, 진행 줄 다음에 한 줄을 추가하게 했다.

```text
[진행: P0 완료 → 다음: C0 또는 P1. ...]
▶ 다음 붙여넣기: prompt/CLAUDE_CODE_PROMPTS_e2e_v1.md 의 C0 블록 (또는 _l1sw.txt가 있으면 P1 블록)
```

사용자가 "지금 어느 P블록을 붙여넣지"를 스스로 판단하지 않게 한다.

### 4.2 타임스탬프 자동 채움 명문화

공통 운영 규칙 6번에 명시를 추가했다.

```text
review_logs/*_<YYYYMMDD>_<HHMM>_KST.md 등 파일명의 타임스탬프 placeholder는
사람이 적지 않는다. 도구가 현재 KST 시각으로 채운다.
```

### 4.3 문서 지도 3줄

START_HERE 상단에 "평소엔 이 파일 하나면 된다" 지도를 추가했다(5.2와 동일).

---

## 5. 깨진 제어문자 수정 (동작 버그)

START_HERE 자체 검증 명령에 VT(0x0B) 제어문자가 섞여 있었다.

```text
변경 전(깨짐): .\scripts<VT>alidate_package.ps1   → v 누락
변경 후:       .\scripts\validate_package.ps1
```

패키지 전체 md/ps1에서 제어문자(0x00-0x08,0x0B,0x0C,0x0E-0x1F) 0개 확인.

---

## 6. 미변경 (동작/계약/이력 보존)

```text
- P0~P6 단계 로직, current_run.yaml 스키마, taxonomy, keywords SSOT 등 동작 계약은 유지.
- rca_kg/schema/*, manifest_fragments/, skills_seed/ 내용 유지.
- delta/, 기존 review_logs/ history 보존.
- L1SW-first 원칙, 미지 모듈 가드, [RN]/cause unknown 정직성 규칙 유지.
```

---

## 7. 완료 기준

```text
- 최상위 6개 문서가 _5.5 접미사를 가짐. 상호 참조 전부 갱신. 이중 접미사 없음.
- no_human 문자열이 패키지 어디에도 없음. 폴더 3개가 *_tool_generate로 존재.
- validate_package.ps1 required 목록이 실재 파일과 일치.
- 진행 줄에 다음 붙여넣기 블록 안내가 추가됨.
- 타임스탬프 자동 채움이 명문화됨.
- START_HERE에 문서 지도가 있음.
- 제어문자 0개.
```

---

## 8. 남은 미결 (계승)

```text
1. 실제 _l1sw.txt 1건 대상 P0~P6 E2E 검증 (pre-E2E 상태 유지).
2. root_cause.code_ref / links 필드는 5.2 산출물 구조 확정 후 채움.
3. keywords.yaml 작성과 L1SW manifest fragment는 사내 환경에서 수행.
```
