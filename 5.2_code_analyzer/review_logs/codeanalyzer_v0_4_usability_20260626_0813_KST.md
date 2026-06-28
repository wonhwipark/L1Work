# Review Log — CodeAnalyzer Standalone v0.4 (사용자 편의 보강)

생성: 2026-06-26 08:13 KST  
기준 패키지: CodeAnalyzer_standalone v0.3 (output 이동본)

---

## 1. 반영 배경

v0.3 사용자 편의 점검에서 아래 마찰이 확인되었다.

```text
1. copy prompt에 사람이 손으로 채울 <...> placeholder가 누적 70여 개.
   - <slug> 28회, <procedure_slug> 11회, <YYYYMMDD_HHMM_KST> 8회.
   - 특히 copy_phase1이 Phase 0가 방금 만든 structure 파일의 타임스탬프 파일명을
     사람에게 직접 적으라고 요구 → 사람이 알 수 없는 값이라 폴더를 열어 복사해야 함.
2. copy prompt가 7개. 매 단계 "지금 어느 파일을 붙여넣지"를 사람이 판단해야 함.
   진행줄은 상태만 알려주고 다음 파일명을 알려주지 않음.
3. 최상위 .md 6개가 모두 "시작/먼저" 류 표현 → 처음 여는 사람이 어디부터 볼지 모호.
```

v0.4는 동작/토큰 정책을 v0.3 그대로 두고 위 3가지만 개선한다.

---

## 2. 개선 ① — placeholder 자동화 (가장 큰 효과)

### 2.1 slug 자동 승계

```text
- Phase 0이 slug 확정 후 NEXT_STEP_5.2.md의 current_slug에 기록한다.
- copy_phase1 / copy_next_procedure / copy_resume / copy_phase_f는
  slug 입력을 비우면 current_slug를 자동 승계한다.
- 사람은 다른 블록으로 바꿀 때만 slug를 새로 지정한다.
```

각 단계 prompt의 `[입력]`을 "slug: (생략 가능 — 비우면 current_slug 사용)"으로 바꾸고, `[자동 해석 규칙]` 블록을 추가했다.

### 2.2 타임스탬프 / 구조파일명 자동화

```text
- <YYYYMMDD_HHMM_KST>는 사람이 적지 않는다. 새 파일 생성 시 도구가 현재 KST로 채운다.
- structure_json은 사람이 파일명을 적지 않는다.
  output/5.2/<slug>/ 에서 최신 *_focused.json을 자동 선택(없으면 300KB 이하 최신 *.json).
```

copy_phase1의 `structure_json: output/5.2/<slug>/structure_<YYYYMMDD_HHMM_KST>_focused.json`
줄을 제거하고 자동 탐색 규칙으로 대체했다.

효과:

```text
사람이 채우던 placeholder 70여 개 → 사실상 첫 입력(코드루트 + 블록명) 2개로 감소.
```

---

## 3. 개선 ② — 진행줄에 "다음 붙여넣기" 파일명 추가

모든 단계 prompt의 완료 진행줄 다음 줄에 한 줄을 추가했다.

```text
[진행: PHASE1_DONE → 다음: PROC_NEXT:<procedure_slug>]
▶ 다음 붙여넣기: prompt/copy_next_procedure.md
```

상태별 매핑:

```text
SESSION_READY      ▶ copy_track_b.md (대형) 또는 copy_phase0.md
TRACKB_DONE        ▶ copy_phase0.md
PHASE0_DONE        ▶ copy_phase1.md
PHASE1_DONE        ▶ copy_next_procedure.md
PROC_DONE(다음 有) ▶ copy_next_procedure.md
PROC_DONE(마지막)  ▶ copy_phase_f.md
BLOCK_HLD_DONE     ▶ copy_phase0.md (새 블록)
```

세션 부트스트랩에도 규칙 21로 명문화해, step prompt에 hint가 없더라도 동일하게 동작하게 했다.

---

## 4. 개선 ③ — START_HERE 문서 지도 3줄

START_HERE 상단에 "평소에는 이 파일 하나면 된다" 지도를 추가했다.

```text
START_HERE   ← 처음/평소
NEXT_STEP    ← 상태/이어하기
RUNBOOK      ← 막혔을 때만
prompt/      ← 실제 붙여넣기
나머지       ← 설계 이력. 평소엔 안 봐도 됨
```

진입 문서가 6개로 분산돼 보이던 문제를 "1차 문서는 START_HERE 하나"로 정리했다.

---

## 5. 수정/추가 파일

추가:

```text
review_logs/codeanalyzer_v0_4_usability_20260626_0813_KST.md
```

수정:

```text
VERSION_5.2.md                     # v0.4 + 편의 헤드라인, 섹션 번호 정리
START_HERE_5.2.md                  # 문서 지도, slug 자동승계 노트, 진행줄 next-file hint
NEXT_STEP_5.2.md                   # (current_slug 필드 기존 존재 — 변경 없음)
prompt/copy_session_bootstrap.md   # 규칙 18~21(입력 편의 + next-file hint) 추가
prompt/copy_phase0.md              # current_slug 기록, 타임스탬프 자동, next-file hint
prompt/copy_phase1.md              # slug 자동승계, structure 자동탐색, next-file hint
prompt/copy_next_procedure.md      # slug 자동승계, 타임스탬프 자동, next-file hint
prompt/copy_resume.md              # slug 자동승계, next-file hint
prompt/copy_phase_f.md             # slug 자동승계, next-file hint
prompt/copy_track_b.md             # next-file hint
```

미변경(동작/토큰 정책 + history 보존):

```text
RUNBOOK_BLOCK_TO_HLD_5.2.md
RUNTIME_TOKEN_POLICY_5.2.md
HANDOFF_5.2.md
schema/*.md
reference/master_v0.40_section_5_2.md
output_layout/analysis_progress_5.2.template.md
output/5.2/_example_slug/README.md
review_logs/codeanalyzer_v0_2_*.md
review_logs/codeanalyzer_v0_3_*.md
```

---

## 6. 완료 기준

```text
- copy_phase1에서 사람이 타임스탬프 파일명을 적는 줄이 사라짐
- slug 자동승계 규칙이 4개 단계 prompt + 부트스트랩에 명문화됨
- 모든 완료 진행줄에 "▶ 다음 붙여넣기" hint가 붙음
- START_HERE 상단에 문서 지도 3줄이 있음
- v0.3 동작/토큰 정책(index 우선/edge 누적 금지/MSC 분리/output 경로)은 그대로 유지됨
- BEL 등 깨진 바이트 없음
```

---

## 7. 남은 미결 (계승)

```text
1. 실제 사내 L1 코드 1개 블록 대상 E2E 검증 필요
2. RCA 5.5 root_cause.code_ref 연결 계약은 첫 HLD 산출물 이후 확정
3. Stage 분할 임계값은 실데이터로 조정
```
