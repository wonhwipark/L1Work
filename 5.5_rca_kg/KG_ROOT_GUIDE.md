# KG_ROOT_GUIDE — RCA KG 고정 저장소 설정

버전: convenience_v0.21_kg_root_config  
갱신: 2026-06-27 12:21 KST

## 1. 결론

`rca_kg`는 스킬 설치 폴더 아래에 두지 않는다.

```text
스킬 설치 위치
C:\Users\<user>\.claude\skills\root-cause-analyzer\

RCA KG 저장소
D:\AI_Automation\RCA_KG\
```

스킬은 교체 가능한 실행 지침이고, KG는 계속 누적되는 분석 자산이다. 스킬 업데이트 시 `-Force`로 기존 스킬 폴더를 지우면 스킬 아래 데이터도 같이 사라질 수 있으므로 `rca_kg`를 스킬 아래에 두지 않는다.

---

## 2. 기본값과 권장값

새 사용자는 별도 설정 없이 바로 사용할 수 있다.

```text
기본 kg_root = <RCA_standalone 패키지 루트>\rca_kg
```

반복 사용자는 고정 저장소를 지정하는 것이 좋다.

```text
권장 kg_root = D:\AI_Automation\RCA_KG
```

이렇게 하면 RCA 패키지를 v0.21, v0.22로 바꿔도 case YAML, keywords.yaml, index가 한 곳에 계속 누적된다.

---

## 3. 설정 방법

패키지 루트에서 실행한다.

```powershell
.\configure_kg_root.ps1 -KgRoot "D:\AI_Automation\RCA_KG"
```

설정 후 확인한다.

```powershell
Get-Content .\rca_config.yaml
```

Claude Code에서 다시 시작한다.

```text
/root-cause-analyzer
이어서 진행해줘
```

---

## 4. 경로 의미

| 이름 | 의미 | 예시 |
|---|---|---|
| `workspace_root` | RCA_standalone 패키지 루트 | `D:\AI_Automation\RCA_standalone_v0_21` |
| `skill_install_dir` | Claude Code 스킬 설치 위치 | `C:\Users\<user>\.claude\skills\root-cause-analyzer` |
| `kg_root` | 누적 RCA KG 저장소 | `D:\AI_Automation\RCA_KG` |

`workspace_root`와 `kg_root`는 같을 수도 있고 다를 수도 있다. 기본값은 `kg_root = {workspace_root}\rca_kg`이다.

---

## 5. kg_root 내부 기대 구조

```text
RCA_KG/
├── cases/
│   └── unresolved/
├── runtime_tool_generate/
│   └── format_profiles/
├── signals_tool_generate/
├── indexes_tool_generate/
├── manifest_fragments/
├── schema/
├── skills_seed/
└── keywords.yaml
```

`configure_kg_root.ps1`는 위 폴더가 없으면 생성하고, 기본 schema/example/README류 파일은 패키지 내 `rca_kg`에서 복사한다. 기존 KG 파일은 기본적으로 덮어쓰지 않는다.

---

## 6. 금지 위치

아래처럼 스킬 폴더 아래를 KG로 지정하지 않는다.

```text
C:\Users\<user>\.claude\skills\root-cause-analyzer\rca_kg
```

이 위치는 스킬 업데이트 또는 재설치 때 삭제될 수 있다.

---

## 7. 잘못 생성된 rca_kg가 있으면

로그 폴더 아래에 `rca_kg`가 생겼다면 잘못된 KG일 수 있다.

```text
C:\logs\failure_case\rca_kg
```

자동 삭제하지 말고 `STRUCTURE_FIX_GUIDE.md`의 KG 병합 절차를 따른다. 중복 case는 `scripts/compare_kg_cases.ps1`로 먼저 비교한다.
