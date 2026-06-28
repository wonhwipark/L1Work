# Master v0.40 Extract - 5.1 Jira Feedback Loop

- 원본: `master/L1_AI_Automation_Roadmap_v0.40.md`
- 추출 기준: `### 5.1 Jira Feedback Loop`부터 `### 5.2 Code Analyzer` 직전까지
- 경계 검토: 명확함

---

### 5.1 Jira Feedback Loop
```text
(1) Critical Defect Detection
      ↓
(2) AI Root Cause Analysis
      ↓
(3) AI Patch Proposal
      ↓
(4) P4 Shelve Creation
      ↓
(5) Jira Creation
    (Shelve Number + Root Cause Summary + Patch Proposal Summary 포함)
      ↓
(6) Review & Discussion
      ↓
(7) Resolution Decision
    ├─ Reject
    │     ↓
    │   False Positive Rule 정리
    │     ↓
    │   Skill Update
    └─ Resolve
          ↓
        Prevent Rule 정리
          ↓
        Skill Update
```
Jira Feedback Loop는 Critical Defect Workflow의 후속 단계이다.
AI가 결함 후보의 Root Cause를 분석하고 Patch를 제안한 후 P4 Shelve를 생성한다.
Jira 등록 시 Shelve Number, Root Cause Summary, Patch Proposal Summary를 포함하여 Reviewer가 즉시 수정 후보를 확인할 수 있도록 한다.
Review 결과는 Reject와 Resolve로 분기한다. Reject 사례는 False Positive Rule로, Resolve 사례는 Prevent Rule로 정리하여 각각 Skill에 반영한다.
Jira Close 상태는 Jira MCP 폴링(JQL)으로 감지하고 Resolution 필드로 Reject/Resolve를 분류한다.
목적은 Jira 처리 결과를 Rule, Skill, Prompt, Workflow 개선으로 연결하는 것이다.
**Expected Benefit**
- False Positive 감소; 경험 축적; Rule 강화; Review 결과 재사용; Critical Defect 검출 정확도 향상; Jira Close 이후 지식 손실 방지
**Precondition**
- 4.1 Critical Defect Workflow 완성 필요; Jira MCP 연동 필요; Resolution 필드 기준 정의 필요 (Reject/Resolve 분류 기준); Review Comment 수집 방식 필요; Perforce MCP 또는 p4 CLI 연동 필요
**Storage / Reuse**
- Rule DB; False Positive History; Prevent Rule; Review Feedback; Rule Version; Prompt / Skill DB; 다음 Branch Scan에서 Prevent Rule 재사용; 유사 Defect 검출 시 기존 Jira와 RCA 연결
