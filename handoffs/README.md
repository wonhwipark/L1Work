# 업무용 GPT 인계 문서

## 관리 스킬 기능 요약 (공개용 · 업무용 GPT 인계)

| 문서 | 용도 | 검증 범위 |
|---|---|---|
| [L1_SKILL_CAPABILITY_SUMMARY_INHOUSE_HANDOFF_r0001_20261113.md](L1_SKILL_CAPABILITY_SUMMARY_INHOUSE_HANDOFF_r0001_20261113.md) | 관리 스킬 **18개 + 별도 업무용 연동 1개**의 역할·재사용 판단·현재 코드 MSC 활용 요약 | 기존 정적 카탈로그를 비민감 범위에서 요약. 작업 PC 설치·실호출·독립 리뷰 미검증 |

상세 기능 카탈로그와 검증 결과의 정본은 접근 권한이 필요한 CoWork PRIVATE에 있으며, 이 공개 인계에는 회사 코드·운영자료·인증정보를 포함하지 않는다. 스킬 설치·Job 실행·공개 배포를 승인하는 문서가 아니다.

## L1 Knowledge Updater × Workflow

| 상태 | 문서 | 범위 |
|---|---|---|
| **현재 인계 r0005** | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md) | G0 설치 사실 / G1 가정 분리, K5.8 설계표만, 기존 기능 우선 재사용 |
| 이전 r0004 | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0004_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0004_1111.md) | 이전 보완 계약, 과거 기록 보존 |
| 과거 r0002 | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0002_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0002_1111.md) | 이전 통합 인계, 과거 기록 보존 |

저장소 `wonhwipark/L1Work`, branch `main`. 현재 인계는 G0 READ_ONLY와 G1 설계표 작성이며 기존 knowledge/metadata·Work/Evidence·record/schema를 변경하지 않는다. SourceSnapshot·CAS·N:M·복구는 기존 Kernel/Updater/Git 제공자를 우선 재사용하고 미확인 API/record는 추가 확인 또는 BLOCKED로 남긴다.

작업 PC G0는 아직 NOT_RUN이므로 확인된 설치본 사실은 없다. 신규 엔진·schema 확장은 실제 gap이 확인된 최소 범위의 후속 설계 후보로만 검토한다. 구현·그룹 write·설치·모델 호출·외부 전송을 승인하지 않는다. 파일을 내려받아 업무용 GPT에 첨부하고 마지막 원샷 요청을 사용한다.

## 용어·접근 지침

신규 안내에서는 저장소·작업 PC·실행 호스트·접근 권한으로 대상을 지칭한다. 기존 파일명(예: `_INHOUSE_` 포함)은 링크 호환성을 위해 유지한다. 이 인계 목록은 공개 허용 설명만 포함하며 PRIVATE 기록, 회사 코드, 제한 정보의 공개를 승인하지 않는다.
