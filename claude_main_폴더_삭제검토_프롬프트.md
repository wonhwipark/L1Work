# `.claude/main` 폴더 삭제 가능 여부 조사 및 처리 프롬프트

> 사용법: 아래 `---` 아래 전체를 Claude Code / OpenCode 세션에 그대로 붙여넣는다.
> 대상 경로는 `TARGET` 변수에 실제 절대경로를 넣어 사용한다.

---

## 역할

너는 로컬 개발 환경의 디스크 정리를 담당한다. 24GB 규모의 `.claude/main` 디렉터리가
삭제 가능한지 **증거 기반으로 판정**하고, 안전한 경우에만 사용자 승인을 받아 제거한다.

**TARGET = `<여기에 .claude/main 절대경로 입력>`**

---

## 절대 규칙 (위반 금지)

1. **STEP 5 판정 보고 전에는 어떤 삭제·이동·수정도 하지 않는다.** STEP 0~4는 읽기 전용이다.
2. `rm -rf` 를 즉시 실행하지 않는다. 삭제는 반드시 **격리(이름 변경) → 검증 → 최종 삭제** 순서를 따른다.
3. TARGET이 git worktree로 판명되면 `rm -rf` 대신 반드시 `git worktree remove` 를 사용한다.
4. **심볼릭 링크 / NTFS junction 을 먼저 확인한다.** 링크가 포함된 경우, 링크가 가리키는 원본이
   삭제될 수 있으므로 링크를 먼저 끊고 진행한다.
5. 판정이 `CONDITIONAL` 또는 `DO_NOT_DELETE` 이면 삭제를 실행하지 않고 사용자에게 결정을 넘긴다.
6. 불확실하면 삭제하지 않는다. 24GB 회수보다 유실 방지가 우선이다.

---

## STEP 0 — 환경 확인 (읽기 전용)

- OS 판별 (Windows / macOS / Linux). 이후 명령은 해당 OS 문법으로 실행한다.
- TARGET 이 실제 존재하는지, 심볼릭 링크/junction 인지 확인한다.

```bash
# macOS / Linux
ls -ld "$TARGET"
readlink -f "$TARGET"
find "$TARGET" -maxdepth 3 -type l -print | head -50
```

```powershell
# Windows PowerShell
Get-Item $TARGET | Select-Object FullName, LinkType, Target
Get-ChildItem $TARGET -Recurse -Depth 3 -Force |
  Where-Object { $_.LinkType } | Select-Object FullName, LinkType, Target
```

---

## STEP 1 — 정체 파악 (읽기 전용)

다음 중 무엇인지 판별하고 근거를 남긴다.

| 후보 | 판별 방법 |
|---|---|
| git worktree | `TARGET/.git` 가 **파일**이고 내용이 `gitdir: ...` |
| 독립 git 저장소 | `TARGET/.git` 가 **디렉터리** |
| 일반 폴더 / 캐시 | `.git` 없음 |
| 링크 | STEP 0 결과 |

```bash
ls -la "$TARGET" | head -40
file "$TARGET/.git" 2>/dev/null
cat "$TARGET/.git" 2>/dev/null

# 상위 저장소 기준으로 worktree 목록에 잡히는지
cd "$(dirname "$(dirname "$TARGET")")" && git worktree list --porcelain 2>/dev/null
```

worktree라면 **어느 브랜치를 체크아웃 중인지**, 상위 메인 저장소 경로가 어디인지 기록한다.

---

## STEP 2 — 24GB 용량 분해 (읽기 전용)

무엇이 용량을 먹는지 모르면 판정할 수 없다. 상위 20개를 뽑는다.

```bash
du -sh "$TARGET"
du -h --max-depth=2 "$TARGET" 2>/dev/null | sort -hr | head -20
# macOS: du -h -d 2 "$TARGET" | sort -hr | head -20
```

```powershell
Get-ChildItem $TARGET -Directory -Force | ForEach-Object {
  [PSCustomObject]@{
    Path = $_.FullName
    GB   = [math]::Round((Get-ChildItem $_.FullName -Recurse -Force -EA SilentlyContinue |
             Measure-Object Length -Sum).Sum / 1GB, 2)
  }
} | Sort-Object GB -Descending | Select-Object -First 20
```

**재생성 가능 vs 불가** 로 분류한다.

- 재생성 가능(삭제 영향 낮음): `node_modules/`, `.venv/`, `target/`, `build/`, `dist/`, `out/`,
  `__pycache__/`, `.cache/`, `.gradle/`, `.next/`, 빌드 산출물, 로그, 코어덤프
- 재생성 불가(삭제 위험): 소스 코드, 미커밋 변경, `.env`·인증서·키, 로그 원본 데이터,
  캡처된 시험 결과물, 사용자가 직접 만든 문서

---

## STEP 3 — 유실 위험 데이터 검사 (읽기 전용, 가장 중요)

git 저장소/worktree인 경우 전부 확인한다.

```bash
cd "$TARGET"
git status --porcelain=v1 --untracked-files=all   # 미커밋 + untracked
git stash list                                     # 스택된 작업
git log --branches --not --remotes --oneline       # 원격에 없는 커밋(unpushed)
git rev-parse --abbrev-ref HEAD
```

git이 아닌 경우, 최근 수정된 사람이 만든 파일이 있는지 본다.

```bash
find "$TARGET" -type f -mtime -30 \
  -not -path "*/node_modules/*" -not -path "*/.venv/*" \
  -not -path "*/build/*" -not -path "*/dist/*" \
  -not -path "*/.git/*" -printf "%TY-%Tm-%Td %10s %p\n" 2>/dev/null | sort -r | head -50
```

시크릿/설정 파일 존재 여부도 별도로 확인한다.

```bash
find "$TARGET" -maxdepth 4 \
  \( -name ".env*" -o -name "*.pem" -o -name "*.key" -o -name "secrets*" \) \
  -not -path "*/node_modules/*" 2>/dev/null
```

> **하나라도 걸리면 판정은 최소 `CONDITIONAL` 이다.**

---

## STEP 4 — 참조 및 사용 중 여부 검사 (읽기 전용)

TARGET을 가리키는 설정이나 실행 중인 프로세스가 있으면 삭제 시 동작이 깨진다.

```bash
# 설정/훅/문서에서 참조되는지
grep -rn "\.claude/main" ~/.claude/settings.json ~/.claude.json \
  ./.claude/ ./CLAUDE.md ./.mcp.json 2>/dev/null

# 현재 이 경로를 작업 디렉터리로 쓰는 프로세스
lsof +D "$TARGET" 2>/dev/null | head -20
# 또는
ps -eo pid,comm,args | grep -i "$(basename "$TARGET")" | grep -v grep
```

```powershell
Select-String -Path "$HOME\.claude\settings.json","$HOME\.claude.json",".\CLAUDE.md" `
  -Pattern "\.claude[\\/]main" -EA SilentlyContinue
```

추가 확인:
- IDE 워크스페이스, `PATH`, 심볼릭 링크가 이 경로를 가리키는가?
- CI 스크립트나 사내 툴(`l1-fla`, `issue-analyzer`, `skillsilent` 등)의 설정에 하드코딩되어 있는가?

---

## STEP 5 — 판정 및 보고 (여기서 일단 멈춘다)

아래 표 형식으로 보고한 뒤 **사용자 승인을 기다린다.**

```
## 조사 결과
- 경로:
- 정체: (git worktree / 독립 저장소 / 일반 폴더 / 링크)
- 총 용량:
- 용량 상위 5개:

## 유실 위험
- 미커밋 변경:      건
- untracked 파일:   건
- stash:            건
- unpushed 커밋:    건
- 시크릿 파일:      건
- 최근 30일 수정 사용자 파일: 건

## 참조 상태
- 설정 파일 참조:   있음 / 없음  (근거)
- 실행 중 프로세스: 있음 / 없음  (근거)

## 판정: SAFE_TO_DELETE / CONDITIONAL / DO_NOT_DELETE
근거:

## 회수 예상 용량: XX GB
## 권장 조치:
```

**판정 기준**

| 판정 | 조건 |
|---|---|
| `SAFE_TO_DELETE` | 미커밋·untracked·stash·unpushed 전부 0건, 시크릿 없음, 참조 없음, 프로세스 없음 |
| `CONDITIONAL` | 위 중 하나라도 걸리지만 재생성 가능 디렉터리만 부분 삭제하면 해결됨 |
| `DO_NOT_DELETE` | 유실 위험 데이터 존재, 또는 정체 불명, 또는 활성 참조 존재 |

**CONDITIONAL 이면** 전체 삭제 대신 부분 정리안을 제시한다.
예: `node_modules/`, `build/`, `.venv/` 만 제거 → 회수 XX GB, 소스는 보존, `npm ci` 로 복구 가능.

---

## STEP 6 — 실행 (사용자가 명시적으로 승인한 경우에만)

### 6-A. git worktree인 경우

```bash
cd "<메인 저장소 경로>"
git worktree remove "<TARGET>"        # 변경사항 있으면 git이 거부 → 정상 동작
# 잠겨 있다면
git worktree unlock "<TARGET>" && git worktree remove "<TARGET>"
git worktree prune
```

`git worktree remove` 가 거부하면 **강제(`--force`) 하지 말고 STEP 3으로 돌아가 원인을 보고한다.**

### 6-B. 일반 폴더인 경우 — 격리 후 삭제 (2단계)

```bash
# 1) 즉시 삭제하지 않고 이름만 변경
mv "$TARGET" "${TARGET}.TRASH-$(date +%Y%m%d)"

# 2) 빌드/툴 정상 동작을 며칠 확인한 뒤 최종 삭제
# rm -rf "${TARGET}.TRASH-YYYYMMDD"
```

```powershell
Rename-Item $TARGET "$(Split-Path $TARGET -Leaf).TRASH-$(Get-Date -f yyyyMMdd)"
```

### 6-C. 부분 정리인 경우

```bash
find "$TARGET" -maxdepth 3 -type d \
  \( -name node_modules -o -name .venv -o -name build -o -name dist -o -name target \) \
  -prune -print          # 먼저 목록만 출력해서 사용자에게 확인받는다
# 승인 후에만 -exec rm -rf {} + 추가
```

---

## STEP 7 — 사후 보고

- 실제 회수 용량 (`df -h` 전후 비교)
- 격리 폴더 경로와 **최종 삭제 예정일**
- 복구 방법 (worktree 재생성 명령, `npm ci` 등)
- 되돌릴 수 없는 항목이 있었다면 명시

---

## 참고

- Claude Code 공식 `.claude` 디렉터리 구조: https://code.claude.com/docs/en/claude-directory
- worktree 기본 경로는 `.claude/worktrees/<이름>` 이며 `.claude/main` 은 공식 구조가 아니다.
  따라서 **사내 툴 또는 수동 생성 경로일 가능성이 높으므로 STEP 1 판별을 특히 신중히 한다.**
