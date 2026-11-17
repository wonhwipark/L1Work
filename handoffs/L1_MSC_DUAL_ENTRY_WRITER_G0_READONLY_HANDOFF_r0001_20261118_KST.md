# L1 MSC 두 진입 — 업무 GPT / Linux Agent writer G0 읽기 전용 확인

- 기준: 2026-11-18 KST
- 목적: 기존 스킬을 바꾸지 않고 `l1-knowledge-updater`, `work-ledger-kernel`, `doc-converter`, `l1-fix-workflow`의 실제 설치·호출·writer 계약을 확인
- 범위: **READ_ONLY G0**. 회사 코드/로그/고객자료/토큰/인증/상세 MSC 본문·절대 경로는 외부 전달 금지. 실제 Knowledge 게시, Work 생성, 패키지 설치, Job/LLM 호출, 새로운 승인·서명·READY·PUBLIC 게시 금지.

## 확인할 대상

1. 실제 등록된 스킬 이름·버전·현재 실행 진입점과 설치 확인 여부. 미설치와 원문 조회 불가를 구분.
2. Updater 직접 Procedure/Feature 지식 작성과 기존 Workflow 이슈 문서 작성이 서로 필수 호출 없이 동작하는 계약인지 확인. 순수 지식 편집의 Work ID 요구 여부를 실제 스킬 원문·실제 입력 검사로 대조.
3. Updater 개인 Workspace writer의 기존 문서 ID/path/section marker/Preview-diff/CAS·수동 수정 보호/승인·readback 여부. 팀 group writer의 별도 게시·승인·revision 검증과 기존 personal writer 소유권을 구분.
4. Kernel Work Evidence로 `render_output`·`utility`의 HTML/MSC_VIEW.md 등록 가능 여부, `artifact_publish_map.json`의 `published_path` 반환 계약과 상대 링크 리매핑/선택 표기 현황. 경로·SHA는 실제 값 외부 복사 금지, 예/아니오/미확인만 반환.
5. `doc-converter` 두 action `msc-package`, `msc-scenario-build`: `--view-mode ISSUE`의 기본 출력, `PROCEDURE_FEATURE` 기본 HTML, `--html-viewer` 등록 여부를 설치본 parser/managed policy에서 조회. 개발 후보의 기능을 설치된 현재 버전으로 추정하지 말 것.
6. 최종 게시 후 HTML 파일 링크/브라우저 페이지 URL의 구분. 마커 부재·중복·수동 편집 충돌, stale revision, 부분 실패 시 Preview/HOLD 지원 여부. 실제 수정·write 시험 없이 원문 계약만 읽기.

## 회신 양식 (숫자만)

각 코드: `1=원문 확인/지원`, `2=원문 확인/미지원`, `3=조회 불가·미확인`, `4=부분 지원/추가 조건`. 출력은 다음 한 줄만 작성:

`A B C D E F G H I J`

- A: Updater 설치·원문 조회 가능
- B: 순수 지식 작성에 Work ID 강제 없음
- C: Updater 개인 writer의 단일 소유·Preview/충돌 보존
- D: 그룹 writer의 승인·CAS/readback 분리
- E: Kernel HTML Evidence 등록·published_path 매핑
- F: Work-root MSC 안내에 게시 HTML 링크 직접 연결
- G: 상세 MSC_VIEW.md의 원본 상대 링크 remap 제공
- H: Converter ISSUE HTML opt-in(parser·policy 양쪽)
- I: 승인된 업무 호스트에서 실제 HTML 브라우저 접근 경로 파악 가능
- J: 변경 없이 기존 writer 기반 합성 E3를 진행 가능한 계약 존재

확인 실패 시 누락 자료를 10단어 이내로 선택적으로 부연. 추정 결과를 `1`로 올리지 말 것. 본 요청은 코드 수정/설치/Knowledge 반영을 허가하지 않음.

## 후속 연결 규칙

G0 확인 결과와 유효한 코드·게시 승인 범위를 별도로 대조. 미충족 항목만 기존 writer/문서 계약에 맞춰 최소 보완. Work 루트 안내 MD의 링크와 Converter 상세 원본 MD의 링크를 별도로 시험하고, 원본 bytes/hash는 변조하지 않음. 같은 분석·모델/Job 재실행 대신 실패한 링크만 회복.
