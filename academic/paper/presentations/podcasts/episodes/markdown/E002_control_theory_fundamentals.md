# E002: Control Theory Foundations

## Introduction to Control Systems

Control theory is the mathematical framework for making systems behave the way we want. In this episode, we'll build from basic concepts to advanced sliding mode control - the foundation of this entire project.

## What is Control?

### The Fundamental Control Problem

**Goal**: Make a system's output track a desired reference, despite:
- Disturbances (external forces, noise)
- Uncertainties (model errors, parameter variations)
- Constraints (actuator limits, safety bounds)

**Example - Cruise Control:**
```
Desired: Maintain 65 mph
Disturbances: Hills, wind, road friction
Uncertainty: Vehicle mass (empty vs. loaded)
Constraints: Engine power limits
```

### Open-Loop vs. Closed-Loop Control

**Open-Loop** (No Feedback):
- Execute predetermined commands
- No correction for errors
- Example: Microwave timer (no temperature feedback)

**Closed-Loop** (Feedback):
- Measure output, compare to reference, adjust input
- Automatically corrects for disturbances
- Example: Thermostat (measures temperature, adjusts heating)

**For DIP**: Open-loop control is IMPOSSIBLE (unstable system requires continuous feedback)

## State-Space Representation

### Why State-Space?

Modern control theory uses state-space models instead of transfer functions because:
1. Handles multi-input, multi-output (MIMO) systems naturally
2. Works for nonlinear systems
3. Enables optimal control design
4. Direct physical interpretation

### General Form

**Continuous-Time:**
```
ẋ(t) = f(x(t), u(t), t)  # State dynamics
y(t) = h(x(t), u(t), t)  # Output equation
```

Where:
- `x(t)` = state vector (internal system variables)
- `u(t)` = control input
- `y(t)` = measured output
- `f(·)` = dynamics function
- `h(·)` = measurement function

### DIP State-Space Model

For the double-inverted pendulum:

**State Vector** (6 elements):
```
x = [x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂]ᵀ

Where:
  x   = cart position [m]
  θ₁  = first pendulum angle from vertical [rad]
  θ₂  = second pendulum angle from vertical [rad]
  ẋ   = cart velocity [m/s]
  θ̇₁  = first pendulum angular velocity [rad/s]
  θ̇₂  = second pendulum angular velocity [rad/s]
```

**Control Input** (1 element):
```
u = F [N]  # Horizontal force applied to cart
```

**Dynamics** (Simplified Linear Model):
```
M(q)q̈ + C(q,q̇)q̇ + G(q) = Bu
```

Where:
- `M(q)` = mass/inertia matrix (3×3)
- `C(q,q̇)` = Coriolis/centrifugal matrix
- `G(q)` = gravity vector
- `B` = input distribution matrix
- `q = [x, θ₁, θ₂]ᵀ` = generalized coordinates

**Code Implementation:**

From `src/plant/simplified_dip.py`:

```python
def compute_dynamics(self, state: np.ndarray, u: float) -> np.ndarray:
    """
    Compute state derivative: ẋ = f(x, u)

    Args:
        state: [x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂]
        u: control force [N]

    Returns:
        state_dot: [ẋ, θ̇₁, θ̇₂, ẍ, θ̈₁, θ̈₂]
    """
    # Extract positions and velocities
    x, theta1, theta2, x_dot, theta1_dot, theta2_dot = state

    # Compute mass matrix M(q)
    M = self._compute_mass_matrix(theta1, theta2)

    # Compute Coriolis + gravity terms
    h = self._compute_nonlinear_terms(theta1, theta2, theta1_dot, theta2_dot)

    # Input distribution
    B = np.array([1.0, 0.0, 0.0])  # Force applied to cart only

    # Solve for acceleration: q̈ = M⁻¹(Bu - h)
    q_ddot = np.linalg.solve(M, B * u - h)

    # Return full state derivative
    return np.array([x_dot, theta1_dot, theta2_dot,
                     q_ddot[0], q_ddot[1], q_ddot[2]])
```

## Stability Theory

### Lyapunov Stability

**Intuition**: A system is stable if, once near equilibrium, it stays near equilibrium.

**Mathematical Definition:**

An equilibrium point `x* = 0` is **stable** if:
```
∀ ε > 0, ∃ δ > 0 : ‖x(0)‖ < δ ⟹ ‖x(t)‖ < ε, ∀ t ≥ 0
```

Translation: Small initial deviations stay small forever.

**Asymptotic Stability**: Stable + converges to equilibrium:
```
‖x(0)‖ < δ ⟹ lim(t→∞) x(t) = 0
```

### Lyapunov's Direct Method

**Idea**: Find an "energy-like" function `V(x)` that:
1. Is positive definite: `V(x) > 0` for all `x ≠ 0`
2. Decreases along trajectories: `V̇(x) < 0`

**Physical Analogy**: A ball rolling in a bowl
- `V(x)` = potential energy (height)
- `V̇(x) < 0` = ball always moving downward
- Result: Ball settles to bottom (equilibrium)

**Mathematical Form:**

```
V(x) > 0           ∀ x ≠ 0  (positive definite)
V(0) = 0                     (zero at equilibrium)
V̇(x) = ∇V·f(x,u) < 0  ∀ x ≠ 0  (negative definite derivative)

⟹ System is globally asymptotically stable
```

### Quadratic Lyapunov Functions

Common choice for linear systems:

```
V(x) = xᵀPx

Where P is a positive definite matrix (all eigenvalues > 0)
```

**Derivative:**
```
V̇(x) = ẋᵀPx + xᵀPẋ = xᵀ(AᵀP + PA)x

For stability: Aᵀ P + PA = -Q (negative definite)
```

This is the **Lyapunov equation** - solved automatically in MATLAB/Python.

## Sliding Mode Control (SMC) Fundamentals

### What is Sliding Mode Control?

SMC is a **robust nonlinear control technique** that:
1. Defines a "sliding surface" in state space
2. Uses discontinuous control to drive states onto the surface
3. Maintains states on the surface (sliding motion)
4. Guarantees convergence to equilibrium

**Key Property**: Once on the sliding surface, the system is **insensitive to matched uncertainties** (disturbances in control channel).

### Two-Phase Design

**Phase 1 - Sliding Surface Design:**

Define a surface `s(x) = 0` such that `s(x) = 0` ⟹ desired behavior.

For DIP, we want angles → 0, so:
```
s(x) = k₁θ̇₁ + λ₁θ₁ + k₂θ̇₂ + λ₂θ₂
```

Where:
- `k₁, k₂` = velocity gains (derivative term)
- `λ₁, λ₂` = position gains (proportional term)

**Insight**: `s = 0` is a manifold in 6D state space. If `s = 0`, then:
```
k₁θ̇₁ + λ₁θ₁ = -( k₂θ̇₂ + λ₂θ₂)
```

This is a 1st-order ODE! Solution:
```
θ₁(t) = θ₁(0)exp(-λ₁t/k₁)
```

So angles decay exponentially with time constant `τ = k₁/λ₁`.

**Phase 2 - Reaching Law Design:**

Design control `u` to drive `s → 0` and keep it there.

**Reaching Law:**
```
ṡ = -η·sign(s) - ks

Where:
  η > 0: reaching gain (how fast to approach surface)
  k > 0: damping gain (prevents oscillation)
  sign(s) = +1 if s > 0, -1 if s < 0
```

**Control Law:**

Substitute `ṡ = (∂s/∂x)ẋ` and solve for `u`:
```
u = u_eq + u_sw

Where:
  u_eq = "equivalent control" (model-based, keeps s=0 if already there)
  u_sw = "switching control" (robust feedback, drives s→0)
```

### Code Implementation

From `src/controllers/smc/algorithms/classical/controller.py`:

```python
def compute_control(self, state: np.ndarray, state_vars: Any,
                   history: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute classical SMC control law.
    """
    # 1. Compute sliding surface
    surface_value = self._surface.compute(state)
    # s = k₁θ̇₁ + λ₁θ₁ + k₂θ̇₂ + λ₂θ₂

    # 2. Estimate surface derivative
    surface_derivative = self._estimate_surface_derivative(state)
    # ṡ ≈ k₁θ̈₁ + λ₁θ̇₁ + k₂θ̈₂ + λ₂θ̇₂

    # 3. Equivalent control (model-based feedforward)
    u_equivalent = self._equivalent.compute(state, self._surface,
                                           surface_derivative)

    # 4. Switching control (robust feedback)
    u_switching = self._boundary_layer.compute_switching_control(
        surface_value, self.config.K, surface_derivative
    )

    # 5. Derivative control (damping)
    u_derivative = -self.config.kd * surface_derivative

    # 6. Total control
    u_total = u_equivalent + u_switching + u_derivative

    # 7. Saturation
    u_saturated = np.clip(u_total, -self.config.max_force,
                         self.config.max_force)

    return {'u': float(u_saturated), ...}
```

### Boundary Layer Method

**Problem**: Discontinuous control `sign(s)` causes **chattering** (high-frequency oscillations) due to:
- Measurement noise
- Actuator dynamics
- Finite sampling time

**Solution**: Replace `sign(s)` with smooth approximation inside boundary layer `Φ`:

```
sign(s) → sat(s/Φ)

Where sat(s/Φ) = {  s/Φ       if |s| ≤ Φ
                  { sign(s)    if |s| > Φ
```

**Trade-off**:
- Large `Φ`: Smooth control, but reduces robustness (chattering ↓, accuracy ↓)
- Small `Φ`: More chattering, better tracking (chattering ↑, accuracy ↑)

**Typical Values**: `Φ = 0.1 - 0.5` for DIP

From `config.yaml`:
```yaml
controllers:
  classical_smc:
    boundary_layer: 0.3  # Increased from 0.02 for chattering reduction
```

## Super-Twisting Algorithm (STA)

### Limitations of Classical SMC

Classical SMC has 1st-order sliding: `s → 0` in finite time, but `ṡ ≠ 0` (discontinuous).

**Problem**: Switching still present in derivative, causes chattering.

### Higher-Order Sliding Modes

**Idea**: Make `s = ṡ = ṡ̈ = ... = s⁽ʳ⁻¹⁾ = 0` (r-sliding mode).

**2-Sliding Mode (STA)**: Ensure `s = 0` AND `ṡ = 0` simultaneously.

**Advantages**:
- Continuous control (chattering ↓ dramatically)
- Finite-time convergence
- Robust to Lipschitz disturbances

### STA Control Law

```
u = u₁ + u₂

Where:
  u̇₁ = -K₁·sign(s)                    # Integral term
  u₂ = -K₂·|s|^(1/2)·sign(s)         # Proportional term (with fractional power)
```

**Key Feature**: Fractional power `|s|^(1/2)` provides:
- Strong control when far from surface (`s` large)
- Gentle control when close to surface (`s` small)

**Gain Conditions** (for finite-time stability):

```
K₁ > 0, K₂ > 0

And for Lipschitz disturbances with constant L:
  K₂ > 2L
  K₁ > (K₂·L)/(K₂ - 2L)
```

### Code Implementation

From `src/controllers/smc/algorithms/super_twisting/twisting_algorithm.py`:

```python
def compute_twisting_control(self, s: float, dt: float) -> float:
    """
    Compute super-twisting control.

    Args:
        s: Sliding surface value
        dt: Time step [s]

    Returns:
        u: Control output
    """
    # Proportional term (continuous)
    u2 = -self.K2 * (abs(s) ** 0.5) * np.sign(s)

    # Integral term (continuous, updated via integration)
    self.u1_integral += -self.K1 * np.sign(s) * dt

    # Total control
    u = self.u1_integral + u2

    return u
```

## Adaptive Sliding Mode Control

### Motivation

**Problem**: Gain tuning is conservative
- Must choose gains large enough for worst-case disturbances
- Results in high control effort during nominal operation
- Inefficient actuator usage

**Solution**: Adapt gains based on real-time sliding surface magnitude:
```
K̇ = γ·|s|  when |s| > ε (dead zone)
K̇ = 0      when |s| ≤ ε
```

Where:
- `γ` = adaptation rate
- `ε` = dead zone (prevent wind-up from noise)

### Adaptation Law Derivation

**Goal**: Ensure Lyapunov stability while adapting.

**Lyapunov Function:**
```
V = (1/2)s² + (1/2γ)(K - K*)²

Where K* = unknown ideal gain
```

**Derivative:**
```
V̇ = s·ṡ + (1/γ)(K - K*)·K̇

Choose K̇ = γ·|s|·sign(s²) = γ·|s|  (always positive)

Then: V̇ = s·ṡ + (K - K*)·|s|
```

If `ṡ = -K·|s|·sign(s)` and `K > K*`:
```
V̇ = s·(-K·|s|·sign(s)) + (K - K*)·|s|
  = -K·|s|² + (K - K*)·|s|
  = -K*·|s|² < 0  ✓
```

### Practical Adaptive Law

From `src/controllers/smc/algorithms/adaptive/adaptation_law.py`:

```python
def update_gains(self, s: float, dt: float) -> None:
    """
    Update adaptive gains based on sliding surface.

    Args:
        s: Sliding surface value
        dt: Time step [s]
    """
    s_abs = abs(s)

    # Dead zone (prevent noise-induced wind-up)
    if s_abs > self.dead_zone:
        # Increase gain when outside dead zone
        self.K1 += self.gamma1 * s_abs * dt
        self.K2 += self.gamma2 * s_abs * dt
    else:
        # Leak gains when inside dead zone (prevent ratcheting)
        self.K1 *= (1 - self.leak_rate * dt)
        self.K2 *= (1 - self.leak_rate * dt)

    # Enforce bounds
    self.K1 = np.clip(self.K1, self.K_min, self.K_max)
    self.K2 = np.clip(self.K2, self.K_min, self.K_max)
```

**Key Features:**
1. **Dead Zone**: Prevents adaptation from noise (`|s| < ε`)
2. **Gain Leak**: Prevents "ratcheting" (gains increasing indefinitely)
3. **Bounded Adaptation**: Enforces `K_min ≤ K ≤ K_max`

## Robustness Properties

### Matched vs. Unmatched Uncertainties

**Matched Uncertainties** (in control channel):
```
ẋ = f(x) + (B₀ + ΔB)u + Bd

Where:
  ΔB = model error in input matrix
  d = disturbance in control channel
```

**SMC Property**: Complete rejection of matched uncertainties once on sliding surface!

**Proof Sketch:**
On sliding surface `s = 0`:
```
ṡ = 0 = (∂s/∂x)[f(x) + Bu + Bd]

Solve for u:
u_eq = -(∂s/∂x·B)⁻¹(∂s/∂x·f(x))

The disturbance d cancels out in ṡ = 0 equation!
```

**Unmatched Uncertainties** (not in control channel):
```
ẋ = f(x) + d_unmatched + Bu
```

SMC **cannot** perfectly reject these, but can attenuate them.

### Example: DIP with Mass Uncertainty

Suppose real cart mass is `M = M₀(1 + Δ)` where `|Δ| ≤ 0.2` (±20% error).

**Simulation from MT-6 Benchmark:**

| Controller | Nominal (Δ=0) | Perturbed (Δ=0.2) | Overshoot Increase |
|------------|---------------|-------------------|-------------------|
| Classical SMC | 4.2° | 5.8° | +1.6° |
| STA-SMC | 3.1° | 4.3° | +1.2° |
| Adaptive SMC | 3.8° | 4.1° | +0.3° |

**Conclusion**: Adaptive SMC most robust to parameter variations.

## Convergence Time Analysis

### Finite-Time Convergence

**Definition**: `x(t) = 0` for all `t ≥ T_f` where `T_f < ∞`.

**Contrast with Exponential Convergence**:
- Exponential: `‖x(t)‖ ≤ Ce^(-αt)` (never exactly zero, t→∞)
- Finite-time: `x(t) = 0` at finite time

### Classical SMC Convergence Time

For reaching law `ṡ = -η·sign(s)`:

```
|s(t)| = |s(0)| - η·t

Reaches s=0 at time: T_f = |s(0)|/η
```

**Example**: `s(0) = 0.5`, `η = 2.0` → `T_f = 0.25` seconds

### STA Convergence Time

For super-twisting with `ṡ = -K₁sign(s)` and `u₂ = -K₂|s|^(1/2)sign(s)`:

```
T_f ≤ (2|s(0)|^(1/2))/K₂ + 2K₂/K₁

Typically: T_f ~ 0.1 - 1.0 seconds for DIP
```

Faster than classical SMC for same gains!

## Common Pitfalls and Tips

### Pitfall 1: Derivative Explosion

**Problem**: Numerical differentiation amplifies noise.

```python
# BAD: Numerical derivative of noisy signal
s_dot = (s[k] - s[k-1]) / dt  # Noise amplified by 1/dt!
```

**Solution**: Use model-based derivative or filtering.

```python
# GOOD: Model-based estimate
s_dot = self._surface.compute_derivative(state, state_dot)

# ALTERNATIVE: Low-pass filter
s_dot_filtered = alpha * s_dot + (1-alpha) * s_dot_prev
```

### Pitfall 2: Gain Over-Tuning

**Problem**: Gains too large → excessive control effort, chattering.

**Rule of Thumb**:
- Start with small gains (K ~ 1-5)
- Increase gradually until performance acceptable
- Use PSO for final optimization

**From MT-8 Robust PSO Results:**
```yaml
# Before optimization (manual tuning)
classical_smc:
  gains: [5.0, 5.0, 5.0, 0.5, 0.5, 0.5]  # Conservative

# After PSO (optimal)
classical_smc:
  gains: [23.07, 12.85, 5.51, 3.49, 2.23, 0.15]  # +360% on some gains
```

### Pitfall 3: Ignoring Saturation

**Problem**: Design assumes unbounded control, but actuators saturate!

**Consequence**: Sliding surface may be unreachable if gains too high.

**Solution**: Include saturation in design, validate with simulations.

```python
# Always saturate control
u_saturated = np.clip(u_total, -max_force, max_force)

# Check for excessive saturation (diagnostic)
saturation_duty = np.mean(np.abs(u_history) > 0.95 * max_force)
if saturation_duty > 0.2:  # >20% of time saturated
    print("[WARNING] Excessive saturation, reduce gains")
```

### Tip 1: Start with Simplified Model

Linear model is much faster for PSO optimization:

```bash
# Fast PSO with simplified model (minutes)
python simulate.py --ctrl classical_smc --run-pso --save gains.json

# Validate with full nonlinear model (seconds)
python simulate.py --load gains.json --plot --use-full-dynamics
```

### Tip 2: Visualize Sliding Surface

Understanding `s(t)` is key to debugging control:

```python
# Plot sliding surface trajectory
plt.plot(t, s_history)
plt.axhline(y=0, color='r', linestyle='--', label='Target')
plt.axhline(y=boundary_layer, color='g', linestyle=':', label='Boundary Layer')
plt.axhline(y=-boundary_layer, color='g', linestyle=':')
plt.ylabel('Sliding Surface s(t)')
plt.xlabel('Time [s]')
plt.legend()
```

**Good behavior**: `s(t)` converges to zero and stays within boundary layer.
**Bad behavior**: `s(t)` oscillates or diverges → check gains!

## Summary and Key Takeaways

### Control Theory Fundamentals

1. **State-Space Models**: Standard form for modern control design
2. **Lyapunov Stability**: Energy-like functions prove convergence
3. **Feedback Control**: Essential for unstable systems like DIP

### Sliding Mode Control

1. **Two-Phase Design**: Surface design + reaching law
2. **Robustness**: Perfect rejection of matched uncertainties
3. **Finite-Time Convergence**: Reaches equilibrium in finite time
4. **Chattering**: Trade-off between robustness and smoothness

### Advanced Techniques

1. **Super-Twisting**: 2-SMC with continuous control
2. **Adaptive SMC**: Real-time gain adjustment
3. **Hybrid Controllers**: Combine multiple techniques

### Practical Implementation

1. **Boundary Layers**: Essential for chattering reduction
2. **Saturation Handling**: Must account for actuator limits
3. **Model-Based Components**: Improve performance but require accurate model

## Next Episode Preview

**E003: Plant Models and Dynamics** will cover:
- Lagrangian mechanics for DIP
- Simplified vs. full nonlinear models
- Mass matrix structure and singularities
- Coriolis and centrifugal terms
- Model validation and accuracy

## References

[1] Utkin, V., Guldner, J., & Shi, J. (2009). *Sliding Mode Control in Electro-Mechanical Systems*. CRC Press.

[2] Khalil, H. K. (2002). *Nonlinear Systems* (3rd ed.). Prentice Hall.

[3] Levant, A. (2005). Homogeneity approach to high-order sliding mode design. *Automatica*, 41(5), 823-830.

[4] Slotine, J. J. E., & Li, W. (1991). *Applied Nonlinear Control*. Prentice Hall.

---

**Episode Length**: ~1200 lines
**Reading Time**: 30-35 minutes
**Prerequisites**: Linear algebra, differential equations, basic control theory
**Next**: E003 - Plant Models and Dynamics
