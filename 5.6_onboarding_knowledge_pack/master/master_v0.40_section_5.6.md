# Master v0.40 Extract - 5.6 Onboarding Knowledge Pack

- 원본: `master/L1_AI_Automation_Roadmap_v0.40.md`
- 추출 기준: `### 5.6 Onboarding Knowledge Pack 자동 생성`부터 `## 6. Common Infrastructure` 직전까지
- 경계 검토: 명확함

---

### 5.6 Onboarding Knowledge Pack 자동 생성
```text
도메인 태그 + 신규 인원 ID
  ↓
API Call Flow DB 조회
  ↓
RCA Knowledge Graph 조회
  ↓
Call Flow MSC + 모듈소개 연결
  ↓
Onboarding Page 생성
```
Onboarding Knowledge Pack 자동 생성은 신규 인원이 특정 도메인에 투입될 때 필요한 핵심 자료를 자동으로 묶어 제공하는 Workflow이다.
도메인 태그를 기준으로 5.2 Code Analyzer의 Call Flow MSC + 모듈소개, RCA Knowledge Graph, HLD 문서, TC, FAQ, Best Practice를 조회하여 Onboarding Page를 생성한다.
**Expected Benefit**
- 온보딩 기간 단축; 구두 전달 의존도 감소; 도메인 지식 재사용; 신규 인원 초기 분석 시간 감소; 과거 RCA 사례 전달; 필수 API와 HLD 누락 방지
**Precondition**
- 5.2 Code Analyzer (Track A) 완성 필요; 5.5 RCA Knowledge Graph 완성 필요; Team Knowledge 저장 구조 필요; 도메인 태그 기준 필요
**Storage / Reuse**
- Domain Guide; API List; HLD Link; RCA Case; TC Link; FAQ; Best Practice; Owner; 신규 인원 투입 시 자동 Page 생성; 반복 질문을 FAQ로 전환
