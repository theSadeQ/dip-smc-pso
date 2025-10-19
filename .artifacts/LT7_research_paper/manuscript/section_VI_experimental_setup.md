# VI. EXPERIMENTAL SETUP

This section describes the simulation environment, validation methodology, and statistical analysis procedures used to evaluate the PSO-optimized adaptive boundary layer SMC. We present the simulation parameters (Section VI-A), Monte Carlo validation methodology (Section VI-B), performance metrics (Section VI-C), and statistical analysis procedures (Section VI-D).

## A. Simulation Environment

### 1) Numerical Integration

The nonlinear DIP dynamics (Section III) are integrated using the **4th-order Runge-Kutta (RK4)** method with fixed time step:

```latex
\Delta t = 0.001 \, \text{s} \quad (1 \, \text{kHz sampling rate})
```

**Integration Accuracy:**
- Local truncation error: $\mathcal{O}(\Delta t^5)$
- Global truncation error: $\mathcal{O}(\Delta t^4)$

The RK4 method provides excellent accuracy-to-cost tradeoff for nonlinear mechanical systems, with typical angular position errors $< 10^{-6}$ rad over 10-second simulations when compared to adaptive step-size integrators (e.g., ODE45).

**Simulation Duration:**
All trials simulate 10 seconds of physical time:

```latex
t \in [0, 10] \, \text{s}
```

This duration is sufficient to observe:
- Reaching phase (system approaches sliding surface)
- Sliding phase (tracking along $s \approx 0$)
- Steady-state behavior (settling time evaluation)

### 2) Initial Conditions

Initial conditions are sampled from three distributions depending on the experiment:

**MT-5 (Baseline Comparison) and MT-6 (Adaptive Boundary Layer Optimization):**
- Cart position: $x(0) = 0$ m (fixed)
- Pendulum angles: $\theta_1(0), \theta_2(0) \sim \mathcal{U}(-0.05, 0.05)$ rad (uniform random)
- Velocities: $\dot{x}(0) = \dot{\theta}_1(0) = \dot{\theta}_2(0) = 0$ (starting from rest)

**Rationale:** ±0.05 rad ≈ ±2.86° represents small perturbations near equilibrium, typical for stabilization tasks.

**MT-7 (Robustness Validation):**
- Cart position: $x(0) = 0$ m (fixed)
- Pendulum angles: $\theta_1(0), \theta_2(0) \sim \mathcal{U}(-0.3, 0.3)$ rad (6× larger range)
- Velocities: $\dot{x}(0) = \dot{\theta}_1(0) = \dot{\theta}_2(0) = 0$

**Rationale:** ±0.3 rad ≈ ±17.2° represents large perturbations outside the training distribution, stress-testing generalization.

**MT-8 (Disturbance Rejection):**
- Initial conditions: $x(0) = 0$, $\theta_1(0) = \theta_2(0) = 0.05$ rad (small perturbation)
- External disturbances applied after initial stabilization (see Section VI-A.4)

### 3) Control Implementation

**Discrete-Time Implementation:**
The controller computes control input $u[k]$ at each time step based on current state $\mathbf{x}[k]$:

```latex
u[k] = u_{\text{eq}}[k] + u_{\text{sw}}[k]
```

where:
- $u_{\text{eq}}[k]$ - equivalent control (computed from system matrices)
- $u_{\text{sw}}[k] = -K \cdot \text{sat}(s[k]/\epsilon_{\text{eff}}[k]) - k_d \cdot s[k]$

**Sliding Surface Derivative Estimation:**
The adaptive boundary layer requires $|\dot{s}|$, computed via:

1. **Numerical differentiation**: Backward Euler
   ```latex
   \dot{s}[k] \approx \frac{s[k] - s[k-1]}{\Delta t}
   ```

2. **Low-pass filtering**: Exponential moving average with coefficient $\beta = 0.3$
   ```latex
   \dot{s}_{\text{filtered}}[k] = \beta \dot{s}[k] + (1 - \beta) \dot{s}_{\text{filtered}}[k-1]
   ```

This reduces noise amplification from numerical differentiation while maintaining responsiveness.

**Control Saturation:**
The control input is clipped to actuator limits:

```latex
u_{\text{saturated}}[k] = \text{clip}(u[k], -150, 150) \, \text{N}
```

### 4) Disturbance Profiles (MT-8)

Three disturbance scenarios are tested:

**Step Disturbance:**
```latex
d_{\text{step}}(t) = \begin{cases}
10 \, \text{N} & t \geq 5 \, \text{s} \\
0 & t < 5 \, \text{s}
\end{cases}
```

**Impulse Disturbance:**
```latex
d_{\text{impulse}}(t) = 30 \, \text{N} \cdot \delta(t - 5) \quad (\text{applied as } 30 \, \text{N} \text{ for } 1 \text{ ms})
```

**Sinusoidal Disturbance:**
```latex
d_{\text{sin}}(t) = 8 \sin(2\pi \cdot 0.5 \cdot t) \, \text{N} \quad (0.5 \, \text{Hz}, \, t \geq 0)
```

All disturbances are applied as external forces on the cart (same direction as control input $u$).

### 5) Hardware and Software

**Computational Platform:**
- CPU: 12-core Intel Xeon @ 3.2 GHz
- RAM: 32 GB
- OS: Windows 10

**Software Stack:**
- Python 3.9.7
- NumPy 1.21.2 (numerical integration, matrix operations)
- SciPy 1.7.1 (FFT for chattering index)
- PySwarms 1.3.0 (PSO optimization)
- Matplotlib 3.4.3 (visualization)

**Reproducibility:**
All simulations use fixed random seeds for reproducibility:
- MT-5: seed 42
- MT-6 training: seed 42 (PSO initialization)
- MT-6 validation: seed 42 (Monte Carlo trials)
- MT-7: seeds 42-51 (10 independent runs)

## B. Monte Carlo Validation Methodology

### 1) Sample Sizes

Monte Carlo simulations are used to quantify statistical variability across random initial conditions:

**TABLE II: MONTE CARLO SAMPLE SIZES PER EXPERIMENT**

| Experiment | Description | Sample Size | Random Seeds |
|------------|-------------|-------------|--------------|
| MT-5 | Baseline controller comparison | 100 per controller (400 total) | 42 |
| MT-6 Training | PSO optimization (fitness evaluation) | ~500 (30 particles × ~17 iterations) | 42 (PSO init) |
| MT-6 Fixed | Fixed boundary layer validation | 100 | 42 |
| MT-6 Adaptive | Adaptive boundary layer validation | 100 | 42 |
| MT-7 | Robustness stress testing | 500 (50 per seed) | 42-51 (10 seeds) |
| MT-8 | Disturbance rejection | 12 (3 disturbances × 4 controllers) | N/A (deterministic) |

**Sample Size Justification:**
- **n = 100**: Standard for control systems validation, provides 95% confidence intervals with width ~0.2σ
- **n = 500** (MT-7): Larger sample to detect rare failure modes (90.2% failure rate requires many attempts)
- **n = 12** (MT-8): Deterministic scenarios (no randomness), each combination tested once

### 2) Termination Criteria

Simulations terminate early (before 10 seconds) if **divergence** is detected:

**Divergence Conditions:**
1. $|\theta_1| > \pi/2$ rad (90°) - pendulum falls beyond horizontal
2. $|\theta_2| > \pi/2$ rad (90°) - second pendulum falls beyond horizontal
3. $|u| > 10 \times u_{\max}$ - control saturation exceeded significantly (numerical instability indicator)

**Success Rate Computation:**
```latex
\text{Success Rate} = \frac{\text{Number of non-divergent trials}}{\text{Total trials attempted}} \times 100\%
```

For MT-7, the success rate was 9.8% (49 out of 500 trials converged).

### 3) Data Collection

Each simulation records time series data at 1 kHz:
- State vector: $\mathbf{x}(t) = [x, \theta_1, \theta_2, \dot{x}, \dot{\theta}_1, \dot{\theta}_2]^T$
- Control input: $u(t)$
- Sliding surface: $s(t)$
- Adaptive boundary layer (if applicable): $\epsilon_{\text{eff}}(t)$

Data is stored in CSV format for post-processing and analysis.

## C. Performance Metrics

### 1) Chattering Index

The primary metric quantifying high-frequency control variations:

```latex
C = \frac{1}{N_f} \sum_{k: f_k > 10 \, \text{Hz}} |U(f_k)|^2
```

where:
- $U(f_k)$ - FFT of control signal $u(t)$
- $f_k$ - frequency bins
- $N_f$ - number of frequency bins above 10 Hz threshold

**Computation Procedure:**
1. Extract control signal time series $u(t)$ for $t \in [0, 10]$ s (10,000 samples)
2. Compute FFT: $U(f) = \text{FFT}(u(t))$
3. Compute power spectral density: $|U(f)|^2$
4. Sum power in frequencies $f > 10$ Hz
5. Normalize by number of high-frequency bins

**Interpretation:** Higher $C$ indicates more severe chattering (undesirable). Reduction in $C$ is the primary optimization objective.

### 2) Settling Time

Time required for pendulum angles to reach and remain within tolerance:

```latex
T_s = \min\{t : |\theta_1(\tau)| < 0.05 \text{ and } |\theta_2(\tau)| < 0.05, \, \forall \tau \in [t, 10]\}
```

If no settling occurs within 10 seconds, $T_s = 10$ s (penalized).

**Tolerance Rationale:** 0.05 rad ≈ 2.86° is a standard precision requirement for robotic systems.

### 3) Overshoot

Maximum angular deviation during transient response:

```latex
O = \max\left(\max_{t \in [0, 10]} |\theta_1(t)|, \max_{t \in [0, 10]} |\theta_2(t)|\right)
```

**Note:** Overshoot is measured as absolute maximum (not percentage) since target is $\theta_i = 0$.

### 4) Control Energy

Total squared control effort over simulation duration:

```latex
E = \int_0^{10} u^2(t) \, dt \approx \Delta t \sum_{k=0}^{10000} u[k]^2
```

**Units:** N²·s (Newton-squared-seconds)

**Interpretation:** Lower energy indicates more efficient control. Comparing fixed vs. adaptive boundary layers at equal chattering reduction ensures no energy penalty.

### 5) Success Rate (MT-7)

Fraction of trials that converged without divergence:

```latex
\text{Success Rate} = \frac{n_{\text{success}}}{n_{\text{total}}} \times 100\%
```

where $n_{\text{success}}$ counts trials satisfying $|\theta_1|, |\theta_2| \leq \pi/2$ for all $t \in [0, 10]$ s.

## D. Statistical Analysis Procedures

### 1) Hypothesis Testing

**Null Hypothesis (H₀):** Adaptive boundary layer does not reduce chattering compared to fixed boundary layer ($\mu_{\text{adaptive}} \geq \mu_{\text{fixed}}$).

**Alternative Hypothesis (H₁):** Adaptive boundary layer significantly reduces chattering ($\mu_{\text{adaptive}} < \mu_{\text{fixed}}$).

**Test Statistic:** Welch's t-test (accounts for unequal variances)

```latex
t = \frac{\bar{x}_{\text{fixed}} - \bar{x}_{\text{adaptive}}}{\sqrt{s_{\text{fixed}}^2/n_{\text{fixed}} + s_{\text{adaptive}}^2/n_{\text{adaptive}}}}
```

with degrees of freedom computed via Welch-Satterthwaite approximation.

**Significance Level:** $\alpha = 0.05$ (95% confidence)

**Decision Rule:** Reject H₀ if $p < 0.05$

### 2) Effect Size

Cohen's d quantifies the standardized difference between fixed and adaptive boundary layers:

```latex
d = \frac{\mu_{\text{fixed}} - \mu_{\text{adaptive}}}{\sigma_{\text{pooled}}}
```

where:

```latex
\sigma_{\text{pooled}} = \sqrt{\frac{(n_{\text{fixed}} - 1)s_{\text{fixed}}^2 + (n_{\text{adaptive}} - 1)s_{\text{adaptive}}^2}{n_{\text{fixed}} + n_{\text{adaptive}} - 2}}
```

**Interpretation (Cohen's conventions):**
- $|d| < 0.2$: Negligible effect
- $0.2 \leq |d| < 0.5$: Small effect
- $0.5 \leq |d| < 0.8$: Medium effect
- $|d| \geq 0.8$: Large effect

For our MT-6 results, $d = 5.29$ indicates a **very large** effect (exceptional in control systems research).

### 3) Confidence Intervals

95% confidence intervals are computed using the bootstrap method with 10,000 resamples:

**Bootstrap Procedure:**
1. Given dataset $\{x_1, \ldots, x_n\}$, generate 10,000 bootstrap samples by sampling with replacement
2. Compute mean $\bar{x}^*$ for each bootstrap sample
3. Sort bootstrap means: $\bar{x}^*_{(1)} \leq \cdots \leq \bar{x}^*_{(10000)}$
4. 95% CI: $[\bar{x}^*_{(250)}, \bar{x}^*_{(9750)}]$ (2.5th and 97.5th percentiles)

**Advantages over Parametric CI:**
- No normality assumption required
- Robust to outliers
- Asymptotically accurate for general distributions

### 4) Multiple Comparisons Correction

When comparing multiple controllers (MT-5), we apply the **Bonferroni correction** to control family-wise error rate:

**Adjusted significance level:**
```latex
\alpha_{\text{adj}} = \frac{\alpha}{m}
```

where $m$ is the number of pairwise comparisons.

For MT-5 with 3 controllers (Classical, STA, Adaptive), $m = 3$ pairwise tests:
```latex
\alpha_{\text{adj}} = \frac{0.05}{3} \approx 0.0167
```

Reject H₀ only if $p < 0.0167$ (more stringent than standard 0.05).

## E. Validation Summary

**Comprehensive Validation Strategy:**
1. **Baseline comparison** (MT-5): Establish Classical SMC superiority in energy efficiency (20× better than STA/Adaptive)
2. **Adaptive boundary layer validation** (MT-6): Demonstrate 66.5% chattering reduction with statistical significance ($p < 0.001$, $d = 5.29$)
3. **Robustness stress testing** (MT-7): Identify generalization failure (50.4× degradation, 90.2% failure rate)
4. **Disturbance rejection** (MT-8): Expose brittleness under external perturbations (0% convergence)

This multi-faceted validation provides both positive results (MT-6 success) and negative results (MT-7/MT-8 failures), offering an honest assessment of the PSO-optimized adaptive boundary layer approach.

---

## Summary

This section detailed the experimental setup for evaluating PSO-optimized adaptive boundary layer SMC:

1. **Simulation environment** (Section VI-A): RK4 integration at 1 kHz, 10-second trials, three initial condition distributions, three disturbance profiles
2. **Monte Carlo methodology** (Section VI-B): Sample sizes 100-500 per experiment, fixed random seeds for reproducibility, divergence-based termination
3. **Performance metrics** (Section VI-C): Chattering index (FFT-based), settling time, overshoot, control energy, success rate
4. **Statistical analysis** (Section VI-D): Welch's t-test, Cohen's d effect size, bootstrap 95% CI, Bonferroni correction for multiple comparisons

The rigorous validation methodology ensures that results (Section VII) are statistically robust and reproducible.

**Next:** Section VII presents comprehensive experimental results from MT-5, MT-6, MT-7, and MT-8, including both positive findings (66.5% chattering reduction) and critical limitations (generalization and disturbance rejection failures).
