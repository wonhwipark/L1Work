# L1 MSC → Procedure/Feature MD 링크 — 업무 GPT G0 검토 인계

- 개정: r0001 / 2026-11-16 KST
- 정본: GitHub PUBLIC `wonhwipark/L1Work`, branch `main`, 경로 `handoffs/L1_MSC_LINK_SKILL_G0_REVIEW_HANDOFF_r0001_20261116_KST.md`
- 단계: **읽기 전용 G0 설치본·인터페이스 확인 요청**. 인계 게시만으로 업무 검토/수정/시험/설치/지식 게시/유료 호출이 실행되지 않음
- 선행 문서: [Knowledge Updater × Workflow r0005](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md), [MSC B 뷰어 컨셉 리뷰 r0001](L1_KNOWLEDGE_MSC_B_VIEWER_GPT_REVIEW_HANDOFF_r0001_20261114_KST.md). 기존 인계·승인·실행 상태를 대체하지 않는 좁은 후속 요청

## 1. 목표와 스킬별 책임

두 진입, 즉 `l1-fix-workflow` 업무 분석과 `l1-knowledge-updater` 직접 Procedure/Feature 분석 모두 **동일 업무용 `l1-workspace` Work**에 초안·코드 사실·MSC 원본·Evidence·결정을 보존한다. 승인된 그룹 지식만 `l1sw-dev-knowledge`의 실제 writer에 반영한다. 검증된 기존 분석은 HTML 보기를 위해 재실행하지 않는다.

| 대상 | 공개 소스 기준 / 실제 설치 확인 | 우선 검토 |
|---|---|---|
| `doc-converter` | [v0.2.21 ZIP](../doc-converter_v0_2_21_1106.zip) | 기존 renderer/MSC package 재사용. SVG 내장 **B형 단일 HTML** 자동 생성, 파일명 충돌 방지, 조건부 Phase 이동은 최소 EXTEND 후보 |
| `work-ledger-kernel` | [v0.7.37 ZIP](../work-ledger-kernel_v0_7_37_1103.zip) | Work·Evidence·게시 경로·hash·readback CONNECT. SVG 복사가 정말 불가할 경우 제한된 EXTEND 후보 |
| `l1-fix-workflow` | [v1.6.67 ZIP](../l1-fix-workflow_v1_6_67_1110.zip) | 기존 Work 조회/재개·분석/MSC handoff REUSE·CONNECT. 별도 렌더러나 그룹 writer 신설 금지 |
| `code-analyzer` | [v0.15.2 ZIP](../code-analyzer_v0_15_2_1107.zip) | 검증 코드 사실·기존 MSC 참조·source revision REUSE. viewer 목적으로 분석 재실행 금지 |
| **`l1-knowledge-updater`** | **업무 설치본 원문·버전 미확인 / 후속 G0 필수** | 두 진입의 같은 Work 저장, 후보/Preview/승인, 그룹 writer·MSC 링크 연계 확인 |

추가 확인: 그룹 공용 `l1sw-dev-knowledge` writer의 실제 I/O·권한·저장 위치, 기존 Git 게시 및 HTML/SVG 독자 접근. 동명 GitHub.com 저장소를 업무 정본으로 추정하지 않는다. 공개 ZIP과 설치본의 동등성은 미확인.

## 2. 업무 GPT 읽기 전용 확인 질문 Q1~Q8

**Q1 / Updater 두 진입:** 설치된 `l1-knowledge-updater`의 버전·entrypoint·I/O는 무엇인가? 직접 분석과 Workflow 결과 인계가 각각 같은 업무 Work를 저장/갱신하는지 확인. 전체 Workflow를 Updater 저장의 필수 호출로 만들지 않음.

**Q2 / 입력 호환:** `code-analyzer` semantic spec, verified scenario IR, 기존 PUML/MSC 중 실제 producer가 내는 유형과 converter가 받는 유형을 분리. 실제 source revision·`msc_ref` 근거와 기존 exporter/adapter 여부를 확인. IR을 임의 추정하지 말 것.

**Q3 / converter:** 설치본 MSC→원본/SVG/HTML 변환·manifest·filename 정제·크기 상한·렌더 실패 처리 확인. 정제 뒤 한글 시나리오명 충돌 시 덮어쓰기가 발생하는가? 임의 단계 좌표 대신 SVG의 실제 divider 라벨과 정확히 1개 일치할 때만 이동 가능하게 할 수 있는가?

**Q4 / Kernel 게시:** 실제 Evidence 등록/export가 `.html`/`.svg`/`.puml`을 어떤 조건·size gate로 수용하는가? 게시 때 파일명이 rename된다면 실제 `published_path`/hash/size/readback과 대상 MD 상대 링크를 매핑할 수 있는가? 무음 누락 시 완료 처리하지 않는가?

**Q5 / MD writer 소유권:** Workspace MSC 절은 각 진입의 기존 writer, 그룹 MSC 절은 승인된 그룹 writer가 최종 책임지는가? 기존 marker·Preview/diff·수동 본문 보존·source revision 충돌 감지·중복 append 방지 계약이 있는가? 미확인이면 자동 덮어쓰기 보류.

**Q6 / 그룹 지식:** `l1sw-dev-knowledge`의 실제 그룹 writer와 Updater의 후보·중복/충돌·Preview·승인·게시·readback 연결 확인. 그룹 독자가 개인 Work의 비공개 뷰어 URL을 열 수 있다고 가정하지 말 것.

**Q7 / 단계별 폴백:** 실제 브라우저 HTML URL/권한·SVG 표시가 확인되면 'MSC 확대 보기'; HTML 렌더 불가면 SVG 보기 + HTML 다운로드; SVG도 없으면 원본 + '그림 미완료'; 원본도 없으면 빈 링크 없이 미확보. 없는 `MSC_DELTA.md` 등 선택 자료 링크를 생성하지 않는지 확인.

**Q8 / 실패 격리:** 게시 자산과 MD의 hash/revision/readback을 순서대로 대조하고 링크를 마지막에 연결할 수 있는가? 그룹 게시 뒤 Workspace 역링크 실패는 링크만 복구하고 분석/Job을 재실행하지 않는가? AS-IS Procedure 문서에 이슈 전용 변경 문구가 무조건 삽입되지 않는가?

## 3. 결과 회신 형식 및 검증 경계

| 구분 | 회신 요청 |
|---|---|
| G0 설치 사실 | 실제 스킬명/버전, 접근한 원문·함수·입력/출력, 읽기 전용 확인 방법·시점 |
| 구분 | `INSTALLED_SOURCE_READ` / `CONTRACT_READ` / `HOST_OBSERVATION` / `NOT_RUN` |
| 항목별 판정 | `REUSE` / `CONNECT` / 입증된 최소 `EXTEND` / `ADDITIONAL_CHECK_REQUIRED` / `BLOCKED` |
| 차이와 최소 보완 | 공개 ZIP과 설치본 차이, 변경 후보와 필요한 회귀시험. 미확인 API/field/schema를 만들지 않음 |
| 시험·적용 | `PASS/FAIL/SKIP/NOT_RUN`; 코드 정적 확인·업무 E2E·그룹 게시·브라우저 렌더·RAG 소비 분리 |
| 다음 한 행동 | 현재 허용된 검증으로 좁혀서 한 가지 제시. 비민감 판정 요약만 대화로 회신 |

**금지:** 이 요청만으로 설치/코드 수정·패키지 제작/배포·기존 metadata/Work/DB/그룹 지식 write·실제 회사 코드 재분석·모델/Job 호출·호스팅 변경을 실행하지 않는다. 회사 소스, 상세 MSC, 운영 경로, 로그, 고객자료, 인증정보를 GitHub PRIVATE/PUBLIC에 올리지 않는다. 상세 근거는 권한이 허용된 업무 호스트 내부에만 보존.

**업무 GPT 전달 문구:** “이 인계의 Q1~Q8을 현재 설치된 실제 스킬 원문과 기존 G0 결과를 바탕으로 읽기 전용 검토해 주세요. 기존 기능 REUSE/CONNECT와 입증된 최소 EXTEND를 구분하고, 두 진입·같은 Work·그룹 writer·MSC 링크/폴백 조건의 gap만 비민감 요약으로 회신해 주세요. 수정·실행·게시·유료 호출은 하지 마세요.”
