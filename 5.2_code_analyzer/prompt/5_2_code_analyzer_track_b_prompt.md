# 5.2 Code Analyzer — Track B: 정적 구조 추출 프롬프트 v1.1

- **Version:** v1.1 (§0 3-file 관계 및 명칭 정리)
- **Updated:** 2026-06-18 (KST)
- **Track:** B — bash 기반 정적 추출 (Track A의 선택적 선행 단계)
- **방식:** Python 패키지 없음. Claude Code가 find/wc/ctags/grep으로 추출 → structure.json
- **Related Skill:** `staged-code-analyzer`

---

## 0. 이 문서의 역할 — prompt/ 폴더 내 5.2 관련 3개 파일

`L1a/prompt/`에는 5.2 Code Analyzer 관련 파일이 3개 있다. **2개(신규) + 1개(구세대, 별도 계열)** 구조이며, "Track A/B" 명칭은 신규 2개 페어에만 쓴다.

| 파일 | 계열 | 방식 | 상태 |
|---|---|---|---|
| `5_2_code_analyzer_py_package_prompt.md` | **별도 계열** (Track 아님) | Python 패키지(`code_analyzer/`)를 빌드하라는 지시 — 파싱+HLD생성을 코드로 구현 | 기존, historical record로 보존 |
| `5_2_code_analyzer_track_b_prompt.md` (본 문서) | Track 페어 | bash(find/wc/ctags/grep) 정적 추출 → `structure.json` | 신규, Track A의 선택적 선행 단계 |
| `5_2_code_analyzer_track_a_prompt.md` | Track 페어 | staged-code-analyzer 스킬로 Claude가 직접 단계별 MSC 생성 | 신규, 메인 실행 경로 |

py_package 파일은 본 문서(Track B)와 무관하다. py_package는 **분석 로직 자체를 Python 코드로 구현**하는 접근이고, Track B는 **분석 로직 없이 bash로 구조만 추출**해 Track A(Claude)에 넘기는 가속기다. "Track" 번호는 신규 페어 전용 명칭으로, py_package 파일을 가리킬 때는 쓰지 않는다.

Track B는 Track A(staged-code-analyzer) 실행 **전에** 한 번 돌리는 정적 구조 추출 단계다. 필수가 아니라 **선택적 가속기**다.

```
Track B (본 문서)         Track A (5_2_code_analyzer_track_a_prompt.md)
bash 추출 → structure.json → Phase 0 인풋으로 제공 → 모듈별 MSC 생성
```

**Track B가 주는 것**
- 파일/함수 목록을 Claude가 소스를 직접 읽지 않아도 파악 → Phase 0 토큰↓
- IPC REQ 지점 위치를 grep으로 정확히 → Claude의 탐색 오버헤드↓
- CNF 핸들러(파일 하나)를 미리 식별 → stage에서 targeted 1회 read로 족함
- domainType 분기 위치를 사전 파악 → MSC 분기 구성에 직접 활용

**Track B가 주지 않는 것** (Track A Claude가 담당)
- IPC REQ↔CNF 의미적 매칭 (grep은 위치만 찾고 연결은 Claude가 함)
- 호출 순서 / timing (정적 추출 불가, Claude body read로 확정)
- 매크로 안에 숨은 IPC 호출 → `[RN]`으로 남기고 Track A가 해소

---

## 1. 선행 조건

```text
- Claude Code 사용 가능
- 분석 대상 코드가 로컬 경로에 접근 가능
- staged-code-analyzer 스킬 설치됨
```

---

## 2. 공통 설계 원칙

`prompt/5_0_common_automation_framework.md`를 단일 출처로 참조.

추가 원칙:
- §5.0.1 Assume Nothing: 환경 도구(ctags) 가용성을 먼저 확인, 없으면 grep 폴백
- §5.0.2 Reuse First: Python 파서 빌드 없이 기존 bash 도구만 사용
- §5.0.8 Artifact: overwrite 금지, timestamp 기반 파일명

---

## 3. 입력값

```text
- 코드 루트 경로
- 분석 확장자 (기본: .c .cpp .h .hpp)
- 제외 폴더 (기본: test/ third_party/ build/)
- target slug (선택, 미지정 시 폴더명에서 유도)
- IPC REQ 패턴 (선택, 기본: HAL_ / _REQ / SendMsg / PostMsg)
- IPC CNF 패턴 (선택, 기본: _CNF / CnfHandler / MsgDispatch)
```

---

## 4. 출력값

```text
structure_<YYYYMMDD_HHMM_KST>.json
  ├── meta          (root, slug, extracted_at, files, total_loc)
  ├── modules       (file, loc, functions[name, line, signature])
  ├── call_edges    (from, to, file, line, type[CALL|IPC_REQ])
  ├── ipc_req_sites (caller, ipc_call, file, line)
  ├── ipc_cnf_handler (function, file, line, branches[condition, calls])
  └── domain_branches (file, function, line, pattern)
```

curated 출력만 허용. raw AST / 심볼 테이블 전체 덤프 금지.

---

## 5. Artifact 규칙 (§5.0.8)

```text
%USERPROFILE%\artifacts\code_analyzer\<slug>\
└── structure_<YYYYMMDD_HHMM_KST>.json    ← 재실행 시 새 timestamp, overwrite 금지
```

---

## 6. AI 실행 지시 프롬프트

아래를 Claude Code에 **그대로 붙여넣고** `<>` 값만 채워서 실행한다.

```text
staged-code-analyzer Track B: <코드루트경로> 의 정적 구조를 bash로 추출해서 structure.json을 만들어줘.

[입력값]
- 코드 루트: <코드루트경로>
- 분석 확장자: .c .cpp .h .hpp
- 제외 폴더: <test/ third_party/ build/>
- IPC REQ 패턴: <HAL_ _REQ SendMsg PostMsg>
- IPC CNF 패턴: <_CNF CnfHandler MsgDispatch>
- target slug: <slug명, 빈 칸이면 폴더명에서 유도>

[추출 순서 — 이 순서대로 실행]

Step 1. 환경 확인
  - which ctags 확인. 없으면 grep 폴백 모드로 진행 (checkpoint에 "ctags unavailable" 기록)

Step 2. 파일 목록 + LOC
  - find <루트> -name '*.c' -o -name '*.cpp' -o -name '*.h' -o -name '*.hpp'
    (제외 폴더 적용)
  - xargs wc -l | sort -n

Step 3. 함수 시그니처 추출
  - ctags 사용 가능: ctags -R --fields=+n --c-kinds=fp -f - <루트>
  - ctags 없음: grep -rn '^[a-zA-Z_][a-zA-Z0-9_ *]*\s\+[A-Za-z_][A-Za-z0-9_]*\s*(' 패턴 폴백

Step 4. IPC REQ 지점 찾기
  - grep -rn "<IPC REQ 패턴>" <루트> --include="*.c" --include="*.cpp"
  - caller 함수 이름 + file + line 추출

Step 5. IPC CNF 핸들러 찾기
  - grep -rn "<IPC CNF 패턴>" <루트> --include="*.c" --include="*.cpp"
  - 핸들러 파일 (하나여야 함) + 함수명 + line 추출
  - 해당 함수 내 domainType 분기 구조 grep으로 확인

Step 6. domainType / stackId / RAT 분기 위치
  - grep -rn "domainType\|stackId\|rat ==" <루트> --include="*.c" --include="*.cpp"

Step 7. structure.json 합성
  - 위 결과를 curated JSON으로 합성
  - raw AST / 심볼 전체 테이블 금지
  - 매크로 안에 감춰진 IPC 호출 → call_edges에 "note": "[RN] macro-wrapped" 추가
  - 저장: %USERPROFILE%\artifacts\code_analyzer\<slug>\structure_<YYYYMMDD_HHMM_KST>.json
    (overwrite 금지)

[완료 후]
structure.json 경로와 요약 통계 (파일 수, 함수 수, IPC REQ 사이트 수, CNF 핸들러 확인 여부)를 출력하고 멈춰.
Track A 실행은 내가 별도로 시작할게.
```

---

## 7. 사용 예시

**입력**:
```
코드 루트: C:\p4\src\L1_CHANNEL\txswitch
slug: txswitch
제외: test\ build\
```

**Step 2 결과** (wc -l 요약):
```
400  src/txswitch/TxSwitchMngr.c
350  src/txswitch/TxSwitchMngrNr.c
250  inc/TxSwitch.h
...
total 1200 lines (5 files)
```

**Step 4 결과** (IPC REQ grep):
```
src/txswitch/TxSwitchMngr.c:145:  HAL_TxPathSet(&txParam);
src/endc/EndcCoord.c:230:         HAL_TxPathSet(&endcParam);
src/ulca/UlcaProc.c:312:          HAL_TxPathSet(&ulcaParam);
```

**Step 5 결과** (CNF handler grep):
```
src/handlers/L1_cnf_handler.c:50:  void RrcTxPathCnf(TxPathCnfParam_t *param) {
src/handlers/L1_cnf_handler.c:55:    switch(param->domainType) {
src/handlers/L1_cnf_handler.c:58:      case 0: case 2: TxSwitchUpdate(param); break;
src/handlers/L1_cnf_handler.c:61:      case 1: case 3: EndcUpdate(param); break;
```

**완료 출력**:
```
structure_20260618_0845_KST.json 생성 완료
  저장 위치: %USERPROFILE%\artifacts\code_analyzer\txswitch\structure_20260618_0845_KST.json
  파일 5개 / 함수 28개
  IPC REQ 사이트 3개 (TxSwitchMngr, EndcCoordinator, UlcaProcedure)
  CNF 핸들러 확인: RrcTxPathCnf @ L1_cnf_handler.c:50 (domainType 분기 2개)
  [RN] 0개
Track A 실행 준비 완료.
```

---

## 8. 검증 기준

```text
- structure.json 에 raw AST가 없어야 한다.
- ipc_req_sites 에 REQ 호출 지점이 모두 포함되어야 한다.
- ipc_cnf_handler 가 정확히 하나여야 한다. (두 개 이상이면 사용자에게 확인 요청)
- 매크로 감춰진 호출은 [RN] note로 표시되어야 한다.
- 재실행 시 기존 structure.json 이 overwrite되지 않아야 한다.
- ctags 없는 환경에서도 grep 폴백으로 완료되어야 한다.
```
