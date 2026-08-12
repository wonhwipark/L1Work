# l1sw-private-skills 사내 GitHub Repository 생성 프롬프트
## 기준일: 2026-08-12
## 목적: Private Skill Hub Repository 최초 생성 및 기본 Scaffold 구성

아래 내용을 새 Claude Code / OpenCode 작업창에 그대로 입력해서 수행해줘.

---

# 0. 목표

사내 GitHub에 아직 존재하지 않는 다음 Private Repository를 새로 생성한다.

```text
Repository Name: l1sw-private-skills
Visibility: PRIVATE
Purpose: 개인 Private Skill의 버전 관리 / 배포 / 설치 / 복구
```

이 Repository는 실행 중 데이터 저장소가 아니다.

역할 구분:

```text
l1sw-private-skills
= Private Skill package / implementation distribution hub

~/.claude/skills/<skill>/
= 설치된 Skill package / SKILL.md / VERSION / skillsilent contract

~/l1sw-skills/private-skills/<skill>/
= 설치된 실제 implementation

~/l1sw-data/<skill>/
= 필요한 Skill만 사용하는 장기 Persistent

~/l1sw-knowledge/
= Shared L1 Knowledge authoritative live SSOT

l1sw-private-knowledge
= Knowledge용 별도 Private Repository
  (이번 작업에서는 생성하지 않음)
```

---

# 1. 절대 운영 원칙

```text
REPOSITORY=l1sw-private-skills
VISIBILITY=PRIVATE

INTERNAL_GIT_USE_SKILL_UPDATER=NO

GROUP_COMMON_SKILL_POLICY=NO_TOUCH
UNLISTED_SKILL_POLICY=NO_TOUCH

LEGACY_DELETE=NO
LEGACY_MODIFY=NO

CREDENTIAL_IN_URL=NO
PAT_IN_FILE=NO
PASSWORD_IN_FILE=NO
TOKEN_IN_FILE=NO

SKILL_UPLOAD_IN_THIS_PHASE=NO
```

이번 단계는 Repository 최초 생성 + 기본 디렉터리/manifest scaffold 생성까지만 수행한다.

아직 Active-12 Skill package를 실제 업로드하지 않는다.

Skill 실제 publish는 이후:

```text
FINAL_VALIDATE_V2
→ Local Reconcile
→ Knowledge Reconcile Close
→ Private Hub Repackage/Precheck
→ 사용자 승인
→ private-skill-publisher
```

순서에서 수행한다.

---

# 2. 작업 시작 전 확인

먼저 현재 환경을 READ ONLY로 확인한다.

확인:

```text
git --version
gh 사용 가능 여부
현재 GitHub host
현재 인증 상태
현재 사용자/organization namespace
동일 이름 repository 존재 여부
현재 local work root
```

사내 GitHub가 github.com이 아닌 Enterprise host이면 현재 configured host를 사용한다.

credential을 출력하지 않는다.

다음 값이 환경에서 자동 판단되지 않을 때만 사용자에게 질문한다.

```text
Q1. Repository를 어느 namespace에 생성할까요?

1. 현재 개인 계정
2. 사내 Organization
```

2번인데 Organization 이름을 알 수 없을 때만 이름을 질문한다.

Repository name은 다시 묻지 않는다.

```text
l1sw-private-skills
```

로 고정한다.

---

# 3. 기존 Repository 중복 검사

먼저 다음 Repository가 이미 존재하는지 확인한다.

```text
l1sw-private-skills
```

존재할 경우:

```text
RESULT=BLOCKED
REASON=REPOSITORY_ALREADY_EXISTS
```

로 중단한다.

기존 Repository를 삭제하거나 덮어쓰지 않는다.

존재하지 않을 때만 다음 단계로 진행한다.

---

# 4. Repository 생성

Repository 생성 조건:

```text
Name: l1sw-private-skills
Visibility: Private
Initialize README: NO 또는 local scaffold 기준
```

사내 정책상 가능하면 이미 인증된 공식 GitHub CLI 또는 사내 공식 Git client를 사용한다.

우선순위:

```text
1. 이미 인증된 gh CLI
2. 이미 구성된 Git remote / enterprise Git client
3. 그 외 안전한 공식 방식
```

금지:

```text
credential 포함 clone URL
PAT 직접 입력값을 script에 저장
token echo
credential logging
```

생성 성공 후 remote URL은 credential 없는 형태로만 출력한다.

---

# 5. Local Scaffold 생성

안전한 새 local work directory를 만든다.

권장 예:

```text
~/l1sw-private-skills-repo/
```

이미 존재하면 임의 삭제하지 않는다.

Repository 기본 구조:

```text
l1sw-private-skills/
├─ README.md
├─ registry.json
├─ skills/
│  └─ .gitkeep
├─ tools/
│  ├─ private-skill-installer/
│  │  └─ .gitkeep
│  └─ private-skill-publisher/
│     └─ .gitkeep
└─ manifests/
   ├─ repository-manifest.json
   └─ checksums.json
```

주의:

```text
현재 실제 Skill package는 skills/ 아래에 넣지 않는다.
현재 installer/publisher 구현도 자동으로 복사하지 않는다.
```

이번 단계는 scaffold만 생성한다.

---

# 6. README.md 최소 내용

README에는 다음 개념만 간단히 기록한다.

```text
# l1sw-private-skills

Private Skill distribution repository.

Purpose:
- Private Skill package/version management
- Private Skill distribution
- Installer/Publisher support
- Reproducible installation

Not used for:
- runtime output
- Skill persistent data
- Shared L1 Knowledge

Canonical runtime locations:
- Package: ~/.claude/skills/<skill>/
- Implementation: ~/l1sw-skills/private-skills/<skill>/
- Persistent when needed: ~/l1sw-data/<skill>/
- Shared Knowledge: ~/l1sw-knowledge/

Internal policy:
- skill-updater is not used for this repository.
```

README에 사용자 이름, PC 이름, token, 내부 credential을 넣지 않는다.

---

# 7. 초기 registry.json

아직 실제 Skill publish 전이므로 empty registry scaffold만 만든다.

```json
{
  "schema_version": 1,
  "repository": "l1sw-private-skills",
  "visibility": "private",
  "skills": []
}
```

현재 Active-12 목록을 아직 registry에 넣지 않는다.

---

# 8. 초기 repository-manifest.json

```json
{
  "schema_version": 1,
  "repository": "l1sw-private-skills",
  "status": "initialized",
  "skill_count": 0
}
```

---

# 9. 초기 checksums.json

```json
{
  "schema_version": 1,
  "files": {}
}
```

---

# 10. Secret / Safety Scan

첫 commit 전에 전체 repository를 검사한다.

검사 유형:

```text
password
passwd
PAT
token
api_key
api key
private key
BEGIN PRIVATE KEY
authorization
cookie
credential
machine-local auth
*.pem
*.key
.env
auth cache
temporary dump
```

실제 credential 또는 의심 값 발견 시:

```text
STOP
COMMIT=NO
PUSH=NO
```

---

# 11. Initial Commit

Secret/Safety Gate가 PASS했을 때만 initial commit 한다.

권장 commit message:

```text
Initialize private skill hub repository
```

포함:

```text
README.md
registry.json
skills/.gitkeep
tools/private-skill-installer/.gitkeep
tools/private-skill-publisher/.gitkeep
manifests/repository-manifest.json
manifests/checksums.json
```

실제 Skill ZIP/package는 포함하지 않는다.

---

# 12. Remote Push

Repository 생성과 local scaffold가 정상이고 secret scan이 PASS한 경우 initial commit을 remote에 push한다.

Push 후 최소 검증:

```text
remote exists
default branch exists
README exists
registry.json exists
manifests/repository-manifest.json exists
manifests/checksums.json exists
skills/ scaffold exists
tools/ scaffold exists
```

API 호출은 최소화한다.

---

# 13. 생성 완료 후 절대 하지 않을 것

이번 단계에서 아래 작업은 수행하지 않는다.

```text
Active-12 Skill publish
Remaining-4 ZIP publish
skillsilent publish
Private Knowledge publish
l1sw-private-knowledge 생성
Group/Common Skill 이동
skill-updater 등록
legacy 삭제
registry에 가짜 Skill entry 추가
installer/publisher 구현 임의 생성
```

---

# 14. 완료 결과 형식

성공 시:

```text
RESULT=PASS
MODE=PRIVATE_HUB_REPOSITORY_INITIALIZE

REPOSITORY=l1sw-private-skills
VISIBILITY=PRIVATE
REMOTE_CREATED=YES
INITIAL_COMMIT=PASS
INITIAL_PUSH=PASS

README=PASS
REGISTRY_SCAFFOLD=PASS
MANIFEST_SCAFFOLD=PASS
CHECKSUM_SCAFFOLD=PASS
SKILLS_SCAFFOLD=PASS
TOOLS_SCAFFOLD=PASS

SECRET_SCAN=PASS
SKILL_PACKAGES_UPLOADED=NO
SKILL_UPDATER_USED=NO
GROUP_COMMON_TOUCHED=NO
LEGACY_TOUCHED=NO

NEXT_STEP=RETURN_TO_PRIVATE_SKILL_FINAL_CLOSE_MASTER_WORKFLOW
```

실패 시:

```text
RESULT=FAIL
MODE=PRIVATE_HUB_REPOSITORY_INITIALIZE
FAILED_STAGE=<stage>
BLOCK_REASON=<reason>
REMOTE_CREATED=YES/NO
INITIAL_PUSH=YES/NO
PRODUCTION_SKILL_CHANGED=NO
LEGACY_CHANGED=NO
NEXT_STEP=<repair action>
```

---

# 15. 최종 실행 지시

위 정책에 따라 지금부터 수행해줘.

중요:

```text
Repository가 없으면 PRIVATE로 생성
Repository가 이미 있으면 overwrite하지 말고 BLOCKED
scaffold까지만 생성
Skill 실제 upload는 하지 않음
credential 저장/출력 금지
skill-updater 사용 금지
Group/Common NO_TOUCH
legacy NO_TOUCH
```

가능한 단계는 연속 수행하고, namespace처럼 실제로 결정 불가능한 값만 사용자에게 질문해줘.
