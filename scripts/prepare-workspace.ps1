param(
    [Parameter(Mandatory = $true)][string]$TaskId,
    [Parameter(Mandatory = $true)][ValidateSet('codex','duanyan')][string]$Harness,
    [Parameter(Mandatory = $true)][ValidateSet('C0','T0','T1','T2')][string]$Condition,
    [Parameter(Mandatory = $true)][ValidateRange(1,99)][int]$Trial
)

$ErrorActionPreference = 'Stop'
if (($Harness -eq 'codex' -and $Condition -ne 'C0') -or ($Harness -eq 'duanyan' -and $Condition -eq 'C0')) {
    throw "Invalid harness/condition pairing: codex uses C0; duanyan uses T0, T1, or T2."
}
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$source = Join-Path $repoRoot (Join-Path 'docs\inputs' $TaskId)
if (-not (Test-Path -LiteralPath $source -PathType Container)) { throw "Unknown task input directory: $source" }

$manifestPath = Join-Path $repoRoot 'docs\inputs\SHA256SUMS.tsv'
if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) { throw "Missing global input manifest: $manifestPath" }
$taskPrefix = "docs/inputs/${TaskId}/"
$manifestRows = @(Import-Csv -LiteralPath $manifestPath -Delimiter "`t" | Where-Object { $_.path.StartsWith($taskPrefix, [System.StringComparison]::Ordinal) })
if ($manifestRows.Count -eq 0) { throw "No global input manifest rows found for task: $TaskId" }
$manifestByPath = @{}
foreach ($row in $manifestRows) {
    if ($manifestByPath.ContainsKey($row.path)) { throw "Duplicate global input manifest row: $($row.path)" }
    $manifestByPath[$row.path] = $row
    $relative = $row.path.Substring($taskPrefix.Length).Replace('/', [System.IO.Path]::DirectorySeparatorChar)
    $expectedFile = Join-Path $source $relative
    if (-not (Test-Path -LiteralPath $expectedFile -PathType Leaf)) { throw "Manifested input file is missing: $($row.path)" }
}
$sourceFiles = @(Get-ChildItem -LiteralPath $source -File -Recurse)
foreach ($file in $sourceFiles) {
    $relative = $file.FullName.Substring($repoRoot.Length + 1).Replace([System.IO.Path]::DirectorySeparatorChar, '/')
    if (-not $manifestByPath.ContainsKey($relative)) { throw "Input file is absent from the global manifest: $relative" }
    $expected = $manifestByPath[$relative]
    $actualHash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    if ([int64]$expected.bytes -ne $file.Length -or $expected.sha256 -ne $actualHash) {
        throw "Input file does not match the global manifest: $relative"
    }
}

$workspaceRoot = Join-Path $repoRoot (Join-Path 'workspaces' (Join-Path $Harness (Join-Path $Condition (Join-Path $TaskId ("trial-{0}" -f $Trial)))))
if (Test-Path -LiteralPath $workspaceRoot) { throw "Workspace already exists; one-use workspaces are never overwritten: $workspaceRoot" }

$inputs = Join-Path $workspaceRoot 'inputs'
$output = Join-Path $workspaceRoot 'output'
New-Item -ItemType Directory -Path $inputs -ErrorAction Stop | Out-Null
New-Item -ItemType Directory -Path $output -ErrorAction Stop | Out-Null
Get-ChildItem -LiteralPath $source -Force | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $inputs -Recurse -Force -ErrorAction Stop
}

$copied = Get-ChildItem -LiteralPath $inputs -File -Recurse | Sort-Object FullName
if ($copied.Count -eq 0) { throw 'Prepared inputs directory is empty.' }
if ((Get-ChildItem -LiteralPath $output -Force).Count -ne 0) { throw 'Prepared output directory is not empty.' }

$copied | ForEach-Object {
    $relative = $_.FullName.Substring($workspaceRoot.Length + 1)
    $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    "${hash}`t${relative}"
} | Set-Content -LiteralPath (Join-Path $workspaceRoot 'INPUT_MANIFEST.sha256.tsv') -Encoding utf8

Write-Output $workspaceRoot
