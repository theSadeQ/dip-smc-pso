# VIII. DISCUSSION

This section interprets the experimental results from Section VII, compares our findings to the state-of-the-art literature (Section II), analyzes the root causes of generalization and disturbance rejection failures, proposes solutions for future work, and discusses broader implications for the sliding mode control community.

## A. Interpretation of Adaptive Boundary Layer Success

The MT-6 results demonstrate that PSO-optimized adaptive boundary layer parameters achieve **66.5% chattering reduction** (6.37 → 2.14, p < 0.001, Cohen's d = 5.29) with **zero energy penalty** (p = 0.339) compared to fixed boundary layer SMC. This represents a substantial advancement over recent literature.

### 1) Comparison with State-of-the-Art

Our chattering reduction compares favorably to recent approaches reviewed in Section II:

- **Fuzzy-adaptive methods** (Frontiers 2024, SFA-SMC 2024) report qualitative chattering mitigation but lack quantitative metrics. Our 66.5% reduction provides a concrete benchmark with statistical significance (p < 0.001).

- **Higher-order SMC** (Ayinalem et al. 2025, HEPSO-SMC 2025) achieve smooth control through integral action at the cost of increased complexity (additional state variables, observers). Our adaptive boundary layer maintains first-order SMC simplicity while achieving comparable chattering reduction through systematic PSO optimization.

- **Hybrid frameworks** (Scientific Reports 2024: Fuzzy + SMC) demonstrate chattering reduction but require extensive domain expertise for fuzzy rule design. Our PSO approach automates parameter selection, making the methodology transferable to other systems without manual tuning.

**Key Distinction:** We are the first to report effect size (Cohen's d = 5.29), indicating the chattering reduction is not only statistically significant but also profoundly meaningful in practice. This "very large" effect size (d > 0.8 by Cohen's conventions) suggests the adaptive boundary layer fundamentally alters control behavior, not merely provides marginal improvement.

### 2) Mechanism Analysis

The 66.5% chattering reduction stems from three complementary mechanisms:

**a) Dynamic Adaptation to System State:**
The formula $\epsilon_{\text{eff}} = \epsilon_{\min} + \alpha|\dot{s}|$ automatically adjusts boundary layer thickness based on sliding surface derivative magnitude. During the reaching phase (large $|\dot{s}|$), the boundary layer widens ($\epsilon_{\text{eff}}$ increases), smoothing the control input and preventing high-frequency oscillations. Near equilibrium (small $|\dot{s}|$), the boundary layer narrows ($\epsilon_{\text{eff}} \approx \epsilon_{\min}$), preserving tracking precision.

**b) PSO-Optimal Parameter Selection:**
The optimized parameters $\epsilon_{\min}^* = 0.0025$ and $\alpha^* = 1.21$ represent a Pareto-optimal tradeoff between chattering (70% weight), settling time (15%), and overshoot (15%). Manual tuning would unlikely discover this optimal combination, as the fitness landscape is non-convex with multiple local minima (evidenced by PSO's 38.4% fitness improvement over initial random particles).

**c) No Energy Penalty:**
The zero energy penalty (p = 0.339) is critical for industrial deployment. Both fixed and adaptive boundary layers exhibit identical mean control energy (5,232 N²·s), confirming that chattering reduction does not come at the cost of increased actuator effort. This distinguishes our approach from higher-order SMC methods that inherently require additional control authority.

### 3) Practical Implications

For industrial mechatronic systems, the 66.5% chattering reduction translates to:
- **Extended actuator lifespan**: Reduced high-frequency mechanical stress (wear on bearings, gears, hydraulic valves)
- **Improved control precision**: Lower oscillations enable tighter trajectory tracking in robotic applications
- **Energy efficiency**: Chattering amplitude reduction directly correlates with reduced energy waste in control oscillations

The statistical robustness (non-overlapping 95% CIs: Fixed [6.13, 6.61], Adaptive [2.11, 2.16]) ensures the result is reproducible across different initial conditions within the training distribution.

## B. Analysis of Generalization Failure

The MT-7 results reveal a critical limitation: PSO parameters optimized for ±0.05 rad initial conditions exhibit **50.4× chattering degradation** (2.14 → 107.61) and **90.2% failure rate** when tested under ±0.3 rad initial conditions. This catastrophic generalization failure demands careful analysis.

### 1) Root Cause: Single-Scenario Overfitting

The generalization failure stems from **optimization bias toward the training distribution**:

**a) Narrow Search Space:**
PSO particles explored parameter combinations exclusively evaluated on initial conditions sampled from $\mathcal{U}(-0.05, 0.05)$ rad. This narrow distribution represents only ~17% of the ±0.3 rad operating range tested in MT-7. The fitness function provided no incentive to achieve robustness beyond this range, leading to parameters optimized for a specific corner of the state space.

**b) Boundary Layer Inadequacy for Large Errors:**
The adaptive formula $\epsilon_{\text{eff}} = \epsilon_{\min} + \alpha|\dot{s}|$ with $\alpha = 1.21$ produces boundary layer thicknesses appropriate for small initial errors. However, when $|\dot{s}|$ increases by 6× (due to 6× larger initial angles), $\epsilon_{\text{eff}}$ also increases proportionally. For large $\epsilon_{\text{eff}}$, the saturation region $|s| \leq \epsilon_{\text{eff}}$ may encompass the entire reachable state space, effectively disabling the switching control and causing divergence.

**c) Gain Mismatch:**
The switching gain $K$ optimized for ±0.05 rad disturbances may be insufficient for the larger matched disturbances equivalent to ±0.3 rad initial errors. The Lyapunov stability requirement $K > \bar{d}$ (Section IV-C) remains valid, but the effective disturbance bound $\bar{d}$ increases with initial condition magnitude.

### 2) Comparison with Literature

**Critical Observation:** All PSO-SMC studies reviewed in Section II (Ayinalem 2025, HEPSO-SMC 2025, quadcopter SMC 2025) validated controllers only on the training distribution. None reported robustness testing beyond optimization conditions. Our MT-7 results suggest these controllers likely suffer similar generalization failures if tested outside their training domains, but such failures go unreported.

**Implication:** The SMC literature exhibits a **validation gap**—controllers are optimized and validated on identical distributions, providing optimistic performance estimates that do not reflect real-world robustness. Our honest reporting of 50.4× degradation fills this gap and establishes a precedent for rigorous validation practices.

### 3) Why Existing Approaches May Avoid This Issue

Interestingly, the adaptive boundary layer methods reviewed in Section II-C (self-regulated, fuzzy-adaptive) may exhibit better generalization due to **continuous online adaptation**. Unlike our fixed PSO parameters, these methods adjust boundary layers in real-time based on current tracking error. However, this comes at the cost of:
- **Increased complexity**: Additional adaptation laws, potential parameter drift
- **Stability challenges**: No Lyapunov guarantees for arbitrary adaptation rules
- **Computational burden**: Real-time optimization or fuzzy inference

Our approach trades off online adaptability for simplicity and theoretical guarantees, but exposes the brittleness of single-scenario optimization.

## C. Disturbance Rejection Failure Analysis

The MT-8 results show **0% convergence** across all controllers (Classical, STA, Adaptive) and all disturbance types (step, impulse, sinusoidal). This universal failure reveals a fundamental limitation of nominal-condition optimization.

### 1) Root Cause: Fitness Function Myopia

The PSO fitness function (Section V-B) optimized for:

```latex
F = 0.70 \cdot C + 0.15 \cdot T_s + 0.15 \cdot O
```

under **disturbance-free conditions**. The chattering index $C$, settling time $T_s$, and overshoot $O$ were measured assuming no external perturbations. Consequently, the optimizer discovered parameters that minimize chattering for nominal trajectories but provide insufficient robustness margin for disturbance rejection.

### 2) Classical SMC Limitation: No Integral Action

The classical SMC control law (Section IV-A) lacks integral action:

```latex
u = u_{\text{eq}} - K \cdot \text{sat}(s/\epsilon_{\text{eff}}) - k_d \cdot s
```

This structure cannot reject **constant disturbances** (e.g., 10 N step force). The equivalent control $u_{\text{eq}}$ cancels nominal dynamics, but the switching term $-K \cdot \text{sat}(s/\epsilon_{\text{eff}})$ provides only proportional feedback on the sliding variable. Without an integral term, steady-state errors persist indefinitely.

**Contrast with Integral SMC:**
An integral sliding surface $s = e + \lambda \int e \, dt$ inherently rejects constant disturbances. The integral term accumulates error over time, forcing the controller to compensate. This explains why existing literature (Section II) often employs higher-order SMC (which includes implicit integral action via auxiliary states) for disturbance-prone environments.

### 3) Comparison with Literature

The disturbance rejection literature (Section II-A: observer-based designs) achieves robustness through:
- **Extended State Observers (ESO)**: Estimate and compensate unmatched disturbances
- **Disturbance Observers**: Reconstruct external forces and cancel them explicitly
- **Robust optimization**: Include worst-case disturbance scenarios in fitness evaluation

Our work demonstrates that **ignoring disturbances during optimization produces brittle controllers**, even when the control law theoretically possesses disturbance rejection properties (through switching gain $K > \bar{d}$). The practical lesson: robustness must be explicitly optimized, not assumed.

## D. Proposed Solutions and Future Directions

The MT-7 and MT-8 failures motivate three concrete future research directions:

### 1) Multi-Scenario Robust PSO

**Objective:** Optimize parameters robust to diverse operating conditions.

**Approach:**
- **Fitness function redesign**: Include multiple initial condition distributions and disturbance scenarios
  ```latex
  F_{\text{robust}} = \max_{\text{scenario } i} \left( 0.70 \cdot C_i + 0.15 \cdot T_{s,i} + 0.15 \cdot O_i \right)
  ```
  where the fitness is the **worst-case performance** across scenarios (minimax optimization).

- **Scenario diversity**: Sample initial conditions from $\mathcal{U}(-0.3, 0.3)$ rad during PSO evaluation, include disturbance rejection trials with step/impulse/sinusoidal forces.

- **Computational cost**: Multi-scenario fitness evaluation increases cost 5-10× (if using 5-10 scenarios per particle), requiring parallel PSO implementation or reduced swarm size.

**Expected Outcome:** Parameters that generalize beyond training distribution, with graceful degradation rather than catastrophic failure.

### 2) Disturbance-Aware Fitness Function

**Objective:** Explicitly penalize poor disturbance rejection during optimization.

**Approach:**
- **Augmented fitness**:
  ```latex
  F_{\text{robust}} = 0.50 \cdot C_{\text{nominal}} + 0.20 \cdot C_{\text{disturbed}} + 0.15 \cdot T_s + 0.15 \cdot O
  ```
  where $C_{\text{disturbed}}$ measures chattering/divergence under external perturbations.

- **Disturbance injection**: Apply step/impulse/sinusoidal forces during PSO evaluation trials, penalize divergence heavily (e.g., $C_{\text{disturbed}} = 1000$ if divergence occurs).

**Expected Outcome:** Parameters that balance nominal chattering reduction with disturbance rejection capability.

### 3) Integral Sliding Mode Control with PSO

**Objective:** Eliminate steady-state errors under constant disturbances.

**Approach:**
- **Integral sliding surface**:
  ```latex
  s = k_1(\dot{\theta}_1 + \lambda_1\theta_1) + k_2(\dot{\theta}_2 + \lambda_2\theta_2) + k_I \int_{0}^{t} (k_1\theta_1 + k_2\theta_2) \, d\tau
  ```
  The integral term $k_I \int (...)$ provides disturbance rejection.

- **PSO optimization**: Tune gains $(k_1, k_2, \lambda_1, \lambda_2, k_I, \epsilon_{\min}, \alpha)$ using disturbance-aware fitness.

**Expected Outcome:** Zero steady-state error under constant disturbances, preserved chattering reduction through adaptive boundary layer.

### 4) Hardware Validation

**Objective:** Validate simulation results on physical DIP system.

**Challenges:**
- **Actuator limitations**: Real motors have friction, backlash, bandwidth limits not modeled in simulation
- **Sensor noise**: Angular position measurements contain noise, affecting $\dot{s}$ estimation
- **Unmodeled dynamics**: Flexible modes, cable dynamics, air resistance

**Approach:**
- Implement controller on real-time embedded system (e.g., dSPACE, NI CompactRIO)
- Test under same initial condition distributions (±0.05 rad, ±0.3 rad)
- Measure actual chattering using accelerometers on pendulum joints

**Expected Outcome:** Validation of simulation findings or identification of simulation-to-reality gap requiring model refinement.

## E. Broader Implications for the SMC Community

Our findings carry three important lessons for the sliding mode control research community:

### 1) Honest Reporting of Negative Results

The 50.4× generalization failure and 0% disturbance rejection are **negative results** that many researchers might omit from publications. However, reporting failures is critical for:
- **Reproducibility**: Preventing others from repeating the same mistakes
- **Scientific integrity**: Providing complete picture of controller performance
- **Future progress**: Identifying concrete limitations to address in follow-on work

**Recommendation:** The SMC community should encourage reporting of generalization failures, disturbance rejection limitations, and validation beyond training distributions. Journals and conferences should value honest negative results as contributions, not weaknesses.

### 2) Validation Beyond Training Distributions

The ubiquitous practice of validating controllers only on the same distribution used for optimization (observed in all Section II studies) provides **optimistically biased performance estimates**. Robust validation requires:
- **Out-of-distribution testing**: Initial conditions 2-10× larger than training range
- **Cross-validation**: Separate training and test sets for Monte Carlo trials
- **Stress testing**: Extreme scenarios (disturbances, parameter variations, sensor noise)

**Recommendation:** Establish a standard validation protocol for optimized controllers: (1) optimize on distribution A, (2) validate on distribution A (in-distribution performance), (3) validate on distribution B >> A (out-of-distribution robustness), (4) report both results with clear distinction.

### 3) Multi-Objective vs. Single-Objective Optimization

Our chattering-weighted fitness function (70-15-15) represents a specific design choice prioritizing chattering reduction. However, different applications may require different tradeoffs:
- **Industrial robots**: Prioritize chattering (wear reduction)
- **Aerospace systems**: Prioritize energy efficiency (battery life)
- **Medical devices**: Prioritize precision (settling time, overshoot)

**Recommendation:** Future PSO-SMC research should report **Pareto fronts** (multi-objective optimization results) rather than single optimized points, allowing designers to select parameters appropriate for their application requirements.

### 4) Theoretical Stability vs. Empirical Robustness

Our Lyapunov stability proof (Section IV-C) guarantees finite-time convergence under Assumptions 1-4 (matched disturbances, $K > \bar{d}$, controllability, positive gains). The MT-6 success validates this theory for nominal conditions. However, the MT-7/MT-8 failures demonstrate that:
- **Theoretical stability ≠ practical robustness**: Lyapunov guarantees are asymptotic (infinite time), but finite-time performance depends on gains
- **Assumptions matter**: Violation of matched disturbance assumption (MT-8) or exceeding disturbance bound (MT-7) invalidates guarantees

**Recommendation:** SMC researchers should complement Lyapunov analysis with systematic robustness testing (Monte Carlo, worst-case scenarios, sensitivity analysis) to ensure theoretical guarantees translate to practical performance.

---

## Summary

This section discussed:

1. **MT-6 Success** (Section VIII-A): 66.5% chattering reduction compares favorably to state-of-the-art (fuzzy-adaptive, HOSMC, hybrids), with very large effect size (d = 5.29) and zero energy penalty

2. **MT-7 Generalization Failure** (Section VIII-B): 50.4× degradation stems from single-scenario overfitting, narrow training distribution (±0.05 rad), and boundary layer inadequacy for large errors

3. **MT-8 Disturbance Rejection Failure** (Section VIII-C): 0% convergence results from fitness function myopia (no disturbance scenarios), lack of integral action in classical SMC, and optimization bias toward nominal conditions

4. **Proposed Solutions** (Section VIII-D): Multi-scenario robust PSO (minimax fitness), disturbance-aware fitness function (50-20-15-15 weights), integral SMC with PSO, and hardware validation

5. **Broader Implications** (Section VIII-E): Honest reporting of negative results, validation beyond training distributions, multi-objective optimization transparency, and bridging the gap between theoretical stability and empirical robustness

**Key Takeaway:** Single-scenario PSO optimization achieves dramatic performance improvements for trained conditions but fails catastrophically outside the training distribution, motivating future research on robust multi-scenario optimization and rigorous validation practices for the SMC community.

**Next:** Section IX concludes the paper with a summary of contributions, acknowledged limitations, and future research directions.
