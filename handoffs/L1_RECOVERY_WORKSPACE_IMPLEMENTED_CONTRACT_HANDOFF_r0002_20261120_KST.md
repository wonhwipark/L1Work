# 업무 GPT 인계 — CL/PR Recovery 분석 보완과 Workspace 저장·조회 연결

- 개정: r0002 / 2026-11-20 KST
- 전달 저장소: wonhwipark/L1Work / branch: main
- 이 문서 상대 경로: handoffs/L1_RECOVERY_WORKSPACE_IMPLEMENTED_CONTRACT_HANDOFF_r0002_20261120_KST.md
- 대상: 업무 GPT, 허용된 로컬 Agent/LLM, 기존 l1-channel-recovery와 업무용 l1-workspace
- 문서 목적: 이미 전달한 분석 방향에 필요한 설계 보완을 덧붙이고, 관리 스킬에서 개발한 저장·조회 계약과 연결
- 이번 업무 요청: **스터디·설계와 실제 설치 계약의 매핑**. 별도 요청 전까지 분석 확장을 위한 스킬 수정·제품 코드 변경·업무 저장소 변경·패키지 배포·운영 설정·Job을 시작하지 않음

## 1. 이전 인계와의 관계

기존 기준은 [수정 CL 기반 미커버 유사 결함 탐색·검사·Recovery 판단 r0002](L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0002_20261119_KST.md)예요. 그 문서의 Seed 전후·현재 대상 구분, V0~V6, 기존 보호 대조, 조치 선택과 근거 보존을 유지해요. 기존 인계의 최소 구현 단계를 이번 설계 요청만으로 다시 실행하지 않아요.

사용자가 전달한 “CL/PR 기반 L1 Recovery 분석 확장 설계” 요청에서 아래 네 가지를 보완 입력으로 채택해요. 이미 있는 분석 기능이나 이번 저장 개발을 다시 구현하라는 뜻은 아니에요.

| 보완 입력 | 적용 위치 | 판단 |
|---|---|---|
| 객체·상태·순서·조건·위반·보호·예외를 갖춘 원인 규칙 | 기존 보고서/체크리스트 | 채택. 신규 Kernel metadata/schema를 요구하지 않음 |
| 필요한 코드 추적 범위·확대·중단 조건 | 기존 분석 단계와 범위 기록 | 채택. 전수 코드 분석을 강제하지 않음 |
| 후보 분류와 미해결 판정의 최소 근거 | 후보 검증·반대 근거 표 | 채택. 코드 유사성·미확인을 결함 확정으로 바꾸지 않음 |
| 양성·정상·상위 보호·실행 불가·자료 부족의 비교 평가 | 효과 검증 계획 | 채택. 저장 성공·합성 시험과 분석 정확도를 분리 |

이 문서는 두 작업을 연결해요.

- **분석 설계:** 과거 수정에서 결함 조건을 추출하고 현재 다른 경로의 미해결 위험을 검증하는 방법.
- **저장·조회 연결:** 그 결과를 같은 Work/Evidence에 보존하고 Recovery별로 탐색하는 방법.

이전 별도 지시로 수행한 Kernel/Workflow 개발은 두 번째 범위예요. 그 개발 결과를 첫 번째 분석 방법의 구현·효과 검증으로 해석하지 않아요.

## 2. 확정된 제약

1. **REQ→CNF 미수신 timeout과 이미 구현된 해당 recovery 커버 범위는 제외**해요. 같은 실패 메커니즘을 다른 이름으로 새 후보화하지 않아요.
2. 해결된 Seed 위치에 불필요한 recovery를 넣지 않아요. 현재 다른 경로에 미해결 위험이 확인될 때만 근본 수정·예방·관측·recovery·상위 이관을 비교해요.
3. CodeQL 설치·사용을 전제하지 않아요. 공개 도구·논문·절차는 아이디어만 선별하며 해당 분석 정확도나 검증 성과를 상속했다고 주장하지 않아요.
4. 코드 유사성은 검색 단서예요. 후보 없음·근거 부족·조사 불가도 유효한 결론이에요. 검색 실패/잘림/timeout은 결과 0건과 구분해요.
5. 현재 MCP는 설치본 확인 자료의 조회·제공을 지원하지 않는다는 사용자 확정 제약을 유지해요. 사용자에게 설치본·manifest·진단 숫자·자료 반출을 다시 요구하거나 MCP 확장 완료를 설계의 선행 조건으로 두지 않아요.
6. 업무 GPT가 접근 가능한 실제 원문·허용된 로컬 Agent의 근거로 기존 기능과 이 문서의 계약을 대조해요. 접근 불가 항목은 미확인으로 남기고 독립적으로 가능한 설계는 계속해요.
7. 업무용 저장소·브랜치·source/Workspace root는 현장 기존 매핑에서 정확히 확인해요. 동명 GitHub.com 저장소나 이 전달 저장소를 업무 정본으로 대입하지 않아요.

## 3. 참고 접근의 채택·보류

| 접근 | 차용하는 생각 | 채택하지 않는 가정·범위 |
|---|---|---|
| CodeQL 변형 분석 | 알려진 결함을 기준으로 원인 조건에 맞는 다른 경로를 찾는 관점 | DB/엔진·언어 분석 기능을 도입하거나 같은 정확도를 얻었다고 가정하지 않음 |
| TyPatch | 패치에서 대상 객체·동작·조건·상태 전이·위반 규칙을 분리하는 관점 | 공통 backend·alias/경로 상태 추적이 텍스트 검색+LLM에 이미 있다고 가정하지 않음. Linux 결과를 L1 효과로 대입하지 않음 |
| Trail of Bits variant-analysis | 원래 결함 이해→좁은 기준 보정→한 요소씩 일반화→후보 대조·기록 | 공개 절차의 고정 잡음 임계값·병렬 Agent·CodeQL/Semgrep 도입을 저사양 환경의 필수 조건으로 채택하지 않음 |

위 표는 서로 다른 종류의 근거에서 아이디어를 고른 설계 판단이에요. 세 접근의 성과를 동일한 검증 결과처럼 합치지 않아요. 단계적 일반화와 좁은 패턴 보정 등 기존 r0002/저사양 순차 설계에 이미 있는 부분은 재사용해요.

## 4. 분석 절차에 반영할 최소 보완

| 단계 | 방법·필수 근거 | 남길 결과·종료 조건 |
|---|---|---|
| A. 입력 고정 | CL/PR 설명·수정 전후 실제 diff/revision, 현재 source·제품/빌드/활성 조건·범위·관련 로그/테스트 확인. merged 사실과 현재 제품/branch 반영 구분 | Seed와 현재 대상의 대응·차이·미접근. 핵심 revision 불명은 해당 판단 보류 |
| B. 결함 복원 | 증상·원인·발생 전제·객체/수명·호출/IPC 순서·깨진 불변 조건·Fix 보장/제외 범위. 설명 주장과 코드 사실 구분 | 원인 하나의 규칙과 anchor. 기능 추가 등 비결함 CL은 알려진 결함 Seed로 강제하지 않음 |
| C. 추적 범위 | 원인과 관련된 caller/callee·상태 reader/writer·초기화/해제/재사용·callback/timer/IPC·실패/취소/복구·공통/상위 보호·조건부 빌드 확인 | 조사 경계·분석 확대 이유·남은 경계. 관련 RAT/Stack/domain/CC/절차만 선택 |
| D. 규칙·보정 | 아래 규칙 표를 작성하고 역사적 결함·수정 후·안전한 유사 사례와 대조 | 검색 매치와 위험 판정 구분. 같은 전제에서 Fix 효과를 설명하지 못하면 규칙 보류/수정 |
| E. 단계적 탐색 | 좁은 기준에서 시작해 검색 의미 또는 공간 범위를 한 번에 한 요소씩 확대. 전체 허용 루트의 좁은 검색과 후보별 정밀 읽기를 구분 | 검색식·유지/일반화 조건·전체 매치·고유 후보·미분석 보존. 잡음 급증 시 조건 재조정 |
| F. 후보 검증 | 입력 유입·전제·같은 객체/세대·실행/빌드 경로·위반·caller/callee/HAL/PHY 보호·후속 fix·반례 확인 | 아래 판정과 결정 근거. 결정적인 보호/도달성 경계가 미확인이면 확정하지 않음 |
| G. 조치 판단 | 근본 수정 가능성, 기존 recovery 포괄, 수정 후 잔여 위험, 실제 검출 신호·권한·안전 복귀 대조 | 원인 수정/예방/관측/국소 recovery/상위 이관 또는 보류. 결함 확인만으로 recovery를 정답으로 정하지 않음 |

관련 비교 축은 LTE/NR, Stack/domain, SCell config/activation/deactivation/release, Tx switching·Dual SIM, DRX/CDRX, L1C/HAL/RF/PHY IPC 중 원인과 관계가 있는 것만 선택해요. 모든 축을 매번 분석하지 않아요.

필요한 코드는 후보 하나의 의미 단위로 제공해요. 관련 분기·return·cleanup·객체/필드 정의·상위 보호를 무작정 잘라내지 않아요. 근거가 부족하면 필요한 정의/호출 경계만 추가 조회하고, 새 근거가 없거나 예산이 소진되면 잔여 후보와 이유를 보존하고 부분 조사로 종료해요.

### 원인 규칙 양식

| 항목 | 내용 |
|---|---|
| 식별·수명 | 추적 객체/자원·같은 작업이라는 근거, 필요한 Stack/domain/CC·세대·소유권 |
| 사전 조건 | 입력·상태·활성/빌드 조건·실패 조건 |
| 동작·순서 | 실제 API/이벤트·상태 전이·정상적으로 지켜야 할 관계 |
| 위반 | 금지 상태/동작·정상 조건이 깨지는 경로 |
| 보호·예외 | caller/callee/wrapper/상위 보호가 유효한 전제, 적용 범위·예외 |
| 근거·한계 | 원본 CL/PR·수정 전후/현재 anchor, 사실/추론, 미확인 추적 경계 |

이 표는 보고서 본문의 의미 양식이에요. 신규 엔진·DB·영속 schema를 요구하지 않아요. 자연어/텍스트 대조로 부족한 alias·간접 호출·비동기 경로·경쟁·수치 문제는 추가 분석 필요로 분리해요. LLM이 문맥을 읽었다는 사실을 실제 정적 분석기의 보장으로 바꾸지 않아요.

### 후보 판정과 확정 근거

| 판정 | 필요한 설명 |
|---|---|
| 이미 해결됨 | 현재 수정 또는 동등 보호가 위반 경로를 막는 코드 근거 |
| 발생 불가능 | 현재 대상의 빌드·입력·객체/수명·실행 전제가 성립하지 않는 근거 |
| 미해결 결함 확인 | 같은 객체/작업에서 입력→전제→실행→위반이 이어지고, 관련 보호 경계를 대조한 근거. 코드로 입증한 범위와 실제 실행 검증을 별도 명시 |
| 추가 검증 필요 / 근거 부족 | 결정적인 옵션·caller/callee·동일성·순서·보호 등 남은 항목과 다음 조회 하나 |

기존 r0002의 직접 Fix 누락·미커버 변형·보호됨·전제 불성립·보류는 세부 사유로 유지해요. 분류 이름을 맞추느라 과거 결과를 삭제하거나 중복 후보를 만들지 않아요. 코드가 비슷하다거나 보호를 찾지 못했다는 사실만으로 미해결 결함을 확정하지 않아요.

Recovery가 필요한 후보는 검출/진입·금지 조건, 실제 상태/자원 소유자, 영향 범위·순서·동시성, 타 Stack/정상 경로 영향, 중복/반복 방지, 완료·실패 처리와 관측/검증을 추가 검토해요.

## 5. 효과 평가 계획

보정에 사용한 Seed와 평가용 사례를 구분해요. 평가 사례로 규칙을 수정하면 그 사례는 보정용으로 옮기고 별도 평가 사례를 남겨요.

- 수정된 Seed, 알려진 누락/미해결 유사 결함.
- 닮았지만 정상인 경로, 다른 계층에서 보호된 경로, 실행 조건 불성립 경로.
- 자료 부족 사례, 검색 결과 잘림·중단·재개·의존 코드 변경 사례.

같은 모델/설정·source·사례·도구·예산·기존 결과 재사용 조건에서 기존/확장 절차를 비교해요. 확인된 신규 결함·오탐/이미 해결됨 재보고·알려진 결함 누락·적절한 보류·trace·동일 입력의 변동과 시간/호출/입출력량을 함께 기록해요.

정답 집합이 있는 사례 세트에서만 그 집합에 대한 누락/재현율을 계산해요. 실제 코드의 알려지지 않은 결함 전체에 대한 재현율을 주장하지 않아요. 한두 건은 절차 확인이며 효과 판정에는 여러 대표 사례가 필요해요.

이 절은 **계획**이에요. 아래 저장 스킬의 시험 통과 수를 이 분석 방법의 정확도나 L1 제품 효과로 보고하지 않아요.

## 6. 관리 스킬에서 구현한 저장·조회 계약

| 대상 | 개발 후보 | SHA-256 |
|---|---|---|
| work-ledger-kernel | 0.7.46 | dabd412847354c77ca105da3ed686924f676f5f3c67428a2b984e68f2998076e |
| l1-fix-workflow | 1.6.75 | d13259cd0c9359dee2cddcb1c622fce5d98b663f9bc6eaea48c8a1c3b46b9ce4 |

두 후보는 development_not_for_deployment예요. 신규 저장/연결 시험 23건 PASS, 관련 합계 100건 중 97 PASS·2 FAIL·1 ERROR였고 실패 3건은 수정 전 원본에서도 같았어요. 신규 독립 코드 리뷰·업무 호스트 통합은 NOT_RUN이에요. 이번 전달은 **MD만**이며 후보 ZIP 공개·설치·정식 배포를 포함하지 않아요.

이 API가 실제 설치본에 있다고 가정하지 않아요. 업무 GPT는 기존 동등 기능과 아래 개발 계약을 대조해 설계하며, 미지원이면 필요한 최소 연결 gap을 명시해요. 사용자에게 설치본 자료를 다시 요구하는 흐름으로 돌아가지 않아요.

### 원본 등록

- 기존 Work ID에 UTF-8 Markdown 또는 JSON object 보고서를 연결. 최대 5 MiB.
- provider=l1-channel-recovery / kind=recovery_analysis / stage=utility.
- utility는 부가 보고서 보존이며 기술 분석 완료 stage를 대신하지 않아요.
- provider_version·code_rev·summary는 호출자가 제공하는 출처 선언. JSON에 해당 provenance가 있으면 선언과 일치해야 해요.
- Kernel preview: recovery_report_preview(work_id, source_path, provider_version, code_rev, summary).
- Kernel 등록: record_recovery_report(work_id, source_path, provider_version, code_rev, summary, expected_sha256, expected_revision).
- preview의 source_sha256·evidence_revision을 고정해 등록. Work·원본 ID/SHA를 재조회해 저장 여부 확인.

기존 Workflow attach-evidence가 같은 preview/apply 경로를 연결해요. 아래는 **구현 계약 예시이며 이번 설계 요청에서 실행할 명령이 아니에요.**

```text
<기존 Workflow launcher> attach-evidence --work-id <기존 ID> --file <결과 MD/JSON> --kind recovery_analysis --provider l1-channel-recovery --provider-version <실제 선언 버전> --code-rev <고정 대상 revision> --summary <요약>
```

별도 유효한 실행 지시가 있을 때 기존 허용 로컬 writer가 preview의 값과 기존 actor/session으로 apply해요. writer 환경 플래그의 신규 활성화 지시가 아니며 MCP read-only 모드에서는 로컬 첨부를 거부해요.

### 재시도와 읽기

Work/본문 hash/생산자 버전/source revision이 같으면 기존 Evidence를 재사용하고, 다른 내용·revision은 이전 원본과 별도 보존해요. stale preview·원본 변조·동일 identity의 다른 summary는 충돌로 거부해요. confidence는 AUTO_CANDIDATE이며 이전 기각 상태를 재시도로 올리지 않아요. 원격 게시 실패로 분석·등록을 다시 실행하지 않고 기존 등록/원격 이력을 확인해 필요한 단계만 복구해요.

Kernel work_recovery_reports(work_id) 또는 recovery-list --work-id <ID>는 원본 경로·SHA와 저장 메타정보를 읽어요. 기존 docs export가 다음 파생 보기를 만들어요.

- works/<work_id>/RECOVERY.md, works/<work_id>/state/recovery_reports.json.
- 루트 RECOVERY.md, index/recovery.json.
- 실제 artifact publish mapping/SHA를 이용한 원본 보고서 링크.

이는 재생성 가능한 읽기 projection이에요. 새 Work 원장·RECOVERY profile을 만들지 않아요. 보고서 등록/export/Git 게시/Viewer 조회/기술 검증/제품 시험을 별도로 보고해요.

## 7. 업무 환경에서 설계할 연결과 산출물

| 구성요소 | 책임 |
|---|---|
| l1-channel-recovery | 원인 규칙·후보 검증·조치 판단과 전체 결과 보고 |
| code-analyzer·기존 Git/P4/Jira·조건부 issue-analyzer | 실제 코드 사실·변경/계보·필요한 로그 근거. 각 실제 생산자의 출처 유지 |
| Kernel·허용 writer | 같은 Work의 보고서 원본·Evidence·hash·이력 보존 |
| Workflow | 기존 Work 선택/재개와 기존 첨부·게시 연결. 저장 때문에 전체 분석을 강제하지 않음 |
| Viewer/읽기 adapter | 저장된 Recovery projection을 기존 문서/읽기 계약에 연결 |
| Knowledge Updater | 개인 Knowledge의 Recovery 모음과 재사용 지식, 선택적 그룹 후보/Preview 연결 |
| l1-github·doc-converter | 기존 허용 Git 게시·필요한 문서/MSC 표현 재사용 |

업무 GPT는 다음을 같은 기존 업무 Work에 설계 결과로 정리해 주세요.

1. 이전 V0~V6와 이번 보완의 매핑, 기존 기능 재사용·확인된 gap·미확인.
2. 대표 비-timeout Seed 하나의 원인 규칙·필요한 코드 범위·보정/평가 사례 계획.
3. 저사양 LLM의 후보별 입력 묶음·짧은 근거 표·추가 조회·확대/중단/재개 방식.
4. 실제 생산자 출력→기존 Work→허용 writer→읽기/Viewer·선택적 Updater의 매핑.
5. 실제 파일/함수/입출력·권한에 근거한 최소 설계와 시험·부분 실패·호환 계획.

분석 원본에는 Seed와 현재 source, 규칙 revision, 조사/미분석 범위, 후보별 보호·반례·판정, 검출·복귀 조건, 실제 시험/NOT_RUN을 남겨요. 각 항목을 Kernel root metadata의 새 필드로 추가하라는 요구는 아니에요.

저장 연결의 향후 수락 기준은 원본 ID/SHA 재조회, Recovery 보기→Work/보고서 연결, 기존 기술 탐색 유지, 동일 결과·부분 실패에서 중복 방지, 이전 revision/기각·보류 보존과 상태 분리예요. 이번 인계만으로 해당 시험을 실제 업무 자료에 실행하거나 결과를 PASS로 기록하지 않아요.

제한 코드·상세 MSC·로그·고객자료·비밀은 허용된 업무 Work에 보존해요. 원문이나 비민감 요약의 외부 전송을 설계 완료 조건으로 요구하지 않아요. 전달용 GitHub 서비스·인증을 업무 스킬의 실행 의존성으로 추가하지 않아요.

## 8. 참고와 이번 확인 범위

- [기존 분석 인계 r0002](L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0002_20261119_KST.md): 기존 분석 방향과 timeout 제외 유지.
- [CodeQL 공식 개요](https://codeql.github.com/docs/codeql-overview/about-codeql/): 변형 분석의 기준 관점 참고. 공식 본문 조회.
- [TyPatch, arXiv:2609.13728](https://arxiv.org/abs/2609.13728): 규칙 추출과 분석 구현 분리 관점 참고. 이번에는 arXiv 초록의 검색 결과로 확인했으며 전체 실험 조건·심사/학회 채택 상태를 확인한 것은 아니에요.
- [Trail of Bits variant-analysis 원문](https://github.com/trailofbits/skills/blob/main/plugins/variant-analysis/skills/variant-analysis/SKILL.md): 원인 이해·좁은 기준 보정·점진적 일반화·후보 판정 참고. 이번 조회 Git blob 8f58f54b1883110f1a38a51c9360d4b9d1b195a8.

조회 기준: 2026-11-20 KST. 위 아이디어의 L1 적용 절차와 평가 계획은 설계 제안이며 외부 연구의 검증 성과가 아니에요. 이번 보완/문서 전달에서 스킬 코드·제품 코드·설치·분석/Job·유료 리뷰를 새로 실행하지 않았어요.

**첫 행동:** 업무 GPT가 이미 전달받은 분석 방향을 이어, 기존 Work에서 원인 규칙·후보 검증·평가 계획과 저장/읽기 연결을 실제 접근 가능한 계약에 매핑해 설계를 작성해 주세요. 사용자에게 MCP 자료 제공을 다시 요청하지 않아요.
