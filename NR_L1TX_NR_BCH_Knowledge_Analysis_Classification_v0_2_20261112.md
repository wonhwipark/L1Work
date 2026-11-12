# NR L1 Tx · NR BCH Controller — Knowledge 분석 분류표

- 문서 버전: `v0.2`
- 정리일: `2026-11-12 KST`
- 상태: **사용자 협의 기반 분류 초안 / 실제 코드 분석 전**
- 대상: **NR L1 Tx**, **NR BCH Controller**만 포함
- 범위 제외: LTE Channel Config Controller 등 다른 모듈의 분류
- 목적: 실제 코드 분석을 수행하기 전에 Knowledge 업데이트에 필요한 **대표 Procedure/Scenario(A)**와 **세부 기술 지식(B)**을 나눠 목록화. 실제 분석·MSC 생성·그룹 지식 업데이트 실행은 별도 단계에서 진행

## 1. 공통 분류 원칙

1. **A. Procedure / Scenario:** 통신 기능 및 3GPP 절차 흐름을 중심으로 대표 시나리오를 관리한다. Overview, 대표 흐름, 모듈별 참여 구간, AS-IS MSC의 출발점이다.
2. **B. Technical Knowledge:** 물리채널, 신호, 리소스, 인터페이스, 상태 관리 등 반복적으로 등장하는 세부 기술을 별도 관리한다. A의 여러 시나리오에서 B 항목을 참조할 수 있다.
3. **모듈 책임 경계:** 실제 해당 컨트롤러가 수행하는 코드는 상세 분석하고, 다른 컨트롤러가 담당하는 기능은 요청·응답·상태 전달 등 인터페이스 경계로 한정한다.
4. **검증 상태:** 아래 항목은 *분석 후보*이다. 실제 구현·동작·소유권이 확인된 코드 사실로 간주하지 않는다. 작업 시 `CODE_VERIFIED`, `INTERFACE_ONLY`, `NOT_APPLICABLE`, `REVIEW_NEEDED` 등을 붙여 확정한다.
5. **공통 산출물 후보:** Overview, 대표 시나리오별 코드 진입/종료 경계, Code Facts(파일·함수·라인·조건), AS-IS MSC, 예외/상태 정보, Knowledge 업데이트 후보. 코드/그룹 Knowledge 원본 수정은 이 문서의 범위 밖이다.

## 2. NR L1 Tx

### A. Procedure / Scenario (8개)

| ID | 대분류 | 대표 분석 시나리오 / 상세 후보 |
|---|---|---|
| TX-A1 | Initial Access / Attach | Initial RACH, 초기 UL Tx 설정, Msg3 송신 관련 L1 Tx 흐름, 초기 접속 완료 단계 |
| TX-A2 | RRC Reconfiguration | UL 송신 설정 변경, BWP 변경, Tx 경로 재구성 |
| TX-A3 | UL Carrier Aggregation (UL CA) | SCell Configuration, Activation, Deactivation, Release, UL CA Tx Path Switching |
| TX-A4 | EN-DC | NR SCG 추가·변경·해제, LTE/NR 동시 송신, Tx Path Switching, 우선순위 및 경합 |
| TX-A5 | Mobility | Handover, RACH 재수행, 셀 전환과 UL Tx 경로 변경 |
| TX-A6 | Connected Mode | 정상 UL 송신, UL 설정 변경, Tx Antenna Switching, 동작 중 상태 전환 |
| TX-A7 | DRX / CDRX 연동 | Sleep/Wakeup과 연관된 UL Tx 중지·재개, 컨트롤러 간 송신 제어 경계 |
| TX-A8 | Exception / Recovery | 설정 실패, 송신 관련 상태 불일치, 재설정·Release·복구 |

> 주의: Attach, RRC, DRX, 물리채널 등의 전체 프로토콜을 NR L1 Tx가 소유한다는 뜻이 아니다. **NR L1 Tx의 실제 수신 메시지에서 하위 HAL/PHY IPC 등 확인 가능한 종료 경계까지** 분석한다.

### B. Technical Knowledge (7개)

| ID | 대분류 | 세부 기술 후보 |
|---|---|---|
| TX-B1 | UL Physical Channel | PUSCH, PUCCH, PRACH: Configuration, 송신 제어, 재전송/관련 조건 |
| TX-B2 | Reference Signal | SRS: Configuration, Trigger, 송신 제어 |
| TX-B3 | Tx Resource | Tx Path, RF Resource, Tx Antenna Selection, RF Path/Tx Chain Allocation 및 Mapping |
| TX-B4 | Tx Switching | Tx Antenna Switching, Tx Path Switching, Tx Chain Switching, UL CA/EN-DC 전환, 자원 충돌·우선순위 조정 |
| TX-B5 | Tx Configuration | BWP, CC Mapping, 송신 관련 Power Control/설정 |
| TX-B6 | Interface | L1 제어 메시지, HAL, PHY IPC, 모듈 간 데이터/제어 경계 |
| TX-B7 | State Management | Configured, Activated, Deactivated, Released 등 송신 관련 상태·전환 |

**분류 해석:** 예를 들어 `TX-A3 UL CA Activation`은 절차의 전체 흐름·MSC를 담당하고, 사용된 Tx Resource·Switching·State 등은 해당 `TX-B*` 기술 상세 항목으로 연결한다. 중복 문서보다는 상호 참조를 우선한다.

## 3. NR BCH Controller

### 합의된 책임 경계

- **Search / Measure의 실제 기능:** Measure Controller 담당 → NR BCH의 상세 구현 분석에서 제외; 결과 수신 및 연동 경계만 포함.
- **CDRX / Idle DRX의 실제 기능:** DRX Controller 담당 → NR BCH의 상세 구현 분석에서 제외; BCH 제어와의 인터페이스만 포함.
- **PBCH/MIB Acquisition:** 독립 최상위 Procedure가 아니라 **Initial Attach / Cell Access** 내부 단계로 포함.
- **SIB Decoding 관련 처리:** 절차적 분석 후보에 포함하되, 실제 복호 수행 주체 및 BCH Controller의 제어 범위를 코드로 확인해야 한다. SIB1은 PBCH가 아닌 PDCCH/PDSCH 경로를 통해 수신된다.
- **RRC Reconfiguration:** RRC가 L1에 전달하는 설정과 BCH가 수행하는 재설정을 별도 대표 Procedure로 관리. *모든 SIB Decoding 직후 반드시 일어나는 고정 순서*라고 가정하지 않는다.

### A. Procedure / Scenario (9개)

| ID | 대분류 | 대표 분석 시나리오 / 상세 후보 | 범위 주의 |
|---|---|---|---|
| BCH-A1 | Initial Attach / Cell Access | 선행 동기 결과 연동 → PBCH/MIB 획득 관련 BCH 처리 → 초기 시스템 정보 단계 연동 | Search/Measure 자체는 제외; PBCH/MIB는 이 범주 내 세부 단계 |
| BCH-A2 | System Information Acquisition | SIB 수신/Decoding 관련 제어, 결과 처리, 시스템 정보 갱신 | SIB 실제 복호/소유 범위 확인 필요 |
| BCH-A3 | RRC Reconfiguration | RRC 설정 수신 후 BCH 관련 재구성 및 상태 전환, BWP Configuration/Reconfiguration | A2 다음에 항상 발생한다고 가정하지 않음 |
| BCH-A4 | Mobility / Handover | Target Cell 전환, BCH 설정 및 정보 재획득 | Search/Measure는 인터페이스까지만 |
| BCH-A5 | Cell Reselection / Recovery | 셀 변경·재획득 과정의 BCH 참여 구간 | 셀 선택 알고리즘은 Measure/상위 모듈 소유일 수 있음 |
| BCH-A6 | Paging Procedure | Paging 관련 BCH 제어 또는 연동 | **실제 BCH 소유 여부 미확인: 조건부 후보** |
| BCH-A7 | Release / Suspend / Resume | BCH 설정 해제·재개와 관련된 상태·자원 처리 | 실제 지원 여부 확인 필요 |
| BCH-A8 | Exception / Recovery | 복호 관련 실패 결과, Timeout, Retry, Reconfiguration, 복구 | 실제 실패 처리 소유권 확인 필요 |
| BCH-A9 | BWP Switching | RRC 설정 기반 BWP 변경, DCI 기반 전환, BWP Inactivity Timer 기반 전환의 BCH 참여 구간 | **독립 대표 시나리오 후보**. DCI/Timer 처리와 실제 BWP 전환의 소유 모듈을 코드로 확인; BCH가 직접 처리하지 않으면 인터페이스만 분석 |

### B. Technical Knowledge (7개)

| ID | 대분류 | 세부 기술 후보 |
|---|---|---|
| BCH-B1 | BCH Configuration | PBCH/BCH 관련 초기 설정·재설정 파라미터와 제어 조건, BWP Configuration/Reconfiguration 연동 |
| BCH-B2 | PBCH / MIB | PBCH 결과 및 MIB 정보 처리, 적용·전달 |
| BCH-B3 | BCH Resource | 수신 리소스 설정 및 관련 상태 |
| BCH-B4 | Interface | Measure Controller, DRX Controller, RRC, HAL/PHY 간 메시지·결과 전달 |
| BCH-B5 | State Management | BCH 설정·감시·재설정·해제의 상태 및 전환 조건, Active BWP 상태·전환 연동 |
| BCH-B6 | Timing / Scheduling | BCH 제어에 필요한 타이밍 및 스케줄링 **연동** (동기/DRX 알고리즘 자체 제외) |
| BCH-B7 | Recovery / Diagnostics | 실패 원인 기록, Timeout, Retry, 오류·상태 진단 |

> **NR BCH 핵심:** 통신 Procedure를 상위 분류로 사용하되, BCH Controller의 자체 동작과 Search/Measure·DRX·RRC 등 타 모듈 연동을 분리한다. `BCH-A6 Paging` 및 실제 SIB Decode 소유 여부는 별도 확인이 필요한 후보이다.

## 4. 추가 항목의 A/B 연결 및 소유권 확인

| 분석 주제 | Procedure/Scenario(A) | Technical Knowledge(B) | 분류 기준 |
|---|---|---|---|
| NR BCH BWP Switching | `BCH-A9` 독립 후보, `BCH-A3` RRC 설정 연동 | `BCH-B1` Configuration, `BCH-B5` State Management, `BCH-B4` Interface | RRC/DCI/Timer 기원별로 분기하되 BCH 직접 수행 범위 확인 |
| NR Tx Antenna Switching | `TX-A6` Connected Mode 등 발생 Procedure에 연결 | `TX-B3` Tx Resource, `TX-B4` Tx Switching | 안테나 선택·전환과 RF Path/Tx Chain 전환을 구별 |
| NR Tx Path Switching | `TX-A3` UL CA, `TX-A4` EN-DC, 필요 시 `TX-A2/A5` | `TX-B3` Tx Resource, `TX-B4` Tx Switching, `TX-B7` State Management | 발생 절차(A)와 경로 결정·충돌·제어(B)를 분리 |

**BWP 주의:** DCI 기반 전환 및 BWP Inactivity Timer에 따른 전환은 NR 시스템 수준의 후보이며, BCH Controller가 직접 수행한다고 가정하지 않는다. 실제 코드 분석에서 `CODE_VERIFIED` / `INTERFACE_ONLY` / `NOT_APPLICABLE`로 분류한다.

**Tx Switching 주의:** Antenna Switching, RF Path Switching, Tx Chain Switching은 하드웨어 자원 및 코드 소유권에 따라 중첩될 수 있지만 개념적으로 동일시하지 않는다. 절차별 MSC는 A에, 공통 결정 로직과 HAL/PHY 제어는 B에 둔다.

## 5. 후속 분석 시 적용할 항목별 기록 형식

| 필드 | 작성 기준 |
|---|---|
| ID / 대분류 | 위 `TX-A*`, `TX-B*`, `BCH-A*`, `BCH-B*` |
| Representative Scenario | Start Event → 핵심 단계 → End Boundary |
| Owner / Dependency | 해당 모듈 직접 책임 vs 타 모듈 인터페이스 |
| Code Evidence | Source revision, 파일/함수/라인, 조건·빌드 옵션 |
| Artifacts | Overview, Code Facts, AS-IS MSC, 상태·예외 설명 |
| Coverage | 미분석 / 분석 중 / 근거 확보 / 적용 제외 / 검토 필요 |
| Knowledge Update | 기존 지식과 차이점·중복 및 업데이트 **후보** |

## 6. 현 단계 판정 및 다음 단계

- **분류 정리:** NR L1 Tx `A 8개 + B 7개`; NR BCH `A 9개 + B 7개`.
- **실제 소스 분석 / MSC 생성 / 기술 검증:** `NOT_RUN`.
- **그룹 `l1sw-dev-knowledge` 정본 업데이트:** `NOT_RUN`.
- **다음 단계:** 두 모듈의 분류표를 검토한 뒤 항목별 우선순위 및 상세 시나리오 경계를 정의하고, 실행 환경에서 설치된 분석 스킬을 활용해 코드 근거를 수집한다.
