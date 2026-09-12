# L1-FLA 무인 실행 / OpenCode Headless 호출 구조 검증 프롬프트

## 목적

현재 `l1-fla v0.3.24`의 리눅스 무인 실행 구조에 대해 아래 주장이 실제 코드 기준으로 맞는지 확인한다.

검증 대상 주장:

1. L1-FLA 무인 실행 프레임워크는 CLI 기반이다.
2. FLA 내부에서 AI 분석이 필요한 시점에는 OpenCode를 headless CLI로 호출할 수 있다.
3. 무인 모델 provider 우선순위가 아래 순서인지 확인한다.

```text
OpenCode -> Claude Code -> Qwen Code
```

4. OpenCode 선택 시 실제 실행 명령이 아래와 유사한지 확인한다.

```bash
opencode run --auto ...
```

5. OpenCode 호출 실패 시 Claude Code / Qwen Code로 fallback 하는지 확인한다.
6. 위 provider 선택/호출이 `l1-fla-auto.py`, `l1-fla.py`, 별도 runner/provider 모듈 중 어디에서 구현되는지 확인한다.
7. `skillsilent`가 이 AI provider 호출 경로에서 필수인지, 선택인지, 전혀 사용되지 않는지 확인한다.

---

# 중요 원칙

- 추정하지 말고 **실제 코드 근거만으로 판단**한다.
- README/SKILL.md 설명보다 **실제 Python/Shell 코드 구현을 우선**한다.
- 문서와 코드가 다르면 반드시 `문서와 구현 불일치`로 표시한다.
- 단순 문자열 검색 결과만으로 결론 내리지 말고, 실제 호출 경로까지 추적한다.
- wrapper 함수가 있다면 최종 `subprocess`, `exec`, `shell`, provider dispatch 지점까지 확인한다.
- 테스트/mock 코드와 production 실행 코드를 구분한다.

---

# 1. 패키지/소스 위치 확인

먼저 현재 설치 또는 압축 해제된 `l1-fla v0.3.24`의 root 경로를 확인한다.

다음 파일/폴더를 우선 탐색한다.

```text
SKILL.md
README.md
scripts/
l1-fla.py
l1-fla-auto.py
provider*
runner*
model*
agent*
orchestr*
```

파일명이 다르면 유사 역할의 파일을 찾아도 된다.

---

# 2. OpenCode 관련 전체 검색

아래 키워드를 전체 소스에서 검색한다.

```text
opencode
opencode run
--auto
claude
claude code
qwen
qwen code
provider
fallback
headless
subprocess
Popen
run(
exec
shell
skillsilent
```

가능하면 아래처럼 사용한다.

```bash
grep -RniE "opencode|claude|qwen|provider|fallback|headless|skillsilent|subprocess|Popen|--auto" .
```

`rg`가 있으면:

```bash
rg -n -i "opencode|claude|qwen|provider|fallback|headless|skillsilent|subprocess|Popen|--auto"
```

---

# 3. Provider 우선순위 검증

다음 내용을 코드에서 확인한다.

## 확인 항목

- provider 후보 리스트가 어디에 정의되어 있는가?
- 기본 provider가 무엇인가?
- 자동 선택 순서가 존재하는가?
- 아래 순서가 실제 코드에 명시되어 있는가?

```text
OpenCode -> Claude Code -> Qwen Code
```

- 환경변수/설정파일로 순서가 변경될 수 있는가?
- 특정 provider를 강제로 지정할 수 있는가?
- OS별로 순서가 달라지는가?
- Linux에서만 별도 처리되는가?

## 반드시 코드 근거 제시

예:

```text
파일: scripts/xxx.py
함수: select_provider()
라인: 120-148

providers = ["opencode", "claude", "qwen"]
```

실제 코드가 다르면 실제 내용을 그대로 설명한다.

---

# 4. OpenCode 실제 호출 명령 검증

OpenCode가 선택되었을 때 최종 실행 명령을 추적한다.

다음을 반드시 확인한다.

- 실제 executable 이름
- 실제 subcommand
- `--auto` 사용 여부
- prompt 전달 방식
- stdin / 파일 / argument 중 무엇을 사용하는지
- timeout 존재 여부
- exit code 처리
- stdout/stderr capture 방식
- JSON/text parsing 방식

특히 아래 주장을 확인한다.

```text
opencode run --auto ...
```

판정은 반드시 다음 중 하나로 한다.

```text
[CONFIRMED]
[PARTIALLY_CONFIRMED]
[NOT_CONFIRMED]
[CONTRADICTED]
```

예:

```text
[PARTIALLY_CONFIRMED]

실제 호출:
opencode run --format json ...

따라서 `opencode run`은 맞지만 `--auto`는 사용하지 않는다.
```

---

# 5. Fallback 동작 검증

OpenCode가 실패했을 때 실제로 다음 provider로 넘어가는지 확인한다.

확인할 실패 조건:

- binary 미설치
- command not found
- timeout
- non-zero exit code
- 빈 응답
- invalid JSON
- parsing 실패
- model invocation 실패

아래와 같은 실제 흐름이 있는지 확인한다.

```text
OpenCode 실패
   ↓
Claude Code
   ↓
Qwen Code
```

단순 provider 목록만 있고 fallback loop가 없다면 `fallback 미구현`으로 판정한다.

---

# 6. 무인 실행 경로에서 실제 호출 지점 추적

리눅스 무인 실행 시 시작점부터 AI provider 호출까지 실제 call chain을 추적한다.

예상 형태:

```text
scheduler
  -> l1-fla-auto.py
  -> l1-fla.py / runner
  -> issue-analyzer
  -> provider selector
  -> opencode CLI
```

하지만 위 구조를 전제로 하지 말고 실제 코드로 작성한다.

최종적으로 아래 형식으로 표현한다.

```text
[실제 호출 경로]

<entry point>
  -> <function/file>
  -> <function/file>
  -> <AI decision point>
  -> <provider selector>
  -> <actual subprocess command>
```

각 단계마다 파일명과 함수명을 적는다.

---

# 7. Skillsilent 개입 여부 확인

다음을 구분해서 확인한다.

## A. FLA 자체 실행

```text
scheduler -> l1-fla-auto.py
```

에서 `skillsilent`가 필요한가?

## B. AI provider 호출

```text
FLA -> OpenCode
```

에서 `skillsilent`가 필요한가?

## C. Child skill 호출

예:

```text
FLA -> issue-analyzer
FLA -> code-analyzer
FLA -> 기타 skill
```

에서 `skillsilent`가 사용되는가?

최종적으로 아래처럼 구분한다.

```text
FLA 무인 entry point:
- skillsilent: 필수 / 선택 / 미사용

OpenCode provider 호출:
- skillsilent: 필수 / 선택 / 미사용

Child skill 호출:
- skillsilent: 필수 / 선택 / 일부만 사용 / 미사용
```

---

# 8. SKILL.md / README와 실제 구현 비교

문서에 아래와 같은 표현이 있는지 확인한다.

```text
skillsilent required
direct python forbidden
opencode
headless
provider
auto
fallback
```

그리고 실제 코드와 비교한다.

아래 표를 작성한다.

| 항목 | 문서 설명 | 실제 코드 | 일치 여부 |
|---|---|---|---|
| OpenCode 지원 | | | |
| provider 순서 | | | |
| `opencode run --auto` | | | |
| fallback | | | |
| skillsilent 필요성 | | | |
| Linux 무인 실행 경로 | | | |

---

# 9. 최종 판정

아래 5개 질문에 각각 하나만 선택한다.

## Q1. Linux 무인 FLA에서 OpenCode를 headless CLI로 실제 호출하는가?

- A. 확인됨
- B. 일부 경로에서만 확인됨
- C. 구현은 있으나 현재 기본 경로에서는 사용 안 함
- D. 확인되지 않음

## Q2. Provider 자동 우선순위가 `OpenCode -> Claude Code -> Qwen Code`인가?

- A. 정확히 맞음
- B. 일부만 맞음
- C. 설정에 따라 달라짐
- D. 그런 우선순위 없음

## Q3. OpenCode 실제 명령이 `opencode run --auto ...` 형태인가?

- A. 정확히 맞음
- B. `opencode run`은 맞지만 option이 다름
- C. 다른 명령을 사용함
- D. OpenCode subprocess 호출 자체가 없음

## Q4. OpenCode 실패 시 자동 fallback이 존재하는가?

- A. Claude -> Qwen까지 실제 fallback
- B. 일부 provider까지만 fallback
- C. provider 목록만 있고 fallback은 없음
- D. fallback 구조 없음

## Q5. Skillsilent는 OpenCode provider 실행에 필수인가?

- A. 필수
- B. 선택
- C. 직접 호출 경로와 Skillsilent 경로가 모두 존재
- D. 미사용

---

# 10. 최종 보고 형식

최종 답변은 아래 형식으로 작성한다.

```markdown
# L1-FLA OpenCode Headless 실행 구조 검증 결과

## 1. 결론

- Linux 무인 entry point:
- AI provider:
- Provider 우선순위:
- OpenCode 실제 명령:
- Fallback:
- Skillsilent 필요성:

## 2. 객관식 판정

- Q1:
- Q2:
- Q3:
- Q4:
- Q5:

## 3. 실제 호출 경로

<call chain>

## 4. 코드 근거

### 근거 1
- 파일:
- 함수:
- 라인:
- 확인 내용:

### 근거 2
...

## 5. 문서와 구현 차이

| 항목 | 문서 | 구현 | 조치 필요 |
|---|---|---|---|

## 6. 수정 필요 여부

- [ ] 수정 불필요
- [ ] SKILL.md만 수정
- [ ] 실행 코드 수정
- [ ] provider/fallback 구조 수정
- [ ] skillsilent 정책 수정

### 수정이 필요하다면 최소 수정안
...
```

---

# 핵심 주의사항

이번 검토의 목적은 OpenCode를 사용할 수 있다는 일반론을 확인하는 것이 아니다.

반드시 **현재 설치된 L1-FLA v0.3.24 실제 코드에서**

1. 어디에서 provider를 선택하고,
2. 어떤 순서로 선택하며,
3. 어떤 CLI 명령을 실행하고,
4. 실패 시 어디로 fallback하며,
5. skillsilent가 그 경로에 실제 개입하는지

를 코드 근거로 확인해야 한다.

근거가 없으면 반드시 `확인 불가`라고 답한다.
