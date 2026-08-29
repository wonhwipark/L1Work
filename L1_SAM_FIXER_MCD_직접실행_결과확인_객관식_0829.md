# l1-sam-fixer 직접 실행 후 MCD 결과 확인 — 객관식 전용 프롬프트

## 목적

회사 Linux PC에서 사용자가 `l1-sam-fixer`를 직접 실행한 뒤,
최신 MCD 결과가 정상적으로 개선되었는지 **객관식 코드 중심으로만** 확인해줘.

이번 확인은 **Job-list 상태를 절대 참조하지 않는다.**

확인 대상은 오직:

```text
l1-sam-fixer 최신 직접 실행 결과
MCD report
MCD improvement points
MCD compare 관련 최신 결과
```

이다.

---

# 0. 절대 원칙

이번 작업은 **읽기 전용 확인**만 수행한다.

금지:

```text
파일 수정
Fixer 재실행
Job-list 조회
Job 재실행
processed state 조회/삭제
Skill 수정
Git/GitHub write
임의 retry
```

명확한 실패 증거가 없으면 실패로 단정하지 말 것.

---

# 1. 최신 Fixer 버전 확인

기대 버전:

```text
0.2.45
```

출력:

```text
QVER=A   # 0.2.45
QVER=B   # 다른 버전
QVER=C   # 확인 불가
```

가능하면 canonical version source를 우선 사용:

```text
~/l1sw-private-skills/l1-sam-fixer/VERSION
~/l1sw-private-skills/l1-sam-fixer/.skill-release.json
~/l1sw-private-skills/l1-sam-fixer/SKILL.md
```

---

# 2. 최신 MCD 결과 존재 여부

우선 아래 범위만 확인:

```text
~/l1sw-private-skills/l1-sam-fixer/output/
~/l1sw-private-skills/l1-sam-fixer/data/
```

최신 MCD 관련 결과를 명확히 특정한다.

출력:

```text
QOUT=A   # 최신 MCD report + improvement points 모두 존재
QOUT=B   # report만 존재
QOUT=C   # improvement points만 존재
QOUT=D   # 둘 다 없음
QOUT=E   # 최신 결과를 명확히 특정할 수 없음
```

---

# 3. CSV 방향 열 인식

최신 run에서 source/target column이 정상 인식됐는지 확인.

출력:

```text
QCSV=A   # from / to
QCSV=B   # SourceFile / TargetFile
QCSV=C   # 다른 실제 header 정상 인식
QCSV=D   # 방향 열 인식 실패
QCSV=E   # 확인 불가
```

그리고 반드시:

```text
SRC=<actual_source_column|NA>
DST=<actual_target_column|NA>
```

를 같이 출력.

---

# 4. dependency_edges 확인

출력:

```text
QEDGE=A   # dependency_edges 정상 생성
QEDGE=B   # dependency_edges 비어 있음
QEDGE=C   # 일부 cycle만 비어 있음
QEDGE=D   # 확인 불가
```

---

# 5. cycle_members 확인

출력:

```text
QMEM=A   # cycle_members 정상 생성
QMEM=B   # cycle_members 비어 있음
QMEM=C   # 일부 cycle만 비어 있음
QMEM=D   # 확인 불가
```

---

# 6. MCD edge column 오류

출력:

```text
QERR=A   # MCD_EDGE_COLUMNS_UNRESOLVED 없음
QERR=B   # MCD_EDGE_COLUMNS_UNRESOLVED 존재
QERR=C   # MCD_EDGE_COLUMNS_NONCANONICAL만 존재
QERR=D   # 기타 MCD edge 관련 오류
QERR=E   # 확인 불가
```

`QERR=D`일 때만:

```text
ERR_CODE=<actual_reason_code>
```

추가.

---

# 7. 실제 코드 분석 Evidence

최신 MCD 결과의 evidence를 확인.

출력:

```text
QEVID=A   # CODE_VERIFIED 존재
QEVID=B   # CODE_FACT 존재
QEVID=C   # CODE_VERIFIED + CODE_FACT 둘 다 존재
QEVID=D   # TOPOLOGY_INFERRED만 존재
QEVID=E   # ANALYSIS_REQUIRED 위주
QEVID=F   # UNRESOLVED 위주
QEVID=G   # 확인 불가
```

판정 우선순위:

```text
실제 코드 분석 성공 > 기존 fact 재사용 > topology fallback > analysis required > unresolved
```

---

# 8. bounded Code Analyzer 수행 여부

출력:

```text
QCODE=A   # edge fact 없던 cycle에 실제 targeted Code Analyzer 수행됨
QCODE=B   # 기존 CODE_FACT만 사용되어 재분석 불필요
QCODE=C   # Code Analyzer 수행 불가하여 topology fallback
QCODE=D   # Code Analyzer가 수행되지 않았는데 이유 불명
QCODE=E   # 확인 불가
```

전체 repository 무제한 scan 여부도 확인 가능하면:

```text
QBOUND=A   # cycle/edge bounded 분석
QBOUND=B   # 범위 과도하게 확대됨
QBOUND=C   # 확인 불가
```

---

# 9. break edge 결정 여부

출력:

```text
QBREAK=A   # 대부분 cycle에 break edge 결정됨
QBREAK=B   # 일부 cycle만 결정됨
QBREAK=C   # 대부분 UNRESOLVED
QBREAK=D   # 확인 불가
```

---

# 10. 두 보고서 일관성

`mcd_report`와 `mcd_improvement_points`의 동일 cycle 판단을 비교.

출력:

```text
QCONS=A   # break edge / recommendation / evidence 일치
QCONS=B   # break edge 불일치
QCONS=C   # recommendation/evidence 불일치
QCONS=D   # 비교 가능한 cycle 부족
QCONS=E   # 확인 불가
```

---

# 11. MCD-<hash> 제목 표시

출력:

```text
QHASH=A   # 사용자 제목에 MCD-<hash> 노출 없음
QHASH=B   # improvement points에 노출
QHASH=C   # MCD report 전반에 노출
QHASH=D   # mcd-compare에도 노출
QHASH=E   # 확인 불가
```

내부 `work_unit_id` hash는 정상적으로 유지되어도 문제 없음.

---

# 12. UNRESOLVED 수준

가능하면 최신 improvement points에서 비율 또는 개수를 확인.

출력:

```text
QUNRES=A   # 거의 없음 / 예외적
QUNRES=B   # 일부 존재
QUNRES=C   # 대부분 존재
QUNRES=D   # 전부 또는 거의 전부
QUNRES=E   # 확인 불가
```

---

# 13. ANALYSIS_REQUIRED 수준

출력:

```text
QAN=A   # 거의 없음 / 예외적
QAN=B   # 일부 존재
QAN=C   # 대부분 존재
QAN=D   # 전부 또는 거의 전부
QAN=E   # 확인 불가
```

---

# 14. 폴더별 Worst Top10

최신 MCD report에서 확인.

출력:

```text
QTOP=A   # 폴더별 Worst Top10 정상 존재
QTOP=B   # 일부 폴더만 존재
QTOP=C   # 없음
QTOP=D   # 확인 불가
```

---

# 15. 폴더별 문제 파일/클래스

출력:

```text
QFILE=A   # 폴더별 가장 문제되는 파일/클래스 표시됨
QFILE=B   # 일부만 표시됨
QFILE=C   # 없음
QFILE=D   # 확인 불가
```

---

# 16. 최종 판정

반드시 아래 중 하나만 선택:

```text
FINAL=A   # v0.2.45 핵심 수정 정상
FINAL=B   # 정상 동작하지만 일부 개선/확인 필요
FINAL=C   # CSV edge parsing 문제 지속
FINAL=D   # cycle/edge 생성 문제 지속
FINAL=E   # 실제 코드분석 연결 문제
FINAL=F   # 두 MCD 보고서 판단 불일치
FINAL=G   # hash/가독성 문제 지속
FINAL=H   # 결과 부족으로 판단 불가
```

권장 판정 규칙:

```text
QCSV=A/B/C
AND QEDGE=A
AND QMEM=A
AND QERR=A/C
AND QEVID=A/B/C
AND QCONS=A
AND QHASH=A
→ FINAL=A
```

```text
QCSV=D
또는 QERR=B
→ FINAL=C
```

```text
QEDGE=B/C
또는 QMEM=B/C
→ FINAL=D
```

```text
QCODE=C/D
AND QEVID=D/E/F
→ FINAL=E
```

```text
QCONS=B/C
→ FINAL=F
```

```text
QHASH=B/C/D
→ FINAL=G
```

그 외:

```text
FINAL=B 또는 H
```

---

# 17. 최종 출력 형식

**설명문 없이 아래 형식으로만 출력해줘.**

```text
QVER=A
QOUT=A
QCSV=C SRC=src_path DST=dst_path
QEDGE=A
QMEM=A
QERR=C
QEVID=C
QCODE=A
QBOUND=A
QBREAK=A
QCONS=A
QHASH=A
QUNRES=B
QAN=A
QTOP=A
QFILE=A
FINAL=A
```

마지막 줄:

```text
MCD245: QVER=A QOUT=A QCSV=C SRC=src_path DST=dst_path QEDGE=A QMEM=A QERR=C QEVID=C QCODE=A QBOUND=A QBREAK=A QCONS=A QHASH=A QUNRES=B QAN=A QTOP=A QFILE=A FINAL=A
```

---

# 18. 출력 제한

- 서술형 설명 금지
- Job-list 관련 상태 출력 금지
- 원인 추측 금지
- 조치 제안 금지
- 재실행 제안 금지
- 질문 금지
- 가능한 한 객관식 코드만 출력

사용자는 마지막 `MCD245:` 한 줄만 사외에 직접 전달할 수 있어야 한다.
