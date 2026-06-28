---
name: root-cause-analyzer
description: Perform root-cause analysis (RCA) on telecom L1 (LTE/NR 5G) protocol logs, turning L1SW Log Analyzer output (_l1sw.txt) into structured case YAML in a knowledge graph. Covers RACH failure, SCG failure, TX abnormal, and L2 max retransmission. Use this whenever the user wants to analyze a failure log, find the cause of an L1 issue, build or update an RCA case, generate a signal from _l1sw.txt, promote keywords, or mentions "_l1sw.txt", "RCA", "root cause", "issue_type", "case YAML", "fingerprint", "cptime", "signal", "P0~P6", or names one of the four issue types. Prefer this skill over ad-hoc log reading for any L1 log-to-cause task, even if the user does not say the word "skill". Drives the staged P0–P6 workflow using current_run.yaml as state.
---

# root-cause-analyzer

L1 채널 모뎀 프로토콜 로그의 근본 원인 분석(RCA)을 수행한다. L1SW Log Analyzer가 만든 `_l1sw.txt`를 입력으로 받아, 단계형 P0~P6 워크플로우로 case YAML(지식그래프)을 생성·갱신한다. 대상 issue_type: RACH failure, SCG failure, TX abnormal, L2 max retransmission.

호출: `/root-cause-analyzer` 또는 자연어 "이 `_l1sw.txt` 원인 분석해줘". 별도 부트스트랩 붙여넣기는 필요 없다 — 아래 "세션 불변 규칙"이 항상 적용된다.

---

## 0. 입력 파이프라인 — RCA는 `.sdm`을 직접 분석하지 않는다

```text
.sdm 원본
  → [L1SW Log Analyzer]   ← 별도 스킬. RCA 밖. module/time 필터로 _l1sw.txt 생성
  → _l1sw.txt              ← RCA의 주 입력
  → [P0~P6]                ← 이 스킬
  → case YAML / keywords.yaml 성장
```

핵심: **P0는 `_l1sw.txt` 생성 전에 도는 환경 진단 단계**다. P0가 `_l1sw.txt` 유무를 보고 분기한다(있으면 P1, 없으면 C0로 L1SW 실행 안내). 즉 `_l1sw.txt` 확보(C0/L1SW)를 P0가 감싼다. RCA가 L1SW를 직접 실행하지는 않는다 — C0는 명령을 안내하고, 파라미터가 확실할 때만 실행한다.

---

## 1. 세션 불변 규칙 (항상 적용 — 별도 붙여넣기 불필요)

KG 루트 (가장 먼저 — 모든 누적 산출물의 기준)
0a. `workspace_root`와 `kg_root`를 분리한다.
   - `workspace_root` = RCA_standalone 패키지 루트(`skill_manifest.yaml`, `rca_config.yaml` 보유 폴더).
   - `kg_root` = 누적 RCA 지식 저장소(`cases/`, `keywords.yaml`, `runtime_tool_generate/`, `signals_tool_generate/` 보유 폴더).
0b. `kg_root`는 스킬 설치 폴더(`.claude/skills/root-cause-analyzer`) 아래에 두지 않는다. 스킬은 업데이트 때 교체 가능하고, KG는 계속 보존되어야 한다.
0c. P0는 먼저 `workspace_root`를 찾고, `{workspace_root}/rca_config.yaml`의 `kg_root`를 읽는다. `kg_root`가 null이면 기본값 `{workspace_root}/rca_kg`를 사용한다.
0d. 모든 누적 산출물 경로는 항상 `{kg_root}/...`로 해석한다. 절대 현재 작업 디렉토리(cwd) 기준 `rca_kg/` 상대경로로 쓰지 않는다.
0e. `{kg_root}/runtime_tool_generate/current_run.yaml`이 상태 SSOT다. `workspace_root`와 `kg_root`가 비어 있으면 P0 또는 `configure_kg_root.ps1`를 먼저 수행한다.
0f. cwd가 로그 파일 폴더인데 그 아래 `rca_kg/`가 있으면 잘못 생성된 KG일 수 있다. 경고하고 `STRUCTURE_FIX_GUIDE.md`의 KG 병합 절차를 안내한다. 자동 삭제·자동 이동은 하지 않는다.

상태 SSOT
1. 상태는 `{kg_root}/runtime_tool_generate/current_run.yaml`이 단일 출처다. 각 단계 시작 시 먼저 읽고, 종료 시 `current_step`/`next_step`/`last_updated_kst` + 해당 P블록을 갱신한다.
2. 사람은 `current_run.yaml`을 직접 편집하지 않고 `NEXT_STEP_5.5.md`를 본다. 각 단계 종료 시 `NEXT_STEP_5.5.md`도 갱신한다.
3. 이전 단계 산출물이 있으면 사용자에게 경로를 다시 묻지 않고 `current_run.yaml`에서 자동 사용한다. 후보가 여러 개면 전체 경로 타이핑 대신 번호만 묻는다.

입력 편의
4. 파일명 타임스탬프 `<YYYYMMDD>_<HHMM>`은 사람이 적지 않는다. 도구가 현재 KST로 채운다.
5. issue_type/경로가 비어 있으면 자동 추천·자동 선택을 우선한다(P3). 사람에게는 "이걸로 진행할까요?"만 묻는다.

자동 전용 영역
6. `*_tool_generate` 폴더(runtime/signals/indexes)는 도구가 쓰고 사람이 직접 편집하지 않는다. "도구가 쓰고, 사람이 판단한다". 승인·원인 판단은 사람이 한다.

분석 정직성 (중요)
7. 미지 모듈 가드: 원인 줄이 `_l1sw.txt`/signal에 없고 주변이 비어 있으면 원인을 단정하지 않는다. 추가 추출(시간창/모듈/명령 후보)을 제시하고 멈춘다. 누적은 `p4.extraction_attempt_count`로 관리하고, 2회 후에도 없으면 `analyzed + confidence: low + 원인 미상`으로 정직하게 종료한다.
8. `unresolved`(담당영역 밖, 핸드오프 필요)와 `analyzed + confidence: low`(저신뢰)는 다른 상태다. 혼동하지 않는다.
9. P3에서는 원인을 단정하지 않는다. 원인 분석은 P4에서만.
10. crash/dump는 L1SW Log Analyzer 전담이다. RCA KG는 crash case를 만들지 않는다.

키워드 SSOT
11. `{kg_root}/keywords.yaml`이 signature 단일 출처다. 키워드를 새로 지어내지 않는다. P6에서만 승인된 case 근거로 candidate → confirmed 승격.

진행줄
12. 모든 응답 끝에 진행 한 줄 + 다음 행동 안내 한 줄을 붙인다.
```text
[진행: <끝낸 단계> 완료 → 다음: <다음 단계>. <요약>]
▶ 다음: <다음 P단계>를 자동 진행 (또는 사람 확인 필요 시 그 항목)
```

---

## 2. 호출과 자동 진입

`/root-cause-analyzer` 또는 자연어 진입 시:

1. `current_run.yaml`과 `NEXT_STEP_5.5.md`를 읽어 현재 상태를 확인한다.
2. 상태가 INIT이거나 첫 실행이면 **P0(환경 진단)**부터 시작한다.
3. 진행 중이면 `next_step`이 가리키는 단계를 이어서 자동 수행한다("이어서"라고만 해도 된다).
4. 사용자가 특정 단계를 지정하면 그 단계로 점프한다.

사람이 줄 최소 입력은 대개 없다(자동 추천·자동 선택). 사람 확인이 필요한 지점에서만 멈춘다(아래 §3 각 단계의 `[사람 확인]`).

---

## 3. P0~P6 워크플로우

각 단계 상세는 `references/`에 있다. 스킬은 `current_run.yaml`의 `next_step`에 따라 다음 단계를 자동으로 이어 수행하되, 각 단계의 `[사람 확인]` 지점에서는 멈추고 한 줄로 묻는다.

```text
P0  환경 진단 + current_run.yaml 초기화           references/p0_env_probe.md
 └ C0  _l1sw.txt 확보 분기 (없을 때만)            references/c0_secure_l1sw.md
P1  _l1sw.txt 출력 형식 역설계                     references/p1_format_probe.md
P2  L1SW manifest fragment 후보 생성              references/p2_manifest_fragments.md
P3  issue_type 추천 + signal 생성                 references/p3_signal.md
P4  원인분석 7단계 + case YAML 생성/갱신           references/p4_rca_and_case.md
P5  자가점검 + 승인 정규화                         references/p5_review.md
P6  keywords candidate → confirmed 승격          references/p6_keywords_promote.md
```

P4 원인분석의 추론 규칙(증상 anchor, cptime 시간창, 가설 2~4개, 인과사슬 작성, confidence 산정)은 `references/methodology.md`를 따른다.

issue_type별 단서표(trigger signatures, required evidence, 정상경로 대비 이탈 지점)는 `references/seeds/<issue_type>_analyzer.md`를 P3~P5에서 부품으로 참조한다.

상태 전이:
```text
INIT → P0 → (C0) → P1 → P2 → P3 → P4 → P5 → P6 → (다음 로그는 P3부터)
```
P2까지는 환경/형식 준비(보통 1회). 실제 로그마다 반복되는 본 루프는 P3 → P4 → P5 → P6다.

---

## 4. current_run.yaml 계약 (요약)

각 단계가 읽고 쓰는 핵심 필드:

```text
workspace_root            ← KG 루트 절대경로. P0가 확정. 모든 rca_kg/ 경로의 기준.
current_step, next_step, last_updated_kst
input.selected_l1sw_txt, input.l1sw_txt_candidates, input.selected_sdm
l1sw.parse_ps1, l1sw.manifest_dir
p1.output_format_doc, p1.cptime_format, p1.module_field_format
p2.generated_fragments, p2.review_log
p3.selected_issue_type, p3.signal_file
p4.case_file | p4.unresolved_file, p4.root_cause_category, p4.confidence,
   p4.candidate_signatures_for_p6, p4.extraction_attempt_count, p4.unknown_module_guard
p5.approved, p5.approved_at_kst, p5.review_status
p6.promoted_signatures, p6.review_log
```

상세 스키마는 `{kg_root}/runtime_tool_generate/current_run.example.yaml`을 참조한다.

---

## 5. reference 파일 안내

필요한 단계의 파일만 읽는다(progressive disclosure).

| 파일 | 언제 |
|---|---|
| `references/p0_env_probe.md` | 진입·환경 진단 |
| `references/c0_secure_l1sw.md` | `_l1sw.txt` 없을 때 |
| `references/p1_format_probe.md` ~ `p6_keywords_promote.md` | 각 단계 |
| `references/methodology.md` | P4 원인분석 추론법 |
| `references/seeds/*.md` | issue_type별 단서 (P3~P5) |

deepdive 원문(`prompt/deepdive/*`), scripts(`scripts/*`), 지식그래프(`rca_kg/*`)는 패키지에 그대로 있고, 스킬은 이를 부품으로 참조한다. 레거시 P0~P6 프롬프트(`prompt/CLAUDE_CODE_PROMPTS_e2e_v1.md`)는 스킬 미설치 환경용으로 보존된다.
