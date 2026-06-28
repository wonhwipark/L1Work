# HANDOFF_5.5 — RCA 설계 이력/유지보수 인계

마지막 갱신: 2026-06-27 12:21 KST  
일반 사용자 시작점: `README.md` 또는 `START_HERE_5.5.md`  
이 문서는 설계 이력과 유지보수 확인용이다.

---

## 1. 패키지 목적

RCA 5.5는 L1SW Log Analyzer가 만든 `_l1sw.txt`를 바탕으로 RCA 결과를 재사용 가능한 지식으로 축적하기 위한 standalone 스킬 패키지다.

```text
_l1sw.txt
→ P0~P6
→ signal
→ case YAML
→ keywords.yaml 후보/confirmed
```

---

## 2. 현재 운영 모델

권장 운영은 `/root-cause-analyzer` 스킬 방식이다.

```text
사용자 입력: _l1sw.txt 경로 또는 .sdm만 있는 상황 설명
스킬 처리: P0~P6 단계 진행, current_run.yaml 기반 이어하기
결과 위치: rca_kg/ 하위 tool_generate/cases/keywords
```

`prompt/` 폴더는 스킬 설치가 불가능한 환경의 레거시 수동 모드로만 유지한다.

---

## 3. 주요 결정

### D1. L1SW-first

RCA는 `.sdm` 원본을 직접 분석하지 않는다. `.sdm`은 L1SW Log Analyzer의 입력이고, RCA의 주 입력은 `_l1sw.txt`다.

### D2. current_run.yaml 기반 stateful 실행

```text
rca_kg/runtime_tool_generate/current_run.yaml
```

이 파일은 현재 로그, 단계, issue_type, signal, case 후보, next_step을 기록한다.

### D3. tool_generate 명명

자동 산출물 폴더는 `_tool_generate` 접미사를 사용한다.

```text
runtime_tool_generate/
signals_tool_generate/
indexes_tool_generate/
```

의미는 “도구가 생성하고 사람이 판단한다”이다.

### D4. 미지 모듈 가드

모르는 모듈이나 담당영역 밖 원인을 단정하지 않는다. evidence가 부족하면 confidence를 낮추거나 unresolved로 저장한다.

### D5. keywords 승격 원칙

P6에서 candidate를 바로 confirmed로 승격하지 않는다. 근거, 반복성, 사람 승인이 충분할 때만 confirmed로 이동한다.

---

## 4. 유지보수 체크포인트

```text
- README/START_HERE/INSTALL_SKILL/USER_GUIDE/NEXT_STEP/RUNBOOK 역할 중복 금지
- 설치 상세는 INSTALL_SKILL.md에만 유지
- 정상 사용 문서에는 수동 복사 명령을 넣지 않음
- prompt/는 legacy로만 설명
- RCA 입력은 _l1sw.txt 기준으로 유지
- current_run.yaml package_version과 VERSION_5.5.md 동기화
```

---

## 5. 열린 항목

```text
1. 실제 사내 _l1sw.txt 기반 E2E 검증
2. CodeAnalyzer 5.2 HLD/MSC와 RCA case code_ref 연결 계약 확정
3. issue_type seed 확장 기준 정리
```
---

## v0.21 kg_root 정책

`workspace_root`는 RCA_standalone 패키지 루트이고, `kg_root`는 누적 RCA KG 저장소다. 기본값은 `<workspace_root>/rca_kg`이며, 반복 사용자는 `configure_kg_root.ps1 -KgRoot "D:\AI_Automation\RCA_KG"`로 고정 저장소를 지정한다. `rca_kg`는 스킬 설치 폴더 아래에 두지 않는다.
