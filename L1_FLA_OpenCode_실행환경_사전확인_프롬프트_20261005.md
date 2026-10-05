# L1-FLA OpenCode 실행환경 사전 확인 프롬프트

## 목적

L1-FLA를 수정하기 전에 사내 OpenCode 환경에서 아래 두 문제의 **실제 원인과 올바른 수정 방향**을 확인한다.

1. L1-FLA가 OpenCode에서 실행될 때 기대 모델인 **`Code LLM - Max`** 대신 **`Qwen3.8-27B LiteLLM`**을 사용하거나 해당 provider 오류로 중단되는 문제
2. OpenCode에서 L1-FLA 실행 시 **프로젝트 디렉터리 외부 파일 접근 권한 필요** 팝업이 발생하는 문제

이 결과는 이후 L1-FLA 수정의 SSOT로 사용한다.

---

## 중요 지시

- **코드/설정 파일을 수정하지 말 것.** 진단과 확인만 수행한다.
- L1-FLA 실제 분석 작업(Jira 다운로드/로그 분석)을 새로 시작하지 말 것.
- 가능하면 `--help`, 설정 조회, 경로/환경 확인 등 **read-only 명령**만 사용한다.
- 추측으로 답하지 말고 실제 OpenCode CLI/설정/로그 근거를 확인한다.
- 답변은 아래 **숫자 객관식 형식**을 반드시 지킨다.
- 모르면 `0`을 선택한다.
- 객관식 번호 외 설명은 `근거:` 영역에만 짧게 적는다.

---

# 1. 현재 L1-FLA 코드에서 확인된 사실

현재 L1-FLA v0.3.38에는 다음 구조가 있다.

### A. Provider 우선순위

```python
MODEL_PROVIDER_SPECS = (
    {"id": "opencode", "label": "OpenCode", ...},
    {"id": "claude", "label": "Claude Code", ...},
    {"id": "qwen", "label": "Qwen Code", ...},
)
```

`model_runner` 기본값:

```text
strategy = fallback
preferred = ""
providers = []
```

따라서 별도 설정이 없으면 설치된 provider를 자동 탐지하고 OpenCode → Claude Code → Qwen Code 순으로 후보가 될 수 있다.

### B. OpenCode 호출 시 모델 지정 없음

Delegated analyzer preflight:

```text
opencode run --auto <prompt>
```

일반 model provider invocation:

```text
opencode run --auto --file <context> --file <template> <instruction>
```

현재 코드에는 `Code LLM - Max` 또는 OpenCode `--model`에 해당하는 명시적 모델 지정이 없다.

### C. Provider fallback

OpenCode 실행이 infrastructure/skill-unavailable 유형으로 실패하면 다음 headless provider를 시도할 수 있는 구조다.

### D. OpenCode 실행 경로

OpenCode에서 L1-FLA top-level은 SkillSilent를 사용하지 않고 public launcher를 직접 호출한다.

L1-FLA가 사용하는 주요 프로젝트 외부 경로 예:

```text
~/l1sw-private-skills/l1-fla/
~/l1sw-local-environment/l1-fla/
```

실제 로그/output/download root 설정에 따라 추가 외부 경로를 사용할 수 있다.

---

# 2. 확인 작업

아래 순서로 read-only 확인한다.

## Step A. OpenCode 모델 선택 방식 확인

가능한 범위에서 다음을 확인한다.

```text
opencode --help
opencode run --help
```

그리고 현재 사내 OpenCode 설정에서 다음을 확인한다.

- `Code LLM - Max`가 실제로 존재하는가?
- UI 표시명과 CLI model ID가 같은가?
- CLI에서 모델을 명시하는 공식 옵션은 무엇인가?
- 예: `--model`, `-m`, profile/config 지정 등
- `opencode run --auto`에서 모델을 생략하면 어떤 모델이 선택되는가?
- 현재 `Qwen3.8-27B LiteLLM`이 선택되는 근거가 default/current model 때문인가?

**실제 분석 요청은 실행하지 않는다.** 모델 목록/설정 조회가 지원될 경우 read-only로 확인한다.

## Step B. Code LLM - Max의 headless 사용 가능 여부

다음을 확인한다.

- `Code LLM - Max`가 OpenCode interactive UI 전용인지
- `opencode run` 같은 headless/non-interactive 실행에서도 지정 가능한지
- 새벽 무인 실행에서도 같은 모델을 지정할 수 있는지
- 사용자 세션/UI 선택 상태에 의존하지 않고 model ID로 고정 가능한지

## Step C. Provider fallback 정책 검토

현재 L1-FLA는 `strategy=fallback`이다.

사용자 요구는 다음과 같다.

> L1-FLA의 OpenCode 분석은 `Code LLM - Max`로 동작하길 기대한다. 다른 모델로 조용히 바뀌어 분석되는 것은 원하지 않는다.

이 요구를 기준으로 다음 중 어떤 정책이 안전한지 판단한다.

- Code LLM - Max 실패 시 즉시 BLOCKED
- 같은 OpenCode 내 다른 모델 fallback
- Claude/Qwen provider까지 자동 fallback

## Step D. 프로젝트 외부 경로 권한 확인

현재 OpenCode에서 다음과 같은 팝업이 발생한다.

> 프로젝트 디렉터리 외부의 파일에 액세스하려면 권한 필요

다음을 확인한다.

- 이 팝업이 OpenCode sandbox/permission 정책에서 발생하는가?
- 어느 실제 경로 접근에서 최초 발생하는가?
- 해당 경로를 영구/지속 allowlist 할 수 있는 공식 설정이 있는가?
- 설정이 있다면 사용자 단위인지 프로젝트 단위인지
- 새벽 무인 실행에서는 이 팝업 없이 접근 가능한가?
- OpenCode headless 실행이 interactive 권한 승인을 요구할 가능성이 있는가?

**권한을 임의로 전체 HOME에 허용하지 말 것.** 필요한 최소 경로만 확인한다.

## Step E. L1-FLA 수정 범위 판단

사내 환경 확인 결과를 기준으로 다음 수정 방향이 맞는지 판단한다.

후보 수정안:

```text
1. OpenCode용 model_id 설정 추가
2. Code LLM - Max의 실제 CLI model ID를 설정값으로 저장
3. OpenCode invocation에 model 선택 인자 명시
4. preflight에서도 동일 model ID의 사용 가능 여부 확인
5. unattended 실행 시 지정 모델이 없거나 실패하면 fail-closed
6. 실제 사용 provider/model을 run metadata와 보고서에 기록
7. OpenCode 외부경로 권한 상태를 preflight/doctor에서 사전 점검
8. 필요한 최소 외부경로를 사용자에게 명확히 표시
9. 권한 미확보 상태에서는 분석 시작 전 BLOCKED 처리
10. 새벽 Scheduler/Job-list 동작은 기존 구조를 최대한 유지
```

---

# 3. 답변 — 숫자 객관식

아래 형식을 **그대로 사용**한다.

## Q1. 현재 Qwen3.8-27B LiteLLM이 선택되는 주원인은?

1. L1-FLA가 OpenCode CLI 호출 시 모델을 명시하지 않아 OpenCode 기본/current model이 사용됨
2. L1-FLA 코드가 Qwen3.8-27B LiteLLM을 명시적으로 지정하고 있음
3. Code LLM - Max 자체가 OpenCode headless에서 지원되지 않음
4. L1-FLA provider 선택이 OpenCode가 아니라 Qwen CLI로 넘어간 것임
0. 확인 불가

**답:**

---

## Q2. Code LLM - Max의 실제 CLI model ID 확인 여부는?

1. 확인됨 — 아래 `MODEL_ID=`에 정확한 ID 기입
2. UI 표시명만 확인되고 CLI model ID는 확인되지 않음
3. Code LLM - Max가 현재 환경에 존재하지 않음
4. CLI model ID 개념 없이 별도 profile/config로 선택해야 함
0. 확인 불가

**답:**

```text
MODEL_ID=
```

**근거:**

---

## Q3. OpenCode에서 특정 모델을 headless로 지정하는 공식 방법은?

1. `--model <model-id>`
2. `-m <model-id>`
3. CLI 인자가 아니라 profile/config/environment 설정으로 지정
4. 기타 — 근거에 실제 syntax 기록
5. headless에서는 모델 지정 불가
0. 확인 불가

**답:**

**실제 syntax:**

```text

```

---

## Q4. Code LLM - Max를 `opencode run` 기반 무인/headless 실행에서 사용할 수 있는가?

1. 가능하며 model ID를 명시하면 됨
2. 가능하지만 별도 profile/config가 필요함
3. interactive UI에서만 가능하여 무인 실행에는 사용할 수 없음
4. 현재 사내 권한/인증 때문에 headless에서는 사용할 수 없음
0. 확인 불가

**답:**

---

## Q5. 사용자 요구 기준으로 가장 안전한 model fallback 정책은?

1. **Code LLM - Max only** — 실패하면 즉시 BLOCKED, 다른 모델 자동 사용 금지
2. Code LLM - Max 실패 시 같은 OpenCode 내 다른 모델 허용
3. OpenCode 실패 시 Claude Code → Qwen Code까지 기존 fallback 유지
4. interactive 실행만 single, 새벽 무인은 fallback 유지
0. 판단 불가

**답:**

---

## Q6. L1-FLA preflight에서 모델까지 검증해야 하는가?

1. provider 실행파일 + 지정 model ID 사용 가능 여부를 모두 검증해야 함
2. provider 실행파일 존재만 확인하면 충분함
3. model 확인은 실제 run 단계에서만 해야 함
0. 판단 불가

**답:**

---

## Q7. 프로젝트 외부 파일 권한 팝업의 원인은?

1. OpenCode 자체의 프로젝트 외부 경로 sandbox/permission 정책
2. L1-FLA/SkillSilent 자체 permission 정책
3. OS 파일 권한(ACL/소유권) 문제
4. 보안 솔루션 또는 별도 사내 wrapper 정책
5. 복합 원인 — 근거에 설명
0. 확인 불가

**답:**

---

## Q8. OpenCode에서 필요한 외부 경로를 지속적으로 허용하는 공식 방법은?

1. 사용자 단위 persistent allowlist 가능
2. 프로젝트 단위 persistent allowlist 가능
3. 세션별 승인만 가능
4. 현재 버전에서는 persistent allowlist 기능 없음
5. OpenCode가 아니라 사내 wrapper/정책 설정에서 허용해야 함
0. 확인 불가

**답:**

**확인된 설정 위치/키:**

```text

```

---

## Q9. 현재 환경에서 L1-FLA가 최소한으로 필요로 하는 프로젝트 외부 접근 범위는?

1. `~/l1sw-private-skills/l1-fla/**` + `~/l1sw-local-environment/l1-fla/**`만으로 충분
2. 위 2개 + 별도 log/download/output root가 필요
3. HOME 전체 접근이 필요
4. 프로젝트 외부 접근 없이 구조 변경 가능
0. 확인 불가

**답:**

**실제 추가 필요 경로가 있으면 기록:**

```text
PATH_1=
PATH_2=
PATH_3=
```

---

## Q10. 다음 L1-FLA 수정 방향으로 가장 적절한 것은?

1. **권장안 전체 적용**
   - OpenCode model ID 명시
   - Code LLM - Max fail-closed
   - preflight model 검증
   - provider/model metadata 기록
   - 외부 경로 permission 사전 진단
   - 새벽 자동 파이프라인 구조 유지
2. 모델 ID 명시만 최소 수정
3. 외부경로 permission 처리만 수정
4. 기존 fallback 구조를 유지하면서 Code LLM - Max를 preferred로만 추가
5. 현재 스킬 수정 전에 OpenCode/사내 환경 추가 조사가 더 필요
0. 판단 불가

**답:**

---

# 4. 최종 출력 형식

반드시 마지막에 아래 블록을 출력한다.

```text
=== L1-FLA OPENCode PRECHECK RESULT ===
Q1=<0~4>
Q2=<0~4>
MODEL_ID=<확인된 실제 ID 또는 UNKNOWN>
Q3=<0~5>
MODEL_SYNTAX=<확인된 실제 syntax 또는 UNKNOWN>
Q4=<0~4>
Q5=<0~4>
Q6=<0~3>
Q7=<0~5>
Q8=<0~5>
PERMISSION_CONFIG=<설정 위치/키 또는 UNKNOWN>
Q9=<0~4>
EXTERNAL_PATHS=<확인된 최소 경로, ; 구분 또는 UNKNOWN>
Q10=<0~5>
CONFIDENCE=<HIGH|MEDIUM|LOW>
FIRST_BLOCKER=<없으면 NONE, 있으면 가장 먼저 해결할 1개>
=== END ===
```

## 판정 원칙

- `CONFIDENCE=HIGH`: OpenCode help/config/log 등 직접 근거로 model ID, 호출 syntax, permission 정책까지 확인
- `CONFIDENCE=MEDIUM`: 핵심 원인은 확인했지만 model ID 또는 permission persistence 중 하나가 미확인
- `CONFIDENCE=LOW`: 추정 위주이거나 실제 OpenCode 설정을 확인하지 못함

`Q2=1`, `Q3=1/2/3/4`, `Q4=1/2`, `Q5=1`, `Q6=1`이 확인되면 L1-FLA에서 **Code LLM - Max 고정 + fail-closed + preflight 모델 검증** 방향으로 수정할 근거가 충분하다.

`Q7~Q9`가 확정되면 OpenCode 프로젝트 외부 경로 권한 문제도 같은 버전에서 함께 수정/안내할 수 있다.
