$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot

$packages = @(
    @('ls06-eno1-effect-size','bix-37.zip','40cbef03-b5c3-4448-b00f-0ba2965dea9b'),
    @('ls06-eno1-significance-audit','bix-37.zip','40cbef03-b5c3-4448-b00f-0ba2965dea9b'),
    @('ls07-combination-treatment-deg','bix-43.zip','15ff11e5-2db1-45b6-b3a3-46bc2a74b821'),
    @('ls07-combination-treatment-mechanism','bix-43.zip','15ff11e5-2db1-45b6-b3a3-46bc2a74b821'),
    @('ls10-neun-power-analysis','bix-19.zip','8c64b1fa-fdcc-41e2-be8d-2f0c8d5faaa1'),
    @('ls10-treatment-response-model','bix-51.zip','93f63fb8-b56c-4ad1-8d3b-d651e2107423')
)

foreach ($package in $packages) {
    $taskDir = Join-Path $repoRoot ("docs\inputs\" + $package[0])
    $archive = Join-Path $taskDir $package[1]
    if (-not (Test-Path -LiteralPath $archive)) {
        Write-Host "SKIP missing $($package[0])/$($package[1])"
        continue
    }
    $tempDir = Join-Path $taskDir '_extract'
    if (Test-Path -LiteralPath $tempDir) { throw "Unexpected existing temp directory: $tempDir" }
    New-Item -ItemType Directory -Path $tempDir | Out-Null
    Expand-Archive -LiteralPath $archive -DestinationPath $tempDir
    $dataDir = Join-Path $tempDir ("CapsuleData-" + $package[2])
    if (-not (Test-Path -LiteralPath $dataDir -PathType Container)) {
        throw "Expected CapsuleData directory not found in $archive"
    }
    Get-ChildItem -LiteralPath $dataDir -Force | ForEach-Object {
        Move-Item -LiteralPath $_.FullName -Destination $taskDir
    }
    Remove-Item -LiteralPath $tempDir -Recurse
    Remove-Item -LiteralPath $archive
    Write-Host "PREPARED $($package[0]) (data only; notebook excluded)"
}
