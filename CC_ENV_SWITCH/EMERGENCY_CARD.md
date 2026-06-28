# EMERGENCY_CARD — 비상 복구

> 전환이 꼬여 Claude Code 가 안 뜨거나 엉뚱한 provider 로 붙을 때.
> **위에서부터** 시도. 모든 복구는 "새 터미널"에서 효과가 난다(env 재로딩).
> 이 카드는 스크립트가 깨져도 동작하도록 설계됨 — 인쇄/메모 권장.

```powershell
# ① 가장 안전 — 골든 원본으로 복귀 (cc-switch 살아있으면)
cc-switch restore original

# ② 직전 상태로 한 단계 되돌리기
cc-switch undo

# ③ 스크립트가 깨졌을 때 — 손으로 골든 원본 덮어쓰기 (스크립트 불필요)
Copy-Item "$env:USERPROFILE\.claude\profiles\_golden\settings.ORIGINAL.json" `
          "$env:USERPROFILE\.claude\settings.json" -Force

# ④ 그래도 이상 — 잔존 환경변수가 가로채는 경우. 현재 창에서 무력화 후 확인
$env:ANTHROPIC_API_KEY=$null; $env:ANTHROPIC_AUTH_TOKEN=$null
$env:ANTHROPIC_BASE_URL=$null; $env:CLAUDE_CODE_USE_BEDROCK=$null
claude /status

# ⑤ 영속 사용자 환경변수까지 의심 — 무엇이 박혀 있는지부터
Get-ChildItem Env: | Where-Object Name -match 'ANTHROPIC|CLAUDE_CODE|AWS_'
# 불필요 항목: setx <이름> ""  후 새 터미널 (또는 시스템 속성 > 환경변수에서 삭제)
```

**핵심**: ③ 골든 스냅샷은 읽기전용 + cc-switch 가 절대 안 건드림 → **언제나 살아있는 복귀점**.
전환을 아무리 반복해도 "원래 AWS 동작 상태"는 이 파일 하나로 항상 되살린다.

---

## 빠른 진단

| 증상 | 1순위 조치 |
|------|-----------|
| claude 가 아예 안 뜸 | ③ 골든 원본 덮어쓰기 → 새 터미널 |
| 엉뚱한 provider 로 붙음 | ④ 잔존 env 무력화 → /status |
| corp 인데 인증 실패 | `setx CORP_ANTHROPIC_TOKEN "<토큰>"` → 새 터미널 |
| ANTHROPIC_API_KEY 가 가로챔 | `setx ANTHROPIC_API_KEY ""` → 새 터미널 |
| 어느 경로인지 모름 | `.\scripts\verify_switch.ps1` |
