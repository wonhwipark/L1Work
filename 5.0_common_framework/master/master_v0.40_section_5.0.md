# Master v0.40 Extract - 5.0 Common Automation Framework

- 원본: `master/L1_AI_Automation_Roadmap_v0.40.md`
- 추출 기준: `## 5.0 Common Automation Framework`부터 `## 5. Key Automation Items` 직전까지
- 경계 검토: 명확함

---

## 5.0 Common Automation Framework

모든 5.x 자동화 항목은 다음 공통 원칙을 따른다. 상세는 [`prompt/5_0_common_automation_framework.md`](L1a/prompt/5_0_common_automation_framework.md)을 참조한다.

### 5.0.5 Prefer Existing Environment

새로운 도구나 패키지를 추가하기보다 기존 환경의 bash/grep/find 등 도구를 최대한 활용한다.
예: Track B (Code Analyzer)는 Python CLI가 아닌 bash 기반 정적 추출 사용.

### 5.0.9 Skill Layer vs Workflow Layer

**Skill Layer:** 재사용 가능한 분석 로직 (staged-code-analyzer, staged-code-review 등)을 스킬 형태로 구현.
Roo Code/Claude Code로 실행하며, 새 L1a 버전마다 07_skills_vX.X.zip 형태로 배포.

**Workflow Layer:** Skill을 호출하는 실행 프롬프트를 `L1a/prompt/` 폴더에 저장.
팀원이 프롬프트를 직접 Claude Code/Roo Code에 입력하여 실행.

두 Layer는 명확히 분리 관리하며, Skill 변경 시 프롬프트와의 호환성을 확인한다.

### 5.0.10 Staged Analysis for Large Codebases

대용량 폴더(30분 이상 분석)는 다음 단계로 나눈다:

1. **Phase 0:** 전체 인벤토리 (빠른 카운트)
2. **Phase 1..N:** 단계별 REQ-site 분석 (각 Stage는 독립적 문맥)
3. **Checkpoint:** 각 Stage 완료 후 `review_progress_<YYYYMMDD>_<HHMM>_KST.md` 저장
4. **Global Carry Mechanism:** Stage별 분석 결과 중 공유 요소(예: IPC CNF 파일 처리)는 1회만 분석하고 이후 Stage에서 재사용
5. **Phase F:** 전 Stage 결과 통합 및 최종 산출물 생성

이를 통해 문맥 초과 위험을 방지하고, 재개/재실행 시 효율성을 높인다.
