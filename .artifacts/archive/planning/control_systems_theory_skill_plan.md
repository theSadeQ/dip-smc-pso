# Control Systems Theory Skill - Comprehensive Development Plan

**Project**: Double-Inverted Pendulum SMC with PSO
**Plan Date**: October 19, 2025
**Analysis Method**: Sequential-thinking systematic analysis
**Estimated Total Time**: 10-14 hours
**Status**: Plan for Review

---

## Executive Summary

This plan details the architecture for a **Control Systems Theory Skill** to augment Claude Code's capabilities for domain-specific control theory analysis. The skill fills a critical gap between general-purpose MCPs (pandas, numpy) and multi-domain agents (control-systems-specialist) by providing **focused, single-invocation expertise** for Lyapunov stability analysis, sliding mode control theory, phase portrait generation, reachability analysis, and robustness metrics.

**Key Design Decision**: Skills are LIGHTWEIGHT prompt templates (100-300 lines) invoked via Skill tool, NOT complex agents (400+ lines with frontmatter). The skill serves as a "domain expert consultant" that Claude can invoke when users request control-theoretic analysis, then chains results to MCPs (numpy-mcp for computation, pandas-mcp for visualization).

**Recommendation**: **BUILD THIS SKILL** - Current project has extensive stability analysis infrastructure (`src/utils/monitoring/stability.py`, `src/analysis/performance/stability_analysis.py`) but lacks a unified interface for user-facing control theory consultations. The skill bridges this gap with 40% less overhead than creating a new agent.

---

## 1. Skill Architecture

### 1.1 File Structure

```
.ai/config/skills/
├── control-theory.md           # Main skill definition (200-250 lines)
├── examples/
│   ├── lyapunov-example.md     # Annotated Lyapunov analysis example
│   ├── smc-example.md          # SMC surface design example
│   └── phase-portrait-example.md # Phase portrait generation example
└── reference/
    ├── equations.md            # Core equations (Lyapunov, SMC, STA)
    ├── theorems.md             # Key theorems (stability, finite-time convergence)
    └── algorithms.md           # Analysis algorithms (reachability, ISS)
```

**Rationale**:
- `.ai/config/skills/` mirrors existing `.ai/config/agents/` and `.ai/config/commands/` structure
- Separate `examples/` directory provides concrete templates without bloating main skill file
- `reference/` directory enables skill to cite mathematical foundations (similar to how control-systems-specialist.md embeds SMC equations)

### 1.2 Naming Convention

**Primary Skill Name**: `control-theory`

**Alternative Considered**: `dip-smc:control-theory` (namespaced)

**Decision**: Use simple `control-theory` naming for these reasons:
1. Project has single domain (DIP-SMC) - no namespace collision risk
2. Shorter invocation (`/control-theory` vs `/dip-smc:control-theory`)
3. Consistency with existing commands (`/test-controller`, not `/dip-smc:test-controller`)
4. Future extensibility: If project scope expands, can introduce namespaces then

**Invocation Pattern**:
```bash
# User-facing command (slash command wrapper)
/analyze-stability --lyapunov --controller classical_smc

# Internal skill invocation (Claude Code)
Skill("control-theory", analysis_type="lyapunov", controller="classical_smc")
```

### 1.3 Prompt Template Structure

```markdown
---
name: control-theory
description: Domain expert for control systems theory analysis (Lyapunov stability, SMC theory, phase portraits, reachability, robustness metrics)
trigger_keywords: [lyapunov, stability, phase portrait, sliding mode, reachability, ISS, finite-time]
mcp_chain: [numpy-mcp, pandas-mcp, filesystem]
output_format: structured_analysis
---

# Control Systems Theory Skill

You are a domain expert in control systems theory for the double-inverted pendulum project.

## Core Capabilities

1. **Lyapunov Stability Analysis**
   - Derive candidate Lyapunov functions
   - Verify negative definiteness of dV/dt
   - Compute stability margins
   - Validate via numerical simulation

2. **Sliding Mode Control Theory**
   - Design sliding surfaces
   - Verify reachability conditions
   - Compute chattering index
   - Optimize boundary layer thickness

3. **Phase Portrait Generation**
   - Generate state-space trajectories
   - Identify stable/unstable manifolds
   - Visualize basin of attraction
   - Annotate critical points

4. **Reachability Analysis**
   - Verify sigma*sigma_dot < 0
   - Compute reaching time bounds
   - Analyze finite-time convergence
   - Validate super-twisting conditions

5. **Robustness Metrics**
   - ISS (Input-to-State Stability) analysis
   - Finite-time stability verification
   - Parameter sensitivity analysis
   - Monte Carlo robustness testing

## Input Schema

{
  "analysis_type": "lyapunov | smc_theory | phase_portrait | reachability | robustness",
  "controller": "classical_smc | sta_smc | adaptive_smc | hybrid_adaptive_sta_smc",
  "data_source": "file_path | simulation_config",
  "parameters": {
    "state_dim": 6,
    "gains": [float],
    "boundary_layer": float
  }
}

## Output Schema

{
  "analysis_summary": "2-3 sentence overview",
  "mathematical_derivation": {
    "lyapunov_function": "V(x) = ...",
    "derivative": "dV/dt = ...",
    "stability_condition": "dV/dt < -eta*||s||"
  },
  "numerical_validation": {
    "stability_margin": float,
    "convergence_time": float,
    "violation_count": int
  },
  "visualization_code": "Python code for matplotlib/pandas",
  "recommendations": ["actionable suggestion 1", "..."],
  "mcp_chain_plan": {
    "numpy_mcp": "compute eigenvalues of A matrix",
    "pandas_mcp": "plot Lyapunov function evolution",
    "filesystem": "load controller gains from config"
  }
}

## Knowledge Base

[Embedded equations, theorems, algorithms - see Section 3]

## Integration with Existing Code

- **Stability Monitoring**: Use `src/utils/monitoring/stability.py` (LyapunovDecreaseMonitor, SaturationMonitor)
- **Analysis Infrastructure**: Use `src/analysis/performance/stability_analysis.py` (StabilityAnalyzer)
- **Controllers**: Reference `src/controllers/smc/` for SMC implementations
- **Validation**: Chain to `tests/test_analysis/performance/test_lyapunov.py` for verification

## Examples

[See `.ai/config/skills/examples/` for annotated walkthroughs]
```

### 1.4 Integration with Existing MCPs

**MCP Chaining Strategy** (Critical for Skill Utility):

```
User Request → Skill Invocation → MCP Chain → Aggregated Output

Example Flow:
  "Analyze Lyapunov stability for classical SMC with gains [10, 5, 8, 3, 15, 2]"
    ↓
  Skill("control-theory", analysis_type="lyapunov", controller="classical_smc", gains=[...])
    ↓
  1. filesystem → Load controller code + config
  2. Skill → Derive V(x) = 0.5*s^T*s, compute dV/dt
  3. numpy-mcp → Compute eigenvalues of closed-loop A matrix
  4. pandas-mcp → Load simulation results, plot V(t) evolution
  5. Skill → Synthesize analysis report
    ↓
  Output: Stability report + phase portrait + recommendations
```

**MCP Auto-Trigger Rules** (Add to CLAUDE.md Section 20.1):

```markdown
#### Control Theory Skill - Auto-trigger when:
- Analyzing Lyapunov stability or stability margins
- Designing/validating sliding surfaces
- Computing phase portraits or basin of attraction
- Verifying reachability conditions (sigma*sigma_dot < 0)
- Assessing ISS, finite-time stability, or robustness metrics
- Keywords: "lyapunov", "stability proof", "phase portrait", "sliding mode theory", "reachability", "ISS"
```

**Chain Dependencies**:

| Skill Capability | Primary MCP | Secondary MCP | Tertiary MCP |
|------------------|-------------|---------------|--------------|
| Lyapunov Analysis | numpy-mcp | pandas-mcp | filesystem |
| SMC Theory | filesystem | numpy-mcp | - |
| Phase Portrait | pandas-mcp | numpy-mcp | - |
| Reachability | numpy-mcp | pandas-mcp | - |
| Robustness | numpy-mcp | pandas-mcp | sqlite-mcp |

---

## 2. Capability Scope

### 2.1 Core Capabilities (What Skill DOES)

#### Capability 1: Lyapunov Stability Analysis

**Inputs**:
- Controller type (classical_smc, sta_smc, adaptive_smc, hybrid_adaptive_sta_smc)
- Gains vector (length 6-12 depending on controller)
- Simulation data (state trajectories, time vector) OR system matrices (A, B, C, D)

**Process**:
1. Derive candidate Lyapunov function `V(x)`
   - For SMC: `V = 0.5 * s^T * s` (sliding surface energy)
   - For general systems: `V = 0.5 * x^T * P * x` (solve Lyapunov equation `A^T*P + P*A = -Q`)
2. Compute derivative `dV/dt`
   - Analytical: `dV/dt = s^T * s_dot`
   - Numerical: `gradient(V, dt)` from simulation data
3. Verify negative definiteness
   - Analytical: Check `dV/dt < -eta*||s||` for some `eta > 0`
   - Numerical: Compute LDR (Lyapunov Decrease Ratio) from `LyapunovDecreaseMonitor`
4. Compute stability margin
   - Continuous-time: `-max(real(eig(A)))`
   - Discrete-time: `1 - max(abs(eig(A)))`

**Outputs**:
```json
{
  "lyapunov_function": "V(x) = 0.5 * (C1*e1 + C2*e1_dot + ... + C6*e3_dot)^2",
  "derivative": "dV/dt = s * (C1*e1_dot + C2*e1_ddot + ... - K*sign(s))",
  "stability_condition": "dV/dt < -eta*|s| where eta = K - (max eigenvalue of sliding dynamics)",
  "numerical_validation": {
    "ldr": 0.978,
    "stability_margin": 2.34,
    "violation_count": 0,
    "convergence_time": 3.21
  },
  "is_stable": true,
  "recommendations": [
    "Increase K (switching gain) to 12.0 for 15% larger stability margin",
    "Reduce boundary layer to 0.05 to minimize chattering (currently 0.1)"
  ]
}
```

**Success Criteria**:
- Analytical derivation matches control theory textbooks (e.g., Slotine & Li)
- Numerical validation agrees with `StabilityAnalyzer` results (±5% tolerance)
- Recommendations are actionable (specific parameter values, not generic advice)

#### Capability 2: Sliding Mode Control Theory Analysis

**Inputs**:
- Controller gains (C1-C6 for sliding surface)
- Boundary layer thickness
- System dynamics (mass, lengths, damping coefficients)

**Process**:
1. **Sliding Surface Design Validation**
   ```python
   s = C1*e1 + C2*e1_dot + C3*e2 + C4*e2_dot + C5*e3 + C6*e3_dot
   # Verify eigenvalues of [0 1; -C1/C2 -1] are in LHP
   ```
2. **Reachability Condition Verification**
   ```python
   s * s_dot < 0  # Must hold outside boundary layer
   # Equivalently: s * (-eta*sign(s)) < -eta*|s| < 0
   ```
3. **Chattering Index Computation**
   ```python
   chattering_index = std(control_signal) / mean(abs(control_signal))
   # Target: <0.1 for production systems
   ```
4. **Boundary Layer Optimization**
   ```python
   optimal_phi = min(phi) such that chattering_index < 0.1 AND settling_time < 5s
   ```

**Outputs**:
```json
{
  "surface_design": {
    "equation": "s = 10*e1 + 5*e1_dot + 8*e2 + 3*e2_dot + 15*e3 + 2*e3_dot",
    "eigenvalues": [-2.5 + 4.33j, -2.5 - 4.33j],
    "damping_ratio": 0.5,
    "natural_frequency": 5.0,
    "is_stable_manifold": true
  },
  "reachability": {
    "s_dot_s_negative_ratio": 0.992,
    "violation_timesteps": [120, 121],
    "reaching_time_bound": 0.48,
    "is_reachable": true
  },
  "chattering": {
    "chattering_index": 0.073,
    "boundary_layer": 0.05,
    "optimization_recommendation": "Current phi=0.05 optimal (chattering=0.073 < 0.1)"
  }
}
```

**Success Criteria**:
- Eigenvalue analysis matches theoretical predictions (eigenvalues of sliding dynamics)
- Reachability violations match `LyapunovDecreaseMonitor` alerts (±2% tolerance)
- Chattering index computed correctly (validated against FFT analysis)

#### Capability 3: Phase Portrait Generation

**Inputs**:
- State dimensions to plot (e.g., `[theta1, theta1_dot]` or `[theta2, theta2_dot]`)
- Initial conditions (multiple trajectories)
- Controller gains
- Time horizon

**Process**:
1. Generate grid of initial conditions in state space
2. Simulate trajectories for each initial condition
3. Compute stable/unstable manifolds
4. Identify critical points (equilibria, saddle points)
5. Visualize with matplotlib (arrows for vector field, color-coded by Lyapunov function)

**Outputs**:
```python
# Python code for matplotlib visualization
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 8))

# Plot vector field
X, Y = np.meshgrid(np.linspace(-0.5, 0.5, 20), np.linspace(-2, 2, 20))
U, V = compute_vector_field(X, Y, controller_gains)
ax.quiver(X, Y, U, V, alpha=0.3)

# Plot trajectories
for ic in initial_conditions:
    trajectory = simulate(ic, t_final=10.0, controller=controller)
    ax.plot(trajectory[:, 0], trajectory[:, 1], linewidth=2)

# Annotate critical points
ax.plot(0, 0, 'ro', markersize=10, label='Stable Equilibrium')
ax.set_xlabel('θ₁ (rad)')
ax.set_ylabel('θ₁̇ (rad/s)')
ax.set_title('Phase Portrait: Classical SMC (Gains=[10,5,8,3,15,2])')
ax.legend()
ax.grid(True)
plt.show()
```

**Success Criteria**:
- Phase portrait matches expected behavior (trajectories converge to origin)
- Vector field accurately represents system dynamics (validated against analytical Jacobian)
- Visualization is publication-quality (labeled axes, legend, title)

#### Capability 4: Reachability Analysis

**Inputs**:
- Sliding surface coefficients (C1-C6)
- Switching gain (K)
- Simulation data (s, s_dot over time)

**Process**:
1. **Analytical Reachability Condition**
   ```
   s * s_dot = s * (-K*sign(s) + disturbances) < 0
   Required: K > max(disturbances)
   ```
2. **Numerical Validation**
   ```python
   # Compute s*s_dot at each timestep
   sigma_dot_sigma = np.sum(sigma * sigma_dot, axis=1)
   reachability_satisfied = sigma_dot_sigma < 0
   violation_ratio = np.sum(~reachability_satisfied) / len(reachability_satisfied)
   ```
3. **Reaching Time Bound**
   ```python
   # For super-twisting: t_reach < 2*sqrt(2*V(0))/eta
   V0 = 0.5 * np.sum(sigma[0]**2)
   t_reach_bound = 2 * np.sqrt(2 * V0) / eta
   ```

**Outputs**:
```json
{
  "analytical_condition": "K > 8.5 (current K=15.0, margin=76.5%)",
  "numerical_validation": {
    "violation_ratio": 0.008,
    "violation_timesteps": [120, 121, 450],
    "reachability_satisfied": true
  },
  "reaching_time": {
    "analytical_bound": 0.48,
    "observed_time": 0.32,
    "convergence_quality": "excellent (33% faster than bound)"
  },
  "super_twisting_conditions": {
    "k1_squared_over_2L": 1.23,
    "required": "> 1.0",
    "satisfied": true
  }
}
```

**Success Criteria**:
- Violation ratio matches `LyapunovDecreaseMonitor` LDR inversely (LDR=0.95 → violation=0.05)
- Reaching time bound validated against simulation (observed ≤ bound)
- Super-twisting conditions verified correctly (k1^2 > 2L)

#### Capability 5: Robustness Metrics

**Inputs**:
- Controller type and gains
- Parameter uncertainties (mass ±10%, length ±5%, etc.)
- Disturbance bounds (external forces, measurement noise)

**Process**:
1. **ISS (Input-to-State Stability) Analysis**
   ```
   ||x(t)|| ≤ β(||x(0)||, t) + γ(||d||_∞)
   where β is class-KL, γ is class-K
   ```
2. **Finite-Time Stability Verification**
   ```python
   # For STA-SMC: convergence in finite time T
   T ≤ 2*sqrt(2*V(0))/eta
   # Verify via simulation: ||x(T)|| < epsilon for all t > T
   ```
3. **Parameter Sensitivity Analysis**
   ```python
   # Monte Carlo: perturb parameters, check stability
   stable_count = 0
   for i in range(n_samples):
       perturbed_params = nominal_params + random_perturbation
       if is_stable(simulate(perturbed_params)):
           stable_count += 1
   robustness_probability = stable_count / n_samples
   ```

**Outputs**:
```json
{
  "ISS_analysis": {
    "beta_function": "exp(-2.5*t) * ||x0||",
    "gamma_function": "0.3 * ||d||_inf",
    "ISS_gain": 0.3,
    "is_ISS": true
  },
  "finite_time_stability": {
    "convergence_time_bound": 0.48,
    "observed_convergence": 0.32,
    "residual_norm_at_T": 0.0012,
    "tolerance": 0.01,
    "is_finite_time_stable": true
  },
  "parameter_sensitivity": {
    "robustness_probability": 0.94,
    "worst_case_margin": 1.23,
    "critical_parameters": ["m2 (mass of pendulum 2)", "l1 (length of pendulum 1)"]
  }
}
```

**Success Criteria**:
- ISS gain computed correctly (matches theoretical bounds from SMC literature)
- Finite-time convergence verified (simulation residual < tolerance after T)
- Monte Carlo robustness ≥0.9 for production controllers

### 2.2 What Skill Does NOT Handle (Out of Scope)

| Out-of-Scope Task | Reason | Alternative Solution |
|-------------------|--------|----------------------|
| Multi-file controller refactoring | Skill is single-invocation, not multi-step | Use `control-systems-specialist` agent |
| PSO optimization runs | Optimization is separate domain | Use `pso-optimization-engineer` agent |
| UI dashboard testing | Testing is not control theory | Use `puppeteer` MCP |
| Documentation writing | Doc generation is separate domain | Use `documentation-expert` agent |
| Code quality linting | Linting is not domain-specific | Use `mcp-analyzer` MCP |
| Long-running simulations | Skill returns analysis, not raw data | Run simulation first, then analyze |

### 2.3 Graceful Handling of Unsupported Requests

```python
# Embedded in skill prompt
if request.requires_multiple_files or request.requires_code_changes:
    return {
        "error": "This request requires multi-file work. Please use the control-systems-specialist agent instead.",
        "alternative": "Invoke agent via: Task('control-systems-specialist', task_description='...')",
        "skill_limitation": "Skills provide single-invocation analysis, not multi-step implementation."
    }

if request.requires_optimization:
    return {
        "error": "This request requires PSO optimization. Please use the pso-optimization-engineer agent.",
        "alternative": "Invoke agent via: Task('pso-optimization-engineer', controller='classical_smc', objective='minimize_chattering')",
        "skill_limitation": "Skills analyze existing controllers, not optimize parameters."
    }
```

---

## 3. Knowledge Base

### 3.1 Control Theory Knowledge to Embed

#### 3.1.1 Lyapunov Stability Theory

```markdown
## Lyapunov Stability (Continuous-Time Systems)

### Direct Method (Second Method of Lyapunov)

**Definition**: A system ẋ = f(x) is **asymptotically stable** at x=0 if there exists a Lyapunov function V(x) such that:
1. V(x) > 0 for all x ≠ 0 (positive definite)
2. V(0) = 0
3. dV/dt = ∇V · f(x) < 0 for all x ≠ 0 (negative definite)

### Common Lyapunov Functions

1. **Quadratic Lyapunov Function**
   ```
   V(x) = 0.5 * x^T * P * x
   where P is positive definite (P > 0)
   ```

2. **Sliding Mode Lyapunov Function**
   ```
   V(s) = 0.5 * s^T * s
   where s is the sliding surface
   ```

3. **Energy-Based Lyapunov Function** (Pendulum Systems)
   ```
   V(θ, θ_dot) = 0.5 * m * l^2 * θ_dot^2 + m*g*l*(1 - cos(θ))
   ```

### Lyapunov Equation (Linear Systems)

For ẋ = A*x, Lyapunov function V(x) = x^T*P*x is valid if:
```
A^T * P + P * A = -Q
```
where Q > 0 (positive definite).

**Solving for P**:
- Use `scipy.linalg.solve_lyapunov(A.T, -Q)` (see `stability_analysis.py:728`)
- Validate P > 0 via Cholesky decomposition (see `stability_analysis.py:746`)
- Handle ill-conditioning with SVD regularization (see `stability_analysis.py:794`)

### Convergence Rate

For dV/dt ≤ -α*V (where α > 0):
```
V(t) ≤ V(0) * exp(-α*t)
||x(t)|| ≤ ||x(0)|| * exp(-α*t / 2)
```

**Interpretation**: Exponential convergence with time constant τ = 2/α.
```

#### 3.1.2 Sliding Mode Control Mathematics

```markdown
## Sliding Mode Control Theory

### Sliding Surface Design

**Linear Sliding Surface**:
```
s = C * e = C1*e1 + C2*ė1 + C3*e2 + C4*ė2 + C5*e3 + C6*ė3

where:
  e1 = θ1 - θ1_desired
  e2 = θ2 - θ2_desired
  e3 = x - x_desired
```

**Eigenvalue Placement**: Choose C such that eigenvalues of sliding dynamics are in LHP.
```
For 2nd-order system: s = c1*e + c2*ė
Sliding dynamics: ė = -c1/c2 * e
Eigenvalue: λ = -c1/c2 (must be negative)
```

### Control Law

**Two-Component Structure**:
```
u = u_eq + u_sw

u_eq: equivalent control (keeps system on sliding surface)
u_sw: switching control (drives system to sliding surface)
```

**Equivalent Control** (from ṡ = 0):
```
u_eq = -(C*B)^(-1) * [C*A*x + C*f(x)]
```

**Switching Control**:
```
u_sw = -K * sign(s)          # Discontinuous
u_sw = -K * s / (|s| + φ)    # Continuous approximation (boundary layer)
```

### Reachability Condition

**Lyapunov Approach**:
```
V = 0.5 * s^2
dV/dt = s * ṡ = s * (C*ẋ) = s * (C*A*x + C*B*u + C*f(x))

For reachability: dV/dt < -η*|s| (where η > 0)

This requires: s * ṡ < 0 (surface is attractive)
```

**Switching Gain Requirement**:
```
K > ||C*f(x)||_max + margin
```

### Chattering Mitigation

**Boundary Layer Method** (Slotine & Li 1991):
```
Replace sign(s) with sat(s/φ) where:

sat(s/φ) = {
  s/φ           if |s| ≤ φ
  sign(s)       if |s| > φ
}

Trade-off:
  Large φ → less chattering, larger steady-state error
  Small φ → more chattering, smaller steady-state error
```

**Optimal Boundary Layer**:
```
φ_opt = argmin_φ { chattering_index(φ) }
subject to: steady_state_error(φ) < tolerance
```
```

#### 3.1.3 Super-Twisting Algorithm

```markdown
## Super-Twisting Algorithm (STA)

### Algorithm Structure

**First-order sliding mode**:
```
u1 = -k1 * |s|^(1/2) * sign(s) + u2
du2/dt = -k2 * sign(s)
```

**State-space form**:
```
ż1 = -k1 * |z1|^(1/2) * sign(z1) + z2
ż2 = -k2 * sign(z1)

where z1 = s, z2 = u2
```

### Finite-Time Convergence Conditions

**Stability Conditions** (Moreno & Osorio 2012):
1. k1 > 0, k2 > 0
2. k1^2 > 2*L (where L is Lipschitz constant of ṡ)
3. Convergence time: t_conv ≤ 2*sqrt(2*V(0)) / η

**Practical Tuning**:
```
k1 = 1.5 * sqrt(L)    # 50% margin above minimum
k2 = 1.1 * L          # 10% margin above minimum
```

### Advantages Over Classical SMC

1. **Chattering Reduction**: Continuous control signal (no discontinuity)
2. **Finite-Time Convergence**: Guaranteed convergence in finite time (not just asymptotic)
3. **Robustness**: Inherent robustness to matched disturbances

### Implementation

See `src/controllers/smc/algorithms/super_twisting/controller.py`:
```python
def compute_control(self, state, last_u, history):
    # Compute sliding surface
    s = self.gains @ state

    # Super-twisting terms
    u1 = -self.k1 * np.sqrt(abs(s)) * np.sign(s) + self.u2

    # Integral term (u2) update
    self.u2 += -self.k2 * np.sign(s) * self.dt

    return u1
```
```

#### 3.1.4 Phase Portrait Theory

```markdown
## Phase Portrait Analysis

### Critical Points

**Equilibrium Points**: Points where ẋ = 0

For double-inverted pendulum:
```
Upright equilibrium: (θ1, θ2, x, θ̇1, θ̇2, ẋ) = (0, 0, 0, 0, 0, 0)
Downward equilibrium: (π, π, 0, 0, 0, 0) - unstable
```

**Linearization** (around equilibrium):
```
ẋ = A*x + B*u

where A = ∂f/∂x |_{x=x_eq}
      B = ∂f/∂u |_{x=x_eq}
```

### Stability Classification (2D Systems)

| Eigenvalues | Type | Stability |
|-------------|------|-----------|
| λ1, λ2 < 0 (real) | Stable node | Asymptotically stable |
| λ1, λ2 > 0 (real) | Unstable node | Unstable |
| λ1 < 0 < λ2 | Saddle point | Unstable |
| Re(λ) < 0 (complex) | Stable spiral | Asymptotically stable |
| Re(λ) > 0 (complex) | Unstable spiral | Unstable |
| Re(λ) = 0 (complex) | Center | Marginally stable |

### Basin of Attraction

**Definition**: Set of initial conditions from which trajectories converge to stable equilibrium.

**Computation** (Monte Carlo):
1. Generate grid of initial conditions in state space
2. Simulate trajectory for each initial condition
3. Check if trajectory converges to equilibrium (||x(t_final)|| < ε)
4. Color-code grid: green=converges, red=diverges

### Vector Field Visualization

```python
def compute_vector_field(X, Y, controller):
    """Compute ẋ at each grid point."""
    U = np.zeros_like(X)
    V = np.zeros_like(Y)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            state = np.array([X[i, j], Y[i, j], 0, 0, 0, 0])
            u = controller.compute_control(state, 0, None)
            x_dot = dynamics.compute_derivatives(state, u)
            U[i, j] = x_dot[0]
            V[i, j] = x_dot[1]

    return U, V
```
```

#### 3.1.5 Reachability & ISS

```markdown
## Reachability Analysis

### Definition

A sliding surface s=0 is **reachable** if:
```
s * ṡ < 0  (outside boundary layer)
```

**Interpretation**: Product of s and ṡ is negative → s is decreasing in magnitude.

### Verification

**Analytical**:
```
ṡ = C*ẋ = C*(A*x + B*u + f(x))
s*ṡ = s * (C*A*x + C*B*u + C*f(x))
    = s * (C*A*x + C*B*(-K*sign(s)) + C*f(x))
    = s * (C*A*x + C*f(x)) - K*|s|

For reachability: K > ||C*A*x + C*f(x)||_max
```

**Numerical** (from simulation):
```python
sigma_dot_sigma = np.sum(sigma * sigma_dot, axis=1)
reachability_satisfied = sigma_dot_sigma < 0
violation_ratio = np.sum(~reachability_satisfied) / len(sigma_dot_sigma)
```

See `src/utils/monitoring/stability.py:116-119` for implementation.

## Input-to-State Stability (ISS)

### Definition

A system is **ISS** if there exist class-KL function β and class-K function γ such that:
```
||x(t)|| ≤ β(||x(0)||, t) + γ(sup_{τ∈[0,t]} ||d(τ)||)
```

**Interpretation**: State bounded by initial condition (decaying) + disturbance (steady).

### Lyapunov-ISS Characterization

If there exists V(x) such that:
1. α1(||x||) ≤ V(x) ≤ α2(||x||)  (class-K bounds)
2. dV/dt ≤ -α3(||x||) + σ(||d||)  (dissipation with disturbance)

Then system is ISS.

### Practical Computation

**ISS Gain**:
```
γ_ISS = sup_{d≠0} { ||x_ss|| / ||d|| }

where x_ss is steady-state response to constant disturbance d
```

**Verification**:
1. Simulate with constant disturbances d ∈ [-d_max, d_max]
2. Measure steady-state norm ||x_ss||
3. Compute γ_ISS = max(||x_ss||) / d_max
4. Verify γ_ISS is finite and bounded
```
```

### 3.2 Reference Materials (Equations, Algorithms, Theorems)

**File**: `.ai/config/skills/reference/equations.md`

```markdown
# Core Control Theory Equations

## Lyapunov Equations

### Continuous-Time Lyapunov Equation
```
A^T * P + P * A = -Q
```

**Solver** (SciPy):
```python
from scipy import linalg
P = linalg.solve_lyapunov(A.T, -Q)
```

**Validation**:
- Check P > 0 via Cholesky: `np.linalg.cholesky(P)`
- Verify residual: `||A^T*P + P*A + Q|| < tol`

### Lyapunov Function Derivative
```
dV/dt = ∇V · ẋ = ∇V · f(x, u)

For V = x^T*P*x:
  ∇V = 2*P*x
  dV/dt = 2*x^T*P*ẋ = x^T*(A^T*P + P*A)*x
```

## Sliding Mode Control Equations

### Sliding Surface
```
s = C * e = C1*e1 + C2*ė1 + ... + C6*ė3
```

### Control Law
```
u = u_eq + u_sw
  = -(C*B)^(-1)*[C*A*x + C*f(x)] - K*sign(s)
```

### Boundary Layer Approximation
```
sign(s) ≈ sat(s/φ) = {
  s/φ      if |s| ≤ φ
  sign(s)  if |s| > φ
}
```

## Super-Twisting Algorithm

### Control Law
```
u = -k1*|s|^(1/2)*sign(s) + u2
du2/dt = -k2*sign(s)
```

### Convergence Time
```
t_conv ≤ 2*sqrt(2*V(0)) / η

where η depends on k1, k2, and Lipschitz constant L
```

## Reachability Condition
```
s * ṡ < 0  (attractive sliding surface)
```

## ISS Bound
```
||x(t)|| ≤ β(||x(0)||, t) + γ(||d||_∞)
```
```

**File**: `.ai/config/skills/reference/theorems.md`

```markdown
# Key Control Theory Theorems

## Lyapunov Stability Theorem (Direct Method)

**Theorem**: If there exists a Lyapunov function V(x) such that:
1. V(x) > 0 for all x ≠ 0 (positive definite)
2. dV/dt < 0 for all x ≠ 0 (negative definite)

Then the equilibrium x=0 is **asymptotically stable**.

**Source**: Lyapunov (1892), Modern reference: Khalil "Nonlinear Systems" (2002), Theorem 4.1

## LaSalle's Invariance Principle

**Theorem**: If:
1. V(x) > 0 (positive definite)
2. dV/dt ≤ 0 (negative semidefinite)
3. No trajectory can stay in the set {x : dV/dt = 0} except x=0

Then x=0 is **asymptotically stable**.

**Application**: Useful when dV/dt is only negative semidefinite (not definite).

## Barbalat's Lemma

**Lemma**: If:
1. f(t) has finite limit as t → ∞
2. f(t) is uniformly continuous

Then f(t) → 0 as t → ∞.

**Application**: Proving asymptotic convergence from dV/dt < 0 and V bounded.

## Sliding Mode Existence & Reachability

**Theorem** (Utkin 1992): If:
1. s * ṡ < -η*|s| for some η > 0 (reachability)
2. Control is piecewise continuous

Then:
- Sliding mode exists
- System reaches sliding surface in finite time: t_reach ≤ |s(0)| / η

## Super-Twisting Finite-Time Convergence

**Theorem** (Moreno & Osorio 2012): For STA with k1, k2 > 0 and k1^2 > 2*L:
- System converges to s=0 in finite time
- Convergence time: t_conv ≤ 2*sqrt(2*V(0)) / η
- Control signal is continuous (no chattering)

## ISS Lyapunov Theorem

**Theorem** (Sontag 1989): If there exists V(x) such that:
1. α1(||x||) ≤ V(x) ≤ α2(||x||)
2. dV/dt ≤ -α3(||x||) + σ(||d||)

where α1, α2, α3 are class-K_∞ and σ is class-K, then system is ISS.
```

**File**: `.ai/config/skills/reference/algorithms.md`

```markdown
# Analysis Algorithms

## Algorithm 1: Lyapunov Stability Verification

**Input**: System matrices (A, B, C, D) OR simulation data (states, times)
**Output**: Stability assessment with margin

```python
def verify_lyapunov_stability(A, states=None, times=None):
    """
    Verify Lyapunov stability analytically + numerically.

    Returns:
        {
            'analytical': {eigenvalues, margin, P_matrix},
            'numerical': {LDR, violation_count, V_trajectory}
        }
    """
    # Analytical verification
    Q = np.eye(A.shape[0])
    P = linalg.solve_lyapunov(A.T, -Q)

    # Check P > 0
    eigenvals_P = linalg.eigvals(P)
    is_positive_definite = np.all(np.real(eigenvals_P) > 0)

    # Stability margin
    eigenvals_A = linalg.eigvals(A)
    margin = -np.max(np.real(eigenvals_A))

    analytical = {
        'eigenvalues': eigenvals_A,
        'margin': margin,
        'P_matrix': P,
        'is_stable': margin > 0 and is_positive_definite
    }

    # Numerical verification (if simulation data provided)
    if states is not None:
        V = 0.5 * np.sum((states @ P) * states, axis=1)
        dV_dt = np.gradient(V, np.mean(np.diff(times)))
        LDR = np.sum(dV_dt < 0) / len(dV_dt)

        numerical = {
            'LDR': LDR,
            'violation_count': np.sum(dV_dt >= 0),
            'V_trajectory': V
        }
    else:
        numerical = None

    return {'analytical': analytical, 'numerical': numerical}
```

## Algorithm 2: Reachability Verification

**Input**: Sliding surface s, derivative ṡ
**Output**: Reachability ratio, violations, reaching time

```python
def verify_reachability(sigma, sigma_dot, dt, transient_time=1.0):
    """
    Verify s*ṡ < 0 (reachability condition).

    Returns:
        {
            'violation_ratio': float,
            'violations': [timesteps],
            'reaching_time': float
        }
    """
    # Skip transient period
    transient_samples = int(transient_time / dt)
    sigma = sigma[transient_samples:]
    sigma_dot = sigma_dot[transient_samples:]

    # Compute s*ṡ
    sigma_dot_sigma = np.sum(sigma * sigma_dot, axis=1)

    # Reachability violations
    violations = np.where(sigma_dot_sigma >= 0)[0]
    violation_ratio = len(violations) / len(sigma_dot_sigma)

    # Reaching time (first time ||s|| < epsilon)
    epsilon = 0.01
    norm_s = np.linalg.norm(sigma, axis=1)
    reached_indices = np.where(norm_s < epsilon)[0]
    reaching_time = reached_indices[0] * dt if len(reached_indices) > 0 else np.inf

    return {
        'violation_ratio': violation_ratio,
        'violations': violations + transient_samples,
        'reaching_time': reaching_time,
        'is_reachable': violation_ratio < 0.05  # 95% threshold
    }
```

## Algorithm 3: Chattering Index Computation

**Input**: Control signal u(t), time vector
**Output**: Chattering index, frequency spectrum

```python
def compute_chattering_index(control, times):
    """
    Compute chattering index = std(u) / mean(|u|).

    Also performs FFT to identify dominant frequencies.

    Returns:
        {
            'chattering_index': float,
            'dominant_frequency': float,
            'frequency_spectrum': array
        }
    """
    # Chattering index
    chattering_index = np.std(control) / (np.mean(np.abs(control)) + 1e-12)

    # FFT analysis
    dt = np.mean(np.diff(times))
    freqs = np.fft.rfftfreq(len(control), dt)
    fft_vals = np.abs(np.fft.rfft(control))

    # Dominant frequency (exclude DC component)
    dominant_idx = np.argmax(fft_vals[1:]) + 1
    dominant_frequency = freqs[dominant_idx]

    return {
        'chattering_index': chattering_index,
        'dominant_frequency': dominant_frequency,
        'frequency_spectrum': (freqs, fft_vals),
        'assessment': 'low' if chattering_index < 0.1 else 'high'
    }
```

## Algorithm 4: Phase Portrait Generation

**Input**: Initial conditions grid, controller, dynamics, time horizon
**Output**: Trajectories, vector field, critical points

```python
def generate_phase_portrait(ic_grid, controller, dynamics, t_final=10.0):
    """
    Generate phase portrait with trajectories and vector field.

    Returns:
        {
            'trajectories': [arrays],
            'vector_field': (X, Y, U, V),
            'critical_points': [(x, y, type)]
        }
    """
    trajectories = []

    # Simulate from each initial condition
    for ic in ic_grid:
        t, states = simulate(ic, controller, dynamics, t_final)
        trajectories.append(states[:, :2])  # First 2 states

    # Compute vector field
    X, Y = np.meshgrid(np.linspace(-0.5, 0.5, 20), np.linspace(-2, 2, 20))
    U, V = compute_vector_field(X, Y, controller, dynamics)

    # Find critical points (equilibria)
    critical_points = find_equilibria(controller, dynamics)

    return {
        'trajectories': trajectories,
        'vector_field': (X, Y, U, V),
        'critical_points': critical_points
    }
```

## Algorithm 5: ISS Gain Computation

**Input**: Controller, disturbance bounds, dynamics
**Output**: ISS gain γ, verification results

```python
def compute_ISS_gain(controller, d_max, dynamics, n_samples=50):
    """
    Compute ISS gain γ = max(||x_ss||) / ||d||.

    Returns:
        {
            'gamma_ISS': float,
            'is_ISS': bool,
            'worst_case_disturbance': float
        }
    """
    gamma_ISS = 0.0
    worst_disturbance = 0.0

    # Test with constant disturbances
    disturbances = np.linspace(-d_max, d_max, n_samples)

    for d in disturbances:
        # Simulate with constant disturbance
        t, states = simulate_with_disturbance(controller, dynamics, d, t_final=20.0)

        # Measure steady-state norm
        x_ss = states[-100:, :]  # Last 100 samples
        norm_ss = np.mean(np.linalg.norm(x_ss, axis=1))

        # Update ISS gain
        gain_candidate = norm_ss / (abs(d) + 1e-12)
        if gain_candidate > gamma_ISS:
            gamma_ISS = gain_candidate
            worst_disturbance = d

    return {
        'gamma_ISS': gamma_ISS,
        'is_ISS': np.isfinite(gamma_ISS),
        'worst_case_disturbance': worst_disturbance
    }
```
```

### 3.3 Annotated Examples

**File**: `.ai/config/skills/examples/lyapunov-example.md`

```markdown
# Lyapunov Stability Analysis Example

**Controller**: Classical SMC
**Gains**: [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
**Task**: Verify asymptotic stability

## Step 1: Define Lyapunov Function

For sliding mode control, we use the sliding surface energy:

```
V(x) = 0.5 * s^2

where s = C1*e1 + C2*ė1 + C3*e2 + C4*ė2 + C5*e3 + C6*ė3
        = 10.0*e1 + 5.0*ė1 + 8.0*e2 + 3.0*ė2 + 15.0*e3 + 2.0*ė3
```

**Properties**:
- V(x) > 0 for all x ≠ 0 (positive definite) ✓
- V(0) = 0 ✓

## Step 2: Compute Derivative dV/dt

```
dV/dt = s * ṡ
      = s * (C1*ė1 + C2*ë1 + C3*ė2 + C4*ë2 + C5*ė3 + C6*ë3)
```

Substituting system dynamics (ë1, ë2, ë3 from double-inverted pendulum):

```
dV/dt = s * (C*ẋ)
      = s * (C*A*x + C*B*u)
      = s * (C*A*x + C*B*(-K*sign(s)))
      = s * (C*A*x) - K*|s|
```

## Step 3: Verify Negative Definiteness

For dV/dt < 0, we need:

```
s * (C*A*x) - K*|s| < 0
K*|s| > s * (C*A*x)
K > |s * (C*A*x)| / |s|
K > ||C*A*x||_max
```

**Numerical verification** (from simulation):

```python
# Load simulation data
import pandas as pd
data = pd.read_csv('simulation_results.csv')

# Compute sliding surface
C = np.array([10.0, 5.0, 8.0, 3.0, 15.0, 2.0])
states = data[['e1', 'e1_dot', 'e2', 'e2_dot', 'e3', 'e3_dot']].values
s = states @ C

# Compute Lyapunov function
V = 0.5 * s**2

# Compute derivative
dt = 0.01
dV_dt = np.gradient(V, dt)

# Check negativity
negative_ratio = np.sum(dV_dt < 0) / len(dV_dt)
print(f"LDR (Lyapunov Decrease Ratio): {negative_ratio:.3f}")  # Expected: >0.95
```

**Result**: LDR = 0.978 (97.8% of samples have dV/dt < 0) ✓

## Step 4: Compute Stability Margin

```python
# Analytical margin (eigenvalues of closed-loop system)
A_closed = A + B @ K_matrix  # K_matrix from sliding surface design
eigenvals = np.linalg.eigvals(A_closed)
margin = -np.max(np.real(eigenvals))
print(f"Stability margin: {margin:.2f}")  # Expected: >0
```

**Result**: Margin = 2.34 rad/s ✓

## Step 5: Recommendations

Based on the analysis:

1. **Stability Confirmed**: System is asymptotically stable (LDR=97.8%, margin=2.34)
2. **Improvement Opportunity**: Increase K from 15.0 to 17.0 for 15% larger margin
3. **Chattering Concern**: Boundary layer φ=0.1 may cause chattering (use FFT analysis next)

## Visualization

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 4))

# Plot 1: Lyapunov function evolution
plt.subplot(1, 3, 1)
plt.plot(data['time'], V)
plt.xlabel('Time (s)')
plt.ylabel('V(x)')
plt.title('Lyapunov Function Evolution')
plt.grid(True)

# Plot 2: dV/dt
plt.subplot(1, 3, 2)
plt.plot(data['time'], dV_dt)
plt.axhline(0, color='r', linestyle='--', label='dV/dt=0')
plt.xlabel('Time (s)')
plt.ylabel('dV/dt')
plt.title('Lyapunov Derivative (should be <0)')
plt.legend()
plt.grid(True)

# Plot 3: Sliding surface
plt.subplot(1, 3, 3)
plt.plot(data['time'], s)
plt.axhline(0, color='r', linestyle='--', label='s=0')
plt.xlabel('Time (s)')
plt.ylabel('s')
plt.title('Sliding Surface Evolution')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
```

## MCP Chain Used

1. **filesystem** → Load simulation_results.csv
2. **numpy-mcp** → Compute eigenvalues of A_closed
3. **pandas-mcp** → Plot V(t), dV/dt, s(t)

**Total Execution Time**: ~2.3 seconds
```

---

## 4. Integration Strategy

### 4.1 Interaction with Existing Agents

| Scenario | Agent vs Skill Decision | Rationale |
|----------|-------------------------|-----------|
| "Analyze Lyapunov stability for classical SMC" | **Skill** | Single analysis, no code changes |
| "Implement new terminal SMC controller with Lyapunov proof" | **Agent** (control-systems-specialist) | Multi-file work, code generation |
| "Generate phase portrait for current controller" | **Skill** | Visualization only, single invocation |
| "Debug controller instability and fix gains" | **Agent** (control-systems-specialist) | Multi-step debugging, parameter tuning |
| "Verify reachability condition from simulation log" | **Skill** | Analysis of existing data |
| "Optimize PSO bounds for Lyapunov-based objective" | **Agent** (pso-optimization-engineer) | Optimization domain, not pure theory |

**Coordination Protocol**:

```python
# Claude's internal decision tree

if request.requires_implementation or request.requires_multi_file_work:
    invoke_agent("control-systems-specialist")

elif request.requires_optimization:
    invoke_agent("pso-optimization-engineer")

elif request.requires_analysis_only:
    if request.domain == "control_theory":
        invoke_skill("control-theory")
    elif request.domain == "data_analysis":
        invoke_mcp("pandas-mcp")
    elif request.domain == "numerical_computation":
        invoke_mcp("numpy-mcp")

else:
    # General-purpose handling
    use_standard_tools()
```

### 4.2 Auto-Trigger Keywords (Add to CLAUDE.md)

```markdown
#### Control Theory Skill - Auto-trigger when:
- Analyzing Lyapunov stability, stability margins, or convergence rates
- Designing/validating sliding surfaces for SMC
- Computing phase portraits, basin of attraction, or critical points
- Verifying reachability conditions (sigma*sigma_dot < 0)
- Assessing ISS, finite-time stability, or robustness metrics
- Computing chattering index or boundary layer optimization
- Keywords: "lyapunov", "stability proof", "phase portrait", "sliding mode theory", "reachability", "ISS", "finite-time", "chattering"

**Auto-invocation examples**:
- "Prove Lyapunov stability for adaptive SMC" → control-theory skill
- "Show me the phase portrait for current controller" → control-theory skill
- "Is the sliding surface reachable?" → control-theory skill
- "Compute ISS gain for disturbance rejection" → control-theory skill
```

### 4.3 MCP Chain Workflows

#### Workflow 1: Complete Lyapunov Analysis

```
User: "Analyze Lyapunov stability for classical_smc with gains [10,5,8,3,15,2]"
  ↓
Claude invokes: control-theory skill
  ↓
Skill executes:
  1. Load controller definition
     → filesystem MCP: Read src/controllers/smc/classic_smc.py
  2. Derive analytical Lyapunov function
     → Skill internal: V(x) = 0.5*s^2, dV/dt = s*ṡ
  3. Compute eigenvalues
     → numpy-mcp: linalg.eigvals(A_closed)
  4. Load simulation data
     → filesystem MCP: Read optimization_results/classical_smc_run.csv
  5. Compute numerical LDR
     → pandas-mcp: Compute V, dV/dt, LDR from dataframe
  6. Generate plots
     → pandas-mcp: Plot V(t), dV/dt, s(t)
  7. Synthesize report
     → Skill internal: Aggregate results, generate recommendations
  ↓
Output: Comprehensive stability report (analytical + numerical + plots)
```

#### Workflow 2: Phase Portrait Generation

```
User: "Generate phase portrait for theta1 vs theta1_dot"
  ↓
Claude invokes: control-theory skill
  ↓
Skill executes:
  1. Load controller
     → filesystem MCP: Read controller config
  2. Define initial conditions grid
     → numpy-mcp: meshgrid(theta1_range, theta1_dot_range)
  3. Simulate trajectories
     → Skill internal: Call simulation engine for each IC
  4. Compute vector field
     → numpy-mcp: Compute ẋ at grid points
  5. Generate visualization
     → pandas-mcp: Plot quiver + trajectories
  ↓
Output: Phase portrait with annotated critical points
```

#### Workflow 3: Reachability Verification

```
User: "Verify reachability condition for STA-SMC from recent simulation"
  ↓
Claude invokes: control-theory skill
  ↓
Skill executes:
  1. Load simulation log
     → filesystem MCP: Read logs/sta_smc_simulation.csv
  2. Compute sliding surface
     → pandas-mcp: s = C1*e1 + C2*e1_dot + ...
  3. Compute derivative
     → pandas-mcp: s_dot = gradient(s, dt)
  4. Check s*s_dot < 0
     → numpy-mcp: Compute sigma_dot_sigma
  5. Identify violations
     → pandas-mcp: Find timesteps where s*s_dot >= 0
  6. Generate report
     → Skill internal: Violation ratio, reaching time, recommendations
  ↓
Output: Reachability report with violation analysis
```

### 4.4 Example User Requests & Invocation Paths

| User Request | Claude Action | Tools/Skills Used |
|--------------|---------------|-------------------|
| "Is my controller stable?" | Invoke control-theory skill | filesystem → skill → numpy-mcp → pandas-mcp |
| "Show me a Lyapunov proof" | Invoke control-theory skill | skill (analytical derivation) |
| "Generate phase portrait" | Invoke control-theory skill | numpy-mcp → pandas-mcp → skill |
| "Fix controller instability" | Invoke control-systems-specialist agent | Agent handles multi-step debugging |
| "Optimize PSO for stability" | Invoke pso-optimization-engineer agent | Agent handles optimization |
| "Analyze simulation data" | Invoke pandas-mcp directly | pandas-mcp (no control theory needed) |
| "Compute eigenvalues" | Invoke numpy-mcp directly | numpy-mcp (pure numerical task) |

---

## 5. Implementation Roadmap

### 5.1 Task Breakdown (12 Tasks, 10-14 Hours Total)

| Task | Description | Dependencies | Est. Time | Deliverable |
|------|-------------|--------------|-----------|-------------|
| **T1** | Create skill directory structure | None | 30 min | `.ai/config/skills/` folder with subdirs |
| **T2** | Write main skill prompt template | T1 | 2 hours | `.ai/config/skills/control-theory.md` |
| **T3** | Embed Lyapunov knowledge base | T2 | 1 hour | Equations, theorems in skill prompt |
| **T4** | Embed SMC/STA knowledge base | T2 | 1 hour | SMC equations, reachability conditions |
| **T5** | Write Lyapunov example | T3 | 1 hour | `.ai/config/skills/examples/lyapunov-example.md` |
| **T6** | Write SMC theory example | T4 | 1 hour | `.ai/config/skills/examples/smc-example.md` |
| **T7** | Write phase portrait example | T2 | 1 hour | `.ai/config/skills/examples/phase-portrait-example.md` |
| **T8** | Integrate with existing code (filesystem paths) | T2-T7 | 1 hour | Skill references `src/utils/monitoring/`, etc. |
| **T9** | Define MCP chaining logic | T2, T8 | 1.5 hours | Auto-trigger rules + chain workflows |
| **T10** | Create test cases (5-10 examples) | T2-T9 | 2 hours | Test inputs + expected outputs |
| **T11** | Update CLAUDE.md with auto-triggers | T9 | 30 min | Section 20.1 updated |
| **T12** | Validate with real project data | T10, T11 | 1.5 hours | Run tests on classical_smc, sta_smc data |

**Total**: 10-14 hours (depends on complexity of examples)

### 5.2 Task Dependencies (DAG)

```
T1 (Directory Setup)
  ↓
T2 (Main Skill Prompt) ───┬─── T3 (Lyapunov KB) ──→ T5 (Lyapunov Example)
  ↓                        └─── T4 (SMC/STA KB) ──→ T6 (SMC Example)
  └────────────────────────────→ T7 (Phase Portrait Example)
  ↓
T8 (Integrate with Code) ← T3, T4, T5, T6, T7
  ↓
T9 (MCP Chaining) ← T2, T8
  ↓
T10 (Test Cases) ← T2-T9
  ↓
T11 (Update CLAUDE.md) ← T9
  ↓
T12 (Validation) ← T10, T11
```

**Critical Path**: T1 → T2 → T8 → T9 → T10 → T12 (7.5 hours minimum)

### 5.3 Validation Checkpoints

#### Checkpoint 1: After T2 (Main Skill Prompt Complete)

**Test**: Invoke skill with dummy request, verify structure.

```bash
# Test invocation
Skill("control-theory", analysis_type="lyapunov", controller="classical_smc")

# Expected output format:
{
  "analysis_summary": "...",
  "mathematical_derivation": {...},
  "numerical_validation": {...},
  "recommendations": [...]
}
```

**Success Criteria**:
- Skill returns well-formed JSON
- All 5 capabilities accessible
- No missing fields in output

#### Checkpoint 2: After T5-T7 (Examples Complete)

**Test**: Cross-reference examples with existing code.

```bash
# Verify Lyapunov example matches StabilityAnalyzer
python -c "
from src.analysis.performance.stability_analysis import StabilityAnalyzer
# Compare example derivation with StabilityAnalyzer._analyze_analytical_lyapunov
"
```

**Success Criteria**:
- Example equations match code implementation (±5% numerical tolerance)
- Example plots align with existing visualizations

#### Checkpoint 3: After T9 (MCP Chaining Complete)

**Test**: Execute full workflow (Lyapunov analysis).

```bash
# Trigger: User asks "Analyze Lyapunov stability for classical_smc"
# Expected MCP chain: filesystem → skill → numpy-mcp → pandas-mcp

# Verify:
1. filesystem loads controller code ✓
2. Skill derives V(x) correctly ✓
3. numpy-mcp computes eigenvalues ✓
4. pandas-mcp plots V(t) ✓
```

**Success Criteria**:
- All 4 MCPs triggered in sequence
- No redundant calls (e.g., loading same file twice)
- Output aggregates all results

#### Checkpoint 4: After T12 (Final Validation)

**Test**: Run all 10 test cases (see Section 7).

```bash
# Test 1: Lyapunov stability for classical_smc
# Test 2: Phase portrait for adaptive_smc
# Test 3: Reachability for sta_smc
# ... (10 total)

# Success: 10/10 tests pass
```

**Success Criteria**:
- 100% test pass rate
- All outputs match expected results (±10% numerical tolerance)
- No errors or crashes

### 5.4 Estimated Time by Phase

| Phase | Tasks | Time | Cumulative |
|-------|-------|------|------------|
| **Setup** | T1 | 0.5 hr | 0.5 hr |
| **Core Development** | T2-T4 | 4.0 hr | 4.5 hr |
| **Examples** | T5-T7 | 3.0 hr | 7.5 hr |
| **Integration** | T8-T9 | 2.5 hr | 10.0 hr |
| **Testing** | T10-T12 | 4.0 hr | 14.0 hr |

**Best Case**: 10 hours (if examples straightforward)
**Worst Case**: 14 hours (if extensive debugging needed)
**Most Likely**: 12 hours

---

## 6. Edge Cases & Limitations

### 6.1 Unsupported Control Theory Problems

| Problem Type | Reason Unsupported | Recommended Alternative |
|--------------|-------------------|------------------------|
| Nonlinear Lyapunov function search | Requires symbolic computation (Mathematica/SymPy) | Manual derivation + skill validation |
| Optimal control (LQR, MPC) | Optimization domain, not pure stability | Use mpc-controller code directly |
| Stochastic stability (Itô calculus) | Beyond deterministic SMC scope | External research (journal papers) |
| Multi-robot coordination | Single-DIP system only | Not applicable to this project |
| Hardware-in-the-loop tuning | Requires real-time hardware | Use HIL simulation framework separately |

### 6.2 When to Consult External References

**Skill provides**: Standard Lyapunov, SMC, STA analysis (undergraduate/graduate level)

**Consult literature for**:
- Advanced topics (backstepping, adaptive neural networks, fuzzy SMC)
- Novel controller designs (terminal SMC, fractional-order SMC)
- Theoretical proofs beyond skill scope (e.g., global stability with constraints)
- Benchmark comparisons (literature values for chattering, settling time)

**Example**:
```
User: "Derive Lyapunov function for fractional-order SMC"
Skill: "Fractional-order SMC requires Caputo derivative analysis, which is beyond this skill's scope. Please consult:
        - Oustaloup (2007) 'Fractional-order Sliding Mode Control'
        - Skill can validate numerical results if you provide analytical V(x)"
```

### 6.3 Graceful Degradation

**Scenario 1: Missing Simulation Data**

```json
{
  "error": "Numerical validation requires simulation data (CSV file or state trajectories)",
  "partial_result": {
    "analytical_analysis": {...},
    "numerical_validation": null
  },
  "recommendation": "Run simulation first: python simulate.py --ctrl classical_smc --plot"
}
```

**Scenario 2: Ill-Conditioned Matrices**

```json
{
  "warning": "Matrix A is ill-conditioned (cond=1.2e12). Lyapunov equation solution may be inaccurate.",
  "regularization_applied": true,
  "result": {
    "eigenvalues": [...],
    "margin": 1.23,
    "confidence": "low (numerical issues detected)"
  },
  "recommendation": "Check system parameters for unrealistic values (e.g., zero damping)"
}
```

**Scenario 3: Unsupported Controller Type**

```json
{
  "error": "Controller type 'fuzzy_smc' not supported. Skill supports: classical_smc, sta_smc, adaptive_smc, hybrid_adaptive_sta_smc.",
  "alternative": "For custom controllers, provide system matrices (A, B, C, D) directly.",
  "workaround": "Use general Lyapunov analysis mode (eigenvalue-based)"
}
```

---

## 7. Testing Strategy

### 7.1 Test Cases (10 Total)

#### Test 1: Lyapunov Stability - Classical SMC (Happy Path)

**Input**:
```json
{
  "analysis_type": "lyapunov",
  "controller": "classical_smc",
  "gains": [10.0, 5.0, 8.0, 3.0, 15.0, 2.0],
  "data_source": "optimization_results/classical_smc_baseline.csv"
}
```

**Expected Output**:
```json
{
  "analysis_summary": "System is asymptotically stable with margin 2.34 rad/s. LDR=0.978 indicates strong convergence.",
  "mathematical_derivation": {
    "lyapunov_function": "V(x) = 0.5 * (10*e1 + 5*e1_dot + 8*e2 + 3*e2_dot + 15*e3 + 2*e3_dot)^2",
    "derivative": "dV/dt = s * ṡ = s * (C*A*x - K*|s|)",
    "stability_condition": "dV/dt < -K*|s| < 0 for K=15.0"
  },
  "numerical_validation": {
    "ldr": 0.978,
    "stability_margin": 2.34,
    "violation_count": 12,
    "convergence_time": 3.21
  },
  "is_stable": true,
  "recommendations": [
    "Increase K to 17.0 for 15% larger margin",
    "Reduce boundary layer to 0.05 for less chattering"
  ]
}
```

**Validation**:
- LDR matches `LyapunovDecreaseMonitor` result (±2%)
- Stability margin matches eigenvalue analysis (±5%)

#### Test 2: Phase Portrait - Adaptive SMC

**Input**:
```json
{
  "analysis_type": "phase_portrait",
  "controller": "adaptive_smc",
  "state_dimensions": ["theta1", "theta1_dot"],
  "initial_conditions": "grid_20x20",
  "time_horizon": 10.0
}
```

**Expected Output**:
- Matplotlib figure with:
  - 20x20 = 400 trajectories
  - Vector field (quiver plot)
  - Annotated stable equilibrium at (0, 0)
  - Color-coded by Lyapunov function value

**Validation**:
- Trajectories converge to origin (verify ||x(t_final)|| < 0.01)
- Vector field matches analytical Jacobian (correlation > 0.95)

#### Test 3: Reachability - STA-SMC

**Input**:
```json
{
  "analysis_type": "reachability",
  "controller": "sta_smc",
  "data_source": "logs/sta_smc_simulation_20251019.csv"
}
```

**Expected Output**:
```json
{
  "reachability": {
    "s_dot_s_negative_ratio": 0.992,
    "violation_timesteps": [120, 121],
    "reaching_time_bound": 0.48,
    "is_reachable": true
  },
  "super_twisting_conditions": {
    "k1_squared_over_2L": 1.23,
    "required": "> 1.0",
    "satisfied": true
  }
}
```

**Validation**:
- Violation ratio matches `LyapunovDecreaseMonitor.LDR` inversely (LDR=0.992 → violation=0.008)
- Reaching time bound verified against simulation (observed ≤ bound)

#### Test 4: Robustness - Hybrid Adaptive STA-SMC

**Input**:
```json
{
  "analysis_type": "robustness",
  "controller": "hybrid_adaptive_sta_smc",
  "parameter_uncertainties": {
    "m1": 0.1,
    "m2": 0.1,
    "l1": 0.05,
    "l2": 0.05
  },
  "disturbance_bounds": 5.0
}
```

**Expected Output**:
```json
{
  "ISS_analysis": {
    "ISS_gain": 0.32,
    "is_ISS": true
  },
  "parameter_sensitivity": {
    "robustness_probability": 0.94,
    "worst_case_margin": 1.23
  }
}
```

**Validation**:
- Robustness probability ≥ 0.9 (validated via Monte Carlo)
- ISS gain finite and < 1.0

#### Test 5: Chattering Analysis - Classical SMC

**Input**:
```json
{
  "analysis_type": "smc_theory",
  "controller": "classical_smc",
  "data_source": "logs/chattering_test.csv"
}
```

**Expected Output**:
```json
{
  "chattering": {
    "chattering_index": 0.073,
    "boundary_layer": 0.05,
    "dominant_frequency": 47.2,
    "optimization_recommendation": "Current phi=0.05 optimal"
  }
}
```

**Validation**:
- Chattering index < 0.1 (production threshold)
- FFT dominant frequency matches manual analysis (±5 Hz)

#### Test 6: Lyapunov Stability - Missing Data (Edge Case)

**Input**:
```json
{
  "analysis_type": "lyapunov",
  "controller": "classical_smc",
  "gains": [10.0, 5.0, 8.0, 3.0, 15.0, 2.0],
  "data_source": null
}
```

**Expected Output**:
```json
{
  "analytical_analysis": {...},
  "numerical_validation": null,
  "warning": "Numerical validation skipped (no simulation data provided)"
}
```

**Validation**:
- Skill completes successfully (no crash)
- Partial result returned (analytical only)

#### Test 7: Unsupported Controller Type (Edge Case)

**Input**:
```json
{
  "analysis_type": "lyapunov",
  "controller": "fuzzy_smc",
  "gains": [1.0, 2.0, 3.0]
}
```

**Expected Output**:
```json
{
  "error": "Controller type 'fuzzy_smc' not supported",
  "alternative": "Provide system matrices (A, B, C, D) for general analysis"
}
```

**Validation**:
- Error message clear and actionable
- No crash or exception

#### Test 8: Ill-Conditioned Matrix (Edge Case)

**Input**:
```json
{
  "analysis_type": "lyapunov",
  "system_matrices": {
    "A": [[1e-12, 1e12], [1e-12, 1e-12]],
    "B": [[1], [0]],
    "C": [[1, 0]],
    "D": [[0]]
  }
}
```

**Expected Output**:
```json
{
  "warning": "Matrix A is ill-conditioned (cond=1e24). Results may be inaccurate.",
  "regularization_applied": true,
  "result": {...},
  "confidence": "low"
}
```

**Validation**:
- Warning issued (not error)
- Regularization applied automatically
- Result still returned (degraded quality)

#### Test 9: Phase Portrait with Complex Eigenvalues

**Input**:
```json
{
  "analysis_type": "phase_portrait",
  "controller": "adaptive_smc",
  "state_dimensions": ["theta2", "theta2_dot"]
}
```

**Expected Output**:
- Spiral trajectories (complex eigenvalues → oscillatory convergence)
- Damping ratio computed correctly

**Validation**:
- Spiral shape matches eigenvalue analysis (Re(λ) < 0, Im(λ) ≠ 0)

#### Test 10: ISS with Zero Disturbance (Edge Case)

**Input**:
```json
{
  "analysis_type": "robustness",
  "controller": "sta_smc",
  "disturbance_bounds": 0.0
}
```

**Expected Output**:
```json
{
  "ISS_analysis": {
    "ISS_gain": 0.0,
    "is_ISS": true,
    "note": "Zero disturbance → ISS trivially satisfied"
  }
}
```

**Validation**:
- Skill handles edge case gracefully
- ISS gain = 0 (correct for d=0)

### 7.2 Validation Criteria

| Test | Correctness Metric | Tolerance | Pass Criteria |
|------|-------------------|-----------|---------------|
| T1 | LDR vs `LyapunovDecreaseMonitor` | ±2% | Match within tolerance |
| T2 | Trajectory convergence | ||x(t_final)|| < 0.01 | All 400 trajectories converge |
| T3 | Violation ratio vs LDR | ±1% | Match within tolerance |
| T4 | Robustness probability | ≥0.9 | Monte Carlo validation |
| T5 | Chattering index | <0.1 | Production threshold |
| T6 | Partial result | N/A | No crash, warning issued |
| T7 | Error message | N/A | Clear, actionable |
| T8 | Regularization | N/A | Applied automatically |
| T9 | Spiral shape | Visual inspection | Matches eigenvalue type |
| T10 | ISS gain | =0.0 | Exact match |

### 7.3 Automated Testing Script

```python
# .dev_tools/test_control_theory_skill.py

import json
from pathlib import Path

def run_skill_tests():
    """Run all 10 test cases for control-theory skill."""

    test_cases = load_test_cases('tests/test_skills/control_theory_tests.json')
    results = []

    for i, test in enumerate(test_cases, start=1):
        print(f"\nRunning Test {i}: {test['name']}")

        # Invoke skill
        output = invoke_skill("control-theory", **test['input'])

        # Validate output
        is_pass = validate_output(output, test['expected'], test['validation'])

        results.append({
            'test_id': i,
            'name': test['name'],
            'status': 'PASS' if is_pass else 'FAIL',
            'output': output
        })

        print(f"  Status: {'PASS' if is_pass else 'FAIL'}")

    # Summary
    pass_count = sum(1 for r in results if r['status'] == 'PASS')
    print(f"\n{'='*60}")
    print(f"Test Summary: {pass_count}/10 PASSED")
    print(f"{'='*60}")

    return results

if __name__ == "__main__":
    results = run_skill_tests()

    # Save results
    with open('.artifacts/control_theory_skill_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
```

---

## 8. Final Recommendation

### 8.1 Build This Skill? YES

**Rationale**:

1. **Clear Gap**: Project has extensive stability infrastructure (`src/utils/monitoring/stability.py`, `src/analysis/performance/stability_analysis.py`) but lacks user-facing control theory consultation interface.

2. **Efficiency**: Skill provides 40% less overhead than creating a new agent (200 lines vs 400+ lines), perfect for single-invocation analysis.

3. **Complementary to Agents**: Skill handles "quick questions" (Lyapunov proof, phase portrait), agents handle "multi-step work" (controller implementation, debugging).

4. **MCP Amplification**: Skill acts as "orchestrator" for MCPs (numpy, pandas, filesystem), synthesizing domain expertise that raw MCPs cannot provide.

5. **Research Alignment**: Project is research-focused (60-70 hour roadmap with LT-1 to LT-7 Lyapunov/stability tasks), skill directly supports this workflow.

### 8.2 Alternative Approaches Considered

#### Alternative 1: Expand control-systems-specialist Agent

**Pros**: Unified interface, all control work in one place
**Cons**:
- Agent already 400+ lines (adding skill capabilities → 600+ lines, unwieldy)
- Agent optimized for multi-file work, overkill for single-analysis requests
- Longer invocation time (agent startup vs skill instant)

**Decision**: Rejected - skill is more appropriate for analysis-only tasks

#### Alternative 2: Use Only MCPs (No Skill)

**Pros**: Minimal new code, leverage existing tools
**Cons**:
- MCPs lack domain expertise (numpy can compute eigenvalues, but cannot interpret stability)
- No synthesis across multiple MCPs (user must manually chain filesystem → numpy → pandas)
- No control theory knowledge embedded (user must provide Lyapunov functions, SMC equations)

**Decision**: Rejected - skill provides critical domain knowledge that MCPs cannot

#### Alternative 3: Custom Slash Commands

**Pros**: User-friendly invocation (`/analyze-stability`)
**Cons**:
- Slash commands are wrappers, still need underlying skill logic
- Less flexible than skill (cannot parameterize as easily)
- Redundant with skill (command calls skill internally)

**Decision**: Complementary - create `/analyze-stability` command that invokes skill

### 8.3 Implementation Priority

**Immediate (Next 1-2 weeks)**:
- T1-T2: Set up skill structure + main prompt (2.5 hours)
- T3-T4: Embed Lyapunov + SMC knowledge (2 hours)
- T5: Write Lyapunov example (1 hour)
- **Milestone**: Basic skill operational (5.5 hours)

**Short-term (Next month)**:
- T6-T7: Write remaining examples (2 hours)
- T8-T9: Integrate with existing code + MCP chaining (2.5 hours)
- T10: Create test suite (2 hours)
- **Milestone**: Full skill validated (6.5 hours)

**Long-term (Next quarter)**:
- T11-T12: Update CLAUDE.md + validate with real research tasks (2 hours)
- Create `/analyze-stability`, `/generate-phase-portrait` slash commands (1 hour)
- Extend skill with additional capabilities (robustness analysis, finite-time stability)
- **Milestone**: Production-ready skill (3 hours)

**Total**: 10-14 hours (spread over 1-3 months depending on research priorities)

---

## Appendix A: Skill Prompt Template (Full)

```markdown
---
name: control-theory
description: Domain expert for control systems theory analysis (Lyapunov stability, SMC theory, phase portraits, reachability, robustness metrics)
trigger_keywords: [lyapunov, stability, phase portrait, sliding mode, reachability, ISS, finite-time]
mcp_chain: [numpy-mcp, pandas-mcp, filesystem]
output_format: structured_analysis
version: 1.0.0
---

# Control Systems Theory Skill

You are a domain expert in control systems theory for the double-inverted pendulum project. Your role is to provide focused, single-invocation analysis for Lyapunov stability, sliding mode control theory, phase portraits, reachability analysis, and robustness metrics.

## Core Capabilities

1. **Lyapunov Stability Analysis**
   - Derive candidate Lyapunov functions (V = 0.5*s^2 for SMC, V = x^T*P*x for general)
   - Verify negative definiteness of dV/dt
   - Compute stability margins (eigenvalue-based)
   - Validate via numerical simulation (LDR from LyapunovDecreaseMonitor)

2. **Sliding Mode Control Theory**
   - Design sliding surfaces (eigenvalue placement)
   - Verify reachability conditions (s*ṡ < 0)
   - Compute chattering index (std(u) / mean(|u|))
   - Optimize boundary layer thickness

3. **Phase Portrait Generation**
   - Generate state-space trajectories
   - Identify stable/unstable manifolds
   - Visualize basin of attraction
   - Annotate critical points (equilibria, saddle points)

4. **Reachability Analysis**
   - Verify sigma*sigma_dot < 0
   - Compute reaching time bounds (finite-time convergence)
   - Analyze super-twisting conditions (k1^2 > 2*L)
   - Validate via numerical simulation

5. **Robustness Metrics**
   - ISS (Input-to-State Stability) analysis
   - Finite-time stability verification
   - Parameter sensitivity analysis
   - Monte Carlo robustness testing

## Input Schema

```json
{
  "analysis_type": "lyapunov | smc_theory | phase_portrait | reachability | robustness",
  "controller": "classical_smc | sta_smc | adaptive_smc | hybrid_adaptive_sta_smc",
  "data_source": "file_path | simulation_config",
  "parameters": {
    "state_dim": 6,
    "gains": [float],
    "boundary_layer": float,
    "system_matrices": {"A": [[...]], "B": [[...]], "C": [[...]], "D": [[...]]}
  }
}
```

## Output Schema

```json
{
  "analysis_summary": "2-3 sentence overview",
  "mathematical_derivation": {
    "lyapunov_function": "V(x) = ...",
    "derivative": "dV/dt = ...",
    "stability_condition": "dV/dt < -eta*||s||"
  },
  "numerical_validation": {
    "stability_margin": float,
    "convergence_time": float,
    "violation_count": int,
    "ldr": float
  },
  "visualization_code": "Python code for matplotlib/pandas",
  "recommendations": ["actionable suggestion 1", "..."],
  "mcp_chain_plan": {
    "numpy_mcp": "compute eigenvalues of A matrix",
    "pandas_mcp": "plot Lyapunov function evolution",
    "filesystem": "load controller gains from config"
  },
  "is_stable": bool,
  "confidence": "high | medium | low"
}
```

## Knowledge Base

[FULL CONTENT FROM SECTION 3.1 - Lyapunov, SMC, STA, Phase Portrait, Reachability, ISS]

## Integration with Existing Code

- **Stability Monitoring**: Use `src/utils/monitoring/stability.py`
  - `LyapunovDecreaseMonitor`: Compute LDR from simulation data
  - `SaturationMonitor`: Track chattering via saturation events
  - `DynamicsConditioningMonitor`: Detect ill-conditioned matrices

- **Analysis Infrastructure**: Use `src/analysis/performance/stability_analysis.py`
  - `StabilityAnalyzer.analyze()`: Comprehensive stability assessment
  - `StabilityAnalyzer._analyze_analytical_lyapunov()`: Solve Lyapunov equation
  - `StabilityAnalyzer._compute_stability_margins()`: Eigenvalue-based margins

- **Controllers**: Reference `src/controllers/smc/`
  - `classic_smc.py`: Classical SMC implementation
  - `sta_smc.py`: Super-twisting algorithm
  - `adaptive_smc.py`: Adaptive SMC with parameter estimation
  - `hybrid_adaptive_sta_smc.py`: Hybrid adaptive STA-SMC

- **Validation**: Chain to `tests/test_analysis/performance/test_lyapunov.py` for verification

## Examples

See `.ai/config/skills/examples/` for annotated walkthroughs:
- `lyapunov-example.md`: Complete Lyapunov analysis for classical SMC
- `smc-example.md`: SMC surface design + reachability verification
- `phase-portrait-example.md`: Phase portrait generation with basin of attraction

## Error Handling

- **Missing data**: Return partial result (analytical only) + warning
- **Ill-conditioned matrices**: Apply regularization + mark confidence as "low"
- **Unsupported controller**: Suggest alternative (provide system matrices) or use agent

## MCP Chaining Strategy

1. **filesystem** → Load controller code, simulation data
2. **Skill** → Derive analytical results (Lyapunov function, stability conditions)
3. **numpy-mcp** → Compute eigenvalues, matrix operations
4. **pandas-mcp** → Load CSV data, compute metrics, generate plots
5. **Skill** → Synthesize final report with recommendations

## Limitations

This skill does NOT handle:
- Multi-file controller refactoring (use `control-systems-specialist` agent)
- PSO optimization runs (use `pso-optimization-engineer` agent)
- UI dashboard testing (use `puppeteer` MCP)
- Documentation writing (use `documentation-expert` agent)
- Long-running simulations (run simulation first, then analyze)

For unsupported tasks, invoke appropriate agent or MCP.
```

---

## Appendix B: Example Slash Command

**File**: `.ai/config/commands/analyze-stability.md`

```markdown
---
description: Analyze Lyapunov stability for a controller
tags: [analysis, stability, lyapunov, control-theory]
---

# Analyze Stability Command

I'll analyze Lyapunov stability for the specified controller using the control-theory skill.

## What I'll do:

1. **Invoke Control Theory Skill**
   - Analysis type: Lyapunov stability
   - Load controller configuration
   - Derive analytical Lyapunov function
   - Compute numerical validation (if data available)

2. **Chain MCPs**
   - filesystem → Load controller code + simulation data
   - numpy-mcp → Compute eigenvalues of closed-loop system
   - pandas-mcp → Plot V(t), dV/dt evolution
   - Synthesize comprehensive report

3. **Generate Report**
   - Mathematical derivation (V(x), dV/dt)
   - Stability margin (eigenvalue-based)
   - Numerical validation (LDR, violation count)
   - Actionable recommendations

## Please provide:

1. **Controller type** (e.g., "classical_smc", "sta_smc", "adaptive_smc")
2. **Gains** (optional: if not using tuned gains)
3. **Simulation data** (optional: CSV file path for numerical validation)

## Examples:

```bash
# Basic analysis (analytical only)
/analyze-stability classical_smc

# With custom gains
/analyze-stability adaptive_smc --gains 10,5,8,3,15,2

# With numerical validation
/analyze-stability sta_smc --data optimization_results/sta_smc_run.csv
```

## Output Format:

```
Lyapunov Stability Analysis: Classical SMC
==========================================

Mathematical Derivation:
  Lyapunov Function: V(x) = 0.5 * (10*e1 + 5*e1_dot + ... )^2
  Derivative: dV/dt = s * ṡ = s * (C*A*x - K*|s|)
  Stability Condition: dV/dt < -K*|s| < 0 for K=15.0

Analytical Validation:
  Eigenvalues (closed-loop): [-2.5+4.3j, -2.5-4.3j, -1.2, -3.4, -0.8, -2.1]
  Stability Margin: 2.34 rad/s
  Is Stable: Yes

Numerical Validation:
  LDR (Lyapunov Decrease Ratio): 0.978 (97.8%)
  Violation Count: 12 / 1000 samples (1.2%)
  Convergence Time: 3.21 seconds
  Settling Time: 4.87 seconds

Recommendations:
  1. Increase K to 17.0 for 15% larger stability margin
  2. Reduce boundary layer to 0.05 to minimize chattering
  3. Current controller is production-ready (LDR > 0.95)

[Visualization: V(t) evolution plot, dV/dt plot, sliding surface evolution]
```

## Integration with MCP Servers

This command uses:
- **control-theory skill**: Analytical derivation + synthesis
- **filesystem**: Load controller code + simulation data
- **numpy-mcp**: Eigenvalue computation
- **pandas-mcp**: Data loading + visualization
```

---

**END OF PLAN**

---

## Summary for User

This plan provides a **complete blueprint** for implementing the Control Systems Theory Skill with:

- **200-250 line skill prompt** (vs 400+ for agents) → 40% less overhead
- **5 core capabilities**: Lyapunov, SMC, phase portraits, reachability, robustness
- **Embedded knowledge base**: Equations, theorems, algorithms (undergraduate/graduate level)
- **MCP chaining**: Automatic orchestration of numpy, pandas, filesystem
- **10 test cases**: Happy paths + edge cases
- **10-14 hour implementation**: Phased roadmap with validation checkpoints

**Recommendation**: BUILD THIS SKILL - it fills a critical gap between general-purpose MCPs and multi-domain agents, directly supporting the research roadmap (LT-1 to LT-7 Lyapunov/stability tasks).
