# Job-list 실행 결과를 GitHub Fail/Pass로 판정하는 버전 비종속 메커니즘

## 1. 문서 목적

이 문서는 회사 PC에서 현재 설치된 Job-list의 설치 및 실행 상태를 외부 GitHub Release Asset으로 읽기 전용 관측하는 운영 계약을 정의한다.

이 계약은 특정 Job-list 버전에 종속되지 않는다. Job-list가 업데이트되더라도 관측 단계명, Asset 이름, 보안 경계와 판정 의미를 유지한다. 실행된 실제 버전은 로컬 evidence의 `engine_version`과 설치 identity로 확인한다.

핵심 원칙:

1. 회사 PC에는 외부 GitHub 쓰기 권한을 부여하지 않는다.
2. 회사 PC는 승인된 Release Asset에 HTTPS GET만 수행한다.
3. 개인 PC 또는 승인된 유지보수 PC만 Release Asset을 관리한다.
4. GitHub `download_count`의 실행 전후 delta로 원격 진행 상태를 1차 판정한다.
5. 로컬 durable evidence를 최종 진실로 사용한다.
6. 관측 실패는 이미 확정된 설치 또는 Job 결과를 바꾸지 않는다.

### 1.1 관련 문서

| 문서 | 다루는 것 | 질문 |
|---|---|---|
| **이 문서** | 실행이 **어디까지 진행됐는지** 판정 | "설치가 성공했나?" |
| `remote_trigger_and_liveness_mechanism.md` | 실행을 **언제 시작시킬지**와 **살아 있는지** | "지금 돌릴 수 있나? 애초에 살아 있나?" |

두 계약은 같은 신호 채널을 쓰지만 다른 Asset 집합을 사용한다. 신호 요청 정책(§10), 전파 지연(§13.1), 오판 방지 규칙(§16)은 양쪽에 공통으로 적용된다.

---

## 2. 이 계약이 해결하는 문제

관측 채널이 단계 해상도를 갖지 못하면 서로 다른 사건이 모두 같은 값으로 보인다. 특히 **모든 delta가 `0`인 상태**는 다음을 구분하지 못한다.

| 실제 사건 | 정상 여부 |
|---|---|
| Scheduler cycle 자체가 실행되지 않음 | 이상 |
| cycle은 실행됐으나 대상 패키지가 이미 최신이라 installer 미실행 | **정상** |
| 다운로드 실패 | 이상 |
| 패키지 검증 차단 | 이상 |
| 실행은 정상이나 Asset이 없어 신호가 404로 소멸 | 관측 결함 |
| 실행은 정상이나 count 전파가 아직 완료되지 않음 | 관측 시점 오류 |

`0`을 곧바로 실패로 읽으면 위의 정상 두 건과 관측 결함 두 건을 모두 실패로 오판한다. 이 계약의 목적은 관측값 하나하나가 **어떤 사건까지 좁혀주는지**를 고정하는 데 있다.

판정 가능한 상태로 만들기 위한 네 가지 수단은 다음과 같다.

1. 단계 세분화: 어디까지 진행했는지를 마지막 성공 단계로 특정한다.
2. 갱신 강제: 새 배포를 올려 "이미 최신이라 정상적으로 아무 일도 없었음"을 제거한다.
3. 독립 카나리아: 대상 패키지 밖에서 엔진 생존 여부를 따로 확인한다.
4. **생존 신호(heartbeat): 할 일의 유무와 무관하게 매 cycle 무조건 발사한다.**

네 번째가 위 표의 첫 두 행을 근본적으로 분리한다. 1~3번은 모두 "무언가 할 일이 있었을 때"만 증거를 남기므로, 할 일이 없는 정상 상태와 cycle 자체가 죽은 상태를 끝내 구분하지 못한다. 생존 신호는 그 구분을 유일하게 해결한다.

생존 신호의 발사 주체와 계약은 별도 문서 `remote_trigger_and_liveness_mechanism.md`에서 정의한다. 이 문서는 그 신호를 판정에 사용하는 방법만 다룬다.

---

## 3. 보안 경계

| 환경 | 허용 | 금지 |
|---|---|---|
| 회사 PC | HTTPS GET, metadata READ, package/job 다운로드 | push, upload, Release 편집, Asset 삭제, 외부 write API |
| 개인/유지보수 PC | 승인된 Release/Asset 유지보수, 패키지 배포 | 회사 데이터 또는 상세 실행 결과 업로드 |

회사의 실행 결과 본문은 GitHub로 전송하지 않는다. 회사 PC가 미리 준비된 Asset을 GET하면 GitHub의 누적 `download_count`만 증가한다.

모든 관측 URL은 호출 전에 allowlist로 검사한다.

```text
PASS endpoint:
https://github.com/wonhwipark/Pass/releases/download/signal-v1/pass.signal

FAIL 및 단계 endpoint prefix:
https://github.com/wonhwipark/Fail/releases/download/signal-v1/
```

단계 신호는 `<skill>-<stage>.signal` 형식만 허용한다. 다른 scheme, host, repository, tag 또는 path는 네트워크 요청 전에 거부한다.

---

## 4. 버전 비종속 Asset 계약

### 4.1 최종 호환 신호

```text
pass.signal
fail.signal
```

- 전체 결과가 `SUCCESS`이면 `pass.signal`을 기본 2회 GET한다.
- 전체 결과가 `SUCCESS`가 아니면 `fail.signal`을 기본 2회 GET한다.
- 실행 가능한 Job이 없는 성공 cycle은 최종 호환 신호를 생략할 수 있다.
- 운영 정책으로 반복 횟수를 1회까지 낮출 수 있으나 2회를 초과하지 않는다.

### 4.2 설치 단계 신호

```text
job-list-install-start.signal
job-list-source-scanned.signal
job-list-identity-ok.signal
job-list-identity-mismatch.signal
job-list-canonical-copied.signal
job-list-legacy-merged.signal
job-list-entry-written.signal
job-list-sha-verified.signal
job-list-install-confirmed.signal
job-list-fail-install.signal
```

### 4.3 Runner 단계 신호

```text
job-list-runner-start.signal
job-list-context-ready.signal
job-list-queue-valid.signal
job-list-intake-written.signal
job-list-queue-claimed.signal
job-list-job-start.signal
job-list-job-committed.signal
job-list-run-pass.signal
job-list-run-fail.signal
```

### 4.4 이름 규칙

Asset 이름에는 버전 번호를 넣지 않는다. 패치 버전이 바뀌어도 같은 이름과 의미를 유지한다.

버전 접두를 쓰면 두 가지가 동시에 깨진다. 첫째, 배포마다 Asset 세트를 새로 만들어야 하고 하나라도 누락되면 그 단계는 영구히 `0`이 된다. 둘째, 패키지 안에 박힌 접두가 실제 배포 버전과 어긋나면 관측값이 어느 버전의 실행인지 식별할 수 없게 된다. 실제로 패키지 버전만 올리고 신호 접두를 이전 값으로 남긴 배포가 있었고, 그 구간의 count는 두 버전 중 어느 쪽 실행인지 구분할 수 없었다.

실행된 버전은 Asset 이름이 아니라 로컬 설치 identity로 확인한다.

---

## 5. 단계별 정확한 의미

| 단계 | 호출 주체 | 신호가 확정하는 사실 |
|---|---|---|
| `install-start` | installer | installer entry 진입 |
| `source-scanned` | installer | source에 허용되지 않은 symlink/junction-like entry 없음 |
| `identity-ok` | installer | 다섯 identity가 모두 존재하고 패키지 버전과 일치 |
| `identity-mismatch` | installer | identity 검증 실패로 설치 중단 |
| `canonical-copied` | installer | canonical implementation 복사 완료 및 `SKILL.md` 존재 |
| `legacy-merged` | installer | legacy storage 병합 완료 |
| `entry-written` | installer | discovery entry에 `SKILL.md` 기록 완료 |
| `sha-verified` | installer | canonical과 entry의 `SKILL.md` SHA-256 일치, entry에 `SKILL.md`만 존재 |
| `install-confirmed` | installer | 위 검증을 모두 통과하고 설치 evidence durable write 완료 |
| `fail-install` | installer | installer가 명시적 예외를 포착함 |
| `runner-start` | runner | Python runner entry 진입 |
| `context-ready` | runner | branch, transport, canonical result root 결정 완료 |
| `queue-valid` | runner | queue schema 검증 성공 |
| `intake-written` | runner | run별 intake evidence atomic write 완료 |
| `queue-claimed` | runner | run별 queue-claimed evidence atomic write 완료 |
| `job-start` | runner | 실제 실행 대상 Job의 executor 호출 직전 |
| `job-committed` | runner | 해당 executor-started Job의 outcome/history/processed 및 queue 결과 commit 완료 |
| `run-pass` | runner | runner 최종 상태가 `SUCCESS`로 계산됨 |
| `run-fail` | runner | runner 최종 상태가 `SUCCESS`가 아닌 상태로 계산됨 |

단계 신호는 호출 주체가 확정할 수 있는 범위보다 넓게 해석하지 않는다.

특히 `install-confirmed`는 installer 내부 검증 완료를 의미하며 Skill-Updater 전체 transaction의 최종 commit을 의미하지 않는다. 이후 updater 외곽 검증 실패나 rollback은 별도로 발생할 수 있다.

### 5.1 실패 지점은 마지막 성공 단계로 특정한다

실패 Asset을 단계 수만큼 만들지 않는다. 성공 단계가 순서대로 배치되어 있으면, **마지막으로 증가한 단계와 그다음 단계 사이**가 실패 구간이다.

```text
source-scanned +1, identity-ok 0, identity-mismatch 0
  -> identity 수집 도중 중단
source-scanned +1, identity-mismatch +1
  -> identity 불일치로 정상 거부
canonical-copied +1, legacy-merged 0
  -> legacy 병합 구간에서 중단
entry-written +1, sha-verified 0
  -> entry 기록 후 checksum 검증 실패
```

`identity-mismatch`와 `fail-install`만 별도 실패 출구로 둔다. 전자는 계약이 정의한 정상 거부이고, 후자는 그 외 예외의 포괄 표지다.

---

## 6. Installer 확인 계약

`install-confirmed`는 다음 검증을 모두 통과한 뒤에만 호출한다.

1. source에 허용되지 않은 symlink 또는 junction-like entry가 없다.
2. 다음 다섯 identity가 패키지의 현재 버전과 모두 같다.

```text
VERSION
.skill-release.json.version
SKILL.md 선언 version
skillsilent/contract.json.skill_version
skillsilent/manifest.json.skill_version
```

3. canonical implementation 복사가 완료됐다.
4. discovery entry에는 `SKILL.md`만 존재한다.
5. canonical과 discovery entry의 `SKILL.md` SHA-256이 같다.
6. 설치 검증 receipt와 관측 evidence가 canonical output 아래에 durable write됐다.

하나라도 실패하면 `install-confirmed`를 보내지 않는다. identity 불일치는 `identity-mismatch`, 그 외 예외는 `fail-install`을 best-effort로 호출한다.

**identity 검증은 파일을 복사하기 전에 수행한다.** 복사 후에 검증하면 이미 불일치 패키지가 canonical에 반영된 뒤이며, rollback 실패 시 잘못된 구성이 남는다.

ZIP 파일명이나 일부 metadata만 갱신해서는 안 된다. 과거 선택된 ZIP 버전과 authoritative metadata가 달라 updater가 `RELEASE_IDENTITY_MISMATCH`로 설치를 차단한 사례를 재발 방지 기준으로 삼는다.

### 6.1 nested manifest의 지위

Skill-Updater는 top-level `.skill-release.json`, `VERSION`, `SKILL.md`만 authoritative로 취급하고 nested manifest는 관찰값으로 둔다. 따라서 `skillsilent/contract.json`과 `skillsilent/manifest.json`이 뒤처져 있어도 updater는 경고만 남기고 설치를 진행할 수 있다.

updater가 차단하지 않는다는 사실이 계약 위반을 정당화하지 않는다. installer는 다섯 identity 전부를 hard gate로 검사해야 한다. 실제로 nested manifest 두 개가 이전 버전 값으로 남은 패키지가 updater를 통과해 설치된 사례가 있으며, 이 경우 설치된 스킬의 자기 신고 버전이 파일마다 달라진다.

### 6.2 배포된 identity는 불변이다

한 번이라도 배포(업로드, 설치, 또는 §17 게이트 통과)된 버전의 내용을 그 자리에서 고치고 같은 identity로 다시 내보내지 않는다. 내용이 바뀌면 반드시 새 버전을 발급한다.

이 원칙을 어기면 두 가지가 동시에 일어난다.

1. 이미 그 버전을 설치한 PC는 "로컬 버전 == 원격 후보 버전"이므로 갱신을 건너뛴다. 새로 넣은 코드는 그 PC에서 영원히 실행되지 않는다.
2. 이 건너뜀은 **정상 SKIPPED와 구분되지 않는다.** installer가 아예 호출되지 않으므로 어떤 신호도 발사되지 않고, 실패 흔적이 전혀 남지 않는다. §2가 "정상"으로 분류한 "이미 최신이라 installer 미실행" 사례와 원격에서 완전히 동일하게 보인다.

이 실수는 스스로를 감춘다 — 결과를 보고는 알아챌 방법이 없다. 예방은 버전 번호 규율(§4.4, 본 절)을 지키는 것뿐이다.

---

## 7. Queue durable 경계와 Job 카운트 의미

Runner는 다음 순서를 지킨다.

```text
queue load
→ schema validate
→ queue-valid
→ intake.json atomic write
→ intake-written
→ queue_claimed.json atomic write
→ queue-claimed
→ Job별 executor 실행 및 결과 durable commit
→ 전체 상태 계산
→ 최종 신호
```

`queue_claimed.json`은 이 run이 실행 대상으로 삼은 `id:revision` 목록을 담고, **어떤 executor보다 먼저** 기록한다. 실행 도중 프로세스가 사라져도 무엇을 claim했는지가 로컬에 남는다.

`job-start`와 `job-committed`는 같은 모집단을 센다.

- `job-start`: executor를 실제 호출하는 Job만 1회 집계한다.
- `job-committed`: 그 executor-started Job의 결과를 durable commit한 뒤 1회 집계한다.
- `ALREADY_PROCESSED`, `DISABLED`, dependency block, 이전 실패에 따른 미실행, 실행 한도 초과 등 executor에 진입하지 않은 행은 두 카운터에서 제외한다.
- 정상적으로 완료된 한 실행 구간에서는 두 delta가 같아야 한다.
- `job-start > job-committed`이면 실행 중단 또는 commit 이전 장애 가능성이 있다.
- `job-committed > job-start`는 계약 위반 또는 관측 구간 중첩을 의미한다.

원본 queue는 각 결과가 durable commit되기 전에 파괴하거나 소비하지 않는다. Retryable failure와 미실행 결과는 다음 cycle의 재시도 대상으로 남긴다. 완료 receipt는 `SUCCESS`에만 기록한다.

---

## 8. 계측 가능 경계

관측 코드를 넣을 수 있는 위치는 **배포되는 패키지 안**뿐이다. 그 앞 구간은 이미 대상 PC에 설치된 실행 엔진의 코드이므로, 새 패키지를 올려도 그 cycle에는 반영되지 않는다.

| 구간 | 실행 주체 | 계측 가능 여부 |
|---|---|---|
| Scheduler 기동 | OS scheduler | 불가 |
| 원격 후보 조회 | 엔진 | 불가 (해당 cycle에는 반영 안 됨) |
| 패키지 다운로드 | 엔진 | 조건부 (아래 8.1) |
| SHA·identity 검증, 설치 판정 | 엔진 | 불가 (해당 cycle에는 반영 안 됨) |
| installer 진입 이후 | **패키지** | **가능** |
| runner 전 구간 | **패키지** | **가능** |

따라서 `install-start`가 증가하지 않은 상태는 그 앞 네 구간 중 어디서 끊겼는지 **단독으로는 구분할 수 없다.** 이 구분에는 §9의 카나리아와 로컬 evidence가 필요하다.

### 8.1 다운로드 자체를 신호로 쓰는 조건

패키지 배포 방식이 Release Asset이면 엔진이 `browser_download_url`로 내려받으므로 패키지 ZIP의 `download_count`가 그대로 "엔진이 이 패키지를 실제로 받았다"는 신호가 된다. 코드 변경이 전혀 필요 없다.

반면 저장소 root ZIP 방식이면 `raw.githubusercontent.com`을 사용하며 **이 경로에는 다운로드 카운터가 없다.**

배포 방식은 대상 PC의 로컬 config가 결정하므로 원격에서 전환할 수 없다. 전환하려면 대상 PC에서 직접 설정해야 한다.

---

## 9. 독립 카나리아

대상 패키지와 무관한 두 번째 패키지에 설치 단계 신호를 심어 함께 배포한다. 카나리아는 최소 3단계만 갖는다.

```text
<canary>-install-start.signal
<canary>-install-confirmed.signal
<canary>-fail-install.signal
```

판정:

| 카나리아 | 대상 패키지 | 해석 |
|---|---|---|
| 증가 | 증가 | 엔진·대상 모두 정상. 세부 단계로 내부 진행 판독 |
| 증가 | `0` | 엔진은 생존. **대상 패키지 고유 문제** |
| `0` | `0` | **Scheduler 또는 엔진 자체가 실행되지 않음** |
| `0` | 증가 | 관측 구간 중첩 또는 카나리아 미등록 확인 필요 |

카나리아 선정 기준:

1. 대상 PC의 updater config에 **이미 등록되어 있고 활성**일 것. 미등록 스킬은 아무리 배포해도 처리되지 않는다. 등록은 대상 PC의 로컬 config이므로 원격에서 추가할 수 없다.
2. 자체 native installer를 가질 것. installer가 없으면 신호를 넣을 위치가 없다.
3. 패키지가 작고 부작용이 적을 것.
4. 다섯 identity가 이미 일치할 것. 그래야 신호 부재를 패키지 결함이 아니라 엔진 미도달로 읽을 수 있다.

---

## 10. 요청 정책

모든 단계 및 최종 신호 요청은 다음 속성을 사용한다.

```text
Method: GET
Scheme: HTTPS
Accept: application/octet-stream
Cache-Control: no-cache
Pragma: no-cache
Timeout: 짧고 유한한 값
Success: HTTP 200 이상 400 미만
```

단계 신호는 제한된 횟수만 재시도한다. 권장 기본값은 최대 3회이며 첫 지연부터 지수 백오프를 적용한다. 최종 `pass.signal`/`fail.signal`은 기존 운영 해석을 위해 최대 2회 정책을 유지한다.

신호 요청은 best-effort 관측 기능이다.

- 네트워크 실패가 설치 성공을 실패로 바꾸지 않는다.
- 네트워크 실패가 Job 성공을 실패로 바꾸지 않는다.
- 실패한 요청도 로컬 evidence에 기록한다.
- GitHub count가 증가하지 않았다면 로컬 evidence와 함께 판정한다.

User-Agent는 집계에 영향을 주지 않는다. 서로 다른 User-Agent로 보낸 요청이 모두 집계되는 것을 확인했다.

### 10.1 best-effort 확장 단계는 함수 자신이 예외를 흡수한다

한 단계의 결과가 대상 패키지 자신의 성공/실패에 영향을 주면 안 된다고 선언했다면, 그 보장은 **함수 정의 내부**에 있어야 한다. 호출부의 try/except만으로 보장하면, 그 함수가 다른 경로로 재사용되거나 내부 로직이 확장될 때 이 보장이 조용히 깨질 수 있다.

이 함수를 격리 상태에서(실제 대상이 아니라 합성 fixture로) 직접 호출해 고의로 손상된 입력을 주고도 예외 없이 알려진 결과값 집합 중 하나만 반환하는지 검증한다. 이 검증이 없으면 "never raises"는 코드가 아니라 주석의 주장일 뿐이다.

---

## 11. 관측 내구성

### 11.1 Correlation ID

installer와 runner는 각 process/run에 correlation ID를 부여한다. scheduler 또는 updater가 `JOB_LIST_CORRELATION_ID`를 전달하면 전체 체인이 같은 값을 사용한다.

GitHub `download_count` 자체에는 correlation ID가 없으므로 다음 용도로만 사용한다.

- 로컬 installer JSONL과 runner JSONL 연결
- summary와 단계 시도 연결
- 동일 시간대의 중복 실행 구분

### 11.2 JSONL durable evidence

모든 단계 시도는 canonical Job-list output 아래 append-only JSONL로 기록한다.

권장 record:

```json
{
  "schema_version": 1,
  "engine_version": "<installed-version>",
  "component": "installer-or-runner",
  "correlation_id": "<correlation-id>",
  "run_id": "<run-id-or-null>",
  "job_key": "<id:revision-or-null>",
  "stage": "<stage>",
  "attempted_at": "<timestamp>",
  "url": "<allowlisted-url>",
  "attempts": [],
  "ok": true,
  "status": 200,
  "resolved_url": "<resolved-url>",
  "error": null,
  "completed_at": "<timestamp>"
}
```

기록은 append 후 flush/fsync한다. 관측 파일 쓰기 실패는 본 작업 결과를 뒤집지 않지만 가능한 경우 summary의 `persistence_error`에 남긴다.

**로컬 JSONL은 원격 판정을 대체하지 않는다.** 대상 PC에 접근할 수 없는 동안에는 읽을 수 없으므로, 원격에서만 판정해야 하는 상황에서는 단계 신호의 해상도를 높이는 편이 우선한다. 두 수단은 용도가 다르다. 신호는 접근 불가 구간의 1차 판정용이고, JSONL은 접근 가능해진 뒤의 원인 확정용이다.

### 11.3 보존과 회전

- JSONL은 크기 기준으로 회전한다.
- 기본 권장 한도는 파일당 1 MiB이다.
- 기본 권장 보존은 현재 파일과 이전 5세대이다.
- 회전은 canonical output 안에서만 수행한다.
- retired `~/.claude/main` 또는 branch output을 영속 SSOT로 사용하지 않는다.

### 11.4 진단 요약

Runner summary에는 최소한 다음 값을 포함한다.

```text
correlation_id
observation JSONL path
전체 단계 시도 수
성공/실패 수
stage별 record 수
executor 시작 수
executor outcome commit 수
최종 일반 PASS/FAIL 신호 결과
최종 run-pass/run-fail 단계 신호 결과
```

Installer summary에는 다음 값을 포함한다.

```text
correlation_id
설치된 실제 버전
다섯 identity 검증 결과
canonical/entry SKILL.md SHA-256
discovery entry 파일 목록
install-confirmed 전송 결과
```

---

## 12. 최종 신호의 이중 계약

두 종류의 최종 신호를 함께 사용할 수 있다.

1. 일반 `pass.signal`/`fail.signal`
   - 기존 운영 대시보드 호환용
   - 기본 2회 GET
   - 실행 가능한 Job이 없는 성공 run에서는 생략 가능

2. `job-list-run-pass.signal`/`job-list-run-fail.signal`
   - runner가 최종 상태 계산 지점까지 도달했는지 진단
   - 단계 신호 정책에 따라 호출

두 계층은 중복 결함이 아니다. 일반 신호는 최종 결과 호환 계약이고, `job-list-run-*`는 최종 단계 도달 여부를 분리 진단하는 계약이다.

---

## 13. 원격 운영 판정

### 13.1 전파 지연

`download_count`는 즉시 갱신되지 않는다. **성공한 GET이 API 응답에 반영되기까지 최대 약 20분이 걸리는 것을 실측했다.** 같은 시각에 보낸 요청이라도 Asset마다 반영 시점이 다르다.

따라서 관측 시각은 다음을 만족해야 한다.

```text
관측 시각 >= cycle 종료 예상 시각 + 20분
```

이 여유를 두지 않고 읽은 `0`은 판정 근거가 되지 못한다. 지연 때문에 아직 반영되지 않은 것과 실행되지 않은 것이 같은 값으로 보이기 때문이다.

### 13.2 관측 전

예정된 Fresh Cycle 직전에 관련 Asset의 `download_count`를 한 번 읽고 기준값을 저장한다. Asset 본문을 브라우저로 직접 다운로드하지 않는다.

유지보수 PC에서 검증이나 시험 실행을 했다면, **그 활동의 전파가 끝난 뒤에** baseline을 잡는다.

### 13.3 관측 후

Fresh Cycle 종료 예상 시점에 §13.1의 여유를 더한 뒤 같은 Asset metadata를 다시 읽어 delta를 계산한다.

```text
DELTA = AFTER - BASE
```

`download_count`는 누적값이며 run ID를 포함하지 않는다. 절대값만 보고 특정 실행 결과를 단정하지 않는다.

### 13.4 카운터 유효성 확인

관측 결과로 실패를 판정하기 전에, 카운터가 지금 동작하는지를 먼저 확인한다. 방법은 대조 실험이다.

```text
1. 대상과 무관한 Asset 하나를 고른다.
2. 그 Asset에 HTTPS GET을 1회 보내고 HTTP status를 기록한다.
3. 20분 뒤 count를 다시 읽는다.
```

- count 증가 → 카운터 정상. `0`인 단계는 실제로 신호가 도달하지 않은 것이다.
- count 불변 → 카운터를 신뢰할 수 없다. **이 구간의 모든 원격 판정을 보류하고** 로컬 evidence로만 판단한다.

이 확인 없이 `0`을 실패로 읽지 않는다. 이 절차는 카운터가 정상임을 확인하는 데 실제로 사용되었고, 그 결과 실행 1회가 만든 단계별 증가분이 코드상의 호출 횟수와 정확히 일치함을 확인했다.

### 13.5 주요 판정표

| 관측 delta | 1차 판정 |
|---|---|
| **heartbeat `0`** | **Scheduler 또는 dispatcher 미실행. 아래 행을 해석하기 전에 이것부터 본다** |
| heartbeat 증가, 나머지 전부 `0` | **정상.** 살아 있고 이번 구간에 할 일이 없었음 |
| heartbeat 증가, 카나리아 `0`, 대상 `0` | 엔진까지 도달하지 못함. dispatcher와 엔진 사이 구간 문제 |
| 카나리아 `0`, 대상 `0` (heartbeat 미도입 시) | Scheduler 또는 엔진 미실행 |
| 카나리아 `+1`, `install-start 0` | 엔진 생존, 대상 패키지 다운로드·검증·선택 구간 문제 |
| `install-start +1`, 이후 0 | installer 진입 후 중단, 프로세스 종료 또는 신호 실패 가능 |
| `source-scanned +1`, `identity-* 0` | identity 수집 도중 중단 |
| `identity-mismatch +1` | 패키지 identity 불일치로 정상 거부 |
| `canonical-copied +1`, `legacy-merged 0` | legacy 병합 구간 중단 |
| `entry-written +1`, `sha-verified 0` | entry 기록 후 checksum 또는 entry 구성 검증 실패 |
| `install-confirmed +1`, `runner-start 0` | installer 검증 완료 후 runner 이전 구간 중단 또는 Job Sync 비활성 |
| `runner-start +1`, `queue-valid 0` | context/queue load/validation 이전 또는 도중 실패 가능 |
| `queue-valid +1`, `intake-written 0` | durable intake 이전 중단 가능 |
| `intake-written +1`, `queue-claimed 0` | durable queue claim 이전 중단 가능 |
| `job-start > job-committed` | executor 시작 후 durable 결과 commit 전 중단 가능 |
| `run-pass +1`, `pass.signal +2` | 정상 성공 관측 |
| `run-fail +1`, `fail.signal +2` | 오류 포함 완료 또는 runner 실패 관측 |
| `runner-start +1`, 최종 신호 0 | 실행 중단, 빈 실행 또는 최종 신호 네트워크 실패 가능 |
| 모든 delta 0 | §13.1 여유와 §13.4 유효성 확인을 먼저 수행한 뒤에만 해석. 생존 신호가 도입돼 있으면 그 값이 먼저 판정을 가른다 |

단계 신호가 재시도될 수 있으면 성공적인 한 단계가 delta `1`보다 크게 나타날 수 있다. 정확한 시도 수와 성공 여부는 로컬 JSONL로 확정한다.

### 13.6 갱신 강제

`install-start 0`에는 "이미 최신이라 installer가 정상적으로 실행되지 않았다"는 정상 해석이 항상 포함된다. 이 해석을 제거하려면 관측 구간 전에 **대상 패키지의 새 버전을 배포**한다.

그러면 대상 PC의 설치 버전이 무엇이든 그 cycle에서 반드시 installer가 실행되므로, `install-start 0`은 정상 해석을 잃고 이상으로 좁혀진다.

---

## 14. 최종 상태와 재시도

다음 상태가 하나라도 있으면 전체 결과를 오류 포함 상태로 판정한다.

```text
FAILED
FAILED_SAFE
CRITICAL
BLOCKED
BLOCKED_SAFE
COMPLETED_WITH_ERRORS
NOT_ATTEMPTED_PREVIOUS_FAILURE
NOT_ATTEMPTED_LIMIT
```

정책:

- `SUCCESS`: 완료 receipt 생성, 같은 `id:revision` 중복 실행 방지
- Retryable failure: SUCCESS receipt를 만들지 않고 queue에 남겨 다음 cycle에서 재시도
- Terminal-safe block: SUCCESS로 위장하지 않되 무한 재시도를 방지
- queue 검증, lock, 파일 접근 등 외곽 예외: runner 전체 `FAILED`

최종 선택 규칙:

```text
overall == SUCCESS  → PASS
overall != SUCCESS  → FAIL
```

---

## 15. 로컬 authoritative evidence

GitHub 신호는 원격 1차 관측 수단이다. 최종 원인은 회사 PC의 canonical Job-list output으로 확정한다.

필수 로컬 정보:

- 실제 설치/실행 버전
- correlation ID와 run ID
- Job별 `id:revision`
- Job별 status 및 오류
- queue 잔여 항목
- 단계별 HTTP status와 오류
- 일반 PASS/FAIL 신호 결과
- retryable/terminal 분류
- **Job Sync 활성 여부**

Job Sync가 비활성이면 runner 계열 신호는 구현과 무관하게 영구히 `0`이다. 이 경우 runner 단계의 `0`은 실패가 아니라 미실행이며, Job이 애초에 처리되지 않고 있다는 별개의 문제를 뜻한다. 원격 신호만으로는 이 상태를 확인할 수 없으므로 로컬에서 반드시 확인한다.

경로는 canonical Job-list root 아래의 다음 논리 구조를 따른다.

```text
output/runs/<run_id>/summary.json
output/runs/<run_id>/intake.json
output/runs/<run_id>/queue_claimed.json
output/result-signal/<run_id>.json
output/observations/<run_id>.jsonl
output/install-observations/latest-install.json
output/install-observations/latest-summary.json
data/state/history/job_history.jsonl
```

정확한 물리 경로는 설치 환경의 canonical private root를 따른다. retired `~/.claude/main`을 실행, 결과, 관측 또는 fallback 경로로 사용하지 않는다.

---

## 16. 오판 방지 규칙

1. 절대 `download_count`만 보고 현재 실행을 단정하지 않는다.
2. 반드시 실행 직전/직후 delta를 사용한다.
3. **전파 지연 여유를 확보하기 전의 `0`을 판정에 쓰지 않는다.**
4. **`0`을 실패로 읽기 전에 카운터 유효성을 대조 실험으로 확인한다.**
5. **Asset이 Release에 존재하는지 먼저 확인한다.** 없는 Asset에 대한 GET은 404이고, best-effort 정책상 조용히 무시되어 영구히 `0`으로 남는다. 이는 실행되지 않은 것과 구별되지 않는다.
6. 관측 구간에 브라우저 수동 다운로드를 섞지 않는다.
7. 수동 실행과 Scheduler 실행을 같은 관측 구간에 섞지 않는다. 유지보수 PC의 검증 실행도 마찬가지이며, 그 전파가 끝난 뒤 baseline을 다시 잡는다.
8. delta `0`을 자동 FAIL로 해석하지 않는다. `install-start 0`에는 "이미 최신"이라는 정상 해석이 포함된다.
9. PASS와 FAIL이 함께 증가하면 여러 run 또는 관측 구간 중첩을 확인한다.
10. 단계 신호 재시도 때문에 delta가 1보다 클 수 있음을 고려한다.
11. GitHub 신호와 로컬 evidence가 충돌하면 로컬 durable evidence를 우선한다.
12. `install-confirmed`를 updater 전체 commit으로 해석하지 않는다.
13. Asset 이름에 버전을 넣거나 버전마다 계약을 복제하지 않는다.
14. 엔진이 차단하지 않는다는 이유로 identity 불일치를 허용하지 않는다.
15. runner 신호의 `0`을 해석하기 전에 Job Sync 활성 여부를 확인한다.
16. 이미 배포되거나 설치된 버전의 내용을 그 자리에서 고쳐 같은 identity로 재배포하지 않는다(§6.2). 이 위반은 정상 SKIPPED와 원격에서 구분되지 않아 흔적 없이 사라진다.
17. best-effort 확장 단계가 실제로 예외를 흡수하는지 실제 실행으로 검증하기 전에는 "never raises" 주석을 신뢰하지 않는다(§10.1).
18. **생존 신호가 있는 구성에서는 그 값을 가장 먼저 읽는다.** 생존 신호가 `0`이면 나머지 단계의 `0`은 아무 정보도 주지 않는다. 실행 주체가 시작되지 않았으므로 어느 단계도 발사될 기회가 없었기 때문이다.
19. **수동 실행 성공을 예약 실행 성공의 근거로 삼지 않는다.** 두 경로는 실행 주체, 인터프리터, 콘솔 유무, 권한 컨텍스트가 다르며, 예약 경로에서만 나타나는 결함이 실제로 확인된 바 있다(`remote_trigger_and_liveness_mechanism.md` §13).
20. **진단 기능 자체를 검증 대상에서 제외하지 않는다.** 도구가 "문제없음"이라고 보고하는 것을 근거로 삼기 전에, 알려진 상태를 올바르게 보고하는지 먼저 확인한다. 진단이 거짓을 보고하면 멀쩡한 것을 고치는 동안 실제 문제는 방치된다.

---

## 17. 배포 전 검증 게이트

관측 계약을 바꾼 패키지는 유지보수 PC에서 다음을 통과한 뒤에만 배포한다. 하나라도 실패하면 배포하지 않는다.

1. 새 Asset 전체가 Release에 존재하고 baseline count를 기록했다.
2. 패키지의 다섯 identity가 모두 일치한다.
3. installer가 임시 대상 경로에 실제로 실행되어 정상 종료한다.
4. entry에 `SKILL.md`만 남고 canonical과 SHA-256이 일치한다.
5. **전파 지연 후 각 단계 count가 코드상의 호출 횟수와 정확히 일치한다.**
6. 실패 단계 Asset은 증가하지 않았다.
7. 패키지 테스트 스위트의 실패 집합이 직전 배포와 동일하다. 새 실패가 있으면 원인을 규명한다.
8. 배포용 아카이브의 경로 구분자가 `/`이고 최상위 항목이 스킬 폴더 하나뿐이다.
9. 자기 설치 이후에 이어지는 추가 단계(예: §19 부트스트랩)가 있다면, 그 단계까지 포함한 전체 프로세스가 예외 없이 종료하고 exit code가 0이다.

5번이 이 게이트의 핵심이다. 신호가 실제로 집계되는 것을 눈으로 확인하기 전에는, 그 배포로 얻은 모든 `0`이 실행 실패인지 관측 결함인지 구분할 수 없다.

9번은 단위 테스트만으로는 잡히지 않는다. 핵심 설치가 이미 성공한 뒤에 이어지는 부가 단계에서 처리되지 않은 예외가 발생하면 프로세스 exit code가 비정상이 되고, 엔진은 이를 installer 전체 실패로 해석해 성공한 설치를 rollback하거나 FAILED로 오분류할 수 있다. 실제로 이 항목의 실제 실행 검증이 정확히 이런 결함을 잡아냈다: 부가 단계 자체는 목표를 정확히 달성했지만 그 결과를 보고하는 신호 이름이 요청 목록에 등록되지 않아 처리되지 않은 예외로 크래시했다.

검증 실행은 관측 구간을 오염시키므로 §13.2에 따라 baseline을 다시 잡는다.

---

## 18. 릴리스 및 회귀 검증

Job-list 업데이트 전 다음을 자동 검증한다.

1. 다섯 package identity가 모두 같다.
2. ZIP 파일명 버전과 ZIP 내부 authoritative identity가 같다.
3. stage URL이 고정 allowlist를 만족하고 이름에 버전 토큰이 없다.
4. 요청 header에 no-cache, Pragma, octet-stream Accept가 있다.
5. 모든 단계 시도가 JSONL에 기록된다.
6. JSONL 회전 및 보존 한도가 동작한다.
7. 재시도 횟수가 제한되고 지수 백오프를 사용한다.
8. installer identity/SHA/entry 검증 실패 시 `install-confirmed`가 발생하지 않는다.
9. identity 검증이 canonical 복사보다 먼저 수행된다.
10. `intake-written`과 `queue-claimed`는 대응 파일의 atomic write 이후에만 발생한다.
11. `job-start`와 `job-committed`가 executor-started Job만 센다.
12. summary에 correlation 및 진단 집계가 포함된다.
13. 회사 PC 경로에서 외부 GitHub write 코드가 존재하지 않는다.
14. best-effort 확장 단계 함수를 격리 상태에서 고의로 손상된 입력으로 직접 호출해도 예외 없이 알려진 결과값 집합 중 하나만 반환한다(10.1).

### 18.1 규범 계약과 실제 ZIP의 준수 확인

각 릴리스의 별도 검증 산출물에는 최소 다음 항목을 남긴다. 이 운영 문서에는 특정 버전값을 고정하지 않는다.

| 항목 | 규범 계약 | 실제 ZIP에서 추출할 값 |
|---|---|---|
| Package identity | 다섯 identity와 ZIP filename 일치 | 각 identity 실제 값 |
| Installer Asset | `job-list-install-*.signal` 외 설치 단계 | installer URL 상수 |
| Runner Asset | `job-list-*.signal` | runner stage URL map |
| 요청 보안 | HTTPS allowlist 및 필수 header | request 생성 코드 |
| Durable evidence | canonical JSONL과 summary | 실제 write path와 schema |
| Queue 단계 | durable write 이후 signal | 실제 호출 순서 |
| Job 카운트 | executor-started Job만 집계 | 실제 조건과 호출 위치 |

실제 ZIP이 규범 계약과 다르면 `CONTRACT_IMPLEMENTATION_MISMATCH`로 기록한다. 이 경우 원격 증거를 무조건 폐기하지는 않지만, 실제 ZIP에서 추출한 Asset과 실제 호출 의미만 사용하여 제한적으로 해석한다. 규범 Asset의 count를 해당 배포의 실행 증거로 대체해서는 안 된다.

릴리스 후에는 원격 ZIP을 다시 내려받아 SHA-256과 내부 identity를 검증하고, 고정 Asset 목록이 Release에 존재하는지 확인한다. 문서에는 특정 배포 ZIP 이름, 버전 또는 SHA-256을 고정값으로 기록하지 않는다. 해당 값은 각 릴리스의 release note 또는 검증 산출물에서 관리한다.

---

## 19. 대상 config의 원격 부트스트랩

이 절은 관측이 아니라 관측 대상 자체를 원격에서 켜는 방법을 다룬다. 어떤 기능을 켜는 코드 경로가 대상 PC에서 직접 실행하는 로컬 명령 하나뿐이면, 그 PC를 원격에서 그 상태로 만들 방법이 없다. 이는 §15가 지적한 "필수 로컬 확인 항목이 비활성"인 상황의 근본 원인이 될 수 있다.

### 19.1 문제

- 어떤 기능을 켜는 코드 경로가 로컬 setup 하나뿐이다.
- 원격 배포는 관측 대상 패키지의 내용만 바꿀 수 있고, 다른 패키지(엔진)의 config는 건드릴 수 없다는 것이 §8의 원래 전제였다.
- 결과적으로 그 기능이 꺼진 PC는 원격에서 켤 방법이 없고, PC를 직접 방문해야만 해결된다.

### 19.2 해법: 부트스트랩은 대상 패키지의 설치 부산물을 이용한다

관측 대상 패키지의 installer는 자신이 설치되는 그 PC에서 실행되므로, 같은 PC에 있는 엔진의 config 파일에 대해 로컬 프로세스와 동일한 읽기/쓰기 권한을 이미 갖는다. §8이 말한 "패키지 밖은 계측 불가"는 관측(읽기)에 대한 제약이며, 설치가 진행되는 그 PC에서 로컬 파일을 쓰는 것 자체를 막지 않는다. 이 부산물을 이용해, installer가 자기 자신의 설치를 마친 뒤 엔진의 config에서 해당 기능이 꺼져 있으면 켠다.

이 패턴은 특정 기능에 한정되지 않는다. "대상 config를 원격에서 켤 코드 경로가 없고, 이 패키지의 installer가 그 config에 로컬 접근권을 이미 갖는다"는 조건이 성립하면 같은 방식을 다른 부트스트랩 문제에도 적용할 수 있다.

### 19.3 안전 규칙

부트스트랩은 다음을 모두 만족해야 한다.

1. **자기 설치 이후에만 실행한다.** 대상 패키지 자신의 `install-confirmed` 뒤에만 시작하며, 그 성공에 전제조건을 걸지 않는다.
2. **완전히 격리된다.** 부트스트랩의 실패는 대상 패키지 자신의 설치 성공/실패에 어떤 영향도 주지 않는다. `fail-install`을 트리거하지 않는다.
3. **정확히 그 키만 쓴다.** 대상 config의 다른 키는 절대 읽지도 손대지도 않는다. 병합이 아니라 하나의 하위 키 전체를 교체하는 방식으로 한정한다.
4. **idempotent하다.** 이미 켜져 있으면 아무 것도 쓰지 않는다. 재실행이 파일을 바이트 단위로 그대로 두어야 한다.
5. **엔진 자신의 검증 규칙을 그대로 복제해 쓰기 전/후에 적용한다.** 쓰려는 값이 엔진이 스스로 검사하는 규칙을 통과하지 못하면 쓰지 않는다.
6. **원자적으로 쓰고, 쓰기 전 타임스탬프 백업을 남긴다.** 쓴 뒤 다시 읽어 검증을 통과하는지 확인하고, 실패하면 백업으로 되돌린다.
7. **함수 자신이 스스로 예외를 흡수한다(10.1).** 호출부의 try/except에 기대지 않는다.
8. **전제조건이 성립하지 않으면 조용히 skip한다.** config 파일이 없거나, 대상 패키지 자신이 엔진의 활성 target 목록에 없는 등 비정상 상태에서는 아무것도 쓰지 않고 skip 결과를 낸다.

### 19.4 관측 신호

부트스트랩 결과도 다른 단계와 같은 규칙(버전 비종속, `<skill>-<stage>.signal`)을 따르는 별도 신호 3종으로 보고한다.

```text
<skill>-<config-key>-enabled.signal
<skill>-<config-key>-already-enabled.signal
<skill>-<config-key>-skipped.signal
```

이 신호는 대상 패키지 자신의 `install-confirmed`/`fail-install`과 분리되어 있으므로, §13.5의 판정표에 다음 행을 추가한다.

| 관측 delta | 1차 판정 |
|---|---|
| `install-confirmed +1`, 부트스트랩 신호 3종 모두 0 | 부트스트랩 단계 진입 전 조용한 중단 (19.3-7 위반 의심) |
| `*-skipped +1` | 전제조건 미충족으로 정상 skip. 실패 아님 |
| `*-already-enabled +1` | 이미 켜져 있었음. 정상 |
| `*-enabled +1` | 이번 실행에서 최초로 켜짐 |

### 19.5 발견된 실패 사례

이 부트스트랩을 실제 PC에서 처음 실행했을 때, 부트스트랩 함수 자체는 config를 정확히 켰지만 그 결과를 보고하는 신호 이름이 요청 목록에 등록되지 않아 처리되지 않은 예외로 프로세스가 비정상 종료했다. 핵심 설치는 이미 성공했음에도, 엔진이 이 exit code를 installer 실패로 해석해 대상 패키지 전체를 실패 처리하거나 rollback을 시도할 수 있는 상황이었다.

원인은 19.3-7("함수 자신이 스스로 예외를 흡수한다")이 함수 docstring에만 선언되고 실제로는 호출부의 try/except에만 의존했던 데 있었다. 함수 내부가 아니라 호출부에서만 감싸면, 그 함수가 다른 경로로 재사용되거나 내부 로직이 늘어날 때 이 보장이 조용히 깨질 수 있다. 이 사례 이후 19.3-7을 함수 정의 자체에 강제하는 것으로 확정했고, 이를 검증하는 자동 테스트를 §18-14로 추가했다.

---

## 20. 운영 요약

```text
배포 전 게이트 통과 (§17)
→ 검증 활동 전파 완료 대기
→ 관측 전 Asset count baseline
→ Scheduler Fresh Cycle
→ 종료 예상 시각 + 전파 지연 여유 대기
→ 카운터 유효성 확인
→ 생존 신호 delta 확인 (§16-18: `0`이면 여기서 고장 확정, 이하 해석 불가)
→ 카나리아 delta로 엔진 생존 판정
→ installer 단계 delta 확인
→ 부트스트랩 단계 delta 확인 (§19, 해당 시)
→ runner/queue/job/final 단계 delta 확인
→ 일반 pass/fail delta로 호환 판정
→ 이상 또는 실패 시 correlation ID로 로컬 JSONL/summary 연결
→ 로컬 durable evidence로 최종 원인 확정
```

이 계약은 이후 Job-list가 업데이트되어도 동일하게 유지한다. 구현 변경으로 단계 의미를 바꿔야 한다면 Asset 이름을 재사용한 채 의미를 몰래 바꾸지 말고, 계약 개정과 호환성 검토를 먼저 수행한다.
