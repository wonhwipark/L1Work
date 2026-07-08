당신은 스킬 구현가다. 목적: issue-analyzer manifest 보강 스크립트
manifest_augment.py 를 구현한다 (v0.4). 설계는 이미 승인됐다.
아래 확정 사항을 어기지 말 것. 이 제약 밖의 창의적 변형 금지.

[설계 확정 — 변경 금지]
Q1. regex 생성: full msg_symbol 전체를 그대로 사용. 축약형 생성 금지.
    변환은 정규식 특수문자 escape + 앞뒤 \[ \] 래핑만.
    (예: L1C_L1C_..._IND → \[L1C_L1C_..._IND\])
Q2. fragment 귀속: msg_symbol 첫 키워드 기반 분류.
    L1C_L1C_*→channel / L1C_L2_*→front / L1C_PHY_*→channel /
    RSM_*→common / NR_*·LTE_*→proc / MEAS_*→meas
    위 어디에도 안 맞으면 대폴백 = common.json (고정).
Q3. 중복 판정: 문자열 비교만. 정규식 동치 판정 금지.
    - 정확 일치(동일 regex 존재) → 제외
    - 앞부분 포함(기존 regex가 신규를 문자열로 포함) → 제외
    - 그 외 → 신규 후보 유지
Q4. 승인 UI: numbered list 제시 후 사용자 입력 검증.
    - 유효: 존재하는 번호의 조합 / 공백(=전체 기각)
    - 무효: 범위 밖 번호·중복 번호·비정수 → 재입력 요청
    - 미선택 항목 = 기각
Q5. 기존 중복 자동 조회: 각 fragment.json을 읽어 기존 regex 목록을
    추출하고 Q3 규칙으로 신규 후보와 대조. 수동 조회 금지.

[불변 원칙 — 위반 금지]
- regex를 임의 생성하지 않는다. 5.2 msg_symbol 근거 있는 것만 후보.
- _meta.json 수정 금지. output_suffix "_l1sw" 변경 금지.
- 기존 l1sw 유래 regex 삭제/변경 금지. append만.
- python (not python3). ASCII-only 소스.

[입력 계약 — 프롬프트1에서 확정됨]
- 5.2 structure.json 위치: {code_map}/{file_group}/structure_<ts>_focused.json
- 대상: ipc[] 배열 중 role이 "input" 또는 "output" 인 항목의 msg_symbol
- v0.9.8 미만(msg_symbol 필드 없음): SKIP + 경고 후 계속

구현 요구사항:
1. manifest_augment.py 단일 파일.
   인자: --code-map <경로> --manifest <issue-analyzer/manifest 경로>
   옵션: --dry-run (append 없이 후보 리스트만 출력)
2. 실행 흐름:
   (a) code_map 하위 structure_*_focused.json 전부 스캔
   (b) role input/output msg_symbol 수집
   (c) Q2로 fragment 귀속 분류
   (d) Q5로 기존 fragment.json 읽어 Q3 중복 제거
   (e) Q4 승인 UI: numbered 표 출력 → 사용자 입력 대기
   (f) 채택분만 해당 fragment.json에 append
   (g) manifest/_preserve.md 에 이력 기록
       (일자 / 소스 code_map 버전 / file_group / 채택 개수)
3. _preserve.md 없으면 생성, 있으면 append.
4. 모든 파일 쓰기 전 백업(.bak) 생성.

먼저 전체 코드를 제시하고, 그 아래에:
- 사용법 5줄 (실제 명령어 예시)
- 이 스크립트가 건드리는 파일 목록
- 한계/주의 3줄
을 붙인다. 구현 후 사용자 검토를 받는다 (바로 배포 금지).
