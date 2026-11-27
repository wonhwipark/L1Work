# L1 Channel Recovery V2 Cause Rule / V3 Search Plan 단계별 구현 인계
- r0001 · 2026-11-27 11:00 KST · 업무 GPT 설계 및 Qwen 구현용
- 기준: [r0007 통합 인계](./L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0007_20261125_KST.md)
- 관련: [V2/V3 원인 분리 진단](./L1_RECOVERY_V2_V3_PROCEDURE_KNOWLEDGE_DIAGNOSTIC_DESIGN_HANDOFF_r0001_20261126_KST.md)
- 이번 범위는 V2/V3의 점진적 개선. 기존 r0007의 다른 단계 및 책임 경계 유지.

## 1. 배경 및 목적
실제 Recovery 시험에서 유사 경로 탐색, 보호 판정·수정 방안 및 MSC 품질 문제가 관찰됨. V2 원인 규칙부터 부정확할 가능성이 있으나 실제 실패 로그와 활성 스킬은 설계 GPT에서 미확인. 약 1500개 LTE/NR L1 C/C++ 파일, Qwen3.6-27B 환경에서 자유 추론과 자율 탐색 부담을 줄이고 원본 근거 기반 재현성을 높임. 전체 Knowledge 구축, 신규 인덱스, 멀티에이전트 도입은 선행 조건이 아님.

## 2. 업무 GPT 요청
기존 활성 l1-channel-recovery 및 code-analyzer의 실제 원문·revision·action·영수증을 확인하고 아래 요구사항과 대조. 이미 구현된 기능은 재사용하고 누락된 계약만 최소 수정. 기존 비-timeout PR/CL 한 건을 기준으로 현행 결과를 보존하고 각 차수별 실제 스킬 코드 적용 및 시험을 수행. 단계별 사용자 확인 후 다음 차수 진행. 제품 코드 변경·운영 설치·Job 활성화는 별도 승인 범위로 유지.

## 3. V2 Cause Rule 구조화
PR/Jira 주장과 코드 사실을 분리. 수정 전후 및 정상 Procedure의 관련 경로를 분석하고 특정 if문이나 함수명이 아닌 Fix가 보장하는 정상 조건을 추출.
필수 필드:
| 필드 | 의미 |
|---|---|
| rule_id | Seed 및 규칙 식별자 |
| resource/object/owner/generation | 동일 자원·객체·작업 세대 및 소유자 |
| preconditions | 결함 성립 필수 전제 |
| trigger | 실패 유발 이벤트 |
| first_violation | 최초 잘못된 상태 사용·통지·동작 |
| ordering | 필수 선후 관계 및 비동기 경계 |
| invariant | 정상 유지 조건 |
| fix_mechanism | 기존 Fix가 보호하는 원리 및 한계 |
| anchors | 실제 API·상태 변수·메시지·자원 symbol |
| evidence | 수정 전/후/정상 반례의 revision/build/path/function/line |
| confidence/status | CONFIRMED/INFERRED/UNKNOWN 및 검증 결과 |

가상 예시(실제 제품 결함 아님):
```yaml
cause_rule:
  id: CR-001
  resource: RF_TX_RESOURCE
  preconditions: [previous_release_pending, same_resource]
  trigger: new_tx_activation
  first_violation: activation_before_release_complete
  invariant: release_complete_before_activation
  fix_mechanism: release_completion_guard
  anchors: [] # 실제 원본에서 확인한 symbol만 입력
  evidence:
    before_fix: null
    after_fix: null
    normal_case: null
  validation: UNVERIFIED
```
수정 전 실패, 수정 후 보호, 정상 반례를 각각 설명할 수 있는 규칙만 V3에 전달. 필드 존재 여부와 의미 정확도는 별개로 검사. 근거 부족·충돌은 보류하고 다음 조회를 명시. 원인이 여러 개면 규칙 분리. Procedure 지식이 부족하면 기존 Knowledge를 조회하거나 관련 정상 경로만 추가 분석하고 revision을 대조.

## 4. V3 Search Plan 및 동일 패턴 탐색
Cause Rule의 실제 anchors를 명시적 검색 조건으로 변환. LLM은 후보 의미 판단에 집중하고 후보 열거는 기존 Analyzer 및 허용된 결정론적 검색 기능으로 수행.
| 탐색 수준 | 대상 | 적용 |
|---|---|---|
| L1 | 동일 API 호출 위치 | 우선 |
| L2 | 직접 caller/callee 및 wrapper | 우선 |
| L3 | 동일 상태 읽기/쓰기, 자원·메시지·handler | L1/L2 검증 후 |
| L4 | 다른 API의 의미적 동일 동작 | 후속 별도 설계 |

Search Plan 필수 항목: rule_id, source revision/build, scope, anchors, 검색 종류, 실제 지원 action 및 인자, 파일/확장/시간/토큰 상한, 제외 기준, 종료·재개 조건. 존재하지 않는 action을 추정 호출하지 않음. 단순 문자열 검색은 후보 생성용이며 overload, macro, 조건부 컴파일, 간접 호출 및 비동기 dispatch는 원본으로 검증하고 미확정으로 표시.
후보 목록 필수 항목: candidate_id, rule_id, path/function/line, 발견 query, 객체/작업 관계, 근거, 관련/무관/미확인, 제외 이유, 조사 상태. 동일 위치라도 객체·빌드·실행 경로가 다르면 무조건 합치지 않음.
전체 대상 파일, 실제 조회 파일, 검색 hit, 중복, 제외, 조사 완료, 미조사, 잘림, 잔여 범위 및 종료 이유를 기록. 후보 관련성은 결함 확정이 아님. V4 기존 보호 판정으로 전달하며 V3 누락을 V4 종결 검사로 대체하지 않음.

## 5. 단계별 구현 및 수락
| 차수 | 변경 | 수락 시험 |
|---|---|---|
| 0 | 현행 기준선 확보 | 동일 PR, revision/build, 모델/예산, 기대 후보 및 정상 반례 고정 |
| 1 | Cause Rule 구조화 | 필수 필드·근거 참조 검사, 개발자 원인 판정 일치 |
| 2 | 원본·반례 검증 게이트 | 잘못된 규칙과 근거 없는 확정 차단 |
| 3 | Cause Rule→Search Plan | 실제 symbol/action 매핑, 범위·예산·재개 조건 검증 |
| 4 | L1/L2 탐색 | 기대 직접 호출 후보 누락 및 오탐 측정, 원본 대조 |
| 5 | 후보 목록·coverage 관리 | 중복/제외/미조사/잘림 재현 및 재개 시험 |
| 6 | L3 상태·자원 탐색 | 기존 기능 재사용, 확인된 결손만 보완 요청 |

각 차수는 이전 통과 산출물을 재사용하고 별도 실행·회귀·롤백 가능하도록 구성. 동일 Seed에서 변경 전후 비교 후 다른 Seed로 일반화 검증. 평가용 기대 후보는 입력에 노출하지 않음. 지표: V2 필수 전제·최초 위반 정확도, 근거 없는 확정 수, 정상 반례 오판, V3 recall/precision, 미조사량, 실행 시간·토큰. 대표 사례의 핵심 원인 오류·알려진 직접 후보 누락·근거 없는 확정은 0건을 수락 목표로 제안하며 전체 코드 탐색 완전성을 보장하지 않음. 실제 개선율은 측정 후 보고.

## 6. 책임 경계
- Recovery: 구조화·검증·Search Plan·후보 관리 및 기존 V4 연결.
- Code Analyzer: 기존 코드 사실 추출 action 재사용. 결손 발견 시 재현 입력·기대/실제 결과·필요 계약을 설계 GPT에 전달. 임의 신규 parser/index 개발 금지.
- Knowledge Updater: 필요한 경우 정상 Procedure 지식 제공. 전체 구축 불필요.
- Doc Converter, Kernel, Viewer: 기존 계약 유지. V4~V6 로직은 이번 변경 대상 제외.
- 기존 Work에 차수별 산출물·시험 근거·재개점 보존. 업무 소스 및 상세 증빙 공개 반출 금지.

## 7. 첫 회신 및 완료 조건
업무 GPT는 활성본/action 확인 결과, 기존 구현과 gap, Seed 및 기준선, 차수별 수정 파일과 시험 계획을 먼저 회신. 이후 1차부터 실제 스킬 적용 결과와 PASS/FAIL/NOT_RUN, 차단 사유 및 다음 차수를 보고. 기존 r0007과 충돌 시 책임 경계 및 안전 게이트 유지. 신규 독립 리뷰 요청 없음.
현재 상태: 설계 인계용. 실제 구현·시험·운영 배포 미확인.
