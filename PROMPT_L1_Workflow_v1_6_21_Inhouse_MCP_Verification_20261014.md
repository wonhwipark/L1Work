# 사내 LLM 검증 프롬프트 — l1-fix-workflow v1.6.21

기준: 2026-10-14 KST / 대상: **사내 Linux MCP 호스트**

## 사용 순서
1. 아래 **[프롬프트 A]**를 사내 LLM에 입력하고 숫자 결과를 받는다.
2. 버전·설정이 정상이라면 실제 P4 Client/경로 등록 여부를 확인한다. **미등록이면 임의 등록하지 않는다.**
3. 실제 분석 성공까지 검증하려면 별도 승인 후 **[프롬프트 B]**를 실행한다. A만으로 E2E 성공이라고 판단하지 않는다.

## 프롬프트 A — 설치/설정 진단 (복사해서 실행)

```text
사내 Linux에서 l1-fix-workflow v1.6.21 배포 상태를 진단해줘.
대상은 실제 MCP Wrapper가 참조하는 설치본이다. ZIP/캐시/다른 경로에 있는 파일 버전을 설치 버전으로 간주하지 마.

[금지] 모든 설정 변경, skill-updater 강제 실행, Provider 자동 설치, 코드 루트 등록·승인·활성화, Jira 생성/Comment, 빌드/UT, Git checkout/pull/push/worktree, P4 sync/edit/submit/revert, Docs publish. 조회 명령만 수행. 신규 Work/Evidence도 생성하지 마.

1. 기존 MCP run_l1_fix_workflow 연결과 실제 로드 위치 확인. 가능한 경우 동일 Wrapper 경로에서 버전 확인. v1.6.21 여부를 보고. CLI 사용 가능 시 실제 설치본에서 `python3 -m l1_fix_workflow --version`.
2. Kernel v0.7.13, skill-updater v0.5.42, code-analyzer v0.15.0의 설치본/실행 경로를 확인. 버전이 불명확하면 UNKNOWN; 추정 금지.
3. `python3 -m l1_fix_workflow provider-status`로 기존 Provider Manifest의 code-analyzer 등록·launcher·승인·실행가능 상태를 확인. 비밀정보/전체 Manifest를 출력하지 마.
4. `python3 -m l1_fix_workflow code-roots list`로 ~/.l1-ledger/code_roots.json의 origin, enabled, root_id, scm을 확인. Registry가 없고 기존 단일 smp1900 Manifest만 있으면 LEGACY로 보고(자동 생성 금지). CLI가 안 되면 같은 MCP에 "현재 코드 루트 설정 보여줘"를 읽기 전용으로 요청.
5. smp1900 Git 실제 경로(/home/whpark/Project/smp1900), 현재 HEAD 및 Root 매핑만 읽기 전용으로 확인. Checkout 전환 금지.
6. SMP1800/SMP1770은 각각 등록 경로·p4_client·enabled를 확인. 이미 등록·승인된 경우에만 P4 Client/View와 로컬 경로 매핑을 `p4 info`, `p4 -c CLIENT client -o CLIENT`, 필요 시 지정된 실제 파일 1개에 대해 `p4 where`/`p4 have`로 조회. 경로/Client 미설정은 WAIT_CONFIG로 보고. 서버 접근 실패는 BLOCKED로 구분. 다른 클라이언트를 추정해 사용하지 마.
7. 코드 루트 선택을 MCP 자연어 조회가 처리하는지 확인. 읽기 전용 명령 결과에 Provider 1개, Git/P4 루트 분리 정보가 노출되는지 검사. MCP Wrapper가 신규 CLI로 연결되지 않으면 WRAPPER_ROUTE_MISSING.
8. Jira 쓰기 기본 DENY, 빌드/UT 기본 OFF, Git/P4 쓰기 및 Docs Push 기본 차단 정책이 설정/코드상 유지되는지 확인 가능한 범위에서 점검. 미검증을 PASS로 표시하지 마.

응답은 모바일 입력용으로 간단히:
1) 숫자 한 줄: A B C D E F G H I (9개, 공백 구분)
 A Workflow 설치: 1=1.6.21,2=다른 버전,3=확인불가
 B Kernel: 1=0.7.13,2=다름,3=확인불가
 C Updater: 1=0.5.42,2=다름,3=확인불가
 D Code Analyzer: 1=0.15.0 실행 등록,2=누락/차단,3=확인불가
 E MCP 루트 조회: 1=성공,2=라우팅/연결 실패,3=확인불가
 F Registry: 1=owner_registry,2=legacy 단일 루트,3=미설정/오류
 G smp1900: 1=승인·경로 정상,2=미등록/비활성,3=경로 오류/확인불가
 H SMP1800: 1=승인·매핑 정상,2=WAIT_CONFIG,3=BLOCKED/불일치
 I SMP1770: 1=승인·매핑 정상,2=WAIT_CONFIG,3=BLOCKED/불일치
2) 다음 줄: 주요 BLOCKED 오류 코드 최대 3개만(없으면 NONE).
3) 다음 줄: 현재 가능한 다음 행동 1개만. 실분석은 실행하지 않았다고 명시.
긴 JSON/로그/개인 경로·인증정보는 붙여넣지 마.
```

## 프롬프트 B — 실제 분석 검증 (A 이후, 별도 사용자 승인 시에만)

```text
이제 사용자가 지정한 기존 Work와 승인된 단일 코드 루트에서 작은 C/C++ 함수 1건만 읽기 전용 Code Analyzer 분석해줘. 대상 Work ID, root_id, 함수 또는 코드 경로가 명시되지 않으면 실행하지 말고 필요한 항목만 물어봐. 신규 Work 생성 금지. 기존 run_l1_fix_workflow를 통해 실행하고 root_id·scm을 명시해라. Git/P4 checkout/sync/edit/submit/push, Jira 쓰기, 빌드/UT, 문서 게시 금지.

실제 Runner 종료 상태/exit code 확인 후 Work Evidence ID와 `behavior_facts_with_provenance.json`의 존재·source_provenance 확인. Git은 HEAD·로컬 파일 SHA, P4는 각 파일 depotFile·haveRev·매칭되는 CL(없으면 null)·로컬 SHA 확인. 분석 전후 변경 시 STALE_SOURCE로 보고. 경로만 있거나 QUEUED/READY라면 성공이라고 하지 마. P4는 실제 사내 Client 테스트인지 mock인지 구분. 응답: 1=E2E PASS, 2=BLOCKED, 3=RUN FAILED, 4=NOT TESTED + 핵심 오류 코드 한 줄.
```

**해석:** A에서 H/I=2는 곧바로 기능 결함이 아니라 P4 등록·승인 대기일 수 있다. P4 실제 분석 PASS는 B에서 별도 검증해야 한다. STEP 3(FEATURE REQ/CMT/DEC)와 STEP 4(HLD/MSC 누적)는 v1.6.21 완료 범위가 아니다.
