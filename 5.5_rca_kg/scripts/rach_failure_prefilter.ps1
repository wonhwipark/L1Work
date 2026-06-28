# ============================================================
# RACH Failure Pre-filter
# 용도: 대용량 로그에서 RACH 관련 줄만 추출하여 LLM 분석 입력 생성
# 실행: .\rach_failure_prefilter.ps1 -InputLog "service.log"
# ============================================================

param(
    [string]$InputLog  = "service.log",
    [string]$OutputTxt = "rach_signal.txt",
    [int]   $Context   = 20        # 매칭 전후 몇 줄 포함할지
)

# ============================================================
# Keywords - 이 블록만 수정하면 됩니다
# ============================================================
$keywords = @(
    "PHY_TIMER_EXPIRY",     # 확인됨
    "RACH",                 # 추정 - 로그 확인 후 유지/삭제
    "preamble",             # 추정
    "RAR",                  # 추정
    "Msg1", "Msg2", "Msg3", "Msg4",  # 추정
    "rach_fail",            # 추정
    "RA-RNTI"               # 추정
)
# ============================================================

if (-not (Test-Path $InputLog)) {
    Write-Error "입력 파일 없음: $InputLog"
    exit 1
}

$pattern = ($keywords | ForEach-Object { [regex]::Escape($_) }) -join "|"

Write-Host "입력: $InputLog"
Write-Host "키워드: $($keywords -join ', ')"
Write-Host "전후 context: $Context 줄"

Select-String -Path $InputLog -Pattern $pattern -Context $Context, $Context `
    | Out-File $OutputTxt -Encoding utf8

$lineCount = (Get-Content $OutputTxt | Measure-Object -Line).Lines
Write-Host "완료: $OutputTxt ($lineCount 줄)"
