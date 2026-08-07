# NDSS 2027 #474 大修 TODO

> 执行细则见 `revision-plan.md`（改哪里、改成什么）；对审稿人的承诺见 `reviews/Revision-Plan-EN.md`。
> 本文件只管**顺序与状态**。行号为锚点，执行时以实际为准。
> 用法：从上往下做，一次一条。`[ ]` 未做 / `[~]` 进行中 / `[x]` 完成。

---

## P0 — 今天就要启动（长周期，卡在别人手里或卡在机器上）

- [X] **P0-1 给 Bluetooth SIG 发邮件问当前状态**
  整个大修唯一不受我们控制的关键路径，回复可能要数周。同一封邮件里顺便确认 2025-02-07 回复的完整原文（见 T8-2）。
  → 发出即算完成，回复到了再回来做 T8-*。

- [X] **P0-2 翻出 SIG 全部往来邮件，确定披露时间线**
  必须落到：哪天报的、哪天回的、每封回信的原话。
  ⚠ 现状有冲突：`ethics.tex:6` 引的是「appears much more practical」（偏正面），`reviews/Rebuttal-NDSS-2027.md:42` 写的是「潜在威胁但成功利用需要特定条件」（偏保留）。
  → 判定：是两封不同的信，还是同一封被各取一半？结论直接写进本文件，T8-2 依赖它。

- [ ] **P0-3 建两个 Docker 容器并跑通**
  `A: Tamarin 1.8.0 + Maude 3.1 + Python 3.12`（WPA2-PSK / BLE / BC，论文现有数字的来源）
  `B: Tamarin 1.10.0 + Maude 3.1 + Python 3.10`（三个 Alipay）
  → 两个容器都能从干净环境跑通 smoke test 才算完成。T7-* 和所有重跑实验都依赖它。

- [ ] **P0-4 补跑 plain-Tamarin baseline**（要求5b）—— **补从没有过的对照组，不是重跑**
  ⚠ **论文现有的 EntropyVerif 数字全部作数，一个都不重跑**（revision-plan「执行前提 3」）。缺的是对照组：同一协议**去掉低熵标签与 oracle** 后的 plain Tamarin 耗时——这组数从来没采集过，而要求5b 与 EN 承诺书第 5 条都明确承诺了。
  **要跑的**：WPA2-PSK / BLE / BC 的 plain-Tamarin 版本。
  **不用跑的**：三个 Alipay 的 baseline 已经有了——T5-1 里 `133.65→142.58s` 箭头**左边**那组（原模型 133.65 / 133.30 / 597.38s）就是。
  ⚠ 必须跑在**与论文现有数字相同的环境**（Tamarin 1.8.0、同一台 Ryzen 9 7950X3D / 192 GB），这样新 baseline 才能与既有 EntropyVerif 数字直接配对；配对成立，EntropyVerif 侧就不需要动。
  ⚠ 成本预期不高：去掉 oracle 就没有 MDerive 分支，搜索空间远小于 EntropyVerif 版，不是 27 小时那个量级（27 h 是 EntropyVerif 侧的数）。
  → 每条记录：版本、tactic 配置、wall-clock、终止状态、peak RSS。

- [ ] **P0-5 BC「无 tactic」对照**（要求6，供 T6-3 用）—— 这才是唯一可能真的很贵的一项
  3 个慢配置在**不给 tactic** 时是否终止。⚠ **设超时上限**（例如 48 h），到点就记「did not terminate within N h」——这本身就是要求6 想要的答案，不必跑到底。

---

## 第一批 — 定调子（先做，后面所有措辞都引用它）

- [ ] **T2-1 §III-A 写明「只考虑确定性攻击者」**（要求2）
  `brute-force-modeling.tex:8-11` 现有条件 (i)(ii) 但未点明 deterministic，也未声明概率性/部分信息 out-of-scope。
  ⚠ 要写清：「确定性」只限定**新增的破解能力**，不限制攻击者原有的非确定性协议选择。

- [ ] **T1-1 §III-A 加 scope 段落**（要求1b）
  紧接 T2-1 之后写，三点：**能捕获**（正向验证型破解）/ **不能捕获**（需逆向运算、部分输入未知——用 reviewer A1 的双密文例子）/ **可能过近似**（预算是标称比特长度标签、不是成本模型）。
  ⚠ 两个方向都要写（Reviewer D 明确要求 "when sound and when it may produce false positives"）；平实语言，**不写定理**。
  ⚠ scope 只在这里展开**一次**，`discussion-conclusion.tex` 只回指。

- [ ] **T1-2 abstract 加 scope 限定**（要求1a）
  `main.tex:114` 加一句；`:116` "anchors verification results to a concrete computational budget" 一并收窄。

---

## 第二批 — overclaim 逐句清扫（要求1a）

- [ ] **T1-3 `introduction.tex:40`**——"capable of capturing **all** brute-force behaviors"，审稿人直接引用，**必改**。
- [ ] **T1-4 `brute-force-modeling.tex:42`**——"To **generally capture all** brute force attacks"，**必改**；`:4` "in a **general manner**" 一并改。
- [ ] **T1-5 `introduction.tex` 其余四处**——`:24` "cover **general**"、`:27` "**generally** capturing"、`:35` "**general** and automated method"、`:41` "**verify the security**"（→「在给定攻击者模型与预算下未发现攻击」）。
- [ ] **T1-6 `methodology.tex:23`**——"**generally** compromise… **comprehensive** security analysis"。
- [ ] **T1-7 `results.tex:175-182`（VI-F Summary）**——EN 稿点名 Section VI，**原计划漏列**。"successfully introducing low-entropy keys…" 与 "overlooked by former model" 收窄为「在所定义的攻击者与预算下」；明确未发现攻击 ≠ 安全。
- [ ] **T1-8 soundness 两处**——`introduction.tex:56` 与 `discussion-conclusion.tex:30` 的 "verification soundness is inherited from the unmodified Tamarin backend"。
  ⚠ 改平实说法（只产生标准 Tamarin 规则、不改后端、结论相对于所定义攻击者模型陈述、报告的攻击带 concrete trace）；**不用 solver/modeling soundness 这类自造术语**。

---

## 第三批 — 技术表述（要求4，review A 逐条）

- [ ] **T4-1 定义 $\delta(t)$**——`methodology.tex:85, 99`。明确 = **syntactic-subterm closure**，给递归定义。⚠ 以 rebuttal A3 为准：**不是**模等式理论的推导，**不是**攻击者知识。
- [ ] **T4-2 定义 $\rho(t)$**——`methodology.tex:86, 100`。递归定义为构造 $t$ 所用的原子叶项。
- [ ] **T4-3 换掉单字母希腊符号**——`methodology.tex:85-89, 99-109` 的 $\delta/\rho/\varepsilon/\tau/c$，改可读命名，或至少首次出现处逐个解释。
- [ ] **T4-4 序列改集合**——`methodology.tex:101-109` 形式定义改用集合；仅在必须生成函数参数元组时施加固定顺序。
- [ ] **T4-5 补 $f'$ 的偏应用定义**——`brute-force-modeling.tex:95`。直接采用审稿人给的 $f'_{a_i}(\ldots)=f(x_1,\ldots,a_i,\ldots,x_n,k)$；说明该记号**不赋予攻击者新的密码学原语**；说明重复参数、出现位置、元组顺序、原始语法 vs 模等式相等在编译中的处理。
- [ ] **T4-6 补总体说明 + 三个 worked example**——一个可捕获的正向验证案例、审稿人双密文反例、跨会话 UMD 组合案例。
- [ ] **T4-7 compromise 假设写成建模限制**——BLE 沿用既有模型的攻击者模型（不含诚实参与方 compromise），BC 同一选择。按 rebuttal A4 口径，**不暗示能抵抗参与方 compromise**；⚠ **不改 lemma**，审稿人问的是 "why not"，给理由即可。
- [ ] **T4-8 FVP 写进正文**——methodology 等式理论处写一句：用 **fvpgen（Cheval & Fontaine, CSF 2025）** 验证满足 finite-variant property（subterm-convergent 只是充分非必要）。
  ⚠ **EN 承诺书 8 条里没有任何一条会提醒你做这件事**（它藏在第 4 条「review A 的不准确表述」之下），逐条对照 EN 稿时极易漏。bib 引用 + artifact 脚本见 T7-5。

---

## 第四批 — Related Work（要求3，整段缺失）

- [ ] **T3-1 新增 "Equivalence-based offline-guessing analysis" 段**——`related-work.tex:45-48` 之后，讨论 ProVerif diff-equivalence 与 Tamarin (conditional) observational equivalence。
  定位口径：等价性方法能揭示某密钥*存在* brute-force risk，但**不建模猜测是否在预算内**——于是 128 位 SK 被当作可控风险、协议照常部署，而 UMD 实际存在。EntropyVerif 把 risk 变成**预算约束下、带 trace 的具体攻击**，破解值继续参与后续协议、可跨会话组合。
  ⚠ **不要写**：不声称 Tamarin 内部附加了数值成本；不声称等价性方法原理上无法表达 BC 场景或传播猜测值。呈现为**互补**。
- [ ] **T3-2 对比表加一行**——`related-work.tex:6-36`，维度：guarantees / cost treatment / output / candidate-validation coverage / manual modeling。
- [ ] **T3-3 重新定位 summary**——`related-work.tex:62` "first to check all four boxes"；`:48` "remain… unstudied" 一并调整。
- [ ] **T3-4 补 bib**——ProVerif diff-equivalence、Tamarin observational-equivalence 文献。

---

## 第五批 — 人工引导（要求6，**含事实错误**）

- [ ] **T6-1 改 `results.tex:168` 两处事实错误**（**必改**）
  (a) "auxiliary **source lemmas**" 与实际不符——BC 实际只有 in-file tactic `tacticSecrecySK`，无 `[sources]`；
  (b) "prioritizes goals containing **MDerive over K**" **与实现相反**——实际 prio `KU`、deprio `MDerive`。
- [ ] **T6-2 `discussion-conclusion.tex:13`**——"a small number of auxiliary lemmas" 同步改为 tactic。
- [ ] **T6-3 重写 `results.tex:167-170` 整段 Human guidance**
  ⚠ 落到 EN 稿承诺的这句话上：最终 BC 模型「**only heuristic tactics that adjust goal and branch priorities**」——不得比它更强或更弱。
  内容：准确描述 tactic（BC `tacticSecrecySK`、BLE `tacticSecrecy`/`tacticMITM`）+ 给/不给引导的影响（接 T5-2 的 baseline）+ 每个案例说明默认搜索是否终止、tactic 是必需还是仅提速、哪些通用哪些按模型调整。
- [ ] **T6-4 补协议级知识**——Reviewer B 原话要的是 "the protocol-level knowledge that was required to create it"：设计 BC tactic 需要知道哪些 BC 值是低熵的、哪些目标与破解相关、哪些派生分支可以提前关闭。
- [ ] **T6-5 记录全部建模选择**——低熵值的识别与标记、决定标记所用的外部可行性阈值、协议/compromise 假设、编译器 `derive-level`/`propagate-level` 边界。
- [ ] **T6-6 说明 tactic 只影响搜索顺序/终止表现**，不改变已完成 proof 的语义。
- [ ] **T6-7 区分 WPA2 上游 `[sources]`**——KRACK 的 `nonce_reuse_key_type [sources]` 属基础模型既有，非本文低熵机制新增。
- [ ] **T6-8 统一命名**——论文、tactic 文件、提交 artifact 三者一致（BC 搜索 tactic 与低熵/`MDerive` 目标名）。

---

## 第六批 — 评估（要求5，依赖 P0-3/P0-4）

- [ ] **T5-0 在 `results.tex` 新建 `\subsection{Performance Evaluation}`**
  位置：VI-D UMD 之后、VI-E Reproducibility 之前。EN 稿明确承诺了这个独立小节。5a/5b/5c 全部收进来；Reproducibility 只留工具链/复现说明。
- [ ] **T5-1 写入 Alipay 三个模型**（要求5a，**已有数据，不需重新建模**）
  `alipay_app` 133.65→142.58s；`alipay_mobile_web` 133.30→142.25s；`alipay_order_code` 597.38→2509.61s（tactic 调整后 214.68→556.30s）。
  ⚠ **必须标注跑在 Tamarin 1.10.0**，只在彼此之间比较，不与 1.8.0 数字并列。
  ⚠ 不把这些协议无条件称作 "non-exploitable"；`alipay_order_code` 调整前后两组数都报，tactic 调整如实计入人工引导。
  建模说明写进 `case-studies.tex`，结果表 + 讨论写进 `results.tex`。
- [ ] **T5-2 写入 plain-Tamarin baseline 对比**（要求5b，等 P0-4 出数）
  EntropyVerif 侧直接用论文既有数字，baseline 用 P0-4 新采的，成对呈现。
  说明该比较测的是「增加破解能力的成本」，不是两个等价安全分析的比较（plain Tamarin 无法表达该能力）。
- [ ] **T5-3 生成 11 个 proof 的 proof-step breakdown 表**（要求5c）
  数据源：`case_studies/bc/results.zip` → `results/`（8 QA + 3 SA，均 Tamarin 1.8.0 输出）。方法与现成数据见 `breakdown-proofstep.md`。
  ⚠ **不要写死单一百分比**——11 个配置 MDerive 占比 0%–43%，耗时的无攻击配置在 10%–43%。给整张表，或写「耗时无攻击配置中 MDerive 占 18%–43%」。
- [ ] **T5-4 核对文件名编码与表格行的对应**——CLEO/CSCLE/CSCO × CSKS/CLKS/CEKS × P… 按 `case-studies.tex` 的设备记法核对后再引用。
- [ ] **T5-5 写清 breakdown 的性质**——是 **proof-step** breakdown，**不是 wall-clock 逐秒归因**（Tamarin 约束求解相互依赖，无法分摊）；标注为「搜索工作量集中位置的结构性代理」；解读为「relationship-breaking oracle 引入的 MDerive 分支是搜索空间膨胀的直接来源」。

---

## 第七批 — Artifact（要求7，依赖 P0-3）

- [ ] **T7-1 `results.tex:157-159` / `:172-173` 加固定版本工具链**——当前只有 "unmodified Tamarin backend"，无版本号。写明两个容器的归属。
  ⚠ **不声称原模型在 1.10 下重跑过或结果一致**（只重跑了小部分，审稿人也没要求跨版本重跑）。
- [ ] **T7-2 写 manifest**——每个表格行 → 所属容器、模型、命令、预期结果、资源需求。
- [ ] **T7-3 交代 `result/...tmp` 失败原因**——**Python 版本不兼容（3.14+ 出现，3.13 及以前正常）**（rebuttal A5）。每个容器固定受支持的 Python，加回归测试，从干净环境验证两个容器的说明步骤。
- [ ] **T7-4 交代内存口径**——审稿人的 >210 GB 来自 Tamarin **1.12.0**；1.8.0 可在 192 GB 内完成 BC 批处理，**1.10.0 同样可以（17 h 05 min，rebuttal 已报告的测量，须接上以免与 rebuttal 口径断裂）**。给准确命令、peak-RSS 日志、hash。
- [ ] **T7-5 FVP 的 bib + artifact 部分**——加 Cheval & Fontaine (CSF 2025) 引用；fvpgen 的命令、输入、输出、日志放进 artifact。（正文那句见 T4-8。）
- [ ] **T7-6 补 batch/interactive 脚本（列全 flags）**；每个容器分开低资源 smoke test 与全量评估，昂贵目标顺序执行，每个模型/lemma 可单独调用，附机器可读日志与 checksum。
- [ ] **T7-7 更新匿名仓库文档**——EN 稿承诺「more detailed instructions and commands」。仓库：`anonymous.4open.science/r/EntropyVerif-BF04`。
- [ ] ~~硬件配置~~——`results.tex:3` / `:158` 的 AMD Ryzen 9 7950X3D / 192 GB 正文已正确，**无需改**。

---

## 第八批 — 披露（要求8，依赖 P0-1/P0-2）

- [ ] **T8-1 改 `main.tex:116` 摘要末句**（**最高优先级单点修改，原计划漏列**）
  现为 "responsibly disclosed to **the vendor**"，与 `introduction.tex:49/:58`、`ethics.tex` 及「我们未直接联系单个厂商」**直接矛盾**。Reviewer B 原话就质疑 "it appears that no affected vendors were contacted"——摘要这句会被当成失实陈述。
  → 改为 "disclosed to the **Bluetooth SIG**"。
- [ ] **T8-2 统一 SIG 原话口径**（等 P0-2 结论）
  若确为两封信：写成带日期的时间线，两句都写，**不许只留有利的那句**；若为同一封：以邮件全文为准，论文与 rebuttal 同时改齐。
  ⚠ 绝不能停在「论文引正面半句、rebuttal 说保留半句」的状态。
- [ ] **T8-3 重写 `results.tex:148-151`**——删掉含糊的 "positive response"（Reviewer B 加引号点名了这个词）；`:150-151` 的 "will provide further feedback" / "keep communicating" 若无新邮件支撑，改为「截至 YYYY-MM-DD 无后续」。
- [ ] **T8-4 更新 `ethics.tex:4-7`**——带日期的事实记录，与 T8-3 完全一致。
- [ ] **T8-5 改 `ethics.tex:19`**（**必改**）——"Until specification updates and firmware patches are deployed" 暗示规范更新与固件补丁已在推进，属未经确认的修复暗示。改为不预设修复的表述。
- [ ] **T8-6 说明披露渠道选择**——UMD 是蓝牙**协议设计层面**的缺陷、非厂商实现 bug，故通过 SIG 协调披露；SIG 是否进一步通知厂商由其自行安排；我们未直接联系单个厂商。
- [ ] **T8-7 说明验证边界**——UMD 来自符号模型的推导与验证，尚未在实体设备上验证（`ethics.tex:11-13` 已有，保留并与正文呼应）。

---

## 收尾 — 全文一致性回扫（全部做完后一次性过）

- [ ] **C-1 版本**——1.8.0 / 1.10.0 归属全文一致；不出现「所有结果同一工具链」；性能对比表内无跨版本并列。
- [ ] **C-2 source lemma**——`results.tex:168`、`discussion-conclusion.tex:13` 统一为「in-file goal-ordering tactic，无 `[sources]`」，且不强于 EN 稿措辞；WPA2 上游 `[sources]` 单独说明。
- [ ] **C-3 无攻击协议**——Alipay（非 EMV），rebuttal 与论文一致。
- [ ] **C-4 披露四处 + rebuttal**——`main.tex:116`、`introduction.tex:49/:58`、`results.tex:148-151`、`ethics.tex:4-7` 口径一致，不提厂商、不暗示补丁；`discussion-conclusion.tex:22` 一并核对；与 `Rebuttal-NDSS-2027.md:42` 对齐。
- [ ] **C-5 FVP 三处齐备**——bib + 正文一句 + artifact 脚本。
- [ ] **C-6 scope 段落唯一**——只在 §III-A 展开一次，`discussion-conclusion.tex` 只回指，不出现两份措辞不同的 scope。
- [ ] **C-7 EN 承诺书逐条回扫**——拿 `reviews/Revision-Plan-EN.md` 的 8 条对照定稿，确认每条都有落点，尤其**第 5 条的独立小节**与**第 7 条的 Dockerfile**。
- [ ] **C-8 中英一致**——若 EN 稿有任何改动，英文与中文对照两部分同步。
