# L1 Knowledge 분석 항목 분류 검토 — 사내 GPT 1차 검토 프롬프트

- 문서: `r0001 / 2026-11-13 KST`
- 대상: `NR BCH (L1 Channel)` / `NR L1 Tx` / `LTE ChCfg (L1 Channel)` / `LTE L1 Tx` (4개)
- 입력 정본 후보: Confluence 이관용 `L1 NR/LTE Procedure·Feature 분류표 v0.8` (본문에 **전체 삽입**)
- 실행 모드: `READ_ONLY / CLASSIFICATION_REVIEW_ONLY`
- 산출물 목적: 담당자 협의·주관 회의·후속 `l1-knowledge-updater` 활용에 앞서 분석 **아이템의 적절성, 누락, 분류 기준**을 검토
- 전제: **담당자 검토가 완료됐다는 의미가 아님**. v0.8은 초안이며 이전 v0.6과의 완전한 1:1 대조는 미검증

---

## 1. 귀하의 역할 및 1차 검토 범위

당신은 무선 모뎀 **LTE/NR L1 소프트웨어 및 3GPP 절차**를 이해하는 사내 검토자입니다. 아래 4개 모듈의 전체 분류표를 읽고, 실제 지식 업데이트를 시작하기 전 **어떤 Procedure/Feature 아이템을 수집해야 하는지**를 검증하세요.

**이번 검토의 최우선 과제:**

1. 각 모듈의 **Procedure / Feature 대분류와 세부 항목에 누락**이 있는가?
2. 항목명이 **3GPP 절차 이름과 L1 구현 하위 흐름을 혼동**하고 있지 않은가?
3. Procedure(A: 통신 사건·절차 흐름)와 Feature(B: 공통 구현 기술·능력)의 **분류가 올바른가**? 예: 단순 `Tx Resource` 자체는 통상 기술 Feature이며, 특정 자원 변경 절차 중 수행되는 단계는 Procedure의 세부 시나리오가 될 수 있음.
4. 하나의 항목이 너무 넓거나 좁아 분해·병합할 필요가 있는가? 동일한 기술의 Procedure / Feature **교차 등록은 허용**하되, 완전히 같은 설명을 중복 저장하도록 유도하지 않는가?
5. 현재 분석 대상이 되는 기능 중 **모듈 고유의 중요 시나리오**가 빠졌는가? 지원 여부 미확인 항목을 억지로 사실로 확정하지 않았는가?

**이번 범위에서 제외:** 모듈 간 상세 인터페이스 계약, 공식 오너 할당, 소스 코드 변경, 구현, 테스트, MSC 생성, 지식 문서 실제 쓰기, Job 실행, GitHub/Confluence 게시 및 스킬 패키징·설치. 외부 시스템 또는 운영 저장소를 수정하지 마세요.

## 2. 필수 분류·담당 경계 (사용자가 제공한 기준)

| 모듈 | 사용자 지정 분석 중심 | 주의할 경계 |
|---|---|---|
| **NR BCH (`BCH_CTRLR`)** | 명칭은 BCH이지만 실제 역할은 **NR L1 Channel Controller**. RRC/L1 DL·UL Channel Config, SCell Configuration/Activation/Deactivation/Release, BWP Switching 등 | PBCH만 담당하는 좁은 모듈로 해석하지 않음. Cell Search·Measurement는 Measure Controller, Idle DRX/CDRX 본체는 DRX Controller 소유 |
| **NR L1 Tx** | UL 송신 설정·Tx Resource·Tx Antenna/Path Switching, SCell의 **UL Tx 관련 참여 구간** | SCell 전체 관리자가 아님. **UL Tx Switching, SRS Carrier Switching**은 관련 Procedure의 조건부 하위 흐름. **CDRX 연동**만 분류(일반 DRX 소유 아님) |
| **LTE ChCfg** | NR BCH에 대응하는 **LTE L1 Channel Configuration** 동작. LTE RRC·PCell/SCell/CA와 DL·UL Channel Config | NR 고유 BWP Switching을 LTE로 복제하지 않음 |
| **LTE L1 Tx** | LTE UL 송신·RF/BB Tx 자원·Tx Path 및 SCell UL 참여, EN-DC 연동 | NR에서 지원한 기능이 LTE에서도 구현됐다고 단정하지 말 것 |

**별도 확인할 중요 항목:** NR L1 Tx의 **NRDC → BB TX Reconfig, F1 Rank Change**; **UL CA → SLO, RF Tx Configuration**; **Dual SIM → Tx Sharing, BB Tx Change**. NRDC는 EN-DC와 별도 범주. `SLO`, `F1 Rank Change`, `BB TX Reconfig`와 `BB Tx Change`의 정확한 사내 정의·실행 조건은 실제 근거 없이 추정하지 마세요.

**SCell 표기 주의:** DL/UL Config/Activation/Deactivation/Release는 모듈 안에서 나뉘는 *L1 처리 범위*를 표현한 것입니다. 3GPP에서 DL/UL Activation이 각각 별도의 독립 네트워크 이벤트로 존재한다고 단정하면 안 됩니다. **Paging을 NR BCH의 독립 Procedure로 재도입하지 마세요**. PBCH/MIB 획득은 Initial Access 맥락의 세부 동작과 기술 분류에서 다룰 수 있지만 독립 상위 Procedure로 강제하지 마세요.

## 3. 정확한 검토 방법

**3.1 Procedure와 Feature 정의**

- `Procedure`: 3GPP RRC/MAC/PHY 동작에서 시작하는 통신 시퀀스 또는 그 절차에 대해 담당 모듈이 실제 수행하는 L1 처리 단계. 대분류는 가급적 규격 용어를 사용하되, `NRDC`, `Dual SIM`, `Connected UL Tx`, `ULCA`처럼 **기술 맥락/시나리오를 묶는 실무 범주**는 `3GPP 규정된 단일 Procedure`라고 부르지 말고 별도 표시.
- `Feature`: 둘 이상의 절차에서 재사용될 수 있는 기능·알고리즘·자원/설정/상태·PHY/RF/HAL 인터페이스. 예: RF Tx Configuration, SRS Carrier Switching 기술 구현, Channel Resource State, Tx Switching 알고리즘.
- 하나의 기능이 양쪽에 등장할 수 있으나 `Procedure` 쪽은 **언제/왜/어떤 흐름**, `Feature` 쪽은 **설정·상태·제약·구현 원리**를 분석하는 것이 목적.
- 현재 사용자 관심은 **아이템 목록의 완전성**이며 모듈 간 소유권 관계 도식화는 후속 단계. 필요 시 최소한의 경계만 지적.

**3.2 각 검토 항목의 판정**

- `유지`: 현재 항목·위치 적절.
- `명칭 수정`: 용어 불명확 또는 3GPP 의미와 혼동.
- `Procedure↔Feature 이동`: 분류 축이 맞지 않음.
- `분리/병합`: 하위 아이템 수준 조정.
- `추가`: 누락된 분석 항목 제안.
- `제외 후보`: 모듈 관련성이 낮거나 사용자 기준에서 분명히 제외되는 동작.
- `판정 보류`: 실제 코드·사내 기능 정의를 확인해야 판단 가능.

근거 수준을 `E3=실제 코드/프로젝트 근거 확인`, `E2=사용자가 제공한 명시적 모듈 역할`, `E1=3GPP 일반 정의 및 설계 추론`, `E0=미확인 가설`로 명시하세요. 원본·실측 자료를 제공받지 않았다면 **E3를 사용하지 마세요**. 표에 '코드 확인'이 있는 것은 구현 증명이 아니라 확인 과제입니다. 3GPP 표준 절차와 사내 클래스 책임을 별개로 판단하고, 코드 접근이 불가능하면 그 사실을 명시하세요.

**3.3 원본 보존**

- 아래 v0.8에는 **A 성격의 Procedure 하위 시나리오 97개, B 성격의 Feature 하위 항목 84개(총 181개)**가 있습니다. `모듈/대분류/세부 항목` 계층을 유지하세요.
- 4열 `Module | Owner | Progress | Update source or contents`는 **양식 고정**. 후반 3열은 지금은 전부 공백이며, 검토 중 임의 작성·가정 금지. 신규 권고 분류표를 만들더라도 같은 형식으로 유지.
- 항목마다 `모듈/대분류/세부`까지 식별해 변경을 제안하고, **원본 행을 삭제하거나 수정한 것처럼 표시하지 마세요**. 실제 원본 수정은 사용자 승인 후.
- v0.6 원본이 제공되지 않았다면 v0.6↔v0.8의 1:1 동일성을 검증했다고 말하지 마세요.

## 4. 응답 형식 (표 중심 · 수정 필요 항목 우선)

아래 순서를 따르되 **전체 181행의 단순 재출력은 생략**하고 실질적인 오류·누락을 중점 보고하세요.

**① 모듈별 분류 완전성 진단**

| Module | Procedure 분류 평가 | Feature 분류 평가 | 핵심 누락·중복·용어 위험 | 근거 수준 |
|---|---|---|---|---|
| NR BCH (L1 Channel) | | | | |
| NR L1 Tx | | | | |
| LTE ChCfg (L1 Channel) | | | | |
| LTE L1 Tx | | | | |

**② 수정·이동·병합·제외 제안 (기존 항목 델타)**

| Module | 현재 Procedure/Feature · 대분류 · 항목 | 판정 | 권고 명칭/위치 | 이유 및 예상 영향 | 근거 수준 |
|---|---|---|---|---|---|

**③ 신규 추가 후보 (누락 항목)**

| Module | Procedure/Feature | 제안 대분류 | 누락된 시나리오·기술 | 추가해야 하는 이유 | 근거 수준 |
|---|---|---|---|---|---|

**④ 판정 보류 / 사내 확인 질문**

| Module | 확인 대상 | 확인해야 하는 정확한 질문 | 필요 근거 | 확정 전 상태 |
|---|---|---|---|---|

**⑤ 최종 의견**

- `READY_FOR_OWNER_REVIEW` / `NEEDS_CORRECTION_BEFORE_OWNER_REVIEW` / `INSUFFICIENT_EVIDENCE` 중 하나를 추천하고 이유를 3~5문장으로 설명.
- 우선 수정할 중요 오류 상위 5개를 추천. **임의로 완료/실행/배포 PASS 선언 금지**.
- 수정이 필요하면 **원본 대비 변경 제안만** 제출. 담당자가 Confluence에 직접 옮길 수 있는 수정된 전체 테이블은 별도 요청을 받은 경우에만 제공.
- 사내 코드, 경로, 로그, 고객 정보, 스크린샷, 영업비밀, 키/토큰 등은 외부로 복사하거나 답변에 인용하지 마세요. 외부 전달이 필요하면 반출 가능한 비민감 **범주형/요약형 결과**로만 정리.

## 5. 입력 데이터 — Confluence용 v0.8 전체 분류표 (내용 고정)

> 다음 테이블은 담당자가 검토할 **초안 입력**입니다. 아직 분류 정확성·기능 구현 검증이 끝난 확정본이 아닙니다.

| Module | Owner | Progress | Update source or contents |
|---|---|---|---|
| **NR BCH (L1 Channel) / Procedure** | | | |
| ↳ **Initial Access / Attach** | | | |
| 　　• Cell synchronization 완료 이후 PBCH/MIB 수신 설정·획득 연동 | | | |
| 　　• Initial Access 관련 L1 채널 초기 설정 | | | |
| ↳ **System Information Acquisition** | | | |
| 　　• SIB1 수신·복호 관련 L1 설정 | | | |
| 　　• 기타 SIB/SI 수신 설정 및 변경 적용 | | | |
| 　　• System Information 갱신/재획득 | | | |
| ↳ **RRC Reconfiguration** | | | |
| 　　• RRC 전달 DL 채널 설정 적용 | | | |
| 　　• RRC 전달 UL 채널 설정 적용 | | | |
| 　　• RRC 재설정 시 L1 채널 자원 변경 | | | |
| ↳ **Mobility / Handover** | | | |
| 　　• Target Cell L1 채널 설정 준비·적용 | | | |
| 　　• Handover 이후 L1 채널 재설정 | | | |
| ↳ **Cell Change / Recovery** | | | |
| 　　• Cell Reselection 결과에 따른 채널 설정 변경 연동 | | | |
| 　　• Cell Change 시 L1 채널 재초기화 | | | |
| ↳ **Release / Suspend / Resume** | | | |
| 　　• L1 채널 Release 및 자원 정리 | | | |
| 　　• Suspend/Resume 관련 채널 상태 복원 (코드 확인) | | | |
| ↳ **Exception / Recovery** | | | |
| 　　• 채널 설정 실패·Timeout 처리 | | | |
| 　　• MIB/SIB 수신 실패와 L1 복구 연동 | | | |
| ↳ **BWP Switching** | | | |
| 　　• RRC 기반 BWP 설정·전환 | | | |
| 　　• DCI 기반 Active BWP 전환 연동 | | | |
| 　　• BWP Inactivity Timer 기반 전환 연동 | | | |
| 　　• BWP 전환 시 DL/UL 채널 설정 및 상태 반영 | | | |
| ↳ **SCell Config / Activation / Deactivation / Release** | | | |
| 　　• DL SCell Configuration | | | |
| 　　• UL SCell Configuration | | | |
| 　　• DL SCell Activation | | | |
| 　　• UL SCell Activation | | | |
| 　　• DL SCell Deactivation | | | |
| 　　• UL SCell Deactivation | | | |
| 　　• DL SCell Release | | | |
| 　　• UL SCell Release | | | |
| **NR BCH (L1 Channel) / Feature** | | | |
| ↳ **L1 Channel Configuration** | | | |
| 　　• DL/UL Physical Channel 설정 파라미터 | | | |
| 　　• RRC → L1 Configuration 매핑·적용 조건 | | | |
| 　　• 채널 Config/Reconfig 순서 및 의존성 | | | |
| ↳ **PBCH / MIB / System Information** | | | |
| 　　• PBCH/MIB 수신 관련 채널 설정·결과 처리 | | | |
| 　　• SIB1/SI 수신 설정·결과 연동 | | | |
| ↳ **BWP / CC / SCell Resource** | | | |
| 　　• Active DL/UL BWP 상태·설정 | | | |
| 　　• PCell/SCell 채널 자원 설정 | | | |
| 　　• SCell Config/Act/Deact/Release 시 자원 전이 | | | |
| ↳ **Interface** | | | |
| 　　• RRC ↔ BCH 제어/결과 인터페이스 | | | |
| 　　• Measure Controller 결과 입력 인터페이스 | | | |
| 　　• DRX Controller와 채널 설정 연동 경계 | | | |
| 　　• PHY/HAL 설정 명령 및 응답 | | | |
| ↳ **State Management** | | | |
| 　　• 채널 Config/Active/Release 상태 전이 | | | |
| 　　• SCell Activation/Deactivation 상태 | | | |
| 　　• BWP Switching 트리거별 상태 변경 | | | |
| ↳ **Timing / Scheduling** | | | |
| 　　• 채널 설정 적용 시점·동기화 | | | |
| 　　• BWP/SCell 변경의 타이밍 제약 | | | |
| 　　• 설정 요청과 PHY 적용 순서 | | | |
| ↳ **Recovery / Diagnostics** | | | |
| 　　• 설정 Timeout/실패 감지·복구 | | | |
| 　　• MIB/SIB 관련 실패 분류 | | | |
| 　　• 상태 추적 로그·원인 분석 포인트 | | | |
| **NR L1 Tx / Procedure** | | | |
| ↳ **Initial Access / UL Transmission** | | | |
| 　　• PRACH 송신 경로·파라미터 설정 연동 | | | |
| 　　• Msg3/초기 PUSCH 송신 설정 | | | |
| ↳ **RRC Reconfiguration** | | | |
| 　　• UL Tx 설정 변경 반영 | | | |
| 　　• 상위 채널 설정 변경에 따른 Tx 자원 재구성 | | | |
| ↳ **UL CA / SCell 참여** | | | |
| 　　• UL SCell Configuration 중 Tx 관련 설정 | | | |
| 　　• UL SCell Activation 중 Tx 관련 처리 | | | |
| 　　• UL SCell Deactivation 중 Tx 관련 처리 | | | |
| 　　• UL SCell Release 중 Tx 자원 정리 | | | |
| 　　• UL Tx Switching (조건부) | | | |
| 　　• SRS Carrier Switching (조건부) | | | |
| 　　• SLO (사내 정의 확인) | | | |
| 　　• RF Tx Configuration | | | |
| 　　• UL CA 동작 중 Tx Path 전환 | | | |
| ↳ **EN-DC** | | | |
| 　　• LTE/NR 동시 송신 시 NR Tx 설정 연동 | | | |
| 　　• EN-DC Tx 자원 공유·경로 전환 | | | |
| ↳ **Mobility / Handover** | | | |
| 　　• Mobility 시 UL Tx 경로 및 설정 재구성 | | | |
| ↳ **Connected Mode UL Tx** | | | |
| 　　• Tx Antenna Switching | | | |
| 　　• Tx Path Switching | | | |
| 　　• Tx Chain/BB Tx 자원 재할당 (코드 확인) | | | |
| ↳ **CDRX 연동** | | | |
| 　　• CDRX 진입·복귀에 따른 UL Tx 동작 연동 | | | |
| ↳ **Exception / Recovery** | | | |
| 　　• UL Tx 설정 실패 및 경로 복구 | | | |
| 　　• Tx Switching 실패·재시도 처리 | | | |
| ↳ **NRDC** | | | |
| 　　• BB TX Reconfiguration | | | |
| 　　• F1 Rank Change (사내 의미 확인) | | | |
| ↳ **Dual SIM** | | | |
| 　　• Tx Sharing | | | |
| 　　• BB Tx Change | | | |
| **NR L1 Tx / Feature** | | | |
| ↳ **UL Physical Channel** | | | |
| 　　• PUSCH/PUCCH/PRACH 송신 설정 | | | |
| 　　• UL Physical Channel 송신 경로별 동작 | | | |
| ↳ **Reference Signal / SRS** | | | |
| 　　• SRS 송신 설정 및 자원 | | | |
| 　　• SRS Carrier Switching의 트리거·제약 | | | |
| 　　• DMRS 관련 Tx 설정 (코드 확인) | | | |
| ↳ **Tx Resource** | | | |
| 　　• Tx Antenna / RF Path / Tx Chain Allocation | | | |
| 　　• UL CA/NRDC/Dual SIM 자원 공유·우선순위 | | | |
| 　　• BB Tx Resource 할당·해제 | | | |
| ↳ **Tx Switching** | | | |
| 　　• UL Tx Switching 결정 조건·상태 | | | |
| 　　• Tx Antenna Switching 알고리즘·조건 | | | |
| 　　• Tx Path Switching 알고리즘·조건 | | | |
| 　　• SRS Carrier Switching 구현 및 복귀 | | | |
| 　　• Dual SIM Tx Sharing 충돌·우선순위 | | | |
| ↳ **Tx Configuration** | | | |
| 　　• RF Tx Configuration | | | |
| 　　• BB TX Reconfig (NRDC) | | | |
| 　　• BB Tx Change (Dual SIM) | | | |
| 　　• F1 Rank Change (NRDC; 사내 정의 확인) | | | |
| 　　• SLO (ULCA; 사내 정의 확인) | | | |
| ↳ **Interface** | | | |
| 　　• L1 Channel Controller ↔ Tx 설정/이벤트 | | | |
| 　　• TxCfgMngr/TxSwitchMngr ↔ HAL/RF 인터페이스 | | | |
| 　　• PHY 송신 설정·결과 인터페이스 | | | |
| ↳ **State / Recovery** | | | |
| 　　• UL Tx 및 Tx Path 상태 관리 | | | |
| 　　• CDRX 연동 시 UL Tx 상태 전이 | | | |
| 　　• RF/BB 설정 실패 진단·복구 | | | |
| **LTE ChCfg (L1 Channel) / Procedure** | | | |
| ↳ **Initial Access / Attach** | | | |
| 　　• LTE PBCH/MIB 획득 관련 L1 채널 설정 | | | |
| 　　• Initial Access용 DL/UL 채널 초기 설정 | | | |
| ↳ **System Information Acquisition** | | | |
| 　　• LTE SIB1/SI 수신 관련 채널 설정 | | | |
| 　　• System Information 변경·갱신 처리 | | | |
| ↳ **RRC Reconfiguration** | | | |
| 　　• LTE RRC 전달 DL 채널 설정 적용 | | | |
| 　　• LTE RRC 전달 UL 채널 설정 적용 | | | |
| 　　• L1 채널 자원 재설정 | | | |
| ↳ **SCell Config / Activation / Deactivation / Release** | | | |
| 　　• DL SCell Configuration | | | |
| 　　• UL SCell Configuration | | | |
| 　　• DL SCell Activation | | | |
| 　　• UL SCell Activation | | | |
| 　　• DL SCell Deactivation | | | |
| 　　• UL SCell Deactivation | | | |
| 　　• DL SCell Release | | | |
| 　　• UL SCell Release | | | |
| ↳ **Mobility / Handover** | | | |
| 　　• Target Cell 채널 설정 및 Handover 연동 | | | |
| 　　• Cell Change 후 채널 설정 변경 | | | |
| ↳ **PCell / CC Reconfiguration** | | | |
| 　　• PCell 관련 채널 설정 변경 | | | |
| 　　• CA 구성 CC 추가·제거에 따른 채널 설정 반영 | | | |
| ↳ **EN-DC LTE Anchor 연동** | | | |
| 　　• EN-DC LTE 측 채널 설정·재설정 | | | |
| 　　• NR 연동을 위한 LTE 채널 설정 변경 | | | |
| ↳ **Release / Exception / Recovery** | | | |
| 　　• LTE L1 채널 해제·자원 정리 | | | |
| 　　• 채널 설정 실패·Timeout 복구 | | | |
| **LTE ChCfg (L1 Channel) / Feature** | | | |
| ↳ **LTE Channel Configuration** | | | |
| 　　• DL/UL Physical Channel 설정 파라미터 | | | |
| 　　• LTE RRC → L1 설정 매핑 | | | |
| 　　• Channel Config/Reconfig 적용 순서 | | | |
| ↳ **MIB / SIB / System Information** | | | |
| 　　• LTE MIB 관련 채널 설정·결과 처리 | | | |
| 　　• LTE SIB/SI 수신 설정·갱신 연동 | | | |
| ↳ **PCell / SCell / CC Resource** | | | |
| 　　• PCell/CC 설정·유지 | | | |
| 　　• SCell Config/Act/Deact/Release 자원 상태 | | | |
| 　　• DL/UL CA 채널 설정·리소스 | | | |
| ↳ **Interface** | | | |
| 　　• RRC ↔ ChCfg 제어·상태 인터페이스 | | | |
| 　　• Measure/DRX Controller 연동 경계 | | | |
| 　　• PHY/HAL 설정 명령·결과 | | | |
| ↳ **State Management** | | | |
| 　　• PCell/SCell 채널 상태 전이 | | | |
| 　　• Config/Active/Deactive/Release 상태 관리 | | | |
| 　　• EN-DC LTE Anchor 설정 상태 (코드 확인) | | | |
| ↳ **Timing / Scheduling** | | | |
| 　　• 채널 설정 타이밍 및 적용 시점 | | | |
| 　　• SCell Activation/Deactivation 타이밍 | | | |
| 　　• Handover 시 채널 설정 순서 | | | |
| ↳ **Recovery / Diagnostics** | | | |
| 　　• 설정 Timeout/실패 처리 | | | |
| 　　• 채널 재설정·해제 시 정합성 검증 | | | |
| 　　• 상태/오류 로그 분석 포인트 | | | |
| **LTE L1 Tx / Procedure** | | | |
| ↳ **Initial Access / UL Transmission** | | | |
| 　　• PRACH 송신 설정 및 경로 초기화 | | | |
| 　　• Msg3/초기 PUSCH 송신 설정 | | | |
| ↳ **UL Tx Configuration** | | | |
| 　　• RRC 구성에 따른 UL Tx 파라미터 반영 | | | |
| 　　• UL 송신 자원·BB/RF 설정 변경 | | | |
| ↳ **UL CA / SCell 참여** | | | |
| 　　• UL SCell Configuration 중 Tx 설정 | | | |
| 　　• UL SCell Activation 중 Tx 처리 | | | |
| 　　• UL SCell Deactivation 중 Tx 처리 | | | |
| 　　• UL SCell Release 중 Tx 자원 정리 | | | |
| 　　• UL CA Tx 자원 재할당 및 경로 전환 | | | |
| ↳ **UL Tx Resource** | | | |
| 　　• PCell/SCell Tx 자원 구성 | | | |
| 　　• Power/Tx Chain 자원 제약 연동 (코드 확인) | | | |
| ↳ **Tx Antenna / Path Switching** | | | |
| 　　• Tx Antenna Switching (실제 지원 여부 확인) | | | |
| 　　• Tx Path Switching | | | |
| 　　• RF Tx Configuration 연동 | | | |
| ↳ **EN-DC** | | | |
| 　　• LTE/NR 동시 송신 시 LTE Tx 자원·경로 조정 | | | |
| 　　• EN-DC Tx Sharing/전환 연동 | | | |
| ↳ **Dual SIM** | | | |
| 　　• Tx Sharing (실제 지원 여부 확인) | | | |
| 　　• BB Tx Change (실제 지원 여부 확인) | | | |
| ↳ **Exception / Recovery** | | | |
| 　　• UL Tx 경로·설정 실패 복구 | | | |
| 　　• Tx Resource Release 및 재초기화 | | | |
| **LTE L1 Tx / Feature** | | | |
| ↳ **UL Physical Channel** | | | |
| 　　• LTE PRACH/PUSCH/PUCCH 송신 설정 | | | |
| 　　• UL Tx 파라미터·채널별 동작 | | | |
| ↳ **Reference Signal / SRS** | | | |
| 　　• LTE SRS 송신 설정·리소스 | | | |
| 　　• UL CA 관련 SRS 송신 연동 (코드 확인) | | | |
| ↳ **Tx Resource** | | | |
| 　　• RF Path/Tx Chain/BB Tx 자원 할당 | | | |
| 　　• PCell/SCell UL Tx Resource 관리 | | | |
| 　　• EN-DC 및 Dual SIM 자원 제약 | | | |
| ↳ **Tx Switching** | | | |
| 　　• Tx Path Switching 결정·실행 | | | |
| 　　• Tx Antenna Switching (지원 여부 확인) | | | |
| 　　• Tx Sharing/우선순위·충돌 처리 | | | |
| ↳ **Tx Configuration** | | | |
| 　　• RF Tx Configuration | | | |
| 　　• BB Tx Change (코드 확인) | | | |
| 　　• UL CA 송신 자원 재구성 | | | |
| ↳ **Interface** | | | |
| 　　• LTE ChCfg ↔ L1 Tx 설정 인터페이스 | | | |
| 　　• TxCfgMngr/TxSwitchMngr ↔ RF/HAL 인터페이스 | | | |
| 　　• EN-DC LTE/NR Tx 연동 인터페이스 | | | |
| ↳ **State / Recovery** | | | |
| 　　• UL Tx/Tx Path 상태 전이 | | | |
| 　　• 설정 실패·Tx Resource 복구 | | | |
| 　　• Release 및 재초기화 상태 관리 | | | |


---

## 6. 종료 조건

- 네 모듈의 **Procedure/Feature 각각**을 검토하고, 수정을 제안할 때 해당 원문 행을 정확히 식별했는가?
- `누락 검토`와 `구현 증명`을 구별했는가?
- 원본 Confluence 표의 **Owner / Progress / Update source or contents 공백**을 유지했는가?
- 코드/문서/검토 근거가 없는 사내 기능 명칭을 단정하지 않았는가?
- 이번 단계에서 `l1-knowledge-updater` 실행 또는 Knowledge 정본 갱신을 수행하지 않았는가?

최종 답변은 **검토 결과**이며 지식 업데이트 자체가 아닙니다. 실제 코드 기반 분석 계획·MSC·그룹 Knowledge 변경은 검토 결과를 사용자에게 전달하고 후속 실행을 명시적으로 요청받은 뒤 별도로 진행하세요.
