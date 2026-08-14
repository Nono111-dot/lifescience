# BixBench 原生评分标准：已选 LS06、LS07、LS10

## 证据与解释边界

本文件以本地下载的官方 `BixBench.jsonl` 为逐行证据：`.tmp_tests/BixBench.jsonl`，BixBench `version=1.5`，SHA-256 `0D1204DCDAE7193A9132CED5A3502008F6B3B163DEBC1B65B2AA2D86CB132DC9`。上游文件地址为 <https://huggingface.co/datasets/futurehouse/BixBench/blob/main/BixBench.jsonl>。

JSONL公开字段包括 `question`、`ideal`、`distractors`、`eval_mode`、capsule和来源信息，但不包含 verifier 实现、数值容差实现细节、参考分析脚本或80分artifact rubric。因此：

- `str_verifier`：下文只能确认上游声明为字符串型核验及其ideal；不能据此声称知道其未公开的规范化/匹配代码。
- `range_verifier`：ideal本身给出接受区间；区间端点是否闭合的实现未公开，本地grader应明确采用自己的端点政策。
- `llm_verifier`：上游以语义判定为目标；具体judge prompt、模型、温度和版本未随JSONL提供。
- Coverage、完整表格、方向、summary和脚本是本项目的artifact扩展，不能称为BixBench原生分项。

## LS06-1 `ls06-eno1-effect-size`

### `bix-37-q1`

- 原题目标：从蛋白组数据回答肿瘤与正常样本间ENO1蛋白丰度fold change。
- 原题：`Based on the proteomics data, what is the fold change in ENO1 protein abundance between tumor and normal samples?`
- `eval_mode`: `llm_verifier`
- `ideal`: `4.81-fold increase in tumor`
- 原生判定方式：语义上同时要求fold change约为4.81，并表达肿瘤方向为升高。具体LLM judge配置未公开。
- 输入可复算：冻结工作簿 `Proteomic_data .xlsx`、sheet `Tumor vs Normal`唯一ENO1行的Normal=`72896133.2946858`、Tumor=`350385456.451912`、Ratio/FC=`4.81`。

### `bix-37-q4`

- 原题目标：回答Tumor相对Normal的ENO1 log2 fold change，四舍五入到两位小数。
- `eval_mode`: `str_verifier`
- `ideal`: `2.27`
- 原生判定方式：上游声明字符串型核验；JSONL未公开数值解析或字符串规范化规则。
- 输入可复算：同一ENO1行 `log2FC=2.27`；且 `log2(4.81)`与其在两位小数精度一致。

### 与本项目artifact rubric的边界

BixBench原生只对最终FC/方向和log2FC设定目标。Normal/Tumor原始值、唯一gene、source_file/source_sheet、JSON schema、report和analysis.py不是原生标准。建议本项目把40分core拆为Normal 10、Tumor 10、FC 10、log2FC 10；direction 15检查FC>1、log2FC>0及“tumor increase”；summary 5只检查报告与机器结果一致。原生ideal仍是最终科学正确性的首要锚点。

## LS06-2 `ls06-eno1-significance-audit`

### `bix-37-q3`

- 原题目标：回答ENO1肿瘤与正常差异蛋白丰度的adjusted p-value。
- 原题：`What is the adjusted p-value for ENO1's differential protein abundance/levels between tumor and normal samples?`
- `eval_mode`: `str_verifier`
- `ideal`: `0.226`
- 原生判定方式：字符串型核验；未公开格式规范化。distractor `0.031`对应raw p-value，可用于构造科学错误样例。
- 输入可复算：ENO1行 `p.value=0.031`、`adj.Pval=0.226`，能确定没有把raw p冒充adjusted p。

### 与本项目artifact rubric的边界

FDR阈值0.05、`significant=false`、来源字段、JSON/report/script均来自本项目任务卡，不是原生评分字段。建议core 40只锚定adjusted p；direction/decision 15检查任务卡给定阈值、布尔值与 `0.226>0.05`一致；summary 5检查报告明确“不显著”。

## LS07-1 `ls07-combination-treatment-deg`

### `bix-43-q3`

- 原题目标：用DESeq2比较CBD/cisplatin联合处理与DMSO对照，并按三重阈值计数DEG。
- 原题：`Using DESeq2 for differential expression analysis, how many genes show significant differential expression (adjusted p-value < 0.05, absolute log2 fold change > 0.5, baseMean > 10) in the CBD/cisplatin combination treatment compared to DMSO control?`
- `eval_mode`: `str_verifier`
- `ideal`: `677`
- 原生判定方式：字符串型最终计数核验；未公开是否接受带单位、千位分隔或等价数值格式。
- 输入可复算：capsule `15ff11e5-2db1-45b6-b3a3-46bc2a74b821`包含counts、布局/metadata及映射数据，可依原题指定DESeq2、contrast和严格阈值重新生成计数。复算必须固定DESeq2/R版本、design、reference level、独立过滤和缺失padj处理；JSONL本身未给这些软件细节。

### 与本项目artifact rubric的边界

原生只锚定最终计数677，不要求完整DE表。建议本项目core 40同时检查每基因baseMean/log2FC/pvalue/padj及最终677，但正式启用前须用固定DESeq2环境生成reference表；direction 15检查contrast方向和pass规则，不应仅凭最终计数给满分；summary 5检查计数/阈值一致。若未固定DESeq2环境，此题应保持blocked，而不是把677扩写成伪reference表。

## LS07-2 `ls07-combination-treatment-mechanism`

### `bix-43-q5`

- 原题目标：以全部DEG（`p<0.05`, `abs(lfc)>0.5`, `baseMean>10`）为输入，使用gseapy和`Reactome_2022`找出联合处理主要富集机制。
- 原题：`What is the primary cellular mechanism enriched in the CBD/cisplatin combination treatment when performing enrichment analysis using gseapy as method and Reactome_2022 as geneset library with all differentially expressed genes (p<0.05, absolute lfc>0.5, baseMean>10)?`
- `eval_mode`: `llm_verifier`
- `ideal`: `TP53-mediated cell cycle regulation`
- 原生判定方式：语义判定机制是否等价于TP53介导的细胞周期调控；具体LLM judge配置未公开。
- 输入可复算：从相同capsule可重新做DE和富集，但必须获得并冻结上游明确指定的`Reactome_2022`基因集以及gseapy版本。注意该原题使用raw `p<0.05`，与q3的`adjusted p<0.05`不同，不得擅自合并阈值。

### 与本项目artifact rubric的边界

原生ideal是机制短答案，不提供完整pathway ranking、p值、padj、universe或tie-break。建议本项目在真正提供冻结的`Reactome_2022`后，core 40检查富集表与top TP53/cell-cycle证据，direction 15检查机制call与表一致且不把富集写成已证明因果，summary 5检查克制表达。在gene set未冻结前，本题仍是blocked；不能用自行选取的新Reactome release替代原题标准。

## LS10-1 `ls10-neun-power-analysis`

### `bix-19-q1`

- 原题目标：由NeuN数据计算pooled-SD Cohen's d，并进行双样本t检验power analysis；alpha=0.05、power=0.80；返回每组样本量。
- `eval_mode`: `str_verifier`
- `ideal`: `337`
- 原生判定方式：字符串型样本量核验；solver和版本未公开。

### `bix-19-q2`

- 原题目标：回答KD与CTRL NeuN计数的Cohen's d。
- `eval_mode`: `range_verifier`
- `ideal`: `(0.215,0.217)`
- 原生判定方式：数值落入上游给定区间；端点策略未公开。

### 相关交叉证据 `bix-19-q5`

- 目标同为80% power下所需每组最小样本量。
- `eval_mode`: `llm_verifier`
- `ideal`: `337 samples`
- 用途：为q1的337提供同一capsule内的语义交叉证据；本项目选题来源当前标注q1/q2，q5不另算一道题。

### 输入可复算及边界

冻结CSV可独立算得KD mean `214.5`、CTRL mean `210.625`、sample SD `10.9414023651`与`22.8531804601`、pooled SD `17.9162236933`、KD-minus-CTRL d `0.2162844172`。这些中只有d区间及n=337是原生评分目标；means/SD/pooled SD、JSON schema、signed convention、report/script是扩展。建议core 40为means 8、SD 8、pooled SD 6、d 8、n 10；decision 15检查alpha/power/two-sided和向上取整。正式启用前必须固定一个power solver并复现337，不能虚构上游所用包。

## LS10-2 `ls10-treatment-response-model`

### `bix-51-q3`

- 原题目标：BMI、age、gender联合logistic模型中age预测PR反应的p-value。
- `eval_mode`: `range_verifier`
- `ideal`: `(0.0024,0.0026)`
- 原生判定方式：p-value落入区间；未公开端点政策。

### `bix-51-q4`

- 原题目标：同一联合logistic模型中年龄每增加一年的remission log-odds变化。
- `eval_mode`: `range_verifier`
- `ideal`: `(-0.085,-0.075)`
- 原生判定方式：age coefficient落入区间；未公开端点政策。

### 输入可复算及边界

冻结工作簿以80条非空outcome记录、PR=1、BMI+age+gender、female reference的标准未惩罚binomial-logit MLE复算得到：age estimate `-0.0795084690`、SE `0.0262977303`、Wald p `0.0024995441`、OR `0.9235701982`。原生只锚定coefficient和p的范围；SE、OR、complete-case计数、编码/reference metadata、完整系数表、report/script都是扩展。建议core 40拆为estimate/SE/p/OR各10，direction 15检查负系数、OR<1且p<0.05，summary 5检查报告一致。正式启用前应在固定R `glm`或statsmodels版本中二次复算；不得声称female reference或具体SE/OR是BixBench公开原生条件。

## 六题使用规则汇总

| 本地任务 | 原生主锚点 | 当前可离线复算 | 不得冒充原生的扩展 |
|---|---|---|---|
| LS06 effect | 4.81 increase；2.27 | 是 | raw values、schema、report、script |
| LS06 significance | adjusted p=0.226 | 是 | FDR decision、source、report、script |
| LS07 DEG | count=677 | 条件性 | 完整DE表及逐行gold |
| LS07 mechanism | TP53-mediated cell-cycle regulation | 缺冻结Reactome_2022 | pathway表、统计量、tie-break |
| LS10 power | d区间；n=337 | d是；n待固定solver | 中间统计、solver假设、artifact |
| LS10 logistic | age p和系数区间 | 是，待第二软件确认 | SE、OR、coding metadata、artifact |

原生ideal用于科学答案锚定；本项目80分细则用于评估可复现artifact质量。两者应在结果表中分列，不应把扩展得分解释为BixBench官方分数。
