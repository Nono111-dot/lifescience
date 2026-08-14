# CompBioBench来源题逐题公开边界

以下12题均来自公开的 `compbiobench.v1.tsv`。这里的“verifier边界”对每题相同：公开数据没有答案列，公开 runner 只运行agent、抽取答案和保存trace；官方正确性由私有 server-side leaderboard判定。因而下文只确认题面规定的答案形态，**不声称知道官方gold或其容错规则**。

## `deleterious-mutation-q2` → `ls02-deleterious-mutation`

- 原生问题：在仅覆盖人chr9一个50 Mb区块的单端1×150 bp外显子组FASTQ中，找出一个高度LoF不耐受基因里的高置信度、符合体细胞嵌合的nonsense SNV；报告大写HGNC符号和四舍五入到最近10%的alternate allele frequency。
- 原生答案形式：`GENE,10`式的单行答案。
- `internet_required=True`；输入：`deleterious.mutation.q2.R1.fq.gz`。
- 可公开检查：HGNC样式、逗号分隔、整数百分数。基因/AF正确性必须由私有leaderboard或冻结reference后独立复算。
- 不可从公开资料声称：官方比对器、variant caller、LoF数据库版本、最小深度/alt reads、AF额外容差。

## `find-deletion-q1` → `ls02-find-deletion`

- 原生问题：从模拟于hg38某条染色体、含大缺失的浅层paired-end WGS FASTQ定位近似缺失坐标；起止坐标均四舍五入到最近100,000 bp。
- 原生答案形式：`chr:start-end`，示例 `chr1:10000000-10300000`。
- `internet_required=True`；输入：R1/R2 FASTQ。
- 可公开检查：格式、start<end、端点是100,000倍数。没有公开gold或除原生舍入外的官方误差带。

## `vcf-infer-build-q1` → `ls02-infer-genome-build`

- 原生问题：给定无rsID、header不声明build的chr20双等位SNP VCF，根据坐标和REF判断reference build。
- 原生答案形式：只能是 `hg18`、`hg19`、`hg38`、`T2T-CHM13`之一。
- `internet_required=True`；输入：`vcf.infer.build.q1.vcf.gz`。
- 可公开检查：闭集标签精确匹配。公开资料没有官方match-rate cutoff或gold。

## `cryptic-exon-q1` → `ls03-cryptic-exon`

- 原生问题：人bulk RNA-seq FASTQ中恰有一个高表达coding gene，含由两个novel junction形成的cryptic exon；报告基因。
- 原生答案形式：一个大写HGNC gene symbol。
- `internet_required=True`；输入：`cryptic.exon.q1.fq.gz`。
- 可公开检查：单个大写符号。novelty依赖的genome/annotation版本、junction支持阈值和官方gold均未公开。

## `sample-swap-atac-q1` → `ls03-atac-sample-swap`

- 原生问题：依据axolotl organs的bulk ATAC count和AmexG_v6.0-DD染色体chunk信息判断是否sample swap。
- 原生答案形式：无swap时 `None`；否则以case-sensitive lexicographic order输出两个名称，如 `Brain,GallBladder`。
- `internet_required=True`；输入：counts TSV和chrom sizes。
- 可公开检查：`None`或有序二元字符串。题面混用“organ”和“cell type”，官方gold/marker依据未公开。

## `genome-coords-q1` → `ls03-genome-coordinates`

- 原生问题：600个cell、每个250个连续time point；由enhancer/promoter三维坐标计算Euclidean distance，并把`distance <= 260 nm`定义为contact；仅基于计算量选择最可辩护结论。
- 原生答案形式：单个字母A–E。A独立无关系；B转录促进接近；C接近促进转录；D反馈环；E题面未覆盖的另一解释。
- `internet_required=False`；输入：`single_cell_dynamics_question.csv`。
- 可公开检查：A–E闭集以及distance/contact的确定性复算。题面未给关联、lag或因果裁决阈值，私有gold不可见。

## `differential-composition-q1` → `ls04-differential-composition`

- 原生问题：两个视网膜个体的raw scRNA matrix（列为通过QC的barcode）中，有一种cell type在一名个体中严重depleted；从指定16个label里选择其名称。
- 原生答案形式：指定label vocabulary中的一个名称。
- `internet_required=True`；输入：两个MTX和common genes列表。
- 可公开检查：标签是否在给定列表。公开题面未规定annotation方法、marker版本或“severely depleted”数值阈值。

## `perturb-seq-align-q1` → `ls04-perturbseq-reference-map`

- 原生问题：reference和query Perturb-seq使用相同guides、不同cell type，query缺target metadata；找出依次对应PABPC1、NUDT21、LEO1的guides。
- 原生答案形式：按目标出现顺序的三个guide，以逗号分隔，如 `guide1,guide2,guide3`。
- `internet_required=False`；输入：reference/query两个h5ad。
- 可公开检查：正好三个有序guide ID。公开资料无top-k/相关性容差或gold。

## `spatial-sim-q1` → `ls04-spatial-deconvolution`

- 原生问题：利用打包的single-cell counts/metadata与Visium counts/features/barcodes/images/positions，判断`Spot_710-1`包含哪些cell type。
- 原生答案形式：cell types按alphabetical order以逗号分隔，如 `Endothelial,Macrophage`。
- `internet_required=True`；输入：`spatial.sim.tar.gz`。
- 可公开检查：排序与字符串结构。公开题面里tissue image文件描述有拼写/重复，且没有deconvolution方法、比例阈值或gold。

## `protein-shape-q1` → `ls05-protein-shape`

- 原生问题：考虑PDB的所有可能projection，判断最像哪个大写字母。
- 原生答案形式：`B,D,F,H,J,L,N,P,R,T,V,X,Z`中的一个字母。
- `internet_required=False`；输入：`protein.shape.q1.pdb`。
- 可公开检查：闭集标签与PDB可解析性。公开题面没有projection选择或形状相似度metric，因此不能声称一个本地视觉oracle是官方verifier。

## `multiome-match-atac-rna-q1` → `ls08-multiome-column-match`

- 原生问题：RNA TPM和ATAC 10 kb-bin counts各有相同8个pseudo-bulk populations；ATAC列被置换。对每个RNA列i输出匹配ATAC列的0-based index。
- 原生答案形式：长度8、无空格、分号分隔的字符串，如 `7;6;5;4;3;2;1;0`。
- `internet_required=True`；输入：RNA/ATAC gzipped TSV。
- 可公开检查：8个0–7整数且构成permutation。正确permutation和官方容错不公开。

## `ep-interactions-q1` → `ls08-enhancer-promoter-integration`

- 原生问题：整合Hi-C-like 3D proximity与CRISPR disruption后的promoter expression，选择最不符合真实causal enhancer–promoter interaction的一对。
- 原生答案形式：单个字母A–G，对应EP1–EP7。
- `internet_required=False`；输入：Hi-C CSV与expression CSV。
- 可公开检查：A–G闭集及两个表的确定性统计。
- 原生冲突：题面开头称有八个候选EP1–EP8，但选项只有EP1–EP7；使用前必须确认EP8为何被排除。公开资料没有integration权重、阈值或gold。

## 评分使用原则

对上述题，能够诚实称为“CompBioBench原生评分”的只有：提交原生单一答案到官方私有leaderboard并获得返回结果。若项目需要离线grader，应由两名reviewer基于冻结输入/reference独立复算，并在结果中标为 `local_independent_oracle`；不要标为 `CompBioBench verifier`。任何Coverage/脚本/report/partial-credit项目也必须标为评测工作流的扩展层。
