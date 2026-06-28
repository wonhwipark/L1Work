# L1Work

## 목적
`L1Work/`는 기존 `L1a` 작업공간을 유지하면서 5.x 자동화 트랙을 상세화하기 위한 별도 작업공간입니다. 기존 `prompt/`, `CodeAnalyzer_standalone/`, `RCA_standalone/`, `rca_kg/` 자산은 읽기 전용 원천으로만 참조합니다.

## 운영 원칙
- 신규 파일은 `L1Work/` 하위에만 생성합니다.
- 기존 원천 자산은 이동/삭제/수정하지 않습니다.
- 각 트랙은 `draft -> staging -> current -> archive` 흐름으로 관리합니다.
- 5.2와 5.5는 기존 standalone/KG 자산이 있어 `staging-source-ready`로 시작합니다.
- 나머지 트랙은 `draft` 상태에서 요구사항 상세화를 시작합니다.

## 폴더 구조
```text
L1Work/
├── README.md
├── WORKBOARD.md
├── TRACK_REGISTRY.md
├── RELEASE_BOARD.md
├── common/
│   ├── README.md
│   ├── workflow.md
│   ├── templates/
│   └── policies/
├── 5.0_common_framework/
├── 5.1_jira_feedback_loop/
├── 5.2_code_analyzer/
├── 5.3_confluence_collection/
├── 5.4_hld_code_consistency/
├── 5.5_rca_kg/
└── 5.6_onboarding_knowledge_pack/
```

## 시작 방법
1. `WORKBOARD.md`에서 전체 트랙 상태를 확인합니다.
2. 대상 트랙의 `README.md`와 `source_refs.md`를 확인합니다.
3. `TRACK_STATUS.md`에서 현재 단계, 진행 항목, 차단 항목을 확인합니다.
4. 새 세션은 `HANDOFF.md`를 먼저 읽고 이어서 작업합니다.
5. release 후보는 `release/staging/`에 모으고 검증 후 `release/current/`로 승격합니다.
