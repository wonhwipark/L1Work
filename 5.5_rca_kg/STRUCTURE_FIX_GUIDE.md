# STRUCTURE_FIX_GUIDE — RCA 구조 복구 가이드

대상 버전: convenience_v0.21_kg_root_config  
갱신: 2026-06-27 12:21 KST

## 0. kg_root 위치 수정

`rca_kg`가 스킬 설치 폴더 아래에 있으면 안 된다.

잘못된 위치:

```text
C:\Users\<user>\.claude\skills\root-cause-analyzer\rca_kg
```

권장 위치:

```text
D:\AI_Automation\RCA_KG
```

설정:

```powershell
.\configure_kg_root.ps1 -KgRoot "D:\AI_Automation\RCA_KG"
```

---


갱신: 2026-06-27 12:21 KST  
대상 버전: convenience_v0.21_kg_root_config

이 문서는 `install_skill.ps1` 실행 시 패키지 구조가 기대 구조와 맞지 않을 때 참고하는 복구 가이드다.

---

## 1. 원칙

설치 스크립트는 아무 폴더나 자동으로 추측해서 설치하지 않는다. 스킬 설치는 Claude Code가 읽어야 하므로 다음 조건을 만족해야 한다.

```text
<package root>/skills/root-cause-analyzer/SKILL.md
```

이 위치가 맞지 않으면 설치는 중단된다. 대신 스크립트가 현재 발견한 `SKILL.md` 후보와 기대 구조를 보여주고, 사용자가 어떻게 맞춰야 하는지 안내한다.

---

## 2. 기대 구조

```text
<package root>/
├─ skill_manifest.yaml
└─ skills/
   └─ root-cause-analyzer/
      ├─ SKILL.md
      └─ references/
         └─ ...
```

필수 파일:

- `skills/root-cause-analyzer/SKILL.md`
- `skills/root-cause-analyzer/references/index.md`
- `skills/root-cause-analyzer/references/p0_env_probe.md`
- `skills/root-cause-analyzer/references/c0_secure_l1sw.md`
- `skills/root-cause-analyzer/references/p1_format_probe.md`
- `skills/root-cause-analyzer/references/p2_manifest_fragments.md`
- `skills/root-cause-analyzer/references/p3_signal.md`
- `skills/root-cause-analyzer/references/p4_rca_and_case.md`
- `skills/root-cause-analyzer/references/p5_review.md`
- `skills/root-cause-analyzer/references/p6_keywords_promote.md`
- `skills/root-cause-analyzer/references/methodology.md`
- `skills/root-cause-analyzer/references/seeds/README.md`

---

## 3. 자주 발생하는 구조 오류

### 3.1 스킬 폴더명이 바뀐 경우

잘못된 예:

```text
skills/code_analyzer/SKILL.md
```

또는

```text
skills/RCA/SKILL.md
```

맞춰야 하는 구조:

```text
skills/root-cause-analyzer/SKILL.md
```

### 3.2 한 단계 더 깊게 풀린 경우

잘못된 예:

```text
skills/root-cause-analyzer/root-cause-analyzer/SKILL.md
```

맞춰야 하는 구조:

```text
skills/root-cause-analyzer/SKILL.md
```

### 3.3 TargetSkillsDir를 잘못 지정한 경우

`-TargetSkillsDir`에는 스킬 폴더 자체가 아니라 상위 `skills` 폴더를 넣는다.

잘못된 예:

```powershell
.\install_skill.ps1 -TargetSkillsDir "C:\Users\<user>\.claude\skills\root-cause-analyzer"
```

올바른 예:

```powershell
.\install_skill.ps1 -TargetSkillsDir "C:\Users\<user>\.claude\skills"
```

---

## 4. 복구 방법

가장 안전한 방법은 ZIP을 다시 푸는 것이다.

```text
1. ZIP을 새 폴더에 다시 압축 해제
2. 패키지 루트에서 skill_manifest.yaml 확인
3. skills/root-cause-analyzer/SKILL.md 존재 확인
4. .\install_skill.ps1 실행
```

수동으로 폴더를 맞출 수도 있다.

```powershell
New-Item -ItemType Directory -Force -Path ".\skills" | Out-Null
Move-Item -Path "<현재-스킬-폴더>" -Destination ".\skills\root-cause-analyzer"
```

단, `references` 폴더도 `SKILL.md`와 같은 스킬 폴더 아래에 있어야 한다.

---

## 5. 설치 후 검증

```powershell
.\validate_install.ps1
```

직접 위치를 지정한 경우:

```powershell
.\validate_install.ps1 -TargetSkillsDir "C:\Users\<user>\.claude\skills"
```

---

## 6. KG가 잘못된 위치에 생긴 경우 (rca_kg 병합 절차)

### 6.1 증상

`rca_kg/` 폴더가 RCA_standalone 패키지 루트가 아니라, **분석한 `_l1sw.txt` 파일의 상위 폴더에 생겼다.** case YAML도 그 안에 들어 있다.

원인: 이전 버전은 산출물 경로가 상대경로 `rca_kg/`였고, Claude Code의 현재 작업 디렉토리(cwd)가 로그 폴더로 잡히면 거기에 KG가 만들어졌다. v0.20부터 P0-0가 `workspace_root`를 절대경로로 확정해 이 문제를 막는다.

### 6.2 원칙

KG는 하나로 누적되어야 패턴 재발 감지·signature 승격이 동작한다. 잘못 생긴 KG의 case를 **정본 KG(`{kg_root}/`)로 병합**한다. 스크립트가 자동 삭제하지 않으므로 사람이 확인하며 옮긴다.

### 6.3 병합 절차

먼저 두 위치를 대조해 병합 계획을 본다(읽기 전용, 파일을 옮기지 않음):

```powershell
.\scripts\compare_kg_cases.ps1 `
  -SourceCasesDir "<로그폴더>\rca_kg\cases" `
  -TargetCasesDir "{workspace_root}\rca_kg\cases" `
  -IncludeUnresolved
```

출력의 NEW / DUP / SAMEID 분류에 따라 아래대로 병합한다.

정본 위치:

```text
{kg_root}/                  ← 정본 KG 저장소
```

잘못된 위치(예):

```text
<로그폴더>/rca_kg/              ← 잘못 생성됨
```

1. 두 위치의 `cases/`를 비교한다. case_id는 fingerprint 기반이라 같은 장애면 파일명이 같을 수 있다.
2. **fingerprint가 겹치지 않는 case**: 정본 `cases/`로 그대로 이동.
3. **fingerprint가 겹치는 case**: 같은 장애의 중복이다. 한쪽만 남기고, `occurrence_count`·`recent_occurrences`·`last_seen`을 합산해 정본 쪽을 갱신한다(P4 PART B 7번 규칙과 동일).
4. `unresolved/`도 같은 방식으로 병합.
5. `keywords.yaml`: 잘못된 위치에서 승격된 signature가 있으면, 정본 keywords.yaml과 비교해 누락 signature만 candidate로 추가(P6 규칙 준수, 임의 confirmed 승격 금지).
6. `signals_tool_generate/`·`indexes_tool_generate/`는 재생성 가능한 산출물이므로 옮기지 않아도 된다. 병합 후 다음 분석에서 정본 기준으로 다시 생성된다.
7. 병합이 끝나면 잘못된 위치의 `rca_kg/`를 삭제한다(사람이 직접).

PowerShell 예시(겹치지 않는 case 이동만 — 겹치는 case는 위 3번대로 수동 병합):

```powershell
$src = "<로그폴더>\rca_kg\cases"
$dst = "{workspace_root}\rca_kg\cases"
Get-ChildItem -Path $src -Filter *.yaml -File | ForEach-Object {
  $target = Join-Path $dst $_.Name
  if (Test-Path $target) {
    Write-Host "[중복-수동확인] $($_.Name)"   # fingerprint 겹침 가능 → occurrence 합산
  } else {
    Move-Item $_.FullName $target
    Write-Host "[이동] $($_.Name)"
  }
}
```

### 6.4 재발 방지

병합 후 새 분석을 시작할 때, P0 표 맨 위의 `workspace_root`가 RCA_standalone 패키지 루트의 절대경로인지 확인한다. 이 값이 로그 폴더를 가리키면 멈추고 경로를 바로잡는다.

