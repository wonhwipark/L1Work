# USER_GUIDE_5.5 — root-cause-analyzer 사용 가이드

버전: convenience_v0.21_kg_root_config  
갱신: 2026-06-27 12:21 KST  
대상: L1SW 로그 기반 RCA, case YAML 생성, keywords 후보 승격

---

## 1. 입력 파이프라인

```text
.sdm 원본
  → L1SW Log Analyzer
  → _l1sw.txt
  → /root-cause-analyzer
  → P0~P6
  → case YAML / keywords.yaml 후보
```

RCA는 `.sdm`을 직접 읽지 않는다. `_l1sw.txt`가 없으면 P0/C0에서 L1SW 실행 또는 파일 준비를 안내한다.

---

## 2. 설치와 KG 저장소

```powershell
.\install_skill.ps1
.\validate_install.ps1
```

| 방식 | 설명 | 명령 |
|---|---|---|
| 기본 | `<패키지루트>\rca_kg` 사용 | 설정 불필요 |
| 권장 | 버전과 무관한 고정 저장소 사용 | `.\configure_kg_root.ps1 -KgRoot "D:\AI_Automation\RCA_KG"` |

`kg_root`는 스킬 설치 폴더 아래에 두지 않는다.

---

## 3. 처음 분석 시작

```text
/root-cause-analyzer
C:\logs\ue01_20260627_l1sw.txt 원인 분석해줘
```

스킬은 `{kg_root}/runtime_tool_generate/current_run.yaml`과 `NEXT_STEP_5.5.md`를 기준으로 P0부터 시작하거나 진행 중 단계로 복귀한다.

---

## 4. 단계 개요

| 단계 | 목적 | 사람 확인 |
|---|---|---|
| P0 | workspace_root/kg_root 확정, 환경 진단, `_l1sw.txt` 유무 확인 | 필요 |
| C0 | `_l1sw.txt` 확보 안내 | 필요 시 |
| P1 | `_l1sw.txt` 포맷 역설계 | 필요 |
| P2 | manifest fragment 후보 생성 | 필요 |
| P3 | issue_type 추천, signal 생성 | 필요 |
| P4 | 원인분석 7단계, case YAML 생성/갱신 | 필요 |
| P5 | 자가점검, 승인 정규화 | 필요 |
| P6 | keywords candidate 승격 | 필요 |

두 번째 로그부터는 상태가 준비되어 있으면 보통 P3부터 시작한다.

---

## 5. 결과 확인

| 위치 | 의미 |
|---|---|
| `{kg_root}/runtime_tool_generate/current_run.yaml` | 현재 RCA 진행 상태 |
| `{kg_root}/runtime_tool_generate/format_profiles/` | P1 로그 포맷 역설계 결과 |
| `{kg_root}/signals_tool_generate/` | P3 issue_type별 signal |
| `{kg_root}/cases/*.yaml` | 분석 완료 또는 승인 대기 case |
| `{kg_root}/cases/unresolved/*.yaml` | 담당영역 밖/원인 미상/추가 확인 필요 case |
| `{kg_root}/indexes_tool_generate/index.md` | case 검색용 index |
| `{kg_root}/keywords.yaml` | confirmed/candidate signature 지식 |

---

## 6. 이어하기

```text
/root-cause-analyzer
이어서 진행해줘
```

---

## 7. 분석 정직성 원칙

```text
- 모르는 모듈을 아는 것처럼 단정하지 않는다.
- anchor cptime과 최초 이탈 지점을 분리한다.
- 가설은 최소 2개 이상 비교한다.
- evidence가 약하면 confidence를 낮게 기록한다.
- L1 담당영역 밖이면 unresolved로 분리한다.
```
