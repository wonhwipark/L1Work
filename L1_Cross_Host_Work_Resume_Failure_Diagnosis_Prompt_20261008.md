# L1 Cross-Host Work Resume 실패 진단 프롬프트

- 작성일: 2026-10-08 (KST)
- 기준: work-ledger-kernel v0.7.8 / l1-fix-workflow v1.6.1 / l1-github v0.3.38
- 목적: Windows Work → GitHub → Linux 복원 과정의 First Failed Stage 특정
- 원칙: 수정 금지. 실제 코드·로그·Git 상태 확인 후 숫자로만 판정.

## 답변 규칙
각 문항은 `Q1 = 1`, 증거는 `E1 = ...` 형식. 판정 불가는 0. 추측 금지.

## Q1. 최초 실패 단계
1 Windows→GitHub push
2 Linux Work 발견
3 Ledger CLI 요청 생성
4 CLI process 실행
5 l1-github clone/fetch/download
6 branch/HEAD checkout·검증
7 Linux workspace binding/rebind
8 Ledger Work state 복원
9 l1-fix-workflow resume/provider
10 위 단계 이후
0 판정 불가

## Q2. GitHub의 Work 정보
1 모두 존재
2 Work 정보 없음
3 일부 metadata 누락
4 commit만 있고 push 안 됨
5 잘못된 repo/branch
6 remote가 오래된 상태
0 확인 불가

## Q3. 복원용 metadata
1 충분
2 work_id/name 부족
3 repository 정보 부족
4 branch/HEAD 부족
5 binding/resume 정보 부족
6 복수 부족
0 확인 불가

## Q4. Linux Work resolve
1 정확한 Work
2 찾지 못함
3 다른 Work
4 복수 후보에서 중단
5 remote에는 있으나 local ledger가 못 찾음
0 확인 불가

## Q5. Work discovery source
1 local ledger
2 GitHub remote
3 local→GitHub fallback
4 GitHub→local fallback
5 병합
6 기타
0 확인 불가

## Q6. Ledger CLI 요청
1 정상
2 요청 미생성
3 executable/path 오류
4 argument 누락
5 Windows path 잔존
6 work/repo/branch argument 오류
7 실행기로 전달 안 됨
0 확인 불가

## Q7. 실제 CLI command
1 정상
2 executable 없음
3 script/module 없음
4 argument contract 불일치
5 Windows 전용 path/형식
6 permission
7 runtime/Python 문제
0 확인 불가
E7에는 token 제거한 실제 command 기록.

## Q8. CLI 실행
1 exit 0
2 non-zero
3 spawn 실패
4 timeout
5 dependency/import 실패
6 인증 실패
7 network/MCP/GitHub 접근 실패
0 확인 불가

## Q9. CLI result parsing
1 정상
2 CLI 성공을 실패로 해석
3 JSON/result contract 불일치
4 stdout/stderr 혼합
5 result field 누락
6 exit-code 처리 오류
0 확인 불가

## Q10. Linux repository 준비
1 정상
2 clone 실패
3 fetch 실패
4 잘못된 repo
5 directory 충돌
6 remote 설정 오류
7 인증 문제
0 확인 불가

## Q11. branch/HEAD
1 정상
2 remote branch 없음
3 local branch 생성 실패
4 다른 branch
5 detached HEAD
6 branch는 맞지만 HEAD mismatch
0 확인 불가

## Q12. v0.7.8 drift guard가 차단하는가
1 guard 통과
2 BRANCH mismatch
3 HEAD mismatch
4 repository identity mismatch
5 snapshot/expected state 부족
6 rebind보다 guard가 먼저 실행
7 guard 미실행
0 확인 불가

## Q13. Windows binding이 Linux에서 그대로 비교되는가
1 Linux state로 정상 re-establish
2 Windows repo path 재사용
3 Windows branch state 재사용
4 Windows HEAD state 재사용
5 Windows workspace identity 재사용
6 복수 항목 재사용
0 확인 불가

## Q14. Linux binding/rebind
1 정상 생성/갱신
2 생성 안 됨
3 Windows binding 그대로 사용
4 path만 변경, Git identity 미갱신
5 branch 미갱신
6 HEAD 미갱신
7 저장 후 readback 실패
0 확인 불가

## Q15. 현재 실행 순서
정상 기대:
remote Work 확인 → Linux repo 준비 → repo/branch/HEAD 검증 → Linux rebind/establish → verified state 저장 → resume → source-write guard

1 정상
2 guard가 rebind보다 먼저
3 binding이 checkout보다 먼저
4 Windows binding 검증 후 Linux rebind
5 Git 검증 없이 resume
6 복수 순서 오류
0 확인 불가

## Q16. Ledger Work state 복원
1 정상
2 Work record 실패
3 event/history 실패
4 binding 실패
5 schema/version 호환 실패
6 Windows absolute path 문제
7 중복 Work 충돌
0 확인 불가

## Q17. Windows absolute path runtime 사용
1 없음
2 workspace path
3 repository path
4 artifact/output path
5 CLI/script path
6 복수
0 확인 불가

## Q18. l1-fix-workflow resume
1 정상
2 Work resolve 실패
3 provider resolve 실패
4 binding 불일치
5 lease/state 문제
6 source-write guard 차단
7 resume context 실패
0 확인 불가

## Q19. 주 책임 컴포넌트
1 work-ledger-kernel
2 l1-github
3 l1-fix-workflow
4 kernel+l1-github interface
5 kernel+workflow interface
6 github+workflow interface
7 3개 contract
8 GitHub/인증/환경
9 사용자 local Git 상태
0 확인 불가

## Q20. 결함 성격
1 CLI command 생성
2 CLI execution
3 CLI result contract/parsing
4 Cross-host path portability
5 clone/fetch/checkout
6 binding/rebind lifecycle
7 drift guard ordering
8 Work state restore
9 workflow resume routing
10 외부 환경/인증
0 확인 불가

## Q21. 최소 수정 대상
1 kernel만
2 l1-github만
3 workflow만
4 kernel+l1-github
5 kernel+workflow
6 github+workflow
7 3개 모두
8 코드 수정 불필요
0 증거 부족, 수정 금지

## Q22. 바로 수정 가능한가
1 YES, root cause 증거 확보
2 NO, 추가 로그 필요
3 NO, CLI command/result 필요
4 NO, Git 상태 필요
5 NO, binding/ledger state 필요
6 NO, 재현 필요
0 판정 불가

## Q23. 다음 최소 증거
1 Ledger 로그
2 실제 CLI command
3 CLI stdout/stderr + exit code
4 Linux git status/branch/HEAD/remote
5 Work binding
6 Work ledger/event
7 GitHub Work metadata
8 Windows push 직전 Work/binding
9 전체 재현 trace
0 추가 정보 불필요

# 최종 출력 형식
[Cross-host Resume Diagnosis]

Q1=<n> Q2=<n> Q3=<n> Q4=<n> Q5=<n>
Q6=<n> Q7=<n> Q8=<n> Q9=<n> Q10=<n>
Q11=<n> Q12=<n> Q13=<n> Q14=<n> Q15=<n>
Q16=<n> Q17=<n> Q18=<n> Q19=<n> Q20=<n>
Q21=<n> Q22=<n> Q23=<n>

FIRST_FAILED_STAGE = ...
ROOT_CAUSE = ...
OWNER = ...
MINIMUM_FIX = ...
NEXT_EVIDENCE = ...

E1=...
E6=...
E7=...
E8=...
E12=...
E14=...
E19=...
E20=...

# 금지
1 진단 전 코드 수정
2 Windows binding을 Linux에서 무조건 유효 취급
3 OS path 차이를 단순 Git drift 판정
4 자동 checkout/reset/stash/rebase/merge
5 mismatch 무시 후 source-write
6 CLI 실행 실패와 parsing 실패 혼동
7 remote 문제와 local binding 문제 혼동
8 로그 없이 root cause 확정
9 기존 P2 ambiguity 기능 불필요 수정
10 l1-dev-knowledge 또는 폐기된 l1sw-dev-feature 포함

핵심 목표는 Windows push → Linux discovery → Ledger CLI → CLI 실행 → GitHub restore → checkout → Linux rebind → Work restore → workflow resume 중 처음 깨지는 한 지점을 실제 증거로 특정하는 것이다.
