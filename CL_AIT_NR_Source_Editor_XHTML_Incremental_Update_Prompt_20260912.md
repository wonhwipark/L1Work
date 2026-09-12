# CL-AIT NR 기존 HLD 결과 → Confluence Source Editor용 XHTML 추가 생성 프롬프트

## 현재 상태

이전에 아래 작업은 이미 완료되어 있다.

- NR CL-AIT HLD 최종 취합
- `CL_AIT_NR_HLD_FINAL.md` 생성
- HTML preview 생성
- PlantUML MSC / Class Diagram 포함
- Diagram Commentary 포함
- Confluence 수동 붙여넣기용 산출물 일부 생성

이번에는 **기존 HLD를 다시 작성하거나 다시 취합하지 말고**, 새로 업데이트된 `doc-converter v0.2.8` 기능만 적용한다.

## 목표

기존 `CL_AIT_NR_HLD_FINAL.md`를 그대로 재사용하여 다음을 추가 생성한다.

```text
CL_AIT_NR_HLD_FINAL.storage.xhtml
CL_AIT_NR_HLD_FINAL_CONFLUENCE_SOURCE_EDITOR_PASTE.md
CL_AIT_NR_HLD_FINAL_CONFLUENCE_VALIDATION.json
```

필요하면 기존 HTML과 manual fallback guide도 v0.2.8 기준으로 갱신한다.

## 중요한 제약

- HLD 내용 재작성 금지
- `hld-composer` 재실행 금지
- Code / UT / Scenario 분석 재실행 금지
- LTE 작업 시작 금지
- REST API publish 금지
- 기존 FINAL.md를 Source of Truth로 사용
- 기존 FINAL.md가 여러 개 발견되면 최신 파일을 임의 선택하지 말고 후보를 보여주고 멈출 것

## 실행 방법

가능하면 `doc-converter`의 새 Source Editor 경로를 사용한다.

```text
skillsilent run doc-converter source-editor-package -- \
  --input <CL_AIT_NR_HLD_FINAL.md> \
  --output-dir <기존 final_hld output 폴더> \
  --plantuml-macro plantuml \
  --json
```

기존 `cl-ait-dev-orchestrator v0.1.5`의 `manual-confluence-package` 경로를 재사용하더라도,
`doc-converter v0.2.8`에서는 동일 output 폴더에 `.storage.xhtml`이 추가 생성되어야 한다.

## 검증 Gate

다음 조건을 확인한다.

```text
Storage XHTML 생성                     = PASS
REST publish 사용                      = false
Input PlantUML count                   = Storage PlantUML macro count
Unconverted PlantUML code macro count  = 0
XML validation                         = PASS
Diagram Commentary missing             = 0 권장
```

PlantUML macro count가 맞지 않으면 완료로 판정하지 말 것.

## 최종 결과

아래 형식으로만 요약 보고한다.

```text
[Confluence Source Editor Package Update]

Source FINAL.md:
- <path>

Generated:
- <path>/CL_AIT_NR_HLD_FINAL.storage.xhtml
- <path>/CL_AIT_NR_HLD_FINAL_CONFLUENCE_SOURCE_EDITOR_PASTE.md
- <path>/CL_AIT_NR_HLD_FINAL_CONFLUENCE_VALIDATION.json

PlantUML:
- input:
- storage macro:
- match: PASS | FAIL

Commentary:
- missing:

REST publish:
- false

Status:
- SOURCE_EDITOR_PACKAGE_READY
또는
- BLOCKED
```

## 사용자 수동 적용 방법

`SOURCE_EDITOR_PACKAGE_READY`이면 사용자에게 아래만 안내한다.

1. Confluence 페이지 Edit
2. `<> Open in Source Editor`
3. 기존 Source 전체를 로컬에 먼저 백업
4. 새 페이지/전체 교체가 목적이면 `CL_AIT_NR_HLD_FINAL.storage.xhtml` 전체 붙여넣기
5. Apply
6. 일반 편집 화면에서 Heading / Table / PlantUML MSC / Class Diagram / Commentary 확인
7. 정상 확인 후 Save

이번 작업의 목적은 **기존 HLD를 건드리지 않고 Source Editor용 Storage XHTML만 안전하게 추가 생성하는 것**이다.
