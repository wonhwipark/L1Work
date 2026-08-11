# 사내 Private Skill Hub 운영 전환 프롬프트

## 목적

이 문서는 현재까지 진행한 Private Skill 마이그레이션/배포 작업의 상태와 향후 사내 Private GitHub 운영 원칙을 다음 작업 세션에 정확히 인계하기 위한 실행 프롬프트다.

가장 중요한 원칙:

```text
사내 Private GitHub 경로에서는 skill-updater 개념을 사용하지 않는다.
```

`skill-updater`는 사외 Git 기반 배포에서만 사용하는 별도 체계다.

사내 배포/설치는 아래 전용 도구만 사용한다.

```text
private-skill-publisher
private-skill-installer
```

---

## 1. 최종 사내 아키텍처

```text
사내 Private GitHub
= Private Skill source/package/version/distribution SSOT
        │
        ├─ skills/
        │   └─ 업무 Private Skill
        │
        ├─ tools/
        │   ├─ private-skill-publisher
        │   └─ private-skill-installer
        │
        ├─ registry.json
        │
        └─ manifests/
            ├─ repository-manifest.json
            └─ checksums.json
```

로컬 설치/실행 구조:

```text
사내 Private GitHub
        ↓
private-skill-installer
        ↓
~/.claude/skills/<skill>/
= installed package + SKILL.md + skillsilent metadata
        ↓
~/l1sw-skills/private-skills/<skill>/
= actual executable implementation runtime
        ↓
skillsilent
```

Persistent/Knowledge 구조:

```text
~/.claude/main/<skill>/
= persistent/runtime/output/state/data

~/l1sw-knowledge/
= approved persistent Knowledge SSOT
```

이 경계들을 절대 혼합하지 않는다.

---

## 2. 사내에서 금지되는 updater 개념

다음 흐름은 사내에서는 사용하지 않는다.

```text
GitHub
→ skill-updater
→ install/update
```

다음 용어/단계도 사내 workflow에서 제거한다.

```text
GITHUB_TO_UPDATER_CANARY
UPDATER_CANARY
SKILL_UPDATER_INTERNAL
UPDATER_REPRODUCIBILITY
```

사내에서 올바른 표현:

```text
PRIVATE_HUB_INSTALLER_CANARY
PRIVATE_HUB_INSTALL
PRIVATE_HUB_PUBLISH
PRIVATE_HUB_REPRODUCIBILITY
```

`skill-updater` 관련 코드, 문서, NEXT_STEP 값, 테스트, 결과 필드가 사내 Private Hub 경로에 남아 있으면 legacy residue로 간주하고 제거 또는 교정한다.

단, 사외용 `skill-updater` 자체를 삭제하거나 수정하지 않는다.

```text
EXTERNAL_SKILL_UPDATER_POLICY=NO_TOUCH
```

---

## 3. 사내 GitHub Repository

권장 repository 이름:

```text
l1sw-private-skills
```

권장 구조:

```text
l1sw-private-skills/
├─ README.md
├─ registry.json
│
├─ skills/
│  ├─ code-analyzer/
│  ├─ code-fix/
│  ├─ doc-converter/
│  ├─ hld-code-compare/
│  ├─ hld-code-implement/
│  ├─ hld-composer/
│  ├─ issue-analyzer/
│  ├─ issue-fix-implement/
│  ├─ l1_fla/
│  ├─ l1-sam-fixer/
│  ├─ p4-code-owner/
│  ├─ p4-fix-kb/
│  ├─ slte-knowledge-manager/
│  └─ slte-port-impact-analyzer/
│
├─ tools/
│  ├─ private-skill-installer/
│  └─ private-skill-publisher/
│
└─ manifests/
   ├─ repository-manifest.json
   └─ checksums.json
```

역할:

```text
skills/
= 업무 Private Skill

tools/
= distribution infrastructure
```

Installer/Publisher는 Private 14에 포함하지 않는다.

---

## 4. 엄격한 Private Skill 14 Allowlist

처리 가능한 업무 Skill은 아래 14개뿐이다.

```text
code-analyzer v0.13.19
code-fix v0.4.5
doc-converter v0.2.0
hld-code-compare v0.10.4
hld-code-implement v0.5.9
hld-composer v0.4.13
issue-analyzer v0.11.5
issue-fix-implement v0.3.1
l1_fla v0.2.0
l1-sam-fixer v0.2.14
p4-code-owner v0.6.0
p4-fix-kb v0.2.2
slte-knowledge-manager v0.4.5
slte-port-impact-analyzer v0.8.23
```

정책:

```text
PRIVATE14_ONLY=YES
GROUP_COMMON_SKILL_POLICY=NO_TOUCH
UNLISTED_SKILL_POLICY=NO_TOUCH
```

Group/Common/Shared Skill에는 다음을 절대 수행하지 않는다.

```text
copy
repair
overwrite
delete
move
rename
reconcile
activate
execution_root 변경
manifest 변경
register/unregister
cleanup
quarantine
version 변경
publish
install
```

필요하면 dependency availability에 대한 read-only 확인만 허용한다.

---

## 5. Publisher 역할

`private-skill-publisher`는 로컬 Private Skill을 사내 GitHub로 올리는 전용 도구다.

사용자 입력:

```text
1. 업로드할 Skill 선택
2. 사내 Private Git repository URL
```

선택 단위:

```text
USER_SELECTION=SKILL_ONLY
PER_FILE_USER_SELECTION=NO
```

Skill 내부 파일은 Publisher가 자동으로 결정한다.

기본 방식:

```text
PER-SKILL MINIMAL PACKAGE
```

포함 후보:

```text
SKILL.md
VERSION
skillsilent/manifest.json
skillsilent/contract.json
skillsilent/policy.json
managed implementation assets
dependency metadata
explicit local runtime references
```

제외:

```text
~/.claude/main/**
~/l1sw-knowledge/**

runtime/
output/
history/
cache/
backup/
quarantine/
candidates/
migration data

tests/              # 배포에 불필요한 경우
examples/           # 배포에 불필요한 경우
release notes       # runtime에 불필요한 경우
validation docs     # runtime에 불필요한 경우

PAT
password
token
credential
cookies
.env
private keys
```

Publisher는 선택된 Skill만 다음 위치에 반영한다.

```text
skills/<skill>/
```

미선택 Skill과 기타 repository 내용은 NO_TOUCH다.

Publisher 성공 시 갱신:

```text
registry.json
manifests/checksums.json
manifests/repository-manifest.json
tools/private-skill-installer/
tools/private-skill-publisher/
```

Git 인증 정책:

```text
PAT 입력 요청=NO
password 입력 요청=NO
URL 내 credential=금지
기존 Git Credential Manager 또는 SSH 사용
```

---

## 6. Installer 역할

`private-skill-installer`는 사내 Private GitHub에서 로컬 PC로 Skill을 직접 설치하는 전용 도구다.

흐름:

```text
사내 Git
→ registry.json 조회
→ 설치 가능한 Private Skill 목록 표시
→ 사용자 Skill 선택
→ checksum 검증
→ package 설치
→ managed implementation sync
→ skillsilent route 검증
→ 결과 판정
```

설치 경로:

```text
~/.claude/skills/<skill>/
```

실행 implementation:

```text
~/l1sw-skills/private-skills/<skill>/
```

Persistent:

```text
~/.claude/main/<skill>/
```

정책:

```text
PERSISTENT_MAIN_POLICY=NO_TOUCH
```

Knowledge:

```text
~/l1sw-knowledge/
```

정책:

```text
KNOWLEDGE_POLICY=NO_TOUCH
```

Installer는 `registry.json`과 `manifests/checksums.json`을 기준으로 version/path/file SHA를 검증한다.

---

## 7. 현재 완료된 단계

진행 흐름:

```text
Implementation Repair
→ Activation
→ Private-14 Final Validate
→ Knowledge Migration Prepare
→ Knowledge Activate / Functional Validate
→ Macro Phase 2 Final Gate
→ Private Hub staging/publish
```

v0.3.24 최종 설계에는 기존 v0.3.23 기능이 앞부분에 통합되어 있다.

```text
v0.3.22 PASS
→ v0.3.24
   ├ Knowledge active path 전환
   ├ Knowledge 기능 검증
   ├ Private cross-skill 검증
   ├ Macro Phase 2 Final Gate
   ├ Private Skill minimal packaging
   ├ 사용자 Skill 선택
   ├ repository URL 입력
   ├ Publisher 실행
   ├ registry/checksum 갱신
   └ remote 검증
```

현재 사내 GitHub 업로드는 완료된 상태다.

따라서 현재 다음 단계는 updater canary가 아니다.

---

## 8. 현재 정확한 다음 단계

```text
PRIVATE_HUB_INSTALLER_CANARY
```

목적:

사내 GitHub에 올라간 Skill 중 1개를 `private-skill-installer`로 직접 설치하여 전체 사내 배포 경로를 검증한다.

절대 실행하지 않는다:

```text
skill-updater
GitHub→updater canary
사외 updater workflow
```

Canary 흐름:

```text
사내 l1sw-private-skills
        ↓
tools/private-skill-installer
        ↓
Canary Skill 1개
        ↓
registry.json verify
        ↓
checksums.json verify
        ↓
~/.claude/skills/<skill>/
        ↓
~/l1sw-skills/private-skills/<skill>/
        ↓
skillsilent route validate
        ↓
read-only functional smoke
```

---

## 9. Canary 필수 검증 항목

```text
REPOSITORY_LAYOUT=PASS
REGISTRY_LOAD=PASS
SKILL_ALLOWLIST=PASS
VERSION_VERIFY=PASS
CHECKSUM_VERIFY=PASS

PACKAGE_INSTALL=PASS
IMPLEMENTATION_SYNC=PASS
EXECUTION_ROOT_VERIFY=PASS

PERSISTENT_MAIN_TOUCHED=NO
KNOWLEDGE_TOUCHED=NO
GROUP_COMMON_SKILL_TOUCHED=NO

READ_ONLY_FUNCTIONAL_SMOKE=PASS
SKILL_UPDATER_USED=NO
```

추가로 다음 사이의 version/SHA 재현성을 확인한다.

```text
Git repository source
↔ installed package
↔ managed runtime implementation
```

---

## 10. Canary 실패 정책

Canary 실패 시 전체 Skill 확대 설치를 금지한다.

```text
FULL_INSTALL_ALLOWED=NO
```

Skill 단위 rollback만 수행한다.

권장 backup:

```text
~/.claude/main/private-skill-installer/backups/
```

Rollback 범위:

```text
~/.claude/skills/<canary>/
~/l1sw-skills/private-skills/<canary>/ 의 managed files
```

절대 rollback하지 않는 것:

```text
~/.claude/main/<skill>/
~/l1sw-knowledge/
다른 Private Skill
Group/Common/Shared Skill
```

---

## 11. Canary 성공 후

Canary PASS 후:

```text
PRIVATE_HUB_FULL_INSTALL_VALIDATE
```

동일 Installer로 GitHub에 실제 등록된 나머지 선택 Skill을 설치/검증한다.

전체 검증 후:

```text
PRIVATE_HUB_REPRODUCIBILITY=PASS
```

이후:

```text
Skill Naming 정리
→ 필요한 Skill만 Selected Group Promote
→ Steady State
```

---

## 12. Steady State

향후 사내 Private Skill 수정/배포:

```text
Private Skill source 수정
→ UT/self-check
→ semantic version bump
→ local functional validation
→ private-skill-publisher
→ 사내 l1sw-private-skills
→ registry/checksum 갱신
→ remote verification
```

설치/업데이트:

```text
사내 l1sw-private-skills
→ private-skill-installer
→ Skill 선택
→ SHA/version 검증
→ package install/update
→ implementation sync
→ skillsilent route validation
→ functional smoke
```

사내 생명주기에는 `skill-updater`가 없다.

---

## 13. 다음 작업 세션 실행 지시

다음 작업에서는 다음 순서로 진행한다.

1. 현재 사내 `l1sw-private-skills` repository 구조가 `L1SW_PRIVATE_SKILLS_MONOREPO_V1` 규약과 일치하는지 확인한다.
2. `registry.json`, `manifests/checksums.json`, `tools/private-skill-installer/`가 실제 repository에 존재하는지 확인한다.
3. `skill-updater` 또는 `GITHUB_TO_UPDATER_CANARY` 표현/로직을 사내 Private Hub 경로에서 사용하지 않는다.
4. 설치 가능한 Skill 목록에서 Canary 1개를 선정한다.
5. `private-skill-installer`를 사용하여 Canary Skill만 설치한다.
6. 다음 항목을 자동 판정한다.

```text
registry
version
checksum
package install
implementation sync
skillsilent execution_root
persistent preservation
Knowledge preservation
Group/Common NO_TOUCH
read-only smoke
```

7. PASS일 경우에만 나머지 선택 Skill로 확대한다.
8. 모든 결과는 사람이 긴 로그를 찾지 않아도 되도록 machine-readable summary를 남긴다.

권장 PASS 출력:

```text
RESULT=PASS
MODE=PRIVATE_HUB_INSTALLER_CANARY

CANARY_SKILL=<skill>

REGISTRY_LOAD=PASS
VERSION_VERIFY=PASS
CHECKSUM_VERIFY=PASS
PACKAGE_INSTALL=PASS
IMPLEMENTATION_SYNC=PASS
EXECUTION_ROOT_VERIFY=PASS
READ_ONLY_FUNCTIONAL_SMOKE=PASS

PERSISTENT_MAIN_TOUCHED=NO
KNOWLEDGE_TOUCHED=NO
GROUP_COMMON_SKILL_TOUCHED=NO
SKILL_UPDATER_USED=NO

READY_FOR_FULL_INSTALL_VALIDATE=YES
NEXT_STEP=PRIVATE_HUB_FULL_INSTALL_VALIDATE
```

실패 출력:

```text
RESULT=FAIL
MODE=PRIVATE_HUB_INSTALLER_CANARY

CANARY_SKILL=<skill>
FAILED_CHECKS=<machine-readable list>

ROLLBACK_PERFORMED=YES/NO
PERSISTENT_MAIN_TOUCHED=NO
KNOWLEDGE_TOUCHED=NO
GROUP_COMMON_SKILL_TOUCHED=NO
SKILL_UPDATER_USED=NO

READY_FOR_FULL_INSTALL_VALIDATE=NO
NEXT_STEP=FIX_PRIVATE_HUB_INSTALLER_CANARY
```

---

## 14. 절대 원칙

```text
INTERNAL_GIT_USE_SKILL_UPDATER=NO

PRIVATE_HUB_PUBLISHER=YES
PRIVATE_HUB_INSTALLER=YES

USER_SELECTION_UNIT=SKILL
USER_FILE_SELECTION=NO

PRIVATE14_ONLY=YES
GROUP_COMMON=NO_TOUCH
UNLISTED_SKILL=NO_TOUCH

PERSISTENT_MAIN=NO_TOUCH
KNOWLEDGE_STORE=NO_TOUCH

SECRET_TO_GIT=NO

CANARY_FIRST=YES
FULL_INSTALL_AFTER_CANARY_PASS=YES
```

이 원칙을 이후 모든 사내 Private Skill 설계, 코드, 문서, 테스트, 결과 필드, `NEXT_STEP` 값에 적용하라.
