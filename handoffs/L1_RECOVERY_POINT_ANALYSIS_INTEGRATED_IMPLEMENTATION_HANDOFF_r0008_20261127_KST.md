# L1 Channel Recovery 통합 상세 설계·단계별 구현 인계 r0008

- 2026-11-27 KST · 기존 Work 재사용 · 업무 GPT 설계/수락 기준 확정, Qwen3.6-27B 구현·실행
- 대상: 기존 `l1-channel-recovery`의 분석·오케스트레이션 개선. 제품 코드 수정, 운영 설치, Job 활성화, 그룹 지식 게시 및 신규 독립 리뷰는 이번 요청 범위 밖.
- r0007 전체 기본 설계 + 11/26 V2/V3 진단 + 11/27 V2/V3 구현 지시를 단일 실행 기준으로 통합. 기존 문서와 시험 기록은 보존. Viewer/Kernel/Workflow/Converter의 기존 계약은 유지하며 과거 ZIP은 재설치 입력이 아님.
- 상태: 설계 GPT 인계본. 실제 업무 환경 구현·회귀·연동 결과는 미확인. 본문 수치 목표는 수락 기준이며 실측 성과가 아님.

## 0. 업무 GPT 원샷 요청

> 이 문서를 Recovery의 단일 최신 실행 기준으로 사용해 주세요. 기존 활성 스킬의 실제 원문·지원 action·기존 Work와 대조하여 이미 구현된 기능은 재사용하고 결손만 최소 수정해 주세요. 먼저 기존 비-timeout PR/CL Seed 1건의 현재 실행 결과를 보존하고, 정상 반례와 기대 후보를 담당자가 별도 고정해 주세요. 변경 전 기준선과 원인 분리 실험을 확보한 뒤 V2 Cause Rule과 V3 Search Plan을 순차 개선해 주세요. V0/V1/V4~V6는 기존 r0007 계약을 유지하되 실제 결손만 보완해 주세요. 최신 활성 Analyzer·Converter를 실제 호출하고 기존 Work/Evidence 등록 및 Viewer 열람을 각각 검증해 주세요. 구버전 재설치, 새 writer/schema/adapter 추정 구현, 전체 Source Map/Knowledge 구축의 선행 강제, 무조건적인 Subagent 도입, 추가 독립 리뷰는 금지해 주세요. 각 차수 결과와 근거, 다음 단계 계획을 회신하고 사용자 확인 후 다음 차수로 진행해 주세요.

## 1. 목표와 문제 정의

과거 merged PR/P4 submitted CL에서 수정 위치 자체가 아니라 결함 발생 조건·최초 위반·수정이 보장하는 정상 조건을 추출하고, 현재 코드의 다른 실행 경로에 동일 원인 패턴이 잔존하는지 분석. 이미 해결된 Seed만 보고 탐색을 종결하지 않으며, 기존 Fix를 모든 후보에 복제하지 않음. 사용자 확인으로 이미 처리한 REQ→CNF 미수신 timeout 메커니즘은 제외.

실제 Recovery 시험에서 유사 경로 탐색, 보호 판정/조치 방안, MSC 품질 문제가 관찰됐으며 V2부터 부정확할 가능성이 제기됨. 정확한 실패 PR/CL·로그·활성 Recovery revision은 설계 GPT에서 미확인. 약 1,500개 LTE/NR L1 C/C++ 파일과 Qwen3.6-27B 환경에서 자유 추론 대신 검증된 코드 사실·정상 Procedure·명시적 검색계획을 사용. 범위는 현장 분모로 다시 고정하고 전체 탐색 완전성을 주장하지 않음.

## 2. 최신 의존성 및 적용 원칙

| 구성 | 기준 및 처리 |
|---|---|
| Recovery | 기존 업무 GPT 관리 활성본. 본 문서 기준 gap 확인 및 최소 변경 |
| Code Analyzer | L1Work 최신 ZIP v0.15.7(11/27). v0.15.6 실제 적용은 사용자 확인. v0.15.7의 실제 활성 여부·action·설치 영수증 확인. 임의 다운그레이드/재설치 금지 |
| Viewer | 최신 ZIP v0.5.8(11/27). v0.5.6 가독성, v0.5.7 섹션 순서, v0.5.8 독립 Source Map 계승. 기존 Recovery 메뉴·Work·MSC 기능 유지 검증. 실제 활성본 확인 |
| Kernel | 최신 ZIP v0.7.47. 기존 Recovery projection 및 Evidence 저장·재조회 계약 재사용 |
| Workflow | 최신 ZIP v1.6.75. 같은 버전의 과거 후보 ZIP 내용이 다르므로 실제 활성 hash/action 확인. 임의 교체 금지 |
| Doc Converter | 최신 ZIP v0.2.26. 실제 지원 action으로 PUML/SVG/HTML 변환 |
| Knowledge Updater / Source Map | Updater r0002 및 Source Map r0003 별도 계약. 검증된 관련 Procedure/관계만 선택적으로 조회. 전체 구축·새 인덱스는 필수 아님 |

**배포와 실행 기준:** L1Work 루트 ZIP은 Skill Updater 자동 배포 원본이므로 관리상 최신 게시 버전을 운영 기준으로 삼음(사용자 지시). 단, 11/27 Analyzer v0.15.7 및 Viewer v0.5.8의 기존 전달서에는 development_not_for_deployment가 명시됨. 해당 표기는 실제 자동 설치를 차단하는 기술적 게이트라고 단정하지 않음. G0에서 실제 활성 버전·설치 결과·지원 action을 확인하고, 배포 정책/활성 상태가 충돌하면 사용자에게 보고. 이미 설치된 버전을 임의 롤백하거나 새 설치를 강제하지 않음. 현재 호스트 상태를 확인한 뒤 동일 모델/도구 버전을 비교 시험 동안 고정. 버전 변경이 필요한 경우 새 기준선을 확보. 구버전 Viewer v0.5.3/v0.5.6/v0.5.7은 역사·계약 참조에 한정.

**Analyzer v0.15.7 주의:** 전처리 형제 분기 배제·nested guard·line splice·범위 종료 개선, condition_semantics_version=2, 실제 build 활성 UNKNOWN/해석 불가 UNCERTAIN 분리. 기존 legacy pending patch는 덮어쓰지 않고 별도 새 scope에서 원문 재분석. 정적 guard를 실제 build 활성/런타임 실행으로 승격 금지. 지원 action이 확인되지 않으면 추정 호출하지 않음.

## 3. 책임 경계 및 실패 재개

| 담당 | 역할 |
|---|---|
| Recovery | Seed 원인·Cause Rule·Search Plan·후보 관리·보호 시점·조치·MSC 의미 수락 |
| Analyzer | 기존 action으로 코드 사실/호출/분기/등록/상태·원문 근거 추출 |
| Knowledge Updater | 필요시 정상 Procedure 지식 제공/작성, Source Map 소유 및 갱신. Recovery는 읽기·참조만 |
| Converter | 검증된 Scenario IR의 PUML/SVG/B형 HTML 생성 |
| Workflow/승인 writer | 기존 Work 선택·재개·첨부·등록 요청 |
| Kernel | 원본 Evidence 저장·SHA/revision·CAS·파생 조회·readback |
| Viewer | Recovery 목록·검색·상세·Work 연결 및 검증된 artifact 열람 |

REUSE → CONNECT → 실제 증명된 gap만 담당 컴포넌트의 별도 작업으로 EXTEND. Recovery에서 신규 저장 schema/DB/writer/index/UI/API를 구현하지 않음. Analysis, MSC, 저장, Viewer, 제품 효과를 독립 판정. 후속 저장/열람 실패로 완료한 분석·변환·모델·Job을 재실행하지 않음. 입력·revision·build·버전·범위·영수증이 일치하는 결과를 재사용하고 실패 단계만 재개. 실제 증빙은 업무 Work 내부 보존.

## 4. G0 및 기준선 (변경 전)

1. 기존 Work/Seed와 실제 실행 실패 결과, 활성 Recovery/Analyzer/Converter/Workflow/Kernel/Viewer 버전·revision·action·권한·영수증을 확인. 필요한 의존 단계만 보류하며 독립 분석을 막지 않음.
2. 이번 요청의 명시 제품 소스 폴더를 우선 검증. 미지정이면 같은 프로젝트의 유효한 저장 경로 재사용. 경로 불명/권한 오류/복수 후보 또는 요청 revision 불일치 시 필요한 선택만 한 번 질문. 유효 경로와 revision 미지정이면 관찰 Git commit/P4 revision 고정. 경로 오류 시 임의 다른 경로 전환/checkout/전체 디스크 탐색 금지. 무인 실행이면 미확인과 재개 위치 보존.
3. PR/CL 수정 전·후·현재 source revision/build, 파일/확장/시간/토큰 예산, 모델/설정, 실제 조사 범위를 고정. 기존 Work의 비-timeout Seed 1건을 사용. 담당자가 원인·기대 후보·정상 반례를 평가용으로 별도 고정하고 정답은 모델 입력에 노출하지 않음.
4. 현행 결과(D0)를 보존. 동일 조건의 기존 영수증이 유효하면 재사용. 이전 r0006 비교 자료가 없거나 조건이 다르면 비교 불가로 표시하되 강화 단일 실행 자체의 수락 시험은 진행 가능.

## 5. V0~V6 전체 분석 계약

| 단계 | 실행·출력 | 통과/재개 |
|---|---|---|
| V0 입력 고정 | Work/Seed/경로/revision/build/예산 | 불명확하면 해당 입력만 보류 |
| V1 Seed 전후 | 실제 diff·주변 코드로 증상·실패 인과·Fix 효과·한계 검증 | Jira/PR 주장과 코드 사실 분리 |
| V2 Cause Rule | 객체·자원·세대·소유권·필수 전제·최초 위반·정상 불변조건 | 전/후/정상 반례 일치 시 V3 |
| V3 Search Plan | 명시 검색 조건·후보·coverage·잔여 범위 | 원본 대조, 미조사/잘림 보존 |
| V4 보호 판정 | 같은 작업의 첫 위반 전 보호 효력, 우회 분기·반례·빌드 | 4분류 및 종결 재검사 |
| V5 조치 | 검출·원인 수정·사전 검사·국소 복구·상위 이관 비교 | 소유권·부작용·복귀·실패 처리 |
| V6 산출 | 검증 Scenario IR·MSC·보고서·기존 writer | 두 생산자 호출, 의미/저장/열람 분리 |

### 5.1 V2 Cause Rule (최신 구현 계약)

V1→V2에서 관련 정상 Procedure의 시작/종료, 호출·메시지 순서, 모듈 책임, 상태 전이, 객체/세대/자원 소유권 및 비동기 경계를 확인. 필요한 기존 Knowledge를 revision/build 대조하여 재사용하고 부족한 경우 해당 정상 경로만 추가 분석.

필수 구조:
```yaml
cause_rule:
  rule_id: null
  resource: null
  object: null
  owner: null
  generation: null
  preconditions: []
  trigger: null
  first_violation: null
  ordering: []
  invariant: null
  fix_mechanism: null
  anchors: []
  evidence:
    before_fix: []
    after_fix: []
    normal_case: []
  confidence: UNKNOWN
  validation: UNVERIFIED
```
위 예시는 보고서/단계 산출물의 논리 구조이며 신규 저장 schema가 아님. evidence는 source revision/build/path/function/line 및 실제 참조. 하나의 if문/함수명으로 규칙을 대신하지 않음. 수정 전 최초 실패, 수정 후 적시 보호, 정상 반례를 동시에 설명해야 함. 규칙이 다수이면 분리. 형식 적합과 의미 정확도를 별도 검사. 근거 충돌/부족은 보류하고 다음 조회 명시. CONFIRMED/INFERRED/UNKNOWN과 시험 PASS/FAIL/NOT_RUN 구분.

### 5.2 V3 Search Plan (최신 구현 계약)

Cause Rule의 원본 확인 anchors를 검색 조건으로 변환. LLM은 의미 판단에 집중하고 후보 열거는 기존 Analyzer 및 허용된 결정론적 검색 사용.

| 수준 | 탐색 | 우선순위 |
|---|---|---|
| L1 | 동일 API 호출 위치 | 우선 |
| L2 | 직접 caller/callee·wrapper | 우선 |
| L3 | 동일 상태 read/write·자원·메시지·handler | L1/L2 검증 이후 |
| L4 | 다른 API의 의미적 동일 동작 | 후속 별도 설계 |

Search Plan 필수 항목: rule_id, source revision/build, scope, anchors, query 종류, 실제 지원 action/인자, 파일/확장/시간/토큰 상한, 제외 기준, 종료 및 재개 조건. 문자열 검색은 후보 열거이며 overload/macro/조건부 컴파일/간접 호출/비동기 dispatch는 원문 대조. Source Map은 검증된 정적 관계를 보조로 쓰되 실제 도달·순서의 증거로 단정하지 않음.

Candidate 필수 항목: candidate_id, rule_id, path/function/line, 발견 query, 객체/작업 관계, 근거, 관련/무관/미확인, 제외 이유, 조사 상태. 동일 위치라도 객체/빌드/경로가 다르면 일괄 합치지 않음. 전체 파일 분모, 실제 읽은 서로 다른 제품 파일, 메타데이터 별도, hit/중복/제외/조사 완료/미조사/잘림/잔여 범위/종료 이유 기록. 예산 도달 또는 추가 근거 없음에서 종료하고 재개점 남김. 후보 관련성은 결함 확정 아님. V3 누락을 V4 종결 검사로 대체하지 않음.

### 5.3 V4/V5 기존 판정·조치 유지

| 판정 | 필수 근거 |
|---|---|
| 이미 해결됨 | 현재 build·같은 작업의 관련 실패 분기에서 첫 위반 전에 동등 보호 |
| 발생 불가능 | 해당 후보에서 필수 전제가 성립하지 않는 build/객체/분기 근거 |
| 미해결 확인 | 같은 작업의 입력→실패 분기→최초 위반 및 보호 결손 |
| 추가 검증 필요 | 확인되지 않은 관련 분기/순서/소유권/빌드 또는 상충 근거 |

종결 전에 반대 근거, 보호 우회, 다른 작업 세대 callback을 재검사. HAL 실패 판단 뒤 정리하더라도 그 전에 잘못된 성공 통지가 나갔다면 적시 보호가 아님. V5는 검출 신호 → 정리 권한·실제 획득분 → 부분 SW/HW 부작용 → 종료 통지 → 복귀 확인 → 실패 시 상위 이관. 공유 RF/다른 Stack 영향과 소유권 불명 시 무조건 국소 복구 금지. 제품 변경은 별도 승인 및 실시간/고정 자원 제약(new/delete 금지). 상세 조치 분류는 r0007 §4 유지.

### 5.4 V6 MSC 및 Work/Viewer 통합

- Analyzer 실제 호출의 버전/action/revision/범위/결과/원본 근거/영수증 기록. 줄 번호나 양 끝 이름만으로 호출/등록/런타임 순서를 확정하지 않음.
- Seed 수정 전·후, 현재 후보 AS-IS, 제안 TO-BE를 분리. 검증된 Scenario IR의 발신/수신/순서/분기/비동기 대응 원본 대조. Edge 정의·근거는 Recovery 책임. 미확정 Edge 의존 요소만 보류하고 독립 검증 요소는 변환. 조치 없음은 해당 없음 사유 기록.
- Converter 실제 호출 후 입력 해시·영수증·PlantUML/SVG/B형 HTML·상대 링크·SHA 기록. 형식 PASS만으로 의미 PASS 금지. 역순/방향/메시지 불일치 또는 검증 불가 산출물은 등록·링크 차단. 실패 입력 보존 후 해당 IR/변환만 재개.
- 기존 승인 writer의 preview→source SHA/Evidence revision 고정→등록→readback 사용. 11/24 개발 계약: provider=l1-channel-recovery, kind=recovery_analysis, stage=utility; recovery_report_preview, record_recovery_report, work_recovery_reports는 실제 활성 action 대조 후에만 사용. UTF-8 MD/JSON 5 MiB 이하 조건도 설치본 확인. Work ID 유지, 등록 응답/Evidence ID/SHA/revision/재조회 기록. utility 첨부는 제품 효과 검증 완료 아님.
- Kernel이 기존 works/<work-id>/RECOVERY.md, state/recovery_reports.json, 루트 RECOVERY.md, index/recovery.json 및 recovery/README.md, recovery/index.json, recovery/works/<work-id>/<Evidence ID>.md 파생 보기 관리. Recovery가 직접 쓰거나 새 schema 생성 금지.
- Viewer의 Recovery 메뉴/목록/검색/상세 → 기존 Work → 검증된 MSC HTML/SVG 본문 링크 유지. 별도 MSC 탭은 만들지 않음. 실제 adapter/ACL/SHA/CSP/경로 확인. 합성 API/fixture를 운영 서비스에 덮어쓰지 않음. Source Map 메뉴는 별개 읽기 경로이며 Recovery 데이터를 재분류하거나 강제 이관하지 않음. 기존 Knowledge 섹션 순서/표시 변경은 Viewer 책임.
- 저장이나 열람 실패는 각 담당에게 근거와 재개점 전달. 분석·MSC 유효 결과는 그대로 보존.

## 6. 원인 분리 실험 및 최소 Knowledge

동일 Seed/revision/build/모델/도구/예산에서 독립 맥락으로 비교. 가능하면 반복하여 변동성 기록. 기존 결과 재사용은 입력과 영수증이 일치할 때만. D0는 변경 전 기준선으로 유지.

| 조건 | 제공 입력 | 판단 단서 |
|---|---|---|
| D0 | 현행 Recovery | 비교 기준 |
| D1 | 검증된 코드 fact 추가 | 사실 획득/전달 문제 |
| D2 | 검증된 정상 Procedure Knowledge 추가 | 정상 맥락 부족 |
| D3 | D1+D2 | 상호 보완 또는 잔여 오류 |

개선이 관찰돼도 단일 시험으로 원인 확정하지 않음. D3 실패 시 단계 지침/도구 사용/추론 한계를 추가 분리(필요시 동일 입력 강한 모델 비교, 별도 허용 범위). 정답 혼입·중복 입력 통제. 정상 Procedure 한 건만 기존 Updater로 조회/검증하거나 필요 시 생성. Module/Feature/Procedure/Scenario 교차 참조, 정상 MSC, 상태/소유권/순서 불변조건, revision/build/원문 포함. 오래되거나 충돌한 지식은 가설로 취급. 전체 지식 구축은 별도 결정.

## 7. 단계별 구현 순서 및 수락

| 차수 | 진행 | 수락 증거 |
|---|---|---|
| 0 | 활성 계약 G0, 현행 기준선/원인 분리 | 동일 Seed 기준 D0 및 D1~D3 비교 가능한 범위, 결손과 변경 지점 |
| 1 | V2 구조화 | 개발자 원인 판정 일치, 필수 필드 및 원본 참조 |
| 2 | V2 반례/원본 게이트 | 틀린 규칙의 V3 진입 차단 |
| 3 | Cause Rule→Search Plan | 실제 symbol/action, 범위/예산/재개 매핑 |
| 4 | V3 L1/L2 | 기대 직접 후보 누락·오탐 및 원문 대조 |
| 5 | 후보/coverage | 중복/제외/미조사/잘림 재현 및 재개 |
| 6 | V3 L3 | 상태·자원·메시지/handler 탐색, 실제 결손만 보완 |
| 7 | V4~V6 회귀·연동 | 기존 보호 판정/조치/MSC/등록/열람 계약 유지 |

차수마다 최소 변경·독립 시험·롤백 가능 상태·사용자 확인. D1~D3 수행에 필요한 자료가 없다면 진단 미확인과 제약을 기록하고, 확보한 기준선으로 독립 가능한 개선을 진행할지 사용자와 확인. 동일 Seed 전후 비교 및 별도 Seed 일반화 검증. V2 핵심 원인 오류, 알려진 직접 후보 누락, 근거 없는 확정, 잘못된 MSC 순서 각 0건을 대표 수락 목표로 설정. 전체 제품 코드 무결함을 보장하지 않음. V3 recall/precision은 분모와 함께, V4 오종결/보류, V5 조치 타당성, V6 의미 오류, 시간/토큰/실제 조사량을 보고.

**Agent 비교:** r0007 A(현행 r0006 또는 비교 가능한 기존 결과) / B(강화 단일 실행) / C(반복 결손 단계 하나 분리) 유지. D0~D3는 원인 분리 실험으로 A/B/C와 별개. B 충족 시 단일 실행 채택. 반복 오류의 위치가 입증된 경우만 seed-analyst 또는 candidate-checker 등 한 역할, 순차·깊이 1·읽기 전용으로 시험. 동일 전체 예산 합산, 프라이머리 최종 판정·등록 요청 책임 유지. 위임 불가 시 단일 경로 유지. 병렬화/전체 인덱스는 별도 실측 후 판단.

## 8. 최종 통합 시험 및 회신

| 시험 | 확인 |
|---|---|
| T01 | 명시/저장 경로·revision 분기, 질문 최대 1회, 입력 고정 전 분석 0 |
| T02 | Seed 전후·정상 반례 V2 원인 규칙 및 잘못된 규칙 차단 |
| T03 | V3 직접 호출/등록/상태/guard/빌드, 예산·미조사·누락/오탐 |
| T04 | V4 적시/늦은 보호·비활성 build·다른 세대 callback·종결 반대 근거 |
| T05 | V5 검출·소유권·부작용·복귀·금지 조건 |
| T06 | Analyzer 및 Converter 실제 영수증, MSC 네 관점·역순/방향 차단·미확정 Edge |
| T07 | Work/Evidence 등록·SHA/revision/CAS·readback·중복 방지 및 파생 Recovery 인덱스 |
| T08 | Viewer Recovery 목록→상세→Work→실제 HTML/SVG 본문 링크, ACL/CSP/404/변조/경로 이탈 차단, 데스크톱·모바일 |
| T09 | 기존 Viewer A01~A10/H01~H05/T1~T8 및 V56/V57과 최신 Source Map 변경 회귀(별도 Viewer 담당) |
| T10 | 단계별 실패/재개, 유효 결과 재사용, 중복 모델/Job/Analyzer 호출 0 |

최초 회신: ACTIVE_G0(버전/실행 action/권한/설치 결과), 기존 Work/Seed·기준선, 기존 구현 대비 gap·변경 파일·차수별 시험 계획. 이후 차수별 PASS/FAIL/SKIP/NOT_RUN/BLOCKED, 실제 결과·근거·지표(분자/분모)·변경 revision·재개점·다음 한 행동. 분석·MSC·Work 저장·Viewer 연동·제품 효과를 각각 판정. 실제 제품 시험 미실행이면 제품 효과 미검증. Viewer/Kernel/Converter 통합 결손은 독립 담당 작업으로 전달하고 Recovery 구현의 전체 선행 게이트로 만들지 않음.

## 9. 원본 및 우선순위

이 문서는 아래 세 문서를 통합한 단일 실행 지침. 기존 상세 설명과 수락 계약은 보존하며, V2/V3 충돌 시 11/27 구현 요구와 이 통합본 우선. 기존 인계의 역사적 시험 결과/구버전 ZIP은 현재 설치 지시로 해석하지 않음. 별도 스킬 책임은 최신 담당 인계 기준.

1. [Recovery 통합 설계 r0007 (11/25)](./L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0007_20261125_KST.md) — 전체 V0~V6, 보호·MSC·재개, A/B/C, 기존 R1 지적 4건 반영.
2. [V2/V3 Procedure Knowledge 진단 r0001 (11/26)](./L1_RECOVERY_V2_V3_PROCEDURE_KNOWLEDGE_DIAGNOSTIC_DESIGN_HANDOFF_r0001_20261126_KST.md) — D0~D3, 최소 Procedure, 원인 분리.
3. [V2/V3 단계별 구현 r0001 (11/27)](./L1_RECOVERY_V2_CAUSE_RULE_V3_SEARCH_PLAN_IMPLEMENTATION_HANDOFF_r0001_20261127_KST.md) — 구조화·Search Plan·coverage·차수별 수락.
4. [Recovery/Viewer/Kernel/Converter 기존 계약 (11/24)](./L1_CHANNEL_RECOVERY_VIEWER_KERNEL_CONVERTER_COMPLETE_HANDOFF_r0001_20261124_KST.md) — writer/projection/ACL/MSC 연결 계약만 재사용, 과거 Viewer ZIP 입력 제외.
5. [Viewer v0.5.6](./L1_WORKSPACE_VIEWER_V056_TECHNICAL_KNOWLEDGE_READABILITY_COMPLETE_HANDOFF_r0001_20261126_KST.md) · [v0.5.7](./L1_WORKSPACE_VIEWER_V057_KNOWLEDGE_SECTION_ORDER_COMPLETE_HANDOFF_r0001_20261126_KST.md) · [Viewer v0.5.8/Analyzer v0.15.7](./L1_SOURCE_MAP_VIEWER_ANALYZER_DEVELOPMENT_DELIVERY_r0001_20261127_KST.md) — 최신 표시/compile-condition/회귀 조건.
6. [Source Map r0003](./L1_SOURCE_MAP_1500_UPDATER_INTEGRATED_HANDOFF_r0003_20261127_KST.md) · [Knowledge Updater r0002](./L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0002_20261125_KST.md) — 선택 지원, 구축·게시 별도.
7. [Analyzer v0.15.6 과거 개발 인계](./CODE_ANALYZER_V0156_DEVELOPMENT_DELIVERY_r0001_20261125_KST.md) — 당시 시험/개발 후보 기록, 사용자 확인으로 실제 v0.15.6 적용 상태 갱신.

## 10. 자체 검토 판정 및 제한

- 문서 계약 정합성: 조건부 GO. Viewer 0.5.6~0.5.8의 변경은 표현 및 Source Map 읽기 중심이며 Recovery 내부·저장 계약 변경이 요구되지 않음. 단 실제 adapter/권한/활성 스킬 및 업무 E2E는 확인 필요.
- r0007의 11/24 Viewer 참조는 계약 참조로 유지하되 구버전 재설치 금지. v0.15.6 사용자 적용 확인과 v0.15.7 개발 전용 표기의 자동 배포 가능성 구분.
- 기존 r0003 R1 독립 리뷰 지적(M1/N1/N2/N3)의 경로/revision, 의미 검증 실패, Workflow 매핑, Edge 미확정 처리 유지. 신규 독립 리뷰 없음.
- 현장 원인 진단, 변경 코드 구현, 실제 모델 품질, 설치 상태, E2E 및 제품 효과는 본 인계 게시 시점 미검증.
- NEXT_ONE_ACTION: 업무 GPT에서 기존 Work를 선택하여 G0와 대표 비-timeout Seed의 변경 전 기준선 및 현재 구현 gap을 회신.
