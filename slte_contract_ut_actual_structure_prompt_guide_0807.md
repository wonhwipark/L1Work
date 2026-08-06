# SLTE TxMngr Contract UT — 실제 UT 구조 학습·업데이트 가이드 프롬프트

## 1. 문서 목적

이 문서는 Legacy NR Tx 시나리오를 기준으로 SLTE TxMngr Contract UT를 만들 때, 실제 SLTE UT 폴더의 코드 형식을 먼저 학습하고 재사용하기 위한 가이드다.

문서나 예시에서 보이는 아래 형식은 실제 UT 코드의 기본값이 아니다.

```cpp
TEST_F(TxMngrBwpSwitchTest,
       SendsPathConfigReqWithRankMappedFromTargetBwp);
```

실제 SLTE UT가 다른 Test 선언 macro, Fixture, Jomock, input 주입 방식, output 비교 문법을 사용한다면 반드시 실제 코드를 먼저 학습해야 한다.

핵심 원칙은 다음과 같다.

```text
Legacy Scenario Contract
+ 실제 SLTE TxMngr Architecture
+ 실제 SLTE UT Source Pattern
= SLTE Contract UT
```

---

# 2. 전체 권장 순서

```text
1. Legacy SDM/코드에서 시나리오와 검증 포인트 확인
2. 실제 SLTE UT 폴더 구조 학습
3. UT 구조 후보 검토 및 승인
4. Legacy 검증 포인트를 SLTE TxMngr에 Mapping
5. 승인 UT 구조를 사용해 Contract UT 생성 준비
6. 실제 UT 파일 작성
7. 생성된 UT가 학습된 형식을 따르는지 검증
8. 검증 PASS 후 Code Fix G1/G2 절차로 반영
```

관련 스킬은 다음과 같다.

| 단계 | 스킬 | 주요 Action |
|---|---|---|
| 실제 UT 코드 형식 분석 | `code-analyzer` | `ut-structure-analyze` |
| UT 구조 후보 저장 | `slte-knowledge-manager` | `learn-ut-structure` |
| UT 구조 승인 | `slte-knowledge-manager` | `approve-ut-structure` |
| 승인 UT 구조 조회 | `slte-knowledge-manager` | `query-ut-structure` |
| Contract UT 생성 Context 준비 | `code-fix` | `create-contract-ut` |
| 생성된 UT 문법 검증 | `code-fix` | `contract-ut-validate` |

---

# 3. 케이스별 가이드 프롬프트

## Case 1. 처음으로 SLTE TxMngr UT 폴더를 학습하는 경우

### 사용 상황

- 현재 UT가 어떤 Framework인지 정확히 모른다.
- `TEST_F`, 자체 macro, registration table 중 무엇을 쓰는지 모른다.
- Fixture와 Jomock 형식을 먼저 파악해야 한다.

### 복사 가능한 프롬프트

```text
현재 SLTE NR TxMngr UT 폴더를 분석해서 실제 UT 작성 형식을 학습해줘.

다음 항목을 실제 코드 근거로 추출해줘.
1. Test Case 선언 형식 또는 macro
2. Fixture와 base class
3. SetUp/TearDown 또는 초기화 방식
4. Jomock/Mock 생성과 반환값 설정 방식
5. 대상 함수 input 주입 방식
6. 외부 API 호출 여부 및 인자 검증 방식
7. output/message/CMD 필드 비교 방식
8. include와 build 등록 방식
9. 가장 유사한 대표 UT 파일과 코드 위치

문서 예시의 TEST_F 형식으로 가정하지 말고 실제 소스에서 관찰된 형식만 사용해줘.
대표 Test 선언 예제가 부족하면 UT를 생성하지 말고 generation_ready=false와 부족한 근거를 알려줘.

UT 폴더: <SLTE_NR_TX_UT_FOLDER>
Feature ID: NR_TX_DCI_BWP_SWITCH_PCELL_UL_RANK
```

### 예상 결과

```text
ut_structure_profile.json
ut_structure_report.md
review_questions.json
```

확인할 핵심 필드:

```text
generation_ready
allowed_declaration_tokens
forbidden_unobserved_default_tokens
fixture_patterns
mock_patterns
verification_patterns
representative_files
```

---

## Case 2. UT 폴더 안에 여러 Test Framework나 형식이 섞여 있는 경우

### 사용 상황

- 하나의 UT root에 서로 다른 module의 UT가 섞여 있다.
- 여러 선언 macro가 검출되어 어떤 형식이 TxMngr 기준인지 모호하다.
- 전체 폴더 학습 결과가 너무 넓다.

### 복사 가능한 프롬프트

```text
이 UT root에는 여러 Framework 또는 Test 선언 형식이 섞여 있어.
NR TxMngr와 BWP/Rank/SCC/HAL 연동에 가장 가까운 실제 UT 파일만 범위로 좁혀서 다시 학습해줘.

우선순위는 아래와 같아.
1. TxMngr 또는 BCH 역할을 담당하는 UT
2. PATH_CONFIG_REQ/CNF와 유사한 메시지 UT
3. SCC 송신 Mock이 있는 UT
4. UL Rank 또는 Tx context update UT
5. HAL CMD 송신 UT

서로 다른 선언 형식이 나오면 자동으로 하나를 선택하지 말고 파일별 사용 범위와 대표 예제를 분리해줘.

UT root: <SLTE_NR_TX_UT_ROOT>
우선 분석 파일/폴더:
- <TXMNGR_UT_FOLDER_OR_FILE>
- <SCC_MESSAGE_UT_FOLDER_OR_FILE>
- <HAL_UT_FOLDER_OR_FILE>
```

### 판단 기준

- TxMngr 대상 프로파일과 다른 module 프로파일을 분리한다.
- `allowed_declaration_tokens`에 불필요한 타 Framework token이 들어가지 않아야 한다.
- 여러 선언 방식이 남으면 승인 전 `NEED_REVIEW`로 유지한다.

---

## Case 3. `generation_ready=false` 또는 근거 부족으로 나온 경우

### 사용 상황

- Test 선언 예제가 한 개뿐이다.
- Verification/Jomock 문법이 발견되지 않는다.
- UT 파일이 wrapper나 include만 포함한다.

### 복사 가능한 프롬프트

```text
UT 구조 분석 결과가 generation_ready=false야.
현재 blocker와 review question을 기준으로 부족한 근거를 보완해줘.

다음 순서로 처리해줘.
1. blocker별로 필요한 실제 파일 유형을 알려줘.
2. 동일 module에서 Test Case가 2개 이상 있는 파일을 우선 찾아줘.
3. Jomock expectation 또는 return 설정이 있는 파일을 찾아줘.
4. output/message 필드 비교가 있는 파일을 찾아줘.
5. 찾은 파일만 포함해서 UT structure profile을 다시 생성해줘.

근거가 계속 부족하면 임의의 TEST_F 또는 Assertion 문법을 만들지 말고 생성 중단 상태를 유지해줘.

기존 profile: <UT_STRUCTURE_PROFILE_JSON>
UT root: <SLTE_NR_TX_UT_ROOT>
```

---

## Case 4. 분석 결과를 지식매니저 후보로 저장하는 경우

### 사용 상황

- Code Analyzer의 UT profile이 생성되었다.
- 아직 실제 생성 기준으로 승인하지는 않았다.

### 복사 가능한 프롬프트

```text
이 Code Analyzer UT structure profile을 지식매니저의 승인 대기 후보로 저장해줘.

Feature ID: NR_TX_DCI_BWP_SWITCH_PCELL_UL_RANK
Branch: 1900
Scenario: SLTE
Profile: <UT_STRUCTURE_PROFILE_JSON>

다음 정보가 후보에 유지되어야 해.
- 실제 Test 선언 원문 예제와 파일/라인
- Fixture/base class
- Jomock/Mock token
- Verification/Comparator token
- include와 대표 파일
- 허용된 선언 token
- 관찰되지 않아 금지할 TEST_F 등의 token

승인 전에는 code_generation_allowed=false로 유지해줘.
```

### 예상 상태

```text
status = CANDIDATE
approval_required = true
code_generation_allowed = false
```

---

## Case 5. UT 구조 후보를 검토하고 승인하는 경우

### 사용 상황

- 대표 파일과 선언 문법을 사람이 확인했다.
- 현재 TxMngr UT 작성 기준으로 사용해도 된다고 판단했다.

### 복사 가능한 프롬프트

```text
아래 UT structure 후보를 검토해서 승인 준비 내용을 보여줘.

후보: <UT_STRUCTURE_CANDIDATE_ID_OR_JSON>

특히 아래를 확인해줘.
1. 대표 파일이 실제 SLTE TxMngr UT가 맞는지
2. Test Case 선언 형식이 맞는지
3. Fixture와 base class가 맞는지
4. Jomock/Mock 문법이 맞는지
5. input 주입과 output 검증 문법이 맞는지
6. TEST_F가 실제 코드에 없다면 금지 상태인지

확인 결과가 문제없으면 이 후보를 승인된 UT 생성 기준으로 반영해줘.
승인자: <NAME>
```

승인 실행 의도가 명확한 경우:

```text
UT structure 후보 <CANDIDATE_ID>를 실제 TxMngr UT 생성 기준으로 승인해줘.
승인자는 <NAME>이야.
부분 학습 상태면 승인하지 말고 부족한 근거를 알려줘.
```

### 예상 상태

```text
status = APPROVED
authority = APPROVED_UT_STRUCTURE_KNOWLEDGE
code_generation_allowed = true
```

---

## Case 6. 기존 UT Framework 또는 작성 규칙이 변경된 경우

### 사용 상황

- UT macro나 Fixture가 변경됐다.
- Jomock version 또는 API가 변경됐다.
- 기존 승인 프로파일이 과거 형식이다.

### 복사 가능한 프롬프트

```text
SLTE TxMngr UT 작성 규칙이 변경된 것 같아.
기존 승인 UT profile을 그대로 사용하지 말고 현재 UT 폴더를 다시 분석해서 차이를 비교해줘.

비교 항목:
1. Test 선언 token 변경
2. Fixture/base class 변경
3. SetUp/TearDown 변경
4. Jomock expectation/return 문법 변경
5. input injection 방식 변경
6. output/message/CMD 비교 helper 변경
7. include/build 등록 변경

기존 profile: <APPROVED_UT_PROFILE_JSON>
현재 UT root: <SLTE_NR_TX_UT_ROOT>

차이가 있으면 새 candidate를 만들고 기존 승인 profile을 자동 덮어쓰지 마.
```

### 운영 원칙

- 기존 승인 프로파일을 자동 수정하지 않는다.
- 새 분석 결과는 별도 Candidate로 생성한다.
- 차이 검토 후 새 버전을 승인한다.

---

## Case 7. Legacy 시나리오에서 UT 검증 포인트를 정리하는 경우

### 사용 상황

- Legacy UT는 작성하지 않는다.
- SDM/Legacy 코드에서 API 경계의 입력과 출력만 추출한다.

### 복사 가능한 프롬프트

```text
Legacy 1900의 DCI based BWP ID switching 시나리오를 분석해서 SLTE Contract UT용 검증 포인트를 정리해줘.
Legacy UT 코드는 만들지 마.

현재 예상 흐름은 아래와 같아.
1. BWP ID switching event 수신
2. BCH -> SCC: PATH_CONFIG_REQ
   - Target BWP ID에 해당하는 UL Rank 포함
3. SCC -> BCH: PATH_CONFIG_CNF
4. BCH message handler에서 PCell UL Rank update API 호출
5. UL Rank가 실제로 변경되면 BCH -> HAL CMD 전송

각 검증 포인트를 아래 형식으로 작성해줘.
- Verification Point ID
- Trigger
- Precondition
- Input과 데이터 출처
- Expected external API/message/CMD
- 비교할 필드
- 비교하지 않을 공통 필드
- Negative case 후보
- SDM/코드 근거

Legacy 내부 private helper 호출 여부는 검증 포인트로 만들지 마.
```

---

## Case 8. Legacy 검증 포인트를 SLTE TxMngr에 Mapping하는 경우

### 사용 상황

- VP-01~VP-03이 정의됐다.
- SLTE TxMngr의 실제 API/module을 찾아 채워 넣어야 한다.

### 복사 가능한 프롬프트

```text
Legacy 시나리오 기반 UT 검증 포인트를 SLTE TxMngr 구조에 책임 기준으로 Mapping해줘.
Legacy 함수 이름을 SLTE 함수 이름에 단순 1:1 대응시키지 마.

입력:
- Verification Points: <UT_VERIFICATION_POINTS_FILE>
- SLTE TxMngr source root: <SLTE_TXMNGR_SOURCE_ROOT>
- SLTE UT root: <SLTE_NR_TX_UT_ROOT>

예를 들어 Legacy BCH 역할을 SLTE TxMngr가 직접 담당한다면 아래처럼 정리해줘.
- Legacy BCH event handler 책임 -> SLTE TxMngr BWP switch entry
- Legacy BCH PATH_CONFIG_CNF handler 책임 -> SLTE TxMngr CNF handler
- Legacy BCH HAL send 책임 -> SLTE TxMngr 또는 HAL Adapter

각 항목을 아래 상태로 구분해줘.
- MAPPED
- PARTIAL
- MISSING
- NOT_APPLICABLE
- NEED_REVIEW

Mapping마다 실제 파일/API/구조체 근거를 포함해줘.
```

---

## Case 9. 승인된 실제 UT 구조로 Contract UT 생성을 준비하는 경우

### 사용 상황

- UT Verification Point가 준비됐다.
- SLTE Mapping이 준비됐다.
- 승인된 UT structure profile이 있다.

### 복사 가능한 프롬프트

```text
승인된 실제 SLTE UT structure profile을 사용해서 NR Tx BWP switching Contract UT 생성 Context를 준비해줘.

입력:
- 승인 UT profile: <APPROVED_UT_STRUCTURE_PROFILE_JSON>
- UT 검증 포인트: <UT_VERIFICATION_POINTS_FILE>
- SLTE Mapping: <SLTE_TXMNGR_MAPPING_FILE>
- 대상 UT 폴더: <SLTE_NR_TX_UT_FOLDER>
- Feature ID: NR_TX_DCI_BWP_SWITCH_PCELL_UL_RANK

중요 규칙:
1. TEST_F 예시를 사용하지 마.
2. 승인 profile에서 관찰된 Test 선언 문법만 사용해.
3. 가장 가까운 실제 대표 UT 파일을 기준으로 작성해.
4. Fixture, Jomock, input injection, verification 문법을 profile과 동일하게 유지해.
5. UT 폴더 외 Production 코드는 수정하지 마.
6. 실제 UT 파일 생성 전 허용/금지 token과 대표 예제를 먼저 보여줘.
```

### 예상 결과

```text
contract_ut_context.json
contract_ut_generation_guide.md
```

확인할 항목:

```text
status = READY
allowed_declaration_tokens
forbidden_declaration_tokens
target_ut_dir
code_generation_allowed
```

---

## Case 10. 생성된 UT 코드가 실제 형식을 따르는지 검증하는 경우

### 사용 상황

- UT 후보 파일이 작성됐다.
- G2 반영 전에 문법과 범위를 검사해야 한다.

### 복사 가능한 프롬프트

```text
생성된 SLTE TxMngr Contract UT가 승인된 실제 UT structure profile을 따르는지 검증해줘.

Context: <CONTRACT_UT_CONTEXT_JSON>
후보 UT 파일:
- <CHANGED_UT_FILE_1>
- <CHANGED_UT_FILE_2>

검증 항목:
1. 허용된 Test 선언 token을 사용하는지
2. TEST_F 등 미관찰 Framework token이 들어갔는지
3. 승인된 Jomock/Mock 문법을 사용하는지
4. 승인된 Verification/Comparator 문법을 사용하는지
5. 대상 UT root 밖 파일을 수정했는지
6. Production 코드가 포함됐는지

하나라도 위반하면 patch_allowed=false로 차단하고 수정 방법을 알려줘.
```

### PASS 기준

```text
status = PASS
patch_allowed = true
```

---

## Case 11. 생성 결과가 잘못된 `TEST_F` 형태로 나온 경우

### 사용 상황

- 생성된 UT가 실제 코드와 다른 `TEST_F(...)` 형태다.
- 과거 문서 예시가 생성 기준으로 잘못 사용됐다.

### 복사 가능한 프롬프트

```text
생성된 UT가 실제 SLTE UT와 다른 TEST_F 형식으로 작성됐어.
이 코드는 반영하지 말고 patch_allowed=false로 처리해줘.

다음 순서로 복구해줘.
1. 현재 승인 UT structure profile의 allowed declaration token 확인
2. 가장 가까운 실제 TxMngr UT 대표 파일 확인
3. 잘못 사용된 TEST_F와 Assertion/Mock 문법 목록 출력
4. 실제 선언, Fixture, Jomock, Verification 형식으로 다시 작성할 계획 생성
5. 수정 후보를 contract-ut-validate로 다시 검사

잘못된 후보 파일: <WRONG_TEST_F_UT_FILE>
승인 profile: <APPROVED_UT_PROFILE_JSON>
```

---

## Case 12. 실제 UT 학습 결과가 특정 Feature에 맞지 않는 경우

### 사용 상황

- 일반 TxMngr UT는 학습됐지만 PATH_CONFIG나 HAL CMD 유형과 다르다.
- 대표 예제의 input/output 패턴이 Feature와 맞지 않는다.

### 복사 가능한 프롬프트

```text
현재 승인 UT profile은 일반 TxMngr UT 기준이지만 이번 BWP switching Contract UT와 input/output 형태가 달라.
프로파일 전체를 폐기하지 말고 Feature 인접 예제를 추가 학습해서 보완 후보를 만들어줘.

추가로 찾아야 할 예제:
1. Event 또는 message injection UT
2. SCC outbound message field 비교 UT
3. CNF handler 직접 호출 또는 message dispatch UT
4. 내부/외부 Rank update API call 검증 UT
5. HAL CMD field 비교 UT

기존 승인 profile: <APPROVED_UT_PROFILE_JSON>
추가 분석 root: <SLTE_NR_TX_UT_ROOT>

기존 profile 자동 덮어쓰기 없이 새 candidate로 생성해줘.
```

---

# 4. 간단한 통합 프롬프트

아래 프롬프트는 전체 과정을 한 번에 설명할 때 사용할 수 있다.

```text
Legacy 1900의 DCI based BWP ID switching에 의한 PCell UL Rank 변경 시나리오를 기준으로 SLTE TxMngr Contract UT를 준비해줘.

목표는 Full UT나 Legacy UT 작성이 아니야.
Legacy에서 API 경계별 input/output 검증 포인트를 정의하고, SLTE TxMngr 책임/API에 Mapping한 뒤, 실제 SLTE UT 폴더의 선언·Fixture·Jomock·검증 형식을 학습해서 동일한 형식의 UT를 만드는 거야.

진행 순서:
1. Legacy SDM과 코드에서 아래 흐름 확인
   - BWP switching event
   - PATH_CONFIG_REQ
   - PATH_CONFIG_CNF
   - PCell UL Rank update
   - Rank 변경 시 HAL CMD
2. VP-01~VP-03 input/output Contract 정리
3. 실제 SLTE TxMngr/UT 폴더 분석
4. 실제 Test 선언, Fixture, Jomock, Verification 문법 프로파일 생성
5. 프로파일 승인 전에는 UT 생성 금지
6. Legacy 검증 포인트를 SLTE TxMngr에 책임 기준 Mapping
7. 승인된 실제 UT 프로파일로 Contract UT 생성
8. TEST_F 등 미관찰 문법을 사용하면 차단
9. UT 폴더만 수정하고 Production 코드는 수정하지 않음
10. 생성 후보를 검증한 뒤 G1/G2 절차로 반영

입력 경로:
- Legacy SDM: <PATH>
- Legacy source: <PATH>
- SLTE TxMngr source: <PATH>
- SLTE TxMngr UT root: <PATH>
```

---

# 5. 결과 확인 체크리스트

## UT 구조 학습

- [ ] 실제 Test 선언 예제가 최소 2개 이상인가
- [ ] 대상 TxMngr UT 파일이 대표 예제로 포함됐는가
- [ ] Fixture/base class가 확인됐는가
- [ ] Jomock/Mock 문법이 확인됐는가
- [ ] input 주입 방식이 확인됐는가
- [ ] output/API/CMD 검증 문법이 확인됐는가
- [ ] 실제 코드에 없는 `TEST_F`가 금지 목록인가
- [ ] `generation_ready=true`인가

## 지식 승인

- [ ] Candidate 상태에서 자동 생성 권한이 꺼져 있었는가
- [ ] 사람이 실제 대표 코드를 검토했는가
- [ ] 승인 후 `code_generation_allowed=true`인가
- [ ] 기존 승인 프로파일을 자동 덮어쓰지 않았는가

## Contract UT 생성

- [ ] Legacy 내부 함수가 아니라 외부 API 경계를 검증하는가
- [ ] 실제 SLTE Test 선언 형식을 사용하는가
- [ ] 실제 Fixture와 Jomock 문법을 사용하는가
- [ ] Feature 관련 필드만 비교하는가
- [ ] 대상 UT root 밖 파일을 수정하지 않았는가
- [ ] `contract-ut-validate` 결과가 PASS인가
- [ ] 기존 NR Tx UT Regression을 수행했는가
