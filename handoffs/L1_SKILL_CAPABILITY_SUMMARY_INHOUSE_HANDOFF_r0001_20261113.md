# L1 관리 스킬 기능 요약 — 사내 GPT 인계용 (r0001)

- 작성: 2026-11-13 KST
- 공개 범위: 스킬 이름·일반 기능·재사용 안내만 포함한 **공개 가능 요약본**
- 출처 시점: 2026-11-12에 정리된 관리 대상 **18개 + 별도 사내 스킬 1개**의 기능 목록을 비민감 항목만 요약
- 구분: **기능 소개/정적 패키지 확인 ≠ 사내 설치본/실행 검증/배포 승인**
- 사용법: 이 문서를 사내 GPT에 공유할 경우, 필요한 스킬을 먼저 후보로 제시하고 실제 설치본의 SKILL.md/계약을 사내에서 확인한다. 이 요약만으로 작업 실행·코드 수정·권한을 승인하지 않는다.

## 1. 관리 스킬 기능 일람

| 번호 | 스킬 | 주요 역할·입력→출력 | 확인 시 주의 |
|---:|---|---|---|
| 1 | `issue-analyzer` | 증상/SDM/TXT/로그 → 원인 분석 및 수정 인계 | 근거 로그와 승인 절차 분리 |
| 2 | `code-analyzer` | 고정 소스 범위 → 코드 사실·call flow·MSC 입력 | 코드 리비전과 분석 범위 검증 필요 |
| 3 | `code-fix` | 승인된 결함/수정 범위 → 수정 및 자체 확인 | 수정·shelve·submit은 다른 단계 |
| 4 | `l1-fix-workflow` | 요청/기존 Work → 워크플로우 진행·재개·분석 연결 | 공개 패키지 존재가 설치 승인 아님 |
| 5 | `work-ledger-kernel` | Work/Evidence/결정 → 상태·이력·Resume/Transfer | Work ID·원장 정본과 기존 Schema 보존 |
| 6 | `hld-composer` | 코드 분석/SRS/HLD → 통합·목표 HLD | 현재 코드 사실과 목표 설계 분리 |
| 7 | `doc-converter` | MD/HTML·시나리오 IR → 문서/MSC/PUML/SVG | participant 및 scenario trace 계약 재사용 |
| 8 | `hld-code-compare` | 설계와 소스 근거 → 차이(gap) 보고서 | 증거 유형별 신뢰 수준 분리 |
| 9 | `hld-code-implement` | 승인된 설계 차이 → 변경 후보·구현 기록 | 구현 승인/검증/최종화 구분 |
| 10 | `l1-github` | 저장소/브랜치/PR → Git 근거·안전 작업 | 실제 저장소 역할·Checkout·권한 확인 |
| 11 | `p4-code-owner` | 파일/P4 변경 이력 → 수정자·CL 근거 | 과거 수정자와 공식 module owner 구별 |
| 12 | `l1-cl2git-merge` | P4 CL·대상 Open PR → 충돌 분석/병합 보조 | 일반 이관 도구 아님; 버전 표기 확인 필요 |
| 13 | `l1-sam-fixer` | LOC/MCD 입력 → 분석·수정 후보·검증 기록 | 기존 provider 연동 최신성 확인 |
| 14 | `skill-updater` | 승인 ZIP·정책 → 격리 업데이트·시험·롤백 | 예약/Job 실행을 직접 소유하지 않음 |
| 15 | `skillsilent` | 실행 정책 → 허용/차단 게이트 | 독립 ZIP·호스트 설치 미확인 |
| 16 | `job-list` | 승인된 Job/Profile → one-shot 실행·결과 | Dispatcher/Worker·현재 Job 및 설치 상태 별도 확인 |
| 17 | `autotask-builder` | 일정/Task 설정 → OS 예약작업 정의/관리 | Job-list queue와 독립 |
| 18 | `l1-cleanup` | 정리 대상/정책 → 점검·계획·선택적 격리/복구 | 삭제·purge 별도 승인 |
| 별도 | `l1-knowledge-updater` | 사내 GPT 협업으로 팀 지식 스킬 업데이트 지원 | **사내 전용**. 외부 패키지 정적 감사 대상에서 분리 |

위 표는 **스킬별 책임 소개**이며 새 CLI/API/필드 지원을 보증하지 않는다.

## 2. 작업별 우선 재사용 경로

| 요청 목적 | 먼저 검토할 기존 스킬 |
|---|---|
| 결함·로그 분석 | `issue-analyzer` → `code-analyzer` → 필요 시 `code-fix` |
| 현재 브랜치 코드 분석 및 **AS-IS MSC** | `l1-github`/P4 근거 → `code-analyzer` → `doc-converter` |
| 목표 HLD·설계·실제 구현 차이 | `hld-composer` → `hld-code-compare` → 승인된 `hld-code-implement` |
| Work 이력/문서/재개 | `l1-fix-workflow` + `work-ledger-kernel` |
| P4 CL 관련 Git PR 충돌 | `l1-cl2git-merge` + `l1-github` |
| 예약/잡/스킬 설치 | `autotask-builder`(예약) / `job-list`(Job) / `skill-updater`(갱신) 구분 |
| SAM LOC/MCD | `l1-sam-fixer` |
| 문서·산출물 정리 | `l1-cleanup`의 조회 및 계획부터 |
| 사내 팀 지식 갱신 | 사내 `l1-knowledge-updater`의 실제 설치 계약 확인 |

### 브랜치별 MSC 해석

- 독립적인 **현재 코드 흐름 분석**을 Work 유형 `CODE_ANALYSIS`, 산출물 유형 `MSC_AS_IS`로 구분하는 방향은 **설계 후보**이며, 현재 설치본에 구현 완료됐다고 주장하지 않는다.
- ISSUE Work 안에서 생성한 AS-IS MSC는 Work 목적을 ISSUE로 유지하고 산출물 종류만 분리한다.
- 브랜치명은 변경 가능하므로 **실제 코드 분석 기준 Git 전체 Commit SHA** 또는 P4의 해당 file revision/haveRev 근거를 유지한다.
- `MSC_TO_BE`는 구현 전 목표 설계이며 AS-IS 코드 사실로 자동 승격하지 않는다.
- 기존 Kernel Work 문서 탐색과 인덱스·원장 기능을 중복 개발하지 않는다.

## 3. 검증 상태와 한계

- 2026-11-12 점검 당시 관리 대상 18개 가운데 **17개 ZIP의 파일·정적 패키지 문서 검토**, `skillsilent` 독립 ZIP 미확인이 기록돼 있다. 이는 사내 미설치 판정이 아니다.
- 기존 기록의 예시 패키지: `l1-fix-workflow_v1_6_67_1110.zip`, `work-ledger-kernel_v0_7_37_1103.zip`, `l1-github_v0_3_56_1110.zip`, `job-list_v0_4_36_1112.zip`. **현재 설치 버전 또는 최신 배포 승인본으로 간주하지 않는다.**
- 사내 Work·Git/P4 root/owner·MCP tool ID·Job 및 Provider 실제 입력 검증은 관련 작업의 실측 결과로 따로 판단한다.
- 스킬 이름만으로 새 기능을 만든다고 판단하지 않는다. **REUSE → CONNECT → 실제 결함이 입증된 경우 최소 EXTEND → DEFER/BLOCKED** 순으로 검토한다.
- 코드 원본·내부 로그·고객자료·토큰·개인키·사내 작업 결과를 이 공개 문서에 추가하지 않는다.

## 4. 상세 기준 자료

**공통 스킬 정본**은 별도 PRIVATE 협업 저장소에서 관리 중이다. 해당 저장소는 권한이 있는 사용자만 열 수 있으며, 이 공개 문서는 그 내용을 그대로 복제하지 않는다.

- PRIVATE 기능 카탈로그: `wonhwipark/CoWork-Skill-Collab` / `main` / `collab/knowledge/SKILL_CAPABILITY_CATALOG.md`
- PRIVATE 패키지 정적 점검: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/SKILL_18_PACKAGE_AUDIT_20261112.md`
- PRIVATE 스킬 선택 절차: `collab/ops/CONTRACTS/SKILL_DISCOVERY_AND_REUSE_V1.md`
- PRIVATE 최신 상태: `collab/projects/COWORK-SKILL-DISCOVERY-20261112-001/CURRENT.md`
- 공개 패키지 저장소: `wonhwipark/L1Work`의 승인된 해당 ZIP 경로

이 인계 문서는 **사용자가 요청한 비민감 기능 요약**이다. PRIVATE의 작업별 리뷰·영수증·운영 기록, 실제 스킬 코드, 사내 자료는 복제하지 않았다.

## 5. 사내 GPT에 전달할 간단한 요청

> 이 문서의 스킬 기능 목록을 작업 후보 발견용으로 사용해줘. 내가 요청하는 업무를 기준으로 기존 스킬을 REUSE / CONNECT / 최소 EXTEND / 추가 확인으로 나누고, 필요한 경우 사내 설치된 SKILL.md와 실제 저장소·코드 리비전을 읽기 전용으로 검증해줘. 사내 정보는 외부로 내보내지 말고, 새 Job 실행·코드 수정·스킬 설치는 별도 승인 없이 진행하지 마.
