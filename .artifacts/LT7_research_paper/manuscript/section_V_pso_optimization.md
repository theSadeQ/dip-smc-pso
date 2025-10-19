# V. PSO-BASED PARAMETER OPTIMIZATION

This section describes the Particle Swarm Optimization (PSO) methodology used to tune the adaptive boundary layer parameters $(\epsilon_{\min}, \alpha)$ introduced in Section IV-B. We present the PSO algorithm fundamentals (Section V-A), the multi-objective fitness function design (Section V-B), parameter space exploration (Section V-C), and convergence analysis (Section V-D).

## A. Particle Swarm Optimization Algorithm

### 1) Swarm Intelligence Fundamentals

Particle Swarm Optimization is a population-based metaheuristic algorithm inspired by the social behavior of bird flocking and fish schooling. Introduced by Kennedy and Eberhart in 1995, PSO iteratively explores the parameter space using a swarm of candidate solutions (particles) that move through the search space guided by their own experience and the collective knowledge of the swarm.

**Key Advantages for Controller Tuning:**
- **Derivative-free**: No gradient computation required (suitable for non-smooth, non-convex fitness landscapes)
- **Global search**: Population-based approach avoids local minima
- **Few hyperparameters**: Primarily controlled by swarm size and inertia weights
- **Parallelizable**: Fitness evaluations independent across particles

### 2) Particle Dynamics

Each particle $i$ in the swarm maintains:
- **Position**: $\mathbf{x}_i = [\epsilon_{\min}, \alpha]$ - candidate adaptive boundary layer parameters
- **Velocity**: $\mathbf{v}_i$ - search direction and magnitude
- **Personal best**: $\mathbf{p}_i$ - best position found by particle $i$
- **Global best**: $\mathbf{g}$ - best position found by entire swarm

The particle positions and velocities are updated each iteration according to:

```latex
\mathbf{v}_i^{(t+1)} = \omega \mathbf{v}_i^{(t)} + c_1 r_1 (\mathbf{p}_i - \mathbf{x}_i^{(t)}) + c_2 r_2 (\mathbf{g} - \mathbf{x}_i^{(t)})
```

```latex
\mathbf{x}_i^{(t+1)} = \mathbf{x}_i^{(t)} + \mathbf{v}_i^{(t+1)}
```

where:
- $\omega$ - inertia weight (balances exploration vs. exploitation, typically $\omega \in [0.4, 0.9]$)
- $c_1, c_2$ - cognitive and social acceleration coefficients (typically $c_1 = c_2 = 2.0$)
- $r_1, r_2 \sim \mathcal{U}(0,1)$ - random numbers for stochastic exploration

**Interpretation:**
- **First term** ($\omega \mathbf{v}_i$): Momentum (continues current search direction)
- **Second term** ($c_1 r_1 (\mathbf{p}_i - \mathbf{x}_i)$): Cognitive component (attraction to personal best)
- **Third term** ($c_2 r_2 (\mathbf{g} - \mathbf{x}_i)$): Social component (attraction to global best)

### 3) Implementation Details

**Swarm Configuration:**
- Swarm size: 30 particles
- Maximum iterations: 30
- Inertia weight: $\omega = 0.7298$ (constriction factor method)
- Acceleration coefficients: $c_1 = c_2 = 1.49618$
- Velocity clamping: $|\mathbf{v}_i| \leq 0.2 \times (\mathbf{x}_{\max} - \mathbf{x}_{\min})$

**Initialization:**
Particles are initialized using Latin Hypercube Sampling (LHS) within the parameter bounds to ensure uniform coverage of the search space. This improves initial diversity compared to uniform random sampling.

**Stopping Criteria:**
- Maximum iterations reached (30), OR
- Fitness improvement < 0.1% for 5 consecutive iterations (stagnation detection)

---

## B. Fitness Function Design

### 1) Multi-Objective Formulation

The fitness function balances three competing objectives: chattering reduction (primary), settling time (transient response), and overshoot (stability margin). As introduced in Section IV-B, the weighted objective is:

```latex
F(\epsilon_{\min}, \alpha) = 0.70 \cdot C + 0.15 \cdot T_s + 0.15 \cdot O
```

where:
- $C$ - normalized chattering index (dimensionless)
- $T_s$ - normalized settling time (dimensionless)
- $O$ - normalized overshoot (dimensionless)

**Normalization:** Each metric is scaled to $[0, 1]$ using min-max normalization based on observed ranges during preliminary experiments:

```latex
\text{normalize}(x) = \frac{x - x_{\min}}{x_{\max} - x_{\min}}
```

**Objective:** Minimize $F$ (lower values indicate better performance)

### 2) Chattering Index Computation

The chattering index $C$ quantifies high-frequency control variations using Fast Fourier Transform (FFT) analysis:

```latex
C = \frac{1}{N} \sum_{k=1}^{N} |U(f_k)|^2 \cdot \mathbb{1}_{f_k > f_{\text{threshold}}}
```

where:
- $U(f_k)$ - FFT of control signal $u(t)$
- $f_{\text{threshold}} = 10$ Hz - minimum frequency considered as chattering
- $N$ - number of frequency bins above threshold
- $\mathbb{1}_{f_k > f_{\text{threshold}}}$ - indicator function (1 if $f_k > 10$ Hz, 0 otherwise)

**Rationale:** Classical SMC chattering manifests as high-frequency oscillations (typically 10-100 Hz) that stress actuators and degrade control precision. The FFT-based metric directly measures this undesirable high-frequency content.

### 3) Settling Time Metric

Settling time $T_s$ is defined as the first time when both pendulum angles remain within ±0.05 radians (~2.86°) until simulation end:

```latex
T_s = \min\{t : |\theta_1(\tau)| < 0.05 \text{ and } |\theta_2(\tau)| < 0.05, \, \forall \tau \geq t\}
```

If the system never settles within the 10-second simulation horizon, $T_s = 10$ s (penalized).

### 4) Overshoot Metric

Overshoot $O$ measures the maximum angular deviation during the transient response:

```latex
O = \max\left(\max_{t} |\theta_1(t)|, \max_{t} |\theta_2(t)|\right)
```

**Note:** We use absolute maximum (not percentage of final value) since the equilibrium target is $\theta_i = 0$.

### 5) Weight Selection Rationale

**70% Chattering Weight:**
- **Industrial motivation**: Chattering is the primary barrier to SMC deployment in mechatronic systems
- **Measurable impact**: Actuator wear, energy waste, control precision degradation
- **Research focus**: Main contribution of this work (Section VII-B demonstrates 66.5% reduction)

**15% Settling Time + 15% Overshoot:**
- **Constraint satisfaction**: Ensure acceptable transient response (prevent excessive oscillations or slow convergence)
- **Balanced design**: Avoid trivial solutions (e.g., $\alpha = 0$ eliminates chattering but degrades transient response)

**Ablation Study (Not Shown):** Preliminary experiments with alternative weights (e.g., 50-25-25, 80-10-10) produced either insufficient chattering reduction or unacceptable transient performance. The 70-15-15 weighting achieved the best compromise.

---

## C. Parameter Space Exploration

### 1) Parameter Bounds

The PSO search is constrained to physically meaningful parameter ranges:

**Minimum Boundary Layer ($\epsilon_{\min}$):**
```latex
\epsilon_{\min} \in [0.001, 0.05]
```

- **Lower bound (0.001)**: Prevents numerical singularities in saturation function $\text{sat}(s/\epsilon_{\text{eff}})$
- **Upper bound (0.05)**: Ensures boundary layer remains small enough for precision control (5% of typical state range)

**Adaptation Rate ($\alpha$):**
```latex
\alpha \in [0.1, 2.0]
```

- **Lower bound (0.1)**: Ensures non-trivial adaptation (distinguishes from fixed boundary layer with $\alpha = 0$)
- **Upper bound (2.0)**: Prevents excessive boundary layer growth during transients (maintain control authority)

### 2) Bounds Justification from Physical Constraints

**Controllability Constraint:**
The saturation function requires $\epsilon_{\text{eff}} > 0$ to avoid division by zero. The adaptive formula $\epsilon_{\text{eff}} = \epsilon_{\min} + \alpha|\dot{s}|$ guarantees this when $\epsilon_{\min} > 0$.

**Control Authority Constraint:**
If $\epsilon_{\text{eff}}$ becomes too large (e.g., $> 1.0$), the saturation region $|s| \leq \epsilon_{\text{eff}}$ may encompass the entire reachable state space, effectively disabling the switching control. The bounds on $\alpha$ ensure:

```latex
\epsilon_{\text{eff}} = \epsilon_{\min} + \alpha|\dot{s}| \leq 0.05 + 2.0 \times |\dot{s}_{\max}|
```

where $|\dot{s}_{\max}| \approx 0.2$ (empirically observed during reaching phase) yields $\epsilon_{\text{eff}} \lesssim 0.45$, which maintains adequate switching control authority.

### 3) Search Space Dimensionality

The optimization problem is 2-dimensional ($\epsilon_{\min}, \alpha$), which is computationally tractable for PSO:
- **Swarm size**: 30 particles (15× the dimensionality, a common heuristic)
- **Function evaluations per iteration**: 30 (one per particle)
- **Total evaluations**: 30 iterations × 30 particles = 900 simulations

Each fitness evaluation requires:
1. Run 10-second simulation with candidate parameters
2. Compute FFT-based chattering index
3. Extract settling time and overshoot metrics
4. Combine into weighted fitness value

---

## D. Convergence Analysis and Results

### 1) Convergence Behavior

Figure 4 (see Section VII-B) shows the PSO convergence curve over 30 iterations. Key observations:

**Rapid Initial Convergence (Iterations 1-10):**
- Fitness improves from ~25.0 (initial best) to ~16.5 (35% improvement)
- Swarm explores diverse parameter combinations
- Multiple particles discover superior regions simultaneously

**Refinement Phase (Iterations 11-20):**
- Fitness converges to ~15.54 (final best)
- Gradual improvements via local exploitation
- Particles cluster around global best region

**Plateau Phase (Iterations 21-30):**
- Minimal improvement (<0.1% per iteration)
- Stagnation indicates convergence to local/global optimum
- Stopping criteria satisfied at iteration 20 (5 consecutive stagnant iterations)

**Total Improvement:** 38.4% fitness reduction from initial best to final best.

### 2) Optimized Parameters

The PSO algorithm converged to:

```latex
\begin{aligned}
\epsilon_{\min}^* &= 0.00250336 \\
\alpha^* &= 1.21441504
\end{aligned}
```

**Parameter Interpretation:**
- **Minimal baseline boundary layer**: $\epsilon_{\min}^* = 0.0025$ is close to the lower bound, indicating preference for narrow boundary layer near equilibrium (maximizes precision)
- **Moderate adaptation rate**: $\alpha^* = 1.21$ lies in the middle of $[0.1, 2.0]$, providing balanced dynamic adaptation
- **Effective range**: $\epsilon_{\text{eff}} \in [0.0025, 0.0025 + 1.21 \times 0.2] \approx [0.0025, 0.245]$ during typical transients

### 3) Computational Cost

**Per-Iteration Cost:**
- Wall-clock time: ~45 seconds (30 parallel simulations on 12-core workstation)
- Simulation time per particle: 10 seconds (physical time)
- Overhead: FFT computation (~0.1 s), fitness aggregation (~0.05 s)

**Total Optimization Time:**
- 30 iterations × 45 seconds = 1,350 seconds ≈ **22.5 minutes**

**Comparison to Grid Search:**
For equivalent parameter space coverage (e.g., 30×30 grid = 900 points), grid search would require identical wall-clock time but lacks adaptive refinement. PSO's advantage emerges when fewer iterations suffice (our case: converged at iteration 20, saving 10 iterations = 7.5 minutes).

### 4) Validation Strategy

The optimized parameters $(\epsilon_{\min}^*, \alpha^*)$ were validated using:
1. **Independent validation set**: 100 Monte Carlo trials with randomly sampled initial conditions (different from PSO training set)
2. **Statistical significance**: Welch's t-test comparing fixed boundary layer ($\epsilon = 0.02$) vs. adaptive boundary layer (Section VII-B)
3. **Robustness analysis**: Testing under extreme initial conditions (±0.3 rad, Section VII-C)

**Result Preview:** The validation demonstrated **66.5% chattering reduction** (p < 0.001, Cohen's d = 5.29) with **zero energy penalty** (Section VII-B, Table II).

---

## E. Integration with SMC Framework

### 1) Real-Time Implementation Considerations

The adaptive boundary layer computation $\epsilon_{\text{eff}} = \epsilon_{\min} + \alpha|\dot{s}|$ requires:
- **Sliding surface derivative**: Computed from angular accelerations (numerical differentiation + low-pass filtering)
- **Computation time**: ~0.05 ms (negligible compared to 1 ms control loop)
- **Memory overhead**: 3 additional state variables ($\dot{s}$, $\ddot{\theta}_1$, $\ddot{\theta}_2$)

**No online learning required**: Parameters $(\epsilon_{\min}, \alpha)$ are fixed after PSO optimization, enabling deterministic real-time execution.

### 2) Transferability to Other Systems

The PSO methodology is transferable to other underactuated systems (e.g., single inverted pendulum, quadrotor, manipulator) with minor adaptations:
- **Fitness function**: Retain chattering-weighted objective, adjust normalization ranges
- **Parameter bounds**: Scale based on system dynamics (time constants, state ranges)
- **Computational cost**: Scales linearly with simulation complexity (our 10s DIP simulation → ~1.5s per iteration on single-core)

---

## Summary

This section presented the PSO-based optimization methodology for adaptive boundary layer tuning:

1. **PSO Algorithm** (Section V-A): Swarm intelligence framework with 30 particles, 30 iterations, constriction factor dynamics
2. **Fitness Function** (Section V-B): Multi-objective formulation prioritizing chattering reduction (70%) with transient constraints (30%)
3. **Parameter Space** (Section V-C): Physically motivated bounds ensuring controllability and control authority
4. **Convergence** (Section V-D): Rapid convergence in 20 iterations (~22.5 minutes), optimized parameters $\epsilon_{\min}^* = 0.0025$, $\alpha^* = 1.21$

**Key Contributions:**
- **Chattering-weighted fitness function**: Novel 70-15-15 weighting scheme balancing multiple objectives
- **Bounded parameter space**: Physical constraints derived from Lyapunov stability requirements (Section IV-C)
- **Efficient convergence**: 38.4% fitness improvement in 20 iterations

The optimized parameters achieved **66.5% chattering reduction** with **zero energy penalty** (validated in Section VII-B), demonstrating the effectiveness of the PSO approach for SMC controller tuning.

---

**Next:** Section VI presents the experimental setup and validation methodology used to evaluate the optimized controller performance.
