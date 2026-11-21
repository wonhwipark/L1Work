# 업무 GPT 원샷 인계 r0003 — Viewer Write × 정식 형태의 Workflow/Kernel 전체 스킬 개발 패키지

- 작성: 2026-11-21 KST
- Work: `L1-WORKSPACE-RAG-20261111-001`. 기존 업무 Linux Work·문서·결정·Evidence를 재사용. 같은 목적의 새 Work·원장/DB 생성 금지.
- **정확한 인계 위치:** GitHub PUBLIC `wonhwipark/L1Work`, branch `main`, 상대 경로 `handoffs/L1_WORKSPACE_VIEWER_WRITE_WORKFLOW_KERNEL_FULL_SKILLS_HANDOFF_r0003_20261121_KST.md`
- **기존 r0002 HO 보완:** `handoffs/L1_WORKSPACE_VIEWER_WRITE_V020_WORKFLOW_KERNEL_E2E_ONESHOT_HANDOFF_r0002_20261121_KST.md`. 요구/보안/수락 조건은 유지. 최신 r0003는 **두 스킬 전체 패키지 입력이 실제 게시됨**을 반영하고 설치 판정 이전의 시험을 명시.
- **상태:** `PUBLIC_DEV_FULL_ZIPS_DELIVERED=PASS_REMOTE_VERIFIED`. **Linux 사용·E2E·HOST_INSTALL=NOT_RUN**, `development_not_for_deployment`, 코드 독립 리뷰 NOT_RUN. 문서/ZIP 게시만으로 호스트 실행·신규 유료 모델·Job·키 생성·서비스 변경·Write ON 승인 아님.

## 1. 고정 입력·무결성

| 항목 | L1Work/main 루트의 정확한 파일 | bytes | SHA-256 |
|---|---|---:|---|
| **Workflow 신규 전체 ZIP** | `l1-fix-workflow_v1_6_75_1121.zip` | **832,039** | `fd337ee31e09c9f694146c9d159799ca7182af052c93121e73888a9ee367a0a1` |
| **Kernel 신규 전체 ZIP** | `work-ledger-kernel_v0_7_43_1121.zip` | **379,642** | `9866ff7164884b0fb346bd31d37dbdf2013b5e5910e5857f8e35075624cf92f1` |
| Viewer Read v0.1.2 | `l1-workspace-viewer-ui_v0_1_2_1121.zip` | 74,940 | `9be14c4c34c2a7d923d8b11c01fb0249d41e820861721f275001f0f7d499d9e3` |
| Viewer Write v0.2.0 | `l1-workspace-viewer-write-ui_v0_2_0_1121.zip` | 21,171 | `9f2df44348478eb44615bddef8f211645fa1c07ed71d43580b4fb324e376b6f9` |
| Viewer 환경설정 v0.3.0 | `l1-workspace-viewer-preferences_v0_3_0_1121.zip` | 20,661 | `228c60bada8a92591f7ae855dfabe206e018d9e59970cf2d1b773d4d00072812` |

- 신규 ZIP은 각각 공개 최신 기준 `l1-fix-workflow_v1_6_74_1119.zip` / `work-ledger-kernel_v0_7_42_1116.zip`의 **원격 SHA 고정 바이트**를 읽어 모든 기존 멤버의 압축 데이터와 기존 상대 경로를 보존하고 새 파일을 추가한 **완전한 ZIP**. 원본 ZIP 불변.
- 신규 두 ZIP에는 **VERSION, pyproject.toml, SKILL.md, README.md, .skill-release.json, MANIFEST_SHA256.json** 갱신과 소스·단위시험·설명 문서가 포함. Kernel CHANGELOG, Workflow RELEASE_NOTES 갱신.
- 원격 업로드 commit `fe869519e588a56e2282fbbd854cfed83bf8ad64`. Git blob Workflow `2a75b0ad3108a02e0374706b739b1b7973f17568`, Kernel `a8554d559b46d7292a4add98552c6821d55ac8af`. **재조회 Base64 bytes/size/SHA=PASS**, 기존 311/163개 원본 멤버 CRC+manifest 검사 및 신규 ZIP 전 멤버 검사 PASS.
- 신규 전체 ZIP은 소스 패치 ZIP과 다르며, **현재 업무 Linux에 적용한 설치 완료본이 아님**. 코드 원본 경로, 배포 권한/현장 설치본은 현장 G0에서 독립 확인.

## 2. 스킬 변경 내용 — Write owner 유지

**Workflow v1.6.75**:
- 추가: `l1_fix_workflow/viewer_write_route.py`, `tests/test_viewer_write_route_v1675.py`, `docs/VIEWER_WRITE_SAFE_CONNECT_V1.md`, `RELEASE_NOTES_v1_6_75.md`.
- 기존 Work/문서/원본 revision·SHA와 서버 canonical 결과를 비교해 Viewer 편집 의도를 라우팅하는 순수 함수 `resolve_work_edit`. 잘못된 Work, 비편집 문서, Knowledge owner, 임의 path/ID, stale revision 불일치 fail-closed. 별도 승인/Writer/Work 생성/원본 수정하지 않음.

**Kernel v0.7.43**:
- 추가: `work_ledger_kernel/viewer_write_guard.py`, `tests/test_viewer_write_guard_v0743.py`, `docs/VIEWER_WRITE_SAFE_CONNECT_V1.md`.
- `check_before_operation`: PREVIEW/DRAFT/COMMIT 서버 권한과 source revision 검증.
- `commit_once`: **호스트가 제공한 검증된 잠금·CAS/멱등 writer callback만 1회** 호출하고 영수증/new revision/SHA/readback을 비교. **실제 writer 구현/인증자/CSRF/ACL 보호를 제공하지 않음**. 호출자와 실제 writer가 재검증 책임 소유. WRITE_UNCERTAIN 자동 재시도 0.
- 기존 원장·Work ID/Evidence ID·기존 workflow/Kernel CLI 동작 불변. 테스트용 standalone helper를 서비스가 자동으로 쓰기 API로 호출한다고 가정하지 말 것.

## 3. 현장 원샷 실행 — 사용 중인 Linux 설치본을 우선

1. **G0 최신 확인:** 업무 GPT와 허용된 Linux Agent/실행 LLM이 설치된 실제 Workflow·Kernel·Viewer의 source/branch/revision·중복 설치/현재 활성 호출 경로, 사전 승인/유효 범위, 기존 writer의 Work document/Knowledge owner/CAS/잠금·멱등·readback·ACL/CSRF/편집 세션 구현을 확인. 발견된 현재 버전이 공개 ZIP과 다르면 덮어쓰지 말고 변경점·호환성을 대조.
2. **고정 ZIP 다운로드·검증·격리:** 위 두 전체 스킬 ZIP 및 Viewer 3 ZIP의 SHA-256/bytes/CRC/manifest, 경로/특수 파일/민감정보/필수 파일 확인. 기존 구버전·원본/DB/WAL/SHM·설정·사용 중인 Job/세션 보존. `development_not_for_deployment` 상태 그대로 운영에 자동 설치하지 말 것.
3. **연동:** 현장 Viewer의 인증/읽기 API와 `L1ViewerWriteHostAdapter`를 기존 서버 기준으로 연결. Work 문서는 기존 Workflow/Kernel writer 경로, Knowledge는 Updater owner. 실제 가능한 신뢰된 서버 코드를 통해 **서버 제공 canonical mapping**과 위 두 새 helper만 좁게 CONNECT. 미확인 API/새 DB/schema는 임의 구현 금지.
4. **추가 개발·시험:** 기존 설치본에 helper만 있다고 실동작이 되는 것이 아니므로 필요한 호스트 연결 코드/기존 writer 호출 지점을 확인하고 **입증된 GAP만 최소 변경**. 새 코드의 Workflow 8/8, Kernel 13/13, 교차 합성 4/4, staging 5/5 기존 시험 재실행 + **Workflow 전체 기존 suite, Kernel 전체 기존 suite, Viewer 3개 패키지 공존, 실제 호스트 writer CAS/revision/Evidence/readback** 시험. 실패 시 현장 owner 지침에 따라 rollback.
5. **인증/보안:** 동료 무로그인 Read Only 유지; [수정] 클릭 때만 편집용 인증. 서버 세션/CSRF/rate-limit/계정 보호·문서별 ACL을 초안/Diff/COMMIT/실 writer 직전 재검사. B1 canonical 경로/symlink·B2 검색/raw/download/cache/제목 보호·B3 MSC iframe origin/sandbox/CSP 및 EAuth, E3(localhost), E4(승인된 동료 2계정) 모두 실제 증거로 구분.
6. **MSC/환경설정:** canonical message/participant anchor가 없으면 구조적 MSC 저장 비활성, 부모 DOM에서 수정 요청 초안까지만. Converter B형 HTML/SVG는 파생물. 환경설정 v0.3.0의 숨김/표시는 사용자 화면 정책이며 권한 상승 수단이 아님.
7. **후속 판정·전달:** 안전 시험까지 수행하고 결과·호스트 설치 권한·rollback/원본 버전·변경 파일·증빙을 기존 **업무 Work**에 기록. 실제 운영 적용/WRITE ON은 유효 승인과 모든 보안/Writer/복구 게이트가 충족될 때만. 회사 제한 코드·MSC·로그/키를 L1Work/CoWork PUBLIC에 게시하지 말 것. 문서·ZIP 자체 게시로 이미 적용됐다고 보고하지 말 것.

## 4. 반드시 보고할 숫자 상태

`1 PASS / 2 FAIL / 3 NOT_RUN / 4 BLOCKED / 5 UNKNOWN`.

```text
WORKFLOW_FULL_ZIP_INPUT: [1~5]
KERNEL_FULL_ZIP_INPUT: [1~5]
LINUX_INSTALLED_G0: [1~5]
WORKFLOW_FULL_SUITE: [1~5]
KERNEL_FULL_SUITE: [1~5]
VIEWER_3PACK_UI_E2E: [1~5]
HOST_AUTH_CSRF_ACL: [1~5]
WORK_ID_CAS_WRITE_READBACK: [1~5]
MSC_ANCHOR: [1~5]
B1/B2/B3: [1~5] [1~5] [1~5]
E3/E4: [1~5] [1~5]
HOST_INSTALL/WRITE_ON: [1~5] [1~5]
실제 설치된 버전 / Work ID / 비민감 근거 위치: [...]
변경 요약 / 남은 차단 / 다음 한 행동: [...]
```

**실제 완료 기준:** 기존 Viewer UI에 두 스킬 helper가 존재한다는 사실만이 아니라 **Viewer Write → 해당 Work의 기존 Workflow/Kernel/검증된 writer → 원본 이력 보존/새 revision → readback → Viewer 재조회**를 현장 인증/권한·CAS와 함께 증명. 패키지 검증 자체를 E2E로 승격하지 말 것.
