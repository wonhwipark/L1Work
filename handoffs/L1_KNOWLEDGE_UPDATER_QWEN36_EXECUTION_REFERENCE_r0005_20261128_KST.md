# L1 Knowledge Updater · Qwen 실행 참조서 r0005

2026-11-28 KST · [업무 GPT 실행 인계](./L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0005_20261128_KST.md)의 단계별 참조 · 한 실행에는 해당 절만 전달

## 1. G0 · 활성 지문, 분모, 실제 예산

| 항목 | 필요한 증거 | 실패 시 처리 |
|---|---|---|
| 실행 지문 | 같은 호출 체인의 agent/service → launcher·alias → 실제 script/설정 → 결과 영수증. realpath와 SHA-256을 업무 Work에 기록. Updater·Writer·Reader·Analyzer 및 사용 단계의 Converter/Viewer 등 실제 참여자의 지문을 확정. K2에서 선택한 bundle의 producer·source/build·입력 hash도 확인 | 필수 실행본 hash를 못 고정하면 이 Work의 A~E 전체가 HOLD. 재현·측정·수정·저장·비교 수치를 승격하지 않음. 기존 G0 읽기 진단과 이미 보유한 근거 보존만 진행. 재개 중 지문이 바뀌면 해당 측정 세트를 분리하고 G0 재확인 |
| 버전 차이 | 업무 보고는 Updater frontmatter 1.9.3 / MCP 1.9.1, Writer update 1.10.0, Skill Updater inventory 0.5.38 / capability 0.5.43 / 공개 0.5.44. Analyzer 과거 0.15.2/0.15.6, 공개 0.15.7. 운영 Viewer 0.5.7 사용자 확인, 공개 개발 0.5.8 | 라벨 차이의 원인이 캐시인지 다른 설치본인지 실제 호출 지문으로 판별. 업무 GPT가 읽을 수 없는 원본은 UNKNOWN. 공개 ZIP과 활성 설치를 별도 열로 기록 |
| root·분모 | Writer/Reader가 사용하는 동일 개인 Workspace의 canonical identity와 ACL을 기존 승인된 문서·영수증으로 대조. Map 최초 생성 전이면 부모 root·정책·빈 Map 상태를 검증. 그룹 HITS는 개인 조회 증거로 사용할 수 없음. 1,306 + legacy 121 = 1,427. legacy 57+38+25=120은 실제 파일 집합·중복·기타/제외 규칙으로 정산 | 정산된 목록·revision·필터의 digest와 개수를 고정하기 전 이 Work의 A~E 진행 HOLD. 숫자 1을 임의 기타 항목으로 채우지 않음. 파일 coverage 분모는 manifest, recall 분모는 별도 고정 gold 양성 수 |
| OpenCode 계측 | 동일 모델 ID/버전·tokenizer·활성 스킬/MCP·시스템 프롬프트·도구 정의를 고정. 한 실행에서 매 모델 호출별 요청/응답 usage 또는 동일 tokenizer의 직렬화 근거를 취득. 빈 증거를 넣은 통제 호출이나 기존 검증 영수증으로 고정 오버헤드와 동적 wrapping을 대조 | 실제 토큰을 확인할 수 없으면 TOKEN_USAGE_UNKNOWN. 초과/미측정 구간을 표시하고 모델 품질·비용 비교와 확대만 HOLD. 근사 글자 수를 계측값으로 쓰지 않음 |

**순 payload 예산.** 기존 비율 비교를 위해 task 전체 상한 32,768(입·출력 합계)과 20분은 유지한다. 모델이 쓸 수 있는 예산은 **순 payload**로 산정한다. 각 호출에서 시스템/도구 정의/프로토콜/그 밖의 고정 하네스 토큰을 H로, 질문·선택 근거·이전 대화나 도구 응답의 재전송·모델 출력(계상되는 reasoning 포함)을 P로 분류한다. 캐시 할인은 별도 비용 지표이며 토큰에서 재차 빼지 않는다. 도구의 업무 근거는 P, 직렬화 wrapper는 H로 한 번만 센다. `Σ(H+P) ≤ min(32,768, 승인된 task 총량)`. 공통 순 예산은 비교 조건 중 가장 작은 가용 총량에서 실측/예약한 누적 H를 뺀 값이다. 예를 들어 총량 32,768, 누적 H 8,192이면 P 최대 24,576이다. 이 숫자는 산식 예시다. 매 호출 직전 실제 window와 예약 출력 여유도 확인하고 남은 P가 줄면 반환 범위를 줄인다. 비교 조건마다 H/P/총량, 실제 본문 파일·시간·호출, 잘림을 기록한다.

## 2. A단계의 지정 산출물 · Map Lookup Envelope v1

Updater와 기존 개인 Reader 사이에서 사용하는 **논리 응답 계약**이다. DB·전용 MCP API·공통 지식 schema는 추가하지 않는다. 한 질문, 한 작업 증거 묶음, 한 snapshot·source/build, exact qualified symbol/Message ID, 한 관계 종류, 한 방향, 1-hop을 기본으로 한다. 양방향이 필요하면 두 독립 질의로 나눈다. 여러 질문이나 서로 다른 증거 묶음이 입력되면 업무 GPT가 첫 질문만 분리하고 후속 질문은 대기열에 둔다. 분리가 모호하면 `PARTIAL`과 재질문 하나만 반환한다.

아래는 단일 JSON 응답 예시다. `demo` 값은 합성 참조다. 실제 소비자는 받은 근거를 원문과 대조해야 한다.

```json
{
  "version": 1,
  "question_id": "q1",
  "evidence_bundle_id": "demo-bundle",
  "status": "PARTIAL",
  "pin": {"snapshot": "demo-s1", "source": "demo-rev", "build": "demo-A"},
  "query": {"exact": "Demo::Request", "relation": "registers", "direction": "out", "hops": 1},
  "records": [
    {"from": "Demo::Request", "to": "Demo::Handler", "claim": "테이블의 정적 등록", "origin": "EXTRACTED", "verification": "VERIFIED", "evidence_ref": "demo-e1", "anchor": "demo.cpp:17", "freshness": "CURRENT"}
  ],
  "coverage": {"examined": 1, "eligible": 2, "unit": "registration tables"},
  "gaps": ["두 번째 테이블 미조사", "실행 여부 미확인"],
  "truncated": false,
  "next_probe": "두 번째 등록표에서 같은 키를 확인"
}
```

| 계약 | 소비 규칙 |
|---|---|
| 상태 | OK/EMPTY/PARTIAL/STALE/CONFLICT/DENIED/ERROR. 미설정·미지원은 ERROR와 비민감 사유. 분모를 모르면 eligible=null. EMPTY는 조사 범위에서의 빈 결과. DENIED는 records=[], pin·근거·범위·추가 조회는 null/빈 값으로 반환해 비인가 대상의 존재를 드러내지 않음 |
| 경계 | 증거 1묶음은 같은 pin·같은 질문을 검증하는 여러 근거 행을 포함할 수 있음. 이름 일치, 정적 호출/등록, build 활성, 관측된 runtime은 각각 별도 명제. 잘린 근거를 확정으로 승격하지 않음 |
| 크기·절단 | Map 최대 50개 관계 행, 응답 전체 4,096 **실제 토큰** 이내. 전송 포맷도 50줄 상한을 적용하는 기존 소비자에는 compact JSON을 사용. 필수 메타·누락·truncated·next_probe 공간을 먼저 확보하고 완전한 레코드 단위로 자름. 초과 시 PARTIAL·truncated=true와 누락 요약 유지. 필수 메타조차 못 담으면 최소 오류 응답. 문자열 중간 절단·다른 질문으로 예산 채우기 금지 |
| 복수 질문·묶음 | 첫 질문·해당 묶음까지만 응답. 나머지는 PARTIAL, truncated=true, gaps에 보류 개수로 남긴다. 모호하면 레코드를 비우고 next_probe 한 개로 분리를 요청한다. 권한 거절 시 DENIED의 비공개 규칙이 우선 |
| 보강·fallback | step당 실제 소스 ≤20파일, task당 중복 제거 ≤60파일, 추가 probe 최대 4단계. stale/empty/미지원 시 기존 허용 scope에서 독립 원문 probe. 권한 거절은 해당 경로에서 종료. 정상 Procedure/Feature·MSC는 권한·revision이 일치하는 참조만 제공 |

Discovery 7건은 README, NR/LTE Map 각 1, message/handler 조사, gaps, manifest, 최종 보고로 항목별 hash·분모·재사용/부분 보완/충돌을 기록한다. 29개 증빙 해시와 1,427파일은 서로 다른 분모다. P0은 contains/include/declares/defines/calls, sends/receives/payload, registers/dispatches, guard/build. P1은 상태 read/write, 계층 경계·instance·timer/callback·knowledge_ref. P2 alias/data flow는 대표 질문의 결손에서만 검토한다. 전처리 sibling의 배제 조건·중첩 분기와 실제 build 적용성을 별도로 검증한다.

## 3. B단계 · 기존 Writer에서 manifest 하나로 snapshot 활성화

**기본안은 불변 조각 + 세대별 create-only manifest**다. 같은 저장 계층에서 이름이 서로 다른 manifest를 여러 개 생성하는 것만으로는 “현재”가 하나로 결정되지 않는다. 두 Writer가 같은 이전본에서 출발하면 **동일한 다음 세대의 한 경로**를 경쟁하도록 한다. 호스트 로컬 단일 파일 atomic replace만으로 다중 호스트 CAS를 보장할 수 없다.

1. 승인된 기존 Personal Store Writer로 형제 root `l1-workspace/source-map/`만 해석한다. 기존 workspace identity·actor·ACL·승인·검증·VERBATIM·원격 readback을 재사용한다. 논리 stream은 저장소·정규화한 scope·RAT/build 계열로 고정하고 source revision/추출규칙은 manifest에 기록한다. 다른 build는 별도 stream이다.
2. 관계·역색인·gap 조각을 정규화한 바이트의 SHA-256으로 이름 붙여 create-only 저장한다. 같은 이름/같은 bytes는 재사용, 같은 이름/다른 bytes는 무결성 실패다. 중간 조각만 있는 상태는 활성본이 아니다.
3. 기존에 검증한 세대 g의 manifest digest를 expected parent로 고정한다. 최초는 승인된 genesis 규칙에서 시작한다. 모든 조각의 hash·크기·접근 범위와 parent를 검증한 뒤, **g+1의 고정 슬롯에** 완성 manifest를 원자적 create-if-absent로 한 번 생성한다. stream·세대·parent digest·source/build·scope·producer/hash·조각 목록·coverage·요청 식별자를 포함한다. 공개 시점은 이 생성이 권한 있는 공통 저장소에 성공한 때다. 별도 가변 latest 파일·mtime 정렬·여러 파일 rename은 사용하지 않는다.
4. Reader는 알려진 검증 세대에서 연속하고 parent digest가 맞는 후속 슬롯만 따라간다. 질의 시작에 세대·manifest hash를 고정하고 그 manifest가 참조한 조각만 읽는다. 다음 슬롯 부재와 조회 실패를 구분한다. 누락/분기/손상/접근 불가면 마지막 확인본과 stale/partial/error를 명시한다. 강한 일관성이 검증되지 않은 reader는 “최신”으로 표시하지 않는다.
5. 같은 parent의 두 Writer 중 하나만 새 슬롯을 생성할 수 있어야 한다. 패자는 슬롯의 요청·hash가 같으면 이미 성공한 동일 요청, 다르면 CONFLICT다. 응답 유실은 원격 **기록 SHA**를 재조회해 정산한다. 이후 세대로 임의 재시도하지 않는다. 삭제·rename·등록 변경은 새 snapshot에서 tombstone/역링크 철회, old/new include·매크로·build 역의존 합집합을 갱신한다. 이전 snapshot은 pin된 reader를 위해 보존한다.

**최소 확장 한계.** 기존 Writer 안에서 Map root/유형 allowlist, 기존 단일 파일 무덮어쓰기 primitive의 연결, manifest 검증과 기존 Reader의 pin 해석까지 허용한다. 실제 이름·자료형은 기존 형식에 맞춘다. 기존 primitive가 파일 내용을 덮어쓰거나 호스트별로만 배타적이면 활성화 HOLD. 이미 제공되는 Git tree/조건부 ref 트랜잭션이 같은 원자성·기대 revision·readback을 충족하는지 대안으로 검토한다. 독립 Writer/DB·새 전역 잠금 서비스·raw Git 우회는 범위 밖이다. 기존 지식 G5 승인, 그룹 G6 승인, 개인 Map 쓰기 승인은 각각 기존 범위를 따른다.

## 4. C단계 · Procedure G-2와 소유자 응답 기한

공개 v0.15.7 ZIP에서 실제 launcher의 `behavior-doc` → `knowledge-inventory-export`를 합성 C++로 연결했다. `scripts/behavior_doc.py::scenario_flow`는 entry와 깊이 우선 탐색 정적 flow를 생성했다. 해소된 호출 2개가 있었으나 exporter는 exit 0, 대상 Procedure 0건. `scripts/knowledge_inventory_export.py::procedure_from_item`은 유효 step 2개 이상을 요구하며 `steps/ordered_steps/messages`는 각각 1건으로 추출됐다. 두 파일의 SHA-256 접두는 각각 `0603bee6ab1f`, `b0b08a815bdc`이다.

- **대상 확인.** 깨끗한 분석 root와 별도 출력 경로를 쓴다. `--artifact`는 analysis-root의 다른 JSON·MD를 제외하지 않는다. 실제 대조에서 대상 facts와 무관한 Procedure를 함께 두면 무관한 ID만 1건 반환됐다. input artifact hash, source digest, 대상 ID와 각 step 근거를 대조한다. 기존 resume 지문에는 입력 경로·크기·mtime이 사용되므로 수정 전 0건 캐시를 재사용하지 않는다.
- **호환 경계.** Analyzer 관리자는 확인된 `behavior-facts/v1` 입력만 분기한다. 기존 message-procedure 의미에 맞는 근거와 참여자·방향·조건·순서가 있을 때만 승격한다. DFS 순서, `resolved=true`, 이름 일치, 기본 required 값은 비동기 순서의 증거가 아니다. 미해소·단일 step·상호배타 분기·동명/다른 variant는 명시적 gap. 동일 ID/steps에 fragments만 다른 두 입력은 기존 digest가 같을 수 있으므로 분기·variant까지 대조한다.
- **소유자 대기 종료.** G0에서 실제 실행 지문이 고정됐지만 유지보수 담당자가 미확인/무응답이면, 기존 Work에 담당 후보·요청 시각·실패 bundle hash를 1회 기록한다. 이 인계의 기본 대기 상한은 **다음 업무일 종료(KST)**다. 그때까지 답이 없으면 `GAP_FROZEN_OWNER_UNCONFIRMED`로 C만 동결한다. 소비 경계에서 flow→steps를 번역하는 임시 어댑터는 채택하지 않는다. 원본 facts와 검증된 기존 Procedure만 각각의 근거 수준으로 사용하고 A/B/D/E는 허용 범위에서 진행한다. 소유자 확인·계약/지문 확보 시 같은 사례로 C만 재개한다.
- **통과 근거.** 기존 RACH positive와 세 별칭·1-step, 실제 실패 bundle, 기대 ID/steps를 독립 고정한 변환 가능 양성 1건, 분기·비동기·혼입·재개 반례를 K2→K3까지 대조한다. 적격 사례의 필수 관계 누락과 허위 Procedure는 각각 0. 정당한 제외는 0건과 사유를 함께 기록한다.

## 5. D단계 · 기존 문서 품질과 Map 확대 중단 기준

**기존 문서의 수정 단위는 잘못된 주장 또는 근거가 빈 섹션 하나**다. Module(구조·요소·인터페이스·Features), Feature(원리·조건·상태·Scenarios), Procedure(API·caller/callee·인자·전제·반환·부작용), Scenario(개요·조건·구조·흐름·본문 MSC·예외), Issue(증상·원인·수정·영향·검증)의 기존 ID와 교차 참조를 유지한다. 기존 Scenario UD-1의 10개 H2·순서가 우선이다. 역할을 실제 제목·heading ID에 매핑하며 모르는 제목은 G0에서 확인한다. §1~7 기술 내용, §8 미확인/보류, §10 실제 anchor·중복 검토·MSC 계보를 대조한다. §9 및 미제공 제목은 추정하지 않는다. UD-2~4의 본문·분류·H1, UD-5~10의 anchor·MSC·frontmatter·계보는 실제 게이트와 증거로 재검증한다. 문서의 글자 수·anchor 수가 맞더라도 기술 의미·K5.7 coverage는 별도 판정한다.

**평가 계획.** 대표 NR L1 Tx → UL Tx Switching와 별도 holdout에서 양성 ≥30·음성/반례 ≥10을 사전 고정하고 gold는 모델 입력에서 제외한다. U-baseline→A 요청 정규화→B 기존 Analyzer 연결→필요 시 C 국소 수정으로 비교한다. Map M-D0 현행 / D1 제한 Map / D2 검증된 정상 Procedure / D3 둘 다. Recovery R-D1은 검증 코드 fact이므로 M-D1과 실험을 섞지 않는다. 비교 시 같은 source/build·모델·질문·도구·공통 순 payload·결측 처리 규칙을 적용한다.

**프로그램 중단 기준은 holdout에서 한 번 적용한다.** 먼저 안전선(근거 없는 확정 0, 범위 밖 읽기 0, 중요 분기 누락·잘못된 MSC 방향/순서 0, stale/variant 탐지 100%, recall ≥90%)을 통과해야 한다. 이후 Map의 부가 효과는 **D2 대비 D3**로 판단한다.

| 판정 | 사전 결정 규칙 |
|---|---|
| 확대 | 안전선 충족 후 **recall +5%p 이상**이면서 총 토큰·시간이 기존 task 상한 이내이거나, **recall과 precision이 악화되지 않으면서 실제 총 입출력 토큰 15% 이상 절감**. precision의 분모가 0이면 N/A여서 비용 경로의 동등성은 미입증. 양성 30개에서 순증 1개는 3.33%p |
| 중단 | 유효 holdout에서 위 두 확대 조건을 모두 충족하지 못하면 다음 모듈/전체 1,427파일로의 **Map 확대를 중단**한다. 기존 검증 snapshot·정상 Procedure·직접 Analyzer 경로는 재사용. 안전선 실패도 확대 중단이며 원인만 기록 |
| 측정 보류 | 분모·tokenizer·오버헤드·동일 pin·영수증이 미확인이면 성능 결론을 내리지 않는다. 누락된 측정을 복구할 때까지 확대 동결 |

5%p·15%는 이번 설계의 파일럿 기본 운영값이며 달성 실적이 아니다. recall 분모에는 미조사 양성을 포함하고 precision은 올바른 확정/전체 확정이다. 구축/갱신 비용, 실제 본문 읽기, 순 payload·총 토큰·시간은 각각 기록한다. 표본 1회의 결과를 제품 전체로 일반화하지 않는다.

## 6. E단계 · 영향 범위와 자체 검토 기록

| 소유자/구현 | 판정 및 회귀 |
|---|---|
| Updater / 개인 Writer·Reader | K0·K2·K4·분류·기존 지식 Writer REUSE. Map orchestration·read CONNECT. 업무 보고의 Scenario 3-depth 제약은 독립 root와 불일치, 다중 호스트 create-only·pin은 UNKNOWN. U20~U22로 검증. 요청·승인·원격 기록 SHA 일치 확인 |
| Code Analyzer / Preflight | G-2는 공개판 PROVEN_GAP, 업무 활성본 UNKNOWN. 기존 bounded scope/probe·git-incremental·reuse-validate 재사용. knowledge-analysis-preflight는 근거 참조 검증만 담당 |
| Viewer / Recovery | 개발 v0.5.8 메뉴·합성 adapter 재사용, 실제 운영 v0.5.7 및 Reader/ACL은 G0 확인. 검증된 heading/revision만 화면 순서 변경. Recovery는 정상 Procedure와 Map 선택 조회, 실패 시 bounded 분석. 기존 Work·Knowledge·MSC UI, Recovery V2/V3/V4 무퇴행 |
| Doc Converter / Kernel / Fix Workflow | 기존 Converter `msc-package` 또는 `msc-scenario-build --view-mode PROCEDURE_FEATURE`로 검증 IR→PUML/SVG/HTML·manifest, 실제 파일·상대 링크·방향 판정. Kernel export 전후 개인 지식/Map hash와 index 확인. Workflow v1.6.75의 개인 경로 검사는 knowledge/만 명시하므로 source-map/에 대한 실제 종단 쓰기 차단을 검증. 재현된 담당 경계만 보완 |

**이번 인계의 자체 검토 체크리스트**는 기존 설계와 모델/업무 호스트 판정을 구분하는 명시적 산출물이다. 업무 GPT는 같은 항목에 증거/분모·실패·재개점을 추가해 회신한다.

| 점검 | 증거·판정 |
|---|---|
| ① 저장·경합 | §3의 immutable 조각·부모 고정·유일 세대 슬롯·reader pin·응답 유실을 합성 모델에서 대조. 실제 Writer의 다중 호스트 보장은 G0/B 대기 |
| ② 활성본·⑦ 집계 | 해시 미확정→A~E HOLD, 121/120 차집합을 G0 필수로 지정. 업무 원본 정산 미실행 |
| ③ G-2 교착 | 다음 업무일 종료·C만 동결·기존 검증 Procedure 사용·소유자 확인 시 재개. r0004의 공개 launcher 재현과 구분 |
| ④ 자체검토·⑤ 우선순위 | 현재 체크리스트와 본문 첫 페이지에 문서별 효력 명시. 리뷰 입력 r0004는 고정 원본으로 보존 |
| ⑥ 가치 판정 | D3−D2 확대·중단·측정 보류의 경계값 합성 대조. 실제 Qwen 효과 미측정 |
| ⑧ 실행 형태·⑨ 응답 | 단계별 질문/입력/출력/종료 조건과 별도 참조서, Envelope 예시 JSON 구문 및 필수 필드 점검. 실제 Qwen tokenizer는 G0 대기 |
| ⑩ 오버헤드·⑪ 한 질문 | 호출별 H/P, 순 예산 산식, 한 질문·한 묶음·예산 초과 때 레코드 단위 절단 규칙 명문화 |
| 기존 근거 | 공개 패키지 격리 시험 Analyzer 85/85, Viewer 8/8 Node 프로그램, Converter 표시 13/13, Kernel 합성 export 2회에서 두 root 표본 4개 hash 보존. 업무 보고의 485/485와 별도 32/32·59/59 및 Confluence 1 SKIP은 개별 기록. G4 근거 14, G5 승인 지식 5건 기록 SHA 일치 보고, G6 그룹 게시 미실행. 과거 보고의 SHA 관련 오타는 이 인계에서 ‘기록 SHA’로 정정 |

업무 수락 시 T01~T18·U19~U23 및 기존 UD suite를 재사용한다. 추가 시험은 최초 저장·동일 재시도·경합/중단·응답 유실·reader pin·삭제/rename·양방향 역의존, 부재/오류/거절, 문서의 잘못된 anchor·뒤집힌 MSC를 포함한다. 승인 없는 배포·Job·그룹 게시·추가 독립 리뷰는 이 인계의 실행 단계에 포함하지 않는다.
