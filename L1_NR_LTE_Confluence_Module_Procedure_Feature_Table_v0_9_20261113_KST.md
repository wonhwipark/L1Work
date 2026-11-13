# L1 NR/LTE Confluence Procedure / Feature 분류표 v0.9

- 작성 기준일: **2026-11-13 KST**
- 개정 상태: **DESIGN_REVISED / OWNER_REVIEW_PENDING**
- 용도: 담당자 검토·Confluence 정리·향후 지식 분석 항목 선정
- 적용 모듈: **NR BCH(= NR L1 Channel Controller), NR L1 Tx, LTE ChCfg, LTE L1 Tx**
- 기준 입력: 첨부 Confluence v0.8, 담당자 검토용 v0.7, 담당 모듈 범위 공통 문서 r0001, K5.8/K6 연계 계약 r0005, 별도 관점 GPT 문서 리뷰
- 문서 검토 기준 revision: `7e0bc505cc4adb3f39fb1c1a7d4391a651b4cf48` — 실제 제품 코드 revision이 아님
- 이번 변경: 분류·조건·참조·검토 상태를 반영한 문서 개정. 기존 181개 항목의 계보 유지 + 신규 확인 후보 34개
- 실행 상태: **코드 분석·스킬 실행·지식/메타데이터 갱신·설치/배포 미수행**

> 담당 범위에 관한 사용자 확인과 개별 행의 지원·구현 확인은 서로 다른 상태임. 본 표의 항목은 담당자 검토 후보이며, 기능 구현·표준 적합성·누락 없음의 확정 목록이 아님. `적절` 판정과 문서 작성 완료만으로 현재 코드 사실 또는 updater 정본으로 승격하지 않음.

## 1. 개정 요점과 사용 순서

1. Procedure를 표준 절차 연계 흐름·운용 맥락·로컬 동작으로 구분하고, Feature와 공통 설명 관점을 분리.
2. 기존 **Module → Feature → Scenario**를 유지하며 Procedure를 교차 탐색 뷰로 사용. 같은 기능·시나리오의 복제 정본 생성 방지.
3. SCell의 표준 이벤트와 DL/UL 처리 구간, Channel 주관과 Tx 하위 참여, 조건부 비실행을 구분.
4. 초기 설정/재수립, DC 구성 수명주기, 부분 실패·Release 경합 등 누락 확인 후보 34개 추가.
5. Confluence **Module / Owner / Progress / Update source or contents** 4열 유지. 담당자 검토와 작성 진척을 분리.
6. 담당자는 먼저 범위·분류·포함 여부를 판정하고, 선정 항목의 실제 코드·기존 ID·근거를 후속 확인. 본 문서가 분석 실행 지시나 정본 갱신 승인을 대신하지 않음.

### 1.1 분류 범례

| 표기 | 의미 | 판단 기준·주의 |
|---|---|---|
| **STD-RRC** | RRC 표준 절차에 연계된 L1 처리 후보 | 상위 절차·관련 규격을 식별. 이 표의 로컬 제목이 규격의 독립 절차명이라는 뜻은 아님 |
| **STD-MAC** | MAC 표준 동작에 연계된 L1 처리 후보 | Random Access·SCell 활성/비활성·BWP 연동 등. MAC/PHY 정책·실행 전체를 해당 L1 모듈에 귀속하지 않음 |
| **CONTEXT** | 운용 맥락에서의 구체적 처리 후보 | UL CA·EN-DC·NR-DC·Dual SIM은 조건/맥락. 해당 맥락 안의 트리거·상태·처리를 기술 |
| **LOCAL** | 구현 이벤트·하위 처리·복구 흐름 후보 | 표준과 구별되는 내부 요청·처리 순서·오류 대응. 실제 코드 확인 필요 |
| **FEATURE** | 재사용 기능 또는 기능 상세 범위 후보 | 기존 Feature에 먼저 매핑. 표의 세부 행마다 신규 Feature를 만들지 않음 |
| **ASPECT** | Interface·State·Timing·Diagnostics 등의 설명 관점 | 관련 기존 Feature의 설명 절에 연결. 별도 Feature 귀속 여부는 기존 구조 확인 후 결정 |
| **VERIFY** | 정의·지원·소유권·적용 조건 확인을 우선할 항목 | 표준/로컬/기능 분류를 확정하지 않은 후보. 확인 후 적절한 기존 분류에 연결 |

`P`는 Procedure/동작 시나리오 검토 뷰, `F`는 Feature/공통 기술 검토 뷰를 의미. `VERIFY` 표기도 원래 P/F 뷰 위치를 유지하며 판정을 대기.

### 1.2 모듈 범위와 제외 경계

| 모듈 | 사용자 확인 담당 범위 | 항목별 추가 확인·경계 |
|---|---|---|
| **NR BCH** | PBCH 전용이 아닌 NR L1 Channel Controller. SCell 관련 L1 채널 처리 주관 | RRC/MAC의 표준 절차 전체 소유권과 구별. Search/Measurement·DRX 본체는 외부 소유, 필요한 입력·연동만 포함 |
| **LTE ChCfg** | LTE L1 Channel Configuration Controller | LTE 실제 구현·지원 조건 확인. NR BWP/CORESET 등을 자동 전용하지 않음 |
| **NR L1 Tx** | UL 송신 설정·Tx resource·switching. Channel 절차에 Tx 하위 참여 | 모든 SCell 이벤트에 Tx 처리·Switching이 있는 것으로 가정하지 않음 |
| **LTE L1 Tx** | LTE UL 송신·Tx path/resource·SCell의 Tx 하위 참여 | NR과 공통 분석 틀 사용, 기능 지원·조건·구현 동일성은 별도 확인 |

- DRX는 Tx 연동·채널 설정 인터페이스까지만 후보. Idle DRX/CDRX 상태머신 및 Paging 독립 시나리오는 제외.
- 안테나 선택·Power·SAR/TAS·RF 등 별도 모듈의 알고리즘 소유권은 별도 확인. 이 표의 관련 후보는 담당 Tx가 소비하는 입력·제약·설정·결과 경계를 우선 검토.
- NAS Attach/Registration은 초기 접근의 상위 맥락. 본 표의 L1 절차명으로 사용하지 않음.
- 새 후보 추가는 사용자 담당 범위 또는 실제 코드 소유권의 확장 확정이 아님.

## 2. 기존 지식 구조와 연결 정책

**정본 탐색 구조는 Module → Feature → Scenario를 유지.** Procedure와 운용 맥락은 여러 Feature/Scenario를 찾아가는 뷰로 사용. 표의 P/F 항목 수는 실제 지식 문서·Feature·Scenario 수와 일치하지 않을 수 있음.

### 2.1 문서 검토 ID와 실제 ID

- `NB/NT/LC/LT-Pnn/Fnn`은 **이 문서의 검토행 ID**. 실제 Module·knowledge·Feature·Scenario·Work·MSC participant ID로 등록하거나 대체하지 않음.
- `NB`=NR BCH, `NT`=NR L1 Tx, `LC`=LTE ChCfg, `LT`=LTE L1 Tx.
- v0.8의 각 모듈·뷰별 세부 항목 출현 순서를 1번부터 유지. 제목·분류 수정 뒤에도 원래 행 ID 유지. 신규 후보는 기존 마지막 번호 뒤에 추가.
- 실제 설치본의 Module/Feature/Scenario ID 및 저장 계약은 **미확인**. 동일 제목·경로·브랜치명만으로 동일 ID라고 판단하지 않음.
- 표의 연결은 문서 내 검토 참조. 실제 기존 지식의 ID/section/revision 참조는 후속 확인 후 매핑. 링크는 해당 검토표로 이동하며 행 ID로 세부 항목을 식별.

### 2.2 기준 본문·중복 방지 규칙

| 상황 | 기준 본문 및 연결 정책 |
|---|---|
| 하나의 기능이 CA/DC/Dual SIM에서 사용됨 | 공통 기능 설명은 기존 Feature의 기준 본문에 유지. 맥락별 Scenario에는 트리거·조건·차이·결과만 기록 |
| 하나의 Procedure가 Channel과 Tx를 거침 | 모듈별 적용 구간·상태를 각각 유지하고 상위 흐름으로 연결. 모듈별 다른 상태·조건을 하나의 동일 Scenario로 강제 병합하지 않음 |
| SRS Carrier Switching이 SRS와 Switching에 중복 노출 | 이 문서의 기준 분석행은 NT-F12. NT-F04는 조건 설명 참조, NT-P10은 맥락별 흐름. 실제 기존 Feature 귀속은 후속 확인 |
| Interface/State/Timing/Recovery가 여러 기능에 관련됨 | 관련 기존 Feature의 절·공통 설명을 참조. 뷰 제목을 신규 독립 Feature로 자동 생성하지 않음 |
| TxCfgMngr/TxSwitchMngr 설명이 NR/LTE에 등장 | 공통 소스·기존 지식이 확인되면 기준 설명 재사용. RAT별 입력·조건·자원 차이는 variant/관련 Scenario로 보존 |
| 상세 채널 항목을 신규 후보로 추가함 | NB-F22/F23, LC-F21/F22 등은 기존 포괄 설정 항목의 검토 상세화. 기존 기능 절로 연결할 수 있으면 신규 Feature 생성 불필요 |
| 같은 행처럼 보이지만 제품/Release/build/소스가 다름 | 적용 범위·근거를 비교한 뒤 동등성 판단. 무조건 합치거나 한쪽의 검증을 다른 쪽에 승계하지 않음 |

### 2.3 정본 편입 전 확인표 — 논리 설계만

| 확인 대상 | 필요한 의미 | 현재 상태 |
|---|---|---|
| 기존 귀속 | 실제 Module·Feature·Scenario 또는 설명 절·기준 본문 | **ID 매핑 대기** |
| 적용 범위 | RAT·제품·Release·build 조건·소스 계열 | **개별 항목 미확인** |
| 근거 | 분석 입력의 고정 source revision·코드 anchor·검증 방식·한계 | **코드 확인 미수행** |
| 지식 종류·상태 | AS-IS/설계 의도/가설, 구현·시험·현재성·게시 상태 구분 | **후보 상태만 부여** |
| 변경·게시 | 기존 writer/승인/충돌 방지/readback 계약과 실제 허용 범위 | **미실행** |

위 항목은 기존 계약을 확인하기 위한 목록. 신규 metadata·schema·sidecar·엔진·원장·실행 enum을 정의하지 않음. 기존 필드·참조로 매핑할 수 없다는 실제 gap 확인 전 확장 확정 금지.

**B-01 상태: 연결 정책은 문서에 반영했으나 실제 기존 ID·본문 대조는 미수행. updater 정본 편입은 계속 보류.** 담당자 검토와 문서 작성은 진행 가능.

## 3. Confluence 4열 작성 규칙

| 열 | 기록 의미 | 초기값·운영 방식 |
|---|---|---|
| Module | 검토 ID·모듈·유형·대분류·구체적 항목 | 개별 행을 복사해도 모듈과 유형을 식별할 수 있게 표시 |
| Owner | 작성 담당과 검토 담당 | `작성 미정 · 검토 미정`; 실제 이름은 담당자 합의 후 입력. 코드 소유권·MSC participant와 동일시하지 않음 |
| Progress | 담당자 검토와 문서 작성 진척 | `검토 미검토 · 작성 미착수`; 두 상태를 따로 관리 |
| Update source or contents | 범위·관련 행·조건·근거와 확인 결과 | 초기에는 후보/미확인. 실제 기존 지식·코드 근거는 인가된 환경에서 확인 후 해당 기존 계약에 연결 |

- 검토 상태: `미검토 / 적절 / 누락 / 변경 / 제외`. `누락`은 보완할 내용·추가 행을 설명하고, `변경`은 수정 대상·이유, `제외`는 범위·지원 근거를 함께 기록.
- 작성 상태: `미착수 / 작성 중 / 초안 / 검토 요청 / 작성 완료`를 예시로 사용. 현재 스킬 enum이나 자동 실행 상태 정의가 아님.
- 사실 상태: 초기에는 모두 `구현·지원 미확인`. 코드 근거 확인·런타임 관측·설계 승인·게시 여부는 실제 증거별로 독립 기재. 작성 완료 또는 적절 판정으로 구현 확인을 대체하지 않음.
- 아래 8개 검토표만 필요 범위에서 복사해 사용할 수 있음. 4열 외의 설명표는 문서 범례·검토 보조 자료.

## 4. SCell·BWP·DC 조건

### 4.1 SCell 이벤트와 DL/UL 적용 구간

| 이벤트 | 표준/상위 맥락 | Channel 측 검토 | Tx 측 검토 |
|---|---|---|---|
| 구성·변경 | RRC 구성 적용 | DL과, 구성된 경우 UL 설정 반영 | UL이 구성되고 Tx 변경이 필요한 경우 하위 적용 |
| Activation | MAC 동작 및 적용 Release의 초기 활성 구성 예외 | 동일 SCell 이벤트의 상태·DL 적용 구간 | UL 구성·타이밍·자원 조건에 따른 하위 처리; Switching 필수 아님 |
| Deactivation | MAC CE·타이머 등 적용 조건 | 상태·송수신 동작 제한·잔여 처리 | UL 관련 중지·보존·자원 처리는 실제 구현 확인 |
| Release | RRC 구성 해제 | 구성·자원·대기 요청 정리 | 해당 UL 자원이 있을 때 정리·정산 |

DL/UL 8행은 **4종 이벤트의 영향 구간을 나눈 검토행**. 언제나 8개의 독립 표준 이벤트라는 의미가 아님. MAC CE와 RRC 초기 상태·타이머·dormancy 예외는 적용 Release와 제품에서 재확인.

### 4.2 BWP·DC 조건

- RRC의 BWP 구성 추가·변경과 활성 BWP 전환을 구별. DCI·타이머 등 트리거별 DL/UL·duplex 조건 확인.
- bwp-InactivityTimer 관련 복귀는 DL BWP 기준으로 검토. UL 영향·동시 전환은 적용 조건을 확인해 별도 표시. RRC/DCI/Timer 모두가 항상 BCH의 동일 경로를 거친다고 가정하지 않음.
- EN-DC·NR-DC는 운용 맥락. SCG 추가·변경·해제, PSCell 변경 등 실제 이벤트에서의 Channel/Tx 참여를 확인. 동시 송신·자원 공유는 일부 조건부 시나리오.
- SLO·F1 의미는 담당자/사내 정의 확인 전 미확인 유지. F1을 다른 표준 용어로 추정하여 치환하지 않음.

## 5. 담당자 검토표

각 행의 지원·구현·실제 기존 ID는 아직 미확인. `신규 후보`는 누락이 확정됐다는 뜻이 아니라 포함/제외를 판단할 추가 질문.

### NB-P

**NR BCH — Procedure / 동작 시나리오 / 35개 검토행**

| Module | Owner | Progress | Update source or contents |
|---|---|---|---|
| **NB-P01 · NR BCH** · [STD-RRC] Initial Access / L1 초기 설정 — 동기 획득 결과를 입력받은 뒤 PBCH/MIB 수신 설정·결과를 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F04](#nb-f), [NB-F10](#nb-f); 규격 연결: S1 §5.2; Search/동기 획득 알고리즘은 Measure 소유; BCH의 입력·설정 경계 확인; 사실: 미확인 |
| **NB-P02 · NR BCH** · [STD-RRC] Initial Access / L1 초기 설정 — 초기 접근 시작 시 DL/UL 공통 채널 설정을 준비·적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F01](#nb-f), [NB-F02](#nb-f), [NB-P29](#nb-p); 규격 연결: S1 §5.2·5.3.3; NAS Attach/Registration은 상위 맥락; RRC Setup 적용은 NB-P29로 구체화; 사실: 미확인 |
| **NB-P03 · NR BCH** · [STD-RRC] System Information Acquisition — SIB1 획득 요청에 따른 수신·복호용 L1 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F05](#nb-f); 규격 연결: S1 §5.2; 실제 복호 알고리즘 소유권과 BCH 설정·결과 연동을 구분; 사실: 미확인 |
| **NB-P04 · NR BCH** · [STD-RRC] System Information Acquisition — 기타 SIB/SI 획득 요청·변경 통보에 따른 수신 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F05](#nb-f); 규격 연결: S1 §5.2; 대상 SIB·스케줄링 입력·담당 범위 확인; 사실: 미확인 |
| **NB-P05 · NR BCH** · [STD-RRC] System Information Acquisition — SI 유효성 변경·재획득 요청에 따른 채널 설정 갱신 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F05](#nb-f), [NB-F20](#nb-f); 규격 연결: S1 §5.2; 최초 획득·갱신·실패 재획득의 조건을 구별; 사실: 미확인 |
| **NB-P06 · NR BCH** · [STD-RRC] RRC Reconfiguration — RRC Reconfiguration 수신 시 DL 채널 설정을 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F01](#nb-f), [NB-F02](#nb-f), [NB-F22](#nb-f), [NB-F23](#nb-f); 규격 연결: S1 §5.3.5; SCell/BWP 세부 흐름은 관련 행으로 연결; 전체 설정 설명 복제 방지; 사실: 미확인 |
| **NB-P07 · NR BCH** · [STD-RRC] RRC Reconfiguration — RRC Reconfiguration 수신 시 UL 채널 설정을 적용·Tx에 연계 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F02](#nb-f), [NT-P03](#nt-p), [NT-F19](#nt-f); 규격 연결: S1 §5.3.5; L1 Channel 주관과 Tx 하위 참여 구분; 사실: 미확인 |
| **NB-P08 · NR BCH** · [STD-RRC] RRC Reconfiguration — 재구성 시 채널 자원 변경의 적용 순서·완료 조건을 처리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F03](#nb-f), [NB-F18](#nb-f), [NB-P34](#nb-p); 규격 연결: S1 §5.3.5; 일반 재구성 흐름; SCell·BWP는 세부 시나리오 참조; 사실: 미확인 |
| **NB-P09 · NR BCH** · [STD-RRC] Mobility / Handover — Handover 관련 요청 시 Target Cell L1 설정을 준비·적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F03](#nb-f), [NB-F16](#nb-f), [NB-F25](#nb-f); 규격 연결: S1 §5.3.5; 상위 이동성 판단·절차 전체 대신 L1 적용 구간 분석; 사실: 미확인 |
| **NB-P10 · NR BCH** · [STD-RRC] Mobility / Handover — Handover 적용 후 채널 상태를 정합화·재설정 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F13](#nb-f), [NB-F19](#nb-f), [NB-P34](#nb-p); 규격 연결: S1 §5.3.5; 성공 이후 정합화와 실패 원복을 분리; 사실: 미확인 |
| **NB-P11 · NR BCH** · [STD-RRC] Cell Change 결과 연동 — Cell Reselection 결과 입력에 따른 채널 설정 변경 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F10](#nb-f), [NB-F04](#nb-f), [NB-F05](#nb-f); 규격 연결: S1 §5.2 연계; Selection/Reselection 판단은 외부 소유; 결과 입력 이후만 분석; 사실: 미확인 |
| **NB-P12 · NR BCH** · [LOCAL] Cell Change 결과 연동 — Cell Change 결과에 따른 L1 채널 자원 재초기화 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F07](#nb-f), [NB-F13](#nb-f), [NB-F19](#nb-f); 상위 Cell Change 유형과 기존 자원 유지·해제 조건 확인; 사실: 미확인 |
| **NB-P13 · NR BCH** · [STD-RRC] Release / Suspend / Resume — 정상 Release 요청 시 채널 자원을 해제·정리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F07](#nb-f), [NB-F13](#nb-f), [NB-P35](#nb-p); 규격 연결: S1 §5.3.8; 오류 복구와 정상 해제를 구별; 진행 중 요청 정산은 NB-P35; 사실: 미확인 |
| **NB-P14 · NR BCH** · [STD-RRC] Release / Suspend / Resume — Suspend/Resume 요청 시 채널 설정 보존·복원을 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F02](#nb-f), [NB-F13](#nb-f); 규격 연결: S1 §5.3.8·5.3.13; 지원 제품·Release·실제 저장/복원 범위 확인 필요; 사실: 미확인 |
| **NB-P15 · NR BCH** · [LOCAL] Exception / Recovery — 채널 설정 실패·Timeout 발생 시 오류를 분류·복구 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F19](#nb-f), [NB-P34](#nb-p), [NB-P35](#nb-p); 원복·해제·재시도는 실제 정책 확인; 자동 재시도 가정 금지; 사실: 미확인 |
| **NB-P16 · NR BCH** · [LOCAL] Exception / Recovery — MIB/SIB 획득 실패 통보에 따른 L1 복구 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F20](#nb-f), [NB-P01](#nb-p), [NB-P03](#nb-p), [NB-P05](#nb-p); 수신 실패 판단 주체와 BCH의 후속 처리 구분; 사실: 미확인 |
| **NB-P17 · NR BCH** · [STD-RRC] BWP 구성·전환 — RRC 기반 BWP 구성 변경과 명시된 활성 BWP 변경을 구별해 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F06](#nb-f), [NB-F15](#nb-f), [NB-F17](#nb-f); 규격 연결: S1 §5.3.5 / S2 §5.15; BWP 설정 추가·변경만으로 활성 BWP 전환이 항상 발생하지 않음; 사실: 미확인 |
| **NB-P18 · NR BCH** · [STD-MAC] BWP 구성·전환 — DCI 기반 활성 BWP 변경 결과에 따른 L1 설정·상태 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F06](#nb-f), [NB-F15](#nb-f), [NB-F17](#nb-f), [NT-P03](#nt-p); 규격 연결: S2 §5.15; DL/UL·duplex 조건 및 PHY/MAC/Channel 간 실제 처리 경계 확인; 매 DCI의 BCH 경유를 가정하지 않음; 사실: 미확인 |
| **NB-P19 · NR BCH** · [STD-MAC] BWP 구성·전환 — bwp-InactivityTimer 만료에 따른 DL BWP 복귀를 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F06](#nb-f), [NB-F15](#nb-f), [NB-F17](#nb-f); 규격 연결: S2 §5.15; 기본/초기 DL BWP 등 복귀 조건 확인; UL 동시 전환 여부는 적용 규격·구현 조건을 별도 확인; 사실: 미확인 |
| **NB-P20 · NR BCH** · [LOCAL] BWP 구성·전환 — BWP 변경 시 해당 DL/UL 채널 영향과 완료 조건을 반영 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-P17](#nb-p), [NB-P18](#nb-p), [NB-P19](#nb-p), [NB-F06](#nb-f), [NB-F17](#nb-f); 각 트리거의 공통 처리 절을 참조하는 행; 별도 표준 이벤트로 집계하지 않음; 사실: 미확인 |
| **NB-P21 · NR BCH** · [STD-RRC] SCell 구성·활성·비활성·해제 — SCell RRC 구성·변경 시 DL 채널 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F08](#nb-f), [NB-F14](#nb-f), [NB-F17](#nb-f); 규격 연결: S1 §5.3.5; 구성·변경의 DL 영향 구간; 별도 DL 셀 추가 절차로 해석하지 않음; 사실: 미확인 |
| **NB-P22 · NR BCH** · [STD-RRC] SCell 구성·활성·비활성·해제 — 동일 SCell 구성·변경의 UL 설정 적용·Tx 연계 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F08](#nb-f), [NB-F14](#nb-f), [NB-F17](#nb-f), [NB-P21](#nb-p), [NT-P05](#nt-p); 규격 연결: S1 §5.3.5; UL이 구성된 경우의 영향 구간; UL 미구성 시 비대상; 사실: 미확인 |
| **NB-P23 · NR BCH** · [STD-MAC] SCell 구성·활성·비활성·해제 — SCell Activation 시 DL 채널·상태 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F08](#nb-f), [NB-F14](#nb-f), [NB-F17](#nb-f); 규격 연결: S2 §5.9; SCell 단위 활성 이벤트; RRC 초기 활성 상태 등 예외도 적용 Release에서 확인; 사실: 미확인 |
| **NB-P24 · NR BCH** · [STD-MAC] SCell 구성·활성·비활성·해제 — 동일 SCell Activation의 UL Tx 처리 연계 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F08](#nb-f), [NB-F14](#nb-f), [NB-F17](#nb-f), [NB-P23](#nb-p), [NT-P06](#nt-p); 규격 연결: S2 §5.9; UL 구성·전송 가능 조건 확인; 활성화만으로 Tx Switching 필수 실행을 가정하지 않음; 사실: 미확인 |
| **NB-P25 · NR BCH** · [STD-MAC] SCell 구성·활성·비활성·해제 — SCell Deactivation 시 DL 채널·상태 반영 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F08](#nb-f), [NB-F14](#nb-f), [NB-F17](#nb-f); 규격 연결: S2 §5.9; MAC CE·비활성 타이머 등 트리거를 구분; 구성 해제와 별개; 사실: 미확인 |
| **NB-P26 · NR BCH** · [STD-MAC] SCell 구성·활성·비활성·해제 — 동일 SCell Deactivation의 UL Tx 중지·자원 처리 연계 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F08](#nb-f), [NB-F14](#nb-f), [NB-F17](#nb-f), [NB-P25](#nb-p), [NT-P07](#nt-p); 규격 연결: S2 §5.9; UL이 구성된 경우의 하위 처리; UL 독립 비활성 표준 이벤트로 명명하지 않음; 사실: 미확인 |
| **NB-P27 · NR BCH** · [STD-RRC] SCell 구성·활성·비활성·해제 — SCell RRC Release 시 DL 설정·자원 정리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F08](#nb-f), [NB-F14](#nb-f), [NB-F17](#nb-f); 규격 연결: S1 §5.3.5; 비활성 상태와 구성 해제를 구분; 사실: 미확인 |
| **NB-P28 · NR BCH** · [STD-RRC] SCell 구성·활성·비활성·해제 — 동일 SCell RRC Release의 UL Tx 자원 정리 연계 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [NB-F08](#nb-f), [NB-F14](#nb-f), [NB-F17](#nb-f), [NB-P27](#nb-p), [NT-P08](#nt-p); 규격 연결: S1 §5.3.5; UL 구성 시 하위 자원 정리; 정상 해제의 완료·잔여 요청 확인; 사실: 미확인 |
| **NB-P29 · NR BCH** · [STD-RRC] RRC Setup 연동 — RRC Setup 수신에 따른 공통·전용 L1 채널 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: L1 주관 범위의 후보; 관련: [NB-P02](#nb-p), [NB-F02](#nb-f), [NB-F03](#nb-f); 규격 연결: S1 §5.3.3; 신규 누락 검토 후보; 초기 SI 설정과 연결 설정 적용의 경계 확인; 사실: 미확인 |
| **NB-P30 · NR BCH** · [STD-RRC] RRC Re-establishment 연동 — RRC Re-establishment 관련 L1 초기화·재구성 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: L1 주관 범위의 후보; 관련: [NB-F13](#nb-f), [NB-F19](#nb-f), [NB-P29](#nb-p); 규격 연결: S1 §5.3.7; 이벤트 입력·기존 자원 정리·Setup fallback 관련 적용 구간 확인; 사실: 미확인 |
| **NB-P31 · NR BCH** · [CONTEXT] DC 맥락 / SCG 구성 — EN-DC/NR-DC의 SCG 추가·변경 시 NR 채널 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: L1 주관 범위의 후보; 관련: [NB-F25](#nb-f), [NB-P06](#nb-p), [NB-P07](#nb-p), [NT-P27](#nt-p); 규격 연결: S5 §10.2·10.3; DC 종류·구성 변형별 L1 참여 범위 확인; 동시 송신으로 한정하지 않음; 사실: 미확인 |
| **NB-P32 · NR BCH** · [CONTEXT] DC 맥락 / PSCell 변경 — PSCell 변경 시 NR L1 설정·상태 전환 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: L1 주관 범위의 후보; 관련: [NB-F25](#nb-f), [NB-F03](#nb-f), [NT-P28](#nt-p); 규격 연결: S5 §10.6; 기존 Mobility와 공통·차이 확인; 절차 전체의 BCH 소유를 가정하지 않음; 사실: 미확인 |
| **NB-P33 · NR BCH** · [CONTEXT] DC 맥락 / SCG 해제 — SCG 해제 시 NR 채널·Tx 하위 자원 정리 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: L1 주관 범위의 후보; 관련: [NB-P13](#nb-p), [NB-F25](#nb-f), [NT-P27](#nt-p); 규격 연결: S5 §10.4; DC 종료와 SCell 단독 해제를 구별; 실제 L1 처리 범위 확인; 사실: 미확인 |
| **NB-P34 · NR BCH** · [LOCAL] Exception / 부분 적용 — DL/UL 설정 일부 실패 시 적용 상태 정합화·원복 조건 확인 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: L1 주관 범위의 후보; 관련: [NB-P08](#nb-p), [NB-F19](#nb-f), [NB-F18](#nb-f); 원복 존재·허용 범위·기존 설정 보존 여부를 확인하는 후보; 표준이 항상 원복을 지시한다고 가정하지 않음; 사실: 미확인 |
| **NB-P35 · NR BCH** · [LOCAL] 동시 요청 / Release 경합 — 설정·활성 처리 도중 Release 수신 시 대기 요청 취소·정산 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: L1 주관 범위의 후보; 관련: [NB-P13](#nb-p), [NB-F13](#nb-f), [NB-F18](#nb-f); 실제 직렬화·요청 식별·늦은 응답 처리 정책 확인; 사실: 미확인 |

### NB-F

**NR BCH — Feature / 공통 기술 / 25개 검토행**

| Module | Owner | Progress | Update source or contents |
|---|---|---|---|
| **NB-F01 · NR BCH** · [FEATURE] L1 Channel Configuration — DL/UL Physical Channel 설정 파라미터 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-P02](#nb-p), [NB-P06](#nb-p), [NB-P07](#nb-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NB-F02 · NR BCH** · [FEATURE] L1 Channel Configuration — RRC → L1 Configuration 매핑·적용 조건 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-P06](#nb-p), [NB-P07](#nb-p), [NB-P29](#nb-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NB-F03 · NR BCH** · [FEATURE] L1 Channel Configuration — 채널 Config/Reconfig 순서 및 의존성 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-P08](#nb-p), [NB-F18](#nb-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NB-F04 · NR BCH** · [FEATURE] PBCH / MIB / System Information — PBCH/MIB 수신 관련 채널 설정·결과 처리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-P01](#nb-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NB-F05 · NR BCH** · [FEATURE] PBCH / MIB / System Information — SIB1/SI 수신 설정·결과 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-P03](#nb-p), [NB-P04](#nb-p), [NB-P05](#nb-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NB-F06 · NR BCH** · [FEATURE] BWP / CC / SCell Resource — Active DL/UL BWP 상태·설정 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-P17](#nb-p), [NB-P18](#nb-p), [NB-P19](#nb-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NB-F07 · NR BCH** · [FEATURE] BWP / CC / SCell Resource — PCell/SCell 채널 자원 설정 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-P13](#nb-p), [NB-P21](#nb-p), [NB-P27](#nb-p), [NB-F25](#nb-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NB-F08 · NR BCH** · [FEATURE] BWP / CC / SCell Resource — SCell Config/Act/Deact/Release 시 자원 전이 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-P21](#nb-p), [NB-P23](#nb-p), [NB-P25](#nb-p), [NB-P27](#nb-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NB-F09 · NR BCH** · [ASPECT] Interface — RRC ↔ BCH 제어/결과 인터페이스 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 연동만; 관련: [NB-F02](#nb-f), [NB-P06](#nb-p), [NB-P07](#nb-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NB-F10 · NR BCH** · [ASPECT] Interface — Measure Controller 결과 입력 인터페이스 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 연동만; 관련: [NB-P01](#nb-p), [NB-P11](#nb-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NB-F11 · NR BCH** · [ASPECT] Interface — DRX Controller와 채널 설정 연동 경계 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 연동만; 관련: [NB-F13](#nb-f); DRX Controller 상태머신·Idle DRX·Paging 본체 제외; 채널 설정 연동 입력·완료만 분석; 사실: 미확인 |
| **NB-F12 · NR BCH** · [ASPECT] Interface — PHY/HAL 설정 명령 및 응답 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 연동만; 관련: [NB-F18](#nb-f); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NB-F13 · NR BCH** · [ASPECT] State Management — 채널 Config/Active/Release 상태 전이 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-P08](#nb-p), [NB-P13](#nb-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NB-F14 · NR BCH** · [ASPECT] State Management — SCell Activation/Deactivation 상태 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-F08](#nb-f), [NB-P23](#nb-p), [NB-P25](#nb-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NB-F15 · NR BCH** · [ASPECT] State Management — BWP Switching 트리거별 상태 변경 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-F06](#nb-f), [NB-P17](#nb-p), [NB-P18](#nb-p), [NB-P19](#nb-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NB-F16 · NR BCH** · [ASPECT] Timing / Scheduling — 채널 설정 적용 시점·동기화 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-F03](#nb-f), [NB-F18](#nb-f); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NB-F17 · NR BCH** · [ASPECT] Timing / Scheduling — BWP/SCell 변경의 타이밍 제약 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-F06](#nb-f), [NB-F08](#nb-f); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NB-F18 · NR BCH** · [ASPECT] Timing / Scheduling — 설정 요청과 PHY 적용 순서 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-F03](#nb-f), [NB-F12](#nb-f); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NB-F19 · NR BCH** · [ASPECT] Recovery / Diagnostics — 설정 Timeout/실패 감지·복구 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-P15](#nb-p), [NB-P34](#nb-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NB-F20 · NR BCH** · [ASPECT] Recovery / Diagnostics — MIB/SIB 관련 실패 분류 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-P16](#nb-p), [NB-F04](#nb-f), [NB-F05](#nb-f); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NB-F21 · NR BCH** · [ASPECT] Recovery / Diagnostics — 상태 추적 로그·원인 분석 포인트 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NB-F19](#nb-f), [NB-F20](#nb-f); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NB-F22 · NR BCH** · [FEATURE] L1 Channel Configuration 상세 범위 — PDCCH / CORESET / SearchSpace 설정·매핑의 담당 범위 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 기술 분석 후보; 관련: [NB-F01](#nb-f), [NB-F02](#nb-f), [NB-P06](#nb-p); 규격 연결: S1 §6.3.2; 기존 포괄 항목의 상세 검토행; 별도 Feature 생성 대신 기존 기능의 절 매핑 우선; 사실: 미확인 |
| **NB-F23 · NR BCH** · [FEATURE] L1 Channel Configuration 상세 범위 — PDSCH 설정 파라미터·RRC→L1 매핑의 담당 범위 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 기술 분석 후보; 관련: [NB-F01](#nb-f), [NB-F02](#nb-f), [NB-P06](#nb-p); 규격 연결: S1 §6.3.2; PHY 복호 알고리즘 전체가 아닌 Channel 설정·인터페이스 범위 확인; 사실: 미확인 |
| **NB-F24 · NR BCH** · [VERIFY] BWP / SCell Resource 상세 조건 — 지원 Release의 dormant BWP / SCell dormancy 상태 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 기술 분석 후보; 관련: [NB-F06](#nb-f), [NB-F08](#nb-f), [NB-F14](#nb-f); 규격 연결: S2 §5.9·5.15; 지원 Release·구현 여부 확인 후 포함/제외; SCell Deactivation과 동치 처리 금지; 사실: 미확인 |
| **NB-F25 · NR BCH** · [FEATURE] PCell / PSCell / SCG Resource — SpCell의 PCell/PSCell 역할 및 채널 자원·상태 구분 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 기술 분석 후보; 관련: [NB-F07](#nb-f), [NB-P31](#nb-p), [NB-P32](#nb-p), [NB-P33](#nb-p); 규격 연결: S1 / S5 §10; 기존 Module·Feature 구조 안의 설명 절로 우선 연결; 별도 모듈 생성 지시 아님; 사실: 미확인 |

### NT-P

**NR L1 Tx — Procedure / 동작 시나리오 / 31개 검토행**

| Module | Owner | Progress | Update source or contents |
|---|---|---|---|
| **NT-P01 · NR L1 Tx** · [STD-MAC] Initial Access / Random Access 연동 — Random Access 요청에 따른 PRACH 송신 경로·파라미터 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F01](#nt-f), [NT-F06](#nt-f); 규격 연결: S2 §5.1; MAC Random Access 절차의 송신 하위 구간; RA 전체 소유권으로 확대하지 않음; 사실: 미확인 |
| **NT-P02 · NR L1 Tx** · [STD-MAC] Initial Access / Random Access 연동 — Msg3/초기 PUSCH 송신 요청에 따른 Tx 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F01](#nt-f), [NT-F02](#nt-f); 규격 연결: S2 §5.1; 4-step RA 예시; 2-step RA 지원·MsgA 등은 제품/Release 확인 후 변형 추가; 사실: 미확인 |
| **NT-P03 · NR L1 Tx** · [STD-RRC] RRC Reconfiguration 참여 — RRC 기반 UL 구성 변경을 입력받아 Tx 파라미터 반영 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NB-P07](#nb-p), [NT-F14](#nt-f), [NT-F19](#nt-f); 규격 연결: S1 §5.3.5; Channel 주관 흐름의 하위 참여; 적용 조건과 변경 없음 경로 확인; 사실: 미확인 |
| **NT-P04 · NR L1 Tx** · [LOCAL] Channel Configuration 참여 — 상위 채널 구성 변경 시 Tx 자원을 재구성 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F06](#nt-f), [NT-F08](#nt-f), [NT-F19](#nt-f); RF/BB 재설정 필요 여부와 요청·응답 순서 확인; 사실: 미확인 |
| **NT-P05 · NR L1 Tx** · [LOCAL] UL CA / SCell 하위 참여 — UL이 구성된 SCell의 구성·변경 시 Tx 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NB-P22](#nb-p), [NT-F06](#nt-f), [NT-F08](#nt-f), [NT-F19](#nt-f); Channel 주관 이벤트에 조건부 참여; DL-only SCell·Tx 변경 없음 경로를 별도 판정; 사실: 미확인 |
| **NT-P06 · NR L1 Tx** · [LOCAL] UL CA / SCell 하위 참여 — UL이 구성된 SCell의 활성 시 Tx 설정·상태 반영 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NB-P24](#nb-p), [NT-F06](#nt-f), [NT-F08](#nt-f), [NT-F19](#nt-f); Channel 주관 이벤트에 조건부 참여; DL-only SCell·Tx 변경 없음 경로를 별도 판정; 사실: 미확인 |
| **NT-P07 · NR L1 Tx** · [LOCAL] UL CA / SCell 하위 참여 — UL이 구성된 SCell의 비활성 시 송신·자원 상태 반영 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NB-P26](#nb-p), [NT-F06](#nt-f), [NT-F08](#nt-f), [NT-F19](#nt-f); Channel 주관 이벤트에 조건부 참여; DL-only SCell·Tx 변경 없음 경로를 별도 판정; 사실: 미확인 |
| **NT-P08 · NR L1 Tx** · [LOCAL] UL CA / SCell 하위 참여 — UL이 구성된 SCell의 해제 시 Tx 자원 정리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NB-P28](#nb-p), [NT-F06](#nt-f), [NT-F08](#nt-f), [NT-F19](#nt-f); Channel 주관 이벤트에 조건부 참여; DL-only SCell·Tx 변경 없음 경로를 별도 판정; 사실: 미확인 |
| **NT-P09 · NR L1 Tx** · [CONTEXT] UL CA 맥락 / 조건부 Switching — UL CA 구성·활성 상태 변화 중 조건 충족 시 UL Tx Switching 수행 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F09](#nt-f), [NT-P05](#nt-p), [NT-P06](#nt-p); CA는 운용 맥락; 실제 Switching 입력·우선순위·비실행 조건 확인; 사실: 미확인 |
| **NT-P10 · NR L1 Tx** · [CONTEXT] UL CA 맥락 / 조건부 Switching — UL CA 등에서 SRS Carrier Switching 조건 충족 시 전환·복귀 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F12](#nt-f), [NT-F04](#nt-f); CA 전용 여부와 다른 운용 맥락의 재사용 범위 확인; 기준 설명은 NT-F12; 사실: 미확인 |
| **NT-P11 · NR L1 Tx** · [VERIFY] UL CA 맥락 / 사내 용어 — UL CA 관련 SLO 이벤트의 Tx 처리 흐름 확인 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F18](#nt-f); SLO 의미·트리거·적용 제품을 담당자가 확인하기 전 독립 절차로 확정하지 않음; 사실: 미확인 |
| **NT-P12 · NR L1 Tx** · [CONTEXT] UL CA 맥락 / Tx Configuration — UL CA 구성 변경 시 필요한 RF Tx Configuration 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F14](#nt-f), [NT-P04](#nt-p); RF Tx Configuration은 재사용 기능; 이 행은 CA 변경 시 호출 조건만 기록; 사실: 미확인 |
| **NT-P13 · NR L1 Tx** · [CONTEXT] UL CA 맥락 / 조건부 Switching — UL CA 동작 중 경로 변경 요청에 따른 Tx Path 전환 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F11](#nt-f), [NT-F06](#nt-f); NT-P09와 동일 흐름인지 구별; 같으면 기준 시나리오 참조로 처리; 사실: 미확인 |
| **NT-P14 · NR L1 Tx** · [CONTEXT] EN-DC 맥락 — EN-DC에서 동시 송신 조건이 성립할 때 NR Tx 설정 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F07](#nt-f), [NT-F14](#nt-f), [NT-P27](#nt-p); 규격 연결: S5 §10; EN-DC의 일부 조건부 시나리오; EN-DC 전체를 동시 송신으로 정의하지 않음; 사실: 미확인 |
| **NT-P15 · NR L1 Tx** · [CONTEXT] EN-DC 맥락 — EN-DC 자원 제약 변화 시 NR Tx 공유·경로 전환 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F06](#nt-f), [NT-F11](#nt-f), [NT-F07](#nt-f), [LT-P16](#lt-p); 규격 연결: S5 §10; NR/LTE 우선순위·공유 구현은 코드 확인; RAT 양쪽 결과 연결; 사실: 미확인 |
| **NT-P16 · NR L1 Tx** · [STD-RRC] Mobility / Handover 참여 — Mobility 시 UL Tx 경로·설정을 재구성 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NB-P09](#nb-p), [NT-F06](#nt-f), [NT-F14](#nt-f), [NT-F19](#nt-f); 규격 연결: S1 §5.3.5; Target 적용·원복·자원 재사용 조건 확인; 사실: 미확인 |
| **NT-P17 · NR L1 Tx** · [LOCAL] Connected Mode / Tx Switching — Connected 상태에서 안테나 전환 트리거 수신 시 Tx 설정 변경 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F10](#nt-f), [NT-F06](#nt-f); 안테나 선택 알고리즘의 실제 소유 모듈 확인; 외부 결정이면 입력·적용만 분석; 사실: 미확인 |
| **NT-P18 · NR L1 Tx** · [LOCAL] Connected Mode / Tx Switching — Connected 상태에서 경로 전환 요청 시 Tx Path 변경 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F11](#nt-f), [NT-F06](#nt-f); CA/EN-DC/Dual SIM에서도 같은 기능을 참조; 조건 차이만 시나리오로 기록; 사실: 미확인 |
| **NT-P19 · NR L1 Tx** · [LOCAL] Connected Mode / Tx Resource — Tx Chain/BB 자원 변경 요청 시 재할당·정합화 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F06](#nt-f), [NT-F08](#nt-f); 실제 지원·자원 소유·트리거 확인 필요; 사실: 미확인 |
| **NT-P20 · NR L1 Tx** · [LOCAL] CDRX 연동 — CDRX 진입·복귀 이벤트에 따른 UL Tx 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F23](#nt-f), [NT-F19](#nt-f); DRX 상태머신·스케줄링 알고리즘은 제외; 실제 Tx 설정·명령 연동만 확인; 사실: 미확인 |
| **NT-P21 · NR L1 Tx** · [LOCAL] Exception / Recovery — RF/BB Tx 설정 실패 시 경로·자원 복구 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F24](#nt-f), [NT-F22](#nt-f); 복구 수준·이전 상태 보존·Release 경합 정책 확인; 사실: 미확인 |
| **NT-P22 · NR L1 Tx** · [LOCAL] Exception / Recovery — Tx Switching 실패 시 원복·재시도 가능 조건 처리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F24](#nt-f), [NT-F09](#nt-f), [NT-F11](#nt-f); 재시도 존재·상한·취소 조건은 코드 근거로 확인; 무조건 재시도 가정 금지; 사실: 미확인 |
| **NT-P23 · NR L1 Tx** · [CONTEXT] NR-DC 맥락 — NR-DC 구성 변화에 따른 BB Tx Reconfiguration 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F15](#nt-f), [NT-F08](#nt-f), [NT-P28](#nt-p); 규격 연결: S5 §10; EN-DC와 맥락 구분; BB 재구성 공통 구현 여부는 별도 확인; 사실: 미확인 |
| **NT-P24 · NR L1 Tx** · [VERIFY] NR-DC 맥락 / 사내 용어 — NR-DC 관련 F1 Rank Change 이벤트의 Tx 영향 확인 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F17](#nt-f); F1 의미를 인터페이스명·FR1·표준 Rank Change로 임의 해석하지 않음; 사실: 미확인 |
| **NT-P25 · NR L1 Tx** · [CONTEXT] Dual SIM 맥락 — Dual SIM 경합·반환 이벤트에 따른 Tx Sharing 처리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F13](#nt-f), [NT-F07](#nt-f); 공유·우선순위·양보·복귀 조건 확인; 기준 설명은 NT-F13; 사실: 미확인 |
| **NT-P26 · NR L1 Tx** · [CONTEXT] Dual SIM 맥락 — Dual SIM Tx 자원 소유 변경 시 BB Tx Change 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [NT-F16](#nt-f), [NT-F08](#nt-f); BB 변경 필요 조건·기존 자원 유지·반환 순서 확인; 사실: 미확인 |
| **NT-P27 · NR L1 Tx** · [CONTEXT] EN-DC 맥락 / 수명주기 — EN-DC 구성·변경·해제 시 NR Tx 설정·정리 참여 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: Tx 하위 참여 후보; 관련: [NB-P31](#nb-p), [NB-P33](#nb-p), [NT-F14](#nt-f), [NT-F08](#nt-f); 규격 연결: S5 §10.2·10.3·10.4; 동시 송신 이외의 설정·해제 영향과 영향 없음 경로를 확인; 사실: 미확인 |
| **NT-P28 · NR L1 Tx** · [CONTEXT] NR-DC 맥락 / 구성 변경 — NR-DC의 PSCell 등 구성 변화 시 Tx 경로·BB 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: Tx 하위 참여 후보; 관련: [NB-P32](#nb-p), [NT-P23](#nt-p), [NT-F15](#nt-f); 규격 연결: S5 §10; NR-DC 구성 변형별 실제 호출·변경 필요 조건 확인; 사실: 미확인 |
| **NT-P29 · NR L1 Tx** · [LOCAL] 동시 요청 / Release 경합 — Tx Switching 진행 중 Release 수신 시 취소·자원 정리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: Tx 하위 참여 후보; 관련: [NB-P35](#nb-p), [NT-F24](#nt-f), [NT-F22](#nt-f); 이미 적용된 RF/BB 단계·대기 응답·복귀 가능 상태 확인; 사실: 미확인 |
| **NT-P30 · NR L1 Tx** · [LOCAL] 동시 요청 / Switching 경합 — 전환 요청 중첩 시 병합·대기·기각 등 실제 처리 정책 확인 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: Tx 하위 참여 후보; 관련: [NT-F09](#nt-f), [NT-F11](#nt-f), [NT-F22](#nt-f); 존재하는 정책만 기록; 신규 큐·재시도 엔진 제안으로 확대하지 않음; 사실: 미확인 |
| **NT-P31 · NR L1 Tx** · [VERIFY] Timing 입력 연동 — TA/TAG 등 송신 타이밍 유효 조건 변경의 Tx 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 연동만; 관련: [NT-F26](#nt-f), [NT-F19](#nt-f); 타이머·MAC Timing Alignment 절차 본체는 제외; 입력·송신 허용·설정 연계의 실제 경계 확인; 사실: 미확인 |

### NT-F

**NR L1 Tx — Feature / 공통 기술 / 27개 검토행**

| Module | Owner | Progress | Update source or contents |
|---|---|---|---|
| **NT-F01 · NR L1 Tx** · [FEATURE] UL Physical Channel — PUSCH/PUCCH/PRACH 송신 설정 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-P01](#nt-p), [NT-P02](#nt-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NT-F02 · NR L1 Tx** · [FEATURE] UL Physical Channel — UL Physical Channel 송신 경로별 동작 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-F01](#nt-f), [NT-F06](#nt-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NT-F03 · NR L1 Tx** · [FEATURE] Reference Signal / SRS — SRS 송신 설정 및 자원 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-F12](#nt-f), [NT-F04](#nt-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NT-F04 · NR L1 Tx** · [ASPECT] Reference Signal / SRS — SRS Carrier Switching의 트리거·제약 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-F12](#nt-f), [NT-P10](#nt-p); SRS Carrier Switching의 조건 설명 절; 기준 기능 설명은 NT-F12에 연결하여 중복 본문 방지; 사실: 미확인 |
| **NT-F05 · NR L1 Tx** · [FEATURE] Reference Signal / SRS — DMRS 관련 Tx 설정 (코드 확인) | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-F01](#nt-f), [NT-F27](#nt-f); 기존 Feature ID 재사용 여부 확인; 지원·의미·실제 소유권 미확인; 사실: 미확인 |
| **NT-F06 · NR L1 Tx** · [FEATURE] Tx Resource — Tx Antenna / RF Path / Tx Chain Allocation | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-P04](#nt-p), [NT-P05](#nt-p), [NT-P19](#nt-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NT-F07 · NR L1 Tx** · [FEATURE] Tx Resource — UL CA/NR-DC/Dual SIM 자원 공유·우선순위 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-F06](#nt-f), [NT-F13](#nt-f), [NT-P14](#nt-p), [NT-P23](#nt-p), [NT-P25](#nt-p); CA/DC/Dual SIM별 자원 제약을 비교하는 설명; Dual SIM 충돌·우선순위 상세는 NT-F13 참조; 사실: 미확인 |
| **NT-F08 · NR L1 Tx** · [FEATURE] Tx Resource — BB Tx Resource 할당·해제 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-F06](#nt-f), [NT-P19](#nt-p), [NT-P23](#nt-p), [NT-P26](#nt-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NT-F09 · NR L1 Tx** · [FEATURE] Tx Switching — UL Tx Switching 결정 조건·상태 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-P09](#nt-p), [NT-F11](#nt-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NT-F10 · NR L1 Tx** · [FEATURE] Tx Switching — Tx Antenna Switching 알고리즘·조건 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 소유권 확인 필요; 관련: [NT-P17](#nt-p), [NT-F06](#nt-f); 안테나 선택 알고리즘이 별도 모듈 소유이면 Tx는 결정 입력·적용·결과만 분석; 사실: 미확인 |
| **NT-F11 · NR L1 Tx** · [FEATURE] Tx Switching — Tx Path Switching 알고리즘·조건 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-P13](#nt-p), [NT-P18](#nt-p), [NT-F06](#nt-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NT-F12 · NR L1 Tx** · [FEATURE] Tx Switching — SRS Carrier Switching 구현 및 복귀 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-P10](#nt-p), [NT-F03](#nt-f), [NT-F04](#nt-f); SRS Carrier Switching의 본 문서 내 기준 분석행; 실제 기존 Feature ID는 미확인; NT-F04는 조건 설명 참조; 사실: 미확인 |
| **NT-F13 · NR L1 Tx** · [FEATURE] Tx Switching — Dual SIM Tx Sharing 충돌·우선순위 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-P25](#nt-p), [NT-F07](#nt-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NT-F14 · NR L1 Tx** · [FEATURE] Tx Configuration — RF Tx Configuration | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-P03](#nt-p), [NT-P12](#nt-p), [NT-F20](#nt-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NT-F15 · NR L1 Tx** · [FEATURE] Tx Configuration — BB TX Reconfig (NR-DC) | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-P23](#nt-p), [NT-F08](#nt-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NT-F16 · NR L1 Tx** · [FEATURE] Tx Configuration — BB Tx Change (Dual SIM) | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-P26](#nt-p), [NT-F08](#nt-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **NT-F17 · NR L1 Tx** · [VERIFY] Tx Configuration — F1 Rank Change (NR-DC; 사내 정의 확인) | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-P24](#nt-p), [NT-F27](#nt-f); F1 사내 정의·Rank 의미·NR-DC 적용 조건 확인 전 표준 개념으로 치환 금지; 사실: 미확인 |
| **NT-F18 · NR L1 Tx** · [VERIFY] Tx Configuration — SLO (UL CA; 사내 정의 확인) | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-P11](#nt-p); SLO 사내 정의·발생 조건·지원 제품·관련 입력 확인 필요; 사실: 미확인 |
| **NT-F19 · NR L1 Tx** · [ASPECT] Interface — L1 Channel Controller ↔ Tx 설정/이벤트 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 연동만; 관련: [NB-P07](#nb-p), [NT-P03](#nt-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NT-F20 · NR L1 Tx** · [ASPECT] Interface — TxCfgMngr/TxSwitchMngr ↔ HAL/RF 인터페이스 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 연동만; 관련: [NT-F14](#nt-f), [NT-F09](#nt-f), [LT-F15](#lt-f); 공통 TxMngr 설명 재사용 후보; LT-F15와 공통 소스/인터페이스가 같은지 확인 후 기준 문서 지정; 사실: 미확인 |
| **NT-F21 · NR L1 Tx** · [ASPECT] Interface — PHY 송신 설정·결과 인터페이스 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 연동만; 관련: [NT-F01](#nt-f), [NT-F14](#nt-f); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NT-F22 · NR L1 Tx** · [ASPECT] State / Recovery — UL Tx 및 Tx Path 상태 관리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-F06](#nt-f), [NT-F09](#nt-f), [NT-F11](#nt-f); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NT-F23 · NR L1 Tx** · [ASPECT] State / Recovery — CDRX 연동 시 UL Tx 상태 전이 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-P20](#nt-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NT-F24 · NR L1 Tx** · [ASPECT] State / Recovery — RF/BB 설정 실패 진단·복구 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [NT-P21](#nt-p), [NT-P22](#nt-p), [NT-P29](#nt-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **NT-F25 · NR L1 Tx** · [VERIFY] Power 제약 입력 — Tx Power / 최대전력 등 제약 입력과 적용 경계 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 연동만; 관련: [NT-F06](#nt-f), [NT-F19](#nt-f), [NT-F20](#nt-f); Power 제어·SAR/TAS·RF 알고리즘 소유권을 별도 확인; 담당 Tx의 입력·적용 구간만 후보; 사실: 미확인 |
| **NT-F26 · NR L1 Tx** · [VERIFY] Timing 입력 — TA/TAG 등 Tx Timing 입력·유효성 인터페이스 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 연동만; 관련: [NT-P31](#nt-p), [NT-F19](#nt-f), [NT-F22](#nt-f); MAC 타이머·정책을 Tx 기능으로 귀속하지 않음; 실제 입력·조건 확인; 사실: 미확인 |
| **NT-F27 · NR L1 Tx** · [VERIFY] UL Physical Channel 상세 조건 — Rank / antenna port / precoding 관련 Tx 설정의 적용 범위 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 기술 분석 후보; 관련: [NT-F01](#nt-f), [NT-F05](#nt-f), [NT-F17](#nt-f); F1 의미와 별개로 실제 Tx 설정 책임 확인; NR-DC 전용 또는 전체 지원이라고 확정하지 않음; 사실: 미확인 |

### LC-P

**LTE ChCfg — Procedure / 동작 시나리오 / 29개 검토행**

| Module | Owner | Progress | Update source or contents |
|---|---|---|---|
| **LC-P01 · LTE ChCfg** · [STD-RRC] Initial Access / L1 초기 설정 — 동기 획득 결과 이후 LTE PBCH/MIB 관련 L1 설정 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F04](#lc-f), [LC-F10](#lc-f); 규격 연결: S3 §5.2; Search/Measurement 본체 제외; NAS Attach는 상위 맥락으로만 취급; 사실: 미확인 |
| **LC-P02 · LTE ChCfg** · [STD-RRC] Initial Access / L1 초기 설정 — LTE 초기 접근 시 DL/UL 공통 채널 설정 준비·적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F01](#lc-f), [LC-F02](#lc-f), [LC-P24](#lc-p); 규격 연결: S3 §5.2·5.3.3; 초기 공통 설정과 RRC Setup 전용 설정을 구별; 사실: 미확인 |
| **LC-P03 · LTE ChCfg** · [STD-RRC] System Information Acquisition — LTE SIB1/SI 획득 요청에 따른 채널 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F05](#lc-f); 규격 연결: S3 §5.2; 수신·복호 알고리즘과 ChCfg의 설정 연동 경계 확인; 사실: 미확인 |
| **LC-P04 · LTE ChCfg** · [STD-RRC] System Information Acquisition — SI 변경·재획득 요청에 따른 L1 설정 갱신 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F05](#lc-f), [LC-F18](#lc-f); 규격 연결: S3 §5.2; 최초 획득·유효성 변경·실패 재획득 조건 구분; 사실: 미확인 |
| **LC-P05 · LTE ChCfg** · [STD-RRC] RRC Reconfiguration — LTE RRC Reconfiguration에 따른 DL 채널 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F01](#lc-f), [LC-F02](#lc-f), [LC-F21](#lc-f), [LC-F22](#lc-f); 규격 연결: S3 §5.3.5; SCell·CC 세부 흐름을 참조하고 중복 기술 방지; 사실: 미확인 |
| **LC-P06 · LTE ChCfg** · [STD-RRC] RRC Reconfiguration — LTE RRC Reconfiguration에 따른 UL 채널 설정·Tx 연계 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F02](#lc-f), [LT-P03](#lt-p), [LT-F14](#lt-f); 규격 연결: S3 §5.3.5; ChCfg 주관과 Tx 하위 참여 구분; 사실: 미확인 |
| **LC-P07 · LTE ChCfg** · [STD-RRC] RRC Reconfiguration — LTE 재구성 시 채널 자원·적용 상태 정합화 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F03](#lc-f), [LC-F19](#lc-f), [LC-P27](#lc-p); 규격 연결: S3 §5.3.5; 일반 재구성 흐름으로 사용; PCell/CC·SCell의 상위 참조 관계 확인; 사실: 미확인 |
| **LC-P08 · LTE ChCfg** · [STD-RRC] SCell 구성·활성·비활성·해제 — SCell RRC 구성·변경 시 DL 채널 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F07](#lc-f), [LC-F12](#lc-f), [LC-F16](#lc-f); 규격 연결: S3 §5.3.5; 구성·변경의 DL 영향 구간; 별도 DL 셀 추가 절차로 해석하지 않음; 사실: 미확인 |
| **LC-P09 · LTE ChCfg** · [STD-RRC] SCell 구성·활성·비활성·해제 — 동일 SCell 구성·변경의 UL 설정 적용·Tx 연계 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F07](#lc-f), [LC-F12](#lc-f), [LC-F16](#lc-f), [LC-P08](#lc-p), [LT-P05](#lt-p); 규격 연결: S3 §5.3.5; UL이 구성된 경우의 영향 구간; UL 미구성 시 비대상; 사실: 미확인 |
| **LC-P10 · LTE ChCfg** · [STD-MAC] SCell 구성·활성·비활성·해제 — SCell Activation 시 DL 채널·상태 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F07](#lc-f), [LC-F12](#lc-f), [LC-F16](#lc-f); 규격 연결: S4 §5.13; SCell 단위 활성 이벤트; RRC 초기 활성 상태 등 예외도 적용 Release에서 확인; 사실: 미확인 |
| **LC-P11 · LTE ChCfg** · [STD-MAC] SCell 구성·활성·비활성·해제 — 동일 SCell Activation의 UL Tx 처리 연계 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F07](#lc-f), [LC-F12](#lc-f), [LC-F16](#lc-f), [LC-P10](#lc-p), [LT-P06](#lt-p); 규격 연결: S4 §5.13; UL 구성·전송 가능 조건 확인; 활성화만으로 Tx Switching 필수 실행을 가정하지 않음; 사실: 미확인 |
| **LC-P12 · LTE ChCfg** · [STD-MAC] SCell 구성·활성·비활성·해제 — SCell Deactivation 시 DL 채널·상태 반영 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F07](#lc-f), [LC-F12](#lc-f), [LC-F16](#lc-f); 규격 연결: S4 §5.13; MAC CE·비활성 타이머 등 트리거를 구분; 구성 해제와 별개; 사실: 미확인 |
| **LC-P13 · LTE ChCfg** · [STD-MAC] SCell 구성·활성·비활성·해제 — 동일 SCell Deactivation의 UL Tx 중지·자원 처리 연계 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F07](#lc-f), [LC-F12](#lc-f), [LC-F16](#lc-f), [LC-P12](#lc-p), [LT-P07](#lt-p); 규격 연결: S4 §5.13; UL이 구성된 경우의 하위 처리; UL 독립 비활성 표준 이벤트로 명명하지 않음; 사실: 미확인 |
| **LC-P14 · LTE ChCfg** · [STD-RRC] SCell 구성·활성·비활성·해제 — SCell RRC Release 시 DL 설정·자원 정리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F07](#lc-f), [LC-F12](#lc-f), [LC-F16](#lc-f); 규격 연결: S3 §5.3.5; 비활성 상태와 구성 해제를 구분; 사실: 미확인 |
| **LC-P15 · LTE ChCfg** · [STD-RRC] SCell 구성·활성·비활성·해제 — 동일 SCell RRC Release의 UL Tx 자원 정리 연계 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F07](#lc-f), [LC-F12](#lc-f), [LC-F16](#lc-f), [LC-P14](#lc-p), [LT-P08](#lt-p); 규격 연결: S3 §5.3.5; UL 구성 시 하위 자원 정리; 정상 해제의 완료·잔여 요청 확인; 사실: 미확인 |
| **LC-P16 · LTE ChCfg** · [STD-RRC] Mobility / Handover — Handover 관련 Target Cell 채널 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F03](#lc-f), [LC-F17](#lc-f), [LT-P21](#lt-p); 규격 연결: S3 §5.3.5; 상위 이동성 판단 제외; L1 적용·완료 순서 중심; 사실: 미확인 |
| **LC-P17 · LTE ChCfg** · [LOCAL] Cell Change 결과 연동 — Cell Change 결과에 따른 LTE 채널 설정 변경 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F10](#lc-f), [LC-F06](#lc-f), [LC-P29](#lc-p); HO와 Reselection 등 원인별 변형을 구별; 판단 알고리즘 제외; 사실: 미확인 |
| **LC-P18 · LTE ChCfg** · [STD-RRC] PCell / CC 재구성 참여 — PCell 구성 변경 요청 시 LTE 채널 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-P05](#lc-p), [LC-P06](#lc-p), [LC-F06](#lc-f); 규격 연결: S3 §5.3.5; RRC Reconfiguration의 세부 변형인지 확인; 별도 기준 본문 중복 생성 방지; 사실: 미확인 |
| **LC-P19 · LTE ChCfg** · [STD-RRC] PCell / CC 재구성 참여 — CA 구성 CC 추가·제거 시 해당 채널 설정 반영 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-P08](#lc-p), [LC-P09](#lc-p), [LC-P14](#lc-p), [LC-P15](#lc-p), [LC-F08](#lc-f); 규격 연결: S3 §5.3.5; SCell 구성·해제와 같은 흐름이면 해당 행 참조; CC와 SCell 용어 범위 확인; 사실: 미확인 |
| **LC-P20 · LTE ChCfg** · [CONTEXT] EN-DC LTE Anchor 맥락 — EN-DC 구성 요청에 따른 LTE Anchor 채널 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F14](#lc-f), [LC-F02](#lc-f), [LC-P26](#lc-p); 규격 연결: S5 §10; 운용 맥락과 실제 RRC 구성 적용 절차를 구별; 사실: 미확인 |
| **LC-P21 · LTE ChCfg** · [CONTEXT] EN-DC LTE Anchor 맥락 — NR 연계 구성 변화의 LTE 채널 영향 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-P20](#lc-p), [LC-F14](#lc-f), [NB-P31](#nb-p); 규격 연결: S5 §10; 영향 없음 경로도 확인; NR 전체 절차를 LTE 소유로 확대하지 않음; 사실: 미확인 |
| **LC-P22 · LTE ChCfg** · [STD-RRC] 정상 Release — 정상 Release 시 LTE L1 채널·자원 정리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F06](#lc-f), [LC-F13](#lc-f), [LC-P28](#lc-p); 규격 연결: S3 §5.3.8; 설정 실패 복구와 정상 해제를 별도 분류; 사실: 미확인 |
| **LC-P23 · LTE ChCfg** · [LOCAL] Exception / Recovery — 채널 설정 실패·Timeout 발생 시 LTE L1 복구 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: L1 주관 범위의 후보; 관련: [LC-F18](#lc-f), [LC-F19](#lc-f), [LC-P27](#lc-p); 실패 범위와 원복·초기화·해제 선택 조건 확인; 사실: 미확인 |
| **LC-P24 · LTE ChCfg** · [STD-RRC] RRC Setup 연동 — RRC Setup 관련 LTE 공통·전용 L1 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: L1 주관 범위의 후보; 관련: [LC-P02](#lc-p), [LC-F02](#lc-f), [LC-F03](#lc-f); 규격 연결: S3 §5.3.3; 초기 SI 설정과 연결 설정 적용의 경계 확인; 사실: 미확인 |
| **LC-P25 · LTE ChCfg** · [STD-RRC] RRC Re-establishment 연동 — RRC Re-establishment 관련 LTE L1 초기화·재설정 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: L1 주관 범위의 후보; 관련: [LC-F12](#lc-f), [LC-F18](#lc-f), [LC-P24](#lc-p); 규격 연결: S3 §5.3.7; 일반 실패 복구와 구별하여 L1 적용 구간·기존 자원 처리 확인; 사실: 미확인 |
| **LC-P26 · LTE ChCfg** · [CONTEXT] EN-DC 맥락 / 수명주기 — EN-DC 변경·해제 시 LTE Anchor 채널 영향 반영 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: L1 주관 범위의 후보; 관련: [LC-P20](#lc-p), [LC-P21](#lc-p), [LC-F14](#lc-f), [LT-P24](#lt-p); 규격 연결: S5 §10.3·10.4; NR 설정 변화의 LTE 영향 없음 경로 포함; LTE가 NR 절차 전체를 주관한다고 가정하지 않음; 사실: 미확인 |
| **LC-P27 · LTE ChCfg** · [LOCAL] Exception / 부분 적용 — 채널 설정 일부 실패 시 LTE 적용 상태 정합화·원복 조건 확인 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: L1 주관 범위의 후보; 관련: [LC-P07](#lc-p), [LC-P23](#lc-p), [LC-F19](#lc-f); 원복·초기화·해제 정책은 실제 근거로 확인; 모든 실패에 원복이 있다고 가정하지 않음; 사실: 미확인 |
| **LC-P28 · LTE ChCfg** · [LOCAL] 동시 요청 / Release 경합 — 구성 처리 도중 Release 수신 시 요청 취소·늦은 응답 처리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: L1 주관 범위의 후보; 관련: [LC-P22](#lc-p), [LC-F03](#lc-f), [LC-F13](#lc-f), [LT-P23](#lt-p); 진행 중 설정과 정상 해제의 순서·완료 조건 확인; 사실: 미확인 |
| **LC-P29 · LTE ChCfg** · [LOCAL] Cell Change 결과 연동 — Cell Reselection 결과 이후 LTE 채널 재초기화 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 결과 입력 연동; 관련: [LC-P17](#lc-p), [LC-F10](#lc-f), [LC-F04](#lc-f), [LC-F05](#lc-f); Selection/Reselection 판단 알고리즘 제외; 결과 입력 이후의 L1 영향만 확인; 사실: 미확인 |

### LC-F

**LTE ChCfg — Feature / 공통 기술 / 22개 검토행**

| Module | Owner | Progress | Update source or contents |
|---|---|---|---|
| **LC-F01 · LTE ChCfg** · [FEATURE] LTE Channel Configuration — DL/UL Physical Channel 설정 파라미터 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-P02](#lc-p), [LC-P05](#lc-p), [LC-P06](#lc-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LC-F02 · LTE ChCfg** · [FEATURE] LTE Channel Configuration — LTE RRC → L1 설정 매핑 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-P05](#lc-p), [LC-P06](#lc-p), [LC-P24](#lc-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LC-F03 · LTE ChCfg** · [FEATURE] LTE Channel Configuration — Channel Config/Reconfig 적용 순서 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-P07](#lc-p), [LC-F11](#lc-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LC-F04 · LTE ChCfg** · [FEATURE] MIB / SIB / System Information — LTE MIB 관련 채널 설정·결과 처리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-P01](#lc-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LC-F05 · LTE ChCfg** · [FEATURE] MIB / SIB / System Information — LTE SIB/SI 수신 설정·갱신 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-P03](#lc-p), [LC-P04](#lc-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LC-F06 · LTE ChCfg** · [FEATURE] PCell / SCell / CC Resource — PCell/CC 설정·유지 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-P18](#lc-p), [LC-P19](#lc-p), [LC-P22](#lc-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LC-F07 · LTE ChCfg** · [FEATURE] PCell / SCell / CC Resource — SCell Config/Act/Deact/Release 자원 상태 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-P08](#lc-p), [LC-P10](#lc-p), [LC-P12](#lc-p), [LC-P14](#lc-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LC-F08 · LTE ChCfg** · [FEATURE] PCell / SCell / CC Resource — DL/UL CA 채널 설정·리소스 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-P19](#lc-p), [LC-P08](#lc-p), [LC-P09](#lc-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LC-F09 · LTE ChCfg** · [ASPECT] Interface — RRC ↔ ChCfg 제어·상태 인터페이스 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 연동만; 관련: [LC-F02](#lc-f), [LC-P05](#lc-p), [LC-P06](#lc-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LC-F10 · LTE ChCfg** · [ASPECT] Interface — Measure/DRX Controller 연동 경계 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 연동만; 관련: [LC-P01](#lc-p), [LC-P17](#lc-p), [LC-P29](#lc-p); Measure의 Search/Measurement 및 DRX 상태머신·Paging 본체 제외; 결과·설정 인터페이스만 분석; 사실: 미확인 |
| **LC-F11 · LTE ChCfg** · [ASPECT] Interface — PHY/HAL 설정 명령·결과 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 연동만; 관련: [LC-F03](#lc-f); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LC-F12 · LTE ChCfg** · [ASPECT] State Management — PCell/SCell 채널 상태 전이 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-F06](#lc-f), [LC-F07](#lc-f); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LC-F13 · LTE ChCfg** · [ASPECT] State Management — Config/Active/Deactivated/Release 상태 관리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-F07](#lc-f), [LC-P10](#lc-p), [LC-P12](#lc-p), [LC-P22](#lc-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LC-F14 · LTE ChCfg** · [ASPECT] State Management — EN-DC LTE Anchor 설정 상태 (코드 확인) | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-P20](#lc-p), [LC-P21](#lc-p), [LC-P26](#lc-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 지원·의미·실제 소유권 미확인; 사실: 미확인 |
| **LC-F15 · LTE ChCfg** · [ASPECT] Timing / Scheduling — 채널 설정 타이밍 및 적용 시점 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-F03](#lc-f); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LC-F16 · LTE ChCfg** · [ASPECT] Timing / Scheduling — SCell Activation/Deactivation 타이밍 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-F07](#lc-f), [LC-P10](#lc-p), [LC-P12](#lc-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LC-F17 · LTE ChCfg** · [ASPECT] Timing / Scheduling — Handover 시 채널 설정 순서 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-P16](#lc-p), [LC-F03](#lc-f); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LC-F18 · LTE ChCfg** · [ASPECT] Recovery / Diagnostics — 설정 Timeout/실패 처리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-P23](#lc-p), [LC-P27](#lc-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LC-F19 · LTE ChCfg** · [ASPECT] Recovery / Diagnostics — 채널 재설정·해제 시 정합성 검증 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-F06](#lc-f), [LC-F07](#lc-f), [LC-P27](#lc-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LC-F20 · LTE ChCfg** · [ASPECT] Recovery / Diagnostics — 상태/오류 로그 분석 포인트 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LC-F18](#lc-f), [LC-F19](#lc-f); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LC-F21 · LTE ChCfg** · [FEATURE] LTE Channel Configuration 상세 범위 — LTE PDCCH 설정·RRC→L1 매핑의 담당 범위 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 기술 분석 후보; 관련: [LC-F01](#lc-f), [LC-F02](#lc-f), [LC-P05](#lc-p); 규격 연결: S3 §6.3.2; NR CORESET/BWP 개념을 LTE에 자동 전용하지 않음; 제품별 대상 채널 확인; 사실: 미확인 |
| **LC-F22 · LTE ChCfg** · [FEATURE] LTE Channel Configuration 상세 범위 — LTE PDSCH 설정·RRC→L1 매핑의 담당 범위 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 기술 분석 후보; 관련: [LC-F01](#lc-f), [LC-F02](#lc-f), [LC-P05](#lc-p); 규격 연결: S3 §6.3.2; 기존 포괄 항목의 상세 검토행; PHY 알고리즘 전체를 포함하지 않음; 사실: 미확인 |

### LT-P

**LTE L1 Tx — Procedure / 동작 시나리오 / 25개 검토행**

| Module | Owner | Progress | Update source or contents |
|---|---|---|---|
| **LT-P01 · LTE L1 Tx** · [STD-MAC] Initial Access / Random Access 연동 — Random Access 요청에 따른 LTE PRACH 경로·설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F01](#lt-f), [LT-F05](#lt-f); 규격 연결: S4 §5.1; MAC Random Access의 송신 하위 처리만 분석; 사실: 미확인 |
| **LT-P02 · LTE L1 Tx** · [STD-MAC] Initial Access / Random Access 연동 — Msg3/초기 PUSCH 송신 요청에 따른 LTE Tx 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F01](#lt-f), [LT-F02](#lt-f); 규격 연결: S4 §5.1; RA 전체 알고리즘·MAC 정책 소유권과 구별; 사실: 미확인 |
| **LT-P03 · LTE L1 Tx** · [STD-RRC] RRC Reconfiguration 참여 — RRC 기반 UL 구성 변경을 입력받아 LTE Tx 파라미터 반영 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LC-P06](#lc-p), [LT-F11](#lt-f), [LT-F14](#lt-f); 규격 연결: S3 §5.3.5; 상위 ChCfg 이벤트와 Tx 적용·완료 경계 확인; 사실: 미확인 |
| **LT-P04 · LTE L1 Tx** · [LOCAL] Channel Configuration 참여 — 상위 UL 구성 변경 시 BB/RF Tx 설정 재구성 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F05](#lt-f), [LT-F11](#lt-f), [LT-F12](#lt-f); 실제 BB 변경·RF 재설정 필요 조건 확인; 사실: 미확인 |
| **LT-P05 · LTE L1 Tx** · [LOCAL] UL CA / SCell 하위 참여 — UL이 구성된 LTE SCell의 구성·변경 시 Tx 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LC-P09](#lc-p), [LT-F05](#lt-f), [LT-F06](#lt-f), [LT-F14](#lt-f); ChCfg 주관 이벤트에 조건부 참여; UL 미구성·Tx 변경 없음 경로를 구별; 사실: 미확인 |
| **LT-P06 · LTE L1 Tx** · [LOCAL] UL CA / SCell 하위 참여 — UL이 구성된 LTE SCell의 활성 시 Tx 설정·상태 반영 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LC-P11](#lc-p), [LT-F05](#lt-f), [LT-F06](#lt-f), [LT-F14](#lt-f); ChCfg 주관 이벤트에 조건부 참여; UL 미구성·Tx 변경 없음 경로를 구별; 사실: 미확인 |
| **LT-P07 · LTE L1 Tx** · [LOCAL] UL CA / SCell 하위 참여 — UL이 구성된 LTE SCell의 비활성 시 송신·자원 상태 반영 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LC-P13](#lc-p), [LT-F05](#lt-f), [LT-F06](#lt-f), [LT-F14](#lt-f); ChCfg 주관 이벤트에 조건부 참여; UL 미구성·Tx 변경 없음 경로를 구별; 사실: 미확인 |
| **LT-P08 · LTE L1 Tx** · [LOCAL] UL CA / SCell 하위 참여 — UL이 구성된 LTE SCell의 해제 시 Tx 자원 정리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LC-P15](#lc-p), [LT-F05](#lt-f), [LT-F06](#lt-f), [LT-F14](#lt-f); ChCfg 주관 이벤트에 조건부 참여; UL 미구성·Tx 변경 없음 경로를 구별; 사실: 미확인 |
| **LT-P09 · LTE L1 Tx** · [CONTEXT] UL CA 맥락 / 조건부 Switching — UL CA 구성 변화 시 필요 조건에 따른 Tx 재할당·경로 전환 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F13](#lt-f), [LT-F08](#lt-f), [LT-F05](#lt-f); CA 참여만으로 경로 전환·BB 변경을 필수화하지 않음; 사실: 미확인 |
| **LT-P10 · LTE L1 Tx** · [LOCAL] Channel Configuration 참여 — PCell/SCell 구성 변경 시 해당 Tx 자원 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F06](#lt-f), [LT-P03](#lt-p), [LT-P05](#lt-p); UL Tx Resource는 기능명; 실제 자원 변경 이벤트의 시나리오로 기술; 사실: 미확인 |
| **LT-P11 · LTE L1 Tx** · [VERIFY] Tx 제약 변경 연동 — Power/Tx Chain 제약 입력 변경 시 Tx 자원 조정 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F05](#lt-f), [LT-F20](#lt-f); Power·SAR/TAS·RF 알고리즘 소유권은 별도 확인; Tx 입력·적용 범위만 후보; 사실: 미확인 |
| **LT-P12 · LTE L1 Tx** · [VERIFY] Connected Mode / Tx Switching — 안테나 전환 요청 시 LTE Tx 설정 적용 여부 확인 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F09](#lt-f), [LT-F05](#lt-f); LTE 실제 지원·선택 알고리즘 소유 모듈 확인 전 확정하지 않음; 사실: 미확인 |
| **LT-P13 · LTE L1 Tx** · [LOCAL] Connected Mode / Tx Switching — Tx 경로 전환 요청 시 LTE Tx Path 변경 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F08](#lt-f), [LT-F05](#lt-f); UL CA·EN-DC·Dual SIM에서 재사용 시나리오를 참조; 사실: 미확인 |
| **LT-P14 · LTE L1 Tx** · [LOCAL] Channel Configuration 참여 — Tx 경로·구성 변경 시 필요한 RF 설정 적용 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F11](#lt-f), [LT-P04](#lt-p), [LT-P13](#lt-p); RF Tx Configuration 기준 설명은 LT-F11; 호출 조건만 이 행에 기록; 사실: 미확인 |
| **LT-P15 · LTE L1 Tx** · [CONTEXT] EN-DC 맥락 — EN-DC 동시 송신 조건 성립 시 LTE Tx 자원·경로 조정 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F07](#lt-f), [LT-F08](#lt-f), [LT-P24](#lt-p); 규격 연결: S5 §10; 동시 송신은 EN-DC의 일부 조건부 시나리오; 사실: 미확인 |
| **LT-P16 · LTE L1 Tx** · [CONTEXT] EN-DC 맥락 — EN-DC 자원 제약 변화 시 LTE Tx Sharing·경로 전환 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F07](#lt-f), [LT-F16](#lt-f), [NT-P15](#nt-p); 규격 연결: S5 §10; NR/LTE 연동 결과를 연결; Dual SIM 공유 정책과 동일하다고 가정하지 않음; 사실: 미확인 |
| **LT-P17 · LTE L1 Tx** · [CONTEXT] Dual SIM 맥락 — Dual SIM 경합·반환 이벤트의 LTE Tx Sharing 처리 확인 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F10](#lt-f), [LT-F07](#lt-f); 실제 LTE 지원·우선순위·양보·복귀 조건 확인 필요; 사실: 미확인 |
| **LT-P18 · LTE L1 Tx** · [CONTEXT] Dual SIM 맥락 — Dual SIM 자원 소유 변경 시 LTE BB Tx Change 적용 여부 확인 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F12](#lt-f), [LT-F05](#lt-f); 실제 지원·BB 변경 범위 확인; NR 구현을 자동 복제하지 않음; 사실: 미확인 |
| **LT-P19 · LTE L1 Tx** · [LOCAL] Exception / Recovery — UL Tx 경로·설정 실패 발생 시 LTE Tx 복구 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F18](#lt-f), [LT-F17](#lt-f); 원복·재시도·해제의 실제 선택 정책 확인; 사실: 미확인 |
| **LT-P20 · LTE L1 Tx** · [LOCAL] 정상 Release / 재초기화 — 정상 Release 시 Tx 자원 정리 및 후속 재초기화 조건 처리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: Tx 하위 참여 후보; 관련: [LT-F19](#lt-f), [LC-P22](#lc-p), [LT-P23](#lt-p); 기존 Exception/Recovery 묶음에서 정상 해제 분리; 오류 재초기화는 LT-P19와 연결; 사실: 미확인 |
| **LT-P21 · LTE L1 Tx** · [STD-RRC] Mobility / Handover 참여 — Mobility/Handover 시 LTE Tx 경로·자원·설정 재구성 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: Tx 하위 참여 후보; 관련: [LC-P16](#lc-p), [LT-F05](#lt-f), [LT-F11](#lt-f); 규격 연결: S3 §5.3.5; Source/Target 적용·실패 원복·자원 유지 조건 확인; 사실: 미확인 |
| **LT-P22 · LTE L1 Tx** · [VERIFY] CDRX 연동 — CDRX 진입·복귀 시 LTE Tx 연동의 지원·담당 범위 확인 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 연동만; 관련: [LT-F17](#lt-f), [LT-F14](#lt-f), [NT-P20](#nt-p); NR과 동일 지원을 가정하지 않음; DRX 상태머신·Idle DRX·Paging 본체 제외; 사실: 미확인 |
| **LT-P23 · LTE L1 Tx** · [LOCAL] 동시 요청 / Release 경합 — 진행 중 RF/BB 적용·전환과 Release 요청의 취소·정산 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: Tx 하위 참여 후보; 관련: [LT-P20](#lt-p), [LT-F18](#lt-f), [LT-F19](#lt-f), [LC-P28](#lc-p); 정상 해제·실패 복구·늦은 응답의 상태 정합성 확인; 사실: 미확인 |
| **LT-P24 · LTE L1 Tx** · [CONTEXT] EN-DC 맥락 / 수명주기 — EN-DC 변경·해제 시 LTE Tx 설정·자원 영향 반영 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: Tx 하위 참여 후보; 관련: [LC-P26](#lc-p), [LT-F07](#lt-f), [LT-F11](#lt-f), [NT-P27](#nt-p); 규격 연결: S5 §10.3·10.4; 동시 송신 이외의 구성·해제 영향과 영향 없음 경로 확인; 사실: 미확인 |
| **LT-P25 · LTE L1 Tx** · [VERIFY] Timing 입력 연동 — TA/TAG 등 타이밍 유효 조건 변경의 LTE Tx 연동 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 연동만; 관련: [LT-F21](#lt-f), [LT-F14](#lt-f); MAC 타이머·Timing Alignment 정책 본체 제외; 입력·송신 허용·설정 적용 범위 확인; 사실: 미확인 |

### LT-F

**LTE L1 Tx — Feature / 공통 기술 / 21개 검토행**

| Module | Owner | Progress | Update source or contents |
|---|---|---|---|
| **LT-F01 · LTE L1 Tx** · [FEATURE] UL Physical Channel — LTE PRACH/PUSCH/PUCCH 송신 설정 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-P01](#lt-p), [LT-P02](#lt-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LT-F02 · LTE L1 Tx** · [FEATURE] UL Physical Channel — UL Tx 파라미터·채널별 동작 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-F01](#lt-f), [LT-P03](#lt-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LT-F03 · LTE L1 Tx** · [FEATURE] Reference Signal / SRS — LTE SRS 송신 설정·리소스 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-F04](#lt-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LT-F04 · LTE L1 Tx** · [FEATURE] Reference Signal / SRS — UL CA 관련 SRS 송신 연동 (코드 확인) | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-F03](#lt-f), [LT-P09](#lt-p); 기존 Feature ID 재사용 여부 확인; 지원·의미·실제 소유권 미확인; 사실: 미확인 |
| **LT-F05 · LTE L1 Tx** · [FEATURE] Tx Resource — RF Path/Tx Chain/BB Tx 자원 할당 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-P04](#lt-p), [LT-P09](#lt-p), [LT-P10](#lt-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LT-F06 · LTE L1 Tx** · [FEATURE] Tx Resource — PCell/SCell UL Tx Resource 관리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-P05](#lt-p), [LT-P08](#lt-p), [LT-P10](#lt-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LT-F07 · LTE L1 Tx** · [FEATURE] Tx Resource — EN-DC 및 Dual SIM 자원 제약 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-P15](#lt-p), [LT-P17](#lt-p), [LT-F10](#lt-f); EN-DC와 Dual SIM의 자원 제약을 구별; 동일 공유 정책·우선순위라고 추정하지 않음; 사실: 미확인 |
| **LT-F08 · LTE L1 Tx** · [FEATURE] Tx Switching — Tx Path Switching 결정·실행 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-P09](#lt-p), [LT-P13](#lt-p); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LT-F09 · LTE L1 Tx** · [FEATURE] Tx Switching — Tx Antenna Switching (지원 여부 확인) | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-P12](#lt-p); 기존 Feature ID 재사용 여부 확인; 지원·의미·실제 소유권 미확인; 사실: 미확인 |
| **LT-F10 · LTE L1 Tx** · [FEATURE] Tx Switching — Tx Sharing/우선순위·충돌 처리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-P17](#lt-p), [LT-F07](#lt-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LT-F11 · LTE L1 Tx** · [FEATURE] Tx Configuration — RF Tx Configuration | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-P03](#lt-p), [LT-P14](#lt-p), [LT-F15](#lt-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LT-F12 · LTE L1 Tx** · [FEATURE] Tx Configuration — BB Tx Change (코드 확인) | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-P04](#lt-p), [LT-P18](#lt-p); 기존 Feature ID 재사용 여부 확인; 지원·의미·실제 소유권 미확인; 사실: 미확인 |
| **LT-F13 · LTE L1 Tx** · [FEATURE] Tx Configuration — UL CA 송신 자원 재구성 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-P09](#lt-p), [LT-F05](#lt-f), [LT-F06](#lt-f); 기존 Feature ID 재사용 여부 확인; 사실: 미확인 |
| **LT-F14 · LTE L1 Tx** · [ASPECT] Interface — LTE ChCfg ↔ L1 Tx 설정 인터페이스 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 연동만; 관련: [LC-P06](#lc-p), [LT-P03](#lt-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LT-F15 · LTE L1 Tx** · [ASPECT] Interface — TxCfgMngr/TxSwitchMngr ↔ RF/HAL 인터페이스 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 연동만; 관련: [LT-F11](#lt-f), [LT-F08](#lt-f), [NT-F20](#nt-f); NT-F20과 공통 TxMngr 설명 재사용 후보; LTE/NR 차이는 적용 범위·변형으로 기록; 사실: 미확인 |
| **LT-F16 · LTE L1 Tx** · [ASPECT] Interface — EN-DC LTE/NR Tx 연동 인터페이스 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 연동만; 관련: [LT-P16](#lt-p), [NT-P15](#nt-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LT-F17 · LTE L1 Tx** · [ASPECT] State / Recovery — UL Tx/Tx Path 상태 전이 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-F05](#lt-f), [LT-F08](#lt-f); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LT-F18 · LTE L1 Tx** · [ASPECT] State / Recovery — 설정 실패·Tx Resource 복구 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-P19](#lt-p), [LT-P23](#lt-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LT-F19 · LTE L1 Tx** · [ASPECT] State / Recovery — Release 및 재초기화 상태 관리 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | v0.8 계승; 범위: 기술 분석 후보; 관련: [LT-P20](#lt-p); 기존 Feature의 설명 절에 매핑; 단독 Feature 생성 여부는 기존 ID 대조 후 판정; 사실: 미확인 |
| **LT-F20 · LTE L1 Tx** · [VERIFY] Power 제약 입력 — LTE Tx Power / 최대전력 등 제약 입력·적용 경계 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 연동만; 관련: [LT-P11](#lt-p), [LT-F05](#lt-f), [LT-F15](#lt-f); Power·SAR/TAS·RF 알고리즘 소유권은 별도 확인; Tx가 소비하는 제약만 후보; 사실: 미확인 |
| **LT-F21 · LTE L1 Tx** · [VERIFY] Timing 입력 — LTE TA/TAG 등 Tx Timing 입력·유효성 인터페이스 | 작성 미정 · 검토 미정 | 검토 미검토 · 작성 미착수 | **신규 후보**; 범위: 연동만; 관련: [LT-P25](#lt-p), [LT-F14](#lt-f), [LT-F17](#lt-f); 실제 입력·조건과 MAC/PHY/Tx 사이 책임 경계 확인; 사실: 미확인 |

## 6. 변경 계보와 집계

### 6.1 세부 항목 수

아래는 검토행 수이며 실제 Feature/Scenario/지식 문서 수가 아님. 중복 노출은 기준 설명·참조 관계로 해석.

| 모듈 | v0.8 P | v0.8 F | 신규 P | 신규 F | v0.9 P | v0.9 F | v0.9 합계 |
|---|---:|---:|---:|---:|---:|---:|---:|
| NR BCH | 28 | 21 | 7 | 4 | 35 | 25 | 60 |
| NR L1 Tx | 26 | 24 | 5 | 3 | 31 | 27 | 58 |
| LTE ChCfg | 23 | 20 | 6 | 2 | 29 | 22 | 51 |
| LTE L1 Tx | 20 | 19 | 5 | 2 | 25 | 21 | 46 |
| **합계** | **97** | **84** | **23** | **11** | **120** | **95** | **215** |

### 6.2 v0.8 계승 범위

| 모듈 | v0.8 Procedure 출현 순서 → 보존 ID | v0.8 Feature 출현 순서 → 보존 ID | 신규 후보 ID |
|---|---|---|---|
| NR BCH | 1~28 → NB-P01~NB-P28 | 1~21 → NB-F01~NB-F21 | NB-P29~NB-P35, NB-F22~NB-F25 |
| NR L1 Tx | 1~26 → NT-P01~NT-P26 | 1~24 → NT-F01~NT-F24 | NT-P27~NT-P31, NT-F25~NT-F27 |
| LTE ChCfg | 1~23 → LC-P01~LC-P23 | 1~20 → LC-F01~LC-F20 | LC-P24~LC-P29, LC-F21~LC-F22 |
| LTE L1 Tx | 1~20 → LT-P01~LT-P20 | 1~19 → LT-F01~LT-F19 | LT-P21~LT-P25, LT-F20~LT-F21 |

- v0.8 원본은 보존. 기존 181개 검토 관심사항을 유지하고 제목·분류·조건·참조를 수정. 기존행 삭제 0, 신규 검토 후보 34.
- v0.8은 Procedure 대분류 35개, Feature/공통 기술 대분류 28개, 세부 항목 97/84개. 대분류 수와 세부 행 수를 혼용하지 않음.
- v0.9는 상세 후보 추가·재분류로 대분류 집계가 달라질 수 있으므로 위 표에서는 세부 행 수만 비교. 문서 행 수를 기능 완성도·지원 기능 수로 사용하지 않음.

### 6.3 주요 의미 변경

| 기존 표현·구조 | v0.9 반영 |
|---|---|
| Initial Access / Attach | Initial Access / L1 초기 설정으로 정리; NAS는 상위 맥락 |
| SCell의 DL/UL 독립 8절차로 읽힐 수 있는 제목 | 4종 이벤트의 DL/UL 영향 구간 및 UL 구성 조건으로 구체화 |
| BWP 설정·전환 일괄 기술 | 구성과 활성 변경, 트리거·DL/UL 적용 조건 구별 |
| CA/DC/Dual SIM을 모두 Procedure명으로 사용 | CONTEXT와 구체적 처리 트리거를 함께 표시 |
| Feature명만 적힌 Procedure 행 | 해당 기능의 발생 계기·적용 흐름으로 재작성 |
| Interface·State·Timing·Recovery를 동일 수준 Feature로 노출 | ASPECT로 구별하여 관련 기존 기능의 절 연결 우선 |
| 반복된 SRS Carrier Switching 설명 | NT-F12 기준 분석행 + NT-F04 조건 설명 + NT-P10 맥락별 흐름 연결 |
| 정상 Release와 실패 복구 혼합 | LC-P22, LT-P20을 정상 해제 중심으로 구별하고 경합 후보 연결 |
| NR/LTE 기능의 묵시적 대칭 | LTE의 실제 지원·소유권 확인 유지; NR 전용 개념 자동 복제 금지 |

## 7. 리뷰 지적 반영과 남은 게이트

| ID | 수준 | 문서 반영 | 현재 한계·후속 확인 |
|---|---|---|---|
| B-01 | BLOCKING | §2의 기존 ID 재사용·기준 본문·교차 참조·미매핑 정책 | 실제 기존 ID/본문 대조 미수행. **updater 정본 편입은 보류 유지** |
| M-01 | MAJOR | 범례·절차/맥락 구분·초기 접근 명칭 정리, P행 트리거 구체화 | 적용 Release·표준 세부 조건·로컬 경계 확인 필요 |
| M-02 | MAJOR | §4.1, SCell DL/UL 영향 구간·UL 조건부 참여 | 코드 실제 호출·비실행·초기 활성 예외 확인 필요 |
| M-03 | MAJOR | §1.2·§2.2, 주관/참여/연동, NR/LTE 공통 설명 연결 | 공통 소스·기존 기준 문서·실제 소유권 확인 필요 |
| M-04 | MAJOR | BWP 조건·VERIFY·SLO/F1 미확인 유지 | 지원 제품/Release·정의·실제 처리 모듈 확인 필요 |
| M-05 | MAJOR | 모듈별 신규 검토 후보 34개 | 담당자 포함/연동/제외·중복 판정 전. 실제 누락 확정 아님 |
| M-06 | MAJOR | 4열 유지·검토 ID·역참조·검토/작성 상태 분리 | Confluence 실제 복사/렌더링 미검증; 설치본 필드/상태 정의는 미확인 |
| m-01 | MINOR | §6에서 대분류/세부 행 수 분리 | 관련 공통 문서의 기존 집계 표는 이 파일 작성으로 수정되지 않음 |
| m-02 | MINOR | 개정·범위·후보 상태·입력 provenance 명시 | 담당자 승인/기존 ID 매핑은 별도 |
| m-03 | MINOR | NR-DC·UL CA 표기 정리·사내 용어 확인 표시 | 원문 식별을 위해 기존 계보 보존 |

문서 보완 완료와 실제 결함 해소·코드/호스트 검증을 구분. 이 파일의 제목·범례 수정으로 기존 운영 데이터·지식 정본·스킬 상태는 변경되지 않음.

### 7.1 관련 공통 문서의 교체 제안 문구

> Confluence 검토표는 Module / Owner / Progress / Update source or contents 4열을 사용. Procedure는 기존 Module → Feature → Scenario를 가로지르는 탐색 뷰이며, Feature/공통 기술에는 재사용 기능과 설명 관점을 구별해 표시. 검토행 ID는 설치본 지식 ID가 아니며, 기존 ID·기준 본문·적용 범위·근거를 확인한 항목만 후속 지식 후보로 연결. 담당자 검토와 문서 작성 진척·코드 사실·게시 상태를 분리.

위 문구는 후속 문서 정합성 보완안. 관련 정본 문서에 실제 반영한 상태는 아님.

## 8. 담당자 검토 완료 기준과 다음 한 동작

| 단계 | 완료 기준 | 현재 |
|---|---|---|
| 분류 문서 개정 | 범례·범위·기존행 계보·신규 후보·조건·참조·상태 구별 | 작성 완료 |
| 담당자 검토 | 행별 적절/누락/변경/제외, 범위·정의·지원 미확인에 대한 의견 | 대기 |
| 기존 구조 대조 | 실제 기존 Module/Feature/Scenario 또는 절·기준 본문 확인, 중복 연결 | 미수행 |
| 코드/적용 범위 확인 | 고정 입력·코드 근거·제품/Release/build 조건·한계 확인 | 미수행 |
| 지식 후보 작성·정본 반영 | 기존 계약에 따른 후보·검토·승인·게시/확인 조건 충족 | 미수행 |

다음 한 동작은 **담당자에게 네 모듈별 검토표를 전달해 포함 범위·분류·지원 미확인을 판정받는 것**. 판단이 필요한 사내 용어·범위는 VERIFY 상태로 유지. 단순 검토용 ID를 실제 지식 ID로 등록하거나 215행을 한꺼번에 자동 분석·생성하지 않음.

## 9. 근거와 표준 확인 범위

### 9.1 설계 입력

- Confluence 분류표 v0.8 — 이 파일의 기존행 계보 기준
- 담당자 검토용 분류표 v0.7 — A 97행, B 84행의 후보 구조
- L1_CHANNEL 담당 모듈 범위 공통 문서 r0001 — NR BCH 역할·Channel/Tx 경계·제외 범위
- K5.8/K6 × Workflow 연계 계약 r0005 — 기존 ID/구조·상태 축·근거·최소 변경 원칙
- 별도 관점 GPT 문서 리뷰 — BLOCKING 1 / MAJOR 6 / MINOR 3의 개선 요구

이 문서는 기술 분류와 담당자 검토용으로 독립해서 읽을 수 있게 작성. 협업 서비스의 접근·인증이나 실행 환경을 전제로 하지 않음.

### 9.2 표준 참고

다음 고정 버전은 분류 경계를 확인하는 참고 자료. 실제 제품의 적용 Release·지원 기능을 보증하지 않으며, 구체적 세부 조건은 담당자가 적용 규격과 대조. 특히 서로 다른 Release의 예외를 합쳐 한 제품의 동작으로 기술하지 않음.

| 표기 | 참고 규격·버전 | 분류상 확인 목적 |
|---|---|---|
| S1 | [3GPP TS 38.331 V17.14.0](https://www.etsi.org/deliver/etsi_ts/138300_138399/138331/17.14.00_60/ts_138331v171400p.pdf) | SI, RRC Setup/Reconfiguration/Re-establishment/Release/Resume 및 RRC 설정 |
| S2 | [3GPP TS 38.321 V17.13.0](https://www.etsi.org/deliver/etsi_ts/138300_138399/138321/17.13.00_60/ts_138321v171300p.pdf) | Random Access, §5.9 SCell 활성/비활성, §5.15 BWP 운용 |
| S3 | [3GPP TS 36.331 V17.2.0](https://www.etsi.org/deliver/etsi_ts/136300_136399/136331/17.02.00_60/ts_136331v170200p.pdf) | LTE RRC 구성·재구성·연결/재수립 관련 절차 확인 |
| S4 | [3GPP TS 36.321 V16.2.0](https://www.etsi.org/deliver/etsi_ts/136300_136399/136321/16.02.00_60/ts_136321v160200p.pdf) | LTE MAC Random Access 및 §5.13 SCell 활성/비활성 |
| S5 | [3GPP TS 37.340 V18.7.0](https://www.etsi.org/deliver/etsi_ts/137300_137399/137340/18.07.00_60/ts_137340v180700p.pdf) | §10의 DC 관련 SN 추가·변경·해제 및 PSCell 변경 맥락 |

표준은 절차·맥락의 구분을 뒷받침하며 사내 모듈·함수·알고리즘의 소유권을 입증하지 않음. 표의 구체적 모듈 참여는 코드·담당자 확인 후보.

## 10. 문서 정적 검증 기록

- 기준 v0.8 파일 SHA-256: `590985fc5e556ab95f9b9f7f12119e17b2d2cd8f64d1daebe8b7334467680108`
- v0.8 파싱: 181행, Procedure 97행 / Feature 84행 — PASS
- 기존행 번호·원본 항목 계보 유지: 181개 — PASS
- 신규 후보: 34개, Procedure 23개 / Feature 11개 — PASS
- 최종 검토행: 215개, Procedure 120개 / Feature 95개 — PASS
- 검토 ID 중복 0, 연결 대상 ID 누락 0, 8개 검토표의 4열 형식 — PASS
- 코드/스킬/실 API/Confluence 호스트 동작 검증 — NOT_RUN
- 실제 기존 ID 매핑·지원 기능·담당자 승인·지식 정본 반영 — NOT_RUN

문서 정적 검증 PASS는 구현·표준 적합성·설치본 호환성·운영 시험 PASS를 의미하지 않음.
