param(
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$inputsRoot = Join-Path $repoRoot 'docs\inputs'

function Get-InputFile {
    param(
        [Parameter(Mandatory=$true)][string]$TaskId,
        [Parameter(Mandatory=$true)][string]$FileName,
        [Parameter(Mandatory=$true)][string]$Url
    )
    $taskDir = Join-Path $inputsRoot $TaskId
    New-Item -ItemType Directory -Force -Path $taskDir | Out-Null
    $target = Join-Path $taskDir $FileName
    if ((Test-Path -LiteralPath $target) -and ((Get-Item -LiteralPath $target).Length -gt 0) -and -not $Force) {
        Write-Host "SKIP $TaskId/$FileName"
        return
    }
    Write-Host "GET  $TaskId/$FileName"
    Invoke-WebRequest -Uri $Url -OutFile $target -MaximumRedirection 10
}

$hfCompBio = 'https://huggingface.co/datasets/Genentech/compbiobench-data-v1/resolve/main/data'
$hfBix = 'https://huggingface.co/datasets/futurehouse/BixBench/resolve/main'

$downloads = @(
    @('ls02-deleterious-mutation','deleterious.mutation.q2.R1.fq.gz',"$hfCompBio/deleterious.mutation.q2.R1.fq.gz?download=true"),
    @('ls02-find-deletion','find.deletion.r1.fq.gz',"$hfCompBio/find.deletion.r1.fq.gz?download=true"),
    @('ls02-find-deletion','find.deletion.r2.fq.gz',"$hfCompBio/find.deletion.r2.fq.gz?download=true"),
    @('ls02-infer-genome-build','vcf.infer.build.q1.vcf.gz',"$hfCompBio/vcf.infer.build.q1.vcf.gz?download=true"),
    @('ls03-cryptic-exon','cryptic.exon.q1.fq.gz',"$hfCompBio/cryptic.exon.q1.fq.gz?download=true"),
    @('ls03-atac-sample-swap','sample.swap.atac.q1.tsv.gz',"$hfCompBio/sample.swap.atac.q1.tsv.gz?download=true"),
    @('ls03-atac-sample-swap','sample.swap.atac.q1.chrom.sizes',"$hfCompBio/sample.swap.atac.q1.chrom.sizes?download=true"),
    @('ls03-genome-coordinates','single_cell_dynamics_question.csv',"$hfCompBio/single_cell_dynamics_question.csv?download=true"),
    @('ls04-differential-composition','differential.composition.q1.1.mtx.gz',"$hfCompBio/differential.composition.q1.1.mtx.gz?download=true"),
    @('ls04-differential-composition','differential.composition.q1.2.mtx.gz',"$hfCompBio/differential.composition.q1.2.mtx.gz?download=true"),
    @('ls04-differential-composition','differential.composition.q1.genes.txt.gz',"$hfCompBio/differential.composition.q1.genes.txt.gz?download=true"),
    @('ls04-perturbseq-reference-map','perturb.seq.align.q1.ref.h5ad',"$hfCompBio/perturb.seq.align.q1.ref.h5ad?download=true"),
    @('ls04-perturbseq-reference-map','perturb.seq.align.q1.query.h5ad',"$hfCompBio/perturb.seq.align.q1.query.h5ad?download=true"),
    @('ls04-spatial-deconvolution','spatial.sim.tar.gz',"$hfCompBio/spatial.sim.tar.gz?download=true"),
    @('ls05-protein-shape','protein.shape.q1.pdb',"$hfCompBio/protein.shape.q1.pdb?download=true"),
    @('ls08-multiome-column-match','multiome.match.atac.rna.q1.rna.tsv.gz',"$hfCompBio/multiome.match.atac.rna.q1.rna.tsv.gz?download=true"),
    @('ls08-multiome-column-match','multiome.match.atac.rna.q1.atac.tsv.gz',"$hfCompBio/multiome.match.atac.rna.q1.atac.tsv.gz?download=true"),
    @('ls08-enhancer-promoter-integration','ep.interactions.q1.hic.csv',"$hfCompBio/ep.interactions.q1.hic.csv?download=true"),
    @('ls08-enhancer-promoter-integration','ep.interactions.q1.expr.csv',"$hfCompBio/ep.interactions.q1.expr.csv?download=true"),
    @('ls06-eno1-effect-size','bix-37.zip',"$hfBix/CapsuleFolder-40cbef03-b5c3-4448-b00f-0ba2965dea9b.zip?download=true"),
    @('ls06-eno1-significance-audit','bix-37.zip',"$hfBix/CapsuleFolder-40cbef03-b5c3-4448-b00f-0ba2965dea9b.zip?download=true"),
    @('ls07-combination-treatment-deg','bix-43.zip',"$hfBix/CapsuleFolder-15ff11e5-2db1-45b6-b3a3-46bc2a74b821.zip?download=true"),
    @('ls07-combination-treatment-mechanism','bix-43.zip',"$hfBix/CapsuleFolder-15ff11e5-2db1-45b6-b3a3-46bc2a74b821.zip?download=true"),
    @('ls10-neun-power-analysis','bix-19.zip',"$hfBix/CapsuleFolder-8c64b1fa-fdcc-41e2-be8d-2f0c8d5faaa1.zip?download=true"),
    @('ls10-treatment-response-model','bix-51.zip',"$hfBix/CapsuleFolder-93f63fb8-b56c-4ad1-8d3b-d651e2107423.zip?download=true")
)

foreach ($item in $downloads) {
    Get-InputFile -TaskId $item[0] -FileName $item[1] -Url $item[2]
}

$inventory = foreach ($file in Get-ChildItem -Path $inputsRoot -Recurse -File) {
    if ($file.Name -eq 'SHA256SUMS.tsv') { continue }
    [pscustomobject]@{
        path = $file.FullName.Substring($repoRoot.Length + 1).Replace('\','/')
        bytes = $file.Length
        sha256 = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    }
}
$inventory | Sort-Object path | Export-Csv -Path (Join-Path $inputsRoot 'SHA256SUMS.tsv') -Delimiter "`t" -NoTypeInformation
Write-Host "Wrote docs/inputs/SHA256SUMS.tsv"
