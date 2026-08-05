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