param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot ".."))
)

$ErrorActionPreference = "Stop"
function Read-SimpleYamlScalar([string]$Path, [string]$Key) {
  if (!(Test-Path $Path)) { return $null }
  $m = [regex]::Match((Get-Content $Path -Raw), "(?m)^" + [regex]::Escape($Key) + ":\s*(.+)$")
  if (!$m.Success) { return $null }
  return $m.Groups[1].Value.Trim().Trim('"').Trim("'")
}
function Join-RelPath([string]$Root, [string]$RelPath) {
  $parts = $RelPath -split '[\\/]+'; $path = $Root
  foreach ($part in $parts) { if (![string]::IsNullOrWhiteSpace($part)) { $path = Join-Path $path $part } }
  return $path
}

$configPath = Join-Path $Root "rca_config.yaml"
$kgRoot = Read-SimpleYamlScalar $configPath "kg_root"
if ([string]::IsNullOrWhiteSpace($kgRoot) -or $kgRoot -eq "null") { $kgRoot = Join-Path $Root "rca_kg" }

$statePath = Join-RelPath $kgRoot "runtime_tool_generate/current_run.yaml"
$nextPath = Join-Path $Root "NEXT_STEP_5.5.md"

if (-not (Test-Path $statePath)) {
  Write-Host "current_run.yaml not found: $statePath"
  Write-Host "Recommended repair:"
  Write-Host "  .\configure_kg_root.ps1 -KgRoot `"$kgRoot`""
  exit 1
}

Write-Host "RCA package root: $Root"
Write-Host "RCA kg_root     : $kgRoot"
Write-Host "RCA current state: $statePath"
$content = Get-Content $statePath -Raw
$current = ([regex]::Match($content, "(?m)^current_step:\s*(.+)$")).Groups[1].Value.Trim()
$next = ([regex]::Match($content, "(?m)^next_step:\s*(.+)$")).Groups[1].Value.Trim()
$signal = ([regex]::Match($content, "(?m)^\s*signal_file:\s*(.+)$")).Groups[1].Value.Trim()
$case = ([regex]::Match($content, "(?m)^\s*case_file:\s*(.+)$")).Groups[1].Value.Trim()
$l1sw = ([regex]::Match($content, "(?m)^\s*selected_l1sw_txt:\s*(.+)$")).Groups[1].Value.Trim()

Write-Host "current_step: $current"
Write-Host "next_step   : $next"
if ($l1sw -and $l1sw -ne "null") { Write-Host "l1sw_txt    : $l1sw" }
if ($signal -and $signal -ne "null") { Write-Host "signal_file : $signal" }
if ($case -and $case -ne "null") { Write-Host "case_file   : $case" }

Write-Host ""
Write-Host "Recommended skill-first command:"
Write-Host "  /root-cause-analyzer"
Write-Host "  이어서 진행해줘"
Write-Host ""
Write-Host "Legacy manual fallback only:"
Write-Host "  prompt/CLAUDE_CODE_PROMPTS_e2e_v1.md block: $next"
Write-Host ""
Write-Host "Human-readable instruction: $nextPath"
if (Test-Path $nextPath) {
  Write-Host ""
  Get-Content $nextPath -TotalCount 80
}
