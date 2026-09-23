# Job-list v0.3.89 미동작 원인 확인 프롬프트

## 목적

회사 복귀 후 `job-list v0.3.89`이 자동 업데이트되었지만
CL-AIT HLD Quality Upgrade Job이 수행되지 않았을 경우,
사내 환경의 실제 파일과 실행 상태를 기준으로 원인을 확인한다.

중요:
- **분석만 수행한다.**
- 파일 수정, queue 재등록, Job 재실행, version 변경, cleanup, scheduler/dispatcher 설치를 하지 않는다.
- 추측하지 말고 실제 파일/로그/상태값만 확인한다.
- 답변은 아래 객관식 번호만 사용한다.
- 여러 항목을 확인한 뒤 마지막에 최종 원인을 1개 선택한다.

---

## 확인 대상

가능하면 아래 항목을 순서대로 확인한다.

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

# Q1. 실제 설치된 job-list 버전

다음 중 하나를 선택한다.

1. `0.3.89`
2. `0.3.88`
3. `0.3.87` 이하
4. VERSION / release metadata 간 버전 불일치
5. 확인 불가

---

# Q2. v0.3.89 package metadata 정합성

다음 파일을 비교한다.

```text
VERSION
.skill-release.json
skillsilent/manifest.json
```

1. 모두 `0.3.89`로 일치
2. 일부만 `0.3.89`
3. 모두 다른 버전
4. 파일 일부가 없음
5. 확인 불가

---

# Q3. bundled one-shot request 상태

`requests/one-shot-jobs.json`을 확인한다.

특히 다음을 실제 값으로 확인한다.

```text
job_id
profile
expires_at
```

선택:

1. request 존재 + 현재 시각 기준 유효
2. request 존재 + `expires_at` 만료
3. request 존재 + 동일/과거 `job_id` 재사용 가능성 있음
4. request는 존재하지만 profile/필드가 비정상
5. request 파일 없음
6. 확인 불가

---

# Q4. activation 결과

`data/state/activation/latest.json`의 해당 CL-AIT Job outcome을 확인한다.

1. `QUEUED`
2. `EXPIRED`
3. `DUPLICATE_SKIPPED`
4. `TARGET_MISMATCH`
5. `REJECTED`
6. 해당 Job 기록 없음
7. activation 파일 없음
8. 확인 불가

---

# Q5. queue 등록 여부

`data/state/core/queue.json`에서 CL-AIT HLD Quality Upgrade Job을 확인한다.

1. 현재 queue에 존재
2. queue에 없음
3. queue 파일 없음
4. 확인 불가

---

# Q6. processed history

`data/state/core/processed.jsonl`에서 동일 `job_id` 또는 해당 CL-AIT HLD Job을 검색한다.

가장 최근 상태를 선택한다.

1. `SUCCESS`
2. `FAILED`
3. `EXPIRED`
4. `SUPERSEDED`
5. `OUTPUT_MISSING`
6. `TIMEOUT`
7. `DUPLICATE` 또는 duplicate 계열
8. 관련 기록 없음
9. processed 파일 없음
10. 확인 불가

---

# Q7. 실제 Job 실행 시작 여부

다음을 확인한다.

```text
data/state/core/running.json
output/core/last_run.json
output/core/logs/
```

1. 실제 실행 시작 흔적 있음
2. queue에는 들어갔지만 실행 시작 흔적 없음
3. queue에도 없고 실행 흔적도 없음
4. 실행 시작 후 중단/실패 흔적 있음
5. 관련 파일 없음
6. 확인 불가

---

# Q8. CL-AIT HLD Quality Upgrade 결과 파일

다음을 확인한다.

```text
output/cl_ait_hld_quality_upgrade/latest_result.json
```

1. 존재 + SUCCESS
2. 존재 + FAILED
3. 존재 + PARTIAL / QUALITY GATE 실패
4. 존재하지만 stale/과거 실행 결과
5. 파일 없음
6. 확인 불가

---

# Q9. HLD 위치 탐색 단계까지 진입했는지

`latest_result.json`, 실행 로그 또는 transcript에서
Common / NR / LTE HLD 탐색 결과를 확인한다.

1. Common / NR / LTE 모두 탐색 성공
2. 일부만 탐색 성공
3. HLD history discovery 실패
4. HLD 탐색 단계 전에 Job 종료
5. 해당 결과 없음
6. 확인 불가

---

# Q10. OpenCode 실행 단계

실행 로그에서 OpenCode 호출 여부를 확인한다.

1. OpenCode 정상 시작
2. OpenCode 시작했으나 오류 종료
3. OpenCode timeout
4. OpenCode permission/input 대기
5. OpenCode 호출 전에 종료
6. OpenCode 관련 기록 없음
7. 확인 불가

---

# Q11. 최종 원인 분류

위 결과를 종합해서 가장 가까운 원인 하나만 선택한다.

1. **Skill Updater 미적용**
   - 실제 설치 버전이 v0.3.89가 아님

2. **Version / package metadata 불일치**
   - updater는 일부 적용됐으나 package 정합성이 깨짐

3. **one-shot request 만료**
   - `expires_at` 때문에 activation에서 `EXPIRED`

4. **동일 Job ID 재사용**
   - 기존 queue/processed 기록 때문에 `DUPLICATE_SKIPPED`

5. **request/profile validation 문제**
   - `REJECTED` 또는 schema/profile 오류

6. **target 조건 문제**
   - `TARGET_MISMATCH`

7. **queue 등록 후 worker가 실행하지 않음**
   - activation은 `QUEUED`지만 실제 runtime 시작 없음

8. **Job runtime 자체 실패**
   - worker 실행 후 FAILED / TIMEOUT / OUTPUT_MISSING

9. **OpenCode 실행 문제**
   - OpenCode error / timeout / permission 대기

10. **HLD history discovery 문제**
    - 기존 Common / NR / LTE HLD 위치 자동 탐색 실패

11. **HLD Quality Gate 실패**
    - Job/OpenCode는 수행됐으나 Class Diagram / MSC / traceability gate 미충족

12. **정상 수행됨**
    - 실제 결과는 SUCCESS이며 사용자가 결과 위치만 확인하지 못한 상태

13. **증거 부족**
    - 필요한 파일/로그가 부족해서 원인을 확정할 수 없음

---

# 응답 형식

**설명문을 먼저 쓰지 말고 아래 형식만 사용한다.**

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
```

예:

```text
Q1=1
Q2=1
Q3=2
Q4=2
Q5=2
Q6=3
Q7=3
Q8=5
Q9=4
Q10=5
Q11=3
```

위 예시는 형식 예시일 뿐이며 실제 답으로 사용하지 않는다.

---

## 추가 규칙

- `Q11`은 반드시 **하나의 번호만** 선택한다.
- 실제 증거가 서로 충돌하면 `Q11=13`을 선택한다.
- 과거 로그를 현재 실행 결과로 오인하지 않는다.
- `latest_result.json`의 timestamp/job_id/version을 확인하여 stale 여부를 판단한다.
- `processed.jsonl`에서는 동일 `job_id`의 가장 최근 기록을 우선한다.
- `requests/one-shot-jobs.json`의 `expires_at`은 현재 사내 PC 시각과 비교한다.
- 이 확인 과정에서 어떤 파일도 수정하지 않는다.
