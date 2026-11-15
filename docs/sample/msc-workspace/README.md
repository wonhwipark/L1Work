# L1 Workspace · MSC 열람 샘플

**[브라우저에서 분석 문서 열기](https://wonhwipark.github.io/L1Work/sample/msc-workspace/)** · **[MSC 확대 뷰어](https://wonhwipark.github.io/L1Work/sample/msc-workspace/works/DEMO-MSC-001/artifacts/analysis/msc/r0001/viewer.html)**

공개 가상 Work `DEMO-MSC-001`을 사용해 **분석 문서 → HTML 뷰어 → 내장 MSC** 경로를 보여주는 예시예요. 기존 B안 공개 샘플의 6개 참여자·36개 메시지·3단계를 재사용했어요. 실제 L1 코드·호출 관계·업무 Work 구조 실측 결과가 아니에요.

| 예시 파일 | 역할 |
|---|---|
| [works/DEMO-MSC-001/README.md](works/DEMO-MSC-001/README.md) | Work 요약과 문서 진입 |
| [works/DEMO-MSC-001/CODE_FACTS.md](works/DEMO-MSC-001/CODE_FACTS.md) | 분석 문서·MSC 미리보기·HTML 링크 |
| [works/DEMO-MSC-001/MSC_VIEW.md](works/DEMO-MSC-001/MSC_VIEW.md) | MSC 목록과 시나리오별 보기 |
| [works/DEMO-MSC-001/문서안내.md](works/DEMO-MSC-001/문서안내.md) | 문서·그림·원본 연결 |
| [works/DEMO-MSC-001/artifacts/analysis/msc/r0001/viewer.html](works/DEMO-MSC-001/artifacts/analysis/msc/r0001/viewer.html) | SVG·보기 기능을 내장한 단일 HTML |
| [works/DEMO-MSC-001/artifacts/analysis/msc/r0001/msc.svg](works/DEMO-MSC-001/artifacts/analysis/msc/r0001/msc.svg) | 전체 MSC 그림 |
| [works/DEMO-MSC-001/artifacts/analysis/msc/r0001/msc-preview.svg](works/DEMO-MSC-001/artifacts/analysis/msc/r0001/msc-preview.svg) | 같은 SVG에서 생성한 첫 단계 미리보기 |
| [works/DEMO-MSC-001/artifacts/analysis/msc/r0001/msc.txt](works/DEMO-MSC-001/artifacts/analysis/msc/r0001/msc.txt) | 원본 MSC 텍스트 |

GitHub 파일 화면에서는 HTML 소스를 보여줘요. 렌더링 화면은 위 브라우저 링크를 사용해 주세요. 확대 뷰어는 HTML에 SVG·CSS·스크립트를 내장해 파일 하나를 내려받아도 열 수 있어요.

정본 예시는 `sample/msc-workspace/`이며 `docs/sample/msc-workspace/`는 기존 Pages 게시 위치에 맞춘 동일 바이트 복사본이에요. 이번 개정은 두 위치를 같은 입력·같은 commit으로 생성했어요. 새 자동 동기화 작업을 설치한 것은 아니에요. 실제 적용 경로는 업무 호스트의 기존 converter/Kernel 계약을 우선해요.
