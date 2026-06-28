# Review Log — CodeAnalyzer Standalone v0.3 (output 이동 + 깨짐 수정 + 토큰/편의 보강)

생성: 2026-06-26 08:13 KST  
기준 패키지: CodeAnalyzer_standalone v0.2 (20260626_0116_KST)

---

## 1. 반영 배경

v0.2 검토 결과, 동작에는 문제가 없으나 아래 3가지가 확인되었다.

```text
1. 산출물 루트 폴더명이 artifacts/ 라서 요청대로 output/ 으로 이동 필요
2. START_HERE 스킬 점검 블록에 BEL(0x07) 제어문자가 섞여 Test-Path 한 줄이 깨짐
3. analysis_progress schema 폐기필드 목록에 동일 줄이 중복됨
추가로 사용 편의/토큰 절감 여지 확인
```

---

## 2. 핵심 변경

### 2.1 산출물 경로 이동 — artifacts/ → output/

canonical path를 전면 변경했다.

```text
변경 전: artifacts/5.2/<slug>/
변경 후: output/5.2/<slug>/
```

- 폴더 `artifacts/` → `output/`, `artifacts_layout/` → `output_layout/` 로 rename.
- 모든 살아있는 문서의 경로 문자열을 `output/5.2/...` 로 일괄 치환.
- `artifacts/5.2/<slug>/` 는 각 폐기 경로 목록에 "v0.2 경로. v0.3에서 output/5.2/로 이동"으로 명시.
- review_logs 의 과거 기록은 history 보존을 위해 변경하지 않음.

마이그레이션은 폴더명 1회 이동으로 끝난다. 내용 계약(필드/schema/진행줄)은 그대로다.

```powershell
if (Test-Path .\artifacts\5.2) { Move-Item .\artifacts\5.2\* .\output\5.2\ -Force }
```

### 2.2 산출물 layout 권위를 스킬 쪽으로 단일화

요청("artifact를 스킬 내부로 이동")에 따라, 산출물 폴더 구조의 권위 문서를 하나로 모았다.

```text
- 산출물 구조는 스킬 staged-code-analyzer 가 소유한다.
- layout 단일 권위 문서: output/5.2/_example_slug/README.md
- START_HERE / 기타 문서는 layout을 복제하지 않고 위 문서를 참조한다.
```

### 2.3 BEL 제어문자 깨짐 수정 (동작 버그)

`START_HERE_5.2.md` 스킬 설치 점검 블록의 둘째 줄에 `\x07`(BEL)이 섞여 있어, 그대로 복사하면 PowerShell `Test-Path` 경로가 깨졌다.

```text
변경 전(깨짐): ...\.claude\skills<BEL>pi-callflow-analysis\SKILL.md
변경 후:       ...\.claude\skills\api-callflow-analysis\SKILL.md
```

겸사겸사 3줄 개별 Test-Path를 1개 블록 ALL_OK / MISSING 단일 체크로 단순화했다. 한 번 붙여넣으면 누락 스킬명을 바로 알려준다.

### 2.4 schema 중복 줄 정리

`schema/analysis_progress.schema.md` 폐기필드 목록의 동일 3줄을 1줄로 정리했다.

```text
변경 전:
  전역 call edge 누적 본문
  전역 call edge 누적 본문
  전역 call edge 본문 누적 블록
변경 후:
  전역 call edge 누적 본문 블록   # procedure별 local_call_edges로 대체
```

---

## 3. 사용 편의 / 토큰 절감 보강

### 3.1 세션 부트스트랩 prompt 신설 (입력 토큰 절감)

`prompt/copy_session_bootstrap.md` 추가.

```text
- 세션당 1회만 붙여넣어 공통 고정 규칙(경로/enum/진행줄/런타임 read 정책)을 한 번에 적용.
- 이후 단계 prompt에서 같은 규칙을 매번 길게 재기술하지 않아도 되어 입력 토큰 감소.
- reference prompt는 여전히 런타임에 읽지 않음.
```

START_HERE 순서표, NEXT_STEP, RUNTIME_TOKEN_POLICY, HANDOFF 시작점에 부트스트랩 단계를 반영.

### 3.2 단계 prompt는 자기완결성 유지

`copy_phase0/1/next/resume/phase_f`는 단독 붙여넣기로도 동작해야 하므로 핵심 규칙은 그대로 둔다. 부트스트랩은 "추가 단축 수단"이지 단계 prompt의 필수 선행이 아니다. (자기완결성과 토큰 절감 사이의 절충)

### 3.3 런타임 토큰 정책은 v0.2 그대로 유지

procedure_runtime_index 우선, structure json 반복 read 차단, 전역 call edge 누적 본문 금지, MSC 분리 .puml — v0.2 정책을 그대로 계승한다. v0.3은 여기에 손대지 않았다.

---

## 4. 수정/추가 파일

추가:

```text
prompt/copy_session_bootstrap.md
review_logs/codeanalyzer_v0_3_output_rename_20260626_0813_KST.md
```

이동(rename):

```text
artifacts/        → output/
artifacts_layout/ → output_layout/
```

수정:

```text
VERSION_5.2.md                 # v0.3 헤드라인 + 버전 표기
START_HERE_5.2.md              # output 경로, 마이그레이션, BEL 수정, 부트스트랩, layout 권위 참조
NEXT_STEP_5.2.md               # 부트스트랩 안내, output 경로
HANDOFF_5.2.md                 # Decision 0(v0.3) 추가, 부트스트랩 시작점, output 경로
RUNBOOK_BLOCK_TO_HLD_5.2.md    # output 경로
RUNTIME_TOKEN_POLICY_5.2.md    # 부트스트랩 문서화, output 경로
reference/master_v0.40_section_5_2.md
prompt/5.2_track_a_prompt.md
prompt/5.2_track_b_prompt.md
prompt/copy_track_b.md
prompt/copy_phase0.md
prompt/copy_phase1.md
prompt/copy_next_procedure.md
prompt/copy_resume.md
prompt/copy_phase_f.md
output_layout/analysis_progress_5.2.template.md
schema/structure.schema.md
schema/analysis_progress.schema.md
output/5.2/_example_slug/README.md
```

미변경(history 보존):

```text
review_logs/codeanalyzer_v0_2_change_log_20260626_0110_KST.md
review_logs/codeanalyzer_v0_2_token_runtime_fix_20260626_0116_KST.md
```

---

## 5. 완료 기준

```text
- canonical path가 output/5.2/<slug>/ 로 전면 통일됨
- 살아있는 문서에 artifacts/5.2 canonical 참조가 남아있지 않음 (폐기/마이그레이션 표기만 존재)
- 패키지 어디에도 BEL(0x07) 제어문자가 없음
- 스킬 점검이 ALL_OK / MISSING 단일 체크로 동작함
- schema 폐기필드 중복 줄 제거됨
- output layout 권위 문서가 output/5.2/_example_slug/README.md 로 단일화됨
- copy_session_bootstrap.md 가 세션 1회 공통 규칙으로 정의됨
- v0.2 런타임 토큰 정책(index 우선/edge 누적 금지/MSC 분리)이 그대로 유지됨
```

---

## 6. 남은 미결 (v0.2에서 계승)

```text
1. 실제 사내 L1 코드 1개 블록 대상 E2E 검증 필요
2. RCA 5.5 root_cause.code_ref 연결 계약은 첫 HLD 산출물 이후 확정
3. Stage 분할 임계값은 실데이터로 조정
```
