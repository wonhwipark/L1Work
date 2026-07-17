# Confluence + Draw.io 업로드 안내

## 1. 권장 순서

1. `hld_code_workflow_confluence.html`을 Confluence 페이지로 가져온다.
2. 페이지를 편집한다.
3. 각 “Draw.io 매크로 권장 파일” 박스 아래에 커서를 둔다.
4. `/draw.io` 또는 설치된 Draw.io 매크로 이름을 입력한다.
5. **Import / Device / File** 계열 메뉴에서 대응 `.drawio` 파일을 선택한다.
6. 페이지 폭에 맞게 다이어그램 크기를 조정한다.
7. 다이어그램 아래의 표 기반 대체 흐름을 확인한다.
8. Draw.io가 정상 표시되면 대체 흐름은 유지, 접기 또는 삭제한다.

## 2. 파일 대응표

| 문서 절 | 파일 |
|---|---|
| 전체 업무 흐름 | `diagrams/01_overall_workflow.drawio` |
| CodeAnalyzer 재사용 및 Compare | `diagrams/02_compare_decision_flow.drawio` |
| NOT_ANALYZED 후속 처리 | `diagrams/03_not_analyzed_recovery.drawio` |
| Implement, G1/G2, Late Gap | `diagrams/04_implement_and_late_gap.drawio` |

## 3. Draw.io가 없는 환경

`fallback/*.svg`를 이미지로 첨부한다. HTML의 표 기반 흐름도 그대로 사용할 수 있다.

## 4. REST 자동화 시 주의

HTML 파일을 REST로 페이지에 넣는 것과 Draw.io 매크로를 생성하는 것은 별도 작업이다.

자동화 전 다음 절차를 권장한다.

```text
사내 Confluence에서 테스트 페이지 생성
→ Draw.io 매크로 하나를 사람이 삽입
→ REST로 페이지 storage format 조회
→ Draw.io 첨부 파일명, macro parameter, page attachment 관계 확인
→ 확인된 형식을 템플릿으로 자동화
```

Cloud, Server/Data Center, Draw.io 앱 버전에 따라 storage format이 다를 수 있으므로 일반화한 매크로 XML을 임의로 하드코딩하지 않는다.

## 5. 표시 권장

- 전체 흐름: 페이지 폭 100%
- 나머지 흐름: 페이지 폭 90~100%
- 긴 페이지에서는 각 다이어그램 바로 아래에 3~5줄 요약 유지
- 다이어그램 텍스트가 작으면 전체화면 보기 안내 추가
