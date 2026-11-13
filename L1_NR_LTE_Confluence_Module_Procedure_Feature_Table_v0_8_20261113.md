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
