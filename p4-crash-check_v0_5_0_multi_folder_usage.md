# p4-crash-check v0.5.0 — 복수 폴더 사용 예시

아래 내용을 그대로 복사해서 사용할 수 있습니다.

## 권장 요청 예시

```text
p4-crash-check로 아래 P4 폴더들을 최근 1년 기준으로 한 번에 분석해줘.

분석 폴더:
- ./L1/TX
- ./L1/ChCfg
- ./L1/SAR

조건:
1. 내가 지정한 폴더만 검색해줘.
2. 1900 → 1800 같은 다른 branch 자동 확장은 하지 마.
3. 같은 CL이 여러 폴더에 걸쳐 있으면 CL 번호 기준으로 1건만 집계해줘.
4. 각 CL 상세에는 어느 요청 폴더에 해당하는지 Scope를 표시해줘.
5. 시작 전에 현재 분석 제외 Submitter ID를 보여주고 추가/삭제 여부를 확인해줘.
6. 기본 분석 기간은 최근 365일로 해줘.
7. Crash가 아닌 CL은 Crash gate에서 제외해줘.
8. CL Description만으로 정보가 충분하면 Jira 조회는 건너뛰어줘.
9. 최종 결과는 Confluence에 붙여넣기 쉬운 정적 HTML로 생성해줘.
10. UNCLASSIFIED CL도 상세에서 확인할 수 있게 해줘.
```

## CLI로 직접 실행

```text
skillsilent run p4-crash-check run -- ./L1/TX ./L1/ChCfg ./L1/SAR --days 365
```

## 서로 다른 branch 폴더를 직접 지정하는 경우

자동으로 branch를 확장하지는 않지만, 사용자가 직접 여러 branch 경로를 지정하는 것은 가능합니다.

```text
skillsilent run p4-crash-check run -- \
  //depot/1900/L1/TX/... \
  //depot/1800/L1/ChCfg/... \
  --days 365
```

이 경우에만 1900과 1800을 함께 분석합니다.

## Category를 제한해서 분석

```text
skillsilent run p4-crash-check run -- \
  ./L1/TX ./L1/ChCfg ./L1/SAR \
  --category WDT,OOB,DATA_ABORT \
  --days 365
```

## 특정 CL만 확인

선택한 여러 폴더 범위 안에서 특정 CL만 확인할 수 있습니다.

```text
skillsilent run p4-crash-check run -- \
  ./L1/TX ./L1/ChCfg \
  --cl CL1234 \
  --cl CL1250
```

## 제외 Submitter 확인/변경

```text
# 현재 제외 ID 확인
skillsilent run p4-crash-check exclude-show --

# 추가
skillsilent run p4-crash-check exclude-update -- --add buildbot

# 삭제
skillsilent run p4-crash-check exclude-update -- --remove olduser
```

## 복수 폴더 집계 규칙

예를 들어 다음과 같이 CL이 존재한다고 가정합니다.

```text
TX     : CL100, CL101
ChCfg  : CL100, CL102
SAR    : CL103
```

최종 전체 수집 CL은 5건이 아니라 다음 **4건**입니다.

```text
CL100
CL101
CL102
CL103
```

`CL100`은 TX와 ChCfg에 모두 걸쳐 있지만 KPI에서는 1건으로 계산하고, 상세 보고서 Scope에는 두 폴더를 모두 표시합니다.
