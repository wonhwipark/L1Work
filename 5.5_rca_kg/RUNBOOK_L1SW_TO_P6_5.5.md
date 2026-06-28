# RUNBOOK_L1SW_TO_P6_5.5 — RCA 문제 해결표

갱신: 2026-06-27 12:21 KST  
정상 시작은 `START_HERE_5.5.md`를 따른다. 이 문서는 막혔을 때만 본다.

---

## 1. 설치 문제

| 증상 | 원인 | 조치 |
|---|---|---|
| `/root-cause-analyzer`가 보이지 않음 | 스킬 미설치 또는 재시작 전 | `INSTALL_SKILL.md`대로 설치 후 Claude Code/VSCode 재시작 |
| `validate_install.ps1` 실패 | 설치 경로가 다름 | `-TargetSkillsDir`로 실제 `.claude\skills` 위치 지정 |
| 기존 버전과 충돌 | 이전 스킬 폴더 잔존 | `install_skill.ps1 -Backup` 또는 `-Force` 사용 |

---

## 2. 입력 파일 문제

| 상황 | 조치 |
|---|---|
| `_l1sw.txt` 있음 | `/root-cause-analyzer` 호출 후 경로를 전달한다. |
| `.sdm`만 있음 | L1SW Log Analyzer로 `_l1sw.txt` 생성이 먼저 필요하다. RCA는 C0에서 안내한다. |
| 로그 경로가 불명확 | 절대경로 또는 패키지 루트 기준 상대경로를 제공한다. |
| 여러 로그가 있음 | 분석할 1개 로그를 먼저 지정한다. |

---

## 3. P0/C0 분기

| P0 결과 | 다음 행동 |
|---|---|
| `_l1sw.txt` 발견 | P1로 진행 |
| `.sdm`만 발견 | C0에서 L1SW 실행 또는 준비 방법 안내 |
| 둘 다 없음 | 로그 파일 위치를 사용자에게 요청 |
| current_run.yaml 불일치 | 새 로그 기준으로 초기화 여부 확인 |

---

## 4. P1 포맷 역설계 문제

| 증상 | 조치 |
|---|---|
| cptime 형식이 안 잡힘 | 로그 앞부분/중간 샘플을 추가 확인한다. |
| 모듈 필드 위치가 불명확 | 대표 라인 20~50개를 추가 샘플링한다. |
| 로그가 너무 큼 | 처음부터 전체 read하지 말고 샘플 + signature 검색으로 진행한다. |

---

## 5. P3 issue_type 문제

| 증상 | 조치 |
|---|---|
| 추천 issue_type이 애매함 | hit count 상위 2개를 비교하고 사용자에게 선택지를 제시한다. |
| 사용자가 issue_type을 이미 알고 있음 | 사용자 지정 issue_type을 우선한다. |
| 해당 issue_type signature가 부족함 | candidate로 기록하고 confidence를 낮춘다. |

---

## 6. P4 원인분석 문제

| 증상 | 조치 |
|---|---|
| 원인 후보가 1개로 단정됨 | 최소 2개 가설을 세우고 반증 단서를 확인한다. |
| anchor는 보이나 원인 줄이 없음 | 시간창을 넓히거나 signal을 재생성한다. |
| 담당영역 밖으로 보임 | `cases/unresolved/`에 handoff 대상으로 저장한다. |
| 추가 추출 2회 후에도 불명확 | confidence low case로 저장한다. |

---

## 7. P5/P6 지식화 문제

| 증상 | 조치 |
|---|---|
| case schema가 안 맞음 | `rca_kg/schema/rca_case.schema.yaml` 기준으로 정규화한다. |
| keywords 승격 근거가 약함 | candidate로만 저장하고 confirmed 승격은 보류한다. |
| 동일 signature가 이미 있음 | occurrence_count와 recent_occurrences를 갱신한다. |

---

## 8. 레거시 수동 모드

`prompt/` 폴더는 스킬 설치가 불가능한 환경에서만 사용한다. 정상 사용자는 `prompt/`를 열 필요가 없다.
---

## KG 저장소 문제

### KG 저장소가 스킬 아래에 있음

증상:

```text
C:\Users\<user>\.claude\skills\root-cause-analyzer\rca_kg
```

판단: 잘못된 위치다. 스킬 업데이트 때 삭제될 수 있다.

조치:

```powershell
.\configure_kg_root.ps1 -KgRoot "D:\AI_Automation\RCA_KG"
```

기존 스킬 아래 `rca_kg`에 case가 있다면 자동 삭제하지 말고 `STRUCTURE_FIX_GUIDE.md`의 KG 병합 절차를 따른다.
