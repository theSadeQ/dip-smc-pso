# Sliding Mode Control Theory

**Understanding the Mathematics and Principles of SMC**

This guide explains the theoretical foundations of sliding mode control, from basic principles to advanced algorithms. You'll learn why SMC works, how to prove stability, and when to use different SMC variants.

---

## Table of Contents

- [Sliding Mode Fundamentals](#sliding-mode-fundamentals)
- [Lyapunov Stability Theory](#lyapunov-stability-theory)
- [Chattering Analysis](#chattering-analysis)
- [Super-Twisting Mathematics](#super-twisting-mathematics)
- [Practical Design Guidelines](#practical-design-guidelines)

---

## Sliding Mode Fundamentals

### What is Sliding Mode Control?

Sliding mode control (SMC) is a **nonlinear control technique** that forces system trajectories to reach and stay on a pre-designed sliding surface. Once on the surface, the system exhibits desired dynamics regardless of uncertainties.

**Key Idea**: Instead of designing control to directly reach the target state, we:
1. Design a **sliding surface** where the system behaves well
2. Design control to **reach** the surface
3. Design control to **stay** on the surface (sliding mode)

### The Sliding Surface

For the double-inverted pendulum, the sliding surface is:

```
s = k₁θ₁ + k₂θ̇₁ + λ₁θ₂ + λ₂θ̇₂
```

Where:
- `θ₁, θ₂` are pendulum angles (error from vertical)
- `θ̇₁, θ̇₂` are angular velocities
- `k₁, k₂, λ₁, λ₂` are **design gains** (we choose these)

**Physical Meaning**:
- `s = 0`: System is on the sliding surface (good dynamics)
- `s > 0`: System is above the surface
- `s < 0`: System is below the surface

### Two Phases of SMC

**Phase 1: Reaching Phase**
- System starts away from surface (`s ≠ 0`)
- Control drives system toward surface
- Reaching condition: `s·ṡ < 0` (surface distance decreases)

**Phase 2: Sliding Mode**
- System reaches surface (`s = 0`)
- Control maintains system on surface
- Desired dynamics: determined by sliding surface design

### Why SMC for Underactuated Systems?

The double-inverted pendulum has:
- **3 degrees of freedom** (cart position, two pendulum angles)
- **1 control input** (horizontal force on cart)
- **Underactuated**: Fewer inputs than DOFs

SMC handles this because:
1. **Sliding surface** combines all states into one "virtual output"
2. **Reaching law** drives this virtual output to zero
3. **Equivalent control** maintains sliding mode despite underactuation

---

## Lyapunov Stability Theory

### Lyapunov Functions: Intuitive Explanation

A **Lyapunov function** is like an "energy" function that:
- Always ≥ 0 (zero only at equilibrium)
- Decreases along system trajectories
- Proves the system converges to equilibrium

**Analogy**: Rolling a ball into a bowl
- Lyapunov function = height of ball
- Equilibrium = bottom of bowl
- Stability = ball always rolls downward

### Lyapunov Function for SMC

For sliding mode control, we use:

```
V(s) = ½s²
```

**Why this function?**
- `V ≥ 0` always (s² is always positive)
- `V = 0` only when `s = 0` (on sliding surface)
- Simple and mathematically tractable

### Stability Proof

To prove stability, we need to show `V̇ < 0` (Lyapunov function decreases):

```
V̇ = d/dt(½s²) = s·ṡ
```

**Reaching Condition**: Design control so that `s·ṡ < 0`

This means:
- If `s > 0` (above surface), then `ṡ < 0` (moving down)
- If `s < 0` (below surface), then `ṡ > 0` (moving up)
- Either way, `s → 0` (converges to surface)

### Classical SMC Control Law

```
u = -(K·sign(s) + ε)
```

Where:
- `K > 0`: Switching gain (control authority)
- `sign(s)`: Discontinuous switching (`+1` or `-1`)
- `ε > 0`: Small constant for robustness

**Why it works**:
```
V̇ = s·ṡ = s·(dynamics + B·u)
   = s·dynamics - s·B·K·sign(s)
   ≈ -K|s|  (if K is large enough)
   < 0  (always negative, so s → 0)
```

### Finite-Time Convergence

Unlike linear control (exponential convergence), SMC achieves **finite-time convergence**:

```
Reaching time: T ≤ |s(0)| / K
```

**Practical Meaning**:
- Larger `K` → faster convergence
- System reaches surface in finite, predictable time
- Independent of initial error magnitude (for large enough K)

---

## Chattering Analysis

### What Causes Chattering?

**Chattering** = high-frequency oscillations in control signal

**Root Cause**: Discontinuous switching in `sign(s)` function
- System crosses surface → control switches
- Switches too fast → actuator can't keep up
- Results in oscillations around surface

**Problems Caused**:
1. **Actuator wear**: Mechanical stress from rapid switching
2. **Energy waste**: Constant acceleration/deceleration
3. **Unmodeled dynamics**: High-frequency excitation
4. **Practical infeasibility**: Real actuators have delays

### Boundary Layer Solution

**Key Idea**: Replace discontinuous `sign(s)` with continuous approximation inside a **boundary layer**

**Boundary Layer Definition**:
```
B_ε = {s : |s| ≤ ε}
```

Where `ε > 0` is the **boundary layer thickness**

**Continuous Switching Functions**:

1. **Saturation (linear in boundary layer)**:
   ```
   sat(s/ε) = {  s/ε    if |s| ≤ ε
              { sign(s)  if |s| > ε
   ```

2. **Hyperbolic tangent (smooth)**:
   ```
   tanh(s/ε) = (e^(s/ε) - e^(-s/ε)) / (e^(s/ε) + e^(-s/ε))
   ```

**Mathematical Properties**:
- **Outside boundary layer** (`|s| > ε`): Behaves like `sign(s)`
- **Inside boundary layer** (`|s| ≤ ε`): Smooth transition
- **At surface** (`s = 0`): Continuous control

### Trade-off: Accuracy vs Chattering

**Smaller `ε`** (thin boundary layer):
- ✅ Better tracking accuracy
- ❌ More chattering

**Larger `ε`** (thick boundary layer):
- ✅ Less chattering
- ❌ Reduced tracking accuracy (steady-state error)

**Practical Guideline**: Choose `ε` such that:
```
ε ≈ 0.01 to 0.1 (for normalized states)
```

### Adaptive Boundary Layer

For time-varying systems, use **adaptive boundary layer**:

```
ε_eff(t) = ε_0 + α|ṡ(t)|
```

Where:
- `ε_0`: Nominal thickness
- `α`: Adaptation rate
- `|ṡ|`: Magnitude of surface derivative

**Advantage**: Automatically adjusts to system dynamics
- High `ṡ` → thicker layer (more chattering reduction)
- Low `ṡ` → thinner layer (better accuracy)

---

## Super-Twisting Mathematics

### Why Super-Twisting?

**Limitation of Classical SMC**: Discontinuous control → chattering

**Super-Twisting Solution**:
- **Second-order sliding mode**: Makes `s = ṡ = 0`
- **Continuous control**: No discontinuous switching
- **Finite-time convergence**: Still faster than linear control

### Super-Twisting Algorithm (STA)

**Control Law**:
```
u = u₁ + u₂

u₁ = -α·|s|^(1/2)·sign(s)
u₂ = ∫(-β·sign(s)) dt
```

Where:
- `α, β > 0`: Super-twisting gains
- `u₁`: Continuous term (no `sign` in coefficient)
- `u₂`: Integral term (smooths control)

**Key Property**: `u` is **continuous** even though `sign(s)` appears, because:
- `|s|^(1/2)` → 0 as `s → 0` (term vanishes at surface)
- `u₂` integrates discontinuous term (integration → continuity)

### Lyapunov Stability for STA

**Lyapunov Function** (more complex than classical SMC):
```
V = 2α|s| + ½ζ²
```

Where `ζ = u₂ + α·|s|^(1/2)·sign(s)`

**Convergence Condition**:
If `α` and `β` satisfy:
```
β > (5α² + 4L) / (4α)
α > L
```

Where `L` is the Lipschitz constant of disturbances

Then: **Finite-time convergence** to `s = ṡ = 0`

### Parameter Selection Guidelines

**Step 1**: Estimate maximum disturbance magnitude `D`
**Step 2**: Set `α > D`
**Step 3**: Set `β > (5α² + 4D) / (4α)`

**Example** (for DIP system):
```
D ≈ 10 (max disturbance from model uncertainties)
α = 15
β = (5·15² + 4·10) / (4·15) = 20.8 → use β = 21
```

### Convergence Time Estimate

**Classical SMC**: `T ≈ |s(0)| / K`
**Super-Twisting**: `T ≈ 2|s(0)|^(1/2) / √(λ_min(P))`

Where `P` is Lyapunov function matrix

**Practical Observation**:
- STA slightly slower than classical SMC initially
- But smoother control (no chattering)
- Overall better practical performance

---

## Practical Design Guidelines

### Step-by-Step SMC Design

**Step 1: Design Sliding Surface**

Choose gains `k₁, k₂, λ₁, λ₂` for desired sliding dynamics:

```
s = k₁θ₁ + k₂θ̇₁ + λ₁θ₂ + λ₂θ̇₂ = 0
```

**Hurwitz Condition** (for stability on surface):
- `k₁, k₂, λ₁, λ₂ > 0` (all positive)
- For faster convergence: increase `k₁, λ₁` (position gains)
- For smoother response: increase `k₂, λ₂` (velocity gains)

**Step 2: Choose Controller Type**

| Scenario | Controller | Rationale |
|----------|-----------|-----------|
| Prototyping | Classical SMC | Simple, well-understood |
| Smooth control needed | Super-Twisting | No chattering |
| Unknown parameters | Adaptive SMC | Online tuning |
| Best performance | Hybrid Adaptive-STA | Combines all advantages |

**Step 3: Tune Parameters**

**Classical SMC**:
- Start with `K = 50` (switching gain)
- Increase `K` until convergence is fast enough
- Choose `ε = 0.01` to 0.05 (boundary layer)
- Reduce `ε` if tracking error is too large

**Super-Twisting**:
- Estimate disturbance bound `D`
- Set `α > D` (e.g., `α = 1.5D`)
- Set `β > (5α² + 4D)/(4α)`
- Fine-tune for smooth control

### Gain Selection: Pole Placement Analogy

The sliding surface `s = 0` defines dynamics:
```
k₁θ₁ + k₂θ̇₁ + λ₁θ₂ + λ₂θ̇₂ = 0
```

Rearranging:
```
θ̇₁ = -(k₁/k₂)θ₁ - (λ₁/k₂)θ₂ - (λ₂/k₂)θ̇₂
```

**Analogy to Linear Systems**: Like placing poles for:
- **Damping**: `ζ ≈ k₂/(2√(k₁))`
- **Natural frequency**: `ωₙ ≈ √(k₁)`

**Design Rules**:
- Want fast response → large `k₁, λ₁`
- Want smooth response → large `k₂, λ₂`
- Typically: `k₂/k₁ ≈ 0.7` to 1.0 (critical to slightly overdamped)

### Robustness Analysis

**SMC Advantages**:
1. **Insensitive to matched uncertainties**:
   - Uncertainties in control direction → rejected
   - Example: Actuator gain variations

2. **Bounds unmatched uncertainties**:
   - Uncertainties not in control direction → bounded error
   - Error proportional to boundary layer `ε`

3. **Finite-time convergence**:
   - Faster than exponential convergence
   - Predictable reaching time

**SMC Limitations**:
1. **Requires bounds on uncertainties**:
   - Need to know max disturbance `D`
   - For gain selection: `K > D/λ_min(B)`

2. **Chattering in classical SMC**:
   - Solved by boundary layer (accuracy trade-off)
   - Or use continuous SMC (STA, higher-order)

3. **Relative degree limitation**:
   - Control must directly affect sliding surface
   - DIP: OK (cart force affects pendulum angles)

### Comparison: Classical vs Super-Twisting

| Aspect | Classical SMC | Super-Twisting |
|--------|--------------|----------------|
| **Control** | Discontinuous | Continuous |
| **Chattering** | Yes (without boundary layer) | No |
| **Convergence** | Finite-time to `s=0` | Finite-time to `s=ṡ=0` |
| **Complexity** | Low (1 gain: K) | Medium (2 gains: α, β) |
| **Tuning** | Easier | Needs disturbance estimate |
| **Accuracy** | Good (with small ε) | Excellent (exact convergence) |
| **Best For** | Known systems, prototyping | Practical systems, research |

---

## Summary

**Key Takeaways**:

1. **SMC Principle**: Force system onto sliding surface where dynamics are good
2. **Lyapunov Proof**: `V = ½s²` decreases → convergence guaranteed
3. **Chattering**: Caused by discontinuous switching, solved by boundary layer or STA
4. **Super-Twisting**: Continuous control, finite-time to `s = ṡ = 0`
5. **Design Process**: Surface design → controller choice → parameter tuning

**Next Steps**:
- Apply theory in [Tutorial 02: Controller Comparison](../tutorials/tutorial-02-controller-comparison.md)
- Implement custom SMC using [Controllers API](../api/controllers.md)
- Deep dive into [SMC Complete Theory](../../mathematical_foundations/smc_complete_theory.md)

---

**Further Reading**:
- Utkin, V. I. (1992). *Sliding Modes in Control and Optimization*. Springer.
- Edwards, C., & Spurgeon, S. (1998). *Sliding Mode Control: Theory and Applications*. CRC Press.
- Shtessel, Y., et al. (2014). *Sliding Mode Control and Observation*. Birkhäuser.

---

**Last Updated**: October 2025
