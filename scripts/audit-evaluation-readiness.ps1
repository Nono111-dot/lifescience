param(
    [ValidateSet('ls06-ls10','all')][string]$Scope = 'ls06-ls10',
    [string]$JsonOut
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$oracleRoot = Join-Path $repoRoot 'docs\oracles'
$inputRoot = Join-Path $repoRoot 'docs\inputs'
$taskPattern = if ($Scope -eq 'ls06-ls10') { '^ls(06|07|08|09|10)-' } else { '^ls\d\d-' }

$rows = @()
Get-ChildItem -LiteralPath $oracleRoot -Directory | Where-Object { $_.Name -match $taskPattern } | Sort-Object Name | ForEach-Object {
    $taskId = $_.Name
    $oracle = Join-Path $_.FullName 'oracle.py'
    $checker = Join-Path $_.FullName 'scientific_checks.py'
    $inputDir = Join-Path $inputRoot $taskId
    $inputCount = if (Test-Path -LiteralPath $inputDir -PathType Container) {
        @(Get-ChildItem -LiteralPath $inputDir -File -Recurse).Count
    } else { 0 }
    $accepted = $false
    if (Test-Path -LiteralPath $checker -PathType Leaf) {
        $accepted = [bool](Select-String -LiteralPath $checker -Pattern '^\s*ACCEPTED\s*=\s*True\b' -Quiet)
    }
    $reasons = @()
    if (-not (Test-Path -LiteralPath $oracle -PathType Leaf)) { $reasons += 'missing_oracle_entry' }
    if ($inputCount -eq 0) { $reasons += 'missing_inputs' }
    if (-not (Test-Path -LiteralPath $checker -PathType Leaf)) { $reasons += 'missing_scientific_checker' }
    elseif (-not $accepted) { $reasons += 'oracle_not_3of3_accepted' }
    $rows += [pscustomobject]@{
        task_id = $taskId
        input_file_count = $inputCount
        oracle_entry = Test-Path -LiteralPath $oracle -PathType Leaf
        scientific_checker = Test-Path -LiteralPath $checker -PathType Leaf
        oracle_accepted = $accepted
        formal_ready = ($reasons.Count -eq 0)
        blockers = $reasons
    }
}

$payload = [ordered]@{
    generated_at = (Get-Date).ToString('o')
    scope = $Scope
    task_count = $rows.Count
    formal_ready_count = @($rows | Where-Object formal_ready).Count
    calibration_only_count = @($rows | Where-Object { -not $_.formal_ready }).Count
    tasks = $rows
}
$json = $payload | ConvertTo-Json -Depth 5
if ($JsonOut) {
    $target = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $JsonOut))
    $parent = Split-Path -Parent $target
    if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent | Out-Null }
    Set-Content -LiteralPath $target -Value $json -Encoding utf8
}
$json
if ($payload.formal_ready_count -ne $payload.task_count) { exit 2 }
