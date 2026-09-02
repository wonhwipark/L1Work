# L1-FLA Daily 1회 테스트 수행 프롬프트

아래 작업을 **Linux PC에서 직접 수행**해줘.

## 목표
autotask-builder에 등록된 `l1_fla_daily` task를 스케줄 시간까지 기다리지 않고 **1회 수동 실행**하고,
Jira title 제외 규칙(`[FLA-SKIP]`)이 정상 적용되는지 확인한다.

## 중요 조건
- Job-list는 사용하지 않는다.
- 기존 `l1_fla_daily` 등록 설정은 변경하지 않는다.
- task를 새로 만들지 않는다.
- 현재 등록된 task를 그대로 1회 실행한다.
- 실제 분석 실행이다.
- 실패 시 임의 수정하지 말고 원인만 정리한다.
- 기존 L1-FLA 영구 설정과 기존 skip list는 삭제/초기화하지 않는다.

## 1. 설치/등록 상태 확인

다음 경로가 존재하는지 확인해줘.

```text
~/l1sw-private-skills/autotask-builder/bin/autotask
~/l1sw-private-skills/autotask-builder/data/config/tasks/task_l1_fla_daily.yaml
~/l1sw-private-skills/l1-fla/bin/l1-fla-auto.py
```

그리고 autotask-builder의 현재 등록 상태를 확인해줘.

## 2. 오늘 Jira List 확인

오늘 날짜 기준 아래 패턴의 파일이 존재하는지 확인해줘.

```text
~/l1sw-private-skills/l1-fla/output/YYYYMMDD/jira_list_tx_MMDD.md
```

예:
```text
2026-09-02
→ ~/l1sw-private-skills/l1-fla/output/20260902/jira_list_tx_0902.md
```

다른 MD 파일은 분석 대상으로 선택하면 안 된다.

## 3. Jira title skip 설정 확인

아래 영구 파일을 확인해줘.

```text
~/l1sw-private-skills/l1-fla/data/config/exclude_jira_titles.md
```

다음 항목이 포함되어 있는지 확인해줘.

```text
[FLA-SKIP]
```

기존 다른 skip 항목은 그대로 유지해야 한다.

## 4. l1_fla_daily 1회 실행

autotask-builder에 등록된 다음 task를 **1회 수동 실행**해줘.

```text
task_l1_fla_daily.yaml
```

실행은 autotask-builder의 `run` 기능을 사용한다.

task 내부의 기대 흐름은 다음과 같다.

```text
L1-FLA preflight
  ↓ 성공 시
L1-FLA run --resume
  ↓
jira_list_tx_MMDD.md
  ↓
Jira 조회
  ↓
title skip 확인
  ↓
[FLA-SKIP] 대상은 분석 제외
  ↓
나머지 Jira만 로그 다운로드 / issue-analyzer 수행
```

preflight가 실패하거나 BLOCKED이면 본 분석을 강제로 실행하지 않는다.

## 5. 수행 결과 검증

실행 완료 후 오늘 L1-FLA output에서 다음 문자열을 검색해줘.

```text
analysis_skipped
jira_title_excluded
FLA-SKIP
```

### 정상 기대 결과

Jira title이 예를 들어:

```text
[FLA-SKIP] test issue
```

라면 해당 Jira는:

```text
fla_status = analysis_skipped
skip_reason = jira_title_excluded
```

또는 동일 의미의 결과로 기록되어야 한다.

그리고 해당 Jira에 대해서는:
- 로그 다운로드
- issue-analyzer 분석

이 수행되지 않아야 한다.

반대로 skip 대상이 아닌 Jira는 정상 분석되어야 한다.

## 6. 최종 보고

작업 완료 후 아래 형식으로만 간단히 보고해줘.

```text
[L1-FLA Daily 1회 테스트 결과]

1. autotask 등록 상태:
   - PASS / FAIL

2. 오늘 Jira List:
   - 파일:
   - jira_list_tx_MMDD.md 단독 선택 여부: PASS / FAIL

3. [FLA-SKIP] 영구 설정:
   - PASS / FAIL

4. preflight:
   - READY / BLOCKED / FAIL

5. l1_fla_daily 1회 실행:
   - PASS / FAIL

6. title skip 실제 동작:
   - PASS / FAIL / 확인대상없음

7. skip된 Jira:
   - Jira Key:
   - Jira Title:
   - skip_reason:

8. 정상 분석된 Jira:
   - Jira Key 목록:

9. 최종 판정:
   - 무인 정시운영 가능
   - 또는 수정 필요

10. 수정 필요 시:
   - 원인:
   - 수정 대상 스킬/파일:
```

## 금지
- 기존 task 삭제 금지
- 기존 profile 초기화 금지
- skip list 초기화 금지
- job-list 호출 금지
- 실패 원인을 숨기고 성공 처리 금지
