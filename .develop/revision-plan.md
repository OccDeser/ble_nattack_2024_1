# NDSS 2027 #474 大修执行清单

> 依据 decision lead 的 8 条大修要求（`reviews/Revision-Tasks.md`）。本文件只列「改哪里、改成什么」，`file:line` 为定位锚点（执行时以实际行号为准）。
> **`reviews/Revision-Plan-EN.md` 是已交付审稿人的承诺书**：本文件必须覆盖它承诺的每一项，且措辞不得与之冲突。EN 稿更简略是正常的（内部计划是超集），但**EN 稿点名的位置和限定语一个都不能漏**。EN 稿如需改动，中英两半须同步。

## EN 承诺书 ↔ 本文件 对应关系

| EN 条目 | 本文件 | EN 稿点名、内部计划须落实的额外约束 |
|---|---|------|
| 1 scope/soundness | 要求1 | 点名 **abstract、Sec I、Sec III-A、Sec VI、Sec VIII** —— 其中 **Sec VI 原计划未列，已补**；scope 段落定在 **III-A** |
| 2 deterministic attacker | 要求2 | "throughout the paper"，以 III-A 为主锚点 |
| 3 equivalence related work | 要求3 | 一致 |
| 4 technical exposition | 要求4 | 一致（FVP 也归入「review A 指出的不准确表述」） |
| 5 evaluation | 要求5 | 承诺 **在 Sec VI 新增一个独立 performance evaluation 小节**；plain-Tamarin 对比须**同一 Tamarin 版本** |
| 6 human guidance | 要求6 | 承诺口径：最终 BC 模型**只用调整 goal/branch 优先级的启发式 tactic** |
| 7 artifact | 要求7 | 承诺 **Dockerfile 固定环境 + 两套版本 + 更详细的说明与命令**；EN 稿未提 FVP，但 FVP 不能因此漏掉 |
| 8 disclosure | 要求8 | 承诺**带日期的准确记录** + 重投前再问 SIG |

## 章节号 ↔ 文件 对照（EN 稿用章节号，本文件用文件名）

| 章节 | 文件 |
|---|---|
| Abstract | `main.tex:111-119` |
| I Introduction | `introduction.tex` |
| II Background | `background.tex` |
| III General Brute-Force Attack Modeling | `brute-force-modeling.tex`；**III-A = Threat Model and Low-Entropy Adversary（`:6-18`）** |
| IV Low-Entropy Analysis Methodology | `methodology.tex` |
| V Case Studies | `case-studies.tex` |
| VI Results | `results.tex`；VI-E Reproducibility `:153`、VI-F Summary `:175` |
| VII Related Work | `related-work.tex` |
| VIII Discussion and Conclusion | `discussion-conclusion.tex` |
| Ethics（无编号） | `ethics.tex` |

## 执行前提

1. **无攻击协议用 Alipay**（rebuttal 中提到的三个），不是 EMV。
2. **breakdown 方案**：用匿名工件 `results.zip` 的 11 个已验证 proof，统计 `solve()` 目标分布作为 proof-step 级 breakdown（详见要求5c）。
3. **运行时间以论文表格数据为准**（`results.tex` 表 + 最慢 ≈27 小时）。
4. **soundness 边界描述清楚即可**，不写成形式化定理——审稿人针对的是 overclaim（要求1 允许「be clear where uncertain」）。
5. **Artifact 两个容器**：`Tamarin 1.8.0 + Maude 3.1 + Python 3.12` 跑 WPA2-PSK / BLE / BC（论文全部报告数字的来源）；`Tamarin 1.10.0 + Maude 3.1 + Python 3.10` 跑三个 Alipay（其字面量含连字符，只有 Tamarin 1.10+ 能解析）。匿名工件：`anonymous.4open.science/r/EntropyVerif-BF04`。

---

## 要求1｜删除 "capture all brute-force"，精确刻画 scope

**原则：只做两件事——(a) 删/收窄 overclaim 措辞；(b) 加一段简短、平实的 scope 说明。不自行引入形式化定理、offline-guessing test 等额外理论论述。**

**(a) 过强声称——逐句收窄：**
- `introduction.tex:40` — "capable of capturing **all** brute-force behaviors…"（审稿人直接引用，**必改**）→ 改为「在确定性攻击者、正向验证型破解下捕获攻击」。
- `brute-force-modeling.tex:42` — "To **generally capture all** brute force attacks"（**必改**）。
- `brute-force-modeling.tex:4` — "in a **general manner**"。
- `introduction.tex:24` "cover **general** brute-force"、`:27` "**generally** capturing"、`:35` "a **general** and automated method"、`:41` "**verify the security** of protocols"（→「在给定攻击者模型与预算下未发现攻击」）。
- `methodology.tex:23` — "**generally** compromise… **comprehensive** security analysis"。
- `main.tex:114`（abstract）— abstract 整体加一句 scope 限定；另注意 `:116` "anchors verification results to a concrete computational budget" 亦属需收窄的声称（预算是标称比特长度标签，非成本模型）。
- **`results.tex:175-182`（VI-F Summary）— EN 稿点名 Section VI，原计划漏列，必改**："successfully introducing low-entropy keys to protocol analysis in symbolic models" 与 "the novel UMD attack **overlooked by former model**" 均为无限定的成效声称 → 收窄为「在所定义的确定性攻击者与预算下」，并明确未发现攻击 ≠ 安全。
- `related-work.tex:48` "remain… unstudied…"、`:62` "first to check all four boxes"（补等价性工作后调整，见要求3）。

**soundness 声称——改平实说法，不用 soundness 层级术语：**
- `introduction.tex:56` 和 `discussion-conclusion.tex:30`（两处重复）— "verification soundness is inherited… from the unmodified Tamarin backend" → 改平实说法：EntropyVerif 只产生标准 Tamarin 规则、不改后端；验证结论相对于所定义的攻击者模型陈述，报告的攻击在预算内可执行、带 concrete trace。**不用 solver/modeling soundness 术语**（自造，审稿人与 rebuttal 均未用）。

**(b) 新增一段简短 scope（平实语言，不写定理/不展开理论）：** **位置定在 `brute-force-modeling.tex` §III-A（`:6-18`，threat model 段末）**——EN 稿点名 Section III-A，不再在 threat model / threats-to-validity 之间二选一；`discussion-conclusion.tex` 的 threats-to-validity 只做一句回指，不重复展开。只说三点：
- **能捕获**：确定性攻击者的正向验证型破解——攻击者掌握函数输出，且除低熵密钥外的输入均为常量或 Dolev–Yao 可推导，通过重算输出验证候选密钥。
- **不能捕获**：需逆向运算 / 部分输入未知的破解（审稿人 A1 例子：两密文比常量、用 dec 逆向验证、nonce 未知），显式标注为当前限制。
- **可能过近似**：预算只是标称比特长度标签、不是成本模型，宽松预算下报出的攻击可能在符号模型中可执行但对真实部署不现实。**两个方向都要写**（Reviewer D 原话要求 "when this oracle abstraction is sound and when it may produce false positives"）。

---

## 要求2｜明确「只考虑确定性攻击者，概率性/部分信息 out-of-scope」

- `brute-force-modeling.tex:8-11`（威胁模型）：已有条件 (i)(ii)，但未点明「deterministic」也未声明概率性 out-of-scope → 补一句明确定性定性 + out-of-scope 声明。
- `main.tex:114`（abstract）与 threats-to-validity 各加一句。
- 「确定性」只限定新增破解能力，不限制攻击者原有的非确定性协议选择——须写明，避免误读。
- 可与 `discussion-conclusion.tex:6`（已承认非均匀分布 over-approx）整合。

---

## 要求3｜补等价性 related work 并精确定位（**整段缺失**）

- `related-work.tex`：在 `:45-48`（Enhanced attacker models）之后**新增一段** "Equivalence-based offline-guessing analysis"，讨论 **ProVerif diff-equivalence** 与 **Tamarin (conditional) observational equivalence**。
- 定位口径：等价性方法能揭示某密钥*存在* brute-force risk（如 SK 下密文可区分、可猜），但**不建模猜测是否在预算内**——于是 128 位 SK 被当作可控风险、协议照常部署，而 UMD 实际存在。EntropyVerif 把该 risk 变成**预算约束下、带 trace 的具体攻击**，破解值继续参与后续协议、可跨会话组合。
- **不要写**：不声称 Tamarin 内部附加了数值成本；不声称等价性方法原理上无法表达 BC 场景或传播猜测值。差异在于验证性质、外部预算标注工作流、trace-based 工具内的自动化。
- 对比表 `:6-36` 加一行（guarantees / cost treatment / output / candidate-validation coverage / manual modeling）；summary `:62` 重新定位；两者呈现为互补。
- 需加 bib：ProVerif diff-equivalence、Tamarin observational-equivalence 相关文献。

---

## 要求4｜改进技术表述——Reviewer A 明确指出的不精准点（逐条）

**总体：** 记号更清晰、补「设计总体描述」、加示例。范围：`methodology.tex` + `brute-force-modeling.tex` 的 oracle 建模整段。

**① "deconstructed" 含义不清**
- 位置：`methodology.tex:85` "$\delta(t)$ = Sub-terms that can be **deconstructed** from $t$"；`:99` "the sequence of all sub-terms that can be deconstructed from $t$"。
- 问题：只有自然语言表述，读者无法判断是语法子项、模等式理论的子项、还是攻击者可推导。
- 改：明确 = **syntactic decomposition**，$\delta(t)$ 是 $t$ 的 **syntactic-subterm closure**，给出递归定义。**以 rebuttal A3 为准：不是模等式理论的推导，也不是攻击者知识。**

**② "construct" 含义不清**
- 位置：`methodology.tex:86` "$\rho(t)$ = Atomic terms required to **construct** $t$"；`:100`。
- 改：递归定义 $\rho(t)$ 为构造 $t$ 所用的原子叶项；明确 = 用 constructor 从原子子项组合出项。

**③ 函数命名不具描述性**
- 位置：`methodology.tex:85-89, 99-109` 的 $\delta(t)$、$\rho(t)$、$\varepsilon(T)$、$\tau(F)$、$c(T)$ 等单字母希腊符号。
- 改：换更可读的名字，或至少在首次出现处逐个解释（已有符号表可强化）。

**④ 用序列而非集合**
- 位置：`methodology.tex:101-109`——$\llbracket\cdot\rrbracket$ 序列、$\circ$ 连接、$\setminus$ 差、$\delta/\varepsilon/\tau/c$ 全部按序列定义。
- 改：形式定义改用集合；仅在必须生成函数参数元组时施加固定顺序。

**⑤ relationship-breaking oracle 的 $f'$ 定义不够**
- 位置：`brute-force-modeling.tex:95` "the oracle will return a new function $f'$ where $f'(X \backslash \{x_i\}, k) = f(X, k)$"。
- 问题：只表达「$f'$ 少一个参数且取值相等」，没说清 $f'$ 是把 $x_i$ 固定为具体值 $a_i$ 后的**偏应用**；不同 $a_i$ 对应不同 $f'$。
- 改：直接采用审稿人给的定义 $f'_{a_i}(x_1,\ldots,x_{i-1},x_{i+1},\ldots,x_n,k)=f(x_1,\ldots,a_i,\ldots,x_n,k)$，并说明该记号不赋予攻击者新的密码学原语；同时说明重复参数、出现位置、元组顺序、原始语法与模等式相等在编译中的处理。

**⑥ 补总体说明与示例**
- 补编译/oracle 设计的总体说明，并给出三个 worked example：一个可捕获的正向验证案例、审稿人双密文反例、跨会话 UMD 组合案例。

**⑦ compromise 假设（威胁模型，非技术表述，但同属 review A）**
- BLE 分析沿用既有 BLE 模型的攻击者模型，其中不含诚实参与方 compromise；BC 采用同一选择。按 rebuttal A4 口径写成**建模限制**，不暗示能够抵抗参与方 compromise。**不改 lemma**——审稿人问的是 "why not"，给出理由即可。

---

## 要求5｜改进评估（reviews B/C/D）

**载体（EN 稿承诺，必须照做）：在 `results.tex` 新增一个独立小节 `\subsection{Performance Evaluation}`**，位置置于 VI-D UMD 之后、VI-E Reproducibility 之前，5a/5b/5c 三块结果全部收进该小节；Reproducibility 小节只留工具链/复现说明（要求7），不再混放性能数字。

### 5a. 无攻击协议：Alipay（三个）——已完成分析，rebuttal 有数据，只需写进正文

- 来源：三个 Alipay 支付协议（来自一篇已被 USENIX Security 2026 接收的工作），含低熵支付 PIN 但不可暴力破解。
- 已有数据：`alipay_app` 133.65→142.58s；`alipay_mobile_web` 133.30→142.25s；`alipay_order_code` 597.38→2509.61s（tactic 调整后 214.68→556.30s）。三个均终止，前两个仅加约 10s。
- **版本标注必须写**：这三个模型跑在 Tamarin 1.10.0（连字符字面量只有 1.10+ 能解析），耗时只在彼此之间比较，不与 1.8.0 的数字并列比较。
- 不把这些协议无条件称作 "non-exploitable"，给完整原模型/EntropyVerif 时间表；`alipay_order_code` 的调整前后两组数都报，tactic 调整如实计入人工引导。
- 大修工作 = 把结果写进 `case-studies.tex`（建模说明）+ `results.tex`（结果表 + 讨论），**不是从头建模**。

### 5b. plain-Tamarin baseline 对比

- `results.tex` 新增：同一协议在**无低熵标签/oracle** 的 plain Tamarin 下的运行时间，以及**有/无 tactic** 的对照，量化 EntropyVerif 的开销与 tactic 收益。需重跑实验。
- **EN 稿承诺「under the same Tamarin version」**：每一对 EntropyVerif ↔ plain-Tamarin 数字必须来自**同一 Tamarin 版本、同一容器、同一机器**，成对采集、成对报告。WPA2-PSK/BLE/BC 的 baseline 在 1.8.0 容器重跑；Alipay 的 baseline 在 1.10.0 容器重跑。**跨版本数字绝不并列成一张对比表**。
- 说明该比较测量的是「增加破解能力的成本」，不是两个等价安全分析的比较（plain Tamarin 无法表达该能力）。
- 每个数字报告工具链版本、tactic 配置、wall-clock 时间、终止状态；**只在同版本产生的数字之间比较**。

### 5c. breakdown（方案已用真实数据验证）

- 数据源：匿名工件 `case_studies/bc/results.zip` → `results/` 下 11 个已验证 proof（8 QA + 3 SA，对应 `results.tex` 表 11 行），均为 Tamarin 1.8.0 输出。
- 方法：统计每个 proof 里 `solve( <goal> )` 目标 fact 的分布，分为「破解相关」（`!MDerive0` / `!MDerive1`）与「标准 DY / 协议」（`!KU` / State* / 协议 fact），给出**证明步骤（proof-step）级 breakdown**，与 `results.tex` 表的 wall-clock 时间并列。
- 样例（最慢无攻击配置 `BC_SESSION_QA_CSCLE_CSKS_PSCLE_PEKS.spthy`，约 365 万行 proof）：`!KU` = 329354，`!MDerive0` = 67872，`!MDerive1` = 4380，协议 fact ≈ 15；总 solve ≈ 401621，MDerive 占比 ≈ 18%。
- **不要写死单一百分比**：11 个配置的 MDerive 占比在 0%–43% 之间，耗时的无攻击配置在 10%–43%。给整张表，或写「耗时无攻击配置中 MDerive 占 18%–43%」。详见 `breakdown-proofstep.md`。
- 论文表述：明确这是 proof-step breakdown，**不是 wall-clock 逐秒归因**（Tamarin 约束求解相互依赖，无法分摊到逐秒），标注为「搜索工作量集中位置的结构性代理」；解读为「relationship-breaking oracle 引入的 MDerive 分支是搜索空间膨胀的直接来源」。
- 执行时：对 11 个 proof 全跑同一统计生成 breakdown 表；文件名编码（CLEO/CSCLE/CSCO × CSKS/CLKS/CEKS × P…）与表格行的对应需按 `case-studies.tex` 的设备记法核对。

---

## 要求6｜详述人工引导（review B）— **含事实错误必改**

**EN 稿已向审稿人承诺的口径（改写时必须落到这句话上）：最终的 BC 模型「only heuristic tactics that adjust goal and branch priorities」——只用调整目标与分支优先级的启发式 tactic，无 `[sources]`、无辅助引理、无 oracle 外部脚本。** 正文措辞不得比这句更强或更弱。

- `results.tex:168` — 两处错：(a) "auxiliary **source lemmas**" 与实际不符（BC 实际只有 in-file tactic `tacticSecrecySK`，无 `[sources]`）；(b) "prioritizes goals containing **MDerive over K**" **与实现相反**（实际 prio `KU`、deprio `MDerive`）。两处都改。
- `discussion-conclusion.tex:13` — "a small number of auxiliary lemmas" 同步改为 tactic。
- `results.tex:167-170` 整段 Human guidance 重写：准确描述 tactic（BC `tacticSecrecySK`、BLE `tacticSecrecy`/`tacticMITM`）+ 给/不给引导的影响（结合 5b baseline）+ 每个案例说明默认搜索是否终止、tactic 是必需还是仅提速、哪些通用哪些按模型调整。
- **补协议级知识**（Reviewer B concrete step 2 原话 "the protocol-level knowledge that was required to create it"）：写明设计 BC tactic 需要知道什么——哪些 BC 值是低熵的、哪些目标与破解相关、哪些派生分支可以提前关闭。
- 记录全部建模选择：低熵值的识别与标记、决定标记所用的外部可行性阈值、协议/compromise 假设、编译器 `derive-level`/`propagate-level` 边界。
- 说明 tactic 只影响搜索顺序/终止表现，不改变已完成 proof 的语义。
- 区分说明：WPA2 模型继承的上游 KRACK `nonce_reuse_key_type [sources]` 属基础模型既有，非本文低熵机制新增。
- 统一命名，使论文、tactic 文件与提交 artifact 一致（BC 搜索 tactic 与低熵/`MDerive` 目标名）。

---

## 要求7｜artifact 可复现（review A）

**EN 稿承诺三件可交付物：(i) Dockerfile 固定环境；(ii) 明确的版本归属（1.8.0 → WPA2-PSK/BLE/BC，1.10.0 → Alipay）；(iii) 更详细的说明与命令。三件都要真的进匿名仓库，不能只在正文写一句。**

- `results.tex:157-159` / `:172-173`：加**固定版本工具链** + **两个 Docker 容器** + **batch/interactive 脚本（列全 flags）**（当前仅 "unmodified Tamarin backend"，无版本）。
- **两个容器**：`Tamarin 1.8.0 + Maude 3.1 + Python 3.12`（WPA2-PSK / BLE / BC，论文报告数字的来源）；`Tamarin 1.10.0 + Maude 3.1 + Python 3.10`（三个 Alipay）。Dockerfile 放匿名仓库。**不声称原模型在 1.10 下重跑过或结果一致**（只重跑了小部分，且无审稿人要求跨版本重跑）。
- 一份 manifest 把每个表格行映射到**所属容器**、模型、命令、预期结果、资源需求。
- `result/...tmp` 失败原因：**Python 版本不兼容（3.14+ 出现，3.13 及以前正常）**（rebuttal A5）。每个容器固定受支持的 Python，加回归测试，从干净环境验证两个容器的说明步骤。
- 内存：审稿人的 >210 GB 来自 Tamarin 1.12.0。1.8.0 可在 192 GB 内完成 BC 批处理，**1.10.0 同样可以（17 h 05 min，即 rebuttal 中报告的测量，须在正文/artifact 说明中接上，避免与 rebuttal 口径断裂）**。给出准确命令、peak-RSS 日志、hash。
- 每个容器分开低资源 smoke test 与全量评估，昂贵目标顺序执行，每个模型/lemma 可单独调用，附机器可读日志与 checksum。
- **FVP**：等式理论用 **fvpgen（Cheval and Fontaine, CSF 2025）** 验证满足 finite-variant property（非 subterm-convergent 只是充分非必要条件）。**正文必须写一句**（放 methodology 等式理论处）——Reviewer A 原话是 "You do not mention any this in the paper"；**加 bib 引用**；命令、输入、输出、日志放进 artifact。
  **注意：EN 承诺书第 7 条没有点名 FVP**，它落在第 4 条「correct all unclear or inaccurate descriptions identified in review A」之下。这不构成冲突，但意味着**没有任何 EN 条目会提醒你做这件事**——不要因为逐条对照 EN 稿而漏掉；执行时它同时挂在要求4 与要求7 下。
- 硬件：`results.tex:3` / `:158` 的 AMD Ryzen 9 7950X3D / 192 GB，正文已正确、无需改。
- 时间数据以论文表为准；数量级一致即可、小误差正常（作者确认）。

---

## 要求8｜更新披露状态（review B）— **四处**保持一致

**⚠ 执行前必须先查证原始邮件——本轮排查发现两处硬冲突，不解决就动笔一定会自相矛盾：**

**冲突① 摘要说披露给「厂商」，其余全文说披露给 SIG。**
- `main.tex:116`（abstract 末句）— "a factor of $2^{116}$ reduction that has been responsibly disclosed to **the vendor**"。
- 与 `introduction.tex:49/:58`（"disclosed to the **Bluetooth SIG**"）、`ethics.tex`、以及要求8 本身「我们未直接联系单个厂商」**直接矛盾**。审稿人 B 原话就质疑 "it appears that no affected vendors were contacted"，摘要里这句会被当成失实陈述。
- 改：abstract 改为 "disclosed to the Bluetooth SIG"。**原计划漏列此处，是本条最高优先级的单点修改。**

**冲突② `ethics.tex` 引的 SIG 原话，比 rebuttal 的口径更有利。**
- `ethics.tex:6` 现引 2025-02-07 回复：SIG 称该场景 "appears **much more practical**" than previously known attacks —— 偏正面。
- `reviews/Rebuttal-NDSS-2027.md:42` 的口径：SIG 承认「潜在威胁，但成功利用需要特定条件」—— 偏保留。
- 二者可能来自**不同邮件**（2025-02-07 回复 vs 后续 follow-up），也可能是同一封被两边各取一半。**动笔前先翻原始邮件确认**：若确为两封，写成带日期的时间线、两句都写，不许只留有利的那句；若为同一封，以邮件全文为准，rebuttal 与论文同时改齐。
- **绝不能出现「论文引正面半句、rebuttal 说保留半句」的状态**——这是 reviewer B 最可能复查的一处。

**其余（原计划保留）：**
- `results.tex:148-151` 与 `ethics.tex:4-7`：均为旧口径 → 更新为带日期的事实记录：报告了什么、SIG 确认了什么、SIG 的原话表述、截至大修时仍无后续技术结论。
- 删除 `results.tex:149` 含糊的 "positive response"（reviewer B 直接加引号点名了这个词）；`:150-151` 的 "will provide further feedback" / "keep communicating" 若无新邮件支撑，改为「截至 YYYY-MM-DD 无后续」。
- **`ethics.tex:19` "Until specification updates and firmware patches are deployed" 必改**——暗示规范更新与固件补丁已在推进，属未经确认的修复暗示，与本条「不暗示任何未经确认的分析、修复或通知」冲突。改为不预设修复的表述（如「在缺乏公开缓解措施的情况下，用户可以…」）。
- 说明 UMD 是蓝牙协议设计层面的缺陷、非厂商实现 bug，故通过 SIG 协调披露；SIG 是否进一步通知厂商由其自行安排；我们未直接联系单个厂商。
- 说明 UMD 来自符号模型的推导与验证，尚未在实体设备上验证（`ethics.tex:11-13` 已有，保留并与正文呼应）。
- 重投前发邮件向 SIG 询问当前状态，按其回复（或未回复）更新——**这封邮件要尽早发**，回复可能要数周，是整个大修里唯一不受我们控制的关键路径。
- **四处**口径完全一致：`main.tex:116`（abstract）、`introduction.tex:49/:58`、`results.tex:148-151`、`ethics.tex:4-7`；`discussion-conclusion.tex:22` 一并核对。

---

## 跨要求一致性核对（执行完统一过一遍）

- **版本**：全文与 artifact 说明中，1.8.0 / 1.10.0 的归属与上表一致；不出现「所有结果同一工具链」之类表述；性能对比表内无跨版本并列。
- **source lemma**：`results.tex:168`、`discussion-conclusion.tex:13` 统一为「in-file goal-ordering tactic，无 `[sources]`」，且不强于 EN 稿的 "only heuristic tactics that adjust goal and branch priorities"；WPA2 上游 `[sources]` 单独说明。
- **无攻击协议**：Alipay（非 EMV），rebuttal 与论文一致。
- **披露（四处 + rebuttal）**：`main.tex:116` 已由 "the vendor" 改为 "the Bluetooth SIG"；`introduction.tex:49/:58`、`results.tex:148-151`、`ethics.tex:4-7` 口径一致，不提厂商、不暗示补丁。`ethics.tex` 所引 SIG 原话与 `Rebuttal-NDSS-2027.md:42` 的口径已对齐（见要求8 冲突②）。
- **FVP**：bib（Cheval & Fontaine, CSF 2025）+ 正文一句 + artifact 脚本，三处齐备（EN 稿未点名，易漏）。
- **scope 段落唯一**：scope 说明只在 §III-A 展开一次，`discussion-conclusion.tex` 只回指，不出现两份措辞不同的 scope 描述。
- **EN 承诺书逐条回扫**：拿 `reviews/Revision-Plan-EN.md` 的 8 条对照定稿，确认每条承诺在正文都有对应落点，且没有承诺了却没做的（尤其第 5 条的独立小节、第 7 条的 Dockerfile）。
- **中英一致**：`reviews/Revision-Plan-EN.md` 的英文与中文对照两部分同步。
