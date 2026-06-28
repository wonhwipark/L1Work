# Review Log — CC_ENV_SWITCH 분리·자동화 v1.0

작성: 2026-06-27 KST
원본: `RCA_standalone/prompt/CLAUDE_CODE_ENV_SWITCH_PROMPTS.md` (245줄)

## 요청
원본 ENV_SWITCH 프롬프트를 RCA 패키지에서 분리하고, CodeAnalyzer 5.2 컨셉처럼 최대한 자동화.

## 결정
STEP 2(윈도우, 125줄)를 전부 스크립트로 사전 제작. STEP 1(리눅스)만 크로스 머신 제약으로 프롬프트 유지하되 출력을 YAML로 구조화.

## 산출물
```
CC_ENV_SWITCH/
  START_HERE.md, NEXT_STEP.md, EMERGENCY_CARD.md, VERSION.md
  prompt/        STEP1_EXTRACT.md, README.md
  templates/     aws/corp settings template, transplant_card template (YAML)
  scripts/       cc-switch.ps1, install_cc_switch.ps1, apply_card.ps1, verify_switch.ps1
```

## 검증
- control-byte scan (BEL 0x07 / VT 0x0B / FF 0x0C / 기타 비출력): **CLEAN** (전 파일)
- PowerShell 4종 brace/paren/bracket/here-string 균형: **OK** (상태머신 토크나이저)
- JSON 템플릿 2종 파싱: **OK**
- transplant_card YAML 로드: **OK**
- apply_card 미니 파서 로직 시뮬레이션: **PASS** (빈 값 스킵, 블록 종료, 후행 섹션 무시)

## 안전 설계 (원본 S1~S6 전부 구현)
S1 읽기전용 골든 / S2 백업 회전(20) / S3 undo / S4 적용전 무결성+교차오염 차단 / S5 적용후 자동검증+자동롤백 / S6 원자적 적용.

## 알려진 제약
- pwsh 미설치 환경(GitHub 릴리스 에셋 도메인 차단)으로 **런타임 실행 테스트는 미수행**. 정적 검증만.
- 실제 사내 게이트웨이 E2E는 환경 의존(미수행).
- SSO 사용 시 aws 템플릿의 `awsAuthRefresh` 주석 활성화 필요.

## 정량 효과
사람 조작 6→3단계, 프롬프트 ~170→~45줄, Claude Code 생성 대기 100% 제거, 수동 검증 2→0.

## 후속(선택)
- 윈도우 실기에서 install → cc-switch aws/corp E2E 1회
- 5.x 시리즈 합류 시 `_x.x` 접미사
