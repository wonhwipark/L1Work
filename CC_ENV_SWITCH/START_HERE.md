# START_HERE — CC_ENV_SWITCH

Claude Code 환경 전환기 (AWS Bedrock ↔ 사내 게이트웨이).
명령 한 번으로 두 백엔드를 토글하고, "무슨 일이 있어도 원복"을 보장한다.

원본 `RCA_standalone/prompt/CLAUDE_CODE_ENV_SWITCH_PROMPTS.md` 에서 분리·자동화한 단독 패키지.

---

## 문서 맵

| 파일 | 역할 | 언제 본다 |
|------|------|-----------|
| **README_따라하기.md** | 처음 보는 사람용 단일 가이드 (이것만 따라하면 끝) | **맨 먼저** |
| **START_HERE.md** | 이 문서. 전체 지도 + 퀵스타트 | 구조가 궁금할 때 |
| **NEXT_STEP.md** | 진행 상태 추적 (slug auto-carry) | 막혔을 때 / 다음 할 일 |
| `prompt/STEP1_EXTRACT.md` | 리눅스에서 이식 카드 추출 (유일한 수동 프롬프트) | 1단계 |
| `prompt/README.md` | 왜 STEP 1만 프롬프트인지 | 궁금하면 |
| `templates/transplant_card.template.yaml` | 이식 카드 표준 형식 | STEP 1 출력 저장처 |
| `templates/aws.settings.template.json` | Bedrock 프로파일 골격 | 수동 편집 시 |
| `templates/corp.settings.template.json` | 사내 게이트웨이 프로파일 골격 | 수동 편집 시 |
| `scripts/install_cc_switch.ps1` | 1회 설치 (디렉토리/골든/등록 자동) | 2단계 |
| `scripts/cc-switch.ps1` | 전환기 본체 (S1~S6 안전장치) | 일상 사용 |
| `scripts/apply_card.ps1` | 카드 YAML → corp 프로파일 자동 반영 | install이 자동 호출 |
| `scripts/verify_switch.ps1` | 전환 상태 독립 검증 | 의심스러울 때 |
| **EMERGENCY_CARD.md** | 비상 복구 5줄 (스크립트 없이도) | 꼬였을 때 |
| `VERSION.md` | 버전·변경 이력 | — |

---

## 3분 퀵스타트

```
[리눅스 사내 PC]
 1. prompt/STEP1_EXTRACT.md 의 프롬프트를 Claude Code 에 붙여넣기
    → 출력 YAML 을 templates/transplant_card.yaml 로 저장

[윈도우 PC]
 2. 사내 토큰 환경변수 등록 (값은 본인이 입력):
       setx CORP_ANTHROPIC_TOKEN "<발급받은_토큰>"
    → 새 터미널 열기

 3. 설치 (원터치):
       cd <이 패키지 폴더>
       .\scripts\install_cc_switch.ps1
    → 디렉토리·골든 스냅샷·프로파일·$PROFILE 등록·카드 반영·검증 자동

 4. 사용:
       cc-switch aws    # Bedrock 으로
       cc-switch corp   # 사내 게이트웨이로
    → 전환 후 반드시 "새 터미널"에서 claude 실행
```

---

## 핵심 원리 (3줄)

- settings.json 의 `env` 가 셸 변수보다 우선 → 전환 = **프로파일 파일 교체**.
- 반대 경로 변수 잔존 금지 (자격증명 사다리 오염 방지) → 두 프로파일은 서로의 변수를 안 가짐.
- 토큰은 파일에 박지 않고 **OS 환경변수 참조**(`${CORP_ANTHROPIC_TOKEN}`).

## 원복 보장 (1순위)

읽기전용 골든 스냅샷 + 타임스탬프 백업 회전(20개) + undo + 검증 실패 시 자동 롤백.
스크립트가 깨져도 `EMERGENCY_CARD.md` 한 줄로 원래 AWS 상태 복귀.
