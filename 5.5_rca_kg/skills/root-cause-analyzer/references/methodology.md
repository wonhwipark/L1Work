# P4 원인분석 방법론 (요약 + 포인터)

전체 방법론은 SSOT인 `prompt/deepdive/RCA_ANALYSIS_METHODOLOGY.md`에 있다. 이 파일은 P4 수행에 필요한 핵심만 요약한다. 깊은 판단이 필요하면 deepdive 원문을 읽는다.

## 대원칙
가설 주도 + 증거 역추적. failure_event를 anchor로 잡고, cptime 구간에서 가설을 확인/반증해 남은 것을 root_cause로 확정한다. 파일 처음부터 읽지 않는다 — anchor부터 바깥으로.

## 7단계 (S1~S7)
- S1 증상 고정: 최초 실패 cptime을 anchor로.
- S2 시간창: anchor 앞으로 충분히(진입까지), 뒤로 약간(fallback까지). **원인은 항상 결과보다 cptime이 작다.**
- S3 정상경로 대조: seed의 happy-path 대비 최초 이탈 지점.
- S4 가설 2~4개.
- S5 가설 가르기: 가설을 구분하는 단서만 추가 확인.
- S6 범위 분리: 단말/계층/API/설정 vs 환경/RF. **환경/RF면 unresolved + handoff**(원인 미상이 아님).
- S7 인과사슬 + confidence: 사슬의 모든 화살표가 로그로 뒷받침되면 ↑, 추정으로 메운 화살표 수만큼 ↓.

## confidence 산정 (느낌 금지, 증거 충족도로)
- high: 인과사슬 전 구간이 로그 증거로 연결.
- medium: 핵심 이탈 지점은 확인, 일부 화살표는 추정.
- low: 최초 이탈은 보이나 원인 줄이 안 보임 / 추정이 다수.
구분: 담당영역 안 + 원인 불확실 = `analyzed + confidence: low`. 담당영역 밖 = `unresolved` + handoff(confidence 표기 안 함).

## 미지 모듈 가드 (핵심 안전장치)
최초 이탈 지점의 원인 줄이 `_l1sw.txt`/signal에 없고 그 위 cptime 구간이 공백이면 = 미지 모듈 누락 신호. 보이는 범위만으로 인과사슬이 매끄러워 confidence가 **거짓으로 높아지는** 것을 막는다. 추가 추출(시간창/모듈/명령 후보)을 제시하고 멈춘다. 누적 2회 후에도 원인 줄이 없으면 confidence를 올리지 말고 low + 원인 미상으로 정직 종료.

## 안티패턴 (하지 말 것)
- wall-clock으로 순서 판단(시험마다 시계 다름 — 순서는 항상 cptime).
- 담당영역 밖(RF/환경)인데 low로 우기기 → S6에서 unresolved로.
- 원인 줄이 안 보이는데 confidence 올리기 → 미지 모듈 가드.

## [E] 경로 — 사람이 원인을 직접 알려준 경우
사람 입력 최소: 인과사슬 + 근거 로그 유무. 자동: confidence 산정, status=reviewed 후보, keywords candidate 후보 기록. 사람이 준 인과사슬도 로그 증거 유무로 confidence를 정직하게 산정한다.
