## You asked:

\# Citation Request: Super-Twisting Algorithm Finite-Time Convergence I need academic citations for the finite-time convergence theorem of the Super-Twisting Algorithm (STA). ## THEOREM STATEMENT "The super-twisting algorithm ensures finite-time convergence to the second-order sliding set {s = 0, ṡ = 0} if the parameters satisfy \[specific conditions\]." ## TECHNICAL CONTEXT \*\*Domain:\*\* Second-Order Sliding Mode Control - Super-Twisting Algorithm (STA) \*\*Background:\*\* Classical SMC achieves first-order sliding (s = 0), but requires discontinuous control in the feedback loop, causing chattering. Super-twisting achieves \*\*second-order sliding\*\* (s = 0 AND ṡ = 0) with: - Continuous control signal (no chattering) - Only sliding variable s needed (not ṡ) - Finite-time convergence \*\*Super-Twisting Algorithm:\*\*

    u̇ = -α·sgn(s)
    u = -λ·|s|^(1/2)·sgn(s) + u̇

Or equivalently:

    u = -λ·|s|^(1/2)·sgn(s) - α·∫sgn(s)dt

Where: - s: sliding variable - λ, α > 0: algorithm gains - |s|^(1/2): fractional power (0.5) - sgn(s): sign function \*\*System Model:\*\* Consider second-order system:

    ṡ = φ(t,x) + γ(t,x)·u
    s̈ = φ̇ + γ̇·u + γ·u̇

With bounded uncertainty:

    |φ̇| ≤ Φ
    0 < γ_min ≤ γ ≤ γ_max

\*\*Convergence Conditions:\*\* Parameters λ, α must satisfy specific inequalities involving bounds Φ, γ\_min, γ\_max. Classic sufficient conditions (Levant 1993):

    λ > √(2Φ/γ_min)
    α > Φ/γ_min

Or with tighter bounds (Moreno & Osorio 2008):

    λ² ≥ 4Φ·(α+Φ)/(γ_min·(α-Φ))

\*\*Second-Order Sliding Mode:\*\* System reaches \*\*second-order sliding set\*\*:

    S² = {(s, ṡ) : s = 0, ṡ = 0}

This is stronger than classical SMC which only achieves s = 0 (but ṡ may oscillate/chatter). ## THEOREM SIGNIFICANCE Super-twisting algorithm represents major advancement: 1. \*\*Chattering reduction:\*\* Continuous control (no high-frequency switching) 2. \*\*Robustness:\*\* Works with bounded uncertainties like classical SMC 3. \*\*Finite-time:\*\* Convergence in finite time T < ∞ 4. \*\*Practical:\*\* Only requires s measurement (not ṡ) ## REQUIRED CITATIONS Find 2-3 papers that: 1. \*\*Prove finite-time convergence\*\* of super-twisting to second-order sliding set 2. \*\*Establish parameter conditions\*\* (λ, α) for convergence with bounded uncertainties 3. \*\*Provide Lyapunov analysis\*\* or convergence time bounds \*\*Essential references:\*\* - \*\*Levant (1993, 2003)\*\* - Original super-twisting algorithm papers - \*\*Moreno & Osorio (2008, 2012)\*\* - Strict Lyapunov functions for STA - \*\*Shtessel et al. (2014)\*\* - Sliding Mode Control and Observation, Chapter 5 - \*\*Edwards & Shtessel (2016)\*\* - Adaptive continuous higher order sliding mode control ## OUTPUT FORMAT For each citation: 1. \*\*Full Citation:\*\* Authors, "Title," Journal/Conference, Year, Pages 2. \*\*DOI/URL:\*\* Link 3. \*\*Relevance:\*\* Which theorem establishes finite-time convergence to {s=0, ṡ=0}? 4. \*\*Key Condition:\*\* Parameter inequalities for λ, α guaranteeing convergence ## FOCUS AREAS Critical topics: - Super-twisting algorithm formulation - Second-order sliding mode definition - Finite-time convergence proofs (Lyapunov, homogeneity) - Parameter tuning conditions - Chattering reduction compared to classical SMC \*\*Historical context:\*\* - Levant (1993): Original STA paper - Levant (2003): Homogeneity-based analysis - Moreno & Osorio (2008): Strict Lyapunov function (major breakthrough) Provide authoritative citations proving super-twisting's finite-time convergence to second-order sliding.

---

## ChatGPT Replied:

Understood. I'll conduct detailed research on the finite-time convergence theorem of the Super-Twisting Algorithm as you described. I will focus on identifying and citing 2–3 authoritative sources that prove finite-time convergence to {s = 0, ṡ = 0}, outline the parameter conditions for λ and α, and provide Lyapunov analyses. Once I've gathered relevant sources, I'll provide full citations, DOIs/URLs, explanations of their contributions, and key parameter conditions. I'll begin this research now.

Worked for 9 minutes

Worked for 6 minutes

Here are key academic references that rigorously establish finite‑time convergence for the super‑twisting algorithm (STA). Each citation is accompanied by the theorem’s relevance and the conditions on the STA gains that guarantee convergence to the second‑order sliding set  $S^2=\{s=0,\dot{s}=0\}$ .

| Ref. (authors, publication & year) | DOI / URL | Relevance to finite‑time convergence | Key conditions on STA gains |
| --- | --- | --- | --- |
| **A. Levant – “Introduction to high‑order sliding modes” (chapter in _Variable Structure Systems_, 2002‑2003)**[tau.ac.il](https://www.tau.ac.il/~levant/hosm2002.pdf#:~:text=The%20following%20controller%20does%20not,the%20initial%20value%20is%20inside) | Preprint: [https://www.tau.ac.il/~levant/hosm2002.pdf](https://www.tau.ac.il/~levant/hosm2002.pdf) | Levant formulated the **super‑twisting controller** to remove chattering while guaranteeing a second‑order sliding mode. For the uncertain integrator  $\dot{x}=a(t)+b(t)u$ , he proposed the dynamic controller (u=-\\lambda | x |
| **J. A. Moreno & M. Osorio – “A Lyapunov approach to second‑order sliding mode controllers and observers,” 47th IEEE CDC (2008)**[skoge.folk.ntnu.no](https://skoge.folk.ntnu.no/prost/proceedings/cdc-2008/data/papers/1621.pdf) | DOI: [10.1109/CDC.2008.4739356](https://doi.org/10.1109/CDC.2008.4739356) | Moreno and Osorio gave the first Lyapunov‑based proof of finite‑time convergence for the super‑twisting algorithm. They proposed a Lyapunov function  $V(x)$  for the closed‑loop system (\\dot{x}\_1=-k\_1 | x\_1 |
| **R. Seeber & J. Horn – “Stability proof for a well‑established super‑twisting parameter setting,” _Automatica_, vol. 84, 2017, pp. 241–243**[tugraz.elsevierpure.com](https://tugraz.elsevierpure.com/ws/portalfiles/portal/23411198/Seeber_2017_Stability_Proof_for_a_Well_Established_Super_Twisting_Parameter_Setting.pdf#:~:text=rules%20have%20become%20very%20popular,16%5D%29.%20The)[tugraz.elsevierpure.com](https://tugraz.elsevierpure.com/ws/portalfiles/portal/23411198/Seeber_2017_Stability_Proof_for_a_Well_Established_Super_Twisting_Parameter_Setting.pdf#:~:text=Main%20Result%20Theorem%201,%E2%88%9A2k2) | DOI: [10.1016/j.automatica.2017.07.002](https://doi.org/10.1016/j.automatica.2017.07.002) | Seeber and Horn revisited the convergence conditions of the STA with disturbances ( | \\delta(t) |

**Summary**

These references collectively formalise the finite‑time convergence theorem for the super‑twisting algorithm. Levant’s original work shows that, under suitable bounds on uncertainties and sufficiently large gains  $\lambda$  and  $\alpha$ , the **super‑twisting controller produces a continuous control signal and drives both the sliding variable and its derivative to zero in finite time**[tau.ac.il](https://www.tau.ac.il/~levant/hosm2002.pdf#:~:text=The%20following%20controller%20does%20not,the%20initial%20value%20is%20inside). Moreno and Osorio constructed a Lyapunov function demonstrating finite‑time convergence for the standard STA and provided an explicit upper bound on the convergence time[skoge.folk.ntnu.no](https://skoge.folk.ntnu.no/prost/proceedings/cdc-2008/data/papers/1621.pdf); their framework also accommodates bounded perturbations by appropriately increasing the gains[skoge.folk.ntnu.no](https://skoge.folk.ntnu.no/prost/proceedings/cdc-2008/data/papers/1621.pdf#:~:text=Theorem%205%3A%20Suppose%20that%20the,%EF%AC%81nite%20time%20to%20the%20origin). Seeber and Horn later refined the parameter conditions, proving that the STA remains finite‑time stable when  $k_2$  exceeds the disturbance bound  $L$  and  $k_1$  exceeds  $\sqrt{k_2+L}$ , enabling lower gains and reduced chattering[tugraz.elsevierpure.com](https://tugraz.elsevierpure.com/ws/portalfiles/portal/23411198/Seeber_2017_Stability_Proof_for_a_Well_Established_Super_Twisting_Parameter_Setting.pdf#:~:text=Main%20Result%20Theorem%201,%E2%88%9A2k2).

---

## ChatGPT Replied:

Understood. I'll conduct detailed research on the finite-time convergence theorem of the Super-Twisting Algorithm as you described. I will focus on identifying and citing 2–3 authoritative sources that prove finite-time convergence to {s = 0, ṡ = 0}, outline the parameter conditions for λ and α, and provide Lyapunov analyses. Once I've gathered relevant sources, I'll provide full citations, DOIs/URLs, explanations of their contributions, and key parameter conditions. I'll begin this research now.

Worked for 9 minutes

Worked for 6 minutes

Here are key academic references that rigorously establish finite‑time convergence for the super‑twisting algorithm (STA). Each citation is accompanied by the theorem’s relevance and the conditions on the STA gains that guarantee convergence to the second‑order sliding set  $S^2=\{s=0,\dot{s}=0\}$ .

| Ref. (authors, publication & year) | DOI / URL | Relevance to finite‑time convergence | Key conditions on STA gains |
| --- | --- | --- | --- |
| **A. Levant – “Introduction to high‑order sliding modes” (chapter in _Variable Structure Systems_, 2002‑2003)**[tau.ac.il](https://www.tau.ac.il/~levant/hosm2002.pdf#:~:text=The%20following%20controller%20does%20not,the%20initial%20value%20is%20inside) | Preprint: [https://www.tau.ac.il/~levant/hosm2002.pdf](https://www.tau.ac.il/~levant/hosm2002.pdf) | Levant formulated the **super‑twisting controller** to remove chattering while guaranteeing a second‑order sliding mode. For the uncertain integrator  $\dot{x}=a(t)+b(t)u$ , he proposed the dynamic controller (u=-\\lambda | x |
| **J. A. Moreno & M. Osorio – “A Lyapunov approach to second‑order sliding mode controllers and observers,” 47th IEEE CDC (2008)**[skoge.folk.ntnu.no](https://skoge.folk.ntnu.no/prost/proceedings/cdc-2008/data/papers/1621.pdf) | DOI: [10.1109/CDC.2008.4739356](https://doi.org/10.1109/CDC.2008.4739356) | Moreno and Osorio gave the first Lyapunov‑based proof of finite‑time convergence for the super‑twisting algorithm. They proposed a Lyapunov function  $V(x)$  for the closed‑loop system (\\dot{x}\_1=-k\_1 | x\_1 |
| **R. Seeber & J. Horn – “Stability proof for a well‑established super‑twisting parameter setting,” _Automatica_, vol. 84, 2017, pp. 241–243**[tugraz.elsevierpure.com](https://tugraz.elsevierpure.com/ws/portalfiles/portal/23411198/Seeber_2017_Stability_Proof_for_a_Well_Established_Super_Twisting_Parameter_Setting.pdf#:~:text=rules%20have%20become%20very%20popular,16%5D%29.%20The)[tugraz.elsevierpure.com](https://tugraz.elsevierpure.com/ws/portalfiles/portal/23411198/Seeber_2017_Stability_Proof_for_a_Well_Established_Super_Twisting_Parameter_Setting.pdf#:~:text=Main%20Result%20Theorem%201,%E2%88%9A2k2) | DOI: [10.1016/j.automatica.2017.07.002](https://doi.org/10.1016/j.automatica.2017.07.002) | Seeber and Horn revisited the convergence conditions of the STA with disturbances ( | \\delta(t) |

**Summary**

These references collectively formalise the finite‑time convergence theorem for the super‑twisting algorithm. Levant’s original work shows that, under suitable bounds on uncertainties and sufficiently large gains  $\lambda$  and  $\alpha$ , the **super‑twisting controller produces a continuous control signal and drives both the sliding variable and its derivative to zero in finite time**[tau.ac.il](https://www.tau.ac.il/~levant/hosm2002.pdf#:~:text=The%20following%20controller%20does%20not,the%20initial%20value%20is%20inside). Moreno and Osorio constructed a Lyapunov function demonstrating finite‑time convergence for the standard STA and provided an explicit upper bound on the convergence time[skoge.folk.ntnu.no](https://skoge.folk.ntnu.no/prost/proceedings/cdc-2008/data/papers/1621.pdf); their framework also accommodates bounded perturbations by appropriately increasing the gains[skoge.folk.ntnu.no](https://skoge.folk.ntnu.no/prost/proceedings/cdc-2008/data/papers/1621.pdf#:~:text=Theorem%205%3A%20Suppose%20that%20the,%EF%AC%81nite%20time%20to%20the%20origin). Seeber and Horn later refined the parameter conditions, proving that the STA remains finite‑time stable when  $k_2$  exceeds the disturbance bound  $L$  and  $k_1$  exceeds  $\sqrt{k_2+L}$ , enabling lower gains and reduced chattering[tugraz.elsevierpure.com](https://tugraz.elsevierpure.com/ws/portalfiles/portal/23411198/Seeber_2017_Stability_Proof_for_a_Well_Established_Super_Twisting_Parameter_Setting.pdf#:~:text=Main%20Result%20Theorem%201,%E2%88%9A2k2).

---

