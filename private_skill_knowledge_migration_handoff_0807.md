# Private Skill / Knowledge 구조 전환 — 새 대화 전달용 Handoff

- 작성 기준: 2026-08-07 KST
- 목적: 새 대화에서 개인 Skill / Knowledge 구조 전환을 안전하게 이어서 진행하기 위한 기준 문서
- 중요: 아래 **현재 확정안**을 최우선으로 사용한다. 과거 경로/네이밍 제안과 충돌하면 이 문서를 우선한다.

---

## 0. 현재 확정안 — 반드시 이 기준에서 시작

### 0.1 Claude Skill Entry

Skill 자체의 `SKILL.md`는 기존 위치를 유지한다.

```text
~/.claude/skills/<skill>/SKILL.md
```

역할:

```text
Claude가 Skill을 탐색/등록하는 entry 위치
```

이 위치를 이번 구조 전환에서 임의로 변경하지 않는다.

---

### 0.2 개인 Skill 실제 자산 기준 경로

향후 개인 Skill의 실제 구현 코드·스크립트·설정·스키마 등의 기준 루트는 다음으로 정렬한다.

```text
~/l1sw-skills/private-skills/<skill>/
```

예:

```text
~/l1sw-skills/private-skills/
├─ code-analyzer/
├─ issue-analyzer/
├─ slte-knowledge-manager/
├─ slte-port-impact-analyzer/
├─ code-fix/
├─ l1_fla/
├─ skillsilent/
├─ skill-updater/
├─ autotask-builder/
└─ ...
```

중요:

```text
private/<skill>         사용하지 않음
private/skills/<skill>  사용하지 않음
private-skills/<skill>  현재 확정
```

---

### 0.3 Knowledge는 Skill과 분리

`slte-knowledge-manager`가 축적하는 Knowledge는 Skill directory 하위에 장기 저장하지 않는다.

Knowledge는 DB/File-based Knowledge Store 성격으로 취급하며 Skill tree와 완전히 분리한다.

최종 로컬 목표:

```text
~/l1sw-knowledge/
```

개념 구조:

```text
~/l1sw-knowledge/
├─ current/
├─ candidates/
├─ catalogs/
├─ indexes/
├─ knowledge_manifest.json
├─ responsibility_catalog.json
│
├─ runs/           # local/runtime, Git 제외
├─ cache/          # Git 제외
├─ snapshots/      # 기본 Git 제외
└─ runtime/        # Git 제외
```

실제 최초 migration에서는 임의로 schema/path를 재설계하지 말고, 현재 Knowledge Manager가 사용하는 Store layout을 최대한 보존한다.

---

## 1. 전체 역할 분리

최종적으로 다음 세 위치의 책임을 분리한다.

```text
~/.claude/skills/<skill>/SKILL.md
        │
        │ Skill discovery / entry
        ▼
~/l1sw-skills/private-skills/<skill>/
        │
        │ Skill implementation
        ▼
~/l1sw-knowledge/
        │
        └─ Persistent Knowledge DB
```

정리:

| 위치 | 역할 |
|---|---|
| `~/.claude/skills/<skill>/SKILL.md` | Claude Skill 탐색/entry |
| `~/l1sw-skills/private-skills/<skill>/` | 개인 Skill 구현 코드/스크립트/설정 |
| `~/l1sw-knowledge/` | 장기 축적 Knowledge Store |

---

## 2. GitHub 구조 방향

### 2.1 Skills와 Knowledge는 repository 분리 권장

현재 방향:

```text
Private GitHub

Repo A: 개인 Skills
└─ private-skills/
   ├─ code-analyzer/
   ├─ issue-analyzer/
   ├─ slte-knowledge-manager/
   └─ ...

Repo B: Knowledge
├─ current/
├─ candidates/
├─ catalogs/
├─ indexes/
└─ ...
```

개념적으로:

```text
Skills Repo
= Program / Skill version SSOT

Knowledge Repo
= Persistent Knowledge SSOT
```

---

### 2.2 그룹 GitHub 구조와의 관계

그룹 공용 GitHub `l1sw-skills`는 현재 다음과 같은 역할별 구조를 사용한다.

```text
dev-skills/
shared-skills/
mgmt-skills/
eval-skills/
```

개인 Private GitHub에서는 이 그룹 폴더들을 빈 폴더로 복제하지 않는다.

개인 repo에는 현재:

```text
private-skills/
```

만 두고, **폴더 naming/hierarchy 철학만 그룹 구조와 맞춘다.**

향후 그룹 공용화가 결정되면 예:

```text
개인:
private-skills/<skill>/

        ↓ Promote

그룹:
dev-skills/<skill>/
```

또는 범용 기능이면:

```text
private-skills/<utility>/
        ↓
shared-skills/<utility>/
```

형태로 자연스럽게 승격할 수 있도록 한다.

---

## 3. Skill Promotion과 Knowledge Promotion은 독립

핵심 원칙:

```text
Skill Promotion ≠ Knowledge Promotion
```

예:

```text
private-skills/slte-knowledge-manager/
        ↓ 그룹 승격
dev-skills/slte-knowledge-manager/
```

이 과정에서 Knowledge DB는:

```text
~/l1sw-knowledge/
```

에 그대로 남는다.

향후 Knowledge 자체를 그룹 공유 자산으로 승격할지는 별도 결정한다.

---

## 4. Skill Naming 변경은 아직 수행하지 않음

현재 Skill 이름은 그대로 유지한다.

예:

```text
code-analyzer
issue-analyzer
slte-knowledge-manager
slte-port-impact-analyzer
code-fix
skillsilent
skill-updater
autotask-builder
l1_fla
...
```

향후 Naming Phase에서 그룹 naming과 충돌/융합성을 보고 별도 정리한다.

특히 다음은 단순히 `l1sw-` prefix를 붙이기 전에 그룹 공용 Skill과 책임 경계를 확인해야 한다.

```text
issue-analyzer
↔ 그룹 l1sw-defect-analyzer
↔ 그룹 l1sw-log-analyzer
```

Infrastructure 성격의 Skill은 `l1sw-` prefix가 불필요할 수 있다.

예:

```text
skillsilent
skill-updater
autotask-builder
```

따라서 **경로 변경과 Naming 변경을 같은 작업으로 수행하지 않는다.**

---

## 5. 전체 Phase 계획

현재 기본 Phase 계획:

```text
Baseline
  ↓
Phase 1  Private GitHub 업로드
  ↓
Phase 2  로컬 경로 Migration
  ↓
Phase 3  Skill Naming 정리
  ↓
Phase 4  필요한 Skill만 그룹 Promote
```

다만 사용자는 현재 퇴근하여 사내 PC에서 직접 Phase 1 작업을 할 수 없는 상황이다.

따라서 새 대화에서는 아래를 우선 검토한다.

```text
Phase 2의 일부 또는 전체를
skill-updater + job-list + safe-skill-migration
을 활용하여 야간 무인으로 먼저 수행할 수 있는가?
```

---

# 6. Baseline — 모든 변경 전에 수행해야 할 것

Baseline에서는 파일을 이동/삭제/rename하지 않는다.

먼저 현재 상태를 기계적으로 inventory한다.

필수 확인 대상:

```text
~/.claude/skills/<skill>/SKILL.md
~/.claude/main/<skill>/...
기타 Skill별 현재 실제 runtime/data path

Skill version
skill-updater 등록 상태
skillsilent 등록/contract
job-list dependency
Skill 간 호출 이름
Knowledge Store root
SLTE_KNOWLEDGE_HOME 설정 여부
```

가능하면 manifest 형태로 기록한다.

예:

```json
{
  "skill": "slte-knowledge-manager",
  "version": "0.4.4",
  "skill_entry": "~/.claude/skills/slte-knowledge-manager/SKILL.md",
  "current_data_root": "~/.claude/main/slte-knowledge-manager",
  "target_skill_root": "~/l1sw-skills/private-skills/slte-knowledge-manager",
  "target_knowledge_root": "~/l1sw-knowledge",
  "migration_status": "NOT_STARTED"
}
```

Baseline의 목적은:

```text
변경 전 상태를 언제든 재현/rollback할 수 있게 만드는 것
```

이다.

---

# 7. Phase 1 — GitHub 업로드 원칙

Phase 1을 수행할 때는 **현재 사내 PC runtime을 변경하지 않는다.**

변경:

```text
GitHub repo 생성
현재 Skill source COPY
Knowledge approved data filtered COPY
.gitignore
secret scan
manifest/checksum
commit/push
```

변경 금지:

```text
Skill rename
현재 실행 경로
~/.claude/skills/<skill>/SKILL.md 위치
skill-updater 등록 이름
skillsilent dependency 이름
job-list Skill 이름
Knowledge runtime root
기존 ~/.claude/main 데이터
```

Phase 1 완료 조건:

```text
GitHub가 없어져도 현재 사내 PC Skill들이 동일하게 정상 동작해야 한다.
```

---

# 8. Phase 2 — 로컬 경로 Migration 원칙

목표:

```text
Skill implementation
→ ~/l1sw-skills/private-skills/<skill>/

Knowledge DB
→ ~/l1sw-knowledge/
```

단:

```text
~/.claude/skills/<skill>/SKILL.md
```

는 유지한다.

---

## 8.1 가장 중요한 원칙: MOVE 금지, COPY 우선

금지:

```text
old → MOVE → new
```

권장:

```text
old
 ├─ 그대로 보존
 └─ COPY → new
```

새 경로가 충분히 검증된 뒤에만 legacy를 archive한다.

즉 일정 기간:

```text
OLD = rollback source
NEW = candidate/active
```

두 벌을 유지한다.

---

## 8.2 Knowledge Manager migration은 override 우선

Knowledge Manager는 `SLTE_KNOWLEDGE_HOME` override를 지원하는 구조가 있으므로, 기본 경로 코드를 처음부터 강제 수정하기보다 override를 우선 사용한다.

개념:

```text
OLD
~/.claude/main/slte-knowledge-manager/

COPY
        ↓

NEW
~/l1sw-knowledge/
```

테스트 시:

```text
SLTE_KNOWLEDGE_HOME=~/l1sw-knowledge
```

만 적용하여 새 Store를 사용하게 한다.

문제가 발생하면 env override를 제거하여 즉시 OLD Store로 rollback할 수 있어야 한다.

---

## 8.3 Knowledge migration 검증 순서

단순 read 성공만으로 migration 완료 처리하지 않는다.

최소 검증:

```text
1. Store load
2. 기존 APPROVED Knowledge 조회
3. branch filtering
4. deterministic query
5. candidate 생성
6. approval flow
7. 신규 rule 저장
8. 재실행 후 신규 rule 조회
9. issue-analyzer 등 downstream에서 APPROVED Knowledge 조회
10. 기존 결과와 주요 digest/건수 비교
```

---

# 9. GitHub / Knowledge 보안 정책

Private repository여도 secret 값은 commit 금지.

저장 금지:

```text
token 실제값
PAT
API key
cookie
password
Authorization header 실제값
client secret
proxy 인증 비밀값
```

환경변수 이름/설정 존재 여부만 저장 가능.

첫 push 전 권장 Gate:

```text
COPY
 ↓
STAGING
 ↓
path allowlist
 ↓
secret scan
 ↓
manifest
 ↓
SHA256/checksum
 ↓
git add
 ↓
git diff --cached 검토
 ↓
commit
 ↓
push
```

Secret pattern 예:

```text
Authorization
Bearer
token
password
passwd
PAT
cookie
client_secret
proxy credential
```

탐지 시 자동 push 금지.

---

# 10. Knowledge Repo에서 Git 대상/제외 대상

기본 방향:

| 데이터 | Git |
|---|---|
| APPROVED Knowledge | O |
| schema/catalog | O |
| responsibility catalog | O |
| knowledge manifest | O |
| candidates | 정책에 따라 |
| indexes | 재생성 가능 여부에 따라 |
| runs/checkpoints | X |
| runtime | X |
| cache | X |
| output | X |
| logs | X |
| migration backup | X |
| Wiki raw snapshots | 기본 X |
| secrets | 절대 X |

Wiki MCP 결과는 현재 `REFERENCE_ONLY`, `decision_evidence=false` 경계를 유지한다.

Wiki raw response를 APPROVED Knowledge와 같은 자산으로 취급하지 않는다.

---

# 11. 현재 퇴근 상태에서 검토할 야간 자동화

사용자가 언급한 사용 가능 자산:

```text
skill-updater
job-list v0.1.6
safe-skill-migration v0.1.1
```

목표는 우선:

```text
Phase 2를 야간에 안전하게 선행할 수 있는지 검토
```

이다.

단, 새 대화에서 실제 패키지 계약/코드를 확인하기 전에는
`safe-skill-migration`이 아래 신규 목표 경로를 지원한다고 가정하지 않는다.

```text
~/l1sw-skills/private-skills/
~/l1sw-knowledge/
```

---

## 11.1 권장 야간 실행 범위

처음부터 destructive migration을 수행하지 않는다.

권장 순서:

```text
JOB 1: inventory / dry-run
        ↓ 성공

JOB 2: target directory 생성
        ↓ 성공

JOB 3: COPY only
        ↓ 성공

JOB 4: checksum / file count / manifest 비교
        ↓ 성공

JOB 5: read-only validation
        ↓ 성공

STOP
```

가능하면 첫 야간에는 여기까지만 수행한다.

**기존 path 삭제/rename/cleanup은 하지 않는다.**

---

## 11.2 첫 야간에 피해야 할 작업

```text
기존 ~/.claude/main 삭제
기존 Skill folder 삭제
기존 SKILL.md 이동
Skill rename
skill-updater target rename
skillsilent contract rename
job-list dependency rename
GitHub push
Knowledge destructive migration
OLD store write disable
```

즉 첫 야간 목표는:

```text
새 구조를 안전하게 미리 만들어두고
기존 구조는 완전히 보존
```

이다.

---

# 12. skill-updater / job-list / safe-skill-migration 역할 후보

새 대화에서 실제 코드 확인 후 확정해야 하지만,
개념적인 역할 분리는 다음이 적절하다.

```text
skill-updater
= 원격 최신 Skill/job 자산 확보 + job_sync trigger

job-list
= one-shot migration 작업 전달/실행 orchestration

safe-skill-migration
= 실제 COPY / verify / rollback-aware migration engine
```

중요:

```text
skill-updater가 직접 migration logic을 가져서는 안 됨
job-list가 migration 세부 로직을 구현해서도 안 됨
safe-skill-migration이 실제 filesystem migration 책임
```

각 Skill의 책임 경계를 유지한다.

---

# 13. 야간 자동화에 필요한 안전 조건

실제 수행 전에 최소 아래 조건 확인.

```text
1. 동일 job revision 재실행 시 idempotent한가
2. 중간 실패 후 resume 가능한가
3. 이미 복사된 파일을 안전하게 처리하는가
4. source를 절대 삭제하지 않는 copy-only mode가 있는가
5. target collision 시 overwrite 정책이 안전한가
6. checksum/file count validation이 있는가
7. 실패 시 source 상태가 변하지 않는가
8. 로그/결과가 다음 날 확인 가능하게 남는가
9. job-list 실패가 updater 전체를 stuck시키지 않는가
10. skillsilent 승인 질문 없이 야간 실행 가능한가
```

하나라도 불명확하면 destructive 단계는 수행하지 않고 dry-run/inventory까지만 한다.

---

# 14. Rollback 원칙

Phase별 rollback 단위를 하나로 유지한다.

| 단계 | 변경 대상 | Rollback |
|---|---|---|
| Baseline | 없음 | 불필요 |
| GitHub upload | Git만 | commit/repo rollback |
| Path migration | path/config/env | legacy root 재활성화 |
| Naming | Skill identity | old-name alias |
| Promotion | distribution | private version 재활성화 |

특히 migration 시:

```text
DELETE를 rollback 방법으로 사용하지 않는다.
```

OLD source 자체가 rollback source가 되어야 한다.

---

# 15. 새 대화에서 우선 수행할 분석

새 대화에서는 다음 파일/Skill을 제공하고 실제 계약을 확인한다.

```text
1. 현재 skill-updater 최신 버전
2. job-list_v0_1_6_0805.zip
3. safe-skill-migration_v0_1_1_20260803.zip
```

가능하면 현재 구조에 영향을 받는 핵심 Skill도 함께 제공:

```text
slte-knowledge-manager
skillsilent
autotask-builder
```

분석 목표:

```text
A. job-list가 safe-skill-migration을 one-shot으로 호출 가능한가
B. safe-skill-migration이 현재 source path를 어떻게 탐색하는가
C. 신규 target root override를 받을 수 있는가
D. COPY_ONLY / DRY_RUN / VERIFY 모드가 있는가
E. idempotent/resume/rollback 정책
F. Knowledge DB를 일반 Skill migration과 분리할 수 있는가
G. 다음날 결과를 어디에서 확인하는가
H. updater job_sync 재수행 시 동일 revision을 다시 실행하지 않는가
```

---

# 16. 새 대화에서의 1차 목표

사용자가 퇴근한 상태이므로,
새 대화의 첫 목표는 **실제 migration을 즉시 실행하도록 만드는 것**이 아니다.

첫 목표:

```text
현재 세 Skill의 계약을 분석하고,
오늘 밤 무인으로 실행해도 안전한 최소 작업 범위를 결정한다.
```

권장 판정:

```text
SAFE
→ inventory + copy + validation job 작성 가능

CONDITIONAL
→ dry-run only

UNSAFE
→ 오늘은 job 등록하지 않고 수정안만 준비
```

---

# 17. 권장 첫 야간 Job 컨셉

실제 코드 검증 후 가능한 경우에만 적용.

```text
[Migration Pre-stage]

1. 기존 Skill/Knowledge source inventory
2. target root existence/create
3. source → target COPY
4. source/target file count 비교
5. 중요 파일 SHA256 비교
6. migration report 작성
7. 기존 source/path/env는 변경하지 않음
8. 완료 후 STOP
```

결과 예:

```text
PASS
PARTIAL
FAILED_SAFE
```

`FAILED_SAFE` 조건:

```text
실패했지만 기존 source/runtime에는 변경 없음
```

이 보장이 매우 중요하다.

---

# 18. 금지 사항

새 대화에서 아래 과거안을 다시 사용하지 않는다.

```text
~/l1sw-skills/private/<skill>/
~/l1sw-skills/private/skills/<skill>/
~/l1sw-skills/private-knowledge/
```

현재 기준:

```text
~/l1sw-skills/private-skills/<skill>/
~/l1sw-knowledge/
```

또한:

```text
~/.claude/skills/<skill>/SKILL.md
```

는 유지한다.

---

# 19. 최종 목표 구조

```text
HOME
│
├─ .claude/
│  └─ skills/
│     ├─ code-analyzer/
│     │  └─ SKILL.md
│     ├─ issue-analyzer/
│     │  └─ SKILL.md
│     └─ slte-knowledge-manager/
│        └─ SKILL.md
│
├─ l1sw-skills/
│  └─ private-skills/
│     ├─ code-analyzer/
│     ├─ issue-analyzer/
│     ├─ slte-knowledge-manager/
│     ├─ code-fix/
│     └─ ...
│
└─ l1sw-knowledge/
   ├─ current/
   ├─ candidates/
   ├─ catalogs/
   ├─ indexes/
   └─ ...
```

GitHub:

```text
Private Skills Repo
└─ private-skills/
   └─ <skill>/

Private Knowledge Repo
└─ Knowledge Store
```

향후:

```text
private-skills/<skill>
        ↓ Promote
group l1sw-skills/dev-skills 또는 shared-skills
```

Knowledge는 별도로 유지/승격한다.

---

# 20. 새 대화에 바로 사용할 요청문

아래 요청으로 시작한다.

```text
첨부한 handoff 문서를 현재 확정 기준으로 사용해줘.

지금은 퇴근해서 사내 PC를 직접 조작할 수 없다.
현재 skill-updater, job-list v0.1.6, safe-skill-migration v0.1.1을 활용해서
Phase 2의 일부를 야간 무인으로 안전하게 선행할 수 있는지 검토하고 싶다.

우선 세 Skill의 실제 구현/계약을 분석해줘.

최우선 조건:
1. 기존 runtime 동작을 깨뜨리지 않을 것
2. MOVE/DELETE 금지, COPY 우선
3. 기존 ~/.claude/skills/<skill>/SKILL.md 유지
4. Skill target은 ~/l1sw-skills/private-skills/<skill>/
5. Knowledge target은 ~/l1sw-knowledge/
6. Skill rename은 아직 하지 않음
7. GitHub push도 이번 야간 migration과 분리
8. 실패해도 기존 source/runtime이 그대로 남는 FAILED_SAFE 구조
9. 가능하면 첫 야간은 inventory → COPY → verify까지만
10. job-list 재실행/업데이터 재수행에서도 idempotent 해야 함

분석 후 아래 중 하나로 판정해줘:
- SAFE: 오늘 밤 copy+verify까지 무인 수행 가능
- CONDITIONAL: dry-run/inventory까지만 가능
- UNSAFE: 현재 버전으로는 야간 수행 금지

필요하면 safe-skill-migration 또는 job-list/skill-updater 수정안을 제안해줘.
```

---

## 21. 핵심 한 줄

```text
지금은 "새 구조로 전환"보다
"기존 구조를 건드리지 않은 채 새 구조를 안전하게 미리 만들어두는 것"이 우선이다.
```
