## You asked:

\# Citation Request: Adaptive Sliding Mode Control Law Properties I need academic citations for the properties and convergence theorem of adaptive sliding mode control. ## THEOREM STATEMENT "The adaptive control law ensures \[specific stability and adaptation properties\]." ## TECHNICAL CONTEXT \*\*Domain:\*\* Adaptive Sliding Mode Control for systems with unknown or time-varying uncertainties \*\*Motivation:\*\* Classical SMC requires knowing uncertainty bound ρ to set switching gain η > ρ. \*\*Problem:\*\* What if ρ is: - Unknown - Time-varying - Conservative estimates lead to excessive control effort/chattering \*\*Solution:\*\* Adaptive SMC adjusts gain online based on sliding variable magnitude. \*\*Adaptive SMC Structure:\*\* \*\*Classical SMC:\*\*

    u = u_eq - η·sgn(s)         (η constant, requires η > ρ)

\*\*Adaptive SMC:\*\*

    u = u_eq - η(t)·sgn(s)      (η(t) adapts online)
    η̇(t) = γ·|s|               (adaptation law)

Or with decay term:

    η̇(t) = γ·|s| - σ·η(t)      (γ > 0, σ ≥ 0)

Where: - η(t): time-varying switching gain - γ: adaptation rate (positive constant) - σ: decay rate (prevents η growing unbounded) - |s|: sliding variable magnitude \*\*Adaptive Law Rationale:\*\* When |s| is large (far from surface): - η̇ > 0: gain increases to accelerate reaching - Provides stronger control authority When |s| is small (near surface): - η̇ ≈ 0: gain stabilizes - Reduces chattering compared to conservative fixed gain \*\*Properties to Establish:\*\* 1. \*\*Stability:\*\* System remains stable despite adaptive gain 2. \*\*Convergence:\*\* s(t) → 0 as t → ∞ (or finite-time) 3. \*\*Bounded adaptation:\*\* η(t) remains bounded (doesn't grow to ∞) 4. \*\*Robustness:\*\* Works for uncertainties within some class 5. \*\*Chattering reduction:\*\* Lower average gain than conservative fixed-gain SMC ## THEOREM SIGNIFICANCE Adaptive SMC provides: - \*\*Automatic tuning:\*\* No need to know ρ precisely - \*\*Reduced conservatism:\*\* Gain adjusts to actual disturbance level - \*\*Better performance:\*\* Lower chattering + same robustness ## REQUIRED CITATIONS Find 2-3 papers that: 1. \*\*Establish stability and convergence\*\* of adaptive sliding mode control laws 2. \*\*Prove boundedness\*\* of adaptive gain η(t) 3. \*\*Provide adaptation law designs\*\* with mathematical analysis (Lyapunov or similar) \*\*Relevant works:\*\* - \*\*Slotine & Li (1987, 1991)\*\* - Adaptive sliding surface control - \*\*Sanner & Slotine (1992)\*\* - Gaussian networks for direct adaptive control - \*\*Plestan et al. (2010)\*\* - New methodologies for adaptive sliding mode control - \*\*Shtessel et al. (2014)\*\* - Sliding Mode Control and Observation, Chapter 6 ## OUTPUT FORMAT For each citation: 1. \*\*Full Citation:\*\* Authors, "Title," Journal/Conference, Year, Pages 2. \*\*DOI/URL:\*\* Link 3. \*\*Relevance:\*\* What properties (stability, convergence, boundedness) are proven? 4. \*\*Key Result:\*\* Adaptation law formula and convergence theorem statement ## FOCUS AREAS Essential topics: - Adaptive gain adjustment in SMC - Lyapunov-based adaptation laws - Boundedness proofs for adaptive parameters - Convergence analysis with time-varying gains - Chattering reduction via adaptation \*\*Distinguish from:\*\* - Fixed-gain SMC (classical approach) - Observer-based adaptive control (different architecture) - Parameter estimation methods (focus here is on gain adaptation) Provide rigorous citations establishing theoretical properties of adaptive sliding mode control laws.

---

## ChatGPT Replied:

Below are a few representative and fairly recent papers (and a book‐chapter) that rigorously analyze adaptive sliding mode (ASM) or adaptive gain SMC laws, along with a summary of their key contributions relative to your list of desired properties. You can pick and adapt (almost verbatim) theorem statements from these in your work (citing them properly).

* * *

Key References with Theoretical Guarantees
------------------------------------------

### 1\. Plestan, Shtessel, Brégeault & Poznyak (2010)

**Full Citation:**  
Franck Plestan, Yuri Shtessel, Vincent Brégeault, Alexander Poznyak, “New methodologies for adaptive sliding mode control,” _International Journal of Control_, Vol. 83, No. 9, 2010, pp. 1907–1919. DOI:10.1080/00207179.2010.501385 [ResearchGate+1](https://www.researchgate.net/publication/232896347_New_methodologies_for_adaptive_sliding_mode_control?utm_source=chatgpt.com)

**Relevance / Properties Proven:**

*   They propose **adaptive-gain sliding mode control laws** (i.e. gain  $K(t)$  varying) that do _not_ require prior knowledge of the bound on the uncertainties (only assuming boundedness). [ResearchGate+1](https://www.researchgate.net/publication/232896347_New_methodologies_for_adaptive_sliding_mode_control?utm_source=chatgpt.com)
    
*   They derive finite-time convergence to the sliding surface, while **preventing overestimation** of the switching gain. [ResearchGate+1](https://www.researchgate.net/publication/232896347_New_methodologies_for_adaptive_sliding_mode_control?utm_source=chatgpt.com)
    
*   They show **boundedness of adaptive gain**  $K(t)$  under reasonable assumptions (i.e. there exists a constant  $K^*$  such that  $K(t) \le K^*$ ) via a Lyapunov argument. [ResearchGate+1](https://www.researchgate.net/publication/232896347_New_methodologies_for_adaptive_sliding_mode_control?utm_source=chatgpt.com)
    

**Key Results / Adaptation Law & Theorem Sketch:**  
One of their adaptive laws is (for scalar sliding variable  $\sigma$ ):

$$
\dot K = \bar K_1 \,|\sigma|,\quad \text{when } \sigma \neq 0
$$

When  $\sigma = 0$ , a decay-law is used (but the details are more complex). [ResearchGate+1](https://www.researchgate.net/publication/232896347_New_methodologies_for_adaptive_sliding_mode_control?utm_source=chatgpt.com)

Theorem (informal, from their work): _Under their adaptation law, the sliding mode is reached in finite time and the gain  $K(t)$  remains bounded (i.e.\\ there exists  $K^*$ ) so long as uncertainties are bounded (even though their bound is not needed a priori)._ [ResearchGate+1](https://www.researchgate.net/publication/232896347_New_methodologies_for_adaptive_sliding_mode_control?utm_source=chatgpt.com)

They also discuss how once the system is in sliding mode, the gain can be decreased or adjusted rather than constantly growing (i.e. mitigating chattering). [ResearchGate+1](https://www.researchgate.net/publication/232896347_New_methodologies_for_adaptive_sliding_mode_control?utm_source=chatgpt.com)

* * *

### 2\. Roy, Baldi & Fridman (2020) — “On Adaptive Sliding Mode Control without a Priori Bounded Uncertainty”

**Full Citation:**  
Spandan Roy, Simone Baldi, Leonid M. Fridman, “On adaptive sliding mode control without a priori bounded uncertainty,” _Automatica_, Vol. 111, 2020, Art. No. 108650. DOI:10.1016/j.automatica.2019.108650 [TU Delft Research Portal+2TU Delft Research Portal+2](https://research.tudelft.nl/en/publications/on-adaptive-sliding-mode-control-without-a-priori-bounded-uncerta?utm_source=chatgpt.com)

**Relevance / Properties Proven:**

*   This work **relaxes the common assumption** that the uncertainty bound must be known a priori. They propose an ASM design that does _not_ require a known bound on the perturbation. [TU Delft Research Portal+2ScienceDirect+2](https://research.tudelft.nl/files/68885091/ASMC_new7_revised2.pdf?utm_source=chatgpt.com)
    
*   They prove **uniform ultimate boundedness** (UUB) of the tracking error (i.e.\\ sliding variable  $s$ ) under their adaptation law. [TU Delft Research Portal+1](https://research.tudelft.nl/en/publications/on-adaptive-sliding-mode-control-without-a-priori-bounded-uncerta?utm_source=chatgpt.com)
    
*   They also derive **boundedness of the switching gain** under mild assumptions (i.e.\\ even though there is no prior bound, the adaptive gain won’t grow unbounded indefinitely). [TU Delft Research Portal+2TU Delft Research Portal+2](https://research.tudelft.nl/en/publications/on-adaptive-sliding-mode-control-without-a-priori-bounded-uncerta?utm_source=chatgpt.com)
    

**Key Results / Adaptation Law & Theorem Sketch:**  
They consider a sliding variable  $s$  and define the control law  $u = u_{\rm eq} - K(t)\, \mathrm{sgn}(s)$  with adaptation:

$$
\dot K = \rho\, |s| - \sigma\, K
$$

for  $\rho>0$ ,  $\sigma>0$  (a decay term to prevent indefinite growth). (In some variants they allow  $\sigma = 0$ .) [TU Delft Research Portal+1](https://research.tudelft.nl/en/publications/on-adaptive-sliding-mode-control-without-a-priori-bounded-uncerta?utm_source=chatgpt.com)

Then they show via a Lyapunov candidate that  $s$  and  $K$  remain bounded, and that  $s$  converges to a compact small neighbourhood or to zero asymptotically under certain tuning. [TU Delft Research Portal+1](https://research.tudelft.nl/en/publications/on-adaptive-sliding-mode-control-without-a-priori-bounded-uncerta?utm_source=chatgpt.com)

They note that the adaptation error (between  $K$  and the “minimum required” gain) is bounded. [TU Delft Research Portal](https://research.tudelft.nl/en/publications/on-adaptive-sliding-mode-control-without-a-priori-bounded-uncerta?utm_source=chatgpt.com)

Thus their Theorem (informal):

> Under the proposed adaptive law, the closed-loop is semi-globally stable,  $s(t)$  is UUB, and  $K(t)$  remains bounded, without requiring a priori bound knowledge of the uncertainty.

* * *

### 3\. Liao, Pan, Borrelli & Hedrick (2018) — “Adaptive sliding mode control without knowledge of uncertainty bounds”

**Full Citation:**  
Yi-Wen Liao, Selina Pan, Francesco Borrelli & J. Karl Hedrick, “Adaptive sliding mode control without knowledge of uncertainty bounds,” arXiv preprint arXiv:1802.09689 (2018). (Later versions may appear in conferences/journals.) [arXiv+2ResearchGate+2](https://arxiv.org/abs/1802.09689?utm_source=chatgpt.com)

**Relevance / Properties Proven:**

*   They present an adaptation law that both **increases**  $K$  when  $|s|$  is large, and **decreases**  $K$  when  $|s|$  is in a specified small neighbourhood (i.e. dynamic adjustment).
    
*   They prove **semi-global stability**, boundedness of  $K(t)$ , and that  $s\to 0$  (or asymptotically small) under their design. [arXiv+2ResearchGate+2](https://arxiv.org/abs/1802.09689?utm_source=chatgpt.com)
    
*   They specifically emphasize **chattering reduction** by reducing switching gain when  $|s|$  is small. [arXiv+1](https://arxiv.org/abs/1802.09689?utm_source=chatgpt.com)
    

**Key Results / Adaptation Law & Theorem Sketch:**  
One adaptation rule they propose is of the form:

$$
\dot{\hat\mu} = \frac{\Psi(s)}{\rho}
$$

where  $\Psi(s)$  is a specially chosen function (positive when outside a band, negative inside) that modulates gain increase/decrease. [arXiv+1](https://arxiv.org/abs/1802.09689?utm_source=chatgpt.com)

They define a Lyapunov function  $V(s, \hat\mu)$  and show  $\dot V \le 0$  and hence boundedness. The result is that  $s$  is bounded and converges to a small region, and  $\hat\mu$  (the adaptive gain estimate) remains bounded. [arXiv+1](https://arxiv.org/abs/1802.09689?utm_source=chatgpt.com)

Thus their convergence theorem is along the lines: _Given the adaptation law, the system trajectories are stable,  $s(t)$  converges to a neighborhood of zero, adaptation gain  $\hat\mu(t)$  remains bounded, and chattering is reduced compared to fixed-gain SMC._ [arXiv+1](https://arxiv.org/abs/1802.09689?utm_source=chatgpt.com)

* * *

### 4\. Utkin & Poznyak (book chapter) — _Adaptive Sliding Mode Control_

**Full Citation:**  
V. I. Utkin & A. S. Poznyak, “Adaptive Sliding Mode Control,” in _Advances in Sliding Mode Control_, Lecture Notes in Control and Information Sciences, Vol. 440, Springer, 2012, pp. 21–53. [SpringerLink+1](https://link.springer.com/chapter/10.1007/978-3-642-36986-5_2?utm_source=chatgpt.com)

**Relevance / Properties Proven:**

*   This chapter provides a systematic overview of adaptation strategies in sliding mode control, including the so-called **σ-adaptation** (adjusting the gain during reaching) and **dynamic adaptation within sliding mode**, using equivalent control ideas. [SpringerLink+1](https://link.springer.com/chapter/10.1007/978-3-642-36986-5_2?utm_source=chatgpt.com)
    
*   It discusses how adaptive SMC can achieve the **minimum necessary discontinuous control amplitude** while preserving finite-time convergence. [SpringerLink](https://link.springer.com/chapter/10.1007/978-3-642-36986-5_2?utm_source=chatgpt.com)
    
*   It gives insight into chattering mitigation via adaptation and the trade-off between performance and robustness. [SpringerLink+1](https://link.springer.com/chapter/10.1007/978-3-642-36986-5_2?utm_source=chatgpt.com)
    

**Key Results / Adaptation Law & Theorem Sketch:**  
Utkin & Poznyak discuss adaptation laws of these types:

*   **σ-adaptation (reaching phase):**  $\dot{\eta} = \gamma |s|$ , analogous to your simple law, ensuring the gain increases until sliding is achieved
    
*   **Dynamic (on-surface) adaptation:** after sliding starts, use the equivalent control estimate to further reduce the gain toward its minimum needed value.
    

They argue that under such adaptation, one can still guarantee **finite-time convergence** to the sliding surface and maintain robustness, while reducing excessive control amplitude. [SpringerLink](https://link.springer.com/chapter/10.1007/978-3-642-36986-5_2?utm_source=chatgpt.com)

* * *

Suggested Theorem Statement (Template) with Supporting Citations
----------------------------------------------------------------

Here is a template for your theorem (you can adapt the precise constants and assumptions) and a “proof sketch” aligned with the above references:

> **Theorem (Adaptive SMC Stability & Convergence).**  
> Consider a nonlinear system with matched uncertainty:
> 
> $$
> \dot x = f(x,t) + b(x,t)\,u + d(x,t),
> $$
> 
> define the sliding variable  $s = \sigma(x)$ . Suppose  $d(x,t)$  is _unknown but bounded_. Use the control law:
> 
> $$
> u = u_{\rm eq}(x) - \eta(t)\,\sgn(s),
> $$
> 
> with adaptation law
> 
> $$
> \dot \eta = \gamma \,|s| - \sigma\,\eta \quad (\gamma > 0,\; \sigma \ge 0).
> $$
> 
> **Then**, under suitable smoothness and matching assumptions and appropriate tuning of  $\gamma, \sigma$ ,
> 
> 1.  All closed-loop signals remain bounded (i.e.\\  $x, s, \eta$  are bounded).
>     
> 2.  The sliding variable  $s(t)$  converges to zero (or to a small residual neighborhood) as  $t\to\infty.$ 
>     
> 3.  The adaptive gain  $\eta(t)$  remains bounded and does not overgrow beyond what is required (i.e.\\ no unbounded growth).
>     
> 4.  The adaptation reduces chattering compared to a conservative fixed gain, because  $\eta$  can decrease when  $|s|$  is small.
>     
> 
> (Variants: one can also get finite-time convergence to sliding, or uniform reaching time, under stronger adaptation laws.)

You can cite **Plestan et al. (2010)** for finite-time convergence and boundedness of gain in adaptive sliding mode laws. You can cite **Roy et al. (2020)** for a version without needing an a priori bound on the uncertainty and uniform ultimate boundedness. You can cite **Utkin & Poznyak (2012)** for general adaptation methodologies and minimal amplitude claims.

* * *

If you like, I can find a more recent, tight “textbook style” proof that uses exactly your form  $\dot\eta = \gamma|s| - \sigma \eta$  and restate a full theorem (with all constant bounds) — would you like me to do that?

---

