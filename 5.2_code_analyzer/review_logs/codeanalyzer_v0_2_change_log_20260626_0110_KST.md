# Review Log — CodeAnalyzer Standalone v0.2 변경 이력

생성: 2026-06-26 01:10 KST

---

## 1. 반영 배경

v0.1 검토 결과 사용자 편의성, 동작 가능성, 토큰 소모 관점에서 다음 문제가 확인되었다.

```text
1. Track B 저장 경로와 Track A Phase 0 탐색 경로가 이원화될 수 있음
2. extraction 방식 상태값이 문서별로 혼재될 가능성이 있음
3. resume key로 사용할 진행줄이 산문형이라 안정성이 낮음
4. Windows 환경에서 bash 의존성이 큼
5. CNF handler를 단일로 가정함
6. Track B grep 결과가 과다해질 수 있음
7. 실행용 copy prompt가 없어 매번 reference prompt 전체를 붙여넣게 됨
```

---

## 2. v0.2 핵심 수정

### 2.1 경로 통일

모든 경로를 아래로 통일했다.

```text
artifacts/5.2/<slug>/
```

폐기:

```text
%USERPROFILE%\artifacts\code_analyzer\<slug>\
artifacts\code_analyzer\<slug>\
```

### 2.2 enum 통일

```text
extraction_mode: git | bash | powershell | internal_search | mixed
```

### 2.3 진행줄 통일

```text
[진행: PHASE0_DONE → 다음: PHASE1_PROCEDURE_DISCOVERY]
```

---

## 3. 추가 파일

```text
schema/structure.schema.md
schema/analysis_progress.schema.md
prompt/copy_track_b.md
prompt/copy_phase0.md
prompt/copy_phase1.md
prompt/copy_next_procedure.md
prompt/copy_resume.md
prompt/copy_phase_f.md
```

---

## 4. 검증 결과

패키지 내부 텍스트에서 폐기 경로 표현을 제거했다. 단, review log에서 폐기 경로를 설명하기 위해 언급한 경우는 예외다.

```text
canonical path: artifacts/5.2/<slug>/
```

---

## 5. 2026-06-26 01:16 KST 추가 흡수

v0.2 확정 전 런타임 토큰 누수 방지 항목을 추가로 흡수했다.

```text
1. analysis_progress.md의 전역 confirmed call edges 누적 본문 블록 제거
2. Phase 1 procedure_runtime_index 도입
3. Phase 2..N structure json 반복 read 차단
4. MSC 저장 방식을 별도 .puml 파일로 통일
5. structure 자동 탐색 우선순위를 focused 우선 / full 300KB 이하로 제한
6. reference prompt 런타임 read 차단 문구 추가
```

상세 변경은 아래 로그를 참조한다.

```text
review_logs/codeanalyzer_v0_2_token_runtime_fix_20260626_0116_KST.md
```
