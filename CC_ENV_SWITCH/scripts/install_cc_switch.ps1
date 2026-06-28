<#
  install_cc_switch.ps1 — CC_ENV_SWITCH 1회 설치
  버전: 1.0

  하는 일:
    1. .claude/profiles, _golden, backups 디렉토리 생성
    2. 현재 settings.json -> _golden/settings.ORIGINAL.json (읽기전용 골든 스냅샷)
    3. aws/corp 템플릿 -> profiles/ 로 배치
    4. transplant_card.yaml 있으면 apply_card.ps1 호출하여 corp 프로파일 자동 완성
    5. cc-switch.ps1 -> .claude/ 로 복사
    6. $PROFILE 에 cc-switch 함수 등록 (이미 있으면 스킵)
    7. cc-switch status 로 설치 확인

  사용:
    이 스크립트가 있는 CC_ENV_SWITCH 폴더에서:
      .\scripts\install_cc_switch.ps1
    (선택) 카드 경로 지정:
      .\scripts\install_cc_switch.ps1 -CardPath .\templates\transplant_card.yaml
#>

[CmdletBinding()]
param(
    [string]$CardPath
)

$ErrorActionPreference = 'Stop'

function Say  { param($m) Write-Host "  $m" -ForegroundColor Cyan }
function Done { param($m) Write-Host "  [OK] $m" -ForegroundColor Green }
function Warn { param($m) Write-Host "  [!] $m" -ForegroundColor Yellow }

# 패키지 루트 = 이 스크립트의 상위 디렉토리
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PkgRoot   = Split-Path -Parent $ScriptDir

$ClaudeDir  = Join-Path $env:USERPROFILE '.claude'
$ProfileDir = Join-Path $ClaudeDir 'profiles'
$GoldenDir  = Join-Path $ProfileDir '_golden'
$BackupDir  = Join-Path $ClaudeDir 'backups'
$Settings   = Join-Path $ClaudeDir 'settings.json'
$GoldenFile = Join-Path $GoldenDir 'settings.ORIGINAL.json'
$CcTarget   = Join-Path $ClaudeDir 'cc-switch.ps1'

Write-Host ""
Say "CC_ENV_SWITCH 설치 시작"
Say "패키지 루트: $PkgRoot"

# 1. 디렉토리
foreach ($d in $ClaudeDir, $ProfileDir, $GoldenDir, $BackupDir) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Force -Path $d | Out-Null }
}
Done "디렉토리 준비"

# 2. 골든 스냅샷 (최초 1회, 이미 있으면 보존)
if (Test-Path $GoldenFile) {
    Warn "골든 스냅샷이 이미 존재 -> 덮어쓰지 않음 (원본 보존)"
} elseif (Test-Path $Settings) {
    Copy-Item $Settings $GoldenFile -Force
    Set-ItemProperty -Path $GoldenFile -Name IsReadOnly -Value $true
    Done "골든 스냅샷 생성(읽기전용): $GoldenFile"
} else {
    Warn "현재 settings.json 이 없어 골든 스냅샷을 만들지 못함. aws 적용 후 수동 생성 권장."
}

# 3. 템플릿 -> 프로파일 배치 (이미 있으면 보존)
$awsTpl  = Join-Path $PkgRoot 'templates\aws.settings.template.json'
$corpTpl = Join-Path $PkgRoot 'templates\corp.settings.template.json'
$awsP    = Join-Path $ProfileDir 'aws.settings.json'
$corpP   = Join-Path $ProfileDir 'corp.settings.json'

if (-not (Test-Path $awsP)) {
    if (Test-Path $awsTpl) { Copy-Item $awsTpl $awsP -Force; Done "aws 프로파일 배치" }
    else { Warn "aws 템플릿 없음: $awsTpl" }
} else { Warn "aws 프로파일 이미 존재 -> 보존" }

if (-not (Test-Path $corpP)) {
    if (Test-Path $corpTpl) { Copy-Item $corpTpl $corpP -Force; Done "corp 프로파일 배치" }
    else { Warn "corp 템플릿 없음: $corpTpl" }
} else { Warn "corp 프로파일 이미 존재 -> 보존" }

# 4. 이식 카드 적용 (있으면)
if (-not $CardPath) {
    $defaultCard = Join-Path $PkgRoot 'templates\transplant_card.yaml'
    if (Test-Path $defaultCard) { $CardPath = $defaultCard }
}
if ($CardPath -and (Test-Path $CardPath)) {
    $applyScript = Join-Path $ScriptDir 'apply_card.ps1'
    if (Test-Path $applyScript) {
        Say "이식 카드 적용: $CardPath"
        & $applyScript -CardPath $CardPath -ProfilePath $corpP
        Done "corp 프로파일에 카드 반영"
    } else { Warn "apply_card.ps1 없음 -> 카드 자동 적용 건너뜀" }
} else {
    Warn "transplant_card.yaml 없음 -> corp 프로파일은 템플릿 상태(수동 편집 필요)"
}

# 5. cc-switch.ps1 복사
$ccSource = Join-Path $ScriptDir 'cc-switch.ps1'
if (Test-Path $ccSource) {
    Copy-Item $ccSource $CcTarget -Force
    Done "cc-switch.ps1 -> $CcTarget"
} else {
    throw "cc-switch.ps1 을 찾을 수 없음: $ccSource"
}

# 6. $PROFILE 에 함수 등록
$funcLine = @"

# ── cc-switch (CC_ENV_SWITCH) ──
function cc-switch { & "$CcTarget" @args }
"@
$profilePath = $PROFILE
$profileParent = Split-Path -Parent $profilePath
if (-not (Test-Path $profileParent)) { New-Item -ItemType Directory -Force -Path $profileParent | Out-Null }
if (-not (Test-Path $profilePath)) { New-Item -ItemType File -Force -Path $profilePath | Out-Null }

$existing = Get-Content $profilePath -Raw -ErrorAction SilentlyContinue
if ($existing -and $existing -match 'function cc-switch') {
    Warn "`$PROFILE 에 cc-switch 가 이미 등록됨 -> 스킵"
} else {
    Add-Content -Path $profilePath -Value $funcLine -Encoding UTF8
    Done "`$PROFILE 에 cc-switch 함수 등록: $profilePath"
}

# 7. 토큰 안내
$tok = [Environment]::GetEnvironmentVariable('CORP_ANTHROPIC_TOKEN','User')
if ([string]::IsNullOrWhiteSpace($tok)) {
    Warn "사내 토큰 미설정. 사내 전환 전에 아래 실행 후 새 터미널:"
    Write-Host '       setx CORP_ANTHROPIC_TOKEN "<발급받은_토큰>"' -ForegroundColor White
}

Write-Host ""
Done "설치 완료"
Say "다음: 새 터미널을 열고 ->  cc-switch status"
Say "사용:  cc-switch aws  |  cc-switch corp"
Write-Host ""
