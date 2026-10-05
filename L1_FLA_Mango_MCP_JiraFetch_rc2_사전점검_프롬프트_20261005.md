# L1-FLA Mango MCP Jira Fetch 실패 사전점검 프롬프트

## 목적

L1-FLA v0.3.39에서 Jira fetch가 아래 증상으로 실패한다.

- `mango_mcp failed rc=2`
- `fetch_jira_mcp.py` 스크립트가 현재 L1-FLA 패키지에 존재하지 않음
- L1-FLA는 외부 SSOT `~/l1sw-local-environment/l1-fla/jira/jira_access.json`의
  `providers.mango_mcp.command`를 실행하는 구조임

**이번 점검의 목적은 수정이 아니라 원인 확정이다.**
코드/설정/파일을 변경하지 말고 READ-ONLY로 조사한다.

최종 답변은 반드시 아래 객관식 형식으로만 정리한다.
추측하지 말고, 확인 불가능하면 `0=모름`을 선택한다.

---

## 조사 대상

가능하면 아래를 실제 파일/설정 기준으로 확인한다.

1. `~/l1sw-local-environment/l1-fla/jira/jira_access.json`
2. `~/l1sw-private-skills/l1-fla/`
3. 현재 설치된 L1-FLA의 `scripts/l1-fla.py`
4. 사용자 HOME 및 기존/백업/이전 스킬 폴더에서 `fetch_jira_mcp.py` 존재 여부
5. OpenCode/Mango MCP에서 Jira issue를 조회하는 실제 지원 방식
6. 실패 당시 command와 stderr/stdout
7. 가능하다면 `mango_mcp failed rc=2` 직전 실제 subprocess command

**파일 수정, install, package update, permission 변경, Jira write는 금지한다.**

---

# Q1. 현재 jira_access.json의 Mango command가 fetch_jira_mcp.py를 직접 참조하는가?

1. 예. `providers.mango_mcp.command`가 `fetch_jira_mcp.py`를 직접 실행한다.
2. 아니오. 다른 command/launcher를 실행한다.
3. command는 비어 있고 환경변수 `L1_FLA_MANGO_JIRA_COMMAND`를 사용한다.
4. jira_access.json 자체가 없거나 읽을 수 없다.
0. 모름

선택 후 아래를 그대로 출력:

`JIRA_COMMAND=<비밀정보 제거 후 token array 또는 command>`
`JIRA_ACCESS_PATH=<실제 경로>`

---

# Q2. rc=2의 직접 원인은 무엇인가?

1. Python이 `fetch_jira_mcp.py` 파일을 찾지 못해 종료한 rc=2
2. `fetch_jira_mcp.py`는 존재하지만 argparse/인자 오류로 rc=2
3. Mango MCP 자체가 rc=2를 반환
4. OpenCode/MCP 권한 또는 외부 경로 접근 실패
5. 다른 원인
0. 모름

근거:
`RC2_EVIDENCE=<stderr 또는 로그 핵심 1~3줄>`

---

# Q3. fetch_jira_mcp.py가 이 PC의 다른 위치에 존재하는가?

HOME과 아래 계열을 검색하되 읽기만 한다.

- `~/l1sw-private-skills/`
- `~/l1sw-skills/`
- `~/l1sw-local-environment/`
- 기존 L1-FLA backup/archive가 있다면 해당 경로
- OpenCode 관련 사용자 설정 경로

1. 존재한다. 과거 L1-FLA 또는 별도 helper에 있음
2. 존재한다. 다른 스킬/공용 helper에 있음
3. 존재하지 않는다.
0. 검색 범위상 확정 불가

존재하면:
`FETCH_SCRIPT_PATH=<실제 경로>`
`FETCH_SCRIPT_OWNER=<l1-fla / 공용 / 다른스킬 / 기타>`

---

# Q4. 과거 정상 동작 시 fetch_jira_mcp.py는 어떤 방식으로 배포됐는가?

1. L1-FLA ZIP/package에 포함됐었다.
2. installer가 설치 중 생성/복사했다.
3. `~/l1sw-local-environment/...` 같은 외부 영구영역에 별도 존재했다.
4. 다른 공용 스킬 또는 MCP helper가 제공했다.
5. 실제로는 fetch_jira_mcp.py를 사용한 적 없고 현재 설정에 잘못 남아 있다.
0. 모름

가능하면 근거 파일/버전:
`PAST_SOURCE=<경로 또는 버전>`

---

# Q5. 현재 사내 Mango MCP에서 Jira issue READ를 수행하는 올바른 방식은 무엇인가?

1. Python helper(`fetch_jira_mcp.py`)가 OpenCode/Mango MCP를 호출해야 한다.
2. 별도 사내 CLI/command를 직접 호출하면 된다.
3. OpenCode 세션에서 Mango MCP tool/action을 호출해야 하며 일반 subprocess만으로는 직접 MCP 호출이 불가하다.
4. 다른 공용 스킬을 통해 호출해야 한다.
5. 현재 환경에서는 Mango MCP Jira read 자체가 불가하다.
0. 모름

실제 지원되는 인터페이스가 확인되면:
`MANGO_JIRA_INTERFACE=<command 또는 tool/action 이름>`
`MANGO_JIRA_TRANSPORT=<python_helper / cli / opencode_mcp / skill / 기타>`

---

# Q6. fetch_jira_mcp.py가 필요하다면 입력 contract는 무엇이어야 하는가?

1. positional Jira key: `fetch_jira_mcp.py SOC-123`
2. `--issue-key SOC-123`
3. stdin JSON
4. 다른 형식
5. helper 자체가 불필요하다.
0. 모름

`EXPECTED_INPUT=<실제 확인된 형식>`

---

# Q7. L1-FLA가 기대하는 fetch 결과 JSON과 현재 Mango 결과는 호환되는가?

L1-FLA `fetch_jira()`가 실제로 파싱하는 구조와 Mango MCP 결과를 비교한다.

1. 그대로 호환된다.
2. wrapper 1단계만 벗기면 호환된다.
3. field mapping 변환이 필요하다.
4. 현재 Mango 결과를 확인할 수 없다.
0. 모름

필요 시:
`RESULT_MAPPING=<예: result.issue -> issue / data -> issue 등 간단히>`

---

# Q8. Remote Link 조회도 별도 helper가 필요한가?

현재 `providers.mango_mcp.remote_links` 설정도 확인한다.

1. Jira issue helper와 같은 helper/action으로 지원 가능
2. 별도 remote-link helper/action이 필요
3. Remote Link는 현재 비활성/미사용이므로 이번 수정 대상 아님
4. 설정은 존재하지만 잘못돼 있음
0. 모름

`REMOTE_LINK_STATUS=<configured/unconfigured/disabled/unknown>`

---

# Q9. 이번 L1-FLA 수정 방향은 어느 것이 가장 안전한가?

1. `fetch_jira_mcp.py`를 L1-FLA package에 복원하고 installer가 canonical 경로를 자동 등록
2. 기존 외부 helper를 재사용하고 package에는 넣지 않으며 경로 검증만 추가
3. Python helper를 제거하고 실제 Mango CLI command를 직접 SSOT에 등록
4. OpenCode+Mango MCP 호출 adapter를 L1-FLA에 새로 포함
5. 현재 `jira_access.json`의 stale command만 정정하면 되고 L1-FLA 코드 수정은 불필요
0. 추가 확인 필요

---

# Q10. 재발 방지를 위해 installer/preflight에서 무엇을 반드시 검사해야 하는가?

1. 등록된 command의 실행파일/스크립트 존재 여부만 검사
2. 존재 여부 + `{issue_key}` placeholder + 실행 가능 여부 검사
3. 2번 + read-only probe 1회까지 수행
4. 별도 검사 불필요
0. 모름

---

# 최종 답변 형식

설명문을 길게 쓰지 말고 아래 블록으로 끝낸다.

```text
Q1=<0~4>
JIRA_COMMAND=<...>
JIRA_ACCESS_PATH=<...>

Q2=<0~5>
RC2_EVIDENCE=<...>

Q3=<0~3>
FETCH_SCRIPT_PATH=<...>
FETCH_SCRIPT_OWNER=<...>

Q4=<0~5>
PAST_SOURCE=<...>

Q5=<0~5>
MANGO_JIRA_INTERFACE=<...>
MANGO_JIRA_TRANSPORT=<...>

Q6=<0~5>
EXPECTED_INPUT=<...>

Q7=<0~4>
RESULT_MAPPING=<...>

Q8=<0~4>
REMOTE_LINK_STATUS=<...>

Q9=<0~5>

Q10=<0~4>

CONFIDENCE=<HIGH/MEDIUM/LOW>
FIRST_BLOCKER=<가장 먼저 고쳐야 할 1개>
RECOMMENDED_FIX=<Q9 선택 내용을 한 줄로>
```

## 판정 원칙

- 실제 파일/로그/설정 근거가 있으면 우선한다.
- `fetch_jira_mcp.py`를 임의로 새로 작성하거나 복구하지 않는다.
- 기존 설정을 변경하지 않는다.
- Jira에 write하지 않는다.
- Mango MCP 호출 방식이 확인되지 않았는데 추측해서 adapter를 제안하지 않는다.
- **이번 점검은 L1-FLA Jira fetch 실패 원인 확인만 한다. 다른 기능 개선 제안은 하지 않는다.**
