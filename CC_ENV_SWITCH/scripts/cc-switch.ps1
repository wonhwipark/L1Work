<#
  cc-switch.ps1 — Claude Code 환경 프로파일 전환기 (AWS Bedrock <-> 사내 게이트웨이)
  버전: 1.0  (CC_ENV_SWITCH standalone)

  설계 원칙:
    - settings.json 의 env 가 셸 변수보다 우선 -> 전환 = "프로파일 파일 교체"
    - 반대 경로 변수 잔존 금지 (자격증명 사다리 오염 방지)
    - 토큰은 OS 환경변수 참조 (${ENV}), 파일 하드코딩 금지
    - "원복 보장"이 1순위: 골든 스냅샷 + 타임스탬프 백업 + undo + 자동 롤백

  명령:
    cc-switch aws              AWS(Bedrock) 프로파일 적용
    cc-switch corp             사내 게이트웨이 프로파일 적용
    cc-switch status           현재 활성 프로파일 + /status 안내
    cc-switch undo             직전 전환 직전 상태로 즉시 원복
    cc-switch restore original 읽기전용 골든 스냅샷으로 복귀
    cc-switch restore <file>   지정 타임스탬프 백업으로 복귀
    cc-switch list             백업/스냅샷 목록 + provider 한 줄 요약
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Command = 'status',

    [Parameter(Position = 1)]
    [string]$Arg,

    # corp 전환 시 Bedrock 모델 잔류를 실제로 지우지 않고 "지울 항목만" 미리보기
    [switch]$DryRun
)

# ───────────────────────────────────────────────
# Config (환경에 맞게 수정 가능한 유일한 블록)
# ───────────────────────────────────────────────
$Config = @{
    ClaudeDir    = (Join-Path $env:USERPROFILE '.claude')
    ProfileDir   = (Join-Path $env:USERPROFILE '.claude\profiles')
    GoldenDir    = (Join-Path $env:USERPROFILE '.claude\profiles\_golden')
    BackupDir    = (Join-Path $env:USERPROFILE '.claude\backups')
    SettingsPath = (Join-Path $env:USERPROFILE '.claude\settings.json')
    ActiveMarker = (Join-Path $env:USERPROFILE '.claude\.cc_active')
    LastBackup   = (Join-Path $env:USERPROFILE '.claude\.cc_last_backup')
    GoldenFile   = (Join-Path $env:USERPROFILE '.claude\profiles\_golden\settings.ORIGINAL.json')
    MaxBackups   = 20
    VerifyCmd    = 'claude --version'   # 더 강한 검증: 'claude -p "reply OK"'
    CorpTokenVar = 'CORP_ANTHROPIC_TOKEN'

    # corp 프로파일 env 에 남겨도 되는 키 화이트리스트 (이외는 정화 시 제거)
    CorpEnvAllow = @(
        'ANTHROPIC_BASE_URL','ANTHROPIC_AUTH_TOKEN','ANTHROPIC_MODEL',
        'CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS'
    )
    # Bedrock 모델 ID 형식 (corp 에서 발견되면 라우팅 누수로 간주)
    BedrockModelRegex = '^(global\.|us\.|apac\.|eu\.)?anthropic\.claude'
    # corp 톱레벨에서 제거 대상 (Bedrock 모델 라우팅 잔류)
    CorpTopLevelStrip = @('modelOverrides','availableModels')
}

# ───────────────────────────────────────────────
# 유틸
# ───────────────────────────────────────────────
function Write-Info  { param($m) Write-Host "  $m" -ForegroundColor Cyan }
function Write-Ok    { param($m) Write-Host "  [OK] $m" -ForegroundColor Green }
function Write-Warn2 { param($m) Write-Host "  [!] $m" -ForegroundColor Yellow }
function Write-Err2  { param($m) Write-Host "  [X] $m" -ForegroundColor Red }

function Get-Stamp { (Get-Date).ToString('yyyyMMdd_HHmmss') }

# 프로파일 JSON 의 provider 한 줄 요약
function Get-ProviderSummary {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return 'missing' }
    try {
        $j = Get-Content $Path -Raw | ConvertFrom-Json
        $env = $j.env
        if ($null -eq $env) { return 'no-env-block' }
        if ($env.CLAUDE_CODE_USE_BEDROCK) { return "bedrock (region=$($env.AWS_REGION))" }
        if ($env.ANTHROPIC_BASE_URL) {
            $h = ([Uri]$env.ANTHROPIC_BASE_URL).Host
            return "gateway ($h)"
        }
        return 'direct/unknown'
    } catch { return 'parse-error' }
}

# S4: 적용 전 무결성 검증 + 교차 오염 차단
function Test-ProfileIntegrity {
    param([string]$Path, [string]$Kind)  # Kind = 'aws' | 'corp'
    if (-not (Test-Path $Path)) { Write-Err2 "프로파일 없음: $Path"; return $false }
    try {
        $j = Get-Content $Path -Raw | ConvertFrom-Json -ErrorAction Stop
    } catch {
        Write-Err2 "JSON 파싱 실패: $Path"; return $false
    }
    if ($null -eq $j.env) { Write-Err2 "env 블록 없음: $Path"; return $false }

    $env = $j.env
    if ($Kind -eq 'aws') {
        if ($env.ANTHROPIC_BASE_URL -or $env.ANTHROPIC_AUTH_TOKEN) {
            Write-Err2 "aws 프로파일에 사내 변수(BASE_URL/AUTH_TOKEN) 혼입 -> 중단"; return $false
        }
        if (-not $env.CLAUDE_CODE_USE_BEDROCK) {
            Write-Warn2 "aws 프로파일에 CLAUDE_CODE_USE_BEDROCK 없음 (의도된 것인지 확인)"
        }
    } elseif ($Kind -eq 'corp') {
        if ($env.CLAUDE_CODE_USE_BEDROCK) {
            Write-Err2 "corp 프로파일에 CLAUDE_CODE_USE_BEDROCK 혼입 -> 중단"; return $false
        }
        $awsLeak = $env.PSObject.Properties.Name | Where-Object { $_ -like 'AWS_*' }
        if ($awsLeak) {
            Write-Err2 "corp 프로파일에 AWS_* 변수 혼입($($awsLeak -join ',')) -> 중단"; return $false
        }
        if (-not $env.ANTHROPIC_BASE_URL) {
            Write-Warn2 "corp 프로파일에 ANTHROPIC_BASE_URL 없음 (의도된 것인지 확인)"
        }
        # Bedrock 모델 라우팅 잔류 최종 차단 (정화가 우회된 경우 대비)
        $modelLeak = @()
        foreach ($mk in $env.PSObject.Properties.Name) {
            if ($Config.CorpEnvAllow -notcontains $mk) { $modelLeak += "env.$mk" }
        }
        if ($env.ANTHROPIC_MODEL -match $Config.BedrockModelRegex) { $modelLeak += "env.ANTHROPIC_MODEL($($env.ANTHROPIC_MODEL))" }
        foreach ($tl in $Config.CorpTopLevelStrip) { if ($j.$tl) { $modelLeak += $tl } }
        if ($modelLeak) {
            Write-Err2 "corp 프로파일에 Bedrock 모델 라우팅 잔류($($modelLeak -join ', ')) -> 중단"; return $false
        }
        # 토큰 placeholder 가 안 풀린 채 남아있는지 점검
        if ($env.ANTHROPIC_AUTH_TOKEN -match '\$\{.*\}' -or $env.ANTHROPIC_AUTH_TOKEN -match 'PLACEHOLDER') {
            $tok = [Environment]::GetEnvironmentVariable($Config.CorpTokenVar, 'User')
            if ([string]::IsNullOrWhiteSpace($tok)) {
                Write-Warn2 "사내 토큰 환경변수 $($Config.CorpTokenVar) 미설정. setx $($Config.CorpTokenVar) `"<토큰>`" 후 새 터미널."
            }
        }
    }
    return $true
}

# S2: 타임스탬프 백업 회전
function Backup-Current {
    param([string]$From, [string]$To)
    if (-not (Test-Path $Config.SettingsPath)) {
        Write-Warn2 "현재 settings.json 없음 -> 백업 건너뜀 (최초 적용으로 간주)"
        return $null
    }
    if (-not (Test-Path $Config.BackupDir)) { New-Item -ItemType Directory -Force -Path $Config.BackupDir | Out-Null }
    $stamp = Get-Stamp
    $bk = Join-Path $Config.BackupDir "settings_${stamp}_${From}-to-${To}.json"
    Copy-Item $Config.SettingsPath $bk -Force
    Set-Content -Path $Config.LastBackup -Value $bk -Encoding UTF8
    # 회전: 최근 N개만 유지
    $all = Get-ChildItem $Config.BackupDir -Filter 'settings_*.json' | Sort-Object LastWriteTime -Descending
    if ($all.Count -gt $Config.MaxBackups) {
        $all | Select-Object -Skip $Config.MaxBackups | Remove-Item -Force
    }
    return $bk
}

# S6: 원자적 적용
function Set-SettingsAtomic {
    param([string]$SourceProfile)
    $tmp = "$($Config.SettingsPath).tmp"
    Copy-Item $SourceProfile $tmp -Force
    Move-Item $tmp $Config.SettingsPath -Force
}

# S4b: corp 프로파일에서 Bedrock 모델 라우팅 잔류를 화이트리스트 기준으로 정화.
#   - 톱레벨 modelOverrides/availableModels 제거
#   - env 화이트리스트 외 키 제거 (DEFAULT_SONNET/HAIKU/OPUS_MODEL 등 포함)
#   - ANTHROPIC_MODEL 이 Bedrock 형식이면 제거
# 반환: @{ Removed=[string[]]; Json=[정화된 객체 또는 $null] }
function Repair-CorpProfile {
    param([string]$Path)
    $removed = @()
    try {
        $j = Get-Content $Path -Raw | ConvertFrom-Json -ErrorAction Stop
    } catch {
        return @{ Removed = @(); Json = $null; Error = 'parse' }
    }

    # 1) 톱레벨 Bedrock 라우팅 필드 제거
    foreach ($tl in $Config.CorpTopLevelStrip) {
        if ($j.PSObject.Properties.Name -contains $tl) {
            $j.PSObject.Properties.Remove($tl); $removed += $tl
        }
    }

    # 2) env 화이트리스트 외 키 제거 (블랙리스트 아님 → 새 Bedrock 필드도 자동 차단)
    if ($j.env) {
        foreach ($name in @($j.env.PSObject.Properties.Name)) {
            if ($Config.CorpEnvAllow -notcontains $name) {
                $j.env.PSObject.Properties.Remove($name); $removed += "env.$name"
            }
        }
        # 3) ANTHROPIC_MODEL 이 Bedrock 형식이면 제거 (게이트웨이 모델명은 보존)
        if ($j.env.ANTHROPIC_MODEL -and ($j.env.ANTHROPIC_MODEL -match $Config.BedrockModelRegex)) {
            $bad = $j.env.ANTHROPIC_MODEL
            $j.env.PSObject.Properties.Remove('ANTHROPIC_MODEL')
            $removed += "env.ANTHROPIC_MODEL($bad)"
        }
    }

    return @{ Removed = $removed; Json = $j; Error = $null }
}

# S5: 적용 후 자동 검증
function Test-RuntimeOk {
    try {
        $null = Invoke-Expression $Config.VerifyCmd 2>&1
        return ($LASTEXITCODE -eq 0)
    } catch {
        return $false
    }
}

# ───────────────────────────────────────────────
# 핵심: 전환
# ───────────────────────────────────────────────
function Invoke-Switch {
    param([ValidateSet('aws','corp')][string]$Kind)

    $profile = Join-Path $Config.ProfileDir "$Kind.settings.json"
    $from = if (Test-Path $Config.ActiveMarker) { Get-Content $Config.ActiveMarker -Raw } else { 'unknown' }
    $from = $from.Trim()

    Write-Info "전환: $from -> $Kind"

    # S4b: corp 는 적용 전 Bedrock 모델 라우팅 잔류를 자동 정화 (화이트리스트 기준)
    if ($Kind -eq 'corp') {
        $rep = Repair-CorpProfile -Path $profile
        if ($rep.Error -eq 'parse') {
            Write-Err2 "corp 프로파일 JSON 파싱 실패 -> 중단: $profile"; return
        }
        if ($rep.Removed.Count -gt 0) {
            if ($DryRun) {
                Write-Warn2 "[DryRun] 정화 대상 (실제로는 지우지 않음):"
                $rep.Removed | ForEach-Object { Write-Host "      - $_" -ForegroundColor Yellow }
                Write-Info "[DryRun] 실제 적용하려면 -DryRun 없이 다시 실행하세요."
                return
            }
            # 정화 결과를 corp 프로파일 파일에 되써서 SSOT 도 깨끗하게 유지
            $rep.Json | ConvertTo-Json -Depth 20 | Set-Content -Path $profile -Encoding UTF8
            Write-Ok "corp 프로파일 자동 정화: Bedrock 라우팅 잔류 제거"
            $rep.Removed | ForEach-Object { Write-Host "      - $_" -ForegroundColor DarkGray }
        } else {
            if ($DryRun) { Write-Ok "[DryRun] 정화할 Bedrock 잔류 없음 (이미 깨끗)"; return }
        }
    } elseif ($DryRun) {
        Write-Warn2 "-DryRun 은 corp 전환에서만 의미가 있습니다. aws 는 정상 진행 또는 중단하세요."
        return
    }

    # S4 무결성 검증
    if (-not (Test-ProfileIntegrity -Path $profile -Kind $Kind)) {
        Write-Err2 "검증 실패 -> 아무것도 바꾸지 않고 중단 (현재 상태 유지)"
        return
    }

    # S2 백업
    $bk = Backup-Current -From $from -To $Kind
    if ($bk) { Write-Ok "백업: $bk" }

    # S6 원자적 적용
    try {
        Set-SettingsAtomic -SourceProfile $profile
    } catch {
        Write-Err2 "적용 중 오류: $_"
        if ($bk) { Copy-Item $bk $Config.SettingsPath -Force; Write-Warn2 "백업에서 복원함" }
        return
    }
    Set-Content -Path $Config.ActiveMarker -Value $Kind -Encoding UTF8
    Write-Ok "프로파일 적용 완료: $Kind"

    # S5 자동 검증 + 실패 시 자동 롤백
    if (Test-RuntimeOk) {
        Write-Ok "런타임 검증 통과 ($($Config.VerifyCmd))"
    } else {
        Write-Err2 "런타임 검증 실패 -> 직전 백업으로 자동 롤백"
        if ($bk) {
            Copy-Item $bk $Config.SettingsPath -Force
            Set-Content -Path $Config.ActiveMarker -Value $from -Encoding UTF8
            Write-Warn2 "롤백 완료. 현재 활성: $from"
        } else {
            Write-Warn2 "백업이 없어 자동 롤백 불가. 'cc-switch restore original' 권장."
        }
        return
    }

    Write-Info "전환 후 반드시 '새 터미널/새 세션'에서 claude 를 실행해야 env 가 다시 읽힙니다."
    Write-Info "확인: 새 터미널 -> claude -> /status"
}

# ───────────────────────────────────────────────
# undo / restore / list / status
# ───────────────────────────────────────────────
function Invoke-Undo {
    if (-not (Test-Path $Config.LastBackup)) { Write-Err2 "undo 기록 없음(.cc_last_backup)"; return }
    $bk = (Get-Content $Config.LastBackup -Raw).Trim()
    if (-not (Test-Path $bk)) { Write-Err2 "백업 파일이 사라짐: $bk"; return }
    Copy-Item $bk $Config.SettingsPath -Force
    # 활성 마커는 파일명에서 from 을 역추출 (..._<from>-to-<to>.json)
    if ($bk -match 'settings_\d{8}_\d{6}_(?<from>[^-]+)-to-') {
        Set-Content -Path $Config.ActiveMarker -Value $Matches['from'] -Encoding UTF8
    }
    Write-Ok "undo 완료. 복원: $bk"
    Write-Info "새 터미널에서 확인하세요."
}

function Invoke-Restore {
    param([string]$Target)
    if ([string]::IsNullOrWhiteSpace($Target) -or $Target -eq 'original') {
        if (-not (Test-Path $Config.GoldenFile)) { Write-Err2 "골든 스냅샷 없음: $($Config.GoldenFile)"; return }
        Copy-Item $Config.GoldenFile $Config.SettingsPath -Force
        Set-Content -Path $Config.ActiveMarker -Value 'original' -Encoding UTF8
        Write-Ok "골든 원본으로 복귀 (최후 복귀점)"
        Write-Info "새 터미널에서 확인하세요."
        return
    }
    # 지정 백업 파일
    $cand = $Target
    if (-not (Test-Path $cand)) { $cand = Join-Path $Config.BackupDir $Target }
    if (-not (Test-Path $cand)) { Write-Err2 "복원 대상 없음: $Target"; return }
    Copy-Item $cand $Config.SettingsPath -Force
    Write-Ok "복원: $cand"
    Write-Info "새 터미널에서 확인하세요."
}

function Invoke-List {
    Write-Info "── 프로파일 ──"
    foreach ($k in 'aws','corp') {
        $p = Join-Path $Config.ProfileDir "$k.settings.json"
        Write-Host ("    {0,-6} {1}" -f $k, (Get-ProviderSummary $p))
    }
    Write-Info "── 골든 스냅샷 ──"
    Write-Host ("    original  {0}" -f (Get-ProviderSummary $Config.GoldenFile))
    Write-Info "── 백업 (최근) ──"
    if (Test-Path $Config.BackupDir) {
        Get-ChildItem $Config.BackupDir -Filter 'settings_*.json' |
            Sort-Object LastWriteTime -Descending | Select-Object -First $Config.MaxBackups |
            ForEach-Object {
                Write-Host ("    {0}  {1}" -f $_.Name, (Get-ProviderSummary $_.FullName))
            }
    } else { Write-Host "    (없음)" }
}

function Invoke-Status {
    $active = if (Test-Path $Config.ActiveMarker) { (Get-Content $Config.ActiveMarker -Raw).Trim() } else { 'unknown' }
    Write-Info "활성 프로파일: $active"
    Write-Host ("    현재 settings.json -> {0}" -f (Get-ProviderSummary $Config.SettingsPath))
    # 잔존 셸/사용자 환경변수 가로채기 경고
    $apiKey = [Environment]::GetEnvironmentVariable('ANTHROPIC_API_KEY','User')
    if (-not [string]::IsNullOrWhiteSpace($apiKey)) {
        Write-Warn2 "사용자 환경변수 ANTHROPIC_API_KEY 가 설정돼 있음 -> Bedrock/게이트웨이 둘 다 가로챌 수 있음."
        Write-Warn2 "불필요하면: setx ANTHROPIC_API_KEY `"`" 후 새 터미널"
    }
    Write-Info "정밀 확인: claude /status (새 터미널에서)"
}

# ───────────────────────────────────────────────
# 디스패치
# ───────────────────────────────────────────────
switch ($Command.ToLower()) {
    'aws'     { Invoke-Switch -Kind aws }
    'corp'    { Invoke-Switch -Kind corp }
    'undo'    { Invoke-Undo }
    'restore' { Invoke-Restore -Target $Arg }
    'list'    { Invoke-List }
    'status'  { Invoke-Status }
    default   {
        Write-Host ""
        Write-Host "cc-switch <command>" -ForegroundColor White
        Write-Host "  aws | corp | status | undo | restore [original|<file>] | list"
        Write-Host "  corp -DryRun   : corp 전환 시 지울 Bedrock 잔류만 미리보기"
        Write-Host ""
    }
}
