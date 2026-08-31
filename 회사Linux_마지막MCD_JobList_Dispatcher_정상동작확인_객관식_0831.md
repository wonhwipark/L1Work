# 회사 Linux — 마지막 MCD Job-list + Dispatcher 정상동작 확인 프롬프트

아래 작업을 **회사 Linux PC의 현재 설치 상태를 대상으로 읽기 전용으로 수행**해줘.

목적은 두 가지다.

1. `Dispatcher`가 정상 설치되어 있고 실제로 주기 실행되고 있는지 확인
2. 가장 마지막 `Job-list MCD` 작업이 단순 실행만 된 것이 아니라, 의도한 MCD gap-fill 흐름까지 정상 수행됐는지 확인

가능한 한 **객관식 + 짧은 답변**으로 결과를 줘.
문제가 있으면 추측하지 말고 실제 state / observer / log / artifact 근거를 따라가서 LLM이 원인을 판단해줘.

---

# 0. 이번 확인의 기준

현재 기대 기준:

```text
Dispatcher        = 0.3.8
Job-list          = 0.3.62
L1 Study Runner   = 0.2.10
L1 SAM Fixer      = 0.2.57
L1 Knowledge Mngr = 0.5.4
Code Analyzer     >= 0.13.31
```

마지막 MCD one-shot의 우선 확인 대상:

```text
job_id   = JOB-20260831-MCD-GAP-FILL-0110
profile  = l1-study-mcd
platform = linux
target   = SMPF/Protocol/Channel/L1
```

이 Job의 기대 동작:

```text
기존 최신 SAM MCD Run 재사용
        ↓
MCD_FACT_GAPS / 미완료 cycle만 선택
        ↓
Code Analyzer로 필요한 코드 근거 보강
        ↓
Knowledge Manager에 observed evidence 기록
        ↓
SAM Fixer MCD batch 완료
        ↓
최신 MCD 보고서 재렌더링
```

단, 위 Job ID가 설치 state/history에서 전혀 발견되지 않는다면
임의로 "미실행"이라고 즉시 단정하지 말고,
현재 설치된 Job-list의 request/state/history에서 **가장 최근 MCD 관련 one-shot**을 찾아서
그 Job을 실제 확인 대상으로 선택해줘.

다음 과거 Job과 혼동하지 말 것:

```text
JOB-20260829-MCD-HANDOFF-AUDIT-02
JOB-20260828-MCD-REPORT-0241
```

가능하면 `JOB-20260831-MCD-GAP-FILL-0110`을 최우선으로 한다.

---

# 1. 절대 원칙

이번 작업은 **확인/진단 전용**이다.

하지 말 것:

```text
파일 수정
Job 재실행
Job 신규 enqueue
processed/consumed state 삭제
stale state 강제 삭제
Study Runner --resume 실행
SAM Fixer 재실행
Code Analyzer 재실행
Skill 수정
설정 수정
Dispatcher cycle 수동 실행
Git/GitHub write
signal asset upload
임의 retry
scheduler 수정
```

허용:

```text
파일 읽기
JSON/JSONL/MD/log 확인
mtime 확인
VERSION 확인
프로세스/스케줄 상태 읽기
Dispatcher status
Dispatcher report
bounded grep/find
```

`Dispatcher cycle`은 GitHub signal GET을 발생시킬 수 있으므로
이번 **확인 작업에서는 실행하지 말 것**.

명확한 증거가 없으면 실패 원인을 추측하지 않는다.

---

# 2. Dispatcher 설치 확인

우선 canonical 경로를 확인한다.

```text
~/l1sw-dispatcher/
```

우선 확인:

```text
~/l1sw-dispatcher/VERSION
~/l1sw-dispatcher/l1sw_dispatcher.py
~/l1sw-dispatcher/config.json
~/l1sw-dispatcher/state.json
~/l1sw-dispatcher/monitor_snapshot.json
```

읽기 전용 명령:

```bash
python3 ~/l1sw-dispatcher/l1sw_dispatcher.py status
python3 ~/l1sw-dispatcher/l1sw_dispatcher.py report
```

판정:

```text
1=A   # Dispatcher 0.3.8 정상 설치 + status 실행 성공
1=B   # 설치되어 있으나 버전이 0.3.8 아님
1=C   # 설치 파일 일부 누락 또는 status 실패
1=D   # Dispatcher 설치 자체를 찾지 못함
1=E   # 판단 불가
```

---

# 3. Dispatcher 주기 실행 등록 확인

Dispatcher 자체가 scheduler를 소유한다고 가정하지 말 것.

현재 설계상 주기 실행 owner는:

```text
autotask-builder
```

이다.

다음 범위 안에서만 Dispatcher schedule 등록 여부를 확인해줘.

```text
~/l1sw-private-skills/autotask-builder/
~/l1sw-dispatcher/
```

필요하면 사용자 계정의 현재 scheduler 상태를 **읽기 전용**으로 확인해도 된다.

Linux 환경에 실제 사용 중인 방식만 확인하고,
cron/systemd/기타 방식을 무작정 모두 수정하거나 생성하지 말 것.

판정:

```text
2=A   # Dispatcher 주기 실행 등록 확인됨
2=B   # 등록 정보는 있으나 비활성/오류
2=C   # Dispatcher schedule 등록을 찾지 못함
2=D   # scheduler 상태를 확인할 근거 부족
```

추가 한 줄:

```text
SCHED=<실제 owner/등록 방식 또는 NA>
```

---

# 4. Dispatcher가 실제 최근에 실행됐는지 확인

단순 설치와 실제 실행은 분리해서 판정한다.

우선:

```text
~/l1sw-dispatcher/state.json
~/l1sw-dispatcher/monitor_snapshot.json
Dispatcher log
```

에서 다음을 확인한다.

```text
최근 cycle timestamp
최근 heartbeat/관측 timestamp
마지막 report/snapshot 갱신 시각
최근 dispatcher 오류
```

현재 시각과 비교해서
설정된 주기 대비 정상적으로 최근 cycle이 수행됐는지 판단한다.

판정:

```text
3=A   # 최근 cycle 수행 확인 + 주기상 정상
3=B   # 실행 흔적은 있으나 현재 기준 stale
3=C   # 설치만 되어 있고 실제 cycle 수행 흔적 없음
3=D   # 최근 cycle에서 Dispatcher 자체 오류 확인
3=E   # 판단 불가
```

추가 한 줄:

```text
LAST_CYCLE=<timestamp|NA>
```

---

# 5. Dispatcher signal 상태 확인

`state.json`, `report`, 관련 log에서 signal flush 상태를 확인한다.

특히 가능하면:

```text
failed
pending
sent/delivered
최근 signal failure
```

를 확인한다.

판정:

```text
4=A   # signal 실패 없음 + pending 없음
4=B   # 일시 pending 존재
4=C   # signal GET/flush 실패 존재
4=D   # signal 상태 필드/근거 확인 불가
```

추가:

```text
SIGNAL=<짧은 실제 상태>
```

중요:

```text
GitHub download_count를 사내에서 새로 발생시키기 위해 cycle을 실행하지 말 것.
현재 남아 있는 Dispatcher state/log만 확인한다.
```

---

# 6. Job-list 설치 버전 확인

확인:

```text
~/l1sw-private-skills/job-list/VERSION
~/l1sw-private-skills/job-list/.skill-release.json
~/l1sw-private-skills/job-list/SKILL.md
```

canonical version source를 우선한다.

판정:

```text
5=A   # 0.3.62
5=B   # 다른 버전
5=C   # 확인 불가
5=D   # Job-list 설치 없음
```

추가:

```text
JOBLIST_VER=<actual|NA>
```

---

# 7. 실제 확인 대상 MCD Job 특정

우선 다음 Job을 찾는다.

```text
JOB-20260831-MCD-GAP-FILL-0110
```

확인 범위:

```text
~/l1sw-private-skills/job-list/requests/
~/l1sw-private-skills/job-list/data/state/
~/l1sw-private-skills/job-list/output/
```

우선 확인 가능한 state:

```text
activation/latest.json
observer/latest_result.json
observer/current_run.json
core/processed.jsonl
기타 job history/observation JSONL
```

`latest_result.json`이 다른 후속 Job으로 덮였으면
processed/history/observations에서 대상 Job ID를 찾아야 한다.

판정:

```text
6=A   # JOB-20260831-MCD-GAP-FILL-0110을 확인 대상으로 특정
6=B   # 해당 Job은 없지만 더 최근의 MCD Job을 명확히 특정
6=C   # MCD Job 후보가 여러 개라 최신 대상을 확정하기 어려움
6=D   # MCD Job 기록 자체를 찾지 못함
```

추가:

```text
JOB=<actual_job_id|NA>
PROFILE=<actual_profile|NA>
```

---

# 8. MCD Job activation / 실행 여부 확인

대상 Job의 activation + processed/history + observer를 함께 확인한다.

`latest_result.json` 하나만 보고 판단하지 않는다.

판정:

```text
7=A   # 실제 실행됨 + SUCCESS/PASS
7=B   # 실제 실행됐지만 PARTIAL/NEEDS_ATTENTION/NEEDS_USER_INPUT
7=C   # FAILED
7=D   # DUPLICATE_SKIPPED
7=E   # TARGET_MISMATCH
7=F   # REJECTED / profile validation 실패
7=G   # expiry 전에 실행되지 못함 / 미실행
7=H   # 실행 흔적은 있으나 최종 receipt 없음
7=I   # 판단 불가
```

추가:

```text
EXEC=<actual status/reason 1줄>
```

---

# 9. l1-study-mcd profile 준비 여부 확인

이번 Job은 `l1-study-mcd` local trusted profile이 있어야 정상 실행된다.

현재 Job-list 설계상:

```text
기존 l1-study가 로컬에 존재
        ↓
study_runner.py contract가 유효
        ↓
필요 시 l1-study-mcd sibling profile 파생
```

을 사용한다.

다음만 확인:

```text
실제 l1-study-mcd profile 존재 여부
target skill = l1-study-runner
mode = mcd
source = latest-sam-report
target = SMPF/Protocol/Channel/L1
timeout/runtime budget가 유효한지
```

판정:

```text
8=A   # profile 정상
8=B   # l1-study는 있으나 l1-study-mcd 생성/준비 실패
8=C   # l1-study-mcd 존재하지만 contract invalid
8=D   # profile 없음
8=E   # 판단 불가
```

---

# 10. MCD dependency gate 확인

실제 실행 당시 또는 현재 결과 state에서 dependency gate 결과를 확인한다.

최소 요구:

```text
l1-study-runner >= 0.2.9
code-analyzer   >= 0.13.31
l1-knowledge-manager >= 0.5.4
l1-sam-fixer    >= 0.2.56
```

현재 기대 설치본:

```text
l1-study-runner = 0.2.10
l1-sam-fixer    = 0.2.57
l1-knowledge-manager = 0.5.4
```

판정:

```text
9=A   # dependency gate PASS
9=B   # dependency 부족으로 DEPENDENCY_NOT_READY
9=C   # 일부 버전이 기대보다 낮음
9=D   # dependency 확인 중 다른 오류
9=E   # 판단 불가
```

부족한 경우에만:

```text
DEP=<skill:actual/required>
```

---

# 11. Study Runner 실제 MCD 수행 상태 확인

우선:

```text
~/l1sw-private-skills/l1-study-runner/data/state/nightly_result.json
~/l1sw-private-skills/l1-study-runner/data/state/observer_result.json
~/l1sw-private-skills/l1-study-runner/data/state/mcd_study_checkpoint.json
```

을 확인한다.

반드시 대상 Job 실행 시각과 timestamp가 맞는지 확인해서
예전 stale 결과를 현재 Job 결과로 오인하지 않는다.

주요 정상 흐름:

```text
LEARNING_DONE
reason=MCD_STUDY_DONE
resumable=false
```

부분 완료 가능 흐름:

```text
ANALYSIS_PARTIAL
reason=MCD_RESUME_READY 또는 MCD_FACT_GAPS
resumable=true
```

판정:

```text
10=A   # LEARNING_DONE / MCD_STUDY_DONE
10=B   # ANALYSIS_PARTIAL / MCD_RESUME_READY
10=C   # ANALYSIS_PARTIAL / MCD_FACT_GAPS
10=D   # REVIEW_PENDING / NEEDS_USER_INPUT
10=E   # BLOCKED
10=F   # FAILED
10=G   # 결과는 있으나 대상 Job과 timestamp 불일치(stale)
10=H   # 결과 파일 없음
10=I   # 판단 불가
```

추가:

```text
STUDY=<status/reason>
```

---

# 12. 실제 Code Analyzer gap-fill 수행 여부 확인

전체 코드 재분석을 찾는 것이 아니다.

이번 Job의 목적에 맞게:

```text
최신 SAM MCD Run 재사용
미완료/fact-gap cycle만 대상
Code Analyzer mcd-edge-probe 또는 동등한 실제 child 분석 수행
batch result 생성
```

이 있었는지 확인한다.

검색 범위는 먼저 아래로 제한:

```text
l1-study-runner의 해당 run/checkpoint
해당 SAM MCD Run의 mcd_batches/evidence
해당 실행과 직접 연결된 Code Analyzer output
```

repository 전체를 무제한 grep하지 말 것.

판정:

```text
11=A   # 실제 gap 대상 Code Analyzer 분석 근거 확인
11=B   # 일부 batch만 분석됨
11=C   # Code Analyzer 호출/결과 없음
11=D   # child 분석 실패
11=E   # intake/index 수준만 생성되고 의미 분석 미완료
11=F   # 판단 불가
```

---

# 13. Knowledge evidence 반영 여부 확인

MCD gap-fill 결과가 Knowledge Manager 또는 SAM evidence에
실제로 연결됐는지 확인한다.

민감한 내용 자체를 출력하지 말고,
evidence 존재/건수/상태만 확인한다.

판정:

```text
12=A   # observed evidence 반영 확인
12=B   # 일부 evidence만 반영
12=C   # evidence 반영 없음
12=D   # Knowledge Manager 관련 실패
12=E   # 판단 불가
```

---

# 14. SAM MCD batch 완료 여부 확인

대상 SAM MCD Run에서:

```text
pending cycle/batch
completed batch
remaining fact gap
dependency_edges / cycle_members
```

상태를 확인한다.

판정:

```text
13=A   # 대상 batch 처리 완료 + pending 없음
13=B   # 일부 완료 + pending 남음
13=C   # batch 완료 호출 실패
13=D   # cycle/edge 데이터 자체 문제
13=E   # 결과가 대상 run과 연결되지 않음
13=F   # 판단 불가
```

가능하면:

```text
MCD_PROGRESS=<completed>/<total>, pending=<count>
```

한 줄만 추가.

---

# 15. 최종 MCD 보고서 재렌더링 확인

최신 SAM MCD Run의 보고서를 확인한다.

우선 범위:

```text
~/l1sw-private-skills/l1-sam-fixer/output/
~/l1sw-private-skills/l1-sam-fixer/data/
```

확인 항목:

```text
대상 MCD Run과 동일한 run인지
보고서 mtime이 해당 gap-fill 실행 이후인지
latest_report/checkpoint와 연결되는지
HTML/MD/Jira 등 기대 artifact 존재 여부
cycle_members 비정상 empty 여부
dependency_edges 비정상 empty 여부
CODE_FACT / CODE_VERIFIED 등 code evidence 반영 여부
ANALYSIS_REQUIRED / UNRESOLVED가 이전보다 해결되었는지 또는 pending으로 명시됐는지
```

판정:

```text
14=A   # 보고서 정상 재렌더링 + evidence 반영
14=B   # 보고서 재렌더링됐으나 일부 gap/pending 남음
14=C   # Study는 수행됐지만 보고서 재렌더링 실패
14=D   # 보고서는 있으나 실행 전 stale 보고서
14=E   # cycle_members/dependency_edges 핵심 결함
14=F   # 최신 보고서를 특정할 수 없음
14=G   # 판단 불가
```

추가:

```text
REPORT=<path basename 또는 NA>
REPORT_TIME=<timestamp|NA>
```

---

# 16. Dispatcher가 이 Skill 상태를 실제 관측했는지 확인

Dispatcher v0.3.8의 `report`와 local snapshot/state에서
가능하면 다음을 확인한다.

```text
l1-study-runner coarse status
l1-sam-fixer coarse status
observer completed_at
reason / quality
```

이번 Job 실행과 timestamp가 맞는지 확인한다.

판정:

```text
15=A   # Dispatcher가 이번 MCD 결과를 정상 관측
15=B   # Dispatcher는 실행 중이나 이번 Skill 결과는 아직 미관측
15=C   # stale/이전 observer를 관측
15=D   # Dispatcher observer 처리 오류
15=E   # 판단 불가
```

---

# 17. 최종 정상동작 판정

아래 중 하나만 선택한다.

```text
16=A   # 완전 정상
       # Dispatcher 정상 + Job 실행 + gap-fill 완료 + report 재렌더링 완료

16=B   # 정상 부분완료
       # Job/Dispatcher는 정상이나 ANALYSIS_PARTIAL continuation이 남음

16=C   # Dispatcher 문제
       # Job 결과와 별개로 Dispatcher 설치/스케줄/실행/signal 관측 문제

16=D   # Job-list 미실행/activation 문제

16=E   # l1-study-mcd profile 문제

16=F   # dependency gate 문제

16=G   # Study Runner 실행 실패

16=H   # Code Analyzer gap-fill 문제

16=I   # Knowledge evidence 반영 문제

16=J   # SAM batch/report 재렌더링 문제

16=K   # stale/observer 연결 문제

16=L   # 여러 계층 문제

16=M   # 근거 부족으로 판단 불가
```

권장 완전 정상 조건:

```text
1=A
2=A
3=A
4=A 또는 B(일시 pending만)
5=A
6=A
7=A
8=A
9=A
10=A
11=A
12=A
13=A
14=A
15=A
→ 16=A
```

`10=B/C`이고 나머지 실행 체인이 정상이라면
무조건 실패로 만들지 말고 우선 `16=B`를 검토한다.

---

# 18. 비정상일 때만 LLM 원인 진단

`16 != A`이면
단순 상태 코드만 나열하지 말고 실제 증거를 따라가서
**가장 앞단의 실제 원인(root/first blocker)** 을 하나 선택한다.

```text
17=A   # Dispatcher 미설치/버전 문제
17=B   # Dispatcher scheduler 미등록/비활성
17=C   # Dispatcher runtime/signal 오류
17=D   # Job-list 업데이트/설치 문제
17=E   # Job 미activation / expiry / 미실행
17=F   # duplicate/target mismatch/reject
17=G   # l1-study-mcd profile 생성/contract 문제
17=H   # dependency gate 문제
17=I   # Study Runner 자체 실패
17=J   # 정상 PARTIAL — continuation 필요
17=K   # Code Analyzer child 분석 문제
17=L   # Knowledge Manager evidence 문제
17=M   # SAM batch completion 문제
17=N   # SAM report rerender 문제
17=O   # stale observer / timestamp 연결 문제
17=P   # 기타 실제 reason
17=Q   # 증거 부족
```

중요:

```text
가장 먼저 실패한 계층을 root cause로 선택한다.
후속 실패를 root cause처럼 보고하지 않는다.
```

예:

```text
l1-study-mcd profile 없음
→ Study Runner 미실행
→ MCD report 미갱신
```

이면 root cause는 `17=G`이다.

---

# 19. 문제 시 확인 깊이

문제가 있을 때만 아래 순서로 추가 확인한다.

```text
1. 설치 VERSION
2. target Job request
3. activation
4. processed/history
5. observer
6. l1-study-mcd profile
7. Study Runner nightly_result / checkpoint
8. dependency gate
9. 해당 child Code Analyzer result
10. Knowledge evidence
11. SAM batch state
12. SAM latest report
13. Dispatcher state/report/log
```

무제한 검색 금지.

각 단계에서 명확한 blocker가 나오면
그 blocker를 우선 원인으로 채택하되,
후속 결과가 왜 안 생겼는지 연결관계만 짧게 확인한다.

---

# 20. 최종 출력 형식

**설명문을 길게 쓰지 말고 아래 형식 그대로 출력해줘.**

```text
1=A
2=A SCHED=<...>
3=A LAST_CYCLE=<...>
4=A SIGNAL=<...>
5=A JOBLIST_VER=<...>
6=A JOB=<...> PROFILE=<...>
7=A EXEC=<...>
8=A
9=A
10=A STUDY=<...>
11=A
12=A
13=A MCD_PROGRESS=<...>
14=A REPORT=<...> REPORT_TIME=<...>
15=A
16=A
17=NA

18=정상. Dispatcher와 마지막 MCD gap-fill Job이 모두 정상 수행됐고 MCD 보고서 재렌더링까지 확인됨.
```

문제 예:

```text
1=A
2=A SCHED=autotask-builder
3=A LAST_CYCLE=...
4=A SIGNAL=failed=0,pending=0
5=A JOBLIST_VER=0.3.62
6=A JOB=JOB-20260831-MCD-GAP-FILL-0110 PROFILE=l1-study-mcd
7=F EXEC=REJECTED: profile unavailable
8=D
9=E
10=H STUDY=NO_RESULT
11=F
12=E
13=F MCD_PROGRESS=NA
14=D REPORT=... REPORT_TIME=...
15=A
16=E
17=G

18=문제: l1-study-mcd profile이 준비되지 않아 Job이 실행 단계로 진입하지 못함.
19=근거: <가장 직접적인 실제 파일/상태/reason 1개>
20=조치: <사용자가 다음에 해야 할 최소 조치 1줄>
```

---

# 21. 출력 제한

최종 답변은 다음을 지킨다.

```text
번호는 반드시 숫자 사용
질문 제목 재출력 금지
장문 설명 금지
가능하면 A/B/C 객관식 사용
경로는 문제 증거가 필요할 때만 1개 표시
로그 원문 대량 출력 금지
소스코드 내용 출력 금지
사내 민감정보 출력 금지
추측 금지
자동 수정 금지
자동 재실행 금지
```

사용자가 실제로 확인해야 할 핵심은 마지막:

```text
16=<최종판정>
17=<원인>
18=<짧은 결론>
19=<핵심 근거, 문제일 때만>
20=<최소 조치, 문제일 때만>
```

이다.

이 기준으로 지금 회사 Linux PC의 실제 상태를 읽고 확인해줘.
