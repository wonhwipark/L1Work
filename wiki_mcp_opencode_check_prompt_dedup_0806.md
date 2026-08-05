# OpenCode Wiki MCP 기술 확인 프롬프트 — 중복 제거본

아래 요청을 **Wiki MCP가 등록된 `opencode.json`을 실제로 사용하는 동일한 OpenCode 프로젝트/환경**에서 수행해줘.

## 0. 목적과 이미 확인된 사실

목적은 Wiki MCP를 `slte-knowledge-manager`의 `REFERENCE_ONLY` provider로 연결하기 위해 **실제 MCP 기술 계약만 확인**하는 것이다.

아래 내용은 이미 확인됐으므로 다시 조사하거나 장문으로 설명하지 마.

- Wiki MCP는 MCP 서버다.
- `opencode.json`으로 등록했다.
- 그룹 내부 자동 인증을 사용한다.
- semantic search, lookup, list, full fetch를 지원한다.
- 읽기 전용이다.
- 공식 Confluence HLD를 학습했다.
- source 경로를 반환한다.
- 지식은 설계 컨셉과 모듈·블록 책임 수준이다.
- 브랜치 delta, failure/recovery condition, correlation key는 제공하지 않는다.
- 응답은 생성형이며 반복 시 표현이 달라질 수 있다.
- 수동 재학습 방식이다.
- 별도 검수·승인 게이트가 없다.
- 응답이 느리거나 장문일 수 있다.
- Wiki 응답은 최종 판정이나 자동 코드 수정 근거로 사용하지 않는다.

이번 확인에서는 아래 기술 항목만 조사한다.

1. 실제 적용 중인 MCP 등록 정보
2. tool 이름과 `inputSchema`
3. search 응답 구조
4. 단일 문서 fetch 응답 구조
5. bounded response 지원 여부
6. raw JSON 확보 가능 여부
7. OpenCode 외부 Python 직접 호출 가능 여부
8. `slte-knowledge-manager` 연계 권장 방식

## 1. 답변 규칙

- 가능한 항목은 숫자 객관식으로 답한다.
- 객관식으로 답할 수 없는 항목은 **한 줄 단답형**으로 답한다.
- 장문 설명은 작성하지 않는다.
- 확인할 수 없는 내용은 `확인 불가`라고 답한다.
- 설정이나 Wiki 데이터를 수정하지 않는다.
- 인증정보와 사내 비밀정보는 반드시 마스킹한다.
- 다음 정보는 출력하지 않는다.
  - token
  - API key
  - cookie
  - password
  - client secret
  - Authorization header
  - 개인 계정 식별정보
- 원본 JSON은 요청된 항목만 제공한다.
- 응답이 길면 지정된 길이에서 자르고 `[TRUNCATED]`를 표시한다.

---

# A. 실제 MCP 등록 정보

## Q1. 적용 중인 `opencode.json` 경로

단답형:

```text
Q1: <절대경로 또는 확인 불가>
```

## Q2. Wiki MCP 등록 이름

단답형:

```text
Q2: <mcp server name>
```

## Q3. 등록 방식

1. local/stdio
2. remote HTTP
3. remote SSE
4. WebSocket
5. 기타
6. 확인 불가

## Q4. 활성 상태

1. 활성 및 정상 연결
2. 등록됐지만 연결 실패
3. 비활성
4. 확인 불가

## Q5. 마스킹한 MCP 설정

Wiki MCP에 해당하는 설정 블록만 JSON으로 출력한다.

출력 허용:

- type
- command
- args
- url
- enabled
- timeout
- environment variable의 **이름**

출력 금지:

- environment variable의 실제 비밀 값
- token
- cookie
- Authorization 값

형식:

```json
{
  "mcp": {
    "<server-name>": {
      "...": "..."
    }
  }
}
```

---

# B. 연결 및 Tool 목록

## Q6. 연결 상태

1. 정상 연결 및 tool 조회 가능
2. 연결은 되지만 tool 조회 불가
3. 인증 실패
4. endpoint 또는 command 실행 실패
5. timeout
6. 기타 오류
7. 확인 불가

오류가 있으면 아래만 단답형으로 작성한다.

```text
오류 코드:
오류 단계:
핵심 메시지:
```

## Q7. Tool 목록

Wiki MCP가 제공하는 모든 tool을 아래 표로 작성한다.

| tool name | 역할 번호 | 필수 입력 | 선택 입력 |
|---|---:|---|---|

역할 번호:

1. semantic search
2. keyword search
3. 문서 목록
4. 단일 문서 lookup
5. 문서 또는 section fetch
6. 파일 저장
7. 기타
8. 확인 불가

필수 입력과 선택 입력은 쉼표로 구분한 필드명만 작성한다.

## Q8. Tool `inputSchema`

각 tool의 `inputSchema` 원본 JSON을 출력한다.

규칙:

- description은 유지해도 된다.
- example 데이터는 생략해도 된다.
- 인증정보는 포함하지 않는다.
- schema가 길면 tool별 8,000자까지만 출력한다.

---

# C. Search 호출 확인

Wiki에 존재하는 L1 설계 키워드로 search를 1회 수행한다.

기본 질의:

```text
TxSwitchMngr SLTE Dual SIM
```

결과가 없으면 실제 존재하는 L1 설계 키워드 하나로 바꾼다.

## Q9. Search에 사용한 tool

단답형:

```text
Q9: <tool name>
```

## Q10. Search 입력 JSON

실제 호출에 사용한 입력 JSON을 그대로 출력한다.

## Q11. Search 결과 구조

1. source metadata + 짧은 snippet
2. source metadata + 생성형 요약
3. 장문 생성형 답변 중심
4. 원문 전체 중심
5. 혼합
6. 확인 불가

## Q12. Search 응답 제한 지원

1. 결과 건수와 문자 수 모두 제한 가능
2. 결과 건수만 제한 가능
3. 문자 수만 제한 가능
4. 제한 필드 없음
5. 확인 불가

## Q13. Search 메타데이터

아래 형식으로 숫자만 답한다.

```text
source_path: 1=있음 / 2=없음 / 3=확인 불가
page_id: 1=있음 / 2=없음 / 3=확인 불가
page_version: 1=있음 / 2=없음 / 3=확인 불가
modified_at: 1=있음 / 2=없음 / 3=확인 불가
stable_source_id: 1=있음 / 2=없음 / 3=확인 불가
```

## Q14. Search 호출 결과 요약

단답형으로 작성한다.

```text
성공 여부:
응답 시간:
결과 수:
응답 크기:
```

## Q15. Search 원본 응답 샘플

원본 JSON을 최대 3건만 출력한다.

- 전체 4,000자 이하
- 초과분은 `[TRUNCATED]`
- source path는 유지
- 사내 비밀정보는 마스킹

---

# D. 단일 문서 Fetch 확인

Search 결과 중 1건을 선택해 상세 조회를 1회 수행한다.

## Q16. Fetch에 사용한 tool

단답형:

```text
Q16: <tool name>
```

## Q17. Fetch 입력 JSON

실제 호출에 사용한 입력 JSON을 그대로 출력한다.

## Q18. Fetch 범위 제한

1. section과 최대 문자 수 모두 지정 가능
2. section만 지정 가능
3. 최대 문자 수 또는 page size만 지정 가능
4. 단일 문서만 선택 가능하며 크기 제한 없음
5. 항상 전체 또는 장문 반환
6. 확인 불가

## Q19. Fetch 결과 메타데이터

아래 형식으로 숫자만 답한다.

```text
source_path: 1=있음 / 2=없음 / 3=확인 불가
page_id: 1=있음 / 2=없음 / 3=확인 불가
page_version: 1=있음 / 2=없음 / 3=확인 불가
modified_at: 1=있음 / 2=없음 / 3=확인 불가
section_identity: 1=있음 / 2=없음 / 3=확인 불가
raw_content_field: 1=있음 / 2=없음 / 3=확인 불가
generated_summary_field: 1=있음 / 2=없음 / 3=확인 불가
```

## Q20. Fetch 호출 결과 요약

단답형:

```text
성공 여부:
응답 시간:
응답 크기:
선택한 source:
```

## Q21. Fetch 원본 응답 샘플

원본 JSON을 최대 3,000자까지만 출력한다.

- 초과분은 `[TRUNCATED]`
- source path는 유지
- 민감정보는 마스킹

---

# E. Snapshot 및 Python 연계 가능성

## Q22. Raw JSON 확보 방식

1. OpenCode 화면 또는 응답에서 원본 JSON 확보 가능
2. OpenCode가 구조화 응답을 제공하지만 일부 가공됨
3. Markdown 또는 자연어만 확보 가능
4. 확인 불가

## Q23. MCP가 직접 파일 저장을 지원하는가

1. 지원
2. 미지원
3. 확인 불가

지원하면 단답형으로 작성한다.

```text
파일 저장 tool:
출력 경로 지정 가능 여부:
저장 형식:
```

## Q24. OpenCode 외부 Python에서 직접 호출 가능한가

1. HTTP endpoint 직접 호출 가능
2. stdio command 직접 실행 가능
3. HTTP와 stdio 모두 가능
4. OpenCode 내부 호출만 가능
5. 확인 불가

근거는 한 줄 단답형으로 작성한다.

```text
근거: <command/url 노출 여부, 인증 의존성, 정책상 제약>
```

## Q25. 인증이 OpenCode 세션에 종속되는가

1. 종속됨
2. 종속되지 않음
3. 확인 불가

## Q26. 동일 응답 digest 생성 가능성

1. raw JSON 전체로 SHA-256 생성 가능
2. 일부 가공된 payload로만 생성 가능
3. 자연어 응답만 가능
4. 확인 불가

---

# F. `slte-knowledge-manager` 연계 판단

## Q27. 권장 연계 방식

1. OpenCode가 Wiki MCP를 호출하고 Python action에 JSON 전달
2. Python action이 MCP endpoint를 직접 호출
3. Python action이 MCP stdio command를 직접 실행
4. MCP가 파일 저장 후 Python action이 import
5. 정보 부족으로 구현 보류

## Q28. 권장 방식의 핵심 근거

최대 3줄 단답형:

```text
1.
2.
3.
```

## Q29. 추가로 필요한 정보

없으면 `없음`, 있으면 최대 5개 단답형으로 작성한다.

---

# G. 변경 여부 확인

아래 형식으로 숫자만 답한다.

```text
설정 파일 수정: 1=안 함 / 2=함
Wiki 데이터 수정: 1=안 함 / 2=함
스킬 실행: 1=안 함 / 2=읽기 전용 / 3=상태 변경
인증정보 노출: 1=없음 / 2=가능성 있음
추가 파일 생성: 1=결과 MD만 / 2=기타 파일도 생성
```

---

# H. 최종 산출물

결과를 하나의 Markdown 파일로 저장한다.

파일명:

```text
wiki_mcp_opencode_probe_result.md
```

문서 순서:

```text
1. 요약
2. MCP 등록 정보
3. 연결 상태
4. Tool 목록
5. Tool inputSchema
6. Search 호출 결과
7. Fetch 호출 결과
8. Snapshot·Python 연계 가능성
9. 권장 연계 방식
10. 변경·보안 확인
11. 확인 불가 항목
```

불필요한 배경 설명, Wiki와 Knowledge Manager의 역할 비교, 이미 확인된 기능 설명은 반복하지 마.
