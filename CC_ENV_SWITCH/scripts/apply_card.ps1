<#
  apply_card.ps1 — transplant_card.yaml -> corp.settings.json 자동 반영
  버전: 1.0

  목적:
    STEP 1(리눅스)에서 추출한 이식 카드(YAML)를 읽어
    corp 프로파일의 env 블록을 채운다. 토큰은 절대 박지 않고
    ${CORP_ANTHROPIC_TOKEN} 참조만 유지한다.

  의존성 없음 (외부 YAML 모듈 불요): 단순 키:값 라인 파서 내장.
    transplant_card.yaml 의 env_keys 블록만 신뢰해서 반영한다.

  사용:
    .\apply_card.ps1 -CardPath .\templates\transplant_card.yaml `
                     -ProfilePath $env:USERPROFILE\.claude\profiles\corp.settings.json
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$CardPath,
    [Parameter(Mandatory)][string]$ProfilePath
)

$ErrorActionPreference = 'Stop'

function Say  { param($m) Write-Host "  $m" -ForegroundColor Cyan }
function Done { param($m) Write-Host "  [OK] $m" -ForegroundColor Green }
function Warn { param($m) Write-Host "  [!] $m" -ForegroundColor Yellow }

if (-not (Test-Path $CardPath)) { throw "카드 없음: $CardPath" }

# ── 미니 YAML 파서: env_keys 블록의 2칸 들여쓰기 'KEY: value' 만 추출 ──
$lines = Get-Content $CardPath
$inEnv = $false
$envKeys = [ordered]@{}
foreach ($ln in $lines) {
    if ($ln -match '^\s*#') { continue }                 # 주석 무시
    if ($ln -match '^env_keys:\s*$') { $inEnv = $true; continue }
    if ($inEnv) {
        # 들여쓰기 없는 새 최상위 키를 만나면 블록 종료
        if ($ln -match '^\S') { $inEnv = $false; continue }
        if ($ln -match '^\s+(?<k>[A-Za-z_][A-Za-z0-9_]*):\s*(?<v>.*)$') {
            $k = $Matches['k']
            $v = $Matches['v'].Trim()
            # 따옴표/인라인 주석 제거
            $v = $v -replace '\s+#.*$', ''
            $v = $v.Trim('"').Trim("'")
            if ($v -ne '') { $envKeys[$k] = $v }
        }
    }
}

if ($envKeys.Count -eq 0) {
    Warn "카드에서 env_keys 를 읽지 못함. corp 프로파일을 수동 편집하세요."
    return
}

Say "카드에서 읽은 env 키: $($envKeys.Keys -join ', ')"

# ── 기존 corp 프로파일 로드 (없으면 기본 골격) ──
if (Test-Path $ProfilePath) {
    $profile = Get-Content $ProfilePath -Raw | ConvertFrom-Json
} else {
    $profile = [pscustomobject]@{ env = [pscustomobject]@{} }
}
if ($null -eq $profile.env) {
    $profile | Add-Member -NotePropertyName env -NotePropertyValue ([pscustomobject]@{}) -Force
}

# ── env 키 주입 (토큰은 항상 참조로 강제) ──
foreach ($k in $envKeys.Keys) {
    $profile.env | Add-Member -NotePropertyName $k -NotePropertyValue $envKeys[$k] -Force
}
# 인증 토큰은 카드 값과 무관하게 환경변수 참조로 고정 (하드코딩 방지)
$profile.env | Add-Member -NotePropertyName 'ANTHROPIC_AUTH_TOKEN' -NotePropertyValue '${CORP_ANTHROPIC_TOKEN}' -Force

# ── 교차 오염 차단: AWS_* / Bedrock 토글 제거 ──
$toRemove = $profile.env.PSObject.Properties.Name | Where-Object { $_ -like 'AWS_*' -or $_ -eq 'CLAUDE_CODE_USE_BEDROCK' }
foreach ($r in $toRemove) {
    $profile.env.PSObject.Properties.Remove($r)
    Warn "corp 프로파일에서 제거(교차 오염): $r"
}

# ── 원자적 저장 ──
$json = $profile | ConvertTo-Json -Depth 10
$tmp = "$ProfilePath.tmp"
Set-Content -Path $tmp -Value $json -Encoding UTF8
Move-Item $tmp $ProfilePath -Force
Done "corp 프로파일 갱신: $ProfilePath"

# 토큰 환경변수 점검
$tok = [Environment]::GetEnvironmentVariable('CORP_ANTHROPIC_TOKEN','User')
if ([string]::IsNullOrWhiteSpace($tok)) {
    Warn "CORP_ANTHROPIC_TOKEN 미설정 -> 사내 전환 전 setx 필요"
}
