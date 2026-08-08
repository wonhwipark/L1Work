# sam.graph.js 데이터 확인 가이드

> **상황**: MCD 스코어(score_penalty, cycle_index, relation_count)가 CSV엔 없고
> HTML 표에만 있는데, 그 표는 JS가 채움. 다운로드된 js 중 **`sam.graph.js`**가
> SAM 전용 스크립트라 여기에 데이터가 있을 가능성이 높음.
> 나머지(datatables, vis, chart, plugins, scripts .bundle.js)는 라이브러리라 무관.
>
> **목표**: sam.graph.js 안 데이터의 **구조와 키 이름**을 확인.
> 그러면 그 데이터를 뽑아 CSV와 합쳐 "스코어순 순환 목록"을 만들 수 있음.

---

## 여는 법

`sam.graph.js`를 텍스트 에디터(메모장, VSCode 등)로 열고 **Ctrl+F**로 검색.

---

## 확인 1 — 데이터가 여기 있나

아래 단어를 차례로 검색:
- `score_penalty`
- `cycle_index`
- 실제 스코어 값 하나 (예: `-4.01`)

**답:**
- [ ] 위 중 하나라도 검색되나요? (되면 → 확인 2로 / 안 되면 → 확인 4로)
- [ ] 검색되면, 파일 크기는 대략? (데이터가 많으면 파일이 큼)

```
[답]

```

---

## 확인 2 — 데이터 형태 ★ 핵심

`score_penalty`가 검색된 곳 주변을 보고, 어느 쪽인지 표시:

- [ ] **형태 A — 데이터가 직접 박힘**
      예: `var data = [{"cycle_index":1, "score_penalty":-4.01, ...}, ...];`
      (JSON 배열/객체가 파일 안에 있음)

- [ ] **형태 B — 로직만, 데이터는 밖에서 받음**
      예: `var data = window.samData;`
      또는 `document.getElementById(...)` 로 읽어옴

```
[형태 A/B 중 무엇인지]

```

---

## 확인 3 — 데이터 구조 복사 (형태 A일 때) ★ 가장 중요

데이터 **한 덩어리(한 순환분)**의 구조/키 이름을 복사.
**실제 값은 가려도 됨. 키 이름과 구조만 필요.**

```
[여기에 한 순환 항목 구조 붙여넣기]
예: {"cycle_index": N, "module": "___", "relation_count": N, "score_penalty": -N.NN}


```

**추가로 답:**
- [ ] 데이터 변수 시작 부분? (예: `var cycleData = [`, `const rows = [`)
- [ ] module(순환 대상) 표현: from/to 두 개? 화살표 문자열? 배열?
- [ ] 각 항목에 CSV와 연결할 **cycle_index(또는 cycle_id)** 가 있나요?

```
[답]

```

---

## 확인 4 — 데이터 출처 추적 (형태 B이거나, 확인 1이 "검색 안 됨"일 때)

sam.graph.js가 데이터를 밖에서 받으면, 어디서 받는지 확인.
sam.graph.js 안에서 아래를 검색:
- [ ] `fetch(` / `ajax` / `.json` — 있으면 그 URL·파일명 적기
- [ ] `getElementById` / `querySelector` — html 요소에서 읽는다는 뜻, 그 id/선택자 적기
- [ ] `window.` 뒤에 오는 변수명 (예: `window.samData`)

```
[답]

```

> 형태 B이면 데이터가 **html 파일 안 `<script>` 태그**에 있을 가능성이 큼.
> 그 경우 html을 Ctrl+U로 열어 `<script>` 안 데이터를 확인 (다음 단계에서 안내).

---

## 우선순위

1. **확인 1** — 데이터가 sam.graph.js에 있나
2. **확인 3** — 있으면 **구조/키 이름 복사** (스크립트 재료)

이 둘이 핵심. **확인 3의 데이터 구조**만 가져오면
sam.graph.js에서 스코어를 뽑는 스크립트를 만들 수 있음.

---

## 이후 진행 (참고)

| 결과 | 다음 |
|------|------|
| 형태 A (데이터 직접 박힘) | js에서 JSON 뽑는 Python 스크립트 → CSV와 cycle_index로 병합 → 스코어순 목록 |
| 형태 B → html `<script>`에 데이터 | html에서 데이터 추출로 전환 |
| 형태 B → 외부 .json/API | 그 파일·URL 직접 확인 |

**핵심 요청**: 확인 3에서 score_penalty가 담긴 **데이터 한 덩어리의 구조/키 이름**.
값은 가려도 되고 구조만 있으면 됨.
