# L1 Knowledge Updater · 업무 GPT 실행 인계 r0005

2026-11-28 KST · 기존 Work `L1-WORKSPACE-RAG-20261111-001` · **설계 입력 수락 / 실행 지침 보완 반영 / 업무 적용 G0 대기**

**첫 행동은 G0-1 한 건입니다.** 업무 GPT가 단계 하나와 증거 묶음 하나를 선택해 Qwen3.6-27B에 전달하세요. Source Map은 기존 Discovery와 Analyzer로 원본 탐색 범위를 좁히고, 기술 설명·정상 Procedure·MSC는 기존 Knowledge에서 관리합니다. Map은 기존 Personal Store Writer로 `l1-workspace/source-map/`에 저장합니다. 세부 스키마·저장 표준·반례는 [실행 참조서](./L1_KNOWLEDGE_UPDATER_QWEN36_EXECUTION_REFERENCE_r0005_20261128_KST.md)에 모았습니다.

**판정 근거**는 사용자 검토 의견 11건, r0004의 공개 패키지 재현, 이번 문서의 자체 점검이에요. 사용자 제안 중 manifest의 단일 활성화와 순 payload 예산은 각각 동시 작성 경합과 기존 총 토큰 한도를 고려해 보완 수용했어요. r0004의 CoWork 요청은 별도 이력으로 보존해요. [기존 요청](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/d9ca3667079abb8bbdc87406ae05686834d598a5/collab/requests/REQ-L1-KNOWLEDGE-UPDATER-R0004-R1-20261128/REQUEST.md)

### 첫 페이지 · 어떤 문서를 적용할지

| 선행 문서 | 효력 | 적용 범위 |
|---|---|---|
| **본 인계 r0005 / 같은 revision의 실행 참조서** | 유효 · 1순위 | 본문은 실행 순서·판정, 참조서는 해당 단계의 데이터·시험 계약. 서로 충돌하면 그 단계 HOLD 후 업무 GPT가 정정 |
| 현황 MCP 인계 r0001(11/28) | 부분 유효 | 보고된 관측·이력 보존. 후속 Work 지시와 미확정 대안은 r0005로 대체 |
| [통합 인계 r0004 · 고정 리뷰 입력](https://github.com/wonhwipark/CoWork-Skill-Collab/blob/d9ca3667079abb8bbdc87406ae05686834d598a5/collab/packages/l1_knowledge_updater_r0004_1128_REVIEW_INPUT.zip) | 부분 유효 | G-2 재현·공개 패키지 시험 근거 유효. 저장 기본안·G0·예산·중단 기준은 r0005 적용 |
| [Updater r0003](./L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0003_20261127_KST.md) / [r0002](./L1_KNOWLEDGE_UPDATER_QWEN36_ANALYSIS_QUALITY_IMPLEMENTATION_HANDOFF_r0002_20261125_KST.md) | 부분 유효 | T01~T18·U19~U23, 근거·권한·그룹 승인·역링크. 유형별 권장 섹션은 실제 UD 템플릿에 매핑 |
| [1,500파일 Source Map r0003](./L1_SOURCE_MAP_1500_UPDATER_INTEGRATED_HANDOFF_r0003_20261127_KST.md) | 부분 유효 | 관계 방향·원문 예시·증분 반례. snapshot·조회 응답·실행 예산·파일럿 판정은 이번 참조서 적용 |
| [공통 연동 r0001](./L1_RECOVERY_SOURCE_MAP_VIEWER_INTEGRATED_IMPLEMENTATION_HANDOFF_r0001_20261127_KST.md) / [Recovery r0008](./L1_RECOVERY_POINT_ANALYSIS_INTEGRATED_IMPLEMENTATION_HANDOFF_r0008_20261127_KST.md) | 담당 영역 유효 | 공통 읽기, Recovery V2/V3/V4와 자체 실험. 기존 Work·영수증 재사용 |
| [Viewer v0.5.6](./L1_WORKSPACE_VIEWER_V056_TECHNICAL_KNOWLEDGE_READABILITY_COMPLETE_HANDOFF_r0001_20261126_KST.md) / [v0.5.7](./L1_WORKSPACE_VIEWER_V057_KNOWLEDGE_SECTION_ORDER_COMPLETE_HANDOFF_r0001_20261126_KST.md) / [Viewer·Analyzer 개발 전달](./L1_SOURCE_MAP_VIEWER_ANALYZER_DEVELOPMENT_DELIVERY_r0001_20261127_KST.md) | 담당 영역 유효 | 표시 역할·순서 및 공개 패키지의 출처. 운영 활성 상태는 G0에서 실측 |
| [그룹 R1 r0002](./L1_KNOWLEDGE_UPDATER_R1_G0_DETAILED_HANDOFF_r0002_20261117_KST.md) / [Workflow r0005](./L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md) | 권한·동기화 유효 | 그룹 Preview·승인·충돌·readback과 Workflow 읽기 전용 |
| [Job List·Agent MCP 실행/결과 인계 r0001](./L1_JOBLIST_KNOWLEDGE_UPDATER_RECOVERY_MCP_EXECUTION_RESULT_HANDOFF_r0001_20261128_KST.md) | 운영 연동에 유효 | 기존 Job의 실행 영수증·결과 조회에 적용. 이 문서의 G0와 연결하며 분석 계약·파일럿 기준은 r0005 적용 |
| [초기 Map G0](./L1_SOURCE_MAP_LLM_FIRST_G0_HANDOFF_r0001_20261127_KST.md) / [초기 범위 인계](./L1_SOURCE_MAP_KNOWLEDGE_UPDATER_VIEWER_SCOPE_HANDOFF_r0001_20261127_KST.md) | 실행 지시 대체 | 설계 이력으로 보존. 새 작업 진입점은 이 문서 하나 |

### 업무 GPT → Qwen · 단계별 독립 프롬프트

매 행의 인용문이 독립 실행 프롬프트예요. `<묶음>`은 업무 GPT가 같은 pin·같은 목적의 증거만 모아 지정하는 입력이에요. 한 번에 한 행만 전달하세요. 질문이 둘이면 첫 번째 질문만 선택하고 나머지는 대기열에 남겨 주세요.

| 단계 · 실행 질문 | 입력 1묶음 | 출력 | 종료·재개 조건 |
|---|---|---|---|
| G0-1 “<묶음>에서 이번 시험에 실제 호출되는 실행본의 SHA-256을 확정해 줘.” | 실행 경로·영수증·코드 지문 | actor/entrypoint/hash 대조표 | 필수 지문 미확인 시 **A~E 전부 HOLD**. G0 진단만 재개 |
| G0-2 “<묶음>에서 개인 Writer와 Reader가 같은 승인 root와 snapshot을 가리키는지 확인해 줘.” | 한 검증 대상의 개인 저장·조회 기록 | root/ACL/조회 결과 | 미설정·권한 불명·불일치 시 G0 HOLD |
| G0-3 “<묶음>에서 legacy 121개와 분류 합계 120개의 차이를 파일 단위로 설명해 줘.” | 동일 revision manifest와 분류 목록 | 차집합·제외 이유·고정 분모 해시 | 1건 미정산 또는 분모 미고정이면 G0 HOLD |
| G0-4 “<묶음>에서 이 하네스의 실제 순 payload 예산을 구해 줘.” | OpenCode 모델·tokenizer·usage 계측 | 공통 순 예산·측정 방식 | 오버헤드 실측 실패 시 모델 비교 HOLD. G0-1~3 통과 후 승인된 비모델 시험은 분리 가능 |
| A “<묶음>의 정확한 대상에서 지정 방향 1-hop 근거를 반환해 줘.” | 한 질문·한 source/build/snapshot·대상 | **Map Lookup Envelope v1** 1개 | 참조서의 크기·누락·권한 검사 후 종료. 다음 probe는 별도 질문 |
| B “<묶음>의 후보를 기존 Writer로 공개했을 때 한 세대만 보이는지 검증해 줘.” | 격리된 후보와 이전 manifest | 승자/충돌/readback 영수증 | 저장 승인·원자적 create-only 미입증 시 B만 HOLD |
| C “<묶음>에서 대상 Procedure가 추출되거나 제외된 이유를 판정해 줘.” | 한 실패 사례의 facts·bundle·선택 근거 | 대상 ID·단계·근거 또는 명시적 GAP | 활성 소유자·계약 미확인 시 기한 후 동결. 다른 사례와 합산 금지 |
| D1 “<묶음>에서 이 문서의 지정 주장 하나를 원문 근거로 검증해 줘.” | 기존 Knowledge 한 주장과 anchor | 수용/수정/미확인 및 해당 섹션 diff | UD와 기술 판정 개별 기록. 유효한 기존 문서·MSC는 재사용 |
| D2 “<묶음>에서 같은 holdout의 D3−D2로 Map 확대 여부를 판정해 줘.” | 고정 평가표·예산/사용량·4조건 결과 | 확대/중단/측정 보류 | 참조서의 사전 기준을 적용. 기준선·정답을 사후 변경하지 않음 |
| E “<묶음>에서 한 소비자의 읽기/표시가 고정 원본과 일치하는지 확인해 줘.” | 소비자 1개·snapshot·문서·ACL | PASS/FAIL 및 해당 경로 | 실패한 소비자만 재개. 그룹 게시·실제 운영 변경은 기존 별도 승인 |

### 구현 경계와 인계 판정

- **Updater가 맡을 일**은 생성/증분 요청, 기존 K2/K4의 선택적 조회, 근거·서술 검증이에요. **Writer가 맡을 일**은 기존 개인 저장 경로에 Map 유형을 허용하고, 승인된 불변 조각과 세대별 manifest의 조건부 생성을 제공하는 것이에요. 기본안을 충족할 수 없으면 분석 후보를 보존하고 활성화만 보류하세요.
- **G-2**는 공개 Analyzer v0.15.7 생산자와 exporter 사이에서 재현했어요. 활성 업무본 확인 후 Analyzer 담당자가 호환 처리를 맡아요. **Viewer·Recovery·Kernel·Workflow·Converter**의 소유 범위와 회귀는 참조서 §6에 있어요.
- **측정 경계**를 유지하세요. 업무 보고의 485건과 별도 32·59건을 각각 기록하고, UD 통과와 기술 coverage를 따로 판정해요. 11/09 HEAD와 dirty 7,515건 제외는 해당 Discovery의 기준선이에요. G5의 지식 쓰기 승인과 개인 Map 쓰기 승인은 별개예요.
- **업무 GPT 회신**은 단계 / 소유자 / pin·hash / 입력 증거 / 출력 / 시험 분모·결과 / 승인 범위 / 재개점 한 행이면 충분해요. 업무 코드·절대 경로·상세 MSC·원본 로그는 업무 Work에 보존하세요.
