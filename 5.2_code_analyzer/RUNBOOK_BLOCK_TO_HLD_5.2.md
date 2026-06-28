# RUNBOOK_BLOCK_TO_HLD_5.2 — CodeAnalyzer 문제 해결표

갱신: 2026-06-27 10:38 KST  
정상 시작은 `START_HERE_5.2.md`를 따른다. 이 문서는 막혔을 때만 본다.

---

## 1. 설치 문제

| 증상 | 원인 | 조치 |
|---|---|---|
| `/code-analyzer`가 보이지 않음 | 스킬 미설치 또는 재시작 전 | `INSTALL_SKILL.md`대로 설치 후 Claude Code/VSCode 재시작 |
| `validate_install.ps1` 실패 | 설치 경로가 다름 | `-TargetSkillsDir`로 실제 `.claude\skills` 위치 지정 |
| 기존 버전과 충돌 | 이전 스킬 폴더 잔존 | `install_skill.ps1 -Backup` 또는 `-Force` 사용 |

---

## 2. 입력 문제

| 증상 | 원인 | 조치 |
|---|---|---|
| 분석 대상이 너무 넓음 | 블록/API명이 모호함 | 블록명, 대표 API, 메시지명 중 하나를 명확히 지정 |
| 파일 후보가 너무 많음 | 코드 루트가 상위 폴더 전체임 | L1 관련 하위 루트로 좁혀 재요청 |
| API 기준 분석이 안 이어짐 | API가 여러 overload/동명이인 | 파일 경로 또는 주변 함수명을 같이 제공 |

---

## 3. output/slug 문제

| 증상 | 원인 | 조치 |
|---|---|---|
| 결과가 안 보임 | 다른 slug로 생성됨 | `output/5.2/` 아래 최신 폴더 확인 |
| 이어하기가 엉뚱한 블록으로 감 | `current_slug` 불일치 | 요청에 원하는 slug 또는 블록명을 명시 |
| 과거 `artifacts/` 경로가 보임 | 구버전 산출물 | 새 결과는 `output/5.2/<slug>/`만 사용 |

canonical path:

```text
output/5.2/<slug>/
```

---

## 4. structure 문제

| 증상 | 원인 | 조치 |
|---|---|---|
| full structure가 너무 큼 | 전체 코드맵을 읽으려 함 | focused structure를 새로 생성하도록 요청 |
| structure root가 입력 코드루트와 다름 | 다른 분석 캐시를 집음 | 코드 루트와 slug를 명시해 재생성 |
| procedure 목록이 누락됨 | 후보 파일 축소가 과도함 | 누락 API/파일명을 추가로 제공하고 재탐색 요청 |

자동 탐색 우선순위:

```text
1. 최신 structure_*_focused.json
2. 300KB 이하의 structure_*.json
3. 큰 full structure는 명시 지정 시만 사용
```

---

## 5. MSC/HLD 문제

| 증상 | 원인 | 조치 |
|---|---|---|
| HLD 안에 MSC가 inline으로 들어감 | 구방식 출력 | 별도 `.puml`로 분리하고 HLD에는 `msc_ref`만 남기도록 요청 |
| procedure가 너무 많음 | 범위가 넓음 | 우선순위 procedure부터 분석하도록 요청 |
| call edge가 과도하게 커짐 | 전역 누적 본문 생성 | procedure별 local edge + 전역 ID 요약만 유지하도록 요청 |

---

## 6. 레거시 수동 모드

`prompt/` 폴더는 스킬 설치가 불가능한 환경에서만 사용한다. 정상 사용자는 `prompt/`를 열 필요가 없다.
