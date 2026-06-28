# L1SW Log Analyzer 동작 정리 + L1SW → 5.5 전체 Flow

작성일: 2026-06-20 (온사이트 확인 A~F 기반, Option A 확정)
근거 문서: `L1SW_CHECKLIST_OBJECTIVE_v2.md`, `L1SW_LOG_ANALYZER_COMPARISON.md`

---

## 1. L1SW Log Analyzer란

사내에서 이미 배포되어 사용 중인 Claude Code 스킬. 대용량 `.sdm` 로그를 1차로 줄이고
사람이 보기 좋은 HTML 리포트로 만들어주는 도구다. 5.5 RCA Knowledge Graph와는 별개로
개발되었으나, 2026-06-20 확인 결과 **역할이 정확히 보완 관계**임이 확정되었다(Option A).

```text
이름:        l1sw-log-analyzer
스킬 위치:    C:\Users\<id>\.claude\skills\l1sw-log-analyzer\
핵심 스크립트: scripts\parse.ps1 (내부에서 scripts\sdm_to_test.ps1 호출)
```

### 1.1 처리 파이프라인

```text
.sdm (원본, 예: 704.9 MB)
   ↓  sdm_to_test.ps1 — 바이너리 .sdm을 timestamp 컬럼 기반 평문 텍스트로 변환
전체 .txt
   ↓  parse.ps1 — manifest fragment JSON의 모듈명→regex 매핑으로 필터링
      옵션: -Modules (모듈 부분집합), -TimeFrom/-TimeTo (시간 윈도우)
_l1sw.txt (예: 5 MB, 45,624행 — 원본 대비 약 1/140 압축)
   ↓  분석가가 grep/sed로 관련 구간 발췌 (수백 KB 단위)
   ↓  HTML 리포트 생성 (severity 배지 + 핵심패턴 통계표)
<JIRA_KEY>_#N_vM_<dump폴더명>.html
   ↓  (옵션) jira/scripts/attach.py 호출
Jira 이슈에 HTML 첨부
```

### 1.2 필터링 기준 — manifest fragment JSON

모듈/시간 필터의 Single Source of Truth는 manifest 디렉터리의 **5개 fragment JSON**이다.
각 JSON은 `"모듈명": "regex"` 구조로 되어 있다.

```json
// 예시 (proc.json)
{
  "Allocator": "\\[Allocator\\]",
  "DSSM": "\\[DSSM\\]|##\\[DSSM\\]"
}
```

이 regex가 prefix/키워드 기반 필터링에 그대로 사용된다. `-Modules` 옵션으로 전체 모듈
목록 중 부분집합만 골라 필터할 수 있다 (예: `proc` 파트의 Allocator, PathArbitor, DSSM /
`front` 파트의 LTE_FRONT, RXCFG 등).

**중요:** 이 regex는 **모듈명만** 매핑하며, 증상 키워드(예: `PHY_TIMER_EXPIRY`)는 매핑하지
않는다. 즉 L1SW는 "어느 모듈에서 난 로그인가"는 걸러주지만 "이게 어떤 유형의 문제인가"는
판단하지 않는다.

### 1.3 출력물

- **최종 산출물은 HTML only.** JSON/YAML/CSV 같은 기계가 읽을 구조화 출력 옵션은 없다.
- 중간 산출물인 `_l1sw.txt`는 기계 처리 가능한 평문이지만, 별도의 구조화 스키마(필드 구분)는
  없다. `parse.ps1` 실행 시 stdout 마지막 줄에 `_l1sw.txt` 경로가 출력된다.
- HTML 리포트 안의 "핵심패턴통계표"에 grep 카운트가 들어 있지만, 이는 사람이 읽기 위한
  free-form 텍스트이지 파싱을 의도하고 설계된 구조가 아니다.
- **라인번호가 없다.** `.sdm` → 텍스트 변환 결과는 timestamp 컬럼 기반이며, 행 번호 컬럼이
  별도로 부여되지 않는다. (`.sdm` 바이너리 버전에 따라 내부 코드/라인 위치가 달라질 수 있기
  때문에 라인번호를 매기지 않는 것으로 추정됨.) `_l1sw.txt`에도 라인번호는 없다.

### 1.4 issue_type 분류 — 없음

HTML 보고서, manifest 어디에도 RACH/SCG/TX/L2 같은 **문제유형(issue_type) 라벨 체계는
존재하지 않는다.** L1SW는 모듈 단위로만 로그를 분류하며, "이 증상이 어떤 유형의 장애인가"는
전적으로 분석가(또는 5.5)의 몫이다.

### 1.5 지식 누적 구조

L1SW에도 지식 누적 메커니즘이 있다. 두 가지 방식이 함께 쓰인다.

| 방식 | 누적 위치 | 누적 단위 |
|---|---|---|
| skill 파일 직접 수정 | `references/<part>/<module>.md` | 모듈 기반 (예: Allocator, RXCFG) |
| manifest 갱신 | `manifest/<part>.json` | modules 객체에 regex 한 줄 추가 |
| cross-folder 조합 | `log_prefixes.md`의 cross-folder 섹션 | 증상 단위 (모듈 조합으로 나타나는 현상) |

cross-folder 섹션 예시: *"BPLMN scan 후 hold/resume 시 RF path on 누락 → LTE_FRONT +
L1cRxCfgPrcs"* — 이건 "이 증상이 어느 모듈 조합에서 나타나는가"를 기록한 것이지, 5.5의
issue_type/root_cause처럼 "이 증상이 어떤 유형·원인으로 귀결되는가"를 기록한 게 아니다.
**분류축이 다르므로 중복이 아니라 인접 영역**으로 판단한다.

재사용 방식은 **분석가가 수동으로 참조**하는 것뿐이다. step2에서 `log_prefixes.md`를
읽고 → 해당 모듈 `.md`를 읽는 절차를 사람이 직접 수행하며, 프롬프트에 자동으로 주입되는
메커니즘은 없다.

### 1.6 crash(dump) 분석 — L1SW 전담

dump 파일 기반 crash 분석 기능이 L1SW에 이미 존재한다. 다른 issue_type과 동일한 공통
HTML 절차(step8)를 쓰며, 차이는 "분석한계 섹션에 dump 미확보를 명시"하는 정도뿐이다.
HTML 파일명 패턴(`<JIRA_KEY>_#N_vM_<dump폴더명>.html`)으로 외부에서 경로 참조가 가능하다.

→ **5.5는 crash를 자체 분석하지 않기로 확정.** L1SW 산출물을 경로로만 참조한다.

### 1.7 외부 자산 연결

Jira 첨부 자동화(`jira/scripts/attach.py`)는 있다. HLD/TC/API 문서를 연결하는 필드나
기능은 없다. 이 부분은 5.5의 고유 가치 영역이다.

### 1.8 운영 환경 메모

```text
parse.ps1 경로:        C:\Users\<id>\.claude\skills\l1sw-log-analyzer\scripts\parse.ps1
sdm-parser 내부호출:    C:\Users\<id>\.claude\skills\l1sw-log-analyzer\scripts\sdm_to_test.ps1

_l1sw.txt 보존:        항상 보존됨 (자동삭제 로직 없음).
                       -KeepFull 스위치는 "필터 전 전체 텍스트" 보존 여부 옵션이며,
                       _l1sw.txt 자체와는 별개.

크기/토큰 가늠:        .sdm 704.9MB → _l1sw.txt 5MB(45,624행), 약 1/140 압축.
                       평문 약 100~150만 토큰 수준(1토큰 약 3~4bytes)이나,
                       실제 분석에서는 전체를 한 번에 read하지 않고
                       sed -n/grep으로 구간 발췌 → 호출당 실투입 토큰은
                       수천~수만 줄(수백KB) 단위. 시간윈도우 적용 시 더 작아짐.
```

---

## 2. L1SW → 5.5 전체 Flow

### 표 1. 파이프라인 단계별 — 누가 무엇을 하는가

| 단계 | 입력 | L1SW가 하는 일 | L1SW 출력 | 5.5가 이어받아 채우는 것 | 5.5 출력 |
|---|---|---|---|---|---|
| 0. 원본 수집 | `.sdm` (예: 704MB) | `parse.ps1` → `sdm_to_test.ps1` 변환 | 전체 `.txt` | — | — |
| 1. 1차 필터 | 전체 `.txt` | manifest regex(모듈명) + `-TimeFrom/-TimeTo` + `-Modules` 필터 | **`_l1sw.txt`** (예: 5MB, 1/140 압축) | — | — |
| 2. 구간 발췌 | `_l1sw.txt` | 분석가가 grep/sed로 구간 추출 | 텍스트 구간 (수백KB) | — | — |
| 3. 사람용 리포트 | 발췌 구간 | severity 배지 + 핵심패턴 통계표 | **HTML** (`<JIRA>_#N_vM_<dump>.html`) | — | — |
| 4. issue_type 분류 ⭐ | `_l1sw.txt` / HTML | ❌ 멈춤 (모듈명만, 유형 라벨 없음) | — | rach/scg/tx/l2 4종 유형 판정 | `issue_type` |
| 5. 구조화 추출 ⭐ | 발췌 구간 | ❌ HTML 평문만, 파싱 비의도 | — | 패턴·증상·timestamp를 YAML 필드로 추출 | `cases/*.yaml` |
| 6. Root Cause ⭐ | 구조화 데이터 | ❌ 없음 | — | `root_cause_category` 분류 + evidence 연결 | case의 `root_cause` |
| 7. 외부자산 연결 ⭐ | jira_key (HTML 파일명) | Jira 첨부만 | jira_key | jira_key 정합 + HLD/TC/API 연결 | case의 `related` |
| 8. 지식 누적 | 확정된 case | 모듈+증상 혼합 축 `.md`/manifest 수정 | 모듈/증상 지식 | **issue_type 축** `skills_seed/*.md` 정제 | skills_seed 갱신 |
| 9. 과거 케이스 검색 ⭐ | 신규 증상 | ❌ 자동 참조 없음 | — | index → 유사 case 검색 | `indexes/index.md` |

⭐ = L1SW가 멈추고 5.5가 채우는 공백 (총 6개 영역)

### 표 2. case YAML 필드별 — 채움 주체

| case 필드 | 채움 주체 | 근거 |
|---|---|---|
| `source.original_log` | L1SW 파이프라인 메타 | `.sdm` 경로/크기 |
| `source.signal_file` | L1SW `_l1sw.txt` 경로 그대로 참조 | 항상 보존됨 |
| `symptom.occurred_at` | **timestamp 기반** | 라인번호 없음 |
| `symptom.module` | L1SW 모듈 prefix (`[DSSM]` 등) | 모듈명만 regex 매핑 |
| `symptom.severity` | L1SW severity 배지 | — |
| `log_patterns[].time_range` | **timestamp 범위** (구 `line_range`에서 변경) | 라인번호 없음, schema 수정 완료 |
| `log_patterns[].frequency` | 5.5가 직접 집계 | HTML 통계표는 비구조 텍스트 |
| `issue_type` | **5.5 고유** | L1SW에 유형 라벨 없음 |
| `root_cause.*` | **5.5 고유** | L1SW에 없음 |
| `related.jira` | jira_key 정합 | HTML 파일명에서 추출 |
| `related.hld/tc/api` | **5.5 고유** | L1SW에 연결 필드 없음 |
| `skill_seed` | **5.5 고유 (issue_type 축)** | L1SW는 모듈+증상 혼합 축 |

---

## 3. 핵심 요약

- L1SW는 **로그를 줄이고(1차 필터) 사람이 보게 만드는(HTML)** 도구, crash는 전담 분석까지 한다.
- 5.5는 L1SW가 멈추는 지점부터 시작해 **유형 분류·구조화 저장·원인 분석·외부 자산 연결·
  지식 정제·과거 사례 검색**을 담당하는 후처리 계층이다.
- 두 시스템은 **중복이 아니라 보완 관계**이며, 5.5의 입력원은 raw 로그가 아니라 L1SW가
  생성한 `_l1sw.txt`로 확정되었다 (Option A).
- 라인번호가 없다는 제약 때문에 5.5의 모든 위치 식별은 **timestamp 기준**으로 통일되었다.
