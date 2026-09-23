# Skill Updater + Job-list v0.3.89 통합 미동작 진단 프롬프트

## 목적

회사 복귀 후 아래 상황을 진단한다.

- `skill-updater`가 실행되었는지
- `job-list v0.3.89`를 실제 신규 버전으로 감지/설치했는지
- 설치 후 Job-list activation을 호출했는지
- one-shot request가 queue에 등록되었는지
- worker가 실행되었는지
- OpenCode가 시작되었는지
- 기존 Common / NR / LTE HLD를 발견했는지
- PlantUML Class Diagram / MSC 보강이 실제 수행되었는지
- Quality Gate / backup / sync-back에서 실패했는지

최종 목적은
**Skill Updater 문제 / Job-list activation 문제 / queue-worker 문제 / OpenCode 문제 / HLD discovery 문제 / HLD 품질보강 문제**
중 어디에서 중단되었는지 명확히 분리하는 것이다.

---

# 중요 규칙

1. **READ-ONLY 진단만 수행한다.**
2. 파일 수정 금지.
3. queue 재등록 금지.
4. Job 재실행 금지.
5. version 변경 금지.
6. cleanup 금지.
7. Skill Updater 재실행 금지.
8. Job-list activate 수동 실행 금지.
9. scheduler / dispatcher 설치 또는 변경 금지.
10. 추측하지 말고 실제 파일/로그/상태값만 사용한다.
11. 과거 실행 결과를 현재 실행 결과로 오인하지 않는다.
12. timestamp / version / job_id를 반드시 함께 확인한다.
13. 답변은 마지막에 지정한 **숫자 객관식 형식만** 사용한다.

---

# 기준 버전

확인 대상:

```text
skill-updater v0.5.32
job-list v0.3.89
```

Job-list v0.3.89가 실제 설치되지 않았다면 그 사실 자체가 진단 결과다.

---

# 우선 확인 대상

가능한 실제 설치 경로에서 아래 파일을 찾는다.

## Skill Updater

```text
VERSION
.skill-release.json
update_result.json
latest_result.json
logs/
output/
```

Skill Updater 결과 파일명이 다르면
실제 코드/설정에서 update 결과를 기록하는 파일을 찾아 사용한다.

특히 아래 정보를 확인한다.

```text
target = job-list
result_status
installed_version
remote_version
previous_version
new_version
job_sync.status
job_sync.detail
job_sync.returncode
job_sync.stdout_tail
job_sync.stderr_tail
```

---

## Job-list

```text
VERSION
.skill-release.json
skillsilent/manifest.json

requests/one-shot-jobs.json

data/state/activation/latest.json
data/state/core/queue.json
data/state/core/processed.jsonl
data/state/core/running.json

output/core/last_run.json
output/core/logs/

output/cl_ait_hld_quality_upgrade/latest_result.json
```

파일이 없으면 "없음" 자체를 결과로 기록한다.

---

# STEP A. Skill Updater 자체 확인

## Q1. Skill Updater가 실제 실행되었는가?

1. 이번 자동 업데이트 시각에 실행 기록 있음
2. 실행 기록은 있으나 과거 기록뿐임
3. 실행 기록 없음
4. 로그/결과 파일이 없어 확인 불가

---

## Q2. Skill Updater 실행 모드는 무엇인가?

1. 실제 update/install 모드
2. check / dry-run / scan-only 모드
3. mode 값이 비정상 또는 알 수 없음
4. 확인 불가

---

## Q3. Skill Updater가 `job-list`를 대상 스킬로 인식했는가?

1. 대상에 `job-list` 포함
2. 대상 목록에는 있으나 skip됨
3. 대상 목록에 `job-list` 없음
4. 대상 목록 확인 불가

---

## Q4. Skill Updater가 감지한 Job-list 버전 관계

다음 중 하나를 선택한다.

1. installed < remote, 즉 update 필요로 판단
2. installed == remote, 즉 no version change
3. installed > remote
4. installed/remote 중 하나 이상 읽기 실패
5. version format/parsing 오류
6. 확인 불가

---

## Q5. Skill Updater의 `job-list` update 결과

실제 result_status를 가장 가까운 항목으로 선택한다.

1. `UPDATED`
2. `SKIPPED_NO_VERSION_CHANGE`
3. `NOT_AVAILABLE`
4. `FAILED`
5. `FAILED_NONBLOCKING`
6. `SKIPPED`
7. `CHECK_ONLY`
8. 다른 상태
9. 관련 기록 없음
10. 확인 불가

---

## Q6. Job-list 실제 설치 버전

다음을 함께 확인한다.

```text
job-list/VERSION
job-list/.skill-release.json
job-list/skillsilent/manifest.json
```

1. 모두 `0.3.89`
2. 일부만 `0.3.89`
3. 모두 `0.3.88`
4. `0.3.87` 이하
5. 서로 다른 버전으로 불일치
6. 파일 일부 또는 전체 없음
7. 확인 불가

---

# STEP B. Skill Updater → Job-list 후처리 확인

## Q7. Skill Updater의 Job-list post-update sync/activation 상태

`job_sync.status` 또는 이에 대응하는 실제 필드를 확인한다.

1. `CALLED`
2. `SKIPPED_NO_VERSION_CHANGE`
3. `NOT_AVAILABLE`
4. `FAILED_NONBLOCKING`
5. `FAILED`
6. post-update activation 자체가 호출되지 않음
7. 해당 필드/기록 없음
8. 확인 불가

---

## Q8. post-update activation 호출의 return code

1. return code = 0
2. return code != 0
3. timeout
4. process launch 자체 실패
5. return code 기록 없음
6. 확인 불가

---

## Q9. post-update activation stderr/stdout에서 가장 가까운 상태

1. 정상 activation/queue 관련 출력
2. version/no-change 관련 skip
3. request 파일 없음
4. profile 없음
5. schema/validation 오류
6. permission/access 오류
7. Python/runtime 실행 오류
8. timeout
9. 다른 오류
10. 출력 없음
11. 확인 불가

---

# STEP C. Job-list request 확인

## Q10. `requests/one-shot-jobs.json` 존재 여부

1. 존재
2. 파일 없음
3. 존재하지만 JSON parse 실패
4. 확인 불가

---

## Q11. CL-AIT HLD one-shot request 존재 여부

1. 존재
2. request 파일은 있으나 해당 Job 없음
3. 중복/여러 개 존재
4. 확인 불가

---

## Q12. one-shot request의 profile

1. `cl-ait-hld-quality-upgrade-windows`
2. 다른 profile
3. profile 필드 없음
4. 확인 불가

---

## Q13. one-shot request의 `expires_at`

현재 사내 PC 시각과 실제 비교한다.

1. expires_at 없음
2. expires_at 존재 + 아직 유효
3. expires_at 존재 + 이미 만료
4. timezone 해석 불명확
5. 필드 형식 오류
6. 확인 불가

---

## Q14. one-shot request의 `job_id` 중복 가능성

`queue.json`, `processed.jsonl`, activation history에서 동일 ID를 찾는다.

1. 동일 job_id 과거 기록 없음
2. 동일 job_id가 queue에 이미 있음
3. 동일 job_id가 processed에 이미 있음
4. queue와 processed 양쪽에 있음
5. 동일 ID 확인 불가

---

# STEP D. Job-list activation 결과

## Q15. `data/state/activation/latest.json` 존재 여부

1. 이번 실행 시각 기준 최신 파일 존재
2. 존재하지만 과거 실행 결과
3. 파일 없음
4. parse 실패
5. 확인 불가

---

## Q16. 해당 CL-AIT Job activation outcome

1. `QUEUED`
2. `EXPIRED`
3. `DUPLICATE_SKIPPED`
4. `TARGET_MISMATCH`
5. `REJECTED`
6. `SUPERSEDED`
7. 다른 상태
8. 해당 Job 기록 없음
9. 확인 불가

---

# STEP E. Queue / worker 확인

## Q17. `data/state/core/queue.json` 상태

1. 해당 Job 현재 queue에 존재
2. queue 파일은 있으나 해당 Job 없음
3. queue 파일 없음
4. queue JSON parse 오류
5. 확인 불가

---

## Q18. `data/state/core/processed.jsonl`에서 해당 Job의 최신 상태

1. `SUCCESS`
2. `FAILED`
3. `EXPIRED`
4. `SUPERSEDED`
5. `OUTPUT_MISSING`
6. `TIMEOUT`
7. duplicate 계열
8. 다른 상태
9. 관련 기록 없음
10. processed 파일 없음
11. 확인 불가

---

## Q19. `data/state/core/running.json`

1. 해당 Job 현재 RUNNING
2. running 파일은 있으나 해당 Job 없음
3. stale RUNNING 기록
4. running 파일 없음
5. parse 오류
6. 확인 불가

---

## Q20. worker가 실제 해당 Job을 시작했는가?

다음을 종합한다.

```text
running.json
last_run.json
output/core/logs/
processed.jsonl
```

1. 실제 시작함
2. queue에는 들어갔지만 시작 흔적 없음
3. 시작했으나 즉시 실패
4. 시작 후 timeout
5. 시작 여부 확인 불가

---

# STEP F. Job runtime / OpenCode 확인

## Q21. `output/core/last_run.json`

1. 이번 CL-AIT Job 실행 결과 존재
2. 파일은 있으나 다른 Job
3. stale/과거 결과
4. 파일 없음
5. parse 오류
6. 확인 불가

---

## Q22. CL-AIT HLD job wrapper 시작 여부

1. wrapper 시작 확인
2. wrapper 시작 전에 종료
3. wrapper 시작했으나 초기 validation 실패
4. 관련 로그 없음
5. 확인 불가

---

## Q23. OpenCode 호출 여부

1. OpenCode 정상 시작
2. OpenCode process launch 실패
3. OpenCode 시작 후 non-zero 종료
4. OpenCode timeout
5. OpenCode permission/input 대기
6. OpenCode binary/path 문제
7. OpenCode 호출 전에 Job 종료
8. OpenCode 관련 기록 없음
9. 확인 불가

---

# STEP G. HLD discovery 확인

## Q24. HLD history discovery 결과

기존 Job-list/OpenCode history에서 HLD 위치를 탐색했는지 확인한다.

1. discovery 성공
2. discovery 실행했으나 실패
3. discovery 전에 Job 종료
4. discovery 관련 기록 없음
5. 확인 불가

---

## Q25. Common / NR / LTE HLD 탐색 결과

1. Common / NR / LTE 모두 성공
2. Common만 성공
3. NR만 성공
4. LTE만 성공
5. Common + NR
6. Common + LTE
7. NR + LTE
8. 모두 실패
9. 확인 불가

---

## Q26. 선택된 HLD가 실제 서로 다른 coherent set인가?

1. Common / NR / LTE 각각 정상 파일
2. 일부 경로가 중복/동일 파일
3. 일부 파일이 존재하지 않음
4. coherent set validation 실패
5. 확인 불가

---

# STEP H. Staging / HLD 보강 확인

## Q27. transient staging 생성 여부

1. staging 정상 생성
2. staging 생성 실패
3. source HLD copy 실패
4. staging 관련 기록 없음
5. 확인 불가

---

## Q28. 기존 HLD 기준 보강 모드 확인

1. 기존 Common / NR / LTE HLD를 읽고 augment/update 수행
2. 신규 HLD 생성 모드로 잘못 동작
3. 일부 HLD만 augment
4. 보강 단계까지 진입하지 못함
5. 확인 불가

---

## Q29. Common HLD PlantUML 결과

1. Class Diagram >= 1, MSC >= 1 모두 만족
2. Class Diagram만 만족
3. MSC만 만족
4. 둘 다 미달
5. Common HLD 작업 미수행
6. 확인 불가

---

## Q30. NR HLD PlantUML 결과

1. Class Diagram >= 1, MSC >= 4 모두 만족
2. Class Diagram만 만족
3. MSC 일부만 존재
4. 둘 다 미달
5. NR HLD 작업 미수행
6. 확인 불가

---

## Q31. LTE HLD PlantUML 결과

1. Class Diagram >= 1, MSC >= 4 모두 만족
2. Class Diagram만 만족
3. MSC 일부만 존재
4. 둘 다 미달
5. LTE HLD 작업 미수행
6. 확인 불가

---

# STEP I. Quality Gate / sync-back 확인

## Q32. Quality Gate 결과

1. PASS
2. FAIL - PlantUML Class/MSC 부족
3. FAIL - code traceability 부족
4. FAIL - error/skip/release path 부족
5. FAIL - production source 변경 감지
6. FAIL - 기타
7. Quality Gate 미실행
8. 확인 불가

---

## Q33. autonomous repair pass

1. 필요 없었음
2. 1회 수행 후 PASS
3. 1회 수행했으나 FAIL
4. repair pass 자체 실패
5. repair 단계 없음/미실행
6. 확인 불가

---

## Q34. backup 결과

1. backup 성공
2. backup 실패
3. backup 단계 미도달
4. 확인 불가

---

## Q35. atomic sync-back 결과

1. sync-back 성공
2. sync-back 실패
3. Quality Gate 실패로 sync-back 차단
4. production source change 감지로 차단
5. sync-back 단계 미도달
6. 확인 불가

---

# STEP J. 최종 CL-AIT 결과

## Q36. `output/cl_ait_hld_quality_upgrade/latest_result.json`

1. 이번 실행 결과 + SUCCESS
2. 이번 실행 결과 + FAILED
3. 이번 실행 결과 + PARTIAL
4. 파일은 있으나 stale/과거 실행
5. 파일 없음
6. parse 오류
7. 확인 불가

---

# 최종 원인 분류

## Q37. 가장 직접적인 1차 원인

반드시 **하나만** 선택한다.

### Skill Updater 계층

1. **Skill Updater 자체가 실행되지 않음**
2. **Skill Updater가 check/dry-run으로만 실행됨**
3. **Skill Updater가 job-list를 대상에서 누락**
4. **Skill Updater가 v0.3.89를 새 버전으로 감지하지 못함**
5. **Skill Updater의 job-list 설치/교체 실패**
6. **Skill Updater post-update Job sync 호출 안 됨**
7. **Skill Updater post-update Job sync 실패/timeout**

### Job-list package / activation 계층

8. **Job-list 실제 설치 버전/metadata 불일치**
9. **one-shot request 파일 또는 request 누락**
10. **one-shot request 만료**
11. **동일 job_id 재사용으로 duplicate skip**
12. **request/profile/schema validation 실패**
13. **target mismatch**
14. **activation 결과 파일 자체가 생성되지 않음**

### Queue / worker 계층

15. **activation은 QUEUED지만 queue 반영 실패**
16. **queue 등록은 됐지만 worker 미실행**
17. **stale running/lock/state 때문에 실행 차단**
18. **worker runtime FAILED**
19. **worker TIMEOUT**
20. **OUTPUT_MISSING / 결과 수집 실패**

### OpenCode 계층

21. **OpenCode binary/path/launch 실패**
22. **OpenCode non-zero 종료**
23. **OpenCode timeout**
24. **OpenCode permission/input 대기**

### HLD discovery / content 계층

25. **HLD history discovery 실패**
26. **Common / NR / LTE HLD coherent set 탐색 실패**
27. **staging/copy 실패**
28. **기존 HLD augment 단계 실패**

### Quality / output 계층

29. **PlantUML Class Diagram / MSC Gate 실패**
30. **code traceability 또는 runtime path Gate 실패**
31. **production source 변경 감지로 sync-back 차단**
32. **backup 실패**
33. **atomic sync-back 실패**

### 정상/불확실

34. **정상 수행 완료 — SUCCESS**
35. **정상 수행됐으나 사용자가 결과 위치를 확인하지 못한 상태**
36. **과거/stale 로그만 있어 현재 실행 여부 판단 불가**
37. **증거 부족으로 원인 확정 불가**
38. **복수 원인이 있으나 가장 선행 원인을 특정할 수 없음**

---

# Q38. 문제 계층 분류

Q37의 원인이 속하는 계층 하나만 선택한다.

1. Skill Updater
2. Job-list package/version
3. Job-list activation/request
4. Queue/worker
5. OpenCode
6. HLD discovery/staging
7. HLD content/Quality Gate
8. backup/sync-back
9. 정상
10. 불명확

---

# Q39. 재실행 전에 수정이 필요한가?

1. 수정 없이 재실행 가능
2. Skill Updater 수정/설정 확인 필요
3. Job-list version/package 수정 필요
4. one-shot request re-arm 필요
5. job_id 변경 필요
6. expires_at 변경/제거 필요
7. queue/runtime state 정리 필요
8. OpenCode 환경 수정 필요
9. HLD path/history 정보 수정 필요
10. HLD Quality Gate 대응 필요
11. 원인 불명확하여 수정 판단 불가

주의:
이 질문은 "어떤 조치가 필요해 보이는지" 분류만 한다.
실제 수정이나 재실행은 하지 않는다.

---

# 최종 응답 형식

설명문, 표, 코드블록 설명을 추가하지 말고
**아래 형식 그대로 숫자만 채운다.**

```text
Q1=#
Q2=#
Q3=#
Q4=#
Q5=#
Q6=#
Q7=#
Q8=#
Q9=#
Q10=#
Q11=#
Q12=#
Q13=#
Q14=#
Q15=#
Q16=#
Q17=#
Q18=#
Q19=#
Q20=#
Q21=#
Q22=#
Q23=#
Q24=#
Q25=#
Q26=#
Q27=#
Q28=#
Q29=#
Q30=#
Q31=#
Q32=#
Q33=#
Q34=#
Q35=#
Q36=#
Q37=#
Q38=#
Q39=#
```

---

# 선택적 증거 코드

숫자 답변 뒤에 추가 설명은 금지한다.

단, 진단 신뢰도 확인을 위해 마지막에 아래 4줄만 추가할 수 있다.

```text
E1=<확인한 skill-updater 결과 파일 경로 또는 NONE>
E2=<확인한 job-list activation 파일 경로 또는 NONE>
E3=<확인한 processed/latest_result 파일 경로 또는 NONE>
E4=<가장 최근 관련 timestamp 또는 NONE>
```

예:

```text
Q1=1
Q2=1
...
Q37=10
Q38=3
Q39=6
E1=C:\\...\\skill-updater\\output\\update_result.json
E2=C:\\...\\job-list\\data\\state\\activation\\latest.json
E3=C:\\...\\job-list\\data\\state\\core\\processed.jsonl
E4=2026-09-23T20:10:31+09:00
```

위 값은 **형식 예시일 뿐이며 실제 답으로 사용하지 않는다.**

---

# 판정 우선순위

여러 문제가 동시에 발견되면 **가장 먼저 실행 흐름을 끊은 원인**을 Q37로 선택한다.

우선순위:

```text
Skill Updater 실행
→ version detection
→ install
→ post-update activation call
→ one-shot validation
→ activation
→ queue
→ worker
→ OpenCode
→ HLD discovery
→ staging
→ HLD augment
→ Quality Gate
→ backup
→ sync-back
```

예를 들어:

- updater가 v0.3.89를 설치하지 못했고 request도 만료되어 있다면
  → Q37은 updater 설치 실패를 선택한다.

- updater/activation은 정상이나 동일 job_id 때문에 duplicate skip이면
  → Q37은 duplicate skip을 선택한다.

- worker까지 실행됐지만 HLD discovery에서 실패했다면
  → Q37은 HLD discovery 실패를 선택한다.

- 모든 단계가 성공했는데 사용자가 결과를 못 찾은 경우
  → Q37은 정상 수행/결과 위치 확인 문제를 선택한다.

---

# 절대 금지

진단 중 다음 명령/동작은 수행하지 않는다.

```text
activate --launch
enqueue
retry
re-arm
install
update
cleanup
delete
reset
force
kill
scheduler 등록/변경
dispatcher 등록/변경
```

현재 상태 보존이 원인 분석보다 우선이다.
