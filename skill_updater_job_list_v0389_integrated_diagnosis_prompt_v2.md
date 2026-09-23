# Skill Updater + Job-list v0.3.89 통합 미동작/진행중 진단 프롬프트

## 목적

회사 복귀 후 아래 상황을 READ-ONLY로 진단한다.

- `skill-updater`가 실제 실행되었는지
- `job-list v0.3.89`를 신규 버전으로 감지/설치했는지
- 설치 후 Job-list activation을 호출했는지
- one-shot request가 queue에 등록되었는지
- worker가 실행되었는지
- **현재 아직 RUNNING 중인지**
- OpenCode가 시작되었는지
- 기존 Common / NR / LTE HLD를 발견했는지
- 기존 HLD를 기준으로 내용 보강을 수행했는지
- PlantUML Class Diagram / MSC가 추가되었는지
- Quality Gate / backup / sync-back에서 실패했는지
- 정상 완료되었는지

최종 목적은 다음 중 어디에 해당하는지 명확히 분리하는 것이다.

```text
1. 아직 정상 진행 중
2. Skill Updater 문제
3. Job-list package/version 문제
4. Job-list activation/request 문제
5. queue/worker 문제
6. OpenCode 문제
7. HLD discovery/staging 문제
8. HLD content/Quality Gate 문제
9. backup/sync-back 문제
10. 정상 완료
11. 증거 부족
```

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
13. **현재 Job이 RUNNING이고 실패 증거가 없다면 장애로 분류하지 않는다.**
14. **RUNNING 상태에서는 `latest_result.json`이 없거나 미완성인 것이 정상일 수 있다.**
15. 답변은 마지막에 지정한 숫자 객관식 형식만 사용한다.

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

## Skill Updater

가능한 실제 설치 경로에서 아래를 확인한다.

```text
VERSION
.skill-release.json
update_result.json
latest_result.json
logs/
output/
```

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

Skill Updater 결과 파일명이 다르면
실제 코드/설정에서 update 결과를 기록하는 파일을 찾아 사용한다.

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

파일이 없으면 없는 상태 자체를 기록한다.

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

1. installed < remote, 즉 update 필요로 판단
2. installed == remote, 즉 no version change
3. installed > remote
4. installed/remote 중 하나 이상 읽기 실패
5. version format/parsing 오류
6. 확인 불가

---

## Q5. Skill Updater의 `job-list` update 결과

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

# STEP E. Queue / worker / 진행중 상태 확인

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

1. 실제 시작함 + 현재도 진행 중
2. 실제 시작함 + 이미 종료됨
3. queue에는 들어갔지만 시작 흔적 없음
4. 시작했으나 즉시 실패
5. 시작 후 timeout
6. 시작 여부 확인 불가

---

## Q21. 현재 상태가 "정상 진행 중"으로 판단되는가?

다음 조건을 종합한다.

정상 진행 중의 예:

```text
activation = QUEUED
AND
worker 시작 흔적 있음
AND
running = 현재 Job
AND
processed에 terminal failure 없음
AND
timeout 기준 미초과
```

선택:

1. 정상 진행 중
2. 실행 중이지만 이미 오류 징후 있음
3. 실행 종료됨
4. 실행 시작 전
5. stale RUNNING으로 의심
6. 판단 불가

**중요: Q21=1이면 이후 미완성 output을 장애로 해석하지 않는다.**

---

# STEP F. Job runtime / OpenCode 확인

## Q22. `output/core/last_run.json`

1. 이번 CL-AIT Job 실행 결과 존재
2. 파일은 있으나 다른 Job
3. stale/과거 결과
4. 파일 없음
5. parse 오류
6. 확인 불가

---

## Q23. CL-AIT HLD job wrapper 시작 여부

1. wrapper 시작 확인
2. wrapper 시작 전에 종료
3. wrapper 시작했으나 초기 validation 실패
4. 관련 로그 없음
5. 확인 불가

---

## Q24. OpenCode 호출 여부

1. OpenCode 정상 시작 + 현재 진행 중
2. OpenCode 정상 시작 + 종료됨
3. OpenCode process launch 실패
4. OpenCode 시작 후 non-zero 종료
5. OpenCode timeout
6. OpenCode permission/input 대기
7. OpenCode binary/path 문제
8. OpenCode 호출 전에 Job 종료
9. OpenCode 관련 기록 없음
10. 확인 불가

---

# STEP G. HLD discovery 확인

## Q25. HLD history discovery 결과

1. discovery 성공
2. discovery 현재 진행 중
3. discovery 실행했으나 실패
4. discovery 전에 Job 종료
5. discovery 관련 기록 없음
6. 확인 불가

---

## Q26. Common / NR / LTE HLD 탐색 결과

1. Common / NR / LTE 모두 성공
2. Common만 성공
3. NR만 성공
4. LTE만 성공
5. Common + NR
6. Common + LTE
7. NR + LTE
8. 아직 탐색 진행 중
9. 모두 실패
10. 확인 불가

---

## Q27. 선택된 HLD가 실제 서로 다른 coherent set인가?

1. Common / NR / LTE 각각 정상 파일
2. 아직 selection 진행 중
3. 일부 경로가 중복/동일 파일
4. 일부 파일이 존재하지 않음
5. coherent set validation 실패
6. 확인 불가

---

# STEP H. Staging / 기존 HLD 보강 확인

## Q28. transient staging 생성 여부

1. staging 정상 생성
2. staging 생성/복사 진행 중
3. staging 생성 실패
4. source HLD copy 실패
5. staging 관련 기록 없음
6. 확인 불가

---

## Q29. 기존 HLD 기준 보강 모드 확인

1. 기존 Common / NR / LTE HLD를 읽고 augment/update 수행
2. 현재 augment 진행 중
3. 신규 HLD 생성 모드로 잘못 동작
4. 일부 HLD만 augment
5. 보강 단계까지 진입하지 못함
6. 확인 불가

---

## Q30. Common HLD PlantUML 결과

1. Class Diagram >= 1, MSC >= 1 모두 만족
2. 현재 생성/보강 진행 중
3. Class Diagram만 만족
4. MSC만 만족
5. 둘 다 미달
6. Common HLD 작업 미수행
7. 확인 불가

---

## Q31. NR HLD PlantUML 결과

1. Class Diagram >= 1, MSC >= 4 모두 만족
2. 현재 생성/보강 진행 중
3. Class Diagram만 만족
4. MSC 일부만 존재
5. 둘 다 미달
6. NR HLD 작업 미수행
7. 확인 불가

---

## Q32. LTE HLD PlantUML 결과

1. Class Diagram >= 1, MSC >= 4 모두 만족
2. 현재 생성/보강 진행 중
3. Class Diagram만 만족
4. MSC 일부만 존재
5. 둘 다 미달
6. LTE HLD 작업 미수행
7. 확인 불가

---

# STEP I. Quality Gate / sync-back 확인

## Q33. Quality Gate 결과

1. PASS
2. 아직 Quality Gate 단계 전/진행 중
3. FAIL - PlantUML Class/MSC 부족
4. FAIL - code traceability 부족
5. FAIL - error/skip/release path 부족
6. FAIL - production source 변경 감지
7. FAIL - 기타
8. Quality Gate 미실행
9. 확인 불가

---

## Q34. autonomous repair pass

1. 필요 없었음
2. 현재 repair 진행 중
3. 1회 수행 후 PASS
4. 1회 수행했으나 FAIL
5. repair pass 자체 실패
6. repair 단계 없음/미실행
7. 확인 불가

---

## Q35. backup 결과

1. backup 성공
2. backup 진행 중
3. backup 실패
4. backup 단계 미도달
5. 확인 불가

---

## Q36. atomic sync-back 결과

1. sync-back 성공
2. sync-back 진행 중
3. sync-back 실패
4. Quality Gate 실패로 sync-back 차단
5. production source change 감지로 차단
6. sync-back 단계 미도달
7. 확인 불가

---

# STEP J. 최종 CL-AIT 결과

## Q37. `output/cl_ait_hld_quality_upgrade/latest_result.json`

1. 이번 실행 결과 + SUCCESS
2. 이번 실행 결과 + FAILED
3. 이번 실행 결과 + PARTIAL
4. 현재 Job RUNNING 중이며 최종 result 아직 없음
5. 파일은 있으나 stale/과거 실행
6. 파일 없음 + Job도 종료됨
7. parse 오류
8. 확인 불가

---

# 최종 상태 / 원인 분류

## Q38. 현재 전체 상태

반드시 **하나만** 선택한다.

1. **정상 진행 중 — 아직 완료 전**
2. Skill Updater 문제
3. Job-list package/version 문제
4. Job-list activation/request 문제
5. queue/worker 문제
6. OpenCode 문제
7. HLD discovery/staging 문제
8. HLD content/Quality Gate 문제
9. backup/sync-back 문제
10. 정상 완료
11. stale/과거 기록 때문에 판단 불가
12. 증거 부족

---

## Q39. 가장 직접적인 1차 원인

Q38=1(정상 진행 중) 또는 Q38=10(정상 완료)이면
아래의 진행/정상 코드를 선택한다.

### 진행/정상

1. **현재 정상 RUNNING 중**
2. **정상 SUCCESS 완료**
3. **정상 수행됐으나 사용자가 결과 위치를 확인하지 못한 상태**

### Skill Updater 계층

4. Skill Updater 자체가 실행되지 않음
5. Skill Updater가 check/dry-run으로만 실행됨
6. Skill Updater가 job-list를 대상에서 누락
7. Skill Updater가 v0.3.89를 새 버전으로 감지하지 못함
8. Skill Updater의 job-list 설치/교체 실패
9. Skill Updater post-update Job sync 호출 안 됨
10. Skill Updater post-update Job sync 실패/timeout

### Job-list package / activation 계층

11. Job-list 실제 설치 버전/metadata 불일치
12. one-shot request 파일 또는 request 누락
13. one-shot request 만료
14. 동일 job_id 재사용으로 duplicate skip
15. request/profile/schema validation 실패
16. target mismatch
17. activation 결과 파일 자체가 생성되지 않음

### Queue / worker 계층

18. activation은 QUEUED지만 queue 반영 실패
19. queue 등록은 됐지만 worker 미실행
20. stale running/lock/state 때문에 실행 차단
21. worker runtime FAILED
22. worker TIMEOUT
23. OUTPUT_MISSING / 결과 수집 실패

### OpenCode 계층

24. OpenCode binary/path/launch 실패
25. OpenCode non-zero 종료
26. OpenCode timeout
27. OpenCode permission/input 대기

### HLD discovery / content 계층

28. HLD history discovery 실패
29. Common / NR / LTE HLD coherent set 탐색 실패
30. staging/copy 실패
31. 기존 HLD augment 단계 실패

### Quality / output 계층

32. PlantUML Class Diagram / MSC Gate 실패
33. code traceability 또는 runtime path Gate 실패
34. production source 변경 감지로 sync-back 차단
35. backup 실패
36. atomic sync-back 실패

### 불확실

37. stale/과거 로그만 있어 현재 실행 여부 판단 불가
38. 증거 부족으로 원인 확정 불가
39. 복수 원인이 있으나 가장 선행 원인을 특정할 수 없음

---

## Q40. 문제 계층 분류

1. 현재 정상 진행 중
2. Skill Updater
3. Job-list package/version
4. Job-list activation/request
5. Queue/worker
6. OpenCode
7. HLD discovery/staging
8. HLD content/Quality Gate
9. backup/sync-back
10. 정상 완료
11. 불명확

---

## Q41. 지금 즉시 수정/재실행이 필요한가?

1. **아니오 — 현재 정상 진행 중이므로 기다려야 함**
2. 아니오 — 정상 완료
3. Skill Updater 수정/설정 확인 필요
4. Job-list version/package 수정 필요
5. one-shot request re-arm 필요
6. job_id 변경 필요
7. expires_at 변경/제거 필요
8. queue/runtime state 정리 필요
9. OpenCode 환경 수정 필요
10. HLD path/history 정보 수정 필요
11. HLD Quality Gate 대응 필요
12. 원인 불명확하여 수정 판단 불가

주의:
- 이 질문은 필요한 조치의 **분류만** 한다.
- 실제 수정이나 재실행은 하지 않는다.
- Q21=1이고 terminal failure 증거가 없으면 원칙적으로 Q41=1이다.

---

# RUNNING 판정 특별 규칙

아래 조건을 만족하면 실패가 아니라 **정상 진행 중**으로 우선 판정한다.

```text
activation = QUEUED
AND
worker 시작 흔적 있음
AND
running.json에서 현재 Job 확인
AND
processed.jsonl에 현재 Job의 FAILED/TIMEOUT/EXPIRED terminal state 없음
AND
허용 timeout을 초과하지 않음
```

이 경우:

```text
Q21=1
Q38=1
Q39=1
Q40=1
Q41=1
```

을 우선 사용한다.

그리고 아래 항목은 아직 완료 전이므로 장애 근거로 사용하지 않는다.

```text
latest_result.json 없음
PlantUML 개수 아직 부족
Quality Gate 미실행
backup 미실행
sync-back 미실행
```

단, 로그에 명백한 error/timeout/permission wait가 있으면 정상 진행 중으로 판정하지 않는다.

---

# 완료 판정 특별 규칙

정상 완료의 최소 조건:

```text
processed = SUCCESS
AND
latest_result = SUCCESS
AND
Quality Gate = PASS
AND
필요한 경우 sync-back = SUCCESS
```

이 경우:

```text
Q38=10
Q39=2
Q40=10
Q41=2
```

---

# 판정 우선순위

여러 문제가 동시에 발견되면 **가장 먼저 실행 흐름을 끊은 원인**을 Q39로 선택한다.

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

단, 현재 Job이 정상 RUNNING이면 후속 단계가 아직 미완료라는 이유로
실패 원인을 선택하지 않는다.

---

# 최종 응답 형식

설명문, 표, 추가 분석을 쓰지 말고
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
Q40=#
Q41=#
```

---

# 선택적 증거 코드

숫자 답변 뒤에 추가 설명은 금지한다.

다만 현재 결과가 어느 실행을 기준으로 한 것인지 확인하기 위해
아래 6줄만 추가할 수 있다.

```text
E1=<확인한 skill-updater 결과 파일 경로 또는 NONE>
E2=<확인한 job-list activation 파일 경로 또는 NONE>
E3=<확인한 queue/running 파일 경로 또는 NONE>
E4=<확인한 processed/latest_result 파일 경로 또는 NONE>
E5=<확인한 현재 job_id 또는 NONE>
E6=<가장 최근 관련 timestamp 또는 NONE>
```

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
