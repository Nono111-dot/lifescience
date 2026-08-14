param([string]$OutFile)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$resultRoot = Join-Path $repoRoot 'results'
$records = @()
if (Test-Path -LiteralPath $resultRoot -PathType Container) {
    Get-ChildItem -LiteralPath $resultRoot -Filter run-metadata.json -File -Recurse | Sort-Object FullName | ForEach-Object {
        $meta = Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json
        $oraclePath = Join-Path $_.Directory.FullName 'oracle.json'
        $oracle = if (Test-Path -LiteralPath $oraclePath) { Get-Content -LiteralPath $oraclePath -Raw | ConvertFrom-Json } else { $null }
        $records += [pscustomobject]@{
            task_id = $meta.task_id; harness = $meta.harness; condition = $meta.condition; trial = $meta.trial
            mode = $meta.mode; interpretation = $meta.interpretation
            grader_status = if ($oracle) { $oracle.grader_status } else { 'missing' }
            hardgate_pass = if ($oracle) { $oracle.hardgate_pass } else { $false }
            deterministic_score = if ($oracle) { $oracle.deterministic_score } else { $null }
            failure_codes = if ($oracle) { @($oracle.failure_codes) -join ',' } else { 'ORACLE_JSON_MISSING' }
        }
    }
}
$lines = @('# Evaluation result summary', '', "Generated: $((Get-Date).ToString('o'))", '', "Runs captured: $($records.Count)", '')
if ($records.Count -eq 0) {
    $lines += 'No frozen run results found.'
} else {
    $formal = @($records | Where-Object { $_.mode -eq 'formal' -and $_.grader_status -eq 'scored' })
    $calibration = @($records | Where-Object { $_.mode -ne 'formal' -or $_.grader_status -ne 'scored' })
    $lines += "Formal scored runs: $($formal.Count)"
    $lines += "Calibration/non-scoreable runs: $($calibration.Count)"
    $lines += ''
    $lines += '| Task | Harness | Condition | Trial | Mode | Grader | Deterministic | Hard gate | Failures |'
    $lines += '|---|---|---:|---:|---|---|---:|---|---|'
    foreach ($r in $records) {
        $score = if ($null -eq $r.deterministic_score) { 'N/A' } else { [string]$r.deterministic_score }
        $lines += "| $($r.task_id) | $($r.harness) | $($r.condition) | $($r.trial) | $($r.mode) | $($r.grader_status) | $score | $($r.hardgate_pass) | $($r.failure_codes) |"
    }
}
$markdown = $lines -join "`n"
if ($OutFile) { Set-Content -LiteralPath $OutFile -Value $markdown -Encoding utf8 }
$markdown
