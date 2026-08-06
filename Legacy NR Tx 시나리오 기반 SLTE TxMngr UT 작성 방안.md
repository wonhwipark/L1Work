# Legacy NR Tx 시나리오 기반 SLTE TxMngr UT 작성 방안

## 1. 추진 배경

SLTE 기반 NR Tx 기능을 새로 구현할 때는 Legacy 1900 코드의 동작을 참고해야 한다.

하지만 Legacy 코드를 그대로 SLTE로 복사하는 방식은 적절하지 않다. Legacy와 SLTE는 다음 항목이 다를 수 있기 때문이다.

- 모듈 구조
- 클래스와 API 이름
- 메시지 전달 방식
- 상태 정보 저장 위치
- HAL 연동 방식
- UT Framework와 Mock 구성 방식

따라서 Legacy에서는 **기능이 어떤 순서와 조건으로 동작하는지**만 추출하고, 실제 구현과 UT는 **SLTE 구조에 맞게 다시 Mapping**하는 방식이 필요하다.

이번 검토 대상 Feature는 다음과 같다.

> DCI-based BWP ID switching에 의한 PCell UL Rank 변경

현재 MSC가 없을 가능성이 있으므로, Legacy SDM 로그와 Legacy 코드를 함께 사용하여 실제 동작 흐름을 확인한다.

---

## 2. 최종 목표

이번 작업의 목표는 Legacy 전체 동작을 재현하는 Full UT를 만드는 것이 아니다.

목표는 다음과 같다.

> Legacy 시나리오 흐름을 기준으로 Tx 관련 API 경계의 입력과 출력을 정의하고, 이를 SLTE TxMngr의 API 및 모듈에 Mapping하여 SLTE용 UT를 작성한다.

UT에서는 TxMngr 내부 구현 과정을 세부적으로 검증하지 않는다.

다음과 같이 모듈 경계에서 관찰할 수 있는 값만 검증한다.

```text
입력 메시지 또는 Event 주입
→ SLTE TxMngr 동작
→ 외부 API 호출 여부 확인
→ 전달된 Message 또는 CMD 주요 필드 비교
```

예를 들어 TxMngr 내부의 private helper 함수가 몇 번 호출됐는지는 검증하지 않는다.

대신 다음을 검증한다.

- SCC로 어떤 메시지가 전송됐는가
- UL Rank Update API에 어떤 값이 전달됐는가
- HAL로 어떤 CMD가 전송됐는가

---

## 3. 이번 작업에서 제외할 범위

이번 단계에서는 다음 작업을 하지 않는다.

- Legacy용 UT 작성
- Legacy 내부 구현 구조를 SLTE에 그대로 복제
- NR Tx 전체 기능에 대한 Full UT
- 모든 예외와 복구 절차 검증
- Transaction 전체 End-to-End 통합 시험
- Production 코드의 자동 구현
- Legacy와 SLTE의 함수 이름을 단순 1:1로 연결

Legacy는 **동작의 정답을 확인하는 자료**로만 사용한다.

실제 UT 대상과 구현 구조는 SLTE TxMngr를 기준으로 한다.

---

## 4. 대상 시나리오

현재 예상하는 기본 흐름은 다음과 같다.

```text
BWP ID Switching Event 수신
        │
        ▼
       BCH
        │
        │ PATH_CONFIG_REQ
        ▼
       SCC
        │
        │ PATH_CONFIG_CNF
        ▼
 BCH Message Handler
        │
        │ PCell UL Rank Update
        ▼
   UL Rank 변경 확인
        │
        │ Rank가 실제로 변경된 경우
        ▼
    BCH → HAL CMD
```

이를 세 개의 UT 검증 구간으로 나눈다.

### 검증 구간 1

```text
BWP ID Switching Event
→ BCH
→ SCC PATH_CONFIG_REQ
```

### 검증 구간 2

```text
SCC PATH_CONFIG_CNF
→ BCH Message Handler
→ PCell UL Rank Update API
```

### 검증 구간 3

```text
PCell UL Rank 변경
→ BCH
→ HAL CMD 전송
```

세 구간을 하나의 긴 UT로 만들지 않고, 각각 독립된 UT로 만드는 것을 기본으로 한다.

이렇게 해야 UT가 실패했을 때 문제가 발생한 위치를 쉽게 구분할 수 있다.

---

## 5. 전체 진행 절차

## 단계 1. Legacy 시나리오 흐름 확인

먼저 Legacy SDM 로그에서 실제 메시지 순서를 확인한다.

예상 확인 항목은 다음과 같다.

```text
BWP ID Switching Event
→ PATH_CONFIG_REQ
→ PATH_CONFIG_CNF
→ UL Rank Update
→ HAL CMD
```

SDM 로그에서는 다음 정보를 찾는다.

- Event 발생 시점
- PCell 여부
- Target BWP ID
- BWP별 Rank 정보
- PATH_CONFIG_REQ 전송
- PATH_CONFIG_CNF 수신
- UL Rank 변경 전후 값
- HAL CMD 전송
- 성공 또는 실패 결과

SDM 로그에 필요한 정보가 부족하면, 로그 출력 문자열을 Legacy 코드에서 검색하여 관련 함수와 API를 찾는다.

### 이 단계의 결과

```text
legacy_scenario_flow.md
```

이 문서에는 다음 내용이 포함된다.

- 시나리오 시작 조건
- 메시지 및 API 호출 순서
- 각 단계의 입력 정보
- 각 단계의 출력 정보
- 다음 단계로 진행되는 조건
- SDM 또는 코드 근거

---

## 단계 2. Legacy API 경계의 검증 포인트 정의

Legacy 함수 이름을 그대로 UT 기준으로 사용하지 않는다.

각 단계에서 외부에서 관찰할 수 있는 입력과 출력으로 검증 포인트를 정의한다.

### VP-01: PATH_CONFIG_REQ 전송

#### Trigger

BCH가 Target BWP ID를 포함한 BWP ID switching event를 수신한다.

#### 입력

- PCell ID
- 현재 BWP ID
- Target BWP ID
- Target BWP에 매핑된 UL Rank
- 현재 UL Rank

#### 기대 출력

SCC로 `PATH_CONFIG_REQ`가 전송된다.

검증 대상 필드는 다음과 같다.

- Message ID
- PCell 또는 Cell ID
- Target BWP ID
- Target BWP에 해당하는 UL Rank

#### 검증하지 않는 항목

- Timestamp
- Reserved field
- Padding
- Runtime에서 자동 생성되는 값
- Feature와 관계없는 공통 메시지 필드

---

### VP-02: PATH_CONFIG_CNF 이후 UL Rank Update

#### Trigger

BCH가 SCC로부터 성공한 `PATH_CONFIG_CNF`를 수신한다.

#### 입력

- Result
- PCell ID
- Target BWP ID
- Confirmed UL Rank

#### 기대 출력

PCell UL Rank Update 기능이 호출된다.

검증 대상은 다음과 같다.

- UL Rank Update API 호출 여부
- PCell ID
- BWP ID
- 적용할 UL Rank
- 필요할 경우 Result 또는 Status

실패한 `PATH_CONFIG_CNF`에서 Update API가 호출되지 않는지는 Legacy 동작을 확인한 뒤 Negative UT로 추가한다.

---

### VP-03: UL Rank 변경 후 HAL CMD 전송

#### Trigger

PCell UL Rank가 기존 값과 다른 값으로 갱신된다.

#### 입력

- Previous UL Rank
- Updated UL Rank
- Target BWP ID
- PCell ID

#### 기대 출력

BCH 또는 TxMngr가 HAL로 Rank 변경 관련 CMD를 전송한다.

검증 대상 필드는 다음과 같다.

- HAL CMD ID
- PCell 또는 Cell ID
- Target BWP ID
- Updated UL Rank

Rank가 동일할 때 HAL CMD를 전송하지 않는지는 Legacy 코드에서 동작을 확인한 뒤 Negative UT로 추가한다.

---

## 단계 3. Legacy 검증 포인트를 SLTE TxMngr에 Mapping

검증 포인트를 정의한 뒤 SLTE 코드에서 해당 책임을 담당하는 모듈과 API를 찾는다.

여기서 중요한 것은 Legacy 함수와 SLTE 함수를 이름으로 연결하는 것이 아니다.

다음과 같이 **책임을 기준으로 Mapping**한다.

```text
Legacy 책임:
Target BWP의 Rank를 포함한 PATH_CONFIG_REQ 전송

SLTE 책임:
동일한 입력을 받아 SCC 연동 메시지를 생성하고 전송하는 TxMngr API
```

### Mapping 표 예시

| 검증 ID | 시나리오 책임 | Legacy 근거 | SLTE 대상 | UT 입력 방식 | UT 출력 검증 |
|---|---|---|---|---|---|
| VP-01 | BWP switching 후 PATH_CONFIG_REQ 전송 | BCH event handler | TxMngr BWP switching entry | Event 또는 API 호출 | SCC Mock 메시지 비교 |
| VP-02 | PATH_CONFIG_CNF 이후 Rank 갱신 | BCH CNF handler | TxMngr CNF handler | CNF 메시지 주입 | Rank Update API 호출 인자 |
| VP-03 | Rank 변경 후 HAL CMD 전송 | BCH HAL send 경로 | TxMngr 또는 HAL Adapter | Rank 변경 입력 | HAL Mock CMD 비교 |

각 항목은 다음 상태 중 하나로 분류한다.

| 상태 | 의미 |
|---|---|
| `MAPPED` | SLTE에 대응 API 또는 모듈이 존재 |
| `PARTIAL` | 일부 기능만 존재하고 추가 구현 필요 |
| `MISSING` | 대응 기능이 없어 새 구현 필요 |
| `NOT_APPLICABLE` | SLTE 구조상 별도 Mapping이 필요하지 않음 |
| `NEED_REVIEW` | 담당자와 설계 협의가 필요 |

`MISSING` 또는 `PARTIAL` 항목이 실제 파트원의 구현 대상이 된다.

---

## 단계 4. 현재 SLTE UT 구조 확인

UT 코드를 작성하기 전에 기존 SLTE NR Tx UT 폴더를 분석한다.

전체 UT Framework를 모두 학습할 필요는 없다.

이번 Feature 작성에 필요한 부분만 확인한다.

### 확인 대상

- TxMngr 객체를 생성하는 Fixture
- SetUp 및 TearDown 방식
- BCH Event 또는 메시지를 주입하는 방법
- SCC 송신 API를 Mock하거나 캡처하는 방법
- `PATH_CONFIG_CNF`를 TxMngr에 주입하는 방법
- UL Rank Update API를 Mock하는 방법
- HAL CMD 송신 API를 Mock하는 방법
- `jomock` 사용 방식
- Message 구조체 비교 helper
- 기존 유사 Test Case
- UT Build 및 실행 방법

### Jomock 사용 원칙

Jomock은 TxMngr 외부 Dependency를 제어하고 검증하는 용도로 사용한다.

사용 대상 예시는 다음과 같다.

- SCC Message Sender
- HAL Command Sender
- Rank Configuration Provider
- Tx Context 또는 Rank Update Interface
- 외부 DB 조회 결과

다음과 같은 내부 helper는 가급적 Mock하지 않는다.

```text
buildPathConfigReq()
getMappedRank()
updateInternalState()
```

내부 helper 호출 횟수보다 최종 출력 메시지와 외부 API 인자를 검증한다.

---

## 단계 5. SLTE UT Specification 작성

Mapping 결과와 UT Framework 분석 결과를 결합하여 실제 UT 작성 기준을 만든다.

### UT-01

```cpp
TEST_F(TxMngrBwpSwitchTest,
       SendsPathConfigReqWithRankMappedFromTargetBwp);
```

#### 입력

- Current BWP ID
- Target BWP ID
- Current UL Rank
- Target BWP의 UL Rank
- BWP Switching Event

#### 검증

SCC Mock에 전달된 `PATH_CONFIG_REQ`의 주요 필드를 비교한다.

---

### UT-02

```cpp
TEST_F(TxMngrPathConfigCnfTest,
       UpdatesPCellUlRankAfterSuccessfulConfirmation);
```

#### 입력

- `PATH_CONFIG_CNF`
- Result = SUCCESS
- Target BWP ID
- Confirmed UL Rank

#### 검증

PCell UL Rank Update API가 올바른 인자로 호출됐는지 확인한다.

---

### UT-03

```cpp
TEST_F(TxMngrUlRankTest,
       SendsHalCommandWhenUlRankChanges);
```

#### 입력

- Previous UL Rank
- Updated UL Rank
- Target BWP ID
- PCell ID

#### 검증

HAL Mock으로 전달된 CMD의 Feature 관련 필드를 비교한다.

---

## 단계 6. Negative UT 결정

Negative UT는 추정으로 작성하지 않는다.

Legacy SDM 또는 코드를 통해 동작이 확인된 경우에만 추가한다.

검토 가능한 후보는 다음과 같다.

```cpp
TEST_F(TxMngrPathConfigCnfTest,
       DoesNotUpdateRankWhenPathConfigFails);

TEST_F(TxMngrUlRankTest,
       DoesNotSendHalCommandWhenUlRankIsUnchanged);

TEST_F(TxMngrBwpSwitchTest,
       DoesNotSendPathConfigReqForInvalidBwpId);
```

Negative UT를 작성하기 전 파트원과 다음 사항을 합의해야 한다.

- 실패 CNF 처리 정책
- Rank 동일 시 HAL CMD 전송 여부
- 유효하지 않은 BWP ID 처리
- Rank 정보가 없을 때의 동작
- 기존 상태 유지 또는 오류 반환 정책

---

## 단계 7. UT를 파트원에게 전달

파트원에게 UT 소스만 전달하지 않는다.

다음 문서를 함께 제공한다.

```text
legacy_scenario_flow.md
ut_verification_points.md
slte_txmngr_mapping.md
slte_gap_report.md
slte_ut_spec.md
slte_ut_patch.diff 또는 Shelved CL
ut_execution_result.md
```

### 파트원 구현 기준

파트원은 Legacy 함수를 그대로 포팅하지 않는다.

다음 기준을 충족하도록 SLTE TxMngr를 구현한다.

- Scenario Contract 만족
- SLTE Architecture 준수
- 기존 TxMngr API 재사용 우선
- 모듈 간 책임 분리 유지
- 신규 UT PASS
- 기존 NR Tx UT Regression PASS
- Feature와 무관한 Legacy 구현 Detail은 반영하지 않음

---

## 6. 스킬별 역할

## 6.1 `sdm-parser`

### 역할

Legacy SDM 원본 로그를 분석 가능한 구조로 변환한다.

### 학습 또는 추출 대상

- CP Time
- UE 또는 Stack
- PCell/SCell
- Message ID
- BWP ID
- UL Rank
- PATH_CONFIG_REQ
- PATH_CONFIG_CNF
- HAL CMD
- 성공 또는 실패 결과

### 산출물

```text
transaction_index.json
runtime_event.json
parsed_sdm.txt 또는 json
```

SDM Parser는 기능의 의미를 최종 판단하지 않는다.

로그를 시간과 Transaction 기준으로 정리하는 역할을 한다.

---

## 6.2 `code-analyzer`

### 역할 1: Legacy 코드 분석

SDM에 표시된 로그 문자열과 Message/API를 Legacy 1900 코드에서 찾는다.

### Legacy 학습 대상

- BWP switching Event handler
- `PATH_CONFIG_REQ` 생성 및 전송 API
- BWP ID별 UL Rank 조회 위치
- `PATH_CONFIG_CNF` handler
- PCell UL Rank Update API
- Rank 변경 판단 조건
- HAL CMD 생성 및 전송 API
- 각 API의 입력과 출력
- 관련 코드 파일과 함수
- 호출 조건과 분기

### 역할 2: SLTE 코드 분석

Legacy에서 정의한 검증 포인트가 SLTE TxMngr의 어디에 대응하는지 찾는다.

### SLTE 학습 대상

- TxMngr의 BWP switching 진입점
- SCC 연동 API
- CNF Message handler
- Rank Update API 또는 상태 저장 위치
- HAL Adapter
- Message 및 CMD 구조체
- 기존 유사 Feature

### 역할 3: SLTE UT 폴더 분석

현재 UT 작성 방식을 파악한다.

### UT 폴더 학습 대상

- Fixture
- Mock
- Jomock 설정
- 메시지 주입 방식
- 메시지 비교 helper
- 기존 유사 Test
- Build 설정

---

## 6.3 `slte-knowledge-manager`

### 역할

각 분석 결과를 Feature 단위로 연결하고 재사용 가능한 지식으로 관리한다.

### 저장해야 할 지식

#### Legacy Scenario Knowledge

```text
FEATURE_SCENARIO
API_CONTRACT
MESSAGE_FLOW
RUNTIME_EVIDENCE
STATE_TRANSITION
```

#### SLTE Mapping Knowledge

```text
SLTE_MODULE_MAPPING
SLTE_API_MAPPING
FIELD_MAPPING
IMPLEMENTATION_GAP
```

#### UT Knowledge

```text
UT_VERIFICATION_POINT
UT_FIXTURE
MESSAGE_INJECTION_PATTERN
JOMOCK_PATTERN
MESSAGE_COMPARATOR
UT_BUILD_CONTRACT
```

### 지식매니저가 하지 않아야 할 일

- SDM만 보고 Feature 동작을 단정
- Legacy 함수와 SLTE 함수를 이름만으로 자동 연결
- 승인 없이 기존 지식 덮어쓰기
- Production 코드를 직접 수정
- Legacy 구현 Detail을 SLTE 설계 기준으로 확정

지식매니저는 분석 결과를 연결하고, 확정되지 않은 항목은 후보나 Gap으로 관리해야 한다.

---

## 6.4 `code-fix`

### 역할

승인된 UT Specification과 SLTE Mapping 결과를 기준으로 실제 UT 코드를 생성하거나 수정한다.

### 입력

- UT 검증 포인트
- SLTE TxMngr Mapping
- 현재 UT Fixture와 Mock Pattern
- 허용된 UT 폴더
- Jomock 작성 방식

### 출력

- UT 소스
- 필요한 Mock 설정
- Message 비교 코드
- Build 수정
- Patch 또는 Shelved CL
- Compile 및 Test 결과

### 제한

기본 실행에서는 Production 코드 수정이 금지되어야 한다.

```text
Allowed:
<SLTE NR Tx UT folder>/**

Denied:
<SLTE NR Tx production source>/**
```

파트원이 Production 코드를 구현하고, UT를 통과시키는 구조로 진행한다.

---

## 6.5 `issue-analyzer`

### 역할

필수 스킬은 아니지만, SDM 로그가 복잡하거나 실패 로그가 포함된 경우 보조적으로 사용한다.

### 사용 시점

- 정상 구간과 실패 구간을 분리해야 할 때
- 실제 문제 구간의 로그를 추출해야 할 때
- 여러 UE 또는 Retry가 한 로그에 포함됐을 때
- SDM에서 Feature 관련 핵심 로그만 뽑아야 할 때

정상 성공 로그가 명확하다면 첫 단계에서는 생략할 수 있다.

---

## 6.6 `skillsilent`

### 역할

각 스킬을 사내 환경에서 질문 없이 실행할 수 있도록 지원한다.

### 필요 기능

- Legacy 코드 읽기
- SLTE 코드와 UT 폴더 읽기
- SDM 로그 읽기
- 분석 산출물 작성
- UT 폴더 수정 시 승인 정책 적용
- 저사양 모델에서 Resume 지원

---

## 6.7 선택적으로 연동할 스킬

### `doc-converter`

분석 결과와 Mapping 문서를 HTML 또는 Confluence 형식으로 변환할 때 사용한다.

### PlantUML 관련 스킬

다음 흐름을 MSC 또는 Sequence Diagram으로 표현할 때 사용한다.

```text
BWP Switching Event
→ PATH_CONFIG_REQ
→ PATH_CONFIG_CNF
→ UL Rank Update
→ HAL CMD
```

문서 공유 목적이며 UT 생성 자체에는 필수가 아니다.

---

## 7. 권장 스킬 연동 순서

```text
Legacy SDM
   │
   ▼
sdm-parser
   │
   ▼
code-analyzer
- Legacy 로그와 코드 연결
- Scenario 및 API Contract 추출
   │
   ▼
slte-knowledge-manager
- Legacy Scenario 지식 관리
- UT 검증 포인트 생성
   │
   ▼
code-analyzer
- SLTE TxMngr 코드 분석
- 현재 SLTE UT 폴더 분석
   │
   ▼
slte-knowledge-manager
- Legacy 검증 포인트와 SLTE Mapping 관리
- Missing/Partial Gap 기록
   │
   ▼
code-fix
- SLTE UT 생성
- Jomock 구성
- UT 폴더에만 Patch 생성
   │
   ▼
파트원
- SLTE TxMngr Feature 구현
   │
   ▼
UT 실행
- 신규 UT PASS
- 기존 NR Tx UT Regression PASS
   │
   ▼
slte-knowledge-manager
- 최종 구현 결과와 As-built Mapping 업데이트
```

---

## 8. 파트원과 사전에 협의할 항목

작업 시작 전 다음 항목을 합의하는 것이 좋다.

### 기능 범위

- 대상은 PCell만인지
- UL Rank만 변경하는지
- BWP ID switching의 어떤 Event가 Trigger인지
- PATH_CONFIG_REQ에 반드시 포함돼야 할 필드
- PATH_CONFIG_CNF의 성공 조건
- HAL CMD 전송 조건

### UT 범위

- API 경계별 3개 UT로 분리할지
- Negative UT를 어디까지 포함할지
- End-to-End UT를 추가할지
- Message 전체 비교인지 관련 필드만 비교인지
- Mock 대상 모듈의 범위

### SLTE 설계

- TxMngr가 BCH 역할을 직접 담당하는지
- SCC Adapter가 별도인지
- Rank 상태 저장 위치
- HAL CMD Builder와 Sender가 분리돼 있는지
- 기존 API를 확장할지 신규 API를 만들지

### 업무 분담

- Legacy SDM과 코드 분석 담당
- SLTE TxMngr Mapping 검토 담당
- UT Fixture 및 Jomock 검토 담당
- TxMngr Production 구현 담당
- UT Review 담당

---

## 9. 성공 기준

이번 작업은 다음 조건을 만족하면 완료로 판단한다.

### 분석

- Legacy 시나리오 순서가 SDM과 코드 근거로 확인됨
- 3개 UT 검증 포인트가 정의됨
- 검증 포인트별 입력과 출력이 명확함

### Mapping

- 각 검증 포인트의 SLTE TxMngr 대응 위치가 확인됨
- `MAPPED`, `PARTIAL`, `MISSING` 상태가 구분됨
- 파트원 구현 대상이 명확함

### UT

- UT 입력을 Fixture에서 재현할 수 있음
- SCC, Rank Update, HAL 경계가 Jomock으로 검증됨
- 내부 private helper에 과도하게 결합하지 않음
- Feature 관련 필드만 비교함
- 구현 전에는 예상대로 실패하거나 Compile Gap이 명확히 표시됨

### 구현 완료

- 신규 UT PASS
- 기존 NR Tx UT Regression PASS
- 최종 SLTE Mapping이 지식매니저에 업데이트됨

---

# 10. 스킬 업데이트 필요사항

아래는 파트원과 작업 방향을 먼저 합의한 후 별도로 진행할 스킬 변경 사항이다.

## 10.1 `code-analyzer` 업데이트

### 필요한 기능

#### Legacy Scenario Contract 분석

```text
scenario-contract-analyze
```

입력:

- Legacy 코드 폴더
- Feature ID
- SDM 분석 결과
- 관련 Message/API Keyword

출력:

- 시나리오 흐름
- API Input/Output
- 코드 근거
- 검증 포인트 후보

#### Log-Code Correlation

```text
log-code-correlate
```

기능:

- SDM 로그 문자열을 코드에서 검색
- 파일, 함수, 라인 연결
- 관련 API와 State 추출
- 다수 후보는 Confidence와 함께 기록

#### UT Structure 분석

```text
ut-structure-analyze
```

기능:

- Fixture 추출
- Jomock Pattern 추출
- Message Injection 방식 추출
- Output Comparator 추출
- Build Target 추출
- 유사 Test Case 추천

---

## 10.2 `slte-knowledge-manager` 업데이트

### 필요한 기능

#### Runtime Log 학습

```text
learn-runtime-log
```

SDM 분석 결과와 Legacy 코드 분석 결과를 연결하여 다음 후보 지식을 만든다.

- Runtime Evidence
- Scenario Flow
- API Contract
- Failure Mode
- Conflict

SDM만으로 자동 승인하지 않는다.

#### UT 검증 포인트 생성

```text
prepare-ut-verification
```

기능:

- Scenario 단계별 검증 포인트 생성
- Trigger/Input/Expected Output 분리
- Feature 관련 필드 지정
- Negative UT 후보 분리

#### SLTE Mapping 관리

```text
map-ut-verification-to-slte
```

기능:

- 검증 포인트와 SLTE 모듈/API 연결
- `MAPPED`, `PARTIAL`, `MISSING` 분류
- Field Mapping 관리
- 구현 Gap 생성

#### UT 폴더 학습

```text
learn-ut-structure
```

기능:

- Fixture
- Jomock Pattern
- Message Injection
- Comparator
- Build Contract

이 정보를 Feature 동작 지식과 분리하여 저장한다.

---

## 10.3 `code-fix` 업데이트

### 필요한 기능

```text
create-contract-ut
```

기능:

- 승인된 UT 검증 포인트 입력
- SLTE Mapping 입력
- 기존 Fixture와 Jomock Pattern 재사용
- API 경계 입력·출력 비교 UT 생성
- UT 폴더만 수정
- Production 코드 수정 금지
- Patch 또는 Shelved CL 생성
- Compile/Test 결과 기록

Full UT 생성 기능보다 **Contract UT 생성 기능**으로 범위를 제한하는 것이 적절하다.

---

## 10.4 `sdm-parser` 업데이트 검토

현재 Parser가 다음 정보를 구조화하지 못한다면 보완이 필요하다.

- UE/Stack/Cell 구분
- CP Time과 Transaction Time
- Message ID
- BWP ID
- UL Rank
- PATH_CONFIG_REQ/CNF 연결
- HAL CMD
- 성공과 실패 Terminal 구분

기존 기능으로 충분하다면 수정하지 않는다.

---

## 10.5 `issue-analyzer` 업데이트 검토

필수 변경은 아니다.

다만 SDM에서 Feature 관련 정상 구간을 자동 추출해야 한다면 다음 기능을 검토할 수 있다.

```text
extract-feature-runtime-evidence
```

정상 로그와 실패 로그를 분리하고, 관련 구간만 지식매니저에 전달하는 용도다.

---

## 10.6 `skillsilent` 연동 정보 업데이트

`skillsilent` Core 자체의 변경보다, 수정되는 각 스킬의 다음 정보 업데이트가 필요하다.

```text
skillsilent/policy.json
skillsilent/contract.json
skillsilent/manifest.json
```

신규 Action이 Silent 및 Resume 환경에서 실행될 수 있도록 등록한다.

---

## 10.7 이번 기능과 관계없는 스킬

다음 스킬은 이번 작업을 위해 직접 수정할 필요가 없다.

- `skill-updater`
- `autotask-builder`
- `job-list`

다만 향후 야간 무인 분석이나 반복 Regression을 자동 실행할 때 별도 연동할 수 있다.

---

# 11. 최종 제안

이번 작업은 다음 원칙으로 진행한다.

> Legacy SDM과 코드는 시나리오 및 기대 동작의 근거로 사용한다.  
> Legacy 시나리오에서 API 경계별 UT 검증 포인트를 정의한다.  
> 검증 포인트를 SLTE TxMngr의 책임과 API에 Mapping한다.  
> 현재 SLTE UT Fixture와 Jomock Pattern을 사용해 입력을 주입하고 외부 출력을 비교하는 Contract UT를 작성한다.  
> 파트원은 UT와 Mapping 문서를 기준으로 SLTE TxMngr를 구현하고, 신규 UT와 기존 Regression을 통과시킨다.

Legacy UT는 작성하지 않는다.

Legacy 구현 구조를 SLTE에 복제하지 않는다.

최종 기준은 Legacy 함수가 아니라 다음 세 가지다.

```text
Legacy Scenario Contract
+ SLTE TxMngr Architecture
+ SLTE UT Framework
```