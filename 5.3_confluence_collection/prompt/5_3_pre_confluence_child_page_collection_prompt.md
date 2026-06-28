# 5.3-pre Confluence Child Page Collection — AI 실행 프롬프트

---

## 1. 목적

이 문서는 Confluence 접속이 이미 가능한 상황에서 이번 주 Parent Page URL을 기준으로 하위 Child Page를 실제로 탐색하고, 필요한 경우 재사용 가능한 discovery profile을 생성/갱신하며, Child Page 본문을 읽어 5.3 Weekly Report Collection의 입력 draft를 생성하기 위한 AI 실행 프롬프트다.

이 문서는 Python 패키지 구현 지시가 아니라 현재 사용 가능한 Confluence read 수단으로 실제 Child Page 후보를 찾고 본문을 취합하여 원본 draft를 생성하는 실행 지시서다.

---

## 2. 선행 전제

아래는 이미 작동 가능한 것으로 전제한다.

```text
- Confluence 접속 및 읽기 권한
- MCP, REST API, 브라우저/현재 세션 등 현재 사용 가능한 Confluence read 수단
- Parent Page URL 접근 가능성
- Child Page 또는 descendant 조회에 필요한 인증/권한
```

이 프롬프트에서는 아래 작업을 수행하지 않는다.

```text
- MCP 서버 설치
- MCP 서버 설정
- REST API 토큰 발급 또는 인증 설정
- Node.js, npm, npx, Python 패키지 설치
- Confluence write/update 권한 검증
```

---

## 3. 입력값

### 3.1 필수 입력

```text
- Parent Page URL: 이번 실행에서 기준으로 삼을 Confluence Parent Page URL
```

### 3.2 선택 입력

```text
- Space Key: Confluence space key를 알고 있는 경우
- Expected Title Pattern: Child Page 제목에 포함될 것으로 예상되는 문자열 또는 정규식
- Expected Label: Child Page에 붙어 있을 것으로 예상되는 label
- Current Week: 예: W23, 2026-W25 등 주차 식별자
- Expected Owner/Team Keyword: 팀명, 담당자명, 조직명 등 본문/제목 필터에 사용할 키워드
- Max Depth: direct child만 볼지, descendants 전체를 볼지 결정하는 깊이 기준
```

선택 입력이 없더라도 Parent Page URL만으로 탐색을 시작해야 한다. 선택 입력은 confidence 산정과 fallback 필터링에만 사용한다.

---

## 4. 수행 순서

아래 순서를 따른다. 특정 단계가 실패해도 즉시 종료하지 말고 다음 fallback 단계로 진행한다.

### 4.1 Parent URL 확인

```text
1. Parent Page URL 형식이 Confluence URL인지 확인한다.
2. URL에서 pageId가 직접 포함되어 있는지 확인한다.
3. pageId가 없으면 URL slug, space key, title 후보를 추출한다.
4. URL 접근 가능성 확인:
   - 200 OK: 진행 (4.2 resolve 단계로)
   - 403 Forbidden: "권한 없음" 기록 → 4.2에서 MCP/다른 수단 가능성 확인 (기존 세션 사용)
   - 401 Unauthorized: "로그인 필요" 기록 → 4.2에서 기존 MCP 세션 사용
   - 404 Not Found: "Page 없음" 기록 → 4.2에서 title/space 기반 resolve 필수 시도
   - 3xx Redirect: redirect 경로 추적 후 최종 URL로 진행
   - Connection Error/Timeout: "접근 불가" 기록 → fallback으로 진행
```

### 4.2 Parent Page ID resolve

```text
1. Parent Page URL에 pageId가 있으면 이를 우선 사용한다.
2. pageId가 없으면 REST API의 content lookup 또는 현재 가능한 Confluence read 수단으로 title/space 기반 resolve를 시도한다.
3. resolve 결과 선택 우선순위 (다중 결과인 경우):
   a) 원본 URL의 space key와 일치하는 page
   b) URL slug와 제목이 일치하는 page (부분 일치)
   c) URL의 ancestor path와 parent 관계가 일치하는 page
   d) 최근 수정된 page (마지막 수정일 최신)
   → 자동 선택 불가 시: user assisted mode로 후보 제시
4. Parent Page ID, title, space key는 실행 결과 요약에는 포함할 수 있으나 strategy profile에는 특정 주차 값으로 저장하지 않는다.
```

### 4.3 REST descendants/children 조회

```text
1. REST API로 Parent Page의 direct children 조회를 시도한다.
2. direct children이 없거나 부족하면 descendants 조회를 시도한다.
3. 각 후보의 title, url, id, depth, parent relation, label, last updated 정보를 가능한 범위에서 수집한다.
4. 조회 실패 시 원인별 처리:
   
   실패 원인 | 처리 방법
   ---------|----------
   403 Forbidden (권한 없음) | → MCP 시도 (4.4), 본문 링크 추출 (4.5)
   401 Unauthorized | → 기존 세션 MCP 사용 가능성 있음 (4.4로)
   404 Not Found | → Parent Page resolve 다시 확인 (4.2 재시도)
   400 Bad Request | → endpoint/parameter 조정 후 재시도 또는 MCP (4.4)
   pagination/truncation | → 최대 200개까지만 수집, 초과 시 confidence 다운 기록
   timeout/connection error | → MCP 시도 (4.4), 본문 링크 (4.5)
```

우선 시도할 REST 조회 유형은 다음과 같다.

```text
- children/page 조회
- descendants/page 조회
- ancestor 기반 CQL 또는 content search
- label/title 조건이 있을 경우 CQL search
```

### 4.4 MCP child page 조회

MCP 도구 이름과 입력 schema는 환경마다 다를 수 있으므로, 특정 함수명을 가정하지 않는다. 현재 세션에서 사용 가능한 MCP Confluence read 도구를 먼저 확인한 뒤, 그 도구가 제공하는 방식에 맞춰 child/descendant 조회를 수행한다.

```text
1. 현재 세션에서 사용 가능한 도구 목록 확인:
   - 도구 이름, 설명, input schema, output 형식 확인
   - "confluence", "child", "page", "tree", "descendant" 키워드 포함 도구 우선 주목

2. 각 도구 schema 검토:
   - input: parent_page_id, parent_page_url, parent_title, space_key 중 어떤 형식 지원하는가?
   - output: page list, tree structure, metadata 포함 범위?

3. 우선 순위 (input 지원 형식):
   a) parent_page_id (가장 정확)
   b) parent_page_url (URL에서 추출 필요)
   c) parent_title + space_key (title/space 기반)
   d) 그 외 schema (비표준 input 형식)

4. 선택된 도구로 조회 시도:
   - input 형식에 맞춰 Parent Page ID/URL/title 전달
   - 결과가 없으면 다음 우선 도구 시도

5. MCP 호출 실패 원인별:
   - schema 불명확: 4.5 본문 링크로
   - timeout: 4.5 본문 링크로
   - auth error: REST 재시도 또는 4.5로
```

### 4.5 Parent 본문 링크 추출

```text
1. Parent Page 본문을 조회한다.
2. 본문 내 Confluence page 링크를 추출한다.
3. 링크 텍스트, URL, 주변 문맥을 함께 기록한다.
4. Parent와 같은 space 또는 ancestor 관계로 보이는 링크를 우선 후보로 분류한다.
5. attachment, external link, anchor link, non-page link는 제외하거나 낮은 confidence로 분류한다.
```

### 4.6 label/title/fuzzy fallback

fallback 진입 조건:
```text
- high confidence 후보가 0개, OR
- medium confidence 후보가 1개 미만, OR
- 사용자가 명시적으로 더 찾기 요청
```

진입 시 다음 fallback을 순차 적용한다.

```text
1. Label Search: expected label이 있으면 해당 label 기반으로 검색한다.
2. Title Pattern Search: expected title pattern 또는 current week를 제목 검색에 사용한다.
3. Space-scoped Search: space key가 있으면 같은 space 내부로 검색 범위를 제한한다.
4. Fuzzy Search: Parent title, current week, team keyword, report keyword를 조합해 유사 제목을 찾는다.
5. User Assisted Mode: 자동 판단이 불가능하면 후보 목록과 부족한 근거를 제시하고 사용자가 선택할 수 있게 한다.
```

User Assisted Mode는 자동화 실패가 아니라 low confidence fallback이다. 이 모드에서는 AI가 다음을 제시해야 한다.

```text
- 후보별 URL/title/id
- 후보로 판단한 근거
- confidence가 낮은 이유
- 사용자가 선택해야 할 최소 선택지
- 선택 후 profile에 저장할 strategy 방향
```

### 4.7 Child Page 본문 읽기 및 취합 원본 draft 생성

Child Page 후보가 high 또는 medium confidence로 확보되면, 후보 Page의 본문을 읽어 5.3 Weekly Report Collection 단계에서 사용할 취합 원본 draft를 생성한다.

```text
1. 확정된 Child Page 본문을 가능한 read 수단으로 조회한다.
2. 각 Child Page별 제목, 작성자/소유자 추정값, URL, 본문 주요 섹션, Action Item, Risk/Issue, 이번 주 진행/다음 주 계획 항목을 보존한다.
3. 본문 구조가 서로 달라도 원문 의미를 과도하게 재작성하지 않고, 출처 URL과 함께 Markdown으로 취합한다.
4. 이전 주 양식 적용이나 최종 TL 보고서 정리는 수행하지 않는다. 이 작업은 5.3 Weekly Report Collection 단계에서 수행한다.
5. 취합 원본 draft를 아래 경로에 저장한다.
```

```text
%USERPROFILE%\artifacts\weekly_report_draft_<YYYYMMDD>_<HHMM>_KST.md
```

이 pre 단계의 산출물은 Child Page 본문 취합 원본이며, 별도의 `weekly_report_source_<YYYYMMDD>_<HHMM>_KST.json` 산출물은 생성하지 않는다.

### 4.8 결과 요약 및 포맷

실행 결과 출력 포맷:

```markdown
---
## 실행 결과: Child Page Collection

**Parent Page:**
- Title: [title]
- Space: [space_key]
- URL: [url] (또는 pageId: [id])
- Resolve 방법: [URL direct / title+space lookup]

**Collection/Discovery Method 시도 결과:**
| Method | 상태 | 후보 수 | 실패 사유 |
|--------|------|--------|---------|
| REST children | ✅/⏭️/❌ | N | - |
| REST descendants | ✅/⏭️/❌ | N | (해당하면) |
| MCP page_tree | ✅/⏭️/❌ | N | (해당하면) |
| Parent body links | ✅/⏭️/❌ | N | (해당하면) |
| Label search | ✅/⏭️/❌ | N | (fallback 진입 시만) |

**발견된 Child Page 후보:**

| # | Title | Confidence | Discovery Method | URL/ID |
|---|-------|-----------|------------------|--------|
| 1 | [title] | High/Medium/Low | [method] | [url] (id: [id]) |
| 2 | [title] | High/Medium/Low | [method] | [url] (id: [id]) |

**최종 결론:**
- 추천: [title1], [title2] (high/medium confidence)
- confidence: High/Medium/Low
- user_assisted_mode_required: true/false

**Draft Artifact:**
- Path: `%USERPROFILE%\artifacts\weekly_report_draft_<YYYYMMDD>_<HHMM>_KST.md`
- Role: Child Page 본문 취합 원본. 5.3 Weekly Report Collection의 입력으로 사용.

**Strategy Profile Preview:**
```json
{
  "last_success_method": "confluence_rest_children",
  "confidence": "high",
  "strategy": {...},
  "fallback_methods": [...]
}
```

---
```

---

## 5. 성공 판정 기준

### 5.1 실행 성공

아래 중 하나 이상을 만족하면 실행 성공으로 본다.

```text
- Parent Page ID를 resolve했고 direct children 또는 descendants 후보를 1개 이상 찾았다.
- REST 또는 MCP로 Parent-child 관계가 확인된 후보를 1개 이상 찾았다.
- Parent 본문 링크에서 Child Page로 볼 수 있는 후보를 1개 이상 찾았다.
- 자동 확정은 어렵지만 user assisted mode에 제시할 수 있는 합리적 후보를 1개 이상 찾았다.
```

### 5.2 실행 실패

아래는 실행 실패로 본다.

```text
- Parent Page URL 접근 또는 resolve가 불가능하다.
- REST/MCP/본문 조회/검색 fallback이 모두 실패했고 후보가 없다.
- 권한 문제로 Parent Page 또는 하위 Page 정보를 확인할 수 없다.
- 후보는 있으나 Parent와의 관계, 제목, label, 본문 링크 근거가 모두 불충분하다.
```

### 5.3 후보 0개인 경우

아래 중 해당되면 실행 실패로 판단한다.

```text
- Parent Page URL 접근 및 resolve 실패
- 모든 discovery method 시도 후 1개 이상 후보 없음
- 권한 문제로 어떤 method도 정보 수집 불가
```

이 경우 결과 요약:
```text
- 실패 원인: [권한 / 네트워크 / 데이터 부재 중 명확히]
- 시도된 discovery method 목록 및 각 실패 사유
- 추가 정보 필요: [예: Confluence 권한 확인, space key 제공 등]
- profile 생성 안 함 (strategy 검증 불가)
```

---

## 7. Confidence 기준

### 7.1 high

```text
- REST descendants/children 또는 MCP page tree에서 Parent-child 관계가 직접 확인됨
- 후보 title 또는 label이 선택 입력과 일치하거나 업무 맥락상 명확함
- 중복 후보가 없거나 최종 후보가 명확히 우세함
```

### 7.2 medium

```text
- Parent 본문 링크 또는 ancestor 기반 검색으로 후보를 찾음
- title/label/current week 중 일부만 일치함
- Parent-child 관계는 간접적으로 확인되지만 후보가 비교적 명확함
```

### 7.3 low

```text
- fuzzy search 또는 user assisted mode로만 후보를 찾음
- 후보가 여러 개이고 자동 선택 근거가 약함
- Parent-child 관계가 직접 확인되지 않음
- title/label/current week 근거가 부분적이거나 불명확함
```

---

## 8. 출력 원칙

### 8.1 실행 결과에는 포함 가능

이번 실행에서 찾은 실제 후보 목록은 사용자에게 보여준다.

```text
- Parent Page URL
- Parent Page ID
- Parent Page title
- Child 후보 URL
- Child 후보 ID
- Child 후보 title
- 후보별 discovery method
- 후보별 confidence
- 판단 근거
```

### 8.2 Strategy Profile에는 저장 금지

Discovery Strategy Profile은 재사용 가능한 방법만 저장한다. 특정 주차에 종속된 값은 저장하지 않는다.

```text
- 특정 주차 Parent Page URL 저장 금지
- 특정 주차 Parent Page ID 저장 금지
- 특정 주차 Child Page URL 목록 저장 금지
- 특정 주차 Child Page ID 목록 저장 금지
- 특정 실행에서만 의미 있는 current week literal 저장 금지
```

### 8.3 Strategy Profile에 저장 가능

```text
- last_success_method
- confidence
- input_type: parent_page_url
- resolve_parent_page_id_at_runtime: true
- discovery_query_type
- child_filter_rule
- fallback_methods
- user_assisted_mode_required 여부
- selected_strategy_reason
- profile_updated_at_kst
```

---

## 9. dry-run/apply 구분

### 9.1 dry-run

dry-run은 기본 모드다.

```text
- Confluence 조회 수행
- Parent resolve 수행
- Child 후보 탐색 수행
- 후보 목록과 confidence 요약 출력
- profile에 저장할 내용 preview 출력
- profile 파일은 생성/수정하지 않음
```

### 9.2 apply

apply는 사용자가 명시적으로 요청한 경우에만 수행한다.

```text
- dry-run과 동일한 조회/요약 수행
- 성공한 discovery strategy를 profile로 저장
- 저장 전 특정 주차 URL/ID/Child 목록이 profile에 포함되지 않았는지 검증
- 기존 profile이 있으면 overwrite 가능
```

Profile 저장 경로는 고정한다.

```text
%USERPROFILE%\artifacts\child_page_discovery_profile.json
```

---

## 10. 다음 주 반복 실행 시 기존 profile 사용

이미 `%USERPROFILE%\artifacts\child_page_discovery_profile.json`이 존재하는 경우, 다음 주 반복 작업에서는 전체 discovery 검증을 처음부터 반복하지 않는다.

기존 profile은 특정 Parent URL, Parent ID, Child URL, Child ID를 저장하는 URL/ID 캐시가 아니다. 기존 profile은 현재 환경에서 검증된 Child Page 탐색 전략을 재사용하기 위한 strategy cache다.

### 10.1 반복 실행 입력과 profile 로딩

다음 주 반복 실행에서는 새 Parent Page URL을 입력받은 뒤, 먼저 기존 profile을 읽는다.

```text
1. 새 Parent Page URL을 입력받는다.
2. %USERPROFILE%\artifacts\child_page_discovery_profile.json 존재 여부를 확인한다.
3. profile이 존재하면 먼저 읽고, profile.last_success_method를 우선 적용한다.
4. Parent Page ID와 Child 후보는 새 Parent Page URL 기준으로 runtime에 다시 resolve/discover한다.
```

### 10.2 last_success_method 우선 적용

`profile.last_success_method`는 다음 주 반복 작업의 1순위 discovery method다.

```text
- last_success_method가 성공하고 confidence가 충분하면 즉시 후보를 확정한다.
   - 발견된 Child 후보의 본문을 읽어 `%USERPROFILE%\artifacts\weekly_report_draft_<YYYYMMDD>_<HHMM>_KST.md` 취합 원본 draft를 생성한다.
   - 생성된 draft를 5_3_weekly_report_collection_py_package_prompt.md 입력으로 넘긴다.
- 이때 profile에는 새 주차의 Parent URL/ID 또는 Child URL/ID 목록을 저장하지 않는다.
```

### 10.3 fallback_methods 적용

`profile.last_success_method`가 실패하거나 confidence가 낮으면 `profile.fallback_methods` 순서대로 탐색한다.

```text
1. fallback_methods에 정의된 순서를 유지한다.
2. 각 fallback은 새 Parent Page URL 기준으로 runtime 조회한다.
3. high 또는 medium confidence 후보가 확보되면 중단하고 결과를 요약한다.
4. 성공한 method가 기존 last_success_method보다 안정적이면 apply 모드에서 profile 업데이트 후보로 제시할 수 있다.
```

### 10.4 재검증 조건

다음 조건 중 하나에 해당하면 기존 profile만으로 충분하지 않다고 판단한다.

```text
- 모든 fallback이 실패한 경우
- user assisted mode가 반복되는 경우
- low confidence 후보만 반복적으로 발견되는 경우
- Confluence 구조/권한/endpoint 변경으로 기존 method가 더 이상 유효하지 않은 경우
```

이 경우 이 문서를 다시 dry-run으로 수행해 discovery strategy를 재검증한다. 재검증 결과가 안정적이면 사용자가 명시적으로 apply를 요청한 경우에만 profile을 갱신한다.

---

## 11. Strategy Profile 예시

아래 예시는 특정 주차 URL/ID를 포함하지 않는 형태만 보여준다.

```json
{
  "profile_type": "confluence_child_page_discovery_strategy",
  "profile_updated_at_kst": "2026-06-18 00:00 KST",
  "last_success_method": "confluence_rest_children",
  "confidence": "high",
  "strategy": {
    "input_type": "parent_page_url",
    "resolve_parent_page_id_at_runtime": true,
    "discovery_query_type": "children_then_descendants",
    "child_filter_rule": {
      "prefer_direct_children": true,
      "include_descendants_when_direct_children_empty": true,
      "use_title_pattern_if_provided": true,
      "use_label_if_provided": true,
      "exclude_non_page_links": true
    }
  },
  "fallback_methods": [
    "confluence_mcp_child_pages",
    "parent_body_link_extraction",
    "label_search",
    "title_pattern_search",
    "space_scoped_search",
    "fuzzy_search",
    "user_assisted_mode"
  ],
  "user_assisted_mode_required": false,
  "selected_strategy_reason": "Parent Page URL can be resolved at runtime and REST children/descendants provides reusable parent-child discovery without storing weekly page identifiers."
}
```

---

## 12. 사용자에게 바로 전달할 AI 실행 프롬프트

아래 본문을 복사해 AI에게 바로 실행 지시로 전달한다.

```text
현재 작업은 MCP 설치, MCP 설정, REST API 인증 설정, Python 패키지 구현 작업이 아니다.
Confluence read 수단은 이미 작동 가능하다고 가정한다.

목표:
Parent Page URL을 기준으로 이번 주 Confluence Child Page 후보를 실제로 찾고, 필요한 경우 이번 환경에서 재사용할 수 있는 Child Page discovery strategy/profile 방향을 정리한 뒤, 확정된 Child Page 본문을 읽어 5.3 Weekly Report Collection의 입력 draft를 생성해줘.

필수 입력:
- Parent Page URL: <여기에 Parent Page URL 입력>

선택 입력:
- Space Key: <알고 있으면 입력>
- Expected Title Pattern: <알고 있으면 입력>
- Expected Label: <알고 있으면 입력>
- Current Week: <알고 있으면 입력>
- Team/Owner Keyword: <알고 있으면 입력>

실행 모드:
- 기본은 dry-run이다.
- dry-run에서는 Confluence 조회와 결과 요약만 수행하고 profile 파일은 생성/수정하지 마라.
- 내가 명시적으로 apply를 요청한 경우에만 profile을 저장해라.
- apply 시 저장 경로는 %USERPROFILE%\artifacts\child_page_discovery_profile.json 이다.

수행 순서:
1. Parent Page URL이 접근 가능한지 확인한다 (200 OK vs 403/401/404/timeout 등 구분 기록).
2. Parent Page URL에서 pageId가 있으면 추출하고, 없으면 사용 가능한 Confluence read 수단으로 Parent Page ID를 resolve한다. (다중 결과 시 우선순위: space key 일치 > slug 일치 > ancestor path 일치 > 최신 수정)
3. REST API로 Parent의 direct children 조회를 시도한다 (실패 시 권한/endpoint/404 등 원인 구분).
4. direct children이 없거나 부족하면 REST descendants 조회를 시도한다.
5. 현재 세션에서 사용 가능한 MCP Confluence read 도구를 확인한다: (도구 목록 → 키워드 필터 → schema 검토: input 형식 확인 → 우선순위: parent_page_id > parent_page_url > parent_title+space_key). MCP 도구 이름은 환경마다 다를 수 있으므로 특정 함수명을 가정하지 마라.
6. Parent Page 본문을 조회해 본문 내 Confluence page 링크를 추출하고 Child 후보로 분류한다.
7. 후보 충분 기준 확인: high confidence 1개 이상? medium confidence 1개 이상? 아니면 fallback 진행.
8. 후보가 부족하면 label search, title pattern search, space-scoped search, fuzzy search를 순차 fallback으로 수행한다.
9. 자동 확정이 어렵지만 후보가 있으면 user assisted mode로 후보별 근거와 선택지를 제시한다.
10. 발견된 Child Page 후보 목록, confidence, 판단 근거, 사용한 discovery method를 요약한다 (§4.8 포맷 참조).
11. high/medium confidence로 확정된 Child Page 본문을 읽고 Markdown으로 취합한다.
12. 취합 원본 draft를 `%USERPROFILE%\artifacts\weekly_report_draft_<YYYYMMDD>_<HHMM>_KST.md`에 저장한다.
13. 별도의 `weekly_report_source_<YYYYMMDD>_<HHMM>_KST.json` 산출물은 생성하지 않는다.
14. profile에 저장할 strategy preview를 제시한다 (특정 주차 URL/ID 미포함 검증).

성공/실패 판정:
- Parent Page ID를 resolve하고 Parent-child 관계가 확인된 후보를 1개 이상 찾으면 high confidence로 판단한다.
- Parent 본문 링크 또는 ancestor/search 기반으로 후보를 찾았고 맥락 근거가 충분하면 medium confidence로 판단한다.
- fuzzy search 또는 user assisted mode로만 후보를 찾았거나 후보가 여러 개면 low confidence로 판단한다.
- Parent resolve 실패, 권한 실패, 모든 fallback 실패로 후보가 0개면 실패로 판단한다. 이 경우 "실패 원인" (권한/네트워크/데이터 부재 중 명확히), "시도된 method 목록", "필요 정보" 기록.

출력 요구:
- 실행 결과 포맷은 이 문서 §4.8 "결과 요약 및 포맷"을 참고해서 테이블과 구조화된 형식으로 출력해라.
- 실행 결과에는 발견된 Child 후보 URL/ID/title을 보여줘도 된다.
- 단, discovery strategy profile에는 특정 주차 Parent URL, Parent ID, Child URL 목록, Child ID 목록을 저장하지 마라.
- profile에는 재사용 가능한 방법만 저장해라.
- 기존 profile이 있으면 새 Parent Page URL 입력 후 profile.last_success_method를 먼저 적용해라.
- last_success_method가 실패하거나 confidence가 낮으면 profile.fallback_methods 순서대로 탐색해라.
- 기존 profile은 특정 URL/ID 캐시가 아니라 탐색 전략 캐시로 취급해라.
- 모든 fallback이 실패하거나 user assisted mode가 반복되면 이 문서를 다시 dry-run으로 수행해 discovery strategy를 재검증해라.
- last_success_method 또는 fallback으로 충분한 confidence의 Child 후보를 찾으면 본문을 읽어 `%USERPROFILE%\artifacts\weekly_report_draft_<YYYYMMDD>_<HHMM>_KST.md` 취합 원본 draft를 생성하고, 이 draft를 5_3_weekly_report_collection_py_package_prompt.md 입력으로 넘겨라.
- 별도의 `weekly_report_source_<YYYYMMDD>_<HHMM>_KST.json` 산출물은 생성하지 마라.
- dry-run이면 profile 저장 없이 preview만 출력해라.
- apply이면 %USERPROFILE%\artifacts\child_page_discovery_profile.json 에 저장하고, 저장 전 특정 주차 URL/ID가 포함되지 않았는지 검증해라.
- 후보가 0개면 실패로 판단하고, profile은 생성하지 마라. 대신 "실패 원인", "시도된 method", "필요 정보" 명확히 기록해라.
```

---

## 13. 완료 체크리스트

```text
- Parent Page URL을 필수 입력으로 받았는가?
- Parent URL 접근 상태 (200 vs 403/401/404/timeout)를 구분하고 기록했는가?
- Parent Page ID를 runtime에 resolve했는가? (다중 결과 시 우선순위 적용했는가?)
- REST children/descendants 조회를 시도했는가? (실패 원인별 처리 적용했는가?)
- MCP 조회 시:
  ① 현재 세션에서 사용 가능한 도구 목록과 schema를 확인했는가?
  ② 특정 도구명을 가정하지 않았는가?
  ③ input 형식별 우선순위를 적용했는가? (parent_page_id > url > title+space)
- Parent 본문 링크 추출을 시도했는가?
- fallback 진입 기준 (high/medium confidence 부족)을 확인했는가?
- label/title/fuzzy fallback을 시도했는가?
- user assisted mode의 조건과 출력이 명확한가?
- 결과를 §4.8 포맷(테이블/구조화)으로 출력했는가?
- 확정된 Child Page 본문을 읽고 취합 원본 draft를 생성했는가?
- draft 저장 경로가 `%USERPROFILE%\artifacts\weekly_report_draft_<YYYYMMDD>_<HHMM>_KST.md`인가?
- 별도의 `weekly_report_source_<YYYYMMDD>_<HHMM>_KST.json` 산출물을 생성하지 않았는가?
- 후보가 0개인 경우를 §5.3 기준으로 판단했는가?
- dry-run과 apply의 차이를 명확히 적용했는가?
- 기존 profile이 있는 경우 profile.last_success_method를 먼저 적용했는가?
- last_success_method 실패/low confidence 시 profile.fallback_methods 순서대로 탐색했는가?
- 기존 profile을 특정 URL/ID 캐시가 아니라 탐색 전략 캐시로 취급했는가?
- 모든 fallback 실패 또는 user assisted mode 반복 시 dry-run 재검증 조건을 명확히 적용했는가?
- 충분한 confidence의 Child 후보를 5_3_weekly_report_collection_py_package_prompt.md 입력으로 넘기는 흐름이 명확한가?
- 성공/실패/confidence 기준을 적용했는가?
- 실행 결과와 strategy profile 저장 원칙을 구분했는가?
- profile 저장 경로가 %USERPROFILE%\artifacts\child_page_discovery_profile.json 인가?
- profile에 특정 주차 URL/ID/Child 목록을 저장하지 않았는가?
- 출력에 "특정 주차 데이터 미포함" 검증 내용이 명확한가?
```
