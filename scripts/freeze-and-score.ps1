param(
    [Parameter(Mandatory = $true)][string]$TaskId,
    [Parameter(Mandatory = $true)][ValidateSet('codex','duanyan')][string]$Harness,
    [Parameter(Mandatory = $true)][ValidateSet('C0','T0','T1','T2')][string]$Condition,
    [Parameter(Mandatory = $true)][ValidateRange(1,99)][int]$Trial,
    [ValidateSet('calibration','formal')][string]$Mode = 'calibration'
)

$ErrorActionPreference = 'Stop'
if (($Harness -eq 'codex' -and $Condition -ne 'C0') -or ($Harness -eq 'duanyan' -and $Condition -eq 'C0')) {
    throw "Invalid harness/condition pairing: codex uses C0; duanyan uses T0, T1, or T2."
}
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$workspace = Join-Path $repoRoot (Join-Path 'workspaces' (Join-Path $Harness (Join-Path $Condition (Join-Path $TaskId ("trial-{0}" -f $Trial)))))
if (-not (Test-Path -LiteralPath $workspace -PathType Container)) { throw "Workspace does not exist: $workspace" }
$initialManifest = Join-Path $workspace 'INPUT_MANIFEST.sha256.tsv'
if (-not (Test-Path -LiteralPath $initialManifest -PathType Leaf)) { throw 'Initial input manifest is missing.' }
$inputFiles = @(Get-ChildItem -LiteralPath (Join-Path $workspace 'inputs') -File -Recurse | Sort-Object FullName)
$currentInputLines = @($inputFiles | ForEach-Object {
    $relative = $_.FullName.Substring($workspace.Length + 1)
    $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    "${hash}`t${relative}"
})
$initialInputLines = @(Get-Content -LiteralPath $initialManifest -Encoding utf8 | ForEach-Object { $_.TrimStart([char]0xFEFF) } | Where-Object { $_ })
if ((Compare-Object -ReferenceObject $initialInputLines -DifferenceObject $currentInputLines).Count -ne 0) {
    throw 'Input integrity check failed: files differ from the preparation manifest.'
}
$reparsePoints = @(Get-ChildItem -LiteralPath $workspace -Force -Recurse | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint })
if ($reparsePoints.Count -ne 0) { throw 'Workspace contains a reparse point; refusing to hash or score it.' }
$oracle = Join-Path $repoRoot (Join-Path 'docs\oracles' (Join-Path $TaskId 'oracle.py'))
if (-not (Test-Path -LiteralPath $oracle -PathType Leaf)) { throw "Oracle entry does not exist: $oracle" }
$checker = Join-Path (Split-Path -Parent $oracle) 'scientific_checks.py'
$accepted = (Test-Path -LiteralPath $checker -PathType Leaf) -and [bool](Select-String -LiteralPath $checker -Pattern '^\s*ACCEPTED\s*=\s*True\b' -Quiet)
if ($Mode -eq 'formal' -and -not $accepted) {
    throw "Formal scoring refused: $TaskId has no 3/3-accepted scientific checker. Use -Mode calibration only for framework evidence."
}

$resultDir = Join-Path $repoRoot (Join-Path 'results' (Join-Path $Harness (Join-Path $Condition (Join-Path $TaskId ("trial-{0}" -f $Trial)))))
if (Test-Path -LiteralPath $resultDir) { throw "Result directory already exists; evidence is append-only: $resultDir" }
New-Item -ItemType Directory -Path $resultDir | Out-Null

$manifest = Join-Path $resultDir 'FROZEN_MANIFEST.sha256.tsv'
$files = Get-ChildItem -LiteralPath $workspace -File -Recurse | Sort-Object FullName
$manifestLines = foreach ($file in $files) {
    $relative = $file.FullName.Substring($workspace.Length + 1)
    $hash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    "${hash}`t${relative}"
}
Set-Content -LiteralPath $manifest -Value $manifestLines -Encoding utf8
$manifestHash = (Get-FileHash -LiteralPath $manifest -Algorithm SHA256).Hash.ToLowerInvariant()

$oracleJson = Join-Path $resultDir 'oracle.json'
$python = Get-Command python -ErrorAction Stop
& $python.Source $oracle --workspace $workspace --json-out $oracleJson | Out-Null
$oracleExit = $LASTEXITCODE
$metadata = [ordered]@{
    recorded_at = (Get-Date).ToString('o')
    mode = $Mode
    task_id = $TaskId
    harness = $Harness
    condition = $Condition
    trial = $Trial
    workspace = $workspace
    frozen_manifest_sha256 = $manifestHash
    oracle_accepted = $accepted
    oracle_exit_code = $oracleExit
    interpretation = if ($accepted) { 'scored' } else { 'calibration_only_oracle_blocked' }
    warning = if ($accepted) { $null } else { 'Do not include this run in formal or headline results.' }
}
$metadata | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $resultDir 'run-metadata.json') -Encoding utf8

# Mark the captured workspace files read-only after all hashes are written. This is
# an evidence-preservation guard, not a substitute for filesystem ACL revocation.
$files | ForEach-Object { $_.IsReadOnly = $true }
$metadata | ConvertTo-Json -Depth 4
if ($oracleExit -ne 0) { exit $oracleExit }
