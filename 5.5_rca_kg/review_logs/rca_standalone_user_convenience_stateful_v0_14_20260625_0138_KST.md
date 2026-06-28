# RCA Standalone v0.14 사용자 편의 stateful 패키지 수정 로그

작성일: 2026-06-25 01:38 KST

## 목적

v0.13 리뷰에서 제안한 사용자 편의 개선안을 실제 패키지에 반영했다.

## 반영 항목

| 항목 | 반영 파일 |
|---|---|
| START_HERE 단일 진입점 | START_HERE_5.5.md |
| P0~P6 상태 저장 | rca_kg/runtime_tool_generate/current_run.yaml |
| 다음 단계 안내 | NEXT_STEP_5.5.md |
| P1 전 `_l1sw.txt` 확보 분기 | RUNBOOK_L1SW_TO_P6_5.5.md, prompt/CLAUDE_CODE_PROMPTS_e2e_v1.md |
| P2 placeholder 제거 | prompt/CLAUDE_CODE_PROMPTS_e2e_v1.md |
| stale signal path 정리 | scripts/README.md |
| tool_generate 의미 명확화 | START_HERE_5.5.md, prompts, RUNBOOK |
| 검증 스크립트 | scripts/validate_package.ps1 |
| 다음 단계 확인 스크립트 | scripts/run_next_step.ps1 |
| taxonomy/skills_seed 불일치 보정 | rca_kg/schema/taxonomy.yaml |

## 남은 검증

실제 사내 Claude Code 환경에서 P0 → C0/P1 → P2 → P3 → P4 → P5 → P6 E2E 1회 수행 필요.
