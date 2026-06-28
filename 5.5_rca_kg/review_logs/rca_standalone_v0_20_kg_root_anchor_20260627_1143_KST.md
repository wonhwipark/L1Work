# RCA Standalone v0.20 — KG 루트 절대경로 고정 (rca_kg 위치 버그 수정)

작성: 2026-06-27 11:43 KST
대상: RCA_standalone (root-cause-analyzer 스킬)
base: convenience_v0.19_manifest_guard

---

## 1. 문제

`rca_kg/`가 RCA_standalone 패키지 루트가 아니라 분석 대상 `_l1sw.txt`의 상위 폴더에 생성됨. case YAML도 그 안에 누적됨.

근본 원인: 스킬 reference의 모든 산출물 경로가 상대경로 `rca_kg/...`로 적혀 있었음. 상대경로는 cwd 기준으로 해석되는데, Claude Code에서 특정 `_l1sw.txt`를 분석시키면 cwd가 그 로그 폴더로 잡혀 거기에 `rca_kg/`가 생성됨.

설계 결함:
- `current_run.yaml`에 `workspace_root` 필드는 있었으나 산출물 경로가 이 필드를 참조하지 않음 (계약과 동작 불일치).
- P0는 "작업 루트가 RCA_standalone인지 확인"만 하고, 아닐 때 절대경로 기준점을 강제 고정하는 로직이 없었음.

영향: KG가 로그 폴더마다 분산 생성 → "하나의 KG로 누적"이라는 설계 의도 붕괴. fingerprint 중복 감지(P4 PART B 6~7), signature 승격(P6)이 분산된 KG에서는 동작 불가.

## 2. 수정 (A 방식: workspace_root 절대경로 고정)

### SKILL.md §1
- KG 루트 불변 규칙 0a~0d 추가 (상태 SSOT 위에 배치 — 모든 경로의 기준이므로).
  - 0a: KG 루트 = `kg_root` 절대경로. `rca_kg/`가 유일한 누적 위치.
  - 0b: 패키지 마커 = `skill_manifest.yaml` + `rca_kg/` 동거 폴더. P0가 절대경로로 `workspace_root`에 저장.
  - 0c: 모든 `rca_kg/...`는 `{workspace_root}/rca_kg/...`로 해석. cwd 기준 금지.
  - 0d: `workspace_root` null이면 P0 먼저. 확정 전 산출물 생성 금지.
- §1.11 keywords.yaml 경로 anchor.
- §4 contract에 `workspace_root`를 최상단 필드로 명시.

### references/p0_env_probe.md
- P0-0 단계 신설 (P0의 첫 작업): 패키지 마커로 `workspace_root` 절대경로 확정 → 검증 → 저장.
  - cwd부터 상위로 마커 탐색 → 기존 workspace_root → 사용자 1회 입력 순.
  - 안전장치: cwd ≠ workspace_root인데 cwd 아래 `rca_kg/`가 있으면 경고 + 병합 가이드 안내. 자동 삭제·이동 금지.
- P0-1(기존 환경 진단)의 모든 `rca_kg/` 경로를 `{workspace_root}/rca_kg/`로 변경.
- P0 표 맨 위 행에 workspace_root 절대경로 명시. [사람 확인]에 workspace_root 확인 추가.

### references/p1~p6
- p1: format probe 산출 doc 경로 anchor.
- p2: manifest_fragments 출력 + review_log 경로 anchor.
- p3: signal 출력 경로 anchor.
- p4: PART B 도입부에 "case는 `{workspace_root}/rca_kg/cases/`에만 생성" 명문화. unresolved 경로 + index 경로 anchor.
- p5: cases/unresolved 탐색 경로 anchor.
- p6: keywords.yaml + review_log 경로 anchor.

### current_run.yaml / current_run.example.yaml
- `workspace_root` 의미 주석 추가. example에 절대경로 표기.

### STRUCTURE_FIX_GUIDE.md
- §6 신설: 잘못 생긴 KG 병합 절차.
  - fingerprint 미겹침 → 이동 / 겹침 → occurrence 합산 / keywords 누락분만 candidate 추가.
  - signals·indexes는 재생성 가능하므로 이동 불필요.
  - 겹치지 않는 case 이동 PowerShell 예시(겹침은 수동).

## 3. 비수정 (의도적 보존)

- `seeds/README.md`의 "원본 패키지 `rca_kg/skills_seed/`는 SSOT" 문구 — skills_seed 절대 경로 아님, 의미 보존.
- SKILL.md §5의 "지식그래프(`rca_kg/*`)는 패키지에 그대로 있고" — 일반 설명 narrative, 산출물 경로 아님.
- `scripts/*.ps1` prefilter — 산출물을 직접 쓰지 않음, 변경 불필요.

## 4. 검증

- control-byte 스캔(BEL 0x07 / VT 0x0B 등): clean, 검출 없음.
- 잔여 bare `rca_kg/` 경로 스캔: 마커 정의·kg_root 정의·narrative 3건만 남음(모두 의도적).
- 사용자 데이터 영향: 기존에 잘못 생긴 KG의 case YAML은 §6 절차로 정본에 병합 필요(사용자 수동 1회).

## 5. 후속

- E2E: 실 환경에서 P0-0가 사내 PC 경로 구조(회사 계정명, 테스트 폴더)에서 마커를 올바르게 찾는지 확인.
- 사용자 보고된 기존 잘못된 KG → 정본 병합 1회 수행 후 재발 없는지 확인.

## 6. 추가 (병합 보조 스크립트)

`scripts/compare_kg_cases.ps1` 신설. 잘못 생긴 KG와 정본 KG의 `cases/`를 fingerprint(signature_set 정렬 + sequence) 기준으로 대조해 NEW/DUP/SAMEID로 분류, 병합 계획 출력.

- 읽기 전용: 파일 이동·삭제·수정 안 함. 계획만 출력.
- 외부 YAML 모듈 의존 없음(자체 경량 파서로 case_id·signature_set·sequence·occurrence_count만 추출). 파서 로직은 EXAMPLE case로 검증 완료.
- `-IncludeUnresolved`: unresolved 함께 대조. `-MovePlan`: NEW 이동 명령 출력(실행 안 함).
- EXAMPLE* 파일은 대조에서 제외.
- STRUCTURE_FIX_GUIDE §6.3 첫 단계로 이 스크립트 호출 연결. scripts/README §6에 사용법 추가.
- control-byte 스캔 clean.
