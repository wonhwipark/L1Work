param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot ".."))
)

$ErrorActionPreference = "Stop"
$failed = $false
$ExpectedVersion = "convenience_v0.21_kg_root_config"
function Pass($msg) { Write-Host "[OK]   $msg" }
function Warn($msg) { Write-Host "[WARN] $msg"; $script:failed = $true }
function Info($msg) { Write-Host "[INFO] $msg" }
function Join-RelPath([string]$Root, [string]$RelPath) {
  $parts = $RelPath -split '[\\/]+'; $path = $Root
  foreach ($part in $parts) { if (![string]::IsNullOrWhiteSpace($part)) { $path = Join-Path $path $part } }
  return $path
}
function Read-All($rel) { return Get-Content (Join-RelPath $Root $rel) -Raw -ErrorAction SilentlyContinue }

Info "RCA package validation root: $Root"

$required = @(
  "README.md", "START_HERE_5.5.md", "NEXT_STEP_5.5.md", "USER_GUIDE_5.5.md",
  "INSTALL_SKILL.md", "KG_ROOT_GUIDE.md", "STRUCTURE_FIX_GUIDE.md", "rca_config.yaml",
  "configure_kg_root.ps1", "install_skill.ps1", "validate_install.ps1",
  "skills/root-cause-analyzer/SKILL.md",
  "skills/root-cause-analyzer/references/p0_env_probe.md",
  "skills/root-cause-analyzer/references/p1_format_probe.md",
  "skills/root-cause-analyzer/references/p2_manifest_fragments.md",
  "RUNBOOK_L1SW_TO_P6_5.5.md",
  "rca_kg/runtime_tool_generate/current_run.yaml",
  "rca_kg/runtime_tool_generate/current_run.example.yaml",
  "rca_kg/runtime_tool_generate/format_profiles/README.md",
  "rca_kg/signals_tool_generate/README.md",
  "rca_kg/indexes_tool_generate/index.md",
  "rca_kg/schema/taxonomy.yaml",
  "rca_kg/keywords.yaml"
)
foreach ($rel in $required) {
  $path = Join-RelPath $Root $rel
  if (Test-Path $path) { Pass "exists: $rel" } else { Warn "missing: $rel" }
}

$activeVersionFiles = @("README.md", "START_HERE_5.5.md", "USER_GUIDE_5.5.md", "NEXT_STEP_5.5.md", "VERSION_5.5.md", "skill_manifest.yaml", "rca_config.yaml", "rca_kg/runtime_tool_generate/current_run.yaml", "rca_kg/runtime_tool_generate/current_run.example.yaml")
foreach ($rel in $activeVersionFiles) {
  $txt = Read-All $rel
  if ($txt -and $txt.Contains($ExpectedVersion)) { Pass "version ok: $rel" } else { Warn "version missing or stale: $rel" }
}

$activeFiles = Get-ChildItem $Root -Recurse -File -Include *.md,*.ps1,*.yaml,*.yml,*.json |
  Where-Object { $_.FullName -notmatch "[\\/]delta[\\/]" -and $_.FullName -notmatch "[\\/]review_logs[\\/]" -and $_.FullName -notmatch "[\\/]prompt[\\/]" }
$staleHits = @()
foreach ($f in $activeFiles) {
  if ($f.Name -eq "validate_package.ps1") { continue }
  $content = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
  if ($content -match "convenience_v0\.(18|19)([^0-9]|$)") { $staleHits += $f.FullName }
}
if ($staleHits.Count -eq 0) { Pass "no stale v0.18/v0.19 package versions in active docs" } else { Warn "stale package version found:`n$($staleHits -join "`n")" }

$skill = Read-All "skills/root-cause-analyzer/SKILL.md"
if ($skill -match "workspace_root" -and $skill -match "kg_root" -and $skill -match "\.claude/skills|\\.claude\\skills") { Pass "SKILL.md explains workspace_root/kg_root separation and skill-folder guard" } else { Warn "SKILL.md missing kg_root separation or skill-folder guard" }
if ($skill -match "\{kg_root\}/runtime_tool_generate/current_run.yaml") { Pass "SKILL.md state SSOT uses kg_root" } else { Warn "SKILL.md state SSOT does not use kg_root" }

$p1 = Read-All "skills/root-cause-analyzer/references/p1_format_probe.md"
if ($p1 -match "\{kg_root\}/runtime_tool_generate/format_profiles") { Pass "P1 writes format profile under kg_root" } else { Warn "P1 still writes format profile outside kg_root" }

# P1~P6 runtime outputs should use {kg_root}; P0/SKILL may mention the default {workspace_root}/rca_kg.
$badRuntimePathHits = @()
$runtimeRefFiles = Get-ChildItem (Join-Path $Root "skills/root-cause-analyzer/references") -File -Filter "p*.md" |
  Where-Object { $_.Name -notmatch "^p0_" }
foreach ($f in $runtimeRefFiles) {
  $content = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
  if ($content.Contains("{workspace_root}/rca_kg/") -or $content.Contains('{workspace_root}\rca_kg\')) { $badRuntimePathHits += $f.FullName }
}
if ($badRuntimePathHits.Count -eq 0) { Pass "P1~P6 runtime output paths use kg_root" } else { Warn "old workspace_root/rca_kg runtime path found:`n$($badRuntimePathHits -join "`n")" }

$keywords = Read-All "rca_kg/keywords.yaml"
foreach ($issue in @("rach_failure", "scg_failure", "tx_abnormal", "l2_max_retransmission")) {
  if ($keywords -match $issue) { Pass "keywords contains issue_type: $issue" } else { Warn "keywords missing issue_type text: $issue" }
}

if ($failed) {
  Write-Host "`n[RESULT] validation completed with warnings/failures. Review items above."
  exit 1
} else {
  Write-Host "`n[RESULT] validation passed."
  exit 0
}
