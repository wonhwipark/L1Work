# L1SW Log Analyzer vs 5.5 RCA Knowledge Graph — 비교 분석

**작성:** Claude (claude.ai 채팅 세션, L1a 패키지 검토 중)
**일시:** 2026-06-19 KST
**배경:** 사용자가 사내에서 L1SW Log Analyzer 스킬을 전달받아 사용 중이며, 5.5 RCA Knowledge Graph와의 상충 여부를 확인하고자 함. 이 검토 과정에서 RCA를 L1a로부터 별도 트랙으로 분리하기로 결정함.

---

## 1. 사용자가 제공한 L1SW Log Analyzer 정보 (원문 정리)

```text
이름: l1sw-log-analyzer

입력 파이프라인:
  .sdm live trace
    → parse.ps1
    → _l1sw.txt 생성
    → 분석

토큰 절약 옵션:
  -TimeFrom, -TimeTo   (시간 윈도우)
  -Modules             (모듈 부분집합, 예: 'Allocator, DSSM')

출력:
  Self-contained HTML 리포트
    - CSS 인라인
    - 다크 헤더
    - 색상 배지(severity 등으로 추정)
  로컬 파일로 저장

필터링 메커니즘 (Single Source of Truth):
  Manifest 디렉터리의 5개 fragment JSON
    → 각 JSON: 모듈명 → regex 매핑 구조
    → sdm parser에 전달되어 prefix/키워드 기반 필터링 수행

모듈 분기:
  -Modules 옵션으로 부분집합 필터 가능 (예: 'Allocator, DSSM')
  [DSSM] 같은 모듈 prefix로 분기 가능
```

**미확인 (다음 세션에서 추가 확인 필요):**
1. `_l1sw.txt` 크기가 원본 `.sdm` 대비 몇 % 수준으로 축소되는가
2. 시간윈도우 + 모듈 필터링 후에도 Context 초과 리스크가 남아있는가
3. 과거 분석 HTML 결과를 다음 분석에서 참조/재사용하는 메커니즘이 있는가
4. issue_type(rach_failure, scg_failure 등) 같은 문제 유형 분류 체계가 있는가, 아니면 모듈 기반 분류만 있는가
5. 분석 결과(HTML)를 구조화 데이터(YAML/JSON)로도 병행 저장하는가

---

## 2. 비교표 (1차 분석, 정보 보완 전)

| 항목 | L1SW Log Analyzer | 5.5 rca_kg/ (L1a) |
|------|---|---|
| 입력 | `.sdm` live trace → `parse.ps1` → `_l1sw.txt` | raw `log.txt` (100MB~1GB) → issue-type pre-filter → `signal_<issue_type>.txt` |
| 필터링 기준 | Manifest 기반 모듈명→regex 매핑 (5개 fragment JSON), prefix/키워드 | Issue type별 keyword/signature (rach/scg/tx/l2/crash) |
| 토큰 절약 방식 | 시간윈도우(`-TimeFrom/-TimeTo`) + 모듈 부분집합(`-Modules`) | Context window(전후 N줄) + issue-type 필터 |
| 분기 기준 | 모듈명 (`[DSSM]`, `Allocator` 등) | 문제 유형 (issue_type) |
| 출력 형식 | Self-contained HTML (사람이 읽는 리포트) | case YAML + RCA Markdown (LLM/Git 친화적 구조화 데이터) |
| 저장 방식 | 로컬 HTML 파일 | `rca_kg/cases/*.yaml` + `indexes/` + `skills_seed/*.md` |
| 재사용 구조 | 미확인 | case YAML 누적 → index → skills_seed 패턴 정제 |

---

## 3. 1차 판단

**상충 가능성이 있는 지점:**

- 입력 전처리 단계가 사실상 중복일 수 있음. `_l1sw.txt`가 이미 모듈/시간 기준으로 충분히 축소된 상태라면, 5.5의 issue-type pre-filter 단계가 이 결과물 위에서 다시 동작해야 하는지, 아니면 생략 가능한지 결정 필요.
- 두 시스템 모두 "대용량 로그를 어떻게 줄여서 LLM/사람에게 넘길 것인가"라는 동일한 문제를 다루고 있어, 두 파이프라인을 그대로 병렬 운영하면 같은 로그를 두 번 가공하게 될 가능성이 있음.

**상충하지 않고 상호 보완적인 지점:**

- 필터링 축(모듈 vs 문제유형)이 직교(orthogonal)함. 같은 신호 소스에 대해 "어느 모듈에서" + "어떤 문제 유형인지"를 동시에 좁히는 데 두 기준을 함께 쓸 수 있음.
- 출력 목적이 다름. L1SW HTML은 사람이 보는 리포트, 5.5 YAML/Markdown은 LLM이 읽고 누적·재사용하는 지식 자산. 한쪽이 다른 쪽을 대체한다기보다, L1SW 출력 이후 단계(RCA 결론을 구조화해서 누적)로 5.5를 이어붙이는 구성이 가능해 보임.

**결론 (잠정):** 완전한 중복은 아니지만, 입력 전처리 단계에서 역할 정리가 필요함. 미확인 5개 항목을 확인한 후 통합 또는 역할 분리 방향을 확정하는 것이 다음 단계.

---

## 4. 통합/분리 방향 옵션 (다음 세션에서 결정)

| 옵션 | 내용 |
|------|------|
| A | L1SW가 1차 필터(모듈/시간) 담당, 5.5는 그 결과(`_l1sw.txt`)를 입력으로 받아 issue-type 분류 + RCA YAML 누적만 담당 (역할 분리, 5.5의 pre-filter 단계 폐기) |
| B | 두 파이프라인 독립 유지, 5.5는 L1SW를 거치지 않은 원시 로그도 처리 가능하게 유지 (병렬 운영) |
| C | 5.5의 case YAML 스키마에 L1SW HTML 리포트 경로/요약을 `source` 필드로 연결만 하고 나머지는 그대로 (느슨한 연동) |

---

## 5. 다음 액션

1. 사내 Claude Code 환경에서 L1SW Log Analyzer 스킬 파일을 직접 읽어 위 5개 미확인 항목 보완
2. 보완된 정보로 위 옵션 A/B/C 중 선택
3. 선택 결과에 따라 RCA 전용 워크플로(아래 `HANDOFF_5.5.md` 참조) 갱신
