<#+
.SYNOPSIS
  Configure persistent RCA kg_root separate from the installed Claude skill.

.EXAMPLE
  .\configure_kg_root.ps1 -KgRoot "D:\AI_Automation\RCA_KG"
#>
param(
  [string]$KgRoot,
  [switch]$Force,
  [switch]$NoPrompt
)

$ErrorActionPreference = "Stop"
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PackageVersion = "convenience_v0.21_kg_root_config"
$ConfigPath = Join-Path $PackageRoot "rca_config.yaml"
$DefaultKgRoot = Join-Path $PackageRoot "rca_kg"

function Write-Ok([string]$Message) { Write-Host "[OK]   $Message" }
function Write-Info([string]$Message) { Write-Host "[INFO] $Message" }
function Write-Fail([string]$Message) { Write-Host "[FAIL] $Message"; exit 1 }
function Normalize-PathText([string]$PathText) {
  if ([string]::IsNullOrWhiteSpace($PathText)) { return $null }
  return [Environment]::ExpandEnvironmentVariables($PathText.Trim().Trim('"'))
}
function Join-RelPath([string]$Root, [string]$RelPath) {
  $parts = $RelPath -split '[\\/]+'
  $path = $Root
  foreach ($part in $parts) {
    if (![string]::IsNullOrWhiteSpace($part)) { $path = Join-Path $path $part }
  }
  return $path
}
function Copy-IfMissing([string]$Source, [string]$Destination) {
  if (!(Test-Path $Source)) { return }
  $parent = Split-Path -Parent $Destination
  if (!(Test-Path $parent)) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
  if ((Test-Path $Destination) -and -not $Force) {
    Write-Info "preserve existing: $Destination"
  } else {
    Copy-Item -Path $Source -Destination $Destination -Force
    Write-Ok "seeded: $Destination"
  }
}
function Set-YamlScalar([string]$Content, [string]$Key, [string]$Value) {
  $escaped = $Value.Replace("'","''")
  $line = "$Key: '$escaped'"
  if ($Content -match "(?m)^$([regex]::Escape($Key)):\s*.*$") {
    return [regex]::Replace($Content, "(?m)^$([regex]::Escape($Key)):\s*.*$", $line)
  }
  return $Content + "`n" + $line + "`n"
}
function Set-YamlBare([string]$Content, [string]$Key, [string]$Value) {
  $line = "$Key: $Value"
  if ($Content -match "(?m)^$([regex]::Escape($Key)):\s*.*$") {
    return [regex]::Replace($Content, "(?m)^$([regex]::Escape($Key)):\s*.*$", $line)
  }
  return $Content + "`n" + $line + "`n"
}

if ([string]::IsNullOrWhiteSpace($KgRoot)) {
  if ($NoPrompt) {
    $KgRoot = $DefaultKgRoot
  } else {
    Write-Host "Default kg_root: $DefaultKgRoot"
    $inputPath = Read-Host "Enter persistent kg_root path, or press Enter to use default"
    if ([string]::IsNullOrWhiteSpace($inputPath)) { $KgRoot = $DefaultKgRoot } else { $KgRoot = $inputPath }
  }
}

$KgRoot = Normalize-PathText $KgRoot
if ([string]::IsNullOrWhiteSpace($KgRoot)) { Write-Fail "KgRoot is empty." }

$kgNorm = $KgRoot.ToLowerInvariant().Replace('/','\\')
if ($kgNorm -match '\\.claude\\skills\\') {
  Write-Fail "Do not place kg_root under .claude\\skills. Choose a persistent folder such as D:\\AI_Automation\\RCA_KG."
}

Write-Info "Package root : $PackageRoot"
Write-Info "KG root      : $KgRoot"

if (!(Test-Path $KgRoot)) {
  New-Item -ItemType Directory -Force -Path $KgRoot | Out-Null
  Write-Ok "created kg_root: $KgRoot"
}

$requiredDirs = @(
  "cases",
  "cases/unresolved",
  "runtime_tool_generate",
  "runtime_tool_generate/format_profiles",
  "signals_tool_generate",
  "indexes_tool_generate",
  "manifest_fragments",
  "schema",
  "skills_seed"
)
foreach ($dir in $requiredDirs) {
  $full = Join-RelPath $KgRoot $dir
  if (!(Test-Path $full)) { New-Item -ItemType Directory -Force -Path $full | Out-Null; Write-Ok "created: $full" }
}

$seedFiles = @(
  "keywords.yaml",
  "cases/EXAMPLE_v2_rach_failure_001.yaml",
  "cases/unresolved/EXAMPLE_unresolved.yaml",
  "runtime_tool_generate/README.md",
  "runtime_tool_generate/current_run.example.yaml",
  "runtime_tool_generate/format_profiles/README.md",
  "signals_tool_generate/README.md",
  "indexes_tool_generate/index.md",
  "manifest_fragments/README.md",
  "schema/keywords.schema.yaml",
  "schema/rca_case.schema.yaml",
  "schema/taxonomy.yaml",
  "skills_seed/crash_analyzer.md",
  "skills_seed/l2_max_retransmission_analyzer.md",
  "skills_seed/rach_failure_analyzer.md",
  "skills_seed/scg_failure_analyzer.md",
  "skills_seed/tx_abnormal_analyzer.md"
)
foreach ($rel in $seedFiles) {
  Copy-IfMissing (Join-RelPath $DefaultKgRoot $rel) (Join-RelPath $KgRoot $rel)
}

$currentRun = Join-RelPath $KgRoot "runtime_tool_generate/current_run.yaml"
if (!(Test-Path $currentRun)) {
  Copy-IfMissing (Join-RelPath $DefaultKgRoot "runtime_tool_generate/current_run.yaml") $currentRun
}
if (Test-Path $currentRun) {
  $content = Get-Content $currentRun -Raw -Encoding UTF8
  $content = Set-YamlBare $content "package_version" $PackageVersion
  $content = Set-YamlScalar $content "workspace_root" $PackageRoot
  $content = Set-YamlScalar $content "kg_root" $KgRoot
  $content = Set-YamlBare $content "kg_root_source" "user_configured"
  $content = Set-YamlScalar $content "last_updated_kst" (Get-Date -Format "yyyy-MM-dd HH:mm 'KST'")
  Set-Content -Path $currentRun -Value $content -Encoding UTF8
  Write-Ok "updated current_run.yaml: $currentRun"
}

$config = @"
# rca_config.yaml
package_version: $PackageVersion
last_configured_kst: '$(Get-Date -Format "yyyy-MM-dd HH:mm 'KST'")'
workspace_root: '$PackageRoot'
kg_root: '$KgRoot'
kg_root_source: user_configured
allow_create_kg_root: true
preserve_existing_kg: true
"@
Set-Content -Path $ConfigPath -Value $config -Encoding UTF8
Write-Ok "updated package config: $ConfigPath"

Write-Host ""
Write-Host "[NEXT] Use Claude Code: /root-cause-analyzer"
Write-Host "[NEXT] Say: 이어서 진행해줘"
Write-Host "[NOTE] Keep kg_root backed up. It stores accumulated RCA knowledge."
