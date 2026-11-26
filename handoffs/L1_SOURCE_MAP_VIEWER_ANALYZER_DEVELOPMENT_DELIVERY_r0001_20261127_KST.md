# Source Map — Viewer v0.5.8 / Code Analyzer v0.15.7 개발 후보 통합 인계
- 기준일: 2026-11-27 KST
- Work: L1-WORKSPACE-RAG-20261111-001
- 대상 저장소: wonhwipark/L1Work, branch main
- 상태: development_not_for_deployment / POSTED_REMOTE_VERIFIED (두 ZIP)
- 독립 리뷰: SKIP_USER_DIRECTIVE. 운영 설치·배포·Job·팀 지식 게시 승인 아님. 기존 활성본 유지.

## 1. 패키지 및 고정 원본
| 대상 | 기존 원본 | 신규 ZIP | 크기(bytes) | 신규 SHA-256 | 게시 commit |
|---|---|---|---:|---|---|
| Viewer | v0.5.7 | [l1-workspace-viewer-wiki-integrated_v0_5_8_1127.zip](../l1-workspace-viewer-wiki-integrated_v0_5_8_1127.zip) | 301164 | 5d7935edba33bf062d167c95f3a44c620c683c33accc9c7aadacb69561fa73de | e80cb844d4409b8b60ca212d2822bd91f1692891 |
| Code Analyzer | v0.15.6 | [code-analyzer_v0_15_7_1127.zip](../code-analyzer_v0_15_7_1127.zip) | 627385 | 6a11cb8685c46d1ac22a1465968193a72708ca90bcfcf453b371c869abdfbeab | d015c6c5c7d7e37ee93e3760ca3022cc48a0a3b8 |

기준 main commit 7d2d59e4b23547598152850439291e84eb782025. 원본 ZIP SHA-256: Viewer 4a7a7ce742106cebbb4192c250a716ec303ac223ad31fb9673dfe61cb8332ddd; Analyzer bf1f369aed47e75c38fad3061041e720d5497953b0d90bcf4dc2fbf0d97b69ef. 기존 ZIP 보존. 신규 ZIP의 실제 원격 bytes 재조회 후 해시 일치. CRC·경로 및 manifest 전수 확인. 변경 파일 외 기존 원본 bytes 유지(Viewer 37개, Analyzer 214개). Viewer 변경된 파일은 재압축하여 크기가 감소했으며 내용 보존은 파일 해시로 확인.

## 2. 변경 범위
### Viewer
- index.html, assets/app.js: 독립 Source Map route, 메뉴, 기존 Knowledge 대상 route, 조회 취소 및 stale 응답 방지.
- assets/source-map.js/.css: 정확 심볼·Message ID 검색, Module/Build 필터, 최대 50개 결과, 증거·snapshot/revision/build, 상태(OK/EMPTY/PARTIAL/STALE/CONFLICT/DENIED/ERROR), 정적 후보와 실제 동작 순서 분리. 기존 Knowledge 링크는 권한 및 source/document revision, build 확인 가능한 경우에만 제공.
- fixtures/demo-data.js, adapters/adapter.js: 합성 데이터 및 읽기 adapter. 실제 업무 데이터 없음. 접근 불가 relation 제외. 기존 Knowledge·MSC·Recovery 문서와 storage schema 수정 없음.
- standalone-preview.html: 통합 자체 포함 미리보기, CSP inline 해시 재생성. tools/build_release.py, VERSION, README_INTEGRATED.md, manifest.sha256 및 개발 노트 갱신.
- tests/source-map.cjs, tests/source-map-fixture-tests.cjs 신규.

### Code Analyzer
- scripts/ca_core/probe_engine.py: 전처리 분기 frame, 이전 sibling 조건 배제, nested scope pop, 물리적 source anchor, line splice 후 lexical sanitize. #elif B → !A && B, #else → !A && !B, #endif 밖에는 해당 frame 조건 없음. 실제 build_activation은 UNKNOWN, 해석 불가 조건은 UNCERTAIN, 파일 budget 초과 aggregate는 partial.
- scripts/ca_core/patch_writer.py: condition_semantics_version=2 및 확정성 점검. 신규 incoming legacy 조건 근거 제외; 기존 legacy pending patch는 덮어쓰지 않고 명시적 오류로 보존, 새 scope에서 원본 재분석 필요.
- tests/test_compile_condition_v0157.py 신규. 버전/설치 메타 및 manifest 갱신.
- Analyzer는 근거 생성만 담당. Source Map 저장·지식 판단·게시, Viewer 렌더링 책임은 이 스킬에 추가하지 않음.

## 3. 실제 시험 및 미실행
| 항목 | 상태 | 범위 |
|---|---|---|
| Analyzer 기존 Outside 오류 재현 | PASS | 격리 harness에서 기존 원본 함수, 수정 후 해당 조건 사실 없음 |
| Analyzer 신규 집중시험 | 9 PASS / 1 SKIP | 격리 harness; 실제 패키지 CLI 1개 skip |
| C++ 전처리기 대조 | PASS | A/B 4조합 |
| Analyzer 기존 75 회귀·실제 CLI·설치 --home 자체점검 | NOT_RUN | 로컬 DNS/ZIP 반입 제한 |
| Viewer 신규 집중 Node 2개 프로그램 | PASS | 합성 분리 harness |
| Viewer Chromium 1280/360px | PASS | 합성 분리 화면: 검색/상세/Knowledge 링크/복귀/연속 조회/권한/키보드/overflow |
| Viewer 실제 ZIP fixture/adapter 보조검증 | PASS | JS parse, DemoTx 두 build 및 Knowledge 링크 |
| Viewer 기존 6개 Node 프로그램·통합 브라우저 | NOT_RUN | 원본 ZIP 로컬 반입 제한 |
| Viewer CRC/manifest/원격 SHA | PASS | 51/51, 50/50, 원격 전체 bytes |
| Analyzer CRC/manifest/원격 SHA | PASS | 224/224, 223/223, 원격 전체 bytes |
| 업무 실제 데이터·권한·호스트 adapter E2E | NOT_RUN | 업무 GPT 확인 필요 |

분리 harness의 PASS를 전체 설치본 검증으로 승격하지 않음. GitHub bytes 경로에서 원본 ZIP을 검증·수정·재패키징했으며 로컬 시험은 해당 신규 코드의 격리 실행에 한정.

## 4. 업무 GPT 실행 요청 (별도 승인 범위 내)
1. 위 두 ZIP의 실제 bytes SHA-256 대조. 기존 활성본과 백업 보존, 임시 디렉터리에서만 압축 해제·검증. Viewer standalone-preview.html 확인.
2. Analyzer 기존 75개 회귀 및 신규 test_compile_condition_v0157.py 전체, 실제 CLI와 임시 --home 설치 자체점검 수행. #if/#elif/#else/#endif, nested, splice, unsupported/UNCERTAIN, budget, legacy patch 거부 및 보존을 확인. 기존 legacy patch를 임의 삭제하지 않고 새 scope 재분석.
3. Viewer 기존 6개 Node 프로그램과 신규 2개, 전체 통합 브라우저 desktop/mobile 실행. Work/Knowledge/MSC/Recovery/검색/편집/도우미 회귀 확인.
4. 실제 기존 host adapter 및 권한·source snapshot/build/document revision 계약 확인. 합성 searchSourceMap/resolveSourceMapKnowledge는 UI 연결 예시이며 실제 API 존재를 주장하지 않음. 미확인 상태에서는 fail-closed. 업무 데이터는 업무 환경에만 유지.
5. 결과를 PASS/FAIL/SKIP/NOT_RUN, 원본/활성본 revision, Evidence 경로, 실제 연결 여부로 보고. 모두 통과 후에만 별도 운영 적용 판정. 추가 독립 리뷰 없음.

다음 한 행동: 업무 GPT에서 격리 전체 회귀 및 실제 adapter 계약 확인을 시작할 수 있도록 본 인계서와 두 ZIP을 전달.
