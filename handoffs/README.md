# 사내 GPT 인계 문서

## L1 Knowledge Updater × Workflow

| 상태 | 문서 | 범위 |
|---|---|---|
| **현재 인계 r0005** | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0005_1111.md) | G0 설치 사실 / G1 가정 분리, K5.8 설계표만, 기존 기능 우선 재사용 |
| 이전 r0004 | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0004_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0004_1111.md) | 이전 보완 계약, 과거 기록 보존 |
| 과거 r0002 | [L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0002_1111.md](L1_KNOWLEDGE_UPDATER_WORKFLOW_INHOUSE_HANDOFF_r0002_1111.md) | 이전 통합 인계, 과거 기록 보존 |

저장소 `wonhwipark/L1Work`, branch `main`. 현재 인계는 G0 READ_ONLY와 G1 설계표 작성이며 기존 knowledge/metadata·Work/Evidence·record/schema를 변경하지 않는다. SourceSnapshot·CAS·N:M·복구는 기존 Kernel/Updater/Git 제공자를 우선 재사용하고 미확인 API/record는 추가 확인 또는 BLOCKED로 남긴다.

사내 G0는 아직 NOT_RUN이므로 확인된 설치본 사실은 없다. 신규 엔진·schema 확장은 실제 gap이 확인된 최소 범위의 후속 설계 후보로만 검토한다. 구현·그룹 write·설치·모델 호출·외부 전송을 승인하지 않는다. 파일을 내려받아 사내 GPT에 첨부하고 마지막 원샷 요청을 사용한다.
