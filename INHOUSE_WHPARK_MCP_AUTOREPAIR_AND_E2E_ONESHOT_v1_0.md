# 사내 개인 MCP 자동복구 구축 + 3개 기능 즉시 재검증 — 통합 원샷

- 버전: v1.0 / 2026-10-23
- 실행 환경: **사내 Linux의 권한 있는 OpenCode CLI** (기존 `whpark-mcp` 저장소 루트)
- 목적: **1단계: 개인 MCP의 범위 제한 자동 진단·복구 구축 → 2단계: MSC·코드분석·로그분석 즉시 검증**을 한 번에 수행
- 적용 전 상태: 원샷 실행 **미수행**. 문서 제공만으로 MCP 설정은 변경되지 않음.
- 범위: `whpark-mcp` 개인 소유·수정 허용 파일과 승인된 로컬 설정만. 회사 보안 정책, 운영 환경 도구 권한, 업무 원본 보호를 유지.

## 사내 OpenCode CLI에 전달할 통합 프롬프트

> 현재 작업 디렉터리가 실제 `whpark-mcp` 저장소인지 먼저 확인하고, 아래 코드블록 **전체를 한 번** 전달하세요. 코드블록 내부만 3,000자 이내로 제한했습니다.

```text
사내 Linux OpenCode CLI에서 기존 개인용 whpark-mcp의 자동 진단·복구를 최초 1회 구축하고, 바로 MSC/코드분석/로그분석 재검증까지 한 요청으로 완료해줘. 내 소유·수정 권한이 확인된 whpark-mcp 프로젝트 내부의 최소 변경은 승인한다. 회사 정책/호스트/도구의 별도 승인이 필요하면 우회하지 말고 보류해. 중간 질문 없이 가능한 작업을 연속 실행해.

기존 관찰: Workflow v1.6.46 MSC 요청이 brief로 반환. Wrapper/CLI 전달과 Evidence 원본은 미확인. code-analyzer는 설정만 연결; l1sw-dev-log-analyzer-plus는 실행 미확인. 실제 원인은 미확정.

[1. 최초 설정/자동복구]
A. 실제 git root, 수정 권한, 등록 MCP tool→기존 Wrapper→Runner→CLI→Provider 진입점과 설치본 버전 확인. 경로 임의 추정·무제한 탐색 금지. 변경 전 diff, 설정 백업, baseline, 롤백 계획 확보.
B. 기존 whpark-mcp의 허용 범위 안에서 재사용 가능한 auto-diagnose/repair 동작을 구현 또는 기존 기능 강화. 허용: read-only 상태 조회, 인자·경로·버전 매핑 수정, 프로젝트 소유 Wrapper/Runner/로컬 설정의 확인된 결함 패치, 테스트. 허용 파일/명령은 좁게 지정. 별도 새 Wrapper 또는 광범위 실행권한 만들지 마.
C. 흐름: 입력 검사→원인 분리(MCP/Wrapper/Runner/CLI/Provider/Evidence)→허용된 최소 수정→스모크/회귀→종료. 동일 장애 복구 최대 2회, 진전 없거나 회귀 시 중단·원복. 지속 설정과 변경 내역/롤백 안내를 프로젝트 내부 승인된 위치에 기록. 가짜 PASS 금지.
D. 사용자 Agent 요청이 실제 기존 Runner를 경유하는지, 이후에도 위 흐름을 호출 가능한지 mock 장애 1건으로 입증. 설정 파일만 작성되고 Agent에서 실행되지 않으면 '구현만' 판정.

[2. 즉시 3기능 재검증]
E. MSC: 정확 Work 20261007-SOC-411668을 대상으로 'resume --work-id 20261007-SOC-411668 --mode context --view msc'의 typed view 전달, CLI effective view, 최종 user_summary 일치를 확인. 실제 등록 Evidence path/파일/SHA 검증 후 canonical 원본이 있을 때만 Phase별 A→B: API Flow 확인. brief·메타·SVG만 출력한 경우 실패. 원본 복구·재등록·MSC 재생성 금지.
F. 코드분석: code-analyzer 설치/Provider/Runner/입력 전달을 점검, 안전한 fixture 스모크 수행. 실제 승인된 코드 입력으로 Provider 실행까지 확인한 경우에만 E2E로 기록. 코드 수정 금지.
G. 로그분석: l1sw-dev-log-analyzer-plus(정확한 이름) 설치/Provider/Runner/입력 전달과 안전한 fixture 스모크 확인. 승인된 실제 로그가 없으면 실분석 E2E 성공으로 보고하지 마.
H. brief/diagnostic, TL 요약, 주간보고 200자 포맷, BUG guard 회귀와 조회 전후 원본 무변경을 검증. 기능별 PASS/FAIL/NOT TESTED를 구별하고, 막힌 검증은 다른 기능까지 차단하지 마.

[보호]
Work/Kernel 원장/Journal/Evidence·Git/P4 원본·GitHub/Jira/Confluence 쓰기, 자격증명 변경, 회사 정책/OS 권한 우회, approval/Push Guard 해제 금지. SHA 검사 유지. Git worktree 금지. 외부 공개·무제한 shell·승인 없는 서비스 재시작 금지. 필요한 별도 승인은 사전 승인으로 간주하지 말고 보류. 비밀정보 로그 기록 금지.

최종 응답은 아래 Q1~Q6 숫자 6개만. 상세 기록은 허용된 로컬 보고서에 보존(경로는 답변하지 마). 재질문·장문 로그 금지. 확인 불가를 성공으로 바꾸지 마.
Q1 자동복구: 1 구현+Agent스모크PASS / 2 구현만 / 3 권한차단 / 4 실패
Q2 Wrapper/Runner: 1 경로·인자검증 / 2 일부만 / 3 오류지속 / 4 미확인
Q3 MSC: 1 실제Flow / 2 원본없음·무결성오류 / 3 brief지속 / 4 실행·확인불가
Q4 코드분석: 1 실제Provider실행 / 2 fixture스모크만 / 3 설정만·실패 / 4 미확인
Q5 로그분석: 1 실제Provider실행 / 2 fixture스모크만 / 3 설정만·실패 / 4 미확인
Q6 보호·회귀: 1 PASS / 2 오류원복 / 3 위반·회귀FAIL / 4 미검증
```

## 판정 및 후속 기준

**숫자만 반환해도 오해하지 않도록 성공 수준을 분리합니다.** `Q1=1`은 개인 MCP 자동복구를 Agent 호출 경로까지 검증했다는 뜻이고, `Q1=2`는 파일/설정 구현만 확인됐다는 뜻입니다. `Q4·Q5=2`는 테스트 입력에 대한 스모크이며, 실제 업무 코드·로그 분석 완료가 아닙니다.

- **핵심 합격:** Q1=1, Q2=1, Q3=1, Q6=1. 코드·로그분석은 실입력 미제공 시 Q4·Q5=2도 정상적인 *부분 검증*입니다.
- **Evidence 오류(Q3=2):** Wrapper를 무리하게 다시 수정하지 말고, 원본 등록 상태를 별도 승인 절차로 처리합니다.
- **권한 차단(Q1=3 등):** MCP Agent로 같은 프롬프트를 반복하지 말고, 정식 수정 권한/승인이 있는 실행 환경에서 해결합니다.
- **소스 범위:** `whpark-mcp` 밖의 Workflow/Kernel/Code Analyzer/Log Analyzer 소스 변경은 이 최초 설정 요청에 포함되지 않습니다. 확인된 외부 스킬 결함은 별도 변경 계획으로 남깁니다.

## 실행 방법

1. 사내 Linux에서 **기존 `whpark-mcp` 프로젝트 루트**를 OpenCode CLI로 연 후 위 코드블록을 한 번 입력합니다.
2. 작업이 끝나면 사내 실행 결과 **숫자 6개만** 이 대화에 전달합니다.
3. 자동복구 체계 자체가 정상 연결됐다면 이후 MSC/코드분석/로그분석 요청마다 동일 진단 프롬프트를 반복할 필요가 줄어듭니다. 다만 권한 부족이나 실제 원본 부재는 자동 복구 대상으로 취급하지 않습니다.
