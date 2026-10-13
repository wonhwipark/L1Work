# TX Abnormal / SAR·TAS L1 Postmortem 프롬프트

## 목표
Jira MD에서 **실제 L1 수정된 TX Abnormal·LTE/NR SAR·TAS 이슈만** Postmortem한다. 현상·원인·Fix 코드, 반복 결함, Side Effect·Regression, 재발 방지를 분석하며 **Jira 설명보다 P4 코드 근거를 우선**한다.

## 도구·범위
- 입력: Jira Issue List MD. 목록 밖 이슈 추가 금지
- `p4-code-owner v0.6.7`의 `jira-fix-cl-scan` 사용
- Jira MCP(Description/Comment), Mango MCP(P4 CL/Diff), Read-only
- 필요 시 `issue-analyzer`, `code-analyzer`, `l1-log-analysis`
- MCP/스킬 불가 시 `BLOCKED` 사유 기록

## Phase 1: L1 수정 대상 선별 (먼저 실행)
1. MD에서 Jira Key 추출·중복 제거
2. Jira Description, **전체 Comment**, Status, Resolution 조회
3. Comment에서 CL 및 출처 추출. **Fix/Integration/참고** 구분
4. P4에서 원본 CL·Branch·수정 파일/API·Diff·수정자 검증
5. **수정 파일 경로로** L1 판정(기준 미설정 시 사용자 확인). Owner 소속으로 판정 금지
6. `TARGET`: L1 수정 확인(Mixed 포함) / `EXCLUDED`: L1 수정 없음 확인 / `PENDING`: CL 또는 근거 불충분

산출물:
- `01_Screening/L1_Target_List.md` (Jira·Feature·Fix CL·L1 수정 파일/API·Owner·근거)
- `01_Screening/Excluded_Pending_List.md` (제외/보류 사유)
- `01_Screening/CL_Evidence.json` (Jira Comment/P4 증거)

MCP에 **총/대상/제외/보류 건수와 보류 사유** 출력. **승인 전 Phase 2 금지.**

## Phase 2: Jira별 Postmortem (승인 후)
승인된 TARGET만 분석. `issue-analyzer`·`code-analyzer` 필요 시 호출, `l1-log-analysis`는 로그 필요 시만 사용.

이슈별: ① 증상·조건 ② Comment 히스토리 ③ Root Cause(`CONFIRMED/PROBABLE/UNKNOWN`) ④ Fix CL·변경 전후 코드 ⑤ Side Effect/Regression ⑥ 검증 누락·예방책.

산출물: `02_Issue_Analysis/{JIRA_KEY}_Postmortem.md`. Comment·P4 근거 첨부; 미확인은 `UNKNOWN`.

## Phase 3: 종합 Postmortem
Feature별 분포, 공통 원인(State/Timing/Config/Interface), 반복 결함·검증 취약점 그룹화. **동일 파일 수정만으로 동일 원인 단정 금지.**

산출물:
- `03_Final_Report/Postmortem_Summary.md` (TL용 요약·공통 원인·반복 패턴·개선 방향)
- `03_Final_Report/Improvement_Action_List.md` (과제·관련 Jira·우선순위·담당자·완료 기준)

## 안전 및 보고 원칙
- 조회·로컬 MD만 허용. **코드 수정·P4 CL·GitHub Push/PR·Jira 쓰기 금지**(별도 명시 승인 필요)
- 실패 시 `PENDING/BLOCKED` 및 사유·증거·진행 상태 보존
- MCP 화면에 **파일 경로·핵심 결과·다음 조치** 출력. HTML은 요청 시만 변환

**지금은 Phase 1만 수행하고 대상 목록을 보고한 뒤 Phase 2 승인 요청.**
