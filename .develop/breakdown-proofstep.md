# BC proof-step 组成（要求5c breakdown 数据源）

> 数据来自匿名工件 `case_studies/bc/results.zip` 的 11 个已验证 proof（8 QA + 3 SA），对每个 proof 统计 `solve(...)` 目标类型。**纯分析已有 proof，未重跑。** 可复现：
> `grep -oE "solve\( *!?[A-Za-z0-9_]+" <proof.spthy> | sed 's/solve( *//' | sort | uniq -c`

| 配置 | !KU | !MDerive0 | !MDerive1 | 总 solve | MDerive 占比 |
|---|---:|---:|---:|---:|---:|
| QA_CSCLE_CSKS_PSCLE_PEKS | 329354 | 67872 | 4380 | 401621 | **18.0%** |
| QA_CLEO_CLKS_PLEO_PEKS | 119292 | 85680 | 5526 | 210511 | **43.3%** |
| SA_CSCO_CSKS_PSCO_PLKS | 81541 | 47712 | 2904 | 132169 | **38.3%** |
| QA_CSCO_CSKS_PSCO_PEKS | 56201 | 5936 | 378 | 62528 | 10.1% |
| QA_CSCO_CSKS_PSCO_PLKS | 5945 | 3360 | 216 | 9533 | 37.5% |
| QA_CLEO_CSKS_PLEO_PLKS | 49 | 8 | 0 | 67 | 11.9% |
| QA_CSCLE_CSKS_PSCLE_PLKS | 49 | 8 | 0 | 67 | 11.9% |
| QA_CLEO_CEKS_PLEO_PLKS | 37 | 2 | 0 | 49 | 4.1% |
| SA_CLEO_CSKS_PLEO_PLKS | 37 | 2 | 0 | 49 | 4.1% |
| SA_CSCLE_CSKS_PSCLE_PLKS | 37 | 2 | 0 | 49 | 4.1% |
| QA_CLEO_CLKS_PLEO_PLKS | 29 | 0 | 0 | 39 | 0.0% |

## 解读（可写进论文，诚实、可核查）
- **耗时来源集中在无攻击、需遍历全部分支的配置**（总 solve 步数上万到 40 万）。这些配置里，破解相关目标 `MDerive0/1` 占证明步骤的 **10%–43%**，是搜索空间膨胀的直接、可量化来源。
- `!KU`（标准 Dolev–Yao 知识构造）占大头，但其中很大一部分是被 `MDerive` 派生分支级联触发的——攻击者需为每个 derivation 分支构造输入。
- 快配置（找到攻击即停、或平凡终止）证明步数只有几十步，占比不具耗时代表性。
- 结论口径：与要求5c 一致——proof-step 组成是「搜索工作量集中在何处」的**结构性代理**，不等同于 wall-clock 时间占比。

## 注意
- 各配置 MDerive 占比从 18% 到 43% 不等，因此论文**不要写死单一百分比**；给整张表或"耗时无攻击配置中 MDerive 占 18%–43%"更准确。
- 文件名编码（CLEO/CSCLE/CSCO × CSKS/CLKS/CEKS × P…）与 `results.tex` 表格行的对应，需按 `case-studies.tex` 的设备记法核对后再引用。
