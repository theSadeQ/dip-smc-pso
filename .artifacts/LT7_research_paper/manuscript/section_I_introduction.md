# I. INTRODUCTION

Sliding mode control (SMC) has emerged as a powerful robust control technique for nonlinear systems due to its insensitivity to matched disturbances and model uncertainties. The core principle of SMC is to design a switching control law that drives system trajectories onto a predefined sliding surface, where desirable dynamics are guaranteed. However, a fundamental barrier to industrial adoption of classical SMC is **chattering**: high-frequency oscillations in the control signal caused by imperfect switching in discrete-time implementations. Chattering leads to excessive actuator wear, energy waste, and degraded control precision, limiting SMC applicability in mechatronic systems requiring smooth control inputs.

## A. Motivation and Background

The double inverted pendulum (DIP) represents a challenging benchmark for control systems research, exhibiting underactuation, nonlinearity, and instability at the upright equilibrium. While linear controllers (e.g., LQR, PID) can stabilize the DIP near equilibrium, they lack robustness to disturbances and parameter variations. SMC provides an attractive alternative through its inherent robustness properties derived from Lyapunov stability theory.

Classical approaches to chattering reduction include: (1) **boundary layer methods** that replace the discontinuous signum function with a saturation function within a boundary layer of thickness $\epsilon$, trading reduced chattering for increased steady-state error; (2) **higher-order sliding modes** (e.g., super-twisting algorithm) that achieve continuous control through integral action, at the cost of increased complexity and computational burden; and (3) **adaptive gain tuning** that adjusts switching gains online based on sliding surface magnitude, requiring careful stability analysis to prevent parameter drift.

Despite decades of research, a practical question remains: **How can we minimize chattering while maintaining control precision and energy efficiency?** The boundary layer approach offers a direct tradeoff: larger $\epsilon$ reduces chattering but degrades tracking accuracy, while smaller $\epsilon$ improves precision but exacerbates chattering. Fixed boundary layer selection thus represents a compromise that may be suboptimal across the entire state space.

## B. Research Gap

Existing SMC chattering mitigation techniques exhibit three key limitations:

1. **Fixed boundary layers** use constant $\epsilon$ regardless of system state, failing to exploit the natural variation in control requirements during transient (reaching phase) versus steady-state (sliding phase) operation.

2. **Manual parameter tuning** relies on trial-and-error or conservative design rules (e.g., $\epsilon > 0.1$), missing the opportunity for systematic optimization tailored to specific performance objectives.

3. **Single-scenario validation** typically evaluates controller performance under nominal conditions only, without rigorously testing robustness to initial condition variations or external disturbances.

Recent work has explored adaptive boundary layers that vary $\epsilon$ based on sliding surface magnitude [citations from Section II], but these approaches lack: (a) principled parameter optimization methods beyond heuristic selection, and (b) honest reporting of generalization failures when controllers are tested beyond their training distribution.

## C. Contributions

This paper addresses the research gap through three primary contributions:

**1. PSO-Optimized Adaptive Boundary Layer for Chattering Reduction**

We propose an adaptive boundary layer mechanism where the effective boundary thickness $\epsilon_{\text{eff}} = \epsilon_{\min} + \alpha|\dot{s}|$ dynamically adjusts based on the sliding surface derivative magnitude. The parameters $(\epsilon_{\min}, \alpha)$ are optimized using Particle Swarm Optimization (PSO) with a chattering-weighted fitness function ($F = 0.70 \cdot C + 0.15 \cdot T_s + 0.15 \cdot O$) that prioritizes high-frequency control variation reduction while maintaining acceptable transient response.

**Experimental validation** demonstrates **66.5% chattering reduction** (6.37 → 2.14, $p < 0.001$, Cohen's $d = 5.29$) with **zero energy penalty** compared to fixed boundary layer SMC, based on 100 Monte Carlo trials with randomly sampled initial conditions.

**2. Lyapunov Stability Analysis for Adaptive Boundary Layer Compatibility**

We provide rigorous theoretical guarantees via Lyapunov stability analysis, proving finite-time convergence to the sliding surface under standard assumptions (matched disturbances, switching gain dominance, controllability). The key theoretical contribution is **Theorem 1**, which establishes that the adaptive boundary layer does not compromise the fundamental stability requirement $K > \bar{d}$, with reaching time bounded by $t_{\text{reach}} \leq \sqrt{2}|s(0)|/(\beta\eta)$ where $\eta = K - \bar{d}$.

**3. Honest Reporting of Generalization Failures and Robustness Limitations**

We identify and quantify critical limitations through systematic stress testing:

- **Generalization failure** (MT-7): PSO parameters optimized for initial conditions within ±0.05 rad exhibit **50.4× chattering degradation** (2.14 → 107.61) and **90.2% failure rate** when tested under ±0.3 rad initial conditions, revealing severe overfitting to the training distribution.

- **Disturbance rejection failure** (MT-8): Controllers optimized for nominal conditions achieve **0% convergence** under external disturbances (10 N step, 30 N·s impulse, 8 N sinusoidal), demonstrating that single-scenario PSO produces brittle controllers lacking robustness.

These negative results provide crucial insights: (a) **multi-scenario PSO** with diverse initial conditions and disturbance profiles is essential for robust controller design, and (b) **validation must extend significantly beyond the training distribution** to expose overfitting. Our honest reporting of failures advances the field by quantifying the brittleness problem that is likely present but unreported in prior single-scenario optimization studies.

## D. Paper Organization

The remainder of this paper is organized as follows:

- **Section II** reviews related work on SMC chattering mitigation, PSO-based controller tuning, and adaptive boundary layer techniques, positioning our contributions within the state-of-the-art.

- **Section III** presents the double inverted pendulum system model, including Euler-Lagrange equations of motion, physical parameters, and state-space representation.

- **Section IV** develops the sliding mode control framework, introduces the adaptive boundary layer mechanism ($\epsilon_{\text{eff}} = \epsilon_{\min} + \alpha|\dot{s}|$), and provides Lyapunov stability analysis with finite-time convergence guarantees.

- **Section V** describes the PSO-based parameter optimization methodology, including the chattering-weighted fitness function design, parameter space exploration, and convergence analysis yielding optimized values $\epsilon_{\min}^* = 0.0025$ and $\alpha^* = 1.21$.

- **Section VI** details the experimental setup, simulation parameters, Monte Carlo validation methodology, and statistical analysis procedures.

- **Section VII** presents comprehensive experimental results: baseline controller comparison (MT-5), adaptive boundary layer validation demonstrating 66.5% chattering reduction (MT-6), generalization failure analysis revealing 50.4× degradation (MT-7), and disturbance rejection failure under external perturbations (MT-8).

- **Section VIII** discusses the implications of our findings, compares results to literature, interprets the generalization failures, and proposes multi-scenario PSO as a solution.

- **Section IX** concludes with a summary of contributions, acknowledged limitations, and future research directions including multi-scenario robust optimization and hardware validation on physical DIP systems.

---

**Key Takeaway:** This work demonstrates that PSO-optimized adaptive boundary layers can achieve dramatic chattering reduction (66.5%) for nominal conditions but fail catastrophically (50.4× degradation) outside the training distribution, motivating future research on robust multi-scenario optimization and honest validation practices in the SMC community.
