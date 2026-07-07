# 프롬프트 1 — sdm-parser 벤더링 + E2E 2차 검증 (A+B 통합)

- **대상 스킬**: issue-analyzer v0.3.1, sdm-parser (내부 설치본)
- **실행 시점**: 이번 내부 방문
- **세션**: 신규 세션 단독 실행 (프롬프트 2와 분리)
- **사용 버전**: issue-analyzer는 제공한 v0.3.1 그대로 / sdm-parser는 `~/.claude/skills/sdm-parser/` 내부 설치본

> 실행 전 확인: `~/.claude/skills/sdm-parser/` 가 실제로 설치돼 있어야 A1 복사가 가능하다. 없으면 A1에서 멈춘다.

---

## 붙여넣을 프롬프트 본문

```
당신은 스킬 통합·검증가다. 한 세션에서 2개 작업을 순서대로 수행한다:
[A] sdm-parser 벤더링(issue-analyzer로 편입) → [B] E2E 2차 검증(미확인 9개).
A가 끝나야 B로 넘어간다. 각 항목 PASS/FAIL/미확인 판정.
FAIL이어도 중단하지 말고 다음 항목으로 (원인 1줄 기록).

═══════════════════════════════
작업 A — sdm-parser를 issue-analyzer로 벤더링
목적: 외부 스킬 경로 의존 제거. issue-analyzer 단독으로 .sdm 변환 보유.
※ 코드는 그대로 복사. 재작성/포팅 하지 않는다.

A0 — 백업 (필수 선행)
- ~/.claude/skills/issue-analyzer/ 와 ~/.claude/skills/sdm-parser/ 를
  각각 통째로 백업(ZIP 또는 복사).
- 판정: 두 백업 존재 = PASS. 실패 시 여기서 멈추고 보고.

A1 — 복사
- ~/.claude/skills/sdm-parser/ 폴더 전체를
  issue-analyzer/vendor/sdm-parser/ 로 복사 (하위 파일 전부, .env 포함).
- 개별 파일명을 단정하지 말고 폴더 트리를 통째로 옮긴다.
- 판정: 원본과 vendor/sdm-parser/ 의 파일 개수·트리 일치 = PASS
        / 누락 시 FAIL(누락 파일명 나열).

A2 — 경로 참조 갱신
- issue-analyzer 내부에서 sdm-parser를 외부 경로
  (~/.claude/skills/sdm-parser 또는 상위 skills/sdm-parser)로
  참조하는 지점을 전부 검색.
- 내부 경로(vendor/sdm-parser)로 교체.
- 판정: 갱신 후 외부 경로 참조 0건 = PASS / 잔존 시 FAIL(file:line 전부).

A3 — 독립 실행 검증 (변환까지만)
- ~/.claude/skills/sdm-parser/ 를 sdm-parser_DISABLED/ 로 임시 리네임.
- 이 상태에서 issue-analyzer 변환을 FAIL 시리즈 중 "가장 작은 .sdm"으로 실행.
- [판정 기준은 변환(full text) 생성까지만]. Step B/추출은 여기서 보지 않는다.
- [타임아웃 규칙] 2분에 중단하지 말 것. 최대 10분 대기.
  경과시간(초)·.sdm 크기(MB)·DMConsole 기동~첫 출력 시간을 로그로 남긴다.
- [막히면] 10분 내 판단 안 서면 중단하고 현재까지 로그와 함께 사용자에게
  보고한다 (사용자가 수동 조절). 임의로 재시도 반복하지 말 것.
- 판정: 외부 스킬 없이 full text 생성 = PASS(변환 독립 성립)
        / 변환 실패 = FAIL(원인 1줄) / 10분 초과 = 미확인(진단 로그 첨부).
- 종료 후 반드시 sdm-parser_DISABLED/ 를 sdm-parser/ 로 복구.

A4 — 타임아웃 진단표 (A3 판정과 무관하게 항상 작성)
| .sdm 크기(MB) | 경과시간(초) | DMConsole 기동 지연(초) | 행업 여부 근거 1줄 |
- 향후 Claude Code 타임아웃 디버깅용 재료. 여기서 고치려 하지 말 것.

═══════════════════════════════
[작업 B 진입 전 — manifest 준비 게이트]
- issue-analyzer/manifest/COPY_FRAGMENTS.md 를 열어 복사 원본 경로를 확인한다.
  (원본은 l1sw-log-analyzer\manifest\ 의 fragment json. 5.2 아님.)
- 그 원본에서 fragment json 7개
  (proc/front/channel/common/meas/mtm/nptm.json)를 manifest/ 로 복사.
- _meta.json 은 복사하지 않는다 (issue-analyzer 것 유지).
- output_suffix "_l1sw" 는 건드리지 않는다.
- 원본 경로가 COPY_FRAGMENTS.md에 없거나 접근 불가면:
  멈추고 사용자에게 "l1sw manifest 경로"를 질문한다.
- 판정: manifest/ 에 fragment 7개 존재 = 게이트 통과.

═══════════════════════════════
작업 B — E2E 2차 검증 (미확인 9개만)
1차(2026-07-07)에서 PASS 9 / FAIL 1(V2-1) / 미확인 9였다.
1차 PASS 항목은 재검증하지 않는다.

[입력 규칙]
- A3가 PASS면 그때 생성된 full text에 Step B를 돌려 _l1sw.txt 확보 후 사용.
- A3가 FAIL/미확인이면 기존 (3).txt (약 35M라인)를 직접 입력.
  이 경우 Step A(변환) 재실행 금지.

[설치 상태 참고 — 판정 대상 아님]
manifest fragment가 게이트 통과 전 0개인 것은 정상이며 FAIL로 판정하지 않는다.

V2-4 — 존재하지 않는 시간 범위
- 입력에 Step B(ia_extract.py)를 --time-from 01:00:00 --time-to 01:00:01 로 실행.
- PASS: 빈 파일 + exit 0 을 "정상(매칭 0건)"으로 처리.
- FAIL: exit≠0 또는 에러 중단 또는 빈 결과를 오류로 취급.

V2-5 — 2-pass 규칙 (Step A 재실행 금지)
- 동일 입력에 Step B만 재실행 (--modules 를 1차와 다르게 지정).
- PASS: 변환 재시도 없이 Step B만 수행.
- FAIL: 변환/DMConsole 재호출 흔적 존재.

V3 — 트랙 2 E2E 1회 완주
- [진행 전 질문] "이 로그에서 분석할 이슈 증상을 1줄로 알려달라
  (예: 특정 시각 TxPower 이상, CA 활성화 실패 등)"
- 답변 수신 후 "원인분석 시작"으로 S0(시작 질문)~S5(보고·기록) 완주.
- 판정 5개 (각각 독립):
  V3-1 모든 원인 후보에 [A/B/C] 등급 부여
  V3-2 근거 없는 후보가 "미확인 항목"으로 분리
  V3-3 case 파일 30라인 이하
  V3-4 records/index.yaml 1줄 append
  V3-5 보고서에 재현 조건 포함

V4 — 루프 가드 (V3 진행 중 관찰, 별도 실행 없음)
  V4-1 S0 질문 후 사용자가 답하기 전 스스로 번호 선택해 진행하면 FAIL
  V4-2 좁히기 2회째 요구 시 사용자 승인을 묻는지

═══════════════════════════════
결과 보고 형식:
| 작업 | 항목 | 판정(PASS/FAIL/미확인) | 비고(FAIL이면 원인 1줄) |
마지막 줄: 종합: PASS n / FAIL n / 미확인 n
A4 진단표는 표 형태로 별도 첨부.
```

---

## 실행 후 회수할 것

1. 판정표 전체 (작업 A + 작업 B)
2. A4 타임아웃 진단표
3. A3가 FAIL/미확인이면 그 진단 로그
4. V3에서 사용한 issue_type(증상 1줄)과 최종 보고서 요약
