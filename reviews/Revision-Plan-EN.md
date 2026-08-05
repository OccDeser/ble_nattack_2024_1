# Revision Plan — Paper #474 (Major Revision)

## English

Dear reviewers,

Thank you very much for your helpful feedback and for providing the revision tasks. We have carefully considered them and plan to make the following revisions:

1. We will revise the scope, applicability, soundness, and completeness claims in the abstract, Section I, Section III-A, Section VI, and Section VIII.

2. We will revise the description of the attacker model throughout the paper to make clear that our framework considers only a deterministic attacker.

3. In Section VII (Related Work), we will add and discuss ProVerif diff-equivalence and Tamarin observational equivalence for offline guessing, and accurately position EntropyVerif against this related work.

4. We will improve the technical exposition and correct all unclear or inaccurate descriptions identified in review A.

5. In Section VI (Results), we will add a subsection on performance evaluation:

   - We will use the three Alipay models to report the overhead on protocols with no exploitable brute-force threat.
   - We will compare EntropyVerif with the corresponding plain-Tamarin models under the same Tamarin version.
   - Directly partitioning Tamarin’s wall-clock time by goal is difficult because its constraint solving is interdependent. We will therefore analyze the `solve(...)` steps in the proof traces and report the proportions associated with `MDerive`, standard Dolev--Yao, and protocol goals. This provides an approximate breakdown of the proof effort introduced by EntropyVerif, rather than an exact time breakdown.

6. We will correct the discussion of human guidance to state that the final BC models use only heuristic tactics that adjust goal and branch priorities.

7. We will provide Dockerfiles to pin the environments. We will use Tamarin 1.8.0 for WPA2-PSK, BLE, and BC. The original Alipay models contain syntax that Tamarin 1.8.0 does not support, so we will provide a second environment with Tamarin 1.10.0. We will also update the documentation with more detailed instructions and commands to make the results easier to reproduce and inspect.

8. We will update the vulnerability disclosure section with a dated and accurate account of the Bluetooth SIG's response and any subsequent update. We will request the latest status from the SIG before resubmission.

We sincerely appreciate your guidance. Please let us know if any part of this plan does not fully address the requested revisions.

## 中文对照

尊敬的 Reviewer A：

非常感谢您提供的宝贵意见，并作为 decision lead 列出 revision tasks。我们经过认真考虑，计划进行以下修改：

1. 我们将修改摘要、Section I、Section III-A、Section VI 和 Section VIII 中关于范围、applicability、soundness 和 completeness 的表述。

2. 我们将调整全文中对攻击者模型的描述，明确我们的框架只考虑确定性攻击者。

3. 我们将在 Section VII（Related Work）中补充并讨论 ProVerif diff-equivalence 和 Tamarin observational equivalence 在离线猜测分析中的工作，并准确定位 EntropyVerif 与这些相关工作的关系。

4. 我们将改进技术表述，并纠正 Reviewer A 指出的所有不清楚或不准确的描述。

5. 我们将在 Section VI（Results）中新增一个独立的性能评估小节：

   - 我们将使用三个 Alipay 模型报告不存在可利用暴力破解威胁时的性能开销。
   - 我们将在相同 Tamarin 版本下对比 EntropyVerif 与相应的 plain-Tamarin 模型。
   - 由于 Tamarin 的约束求解相互依赖，难以按 goal 直接拆分 wall-clock 时间。因此，我们将分析 proof traces 中的 `solve(...)` steps，报告 `MDerive`、标准 Dolev--Yao 和协议 goals 所占的比例。这能够近似反映 EntropyVerif 引入的证明工作量，而不是提供精确的时间拆分。

6. 我们将修正关于人工引导的表述，说明最终的 BC 模型仅使用启发式策略来调整目标和分支的优先级。

7. 我们将在匿名仓库中提供 Dockerfile，以固定运行环境。WPA2-PSK、BLE 和 BC 使用 Tamarin 1.8.0。Alipay 原始模型中包含 Tamarin 1.8.0 不支持的语法，因此我们将提供使用 Tamarin 1.10.0 的第二套环境。我们还将更新更详细的说明和命令，使结果更容易复现和查看。

8. 我们将以带日期的准确事实更新漏洞披露部分，说明 Bluetooth SIG 的回复和后续进展。重投前，我们将再次向 SIG 询问最新状态。

我们衷心感谢您的指导。如本修改计划有任何未能充分回应修改要求之处，敬请您指正。
