# Job-list 실행 후 MCD 결과 확인 프롬프트

## 목적

회사 Linux PC에서 `skill-updater v0.5.28`이 `job-list v0.3.53`을 새 버전으로 설치한 뒤,
Job-list one-shot이 실제로 실행되었는지 확인하고,
MCD handoff audit 결과를 읽어서 **사용자가 사외에 손으로 전달할 수 있는 최소 결과**를 출력해줘.

이번 작업은 **확인/진단만 수행**한다.

- 파일 수정 금지
- Job 재실행 금지
- processed state 삭제 금지
- Skill 수정 금지
- Job-list 수정 금지
- Git/GitHub write 금지
- 임의 retry 금지

---

# 1. 기대 버전

먼저 현재 설치된 Job-list 버전을 확인해줘.

기대:

```text
job-list = 0.3.53
```

가능하면 아래 파일/메타데이터를 사용하되,
실제 패키지 구조에서 canonical version source를 우선 사용해줘.

```text
~/l1sw-private-skills/job-list/VERSION
~/l1sw-private-skills/job-list/.skill-release.json
~/l1sw-private-skills/job-list/SKILL.md
```

결과:

```text
A. 0.3.53 설치됨
B. 다른 버전 설치됨
C. 버전 확인 불가
```

---

# 2. 대상 One-shot Job

이번 확인 대상 Job ID:

```text
JOB-20260829-MCD-HANDOFF-AUDIT-02
```

Profile:

```text
l1-sam-fixer-mcd-handoff-audit
```

Platform:

```text
linux
```

---

# 3. Job activation 결과 확인

우선 아래 파일을 확인해줘.

```text
~/l1sw-private-skills/job-list/data/state/activation/latest.json
```

대상 Job ID를 찾아 다음 중 하나로 판정해줘.

```text
A. QUEUED / LAUNCHED
B. DUPLICATE_SKIPPED
C. TARGET_MISMATCH
D. REJECTED
E. 해당 Job 기록 없음
F. activation 파일 없음
```

가능하면 대상 Job의 실제 status/reason을 그대로 짧게 함께 표시해줘.

---

# 4. Job observer 결과 확인

아래 파일을 확인해줘.

```text
~/l1sw-private-skills/job-list/data/state/observer/latest_result.json
```

가능하면 다음 정보를 출력:

```text
job_id
status
job_status
execution_status
quality_status
reason_codes
artifact_count
user_action_required
```

`observer-result/v1`이 없는 구형 결과라면,
없는 필드는 임의 추측하지 말고 `N/A`로 표시해줘.

---

# 5. MCD Audit 결과 파일 확인

아래 두 결과를 확인해줘.

## JSON

```text
~/l1sw-private-skills/job-list/data/state/mcd_handoff_audit_result.json
```

## MD

```text
~/l1sw-private-skills/job-list/output/mcd_handoff_audit_latest.md
```

각 파일에 대해:

```text
A. 존재
B. 없음
```

으로 표시하고,
존재하면 실제 absolute path도 출력해줘.

---

# 6. Audit 결과 추출

결과가 존재하면 다음 정보를 추출해줘.

## Q1 — MCD CSV 방향 열

```text
A = from / to
B = SourceFile / TargetFile
C = 다른 실제 header
D = 확인 불가
```

가능하면 실제 사용된 column:

```text
SRC=<actual source column>
DST=<actual target column>
```

도 표시.

---

## Q2 — `MCD-<hash>` 노출 범위

```text
A = 개선 포인트 보고서만
B = MCD 보고서 전반
C = mcd-compare에도 존재
D = 확인 불가
```

---

## Q3 — CSV mapping profile

```text
A = 있음
B = 없음
C = 확인 불가
```

---

## MCS CSV

파일명에 `mcs`가 포함된 CSV 검색 결과를 확인해줘.

검색 규칙:

```text
case-insensitive
recursive
extension = .csv
filename contains "mcs"
```

결과:

```text
MCS_COUNT=<number>
```

가능하면 파일명만 최대 10개 보여줘.

**절대경로 전체를 외부 전달용 한 줄에는 넣지 말 것.**

---

# 7. 중요 오류/경고

Audit 결과에서 가장 중요한 reason/error가 있으면 아래 우선순위로 대표 1개를 선택해줘.

예:

```text
MCD_EDGE_COLUMNS_UNRESOLVED
MCD_EDGE_COLUMNS_NONCANONICAL
MAPPING_PROFILE_CONFLICT
MCD_HASH_SCOPE_UNRESOLVED
CSV_SCAN_FAILED
AUDIT_PARTIAL
NONE
```

실제 결과에 다른 reason code가 있으면 실제 값을 우선해도 된다.

추측해서 새 reason code를 만들지 말 것.

---

# 8. 외부 전달용 1줄

최종적으로 반드시 아래 형식의 **한 줄**을 출력해줘.

```text
MCD45: Q1=<A|B|C|D> SRC=<name|NA> DST=<name|NA> Q2=<A|B|C|D> Q3=<A|B|C> MCS=<count> ERR=<reason|NONE>
```

예:

```text
MCD45: Q1=C SRC=src_path DST=dst_path Q2=B Q3=A MCS=7 ERR=MCD_EDGE_COLUMNS_NONCANONICAL
```

Audit 결과가 전혀 없더라도 가능한 정보로 한 줄을 만들어줘.

예:

```text
MCD45: Q1=D SRC=NA DST=NA Q2=D Q3=C MCS=0 ERR=AUDIT_RESULT_MISSING
```

단, `AUDIT_RESULT_MISSING`은 실제 reason code가 없을 때
**사용자 전달용 상태 표현**으로만 사용하고 내부 reason code로 저장하지 말 것.

---

# 9. 실제 MCD 보고서가 있으면 추가 확인

이 Job은 기본적으로 **MCD handoff audit**이므로,
실제 MCD 보고서 재생성이 필수 동작은 아니다.

다만 기존 또는 최신 MCD report artifact가 명확히 존재하면
읽기 전용으로 다음만 추가 확인해줘.

```text
cycle_members empty 여부
dependency_edges empty 여부
MCD-<hash> 사용자 제목 노출 여부
ANALYSIS_REQUIRED 개수
UNRESOLVED 개수
CODE_FACT / CODE_VERIFIED / TOPOLOGY_INFERRED 존재 여부
```

실제 보고서를 찾기 위해 repository 전체를 무제한 검색하지 말 것.

우선 아래 범위만 확인:

```text
~/l1sw-private-skills/l1-sam-fixer/output/
~/l1sw-private-skills/l1-sam-fixer/data/
```

최신 결과가 명확하지 않으면:

```text
MCD_REPORT_CHECK=SKIPPED_NOT_UNAMBIGUOUS
```

로 끝내줘.

---

# 10. 결과 파일이 없을 때 최소 진단

`mcd_handoff_audit_latest.md` 또는 JSON이 없으면
다음 순서만 확인해줘.

```text
1. activation/latest.json
2. observer/latest_result.json
3. processed.jsonl에서 대상 job_id 검색
4. Job-list output directory 존재 여부
```

processed history 경로 후보:

```text
~/l1sw-private-skills/job-list/data/state/core/processed.jsonl
```

다음 중 하나로 원인을 요약:

```text
A. Job이 실행되지 않음
B. Duplicate skip
C. Platform mismatch
D. Profile/validation reject
E. Job 실행됐으나 output 생성 실패
F. 판단 불가
```

**processed state를 삭제하거나 Job을 다시 실행하지 말 것.**

---

# 11. 최종 출력 형식

아래 형식으로만 간결하게 정리해줘.

```text
[Job-list]
A/B/C. 버전 상태

[Activation]
A/B/C/D/E/F. 상태
- 실제 status:
- reason:

[Observer]
- status:
- job_status:
- execution:
- quality:
- reasons:
- artifacts:
- user_action:

[MCD Audit]
- JSON: 존재/없음
- MD: 존재/없음
- Q1:
- SRC:
- DST:
- Q2:
- Q3:
- MCS_COUNT:
- ERR:

[MCD Report Check]
- cycle_members:
- dependency_edges:
- hash title:
- evidence:
- unresolved:
또는
MCD_REPORT_CHECK=SKIPPED_NOT_UNAMBIGUOUS

[판정]
A. 정상 수행 + Audit 결과 정상
B. 정상 수행 + 사용자 확인 필요
C. Job 미수행
D. Job 실패
E. 결과 파일 생성 실패
F. 추가 확인 필요

[사외 전달용]
MCD45: Q1=... SRC=... DST=... Q2=... Q3=... MCS=... ERR=...
```

---

# 12. 최우선 원칙

이번 확인의 목적은
**"왜 실패했을 가능성이 있는지 최대한 많이 의심하는 것"이 아니라,
실제로 남아 있는 state/result를 근거로 빠르게 성공 여부를 확인하는 것**이다.

따라서:

```text
명확한 실패 증거가 없으면 실패로 단정하지 말 것.
불필요한 prerequisite check를 추가하지 말 것.
읽기 전용 확인만 수행할 것.
```

최종적으로 사용자가 사외에 전달해야 하는 것은
가능하면 마지막 `MCD45:` 한 줄이면 충분해야 한다.
