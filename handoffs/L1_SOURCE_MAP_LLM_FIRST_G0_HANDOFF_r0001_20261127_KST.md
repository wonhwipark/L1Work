# 업무 GPT 인계 — Source Map 공통 활용 G0
2026-11-27 KST / 기존 L1 Source Map Discovery Work 재사용. 설계 r0002: https://github.com/wonhwipark/CoWork-Skill-Collab/blob/3ee216ff501172a164958e91106053c1ed6cd1f9/collab/projects/L1-WORKSPACE-RAG-20261111-001/L1_SOURCE_MAP_LLM_FIRST_INTEGRATED_DESIGN_r0002_20261127_KST.md
사용자 결정: 추가 독립 리뷰 생략. 이번 인계는 읽기 전용 G0, 기존 결과 확인용이며 승인/저장/설치/Job/그룹 게시 요청이 아님.

## 목적
Knowledge Updater가 생성한 기존 NR/LTE Source Map을 영속 관리하고 Code Analyzer·Channel Recovery·Updater가 필요한 관계만 조회하도록 연결. 개인 업무 l1-workspace의 source-map/을 knowledge/와 동등한 독립 영역으로 제안, Viewer도 독립 메뉴. 그룹 l1sw-dev-knowledge에는 별도 승인 후 연계. 기존 엔진 재사용, 입증된 결손만 수정.

## 확인 요청
| ID | 확인 사항 |
|---|---|
| G01 | 기존 7개 Discovery 결과/manifest 존재·hash·revision/build·coverage, 구조화 entity/relation/evidence 및 gaps 지원 여부. 기존 결과 재실행 금지 |
| G02 | Updater/Analyzer 활성 version/action별 추출 방식(파서/도구/LLM/수동) 및 실제 원문 검증 상태 구분. 오버로드·동명·조건부 빌드·메시지 등록·간접 호출 한계 |
| G03 | G6 승인 범위(개인/그룹/둘 다), 기존 Personal Store Writer의 독립 경로 ACL/CAS/readback, Kernel export 보존과 충돌 보호 |
| G04 | 기존 조회 기능 및 MCP/Viewer adapter에서 Map 검색·상세·상대 참조·권한 지원, Analyzer/Recovery 읽기 소비 가능 여부 |
| G05 | 모델 실제 ID/context/출력/토큰 계측·파일 읽기 상한, 동일 예산 D0(현행)/D1(Map)/D2(Procedure)/D3(둘 다) 비교 가능 여부 |
| G06 | 기존 그룹 저장 형식·동일 snapshot의 구조화 데이터/MD 파생·기존 결과와 충돌 대조·별도 Preview/승인/게시 readback 지원 |

## 설계 조건
- Updater만 Source Map 생성/갱신/저장·그룹 게시 요청; Analyzer는 제한 코드 사실 공급 및 읽기 소비, Recovery는 읽기 소비, Viewer는 표시.
- EXTRACTED/INFERRED/UNKNOWN과 provenance·원문 검증 상태·revision/build를 분리. 미검증 정보 확정 금지. Map 누락이 코드 부재를 뜻하지 않음.
- 초기 조회 예산 제안: 4096 tokens/50 records, 코드 20 files/step·60 files/task, 총 32768 tokens/20분/task. 실제 제한에 맞춰 시험 전 합의·고정.
- 골드 관계 30개 이상/반례 10개 이상, recall 90% 이상·근거 없는 CONFIRMED 0·stale 검출 100%는 제안 수락 기준. 이번에는 실제 비교 실행하지 않음.

## 회신
각 G01~G06별 PASS/FAIL/UNKNOWN, 실제 지원 action/권한 존재 여부, REUSE/CONNECT/PROVEN_GAP, 영향, 다음 조치만 업무 Work에 기록. 공개 가능한 비민감 상태만 허용 범위에서 회신. 실제 제품 코드/심볼·경로·로그·지도·인증정보 외부 반출 금지.
G0 완료 후 설계 GPT가 실제 필요한 관리 스킬/Viewer 변경을 확정. 기존 Source Map 승인 대기는 유지하며 사용자 명시 승인 없이 해소하지 않음.
