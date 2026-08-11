# `issue-analyzer` Private Hub Installer Canary + Functional Validation Prompt

## 목적

사내 Private Git repository에 이미 업로드된 `issue-analyzer`를 **사내 `private-skill-installer`로 다시 내려받아**, 현재 실사용 환경과 분리된 Canary 환경에 설치하고 무결성/버전/runtime/기능까지 검증한다.

이번 작업에서 가장 중요한 원칙:

```text
사내 Private Git 경로에서는 skill-updater를 절대 사용하지 않는다.
```

---

## 1. 고정 대상 및 절대 정책

```text
MODE=PRIVATE_HUB_INSTALLER_CANARY
CANARY_SKILL=issue-analyzer
EXPECTED_VERSION=0.11.5

INTERNAL_GIT_USE_SKILL_UPDATER=NO
PRIVATE_SKILL_INSTALLER_ONLY=YES

GROUP_COMMON_SKILL_POLICY=NO_TOUCH
UNLISTED_SKILL_POLICY=NO_TOUCH

CURRENT_PRODUCTION_PACKAGE=NO_TOUCH
CURRENT_PRODUCTION_RUNTIME=NO_TOUCH
CURRENT_PRODUCTION_PERSISTENT=NO_TOUCH
KNOWLEDGE_STORE=NO_TOUCH

USER_FILE_SELECTION=NO
BUSINESS_SIDE_EFFECT=NO
```

사내 배포 개념은 다음뿐이다.

```text
사내 Private Git
→ tools/private-skill-installer
→ ~/.claude/skills/<skill>/
→ ~/l1sw-skills/private-skills/<skill>/
→ skillsilent
```

이번 Canary에서는 현재 사용 중인 production 경로를 직접 덮어쓰지 않는다.

---

## 2. Production baseline: read-only only

현재 정상 사용 중인 경로:

```text
~/.claude/skills/issue-analyzer/
~/l1sw-skills/private-skills/issue-analyzer/
~/.claude/main/issue-analyzer/
~/l1sw-knowledge/
```

허용:

```text
read
stat
SHA256
tree manifest
version observation
```

금지:

```text
delete
move
rename
overwrite
repair
cleanup
activation 변경
manifest 변경
persistent 변경
Knowledge 변경
```

---

## 3. Canary 격리 Root

실행마다 고유한 Canary root를 만든다.

```text
<USER_HOME>/l1sw-private-hub-canary/issue-analyzer/<RUN_ID>/
```

예시:

```text
canary-root/
├─ user-home/
│  ├─ .claude/
│  │  ├─ skills/
│  │  │  └─ issue-analyzer/
│  │  └─ main/
│  │     └─ private-skill-installer/
│  └─ l1sw-skills/
│     └─ private-skills/
│        └─ issue-analyzer/
├─ fixture/
│  └─ sample_issue.md
└─ reports/
```

Installer 실행 subprocess에는 가능한 경우 아래 환경을 명시한다.

```text
HOME=<canary-root>/user-home
USERPROFILE=<canary-root>/user-home
CLAUDE_HOME=<canary-root>/user-home/.claude
CLAUDE_SKILLS_ROOT=<canary-root>/user-home/.claude/skills
PRIVATE_SKILLS_ROOT=<canary-root>/user-home/l1sw-skills/private-skills
L1SW_PRIVATE_SKILLS_ROOT=<same as PRIVATE_SKILLS_ROOT>
```

목적은 installer의 package/runtime/backup write가 Canary root 안에서만 발생하게 하는 것이다.

Windows에서는 bash를 사용하지 말고 PowerShell 또는 `python` 직접 실행을 사용한다.

---

## 4. 사용자 입력

사내 repository URL이 현재 context/environment에 없을 때만 한 번 질문한다.

```text
사내 l1sw-private-skills repository URL을 입력하세요.
```

그 외 질문 금지.

Canary Skill은 이미 고정되어 있다.

```text
issue-analyzer
```

파일 단위 선택을 사용자에게 요구하지 않는다.

---

## 5. Repository PRECHECK

사내 repository를 read-only clone/fetch하여 다음 구조를 확인한다.

```text
README.md
registry.json
skills/issue-analyzer/
tools/private-skill-installer/
manifests/repository-manifest.json
manifests/checksums.json
```

필수 repository contract:

```text
REPOSITORY_LAYOUT=L1SW_PRIVATE_SKILLS_MONOREPO_V1
```

`registry.json`에서 반드시 확인:

```text
skill = issue-analyzer
version = 0.11.5
path = skills/issue-analyzer
enabled = true
```

추가 필수 필드:

```text
files
managed_assets
package_digest
```

다음 중 하나라도 있으면 설치 전에 즉시 FAIL:

```text
issue-analyzer 없음
version != 0.11.5
path가 skills/issue-analyzer 밖을 가리킴
registry에 Private-14 외 업무 Skill 존재
symlink/path escape
checksum manifest 없음
private-skill-installer 없음
```

---

## 6. Repository checksum 검증

`manifests/checksums.json`을 기준으로 `registry.json`의 `issue-analyzer.files` 전부를 검증한다.

각 파일:

```text
exists
regular file
not symlink
SHA256 match
```

모두 일치해야 한다.

```text
CHECKSUM_VERIFY=PASS
```

불일치가 하나라도 있으면 installer를 실행하지 않는다.

---

## 7. Production baseline 캡처

Production `issue-analyzer`는 수정하지 않고 다음만 read-only로 수집한다.

```text
PRODUCTION_PACKAGE_EXISTS
PRODUCTION_PACKAGE_VERSION
PRODUCTION_SKILL_MD_SHA256
PRODUCTION_SKILLSILENT_MANIFEST_SHA256

PRODUCTION_RUNTIME_EXISTS
PRODUCTION_IMPLEMENTATION_MARKER
PRODUCTION_MANAGED_ASSETS

PRODUCTION_PERSISTENT_EXISTS
```

가능하면 `registry.json`의 `files` 목록을 기준으로 production package digest도 계산한다.

Git과 production이 다르더라도 production을 자동 수정하지 않는다.

보고만 한다.

```text
PRODUCTION_VS_GIT=IDENTICAL
```

또는

```text
PRODUCTION_VS_GIT=DIFFERENT
```

다를 경우 machine-readable diff를 남긴다.

---

## 8. Installer 자체 검증

사내 repository의 다음 파일을 사용한다.

```text
tools/private-skill-installer/install.py
```

먼저 Python syntax를 검증한다.

```text
python -m py_compile tools/private-skill-installer/install.py
```

성공 결과:

```text
INSTALLER_COMPILE=PASS
```

그다음 list 기능을 확인한다.

개념적 실행:

```text
python tools/private-skill-installer/install.py \
  --repo-url <INTERNAL_REPO_URL> \
  list
```

Windows에서는 동등한 PowerShell/python 직접 실행을 사용한다.

반드시 다음이 확인되어야 한다.

```text
issue-analyzer    0.11.5
```

결과:

```text
INSTALLER_LIST=PASS
```

---

## 9. 격리 Canary 설치

Canary environment를 명시한 subprocess에서만 설치한다.

개념적 명령:

```text
python tools/private-skill-installer/install.py \
  --repo-url <INTERNAL_REPO_URL> \
  install \
  --skills issue-analyzer \
  --yes
```

Production 환경에 write가 발생하면 즉시 FAIL이다.

설치 후 기대 경로:

```text
<canary-user-home>/.claude/skills/issue-analyzer/
<canary-user-home>/l1sw-skills/private-skills/issue-analyzer/
```

결과:

```text
PACKAGE_INSTALL=PASS
IMPLEMENTATION_SYNC=PASS
```

---

## 10. Canary package 검증

대상:

```text
<canary-user-home>/.claude/skills/issue-analyzer/
```

필수:

```text
VERSION == 0.11.5
SKILL.md 존재
VERSION 존재
skillsilent/manifest.json 존재
skillsilent/contract.json 존재
skillsilent/policy.json 존재
```

`registry.json`의 `files`와 비교하여:

```text
missing = 0
SHA mismatch = 0
```

이어야 한다.

결과:

```text
CANARY_PACKAGE_SHA_VERIFY=PASS
```

---

## 11. Managed implementation 검증

`registry.json`의 `managed_assets`를 기준으로 다음 Canary runtime을 검증한다.

```text
<canary-user-home>/l1sw-skills/private-skills/issue-analyzer/
```

각 managed asset에 대해:

```text
package source exists
runtime target exists
file set 동일
per-file SHA256 동일
```

이어야 한다.

Target-only unmanaged runtime 파일을 발견하더라도 자동 삭제하지 않는다.

결과:

```text
IMPLEMENTATION_SHA_VERIFY=PASS
```

---

## 12. implementation marker 검증

Canary runtime의:

```text
.implementation-version.json
```

을 확인한다.

필수 조건:

```text
skill = issue-analyzer
package_version = 0.11.5
repair_status = SUCCESS
assets == registry managed_assets
target_root == Canary runtime
```

결과:

```text
IMPLEMENTATION_MARKER=PASS
```

---

## 13. skillsilent execution_root contract 검증

Canary package의:

```text
skillsilent/manifest.json
```

을 읽는다.

정상 production contract가 portable path를 선언하는지 확인한다.

```text
~/l1sw-skills/private-skills/issue-analyzer/
```

Canary subprocess에서 `HOME`/`USERPROFILE`을 Canary user home으로 설정했을 때 이 경로가 Canary runtime으로 해석되는지 검증한다.

우선순위:

```text
1. manifest execution_root 확인
2. Canary environment 기준 path expand
3. expanded path == Canary runtime 확인
4. skillsilent가 alternate CLAUDE_HOME/Canary environment를 공식 지원할 때만 실제 route smoke
```

Production skillsilent registration/manifest를 수정해서 테스트하지 않는다.

필수 결과:

```text
EXECUTION_ROOT_CONTRACT=PASS
```

실제 alternate-home skillsilent route smoke가 안전하게 지원되면:

```text
SKILLSILENT_CANARY_ROUTE_SMOKE=PASS
```

공식 지원 여부를 확인할 수 없으면:

```text
SKILLSILENT_CANARY_ROUTE_SMOKE=NOT_EXECUTED_UNSUPPORTED
```

이 값 자체는 전체 FAIL 사유가 아니다. 단 `EXECUTION_ROOT_CONTRACT=PASS`는 필수다.

---

## 14. `issue-analyzer` 실제 기능 Canary

설치 확인만 하지 말고 **Canary 설치본의 실제 read-only 분석 기능을 1회 실행**한다.

단, undocumented command를 임의로 만들지 않는다.

먼저 Canary 설치본의 다음 파일을 읽는다.

```text
SKILL.md
skillsilent/contract.json
skillsilent/manifest.json
```

여기서 문서화된 safe read-only analysis entrypoint를 찾는다.

우선순위:

```text
1. documented direct Python entrypoint
2. documented CLI entrypoint
3. documented skillsilent action with Canary-home support
```

코드 수정, issue 생성/수정, Git write, 외부 업무 시스템 write가 필요한 action은 사용하지 않는다.

---

## 15. Functional Smoke Fixture

실제 업무 데이터 대신 synthetic fixture를 사용한다.

파일:

```text
<canary-root>/fixture/sample_issue.md
```

내용:

```markdown
# Sample Issue

## Title
Optional owner field causes configuration analysis failure

## Observed behavior
When a configuration entry does not contain an `owner` field,
the analyzer terminates with a missing-key style error instead of continuing.

## Expected behavior
The analyzer should treat `owner` as optional and continue analysis,
reporting that ownership information is unavailable.

## Reproduction
1. Create a minimal configuration object.
2. Include `name` and `version`.
3. Omit `owner`.
4. Run analysis.

## Constraints
- Read-only analysis only.
- Do not modify source files.
- Do not create a real issue.
- Do not call production business systems.
```

---

## 16. Functional Smoke 실행 기준

Canary 설치본에서 문서화된 safe entrypoint를 찾으면 `sample_issue.md`를 실제로 분석한다.

성공 조건:

```text
process/action completes successfully
analysis output exists
fixture unchanged
production file mutation 없음
Git mutation 없음
external issue create/update 없음
```

분석 결과는 최소한 다음 범주를 다뤄야 한다.

```text
problem/issue summary
likely failure point or investigation target
evidence/reproduction information
recommended next investigation/fix direction
```

정확한 출력 문구/포맷은 강제하지 않고 `issue-analyzer` 자체 contract를 따른다.

성공:

```text
READ_ONLY_FUNCTIONAL_SMOKE=PASS
```

---

## 17. Safe entrypoint가 없는 경우

Canary 설치본 문서에서 안전한 read-only 실행 방법을 찾을 수 없으면 명령을 추측하지 않는다.

결과:

```text
READ_ONLY_FUNCTIONAL_SMOKE=BLOCKED
BLOCK_REASON=NO_DOCUMENTED_SAFE_CANARY_ENTRYPOINT
```

이 경우 전체 RESULT를 PASS로 만들지 않는다.

Production `issue-analyzer`를 대신 실행해서 Canary 기능 검증 PASS로 처리하지 않는다.

---

## 18. Production NO-TOUCH 사후 검증

Canary 전/후 Production baseline을 비교한다.

반드시:

```text
PRODUCTION_PACKAGE_CHANGED=NO
PRODUCTION_RUNTIME_CHANGED=NO
PRODUCTION_PERSISTENT_CHANGED=NO
KNOWLEDGE_CHANGED=NO
GROUP_COMMON_SKILL_TOUCHED=NO
```

검증 방법:

```text
Production package 관찰 대상 SHA 전/후 비교
Production runtime managed asset SHA 전/후 비교
persistent read-only metadata/digest 비교 가능한 범위에서 수행
Knowledge write operation 없음 확인
Group/Common/Shared 경로 enumerate/mutate 하지 않음
```

---

## 19. `skill-updater` 미사용 검증

이번 Canary에서 다음 실행 개념이 없어야 한다.

```text
skill-updater
GITHUB_TO_UPDATER_CANARY
UPDATER_CANARY
```

정책 문서의 문자열 자체는 사용 여부 검사에서 제외한다.

결과:

```text
SKILL_UPDATER_USED=NO
```

사외용 `skill-updater` 설치물 자체를 삭제/수정하지 않는다.

```text
EXTERNAL_SKILL_UPDATER_POLICY=NO_TOUCH
```

---

## 20. Canary cleanup 정책

검증 완료 후 Canary root는 증거 보존을 위해 자동 삭제하지 않는다.

```text
CANARY_CLEANUP_PERFORMED=NO
```

사용자가 명시적으로 승인하기 전까지 보존한다.

Production cleanup은 절대 수행하지 않는다.

---

## 21. PASS Gate

아래가 모두 만족되어야 최종 PASS다.

```text
REPOSITORY_LAYOUT=PASS
REGISTRY_LOAD=PASS
SKILL_ALLOWLIST=PASS
VERSION_VERIFY=PASS
CHECKSUM_VERIFY=PASS

INSTALLER_COMPILE=PASS
INSTALLER_LIST=PASS

PACKAGE_INSTALL=PASS
CANARY_PACKAGE_SHA_VERIFY=PASS
IMPLEMENTATION_SYNC=PASS
IMPLEMENTATION_SHA_VERIFY=PASS
IMPLEMENTATION_MARKER=PASS

EXECUTION_ROOT_CONTRACT=PASS
READ_ONLY_FUNCTIONAL_SMOKE=PASS

PRODUCTION_PACKAGE_CHANGED=NO
PRODUCTION_RUNTIME_CHANGED=NO
PRODUCTION_PERSISTENT_CHANGED=NO
KNOWLEDGE_CHANGED=NO
GROUP_COMMON_SKILL_TOUCHED=NO

SKILL_UPDATER_USED=NO
```

`SKILLSILENT_CANARY_ROUTE_SMOKE=NOT_EXECUTED_UNSUPPORTED`는 허용한다.

---

## 22. 최종 machine-readable PASS 출력

```text
RESULT=PASS
MODE=PRIVATE_HUB_INSTALLER_CANARY
CANARY_SKILL=issue-analyzer
EXPECTED_VERSION=0.11.5

REPOSITORY_LAYOUT=PASS
REGISTRY_LOAD=PASS
SKILL_ALLOWLIST=PASS
VERSION_VERIFY=PASS
CHECKSUM_VERIFY=PASS

INSTALLER_COMPILE=PASS
INSTALLER_LIST=PASS

PACKAGE_INSTALL=PASS
CANARY_PACKAGE_SHA_VERIFY=PASS
IMPLEMENTATION_SYNC=PASS
IMPLEMENTATION_SHA_VERIFY=PASS
IMPLEMENTATION_MARKER=PASS

EXECUTION_ROOT_CONTRACT=PASS
SKILLSILENT_CANARY_ROUTE_SMOKE=PASS_OR_NOT_EXECUTED_UNSUPPORTED
READ_ONLY_FUNCTIONAL_SMOKE=PASS

PRODUCTION_VS_GIT=IDENTICAL_OR_DIFFERENT
PRODUCTION_PACKAGE_CHANGED=NO
PRODUCTION_RUNTIME_CHANGED=NO
PRODUCTION_PERSISTENT_CHANGED=NO
KNOWLEDGE_CHANGED=NO
GROUP_COMMON_SKILL_TOUCHED=NO

SKILL_UPDATER_USED=NO
CANARY_CLEANUP_PERFORMED=NO

READY_FOR_FULL_INSTALL_VALIDATE=YES
NEXT_STEP=PRIVATE_HUB_FULL_INSTALL_VALIDATE
```

---

## 23. 최종 machine-readable FAIL 출력

```text
RESULT=FAIL
MODE=PRIVATE_HUB_INSTALLER_CANARY
CANARY_SKILL=issue-analyzer

FAILED_CHECKS=<machine-readable list>
BLOCK_REASON=<reason>

PRODUCTION_PACKAGE_CHANGED=NO
PRODUCTION_RUNTIME_CHANGED=NO
PRODUCTION_PERSISTENT_CHANGED=NO
KNOWLEDGE_CHANGED=NO
GROUP_COMMON_SKILL_TOUCHED=NO
SKILL_UPDATER_USED=NO

READY_FOR_FULL_INSTALL_VALIDATE=NO
NEXT_STEP=FIX_PRIVATE_HUB_INSTALLER_CANARY
```

---

## 24. 사람이 볼 짧은 결과 요약

machine-readable 결과 뒤에 10줄 이내로 다음만 출력한다.

```text
- 사내 Git에서 issue-analyzer v0.11.5 조회 성공 여부
- registry/checksum 검증 여부
- 격리 Canary 설치 성공 여부
- runtime implementation SHA 일치 여부
- synthetic issue 실제 분석 성공 여부
- production 보존 여부
- Knowledge/Group Common 보존 여부
- skill-updater 미사용 여부
- 전체 설치 검증으로 확대 가능한지 여부
```

사용자에게 긴 로그를 찾아 읽으라고 요구하지 않는다.

---

## 25. 실행 순서 요약

1. 사내 repository 구조와 `issue-analyzer` registry/checksum 검증.
2. 현재 production `issue-analyzer` baseline read-only 캡처.
3. 별도 Canary user-home 생성.
4. repository의 `private-skill-installer`로 `issue-analyzer`만 Canary 설치.
5. package SHA/version 검증.
6. managed runtime SHA 및 implementation marker 검증.
7. execution_root portable contract 검증.
8. Canary `SKILL.md`/contract에서 safe read-only entrypoint 탐색.
9. synthetic `sample_issue.md`를 실제 Canary `issue-analyzer`로 분석.
10. Production/Knowledge/Group Common NO_TOUCH 재검증.
11. `SKILL_UPDATER_USED=NO` 확인.
12. PASS일 때만 `PRIVATE_HUB_FULL_INSTALL_VALIDATE`로 진행.

문제 발견 시 Production을 수정해서 해결하지 말고 fail closed 한다.
