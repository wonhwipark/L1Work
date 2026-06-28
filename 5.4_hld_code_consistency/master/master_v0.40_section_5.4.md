# Master v0.40 Extract - 5.4 HLD-Code Consistency

- 원본: `master/L1_AI_Automation_Roadmap_v0.40.md`
- 추출 기준: `### 5.4 HLD ↔ Code Consistency Check`부터 `### 5.5 RCA Knowledge Graph` 직전까지
- 경계 검토: 명확함

---

### 5.4 HLD ↔ Code Consistency Check
```text
HLD
  ↓
Code 분석
  ↓
Gap Detection
  ↓
누락 Branch 발견
  ↓
HLD 수정안
  ↓
Confluence Update
```
HLD ↔ Code Consistency Check는 HLD 문서와 실제 Code 구현이 일치하는지 확인하는 Workflow이다.
5.2에서 생성된 Call Flow MSC와 JSON 메타데이터를 입력받아, 기존 HLD의 Sequence Diagram 및 구현 설명과 비교하여
runtime Call Flow 변경 여부, 누락된 Branch, 구현 의도 불일치를 검출한다.
**Expected Benefit**
- 설계 최신화; 문서 품질 향상; Code와 HLD 간 불일치 감소; Review 품질 향상; 신규 인원 이해도 향상; 기능 변경 이력 추적 강화
**Precondition**
- HLD 형식 표준화 필요; 5.2 Code Analyzer (Track A) 완료 권장; Confluence Update 권한 필요; Code 분석 범위 지정 필요. 주의: 5.2 Track B 단독 완료는 불충분 (Call Flow MSC 필수)
**Storage / Reuse**
- HLD Section; Code Path; API; Branch Condition; Gap Type; Suggested HLD Update; Confluence Link; Review Status; 다음 HLD 작성 시 Gap Pattern 재사용; Code Review 시 HLD 누락 검출
