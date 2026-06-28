<#
.SYNOPSIS
  Compare two rca_kg/cases directories and print a merge plan (read-only by default).

.DESCRIPTION
  잘못 생긴 KG(SourceCasesDir)와 정본 KG(TargetCasesDir)의 case YAML을 대조해
  fingerprint(signature_set + sequence) 기준으로 다음을 분류한다.
    - NEW    : 정본에 없는 case (그냥 이동하면 됨)
    - DUP    : fingerprint가 정본과 겹침 (occurrence 합산 수동 병합 필요)
    - SAMEID : case_id가 같음 (동일 case 가능성 — 수동 확인)
  기본은 읽기 전용(계획만 출력). -MovePlan 을 주면 NEW 케이스 이동 PowerShell을
  '실행하지 않고' 화면에 출력한다. 실제 이동/합산은 사람이 STRUCTURE_FIX_GUIDE §6 대로 한다.

  이 스크립트는 어떤 파일도 수정·삭제·이동하지 않는다. 분석 전용.

.PARAMETER SourceCasesDir
  잘못 생긴 KG의 cases 폴더. 예: C:\logs\block_x\rca_kg\cases

.PARAMETER TargetCasesDir
  정본 KG의 cases 폴더. 예: C:\work\RCA_standalone\rca_kg\cases

.PARAMETER IncludeUnresolved
  cases\unresolved 도 함께 대조한다.

.PARAMETER MovePlan
  NEW 케이스 이동용 PowerShell 명령을 출력한다(실행 안 함).

.EXAMPLE
  .\compare_kg_cases.ps1 -SourceCasesDir "C:\logs\blk\rca_kg\cases" -TargetCasesDir "C:\work\RCA_standalone\rca_kg\cases"

.EXAMPLE
  .\compare_kg_cases.ps1 -SourceCasesDir "..." -TargetCasesDir "..." -IncludeUnresolved -MovePlan
#>
param(
    [Parameter(Mandatory = $true)] [string]$SourceCasesDir,
    [Parameter(Mandatory = $true)] [string]$TargetCasesDir,
    [switch]$IncludeUnresolved,
    [switch]$MovePlan
)

$ErrorActionPreference = "Stop"

function Write-Info([string]$m) { Write-Host "[INFO] $m" }
function Write-Warn2([string]$m) { Write-Host "[WARN] $m" }
function Write-Fail([string]$m) { Write-Host "[FAIL] $m"; exit 1 }

if (!(Test-Path $SourceCasesDir)) { Write-Fail "SourceCasesDir not found: $SourceCasesDir" }
if (!(Test-Path $TargetCasesDir)) { Write-Fail "TargetCasesDir not found: $TargetCasesDir" }

# ── 아주 단순한 case YAML 파서 (외부 모듈 없이 동작) ──
# case_id, fingerprint.signature_set, fingerprint.sequence, occurrence_count 만 뽑는다.
function Read-CaseFingerprint([string]$Path) {
    $caseId = $null
    $sequence = $null
    $occ = $null
    $sigSet = @()
    $inSigSet = $false
    foreach ($raw in Get-Content -Path $Path -Encoding UTF8) {
        $line = $raw -replace "`t", "    "
        $trim = $line.Trim()
        if ($trim.StartsWith("#") -or [string]::IsNullOrWhiteSpace($trim)) { continue }

        if ($trim -match '^case_id:\s*(.+)$') { $caseId = $matches[1].Trim().Trim('"').Trim("'"); continue }
        if ($trim -match '^occurrence_count:\s*(\d+)') { $occ = [int]$matches[1]; continue }
        if ($trim -match '^sequence:\s*(.+)$') { $sequence = $matches[1].Trim().Trim('"').Trim("'"); continue }

        # signature_set: 블록 진입/이탈 판정 (들여쓰기 기반)
        if ($trim -match '^signature_set:\s*$') { $inSigSet = $true; continue }
        if ($inSigSet) {
            if ($trim -match '^-\s*(.+)$') {
                $sigSet += $matches[1].Trim().Trim('"').Trim("'")
                continue
            } else {
                # 리스트 항목이 아니면 블록 종료
                $inSigSet = $false
            }
        }
    }
    # fingerprint key: signature_set 정렬 + sequence
    $sigKey = ($sigSet | Sort-Object) -join "|"
    $fpKey = "$sigKey##$sequence"
    return [pscustomobject]@{
        file       = (Split-Path $Path -Leaf)
        full_path  = $Path
        case_id    = $caseId
        seq        = $sequence
        sig_set    = ($sigSet -join ",")
        occurrence = $occ
        fp_key     = $fpKey
    }
}

function Get-CaseFiles([string]$Dir) {
    Get-ChildItem -Path $Dir -Filter "*.yaml" -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -notlike "EXAMPLE*" }
}

function Compare-Dir([string]$Src, [string]$Dst, [string]$Label) {
    Write-Host ""
    Write-Host "==================== $Label ===================="
    Write-Host "Source: $Src"
    Write-Host "Target: $Dst"

    $srcCases = @(Get-CaseFiles $Src | ForEach-Object { Read-CaseFingerprint $_.FullName })
    $dstCases = @(Get-CaseFiles $Dst | ForEach-Object { Read-CaseFingerprint $_.FullName })

    if ($srcCases.Count -eq 0) { Write-Info "Source에 비교 대상 case 없음 (EXAMPLE 제외)."; return @() }

    $dstByFp = @{}
    foreach ($d in $dstCases) { if (!$dstByFp.ContainsKey($d.fp_key)) { $dstByFp[$d.fp_key] = @() }; $dstByFp[$d.fp_key] += $d }
    $dstById = @{}
    foreach ($d in $dstCases) { if ($d.case_id) { $dstById[$d.case_id] = $d } }

    $rows = @()
    foreach ($s in $srcCases) {
        $verdict = "NEW"
        $note = "정본에 없음 → 이동"
        if ($s.case_id -and $dstById.ContainsKey($s.case_id)) {
            $verdict = "SAMEID"; $note = "정본에 같은 case_id 존재 → 수동 확인"
        }
        if ($dstByFp.ContainsKey($s.fp_key) -and $s.fp_key -ne "##") {
            $verdict = "DUP"
            $dupFiles = ($dstByFp[$s.fp_key] | ForEach-Object { $_.file }) -join ", "
            $note = "fingerprint 겹침 → occurrence 합산 병합 ($dupFiles)"
        }
        $rows += [pscustomobject]@{
            verdict    = $verdict
            file       = $s.file
            case_id    = $s.case_id
            occ        = $s.occurrence
            note       = $note
            full_path  = $s.full_path
        }
    }

    $rows | Sort-Object verdict, file | Format-Table verdict, file, case_id, occ, note -AutoSize -Wrap | Out-String | Write-Host

    $n = ($rows | Where-Object { $_.verdict -eq "NEW" }).Count
    $d = ($rows | Where-Object { $_.verdict -eq "DUP" }).Count
    $i = ($rows | Where-Object { $_.verdict -eq "SAMEID" }).Count
    Write-Host ("요약 [$Label]: NEW=$n  DUP=$d  SAMEID=$i  (source 총 {0})" -f $srcCases.Count)

    return $rows
}

function Show-MovePlan($Rows, [string]$Dst, [string]$Label) {
    $newRows = @($Rows | Where-Object { $_.verdict -eq "NEW" })
    if ($newRows.Count -eq 0) { return }
    Write-Host ""
    Write-Host "---- 이동 계획 (NEW only, $Label) — 실행 안 함. 확인 후 직접 실행 ----"
    foreach ($r in $newRows) {
        $target = Join-Path $Dst $r.file
        Write-Host "Move-Item `"$($r.full_path)`" `"$target`""
    }
    Write-Host "---- DUP/SAMEID 는 STRUCTURE_FIX_GUIDE.md §6.3 대로 occurrence 합산 수동 병합 ----"
}

# ── cases ──
$srcCasesRoot = $SourceCasesDir.TrimEnd('\','/')
$dstCasesRoot = $TargetCasesDir.TrimEnd('\','/')
$casesRows = Compare-Dir $srcCasesRoot $dstCasesRoot "cases"
if ($MovePlan) { Show-MovePlan $casesRows $dstCasesRoot "cases" }

# ── unresolved ──
if ($IncludeUnresolved) {
    $srcUn = Join-Path $srcCasesRoot "unresolved"
    $dstUn = Join-Path $dstCasesRoot "unresolved"
    if (Test-Path $srcUn) {
        $unRows = Compare-Dir $srcUn $dstUn "cases/unresolved"
        if ($MovePlan) { Show-MovePlan $unRows $dstUn "cases/unresolved" }
    } else {
        Write-Info "Source에 unresolved 폴더 없음 — 건너뜀."
    }
}

Write-Host ""
Write-Info "이 스크립트는 읽기 전용이다. 어떤 파일도 옮기거나 지우지 않았다."
Write-Info "병합 절차 전체: STRUCTURE_FIX_GUIDE.md §6"
Write-Host ""
Write-Host "[진행: KG 대조 완료 → 다음: §6.3 NEW 이동 + DUP 합산]"
Write-Host "▶ 다음: 위 표의 DUP/SAMEID 건을 사람이 확인 후 정본으로 병합"
