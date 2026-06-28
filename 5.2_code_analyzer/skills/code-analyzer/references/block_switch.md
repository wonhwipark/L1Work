# Block/API 전환과 복귀 (block_switch)

분석 중 다른 블록/API를 급히 확인하고 원래 자리로 돌아오는 절차다. 각 블록 상태는 `output/5.2/<slug>/`에 폴더로 분리되어 쌓이므로, 전환은 slug 전환 + 복귀 스택으로 안전하게 처리된다.

## 상태 모델

`NEXT_STEP_5.2.md`에 두 필드를 둔다.

```text
current_slug:   현재 작업 중인 블록 slug
block_stack:    복귀 대기 slug 목록 (LIFO). 예: [scell_config, tx_switch]
```

각 블록의 진행 위치(progress_cursor, DONE procedure, next)는 그 블록의 `output/5.2/<slug>/analysis_progress.md`에 이미 보존된다. 따라서 전환은 "현재 cursor를 그 블록 파일에 확정 저장 → slug만 바꾼다"로 끝난다.

## A. 전환 (현재 블록 보류, 새 블록 시작)

트리거 예: "잠깐 T 블록 먼저 봐줘", "다른 API XxxReq 확인하고 올게".

1. 현재 블록의 `analysis_progress.md`에 progress_cursor를 확정 저장한다(예: `PROC_NEXT:proc_d` 상태 그대로).
2. `NEXT_STEP_5.2.md`의 `block_stack`에 현재 `current_slug`를 push한다.
3. 새 대상(블록/API)으로 §2 규모 판별 → Track A/B → Phase 0를 시작한다. `current_slug`를 새 slug로 바꾼다.
4. 진행줄: `[진행: BLOCK_SWITCH_PUSH:<old_slug> → 다음: PHASE0:<new_slug>] (복귀 대기: block_stack)`

주의: 전환해도 이전 블록의 산출물은 `output/5.2/<old_slug>/`에 그대로 남는다. 덮어쓰지 않는다.

## B. 복귀 (새 블록 확인 끝, 이전으로)

트리거 예: 새 블록이 BLOCK_HLD_DONE에 도달했거나, 사용자가 "원래대로", "C 블록 이어서".

1. `block_stack`에서 가장 최근 slug를 pop한다(비어 있으면 "복귀 대상 없음" 안내).
2. `current_slug`를 pop한 slug로 되돌린다.
3. 그 블록의 `output/5.2/<slug>/analysis_progress.md`에서 보존된 progress_cursor를 읽어 이어간다. resume.md 규칙을 적용한다.
4. 진행줄: `[진행: BLOCK_SWITCH_POP → 다음: <복귀 cursor 예: PROC_NEXT:proc_d>:<slug>]`

## C. 이미 분석한 블록으로 재진입

같은 블록 slug로 다시 들어가면 처음부터가 아니다. `output/5.2/<slug>/analysis_progress.md`의 cursor에서 이어간다(resume.md). 이미 DONE인 procedure는 재분석하지 않으므로, 같은 모듈을 반복 확인해도 비용이 누적되지 않는다.

## 안전 규칙

- 전환·복귀로 인해 어떤 블록의 DONE procedure도 다시 분석하지 않는다.
- block_stack은 LIFO다. 여러 번 중첩 전환(A에서 T로, T에서 U로)해도 pop 순서로 정확히 되돌아온다.
- slug가 충돌하면(같은 이름 재사용) 기존 폴더를 덮지 않고 사용자에게 기존 이어쓰기/새 slug를 묻는다.
- 전환 시점에 진행 중이던 procedure가 "분석 도중"이면, 부분 산출물을 남기지 말고 직전 DONE 경계까지를 cursor로 저장한다(미완 procedure는 next로 표시).

## 예시 흐름

```text
scell_config 분석 중 (proc_a DONE, proc_b DONE, 다음 proc_c)
  ├─ "tx_switch 먼저 봐줘"
  │    → push scell_config (cursor=PROC_NEXT:proc_c), current_slug=tx_switch, Phase 0 시작
  ├─ tx_switch 분석 … BLOCK_HLD_DONE:tx_switch
  └─ "원래대로"
       → pop → current_slug=scell_config, cursor=PROC_NEXT:proc_c 에서 이어감
```
