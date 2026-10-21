# L1_CHANNEL 2026 W42 주간보고 — 통합 보완안

> **TX Sharing Recovery 논의 추가본 (v1.2, 2026-10-22).** W42 취합 초안 사진 3장 + W42 개인 주간보고 사진 4장을 대조해 작성한 v1.0을 기반으로, 사용자가 W41에서 이미 보고했다고 지정한 SAR/TAS 수정 이력을 W42 본문에서 제외. W41 원본은 확보되지 않아 정확한 주차별 변경 비교는 미검증. 사진 바깥의 원문·추가 페이지는 확인하지 못함.
>
> `[보완]`은 개인 주간보고에서 새로 반영한 내용이며, `[확인 필요]`는 원문 추가 확인이 필요한 부분이다.
> **v1.2 변경:** W42 금주 논의 사항으로 TX Sharing 1Tx→2Tx Recovery 및 TX Release 요청 트리거를 개발과제에 추가. 기존 v1.1의 W41 중복 이력 제외 정책은 유지.
> **v1.1 편집 기록:** 기존 `1-1`(SOC-417498/417933/417935 SAR/TAS FunctionType·TxPath 수정)과 `1-2`(SOC-417943 Abnormal Backoff 수정 상세) 삭제. 별개 신규 이슈 `SOC-419988` 유지. `SOC-417943`의 SMP1770 Branch HE 완료(`CL 5366365`)는 W42 화면에 보이나, W41 대비 신규 변화인지 검증할 때까지 본문에는 기재하지 않음.

## 1. 상용과제

### 1-1. SOC-419988 — MMCIF PAL_QUEUE_FULL Crash

- **담당:** 강동국(개인 보고 기준)
- **현상:** MMCIF PAL_QUEUE_FULL Crash (SSS9975XBA-9195).
- **원인:** ST2 HISR에서 `NrSetSarLimitedPolicyIndCb`가 호출될 때 Domain이 지정되지 않아 `MMC_L1C_COMBINED_TAS_INFO_IND`의 Dest Domain이 `0x10`으로 설정됨. ST1 측에서 Abnormal Dest Domain 메시지가 Queue에 누적되어 Queue Full 발생.
- **조치:** Command 생성 시 Object를 추가하여 Callback 함수 호출 시 `MMCIF_CTRLR` Domain을 갖도록 수정.
- **상태:** **CL 5368282 반영 완료. SMP1770 Branch HE 진행 중.**

### 1-2. SOC-416547 — NR Modem OFF 중 RF TX ON / ITMON Crash

- **환경:** SMP1770, Thetis/Solomon.
- **현상:** NR MODEM POWER OFF 상태에서 RF TX ON 실행 시 ITMON Crash.
- **원인:** Multicore 환경에서 TX ON용 HISR가 발생하기 전에 Modem Off 수행. `SetPcellTxPathOnOff`에서 Modem State 확인 없이 TX ON을 진행.
- **진행:** CL 5367029로 1차 반영했으나 FR2 Cal에서 Backout됨. Modem State 확인 방어 코드를 보강한 **CL 5370750 재반영 준비 중**.
- **상태:** 진행 중.

### 1-3. SOC-419447 / SOC-419446 — LTE TX Swap과 2G INT Scheduling 충돌

- **환경:** Solomon.
- **현상:** L2G Gap Measure 중 LTE TX Swap과 충돌하며 2G INT가 지연되어 Schedule 오류·Crash.
- **진행:** LTE TX 담당자가 TX Swap 중 INT Lock 관련 사항 확인 중.
- **상태:** 진행 중.

### 1-4. Terra-5544 / SOC-417072 — RF TX Path Allocation 이관

- **환경:** Terra/Rose/Santa/Papaya.
- **현상:** RF에서 NSA/SA Mode 인식 오류로 TX Path 할당 오류.
- **확인:** 기존 SOC-417072와 동일 이슈임을 로그로 확인. 잘못 배정된 이슈를 SOC-417072로 이관.
- **상태:** **Terra-5544 Duplicated / 완료.**

### 1-5. TERRA-5688 (SSS9975XBA-9202) — 2G Call 종료 후 Sleep 진입 실패

- **환경:** Ulysses/Terra, Crash.
- **현상:** 2G CS Call이 Disconnect된 뒤 GRR IDLE_REQ 미수신으로 Sleep 불가 → Grant Release 실패 → Crash.
- **원인:** 연속적인 Multi-page Concatenated SMS로 인해 상위 비정상 상태 탐지 Timer가 초기화되지 않음.
- **진행:** NAS Signaling이 길어질 경우 WTD(Wait Timer)를 재시작해 비정상으로 판단되지 않도록 GRR/NAS 측 개선 준비 중.
- **상태:** 진행 중.

### 1-6. SOC-416729 — 2G Modem OFF / NR Modem ON HPCM 동시 접근 Crash

- **환경:** Ulysses.
- **현상:** 2G Modem OFF와 NR Modem ON 동시 발생 시 HPCM Component(MARCONI)에 병렬 접근해 MCW 모듈 오류·Crash.
- **원인:** 임계영역 보호 부재.
- **조치:** MCW HPCM On/Off Handler에 `pal_SmSpinLock_IrqSave`/`pal_SmSpinUnlock_IrqRestore` 추가.
- **상태:** **CL 5373662 반영 완료.**

### 1-7. SOC-419903 — 2G DTM / ENCODE NB TASK Crash [보완]

- **담당:** 김광철(개인 보고 기준).
- **환경:** Ulysses, Crash.
- **현상:** 2G DTM 동작 중 Encode NB Task 처리에서 Crash.
- **발생 시퀀스:** DTM Call 중 네트워크 `CHANNEL MODE MODIFY(HR → AMR-WB)` 메시지 수신 → 채널이 `TCH/H(2 burst)`에서 `TCH/F(4 burst)`로 변경 → 음성 버퍼(`ilHandle`) Old Buffer Destroy 후 New Buffer Create → 바로 다음 Frame의 `ENCODE NB TASK` 처리 중 Crash.
- **현재 가설:** 코덱·채널 전환 구간에서 Buffer 재생성과 ENCODE/FORMAT NB Task 스케줄 간 타이밍 연관성이 의심되나 최종 Root Cause 미확정. 기존 초안의 'L2G CSFB 중 DTM' 표현과 세부 조건은 추가 확인 필요.
- **진행:** 재현환경 확보 중, `ENCODENB`/`FORMATNB` Schedule 관련 디버깅 코드 준비 중. 관련 로그 추가 준비.
- **리스크:** 개인 보고 기준 없음.
- **상태:** 진행 중.

### 1-8. SOC-416564 — ROOT Crash / NB Task Invalid Value Access [보완]

- **담당:** 김광철.
- **현상:** NB Task 동작 중 Invalid Value Access로 Crash.
- **진행:** 기존 SOC-310116과 유사함을 확인해 PHY 측 디버깅 요청.
- **상태:** PHY 확인 중.
- **리스크:** 없음(개인 보고 기준).
- **주의:** SOC-416547과 다른 이슈.

### 1-9. SOC-418879 — S952N LGU UL Tput 저하 [보완]

- **담당:** 김민수.
- **현상:** DUT(S952N)가 Serving SSB를 #0으로 선택하는 경우가 있으나 REF(S947N)는 주로 SSB #2를 선택하며, SSB #2 구간에서 UL Tput이 더 좋음.
- **분석:** 특정 시점 SSB #2의 SINR이 우수해도, Serving Cell Power가 Neighbor 대비 약 10 dB 높은 조건에서는 RSRP 중심 Ordering이 정상 동작. SSB #0/#2 간 RSRP 차이가 1 dBm 미만인 환경에서는 네트워크 TCI에 따라 Serving SSB #0 지정 및 UL Tput 저하가 가능.
- **상태:** **Reject 처리.** 동일 현상이 재현되면 Reopen 예정.
- **주의:** 전주에 보고된 룩셈부르크 UL Tput 열세 이슈와 별개.

### 1-10. SOC-418964 — S956B Telenor NR RLF [보완 / 확인 필요]

- **담당:** 김민수.
- **제목:** S956B Telenor 5G SA NR RLF, T310 Expiry.
- **상태/원인/조치:** [확인 필요] 개인 보고 화면 하단에 제목만 보여 후속 내용은 확인 불가.

## 2. 개발과제

### 2-1. TX Sharing — 1Tx → 2Tx Recovery 동작 논의 [W42 신규]

- **배경:** Dual SIM TX Sharing 동작으로 기존 2Tx 구성에서 TX 한 개를 상대 스택에 공유하여 1Tx 상태로 운용하는 경우, 공유 종료 이후 2Tx 구성을 복구하는 동작이 필요함.
- **금주 논의 사항:** **1Tx Sharing 상태 → 2Tx Recovery** 경로를 추가하고, Recovery를 위한 **TX Release 요청 시점**을 다음과 같이 논의함.
  - **TX Suspend 발생 시:** TX Release 요청.
  - **DS-SM 상태가 `CONN → IDLE`로 전환될 때:** TX Release 요청.
- **의도:** 공유 중이던 TX 자원의 점유를 해제하여 1Tx로 축소된 구성의 2Tx 복구가 가능하도록 함.
- **진행 상태:** **Recovery 동작 및 Release 트리거 논의 단계.** 코드 구현, 적용 CL, 2Tx 복구 검증 결과는 제공되지 않아 완료로 표기하지 않음.
- **추가 확인:** TX Release 요청 후 2Tx 재할당·복구의 실행 조건과 순서, 중복 Release 방지, 상대 스택의 점유 종료 판정 및 검증 시나리오는 설계·구현 단계에서 확인 필요.

### 2-2. AI Skill을 통한 Feature 구현 [보완]

- **담당:** 공종욱(사진 상단 표기 기준, 확인 필요).
- **진행률:** 정상 70%.
- **ETA:** 2026-12-31.
- **Feature 구현·리뷰:** `feature-implementation` Skill 기반 코드 작성/리뷰. SOC-414244 SCell TX 중복 Config Recovery에서 Skill로 코드 수정 후 담당 리뷰 진행.
- **Recovery System 설계:** 설계 리뷰에서 불필요한 Counter, OnTick 관련 코드, RegisterReq 관련 복잡성/사용성 피드백 수신. 공통 Skill 개선에 반영.
- **안전장치:** AI 코드 생성 중 임의 판단으로 동작시키는 부분을 발견하고 사용자 질의 후 판단하도록 개선.
- **평가 도구:** `l1sw-implementation-evaluator` Skill 생성 — 순수 AI 생성 코드와 Skill 기반 생성 코드의 비교 평가, SRS가 없는 AI 코드에서 SRS 추출 후 평가하는 기능 추가, NFR 점수 산정 방식 개선 진행.
- **2G Knowledge:** 이슈 기반 Knowledge 추출, `l1sw-dev-knowledge` Skill의 2G 항목에 반영하여 DEV Branch 등록.

## 3. 이슈 관리 및 확인 필요 사항

1. SOC-419903: 'L2G CSFB'와 'DTM Call 중 CHANNEL MODE MODIFY'의 재현 조건 관계, 버퍼 수명 주기/스케줄 충돌 여부를 실제 로그로 확인.
2. SOC-418964: 제목 이외의 상세 현황을 후속 개인 보고 화면에서 확인 후 업데이트.
3. AI Skill 개발 담당은 개인 보고의 시각적 헤더를 기준으로 추정했으므로 원본 문서에서 최종 확인.
4. SOC-419988의 SMP1770 Branch HE 상태를 후속 확인. SOC-417943의 전주 대비 HE 완료 여부는 W41 원본 대조 후 필요 시 금주 변경분만 별도 반영.
5. TX Sharing: TX Suspend 및 DS-SM `CONN → IDLE` 시 TX Release 요청 후 실제 2Tx Recovery 조건·순서, 구현/검증 여부 확인.
6. 기존 W42 초안의 사진 밖 후속 항목은 원문을 추가로 받은 뒤 이어서 통합.
