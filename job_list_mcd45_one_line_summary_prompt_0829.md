# Job-list MCD45 외부 전달용 1줄 요약 추가 프롬프트

## 목적

현재 회사 Linux PC에서 `job-list`의 MCD handoff audit를 수행하면 상세 결과가 아래에 생성된다.

```text
~/l1sw-private-skills/job-list/data/state/mcd_handoff_audit_result.json
~/l1sw-private-skills/job-list/output/mcd_handoff_audit_latest.md
```

하지만 회사 PC의 파일을 사외로 직접 전달하기 어렵기 때문에,
사용자가 결과를 보고 ChatGPT에 손으로 입력해야 한다.

따라서 **기존 상세 JSON/MD 결과는 그대로 유지하면서**,
audit 작업 완료 시 터미널/최종 결과의 마지막에
사외 전달용 **1줄 요약 코드**를 자동으로 출력하도록 `job-list`를 수정해줘.

---

## 핵심 요구사항

### 1. 기존 기능 유지

다음 기존 동작은 절대 제거하거나 약화하지 말 것.

- MCD handoff audit
- `mcs`가 파일명에 포함된 모든 CSV 재귀 검색
- 대소문자 무시
- CSV header 확인
- source/target 방향 열 판정
- `MCD-<hash>` 노출 범위 확인
- mapping profile 존재 여부 확인
- JSON 상세 결과 저장
- MD 상세 결과 저장
- Linux one-shot job
- profile whitelist
- Job-list의 기존 보안 정책
- Dispatcher observer-only 구조

---

## 2. 외부 전달용 1줄 요약

Audit 완료 시 마지막에 아래 형식으로 한 줄을 출력한다.

```text
MCD45: Q1=<A|B|C|D> SRC=<source_column|NA> DST=<target_column|NA> Q2=<A|B|C|D> Q3=<A|B|C> MCS=<count> ERR=<reason_code|NONE>
```

예:

```text
MCD45: Q1=C SRC=src_path DST=dst_path Q2=B Q3=A MCS=7 ERR=MCD_EDGE_COLUMNS_UNRESOLVED
```

정상 예:

```text
MCD45: Q1=A SRC=from DST=to Q2=A Q3=B MCS=4 ERR=NONE
```

---

## 3. 필드 의미

### Q1 — MCD CSV 방향 열

```text
A = from / to
B = SourceFile / TargetFile
C = 둘 다 아닌 다른 실제 header
D = 확인 불가
```

Q1=C인 경우 반드시 `SRC`, `DST`에 실제 발견된 column 이름을 넣는다.

Q1=A/B인 경우에도 가능하면 실제 사용된 이름을 `SRC`, `DST`에 넣는다.

판정 불가 시:

```text
SRC=NA
DST=NA
```

---

### Q2 — `MCD-<hash>` 노출 범위

```text
A = 개선 포인트 보고서만
B = MCD 보고서 전반
C = mcd-compare 결과에도 존재
D = 확인 불가
```

여러 범위에 동시에 해당하면 **가장 넓은 범위**를 선택한다.

우선순위:

```text
C > B > A > D
```

---

### Q3 — mapping profile

```text
A = 있음
B = 없음
C = 확인 불가
```

---

### MCS

파일명에 `mcs`가 포함된 CSV 전체 개수.

조건:

```text
case-insensitive
recursive
*.csv only
```

예:

```text
abc_mcs.csv
MCS_Result.csv
sub/test_mcs_detail.CSV
```

모두 포함한다.

---

### ERR

Audit 수행 중 가장 중요한 reason code 하나를 표시한다.

우선순위 예:

```text
MCD_EDGE_COLUMNS_UNRESOLVED
MAPPING_PROFILE_CONFLICT
MCD_HASH_SCOPE_UNRESOLVED
CSV_SCAN_FAILED
AUDIT_PARTIAL
NONE
```

오류/경고가 없으면:

```text
ERR=NONE
```

상세 오류는 기존 JSON/MD에 계속 기록한다.

---

## 4. 출력 위치

1줄 요약은 최소한 다음 두 곳에서 확인 가능해야 한다.

### A. 터미널 stdout

Audit 종료 직전 마지막 의미 있는 출력으로 표시:

```text
============================================================
MCD45: Q1=C SRC=src_path DST=dst_path Q2=B Q3=A MCS=7 ERR=MCD_EDGE_COLUMNS_UNRESOLVED
============================================================
```

### B. MD 상세 보고서 마지막

`mcd_handoff_audit_latest.md` 마지막에 아래 section 추가:

```markdown
## 외부 전달용 1줄 요약

MCD45: Q1=C SRC=src_path DST=dst_path Q2=B Q3=A MCS=7 ERR=MCD_EDGE_COLUMNS_UNRESOLVED
```

가능하면 JSON에도 같은 문자열을 추가한다.

예:

```json
{
  "external_summary": "MCD45: Q1=C SRC=src_path DST=dst_path Q2=B Q3=A MCS=7 ERR=MCD_EDGE_COLUMNS_UNRESOLVED"
}
```

---

## 5. 사용자 편의성

사용자는 회사에서 아래 한 줄만 보고 사외 ChatGPT에 직접 입력한다.

```text
MCD45: Q1=C SRC=src_path DST=dst_path Q2=B Q3=A MCS=7 ERR=MCD_EDGE_COLUMNS_UNRESOLVED
```

따라서 한 줄은:

- 줄바꿈 없이
- 공백 구분
- 필드 순서 고정
- 사람이 타이핑하기 쉬운 짧은 값
- 절대경로 포함 금지
- 소스코드 내용 포함 금지
- 회사 내부 repository 이름/민감정보 불필요 노출 금지

로 만든다.

---

## 6. 중요: `mcs` CSV 검색

검색 기준은 반드시:

```text
파일명에 "mcs" 포함
AND 확장자가 csv
AND case-insensitive
AND 하위 폴더 recursive
```

Linux Python 구현 예시 의미:

```python
for path in root.rglob("*"):
    if path.is_file() and path.suffix.lower() == ".csv" and "mcs" in path.name.lower():
        ...
```

단, 기존 구현이 더 안전하다면 동일 의미를 유지하면서 기존 함수를 사용한다.

검색한 파일들의 절대경로를 외부 전달용 1줄에 넣지 않는다.

상세 내부 MD/JSON에는 기존 정책 범위 내에서 기록 가능하다.

---

## 7. 실패 시에도 1줄은 생성

가능하면 audit 일부가 실패해도 외부 전달용 한 줄을 남긴다.

예:

```text
MCD45: Q1=D SRC=NA DST=NA Q2=D Q3=C MCS=0 ERR=AUDIT_PARTIAL
```

즉 사용자가 결과를 전혀 전달할 수 없는 상태를 최소화한다.

---

## 8. 구현 원칙

- 저사양 Linux/OpenCode 환경 고려
- Python 기반 deterministic 처리 우선
- LLM에게 CSV parsing이나 file count를 맡기지 말 것
- shell command 문자열 조합 최소화
- 경로는 `pathlib` 우선
- UTF-8 명시
- 기존 Windows 호환성이 있다면 깨뜨리지 말 것
- 기존 Job-list schema/whitelist 정책 유지
- 임의 `command`, `shell`, `entrypoint` 원격 주입 금지
- 기존 one-shot dedupe/expiry/recovery 정책 유지

---

## 9. 테스트

최소 아래 테스트를 추가해줘.

### TC1

```text
from,to
```

→

```text
Q1=A SRC=from DST=to
```

### TC2

```text
SourceFile,TargetFile
```

→

```text
Q1=B SRC=SourceFile DST=TargetFile
```

### TC3

```text
src_path,dst_path
```

→

```text
Q1=C SRC=src_path DST=dst_path
```

### TC4

방향 column 없음

→

```text
Q1=D SRC=NA DST=NA ERR=MCD_EDGE_COLUMNS_UNRESOLVED
```

### TC5

`mcs` CSV 3개 + 일반 CSV 2개

→

```text
MCS=3
```

### TC6

`MCS_A.CSV`, `abc_mcs.csv`, `sub/McS_test.csv`

→ 모두 검색

### TC7

mapping profile 존재

→

```text
Q3=A
```

### TC8

정상 audit

→

```text
ERR=NONE
```

### TC9

stdout 마지막에 정확히 1개의 `MCD45:` line 존재.

### TC10

MD 및 JSON에도 stdout과 동일한 `external_summary`가 저장됨.

---

## 10. 패키지 검증

수정 완료 후 반드시:

1. 전체 기존 테스트
2. 신규 테스트
3. self-check
4. package checksum
5. VERSION / SKILL.md / manifest 버전 일치
6. ZIP 재생성

을 수행한다.

기존 테스트 실패가 발생하면 단순히 삭제하거나 skip으로 바꾸지 말고,
**현재 정상 동작과 충돌하는 오래된 fixture/assertion인지 먼저 확인**한다.

---

## 11. 완료 보고 형식

작업 완료 후 아래 항목만 간결하게 보고해줘.

```text
A. 수정 버전
B. 변경 파일
C. 신규 1줄 format
D. mcs CSV 검색 규칙
E. 테스트 결과
F. self-check 결과
G. 생성 ZIP 경로
```

그리고 실제 출력 예시 1개를 함께 보여줘.

---

## 최종 목표

회사 Linux에서 Job-list audit 완료 후 사용자가 아래 한 줄만 사외로 전달할 수 있어야 한다.

```text
MCD45: Q1=C SRC=src_path DST=dst_path Q2=B Q3=A MCS=7 ERR=MCD_EDGE_COLUMNS_UNRESOLVED
```

이 한 줄만으로 `l1-sam-fixer v0.2.45` 수정에 필요한 핵심 환경 정보를 복원할 수 있어야 한다.
