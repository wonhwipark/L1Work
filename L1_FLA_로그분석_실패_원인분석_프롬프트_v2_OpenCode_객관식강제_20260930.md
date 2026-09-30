# L1-FLA 로그분석 실패 원인분석 프롬프트 v2 — OpenCode 객관식 강제판

## 목적
현재 설치/실행 중인 L1-FLA에서 로그 분석이 실패한 원인을 실제 실행 증거를 기준으로 추적한다.

특히 다음을 구분한다.
- 실제 선택된 Analyzer
- Analyzer 존재/호출 가능 여부
- 로그 획득 실패
- 다운로드 실패
- SDM 변환/QB·binary 문제
- Analyzer invocation 실패
- timeout/stuck
- Provider/환경 문제
- fallback 수행 여부와 실패 이유

기본 Analyzer는 설정 파일에서 실제 값을 확인한 뒤 확정한다. 추측하지 않는다.

---

# 0. 최우선 인터랙션 규칙 — 반드시 준수

이 규칙은 아래 모든 지시보다 우선한다.

## 0.1 사용자에게 질문할 때는 숫자 객관식만 사용

추가 정보가 필요하면 반드시 아래 형식만 출력한다.

```text
[USER INPUT REQUIRED]

Q1. <질문>
1. <선택지>
2. <선택지>
3. <선택지>
4. 확인 불가 / 잘 모르겠음

Q2. <질문>
1. <선택지>
2. <선택지>
3. <선택지>
4. 확인 불가 / 잘 모르겠음

답변 형식:
1 3
```

사용자는 숫자만 입력하면 된다.

## 0.2 주관식 질문 금지

다음 형태는 절대 출력하지 않는다.

- 어떤 Run을 분석할까요?
- 경로를 알려주세요.
- Jira 번호를 입력해주세요.
- 로그 위치를 알려주세요.
- 어떤 환경인지 설명해주세요.
- 추가 정보를 제공해주세요.
- 어떤 스킬을 사용했나요?
- 에러 메시지를 알려주세요.

즉, 자유 입력을 요구하는 문장은 모두 금지한다.

## 0.3 경로/파일/Jira 번호가 필요해도 직접 입력을 요구하지 않는다

먼저 자동 탐색한다.

예:

```text
Q1. 분석 대상 Run을 선택하세요.
1. 20260930_183012
2. 20260930_174455
3. 20260929_231004
4. 가장 최근 실패 Run 자동 선택
```

자동 탐색에 실패해도 다음처럼 객관식으로 묻는다.

```text
Q1. Run을 자동 탐색하지 못했습니다. 다음 동작을 선택하세요.
1. 현재 작업 폴더 재탐색
2. HOME 기준 L1-FLA 영구 폴더 탐색
3. 최근 생성된 final_report.html 전체 탐색
4. 분석 종료
```

"직접 입력" 선택지는 만들지 않는다.

## 0.4 질문 턴에서 출력 가능한 내용

질문이 필요한 경우 다음만 출력한다.

1. `[USER INPUT REQUIRED]`
2. Q1~Q8 객관식 질문
3. 숫자 선택지
4. `답변 형식:`
5. 숫자 예시

질문 앞뒤에 설명 문장을 붙이지 않는다.

## 0.5 질문 직전 자체 점검

사용자에게 출력하기 전에 내부적으로 확인한다.

- 모든 질문에 숫자 선택지가 있는가?
- 자유서술 입력을 요구하는 문장이 없는가?
- "알려주세요 / 입력해주세요 / 설명해주세요 / 제공해주세요" 문장이 없는가?
- 사용자가 숫자만으로 응답 가능한가?

하나라도 아니면 응답을 다시 작성한다.

SELF-CHECK 내용은 사용자에게 출력하지 않는다.

---

# 1. 조사 원칙

1. 최신 실패 Run을 자동으로 찾는다.
2. 사용자에게 파일 위치를 먼저 묻지 않는다.
3. 현재 작업 폴더 → L1-FLA 영구 output → 최근 run 순으로 탐색한다.
4. 동일 날짜에 Run이 여러 개면 timestamp와 실패 Jira 수를 비교한다.
5. 자동 선택이 위험할 때만 객관식 질문을 한다.
6. final_report.html 문구만 보고 결론 내리지 않는다.
7. 최소 result.json 또는 run_state.json까지 교차 확인한다.
8. Analyzer 문제면 selection/preflight/invocation 결과를 확인한다.
9. 로그 획득 실패를 Analyzer 문제로 오판하지 않는다.
10. 실행 증거가 부족한 경우에만 소스코드를 본다.
11. 수정은 하지 않는다.
12. read-only 확인을 우선한다.

---

# 2. 자동 확인 항목

## A. FLA 실행 정보
- 버전
- OS
- interactive / unattended
- run id
- 시작/종료 시간
- 대상 Jira 수
- 성공/실패/skip 수

## B. 실패 Jira별
- Jira
- 최종 상태
- Failure Stage
- Failure Kind
- 선택 Analyzer
- Analyzer preset
- Provider
- Log acquisition owner
- Return code
- Timeout
- Fallback
- Failure reason
- 로그 실제 존재 여부
- SDM 변환 결과 존재 여부

## C. 우선 확인 파일
1. final_report.html
2. final_report.md
3. run_state.json
4. Jira별 result.json
5. Jira별 issue_detail.html
6. analyzer/preflight 로그
7. stdout/stderr
8. profile/config
9. analyzer registry
10. 필요한 경우에만 l1-fla 소스

---

# 3. 실패 단계 분류

반드시 아래 중 하나로 분류한다.

1. SOURCE_ACCESS
2. LOG_DISCOVERY
3. DOWNLOAD
4. SDM_CONVERSION
5. BUILD_BINARY
6. SKILL_UNAVAILABLE
7. ANALYZER_INVOCATION
8. ANALYZER_TIMEOUT
9. ANALYZER_RESULT
10. PROVIDER_INFRA
11. PATH_PERMISSION
12. FALLBACK_FAILURE
13. UNKNOWN

---

# 4. Analyzer 문제 확인 순서

1. 실제 선택 Analyzer
2. profile default_analyzer
3. target별 override
4. legacy analysis.skill
5. Analyzer registry
6. preflight 결과
7. skill 실제 존재/호출 가능 여부
8. provider/headless에서 호출 가능 여부
9. invocation command/prompt
10. return code
11. timeout
12. stderr/summary/limitations
13. fallback 대상
14. fallback 실제 수행 여부
15. fallback 실패 이유

설정에 문자열이 존재한다는 이유만으로 사용 가능하다고 판정하지 않는다.

---

# 5. 로그 획득 실패 확인 순서

1. Jira 본문/댓글 조회
2. Jira Remote Link 조회
3. 로그 위치 후보
4. source type
5. 다운로드 요청 수행 여부
6. 인증/권한 문제
7. 403/404/timeout/network
8. 다운로드됐지만 FLA가 못 찾은 것인지
9. output 폴더 실제 파일 존재 여부
10. 확장자/파일명 인식 문제
11. 다운로드 주체가 FLA인지 delegated analyzer인지
12. Analyzer 직접 다운로드 preset인지

---

# 6. 객관식 질문 생성 규칙

- 한 번에 최대 8문항
- 모든 문항은 숫자 선택형
- 기본 선택지는 1~4
- 마지막 선택지는 가능하면 `확인 불가 / 잘 모르겠음`
- 복수 선택은 `2,4`
- 여러 문항은 `1 3 2 1`
- 자유 입력 금지
- 필요한 후보는 먼저 자동 탐색 후 번호 부여

예시:

```text
[USER INPUT REQUIRED]

Q1. 분석할 실패 Run을 선택하세요.
1. 가장 최근 Run
2. 오늘 가장 최근 실패 Run
3. 실패 Jira가 가장 많은 최근 Run
4. 후보 Run 목록을 다시 탐색

Q2. 조사 범위를 선택하세요.
1. 실패 원인만 확인
2. 실패 원인 + 재발 조건
3. 실패 원인 + 최소 수정 방향
4. 전체 구조까지 점검

답변 형식:
1 3
```

---

# 7. 원인 판정 기준

## 확정
직접 증거 2개 이상이 일치.

예:
- result.json: failure_kind=SKILL_UNAVAILABLE
- preflight log: selected Analyzer unavailable

## 유력
직접 증거 1개 + 정황 증거 일치.

## 미확정
핵심 로그 부족 또는 증거 상충.

---

# 8. 최종 결과 형식

충분한 증거가 모이면 질문 없이 아래 형식으로 결과를 출력한다.

## 결론
- 실패 Jira:
- 실제 사용 Analyzer:
- 실패 단계:
- 실패 유형:
- 직접 원인:
- fallback:
- 판정 신뢰도: 확정 / 유력 / 미확정

## 핵심 증거
1.
2.
3.

## 실행 흐름
`Jira 조회 → 로그 탐색 → 다운로드 → SDM/QB 준비 → Analyzer 선택 → Analyzer 실행 → 결과 수집`

각 단계:
- PASS
- FAIL
- NOT_REACHED
- UNKNOWN

## 실제 중단 지점
- 단계:
- 마지막 정상 처리:
- 최초 실패:
- 이후 미실행 단계:

## Primary Cause
아래 중 정확히 하나:
1. SOURCE_ACCESS
2. LOG_DISCOVERY
3. DOWNLOAD
4. SDM_CONVERSION
5. BUILD_BINARY
6. SKILL_UNAVAILABLE
7. ANALYZER_INVOCATION
8. ANALYZER_TIMEOUT
9. ANALYZER_RESULT
10. PROVIDER_INFRA
11. PATH_PERMISSION
12. FALLBACK_FAILURE
13. UNKNOWN

## 재발 조건
- 동일 조건 재발 가능성:
- 영향 실행 방식:
- Windows/Linux 차이:
- unattended 영향:

## 최소 수정 방향
P0:
-

P1:
-

실제 파일은 사용자 승인 전 수정하지 않는다.

---

# 9. 최종 후속 선택도 반드시 객관식

최종 분석 뒤에는 아래만 추가한다.

```text
[NEXT ACTION]

1. 원인분석만 종료
2. P0 수정안 상세 검토
3. 실제 스킬 수정
4. 동일 실패 재현/검증 절차 작성
5. 다른 실패 Jira와 비교 분석

답변 형식:
1
```

---

# 10. 절대 금지

- HTML 문구 하나만 보고 원인 단정
- Analyzer 이름 추측
- l1-log-analysis가 항상 설치됐다고 가정
- timeout과 skill unavailable 혼동
- fallback 설정만 보고 실제 수행됐다고 가정
- 사용자 승인 없이 코드 수정
- 이미 로컬에 있는 파일을 다시 업로드하라고 요구
- 사용자에게 주관식 질문
- "직접 입력" 선택지 제공

---

# 시작 지시

지금부터 현재 환경의 L1-FLA 최신 실패 Run을 찾아 분석하라.

먼저 자동으로 확인 가능한 증거를 최대한 수집한다.

추가 사용자 정보가 꼭 필요한 경우에만 `[USER INPUT REQUIRED]` 형식의 숫자 객관식 질문을 출력한다.

사용자는 숫자만 입력하면 분석을 계속할 수 있어야 한다.

주관식 질문이 한 문장이라도 포함되면 해당 응답은 잘못된 응답으로 간주하고 객관식 형식으로 다시 작성한다.
