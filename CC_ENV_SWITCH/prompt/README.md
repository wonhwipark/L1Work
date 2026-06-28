# prompt/ — 왜 STEP 1만 프롬프트인가

이 폴더에는 프롬프트가 **하나뿐**이다: `STEP1_EXTRACT.md`.

## 이유

원본 `CLAUDE_CODE_ENV_SWITCH_PROMPTS.md` 는 STEP 1·2 두 프롬프트(245줄)였다.
이 패키지는 그중 **STEP 2를 전부 스크립트로 대체**했다.

| 원본 STEP 2가 하던 일 | 이 패키지에서 | 위치 |
|----------------------|---------------|------|
| cc-switch.ps1 생성 지시 | 사전 제작 완성본 | `scripts/cc-switch.ps1` |
| 프로파일 JSON 골격 기술 | 템플릿 파일 | `templates/*.template.json` |
| 설치/등록 수동 안내 | 1회 실행 스크립트 | `scripts/install_cc_switch.ps1` |
| 이식 카드 → corp 반영 | 자동 파서 | `scripts/apply_card.ps1` |
| 전환 후 수동 검증 | 독립 검증 스크립트 + cc-switch 내장 S5 | `scripts/verify_switch.ps1` |
| 비상 복구 카드 출력 | 사전 배포 파일 | `EMERGENCY_CARD.md` |

## STEP 1이 프롬프트로 남은 이유

리눅스 사내 PC는 윈도우와 **다른 머신**이다. 그 머신의 settings.json·환경변수를
윈도우에서 원격으로 읽을 방법이 없다. 그래서 "그 머신 위에서" Claude Code가
구조를 떠 주는 프롬프트가 필요하다. 이건 크로스 머신 제약이라 자동화 불가.

단, 출력을 **YAML로 강제**해서 윈도우 스크립트(`apply_card.ps1`)가 바로 먹을 수 있게 했다.
즉 STEP 1도 "출력 → 파일 저장" 외엔 사람 손이 안 들어간다.
