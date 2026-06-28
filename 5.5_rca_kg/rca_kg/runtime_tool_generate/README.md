# runtime_tool_generate

갱신: 2026-06-27 12:21 KST

이 폴더는 RCA 실행 상태를 저장하는 도구 생성 영역이다. 일반 사용자는 직접 편집하지 않고 `NEXT_STEP_5.5.md` 또는 `/root-cause-analyzer`의 안내를 따른다.

이 폴더의 실제 위치는 `kg_root/runtime_tool_generate/`이다. 기본값은 `<패키지루트>/rca_kg/runtime_tool_generate/`이고, 사용자가 `configure_kg_root.ps1`로 고정 저장소를 지정하면 그 위치 아래에 생성된다.

## 파일

| 파일/폴더 | 역할 |
|---|---|
| `current_run.yaml` | 현재 실행 상태. P0~P6가 읽고 갱신한다. |
| `current_run.example.yaml` | 상태 파일 예시. 손상 시 복구 참고용. |
| `format_profiles/` | P1이 역설계한 `_l1sw.txt` 출력 형식 명세. |

## 운영 규칙

1. P0는 `workspace_root`와 `kg_root`를 확정한다.
2. P1~P6는 이전 단계의 결과를 `current_run.yaml`에서 읽는다.
3. 각 단계 종료 시 `current_step`, `next_step`, `last_updated_kst`를 갱신한다.
4. 사용자는 이 파일을 직접 편집하지 않고 `NEXT_STEP_5.5.md`를 본다.
5. 세션이 바뀌어도 Claude Code는 이 파일을 읽고 이어서 진행한다.
