## You asked:

\# Citation Request: PSO Particle Convergence Conditions I need academic citations for the convergence theorem of individual particles in Particle Swarm Optimization. ## THEOREM STATEMENT "The particle converges to a stable trajectory if \[specific convergence conditions are met\]." ## TECHNICAL CONTEXT \*\*Domain:\*\* Convergence analysis of Particle Swarm Optimization algorithm \*\*PSO Algorithm Basics:\*\* \*\*Velocity Update:\*\*

    v_i(t+1) = ω·v_i(t) + c₁·r₁·(p_i - x_i(t)) + c₂·r₂·(p_g - x_i(t))

\*\*Position Update:\*\*

    x_i(t+1) = x_i(t) + v_i(t+1)

Where: - x\_i: position of particle i - v\_i: velocity of particle i - p\_i: personal best position - p\_g: global best position - ω: inertia weight - c₁, c₂: cognitive and social coefficients - r₁, r₂: random numbers in \[0,1\] \*\*Convergence Concept:\*\* - Particle trajectory: sequence {x\_i(t), v\_i(t)} over time - Stable trajectory: bounded motion, doesn't diverge to infinity - Conditions typically involve relationships between ω, c₁, c₂ \*\*What the Theorem Establishes:\*\* Mathematical conditions on PSO parameters (inertia weight, acceleration coefficients) that guarantee particles don't exhibit explosive divergence. This is fundamental for PSO to explore search space effectively without instability. ## REQUIRED CITATIONS Find 2-3 seminal papers that: 1. \*\*Derive convergence conditions\*\* for PSO particle dynamics (mathematical analysis, not just empirical) 2. \*\*Establish stability regions\*\* in PSO parameter space (ω, c₁, c₂) 3. \*\*Prove trajectory boundedness\*\* or convergence theorems for individual particles \*\*Prefer papers with:\*\* - Rigorous mathematical analysis (differential equations, Lyapunov methods, linear systems theory) - Explicit parameter bounds for stability (e.g., "if ω < 1 and c₁ + c₂ < 4, then...") - Proofs of convergence or stability (not just simulation observations) ## OUTPUT FORMAT For each citation: 1. \*\*Full Citation:\*\* Authors, "Title," Venue, Year 2. \*\*DOI/URL:\*\* Link to paper 3. \*\*Relevance:\*\* What convergence conditions or stability bounds does this paper establish? 4. \*\*Key Result:\*\* Specific theorem, equation, or parameter bounds (e.g., "ω ∈ \[0.4, 0.9\]") ## FOCUS AREAS Seminal works on PSO theory: - \*\*Clerc & Kennedy (2002):\*\* Constriction coefficient analysis - \*\*Van den Bergh (2002):\*\* Convergence analysis Ph.D. thesis - \*\*Trelea (2003):\*\* Stability and convergence analysis - \*\*Jiang et al. (2007):\*\* Stochastic convergence analysis \*\*Mathematical approaches:\*\* - Order-1 and order-2 stability analysis - Lyapunov stability of PSO dynamics - Stochastic convergence theorems - Linear system stability for particle motion Provide citations that rigorously establish when PSO particles converge to stable trajectories.

---

## ChatGPT Replied:

Understood. I will research and identify 2-3 seminal papers that provide rigorous mathematical analysis on the convergence conditions and stability regions of Particle Swarm Optimization (PSO) particles. I will provide each citation with full details, a DOI or URL, and explain their relevance and key results regarding parameter bounds. I’ll return once this comprehensive list is prepared.

Worked for 11 minutes

Here are academic sources that provide rigorous convergence conditions for individual particles in Particle Swarm Optimization (PSO). Each reference derives parameter bounds (inertia weight and acceleration coefficients) under which a particle’s trajectory is stable or convergent.

### 1\. **Trelea, Ioan Cristian (2003). “The Particle Swarm Optimization Algorithm: Convergence Analysis and Parameter Selection,” _Information Processing Letters_ 85(6): 317–325.**

*   **DOI/URL:** [10.1016/S0020‑0190(02)00447‑7](https://doi.org/10.1016/S0020-0190\(02\)00447-7)
    
*   **Relevance:** Trelea studied a deterministic PSO model by setting the random factors in the velocity update to their means. The paper treated the particle’s motion as a linear system and derived exact conditions for the stability of its equilibrium point.
    
*   **Key result (convergence region):** Let  $a$  be the inertia weight (coefficient multiplying the previous velocity) and  $b=b_1+b_2$  be the sum of the cognitive and social coefficients. Trelea showed that the equilibrium point is stable if and only if the characteristic polynomial’s roots lie inside the unit circle. This leads to the triangular convergence region
    
    $$
     a<1,\qquad b>0,\qquad 2a-b+2>0 .
    $$
    
    When these three inequalities hold, the particle’s trajectory converges to a finite equilibrium; violating them leads to divergent motion or oscillations[par.cse.nsysu.edu.tw](https://par.cse.nsysu.edu.tw/resource/paper/2007/070620/The%20particle%20swarm%20optimization%20algorithm-%20convergence%20analysis%20and%20parameter%20selection.pdf#:~:text=The%20necessary%20and%20suf%EF%AC%81cient%20condition,are%20selected%20inside%20this%20triangle). The paper further explains that parameter pairs near the center of this triangular region produce faster convergence, while those near the boundaries lead to slower oscillatory convergence[par.cse.nsysu.edu.tw](https://par.cse.nsysu.edu.tw/resource/paper/2007/070620/The%20particle%20swarm%20optimization%20algorithm-%20convergence%20analysis%20and%20parameter%20selection.pdf).
    

### 2\. **van den Bergh, Frans (2001). _An Analysis of Particle Swarm Optimizers_, Ph.D. thesis, University of Pretoria.**

*   **URL:** University of Pretoria repository
    
*   **Relevance:** This thesis synthesizes earlier work by Clerc & Kennedy (2002) on the constriction factor. It reformulates the PSO velocity update using a constriction coefficient  $\chi$  that ensures stability without explicit velocity clamping and derives the parameter relation used in practice.
    
*   **Key result (constriction factor conditions):** In the constricted PSO, the velocity update takes the form
    
    $$
     v_{i,j}(t+1) = \chi\Bigl[v_{i,j}(t)+c_1\,r_1\,\bigl(p_i-x_i(t)\bigr)+c_2\,r_2\,\bigl(p_g-x_i(t)\bigr)\Bigr],
    $$
    
    where  $\chi$  is the constriction coefficient and  $\phi=c_1+c_2$ . van den Bergh’s thesis cites the constriction analysis showing that stable trajectories require  $\phi > 4$ , and  $\chi$  is given by
    
    $$
     \chi=\frac{2}{\,\phi-2+\sqrt{\phi^2-4\phi}\,}\quad \text{with }\phi>4.
    $$
    
    For example, choosing  $c_1=c_2=2.05$  gives  $\phi=4.1$  and  $\chi\approx 0.7298$ . Multiplying  $\chi$  by the acceleration coefficients yields effective coefficients  $\chi c_1=\chi c_2\approx 1.4962$  and inertia weight  $w=\chi\approx0.7298$ , which ensure that the particle’s velocity decays and the trajectory converges[bee22.com](https://bee22.com/resources/Bergh%202006.pdf#:~:text=vi%2Cj,%E2%88%92%CF%95%20%E2%88%92%20p%20%CF%952%20%E2%88%924%CF%95). The thesis notes that using this constriction factor often outperforms simple velocity clamping and avoids “particle explosion”[bee22.com](https://bee22.com/resources/Bergh%202006.pdf#:~:text=Eberhart%20and%20Shi%20compared%20the,This%20led%20to%20improved%20performance).
    

### 3\. **Gopal, Anshul; Sultani, Mohammad Mahdi; Bansal, Jagdish Chand (2019). “On Stability Analysis of Particle Swarm Optimization Algorithm,” _Arabian Journal for Science and Engineering_ 45: 2385–2394.**

*   **DOI/URL:** [10.1007/s13369‑019‑03991‑8](https://doi.org/10.1007/s13369-019-03991-8)
    
*   **Relevance:** The authors applied the von Neumann stability criterion to the PSO update equations (treated as finite‐difference schemes) and derived simple bounds on the acceleration coefficients and inertia or constriction parameters that guarantee stability.
    
*   **Key result (inertia and constriction bounds):** For the standard PSO with inertia weight  $w$ , the analysis shows that the magnitude of the amplification factors remains ≤ 1 only when the sum of acceleration coefficients  $c_1+c_2$  satisfies
    
    $$
     0\;\le\;c_1+c_2\;\le\;2(1+w).
    $$
    
    Thus, with an inertial weight  $w\in[-1,1]$ , stable trajectories require the acceleration coefficients to lie in this interval[people.sau.int](https://people.sau.int/~jcbansal/uploads/Gopal2020_Article_OnStabilityAnalysisOfParticleS_\(1\).pdf#:~:text=From%20Eqs,%2824). When the PSO is rewritten using the constriction factor  $\chi$ , the stability criterion becomes
    
    $$
     0\;\le\;c_1+c_2\;\le\;2\Bigl(1+\frac{1}{\chi}\Bigr)\quad (\chi\neq 0).
    $$
    
    In other words,  $c_1+c_2$  must not exceed  $2(1+1/\chi)$ [people.sau.int](https://people.sau.int/~jcbansal/uploads/Gopal2020_Article_OnStabilityAnalysisOfParticleS_\(1\).pdf#:~:text=From%20Eqs,values%20of%20parameters%20c1%2C%20c2). These inequalities provide explicit parameter ranges for practitioners: lower acceleration coefficients ensure stable, bounded particle trajectories, whereas larger coefficients risk divergence or oscillatory behavior.
    

### Other theoretical stability results

While the above three sources are seminal, subsequent studies expanded the convergence regions. For example, Cleghorn & Engelbrecht showed that, under a weak chaotic assumption, canonical PSO is order‑1 and order‑2 stable when  $c_1+c_2<2(1+w)$ ,  $c_1,c_2>0$  and  $-1<w<1$ [repository.up.ac.za](https://repository.up.ac.za/bitstreams/d4b250af-d715-44a9-903a-b6d715492e4f/download#:~:text=particle%20convergence%20in%20the%20CPSO,1%2C%20%2815). Kadirkamanathan et al. used Lyapunov stability to obtain piecewise bounds on  $c_1+c_2$  depending on  $w$ [repository.up.ac.za](https://repository.up.ac.za/bitstreams/d4b250af-d715-44a9-903a-b6d715492e4f/download#:~:text=the%20following%20region%20for%20particle,0%2C%201%29), and Poli & Broomhead derived a curved stability boundary  $c_1+c_2<24\,(1-w^2)/(7-5w)$ [repository.up.ac.za](https://repository.up.ac.za/bitstreams/d4b250af-d715-44a9-903a-b6d715492e4f/download#:~:text=Lastly%2C%20without%20the%20use%20of,%E2%88%921%2C%201%5D%20.%20%2818). These later results refine but do not contradict the early analyses; in practice, choosing parameters inside the smallest of these regions ensures that each particle converges to a bounded trajectory rather than diverging.

These citations collectively demonstrate that PSO particles converge to stable trajectories when the inertia and acceleration parameters satisfy specific mathematical bounds. Selecting parameters outside these regions risks instability or oscillations, while parameter values inside the regions promote convergence.

---

## ChatGPT Replied:

Understood. I will research and identify 2-3 seminal papers that provide rigorous mathematical analysis on the convergence conditions and stability regions of Particle Swarm Optimization (PSO) particles. I will provide each citation with full details, a DOI or URL, and explain their relevance and key results regarding parameter bounds. I’ll return once this comprehensive list is prepared.

Worked for 11 minutes

Here are academic sources that provide rigorous convergence conditions for individual particles in Particle Swarm Optimization (PSO). Each reference derives parameter bounds (inertia weight and acceleration coefficients) under which a particle’s trajectory is stable or convergent.

### 1\. **Trelea, Ioan Cristian (2003). “The Particle Swarm Optimization Algorithm: Convergence Analysis and Parameter Selection,” _Information Processing Letters_ 85(6): 317–325.**

*   **DOI/URL:** [10.1016/S0020‑0190(02)00447‑7](https://doi.org/10.1016/S0020-0190\(02\)00447-7)
    
*   **Relevance:** Trelea studied a deterministic PSO model by setting the random factors in the velocity update to their means. The paper treated the particle’s motion as a linear system and derived exact conditions for the stability of its equilibrium point.
    
*   **Key result (convergence region):** Let  $a$  be the inertia weight (coefficient multiplying the previous velocity) and  $b=b_1+b_2$  be the sum of the cognitive and social coefficients. Trelea showed that the equilibrium point is stable if and only if the characteristic polynomial’s roots lie inside the unit circle. This leads to the triangular convergence region
    
    $$
     a<1,\qquad b>0,\qquad 2a-b+2>0 .
    $$
    
    When these three inequalities hold, the particle’s trajectory converges to a finite equilibrium; violating them leads to divergent motion or oscillations[par.cse.nsysu.edu.tw](https://par.cse.nsysu.edu.tw/resource/paper/2007/070620/The%20particle%20swarm%20optimization%20algorithm-%20convergence%20analysis%20and%20parameter%20selection.pdf#:~:text=The%20necessary%20and%20suf%EF%AC%81cient%20condition,are%20selected%20inside%20this%20triangle). The paper further explains that parameter pairs near the center of this triangular region produce faster convergence, while those near the boundaries lead to slower oscillatory convergence[par.cse.nsysu.edu.tw](https://par.cse.nsysu.edu.tw/resource/paper/2007/070620/The%20particle%20swarm%20optimization%20algorithm-%20convergence%20analysis%20and%20parameter%20selection.pdf).
    

### 2\. **van den Bergh, Frans (2001). _An Analysis of Particle Swarm Optimizers_, Ph.D. thesis, University of Pretoria.**

*   **URL:** University of Pretoria repository
    
*   **Relevance:** This thesis synthesizes earlier work by Clerc & Kennedy (2002) on the constriction factor. It reformulates the PSO velocity update using a constriction coefficient  $\chi$  that ensures stability without explicit velocity clamping and derives the parameter relation used in practice.
    
*   **Key result (constriction factor conditions):** In the constricted PSO, the velocity update takes the form
    
    $$
     v_{i,j}(t+1) = \chi\Bigl[v_{i,j}(t)+c_1\,r_1\,\bigl(p_i-x_i(t)\bigr)+c_2\,r_2\,\bigl(p_g-x_i(t)\bigr)\Bigr],
    $$
    
    where  $\chi$  is the constriction coefficient and  $\phi=c_1+c_2$ . van den Bergh’s thesis cites the constriction analysis showing that stable trajectories require  $\phi > 4$ , and  $\chi$  is given by
    
    $$
     \chi=\frac{2}{\,\phi-2+\sqrt{\phi^2-4\phi}\,}\quad \text{with }\phi>4.
    $$
    
    For example, choosing  $c_1=c_2=2.05$  gives  $\phi=4.1$  and  $\chi\approx 0.7298$ . Multiplying  $\chi$  by the acceleration coefficients yields effective coefficients  $\chi c_1=\chi c_2\approx 1.4962$  and inertia weight  $w=\chi\approx0.7298$ , which ensure that the particle’s velocity decays and the trajectory converges[bee22.com](https://bee22.com/resources/Bergh%202006.pdf#:~:text=vi%2Cj,%E2%88%92%CF%95%20%E2%88%92%20p%20%CF%952%20%E2%88%924%CF%95). The thesis notes that using this constriction factor often outperforms simple velocity clamping and avoids “particle explosion”[bee22.com](https://bee22.com/resources/Bergh%202006.pdf#:~:text=Eberhart%20and%20Shi%20compared%20the,This%20led%20to%20improved%20performance).
    

### 3\. **Gopal, Anshul; Sultani, Mohammad Mahdi; Bansal, Jagdish Chand (2019). “On Stability Analysis of Particle Swarm Optimization Algorithm,” _Arabian Journal for Science and Engineering_ 45: 2385–2394.**

*   **DOI/URL:** [10.1007/s13369‑019‑03991‑8](https://doi.org/10.1007/s13369-019-03991-8)
    
*   **Relevance:** The authors applied the von Neumann stability criterion to the PSO update equations (treated as finite‐difference schemes) and derived simple bounds on the acceleration coefficients and inertia or constriction parameters that guarantee stability.
    
*   **Key result (inertia and constriction bounds):** For the standard PSO with inertia weight  $w$ , the analysis shows that the magnitude of the amplification factors remains ≤ 1 only when the sum of acceleration coefficients  $c_1+c_2$  satisfies
    
    $$
     0\;\le\;c_1+c_2\;\le\;2(1+w).
    $$
    
    Thus, with an inertial weight  $w\in[-1,1]$ , stable trajectories require the acceleration coefficients to lie in this interval[people.sau.int](https://people.sau.int/~jcbansal/uploads/Gopal2020_Article_OnStabilityAnalysisOfParticleS_\(1\).pdf#:~:text=From%20Eqs,%2824). When the PSO is rewritten using the constriction factor  $\chi$ , the stability criterion becomes
    
    $$
     0\;\le\;c_1+c_2\;\le\;2\Bigl(1+\frac{1}{\chi}\Bigr)\quad (\chi\neq 0).
    $$
    
    In other words,  $c_1+c_2$  must not exceed  $2(1+1/\chi)$ [people.sau.int](https://people.sau.int/~jcbansal/uploads/Gopal2020_Article_OnStabilityAnalysisOfParticleS_\(1\).pdf#:~:text=From%20Eqs,values%20of%20parameters%20c1%2C%20c2). These inequalities provide explicit parameter ranges for practitioners: lower acceleration coefficients ensure stable, bounded particle trajectories, whereas larger coefficients risk divergence or oscillatory behavior.
    

### Other theoretical stability results

While the above three sources are seminal, subsequent studies expanded the convergence regions. For example, Cleghorn & Engelbrecht showed that, under a weak chaotic assumption, canonical PSO is order‑1 and order‑2 stable when  $c_1+c_2<2(1+w)$ ,  $c_1,c_2>0$  and  $-1<w<1$ [repository.up.ac.za](https://repository.up.ac.za/bitstreams/d4b250af-d715-44a9-903a-b6d715492e4f/download#:~:text=particle%20convergence%20in%20the%20CPSO,1%2C%20%2815). Kadirkamanathan et al. used Lyapunov stability to obtain piecewise bounds on  $c_1+c_2$  depending on  $w$ [repository.up.ac.za](https://repository.up.ac.za/bitstreams/d4b250af-d715-44a9-903a-b6d715492e4f/download#:~:text=the%20following%20region%20for%20particle,0%2C%201%29), and Poli & Broomhead derived a curved stability boundary  $c_1+c_2<24\,(1-w^2)/(7-5w)$ [repository.up.ac.za](https://repository.up.ac.za/bitstreams/d4b250af-d715-44a9-903a-b6d715492e4f/download#:~:text=Lastly%2C%20without%20the%20use%20of,%E2%88%921%2C%201%5D%20.%20%2818). These later results refine but do not contradict the early analyses; in practice, choosing parameters inside the smallest of these regions ensures that each particle converges to a bounded trajectory rather than diverging.

These citations collectively demonstrate that PSO particles converge to stable trajectories when the inertia and acceleration parameters satisfy specific mathematical bounds. Selecting parameters outside these regions risks instability or oscillations, while parameter values inside the regions promote convergence.

---

