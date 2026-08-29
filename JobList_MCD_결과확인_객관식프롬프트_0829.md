# Job-list 실행 후 MCD 결과 확인 — 객관식 전용 프롬프트

## 목적

회사 Linux PC에서 `skill-updater v0.5.28`이 `job-list v0.3.53`을 설치한 뒤,
아래 대상 Job이 실제로 수행됐는지와 MCD Audit 결과를 **객관식 코드 중심으로만** 확인해줘.

대상 Job:

```text
JOB-20260829-MCD-HANDOFF-AUDIT-02
```

대상 Profile:

```text
l1-sam-fixer-mcd-handoff-audit
```

Platform:

```text
linux
```

---

# 0. 절대 원칙

이번 작업은 **읽기 전용 확인**만 수행한다.

금지:

```text
파일 수정
Job 재실행
processed state 삭제
Skill 수정
Job-list 수정
Git/GitHub write
임의 retry
추가 prerequisite 생성
```

명확한 실패 증거가 없으면 실패로 단정하지 말 것.

---

# 1. Job-list 버전 확인

현재 설치 버전을 확인한다.

기대 버전:

```text
0.3.53
```

출력은 아래 중 하나만 사용:

```text
Q0=A   # 0.3.53 설치됨
Q0=B   # 다른 버전 설치됨
Q0=C   # 버전 확인 불가
```

---

# 2. Activation 결과 확인

확인 파일:

```text
~/l1sw-private-skills/job-list/data/state/activation/latest.json
```

대상 Job ID:

```text
JOB-20260829-MCD-HANDOFF-AUDIT-02
```

출력:

```text
QACT=A   # QUEUED 또는 LAUNCHED
QACT=B   # DUPLICATE_SKIPPED
QACT=C   # TARGET_MISMATCH
QACT=D   # REJECTED
QACT=E   # 대상 Job 기록 없음
QACT=F   # activation 파일 없음
```

추가 설명은 원칙적으로 하지 않는다.

---

# 3. Observer 결과 확인

확인 파일:

```text
~/l1sw-private-skills/job-list/data/state/observer/latest_result.json
```

출력:

```text
QOBS=A   # PASS / SUCCESS
QOBS=B   # PASS지만 NEEDS_ATTENTION 또는 NEEDS_USER_INPUT
QOBS=C   # FAIL / FAILED
QOBS=D   # TIMEOUT / INTERRUPTED / OUTPUT_MISSING
QOBS=E   # 대상 Job 결과 없음
QOBS=F   # observer 파일 없음
```

`observer-result/v1`이 없으면 임의 해석하지 말 것.

---

# 4. MCD Audit 산출물 존재 여부

JSON:

```text
~/l1sw-private-skills/job-list/data/state/mcd_handoff_audit_result.json
```

MD:

```text
~/l1sw-private-skills/job-list/output/mcd_handoff_audit_latest.md
```

출력:

```text
QOUT=A   # JSON + MD 모두 존재
QOUT=B   # JSON만 존재
QOUT=C   # MD만 존재
QOUT=D   # 둘 다 없음
```

---

# 5. Q1 — MCD CSV 방향 열

Audit 결과에서 source/target column을 확인한다.

출력:

```text
Q1=A   # from / to
Q1=B   # SourceFile / TargetFile
Q1=C   # 둘 다 아닌 실제 다른 header
Q1=D   # 확인 불가
```

그리고 반드시:

```text
SRC=<actual_source_column|NA>
DST=<actual_target_column|NA>
```

를 함께 출력.

예:

```text
Q1=C SRC=src_path DST=dst_path
```

---

# 6. Q2 — MCD-<hash> 노출 범위

출력:

```text
Q2=A   # 개선 포인트 보고서에만 노출
Q2=B   # MCD 보고서 전반에 노출
Q2=C   # mcd-compare에도 노출
Q2=D   # 확인 불가
```

여러 조건이 동시에 해당하면 우선순위:

```text
C > B > A > D
```

---

# 7. Q3 — CSV mapping profile

출력:

```text
Q3=A   # mapping profile 있음
Q3=B   # 없음
Q3=C   # 확인 불가
```

---

# 8. MCS CSV 검색 결과

검색 규칙:

```text
파일명에 "mcs" 포함
case-insensitive
recursive
확장자 .csv
```

출력:

```text
MCS=<count>
```

예:

```text
MCS=7
```

파일 목록은 기본 출력하지 않는다.

---

# 9. ERR 객관식

Audit 결과에서 대표 오류/경고 1개를 고른다.

출력:

```text
ERR=A   # NONE
ERR=B   # MCD_EDGE_COLUMNS_UNRESOLVED
ERR=C   # MCD_EDGE_COLUMNS_NONCANONICAL
ERR=D   # MAPPING_PROFILE_CONFLICT
ERR=E   # MCD_HASH_SCOPE_UNRESOLVED
ERR=F   # CSV_SCAN_FAILED
ERR=G   # AUDIT_PARTIAL
ERR=H   # AUDIT_RESULT_MISSING
ERR=I   # 기타 실제 reason 존재
```

`ERR=I`인 경우에만:

```text
ERR_CODE=<actual_reason_code>
```

추가.

---

# 10. 실제 MCD Report 추가 확인

아래 범위만 확인한다.

```text
~/l1sw-private-skills/l1-sam-fixer/output/
~/l1sw-private-skills/l1-sam-fixer/data/
```

최신 MCD report가 명확할 때만 판정.

출력:

```text
QMCD=A   # cycle_members/dependency_edges 정상
QMCD=B   # cycle_members empty
QMCD=C   # dependency_edges empty
QMCD=D   # 둘 다 empty
QMCD=E   # report는 있으나 추가 확인 필요
QMCD=F   # 최신 report를 명확히 특정할 수 없어 skip
```

Evidence 상태:

```text
QEVID=A   # CODE_VERIFIED 존재
QEVID=B   # CODE_FACT 존재
QEVID=C   # TOPOLOGY_INFERRED 존재
QEVID=D   # ANALYSIS_REQUIRED만 주로 존재
QEVID=E   # UNRESOLVED만 주로 존재
QEVID=F   # 확인 불가 / report skip
```

Hash 제목:

```text
QHASH=A   # 사용자 제목에 MCD-<hash> 없음
QHASH=B   # 사용자 제목에 MCD-<hash> 있음
QHASH=C   # 확인 불가
```

---

# 11. 결과가 없을 때 최소 원인 판정

MCD Audit 결과가 없으면 다음만 추가 확인한다.

```text
activation/latest.json
observer/latest_result.json
data/state/core/processed.jsonl
```

출력:

```text
QCAUSE=A   # Job 미실행
QCAUSE=B   # DUPLICATE_SKIPPED
QCAUSE=C   # TARGET_MISMATCH
QCAUSE=D   # REJECTED
QCAUSE=E   # 실행됐으나 output 생성 실패
QCAUSE=F   # 판단 불가
QCAUSE=G   # 해당 없음 (정상 결과 존재)
```

재실행은 하지 않는다.

---

# 12. 최종 판정

반드시 아래 중 하나만 선택:

```text
FINAL=A   # 정상 수행 + Audit 결과 정상
FINAL=B   # 정상 수행 + 사용자 확인 필요
FINAL=C   # Job 미수행
FINAL=D   # Job 실패
FINAL=E   # 결과 파일 생성 실패
FINAL=F   # 추가 확인 필요
```

판정 기준:

```text
QACT=A + QOBS=A + QOUT=A + ERR=A
→ FINAL=A

QACT=A + QOBS=B
또는 ERR이 B~I
→ FINAL=B

QACT=E/F 또는 QCAUSE=A/B/C/D
→ FINAL=C

QOBS=C/D
→ FINAL=D

QACT=A + QOBS=A/B + QOUT=D
→ FINAL=E

그 외
→ FINAL=F
```

---

# 13. 최종 출력 형식

**설명문 없이 아래 형식으로만 출력해줘.**

```text
Q0=A
QACT=A
QOBS=B
QOUT=A
Q1=C SRC=src_path DST=dst_path
Q2=B
Q3=A
MCS=7
ERR=C
QMCD=D
QEVID=D
QHASH=B
QCAUSE=G
FINAL=B
```

마지막 줄에는 반드시 아래 한 줄을 추가:

```text
MCD45: Q0=A QACT=A QOBS=B QOUT=A Q1=C SRC=src_path DST=dst_path Q2=B Q3=A MCS=7 ERR=C QMCD=D QEVID=D QHASH=B FINAL=B
```

---

# 14. 출력 제한

- 서술형 설명 금지
- 원인 추측 금지
- 조치 제안 금지
- 명령어 추가 제안 금지
- 파일 수정 금지
- 질문 금지
- 가능한 한 객관식 코드만 출력

사용자는 마지막 `MCD45:` 한 줄만 사외에 직접 타이핑해 전달할 수 있어야 한다.
