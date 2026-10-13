# 사내 LLM 실행 프롬프트 — Provider 최초 승인 및 smp1900 다중 브랜치 점검

아래 지시를 **사내 Linux에 연결된 LLM**에서 실행하라. 목표는 `l1-fix-workflow`의 Provider를 **최초 1회 승인·등록**하고, `smp1900`의 여러 브랜치를 안전하게 사용할 수 있는지 점검하는 것이다. 설명만 하지 말고 사용 가능한 도구로 실제 점검·처리하되, 도구 권한이 없으면 실행했다고 주장하지 말고 `BLOCKED`로 보고하라.

## 대상 및 불변 정책
- 코드 저장소: `/home/whpark/Project/smp1900` (한 저장소의 다중 브랜치). 다른 저장소는 **등록하지 말 것**.
- 기대 설치본: `l1-fix-workflow v1.6.19`, `skill-updater v0.5.42`. 실제 설치 경로/버전은 조회하여 확인할 것. 설치 경로를 추측해 생성하거나 임의 다운로드하지 말 것.
- Jira **신규 이슈 생성 및 Comment 작성은 금지**. 빌드/UT, 코드 수정, Git checkout/switch/reset/clean/pull/push, Worktree 생성, GitHub 쓰기도 금지.
- 기존 Manifest와 Provider 항목을 보존. 보안 검사 우회 및 임의 실행기 등록 금지. `--approve`는 아래 게이트 모두 충족 시에만 실행.

## 실행 단계
**A. 읽기 전용 사전 점검**
1. Workflow 진입점을 실제 설치 파일·도움말에서 확인. 다음 예시는 경로가 맞는 경우에만 사용:
   `cd ~/l1sw-private-skills/l1-fix-workflow`
2. 현재 설치 버전, `provider-onboard`/`provider-status` 지원 여부, Code Analyzer 실행기 위치·권한, Kernel/Updater 상태를 확인.
3. `git -C /home/whpark/Project/smp1900 rev-parse --show-toplevel`, `status --short`, `branch --show-current`, `branch --list`, `branch -r`를 읽기 전용으로 확인. 현재 브랜치, 로컬/원격 브랜치 개수를 기록. 브랜치 이동 금지.
4. Manifest 및 승인 정책 존재 여부를 확인하되, 토큰·계정·내부 주소·Manifest 전체 내용을 출력하지 말 것.

**B. 승인 미리보기**
실제 Workflow 명령 지원 확인 후 아래 명령을 실행하고 결과를 검증:
```bash
PYTHONPATH="$PWD" python3 -m l1_fix_workflow provider-onboard \
  --code-root /home/whpark/Project/smp1900
```
`PLAN_OK`에 해당하는 정상 미리보기, 신뢰 가능한 Code Analyzer 실행기, 허용된 코드 루트, 파일 쓰기 대상 및 기존 Provider 보존이 확인되는지 점검한다. 이 중 하나라도 불명확하면 **승인 실행 금지**.

**C. 최초 승인·등록 (조건부 실제 실행)**
A·B 성공, 설치본 v1.6.19 호환, 실행 권한이 사내 정책상 허용되는 경우에 한해:
```bash
PYTHONPATH="$PWD" python3 -m l1_fix_workflow provider-onboard \
  --code-root /home/whpark/Project/smp1900 --approve
PYTHONPATH="$PWD" python3 -m l1_fix_workflow provider-status
```
설정이 이미 유효하면 재쓰기 대신 현 상태만 확인. 신규/변경되는 `~/.l1-ledger/provider_bootstrap_policy.json`과 `~/.l1-ledger/provider_deployment_manifest.json`의 존재 및 상태만 보고. `READY`라도 **실제 분석 성공과 혼동하지 말 것**. 실패하면 원인 코드와 안전한 다음 조치를 기록하고 임의 우회하지 말 것.

**D. 다중 브랜치 지원 판정 (읽기 전용)**
Manifest 승인은 저장소 루트 기준인지, 분석 시 선택 가능한 브랜치가 **현재 checkout 브랜치에 한정되는지**, 또는 Git ref 지정/브랜치별 인덱싱을 구현했는지를 **실제 코드·CLI·문서 근거**로 판정. `git grep` 등이 현재 작업 트리만 검색하면 타 브랜치 분석 지원으로 판정하지 말 것. 브랜치마다 별도 승인/별도 Manifest가 필요한지도 판정. 필요한 기능이 없으면 구현하지 말고 개선 항목만 제시.

## 응답 형식 (모바일 복사 용이)
반드시 아래 **8개 항목을 숫자 1줄**로 먼저 출력하고 짧은 사유(최대 5줄)만 추가. 오류가 있으면 오류 코드 1줄 추가.

1. Workflow: 1=1.6.19 확인 / 2=다른 버전 / 3=조회 불가
2. Updater: 1=0.5.42 확인 / 2=다른 버전 / 3=조회 불가
3. 사전 점검: 1=PASS / 2=FAIL / 3=권한 없음
4. 미리보기: 1=PASS / 2=FAIL / 3=미지원
5. 최초 승인: 1=신규 성공 / 2=기존 설정 유효 / 3=차단 / 4=실패
6. Provider 상태: 1=READY / 2=PENDING / 3=BLOCKED / 4=조회 불가
7. 다중 브랜치: 1=명시적 브랜치 선택 검증 / 2=현재 브랜치만 확인 / 3=불명확
8. 브랜치별 승인: 1=불필요 확인 / 2=필요 확인 / 3=불명확

형식 예: `1 1 1 1 1 1 2 1` (예시는 실제 결과가 아님).
