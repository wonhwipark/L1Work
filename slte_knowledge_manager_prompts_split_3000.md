# SLTE Knowledge Manager 활용 프롬프트 모음

아래 프롬프트는 각각 독립적으로 복사해 사용할 수 있다.  
대상 기준: 1770/1800 CL을 1900 SLTE에 반영할 때 추가 수정·HE 필요 여부 판단을 위한 승인 지식 관리.

---

## 1. 초기 L1 기준 지식 등록

```text
slte-knowledge-manager를 사용해서 1900 SLTE L1 기준 지식을 점검하고 필요한 항목을 Candidate로 만들어줘.

L1 직접 관심 경로:
- HEDGE/**
- LTESAE/LteL1/**
- SMPF/L1/**

인접 참고 경로:
- LTESAE/LteL2/**
- LTESAE/LteL3/**

다음 기본 규칙의 기존 등록 여부를 먼저 조회해줘.
- branch: 1900
- scenario: SLTE
- path: LTESAE/LteL1/**
- runtime_usage_class: BUILT_BUT_NOT_USED
- slte_relevance: RELEVANT
- he_decision: NEED_TO_CHECK_HE
- replacement_lookup_required: true
- need_1900_patch: ADDITIONAL_CHANGE_REQUIRED

동일 규칙이 APPROVED 상태로 존재하면 중복 Candidate를 만들지 말고 rule ID와 적용 범위를 보여줘.
없거나 PARTIAL이면 신규 Candidate를 만들어줘.
기존 규칙과 충돌하면 자동 선택하지 말고 충돌 규칙, selector, decision 차이를 표로 보여줘.

LTESAE/** 또는 SMPF/** 전체를 L1 범위로 확장하지 마.
파일·클래스 예외가 이미 있으면 폴더 기본 규칙과 함께 표시해줘.
최종 승인 전에는 APPROVED로 승격하지 마.

출력:
1. 조회 상태
2. 기존 rule ID
3. 생성된 Candidate
4. 충돌·예외
5. 승인 시 실제 Impact 판정에 미치는 영향
```

---

## 2. 대표 L1 build option 등록

```text
slte-knowledge-manager를 사용해서 아래 build option을 1900 L1 대표 옵션 지식으로 등록해줘.

옵션명: <OPTION_NAME>
적용 branch: 1900
적용 scenario: SLTE
관련 경로: <알고 있으면 입력, 없으면 UNKNOWN>
관련 기능 또는 책임: <알고 있으면 입력, 없으면 UNKNOWN>

사용자 확인 내용:
- 이 옵션은 1900 L1에서 사용한다.
- 확인하지 못한 의미는 추정하지 않는다.

코드 확인 요청은 아래 중 입력된 범위만 수행해줘.
- 확인 파일: <FILE_PATH 또는 없음>
- 확인 API/함수: <SYMBOL 또는 없음>
- 코드에서 사용하는 define: <DERIVED_DEFINE 또는 없음>
- 파생 변수: <DERIVED_VARIABLE 또는 없음>
- 파생 API: <DERIVED_API 또는 없음>

처리 규칙:
1. 파일과 API가 없으면 OPTION_NAME_ONLY Candidate로 등록한다.
2. 파일만 있으면 해당 파일 내부만 확인한다.
3. 파일과 API가 있으면 해당 API 본문과 직접 둘러싼 조건·대입·호출만 확인한다.
4. 다른 파일, 전체 호출 그래프, 전체 CMake 구조로 자동 확장하지 않는다.
5. 옵션명과 코드 define·변수·API 이름이 다를 수 있으므로 검색 실패를 미사용으로 단정하지 않는다.
6. derived_define, derived_variable, derived_api와 derivation_chain은 단계별 검증 상태를 분리한다.
7. 확인되지 않은 단계는 CANDIDATE, AMBIGUOUS 또는 NOT_FOUND로 남긴다.
8. runtime ACTIVE, build inclusion, HE 판단은 근거 없이 확정하지 않는다.
9. 자동 승인하지 말고 Candidate와 근거를 보여준다.

출력:
- option Candidate
- 직접 참조 위치
- derived 관계와 각 검증 상태
- 미확정 항목
- 승인 요청 요약
```

---

## 3. 경로·파일·클래스·책임 지식 추가

```text
slte-knowledge-manager를 사용해서 아래 정보를 포팅 판단 지식 Candidate로 정리해줘.

대상 종류: <PATH / FILE / CLASS / API / RESPONSIBILITY>
대상 값: <경로·파일·클래스·API·책임 ID>
branch: 1900
scenario: SLTE

사용자 확인 사실:
<확인한 사실을 입력>

가능한 판정 정보:
- runtime_usage_class: <ACTIVE / BUILT_BUT_NOT_USED / UNKNOWN>
- slte_relevance: <RELEVANT / NOT_RELEVANT / UNKNOWN>
- he_decision: <NEED_TO_CHECK_HE / NO_NEED_TO_HE / REVIEW_REQUIRED>
- need_1900_patch: <ADDITIONAL_CHANGE_REQUIRED / NO_ADDITIONAL_CHANGE / REVIEW_REQUIRED>
- replacement target: <SMPF/L1 경로·클래스·API 또는 UNKNOWN>
- responsibility_id: <예: TX.ACTIVATION_SEQ 또는 UNKNOWN>

우선 기존 APPROVED 규칙을 조회해줘.
동일 identity가 있으면 직접 수정하지 말고 clone-for-update와 supersedes 방식으로 Candidate를 만들어줘.
폴더 규칙보다 구체적인 파일·클래스 규칙은 예외로 표시하되, 범위가 겹친다는 이유만으로 자동 우선 적용하지 말고 selector 구체성과 충돌 여부를 보여줘.
책임 지식은 source와 target을 분리하고, 단순 이름 유사성으로 replacement를 확정하지 마.
현재 CL 하나에만 해당하는 일회성 사실이면 영구 지식 등록 대신 validation case 또는 evidence로 제안해줘.

출력:
1. 기존 매칭 규칙
2. 신규 또는 갱신 Candidate
3. 적용 범위
4. 폴더 기본 규칙과의 관계
5. replacement·responsibility 상태
6. 승인 전 확인할 항목
```

---

## 4. 기존 지식 충돌·누락·노후화 점검

```text
slte-knowledge-manager의 1900 SLTE L1 지식을 점검해줘.

점검 범위:
- HEDGE/**
- LTESAE/LteL1/**
- SMPF/L1/**
- 대표 L1 build option
- derived_define / derived_variable / derived_api
- responsibility와 source→target replacement

다음을 찾아줘.
1. 동일 identity의 중복 APPROVED 규칙
2. 같은 범위에서 runtime_usage_class, he_decision, need_1900_patch가 충돌하는 규칙
3. LTESAE/LteL1/** 기본 강제 규칙을 약화시키는 파일·클래스 예외
4. replacement target이 없거나 KNOWLEDGE_MISS인 책임
5. PARTIAL, AMBIGUOUS, STALE 상태의 derived chain
6. branch 또는 scenario selector가 빠진 규칙
7. 근거가 사용자 확인뿐인데 코드 위치까지 확정한 규칙
8. deprecated 규칙이 아직 조회되는 문제
9. L2/L3 또는 SMPF 비L1 경로에 잘못 확장된 L1 규칙

자동 삭제·자동 승인·자동 충돌 해결은 하지 마.
각 문제마다 rule ID, selector, 현재 decision, 문제 이유, 권장 조치를 표로 보여줘.
갱신이 필요하면 clone-for-update Candidate를 제안하고 기존 rule을 즉시 변경하지 마.
Impact Analyzer에서 HE NOT NEEDED 오판을 일으킬 가능성이 있는 항목을 별도 표시해줘.

마지막에 우선 처리할 항목을 필수/권장/보류로 구분해줘.
```

---

## 5. 분석 스킬용 지식 조회

```text
slte-knowledge-manager를 사용해서 아래 분석 대상에 필요한 승인 지식만 조회해줘.

분석 목적: <IMPACT / ISSUE / L1_SAM_FIX>
branch: 1900
scenario: SLTE
변경 또는 원인 후보 경로:
<PATH 목록>

클래스·API 후보:
<SYMBOL 목록 또는 없음>

관련 build option:
<OPTION 목록 또는 없음>

조회 우선순위:
1. 정확한 파일·클래스·API 예외
2. LTESAE/LteL1/** 강제 폴더 규칙
3. responsibility와 replacement
4. build option 및 derived chain
5. 일반 경로·컴포넌트 지식

반환 시 raw rule 전체를 길게 출력하지 말고 다음만 정규화해서 보여줘.
- status: RESOLVED / PARTIAL / NO_MATCH / CONFLICTED / STALE / OUT_OF_SCOPE
- matched rule IDs
- deciding rule ID
- runtime_usage_class
- he_decision
- need_1900_patch
- replacement_lookup_required
- replacement target
- derived chain과 검증 상태
- review_required_reason

Knowledge 조회 실패, 충돌, PARTIAL 상태를 NO_NEED_TO_HE 또는 NO_ADDITIONAL_CHANGE로 변환하지 마.
확인되지 않은 정보는 UNKNOWN 또는 REVIEW_REQUIRED로 유지해줘.
저사양 모델을 고려해 파일별 상세 원문 대신 rule ID와 근거 위치만 출력하고, 한 번의 조회로 처리해줘.
```

---

## 6. 중단 후 이어서 진행

```text
slte-knowledge-manager의 이전 작업을 이어서 진행해줘.

이전 output 또는 state 경로:
<OUTPUT_OR_STATE_PATH>

처리 규칙:
- 완료된 조회·검증·Candidate 생성 단계는 다시 수행하지 않는다.
- 기존 Candidate와 동일 identity의 중복 Candidate를 만들지 않는다.
- Knowledge version이 변경된 경우 영향받는 조회 단계만 다시 수행한다.
- 지정 파일·API 코드 확인은 이전 evidence가 유효하면 재사용한다.
- 중단 시점 이후 단계부터 Python 결정형 pipeline으로 진행한다.
- 질문은 최종 승인에 필요한 항목만 한 번에 모아서 제시한다.
- PARTIAL, CONFLICTED, STALE 상태를 자동 승인하지 않는다.
- 기존 APPROVED 규칙을 직접 덮어쓰지 않는다.

출력:
1. 재사용한 단계
2. 다시 수행한 단계
3. 현재 Candidate 상태
4. 남은 승인 항목
5. 다음 실행 없이 현재 완료 가능한 결과
```
