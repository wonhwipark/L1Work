# L1 Channel Recovery — Workspace·Kernel·Viewer 통합 인계서

- 문서 식별: `L1_CHANNEL_RECOVERY_WORKSPACE_VIEWER_NEW_CHAT_HANDOFF_r0002_20261124_KST.md`
- 버전: r0002 · 기준일: 2026-11-24 KST
- 문서 성격: **새 대화창 재개용 인계(복구 재구성본)**. 이전 대화에서 생성한 r0002의 원본 바이트를 회수하지 못해, 당시 합의 및 확인 내용을 재구성했다. 원본과 바이트 동일성을 주장하지 않는다.
- 주요 기존 Work: `L1-WORKSPACE-RAG-20261111-001` (Recovery 연계 범위는 기존 Work에서 재개)
- CoWork 정본: GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab`, branch `main`
- 업무 연계 저장소: 업무용 `l1-workspace` (실제 원격 주소·branch·쓰기 권한은 업무 환경에서 확인)
- 공개 전달 경로: GitHub PUBLIC `wonhwipark/L1Work`, branch `main`, `handoffs/` (공개 허용된 비민감 인계만)
- 주의: **문서 작성·게시만으로 실제 업무 GPT 설치, 코드 변경, 호스트 실행 또는 공개 배포가 완료되는 것은 아니다.**

## 1. 이번 작업의 확정된 목적

`l1-knowledge-updater`가 `l1-workspace/knowledge/`와 연결되는 방식에 대응해, 업무 GPT가 관리하는 `l1-channel-recovery`의 분석 결과를 `l1-workspace/recovery/`에서 일관되게 관리하고 Viewer에서 탐색·열람할 수 있도록 **우리 쪽 공통 저장·조회 인프라를 검토·개발**한다.

중요한 **책임 분리**:

| 구성 | 작업 소유자/책임 | 본 인계의 개발 범위 |
|---|---|---|
| `l1-channel-recovery` | **업무 GPT**: 과거 PR/P4 CL 분석, 원인 패턴/유사 결함/방어 검증, Recovery 필요성 판정, Edge 분석 의미 확정, AS-IS·TO-BE MSC 생성 | 실제 스킬 수정은 **우리 작업 범위 제외**. 정확한 입력·출력 계약 요구사항을 업무 GPT에 인계 |
| `code-analyzer`, `l1-github`, P4 관련 도구, `issue-analyzer` | 업무 GPT/업무 Agent: 코드·이력·로그 근거 확보 | 기존 결과 재사용, 미확인 기능 추가 가정 금지 |
| `doc-converter` | 업무 GPT의 MSC 생성 흐름에서 기존 변환 계약 재사용 | Converter 새 구현 금지; HTML/SVG/PlantUML 아티팩트를 받아 저장·표시 |
| `work-ledger-kernel` + 기존 writer | 기존 Work 선택·재개, Evidence/Artifact 원본·revision·SHA·링크·인덱스·권한 계약 | **우리 개발 핵심**: Recovery 결과의 `recovery/` 관리 및 Work 연결. 기존 기능 재사용 후 실증된 결손만 수정 |
| 기존 Workflow(예: `l1-fix-workflow`) | 기존 Kernel/writer 중개; Work 생명주기·승인·CAS·중복 방지 | 필요 시 **최소 연동 수정**, 기존 기능·동일 버전 충돌 보존 |
| `L1 Workspace Viewer` | 읽기 어댑터, 탐색·상세·MSC 표시 | **우리 개발 핵심**: Recovery 항목 검색/필터/상세/원본 Work·MSC 링크 |
| `l1-knowledge-updater` | Recovery에서 확인된 재사용 지식의 팀 Knowledge 게시 별도 담당 | 직접 수정 기본 제외. 확정 지식은 Updater의 기존 승인·게시 절차로 연결 |

이번 범위의 중심은 **Viewer와 work-ledger-kernel**, 필요 시 Workflow의 연결 보완이다. Recovery 분석 로직·Edge 판정·MSC 변환을 우리 쪽에서 중복 구현하지 않는다.

## 2. 선행 검토 및 당시 마지막 상태

이전 대화에서 확인했다고 보고된 인계/검토 자료(아래 링크는 확인 대상 경로이며 **이 재구성 과정에서 최신 원격 본문 재검증을 수행하지 않았음**):

1. 2026-11-19, 분석 상세 설계 r0002: `handoffs/L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0002_20261119_KST.md`  
   https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_RECOVERY_POINT_ANALYSIS_DETAILED_DESIGN_AND_IMPLEMENTATION_HANDOFF_r0002_20261119_KST.md
2. 2026-11-20, Recovery Workspace 구현 계약 r0002: `handoffs/L1_RECOVERY_WORKSPACE_IMPLEMENTED_CONTRACT_HANDOFF_r0002_20261120_KST.md`  
   https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_RECOVERY_WORKSPACE_IMPLEMENTED_CONTRACT_HANDOFF_r0002_20261120_KST.md
3. 2026-11-24, Viewer v0.5.2 · MSC·Updater·Converter 통합 인계 r0002: `handoffs/L1_WORKSPACE_VIEWER_V052_MSC_UPDATER_CONVERTER_COMPLETE_HANDOFF_r0002_20261124_KST.md`  
   https://github.com/wonhwipark/L1Work/blob/main/handoffs/L1_WORKSPACE_VIEWER_V052_MSC_UPDATER_CONVERTER_COMPLETE_HANDOFF_r0002_20261124_KST.md
4. CoWork 관련 상태: `collab/CONTEXT_BRIEF.md`, `collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md`  
   https://github.com/wonhwipark/CoWork-Skill-Collab/blob/main/collab/projects/L1-WORKSPACE-RAG-20261111-001/CURRENT.md
5. CoWork 이전 통합 검토: `collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_RECOVERY_WORKSPACE_SKILL_INTEGRATION_REVIEW_r0001_20261120_KST.md`.

당시 판단:
- 11/20 Recovery 공개 인계는 r0002가 마지막으로 확인되었고, **분석 자체의 개선을 우선하며 Workspace/Viewer 연동은 후속 범위로 보류**하는 결정이 있었다. **이번 사용자 요청은 그 후속 연동의 검토·진행 지시**다.
- 당시 Recovery 스킬의 업무 GPT **실제 설치 버전, 분석·정확도, 업무 호스트의 전체 E2E 실행 결과는 미확인**이었다.
- Recovery 관련 Kernel 후보 `v0.7.46` / Workflow 후보 `v1.6.75`(11/20)가 있었다는 보고가 있으나 개발 후보와 운영 설치는 구분한다.
- 이후 Viewer 흐름의 Kernel `v0.7.43` / Workflow `v1.6.75`(11/21) 후보가 있었다. **Workflow v1.6.75라는 같은 문자열이 서로 다른 소스·ZIP에 사용된 충돌**이 보고되었다. 실제 SHA, zip 내용, 차이를 다시 비교하고 필요한 변경을 새 고유 버전으로 통합해야 한다. 숫자가 더 크다는 이유로 덮어쓰지 않는다.
- 기존 Kernel Recovery projection 후보의 `RECOVERY.md`, `index/recovery.json`과 사용자가 요청한 **물리적 `recovery/` 폴더 관리 기능은 서로 다른 요구**다. 설치되었다고 가정하지 않는다.

## 3. 업무 GPT가 수행하는 Recovery 분석 흐름

1. 기존 merged GitHub PR 또는 P4 submitted CL(시드)을 입력으로, 수정 전/후 코드의 실제 결함 원인을 분석한다.
2. 결함 원인을 대상 객체·상태·순서·조건·누락된 방어 등의 검증 가능한 **원인 규칙**으로 구조화한다.
3. 현행 코드에서 유사 패턴 후보를 찾는다. **Caller·Callee·공통 계층의 기존 방어** 및 실행 가능성을 확인하고, 이미 해결/불가능한 후보를 배제한다.
4. 필요 시 `원인 수정 / 사전 검사 / 런타임 Recovery / 상위 절차 이관 / 추가 근거 필요` 등을 비교하고 실제 Recovery 필요성을 판정한다.
5. 저사양 LLM에 맞춰 탐색을 순차로 수행하고, 확대/종료 기준·반례·검증되지 않은 가정을 명확하게 기록한다.
6. MSC가 유의미한 경우 기존 `doc-converter`를 써서 **Seed 수정 전·후**, **후보 AS-IS**, **조치 TO-BE** MSC를 산출한다. Converter 결과 HTML/SVG/PlantUML은 원본 입력·revision과 함께 연결한다.

**Edge 관련 미확정 사항**: 과거 11/19 인계에 위 MSC 구분은 명시됐다는 이전 검토 결과가 있다. 반면 `Edge`가 무엇을 의미하는지(예: 인과 관계의 호출/상태 전이, 그래프 Edge, 특정 검증 결과 등) 및 별도 산출물의 스키마·판정 계약은 **기존 공개 인계에서 확정적으로 확인되지 않았다**. 이를 임의 정의하지 않는다. 업무 GPT에 Edge의 의미·생성 조건·출력 형식·Evidence 링크·AS-IS/TO-BE에서의 표현을 확인한 후 Kernel/Viewer 표시만 매핑한다.

## 4. 권장 Workspace 저장 원칙 (확정 구현이 아니라 설계 제안)

```text
l1-workspace/
├─ works/<work_id>/          # 기존 Work 원본, 근거, 실행 이력, Evidence·Artifact
├─ knowledge/                # 기존 Updater 관리 경로(계약 재사용)
├─ recovery/                 # 신설 요청: Recovery 분석의 탐색·현재 상태 뷰
│  ├─ README.md              # 탐색/기본 안내(선택)
│  ├─ <module>/              # 실제 모듈 식별자/분류 계약 확인 후 확정
│  │  └─ <case-id>.md        # 사건·규칙·후보·조치·근거 연결(제안)
│  └─ ...
├─ RECOVERY.md               # 기존 Kernel 파생 projection 후보(실재 여부 확인)
└─ index/recovery.json       # 기존 Kernel 파생 인덱스 후보(실재 여부 확인)
```

저장 규칙:
- **단일 원본**: 분석 실행·변경·검증 근거의 권위 있는 원본은 Work/Evidence 체계를 따른다. `recovery/`는 Recovery 케이스의 정리·탐색 문서 또는 읽기 모델이며 원본 보고서를 중복된 독립 정본으로 생성하지 않는다. 어떤 내용이 어느 위치의 정본인지 설계에서 명시한다.
- `recovery/`의 쓰기 소유권은 업무 GPT의 Recovery 작업이 가지되, 실제 commit/writer는 승인된 기존 공통 writer·권한·revision/CAS 검증을 따라야 한다. Viewer는 우선 **읽기 전용**.
- 동일 PR/CL에서 다수 분석 사례가 생기거나 한 원인 규칙이 여러 Work에 걸칠 때 다대다 참조로 연결한다. 문서 복제를 기본 방식으로 사용하지 않는다.
- 식별/추적 요소 후보: Case ID, module/feature/procedure, Source PR·P4 CL, source repository/branch/revision, Work ID, Evidence/Artifact ID, 분석 시점, 원인 규칙, 탐색 범위, 적용 가능한 보호, 반례, Recovery 필요성·불확실성, Edge(의미 확정 후), AS-IS·TO-BE MSC 링크, 판정/승인/변경 이력.
- 파일명/메타데이터/스키마를 실제 기존 Kernel 계약 확인 전에는 **확정 요구로 승격하지 않는다**. 위 구조는 설명용이다.
- 고객 정보·비공개 코드·제한된 로그/MSC·비밀정보의 공개 GitHub 업로드 금지. 업무 L1 원본의 저장은 해당 승인된 환경·저장소에서만 수행한다.

## 5. Viewer 사용 흐름 및 범위

- Viewer 기존 좌측 탐색에 `Recovery` 영역을 추가한다. 모듈·상태·이슈/PR/CL·Work ID로 목록/필터 검색을 지원하되 실제 데이터 계약에 맞춘다.
- 사용자 경로: **Recovery 목록 → 사례 상세(원인 규칙, 후보, 기존 보호, Recovery 필요성·판정) → 연결 Work/Evidence → Seed 전·후/후보 AS-IS/TO-BE MSC(HTML/SVG)**.
- `Edge` 정보는 업무 GPT가 의미·스키마를 확정하고 결과를 제공할 때만 별도 섹션 또는 MSC 내 연결 정보로 표시한다. 정의되지 않은 Edge 지표나 그래프를 Viewer가 추측해 만들지 않는다.
- 모든 상세 항목에 source revision, 최종 검증 시점, 확인되지 않은 가설과 검증된 사실을 구분해 표시한다.
- 기존 Markdown 렌더링, HTML/SVG 안전 처리, 문서 링크/탐색, Work 검색, read adapter를 우선 재사용한다.
- 실제 접근 권한, 원본 경로, 링크 부재, 문서 삭제/이름 변경, 최신 revision 불일치 처리와 브라우저 표시를 시험한다.
- Viewer 수정·추가(write-back)는 **후속 별도 범위**: 인증/승인/Diff/CAS/원격 readback의 존재가 입증된 경우에만 구현한다.

## 6. 변경 범위·호환성 게이트

**우리가 직접 할 작업**

1. CoWork 최신 `CONTEXT_BRIEF`, 해당 `CURRENT`, 진행 결과/영수증을 읽어 기존 Work 재개. 관련 스킬 실제 설치본/후보 SHA와 연결 인터페이스 확인.
2. Recovery 저장 뷰를 `knowledge/` 계약·Kernel writer·기존 Work/Evidence와 대조. Reuse → Connect → 확인된 gap만 Extend.
3. Kernel/Workflow에 필요한 최소 Recovery read/write/projection 연결 개발. Recovery 스킬 구현 없이 **합성 사례로 계약** 시험.
4. Viewer에 Recovery 목록·상세·Work/MSC 링크를 연결하고 합성 데이터 및 가능한 업무 환경 읽기 시험으로 검증.
5. 변경된 소스·패키지의 실제 bytes/SHA, 회귀시험, 독립 리뷰 진행 여부, 공개/비공개 게시 경계를 분리 보고.
6. 업무 GPT용 Recovery 입력/출력·Edge·MSC 계약 **인계 문서** 작성. 실제 업무 GPT에 설치·수정·실행했다고 주장하지 않음.

**우리 쪽 변경 금지/별도 승인 항목**

- 업무 GPT 소유의 `l1-channel-recovery` 스킬 로직 직접 수정/설치(별도 업무 작업).
- 업무 원본 코드/CL/로그 또는 비공개 상세 MSC를 CoWork PRIVATE/PUBLIC로 무단 반출.
- 기존 운영 패키지 강제 교체, LIVE 전환, 유료 모델 호출, 설치/설정·키/토큰 생성, PUBLIC 배포(해당 유효 승인 확인 필요).
- 같은 버전명이지만 다른 ZIP을 확인 없이 덮어쓰기.

## 7. 확인·시험 기준

| 구분 | 완료 기준 | 현 시점 |
|---|---|---|
| G0 최신 설치·계약 확인 | 실제 Kernel/Workflow/Viewer/Recovery/Converter 버전, 원본 ZIP 해시, 호출/저장 인터페이스, CoWork CURRENT 확인 | **NOT_RUN(이 재구성에서)** |
| Recovery 원본 연결 | 1개 시드 + 2개 후보(합성 가능)로 Work/Evidence 참조·원본 SHA·revision·중복 방지·재조회 확인 | **NOT_RUN** |
| 단일 writer·호환성 | CAS/승인/원격 readback, 기존 Knowledge/Work 문서 회귀, Workflow v1.6.75 서로 다른 후보의 변경 무손실 보존 | **NOT_RUN** |
| Viewer | Recovery 목록/상세, Edge 미확정 처리, MSC HTML/SVG, Work 링크, 권한/404/구버전 처리 브라우저 확인 | **NOT_RUN** |
| 실제 업무 GPT Recovery | CL/PR 분석·보호·필요성 판정·Edge·MSC E2E, 업무 GPT 독립 검증 | **별도 업무 범위; NOT_RUN** |
| 독립 리뷰 | 개발 수행자와 독립된 요청·입력·실행·결과·영수증 | **NOT_RUN** |
| 게시·배포 | PRIVATE 게시+원격 바이트 확인, PUBLIC 비민감 산출물 승인 확인, 설치/운영 적용 별개 판정 | **NOT_POSTED / NOT_DEPLOYED** |

시험 판정은 PASS/FAIL/SKIP/NOT_RUN으로 기록하고 **설계 검토·문서 작성·합성 테스트를 실제 업무 환경 E2E PASS로 승격하지 않는다**.

## 8. 새 대화창 실행 지시

> 이 MD 인계서를 기준으로 기존 Work `L1-WORKSPACE-RAG-20261111-001`를 재개해줘. 먼저 GitHub PRIVATE `wonhwipark/CoWork-Skill-Collab/main`의 `collab/CONTEXT_BRIEF.md`, 관련 `CURRENT.md` 상단 및 최신 결과·영수증을 확인하고, 공개 `wonhwipark/L1Work/main`의 관련 11/19·11/20 Recovery 인계와 11/24 Viewer 통합 인계를 대조해줘. 원격 최신본이 본 문서보다 우선이야.  
> **개발 범위는 work-ledger-kernel·Viewer와 입증된 최소 Workflow 연동**이야. `l1-channel-recovery` 분석 로직/스킬 수정·Edge 의미 확정·MSC 생성은 업무 GPT 책임으로 구분해, 필요한 인터페이스를 인계 요구사항으로 작성해줘. 기존 `knowledge/`, Work/Evidence, doc-converter, Viewer 계약을 재사용하고 `l1-workspace/recovery/`의 단일 정본/탐색 구조를 검토·구현·시험해줘.  
> 두 Workflow v1.6.75 후보의 소스/ZIP 차이를 비교하고 실제 설치본/호환성을 확인한 뒤 필요한 변경만 새 버전으로 통합해줘. 기존 시험·게시·승인을 반복하거나 미확인 상태를 완료로 간주하지 말고, 가능한 개발·시험은 진행해줘. 관련 범위의 권한 부족·호스트 미접근은 BLOCKED/NOT_RUN으로 분리하고, 결과는 상태→변경→시험→미검증/필요 승인→산출물/SHA/정확한 원격 경로→다음 한 동작 순서로 보고해줘.

## 9. 지금 시점의 정확한 상태 선언

이 문서는 **이전 대화에서 합의된 설계 방향과 보고된 기존 조사 결과를 인계하기 위한 재구성 문서**다. 이 문서 작성 자체는 GitHub 게시, 새 코드 개발, 시험 실행 또는 업무 GPT Recovery 스킬 수정을 의미하지 않는다. 새로운 창에서는 반드시 원격 최신 `CURRENT`와 소스·실제 호스트의 결과를 확인해서 진행한다.