# Master v0.40 Extract - 5.3 Confluence Collection

- 원본: `master/L1_AI_Automation_Roadmap_v0.40.md`
- 추출 기준: `### 5.3-pre Confluence Child Page Collection`부터 `### 5.4 HLD ↔ Code Consistency Check` 직전까지
- 경계 검토: 명확함
- 포함 범위: `5.3-pre` 선행 수집 항목과 `5.3 Weekly Report Collection`을 단일 5.3 트랙 기준으로 함께 포함

---

### 5.3-pre Confluence Child Page Collection
```text
Parent Page URL 입력
  ↓
Child Page 탐색 (REST API → MCP → 본문 링크 추출 → Label → Title → Fuzzy → User Assisted)
  ↓
Child Page 본문 취합
  ↓
취합 원본 draft 저장
  (%USERPROFILE%\artifacts\weekly_report_draft_<YYYYMMDD>_<HHMM>_KST.md)
```
Confluence Child Page Collection은 5.3 Weekly Report Collection의 선행 실행 항목이다.
매주 새로 생성되는 Parent Page URL을 기준으로 실제 Child Page를 탐색하고, 발견된 Child Page 본문을 취합하여 5.3의 입력 draft를 생성한다.
탐색에 성공한 strategy는 선택적으로 profile로 저장하여 다음 주 실행 시 재사용할 수 있다.
현재 AI 실행 프롬프트 형태로 운용하며, 추후 Python 패키지로 구현 예정이다.
**Expected Benefit**
- 매주 반복되는 Child Page 탐색 및 본문 취합 자동화; 탐색 실패 시 단계별 fallback 제공; 5.3 실행을 위한 입력 draft 안정적 생성
**Precondition**
- Confluence read 가능 (MCP 또는 REST API); Parent Page URL을 사용자가 매주 제공
**Storage / Reuse**
- Child Page 탐색 strategy; 취합 draft; Confluence Page ID; 다음 주 Parent Page 탐색 시 strategy 재사용; Confluence MCP 기반 다른 자동화의 page 탐색 baseline
---
### 5.3 Weekly Report Collection
```text
5.3-pre draft (매주 새로운 Child Page 본문)
  ↓
이전 주 양식 기반 필드 파악 (Risk, Issue, Action Item 등)
  ↓
필드별 내용 추출
  ↓
이전 주 양식 복제 및 필드 갱신
  ↓
Confluence 업로드 또는 로컬 저장
```
Weekly Report Collection은 매주 반복되는 주간보고 작성을 자동화하는 Workflow이다.
5.3-pre에서 생성된 Child Page draft를 입력받아, 이전 주 양식을 기준으로 필드를 파악하고, 이번 주 내용으로 채운다.
Risk Trend, Issue Tracking, Action Item 추적을 자동으로 전월대비 비교하고 우선순위를 제안한다.
**Expected Benefit**
- 주간보고 작성 시간 단축; 주간 반복 질문 자동화; Risk/Issue 추적 강화; Action Item 완료도 추적; 팀 커뮤니케이션 개선
**Precondition**
- 5.3-pre Confluence Child Page Collection 완성 필요; 이전 주 주간보고 양식 존재 필요; Confluence Update 권한 필요; Risk 분류 기준 필요; Action Item 상태 기준 필요
**Storage / Reuse**
- Weekly Report; Risk Trend; Issue List; Action Item; Confluence Link; Next Week 계획; 주간보고 이력; Risk Pattern 축적; Action Item 재사용
