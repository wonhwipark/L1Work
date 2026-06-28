# HANDOFF_5.2 — CodeAnalyzer 설계 이력/유지보수 인계

마지막 갱신: 2026-06-27 10:38 KST  
일반 사용자 시작점: `README.md` 또는 `START_HERE_5.2.md`  
이 문서는 설계 이력과 유지보수 확인용이다.

---

## 1. 패키지 목적

L1a Master v0.40 §5.2 Code Analyzer를 standalone 스킬 패키지로 분리했다.

목적:

```text
- 특정 L1 블록 동작을 HLD 없이 복원
- 특정 API 기준 full call flow와 MSC 생성
- 대형 코드에서 staged 분석으로 토큰 사용량 제어
- RCA 5.5의 root cause code reference로 재사용 가능한 HLD성 md 축적
```

---

## 2. 현재 운영 모델

권장 운영은 `/code-analyzer` 스킬 방식이다.

```text
사용자 입력: 코드 루트 + 블록/API명
스킬 처리: Track A/B 판별, focused structure, procedure 분석, MSC/HLD 생성
결과 위치: output/5.2/<slug>/
```

`prompt/` 폴더는 스킬 설치가 불가능한 환경의 레거시 수동 모드로만 유지한다.

---

## 3. 주요 결정

### D1. 산출물 경로 단일화

```text
output/5.2/<slug>/
```

폐기 경로:

```text
%USERPROFILE%\artifacts\code_analyzer\<slug>\
artifacts/5.2/<slug>/
artifacts\code_analyzer\<slug>\
```

### D2. extraction_mode enum 통일

```text
extraction_mode: git | bash | powershell | internal_search | mixed
```

### D3. token cursor 진행줄

```text
[진행: PHASE0_DONE → 다음: PHASE1_PROCEDURE_DISCOVERY]
```

### D4. 전역 call edge 본문 누적 금지

허용:

```text
procedure별 local_call_edges
전역 EDGE_IDS_DONE 같은 ID 요약
```

금지:

```text
procedure가 늘수록 커지는 전역 call edge 본문 블록
```

### D5. procedure_runtime_index 도입

```text
Phase 1: structure json → procedure_runtime_index 생성
Phase 2..N: procedure_runtime_index[procedure_slug]만 사용
fallback: index 불완전 시 targeted structure read
```

### D6. MSC 분리

```text
output/5.2/<slug>/msc_<procedure_slug>_<YYYYMMDD_HHMM_KST>.puml
```

HLD md에는 `msc_ref`만 둔다.

---

## 4. 유지보수 체크포인트

```text
- README/START_HERE/INSTALL_SKILL/USER_GUIDE/NEXT_STEP/RUNBOOK 역할 중복 금지
- 설치 상세는 INSTALL_SKILL.md에만 유지
- 정상 사용 문서에는 수동 복사 명령을 넣지 않음
- prompt/는 legacy로만 설명
- output 경로는 output/5.2/<slug>/ 하나로 유지
```

---

## 5. 열린 항목

```text
1. 실제 사내 L1 코드 1개 블록 대상 E2E 검증
2. RCA 5.5 root_cause.code_ref 연결 계약 확정
3. Stage 분할 임계값 실데이터 기반 조정
```
