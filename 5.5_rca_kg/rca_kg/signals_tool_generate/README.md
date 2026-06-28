# signals_tool_generate

갱신: 2026-06-27 12:21 KST

이 폴더는 P3 또는 prefilter 스크립트가 생성한 signal 파일을 저장하는 도구 생성 영역이다. 일반 사용자는 직접 편집하지 않는다.

## 역할

```text
_l1sw.txt 전체
→ issue_type별 signature 검색
→ 필요한 cptime 구간만 signal 파일로 축소
→ P4 원인분석 입력으로 사용
```

## 운영 규칙

```text
- 출력 위치는 {kg_root}/signals_tool_generate/로 고정한다.
- signal 파일은 원본 로그를 대체하지 않는다.
- case YAML에는 전체 로그 본문이 아니라 signal 파일 경로와 cptime 범위를 기록한다.
```

수동 prefilter 실행은 `scripts/README.md`를 참고한다. 정상 사용자는 `/root-cause-analyzer`가 안내하는 흐름을 따른다.
