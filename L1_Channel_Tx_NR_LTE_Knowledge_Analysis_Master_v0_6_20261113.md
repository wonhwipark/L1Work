# NR/LTE L1 Channel · L1 Tx — Knowledge 분석 항목 마스터 (사내 GPT 1차 검토용)

- 문서 버전: **v0.6 / 2026-11-13 KST**
- 단계: **대표 Procedure/Scenario와 Technical Knowledge 분석 아이템 선별 (PLANNING ONLY)**
- 대상 4개 모듈: **NR `BCH_CTRLR`(= NR L1 Channel Controller)**, **NR L1 Tx**, **LTE `ChCfg`(= LTE L1 Channel Configuration Controller)**, **LTE L1 Tx**
- **v0.5의 NR 분류표·책임 경계·안정 ID 전부 보존**하고 LTE ChCfg 및 LTE Tx 2개 모듈을 확장. 기존 NR 내용을 LTE에 무비판적으로 복제하지 않음.
- 사용 목적: **사내 GPT가 1차로 누락·중복·소유권·우선순위 검토** → 사용자/GPT 판정 → 나중에 선택한 항목만 `l1-knowledge-updater`에 분석 요청.
- 현재 작업 금지: 사내 코드/로그 반출, 새 Job-list Job 활성화, `l1-knowledge-updater`·`code-analyzer` 실행, MSC 생성, 기존 코드/Knowledge 정본 수정, 운영 설정 수정, PUBLIC/PRIVATE 게시.
- 근거 우선순위: **사용자가 확인한 L1 소유권 > 실제 코드의 동작 사실(후속 단계) > 3GPP 절차 > 클래스명 추측**. 표준은 상위 RRC/MAC/PHY 동작을 규정할 뿐 사내 클래스 소유권을 지정하지 않음.
- `CONFIRMED_FROM_USER`: NR BCH는 SCell DL/UL L1 Procedure 주관, NR L1 Tx는 UL subflow 참가, LTE ChCfg는 이에 대응되는 LTE L1 채널 관리 역할. **LTE의 세부 함수·메시지·지원 Feature는 CODE_TO_VERIFY**.
- 결과 상태: **PREPARED_FOR_INHOUSE_GPT_REVIEW**; 코드 실행/제품 실측/독립 리뷰/그룹 Knowledge 갱신 **NOT_RUN**.

## 0. 전체 구조 및 소유권 개요

| RAT | A. Procedure / Scenario 주관 모듈 | L1 Tx 하위 참여 구간 | B. Technical Knowledge 연계 | 확인 상태 |
|---|---|---|---|---|
| NR | `BCH_CTRLR` (L1 Channel Controller) | NR L1 Tx (UL Tx·Switching·SRS Carrier Switching 등 조건부) | NR BCH-B*, TX-B* | 사용자 역할 확인; 세부 구현 미검증 |
| LTE | `LTE ChCfg` (L1 Channel Configuration Controller) | LTE L1 Tx (UL Tx·RF Tx Config·Tx Path/Sharing 등 조건부) | LTE-CH-B*, LTE-TX-B* | 동일 개념의 LTE 담당 역할 사용자 확인; 세부 구현 미검증 |

**A 축은 Procedure별 전체 대표 흐름과 MSC를, B 축은 여러 Procedure에서 공유하는 기술 원리를 다룹니다.** 원본 MSC는 주관 모듈을 기준으로 관리하고 Tx 구간은 링크 가능한 subflow로 연결합니다. **4개 모듈을 하나의 광역 MSC로 무조건 합치지 않습니다.**

**경계 제외**: Measure Controller의 Search/Measurement 본체, DRX Controller의 Idle DRX/CDRX 본체는 각각 소유 모듈에 남깁니다. Tx는 **CDRX와의 연동 구간만**, Channel Controller는 관련 경계 인터페이스만 분석합니다. Paging 독립 Procedure는 이번 사용자 선별 목록에서 제외합니다.

---

# Part I. 기존 NR 분류 (v0.5 유지)

## 1. 핵심 결론: 주관 Procedure와 참여 모듈의 분리

**`BCH_CTRLR`이라는 이름은 PBCH 전용 기능을 뜻하지 않는다.** 이 제품의 `BCH_CTRLR`은 **NR L1 Channel Controller**로서, **DL/UL SCell Configuration / Activation / Deactivation / Release의 L1 Procedure를 주관**한다. 해당 절차에서 **NR L1 Tx는 UL 송신 관련 일부 구간에 참여**한다. 또 NR L1 Tx에는 **UL Tx Switching**, **Tx Antenna Switching**, **Tx Path Switching**, **SRS Carrier Switching**과 관련된 구성·실행 구간이 포함될 수 있다. 추가로 **NRDC에서 BB TX Reconfig·F1 Rank Change**, **UL CA에서 SLO·RF Tx Config**, **Dual SIM에서 Tx Sharing·BB Tx Change**가 분석 후보로 지정됐다. **NRDC는 EN-DC와 구별**하고, `F1`, `SLO`, `BB TX`의 제품별 의미는 사내 GPT가 실제 코드·정책에서 확인할 대상이다.

| 분석 주제 | 대표 Procedure 주관(A) | L1 Tx 참여 구간(A) | Technical Knowledge(B) | 비고 |
|---|---|---|---|---|
| SCell Configuration | **BCH-A10** | **TX-A3** UL 송신 설정/자원 적용 | BCH-B1/B3/B4/B5, TX-B3/B5/B6/B7 | DL/UL 구성은 분리해 분석. SCell에 UL이 없는 경우 UL 분기는 `NOT_APPLICABLE` |
| SCell Activation | **BCH-A10** | **TX-A3** UL Tx 활성화/전환 조건 | BCH-B3/B5, TX-B3/B4/B7 | 활성화 사건이 항상 안테나·경로 전환을 일으키는 것은 아님 |
| SCell Deactivation | **BCH-A10** | **TX-A3** UL Tx 중지/자원 상태 조정 | BCH-B3/B5/B7, TX-B3/B4/B7 | 중복 중지/재활성화, pending 처리 확인 후보 |
| SCell Release | **BCH-A10** | **TX-A3** UL Tx 자원/설정 해제 | BCH-B1/B3/B5, TX-B3/B5/B7 | Release와 Deactivation은 구별 |
| BWP Switching | **BCH-A9** | 실제 UL Tx 설정 재적용에 한해 TX-A2/A3 연결 | BCH-B1/B3/B5, TX-B5/B6 | RRC/DCI/Timer 기반 전환 중 BCH가 실제 소유하는 경계 확인 |
| UL Tx Switching | SCell 변화에 따른 경우 **BCH-A10**에서 연결 | **TX-A3/A4/A6**의 실제 UL switching 구간 | **TX-B4** | CA/EN-DC 등 트리거별로 분리. SCell 변화와 무관한 switching도 가능 |
| Tx Antenna / Path Switching | 특정 SCell 단계와 연계 시 **BCH-A10**에서 참조 | **TX-A3/A4/A6**의 해당 처리 | **TX-B3/B4** | 안테나·경로·Tx Chain 개념은 실제 코드로 구별 |
| SRS Carrier Switching | SCell 설정·상태와 직접 연계된 구간만 **BCH-A10**에서 참조 | **TX-A3/A6** 및 실제 조건에 따라 TX-A2 | **TX-B2/B4/B5** | **독립 기술 후보이기도 함**. 모든 SCell Activation의 필수 단계로 가정 금지 |
| UL CA SLO · RF Tx Config | **BCH-A10**의 SCell 절차 중 연결된 경우만 참조 | **TX-A3-SLO / TX-A3-RFTX** | **TX-B3/B5/B6/B7** | `SLO` 정의·실행 조건과 RF Tx 설정 경계는 코드로 검증. SCell 4단계 모두에서 실행된다고 가정 금지 |
| NRDC BB TX Reconfig · F1 Rank Change | NRDC 연동이 필요한 L1 Channel 설정 경계만 참조 (`TO_VERIFY`) | **TX-A9** 독립 Procedure | **TX-B5/B6/B7** | EN-DC와 구분. `F1`의 정확한 의미·Rank Change 트리거/결과 확인 |
| Dual SIM Tx Sharing · BB Tx Change | BCH가 실제 연계하는 경우 인터페이스만 참조 (`TO_VERIFY`) | **TX-A10** 독립 Procedure | **TX-B3/B4/B5/B6/B7** | Stack/Domain/Peer 우선순위·자원 경쟁·회수·복구의 실제 소유권 확인 |

**소유권 원칙:** `BCH-A10`에 **전체 L1 SCell 시나리오 Overview/대표 MSC**를 두고, `TX-A3`에는 **그 MSC에서 Tx가 담당하는 수신 메시지 → Tx 설정/상태/스위칭 → HAL/PHY 경계**만 상세화한다. `TX-B*`는 여러 Procedure가 참조하는 공통 기술 설명이다. 동일 흐름의 MSC를 별개의 원본으로 복제하지 않고 **Procedure MSC ↔ Tx subflow ↔ Technical Knowledge** 링크로 연결한다.

## 2. 공통 분석 분류 모델

- **A. Procedure / Scenario:** 네트워크 절차 관점에서 언제·무엇 때문에 시작하고, 모듈 간 어떤 제어/상태/IPC 경계로 끝나는가? `Overview`, 대표 흐름, 조건별 분기, `AS-IS MSC`의 기준.
- **B. Technical Knowledge:** `BWP/CC`, 물리채널/신호, Tx 자원, switching, 인터페이스, 상태·복구 등 반복 활용되는 공통 기술. A에서 재사용.
- **역할:** `LEAD_L1_PROCEDURE`(L1 전체 제어 구간의 주관), `PARTICIPANT_SUBFLOW`(일부 구간), `INTERFACE_ONLY`, `OTHER_MODULE_OWNED`, `TO_VERIFY`.
- **용어 주의:** 3GPP의 **RRC 설정 / MAC 활성화 결정 / PHY 송수신 절차**와 **사내 `BCH_CTRLR`/Tx 클래스 책임**은 다른 계층의 개념. 표에서 `LEAD_L1_PROCEDURE`는 RRC/MAC 규격 자체의 소유를 의미하지 않음.
- **분리:** DL/UL은 L1 내부 영향 범위를 각각 확인하지만, **DL SCell Activation / UL SCell Activation이 언제나 별개 3GPP 이벤트라는 의미는 아님**. SCell 상태 변화가 어느 DL/UL 경로에 영향을 주는지 추적하기 위한 분석 축.
- **검증값:** `PLANNED`, `REVIEW_NEEDED`, `CODE_VERIFIED`, `PARTIAL`, `INTERFACE_ONLY`, `NOT_APPLICABLE`, `BLOCKED` 등. 이름으로 함수·메시지를 지어내지 말 것.

## 3. NR L1 Channel Controller (`BCH_CTRLR`) — A. Procedure / Scenario

> 기존 식별자 유지. `BCH-A6 Paging`은 **삭제 상태로 재사용하지 않음**. 새 SCell 주관 절차는 **`BCH-A10`**으로 신설.

| ID | 대표 Procedure | 분석해야 할 대표 시나리오(후보) | 책임 및 경계 |
|---|---|---|---|
| BCH-A1 | Initial Access / Attach | 동기 결과 수신 → PBCH/MIB 관련 L1 처리 → 초기 채널 설정 및 후속 SI 단계 연동 | Search/Measure 자체는 제외, MIB는 이 Procedure 하위 |
| BCH-A2 | System Information Acquisition | SIB 수신/Decoding 관련 L1 채널 설정·결과 처리·재획득·갱신 | 실제 SIB 복호 주체는 코드 확인. SIB1은 PBCH가 아닌 PDCCH/PDSCH 기반 |
| BCH-A3 | RRC Reconfiguration | RRC에서 전달된 L1 채널 설정 변경, DL/UL 관련 파라미터·BWP/CC 재구성 | RRC와 L1 경계 및 변경 사항의 downstream 적용 범위 |
| BCH-A4 | Mobility / Handover | Target Cell로 전환 시 L1 채널 정리·재설정·상태 전이 | Search/Measure, RRC/MAC 부분은 인터페이스까지만 |
| BCH-A5 | Cell Reselection / Recovery 연동 | 셀 재선택/복구 결과에 따른 채널 재설정·재획득 | 셀 선택 알고리즘 자체는 다른 모듈 소유 |
| BCH-A7 | Release / Suspend / Resume | L1 채널 구성 해제/중단/재개에 따른 자원·상태 전이 | 실제 관련 프로시저와 지원 여부 검증 |
| BCH-A8 | Exception / Recovery | Config 실패·타임아웃·State mismatch·복구 분기 | 진입 조건·후속 호출·Rollback 가능 여부 확인 |
| BCH-A9 | BWP Switching | RRC 설정 변경, DCI 기반 변경, BWP inactivity timer 전환 중 BCH L1 구간 | 각 전환 트리거와 상태 전이; DCI/Timer 실행 소유는 코드로 확인 |
| **BCH-A10** | **SCell Configuration / Activation / Deactivation / Release (DL + UL L1)** | **아래 8개 DL/UL 영향 구간을 통합 Procedure로 분석** | **SCell 관련 L1 Procedure 주관 모듈**. RRC/MAC 상위 이벤트와 Tx 참여 구간을 별도 표시 |

### BCH-A10 세부 분석 아이템: L1 SCell Procedure (최우선 후보)

| 세부 ID | SCell 단계 | DL L1 분석 항목 | UL L1 분석 항목 | Tx 연동 및 확인 포인트 |
|---|---|---|---|---|
| BCH-A10-CFG | Configuration | DL CC/채널/BWP/리소스/상태 초기화, PHY 연동 | UL CC/채널/BWP/UL Resource 설정 **(UL 구성 시)** | `TX-A3-CFG`로 이어지는 설정 전달·수신·적용·IPC; Switching 사전 조건만 해당 시 확인 |
| BCH-A10-ACT | Activation | DL 관련 활성 상태·채널 수신 설정/제어 | UL Tx 허용/활성화 및 관련 상태 **(UL 구성 시)** | `TX-A3-ACT`와 연결. UL Tx Switching·SRS CS 필요성/조건 분기 추적 |
| BCH-A10-DEACT | Deactivation | DL 관련 비활성·감시/채널 상태 처리 | UL 송신 중단·자원/상태 처리 **(UL 구성 시)** | `TX-A3-DEACT`와 연결. SRS/Tx Path/Tx Chain 중단·복귀 정책 확인 |
| BCH-A10-REL | Release | DL 관련 채널/CC/BWP 설정·자원 해제 | UL Tx 설정·자원 해제 **(UL 구성 시)** | `TX-A3-REL`과 연결. 선행 Deact 여부, 중복 Release/cleanup/pending 처리 확인 |

*위 표의 DL/UL 열은 각 사건에서 영향을 받는 **L1 내부 경로**를 분리한 것이지, 별개의 네트워크 Activation MAC CE를 상정한 것이 아니다. 네 단계의 DL/UL 분기를 필요한 경우 8개 하위 증거 세트로 세분 가능.*

### BCH 측 우선 확인 질문

1. `RRC Config` / `MAC SCell Status` 등 상위에서 시작한 실제 메시지가 **어떤 BCH handler로 유입**되는가? 메시지 명칭은 소스에서 확정.
2. Cell/CC/BWP 구성, DL/UL 채널 관련 상태, activation bitmap, release 순서 중 **BCH가 직접 소유**하는 것은 무엇인가?
3. `BCH → NR L1 Tx`로 전달되는 설정/상태/명령은 어느 이벤트에서 생성되는가? Tx는 어떤 Ack/Completion/Error를 반환하는가?
4. SCell 활성화 또는 비활성화가 **UL Tx Switching / SRS Carrier Switching을 요구하는 경우와 요구하지 않는 경우**는 어떻게 구별되는가?
5. 코드가 UL 없는 DL-only SCell, Multi-CC, EN-DC/UL CA, 중복 이벤트·Retry·Release 후 Activation을 어떻게 처리하는가?

## 4. NR L1 Channel Controller — B. Technical Knowledge

| ID | 기술 대분류 | 분석 후보 |
|---|---|---|
| BCH-B1 | L1 Channel Configuration | DL/UL 채널 설정, SCell Add/Modify/Release 파라미터, BWP Configuration 및 재설정 |
| BCH-B2 | PBCH/MIB · SI 처리 연동 | PBCH/MIB 획득 처리, SIB 수신/Decoding 설정·결과 경계(복호 주체 확인) |
| BCH-B3 | Channel / Cell Resource | DL/UL CC, Serving Cell/SCell, BWP, 채널별 리소스 설정과 상태 |
| BCH-B4 | Interface | RRC/MAC 상위 설정 경계, Measure/DRX와의 인터페이스, NR Tx, HAL/PHY IPC |
| BCH-B5 | State Management | Configured/Activated/Deactivated/Released, Active BWP, 상태 불일치와 중복 이벤트 |
| BCH-B6 | Timing / Scheduling 연동 | L1 채널 설정 시점, Activation 적용 시점, BWP 전환 타이밍·동기화 연동(타 모듈 자체 알고리즘 제외) |
| BCH-B7 | Recovery / Diagnostics | Config 실패, Timeout, 재시도·정리·해제, 실패 근거 수집 |

**책임 제외:** Search/Measure 실제 알고리즘은 Measure Controller, Idle DRX·CDRX 실제 기능은 DRX Controller가 담당. **Paging Procedure는 목록에서 제외**. 다만 인터페이스 연동은 필요한 곳에서 제한적으로 기록.

## 5. NR L1 Tx — A. Procedure / Scenario

> 기존 `TX-A1~A8` ID 유지, **TX-A9(NRDC)** 및 **TX-A10(Dual SIM)** 추가. `TX-A7`은 **CDRX 연동만**. SCell 관련 Tx 항목은 **BCH-A10의 하위 참여 구간**으로 표현. NRDC는 EN-DC와 별도 분류.

| ID | 대표 Procedure | NR L1 Tx의 대표 분석 구간 | 역할 |
|---|---|---|---|
| TX-A1 | Initial Access / Attach | Initial RACH, UL Tx 초기 설정, Msg3 송신 관련 Tx 제어 | PARTICIPANT_SUBFLOW |
| TX-A2 | RRC Reconfiguration | Tx 관련 재설정/UL BWP/CC/Tx 리소스 재적용 | PARTICIPANT_SUBFLOW |
| **TX-A3** | **UL CA / SCell Procedure 참여** | **BCH-A10에서 내려온 SCell CFG/ACT/DEACT/REL의 UL Tx 처리, 필요시 UL Tx/SRS Carrier Switching. UL CA 중 SLO 및 RF Tx Config 추가 조사** | **PARTICIPANT_SUBFLOW** (SCell 주관 아님) |
| TX-A4 | EN-DC | NR SCG·LTE/NR 동시 송신 중 Tx 우선순위, 자원 경합/UL switching | PARTICIPANT_SUBFLOW |
| TX-A5 | Mobility | Handover·재RACH·셀 전환 중 UL Tx 재설정/Path 전환 | PARTICIPANT_SUBFLOW |
| TX-A6 | Connected Mode | 정상 UL Tx, Tx Antenna/Path Switching, SRS Carrier Switching(관련 조건 발생 시), 상태 전환 | PARTICIPANT_SUBFLOW |
| TX-A7 | **CDRX 연동** | CDRX 중 Tx 허용/중지/재개 요청 및 Tx 내부 제어 구간 | DRX Controller 실제 상태 머신 제외 |
| TX-A8 | Exception / Recovery | UL Tx Config/Activation/Path 실패, 경쟁·중복 요청·재설정·Release | Tx 범위만 분석 |
| **TX-A9** | **NRDC** | **NRDC 동작 중 BB TX Reconfig, F1 Rank Change**: 초기/변경 Trigger, 재구성 요청·적용·완료, Rank 변경 조건 및 Tx 영향 | **PARTICIPANT_SUBFLOW**, NRDC L1 Tx 경계만 확인; EN-DC와 별도 |
| **TX-A10** | **Dual SIM** | **Tx Sharing, BB Tx Change**: Stack/Domain 간 요청·우선순위·경합·전환·복귀·동시 이벤트 | **PARTICIPANT_SUBFLOW**, Peer/공통 Tx 관리와의 책임 경계 확인 |

### TX-A3 세부 분석 아이템: BCH-A10과 1:1 대응

| 세부 ID | BCH 기준 이벤트 | NR L1 Tx가 분석할 실제 구간 | 조건부 관련 기술 |
|---|---|---|---|
| TX-A3-CFG | `BCH-A10-CFG` | BCH/공통 컨트롤러의 UL SCell 설정 수신 → CC/Tx resource/Tx path 설정 → HAL/PHY 제어 경계 | `TX-B3` 자원, `TX-B5` Config, `TX-B4` switching 준비/결정 |
| TX-A3-ACT | `BCH-A10-ACT` | UL SCell 활성화 전달 → Tx resource enable/상태 전환 → PHY/HAL | 필요 시 **UL Tx Switching, Antenna/Path Switching, SRS Carrier Switching** |
| TX-A3-DEACT | `BCH-A10-DEACT` | UL SCell 비활성화 전달 → UL Tx disable/자원 조정 → 결과/경계 | 이전 switching 자원 회수/재할당, SRS 관련 상태 분기 |
| TX-A3-REL | `BCH-A10-REL` | UL SCell 해제 전달 → Tx 관련 설정·리소스/잔여 상태 정리 | Pending switch 취소/완료 처리, 일관성 검사 |

**중요:** 이 연결은 **'BCH가 SCell L1 Procedure를 주관하고 Tx가 그 일부를 지원한다'는 사용자 확인 정보**를 모델링한다. `TX-A3-*`가 매번 switching을 수행한다는 주장은 아님. 실제 소스에서 trigger/guard/capability/지원 Band/CC/빌드 옵션을 확인해야 함.

### TX-A3 추가 분석 아이템: UL CA의 SLO 및 RF Tx Config

| 세부 ID | 대상 | 사내 GPT가 1차 확인할 분석 범위 | BCH-A10 관계 |
|---|---|---|---|
| **TX-A3-SLO** | **SLO** | 제품 코드에서의 SLO 정의·주관 모듈·Trigger, UL CA 관련 설정/상태·제약, 정상/예외 전환, Tx 참여 구간 | SCell CFG/ACT/DEACT/REL 중 실제 연계되는 이벤트만 링크 (`TO_VERIFY`) |
| **TX-A3-RFTX** | **RF Tx Configuration** | UL CA의 RF Tx Config 요청·설정값·resource/path/antenna 대응·적용 순서·HAL/RF/PHY 경계·결과/복구 | BCH-A10의 UL 구성/상태 이벤트와 조건부 링크; 설정이 각 이벤트에서 항상 수행된다고 가정 금지 |

> `SLO` 약어는 현재 대화에서 기술적 확장형이 확인되지 않았으므로 **원문을 유지**한다. SLO와 RF Tx Config가 동일 기능인지, 선행·후행 또는 독립인지도 코드 근거로 판정한다.

### TX-A9 추가 분석 아이템: NRDC

| 세부 ID | 핵심 분석 주제 | 분류 및 확인 사항 |
|---|---|---|
| **TX-A9-BBTX-RCFG** | **BB TX Reconfig** | NRDC 구성/변경 트리거 → NR L1 Tx의 BB 설정 변경·상태·하위 명령 적용 → 완료/실패. 기존 설정 유지/정리·Race·타 스택 영향 |
| **TX-A9-F1-RANK** | **F1 Rank Change** | Rank 변경 조건·입력/결정 주체·상태/제약·BB TX/PHY 적용 경계·NRDC와의 연동. `F1` 정의·carrier/feature 의미 확인 |

> `NRDC`와 `EN-DC(TX-A4)`는 한 항목으로 합치지 않는다. Rank Change와 BB TX Reconfig 사이의 선후·인과·공통 함수를 **미확정**으로 표시하며, 실제 코드·빌드 옵션으로 판단한다.

### TX-A10 추가 분석 아이템: Dual SIM

| 세부 ID | 핵심 분석 주제 | 분류 및 확인 사항 |
|---|---|---|
| **TX-A10-SHARING** | **Tx Sharing** | Stack/Domain/Peer 상황별 Tx 자원 소유·요청/양보·우선순위·충돌·중단/복귀·중복 이벤트와 예외 경로 |
| **TX-A10-BBTX-CHG** | **BB Tx Change** | Dual SIM 변경 트리거 → BB Tx 설정/리소스 선택·적용·복귀 → HAL/PHY 및 결과 경계. Tx Sharing과의 호출/상태 연계 확인 |

> `BB TX Reconfig`(NRDC)와 `BB Tx Change`(Dual SIM)는 용어가 비슷해도 **서로 다른 분석 시나리오**로 보존한다. 실제 동작이 공통 코드로 합쳐지는지는 사내 근거 확인 후 **B 기술 항목에서만 공통화**한다.

## 6. NR L1 Tx — B. Technical Knowledge

| ID | 기술 대분류 | 분석 후보 |
|---|---|---|
| TX-B1 | UL Physical Channel | PUSCH, PUCCH, PRACH Configuration/송신 제어·경계 |
| **TX-B2** | **Reference Signal / SRS** | SRS Configuration/Trigger/송신, **SRS Carrier Switching**의 Trigger/대상 CC/절차/타이밍 |
| TX-B3 | Tx Resource | Tx Antenna, Tx Chain, RF/Tx Path, CC·RF Resource Allocation/Mapping, **UL CA RF Tx Resource**, **Dual SIM Tx Sharing의 자원 경쟁/우선순위** |
| **TX-B4** | **Tx Switching** | **UL Tx Switching**, **Tx Antenna Switching**, **Tx Path Switching**, **SRS Carrier Switching**, **Dual SIM Tx Sharing**의 연동·제약·우선순위·switch gap/충돌 처리 |
| TX-B5 | Tx Configuration | UL CA/CC/BWP, Tx switching 관련 설정, Power Control 관련 L1 제어, **UL CA SLO/RF Tx Config**, **NRDC BB TX Reconfig·F1 Rank Change의 BB 설정 영향**, **Dual SIM BB Tx Change** |
| TX-B6 | Interface | BCH ↔ Tx, TxCfg/TxCmd, HAL/RF/PHY IPC, 결과·완료/예외 전달, **NRDC/UL CA/Dual SIM 이벤트 발신자·수신자 및 경계** |
| TX-B7 | State Management | Config/Active/Deactive/Release, Tx Path/Chain/Carrier switching 진행 상태·동시성·정리, **NRDC Rank·BB Tx**, **Dual SIM 공유/소유권 상태** |

### Switching 종류별 중복 방지 규칙

| 기술 식별자 | 개념적 분석 경계 | 주요 참조 연결 |
|---|---|---|
| TX-B4-ULSW | **UL Tx Switching**: 복수 UL carrier/band 또는 EN-DC 등에서 UL Tx 전환 정책과 gap/제약 | TX-A3, TX-A4, TX-A6 및 BCH-A10(해당 이벤트에 연계된 경우) |
| TX-B4-ANTSW | **Tx Antenna Switching**: Tx 안테나/안테나 리소스 선택·전환 | TX-A3/A6, 필요 시 TX-A4 |
| TX-B4-PATHSW | **Tx Path Switching**: Tx RF 경로/chain/route 변경 | TX-A3/A4/A6, 필요 시 TX-A5 |
| TX-B2-SRSCS | **SRS Carrier Switching**: 다른 carrier에서의 SRS 송신을 위한 carrier/자원 전환, Tx switch와의 상호작용 | TX-A3/A6, TX-B2/B4, BCH-A10(해당 SCell 상태·설정 변화와 관련될 때만) |
| TX-B5-SLO | **UL CA SLO**: 정확한 약어 정의·설정/상태·조건/인과 관계 분석 (`TO_VERIFY`) | TX-A3-SLO, 필요 시 TX-A3-RFTX |
| TX-B5-RFTX | **RF Tx Config**: UL CA 시 RF 설정 요청·적용·결과/복구, Path/Resource와의 연결 | TX-A3-RFTX, TX-B3/B6 |
| TX-B5-NRDC-BBTX | **NRDC BB TX Reconfig**: BB TX 파라미터 재적용·상태 전이의 공통 기술 | TX-A9-BBTX-RCFG, TX-B6/B7 |
| TX-B5-F1RANK | **F1 Rank Change**: 제품의 `F1` 정의, 랭크 상태/설정 제약·적용 경계 | TX-A9-F1-RANK, TX-B7 |
| TX-B4-DSHARE | **Dual SIM Tx Sharing**: Stack/Domain/Peer 자원 조정과 경합/복귀 정책 | TX-A10-SHARING, TX-B3/B7 |
| TX-B5-DSBBTX | **Dual SIM BB Tx Change**: BB 송신 자원·설정 변경 및 복귀 | TX-A10-BBTX-CHG, TX-B3/B6/B7 |

> UL Tx Switching, Tx Antenna Switching, Tx Path Switching, SRS Carrier Switching은 **자동으로 동의어가 아니다**. 제품 코드에서는 하나의 하위 경로를 공유할 수 있으므로 공통 함수는 한 번만 깊이 분석하고 A 시나리오에서 호출 관계를 링크한다. SRS Carrier Switching은 SCell Configuration/Activation/Deactivation/Release의 **항상 필수인 단계가 아니며**, 이 네 사건과 무관한 조건에서도 발생할 수 있다.

## 7. 대표 시나리오 Coverage / 우선순위 후보

| 우선순위 초안 | 분석 마스터 항목 | 시작·종료 경계 확인 목표 | 공통 기술 참조 |
|---|---|---|---|
| P0 | BCH-A10-CFG/ACT/DEACT/REL | 상위 설정/상태 이벤트 → BCH L1 처리 → Tx/PHY 연계 → 완료/오류 | BCH-B1/B3/B4/B5 |
| P0 | TX-A3-CFG/ACT/DEACT/REL | BCH→Tx event → UL Tx state/config/switch 판단 → HAL/PHY | TX-B3/B4/B5/B6/B7 |
| P1 | BCH-A9 BWP Switching | RRC/DCI/Timer 기원별 BCH 참여 경계 | BCH-B1/B3/B5 |
| P1 | TX-B4 UL Tx / Antenna / Path Switching | 트리거 → 정책·자원 선정 → 전환 완료/오류 | TX-B3/B4/B6/B7 |
| P1 | TX-B2-SRSCS SRS Carrier Switching | SRS 설정·트리거 → carrier/resource 전환 → 송신/복귀 | TX-B2/B4/B5/B6 |
| **P1(초안)** | **TX-A9-BBTX-RCFG / TX-A9-F1-RANK** | NRDC 조건/트리거 → BB TX 재구성·F1 Rank 변화(독립/연동 여부 확인) → 완료/오류 | TX-B5/B6/B7 |
| **P1(초안)** | **TX-A3-SLO / TX-A3-RFTX** | UL CA 조건/Trigger → SLO 및 RF Tx 설정 처리 → 적용/결과 경계 | TX-B3/B5/B6/B7 |
| **P1(초안)** | **TX-A10-SHARING / TX-A10-BBTX-CHG** | Dual SIM 공유·경합 → BB Tx 변경 → 복귀/예외 | TX-B3/B4/B5/B6/B7 |
| P2 | BCH-A1/A2/A3, TX-A1/A2 | 초기 접속/SI/RRC 변경에서 각 모듈 책임 구간 | 관련 B 항목 |
| P2 | 나머지 BCH/TX Procedure | Mobility, EN-DC, Connected Mode, CDRX 연동, 예외/복구 | 관련 B 항목 |

*우선순위는 사용자 확정 전 **추천안**. 첫 목표는 실제 실행이 아니라 '어떤 분석 항목이 있는가'를 선별하는 것.*

---

# Part II. LTE 신규 분류 (v0.6 확장)

## 8. LTE 적용 원칙과 NR↔LTE 차이

1. **LTE ChCfg는 NR BCH와 동일한 업무 관점의 L1 Channel 제어 모듈**입니다. 특히 SCell Configuration / Activation / Deactivation / Release의 **L1 Procedure 개괄과 DL/UL 영향 구간**을 주관한다는 사용자 설명을 LTE로 확장하되, 실제 클래스명·코드 엔트리·메시지·전이 순서는 사내 GPT 검토 대상입니다.
2. **LTE L1 Tx는 LTE ChCfg의 SCell L1 Procedure에서 UL Tx 관련 일부분에 참여**합니다. Tx가 SCell Configuration/Activation의 *상위 RRC/MAC 절차를 소유*한다고 표현하지 않습니다.
3. **LTE에는 NR의 BWP Switching(38.331 BWP 개념)을 그대로 적용하지 않습니다.** LTE PCell/SCell, CC, DL/UL bandwidth, UL/DL carrier configuration·scheduling 등 LTE 고유 단위로 재분류합니다.
4. **NRDC, NR F1 Rank Change를 LTE의 기본 Procedure로 복제하지 않습니다.** 반면 **EN-DC의 LTE 측 동작**은 LTE Tx와 LTE ChCfg의 연동 범위에 해당할 수 있습니다. LTE Master/NR Secondary 구조는 실제 구현·서비스 모드를 확인해야 합니다.
5. LTE ULCA/SLO/RF Tx Config/UL Tx Switching/SRS Carrier Switching/Tx Antenna·Path Switching은 **지원 여부를 별도 확인해야 하는 후보**입니다. NR에 기능이 있다고 LTE에도 무조건 동일하다고 가정하지 않습니다.
6. **Dual SIM Tx Sharing / BB Tx Change**는 LTE에서도 독립 Procedure 분석 후보로 둡니다. 다만 동일한 공통 Tx Manager 구현을 공유하는지, peer-RAT와 stack/domain 우선순위가 어떤지는 사내 코드 확인 후 통합 여부 판정합니다.
7. LTE의 **SCell Activation/Deactivation은 규격상 SCell 상태를 제어**합니다. 아래 DL/UL 컬럼은 L1 구현의 **영향 경로**를 나눈 것이지 규격상 두 개의 별도 Activation/Deactivation 메시지가 항상 존재한다는 뜻이 아닙니다.
8. `LTE ChCfg`라는 표현은 사용자 제공 모듈 명칭입니다. 실제 패키지 디렉터리·클래스·여러 Controller에 기능이 분산됐는지는 실측 없이 단정하지 않습니다.

### 8.1 LTE/NR 항목 대응표

| NR 항목 | LTE 대응 후보 | 매핑 판단 |
|---|---|---|
| BCH-A1 Initial Access/Attach | LTE-CH-A1 LTE Initial Access/Attach | **MATCH_AT_CONCEPT** (LTE MIB/SIB/RRC 차이 확인) |
| BCH-A2 SI Acquisition | LTE-CH-A2 SI Acquisition | MATCH_AT_CONCEPT, LTE SIB 분류로 검증 |
| BCH-A3 RRC Reconfiguration | LTE-CH-A3 `RRCConnectionReconfiguration` | **LTE_SPECIFIC** RRC 명령 및 설정 필드 |
| BCH-A9 BWP Switching | LTE-CH-A9 PCell/Serving Cell Configuration | **NOT_EQUIVALENT**; BWP를 대체 용어로 사용 금지 |
| BCH-A10 SCell CFG/ACT/DEACT/REL | LTE-CH-A10 SCell CFG/ACT/DEACT/REL | MATCH_AT_CONCEPT; RRC 36.331/MAC 36.321 참조 |
| TX-A3 UL CA/SCell participation | LTE-TX-A3 UL CA/SCell participation | MATCH_AT_CONCEPT; UL capability·CC 제약 확인 |
| TX-A4 EN-DC | LTE-TX-A4 EN-DC (LTE 측 역할) | MATCH_AT_CONCEPT, LTE anchor/TX priority 구체값은 CODE_TO_VERIFY |
| TX-A9 NRDC BB TX / F1 Rank | — | **NR_ONLY_CANDIDATE**: LTE에 자동 복제 금지 |
| TX-A10 Dual SIM | LTE-TX-A10 Dual SIM | MATCH_AT_CONCEPT; 공유 구현과 구별된 LTE subflow 확인 |
| TX-A7 CDRX 연동 | LTE-TX-A7 CDRX 연동 | MATCH_AT_CONCEPT; DRX 본체는 DRX Controller 소유 |

## 9. LTE Channel Config (`LTE ChCfg`) — A. Procedure / Scenario

> **LTE ChCfg = LTE L1 Channel Configuration Controller**로 표기합니다. `LTE-CH-A6 Paging`은 초기 목록에 포함하지 않으며 ID A6은 예약(미사용). `LTE-CH-A9`는 NR BWP와 구별되는 LTE PCell/CC 설정 흐름입니다.

| ID | 대표 LTE Procedure | L1 Channel 관점 대표 시나리오 후보 | 역할·범위 |
|---|---|---|---|
| **LTE-CH-A1** | Initial Access / Attach | 셀 동기화 결과 연동 → PBCH/MIB 처리 → LTE SIB 획득 관련 채널 구성 → 최초 RRC/L1 채널 설정 | `LEAD_L1_PROCEDURE`(L1 범위); 탐색/측정 본체 제외 |
| **LTE-CH-A2** | System Information Acquisition / Update | SIB 획득에 필요한 DL 채널 설정, 후속 SI 변경/재수신·처리 경계 | L1 채널 설정 담당 범위만. RRC의 SI 해석 자체 소유 가정 금지 |
| **LTE-CH-A3** | RRC Connection Reconfiguration | RRC에서 하달한 PCell/CC, DL/UL 채널·리소스 설정 변경, 하위 송신·수신 경계 | LTE `RRCConnectionReconfiguration`과 L1 메시지/상태 연결 |
| **LTE-CH-A4** | Mobility / Handover | Target Cell/PCell 전환, 채널 초기화·재설정·적용 순서 및 Completion | 측정·RRC HO 판단은 인터페이스까지만 |
| **LTE-CH-A5** | Cell Reselection / Re-establishment 연동 | 셀 재선택·RRC 재설립 시 채널 제거/재설정/초기화·재획득 영향 | 채널 재설정 경계만; 선택 알고리즘/DRX 제외 |
| **LTE-CH-A7** | Release / Suspend / Resume | 채널 자원 해제·중단·복귀 및 관련 상태 전이 | Rel/제품 지원 여부에 따라 `NOT_APPLICABLE` 가능 |
| **LTE-CH-A8** | Exception / Recovery | 잘못된 구성, 타이밍 불일치, 중복 ACT/DEACT/REL, 실패·Recovery | 채널 관리 책임에 한정 |
| **LTE-CH-A9** | PCell / Serving Cell / CC Reconfiguration | PCell/Serving Cell·DL/UL CC·bandwidth·carrier mapping 변경에 수반되는 L1 channel reconfig | NR BWP 대응이 **아님**; A3/A10과 중복 제거 필요 |
| **LTE-CH-A10** | **SCell Configuration / Activation / Deactivation / Release (DL + UL L1)** | **LTE SCell 4단계별 Channel 전체 영향 및 LTE Tx 참여 흐름** | **LEAD_L1_PROCEDURE**; 규격과 실제 내부 트리거 구분 |
| **LTE-CH-A11** | EN-DC LTE Cell Group 연동 | EN-DC 구성·변경·중단·해제 중 LTE 측 PCell/MCG, L1 Channel 적용/상태·NR 연동 경계 | `TO_VERIFY` — 별도 Controller 주관이면 INTERFACE_ONLY |

### 9.1 LTE-CH-A10 세부 항목 — SCell L1 4단계

| 세부 ID | Procedure | DL L1 설정·영향 | UL L1 설정·영향 (UL 구성 시) | LTE L1 Tx 하위 참조 |
|---|---|---|---|---|
| **LTE-CH-A10-CFG** | SCell Configuration | DL CC/Cell/Channel/PHY 파라미터 적용, 자원·상태 초기화 | UL CC/Tx-related 설정 요청·상태 준비 | **LTE-TX-A3-CFG** |
| **LTE-CH-A10-ACT** | SCell Activation | DL 수신·채널/스케줄링 관련 활성화 영향 | UL Tx enable·리소스 적용 여부 | **LTE-TX-A3-ACT** |
| **LTE-CH-A10-DEACT** | SCell Deactivation | DL 수신·활성 상태 감소/중단 및 정리 | UL Tx 중지/자원 조정·해제 시점 | **LTE-TX-A3-DEACT** |
| **LTE-CH-A10-REL** | SCell Release | DL CC·채널/상태·구성 제거 | UL Tx 구성·자원/잔여 상태 해제 | **LTE-TX-A3-REL** |

**기준 질문**: RRC 추가/해제, MAC ACT/DEACT, inactivity timer 만료 등 어떤 상위 이벤트가 ChCfg로 유입되는가? LTE ChCfg가 직접 어떤 메시지·상태를 소유하며 LTE Tx에는 무엇을 위임하는가? DL-only SCell이면 UL 경로는 `NOT_APPLICABLE`로 기록하고 별도의 UL activation 사건을 지어내지 않습니다.

### 9.2 LTE-CH-A9와 A3/A10 중복 방지

- **LTE-CH-A3**: RRC Connection Reconfiguration이 시작한 전체 L1 Configuration Procedure.
- **LTE-CH-A9**: PCell·Serving Cell·CC 구성을 갱신하는 **공통 세부 기술/하위 시나리오**가 독립적으로 관리할 가치가 있는지 검토하는 *후보*. 실코드가 A3/A10과 100% 중복이면 A9를 `MERGE_TO_A3_OR_A10`으로 보류하고 B1/B3로 흡수.
- **LTE-CH-A10**: SCell 상태/구성 변화 4단계의 대표 MSC와 Tx 하위 참여.

## 10. LTE Channel Config — B. Technical Knowledge

| ID | 기술 대분류 | 분석 후보 및 제외 조건 |
|---|---|---|
| **LTE-CH-B1** | LTE Channel Configuration | DL/UL 채널 설정, RRC에서 전달한 DL/UL 파라미터, SCell Add/Modify/Release, PCell/CC 재설정 (**NR BWP 제외**) |
| **LTE-CH-B2** | PBCH / MIB / LTE SI 처리 연동 | PBCH/MIB, LTE SIB 수신·Decoding을 위한 L1 채널 제어/정보 전달. RRC SI 해석과 구별 |
| **LTE-CH-B3** | Serving Cell / CC / Channel Resource | PCell/SCell 식별·DL/UL CC, LTE bandwidth/CC/resource mapping, 적용 시점 |
| **LTE-CH-B4** | Interface / Inter-controller | RRC/MAC ↔ LTE ChCfg, ChCfg ↔ LTE Tx, Measure/DRX Controller, RF/HAL/PHY IPC |
| **LTE-CH-B5** | State Management | Configured/Activated/Deactivated/Released, pending/duplicate, PCell과 SCell 구별, 여러 CC 상태 |
| **LTE-CH-B6** | Timing / Scheduling 연동 | RRC config 적용 시점, MAC ACT/DEACT 반영 타이밍, LTE 채널/CC 적용·재조정 경계; 스케줄러 자체 소유권 검증 |
| **LTE-CH-B7** | Recovery / Diagnostics | 재설정 실패, 상태 불일치, Release/Deactivation 충돌, 진단/영수증 기반 원인 추적 |

## 11. LTE L1 Tx — A. Procedure / Scenario

> NR Tx의 **A1–A8/A10 분류 개념을 재사용**하지만 LTE 특성에 맞게 명칭·시나리오를 작성합니다. `LTE-TX-A9`는 NRDC 전용이므로 이번 LTE 항목에서 **미사용**합니다. Dual SIM은 **A10**으로 동일한 슬롯에 두어 Cross-RAT 추적을 쉽게 합니다.

| ID | 대표 LTE Procedure | LTE L1 Tx가 실제 분석할 후보 흐름 | 역할·경계 |
|---|---|---|---|
| **LTE-TX-A1** | Initial Access / Attach | LTE Initial RACH, PRACH 및 Msg3 UL 송신·자원 설정의 Tx 참여 구간 | `PARTICIPANT_SUBFLOW` |
| **LTE-TX-A2** | RRC Connection Reconfiguration | RRC/ChCfg 설정 변경 중 UL 송신 리소스/경로/RF Tx 설정 재적용 | `PARTICIPANT_SUBFLOW` |
| **LTE-TX-A3** | UL CA / SCell Procedure 참여 | LTE-CH-A10 네 단계의 UL Tx 설정·활성/비활성·자원 회수, UL CA 관련 RF Tx configuration | `PARTICIPANT_SUBFLOW` — SCell Procedure 주관 아님 |
| **LTE-TX-A4** | EN-DC (LTE 측) | LTE/NR 동시 송신 시 LTE Tx 자원 우선순위·공유·충돌·전환·복귀. 지원 구조에 따라 LTE/MN 인터페이스 확인 | `PARTICIPANT_SUBFLOW`, 37.340/사내 코드 소유권 확인 |
| **LTE-TX-A5** | Mobility / Handover | LTE cell change/HO 중 Tx config/path 정리·재적용, RACH/송신 재개 | `PARTICIPANT_SUBFLOW` |
| **LTE-TX-A6** | Connected Mode | UL 정상 송신, 송신 파라미터 변경, 조건부 Tx Antenna/Path Switching | `PARTICIPANT_SUBFLOW` |
| **LTE-TX-A7** | **CDRX 연동** | CDRX로 인한 Tx 중지/허용/재개에 대한 LTE Tx 내부 처리 | DRX Controller의 CDRX state machine 제외; **Idle DRX 항목 생성 금지** |
| **LTE-TX-A8** | Exception / Recovery | RF/BB Tx 설정 실패, 스택·리소스 경합, 중복 활성화/해제, rollback/복귀 | Tx 소유 구간만 |
| **LTE-TX-A10** | **Dual SIM** | **Tx Sharing, BB Tx Change**: LTE/NR peer와 공유하는 Tx 자원·우선순위·경쟁·전환·복귀 | `PARTICIPANT_SUBFLOW`; 공통 Tx Manager 소유권 검증 |

### 11.1 LTE-TX-A3 — LTE ChCfg SCell 4단계 참여

| 세부 ID | LTE ChCfg의 주관 단계 | LTE L1 Tx 분석 하위 구간 | 확인할 기술 |
|---|---|---|---|
| **LTE-TX-A3-CFG** | LTE-CH-A10-CFG | ChCfg/공통 Tx 제어에서 UL SCell config 수신 → RF/BB/UL resource 설정 → HAL/PHY | LTE-TX-B3/B5/B6 |
| **LTE-TX-A3-ACT** | LTE-CH-A10-ACT | UL 송신 경로 enable/승인 상태·자원 점검 → 완료/오류 경계 | LTE-TX-B3/B4/B7 (switching **조건부**) |
| **LTE-TX-A3-DEACT** | LTE-CH-A10-DEACT | UL 송신 중지·경로/자원 보존 또는 회수 → 결과 경계 | LTE-TX-B3/B7 |
| **LTE-TX-A3-REL** | LTE-CH-A10-REL | UL SCell Tx resource/config 해제·잔여 상태 정리 | LTE-TX-B3/B5/B7 |

### 11.2 LTE L1 Tx의 추가 대표 항목 (지원 여부 검토)

| 후보 세부 ID | 분석 목적 | 현재 판정 |
|---|---|---|
| **LTE-TX-A3-ULCA-RFTX** | LTE UL CA 시 RF Tx Config/CC·band/resource·HAL 적용 순서 및 에러 | `CODE_TO_VERIFY` |
| **LTE-TX-A3-SLO** | LTE UL CA에서 사내 `SLO` 개념이 재사용되는지, 실제 기능·타이밍·구성·제약이 있는지 | **NR에서 존재해도 LTE 자동 적용 금지** `CODE_TO_VERIFY` |
| **LTE-TX-A6-ULSW** | LTE에서 UL Tx Switching/Tx Antenna 또는 Tx Path 전환이 존재하는지, 트리거·자원 경계 | `CODE_TO_VERIFY` |
| **LTE-TX-A6-SRSCS** | LTE SRS Carrier Switching 지원 여부와 SRS 설정·carrier 변경·송신/복귀 관계 | `CODE_TO_VERIFY`; 미지원이면 `NOT_APPLICABLE` |
| **LTE-TX-A10-SHARING** | Dual SIM Tx Sharing과 peer/stack/domain 우선순위, 충돌·회수·재개 | `CONFIRMED_CONCEPT_FROM_USER`, 세부 코드 `TO_VERIFY` |
| **LTE-TX-A10-BBTX-CHG** | Dual SIM BB Tx Change의 진입 조건·모드·원복·RF/BB 영향 | `CONFIRMED_CONCEPT_FROM_USER`, 세부 코드 `TO_VERIFY` |

**NRDC BB TX Reconfig / F1 Rank Change를 LTE Tx에 동일 항목으로 추가하지 않습니다.** 해당 기능이 실제 LTE 코드에 존재하거나 교차 RAT 공통 관리자의 코드 경로로 확인되는 경우에만 **참여 링크**를 추가하도록 사내 GPT에 요청합니다.

## 12. LTE L1 Tx — B. Technical Knowledge

| ID | 기술 대분류 | 분석 후보 |
|---|---|---|
| **LTE-TX-B1** | UL Physical Channel | LTE PUSCH/PUCCH/PRACH의 Tx 측 설정·송신 제어·결과 경계 |
| **LTE-TX-B2** | Reference Signal / SRS | LTE SRS configuration/trigger/송신, carrier switching 지원 여부(미확인) |
| **LTE-TX-B3** | Tx Resource | LTE Tx Antenna, BB/RF Tx Chain, UL CC/resource, LTE/NR peer 간 공유·매핑 |
| **LTE-TX-B4** | Tx Switching / Sharing | LTE Tx Antenna/Path Switching, UL Tx Switching(존재 시), Dual SIM Tx Sharing, EN-DC 공유·전환 분기 |
| **LTE-TX-B5** | Tx Configuration | LTE UL CA, RF Tx Config, BB Tx Change, LTE 송신 파라미터·Power Control 관련 L1 경계, SLO 지원 여부 검증 |
| **LTE-TX-B6** | Interface | LTE ChCfg↔LTE Tx, TxCfg/TxCmd(실제 소유권 확인), HAL/RF/PHY IPC, NR Tx/공통 Tx Manager 간 협업 |
| **LTE-TX-B7** | State Management | LTE PCell/SCell Tx 상태, 경로·sharing·BB Tx change의 state/동시성/복귀/해제 |

## 13. 4개 모듈의 Procedure ↔ Tx 참여 ↔ 기술 매핑

| 상위 시나리오 | Channel Procedure 주관 | Tx 하위 참여 | B 축 연결 | 설계 상태 |
|---|---|---|---|---|
| NR SCell CFG/ACT/DEACT/REL | `BCH-A10-*` | `TX-A3-*` | BCH-B1/B3/B5, TX-B3/B4/B5 | 사용자 소유권 확인 / 코드 검증 전 |
| LTE SCell CFG/ACT/DEACT/REL | `LTE-CH-A10-*` | `LTE-TX-A3-*` | LTE-CH-B1/B3/B5, LTE-TX-B3/B4/B5 | LTE 대응 역할 사용자 확인 / 코드 검증 전 |
| NR BWP Switching | `BCH-A9` | `TX-A2/A3` 필요 시 | BCH-B1/B5, TX-B5 | **NR 전용** |
| LTE PCell/CC Reconfiguration | `LTE-CH-A3/A9` | `LTE-TX-A2` 필요 시 | LTE-CH-B1/B3, LTE-TX-B5 | **LTE 전용**; NR BWP와 다른 항목 |
| NR EN-DC | `BCH` 연동 구간만 | `TX-A4` | TX-B3/B4/B6/B7 | 구현 분담 검증 |
| LTE EN-DC | `LTE-CH-A11`(관여 시) | `LTE-TX-A4` | LTE-TX-B3/B4/B6/B7 | LTE 측 Master/Cell Group 범위 확인 |
| NRDC | Channel 연동 시 인터페이스 | `TX-A9` (BB TX Reconfig/F1 Rank) | TX-B5/B6/B7 | **LTE에 무조건 확장 금지** |
| NR Dual SIM | BCH는 해당 시 연동만 | `TX-A10` | TX-B3/B4/B5/B7 | Tx Sharing/BB Tx Change |
| LTE Dual SIM | LTE ChCfg는 해당 시 연동만 | `LTE-TX-A10` | LTE-TX-B3/B4/B5/B7 | Tx Sharing/BB Tx Change |
| NR/LTE CDRX 연동 | Channel 측은 필요 시 인터페이스 | `TX-A7`, `LTE-TX-A7` | B4/B7 또는 대응 interface | 실제 DRX 기능 소유는 DRX Controller |

**One-source rule:** SCell Procedure 전체 MSC는 각 RAT의 Channel Controller에 두고, Tx MSC는 참가 흐름의 세부 subflow만 작성하도록 *향후 실제 분석 단계*에서 요구합니다. 실제 코드 분석 전에는 이 링크를 확정된 호출 사실로 주장하지 않습니다.

## 14. 사내 GPT 1차 검토 프롬프트 — 4개 모듈 통합 (실행 요청 아님)

> **문서 전체를 입력으로 제공**하고 다음 작업을 수행해 주세요. 이전 v0.5의 NR 전용 지침을 포함하는 **최신 통합 프롬프트**입니다.

### 작업 목적

`NR BCH_CTRLR(=NR L1 Channel)`, `NR L1 Tx`, `LTE ChCfg(=LTE L1 Channel Config)`, `LTE L1 Tx`의 Knowledge 후보 항목을 **A. Procedure/Scenario + B. Technical Knowledge** 두 관점에서 검토합니다. 목표는 실제 소스 전체 분석이나 그룹 지식 업데이트가 아니라, **향후 `l1-knowledge-updater`에게 무엇을 분석시키고 어떤 MSC/Code Facts를 받아야 하는지**를 선정하는 것입니다.

### 필수 검토 내용

1. **분류 완전성**: RAT별 Attach/SI/RRC/CA(SCell 4단계)/Mobility/Connected Mode/EN-DC/Release/Recovery/Dual SIM에 대해 누락·불필요·중복 분석 아이템을 제시합니다.
2. **책임 경계**: NR BCH와 LTE ChCfg는 각 RAT의 Channel Procedure 주관, Tx는 UL Tx 하위 참여자로 구분합니다. Search/Measure·Idle DRX/CDRX 본체는 소유 모듈에서 제외하고 관련 인터페이스만 확인합니다. Paging 독립 항목은 재등록하지 않습니다.
3. **3GPP vs 구현**: TS 38.331/38.321, TS 36.331/36.321 및 37.340의 동작을 참고하되 **규격의 Layer RRC/MAC 동작이 사내 Channel/Tx 코드 소유권을 직접 증명한다는 결론 금지**.
4. **SCell 상세 분류**: LTE-CH-A10↔LTE-TX-A3 및 BCH-A10↔TX-A3 각각 CFG/ACT/DEACT/REL 1:1 대응. DL/UL 구현 영향 구간을 분리하고 실제 별도 MAC 이벤트라고 추정하지 않습니다.
5. **차이점 식별**: LTE와 NR에서 동일한 개념, 다른 구현, RAT 전용 기능 구분. **NR BWP는 LTE에 넣지 않고, NRDC F1 Rank Change를 LTE 항목으로 복사하지 않습니다**. LTE ChCfg A9와 A3/A10의 중복 가능성 판정.
6. **Tx 기술 목록**: NR UL Tx Switching/SRS Carrier Switching/Tx Antenna·Path Switching, NRDC BB TX Reconfig·F1 Rank Change, ULCA SLO·RF Tx Config, NR/LTE Dual SIM Tx Sharing·BB Tx Change. LTE에서는 해당 기술이 실제 지원되는지 먼저 판정하도록 `CODE_TO_VERIFY`로 구분합니다.
7. **향후 분석 요구사항**: 항목별 `Entry Event`, `Exit Boundary`, `Trigger`, `Message/IPC`, `State/Guard`, `Normal/Failure`, `Role`, `Evidence Required`, `MSC Required`, `Link To Other Module`을 표로 설계합니다. 실제 파일/함수명·코드 라인을 만들지 않습니다.
8. **중복 최소화**: 동일 흐름은 Procedure Overview/MSC → Tx subflow → 공통 기술 문서 링크로 재사용, 4개 모듈 범위 밖 코드는 인터페이스 확인에 필요한 최소 구간만 기술합니다.
9. **실행하지 말 것**: 실제 `l1-knowledge-updater`/`code-analyzer`/`doc-converter` 호출, Job-list/Runner/Worker 활성화, 소스·Knowledge·Work·DB 수정, GitHub 외부 게시/승인 변경, 임의 OpenCode 에이전트 실행 및 사내 데이터 반출 금지.

### 출력 형식 (가급적 한 번에, 숫자로 피드백 가능하게)

| 출력 번호 | 내용 | 필수 요소 |
|---|---|---|
| 1 | RAT×모듈별 A/B 분류표 | 안정 ID, 적절/수정/제외/추가, 이유 |
| 2 | 소유권/의존성/호출 관계 후보 | `LEAD_L1_PROCEDURE`, `PARTICIPANT_SUBFLOW`, `INTERFACE_ONLY`, `OTHER_MODULE_OWNED`, `TO_VERIFY` |
| 3 | 4개 모듈의 SCell 절차 매핑 | 실제로는 NR Channel+Tx, LTE Channel+Tx 2쌍 × 4단계 |
| 4 | NR-LTE 차이점 표 | BWP, LTE PCell/CC, EN-DC, NRDC, UL CA, SRS Carrier Switching, Dual SIM |
| 5 | 누락·중복·우선순위 검토 | P0/P1/P2 제안, 전제/차단 표시 |
| 6 | 후속 분석 입력 계약 | Code Facts, 대표 MSC, Overview, 소스 고정, 예외 경로, 재사용 링크 |
| 7 | **사용자 선별 숫자 요약** | `[번호] [기존ID] [선택안 1=유지, 2=수정, 3=제외, 4=보류]`로 응답 가능하게 |

### 상태 표기

- `CONFIRMED_FROM_USER`: 사용자 직접 확인한 담당 책임·업무 개념
- `SPEC_CONTEXT`: 3GPP에서 확인 가능한 규격 절차
- `CODE_TO_VERIFY`: 실제 사내 구현에서 확인할 함수/메시지/분기/지원 여부
- `NOT_APPLICABLE`: RAT/제품 미지원으로 코드 근거가 있을 때만 확정
- `PROPOSED`: 분류 설계자 제안 (사내 GPT/사용자 승인 전)

**완료 조건:** 네 모듈의 분석 대상 후보 목록이 누락·중복·소유권 관점에서 검토되고 사용자가 간결한 숫자 피드백으로 선별할 수 있으면 1차 완료. 실제 기술 지식 생성과 스킬 업데이트는 이후 별도 단계입니다.

## 15. 3GPP 교차 확인 (프로토콜 참조; 구현 책임 증명 아님)

| 규격 | 기술적 근거 | 대상 및 주의 |
|---|---|---|
| TS 38.331 / TS 38.321 | NR RRC의 SCell 구성/해제와 MAC의 SCell 활성화/비활성화 | BCH-A10 및 TX-A3의 절차 맥락; NR 소유권은 사용자 확인 |
| TS 38.214 | UL switching, SRS carrier switching의 물리계층 관련 동작 | NR TX-B2/B4 후보, 실제 코드 지원 여부 별도 |
| **TS 36.331** | LTE RRCConnectionReconfiguration의 SCell 추가/변경/해제 | LTE-CH-A3/A10; RRC vs L1 ChCfg 구분 |
| **TS 36.321 §5.13** | LTE MAC SCell Activation/Deactivation, deactivation timer, lower-layer 영향 | LTE-CH-A10 ACT/DEACT 및 LTE-TX-A3 UL 영향 구분 |
| **TS 37.340** | MR-DC/EN-DC에서 LTE/NR Cell Group 및 Node 역할 | TX-A4, LTE-TX-A4, LTE-CH-A11; 모델별 구현 확인 |

**공개 참조 URL**

- NR RRC TS 38.331: https://www.etsi.org/deliver/etsi_ts/138300_138399/138331/17.14.00_60/ts_138331v171400p.pdf
- NR MAC TS 38.321: https://www.etsi.org/deliver/etsi_ts/138300_138399/138321/18.04.00_60/ts_138321v180400p.pdf
- NR PHY TS 38.214: https://www.etsi.org/deliver/etsi_ts/138200_138299/138214/18.06.00_60/ts_138214v180600p.pdf
- **LTE RRC TS 36.331:** https://www.etsi.org/deliver/etsi_TS/136300_136399/136331/17.11.00_60/ts_136331v171100p.pdf
- **LTE MAC TS 36.321:** https://www.etsi.org/deliver/etsi_ts/136300_136399/136321/17.05.00_60/ts_136321v170500p.pdf
- **MR-DC TS 37.340:** https://atisorg.s3.amazonaws.com/archive/3gpp-documents/Rel16/ATIS.3GPP.37.340.V1620.pdf

## 16. 현재 상태와 다음 한 동작

| 단계 | 현재 판정 |
|---|---|
| NR Channel/Tx v0.5 구분·책임 보존 | `PASS` (문서 수준, 코드 검증과 별개) |
| LTE ChCfg + LTE L1 Tx 대분류 신규 작성 | `PREPARED_FOR_REVIEW` |
| LTE SCell Procedure–Tx subflow 매핑 | `PROPOSED` (소유권 개념 사용자 정보 기반, 세부 코드 검증 전) |
| 사내 GPT 1차 리뷰 | `NOT_RUN` |
| 실제 LTE/NR 소스 분석 / `l1-knowledge-updater` / MSC 렌더 | `NOT_RUN` |
| 지식 정본 갱신 / 스킬 수정 / 배포 / Job 실행 | `NOT_RUN` |
| 독립 Claude Code 리뷰 | `NOT_RUN` (현재 단계 요청 범위 밖) |

**다음 한 동작:** 사내 GPT에 **이 v0.6 문서 전체**를 제공하고 **14절의 프롬프트**로 A/B 분류, 모듈 책임, LTE/NR 차이, 누락/중복을 1차 검토합니다. 피드백은 번호 중심으로 받은 뒤 사용자/GPT가 선별하고, 그 다음에만 `l1-knowledge-updater`용 실제 분석 Job을 분할·승인합니다.
