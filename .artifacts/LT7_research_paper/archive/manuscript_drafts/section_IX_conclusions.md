# IX. CONCLUSIONS

This paper presented a PSO-optimized adaptive boundary layer approach for sliding mode control chattering mitigation in double inverted pendulum systems. We provide a summary of contributions, acknowledge limitations, and outline future research directions.

## A. Summary of Contributions

This work makes three primary contributions to the sliding mode control literature:

**1. PSO-Optimized Adaptive Boundary Layer with Chattering-Weighted Fitness**

We introduced an adaptive boundary layer mechanism $\epsilon_{\text{eff}} = \epsilon_{\min} + \alpha|\dot{s}|$ that dynamically adjusts based on sliding surface derivative magnitude, and optimized the parameters $(\epsilon_{\min}, \alpha)$ using Particle Swarm Optimization with a novel chattering-weighted fitness function ($F = 0.70 \cdot C + 0.15 \cdot T_s + 0.15 \cdot O$). Experimental validation over 100 Monte Carlo trials demonstrated **66.5% chattering reduction** (6.37 → 2.14, $p < 0.001$, Cohen's $d = 5.29$) with **zero energy penalty** ($p = 0.339$) compared to fixed boundary layer SMC. This very large effect size represents a substantial advancement over prior heuristic adaptive boundary layer methods.

**2. Lyapunov Stability Analysis for Time-Varying Boundary Layer**

We provided rigorous theoretical guarantees via Lyapunov's direct method, proving that the adaptive boundary layer preserves finite-time convergence to the sliding surface under standard assumptions (matched disturbances, switching gain dominance $K > \bar{d}$, controllability, positive gains). The key theoretical result is **Theorem 1**, establishing reaching time bounded by $t_{\text{reach}} \leq \sqrt{2}|s(0)|/(\beta\eta)$ independent of the time-varying $\epsilon_{\text{eff}}$. This addresses the theoretical gap in existing adaptive boundary layer literature, which lacked Lyapunov proofs for dynamic boundary thickness.

**3. Honest Reporting of Generalization and Disturbance Rejection Failures**

Through systematic stress testing, we identified and quantified critical limitations:
- **Generalization failure** (MT-7): PSO parameters optimized for ±0.05 rad initial conditions exhibited **50.4× chattering degradation** (2.14 → 107.61) and **90.2% failure rate** (49/500 successful trials) when tested under ±0.3 rad initial conditions, revealing severe overfitting to the narrow training distribution.
- **Disturbance rejection failure** (MT-8): All controllers achieved **0% convergence** under external disturbances (10 N step, 30 N·s impulse, 8 N sinusoidal), demonstrating brittleness when fitness optimization ignores robustness scenarios.

These negative results, rarely reported in the SMC literature, provide actionable insights for future robust optimization research and establish best practices for multi-scenario validation.

## B. Acknowledged Limitations

This work has five primary limitations that contextualize the findings:

**1. Single-Scenario PSO Optimization**

The PSO algorithm optimized parameters exclusively on initial conditions sampled from $\mathcal{U}(-0.05, 0.05)$ rad without disturbance scenarios. This narrow training distribution (representing only ~17% of the ±0.3 rad operating range) caused catastrophic generalization failure. Multi-scenario robust PSO (Section VIII-D) is required for practical deployment.

**2. Simulation-Only Validation**

All results are based on numerical simulation of the nonlinear DIP model using 4th-order Runge-Kutta integration. Real-world hardware exhibits unmodeled dynamics (friction, backlash, flexible modes, sensor noise) that may degrade performance. Hardware validation on a physical DIP system is necessary to confirm simulation findings and identify any simulation-to-reality gap.

**3. Classical SMC Without Integral Action**

The classical SMC structure lacks integral sliding surface, preventing rejection of constant disturbances (evidenced by MT-8's 0% convergence). Integral Sliding Mode Control (ISMC) with PSO-optimized gains would address this limitation but requires additional parameter tuning (integral gain $k_I$).

**4. Fixed Sliding Surface Gains**

While the adaptive boundary layer parameters $(\epsilon_{\min}, \alpha)$ were optimized via PSO, the sliding surface gains $(k_1, k_2, \lambda_1, \lambda_2)$ and switching gain $K$ were manually selected. Joint optimization of all parameters (7-dimensional search space) may further improve performance but increases computational cost (~10× more function evaluations).

**5. System-Specific Results**

The optimized parameters $\epsilon_{\min}^* = 0.0025$ and $\alpha^* = 1.21$ are tailored to the specific DIP configuration (cart mass 1 kg, link masses 0.1 kg, lengths 0.5 m). Transferring these parameters to systems with different mass ratios, lengths, or actuator limits requires re-optimization. However, the PSO methodology itself is transferable.

## C. Future Research Directions

We propose five concrete research directions to address the identified limitations and advance robust SMC design:

**1. Multi-Scenario Robust PSO (High Priority)**

Extend the PSO fitness function to include diverse initial condition distributions (e.g., $\mathcal{U}(-0.3, 0.3)$ rad) and disturbance scenarios (step, impulse, sinusoidal forces) during optimization. Implement minimax fitness $F_{\text{robust}} = \max_{\text{scenario}} F_i$ to optimize worst-case performance rather than average-case. Expected outcome: Parameters that generalize beyond training distribution with graceful degradation rather than catastrophic failure.

**2. Disturbance-Aware Fitness Function (High Priority)**

Redesign the fitness function to explicitly weight disturbance rejection:
```latex
F_{\text{robust}} = 0.50 \cdot C_{\text{nominal}} + 0.20 \cdot C_{\text{disturbed}} + 0.15 \cdot T_s + 0.15 \cdot O
```
where $C_{\text{disturbed}}$ measures chattering/recovery performance under external perturbations. This ensures optimized parameters balance nominal chattering reduction with robustness.

**3. Integral SMC with Joint Parameter Optimization (Medium Priority)**

Incorporate integral sliding surface $s = e + \lambda e + k_I \int e \, dt$ to enable disturbance rejection, and jointly optimize all parameters $(k_1, k_2, \lambda_1, \lambda_2, k_I, K, \epsilon_{\min}, \alpha)$ using PSO with disturbance-aware fitness. Expected outcome: Zero steady-state error under constant disturbances while preserving chattering reduction.

**4. Hardware Validation on Physical DIP (High Priority)**

Implement the PSO-optimized controller on a real-world DIP experimental setup (e.g., Quanser rotary inverted pendulum, custom-built DIP platform) to validate simulation results. Measure actual chattering using accelerometers, test under same initial condition distributions (±0.05 rad, ±0.3 rad), and identify any simulation-to-reality gap requiring model refinement or adaptive online tuning.

**5. Transfer to Other Underactuated Systems (Low Priority)**

Apply the PSO-optimized adaptive boundary layer methodology to other underactuated systems: single inverted pendulum, cart-pole, quadrotor, robotic manipulator. Investigate transferability of the chattering-weighted fitness function (70-15-15) and adaptive boundary layer formula across different system dynamics. This would establish generalizability of the approach beyond the DIP benchmark.

## D. Closing Remarks

This work demonstrates that PSO-optimized adaptive boundary layers can achieve dramatic chattering reduction (66.5%) for nominal operating conditions, but single-scenario optimization produces brittle controllers that fail catastrophically (50.4× degradation) outside the training distribution. These findings motivate two important shifts in SMC research practices:

**1. Robust Multi-Scenario Optimization:** Future controller optimization must include diverse operating conditions (initial conditions, disturbances, parameter variations) during fitness evaluation to ensure generalization beyond the training domain.

**2. Honest Validation and Reporting:** The SMC community should establish rigorous validation protocols that test controllers significantly beyond their training distributions and transparently report both successes and failures. Negative results provide valuable insights for future research and prevent repetition of the same limitations.

By combining systematic optimization, rigorous stability analysis, multi-scenario validation, and honest reporting of limitations, this work advances the practical deployment of sliding mode control in industrial mechatronic systems and establishes methodological best practices for future robust controller design.

---

**Final Word Count:** Approximately 6,000 words (Introduction through Conclusions)

**Reproducibility:** All simulation code, data, and analysis scripts are available at [GitHub repository URL to be added].

**Acknowledgments:** [To be added during final manuscript preparation]
