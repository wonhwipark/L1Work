# VERSION — CC_ENV_SWITCH

## v1.1 (2026-06-27 KST)

### 수정 배경 (실사용 버그)
`cc-switch corp` 후에도 실제 요청이 계속 Bedrock 으로 가던 문제. 원인은 corp
프로파일에 **모델 라우팅 잔류**(`modelOverrides`, `availableModels`,
`ANTHROPIC_DEFAULT_SONNET/HAIKU_MODEL`, Bedrock 형식의 `ANTHROPIC_MODEL`)가
남아, 게이트웨이로 붙어도 모델 해석 단계에서 Bedrock 으로 라우팅된 것.
기존 가드는 `CLAUDE_CODE_USE_BEDROCK`/`AWS_*`(연결 경로 변수)만 검사해
모델 라우팅 축을 놓쳤음.

### 변경 (사용자 편의 우선)
- **cc-switch.ps1**: corp 전환 시 **자동 정화(S4b, Repair-CorpProfile)** 추가.
  - 화이트리스트(`CorpEnvAllow`) 외 env 키 제거 → 블랙리스트가 아니므로 새 Bedrock 필드도 자동 차단.
  - 톱레벨 `modelOverrides`/`availableModels` 제거.
  - Bedrock 형식 `ANTHROPIC_MODEL` 제거(게이트웨이 모델명은 보존).
  - 정화 결과를 corp 프로파일 파일에 되써서 SSOT 도 청소.
  - `cc-switch corp -DryRun` : 지울 항목만 미리보기.
  - `Test-ProfileIntegrity` corp 분기에 모델 누수 최종 차단(방어 심층화).
- **verify_switch.ps1**: 게이트웨이 경로에서 Bedrock 모델 라우팅 잔류 점검 1줄 추가.
  깨끗하면 `[OK] 모델 라우팅 깨끗`, 잔류 시 `[X]` + 재실행 안내.
- **README_따라하기.md (신규)**: 처음 보는 사람이 이 파일 하나만 위→아래로 따라 하면
  설치·설정·전환·검증·문제해결까지 끝나는 단일 가이드. 사내값 추출(리눅스)은 부록으로 분리.

### 사용 흐름
- `cc-switch corp` → 자동 정화 + 적용 (사람 조작 그대로 1단계)
- 불안하면 `cc-switch corp -DryRun` 로 미리보기, `verify_switch.ps1` 로 확인

---

## v1.0 (2026-06-27 KST)

원본 `RCA_standalone/prompt/CLAUDE_CODE_ENV_SWITCH_PROMPTS.md` (245줄 프롬프트 레시피)에서
분리·자동화한 단독 패키지.

### 분리 근거
- RCA 5.5 본체와 무관한 인프라 도구 → 독립 패키지가 적절.

### 자동화 내역 (CodeAnalyzer 5.2 컨셉 적용)
- STEP 2 프롬프트(125줄) 전체를 스크립트 3개로 대체:
  - `cc-switch.ps1` (사전 제작, S1~S6 안전장치 전체 구현)
  - `install_cc_switch.ps1` (1회 설치 자동화)
  - `apply_card.ps1` (이식 카드 YAML → corp 프로파일 자동 반영)
- 이식 카드를 자유 텍스트 → **YAML 구조화** (파싱 안정성)
- 비상 복구 카드를 생성 의존 → **사전 배포 파일**(EMERGENCY_CARD.md)
- 프로파일 골격을 프롬프트 예시 → **템플릿 파일**

### CodeAnalyzer 패턴 적용
- ✅ START_HERE 문서 맵
- ✅ NEXT_STEP slug auto-carry (extract→install→configure→verify→done)
- ✅ verify 독립 스크립트
- ❌ Phase 0→N→F (선형 4단계라 불필요)
- ❌ session bootstrap (스크립트 실행이라 불필요)

### 정량 효과 (vs 원본)
| 지표 | Before | After |
|------|--------|-------|
| 사람 조작 단계 | 6 | 3 |
| 프롬프트 입력량 | ~170줄 | ~45줄 (STEP 1만) |
| Claude Code 생성 대기 | cc-switch 전체 | 0 (사전 제작) |
| 수동 검증 | 2회 | 0 (자동) |

### 안전 설계 (S1~S6)
- S1 읽기전용 골든 스냅샷 (최후 복귀점)
- S2 타임스탬프 백업 회전 (최근 20개)
- S3 undo 스택 (.cc_last_backup)
- S4 적용 전 무결성 검증 + 교차 오염 차단
- S5 적용 후 자동 검증 + 실패 시 자동 롤백
- S6 원자적 적용 (tmp → Move-Item)

### 미해결/후속
- 실제 사내 게이트웨이에서 E2E 검증 (환경 의존)
- SSO 사용 시 `awsAuthRefresh` 라인 활성화 (aws 템플릿 주석 참고)
- 5.x 시리즈 합류 시 `_x.x` 접미사 부여 검토
