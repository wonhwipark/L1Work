# 사내 LLM/Agent 원샷 구현 요청 — PLUS 독립 SDM Parser의 MCP 연동

## 0. 요청 목적과 현재 사실

당신은 사내 개발 환경과 MCP 서버/Agent 연결 구조를 확인할 수 있는 개발·검증 담당자다. **진단만 하지 말고, 권한이 허용되는 범위에서 구현→테스트→결과 보고까지 한 번에 진행**하라. 중간에 질문을 반복하지 말고, 외부 승인이나 접근 권한이 필요한 작업만 명확히 구분하라.

- 대상: 개인 스킬 `issue-analyzer v0.11.48`, 사내 그룹 스킬 `l1sw-dev-log-analyzer-plus`(이하 PLUS), 사내 개인 MCP 프로젝트 `whpark-mcp` 등 **실제 확인되는** 실행 인프라.
- 문제: `issue-analyzer v0.11.48`의 `plus-standalone` backend는 **검증된 독립 CLI 계약만 지원**한다. `references/PLUS_STANDALONE_CONTRACT.md`와 `scripts/plus_standalone_adapter.py`의 `interface_kind=cli` 제약상 MCP 인터페이스를 설정값만 바꿔 연결할 수 없다.
- 직전 사내 검증: Q1~Q8이 모두 `3(NOT TESTED)`. 이는 **MCP 미지원 확정 또는 Parser 자체 불가능을 의미하지 않는다**. 실행 경로와 독립 Parser 계약을 확인해야 한다.
- 목표: `PLUS의 SDM→TXT 단독 변환` 기능만 **권한이 승인된 MCP 인터페이스**로 실행하고, 산출 TXT를 `issue-analyzer`의 기존 TXT 분석 경로에 전달한다.
- 핵심: PLUS의 **전체 분석 orchestration을 실행하지 않는다**. TXT 직입력은 기존 동작을 그대로 유지한다.
- 이 작업은 MSC 접근 권한 문제와 독립적이다. `l1-fix-workflow`, `work-ledger-kernel`, 기타 불필요한 스킬은 수정하지 않는다.

## 1. 실행 원칙 / 금지

1. **최초 확인:** 실제 설치본 버전, MCP 서버/Agent가 접근할 수 있는 MCP 도구 목록, PLUS 내부의 *허용된* standalone 파서 인터페이스(기존 MCP/CLI/안정된 API)와 실행 주체를 실물 기준으로 확인한다.
2. 명령어·옵션·MCP 도구명·Python 함수·MCP provider 스키마·Manifest/Symbol 형식을 **추정하거나 만들어 넣지 않는다**. 아래 도구명/JSON은 설계 후보일 뿐, 기존 인터페이스라는 뜻이 아니다.
3. PLUS 원본 또는 보호된 그룹 스킬을 무단 수정·복제·역공학적 재구현하지 않는다. 그룹 스킬의 안정된 parser 호출이 공식적으로 제공되지 않으면 소유자 승인·계약 확보를 blocker로 남긴다.
4. 사내 MCP 권한/allowlist/등록 정책을 우회하지 않는다. 권한이 허용되는 개인 MCP wrapper 변경만 수행한다. 보호된 서버 등록/배포·운영 재시작은 승인 없는 실행을 금한다.
5. SDM 원본·사내 소스·Symbol·Manifest·토큰·내부 경로를 외부로 전송하지 않는다. 테스트 자료는 승인된 사내 fixture만 사용하며, 최종 답변에는 내부 비밀값/원문 로그를 포함하지 않는다.
6. 임의 `shell=True`, 동적 커맨드, 플래그 추측, 외부 임의 경로 실행, 무단 다운로드, PLUS 전체 분석으로 자동 fallback을 금한다.
7. 구현을 확인할 수 없는 부분은 `NOT TESTED` 또는 정확한 blocker로 기록한다. 스킬 문구 수정이나 Mock PASS를 실제 사내 E2E PASS로 보고하지 않는다.

## 2. S0 — 현행 실행 경로 조사(읽기 전용)

A. `issue-analyzer` 설치본과 ZIP(v0.11.48 또는 실제 최신)의 다음 구성요소를 확인한다.
- `scripts/plus_standalone_adapter.py`
- `scripts/sdm_backend.py`
- `scripts/ia_pipeline.py` (`analyze`, `standalone-convert`, `sdm-config-set`, `sdm-config-show`)
- `references/PLUS_STANDALONE_CONTRACT.md`
- 기존 TXT direct-ingestion 및 `scripts/low_spec_route.py`

B. PLUS의 승인된 소스·설정·실행부를 조사해 다음을 **근거와 함께 식별**한다.
- SDM→TXT 변환만 하는 진입점이 정말 있는가?
- 현재 Agent가 호출 가능한 MCP 도구로 이미 공개되어 있는가?
- 독립 CLI가 있는가? 있다면 현재 서버 또는 사용자 PC에서 실행 가능한가?
- 지원되는 인자와 실제 출력(TXT 경로, 인코딩, 종료 상태)은 무엇인가?
- Manifest/Symbol 등 필수 의존성은 무엇이고, 인식 실패는 어떻게 구분되는가?
- Parser가 돌아가는 호스트와 `issue-analyzer`가 TXT를 읽을 호스트의 파일시스템은 같은가?
- 현재 MCP server/provider 등록·권한·execution allowlist·실행 프로세스 및 도구 공개 방식은 무엇인가?
- Windows/Linux 중 실제로 테스트 가능한 플랫폼은 무엇인가?

C. 경로 선정. 반드시 아래 중 **실제 근거가 있는 경로 하나**를 선택한다.
- **A / 이미 사용 가능한 MCP 도구 존재:** 기존 도구를 재사용. 불필요하게 새 MCP 도구를 만들지 않는다.
- **B / 승인된 standalone CLI/API 존재, MCP 도구 없음:** 개인 MCP의 허용된 확장 지점에 좁은 `SDM→TXT` 도구를 새로 등록한다. CLI/API의 정확한 인터페이스만 호출한다.
- **C / 파서는 있으나 MCP 서버에서 호출 불가:** Agent 실행 환경의 접근성/등록/파일 공유 문제를 파악한다. 승인 가능한 구성을 제시하고 권한 범위에서만 변경한다.
- **D / 독립 파서 계약이 없거나 권한 없음:** 스킬 전체 분석을 대신 돌리지 말고 `NEEDS_PARSER_CONTRACT` 또는 `NOT_AUTHORIZED`로 중단한다.

## 3. S1 — 사내 MCP 도구 계약 수립

호출 인터페이스가 실물로 확인되면 다음 **논리 계약**을 기존 MCP 시스템의 실제 스키마에 맞춰 구현/매핑한다.

### Capability 조회(기존 도구 재사용 가능)
- 목적: Parser 등록/버전/지원 OS, standalone 지원 여부, Manifest/Symbol 필요 여부, 실행 권한, 동일 호스트 경로 접근 가능 여부를 안전하게 반환.
- 실패 시 정확히 `PARSER_UNAVAILABLE`, `NOT_AUTHORIZED`, `NEEDS_PARSER_CONTRACT`, `OS_UNSUPPORTED` 등으로 구분.

### 독립 변환 Tool(이름 예시: `run_plus_sdm_to_txt` — 실제 이름은 기존 명명 규칙 준수)
**입력 필드 후보:**
- `input_path` : 승인된 SDM 파일 경로
- `output_dir` : 허용된 작업 디렉터리(원본과 구별)
- `manifest_ref`, `symbol_ref` : 필요할 때만 허용된 사내 참조
- `timeout_seconds` : 사내 정책에 따른 범위
- `request_id` : 재시도 시 중복 실행/결과 추적 식별자(선택)

**성공 응답 논리 필드:**
- `ok=true`, `status=FINAL_COMPLETE` 또는 실제 표준 성공 상태
- `txt_path` (분석기가 읽을 수 있는 동일 호스트/공유 스토리지 경로)
- `parser_id`, `parser_version`, `elapsed_ms`
- `output_size`, `output_sha256`(가능하면)
- `analysis_invoked=false`, `full_plus_analysis_invoked=false`

**실패 응답 논리 필드:**
- `ok=false`, `status`, `error_code`, `next_action`
- 대표 오류: `NEEDS_PARSER_CONTRACT`, `NOT_AUTHORIZED`, `PARSER_UNAVAILABLE`, `DEPENDENCY_MISSING`, `PARSER_CONTRACT_MISMATCH`, `OS_UNSUPPORTED`, `PARSER_FAILED`, `TIMEOUT`, `TXT_OUTPUT_NOT_FOUND`, `TXT_OUTPUT_INVALID`, `SOURCE_NOT_FOUND`.
- 원문 stdout/stderr, 파일 내용, 토큰, 절대경로 등 민감한 상세 출력은 기본 응답에 넣지 않는다.

### 안전·파일 경계
- 서버 측 입력 파일·실제 확장자/형식 및 읽기 권한 검사, 승인된 root 경로 allowlist, 상대경로/심볼릭 링크 탈출 차단, 출력 디렉터리 정책을 준수한다.
- 실제 Parser 실행은 argv 기반의 승인된 호출만 사용; arbitrary command 실행형 MCP tool을 만들지 않는다.
- SDM 원본 파일은 읽기 전용으로 취급하고 변환 전후 해시가 같음을 검증한다.
- TXT는 파일 존재/0B/인코딩/내용 형식/허용 경로 검사를 통과해야 성공 처리한다.
- **원본 SDM/생성 TXT를 MCP 응답의 대용량 본문으로 보내지 않는다.** 경로 공유 불가능한 교차 호스트 환경은 승인된 파일 전달 수단을 별도 식별하고, 없으면 blocker로 명시한다.
- 장시간 작업이면 기존 MCP 작업 상태 조회·job ID 방식을 재사용하고, 타임아웃·실패·재시도 중복에 대한 종료 정책을 마련한다.

## 4. S2 — issue-analyzer 연결 방식 구현

**우선 순위 1: 최소 변경 Agent 오케스트레이션**
- Agent가 승인된 MCP standalone 도구를 호출 → 검증된 TXT 파일 경로 획득 → 기존 `issue-analyzer analyze --input <TXT>` 호출.
- 이 방식은 `issue-analyzer` Python CLI가 직접 MCP client가 아니어도 동작 가능하다.
- 사용자에게는 자연어 요청 한 번으로 끝나도록 기존 스킬 라우팅 또는 MCP dispatch 설정에서 연결한다.
- TXT 입력 요청 시에는 MCP/parser 호출이 0회여야 한다.

**우선 순위 2: 단일 issue-analyzer 파이프라인 필요 시**
- 실제 MCP client 호출 수단이 검증된 경우에만 전용 `plus-mcp` backend(명칭 후보)를 `issue-analyzer`에 **최소 변경**으로 추가한다.
- 현재 `plus-standalone`은 CLI 전용이므로 `interface_kind=mcp`만 넣거나 CLI 계약을 재사용해 **MCP가 호출되는 척하지 않는다**.
- `sdm_backend.py`의 OS별 선택값·설정, `ia_pipeline.py`의 `analyze`/`standalone-convert` 진입, 변환 상태·출력 검증, low-spec 라우터까지 관련 위치를 확인해 실제 연결한다.
- 기존 `external/sdm-parser` 기본값 및 `plus-standalone` CLI 경로는 변경하지 않는다. PLUS MCP 사용은 명시적인 opt-in으로 설정하고 자동 fallback을 금지한다.
- MCP 실행은 실제 Provider/Agent에 등록된 typed tool call로 수행하며, MCP 세션을 사용할 수 없는 subprocess 안에서 가상의 MCP 라이브러리나 미등록 tool을 호출하지 않는다.

선정한 구현 방식·변경된 파일·선정 이유를 기록한다. **우선 순위 1로 목표가 완전히 달성되면 불필요한 우선 순위 2 구현은 하지 않는다.**

## 5. S3 — 사내 테스트 및 증거 확보

합성/mock과 실제 사내 테스트를 반드시 구분해서 기록한다.

1. MCP 도구 discovery/capability 조회 및 권한 검사 PASS.
2. 승인된 합성 SDM fixture로 **MCP standalone SDM→TXT** 실제 호출 PASS.
3. 생성된 TXT 파일 접근·무결성·인코딩 검증 PASS.
4. 동일 TXT를 `issue-analyzer`에 전달하여 분석 진입 PASS.
5. SDM 단일 요청 한 번으로 변환→분석까지 정상 라우팅 PASS.
6. 기존 TXT 직접 분석에서 Parser/MCP 호출 0회 PASS.
7. Parser 누락, 권한 거부, Manifest/Symbol 누락, 타임아웃, 빈/손상 TXT 시 **분석 미실행** PASS.
8. 원본 SDM 변환 전후 해시 동일, PLUS 전체 분석 호출 0회 PASS.
9. 실제 사용한 플랫폼 Linux/Windows 개별 결과를 PASS/FAIL/NOT TESTED로 구분.
10. 승인된 실로그가 접근 가능한 경우에만 사내 real SDM E2E 실시. 승인 fixture가 없다면 real E2E는 NOT TESTED.
11. `standalone 변환 시간`과 `TXT 분석 시간`을 별도 측정. PLUS 전체 분석 시간을 새로 측정하려고 전체 파이프라인을 실행하지 않는다.

## 6. S4 — 패키징/적용/롤백

- 기본 수정 범위: **허용된 개인 MCP 프로젝트 설정·도구** 및 연결에 필요한 **issue-analyzer** 범위로 한정. PLUS 그룹 소스나 보호된 MCP core 수정 금지.
- 변경 전 설정/코드 버전·SHA 및 백업을 확보한다. MCP 서버가 보호된 운영 환경이면 실제 배포·재시작 전 승인 상태를 보고하고, 허가된 로컬 후보 패키지/패치까지만 만든다.
- 사용자 로컬 환경에서 설치할 수 있는 변경 파일 또는 패치, 등록에 필요한 설정, 짧은 실행 가이드, rollback 절차를 제공한다.
- `issue-analyzer`를 변경하면 실제 현행 버전을 기준으로 패키지 버전을 증가시킨다(예: v0.11.49 후보, **예시일 뿐**). 배포 ZIP 이름에 날짜 suffix를 붙이지 않는다.
- 연결 실패 시 기존 `sdm-parser`/기존 TXT 분석 설정을 복원할 수 있게 한다. 입력 로그·과거 작업 결과를 삭제하지 않는다.

## 7. 결과 답변 (진단 말고 실제 구현 결과)

긴 주관식 설명을 피하고 **숫자 + 짧은 상태** 중심으로 답하라. 중간에는 권한 승인 필요 시에만 질문하라.

```
PATH=<A|B|C|D>
Q1=<1|2|3|4>  # standalone Parser 실제 엔트리포인트 확인
Q2=<1|2|3|4>  # MCP 도구 공개/등록 가능 및 권한 확인
Q3=<1|2|3|4>  # MCP 실제 standalone 변환
Q4=<1|2|3|4>  # TXT 산출·공유 경로/무결성
Q5=<1|2|3|4>  # SDM→TXT→issue-analyzer 분석 E2E
Q6=<1|2|3|4>  # 기존 TXT parser 호출 0회
Q7=<1|2|3|4>  # 실패 시 분석 중단·원본 불변
Q8=<1|2|3|4>  # PLUS 전체 분석 실행 0회
Q9=<1|2|3|4>  # Linux 실환경
Q10=<1|2|3|4> # Windows 실환경
CHANGED=<변경 파일 수 또는 0>
BLOCKER=<NONE|NEEDS_PARSER_CONTRACT|NOT_AUTHORIZED|MCP_TOOL_UNAVAILABLE|MCP_REGISTRATION_REQUIRED|FILE_PATH_NOT_SHARED|DEPENDENCY_MISSING|OS_UNSUPPORTED|OTHER>
NEXT=<한 줄, 필요 없으면 NONE>
```

각 Q 값: `1=PASS / 2=FAIL / 3=NOT TESTED / 4=권한·자료 차단`.

**별도 내부 산출물:** 변경파일 목록, MCP tool 명칭/입출력 스키마, 테스트 로그의 비밀값 없는 요약, 적용/롤백 방법, 실제 변경 파일/패키지. 실물 증거가 없으면 구현 완료로 보고하지 말 것.

## 8. 사용자 관점 최종 동작 확인

자연어 요청(기존 Agent UX 준수):

- `issue-analyzer로 이 SDM 로그 분석해줘` → MCP standalone Parser → TXT 검증 → 기존 issue-analyzer 분석.
- `이 SDM을 TXT로만 변환해줘` → MCP Parser만 호출, 분석은 미실행.
- `이 TXT 로그 분석해줘` → Parser와 MCP 변환 도구 모두 호출하지 않고 기존 분석.

**완료 조건:** 단순 `MCP 등록 가능`이 아니라, 승인된 환경에서 `실제 MCP 변환 성공 + 생성 TXT 분석기 전달 성공 + 기존 TXT 회귀 PASS`를 입증해야 한다. 가능한 작업을 이번 실행에서 끝까지 처리하라.
