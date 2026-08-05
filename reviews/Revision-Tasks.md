Dear authors,

We would like to invite you to submit a major revision of your paper.

Specifically, please address the following concerns raised by the reviewers:

1. Instead of claiming that the framework can capture all brute-force attacks, precisely characterise the settings (attacker models, protocols, cryptographic primitives, other necessary assumptions) where the framework is able to capture attacks, and the settings where that is not the case. Give appropriate justifications for these claims, and/or be clear where the applicability/soundness/completeness is uncertain. Revise all completeness/scope claims accordingly.

2. In addition to 1, specify explicitly the attacher model, i.e., that the framework considers only a deterministic attacker, and that attacks that exploit probabilistic attacker knowledge are out-of-scope.

3. Add and discuss related equivalence-based work (including ProVerif diff-equivalence, and Tamarin observational equivalence for offline guessing), and precisely position EntropyVerif against it.

4. Improve the technical exposition (see review A)

5. Improve the evaluation, by including the non-exploitable protocols (e.g., the three Alipay protocols mentioned in the rebuttal), and a more comprehensive performance evaluation including (performance comparison against plain Tamarin, breakdown on where time is spent). (see reviews B, C, D)

6. Further discuss and elaborate the human guidance needed to perform the proofs (see review B).

7. Ensure that the artifact is reproducible (see review A)

8. Update and accurately report the disclosure status for the discovered vulnerability (see review B)

I will act as the decision lead for this paper and am happy to answer questions about the process. If you have any, please reply to this comment.

Please note that your paper must implement the above changes, and the revised version will be reviewed again before a final decision is made.