<#
.SYNOPSIS
  Validate that the Claude Code skill is installed and matches this package manifest.
#>
param([string]$TargetSkillsDir)

$ErrorActionPreference = "Stop"
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ManifestPath = Join-Path $PackageRoot "skill_manifest.yaml"
function Normalize-PathText([string]$PathText) { if ([string]::IsNullOrWhiteSpace($PathText)) { return $null }; return [Environment]::ExpandEnvironmentVariables($PathText.Trim().Trim('"')) }
function Write-Warn2([string]$Message) { Write-Host "[WARN] $Message" }
function Read-SimpleManifest([string]$Path) {
    if (!(Test-Path $Path)) { Write-Host "[FAIL] Manifest not found: $Path"; exit 1 }
    $manifest = @{ required_files = @(); legacy_skill_names = @() }
    $section = $null
    foreach ($raw in Get-Content -Path $Path -Encoding UTF8) {
        $line = $raw.Trim()
        if ([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith("#")) { continue }
        if ($line -match '^([A-Za-z0-9_]+):\s*(.*)$') {
            $key = $matches[1]; $value = $matches[2].Trim().Trim('"').Trim("'")
            if ([string]::IsNullOrWhiteSpace($value)) { $section = $key; if (!$manifest.ContainsKey($key)) { $manifest[$key] = @() } }
            else { $manifest[$key] = $value; $section = $null }
        } elseif ($line -match '^\-\s*(.+)$' -and $section) {
            $item = $matches[1].Trim().Trim('"').Trim("'")
            $manifest[$section] = @($manifest[$section]) + $item
        }
    }
    return $manifest
}
function Join-RelPath([string]$Root, [string]$RelPath) {
    $parts = $RelPath -split '[\\/]+'; $path = $Root
    foreach ($part in $parts) { if (![string]::IsNullOrWhiteSpace($part)) { $path = Join-Path $path $part } }
    return $path
}
function Get-DefaultSkillsDir() {
    if ($env:CLAUDE_SKILLS_DIR) { return (Normalize-PathText $env:CLAUDE_SKILLS_DIR) }
    if ($env:USERPROFILE) { return (Join-Path $env:USERPROFILE ".claude\skills") }
    if ($HOME) { return (Join-Path $HOME ".claude/skills") }
    return (Join-Path (Get-Location) ".claude\skills")
}
$Manifest = Read-SimpleManifest $ManifestPath
$SkillName = $Manifest.skill_name
if ([string]::IsNullOrWhiteSpace($TargetSkillsDir)) { $TargetSkillsDir = Get-DefaultSkillsDir } else { $TargetSkillsDir = Normalize-PathText $TargetSkillsDir }
$leaf = Split-Path -Leaf $TargetSkillsDir
if ($leaf -eq $SkillName) {
    Write-Warn2 "TargetSkillsDir appears to be the skill folder itself. Use the parent skills directory instead."
    Write-Host "       Given:    $TargetSkillsDir"
    Write-Host "       Expected: $(Split-Path -Parent $TargetSkillsDir)"
}
$TargetSkillDir = Join-Path $TargetSkillsDir $SkillName
Write-Host "[INFO] Checking: $TargetSkillDir"
$ok = $true
foreach ($rel in @($Manifest.required_files)) {
    $prefix = "skills/$SkillName/"; $relNorm = ($rel -replace '\\','/')
    if ($relNorm.StartsWith($prefix)) {
        $installedRel = $relNorm.Substring($prefix.Length)
        $installedFull = Join-RelPath $TargetSkillDir $installedRel
        if (Test-Path $installedFull) { Write-Host "[OK] $installedRel" } else { Write-Host "[FAIL] Missing: $installedRel"; $ok = $false }
    }
}
foreach ($legacy in @($Manifest.legacy_skill_names)) {
    if ([string]::IsNullOrWhiteSpace($legacy)) { continue }
    $legacyPath = Join-Path $TargetSkillsDir $legacy
    if (Test-Path $legacyPath) { Write-Warn2 "Legacy or renamed skill folder exists: $legacyPath" }
}
if ($ok) { Write-Host "[OK] $SkillName install validation passed."; Write-Host "[NEXT] Try: /$SkillName"; exit 0 }
Write-Host ""
Write-Host "Repair guide:"
Write-Host "  1. Re-run install from the package root: .\install_skill.ps1 -Force"
Write-Host "  2. Confirm that TargetSkillsDir is the parent skills directory, not the skill folder itself."
Write-Host "  3. Expected installed root: $TargetSkillDir"
Write-Host "[FAIL] $SkillName install validation failed."
exit 1
