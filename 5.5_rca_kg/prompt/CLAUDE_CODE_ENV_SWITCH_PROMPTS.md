# Claude Code 환경 전환 프롬프트 — 리눅스(사내) 정보 추출 → 윈도우(AWS↔사내) 전환

작성일: 2026-06-23 KST
상황:
- **리눅스 Claude Code = 사내용**(사내 게이트웨이 경유로 추정)
- **윈도우 PC Claude Code = AWS Bedrock 사용 중**
- 목표: 윈도우 PC에서 **AWS ↔ 사내용**을 명령 한 번으로 전환

핵심 원리(2026-06 기준 공식 동작):
- Claude Code는 `~/.claude/settings.json` 의 `env` 블록을 시작 시 읽는다. **v2.x에서는
  settings.json 의 env 가 셸 환경변수보다 우선**한다. → 가장 안전한 전환법은 **프로파일별
  settings.json 을 통째로 바꿔 끼우는 것**.
- AWS Bedrock 경로 = `CLAUDE_CODE_USE_BEDROCK=1` + AWS 자격증명 + `ANTHROPIC_MODEL`(추론 프로파일 ID)
- 사내 게이트웨이 경로 = `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN`
- **자격증명 우선순위 사다리** 때문에, 한 경로의 변수가 남아 있으면 다른 경로 설정이
  "깨진 것처럼" 보인다. → 전환 시 **반대 경로 변수를 반드시 비운다**.

---

# ════════════════════════════════════════════
# STEP 1 — 리눅스(사내) Claude Code 에서 실행할 프롬프트
# ════════════════════════════════════════════

> 리눅스 사내 PC의 Claude Code(또는 터미널)에 아래를 그대로 붙여넣는다.
> 목적: 사내용 접속이 **어떤 변수로** 이뤄지는지 정확히 떠서, 윈도우에 이식할 수 있게 한다.
> ⚠️ 토큰/키 값 자체는 출력하지 말고 **변수 이름과 존재 여부, base_url 호스트**만 뽑는다.

```text
나는 이 리눅스 머신의 Claude Code 가 "사내 게이트웨이"로 접속하도록 설정돼 있다.
이 설정을 윈도우 PC로 이식하려 한다. 아래를 순서대로 수행하고 결과를 표로 정리해줘.
민감값(토큰/키/시크릿)은 절대 평문으로 출력하지 말고 "설정됨/미설정"과 마지막 4자리만 보여줘.

1. 현재 활성 경로 확인:
   - `claude /status` 결과에서 provider 라인(사내 게이트웨이인지, base_url 호스트는 무엇인지).

2. settings.json 의 env 블록 덤프 (값은 마스킹):
   - 다음 파일들을 순서대로 열어 env 키 목록만 보여줘 (있는 것만):
       ~/.claude/settings.json
       ~/.claude/settings.local.json
       ./.claude/settings.json   (프로젝트 단위면)
   - 특히 이 키들의 존재 여부와 (민감하지 않은) 값:
       ANTHROPIC_BASE_URL          → 호스트만 (예: gw.corp.example.com)
       ANTHROPIC_AUTH_TOKEN        → 설정됨/미설정 + 끝 4자리
       ANTHROPIC_API_KEY           → 설정됨/미설정
       ANTHROPIC_MODEL             → 값 그대로
       ANTHROPIC_DEFAULT_OPUS_MODEL / _SONNET_MODEL / _HAIKU_MODEL → 값 그대로
       ANTHROPIC_CUSTOM_HEADERS    → 헤더 "이름"만 (값 마스킹)
       NO_PROXY / HTTPS_PROXY      → 값 그대로 (게이트웨이가 프록시 예외 필요한지 판단용)
       CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS, CLAUDE_CODE_USE_BEDROCK 등 토글류

3. 셸 환경변수 쪽도 확인 (settings.json 외 경로로 주입됐을 수 있음):
   - `env | grep -E 'ANTHROPIC|CLAUDE_CODE|AWS_' | sed -E 's/(TOKEN|KEY|SECRET)=.*/\1=***/'`
   - ~/.bashrc, ~/.profile, /etc/profile.d/ 에 위 변수를 export 하는 줄이 있는지(파일명만).

4. 게이트웨이 호환 정보:
   - base_url 이 사내 게이트웨이면, 그게 Anthropic Messages API 호환인지(LiteLLM/자체).
   - 인증 방식: ANTHROPIC_AUTH_TOKEN(Bearer)인지 ANTHROPIC_API_KEY(sk-)인지.
   - 모델 이름이 게이트웨이 전용 명명인지(예: anthropic/claude-..., 사내 별칭).

5. 위를 아래 "이식 카드" 형식으로 출력해줘 (이 카드를 STEP 2 에 그대로 입력할 것):

   ── 사내(CORP) 이식 카드 ──────────────────
   provider           : <gateway / litellm / ...>
   ANTHROPIC_BASE_URL : <host 만>
   인증 변수          : <ANTHROPIC_AUTH_TOKEN | ANTHROPIC_API_KEY>
   ANTHROPIC_MODEL    : <값 또는 없음>
   기본 모델 핀       : opus=<>, sonnet=<>, haiku=<>  (없으면 생략)
   커스텀 헤더 이름   : <있으면 이름만>
   프록시 예외(NO_PROXY): <필요하면 호스트>
   베타 헤더 토글     : <CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 필요 여부>
   ────────────────────────────────────────
   (토큰 실제값은 윈도우에서 내가 직접 입력하겠다. 여기 적지 마.)
```

> STEP 1 이 끝나면 "이식 카드" 한 장이 나온다. 토큰 실제값은 사내 발급 절차로 따로
> 확보한다(이 프롬프트는 값이 아니라 **구조**만 캔다).

---

# ════════════════════════════════════════════
# STEP 2 — 윈도우 PC Claude Code 에서 실행할 프롬프트
# ════════════════════════════════════════════

> 윈도우 PC의 Claude Code 에 아래를 붙여넣는다. STEP 1 의 "이식 카드"와, 본인이 따로 확보한
> 토큰/AWS 정보를 함께 제공한다. 목적: **프로파일 전환 방식**으로 AWS↔사내 토글 구성.

```text
내 윈도우 PC Claude Code 는 현재 AWS Bedrock 으로 동작 중이다.
여기에 "사내 게이트웨이" 프로파일을 추가해서, 명령 한 번으로 AWS ↔ 사내 전환을 하고 싶다.

[입력 정보]
- 현재 AWS(Bedrock) 설정: 내 ~/.claude/settings.json 의 env 블록을 먼저 읽어서 그대로 재사용.
  (CLAUDE_CODE_USE_BEDROCK, AWS_REGION, AWS_PROFILE 또는 AWS_BEARER_TOKEN_BEDROCK,
   ANTHROPIC_MODEL 등)
- 사내(CORP) 이식 카드: <STEP 1 결과 붙여넣기>
- 사내 토큰: 환경변수로 내가 직접 넣겠다 (프롬프트에 평문 금지).

[설계 원칙 — 반드시 지켜라]
A. settings.json 의 env 가 셸 변수보다 우선하므로, 전환은 "프로파일 settings 파일 교체"로 한다.
   - %USERPROFILE%\.claude\profiles\aws.settings.json     (Bedrock 전용)
   - %USERPROFILE%\.claude\profiles\corp.settings.json    (사내 게이트웨이 전용)
   - 활성 프로파일은 %USERPROFILE%\.claude\settings.json 으로 "복사"해서 적용.
B. 두 프로파일은 상대 경로의 변수를 절대 남기지 않는다(자격증명 사다리 오염 방지):
   - aws.settings.json  에는 ANTHROPIC_BASE_URL / ANTHROPIC_AUTH_TOKEN 없음.
   - corp.settings.json 에는 CLAUDE_CODE_USE_BEDROCK / AWS_* 없음.
C. 토큰/시크릿은 settings.json 에 하드코딩하지 말고 OS 환경변수 참조(${ENV} 또는 빈칸+안내).
   - 사내 토큰: 사용자 환경변수 CORP_ANTHROPIC_TOKEN 으로 두고, corp 프로파일이 이를 읽게.
   - AWS: 기존 방식 유지(AWS_PROFILE SSO 또는 AWS_BEARER_TOKEN_BEDROCK).
D. 사내 게이트웨이가 베타 헤더 비호환이거나 프록시 예외가 필요하면 카드에 따라 반영
   (CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1, NO_PROXY 등).

[해줄 일]
1. 위 두 프로파일 settings.json 파일 내용을 생성해줘 (값은 ${ENV} 참조/플레이스홀더).
2. 전환용 PowerShell 함수 스크립트 `cc-switch.ps1` 를 만들어줘. 동작:
   - `cc-switch aws`  → aws.settings.json 을 settings.json 으로 적용 + 충돌 셸 변수 정리 안내
   - `cc-switch corp` → corp.settings.json 을 settings.json 으로 적용
   - `cc-switch status`   → 현재 활성 프로파일(.active 마커) + `claude /status` 안내
   - `cc-switch undo`     → 직전 전환 직전 상태로 즉시 원복(아래 안전장치 참조)
   - `cc-switch restore <백업파일|original>` → 지정 타임스탬프 백업 또는 골든 스냅샷으로 원복
   - `cc-switch list`     → 백업/스냅샷 목록 + 각 파일의 provider 한 줄 요약
   - 사내 전환 시 CORP_ANTHROPIC_TOKEN 미설정이면 경고하고 설정법 안내.

   [안전장치 — 반드시 이대로 구현. "원복 보장"이 이 스크립트의 1순위 요구사항]
   S1. 불변 골든 스냅샷(원본 보존):
       - 최초 1회, 현재 동작 중인 settings.json 을
         %USERPROFILE%\.claude\profiles\_golden\settings.ORIGINAL.json 으로 복사하고
         읽기전용 속성을 건다(Set-ItemProperty -Name IsReadOnly $true).
       - 이 파일은 cc-switch 가 절대 덮어쓰지 않는다. "무슨 일이 있어도 돌아갈 최후 지점".
       - `cc-switch restore original` 으로 항상 이 상태로 복귀 가능.
   S2. 타임스탬프 백업 회전(덮어쓰기 방지):
       - 매 전환 직전 settings.json 을
         %USERPROFILE%\.claude\backups\settings_YYYYMMDD_HHMMSS_<from→to>.json 으로 저장.
       - 단일 settings.backup.json 으로 덮어쓰지 말 것(두 번째 전환에서 원본 소실됨).
       - 최근 20개만 남기고 오래된 것 정리(원복 이력은 보존, 디스크는 관리).
   S3. undo 스택:
       - 직전 전환 전 파일 경로를 %USERPROFILE%\.claude\.cc_last_backup 에 기록.
       - `cc-switch undo` 는 이 파일을 settings.json 으로 복원 + 활성 마커 되돌림.
   S4. 적용 전 무결성 검증(깨진 설정 차단):
       - 적용할 프로파일 JSON 을 먼저 ConvertFrom-Json 으로 파싱 검증.
       - 파싱 실패하거나 env 블록이 없으면 **적용을 중단**하고 현재 상태 유지(아무것도 안 바꿈).
       - aws 프로파일에 ANTHROPIC_BASE_URL 이, corp 프로파일에 CLAUDE_CODE_USE_BEDROCK/AWS_ 가
         섞여 있으면 경고 후 중단(교차 오염 사전 차단).
   S5. 적용 후 자동 검증 + 실패 시 자동 롤백:
       - 적용 직후 `claude --version` 또는 짧은 `claude -p "reply OK"` 로 기동 확인.
       - 비정상 종료/인증오류면 S3 의 직전 백업으로 **자동 롤백**하고 사유를 출력.
       - 사용자는 깨진 상태에 갇히지 않는다.
   S6. 원자적 적용:
       - settings.json 에 직접 쓰지 말고 settings.json.tmp 에 쓴 뒤 Move-Item -Force 로 교체
         (쓰는 도중 끊겨도 반쪽 파일이 안 남음).
3. PowerShell 프로필($PROFILE)에 `cc-switch` 를 함수로 등록하는 1회 설치 명령.
4. 토큰을 사용자 환경변수로 영속 등록하는 명령 (값은 내가 채움):
   setx CORP_ANTHROPIC_TOKEN "<여기에_내가_입력>"
   (AWS 가 SSO면 awsAuthRefresh 라인도 aws.settings.json 에 넣어줘.)
5. 검증 절차:
   - `cc-switch aws`  → 새 터미널 → `claude` → "what model are you / /status" 로 Bedrock 확인
   - `cc-switch corp` → 새 터미널 → `claude` → /status 로 게이트웨이 호스트 확인
   - 전환 후 반드시 "새 터미널/새 세션"이어야 env 가 다시 읽힌다는 점 명시.

6. 비상 복구 카드(스크립트 없이도 되는 수동 원복)를 별도로 출력해줘.
   - cc-switch 자체가 깨지거나 PowerShell 프로필이 망가져도 손으로 복구할 수 있어야 한다.
   - 골든 스냅샷 경로와, "이 한 줄만 실행하면 원래대로" 명령을 카드로 제공.
   - 이 카드는 사용자가 인쇄/메모해 둘 수 있게 5줄 이내로 압축.

[주의]
- ANTHROPIC_API_KEY 가 사용자 환경에 박혀 있으면 Bedrock/게이트웨이 둘 다 가로챌 수 있다.
  status 확인 시 의도치 않은 키가 우선되면 그 키를 정리하라고 안내해줘.
- settings.json 은 git 에 올리지 마(토큰/내부 URL 유출). .gitignore 안내 포함.
- 실제 토큰/시크릿 값은 네 답변 어디에도 출력하지 마.
- 복구 경로는 스크립트에 의존하지 않는 수동 명령도 반드시 함께 제공하라(자기참조 금지).
```

---

## 비상 복구 카드 (출력 예시 — STEP 2 가 실제 경로로 채워 생성)

> 전환이 꼬여 Claude Code 가 안 뜨거나 엉뚱한 provider 로 붙을 때. **위에서부터 시도**한다.
> 모든 복구는 "새 터미널"에서 효과가 난다(env 재로딩).

```powershell
# ① 가장 안전 — 골든 원본으로 복귀 (cc-switch 안 깨졌으면)
cc-switch restore original

# ② 직전 상태로 한 단계 되돌리기
cc-switch undo

# ③ 스크립트가 깨졌을 때 — 손으로 골든 원본 덮어쓰기 (스크립트 불필요)
Copy-Item "$env:USERPROFILE\.claude\profiles\_golden\settings.ORIGINAL.json" `
          "$env:USERPROFILE\.claude\settings.json" -Force

# ④ 그래도 이상하면 — 잔존 환경변수가 가로채는 경우. 현재 창에서 무력화 후 확인
$env:ANTHROPIC_API_KEY=$null; $env:ANTHROPIC_AUTH_TOKEN=$null
$env:ANTHROPIC_BASE_URL=$null; $env:CLAUDE_CODE_USE_BEDROCK=$null
claude /status

# ⑤ 영속 사용자 환경변수까지 의심되면 — 무엇이 박혀 있는지부터 확인
Get-ChildItem Env: | Where-Object Name -match 'ANTHROPIC|CLAUDE_CODE|AWS_'
# 불필요한 항목은: setx <이름> ""  (또는 시스템 속성 > 환경변수에서 삭제) 후 새 터미널
```

핵심: ③ 골든 스냅샷은 읽기전용 + cc-switch 가 절대 안 건드리므로 **언제나 살아있는 복귀점**이다.
전환을 아무리 반복해도 "원래 AWS 동작 상태"는 이 파일 하나로 항상 되살릴 수 있다.

---

## 참고 — 두 프로파일 settings.json 골격 (STEP 2 가 생성할 결과 예시)

> 값은 채우지 않은 골격이다. STEP 2 가 카드/환경에 맞춰 실제로 생성한다.

`aws.settings.json` (Bedrock):
```jsonc
{
  // SSO 쓰면 awsAuthRefresh 추가: "awsAuthRefresh": "aws sso login --profile <prof>",
  "env": {
    "CLAUDE_CODE_USE_BEDROCK": "1",
    "AWS_REGION": "<예: us-east-1>",
    "AWS_PROFILE": "<프로파일명>",        // 또는 AWS_BEARER_TOKEN_BEDROCK 방식
    "ANTHROPIC_MODEL": "<예: us.anthropic.claude-sonnet-4-6-v1>"
    // 사내 변수(ANTHROPIC_BASE_URL/AUTH_TOKEN)는 여기 없음 — 의도적
  }
}
```

`corp.settings.json` (사내 게이트웨이):
```jsonc
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://<사내 게이트웨이 호스트>",
    "ANTHROPIC_AUTH_TOKEN": "${CORP_ANTHROPIC_TOKEN}",  // OS 환경변수 참조
    "ANTHROPIC_MODEL": "<게이트웨이 모델 별칭 또는 비움>",
    // 게이트웨이가 Bedrock 비호환 베타 거르면:
    "CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS": "1"
    // CLAUDE_CODE_USE_BEDROCK / AWS_* 는 여기 없음 — 의도적
  }
}
```

## 검증 한 줄 요약

```
STEP1(리눅스): /status + settings.json env 로 사내 접속 "구조"만 카드화 (값 마스킹)
STEP2(윈도우): aws/corp 두 프로파일 분리 + cc-switch 로 교체, 전환 후 새 터미널에서 /status 확인
원칙: settings.json env 우선 → 파일 교체 방식. 반대 경로 변수 잔존 금지. 토큰은 OS 환경변수.
안전: 읽기전용 골든 스냅샷(최후 복귀점) + 타임스탬프 백업 회전 + undo + 검증 실패 시 자동 롤백
      + 스크립트 없이도 되는 수동 복구 카드. "전환을 아무리 꼬아도 한 줄로 원복" 보장.
```
