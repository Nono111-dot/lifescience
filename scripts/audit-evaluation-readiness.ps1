param(
    [ValidateSet('ls06-ls10','all')][string]$Scope = 'ls06-ls10',
    [string]$JsonOut
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$oracleRoot = Join-Path $repoRoot 'docs\oracles'
$inputRoot = Join-Path $repoRoot 'docs\inputs'
$inputManifestPath = Join-Path $inputRoot 'SHA256SUMS.tsv'
$taskPattern = if ($Scope -eq 'ls06-ls10') { '^ls(06|07|08|09|10)-' } else { '^ls\d\d-' }

$manifestRows = @()
$manifestByPath = @{}
$duplicateManifestPaths = @{}
if (Test-Path -LiteralPath $inputManifestPath -PathType Leaf) {
    $manifestRows = @(Import-Csv -LiteralPath $inputManifestPath -Delimiter "`t")
    foreach ($row in $manifestRows) {
        if ($manifestByPath.ContainsKey($row.path)) {
            $duplicateManifestPaths[$row.path] = $true
        } else {
            $manifestByPath[$row.path] = $row
        }
    }
}

$rows = @()
Get-ChildItem -LiteralPath $oracleRoot -Directory | Where-Object { $_.Name -match $taskPattern } | Sort-Object Name | ForEach-Object {
    $taskId = $_.Name
    $oracle = Join-Path $_.FullName 'oracle.py'
    $checker = Join-Path $_.FullName 'scientific_checks.py'
    $inputDir = Join-Path $inputRoot $taskId
    $inputFiles = if (Test-Path -LiteralPath $inputDir -PathType Container) {
        @(Get-ChildItem -LiteralPath $inputDir -File -Recurse)
    } else { @() }
    $inputCount = $inputFiles.Count
    $accepted = $false
    if (Test-Path -LiteralPath $checker -PathType Leaf) {
        $accepted = [bool](Select-String -LiteralPath $checker -Pattern '^\s*ACCEPTED\s*=\s*True\b' -Quiet)
    }
    $reasons = @()
    if (-not (Test-Path -LiteralPath $oracle -PathType Leaf)) { $reasons += 'missing_oracle_entry' }
    if ($inputCount -eq 0) { $reasons += 'missing_inputs' }
    if ($manifestRows.Count -eq 0) {
        $reasons += 'missing_global_input_manifest'
    } else {
        $taskPrefix = "docs/inputs/${taskId}/"
        $expectedRows = @($manifestRows | Where-Object { $_.path.StartsWith($taskPrefix, [System.StringComparison]::Ordinal) })
        foreach ($expected in $expectedRows) {
            $expectedRelative = $expected.path.Substring($taskPrefix.Length).Replace('/', [System.IO.Path]::DirectorySeparatorChar)
            $expectedFile = Join-Path $inputDir $expectedRelative
            if (-not (Test-Path -LiteralPath $expectedFile -PathType Leaf)) {
                $reasons += "manifest_file_missing:$($expected.path)"
            }
        }
        foreach ($file in $inputFiles) {
            $relative = $file.FullName.Substring($repoRoot.Length + 1).Replace([System.IO.Path]::DirectorySeparatorChar, '/')
            if (-not $manifestByPath.ContainsKey($relative)) {
                $reasons += "manifest_entry_missing:${relative}"
                continue
            }
            if ($duplicateManifestPaths.ContainsKey($relative)) {
                $reasons += "manifest_entry_duplicate:${relative}"
                continue
            }
            $expected = $manifestByPath[$relative]
            $actualHash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            if ([int64]$expected.bytes -ne $file.Length -or $expected.sha256 -ne $actualHash) {
                $reasons += "manifest_entry_stale:${relative}"
            }
        }
    }
    if (-not (Test-Path -LiteralPath $checker -PathType Leaf)) { $reasons += 'missing_scientific_checker' }
    elseif (-not $accepted) { $reasons += 'oracle_not_3of3_accepted' }
    $reasons = @($reasons | Sort-Object -Unique)
    $manifestFailures = @($reasons | Where-Object { $_ -match '^(missing_global_input_manifest|manifest_)' })
    $rows += [pscustomobject]@{
        task_id = $taskId
        input_file_count = $inputCount
        oracle_entry = Test-Path -LiteralPath $oracle -PathType Leaf
        scientific_checker = Test-Path -LiteralPath $checker -PathType Leaf
        input_manifest_ok = ($manifestFailures.Count -eq 0)
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
