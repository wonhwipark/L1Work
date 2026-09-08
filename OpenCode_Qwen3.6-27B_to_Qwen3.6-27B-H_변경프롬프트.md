# OpenCode LLM 모델 변경 프롬프트
## 목표
현재 OpenCode에서 사용 중인 `qwen3.6-27b` 계열 모델 설정을 찾아
`Qwen3.6-27B-H`로 안전하게 변경한다.

> 중요: 모델의 provider prefix와 실제 model ID 구조는 환경마다 다를 수 있으므로
> `provider/model` 전체 문자열을 임의로 추정하지 말고 현재 설정과 등록된 모델을 먼저 확인한다.

---

## 실행 프롬프트

너는 현재 Linux 개발환경의 OpenCode 설정을 점검하고 수정하는 작업을 수행한다.

### 최종 목표

현재 OpenCode의 기본 LLM이 `qwen3.6-27b` 또는 대소문자만 다른 동일 모델을 사용하고 있다면,
이를 **`Qwen3.6-27B-H`** 모델로 변경한다.

단, provider 이름이나 API endpoint 등 기존 연결 설정은 임의로 변경하지 않는다.

---

# 1. 작업 원칙

다음 규칙을 반드시 지켜라.

1. 설정 파일 위치를 추측해서 바로 수정하지 않는다.
2. 현재 OpenCode가 실제로 참조할 수 있는 모든 설정 위치를 먼저 조사한다.
3. 기존 설정 파일은 수정 전에 백업한다.
4. `provider/model` 형식에서 provider 부분은 기존 값을 우선 유지한다.
5. `Qwen3.6-27B-H`가 현재 provider에 실제 등록되어 있는지 확인한다.
6. 실제 model ID가 `Qwen3.6-27B-H`와 철자/대소문자가 다르면 임의로 변경하지 말고 발견된 ID를 보고한다.
7. API key, token, password 등 인증정보를 화면에 출력하지 않는다.
8. 다른 OpenCode 설정, skill 설정, MCP 설정, permission 설정은 변경하지 않는다.
9. 실패하거나 불확실한 경우 억지로 수정하지 말고 `STOP` 후 원인을 보고한다.
10. 질문을 반복하지 말고 가능한 범위까지 자동으로 조사한 뒤 결과를 보고한다.

---

# 2. 현재 설정 탐색

먼저 다음 항목을 확인한다.

## 2.1 OpenCode 관련 환경변수

다음을 확인한다.

```bash
env | grep -E '^OPENCODE_' || true
```

특히 다음 값을 확인한다.

- `OPENCODE_CONFIG`
- `OPENCODE_MODEL`

인증정보가 포함된 환경변수 값은 출력하지 않는다.

---

## 2.2 전역 설정

다음 위치를 확인한다.

```bash
ls -la ~/.config/opencode/ 2>/dev/null || true
```

후보:

```text
~/.config/opencode/opencode.json
~/.config/opencode/opencode.jsonc
```

---

## 2.3 프로젝트 설정

현재 작업 디렉터리부터 상위 디렉터리까지 다음 파일을 조사한다.

```text
opencode.json
opencode.jsonc
.opencode/opencode.json
.opencode/opencode.jsonc
```

가능하면 다음과 같이 탐색하되 시스템 전체를 무분별하게 검색하지 않는다.

```bash
pwd
find .. -maxdepth 5 \
  \( -name opencode.json -o -name opencode.jsonc \) \
  -print 2>/dev/null
```

---

# 3. 현재 모델 설정 확인

찾은 설정 파일에서 다음 항목을 조사한다.

```text
model
small_model
provider
providers
provider.models
```

또한 다음 문자열을 검색한다.

```bash
grep -RniE \
  'qwen3[._-]?6|qwen.*27b|27b.*qwen|OPENCODE_MODEL' \
  ~/.config/opencode \
  . \
  2>/dev/null | head -200
```

단, 출력 내용에 token/API key/password가 포함될 가능성이 있으면 해당 값은 반드시 마스킹한다.

현재 모델을 아래 형식으로 내부적으로 정리한다.

```text
CONFIG_SOURCE=<실제 적용 설정 파일 또는 환경변수>
CURRENT_PROVIDER=<provider>
CURRENT_MODEL_ID=<model id>
CURRENT_FULL_MODEL=<provider/model>
```

---

# 4. 설정 우선순위 확인

단순히 전역 설정만 수정하지 않는다.

다음 항목 중 더 높은 우선순위가 현재 모델을 덮어쓰고 있는지 확인한다.

1. 실행 시 `--model` 또는 `-m`
2. `OPENCODE_CONFIG`로 지정된 별도 설정
3. 프로젝트 `opencode.json(c)`
4. 프로젝트 `.opencode/opencode.json(c)`
5. 전역 `~/.config/opencode/opencode.json(c)`
6. `OPENCODE_MODEL` 또는 config의 `{env:OPENCODE_MODEL}` 참조
7. OpenCode 세션에서 명시적으로 선택된 모델

현재 설정을 변경해도 상위 우선순위 때문에 효과가 없을 것으로 판단되면
그 사실을 먼저 식별한다.

---

# 5. `Qwen3.6-27B-H` 사용 가능 여부 확인

현재 provider에서 `Qwen3.6-27B-H` 모델이 등록되어 있는지 확인한다.

가능하면 OpenCode의 모델 목록 기능 또는 현재 provider 설정을 이용한다.

예:

```text
/models
```

또는 config의 다음 영역을 확인한다.

```text
provider.<provider-id>.models
providers.<provider-id>.models
```

### 판정

#### CASE A — 정확한 모델 ID 존재

예:

```text
Qwen3.6-27B-H
```

또는 provider가 포함되어:

```text
<existing-provider>/Qwen3.6-27B-H
```

이면 변경 가능하다.

#### CASE B — 유사 모델만 존재

예:

```text
qwen3.6-27b-h
Qwen3.6-27B-H-Instruct
Qwen3.6-27B-H-AWQ
```

이 경우 임의 선택하지 않는다.

`STOP`하고 발견된 후보를 보고한다.

#### CASE C — 모델이 존재하지 않음

설정을 수정하지 않는다.

다음만 보고한다.

```text
TARGET_MODEL_NOT_REGISTERED
```

그리고 현재 provider에서 발견 가능한 Qwen 3.6 27B 계열 모델 목록을 출력한다.

---

# 6. 변경 전 백업

수정 대상이 확정되면 원본 파일을 반드시 백업한다.

예:

```bash
cp -a <config-file> <config-file>.bak_before_Qwen3.6-27B-H
```

동일한 백업 파일이 이미 존재하면 덮어쓰지 말고 timestamp를 붙인다.

예:

```text
opencode.json.bak_before_Qwen3.6-27B-H_YYYYMMDD_HHMMSS
```

---

# 7. 모델 변경

## CASE 1 — config의 `model` 직접 지정

현재 값이 예를 들어:

```json
{
  "model": "myprovider/qwen3.6-27b"
}
```

이고 동일 provider에 목표 모델이 등록되어 있다면:

```json
{
  "model": "myprovider/Qwen3.6-27B-H"
}
```

형태로 변경한다.

### 중요

`myprovider`는 예시이다.

실제 환경의 provider ID를 그대로 유지한다.

---

## CASE 2 — `OPENCODE_MODEL` 참조

config가 다음과 같다면:

```json
{
  "model": "{env:OPENCODE_MODEL}"
}
```

config를 직접 바꾸지 않는다.

먼저 `OPENCODE_MODEL`이 어디에서 정의되는지 찾는다.

후보:

```text
~/.bashrc
~/.bash_profile
~/.profile
~/.zshrc
project .env
실행 wrapper script
systemd Environment
OpenCode 실행 script
```

예를 들어 실제 설정이:

```bash
export OPENCODE_MODEL="myprovider/qwen3.6-27b"
```

이면 목표 모델이 등록되어 있음을 확인한 뒤:

```bash
export OPENCODE_MODEL="myprovider/Qwen3.6-27B-H"
```

로 변경한다.

단, `.env` 또는 shell profile의 다른 항목은 건드리지 않는다.

---

## CASE 3 — custom provider의 model alias

현재 config가 다음과 유사할 수 있다.

```json
{
  "model": "corp/qwen3.6-27b",
  "provider": {
    "corp": {
      "models": {
        "qwen3.6-27b": {
          "modelID": "..."
        }
      }
    }
  }
}
```

이 경우 단순 문자열 치환하지 않는다.

`Qwen3.6-27B-H`가 실제 backend model ID 또는 alias로 등록되어 있는지 확인하고
OpenCode schema와 현재 provider 구조를 유지한 상태에서 최소 변경한다.

기존 모델 정의를 삭제하지 않는다.

---

# 8. JSON / JSONC 유효성 검증

수정 후 JSON이면 syntax를 검증한다.

예:

```bash
python3 -m json.tool <config-file> >/dev/null
```

JSONC이면 주석 때문에 `python -m json.tool`을 강제로 사용하지 않는다.

사용 가능한 OpenCode 자체 validation 또는 JSONC parser가 있다면 그것을 사용한다.

검증 도구가 없으면 최소한 수정한 영역을 다시 읽어 구조가 훼손되지 않았는지 확인한다.

---

# 9. 변경 결과 재확인

수정 후 다음을 다시 확인한다.

```text
EXPECTED_MODEL=<provider>/Qwen3.6-27B-H
```

그리고 설정 파일 또는 환경변수에서 기존:

```text
qwen3.6-27b
```

가 기본 `model`로 계속 남아 있지 않은지 확인한다.

단, provider의 모델 catalog에 기존 모델이 등록된 채 남아 있는 것은 정상이다.
기존 모델 definition 자체를 삭제할 필요는 없다.

---

# 10. OpenCode 실제 선택 모델 검증

가능한 경우 OpenCode를 새 세션으로 실행하거나
모델 목록/상태 확인 기능을 이용해 실제 선택된 모델을 검증한다.

기존 세션에서 모델이 명시적으로 선택되어 있다면
config 변경만으로 해당 기존 세션의 모델이 바뀌지 않을 수 있으므로
**새 세션 기준 기본 모델**도 확인한다.

검증 결과를 다음 중 하나로 판정한다.

```text
PASS
PASS_CONFIG_ONLY
FAIL
STOP
```

의미:

- `PASS`
  - config 변경 완료
  - 실제 OpenCode 모델도 `Qwen3.6-27B-H` 확인

- `PASS_CONFIG_ONLY`
  - config 변경 완료
  - 실제 런타임 검증 수단이 없어 config까지만 확인

- `FAIL`
  - 변경 또는 검증 실패
  - 백업으로 복구 필요

- `STOP`
  - target model 미등록/모델 ID 불확실/설정 출처 불확실 등으로 안전하게 중단

---

# 11. 실패 시 복구

수정 후 OpenCode 실행 오류 또는 모델 연결 오류가 발생하면
임의로 추가 수정하지 않는다.

백업 파일을 이용해 원래 설정으로 복구한다.

복구 후 다음 상태로 보고한다.

```text
ROLLBACK_COMPLETED
```

---

# 12. 최종 보고 형식

작업 완료 후 설명을 길게 늘어놓지 말고 반드시 아래 형식으로 보고한다.

```text
[OpenCode Model Change Result]

RESULT:
  PASS | PASS_CONFIG_ONLY | FAIL | STOP

CONFIG_SOURCE:
  <실제 수정된 파일 또는 환경변수>

BACKUP:
  <백업 파일 경로 또는 N/A>

BEFORE:
  <provider>/<기존 model id>

AFTER:
  <provider>/Qwen3.6-27B-H

TARGET_REGISTERED:
  YES | NO | UNKNOWN

RUNTIME_VERIFIED:
  YES | NO

OVERRIDE_FOUND:
  NONE | <발견된 override>

CHANGED_FILES:
  - <path>

UNCHANGED:
  - API endpoint
  - authentication
  - provider
  - skills
  - MCP
  - permissions

NOTES:
  <필요한 경우에만 1~5줄>
```

---

# 완료 조건

다음 조건을 모두 만족해야 완료이다.

- 기존 설정 위치 확인
- 실제 적용 우선순위 확인
- `Qwen3.6-27B-H` 등록 여부 확인
- 기존 provider 유지
- 수정 전 backup 생성
- 최소 범위 수정
- config syntax/구조 검증
- 가능한 경우 OpenCode 실제 모델 검증
- 최종 결과를 정해진 형식으로 보고

**Target 모델의 실제 등록 여부가 확인되지 않으면 절대 임의로 모델명을 만들어 적용하지 마라.**
