# 프롬프트 2 — manifest 5.2 보강 자동화 설계·구현 (issue-analyzer v0.4)

- **확정 조합**: 1-b (l1sw 베이스 유지) / 2-b (스크립트 자동 생성) / 3-b (사람 승인) / 4-a (suffix 유지)
- **성격**: 검증이 아니라 설계·구현
- **실행 시점**: 프롬프트 1 완료 이후, 아래 선행 조건 충족 시
- **세션**: 프롬프트 1과 반드시 분리된 신규 세션

## 선행 조건 (모두 충족돼야 실행 의미 있음)

1. 프롬프트 1 완료 → manifest에 l1sw fragment 7개가 채워져 있음 (보강할 베이스 존재)
2. 5.2 output이 v0.9.8로 재추출됨 → structure.json에 `msg_symbol` 필드 실재
   (1차 판정표 V1-4가 "v0.9.8 미만 N/A"였으므로, 구버전 output이면 재추출 먼저)
3. 실사용에서 l1sw regex만으로 커버 안 되는 모듈이 생겨 보강 동기가 있음

> 급하지 않다. 프롬프트 1의 성패와 독립적으로 나중에 진행 가능.

---

## 붙여넣을 프롬프트 본문

```
당신은 스킬 설계·구현가다. 목적: issue-analyzer manifest에 5.2 code-analyzer의
msg_symbol 기반 regex 후보를 "증분 보강"하는 절차를 설계·구현한다 (v0.4).
아래 4개 결정은 이미 확정됐다. 재논의하지 말고 이 제약 안에서만 설계한다.

[확정 제약]
- 범위: l1sw 복사본을 베이스로 유지한다. 전체 재생성 아님. 5.2 심볼로 증분 보강만. (1-b)
- 생성: 스크립트가 5.2 structure.json의 msg_symbol을 읽어 regex 후보를 자동 생성. (2-b)
- 승인: 자동 채택 금지. 후보를 numbered 목록으로 제시하고 사용자가 번호로 채택/기각. (3-b)
- 파일명 규약: output_suffix "_l1sw" 및 <stem>_l1sw.txt 는 절대 변경하지 않는다. (4-a)

[불변 원칙 — COPY_FRAGMENTS.md 근거, 위반 금지]
- regex를 임의로 새로 만들지 않는다. 5.2 코드 근거(msg_symbol)가 있는 것만 후보가 된다.
- _meta.json 은 수정하지 않는다.
- 기존 l1sw 유래 regex는 삭제/변경하지 않는다. 오직 추가만 한다.

STEP 1 — 입력 계약 확정
- 5.2 output에서 msg_symbol을 어디서 읽는지 file_group별 structure.json 경로 규칙을 표로.
- msg_symbol 필드가 없는 구버전 bundle(v0.9.8 미만) 입력 시 처리(스킵+경고).

STEP 2 — regex 후보 생성 규칙
- msg_symbol(런타임 로그 문자열 심볼) → fragment regex 변환 규칙을 정의.
  (print 매크로 출력 문자열이 대상. AST 소스 아님.)
- 어느 fragment(.json 7개 중)로 귀속시킬지 분류 기준.
- 이미 존재하는 regex와 중복 판정 방법 (중복은 후보에서 제외).

STEP 3 — 승인 UI (3-b)
- 후보를 이렇게 제시:
  | # | 귀속 fragment | 후보 regex | 근거 msg_symbol (file:line) | 기존 중복 여부 |
- 사용자는 채택할 번호만 회신. 미선택은 기각으로 처리.

STEP 4 — 적용 및 기록
- 채택된 regex만 해당 fragment.json에 append (기존 항목 보존).
- 보강 이력을 manifest/ 하위에 기록 (일자·소스 5.2 버전·채택 개수).
- output_suffix·_meta.json 불변 재확인.

STEP 5 — 산출물
- 스크립트(Python, ASCII-only) 1개 + 사용법 5줄.
- 설계상 미확정/보류 항목을 | # | 항목 | 확정에 필요한 것 | 표로.

먼저 STEP 1~2를 설계안으로 제시하고, 구현 전 사용자 확인을 받는다.
(설계 승인 전 코드 작성 금지.)
```

---

## 비고

- 마지막 두 줄("설계 승인 전 코드 작성 금지")은 자동 생성(2-b)이라도 첫 설계를 사람이 검토하게 하는 게이트다. 한 번에 구현까지 원하면 그 두 줄을 삭제하면 된다.
- 5.2 skill 버전이 v0.9.8이어도, 중요한 건 **그 skill로 뽑은 output(structure.json)에 msg_symbol이 실제로 들어있는지**다. 구버전 output이 남아 있으면 후보 0개가 나온다.
