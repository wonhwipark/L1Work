# Master §5.5 발췌 (원본 출처: L1a/master/L1_AI_Automation_Roadmap_v0.40.md)

> 이 파일은 L1a Master Roadmap v0.40 전체가 아니라 §5.5 섹션만 발췌한 참조용 사본이다.
> RCA가 L1a에서 별도 트랙으로 분리되었으므로, 원본 L1a S0~S9 워크플로 대상이 아니다.
> 단순 참고 자료로만 취급한다.

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

---

## 참고 — topic06 HOLD 상태 (L1a 측 기록)

L1a 워크플로 상에서 이 섹션에 대한 확장 제안(Step 1 대용량 로그 pre-filter)은 `topic06`으로 진행되었으나,
사용자 판단(2.3:C)에 따라 **Delta-only 보류(HOLD)** 상태로 남았다 — Master/Prompt에는 미반영.

보류 당시 사유 (L1a `last_status.md` / decision log 기준):
1. L1SW Log Analyzer 스킬과의 역할 중복/상충 가능성 검토 필요 (본 분리의 직접 계기)
2. 500회 이상 반복 분석 운영안은 팀 운영 방식 추가 논의 필요
3. PowerShell/Python 등 실행 환경 확정 필요

해당 topic06의 전체 산출물(GPT Delta, Claude Review, Decision Log)은 이 패키지의
`delta/`, `review_logs/` 에 그대로 보존되어 있다.
