# L1-FLA OpenCode Headless 실행구조 검증 프롬프트 — 짧은 답변 강제형

## 목적

현재 설치된 `l1-fla v0.3.24` 실제 코드를 확인하여 아래 5개 항목만 판정한다.

검증 대상:
1. Linux 무인 FLA에서 OpenCode를 headless CLI로 실제 호출하는가?
2. Provider 우선순위가 `OpenCode -> Claude Code -> Qwen Code`인가?
3. OpenCode 실제 호출 명령이 `opencode run --auto ...` 형태인가?
4. OpenCode 실패 시 Claude/Qwen으로 자동 fallback 하는가?
5. OpenCode provider 실행에 `skillsilent`가 필수인가?

---

## 검증 원칙

- README/SKILL.md 설명보다 **실제 코드 구현을 우선**한다.
- 추정 금지.
- 실제 production 실행 경로만 본다.
- 테스트/mock 코드는 근거에서 제외한다.
- 최종 subprocess/CLI 호출 지점까지 확인한다.
- 답변은 반드시 아래의 **초단문 형식**으로만 작성한다.
- 긴 설명, 배경 설명, 코드 전문 출력 금지.

---

## 확인할 키워드

소스 전체에서 최소한 아래를 확인한다.

```text
opencode
opencode run
--auto
claude
qwen
provider
fallback
subprocess
Popen
skillsilent
l1-fla-auto
```

필요하면:

```bash
rg -n -i "opencode|claude|qwen|provider|fallback|skillsilent|subprocess|Popen|--auto|l1-fla-auto"
```

---

# 질문

## Q1. Linux 무인 FLA에서 OpenCode headless CLI를 실제 호출하는가?

- A = 호출함
- B = 일부 경로에서만 호출
- C = 구현은 있으나 기본 무인 경로에서는 미사용
- D = 호출하지 않음
- X = 코드 근거 부족

## Q2. Provider 자동 우선순위가 `OpenCode -> Claude Code -> Qwen Code`인가?

- A = 정확히 맞음
- B = 일부만 맞음
- C = 설정에 따라 달라짐
- D = 그런 자동 우선순위 없음
- X = 코드 근거 부족

## Q3. OpenCode 실제 명령이 `opencode run --auto ...`인가?

- A = 정확히 맞음
- B = `opencode run`은 맞지만 option이 다름
- C = 다른 OpenCode 명령 사용
- D = OpenCode subprocess 호출 없음
- X = 코드 근거 부족

## Q4. OpenCode 실패 시 자동 fallback이 있는가?

- A = Claude -> Qwen까지 fallback
- B = 일부 provider까지만 fallback
- C = provider 목록은 있으나 자동 fallback 없음
- D = fallback 구조 없음
- X = 코드 근거 부족

## Q5. OpenCode 실행에 skillsilent가 필수인가?

- A = 필수
- B = 선택
- C = 직접 호출/skillsilent 경로 둘 다 존재
- D = 미사용
- X = 코드 근거 부족

---

# 답변 형식 — 반드시 이것만 출력

아래 형식을 그대로 사용한다.

```text
Q1: A/B/C/D/X
Q2: A/B/C/D/X
Q3: A/B/C/D/X
Q4: A/B/C/D/X
Q5: A/B/C/D/X

E1: <파일명>:<함수명> - OpenCode 호출 근거
E2: <파일명>:<함수명> - provider 순서 근거
E3: <파일명>:<함수명> - 실제 명령 근거
E4: <파일명>:<함수명> - fallback 근거
E5: <파일명>:<함수명> - skillsilent 근거

DOC: OK / MISMATCH / UNKNOWN
FIX: NONE / SKILL_MD / CODE / BOTH
```

## 답변 길이 제한

- 각 `E1~E5`는 **한 줄**
- 각 근거는 **최대 80자**
- 전체 답변은 **15줄 이내**
- 코드 전문 금지
- 장문 설명 금지
- 추가 의견 금지
- 근거를 찾지 못하면 `없음`이라고 적는다.

---

# 판정 예시

```text
Q1: A
Q2: C
Q3: B
Q4: B
Q5: D

E1: model_runner.py:run_opencode - subprocess로 opencode run 호출
E2: provider.py:select_provider - config 순서 사용
E3: model_runner.py:run_opencode - --format json 사용, --auto 없음
E4: provider.py:invoke - OpenCode 실패 후 Claude만 재시도
E5: model_runner.py:run_opencode - skillsilent 없이 직접 subprocess 호출

DOC: MISMATCH
FIX: SKILL_MD
```

---

## 중요

사용자가 다른 ChatGPT 창으로 결과를 직접 전달해야 하므로,
**15줄을 초과하는 설명은 작성하지 않는다.**

필요한 판단은 위 Q1~Q5와 E1~E5만으로 끝낸다.
