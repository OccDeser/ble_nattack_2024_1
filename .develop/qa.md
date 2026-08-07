NDSS 2027 Paper #474 Reviews and Comments
===========================================================================
Paper #474 Small Leaks Sink Great Ships: Automated Analysis of Protocols
that Tolerate Low-Entropy Keys


Review #474A
===========================================================================

Overall merit
-------------
2. Weak reject

Writing quality
---------------
2. Needs improvement

Reviewer expertise
------------------
3. Knowledgeable

Reviewer confidence
-------------------
2. Medium

Paper summary
-------------
The authors propose EntropyVerif, a syntactic-sugar extension of the Tamarin Prover tool that is designed to model dynamic brute-force attacks. Most of the current approaches hard-code the key-reveal rules in a sense that they expect a secret to appear within a specific function symbol during execution. EntropyVerif instead allows users to label low-entropy terms during a protocol  specification. It then emits the Tamarin specification with additional facts and rules that enable extraction (i.e. brute-forcing) of labeled terms (i.e. secrets) from arbitrary function symbols during the execution. The authors use EntropyVerif to rediscover know attacks on WPA2-PSK and BLE,
and to identify a novel attack on BC.

Strengths (bullet points)
-------------------------
- Timely and relevant topic of providing formal assurances for protocols that deal with low-entropy secrets against a Dolev-Yao attacker
- A novel UMD attack on BC.

Weaknesses (bullet points)
--------------------------
- Questionable contributions over state of the art – unclear if EntropyVerif brings something to the table that is not already possible with ProVerif or Tamarin.
- Technical exposition lacking

Detailed comments for authors
-----------------------------
I find the paper topic timely and relevant, and I appreciate the effort of developing the methodology and performing the case studies. However, the paper falls short in several aspects and it lands in the reject territory for me. The main objections that I have are that the proposed method does not seem to push state of the art when it comes to symbolic formal analysis that incorporates the attacker capability to do brute force attacks and, furthermore, numerous technical issues make me unconvinced on the soundness of the overall approach. The novel attack is a nice contributions, but not strong enough on its own to push the paper.

The main objection is the scope – you claim that the tool is capable of capturing all brute-force
behaviors, but the paper has not convinced me that is the case.  Consider, for example, a protocol that uses low-entropy key to encrypt a constant twice, each time paired with a different nonce and afterwards outputs two ciphertext on the network.  This protocol is vulnerable to an offline brute-force attack: an adversary can pick a candidate key, decrypt both ciphertexts and compare the constants.  However, your methodology does not account for this type of attack:  since the nonces are not known to the adversary prior, she cannot use relationship-breaking oracle to get rid of them. Therefore, the value-breaking oracle will never be utilized (since the key is not the only input to the encryption). If am incorrecnt, please elaborate if these kinds of attacks could be captured, and how.

There are works that use equivalence-based methods to verify whether a protocol is vulnerable to brute-force attacks, but I don't see you mention any of them. For example, in the ProVerif tool you can diff-equivalence to verify the resistance to offline-guessing attacks. There is also work in Tamarin (conditional observational equivalence) that does similar.  Both of these can capture the described attack.

The technical exposition of EntropyVerif is lacking in several aspects. Generally, this section needs more polish, better notation, more general description of the design, and examples. Few specific comments:
- What does "deconstructed" mean exactly, subterm relationship / subterm modulo equational theory / attacker knowledge? Similarly, what does it mean to "construct" a term? Given we are dealing with a formal system, precise definitions are needed in my opinion.
- Why not use more descriptive names for the functions?  I had to look multiple times at the definitions to remind myself what the function symbols mean.
- Why not use sets instead of sequences in the definitions, and define latter via lexical order?  
- In the definition of the relationship-breaking oracle, you require that a new function f' satisfies: for all k. f'(X\{a_i\},k) = f(X,k).  However, this is not enough. If I'm not mistaken, the function f' needs to be a partial application of f: f'_{a_i}(x_1,...,x_{i-1},x_{i+1},...,x_n, k) = f(x_1,...,x_{i-1},a_i,x_{i+1},...,x_n, k).
- Why not allow the adversary to compromise honest agents in the BLE and BC secrecy lemmas?

Appreciate the artifact provided by the authors! I have go to the source code to clarify the technical inconsistencies in the paper, but also to try to reproduce the results. I ran into several issues:

 I cannot verify the BC model neither on Arch Linux nor on Fedora.  After doing:
```
cd case_studies/bc
make BC_SESSION_MODELS/BC_SESSION_QA_CLEO_CEKS_PLEO_PLKS.spthy
python3 ./verifier.py
```
I get the following:
```
Verifying model: BC_SESSION_QA_CLEO_CEKS_PLEO_PLKS.spthy
ERROR:root:Unexpected error verifying BC_SESSION_QA_CLEO_CEKS_PLEO_PLKS.spthy
Unexpected error verifying BC_SESSION_QA_CLEO_CEKS_PLEO_PLKS.spthy: [Errno 2] No such file or directory: 'result/BC_SESSION_QA_CLEO_CEKS_PLEO_PLKS.spthy.tmp'
```
Consider using a container to ensure the results can be reproduced faithfully.

Furthermore, I tried to verify all BC models with
```
make all
python3 ./verifier.py
```
However, after several minutes it consumes over 210 GB of available memory, causing swapping to kick in.
Since you wrote that you had 192 GB of memory at disposal, I have assumed that
that the Tamarin command limits the memory usage. However, this does not seem to be the a case.

Moreover, you do not provide a script to execute Tamarin in interactive mode with the appropriate flags enabled. For BC, I had to look into verify.py to figure what flags to use.

When I run Tamarin with the BC/BLE model in an interactive mode, I get a warning
that the set of equations is not subterm convergent.  Did you check that this set of equations
is convergent with a finite-variant property?  You do not mention any this in the
paper.

Ethical Considerations
----------------------
3. I don't see any ethical implications for this paper.

I am attesting that the review is an accurate statement of my own opinion
of the paper and I am solely responsible for writing this review

---------------------------------------------------------------------------
Yes



Review #474B
===========================================================================

Overall merit
-------------
4. Accept

Writing quality
---------------
4. Well-written

Reviewer expertise
------------------
3. Knowledgeable

Reviewer confidence
-------------------
3. High

Paper summary
-------------
This paper proposes EntropyVerif, a syntactic-sugar front end for the TAMARIN model checker that captures the brute-force prerequisites, requirements, and cost of breaking low-entropy keys instead of assuming perfect cryptography. Specifically a key-breaking oracle is defined that can recover function terms marked as low-entropy, provided that the other function terms can be derived. EntropyVerif is then used to rediscover a number of recent attacks on low-entropy key protocols (PMKID, KNOB, and Method Confusion), and a new attack on Bluetooth Classic.

Strengths (bullet points)
-------------------------
* A novel protocol-agnostic abstraction is derived with an oracle that captures brute-force attacks on different protocol stages

* The system is built entirely on top of the TAMARIN kernel, not requiring any underlying modifications that may call correctness into question. Artifacts are made available.

* Two-stage oracle design neatly captures 1) value-breaking, brute-forcing function inputs that are low-entropy, and 2) relationship-breaking, reducing function inputs that the attacker can deterministically predict.
  
* Supports bit-level attacker budgets, allowing claims to be justified in terms of attacker complexity.

* Rediscovers known real-world attacks without protocol-specific oracles, and a new attack on Bluetooth Classic

Weaknesses (bullet points)
--------------------------
* The relationship-breaking oracle introduces many new branches, causing significantly higher complexity as compared to verification without low entropy tags.
  
* Evaluation reports analysis times in EntropyVerif, but no breakdown is provided. Therefore no understanding of the most expensive steps is provided, and the relationship between runtime and protocol complexity is unexplored.

* Verification requires the attacker to derive or observe function outputs and all non-key inputs deterministically. Cases where the attacker has partial information about inputs are not considered.

* Human input is required to design rules that label keys as low-entropy. Further human guidance was required to achieve a feasible runtime for certain protocols.
  
* Lack of quantitative guidance on choosing realistic budgets and mapping them to attacker cost in practice.

Detailed comments for authors
-----------------------------
Thanks for submitting this interesting paper to NDSS! EntropyVerif is a novel and interesting approach to formally verify protocols with low-entropy keys and mapping attacks onto real computational constraints. Whilst the approach does have some inherent weaknesses, including the manual work required to label low-entropy keys and in certain cases guide and prune the verification, nevertheless EntropyVerif generalises over current approaches for analysing these protocols which remain more manual. 

The main weakness of this paper is that the situations in which human guidance is required are currently not widely explored or evaluated. In the more expensive Bluetooth Classic configurations a small number of additional source lemmas and a script to prioritise goals is provided - however, the evaluation does not report the performance gains provided by additions or the extent to which they would be necessary in future work using EntropyVerif.

Furthermore, EntropyVerif only considers attackers that can derive all function inputs deterministically. However, in certain protocols the adversary may be able to determine partial information about some function inputs, which is not considered in this work. As a result, protocols which pass verification may be secure only with respect to this deterministic attacker model. The text of the paper should address this clearly.

Finally, in the evaluation the top-level verification times are provided (e.g. in Table IV), but no performance breakdown is provided to understand the more expensive parts of the process. The authors should consider at least comparing the performance of EntropyVerif against TAMARIN without low-entropy labels to understand the cost of this modelling technique.

Concrete steps for improvement
------------------------------
* Clearly discuss the deterministic nature of the attacker model, acknowledging that attackers that exploit partial information about function inputs are not considered.

* Further discuss the specific human guidance provided in the BC configurations in Section VI.E, and the protocol-level knowledge that was required to create it.

* Evaluate the performance implications of providing/not providing human guidance for different protocols.

* Compare verification performance results with TAMARIN by itself (with no low-entropy labels) to understand the relative performance impact of EntropyVerif.

Ethical Considerations
----------------------
1. This paper/research raises ethical concerns that need to be addressed.

Describe Ethical Concerns
-------------------------
The unilateral multi-downgrade (UMD) attack discovered was disclosed to the Bluetooth SIG in VI.d, receiving a ``positive response'' and the acknowledgment in the appendix. However, the current status is that the SIG has not completed an analysis yet, and it appears that no affected vendors were contacted.

I am attesting that the review is an accurate statement of my own opinion
of the paper and I am solely responsible for writing this review

---------------------------------------------------------------------------
Yes



Review #474C
===========================================================================

Overall merit
-------------
3. Weak accept

Writing quality
---------------
4. Well-written

Reviewer expertise
------------------
2. Some familiarity

Reviewer confidence
-------------------
1. Low

Paper summary
-------------
This paper introduces a protocol-agnostic extension of TAMARIN to automatically reason about brute-force attacks on protocols that tolerate low-entropy keys.  The main idea lies on the introduction of two oracles (a key-breaking oracle and a relationship-break oracle) and an extended rule syntax built upon TAMARIN's existing rewriting rules.  The proposal is implemented as a tool called EntropyVerif which is demonstrated to be capable of discovering known attacks on low-entropy keys as well as a new attack on Bluetooth Classic.

Strengths (bullet points)
-------------------------
- An automatic and protocol-agnostic tool for analyzing protocols with low-entropy keys, which is practical and useful.
- Good results in using the proposed tool in re-discovering existing attacks and a new attack

Weaknesses (bullet points)
--------------------------
- Limited evaluation on 3 protocols only
- Lacking detailed analysis on what contributes to the long analysis time in certain scenarios

Detailed comments for authors
-----------------------------
Thanks for submitting this interesting work to NDSS.  Analyzing protocols that allow low-entropy keys is an interesting problem and the protocol-agnostic solution proposed is new and practical.

The paper is generally well written and easy to follow.

My main concern on the paper is on its evaluation section.  First, the evaluation covers only three protocols (WPA2-PSK, BLE, and BC), covering two rediscovery of known attacks and one new attack.  This limited evaluation makes it hard to fully appreciate the capability of the proposed system.  I understand that there might not be many exploitable protocols there, but the paper could also include some non-exploitable protocols that allow low-entropy keys to show (1) what the proposed technique could potentially ascertain in terms of not vulnerable to brute force attacks; (2) how much time it takes to carry out such analysis.  If, e.g., the analysis never terminates when analyzing such protocols, it would be a critical limitation.

My second concern is the lack of understanding on what contributes to the long analysis time on some scenarios (Table IV).  I understand that most of them are cases where no attack is found, but some analysis on what kind of operations in the protocols adds the most to analysis time will be helpful in understanding the capability and limitation of the proposed system.

Concrete steps for improvement
------------------------------
- extend evaluation to more protocols
- perform deeper analysis on what contributes to the long analysis time

Ethical Considerations
----------------------
3. I don't see any ethical implications for this paper.

I am attesting that the review is an accurate statement of my own opinion
of the paper and I am solely responsible for writing this review

---------------------------------------------------------------------------
Yes



Review #474D
===========================================================================

Overall merit
-------------
3. Weak accept

Writing quality
---------------
3. Adequate

Reviewer expertise
------------------
1. No familiarity

Reviewer confidence
-------------------
1. Low

Paper summary
-------------
This paper proposes EntropyVerif, an extension of TAMARIN for analyzing protocols that tolerate low-entropy keys. The authors evaluate the tool on WPA2-PSK, BLE, and Bluetooth Classic.

Strengths (bullet points)
-------------------------
+ The paper studies an important limitation of symbolic protocol verification.

+ The proposed tool is practically appealing.

+ The claimed new Bluetooth Classic attack is interesting.

Weaknesses (bullet points)
--------------------------
- The attacker model and low-entropy abstraction can be too coarse.

- Evaluation scale is limited and performance may be a concern.

Detailed comments for authors
-----------------------------
Thank authors for submitting this work to NDSS. I am not an expert in this area, but I do have few concerns for this paper:

1. The attacker model and low-entropy abstraction are too coarse. The paper models the attacker as being able to brute-force term labeled low-entropy if its nominal bit length is within a fixed budget, such as 32 or 64 bits. This abstraction is simple, but it may over-approximate real attacker capabilities. In practice, brute-force feasibility depends not only on bit length, but also on the key-derivation function, protocol transcript, salts/nonces, verification oracle, implementation details, and available parallelism. The paper needs a clearer discussion of when this oracle abstraction is sound and when it may produce false positives.

2. The evaluation covers only three protocol families, and many results are rediscoveries of known attacks. This is useful, but limited for supporting a broad claim of protocol-agnostic applicability. In addition, some Bluetooth Classic verification cases take a very long time, up to around 27 hours, and require auxiliary lemmas or heuristic scripts. This raises questions about scalability and usability for more complex protocols.

Ethical Considerations
----------------------
3. I don't see any ethical implications for this paper.

I am attesting that the review is an accurate statement of my own opinion
of the paper and I am solely responsible for writing this review

---------------------------------------------------------------------------
Yes



Rebuttal Response by Author [Yongkang Xiao <xiaoyongkang@whu.edu.cn>] (977 words)
---------------------------------------------------------------------------
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



Comment @A1 by Reviewer A
---------------------------------------------------------------------------
Dear Authors,

Many thanks for the response. If possible, please provide few additional clarification regarding A1 and A2 above.

Regarding the scope of brute force analysis, please note that I tried to give a simplest possible example that would fall outside of the scope of your method.

What do you mean exactly "deterministic forward brute-force attacks"? Also, "attacks requiring inverse operations over outputs with unknown inputs" is problematic since you are reasoning over attacks, rather then the protocol features. For example, can I analyze a protocol that uses encryption using this framework and have some assurance of the soundness?

Regarding equivalence-based work, are you claiming there are protocols-attacks where your method is applicable and equivalence-based work is not?


Comment @A2 by Author [Yongkang Xiao <xiaoyongkang@whu.edu.cn>]
---------------------------------------------------------------------------
We thank the reviewer for the follow-up questions. We would first like to clarify the positioning of EntropyVerif: it analyses protocols under a precisely defined attacker model that characterises a class of brute-force capabilities, and discovers concrete attacks under that model.

**Q1: On the meaning of "deterministic forward brute-force"**

The term describes an attacker capability rather than a class of attacks, and it is this capability that defines our attacker model. For a function application $f(x_1,\ldots,x_n,k)$, the attacker may recover k whenever (i) the output of f has been observed, (ii) all non-key inputs xᵢ are deterministically derivable from the attacker's current knowledge, and (iii) the nominal bit-length of k lies within the given budget. Recovery proceeds by enumerating candidate values of $k$, recomputing f in the forward direction, and comparing the result against the observed output.

Here, *deterministic* means that the correct value of $k$ is uniquely identified, and *forward* means that the attacker may only apply the protocol's own cryptographic primitives in the forward direction, without applying inverse operations to observed values. Our attacker model is the standard one extended with precisely this capability.

**Q2: On reasoning over attacks rather than protocol features, and on protocols using encryption**

We thank the reviewer for this observation, and we agree that our earlier formulation was phrased in terms of attacks rather than protocol features. More precisely, what we described above is our attacker model, and our results are stated with respect to it. An attack reported by the tool is executable under the given budget and comes with a concrete trace.

Concretely, if every operation from the low-entropy value to the public output is invertible, a protocol may admit brute-force attacks that our framework cannot find, since such attacks require capabilities beyond our attacker model. The reviewer's example is of this kind, as it relies on inverse operations over ciphertexts.

This does not mean our framework is useless for such protocols. Our tool can still find attacks that fall within our attacker model. Bluetooth Classic is one such case: its key derivation is built on encryption primitives, and we still found an executable attack (UMD) on it.

**Q3: On the relationship to equivalence-based work**

Equivalence-based methods can determine whether a given key is exposed to brute-force risk. Taking BC as an example, such methods can reveal that SK is subject to a brute-force risk. Their conclusion, however, stops at the observation that ciphertexts under SK are distinguishable and hence guessable. Such analyses do not model whether the guessing is within the attacker's budget. Since SK is 128 bits, the reported attack is regarded as infeasible in practice, and the finding is read as a risk that remains under control. The protocol therefore continues to be deployed, even though an exploitable attack (UMD) does exist. This is the gap our method fills. Equivalence-based analysis shows that a risk exists; our method offers a way to turn that risk into a concrete attack under an explicit budget constraint.


Comment @A3 by Reviewer A
---------------------------------------------------------------------------
Dear Authors, appreciate the response.


Comment @A4 by Author [Yongkang Xiao <xiaoyongkang@whu.edu.cn>]
---------------------------------------------------------------------------
Dear Reviewers,

Thank you for giving us the opportunity to revise our paper.

We noticed that the NDSS 2027 Call for Papers mentions that authors receiving a Major Revision will be provided with a list of revision tasks. However, we could not find such a list in HotCRP or in the decision notification email.

Could you please let us know whether a separate list of revision tasks will be provided later, or whether the reviews and discussion should be treated as the complete list of revision tasks?

Thank you for your time and assistance.


Comment @A5 by Reviewer A
---------------------------------------------------------------------------
Dear Authors, 

We will provide the revision tasks by the end of the day.


Comment @A6 by Author [Yongkang Xiao <xiaoyongkang@whu.edu.cn>]
---------------------------------------------------------------------------
Thank you for the update. We appreciate your prompt response.


Comment @A7 by Reviewer A
---------------------------------------------------------------------------
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