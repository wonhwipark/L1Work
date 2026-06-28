# STEP 1 — 리눅스(사내) 정보 추출 프롬프트

> 이 패키지에서 **사람이 프롬프트로 직접 실행하는 유일한 단계**다.
> 이유: 리눅스 사내 PC는 윈도우와 다른 머신이라 스크립트로 원격 추출이 불가.
> 나머지(설치/전환/검증)는 전부 스크립트가 자동 처리한다.

## 사용법

1. 아래 코드블록을 **리눅스 사내 PC의 Claude Code(또는 터미널)** 에 그대로 붙여넣는다.
2. 출력으로 나온 YAML을 `templates/transplant_card.yaml` 로 저장(또는 윈도우로 복사).
3. ▶ 다음 붙여넣기 필요 없음. 윈도우에서 `scripts/install_cc_switch.ps1` 실행으로 이어진다.

⚠️ 토큰/키/시크릿 **실제 값은 출력 금지**. 변수 이름·존재 여부·host 만 캔다.

---

```text
나는 이 리눅스 머신의 Claude Code 가 "사내 게이트웨이"로 접속하도록 설정돼 있다.
이 설정을 윈도우 PC로 이식하려 한다. 아래를 수행하고, 결과를 지정된 YAML 형식으로만 출력해줘.
민감값(토큰/키/시크릿)은 절대 평문 출력 금지. base_url 은 host 만.

[조사 대상]
1. 현재 활성 경로: `claude /status` 의 provider 라인, base_url host.
2. settings.json env 블록 (있는 것만, 값 마스킹):
     ~/.claude/settings.json
     ~/.claude/settings.local.json
     ./.claude/settings.json
   확인 키:
     ANTHROPIC_BASE_URL (host만)
     ANTHROPIC_AUTH_TOKEN (설정됨/미설정 + 끝4자리)
     ANTHROPIC_API_KEY (설정됨/미설정)
     ANTHROPIC_MODEL (값)
     CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS, NO_PROXY (값)
3. 셸 변수: `env | grep -E 'ANTHROPIC|CLAUDE_CODE|AWS_'` (TOKEN/KEY/SECRET 값 마스킹)
4. 게이트웨이 인증 방식: AUTH_TOKEN(Bearer) 인지 API_KEY(sk-) 인지.

[출력 — 반드시 아래 YAML 형식 그대로, 다른 설명 없이]
version: "1.0"
extracted_at: "<현재 ISO8601 KST>"
source_machine: "linux-corp"
provider:
  type: "<gateway|litellm|direct>"
  base_url_host: "<host만>"
  auth_method: "<bearer|api_key>"
  model_alias: "<있으면, 없으면 빈칸>"
env_keys:
  ANTHROPIC_BASE_URL: "https://<host>"
  ANTHROPIC_MODEL: "<값 또는 빈칸>"
  CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS: "<1 또는 빈칸>"
  NO_PROXY: "<값 또는 빈칸>"
custom_headers: []   # 헤더 이름만
notes: "<특이사항, 토큰 실제값 절대 금지>"

(토큰 실제값은 윈도우에서 내가 직접 환경변수로 넣겠다. 여기 적지 마.)
```

---

## 출력 후 할 일

- 나온 YAML을 `templates/transplant_card.yaml` 로 저장.
- 사내 토큰은 별도 발급 절차로 확보 (이 카드엔 값 없음).
- 윈도우로 이동 → `NEXT_STEP.md` 의 `install` 단계로.
