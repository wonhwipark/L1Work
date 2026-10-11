# 사내 Linux MCP 기존 Wrapper 개선 프롬프트 v4 (간소화)

> 2026-10-12 KST | 사내 Linux LLM용 | 3,000자 이내

## 목표·허용 범위
기존 Linux MCP Wrapper를 재구축하지 말고 미연결/오동작 Action만 최소 수정하라. **P0은 FEATURE Work 갱신→개인 사내 GitHub `work_docs` 게시 복구**다. 다음은 Workflow Provider 연결과 Cleanup 조회다.

MCP Tool `run_skill_updater`, `run_l1_fix_workflow`, `run_l1_fla` 이름·계약을 보존하라. `l1_job`/새 4-Domain MCP 및 Windows MCP 신설 금지.

**승인:** Wrapper와 필요한 하위 스킬(`l1-fix-workflow`/Kernel/`l1-github`) 최소 호환 수정 및 격리 테스트. **금지:** 운영 설치·스케줄 변경·실 Job/삭제/분석·운영 GitHub Push·제품 빌드/UT 실행.

## STEP 1. 기존 호출 경로 조사 (무변경)
- MCP schema→라우터→Provider→receipt를 파일:라인으로 추적해 정상/누락/오동작/미확인을 구분하라.
- Work 선택→REQ/DEC 저장→Export→Push→readback 중 최초 실패 지점을 확인하라. 로그가 없으면 원인 미확정으로 보고하라.
- 실행 계정/설치본/`l1-github` helper/`work_docs` role·인증을 확인하라. 운영 데이터 수정·초기화 금지.

## STEP 2. P0: FEATURE 갱신 + docs-only 게시 복구
- “TX Sharing 요구사항 추가하고 GitHub에 올려줘”를 **기존 Work 선택→Kernel 영속 저장(revision/event_id)→최신 Export→`work_docs` scoped Push→원격 SHA·내용 확인**으로 연결하라. RoutePlan만으로 완료 처리 금지.
- Work ID→확정된 세션 Work→유일한 제목 일치 순으로 선택. 모호하면 `WORK_SELECTION_REQUIRED`; 임의 생성 금지.
- **docs-only**와 “다른 PC에서 이어서” **handoff**를 분리하라. 기존 `docs-push --work-id`의 handoff 의미는 호환 보존하고, 필요하면 명시적 docs-only Action/옵션을 추가하라. docs-only에서는 **제품 코드 Git dirty/HEAD**를 차단 사유로 삼지 말고, 문서 저장소의 충돌·권한·변경 범위는 검증하라. handoff 안전 검증은 완화 금지.
- MCP 프로세스 `cwd`를 Git 루트로 가정하지 마라. 설정된 `work_docs` repo root·브랜치를 resolve하여 명시적 cwd로 실행하라. 제품 코드는 단일 기본 저장소에서 브랜치 전환만 허용; 자동 worktree 생성 금지. 임의 repo fallback·강제 push 금지.
- `work_id+revision+digest+repo/branch`와 receipt로 중복 게시를 차단하라. Push 실패/응답 유실 시 저장 내용 보존, `SAVED_NOT_PUBLISHED`·`retry_from` 반환. 원격 검증 전 성공 금지.

## STEP 3. 비대화형 실행 및 MCP 안전성
MCP 경로의 `input/getpass/confirm/credential prompt`와 숨은 터미널 메뉴를 제거하거나 비대화형 adapter로 우회하라. 없는 CLI 옵션은 임의 전달하지 마라. stdin 차단·타임아웃·자식 프로세스 정리·출력 제한·Git terminal prompt 억제·secret 마스킹을 적용하라. 인증/설정/Work 선택이 부족하면 `AUTH_REQUIRED/REPO_CONFIG_REQUIRED/NEEDS_INPUT`과 필요한 다음 Action만 반환하라. 임의 shell 실행 API를 만들지 마라.

## STEP 4. 나머지 MCP 연결
- Workflow: 명시 실행에서만 `l1-log-analysis` Provider 호출, `run_id/work_id`·Evidence 연결. `plan/resume(context)`는 조회 전용, FLA 우회 금지. 빌드 기본 OFF, 미요청 UT/Push 금지.
- Cleanup: 기존 `l1-cleanup`의 디스크·정책·최근 결과를 읽기 전용 조회. 삭제 엔진·정책 수정 금지.
- Updater/Job-list/Bootstrap 내부 구현 변경 금지. MCP 직접 호출로 신규 예약 Job 활성화 금지; 기존 미완료 Job의 승인된 재개는 별개.

## STEP 5. 격리 검증 및 보고
fixture 검증: ① 3종 schema 호환 ② 비 Git cwd 게시 ③ 제품 코드 dirty에서 docs-only 허용/handoff 차단 ④ Work 모호성·revision 충돌 ⑤ 입력·인증 오류 종료 ⑥ scoped push/readback ⑦ 재시도 중복 방지 ⑧ plan≠실행 ⑨ 조회 부작용 0회. PASS/FAIL/SKIP 구분.

결과는 **(1) 원인/최초 실패 단계 (2) 변경 파일·함수·diff (3) Tool→Action→Provider 매핑 (4) 테스트 결과 (5) 운영 미검증 사항·적용/롤백 절차** 순으로 간결히 제공하라. 기존 정상 구현을 다시 작성하지 말고 가능한 범위에서 단계별 수정·격리 테스트까지 계속 진행하라.
