# USAGE_SCENARIO_5.5 — RCA 전체 운영 시나리오

갱신: 2026-06-27 12:21 KST  
이 문서는 배경과 운영 시나리오를 설명한다. 순서대로 실행하려면 `START_HERE_5.5.md`를 먼저 본다.

---

## 1. 목표

RCA 5.5는 `_l1sw.txt` 기반으로 반복 가능한 RCA 루프를 만든다.

```text
L1SW 출력 확보
→ issue_type 추천
→ signal 생성
→ 원인분석
→ case YAML 축적
→ keywords.yaml 후보/confirmed 지식화
```

---

## 2. 사용자 역할

사용자는 모든 단계를 직접 작성하지 않는다. 사용자는 다음 지점에서만 판단한다.

```text
- 입력 로그가 맞는지 확인
- issue_type 추천을 승인 또는 수정
- RCA 가설/근거가 타당한지 확인
- case 저장/keywords 승격 승인
```

도구가 생성하는 항목:

```text
- current_run.yaml
- signal 파일
- manifest fragment 후보
- case YAML 초안
- index 갱신 후보
- keywords candidate
```

---

## 3. 첫 번째 로그

```text
1. README.md 확인
2. install_skill.ps1 실행
3. /root-cause-analyzer 호출
4. _l1sw.txt 경로 전달
5. P0~P2로 환경/포맷 준비
6. P3~P6로 분석 루프 수행
```

---

## 4. 두 번째 이후 로그

환경과 포맷이 이미 준비되어 있으면 보통 P3부터 시작한다.

```text
/root-cause-analyzer
새 _l1sw.txt 로그 분석해줘
```

스킬은 이전 상태와 새 입력을 비교해 필요한 단계부터 진행한다.

---

## 5. 운영상 중요한 원칙

```text
- .sdm 직접 분석 금지: _l1sw.txt가 RCA 입력이다.
- signal 중심 분석: 전체 로그를 처음부터 끝까지 읽지 않는다.
- time anchor 중심: 실패 cptime 주변에서 원인 후보를 좁힌다.
- 지식 축적: case와 keywords를 재사용 가능하게 남긴다.
- 정직성: 모르면 모른다고 쓰고 unresolved로 분리한다.
```

---

## 6. 문서 역할

| 문서 | 역할 |
|---|---|
| `README.md` | 새 사용자 최초 진입 |
| `START_HERE_5.5.md` | 정상 실행 순서 |
| `INSTALL_SKILL.md` | 설치 전용 |
| `USER_GUIDE_5.5.md` | 실제 사용법 |
| `NEXT_STEP_5.5.md` | 현재 다음 행동 |
| `RUNBOOK_L1SW_TO_P6_5.5.md` | 문제 해결 |
| `HANDOFF_5.5.md` | 설계 이력/유지보수 |
---

## v0.21 kg_root 정책

`workspace_root`는 RCA_standalone 패키지 루트이고, `kg_root`는 누적 RCA KG 저장소다. 기본값은 `<workspace_root>/rca_kg`이며, 반복 사용자는 `configure_kg_root.ps1 -KgRoot "D:\AI_Automation\RCA_KG"`로 고정 저장소를 지정한다. `rca_kg`는 스킬 설치 폴더 아래에 두지 않는다.
