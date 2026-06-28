# ============================================================
# SCG Failure Pre-filter
# 용도: 대용량 로그에서 SCG 관련 줄만 추출하여 LLM 분석 입력 생성
# 실행: .\scg_failure_prefilter.ps1 -InputLog "service.log"
# ============================================================

param(
    [string]$InputLog  = "service.log",
    [string]$OutputTxt = "scg_signal.txt",
    [int]   $Context   = 20        # 매칭 전후 몇 줄 포함할지
)

# ============================================================
# Keywords - 이 블록만 수정하면 됩니다
# 주의: 아래는 모두 추정 키워드입니다
#       실제 로그 확인 후 # 확인됨 / # 삭제 로 표시 업데이트 필요
# ============================================================
$keywords = @(
    "scgFail",              # 추정
    "SCG",                  # 추정
    "PSCell",               # 추정
    "B1Event", "B2Event",   # 추정
    "measReport",           # 추정
    "RLF",                  # 추정 (Radio Link Failure)
    "T310", "T311",         # 추정 (RLF 타이머)
    "beamFail",             # 추정
    "dualConn",             # 추정
    "SCG-Config"            # 추정
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
