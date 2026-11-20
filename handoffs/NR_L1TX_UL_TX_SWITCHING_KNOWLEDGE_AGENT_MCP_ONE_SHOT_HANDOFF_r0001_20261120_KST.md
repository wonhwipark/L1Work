# 업무 GPT 실행 인계 — NR L1 Tx UL Tx Switching Knowledge 실사용 1건

- 개정: r0001 / 2026-11-20 KST
- 전달: `wonhwipark/L1Work`, branch `main`, `handoffs/NR_L1TX_UL_TX_SWITCHING_KNOWLEDGE_AGENT_MCP_ONE_SHOT_HANDOFF_r0001_20261120_KST.md`
- 실행 대상: 연결이 허용된 모바일 Agent → 실제 Linux MCP → 업무 GPT/실행 LLM → 설치된 기존 L1 스킬
- **사용자 최종 목표:** `l1-knowledge-updater`로 **NR L1 Tx / UL Tx Switching**의 기존 지식·소스 구현을 검토하고, **개인 업무용 `l1-workspace`에 검증된 분석 및 지식 초안을 저장·갱신한 다음, 저장된 결과를 다시 조회하여 사용자에게 보여주기**.
- 상태: 실행 인계서. **문서 게시 자체는 Agent/MCP 실행·Knowledge 저장·호스트 적용이 아님**.

## 1. 기존 MCP 공통 인계와 이번 단일 수락 사례

[기존 Linux MCP 업무 스킬 접근 인계 r0002](L1_MCP_AGENT_SKILL_ACCESS_AND_CAPABILITY_HANDOFF_r0002_20261120_KST.md)의 범용 기능 매핑을 대체하거나 처음부터 MCP를 재설계하지 않는다. 이번 요청은 그 연결로 **실제 Updater 분석 → Workspace 저장 → 재조회 → 사용자 결과 반환**을 끝까지 입증하는 대표 시나리오다. 별도 Viewer UI, 그룹 지식 게시, 신규 스킬 패키지·운영 설치/재시작, 제품 C++ 변경은 이번 목표가 아니다.

업무용 `l1-workspace`와 `l1sw-dev-knowledge`의 실제 저장소·호스트는 현장의 기존 설정/계약으로 확인한다. 이름이 비슷한 GitHub.com 저장소를 정본으로 추정하거나 공개 저장소에 회사 자료를 복사하지 않는다.

## 2. 수행 순서 — 이미 승인·설치된 기존 기능 우선

1. **대상/도구 확인:** Agent가 실제로 접근 가능한 MCP `tools/list`, 대상 Linux 호스트 identity, 권한, 설치·로드된 `l1-knowledge-updater`, `code-analyzer`, 기존 Workspace/Kernel writer·readback 경로를 확인. 이름·인자·API·CLI를 추정하여 호출하지 않는다. 도구가 없으면 `BLOCKED_MCP_TOOL_NOT_EXPOSED` 등 정확한 reason을 보고하고 가상 성공으로 대체하지 않는다.
2. **Work/기존 지식 확인:** `NR L1 Tx → UL Tx Switching` 관련 기존 개인 Work·지식, 기존 Module→Feature→Scenario 분류·revision을 조회하고 **같은 목적의 Work를 우선 재개**한다. 분류 검토표의 번호는 실제 Knowledge ID가 아니므로 기존 지식 ID와 대조한다. 기존 분석·Evidence가 신뢰 가능하면 재분석하지 않고 재사용한다.
3. **Updater 직접 진입:** 설치된 `l1-knowledge-updater`의 실제 허용된 분석 진입점으로 현행 지식의 사실/누락/오류를 검토하고, 부족한 구현 사실은 허용된 `code-analyzer` READ 분석으로 보충한다. 분석 기준 source revision을 고정하고 근거·미확인·추론을 구분한다. 기능 부재가 입증되기 전 새로운 Adapter/Job/Writer를 만들지 않는다.
4. **좁은 분석 범위:** UL Tx Switching의 입력 트리거/전제/비실행 조건, 결정 주체와 NR L1 Tx가 담당하는 적용 경계, 상태 전이와 RF/HAL/PHY IPC 전달·완료/실패/해제 처리에서 **소스로 확인되는 내용만** 기술한다. 공통 NR/LTE 관리 계층과 NR 전용 처리의 책임을 구분한다. Tx Antenna/SRS Carrier Switching, UL CA·EN-DC·Dual SIM은 실제 관련성이 입증된 경우에만 조건부 Scenario/참조로 연결하고 별도 기능 지식까지 자동 확대하지 않는다.
5. **Workspace 갱신:** 기존 Workflow/Kernel 허용 writer를 재사용하여 같은 `l1-workspace` Work에 (a) 기존 지식 검토 결과 (b) 코드 사실 및 source revision (c) 수정/신규 지식 초안 (d) 근거/미확인 (e) 사용 스킬과 분석 Run/Evidence (f) 기존 문서와의 차이·검토 결정을 기록한다. 이미 존재한 문서·다른 스킬의 이력은 덮어쓰지 않으며 writer 충돌·revision 보호를 적용한다. **사용자는 개인 Workspace 갱신을 요청했으며 그룹 `l1sw-dev-knowledge`에 대한 자동 게시 승인으로 해석하지 않는다.**
6. **읽기 검증 및 결과 회수:** 저장 결과를 동일 Work ID와 revision으로 재조회. 저장 요청 응답만으로 `PASS`를 선언하지 않고, 실제 변경 문서 경로/commit 또는 저장 revision/내용 readback을 대조한다. 자료 반출 정책 안에서 사용자에게 제목, 핵심 변경점, 누락·미확인, 변경 전후 비교, 저장 위치·검증 상태를 반환한다. 회사 코드·상세 MSC·로그·고객자료·비밀은 업무 호스트의 허용 경로에만 남긴다.

## 3. 최소 결과 — 사용자에게 보여줄 표

| 확인 항목 | 반환 내용 |
|---|---|
| 실행 경로 | 실제 Agent/MCP 도구·권한·호스트 검증 여부 |
| 기존 Knowledge | 조회 범위, 기존 문서/Work 식별자, 기존 revision(허용 범위) |
| 분석·검토 | source revision, 구현 근거 확보 여부, 기존 지식과 비교한 수정/보완 요약 |
| Workspace 갱신 | 생성/갱신/변경 없음, Work ID, 문서 경로 또는 링크, 실제 저장 revision |
| 결과 재조회 | READBACK `PASS / FAIL / NOT_RUN`, 재조회 근거 |
| 미확인·차단 | 첫 차단 단계, reason code, 추가 권한/승인 필요 여부 |
| 다음 조치 | 이번 사례의 다음 행동 한 개 |

시험은 `PASS / FAIL / SKIP / NOT_RUN`; 운영 관측은 `NOT_VERIFIED / BLOCKED`를 구분한다. 작업이 부분적으로 실패하면 이미 검증된 단계의 결과는 보존하고 실패한 단계만 정확히 보고한다.

## 4. 실행·승인 경계 및 종료 조건

- 사용자의 이 요청은 **NR L1 Tx UL Tx Switching 1건의 검토 및 개인 Workspace 저장·결과 조회** 범위다. 제품 코드 수정, 그룹 지식 게시, 신규 운영 설치·설정/서비스 재시작, 공개 게시, 모델의 신규 유료 호출은 유효한 기존 승인 범위를 확인하지 않고 실행하지 않는다.
- 기존 승인된 읽기·분석·저장 인터페이스가 실제로 있으면 **중간 설계 보고서만 작성하고 멈추지 말고** 해당 범위에서 Workspace readback과 결과 표시까지 진행한다.
- 기존 Job ID/Receipt 재사용·자동 재큐잉·불확실 실행 재시도 금지. 비용/중복/권한/timeout 게이트 준수. 추가 승인이나 기능 연결이 필요하면 승인되지 않은 부분만 `BLOCKED`로 보고하고 안전한 선행 단계는 완료한다.
- 사용자에게 MCP 설치본/소스 ZIP·회사 로그 원문을 새로 요청하지 않는다. 업무 GPT와 허용된 로컬 Agent가 자체 접근 가능한 범위에서 G0 확인과 기존 인터페이스 재사용을 진행한다.
- 실행 완료 조건: **실제 Updater(필요한 Analyzer 포함) 결과 + 동일 개인 Work의 저장 revision + 실제 readback + 사용자용 결과 요약**이 하나의 근거 체인으로 확인될 것.

## 5. 업무 GPT 단일 실행 지시

> 이 문서(`wonhwipark/L1Work`, `main`, `handoffs/NR_L1TX_UL_TX_SWITCHING_KNOWLEDGE_AGENT_MCP_ONE_SHOT_HANDOFF_r0001_20261120_KST.md`)를 기준으로, Agent→Linux MCP에서 기존 `l1-knowledge-updater`가 NR L1 Tx UL Tx Switching 지식을 검토하고 개인 `l1-workspace`의 동일 Work에 변경사항·근거를 저장한 뒤 실제 읽기 검증한 결과를 보여 주세요. 기존 Knowledge와 source revision을 먼저 대조하고 소스 확인이 필요하면 허용된 `code-analyzer`를 호출하세요. 별도 그룹 게시/제품 변경/신규 유료 호출/설치 없이 가능한 범위를 끝까지 수행하고, 차단된 단계는 reason과 함께 표시하세요. 실제 저장·조회 근거 없이 완료로 보고하지 마세요.
