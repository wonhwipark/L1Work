# 업무 GPT 인계 — NR L1 Tx UL Tx Switching 저사양 분석·MSC 검증 G0

- r0001 / 2026-11-21 KST
- repo `wonhwipark/L1Work` branch `main` path `handoffs/L1_KNOWLEDGE_UPDATER_LOW_RESOURCE_LLM_MSC_G0_AND_INTEGRATION_HANDOFF_r0001_20261121_KST.md`
- **목적:** 실제 `l1-knowledge-updater`가 저사양 로컬 LLM·기존 `code-analyzer` 및 `doc-converter`에서 Module→Feature→Scenario와 코드 기반 MSC를 안전하게 생성·갱신할 수 있는지 **현재 설치 스킬의 실제 인터페이스를 먼저 확인**.
- 기초 연구/개발·QA 정본: PRIVATE `wonhwipark/CoWork-Skill-Collab/main` `collab/projects/L1-WORKSPACE-RAG-20261111-001/LOW_RESOURCE_LLM_RESEARCH_LICENSE_MSC_AND_CANDIDATE_QA_r0001_20261121_KST.md` (회사 코드·상세 MSC/로그는 반출 금지).
- 기존 실사용 요청 [NR L1 Tx UL Tx Switching 1건 실행](NR_L1TX_UL_TX_SWITCHING_KNOWLEDGE_AGENT_MCP_ONE_SHOT_HANDOFF_r0001_20261120_KST.md)과 같은 목적의 Work를 재개.

## 근거 기반 확정 사항

- 논문/상용 사례의 **계층 탐색, 좁은 call-graph, 근거 pin, 제한 문맥**만 차용; 외부 소스/모델 복사 0. Agentless=MIT, LocAgent·RepoAgent·RepoGraph·Aider=Apache-2.0, GraphRAG/tree-sitter=MIT. RepoAgent 직접 C++ 분석 지원을 가정 금지.
- CodeQL CLI는 비공개 코드 분석에 별도 상용 라이선스 이슈이므로 **설치·실행·번들 금지**, data/control-flow 개념만 참고.
- 개발 보조 ZIP `knowledge_analysis_preflight_v0_1_0_1121.zip`은 GPT 로컬 합성 시험 12 PASS, 15,379 B, SHA-256 `e307358cb9b6b9bfe0a8c3a1306ceca743ec09549e5ef53de5a879cc4e9ba865`. **기존 스킬 변경 패키지가 아니며 GitHub PUBLIC 배송/업무 Linux 설치 아님.** 사용자 제공 대화 산출물로 보유. 이를 마치 `skill-updater` 설치본이라고 보고/호출하지 않음.
- 자체 JSON schema는 Converter native Scenario IR 아님; 시험의 anchor 일치가 진짜 실행 순서/분기·IPC 메시지 검증이 아님. `MAY_INVOKE_CONVERTER=false`, `MAY_PUBLISH_KNOWLEDGE=false` 유지.

## 업무 GPT / Linux Agent G0 READ_ONLY 요청

1. 기존 `code-analyzer` 실제 설치 버전·action·CODE FACT 형식/근거 pin·MSC 출처, `l1-knowledge-updater` 설치 스킬 원본/Updater 직접 진입·개인 Workspace writer의 책임과 권한을 각각 **읽기 전용** 확인. PUBLIC의 `l1-knowledge-manager` 구버전으로 대체 금지.
2. `doc-converter`의 실제 canonical scenario IR, SOURCE_PARENT_DIR_V1, `stack_group`, participant aliases, 입력 `view_mode`, SVG→B형 HTML 성공 조건 및 manifest·readback을 설치 원본/기존 시험 결과로 확인. 메시지·분기 순서·예외 경로의 코드 증빙 1건과 기존 B형 MSC 1건을 내부에서 대조.
3. 설치 스킬이 이미 제공하는 계층 탐색·근거 검증·문맥 제한·문서 갱신을 `REUSE`, 실행 옵션/문서 전달 누락은 `CONNECT`, **명백한 빈 기능만** 최소 `EXTEND`. 가상 CLI, 외부 모델 패키지, 신규 스키마/DB/상용 도구를 기본 요구하지 말 것.
4. 동일 NR L1 Tx UL Tx Switching source revision 고정, 기존 지식 및 2~3 Scenario 대비 탐색 오탐/누락·실제 call-path 근거·문맥/토큰·지연/메모리·MSC participant/phase 재현성을 측정. 결과 원문·회사 코드·상세 MSC를 PUBLIC/PRIVATE로 반출하지 말고 허용된 업무 Workspace에 보존. 외부 공유는 민감정보 제거 요약과 run ID/검증 여부만.
5. 실제 스킬 수정/패키징은 **유효 승인과 필요한 독립 리뷰·배포 게이트 후** 진행. 이번 인계·GPT 로컬 helper 테스트로 호스트 스킬 수정·설치·그룹 Knowledge 게시가 승인되었다고 해석 금지.

## 필수 회신 형식

| 항목 | 판정 |
|---|---|
| Updater/Analyzer/Converter 실제 설치 원본 + source pin | PASS/NOT_RUN/BLOCKED |
| Module/Feature/Scenario 근거 검증 | PASS/FAIL/NOT_RUN + 대표 id |
| 저사양 LLM 토큰·메모리/시간 | 실측/NOT_RUN |
| Converter native scenario IR / B형 MSC | PASS/FAIL/NOT_RUN |
| 기존 코드 재사용/연결/최소 확장 | REUSE/CONNECT/EXTEND/UNKNOWN |
| 패키징·승인·독립 리뷰/업무 설치 | 각각 실측 상태 |
| NEXT_ONE_ACTION | 하나만 |

문서·합성 시험만으로 `l1-knowledge-updater` 정상 동작, 기존 Converter MSC 제작 성공, 신규 배포 가능을 PASS로 판정하지 않는다.
