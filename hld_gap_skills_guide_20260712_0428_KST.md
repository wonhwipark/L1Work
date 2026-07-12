# HLD-코드 Gap 관리 스킬 가이드 — hld-code-compare (5.4) & hld-code-implement (5.4a)

> 대상: L1 채널모뎀 SW 파트원 (Claude Code 처음 쓰는 분 포함)
> 버전: hld-code-compare **v0.6.4** / hld-code-implement **v0.3.2**
> 작성: 20260711 KST

---

## 1. 한 줄 요약

**"설계문서(HLD)와 실제 코드가 얼마나 어긋나 있는지 찾아주고(5.4), 사람이 승인한 것만 골라서 코드에 반영해주는(5.4a) 도구"** 입니다.

- **5.4 hld-code-compare** = 탐지기. HLD와 코드를 대조해서 Gap 리포트를 만듭니다. **코드는 절대 건드리지 않습니다.**
- **5.4a hld-code-implement** = 시공팀. 5.4가 만든 리포트에서 여러분이 **직접 고른 Gap만**, **승인 절차를 거쳐** 코드에 반영합니다.

두 스킬은 일부러 분리돼 있습니다. "찾는 것"과 "고치는 것" 사이에 반드시 **사람의 판단**이 들어가게 하기 위해서입니다. (파트 원칙: *tool writes, human judges*)

---

## 2. 전체 파이프라인에서의 위치

```text
[5.2 code-analyzer]          [여러분]                [5.4 compare]              [5.4a implement]
코드 스캔                     HLD 준비                 HLD ↔ 코드 대조             승인된 Gap만 코드 반영
→ structure_*.json    +    (md 또는 Confluence)  →  → gap_report.yaml       →  → p4 edit → 수정
  (코드에 뭐가 있는지)                                  → gap_summary.md            → shannon-code-review
                                                       (뭐가 어긋났는지)            → impl_log.md
```

- **5.2는 필수가 아닙니다.** 5.2가 없어도 quick 훑기 → 히트 확인(승격)만으로 코드 수정까지 갈 수 있습니다(시나리오 B).
- 코드 수정 전 Perforce 체크아웃(`p4 edit`)과 shannon-code-review 연동이 자동으로 붙습니다.

---

## 3. 핵심 개념 5가지

이 5개만 이해하면 됩니다.

### 3-1. Gap — "어긋난 지점" 하나

HLD와 코드를 대조해서 발견한 불일치 하나하나가 Gap입니다. 각 Gap은 `GAP-001`, `GAP-002` 같은 **GAP-id**를 받습니다.

> **중요:** Gap을 지목할 때는 항상 **GAP-id**로 말하세요. "3번 고쳐줘"(X) → "GAP-003 구현해줘"(O).
> 목록의 행 번호는 문서마다/시점마다 달라져서 엉뚱한 Gap을 고치는 사고가 날 수 있습니다. 스킬도 순번으로 말하면 GAP-id를 되물어 확인하도록 돼 있습니다.

### 3-2. Gap 유형 3가지

| 유형 | 뜻 | 예시 | 5.4a에서 하는 일 |
|---|---|---|---|
| **미구현** | HLD엔 있는데 코드에 없음 | HLD는 `TX_SWITCH_CNF` 수신 처리를 요구하는데 핸들러가 없음 | HLD대로 **새로 구현** |
| **불일치** | 양쪽에 있는데 다름 | 심볼 철자가 다름, REQ/CNF 방향이 반대, NR/LTE 분기 누락 | 어긋난 부분만 **교정** |
| **문서누락** | 코드엔 있는데 HLD에 없음 | 코드에 `UL_CA_IND` 처리가 있는데 HLD에 서술 없음 | 코드는 안 건드리고 **HLD 보완 문안**을 만들어 줌 |

### 3-3. compare_mode — precise vs quick

5.4는 코드 쪽 정보(code inventory)를 얼마나 갖고 시작하느냐에 따라 두 모드로 돕니다.

| 모드 | 조건 | 결과의 신뢰도 | 코드 수정 가능? |
|---|---|---|---|
| **precise** | 5.2 structure json 또는 minimal inventory 있음 | 파일:라인 근거까지 확정 | **가능** |
| **quick_symbol_scan** | inventory 없이 소스 grep만 | 심볼 있다/없다 수준 | **불가** (재분석 안내만) |

Quick 결과 **그 자체로는** 코드 수정으로 이어지지 않습니다. 하지만 막다른 길이 아닙니다 — 리포트 뒤에 grep 히트를 확인해 주면 precise로 **승격**됩니다(시나리오 B). 5.2를 돌리거나 심볼 목록을 직접 작성하는 방법도 있습니다(§4-2).

### 3-4. implement_allowed — "이 Gap, 코드 수정해도 되는가"

5.4가 Gap마다 자동으로 판정해서 기록하는 플래그입니다. 다음을 **전부** 만족해야 true:

1. precise 모드로 비교했고
2. 근거가 structure/minimal inventory이고
3. 유형이 미구현 또는 불일치이고
4. 미구현이라면 "어느 파일에 넣을지"(삽입 앵커)가 확정됨

false인 Gap은 5.4a에서 코드 수정 목록에 아예 올라오지 않습니다. 이중 안전장치입니다.

### 3-5. fix_unit — Gap 안의 세부 수정 항목

Gap 하나가 실제로는 여러 작업일 수 있습니다. 예를 들어 "CNF 핸들러 미구현" Gap은:

```text
1) CNF handler stub 추가        [필수]
2) dispatch table 등록          [필수, 1번 이후]
3) state transition 연결        [선택, 1번 이후]
```

5.4a는 이렇게 쪼갠 뒤 **여러분이 고른 항목만** 구현합니다. "이번엔 stub이랑 dispatch만, state 연결은 다음에" 같은 부분 진행이 됩니다. (fix_unit은 Gap 안에서만 쓰는 번호라 번호 선택 OK)

---

## 4. 입력물 — 뭘 준비해야 하나

### 4-1. HLD 문서 (필수)

| 형태 | 준비 방법 | 비고 |
|---|---|---|
| 로컬 markdown | `.md` 파일 그대로 | `##`/`###` 헤딩이 절차 경계로 인식됨 |
| Confluence 페이지 | confluence-read 스킬로 html 다운로드 | `<h2>`/`<h3>`가 경계. Space shortcuts 같은 UI 잔재는 자동 제외 |

HLD에 특별한 마커나 형식을 맞출 필요 **없습니다.** 지금 쓰는 문서 그대로 넣으면 됩니다.

### 4-2. code inventory (코드 수정까지 가려면 필수)

셋 중 하나:

| 방법 | 준비 | 결과 |
|---|---|---|
| **A. 5.2 code-analyzer 결과** (권장) | 5.2를 먼저 돌려 `structure_*_focused.json` 확보 | precise, 가장 정확 |
| **B. minimal inventory 직접 작성** | 심볼-파일-라인 목록을 JSON으로 (아래 예시) | precise |
| **C. 승격 (5.2 없이 제일 쉬움)** | quick으로 훑은 뒤 grep 히트를 번호로 확인만 하면 됨 | precise (확인한 항목 한정) |
| **D. 아무것도 없음** | 소스 경로만 알려줌 | quick 훑기만 (→ C로 승격 가능) |

**B의 형식** (스킬 안 `schema/minimal_inventory.template.json`에 템플릿 있음):

```json
{
  "producer": "manual",
  "source_path": "src/tx/",
  "ipc_req_sites": [
    { "id": "REQ-001", "msg_symbol": "TX_SWITCH_REQ", "api": "SendIpcMsg",
      "file": "src/tx/tx_switch_mngr.c", "line": 380 }
  ],
  "ipc_cnf_handlers": [
    { "id": "CNF-001", "msg_symbol": "TX_SWITCH_CNF", "api": "OnIpcMsg",
      "file": "src/tx/tx_switch_mngr.c", "line": 412 }
  ]
}
```

---

## 5. 출력물 — 뭐가 나오나

### 5-1. 5.4 (compare)의 출력 — `{cwd}/hld_compare_output/<hld_slug>/` 아래

#### gap_report.yaml — 기계용 원본 (5.4a의 입력)

모든 판정의 단일 원본(SSOT)입니다. Gap마다 유형·근거(HLD 어디, 코드 어디)·확신도·implement_allowed가 기록됩니다. **직접 편집하지 마세요.** 5.4a가 진행 상태(status, fix_units)를 이 파일에 갱신합니다.

```yaml
gaps:
  - id: GAP-001
    type: 미구현
    hld_ref: "tx_switch_hld.md#tx-switch-procedure"
    code_ref: { file: "src/tx/tx_switch_mngr.c", func: "ProcTxSwitch", line: 412,
                msg_symbol: "TX_SWITCH_CNF" }
    detail: "HLD는 CNF 수신 처리를 요구하나 핸들러 없음"
    confidence: HIGH
    implement_allowed: true
    status: 탐지됨
```

#### gap_summary.md — 사람이 보는 검토표 (여러분이 읽을 문서)

이것만 읽으면 됩니다. 구성:

```text
헤더        : 짝이 되는 gap_report 파일명 (5.4a에 넘길 입력)
1. 한눈에    : "코드 수정 가능 N건 / 문서 보완 M건 / 검토 후보 K건" + 유형×확신도 매트릭스
2. 코드 수정 가능  : implement_allowed=true 목록 (GAP-id, 심볼, 근거 위치)
3. 문서 보완 대상  : 문서누락 목록 → 5.4a가 HLD 보완 문안을 만들어 줌
4. 검토 후보      : quick 결과 등 수정 불가 목록 → 재분석 필요
5. 판정 제외      : 근거 부족으로 판정 보류한 것들
6. 다음 행동      : 뭘 하면 되는지 안내
```

### 5-2. 5.4a (implement)의 출력 — `{cwd}/hld_implement_output/<gap_report_stem>/` 아래

#### impl_log.md — 구현 기록 (append 누적)

맨 위에 **Gap 현황 요약표**가 항상 갱신됩니다. "지금까지 뭘 얼마나 고쳤나"는 이 표 하나로 확인:

```text
| GAP-id  | 유형   | status   | fix_unit (done/전체) | 최근 갱신          |
|---------|--------|----------|----------------------|--------------------|
| GAP-001 | 미구현 | 수정완료 | 2/2                  | 20260711_1530_KST |
| GAP-003 | 불일치 | 부분수정 | 1/2                  | 20260711_1512_KST |
```

그 아래로 사이클별 계획·diff 요약·리뷰 결과가 시간순으로 쌓입니다.

#### 그리고 실제 코드 수정

`p4 edit` 체크아웃 → 선택한 fix_unit 범위만 수정 → diff 요약 출력 → shannon-code-review 리뷰. **빌드/UT는 자동 실행하지 않고** 명령만 안내합니다(실행과 결과 확인은 사람 몫).

---

## 6. 사용법 — 실전 시나리오

### 시나리오 A. 처음부터 끝까지 (가장 흔한 경우)

**0단계 — 준비**: HLD md(또는 Confluence 링크)와 5.2 structure json을 준비.

**1단계 — Gap 탐지 (5.4)**

```text
나  : HLD랑 코드 비교해줘. HLD는 tx_switch_hld.md, structure는 어제 5.2로 뽑은 거.
스킬: [S0 입력 확정 → S1 인벤토리 → S2 판정 → S3 리포트]
     gap_summary_tx_switch_20260711_1830_KST.md 생성.
     코드 수정 가능 3건 / 문서 보완 1건 / 검토 후보 0건
     [진행: REPORT_DONE → 다음: gap_summary 검토]
```

**2단계 — 검토표 읽기**: gap_summary.md를 열어 2번 표(코드 수정 가능)를 봅니다. 어떤 GAP-id를 고칠지 정합니다.

**3단계 — 구현 (5.4a)**

```text
나  : GAP-001 구현해줘
스킬: GAP-001 [미구현] TX_SWITCH_CNF — 수정 가능한 항목:
     1) CNF handler stub 추가     [code / 필수]
     2) dispatch table 등록       [code / 필수, 1번 이후]
     3) state transition 연결     [code / 선택, 1번 이후]
     진행할 항목 번호를 선택하세요.
나  : 1, 2
스킬: [계획] 대상: src/tx/tx_switch_mngr.c :: TxSwitchCnfHandler(신규), dispatch table
     변경: TX_SWITCH_CNF 수신 handler stub 추가 및 dispatch 등록
     영향: 이 파일 1개. state 연결은 이번 제외
나  : 진행해
스킬: p4 edit → 수정 → diff 요약 → shannon-code-review 리뷰 → status 갱신
     GAP-001: 부분수정 (2/3 done). 남은 구현 가능 Gap 2건.
```

한 번에 **Gap 하나씩**만 진행됩니다. "전부 고쳐줘"라고 해도 목록 확인 후 하나씩 돕니다.

### 시나리오 B. 5.2 결과가 없을 때 — quick 훑기 → 승격으로 코드 수정까지

5.2 설치가 필수가 아니므로, 없는 분은 이 경로를 쓰면 됩니다.

```text
나  : structure 없는데 일단 HLD랑 소스 폴더만으로 비교해봐
스킬: inventory가 없어 quick_symbol_scan 모드로 진행합니다.
     ... (리포트 생성) ...
     검토 후보 3건입니다. grep 히트를 확인해 주시면 정밀 판정으로 승격할 수 있습니다.
나  : 확인할게
스킬: grep 히트 후보 (확인된 항목만 inventory로 승격됩니다)
     1. TX_SWITCH_REQ → src/tx/tx_switch_mngr.c:380  (SendIpcMsg 호출부)
     2. TX_SWITCH_CNF → src/tx/tx_switch_mngr.c:412  (OnIpcMsg 분기)
     3. TX_SWITCH_CNF → src/tx/tx_switch_test.c:88   (테스트 코드로 추정)
     확인할 번호를 선택하세요 (예: 1,2 / 전체 / 없음).
나  : 1,2
스킬: 승격 inventory 생성(producer: quick_promoted) → precise 재판정 →
     새 gap_report 생성. 코드 수정 가능 2건.
```

여러분이 히트를 확인하는 행위가 곧 "근거 승인"이라서, 이후는 5.2를 쓴 것과 동일하게 코드 수정(시나리오 A의 3단계)으로 이어집니다. 틀린 히트(예: 테스트 코드, 주석)는 선택하지 않으면 버려집니다. 확인 없이 자동 승격되는 일은 없습니다.

원하면 승격 대신 5.2를 돌리거나(§4-2 A) 심볼 목록을 직접 작성해도(§4-2 B) 됩니다.

### 시나리오 C. 문서누락 — HLD를 보완할 때

```text
나  : GAP-004 진행해줘   (문서누락 건)
스킬: 이 Gap은 문서 보완 대상입니다. 코드는 수정하지 않습니다.
     HLD에 추가할 보완 문안(마크다운)을 생성했습니다: ...
```

문안을 Confluence에 실제로 올릴지는 사람이 결정합니다(게시는 스킬 범위 밖).

### 시나리오 D. 중단했다가 이어하기

같은 폴더(cwd)에서 스킬을 다시 부르면 됩니다. 상태 파일(`NEXT_STEP_5.4.md` / `NEXT_STEP_5.4a.md`)을 읽고 멈춘 지점부터 이어갑니다. gap_report 경로도 다시 묻지 않고, impl_log의 현황 요약표를 먼저 보여줍니다.

### 시나리오 E. 코드가 바뀌어서 다시 비교할 때 (재판정)

5.4를 같은 HLD로 다시 돌리면 **새 타임스탬프의 리포트**가 생기고, 기존에 승인/수정하던 이력(status, fix_units)은 **같은 GAP-id로 자동 승계**됩니다. 승인 이력이 날아가지 않습니다. 같은 폴더에 리포트가 여러 개면 **항상 최신 타임스탬프가 유효본**입니다.

### 시나리오 F. Confluence에 현황 올리기 (선택)

리포트 완료(5.4) 또는 구현 사이클 완료(5.4a) 후 스킬이 한 번 물어봅니다:

```text
스킬: [Gap] 페이지를 Confluence에 게시할까요?
나  : 게시해줘
스킬: (최초 1회만) 부모 페이지 확인 — HLD가 Confluence 출신이면 그 페이지 아래로 자동 제안
     → [Gap] 페이지 생성 또는 최신 내용으로 갱신
```

만들어지는 구조 (HLD 원본은 절대 건드리지 않음):

```text
HLD 페이지 (원본)
└── [Gap] <HLD명>   ← HLD당 딱 1페이지
     ├ 현황 요약 (색상 배지)
     ├ Gap 판정표 (3단)
     ├ 구현 이력 (사이클 누적, 상세는 접힘)
     ├ MSC (선택, PlantUML)
     └ 원본 경로
```

발행할 때마다 로컬 원본(gap_report + impl_log)에서 페이지 전체를 다시 그려 갱신합니다. impl_log가 계속 쌓이므로 이력도 자동으로 누적 표시되고, 과거 발행본은 Confluence 페이지 버전 히스토리로 남습니다.

- 상태·확신도는 색상 배지(수정완료=녹색, 부분수정=노랑 등)로, 심볼·경로는 고정폭으로 표시됩니다.
- MSC가 필요하면 5.2가 만든 `.puml` 파일을 지정하세요 — PlantUML 박스로 들어가 다이어그램으로 렌더되고, 플러그인이 없어도 원문이 접힌 코드블록으로 남습니다.
- 로컬 파일이 원본(SSOT)이고 Confluence는 보기용입니다. Confluence에서 직접 고친 내용은 스킬에 반영되지 않으니, 수정은 항상 스킬 쪽에서 하세요.
- 인증은 환경변수(`CONFLUENCE_BASE_URL` + `CONFLUENCE_PAT`, 또는 User **ID**/비밀번호)로 1회 설정합니다.

---

## 7. 안전장치 정리 (왜 믿고 써도 되나)

1. **승인 없이 코드를 만지지 않습니다.** Gap 선택(GAP-id) → fix_unit 선택 → 변경 계획 확인, 3중 게이트를 전부 통과해야 수정이 시작됩니다.
2. **Quick 결과는 코드 수정으로 이어질 수 없습니다.** implement_allowed 플래그가 원천 차단합니다.
3. **수정 범위가 잠겨 있습니다.** 선택한 fix_unit의 파일·함수만. 겸사겸사 리팩토링, 스타일 정리 안 합니다.
4. **근거 없는 추측을 안 합니다.** HLD가 모호하면 `[RN]`으로 남기고 물어봅니다. 2회 물어도 불확정이면 보류하고 다음으로 넘어갑니다.
5. **Perforce 체크아웃 실패 시 수정하지 않습니다.**
6. **모든 판정과 수정에 근거가 붙습니다.** HLD 어느 절, 코드 어느 파일:라인인지 리포트와 로그에 남습니다.

---

## 8. 자주 묻는 질문

**Q. HLD 형식을 바꿔야 하나요?**
아니요. 지금 쓰는 md/Confluence 문서 그대로 됩니다. `##`/`###` 헤딩만 절차 구분에 쓰입니다.

**Q. gap_report.yaml을 직접 고쳐도 되나요?**
안 됩니다. 판정 필드는 5.4, 진행 상태는 5.4a가 소유합니다. 판정이 틀렸다고 생각되면 5.4a에서 "이건 Gap 아니야"라고 하면 `기각` 처리됩니다.

**Q. 여러 Gap을 한 번에 고칠 수 있나요?**
목록 확인 후 순서대로 하나씩 진행됩니다. 한 diff에 여러 Gap을 섞지 않는 게 리뷰와 롤백에 유리하기 때문입니다.

**Q. 빌드까지 해주나요?**
아니요. diff와 리뷰까지만. 빌드/UT 명령은 안내만 하고 실행·확인은 사람이 합니다.

**Q. HLD 범위 일부만 비교할 수 있나요?**
됩니다. 기본이 hld_bounded(선택 헤딩 범위)이고, 헤딩 목록을 번호로 골라 범위를 지정할 수 있습니다. 전체 양방향 대조는 "전체 대조"라고 명시하면 closed_scope로 돕니다.

**Q. 5.2(code-analyzer) 설치가 필수인가요?**
아니요. quick 훑기 → grep 히트 확인(승격)만으로 코드 수정까지 갑니다(시나리오 B). 5.2는 가장 정확하고 편한 경로일 뿐입니다.

**Q. Confluence 게시는 자동인가요?**
아니요. 완료 시점에 한 번 제안만 하고, 승인해야 올라갑니다. 거절하면 다시 묻지 않습니다.

**Q. 파일명이 왜 전부 영문인가요?**
Windows ZIP의 CP949/UTF-8 문제로 한글 파일명이 유실될 수 있어 산출물 파일명은 ASCII로 통일했습니다.

---

## 9. 요약 치트시트

```text
탐지     : "HLD랑 코드 비교해줘" + HLD 경로 (+ structure json 경로)
검토     : hld_compare_output/<slug>/gap_summary_*.md 열기
구현     : "GAP-xxx 구현해줘" → fix_unit 번호 선택 → 계획 확인 → 진행
현황     : hld_implement_output/<stem>/impl_log.md 맨 위 요약표
이어하기 : 같은 폴더에서 스킬 재호출
재비교   : 그냥 다시 돌리면 됨 (승인 이력 자동 승계, 최신 리포트가 유효본)
5.2 없음 : quick 훑기 → "확인할게" → 히트 번호 선택 → precise 승격 → 수정 가능
게시     : 완료 후 "게시해줘" → [Gap] 페이지 최신으로 갱신 (HLD당 1페이지)
철칙     : Gap은 반드시 GAP-id로 지목
```

문의: 박원휘 (TL)
