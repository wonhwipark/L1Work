# MCP 영속 설정 프롬프트 — `.mcp.json` 프로젝트 스코프 (Jira + Confluence)

> 목적: 새 세션마다 Jira/Confluence MCP 연결이 끊겨 손보는 문제를 없앤다.
> 방법: `RCA_standalone/` 루트에 `.mcp.json` 을 두어, 이 폴더를 여는 한
>        모든 새 세션이 같은 MCP 설정을 자동으로 읽게 한다(1순위 해법).
>
> 왜 user 스코프가 아니라 프로젝트 `.mcp.json` 인가:
>   - `claude mcp add --scope user` 가 실제로는 프로젝트 경로에 묶여 새 폴더에서
>     사라지는 버그가 보고됨. `.mcp.json` 은 명시적 파일이라 휘발되지 않는다.
>   - P0~P6 가 어차피 RCA_standalone 을 작업 루트로 열도록 설계됨 → 같은 루트에 두면 항상 붙는다.
>
> ⚠ 중요: 사내는 Confluence/Jira 가 **Server/Data Center** 일 가능성이 높다.
>   - Server/DC 는 보통 **PAT(Personal Access Token)** 인증을 쓴다.
>   - 메모리에 적힌 `@aashari/...` 패키지는 Cloud 전용일 수 있다(Server 미지원).
>   따라서 아래 프롬프트는 "실제 설치된 패키지/엔드포인트를 먼저 조사" 한 뒤
>   거기에 맞는 키 구조로 `.mcp.json` 을 쓰도록 했다. 임의로 키를 지어내지 않는다.
>
> ⚠ OS / 절대경로 정책 (Windows·Linux 공용):
>   - 이 프롬프트들은 Windows 와 Linux/macOS 모두에서 동작한다.
>   - **절대경로(.mymcp 위치 등)는 Claude/Roo 가 임의로 정하지 않는다.**
>     반드시 사용자에게 물어본 값을 사용한다(각 프롬프트의 [0] 단계 참조).
>   - OS 의존 항목은 실행 환경에 맞춰 자동 분기한다:
>     · 환경변수 영속:  Windows = `setx`,  Linux/macOS = `~/.bashrc`/`~/.zshrc` 의 `export`
>     · REST 헬퍼:      Windows = `.ps1`,  Linux/macOS = `.sh`
>     · 경로 구분자:    Windows = `\`,     Linux/macOS = `/`
>   - 양쪽 OS 가 같은 .mcp.json 을 공유한다면 절대경로 대신
>     `${HOME}` / `%USERPROFILE%` / `${ENV_VAR}` 참조를 권장한다(사용자에게 확인).

---

## 공통 0단계 — 자격증명 준비 (사람, 1회)

`.mcp.json` 에 들어갈 값을 미리 준비한다. 토큰은 절대 이 문서에 적지 말고 손에만 둔다.

| 항목 | Cloud | Server/Data Center |
|---|---|---|
| Base URL | `https://<회사>.atlassian.net` | `https://confluence.사내도메인` / `https://jira.사내도메인` |
| 인증 | API Token | **PAT (Personal Access Token)** |
| 사용자 식별 | 이메일 | **User ID (whpark)** 또는 PAT 단독 |

> 사내 자체호스팅이면 Server/DC 칸을 따른다. Confluence User ID 는 whpark.

---

## A. Claude Code 용 프롬프트

```text
@HANDOFF_5.5.md

목표: 이 RCA_standalone 폴더 루트에 .mcp.json 을 만들어서,
새 세션마다 Jira/Confluence MCP 연결이 끊기는 문제를 영구히 없애줘.
임의로 환경변수 키를 지어내지 말고, 아래 조사 결과에 맞는 키 구조로 작성해줘.

[0] 환경·경로 확인 (먼저 나에게 질문)
  아래를 나에게 물어보고, 답을 받은 뒤에 [1]로 진행해줘. 임의로 정하지 마.
  a. 지금 실행 OS 가 Windows 인지 Linux/macOS 인지 (자동 감지되면 감지값을 말하고 확인만 받아).
  b. .mymcp(또는 MCP 설정 보관) 디렉토리의 **절대경로**.
     예시만 제시하고 내 입력을 기다려:
       - Windows 예: C:\Users\whpark\.mymcp\claude
       - Linux 예  : /home/whpark/.mymcp/claude
  c. 토큰을 담을 환경변수 이름을 내가 지정할지, 네가 제안할지.
     (예: CONFLUENCE_PAT, JIRA_PAT — 내가 다른 이름을 주면 그걸 써.)
  d. Windows·Linux 양쪽에서 같은 .mcp.json 을 공유할 계획인지.
     (그렇다면 절대경로 대신 ${HOME}/%USERPROFILE%/${ENV_VAR} 참조를 쓸지 함께 확인해.)
  → 이 답들을 이후 모든 단계에서 그대로 사용해. 경로를 추측하지 마.

[1] 현재 상태 조사 (수정 전에 먼저 보고)
  1. `claude mcp list` 를 실행해서 지금 등록된 MCP 서버와 연결 상태를 보여줘.
  2. 이미 등록돼 있다면 각 서버를 `claude mcp get <name>` 으로 조사해서
     - 어떤 command/args/env 키를 쓰는지
     - Cloud 용 키(ATLASSIAN_SITE_NAME, ATLASSIAN_USER_EMAIL, ATLASSIAN_API_TOKEN)인지
     - Server/DC 용 키(CONFLUENCE_BASE_URL/JIRA_URL + PAT/PERSONAL_TOKEN)인지
     판별해서 표로 보고해줘.
  3. 기존 설정이 어디 저장돼 있는지 찾아줘:
     - ~/.claude.json 의 projects.<경로>.mcpServers (경로 한정 = 새 폴더서 사라지는 원인)
     - [0]b 에서 받은 .mymcp 절대경로 아래 설정 파일
     이 둘의 내용을 비교해서, 어느 쪽이 실제로 동작하는 설정인지 알려줘.

[2] 패키지/엔드포인트 판별
  - Confluence/Jira 가 Cloud 인지 Server/Data Center 인지 판별해줘.
    (사내 자체호스팅 URL 이면 Server/DC. 토큰이 PAT 면 Server/DC.)
  - 그 환경을 지원하는 MCP 패키지가 무엇인지 기존 설정에서 확인해줘.
    Server/DC 인데 Cloud 전용 패키지(@aashari Cloud 전용 등)를 쓰고 있으면,
    그게 끊김의 근본 원인일 수 있으니 명시적으로 경고해줘.

[3] .mcp.json 작성 (RCA_standalone 루트)
  - 위 조사로 확정된 command/args/env 키 구조를 그대로 사용해서
    RCA_standalone/.mcp.json 을 만들어줘.
  - 토큰 같은 비밀값은 .mcp.json 에 직접 넣지 말고 ${ENV_VAR} 참조로 써줘.
    예: "CONFLUENCE_API_TOKEN": "${CONFLUENCE_PAT}"  (변수명은 [0]c 에서 받은 값)
    그리고 그 ENV_VAR 들을 영속 등록하는 명령을 OS 에 맞게 제시해줘(실행은 내가 한다):
      · Windows      : setx CONFLUENCE_PAT "..."   (새 터미널부터 적용)
      · Linux/macOS  : ~/.bashrc 또는 ~/.zshrc 에 export CONFLUENCE_PAT="..." 추가 후 source
    → 이렇게 하면 .mcp.json 은 git/p4 에 올려도 안전하고, 토큰만 OS에 영속된다.
  - .mymcp 등 절대경로가 필요하면 [0]b 에서 받은 경로를 그대로 써. 추측 금지.
    [0]d 에서 "양쪽 OS 공유" 라고 했으면 절대경로 대신 ${HOME}/%USERPROFILE% 참조로 써.
  - 구조 예시(실제 키는 [2] 결과를 따른다. 이건 형태 참고용일 뿐):
    {
      "mcpServers": {
        "confluence": {
          "command": "npx",
          "args": ["-y", "<조사로 확인된 패키지>"],
          "env": { "<확인된 키>": "${...}" }
        },
        "jira": {
          "command": "...",
          "args": ["..."],
          "env": { "<확인된 키>": "${...}" }
        }
      }
    }

[4] 안전장치
  - .mcp.json 에 토큰 평문이 들어가지 않았는지 다시 확인해줘.
  - .gitignore / p4 ignore 에 토큰이 든 .env 류가 있으면 제외되게 안내해줘.
  - 기존에 projects.<경로>.mcpServers 에 중복 등록된 게 있으면,
    충돌하지 않도록 정리 방법을 알려줘(자동 삭제 말고 명령만 제시).

[5] 검증 절차 제시 (내가 실행)
  - 환경변수 영속 등록(Windows setx / Linux export) 후 "새 터미널"에서 RCA_standalone 을 다시 열고
    `claude mcp list` → 둘 다 connected 인지
    `/mcp` → Jira/Confluence 가 보이는지, Authenticate 필요 없는지
    확인하는 순서를 알려줘.
  - 그리고 진짜 새 세션에서도 유지되는지 확인할 1줄 테스트(예: Confluence 스페이스 목록,
    Jira 내 이슈 1건 조회)를 제시해줘.

먼저 [1][2] 조사 결과를 표로 보여주고 멈춰줘. 내가 확인하면 [3]으로 진행한다.
```

---

## B. Roo Code 용 프롬프트

> Roo 는 글로벌 MCP 설정과 워크스페이스(`.roo/mcp.json`) 설정이 분리돼 있다.
> 폴더 이동 시 끊긴다면 워크스페이스 설정이 비었거나 글로벌을 덮어쓰는 경우다.
> Claude Code 의 `.mcp.json` 과 같은 자격증명을 쓰되, Roo 전용 위치에 둔다.

```text
목표: Roo Code 에서 Jira/Confluence MCP 가 새 세션·폴더 이동 후에도 유지되게 설정해줘.
임의로 키를 지어내지 말고, 현재 동작 중인 설정을 먼저 조사한 뒤 거기에 맞춰줘.

[0] 환경·경로 확인 (먼저 나에게 질문)
  아래를 나에게 물어보고, 답을 받은 뒤에 [1]로 진행해줘. 임의로 정하지 마.
  a. 실행 OS (Windows / Linux / macOS). 자동 감지되면 감지값 확인만 받아.
  b. Roo MCP 설정 보관 디렉토리의 **절대경로**.
     예시만 제시하고 내 입력을 기다려:
       - Windows 예: C:\Users\whpark\.mymcp\roo
       - Linux 예  : /home/whpark/.mymcp/roo
  c. Windows·Linux 양쪽에서 같은 워크스페이스를 공유하는지.
     (그렇다면 .roo/mcp.json 안의 경로는 절대경로 대신
      ${HOME}/%USERPROFILE%/${ENV_VAR} 참조로 쓸지 확인해.)
  → 이 답들을 이후 모든 단계에서 그대로 사용해. 경로를 추측하지 마.

[1] 현재 Roo MCP 설정 위치 확인
  - Roo 글로벌 MCP 설정 파일(보통 VSCode 전역 설정 영역의 mcp_settings.json)과
    워크스페이스 .roo/mcp.json 둘 다 찾아줘.
  - [0]b 에서 받은 Roo .mymcp 절대경로 아래 설정도 확인해줘.
    각각 어떤 Jira/Confluence 서버가 어떤 env 키로 등록돼 있는지 표로 보고해줘.
  - 셋 중 실제로 로드되는 게 어느 것인지, 충돌(같은 서버 다른 설정)이 있는지 알려줘.

[2] Cloud vs Server/DC 판별
  - 등록된 URL/토큰 형태로 Cloud 인지 Server/Data Center 인지 판별해줘.
  - Server/DC 인데 Cloud 전용 패키지를 쓰고 있으면 경고해줘(끊김 원인 가능성).

[3] 워크스페이스 .roo/mcp.json 작성
  - RCA_standalone/.roo/mcp.json 에 Jira/Confluence 서버를
    [2] 에서 확정한 패키지·키 구조로 작성해줘.
  - Claude Code 와 동일한 자격증명을 쓰되, 토큰은 평문 금지.
    Roo 가 ${ENV_VAR} 참조를 지원하면 그걸 쓰고, 지원 안 하면
    별도 비공개 파일(.mymcp/roo/) 참조 방식으로 분리해줘.
  - [0]b 에서 받은 .mymcp\roo 경로를 가리키는 참조가 상대경로면 절대경로로 바꿔줘
    (상대경로는 폴더 이동 시 깨진다). [0]c 가 "양쪽 OS 공유" 면 절대경로 대신
    ${HOME}/%USERPROFILE% 참조로 써줘.

[4] 글로벌 vs 워크스페이스 우선순위 정리
  - 워크스페이스 설정이 글로벌을 의도대로 덮어쓰는지 확인해줘.
  - 중복/충돌 서버 정의가 있으면 정리 방법을 알려줘(자동 삭제 말고 안내만).

[5] 검증
  - 설정 후 Roo 를 재시작하고, RCA_standalone 을 새로 열었을 때
    Jira/Confluence 도구가 도구 목록에 뜨는지 확인하는 절차를 알려줘.
  - 새 세션에서 Confluence 스페이스 목록 / Jira 이슈 1건 조회로 연결을 확인할
    1줄 테스트를 제시해줘.

먼저 [1][2] 조사 결과를 표로 보여주고 멈춰줘. 확인 후 [3]으로 진행한다.
```

---

## C. REST API 폴백 (MCP 가 막혔을 때)

> 사내 정책으로 MCP 가 불안정하면, Claude Code/Roo 가 직접 REST 를 호출하는 방식이 더 안정적일 수 있다.
> 토큰은 OS 환경변수에만 두고, 스크립트는 그걸 읽기만 한다.

```text
목표: Jira/Confluence REST 를 환경변수 토큰으로 호출하는 헬퍼를 RCA_standalone/scripts/ 에 만들어줘.
먼저 나에게 물어봐: 실행 OS(Windows/Linux/macOS)와, 토큰 환경변수 이름.
  → OS 에 맞춰 Windows 면 .ps1, Linux/macOS 면 .sh 로 만들어. 경로는 추측하지 마.
조건:
  - 토큰은 코드/문서에 적지 말고 환경변수(예: CONFLUENCE_PAT, JIRA_PAT)에서만 읽어.
  - Server/DC 면 PAT Bearer 인증, Cloud 면 Basic(email:token) 인증으로 분기해줘.
  - 먼저 어떤 환경인지 [HANDOFF/기존 설정]에서 판별하고, 그에 맞는 1줄을 만들어줘.
  - 동작 확인용 read-only 호출(스페이스 목록 / 내 이슈 조회)부터 만들어줘. write 는 별도 승인.
  - 환경변수 미설정 시 친절히 안내하고 종료하게 해줘.
출력:
  - scripts/atlassian_rest_probe.ps1 (또는 .sh) — 연결 확인용
  - 사용법을 scripts/README.md 에 한 섹션 추가
토큰 평문이 어디에도 남지 않는지 마지막에 확인해줘.
```

---

## 한 줄 요약

```text
원인:  user 스코프 휘발 버그 + Server/DC인데 Cloud 패키지/이메일 사용 가능성
1순위: RCA_standalone/.mcp.json (프로젝트 스코프) + 토큰은 OS 환경변수(${})
공용:  Windows·Linux 모두 동작. 절대경로·환경변수영속(setx/export)·헬퍼확장(.ps1/.sh)은 OS별 자동 분기
경로:  .mymcp 등 절대경로는 추측 금지 — [0] 단계에서 사용자에게 물어본 값만 사용
핵심:  키를 지어내지 말고 "현재 설정/엔드포인트를 조사 → 그 구조로" 작성
검증:  새 터미널·새 세션에서 RCA_standalone 열고 `claude mcp list` / `/mcp` 둘 다 connected
```
