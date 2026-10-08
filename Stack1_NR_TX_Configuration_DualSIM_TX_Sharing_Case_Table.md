# Stack1 NR TX Configuration 기준 1차 Case Table

현재 단계에서는 **Dual SIM 정책을 결정하기 전에 Stack1(NR)의 UL TX 형태를 빠짐없이 펼쳐 놓는 테이블**로 정리한다.

특히 `PCell 2TX + SCell 2TX` 같은 경우를 단순히 4TX로 해석하지 않도록, **CC별 TX Configuration**과 **실제 Stack1 TX Resource 관점**을 분리한다.

| Case | Stack1 Feature / Mode | PCell TX | SCell#1 TX | SCell#2 TX | TX Configuration 요약 | Stack1 TX Resource 관점 | Peer Stack | TX Sharing / Dual SIM 동작 |
|---|---|---:|---:|---:|---|---|---|---|
| C1 | NR Single UL | 1TX | - | - | **PCell 1TX** | 1TX | LTE 1TX / NR 1TX | **TBD** |
| C2 | UL MIMO | 2TX | - | - | **PCell 2TX** | 2TX | LTE 1TX / NR 1TX | **TBD** |
| C3 | UL CA | 1TX | 1TX | - | **PCell 1TX + SCell 1TX** | 2TX | LTE 1TX / NR 1TX | **TBD** |
| C4 | UL Tx Switching | 1TX | 2TX | - | **PCell 1TX ↔ SCell 2TX** | Switching Case | LTE 1TX / NR 1TX | **TBD** |
| C5 | UL Tx Switching | 2TX | 1TX | - | **PCell 2TX ↔ SCell 1TX** | Switching Case | LTE 1TX / NR 1TX | **TBD** |
| C6 | UL Tx Switching | 2TX | 2TX | - | **PCell 2TX ↔ SCell 2TX** | Switching Case | LTE 1TX / NR 1TX | **TBD** |
| C7 | UL 3CC | 1TX | 1TX | 1TX | **PCell 1TX + SCell#1 1TX + SCell#2 1TX** | 3TX | LTE 1TX / NR 1TX | **TBD** |

## 검토 시 주의사항

C4~C6은 `PCell TX + SCell TX = Stack1 TX 개수`로 단순 합산하지 않는다.

UL Tx Switching 동작이므로 실제 Dual SIM 정책 검토 시에는 다음 항목을 별도로 확인한다.

- 현재 어느 UL path가 활성화되어 있는지
- 해당 시점에 실제 몇 개의 physical TX resource를 점유하는지
- Peer Stack이 1TX를 요청했을 때 TX Sharing이 필요한지
- Sharing이 필요한 경우 Stack1에서 어떤 TX를 Release/Share할지
- Sharing 이후 Stack1의 최종 TX 상태가 무엇인지

## 다음 단계 검토용 확장 구조

`Stack1 Configuration → 현재 Active TX 수 → Stack2 1TX 요청 → Sharing 필요 여부 → Stack1에서 어떤 TX를 Release/Share할지 → 결과 Stack1 TX 상태`

우선 C2부터 Case별로 TX Sharing / Dual SIM 동작을 결정해 나가는 방식으로 검토한다.
