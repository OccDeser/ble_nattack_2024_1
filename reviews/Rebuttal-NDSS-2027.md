We thank all reviewers for their constructive feedback. 
Due to space limitations, we address the main concerns below. 
We look forward to clarifying any remaining points during the interactive discussion period.

## To Reviewer A

1. **Scope of brute-force analysis.** We agree that EntropyVerif cannot capture the example in which the same low-entropy key encrypts a known constant twice together with different unknown nonces. 
We clarify two characteristics of this attack. 
First, this attack relies on decrypting the ciphertexts with each candidate key and therefore cannot be applied to cryptographic functions without an inverse operation, such as hash functions. 
Second, trial decryption provides only probabilistic confidence: a wrong key may also yield the expected constant, and a shorter constant increases this false-acceptance probability. 
Two ciphertexts reduce, but do not eliminate, this probability. 
We will revise our scope claim: EntropyVerif models deterministic forward brute-force attacks while attacks requiring inverse operations over outputs with unknown inputs and probabilistic candidate validation are outside its scope.

2. **Equivalence-based work.** We will add related work using ProVerif diff-equivalence and Tamarin observational equivalence to analyze offline-guessing attacks. 
Unlike these equivalence-based analyses, EntropyVerif models budget-bounded low-entropy compromise as an explicit attacker capability in standard Tamarin traces, allowing recovered key components to participate in subsequent protocol steps and be composed across sessions, as demonstrated by the UMD attack.

3. **Formal definitions.** "Deconstruct" means syntactic decomposition, not deduction modulo the equational theory or attacker knowledge. 
Specifically, $\delta(t)$ is the syntactic-subterm closure of $t$, while $\rho(t)$ contains its atomic terms. 
We will replace the ambiguous terminology with recursive definitions and more descriptive names. 
We agree that sets provide a cleaner formalization. Sequences are only an implementation choice, so we will use sets formally and impose a fixed order only when producing an argument tuple. We will also correct $f'$ as the partial application
$f'_{a_i}(x_1,\ldots,x_{i-1},x_{i+1},\ldots,x_n,k)=f(x_1,\ldots,x_{i-1},a_i,x_{i+1},\ldots,x_n,k).$

4. **Compromise.** Our BLE case study applies EntropyVerif to an existing BLE model whose attacker model does not include the compromise of honest participants. Our BC model adopts the same attacker model.

5. **Artifact and equational theory.** The `result/...tmp` failure is caused by a Python version incompatibility. It occurs with Python 3.14 or later, but not with Python 3.13 or earlier.
The memory blow-up is version-dependent: Tamarin 1.12.0 exhausts memory quickly, whereas Tamarin 1.10.0 completed BC `make all` in 17 h 05 min within the reported 192 GB limit. 
We will provide a ready-to-run docker image with fixed versions of Tamarin 1.10.0 and Python 3.12. 
We will also provide an interactive-mode script with all required flags.
Although our equations are not subterm-convergent, we verified the finite-variant property using fvpgen (V. Cheval and C. Fontaine, "Automatic verification of Finite Variant Property beyond convergent equational theories," CSF 2025) and will include this check in the artifact.

## To Reviewer B

1. **Human guidance.** Our final BC models use only heuristic tactics that adjust goal and branch priorities so that infeasible branches can be closed earlier, accelerating Tamarin's analysis. 
In particular, the tactics deprioritize brute-force-related goals involving `MDerive` and `LowEntropy`, allowing Tamarin to analyze them after other goals. 
The underlying strategy is general, although its application may require minor adjustments for each concrete model. 
Auxiliary lemmas were used only in an earlier version. The final BC models use tactics alone, and we will correct the corresponding statement in the paper. We will also carefully proofread the entire manuscript to identify and correct any similar inconsistencies or typographical errors.

2. **Deterministic attacker.** As discussed in A1, EntropyVerif cannot cover attacks involving uncertain or partial input information, and its verification results provide guarantees only under the deterministic attacker model.

3. **Performance.** For the BLE protocol, which has an exploitable brute-force threat, the original model required 2376.10 seconds, whereas EntropyVerif required 14,918.34 seconds. For protocols that contain low-entropy values but have no exploitable brute-force threat, EntropyVerif introduces little additional runtime, as discussed in C1.

4. **Disclosure.** We reported the issue to the Bluetooth SIG. In response to our follow-up, the SIG acknowledged that the attack poses a potential threat while noting that successful exploitation requires specific conditions. We have not received any further updates from the SIG, but we remain committed to cooperating fully with the SIG in addressing this issue.

## To Reviewer C

1. **Evaluation.** We applied EntropyVerif to three Alipay payment protocol models developed in a work accepted by USENIX Security 2026. These protocols contain low-entropy payment PINs but do not permit their recovery through brute-force attacks.

    | Model | Original | EntropyVerif | Original (adjusted) | EntropyVerif (adjusted) |
    |---|---:|---:|---:|---:|
    | `alipay_app` | 133.65 s | 142.58 s | -- | -- |
    | `alipay_mobile_web` | 133.30 s | 142.25 s | -- | -- |
    | `alipay_order_code` | 597.38 s | 2,509.61 s | 214.68 s | 556.30 s |

    All three analyses terminated without tactic modifications, and EntropyVerif added only about 10 s for the first two models. For `alipay_order_code`, we applied a minor tactic adjustment to both versions, reducing their verification times to 36% and 22% of the unadjusted times, respectively. This indicates that its initially long runtime was largely caused by a suboptimal tactic in the original model.

2. **Long-running analyses.** The generated brute-force rules introduce additional goals. This is especially costly for secure configurations, for which Tamarin must close all remaining proof branches rather than terminate upon finding an attack. 

## To Reviewer D

1. **Abstraction accuracy.** We agree that overestimating the attacker's brute-force capability may identify attacks that are valid in the symbolic model but infeasible in practice. EntropyVerif allows the modeler to select a budget appropriate to the practical attacker being modeled, as illustrated by our two BC attacker configurations. We will clarify that verification results are conditional on the selected attacker model and budget.

2. **Scalability.** As discussed in B1, the additional goals introduced by EntropyVerif can increase verification time. Our BC models use no auxiliary lemmas and rely only on heuristic tactics that prioritize goals and branches. The additional Alipay evaluations in C1 show that all three analyses terminate successfully, although the overhead can vary substantially across protocol models.
