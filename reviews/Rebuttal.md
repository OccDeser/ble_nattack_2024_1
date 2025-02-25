We sincerely thank the reviewers for their constructive feedback. Due to the word limit, we address the major concerns below and will respond to other comments via the submission system. 

## Review A

1. The full models, automatic verification scripts, and proof traces are provided in [16] [https://anonymous.4open.science/r/EntropyVerif-F8DC](https://anonymous.4open.science/r/EntropyVerif-F8DC).

2. Our work introduces two oracles that enable Tamarin to brute-force low-entropy secrets *without prior knowledge* needed by attacks, thereby automating new attack discovery. Specifically, we eliminate the need for manual rules for arguments and functions exploited by each brute-force attack.

3. Bluetooth SIG recently acknowledged UMD attacks. Our attacks pose a greater threat to BC devices and are more dangerous than the famous KNOB attacks because they:
    - **Only require peripheral devices to support short keys**, making them easier to exploit than KNOB attacks, which require both central and peripheral devices.
    - **Present greater mitigation challenges**: Central devices (e.g., smartphones) can easily patch vulnerabilities via OTA updates, mitigating KNOB attacks. However, peripherals (especially those using low-cost chips) often lack firmware upgrade mechanisms, making security patches difficult to implement. In these cases, fully mitigating UMD attacks demands costly hardware upgrades.

4. Our extension fully supports Tamarin to analyze all possible secrets injected in protocols automatically, provided that all secrets are implicitly marked as low-entropy. However, we chose to let users mark manually for the following reasons:
    - In protocols where **high-entropy secrets** are used, attackers cannot brute-force them. Then, performing low-entropy analysis is meaningless.
    - **Advances in computational power** enhance attackers' capabilities. By enabling users to mark specific secrets as low-entropy, we adapt to varying attackers, offering a more accurate assessment of the protocol's security boundaries.

5. **Existing Protocol Analysis**: Our survey of other mainstream protocols (e.g., TLS and 5G-AKA) revealed that they employ keys with sufficient entropy, thereby eliminating the need for our methodology.

## Review B

1. **Novelty**: Our work is inspired by [9] but differs significantly. In [9], a specialized rule is applied to break low-entropy keys, but it requires prior knowledge of the concrete functions and arguments exploited by attackers, which limits its use in other brute-force attacks. However, we only require users to mark secrets based on protocol design/specification and enable Tamarin to automatically combine and identify exploitable functions and arguments which makes uncovering new attacks possible.

2. **Impact of Generalization**: We acknowledge that Section 6 inadequately demonstrates the impact of our methodology through case studies. Here, we clarify the key points:
    - **Effectiveness**: In our comparison, we supplemented the model in [21] with PMKID implementation (and it still failed to detect the PMKID attack), but we did not emphasize this clearly. When applying our extension to this model, the attack was successfully detected, showcasing the effectiveness of our methodology.
    - **Adaptability**: [9] omitted the session phase in their model, while adding it prevented their model from detecting KNOB attacks. This revealed their reliance on prior knowledge and model-specific customization. Our methodology detected the attack regardless of the session phase, demonstrating its adaptability. We regret not including the comparison between [9] and ours on the model without the session phase, and we will address this oversight in the revised version.
    - **Automation**: Our methodology, demonstrated in the BC case study, can automatically identify exploitable function-argument combinations. This capability enables the automated discovery of new attacks, as evidenced by the UMD attack we identified.

3. **UMD Attack**: We believe that the UMD attack still poses significant risks, and our reasoning aligns with Review A (Response 3).

4. **Performance Analysis**:  Low-entropy analysis increases verification time (e.g., BLE: 2,376s -> 14,918s). Further time comparisons will be provided in Section 6. While our methodology may fail to terminate, it is important to note that even Tamarin cannot guarantee that all verifications will terminate, as the undecidability of protocol correctness is a common challenge in formal verification.

5. **Contribution**: Please refer to Review A (Response 2), Review B (Response 1), and Review C (Response 1).

## Review C	

1. We acknowledge that an attacker can recover the key given all arguments and function values. The core challenge lies in identifying exploitable functions — precisely the capability we aim to develop in Tamarin. Our methodology enables Tamarin to automatically identify vulnerable functions/arguments and dynamically combine them to discover new attacks. The UMD attack we discovered exemplifies this methodology, demonstrating how the coordinated use of multiple functions can compromise secrets.
