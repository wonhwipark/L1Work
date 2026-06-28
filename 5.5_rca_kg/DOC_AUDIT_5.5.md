# DOC_AUDIT — 사용자 문서 정리 결과

갱신: 2026-06-27 12:21 KST

## 정리 원칙

```text
1. 새 사용자는 README.md에서 시작한다.
2. 정상 실행은 `START_HERE_5.5.md`와 스킬 호출만 따른다.
3. 설치 상세는 INSTALL_SKILL.md에만 둔다.
4. USER_GUIDE는 설치 후 사용법만 설명한다.
5. NEXT_STEP은 현재 다음 한 걸음만 보여준다.
6. RUNBOOK은 막혔을 때 증상별 조치만 제공한다.
7. HANDOFF는 설계 이력/유지보수용으로 격리한다.
8. prompt/는 legacy only로 표시한다.
```

## 검토 결과

정상 사용자 경로의 문서에서는 직접 수동 복사 설치 절차를 제거하고, `install_skill.ps1` / `validate_install.ps1` 기준으로 통일했다.


---

## 추가 점검 — v0.19 manifest guard (2026-06-27 12:21 KST)

- 설치 구조 검증은 `skill_manifest.yaml`을 기준으로 한다.
- 구조 불일치 시 `install_skill.ps1`이 복구 가이드를 출력한다.
- 상세 복구 문서는 `STRUCTURE_FIX_GUIDE.md`다.
---

## v0.21 kg_root 정책

`workspace_root`는 RCA_standalone 패키지 루트이고, `kg_root`는 누적 RCA KG 저장소다. 기본값은 `<workspace_root>/rca_kg`이며, 반복 사용자는 `configure_kg_root.ps1 -KgRoot "D:\AI_Automation\RCA_KG"`로 고정 저장소를 지정한다. `rca_kg`는 스킬 설치 폴더 아래에 두지 않는다.
