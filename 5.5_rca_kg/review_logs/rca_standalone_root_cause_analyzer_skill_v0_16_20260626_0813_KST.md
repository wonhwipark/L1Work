# Review Log — RCA Standalone v0.16 (root-cause-analyzer 스킬화)

생성: 2026-06-26 08:13 KST  
기준 패키지: RCA_standalone convenience_v0.15 (_5.5 + tool_generate)

---

## 1. 배경

5.2 CodeAnalyzer를 v0.5에서 `code-analyzer` 스킬로 승격한 것과 동일 컨셉을 5.5 RCA에 적용했다. P0~P6 프롬프트 묶음을 `root-cause-analyzer` 스킬로 만들었다.

사용자 결정:
```text
- 진행: 스킬 전체 생성 (추후 사용자 편의)
- 스킬명: root-cause-analyzer
- seeds: 스킬 안으로 흡수(복사)
```

P0 타이밍 질문 답: P0는 _l1sw.txt 생성 전 환경 진단 단계다. _l1sw.txt 유무를 보고 분기(있으면 P1, 없으면 C0로 L1SW 실행 안내). RCA가 L1SW를 직접 실행하지는 않는다.

---

## 2. 5.2 ↔ 5.5 스킬화 매핑

```text
5.2 copy_phase*           → 5.5 P0~P6 references
5.2 copy_session_bootstrap → 5.5 공통 운영 규칙 → SKILL.md §1
5.2 NEXT_STEP.current_slug → 5.5 current_run.yaml (이미 더 강력)
5.2 Track A/B 자동판별      → 5.5 P3 issue_type 자동추천 (이미 존재)
5.2 (없음)                 → 5.5 skills_seed → references/seeds
```

5.5가 5.2보다 스킬화에 유리했던 점: current_run.yaml로 상태가 이미 완성돼 있고, issue_type 자동추천(P3)이 이미 있어 자동판별을 새로 안 만들어도 됐다.

---

## 3. 생성한 스킬

```text
skills/root-cause-analyzer/
├── SKILL.md (133줄)
│   §0 입력 파이프라인 (.sdm→L1SW→_l1sw.txt→P0~P6), P0 타이밍 명시
│   §1 세션 불변 규칙 (상태 SSOT, 입력 편의, 자동전용영역, 분석 정직성, 키워드 SSOT, 진행줄)
│   §2 호출/자동 진입
│   §3 P0~P6 워크플로우 + 상태 전이
│   §4 current_run.yaml 계약
│   §5 reference 안내
└── references/
    ├── p0_env_probe.md, c0_secure_l1sw.md
    ├── p1_format_probe.md, p2_manifest_fragments.md, p3_signal.md
    ├── p4_rca_and_case.md (원인분석 7단계 + case YAML)
    ├── p5_review.md, p6_keywords_promote.md
    ├── methodology.md (P4 추론 요약 + deepdive SSOT 포인터)
    └── seeds/ (rach/scg/tx/l2 4종 + README)
```

설계 원칙:
- methodology는 deepdive 원문을 복제하지 않고 요약 + 포인터(SSOT 보존).
- seeds는 4종만 흡수, crash는 deprecated이고 RCA KG 대상이 아니라 제외. 원본 rca_kg/skills_seed/는 SSOT 유지.
- 분석 정직성 규칙(미지 모듈 가드, unresolved≠low, cptime 순서, crash 제외)을 SKILL.md §1에 강하게 보존.

---

## 4. 문서/스크립트 갱신

```text
START_HERE_5.5.md   §1 스킬 기반 순서표, §6 문서역할에 스킬 추가,
                    §7 스킬 설치(포함본 복사), §8 상세 사용법 신설
                    (전체 흐름/처음 시작/단계별 [사람 확인]/이어하기·반복/
                     분석 정직성/막혔을 때/레거시)
NEXT_STEP_5.5.md    스킬 호출 우선 + 레거시 폴백
VERSION_5.5.md      v0.16 헤드라인
scripts/validate_package.ps1   required에 skills/root-cause-analyzer/SKILL.md 추가
```

---

## 5. 하위 호환 (미변경)

```text
- prompt/CLAUDE_CODE_PROMPTS_e2e_v1.md : 레거시 수동 P0~P6. 스킬 미설치 환경용으로 유지.
- prompt/deepdive/* : 방법론 SSOT 유지.
- rca_kg/* (schema, keywords, skills_seed, manifest_fragments, cases) : 유지.
- scripts/*_prefilter.ps1 등 : 유지.
- current_run.yaml 스키마/계약 : 유지.
```

---

## 6. 완료 기준

```text
- skills/root-cause-analyzer/SKILL.md 존재, frontmatter 유효, 133줄(<500).
- references 9개(P0~P6+C0+methodology) + seeds 4종 + README 존재. 전부 resolve.
- 공통 운영 규칙이 SKILL.md에 내장(부트스트랩 자동).
- P0 타이밍/L1SW 비자동실행이 SKILL.md에 명문화.
- 분석 정직성 규칙 보존.
- START_HERE §8 상세 사용법 존재.
- validate required에 스킬 추가.
- 제어문자 0. 레거시 P0~P6 보존.
```

---

## 7. 남은 미결

```text
1. 실제 _l1sw.txt 1건으로 스킬 E2E (P0 진단→P3~P6 루프, 미지 모듈 가드 동작 확인).
2. C0 L1SW 자동실행 수위 결정 (현재 "안내" 기본. 파라미터 확실 시만 실행).
3. skill-creator eval로 /root-cause-analyzer 트리거율 측정 후 description 튜닝(선택).
4. RCA 5.5 ↔ 5.2 code_ref 연결 계약 (첫 HLD 산출물 이후).
```
