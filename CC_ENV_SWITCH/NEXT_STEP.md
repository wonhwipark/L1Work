# NEXT_STEP — CC_ENV_SWITCH 진행 상태

> CodeAnalyzer 5.2 의 slug auto-carry 패턴. 막히면 `current_slug` 만 보면 된다.
> 각 단계 끝에 `next` 가 있어 다음 할 일이 자명하다.

```yaml
current_slug: extract    # extract → install → configure → verify → done

slugs:
  extract:
    label: "STEP 1 — 리눅스에서 이식 카드 추출"
    machine: "리눅스 사내 PC"
    action: "prompt/STEP1_EXTRACT.md 의 프롬프트를 Claude Code 에 붙여넣기"
    output: "templates/transplant_card.yaml (출력 YAML 저장)"
    next: install
    note: "이 패키지에서 유일하게 사람이 프롬프트로 하는 단계"

  install:
    label: "설치 — install_cc_switch.ps1"
    machine: "윈도우 PC"
    prereq:
      - "templates/transplant_card.yaml 준비됨"
      - "setx CORP_ANTHROPIC_TOKEN \"<토큰>\" 실행 후 새 터미널"
    action: ".\\scripts\\install_cc_switch.ps1"
    auto:
      - "디렉토리 생성(profiles/_golden/backups)"
      - "골든 스냅샷(읽기전용) 생성"
      - "aws/corp 프로파일 배치"
      - "apply_card.ps1 자동 호출로 corp 프로파일 완성"
      - "cc-switch.ps1 복사 + $PROFILE 등록"
    next: configure

  configure:
    label: "프로파일 확인 (선택)"
    machine: "윈도우 PC"
    action: "%USERPROFILE%\\.claude\\profiles\\ 의 aws/corp JSON 확인"
    check:
      - "aws: AWS_PROFILE, ANTHROPIC_MODEL 채워졌는지"
      - "corp: ANTHROPIC_BASE_URL host 맞는지, AUTH_TOKEN 이 ${CORP_ANTHROPIC_TOKEN} 인지"
    next: verify
    note: "카드가 정확했으면 손댈 것 없음"

  verify:
    label: "전환 검증"
    machine: "윈도우 PC"
    action:
      - "cc-switch aws  → 새 터미널 → claude /status (Bedrock 확인)"
      - "cc-switch corp → 새 터미널 → claude /status (게이트웨이 host 확인)"
      - "(의심 시) .\\scripts\\verify_switch.ps1"
    next: done

  done:
    label: "완료 — 일상 사용"
    usage:
      - "cc-switch aws    # Bedrock"
      - "cc-switch corp   # 사내 게이트웨이"
      - "cc-switch status # 현재 상태"
      - "cc-switch undo   # 직전 전환 원복"
      - "cc-switch restore original  # 골든 원본 복귀"
    note: "전환 후 항상 새 터미널에서 claude 실행"
```

## 막혔을 때

- 전환이 꼬임 → `EMERGENCY_CARD.md`
- "어느 경로로 붙는지" 불명 → `.\scripts\verify_switch.ps1`
- corp 프로파일이 비어 있음 → 카드 재적용: `.\scripts\apply_card.ps1 -CardPath <카드> -ProfilePath <corp.json>`
