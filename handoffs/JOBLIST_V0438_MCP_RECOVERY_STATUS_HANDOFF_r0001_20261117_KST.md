# Job-list v0.4.38 / Linux MCP 복구 현황 인계

- 상태 정리: r0001 / 2026-11-17 KST
- 용도: **모바일 Agent·업무 LLM이 다음 요청에서 현재 장애 경계를 오해하지 않도록 하는 비민감 현황**.
- 기존 실행 프롬프트: [r0003 근본 원인 분석·최소 복구 요청](JOB_LIST_V0438_LINUX_MCP_ROOTCAUSE_RECOVERY_PROMPT_r0003_20261117_KST.md).
- **이 문서는 실행 요청/운영 승인/READY/Job 재실행 트리거가 아님.** 실제 운영 결과는 Linux 호스트에서 별도 확인.

## 현재 확인된 사항

| 구분 | 최신 관측·판정 |
|---|---|
| GitHub PAT / Skill-Updater | 사용자 측 인증 복구 후 업데이트 성공 보고. 모바일 Agent 측 `github_exec` 401과 **별개 인증 환경** |
| Job-list | 설치 `v0.4.38` 확인(모바일 MCP readback). 실제 ZIP bytes와 Runner 로드 연계 미검증 |
| 활성 프로필 | `nr-l1tx-init-rach-analysis-linux`, Job `JOB-20261115-NR-L1TX-INIT-RACH-EXEC-01`가 Catalog에서 active 보고 |
| 큐 기록 | `DONE/SUCCESS`, 시도 1회. 그러나 `run_id`, `worker_started_at`, `enqueued_at` 모두 null 보고 |
| 실행·산출물 | **UNKNOWN** — CODE_FACTS·MSC의 실제 존재·내용과 Worker 실행 완료 증거 미확보 |
| 결과 조회 | `RESULT_UNSUPPORTED`; 결과 allowlist에 대상 ID 미포함 보고. 근본 원인·대체 조회 경로 미확정 |
| 등록 목록 | Catalog 9 / Registry 6 / Bootstrap 5. 반드시 같아야 한다는 계약은 미확인 |
| MCP 실제 패치 | 모바일 Agent에서 변경/배포 증거 없음. **NOT_APPLIED** |
| 전체 복구 | **미완료**. 운영 회귀시험·독립 리뷰도 이번 요청에서 NOT_RUN |

## 왜 모바일 Agent 실행 요청으로는 복구되지 않았는가

- r0003 문서 자체는 정상 수신·읽기 완료.
- 모바일 Agent에 노출된 Linux MCP 도구는 **READ/PLAN만 확인**. `remote_enqueue`, `remote_retry`, `remote_cancel`, `apply_patch`가 `NOT_IMPLEMENTED`라고 보고.
- 모바일 Agent 컨테이너와 Linux 운영 호스트는 **별도 machine**. 운영 소스·결과 디렉터리의 직접 읽기/수정 권한이 없어 소스 패치, 재시작, Job 실행과 시험은 수행하지 못함.
- 이것은 **모바일 Agent 경계**가 확인된 것이며, Linux 호스트 내부의 기존 Job-list CLI/Runner 실행까지 불가능하다는 증명은 아님.

## 다음 한 동작

**Linux 운영 호스트에 접근 가능한 업무 LLM 세션에서 r0003을 직접 실행.** 먼저 기존 RACH Job의 출력 파일·영수증·Worker 시작 근거를 조회해 **① 실제 분석 결과 존재 여부, ② DONE/SUCCESS의 정확한 처리 단계**를 확정한다. 그 다음 확인된 결함만 최소 수정·시험한다.

- 이미 소비됐을 가능성이 있는 RACH Job을 **무조건 재실행·재큐잉 금지**.
- 별도 승인 범위를 확인하지 않은 운영 파일/DB/서비스 변경이나 추가 유료 호출 금지.
- Job-list로 **별도의 복구 요청을 전달하는 방안**은 설계 가능성은 있으나 현재 호스트 Runner 지원·중복 방지·결과 반환 계약이 확인되기 전 **실행 가능 PASS 판정 금지**.
- 원본 업무 코드, 상세 로그, 토큰 및 상세 MSC는 PUBLIC GitHub에 올리지 않음. 실제 증빙은 허용된 업무 로컬 경로에 보존.

## 연계

- 기존 복구 요청: [r0003](JOB_LIST_V0438_LINUX_MCP_ROOTCAUSE_RECOVERY_PROMPT_r0003_20261117_KST.md)
- CoWork PRIVATE 기존 Work: `collab/projects/JOBLIST-NRTX-20261112-001/CURRENT.md`
- 코드 분석 Work: `collab/projects/NR-L1TX-CODE-ANALYSIS-20261115-001/CURRENT.md`
