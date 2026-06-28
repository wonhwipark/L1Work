<#
.SYNOPSIS
  Install the Claude Code skill from this standalone package.

.DESCRIPTION
  Reads skill_manifest.yaml, validates source structure before copying, warns about legacy folders,
  and prints a repair guide when the package structure does not match the manifest.
#>
param(
    [string]$TargetSkillsDir,
    [switch]$Force,
    [switch]$Backup,
    [switch]$NoPrompt
)

$ErrorActionPreference = "Stop"
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ManifestPath = Join-Path $PackageRoot "skill_manifest.yaml"

function Write-Info([string]$Message) { Write-Host "[INFO] $Message" }
function Write-Ok([string]$Message) { Write-Host "[OK] $Message" }
function Write-Warn2([string]$Message) { Write-Host "[WARN] $Message" }
function Write-Fail([string]$Message) { Write-Host "[FAIL] $Message"; exit 1 }

function Normalize-PathText([string]$PathText) {
    if ([string]::IsNullOrWhiteSpace($PathText)) { return $null }
    return [Environment]::ExpandEnvironmentVariables($PathText.Trim().Trim('"'))
}

function Read-SimpleManifest([string]$Path) {
    if (!(Test-Path $Path)) { Write-Fail "Manifest not found: $Path" }
    $manifest = @{ required_files = @(); legacy_skill_names = @() }
    $section = $null
    foreach ($raw in Get-Content -Path $Path -Encoding UTF8) {
        $line = $raw.Trim()
        if ([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith("#")) { continue }
        if ($line -match '^([A-Za-z0-9_]+):\s*(.*)$') {
            $key = $matches[1]
            $value = $matches[2].Trim().Trim('"').Trim("'")
            if ([string]::IsNullOrWhiteSpace($value)) {
                $section = $key
                if (!$manifest.ContainsKey($key)) { $manifest[$key] = @() }
            } else {
                $manifest[$key] = $value
                $section = $null
            }
        } elseif ($line -match '^\-\s*(.+)$' -and $section) {
            $item = $matches[1].Trim().Trim('"').Trim("'")
            $manifest[$section] = @($manifest[$section]) + $item
        }
    }
    foreach ($key in @("skill_name", "expected_source_dir")) {
        if (!$manifest.ContainsKey($key) -or [string]::IsNullOrWhiteSpace($manifest[$key])) { Write-Fail "Manifest field missing: $key" }
    }
    return $manifest
}

function Join-RelPath([string]$Root, [string]$RelPath) {
    $parts = $RelPath -split '[\\/]+'
    $path = $Root
    foreach ($part in $parts) {
        if (![string]::IsNullOrWhiteSpace($part)) { $path = Join-Path $path $part }
    }
    return $path
}

function Show-ExpectedTree($Manifest) {
    $skillName = $Manifest.skill_name
    Write-Host ""
    Write-Host "Expected minimum package structure:"
    Write-Host "  <package root>"
    Write-Host "  ├─ skill_manifest.yaml"
    Write-Host "  └─ skills"
    Write-Host "     └─ $skillName"
    Write-Host "        ├─ SKILL.md"
    Write-Host "        └─ references"
    Write-Host "           └─ ..."
}

function Show-StructureRepairGuide($PackageRoot, $Manifest, $MissingFiles) {
    $skillName = $Manifest.skill_name
    $expectedSourceDir = Join-RelPath $PackageRoot $Manifest.expected_source_dir
    Write-Host ""
    Write-Warn2 "Package structure does not match skill_manifest.yaml. Installation was stopped before copying."
    Write-Host ""
    Write-Host "Expected source directory:"
    Write-Host "  $expectedSourceDir"
    Write-Host ""
    Write-Host "Missing required file(s):"
    foreach ($missing in $MissingFiles) { Write-Host "  - $missing" }

    $skillsRoot = Join-Path $PackageRoot "skills"
    $candidates = @()
    if (Test-Path $skillsRoot) { $candidates = @(Get-ChildItem -Path $skillsRoot -Filter "SKILL.md" -Recurse -File -ErrorAction SilentlyContinue) }

    if ($candidates.Count -gt 0) {
        Write-Host ""
        Write-Host "Detected SKILL.md candidate(s):"
        foreach ($candidate in $candidates) { Write-Host "  - $($candidate.FullName)" }
        Write-Host ""
        Write-Host "Repair guide:"
        Write-Host "  1. Pick the candidate that belongs to '$skillName'."
        Write-Host "  2. Move or rename its parent folder so this file exists:"
        Write-Host "     $expectedSourceDir\SKILL.md"
        Write-Host "  3. Keep the references folder under the same skill folder."
        Write-Host ""
        Write-Host "Example PowerShell pattern, adjust <detected-skill-folder> before running:"
        Write-Host "  New-Item -ItemType Directory -Force -Path \"$(Split-Path -Parent $expectedSourceDir)\" | Out-Null"
        Write-Host "  Move-Item -Path \"<detected-skill-folder>\" -Destination \"$expectedSourceDir\""
    } else {
        Write-Host ""
        Write-Host "No SKILL.md was found under:"
        Write-Host "  $skillsRoot"
        Write-Host ""
        Write-Host "Repair guide:"
        Write-Host "  1. Re-extract the ZIP without changing the internal folder names."
        Write-Host "  2. Confirm that the package root contains a skills folder."
        Write-Host "  3. Confirm that this file exists before installing:"
        Write-Host "     $expectedSourceDir\SKILL.md"
    }
    Show-ExpectedTree $Manifest
    Write-Host ""
    Write-Host "After fixing the structure, run again:"
    Write-Host "  .\install_skill.ps1"
}

function Test-SourceStructure($PackageRoot, $Manifest) {
    $missing = @()
    foreach ($rel in @($Manifest.required_files)) {
        $full = Join-RelPath $PackageRoot $rel
        if (!(Test-Path $full)) { $missing += $rel }
    }
    if ($missing.Count -gt 0) { Show-StructureRepairGuide $PackageRoot $Manifest $missing; exit 1 }
    return $true
}

function Get-DefaultSkillsDir() {
    $candidates = New-Object System.Collections.Generic.List[string]
    if ($env:CLAUDE_SKILLS_DIR) { $candidates.Add($env:CLAUDE_SKILLS_DIR) }
    if ($env:USERPROFILE) { $candidates.Add((Join-Path $env:USERPROFILE ".claude\skills")) }
    if ($HOME) { $candidates.Add((Join-Path $HOME ".claude/skills")) }
    $unique = @()
    foreach ($candidate in $candidates) {
        $normalized = Normalize-PathText $candidate
        if ($normalized -and ($unique -notcontains $normalized)) { $unique += $normalized }
    }
    foreach ($candidate in $unique) { if (Test-Path $candidate) { return $candidate } }
    if ($unique.Count -gt 0) { return $unique[0] }
    return (Join-Path (Get-Location) ".claude\skills")
}

function Confirm-TargetParent([string]$TargetSkillsDir, [string]$SkillName, [switch]$NoPrompt) {
    $leaf = Split-Path -Leaf $TargetSkillsDir
    if ($leaf -eq $SkillName) {
        $parent = Split-Path -Parent $TargetSkillsDir
        Write-Warn2 "TargetSkillsDir points to the skill folder itself. It should point to the parent 'skills' directory."
        Write-Host "  Given:    $TargetSkillsDir"
        Write-Host "  Use this: $parent"
        if ($NoPrompt) { Write-Fail "Use -TargetSkillsDir \"$parent\" with -NoPrompt." }
        $answer = Read-Host "Use parent path instead? [Y/n]"
        if ([string]::IsNullOrWhiteSpace($answer) -or $answer -match '^[Yy]') { return $parent }
        Write-Fail "Installation cancelled. TargetSkillsDir must be the parent skills directory."
    }
    return $TargetSkillsDir
}

function Warn-LegacySkillFolders([string]$TargetSkillsDir, $Manifest) {
    foreach ($legacy in @($Manifest.legacy_skill_names)) {
        if ([string]::IsNullOrWhiteSpace($legacy)) { continue }
        $legacyPath = Join-Path $TargetSkillsDir $legacy
        if (Test-Path $legacyPath) {
            Write-Warn2 "Possible legacy or renamed skill folder found: $legacyPath"
            Write-Host "       This installer will install '$($Manifest.skill_name)' and will not delete '$legacy'."
            Write-Host "       To avoid duplicate slash commands, review or remove the legacy folder manually."
        }
    }
}

function Show-InstalledTree([string]$TargetSkillDir) {
    Write-Host ""
    Write-Host "Installed file preview:"
    $files = @(Get-ChildItem -Path $TargetSkillDir -File -Recurse -ErrorAction SilentlyContinue | Select-Object -First 30)
    foreach ($file in $files) {
        $rel = $file.FullName.Substring($TargetSkillDir.Length).TrimStart([char[]]@([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar))
        Write-Host "  - $rel"
    }
    if ($files.Count -eq 0) { Write-Host "  (no files found)" }
}

$Manifest = Read-SimpleManifest $ManifestPath
$SkillName = $Manifest.skill_name
$SourceSkillDir = Join-RelPath $PackageRoot $Manifest.expected_source_dir
$SourceSkillMd = Join-Path $SourceSkillDir "SKILL.md"

Write-Info "Package root: $PackageRoot"
Write-Info "Manifest: $ManifestPath"
Write-Info "Expected skill: $SkillName"
Test-SourceStructure $PackageRoot $Manifest | Out-Null
Write-Ok "Source structure matches skill_manifest.yaml."
Write-Ok "Source skill found: $SourceSkillMd"

$targetWasProvided = -not [string]::IsNullOrWhiteSpace($TargetSkillsDir)
if ($targetWasProvided) {
    $TargetSkillsDir = Normalize-PathText $TargetSkillsDir
} else {
    $TargetSkillsDir = Get-DefaultSkillsDir
    Write-Info "Default Claude skills path detected:"
    Write-Host "       $TargetSkillsDir"
    if (!$NoPrompt) {
        $answer = Read-Host "Use this path? [Y/n/custom]"
        if ([string]::IsNullOrWhiteSpace($answer) -or $answer -match '^[Yy]') { }
        elseif ($answer -match '^[Nn]') { Write-Fail "Installation cancelled by user." }
        elseif ($answer -match '^(custom|c)$') {
            $custom = Read-Host "Enter target Claude skills directory"
            $TargetSkillsDir = Normalize-PathText $custom
            if ([string]::IsNullOrWhiteSpace($TargetSkillsDir)) { Write-Fail "Empty target path." }
        } else { Write-Fail "Unknown choice: $answer" }
    }
}

$TargetSkillsDir = Confirm-TargetParent $TargetSkillsDir $SkillName -NoPrompt:$NoPrompt
$TargetSkillDir = Join-Path $TargetSkillsDir $SkillName
Write-Info "Install target: $TargetSkillDir"

if (!(Test-Path $TargetSkillsDir)) {
    New-Item -ItemType Directory -Force -Path $TargetSkillsDir | Out-Null
    Write-Ok "Created target skills directory: $TargetSkillsDir"
}

Warn-LegacySkillFolders $TargetSkillsDir $Manifest

if (Test-Path $TargetSkillDir) {
    Write-Warn2 "Existing skill found: $TargetSkillDir"
    if ($Backup) {
        $backupDir = "$TargetSkillDir.bak_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Move-Item -Path $TargetSkillDir -Destination $backupDir -Force
        Write-Ok "Existing skill backed up to: $backupDir"
    } elseif ($Force) {
        Remove-Item -Path $TargetSkillDir -Recurse -Force
        Write-Ok "Existing skill removed."
    } elseif ($NoPrompt) {
        Write-Fail "Existing skill found. Use -Force or -Backup with -NoPrompt."
    } else {
        $overwrite = Read-Host "Overwrite existing skill? [Y/n/backup]"
        if ([string]::IsNullOrWhiteSpace($overwrite) -or $overwrite -match '^[Yy]') {
            Remove-Item -Path $TargetSkillDir -Recurse -Force
            Write-Ok "Existing skill removed."
        } elseif ($overwrite -match '^(backup|b)$') {
            $backupDir = "$TargetSkillDir.bak_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
            Move-Item -Path $TargetSkillDir -Destination $backupDir -Force
            Write-Ok "Existing skill backed up to: $backupDir"
        } elseif ($overwrite -match '^[Nn]') {
            Write-Fail "Installation cancelled by user."
        } else { Write-Fail "Unknown choice: $overwrite" }
    }
}

Copy-Item -Path $SourceSkillDir -Destination $TargetSkillsDir -Recurse -Force
$InstalledSkillMd = Join-Path $TargetSkillDir "SKILL.md"
if (!(Test-Path $InstalledSkillMd)) { Write-Fail "Install validation failed. Missing: $InstalledSkillMd" }

$installedMissing = @()
foreach ($rel in @($Manifest.required_files)) {
    $prefix = "skills/$SkillName/"
    $relNorm = ($rel -replace '\\','/')
    if ($relNorm.StartsWith($prefix)) {
        $installedRel = $relNorm.Substring($prefix.Length)
        $installedFull = Join-RelPath $TargetSkillDir $installedRel
        if (!(Test-Path $installedFull)) { $installedMissing += $installedRel }
    }
}
if ($installedMissing.Count -gt 0) {
    Write-Warn2 "Install completed, but some manifest files were not found in the target:"
    foreach ($missing in $installedMissing) { Write-Host "  - $missing" }
    Write-Fail "Installed structure does not match manifest."
}

Write-Ok "$SkillName installed."
Write-Ok "Validated: $InstalledSkillMd"
Show-InstalledTree $TargetSkillDir
Write-Host ""
Write-Host "[NEXT] Restart Claude Code or VSCode if the skill is not visible yet."
Write-Host "[NEXT] Try: /$SkillName"
