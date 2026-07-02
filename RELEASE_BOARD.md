# 5.2 CodeAnalyzer ↔ l1sw-log-analyzer manifest 연결 가능성 진단
# (판정 전용 · 파일 수정 금지)

## 역할
너는 두 스킬의 산출물 구조를 대조하는 진단자다.
- 5.2 CodeAnalyzer: 정적 코드 분석 → structure.json (ipc_req_sites / ipc_cnf_handlers / call_edges / modules / domain_branches, 각각 file:line 앵커)
- l1sw-log-analyzer: 사내 스킬. **Manifest 디렉터리의 fragment JSON(모듈명 → regex 매핑)** 을 SSOT로 .sdm parser에 넘겨 prefix/키워드 필터링 수행.
목적: **5.2 structure.json이 l1sw manifest fragment(모듈명→regex)를 코드 근거로 확장/보강할 수 있는지** 판정하고,
그 결과로 **5.5 RCA의 존재 이유(vision)를 재정의**한다.

## 절대 규칙
1. 어떤 파일도 수정/생성/삭제하지 않는다. 읽기·대조·판정만.
2. manifest fragment의 JSON 구조를 추측하지 않는다. **실제 파일을 열어 확인한 키만** 근거로 쓴다. 못 연 항목은 "미확인"으로 남기고 추측 매핑 금지.
3. 모든 결론은 객관식(번호). 사람은 번호만 고른다.
4. 매핑 후보는 반드시 3열로: (manifest 실제 키/값 ↔ 5.2 실제 필드/값 ↔ 코드상 근거 file:line).

## STEP 0 — 대상 확보
아래 경로를 스스로 확정. 못 찾으면 "미확인".
- l1sw-log-analyzer 스킬 위치 (SKILL.md + Manifest 디렉터리).
- **manifest fragment JSON 5개** 실제 경로 (모듈명→regex 매핑이 든 파일).
- 5.2 structure.json 샘플 1개 (`output/5.2/<slug>/structure_*.json`). 없으면 5.2 schema 문서로 대체하되 "샘플 미확보" 명시.
출력: `| 대상 | 경로 | 확인여부 |`

## STEP 1 — manifest fragment 실구조 해부 (최우선, 관찰 전용)
fragment JSON 1~2개를 실제로 열어 있는 그대로 기록. 해석 금지.
- 최상위 스키마: 모듈명이 키인가? regex는 값 배열인가 객체인가?
- **regex/키워드 실제 예시 5개** 그대로 인용 (예: prefix `[DSSM]`, 특정 메시지명 등).
- regex가 매칭하려는 대상이 무엇인지 추정 근거: 메시지명 / IPC명 / 함수명 / 로그 태그 중 어디에 가까운가.
- 모듈 식별자 표기법 (`Allocator`, `DSSM` 등)과 5.2 modules[].file / domain_branches 표기법의 형태 차이.
- issue_type 축이 manifest에 있는가, 아니면 순수 모듈 축인가. (문서상 "모듈 분기"로 추정됨 — 실제 확인)
출력: `| fragment 파일 | 모듈키 | regex 예시 | 매칭대상 성격 | 비고 |`

## STEP 2 — 5.2 → manifest regex 도출 가능성 대조
STEP 1의 각 모듈/regex에 대해, 5.2 structure.json이 그 regex를 **코드 근거로 재현/보강**할 수 있는지 확인.
검증 관점:
- manifest regex가 노리는 메시지/IPC명이 5.2 `ipc_req_sites[].ipc_call` / `ipc_cnf_handlers[].function` / `call_edges[](type=IPC_*)` 에 실제로 등장하는가.
- manifest 모듈키가 5.2 `modules[].file` 또는 `domain_branches[].condition`(NR/LTE 등)으로 매핑되는가.
- 5.2가 manifest에 **없던** 메시지/핸들러를 추가로 잡아내는가 (= recall 향상 여지).
출력: `| manifest 모듈/regex | 5.2 대응 필드·값 | 코드근거 file:line | 관계(재현/보강/신규/무관) |`

## STEP 3 — 연결 가능성 판정 (객관식, STEP1~2 관찰값으로만 근거)
  [1] 직접 연결: manifest regex 대상이 5.2 IPC/메시지/함수 필드와 동일 축. 5.2 → regex 자동 도출 파이프라인 구성 가능.
  [2] 부분 연결: 모듈 축은 매핑되나 regex↔5.2필드 형식이 달라 변환 어댑터 1개 필요.
  [3] 간접 연결: manifest가 로그 문자열 태그 수준이라 코드앵커와 직접 대응 안 됨. 5.2는 "regex 후보 근거"로만 기여(값은 사람 확정).
  [4] 판정 불가: fragment 실구조 미확보. 무엇을 더 열어야 하는지 명시.

## STEP 4 — 5.5 vision 재정의 (객관식, 복수 가능)
STEP 3 결과에 따라 5.5 RCA 역할을 택하고, 각 선택에 "그렇다면 5.5 존재 이유 1줄"을 붙임.
  [A] 생성기: 5.2가 manifest fragment(regex)를 코드에서 생성. 5.5 축소/불필요.
  [B] 검증기: 5.2 생성 regex를 5.5가 실로그로 검증→confirmed 승격하는 피드백 루프. (기존 keywords.yaml 승격 메커니즘 재활용)
  [C] 지식화기: 필터·원인탐색은 l1sw+5.2, 5.5는 case/signal 축적·재사용만. (현 강점 유지)
  [D] 흡수: 5.5 고유가치 없음. keywords.yaml을 5.2→manifest 파이프라인으로 이관 후 5.5 폐지.

## STEP 5 — 남은 미확인 항목 정리
문서(L1SW_LOG_ANALYZER_COMPARISON.md)의 미확인 5개 중 이번에 확인된 것/여전히 미확인인 것 구분:
  1) _l1sw.txt 축소율  2) 필터 후 context 초과 리스크  3) 과거 결과 재사용 메커니즘
  4) issue_type 분류 유무  5) 구조화 데이터(YAML/JSON) 병행 저장 유무

## 최종 출력
1. 경로표(S0) 2. fragment 해부표(S1) 3. 대조표(S2)
4. 연결판정: [번호]+3줄 근거  5. 5.5 vision: [문자]+1줄  6. 미확인 항목 상태(S5)
파일은 절대 수정하지 마라. 판정만 보고하라.
