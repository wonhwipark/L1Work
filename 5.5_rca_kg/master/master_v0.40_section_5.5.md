# Master v0.40 Extract - 5.5 RCA Knowledge Graph

- 원본: `master/L1_AI_Automation_Roadmap_v0.40.md`
- 추출 기준: `### 5.5 RCA Knowledge Graph`부터 `### 5.6 Onboarding Knowledge Pack 자동 생성` 직전까지
- 경계 검토: 명확함

---

### 5.5 RCA Knowledge Graph
```text
Issue
  ↓
Log
  ↓
Root Cause
  ↓
Fix
  ↓
Jira
  ↓
HLD
  ↓
TC
  ↓
API
  ↓
Knowledge Layer
```
RCA Knowledge Graph는 Issue, Log, Root Cause, Fix, Jira, HLD, TC, API를 연결하는 구조화된 지식 그래프이다.
RCA를 Graph 형태로 저장하면 특정 API, 특정 Root Cause, 특정 Log Pattern, 특정 Jira, 특정 TC를 기준으로 과거 사례를 재사용할 수 있다.
**Expected Benefit**
- 분석 시간 감소; 경험 재사용; 신규 인원 지원; 유사 Issue 검색; Root Cause Pattern 축적; Prevent Rule 생성; TC 보강 근거 확보
**Precondition**
- 5.2 Code Analyzer (Track A) 구축 필수. 주의: 5.2 Track B 단독 완료는 불충분 (API 연결 정보가 Track B JSON에 불완전).
- Jira와 RCA 문서 연결 필요; Log Pattern 저장 기준 필요; Root Cause 분류 기준 필요
**Storage / Reuse**
- Issue; Log; Root Cause; Fix; Jira; HLD; TC; API; Known Defect; Prevent Rule; 신규 Issue 분석 시 유사 RCA 검색; Critical Defect Rule 생성
