<#
  verify_switch.ps1 — 전환 상태 독립 검증
  버전: 1.0

  cc-switch 와 무관하게, 현재 Claude Code 가 "어느 경로로" 붙을지를
  파일/환경변수 관점에서 진단한다. 잔존 변수 가로채기를 잡아낸다.

  사용:
    .\verify_switch.ps1
#>

function Say  { param($m) Write-Host "  $m" -ForegroundColor Cyan }
function Ok   { param($m) Write-Host "  [OK] $m" -ForegroundColor Green }
function Warn { param($m) Write-Host "  [!] $m" -ForegroundColor Yellow }
function Bad  { param($m) Write-Host "  [X] $m" -ForegroundColor Red }

$Settings = Join-Path $env:USERPROFILE '.claude\settings.json'
$Active   = Join-Path $env:USERPROFILE '.claude\.cc_active'

Write-Host ""
Say "── settings.json 진단 ──"
if (Test-Path $Settings) {
    try {
        $j = Get-Content $Settings -Raw | ConvertFrom-Json
        $e = $j.env
        if ($e.CLAUDE_CODE_USE_BEDROCK) {
            Ok "경로: AWS Bedrock (region=$($e.AWS_REGION), model=$($e.ANTHROPIC_MODEL))"
        } elseif ($e.ANTHROPIC_BASE_URL) {
            $h = ([Uri]$e.ANTHROPIC_BASE_URL).Host
            Ok "경로: 사내 게이트웨이 ($h)"
            if ($e.ANTHROPIC_AUTH_TOKEN -match '\$\{') {
                Warn "AUTH_TOKEN 이 환경변수 참조 상태 -> CORP_ANTHROPIC_TOKEN 설정 확인 필요"
            }
            # 게이트웨이로 붙지만 모델 ID 가 Bedrock 형식이면 실제 요청이 Bedrock 으로 샐 수 있음
            $allow = @('ANTHROPIC_BASE_URL','ANTHROPIC_AUTH_TOKEN','ANTHROPIC_MODEL','CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS')
            $brx   = '^(global\.|us\.|apac\.|eu\.)?anthropic\.claude'
            $leak  = @()
            foreach ($n in $e.PSObject.Properties.Name) { if ($allow -notcontains $n) { $leak += "env.$n" } }
            if ($e.ANTHROPIC_MODEL -match $brx) { $leak += "env.ANTHROPIC_MODEL($($e.ANTHROPIC_MODEL))" }
            foreach ($tl in 'modelOverrides','availableModels') { if ($j.$tl) { $leak += $tl } }
            if ($leak) {
                Bad "Bedrock 모델 라우팅 잔류 발견: $($leak -join ', ')"
                Warn "게이트웨이로 붙어도 모델 해석 단계에서 Bedrock 으로 샐 수 있음 -> 'cc-switch corp' 재실행(자동 정화)"
            } else {
                Ok "모델 라우팅 깨끗 (Bedrock 잔류 없음)"
            }
        } else {
            Warn "경로 불명확 (Bedrock/게이트웨이 둘 다 아님)"
        }
    } catch { Bad "settings.json 파싱 실패" }
} else { Bad "settings.json 없음" }

if (Test-Path $Active) {
    Say "활성 마커: $((Get-Content $Active -Raw).Trim())"
}

Write-Host ""
Say "── 환경변수 가로채기 점검 ──"
$found = $false
foreach ($scope in 'User','Process') {
    foreach ($name in 'ANTHROPIC_API_KEY','ANTHROPIC_AUTH_TOKEN','ANTHROPIC_BASE_URL','CLAUDE_CODE_USE_BEDROCK') {
        $v = [Environment]::GetEnvironmentVariable($name, $scope)
        if (-not [string]::IsNullOrWhiteSpace($v)) {
            $found = $true
            $masked = if ($name -match 'TOKEN|KEY') { '***' + ($v.Substring([Math]::Max(0,$v.Length-4))) } else { $v }
            Warn "[$scope] $name = $masked  (settings.json 보다 우선될 수 있음)"
        }
    }
}
if (-not $found) { Ok "가로챌 환경변수 없음 (settings.json 단독 결정)" }

Write-Host ""
Say "정밀 확인은: 새 터미널 -> claude /status"
Write-Host ""
