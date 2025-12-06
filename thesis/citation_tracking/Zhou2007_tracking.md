# Citation Tracking: Zhou et al. (2007) - Adaptive Control With Backlash Nonlinearity

## Document Metadata

- **Authors**: Jing Zhou, Chengjin Zhang, and Changyun Wen
- **Title**: Robust Adaptive Output Control of Uncertain Nonlinear Plants With Unknown Backlash Nonlinearity
- **Publication**: IEEE Transactions on Automatic Control, Vol. 52, No. 3, March 2007
- **Pages**: pp. 503-509 (7 pages)
- **DOI**: 10.1109/TAC.2006.890473
- **Local Path**: `thesis/sources_archive/manuelly downloaded/zhou2007.pdf`

**Keywords**: Adaptive control, backstepping, backlash, nonlinear systems, stability, output feedback

---

## Quick Reference: Core Contributions

1. **Smooth backlash inverse** - Avoids chattering from nonsmooth inverse functions
2. **Output feedback control** - No state measurement required (observer-based)
3. **Adaptive backstepping** - Handles unknown backlash parameters (m, Br, Bl)
4. **Transient performance** - Explicit L₂ tracking error bounds
5. **Tuning functions** - Solves over-parametrization problem

**Key innovation**: Smooth inverse using χᵣ(u̇) and χₗ(u̇) functions instead of discontinuous indicator functions

---

## System Class and Problem Statement (Section II)

### System Model

**Nonlinear system** (Eq. 1-3, p. 503):
```latex
ẋ = Ax + ψ(y) + ∑ᵢ₌₁ʳ θᵢφᵢ(y) + bu          (1)
y = e₁ᵀx,   u = B(v)                         (2)
```

where:
```latex
A = [0   Iₙ₋₁]    b = [  0  ]    ψ(y) = [ψ₁(y)]
    [0    0  ]        [bₘ  ]            [ ⋮   ]
                      [ ⋮  ]            [ψₙ(y)]
                      [b₀ ]
```

**Backlash characteristic** (Eq. 4, p. 503):
```latex
u(t) = B(v) = {
  m(v(t) - Bᵣ),  if v̇(t) > 0 and u(t) = m(v(t) - Bᵣ)
  m(v(t) - Bₗ),  if v̇(t) < 0 and u(t) = m(v(t) - Bₗ)
  u(t),          otherwise
}                                             (4)
```

**Parameters**:
- m ≥ m₀ > 0: slope of backlash (unknown)
- Bᵣ > 0, Bₗ < 0: backlash width parameters (unknown)

**Cite for**:
- Backlash actuator model
- Output feedback control problem formulation
- Uncertain nonlinear systems with actuator nonlinearity

---

## Smooth Backlash Inverse (Section II.B)

### Proposed Inverse Function

**Smooth inverse** (Eq. 5-7, p. 504):
```latex
v = BI(u) = (1/m)u + Bᵣχᵣ(u̇) + Bₗχₗ(u̇)      (5)
```

where:
```latex
χᵣ(u̇) = e^(ku̇) / (e^(ku̇) + e^(-ku̇))        (6)

χₗ(u̇) = e^(-ku̇) / (e^(ku̇) + e^(-ku̇))       (7)
```

**Properties** (Eq. 8-9, p. 504):
```latex
χᵣ(u̇) → 1 as u̇ → ∞,   χᵣ(u̇) → 0 as u̇ → -∞
χₗ(u̇) → 0 as u̇ → ∞,   χₗ(u̇) → 1 as u̇ → -∞
```

**Key advantage**:
- Larger k → sharper transitions (closer to ideal inverse)
- Smooth and differentiable (avoids chattering)
- No sign function discontinuities

**Cite for**:
- Smooth inverse design for hysteresis/backlash
- Avoiding chattering in adaptive control
- Alternative to nonsmooth inverse indicator functions

---

### Backlash Reparametrization (Eq. 10-13, p. 505)

**Reformulated backlash**:
```latex
u(t) = σᵣ(t)m(v(t) - Bᵣ) + σₗ(t)m(v(t) - Bₗ) + σₛ(t)uₛ   (10)
```

where:
```latex
σᵣ(t) = {1, if u̇(t) > 0;  0, otherwise}      (11)
σₗ(t) = {1, if u̇(t) < 0;  0, otherwise}      (12)
σₛ(t) = {1, if u̇(t) = 0;  0, otherwise}      (13)
```

**Constraint**: σᵣ(t) + σₗ(t) + σₛ(t) = 1

**Adaptive inverse** (Eq. 14-15, p. 505):
```latex
v(t) = BI^(uₐ) = (1/m̂)[uₐ + m̂Bᵣχᵣ(u̇ₐ) + m̂Bₗχₗ(u̇ₐ)]   (14)

uₐ(t) = m̂v(t) - m̂Bᵣχᵣ(u̇ₐ) - m̂Bₗχₗ(u̇ₐ)                (15)
```

**Control error** (Eq. 16, p. 505):
```latex
u(t) - uₐ(t) = m̃v - m̃Bᵣχᵣ(u̇ₐ) - m̃Bₗχₗ(u̇ₐ) + dᵦ(t)   (16)
```

where m̃ = m - m̂, and dᵦ(t) is unparameterizable part

**Proposition** (p. 505): dᵦ(t) is bounded for all t ≥ 0
- Case 1 (σᵣ=1): |dᵦ(t)| ≤ m(Bᵣ - Bₗ)
- Case 2 (σₗ=1): |dᵦ(t)| ≤ m(Bᵣ - Bₗ)
- Case 3 (σₛ=1): |dᵦ(t)| ≤ m(Bᵣ - Bₗ + Bₛ)

**Cite for**:
- Adaptive backlash inverse design
- Bounded disturbance from inverse approximation
- Reparametrization for backstepping control

---

## State Estimation Filters (Section III)

### Observer Design

**State estimate** (Eq. 22, p. 505):
```latex
x̂(t) = ξ₀ + ∑ᵢ₌₁ʳ θᵢξᵢ + ∑ᵢ₌₀ᵐ bᵢηᵢ        (22)
```

**Filter dynamics** (Eq. 23-25, p. 505):
```latex
η̇ᵢ = A₀ηᵢ + eₙu,   i = 0,1,...,m           (23)
ξ̇₀ = A₀ξ₀ + ky + ψ(y) + χ                  (24)
ξ̇ᵢ = A₀ξᵢ + φᵢ(y),   i = 1,...,r           (25)
```

where A₀ = A - ke₁ᵀ has stable eigenvalues

**Estimation error**: ε = x(t) - x̂(t) satisfies ε̇ = A₀ε

**Reparametrized filters** (Eq. 26-27, p. 505):
```latex
ηᵢⱼ(t) = [qᵢⱼ(p)/Δ(p)]u(t),   i=0,...,m; j=1,...,n   (26)

u(t) = βᵀω̂(t) + dᵦ(t)                                  (27)
```

where β = [m, mBᵣ, mBₗ]ᵀ and ω̂(t) = [v, χᵣ(u̇ₐ), χₗ(u̇ₐ)]ᵀ

**Cite for**:
- Output feedback observer design
- Filter-based state estimation
- Reparametrization for adaptive control

---

## Adaptive Controller Design (Section IV)

### Backstepping Coordinates

**Change of variables** (Eq. 34, p. 506):
```latex
z₁ = y - yᵣ
zᵢ = β̂ᵀω̂ₘ₂⁽ⁱ⁻²⁾ - eŷᵣ⁽ⁱ⁻¹⁾ - αᵢ₋₁,   i=2,3,...,ρ
```

where ρ = n - m is the relative degree, αᵢ₋₁ is virtual control

### Smooth Function Design (Eq. 35, p. 506)

**To avoid sign function chattering**:
```latex
sgᵢ(zᵢ) = {
  zᵢ/|zᵢ|,                               if |zᵢ| ≥ δᵢ
  zᵢ/((δᵢ-zᵢ)ᵍ + |zᵢ|),                 if |zᵢ| < δᵢ
}

fᵢ(zᵢ) = {1, if |zᵢ| ≥ δᵢ;  0, if |zᵢ| < δᵢ}
```

where q = round[(ρ - i + 2)/2], ensuring (ρ - i + 1)th order differentiability

**Cite for**:
- Chattering avoidance in adaptive SMC
- Smooth approximation of sign function
- Differentiable control laws for backstepping

---

### Step 1: Tracking Error Dynamics (Eq. 36-43, p. 506)

**Virtual control** (Eq. 37-38, p. 506):
```latex
α₁ = êα̃₁                                                  (37)

α̃₁ = -(c₁ + b̂ₘ²/4)(|z₁| - δ₁)^ρ sg₁ - ξ₀₂
     - Θ̂ᵀφ(t) - D̂sg₁ - (δ₂ + 1)√(b̂ₘ² + δ₀) · sg₁    (38)
```

**Adaptation laws** (Eq. 41-43, p. 506):
```latex
β̇̂ᵢ = eᵢᵀτ,   i = 2,3                                    (41)
β̇̂₁ = Proj(e₁ᵀτ),   i = 1 (with projection)              (41)
τ = -sign(bₘ)ω̂ₘ₂(t)(|z₁| - δ₁)^ρ f₁ sg₁                 (42)
ė̂ = sign(bₘ)γₑ(1 + ẏᵣ)(|z₁| - δ₁)^ρ f₁ sg₁              (43)
```

**Lyapunov function** (Eq. 40, p. 506):
```latex
V₁ = 1/(ρ+1)(|z₁| - δ₁)^(ρ+1) f₁ + (1/2)|bₘ|β̃ᵀΓ_β⁻¹β̃
     + (1/2)Θ̃ᵀΓ_Θ⁻¹Θ̃ + |bₘ|/(2γₑ)ẽ² + 1/(2γ_d)D̃²
     + 1/(2l₁)εᵀPε
```

**Cite for**:
- First backstepping step for output feedback
- Adaptive parameter update laws
- Lyapunov-based stability analysis

---

### Step i (i = 2,...,ρ-1): Intermediate Steps (Eq. 46-52, p. 507)

**Virtual control** (Eq. 46, p. 507):
```latex
αᵢ = -(cᵢ + 1)(|zᵢ| - δᵢ)^(ρ-i+1) sgᵢ - gᵢ - (δᵢ₊₁ + 1) sgᵢ
     + (∂αᵢ₋₁/∂y)Θ̂ᵀφ + (∂αᵢ₋₁/∂y)β̂ᵀω̂ₘ₂(t)
     + ‖∂αᵢ₋₁/∂y‖² + δ₀ - D̂ sgᵢ + ...
```

**Adaptation updates** (Eq. 47-51, p. 507):
```latex
b̂̇ₘ = γᵦ(|z₁| - δ₁)^ρ f₁ sg₁ z₂                          (47)
D̂ᵢ = D̂ᵢ₋₁ - ‖∂αᵢ₋₁/∂y‖² + δ₀ - (|zᵢ| - δᵢ)^(ρ-i+1) fᵢ  (48)
Θᵢ = Θᵢ₋₁ - (∂αᵢ₋₁/∂y)φ(|zᵢ| - δᵢ)^(ρ-i+1) fᵢ sgᵢ       (49)
εᵢ = εᵢ₋₁ - (∂αᵢ₋₁/∂y)(|zᵢ| - δᵢ)^(ρ-i+1) fᵢ sgᵢe₂      (50)
βᵢ = βᵢ₋₁ - (∂αᵢ₋₁/∂y)ω̂ₘ₂(|zᵢ| - δᵢ)^(ρ-i+1) fᵢ sgᵢ     (51)
```

**Cumulative Lyapunov** (Eq. 52, p. 507):
```latex
Vᵢ = ∑ₖ₌₁ⁱ 1/(ρ-k+2)(|zₖ| - δₖ)^(ρ-k+2) fₖ
     + (1/2)|bₘ|β̃ᵀΓ_β⁻¹β̃ + (1/2)Θ̃ᵀΓ_Θ⁻¹Θ̃
     + (1/2)β̃ᵀΓ_β⁻¹β̃ + |bₘ|/(2γₑ)ẽ²
     + 1/(2γᵦ)b̃ₘ² + 1/(2l₁)εᵀPε
```

**Cite for**:
- Recursive backstepping design
- Tuning functions (avoiding over-parametrization)
- Virtual control law structure

---

### Step ρ: Final Control Law (Eq. 53-60, p. 507)

**Using smooth inverse**:
```latex
β̂ᵀω̂ₘ₂⁽ρ⁻¹⁾ = uₐ(t) + ω₀                                (53)

ω₀ = -(k₂p^(n-2) + ... + kₙ₋₁p + kₙ)I₃/(p^n + k₁p^(n-1) + ... + kₙ)ω̂(t)   (54)
```

**Derivative of zₚ** (Eq. 55, p. 507):
```latex
ż_ρ = uₐ + gₚ - (∂α_{ρ-1}/∂y)Θᵀφ - (∂α_{ρ-1}/∂y)βᵀω̂ₘ₂(t)
      - (∂α_{ρ-1}/∂Θ̂)Θ̇̂ - (∂α_{ρ-1}/∂D̂)Ḋ̂
      - (∂α_{ρ-1}/∂β̂)β̇̂ - (∂α_{ρ-1}/∂ξ₀)ξ̇₀
      - (∂α_{ρ-1}/∂y)d(t) - (∂α_{ρ-1}/∂y)ε₂
```

**Final Lyapunov** (Eq. 56, p. 507):
```latex
Vₚ = V_{ρ-1} + (1/2)(|z_ρ| - δₚ)² fₚ + 1/(2γ_d)D̃²
```

**Adaptation laws** (Eq. 57, p. 507):
```latex
Θ̇̂ = Γ_Θ τ_Θ,   β̇̂ = Γ_β τ_β,   Ḋ̂ = γ_d τ_D
```

**Design signal** (Eq. 58, p. 507):
```latex
χ = l₁P⁻¹τ_χₚ
```

**Final control** (Eq. 59-60, p. 507):
```latex
uₐ = α_ρ                                              (59)

v(t) = (1/m̂)[uₐ + m̂Bᵣχᵣ(u̇ₐ) + m̂Bₗχₗ(u̇ₐ)]           (60)
```

**Cite for**:
- Complete adaptive backstepping design
- Final control law with backlash inverse
- Parameter adaptation completion

---

## Stability and Performance (Theorem 1, p. 508)

### Main Result (Eq. 61-63, p. 508)

**Lyapunov derivative** (Eq. 61, p. 508):
```latex
V̇_ρ ≤ -∑ᵢ₌₁ᵖ cᵢ(|zᵢ| - δᵢ)^(2(ρ-i+1)) fᵢ - (1/l₁)εᵀε
```

**Theorem 1** (p. 508):
> All signals in the closed-loop system are bounded, and:
>
> 1. Asymptotic tracking: lim_{t→∞} |y(t) - yᵣ(t)| = δ₁
>
> 2. Transient performance (L₂ norm):

```latex
‖|y(t) - yᵣ(t)| - δ₁‖₂ ≤ (1/√(c₁))^(1/2) [
  (1/2)Θ̃(0)ᵀΓ_Θ⁻¹Θ̃(0) + |bₘ|/(2Γ_β)β̃(0)²
  + |bₘ|/(2γₑ)ẽ(0)² + 1/(2γ_d)D̃(0)²
  + 1/(2γᵦ)b̃ₘ(0)² + 1/(2l₁)ε(0)²
]^(1/2)                                               (63)
```

**Key features**:
- Tracking error converges to [-δ₁, δ₁]
- Explicit transient bound (function of initial errors)
- Tunable via c₁, γ_d, γₑ, γᵦ, Γ_β, Γ_Θ

**Cite for**:
- Adaptive control stability guarantees
- L₂ transient performance bounds
- Explicit design parameter effects

---

## Implementation Notes for DIP Thesis

### Comparison with Standard Approaches

**Traditional backlash compensation** [1]:
- Uses nonsmooth indicator functions
- May cause chattering in control signal
- Requires sign(v̇) which is discontinuous

**Zhou et al. 2007 approach**:
- Smooth χᵣ(u̇) and χₗ(u̇) functions
- Continuous and differentiable
- Tunable sharpness via parameter k

**Advantage for DIP**:
- Real hardware implementation (no chattering)
- Compatible with backstepping (needs differentiability)
- Works with output feedback (no state measurement)

---

### DIP-Specific Adaptations

**For 2-DOF DIP system** (arm angle θ₁, pendulum angle θ₂):

If backlash exists in motor actuator:
1. **System model** becomes:
   ```latex
   θ̈₁ = f₁(θ₁, θ₂, θ̇₁, θ̇₂) + g₁(θ₁, θ₂)u
   θ̈₂ = f₂(θ₁, θ₂, θ̇₁, θ̇₂) + g₂(θ₁, θ₂)u
   y = θ₂,   u = B(v)
   ```

2. **Backlash inverse**:
   ```latex
   v(t) = (1/m̂)[uₐ + m̂Bᵣχᵣ(u̇ₐ) + m̂Bₗχₗ(u̇ₐ)]
   ```

3. **State observer** for θ₁, θ̇₁, θ̇₂ (only θ₂ measured)

4. **Backstepping design** with virtual controls

**Parameter tuning**:
- k: Large (k ≈ 50-100) for sharp transitions
- δ₁: Small (δ₁ ≈ 0.01 rad) for tight tracking
- c₁, c₂: Balance speed vs. overshoot
- γ_d: Adapt to disturbance bound quickly

---

### Practical Considerations

**Advantages**:
1. **No backlash parameters needed** - All adapted online
2. **Output feedback** - Only angle measurement required
3. **Explicit performance** - Can predict tracking error bound
4. **No chattering** - Smooth control signal

**Limitations**:
1. **Ultimate bound** - Tracking to ±δ₁ (not zero)
2. **Relative degree** - Needs ρ = n - m known
3. **Parameter bounds** - Requires m ≥ m₀ (lower bound)
4. **Complexity** - More complex than simple PID

**When to use**:
- Real hardware with actuator backlash
- When state measurement unavailable/expensive
- When tight tracking required (δ₁ adjustable)
- When chattering must be avoided

---

## Key Equations Cross-Reference

| Equation | Page | Description | Use For |
|----------|------|-------------|---------|
| (4) | 503 | Backlash characteristic | Model definition |
| (5)-(7) | 504 | Smooth inverse BI(u) | Inverse design |
| (14)-(15) | 505 | Adaptive inverse | Controller |
| (16) | 505 | Control error u - uₐ | Error analysis |
| (22)-(25) | 505 | State observer | Output feedback |
| (34) | 506 | Backstepping coordinates | Design framework |
| (35) | 506 | Smooth functions sg, f | Avoid chattering |
| (37)-(38) | 506 | Virtual control α₁ | Step 1 design |
| (41)-(43) | 506 | Adaptation laws | Parameter update |
| (59)-(60) | 507 | Final control law | Implementation |
| (61) | 508 | Lyapunov derivative | Stability proof |
| (63) | 508 | L₂ performance bound | Transient analysis |

---

## Simulation Example (Section V, p. 508)

### Test System

**Plant** (Eq. 64, p. 508):
```latex
ẋ₁ = x₂
ẋ₂ = u + a(1 - e^(-x₁))/(1 + e^(-x₁))
y = x₁,   u = B(v)
```

**Parameters**:
- a = 1 (unknown)
- m = 1, Bᵣ = 0.5, Bₗ = -0.8 (unknown)
- Reference: yᵣ(t) = 10 sin(2.5t)

**Controller tuning**:
- c = 2, γₑ₀ = 1, δ₁ = 0.01, γ = 1
- c₁ = c₂ = c, γₐ = γ_d = γ, Γ_β = I₃
- Initial estimates: â(0) = 1.2, D̂(0) = 0.4, β̂(0) = [1, 0.4, 0.6]ᵀ
- Initial state: y(0) = 0.6

**Results** (Figs. 3-4, p. 509):
- **Tracking error**: Converges to ±0.01 rad (δ₁ bound)
- **Control v(t)**: Smooth, no chattering
- **Comparison**: Better than [10] (state feedback, disturbance treatment)

**Cite for**:
- Validation example
- Parameter tuning guidelines
- Performance comparison

---

## Related Work Connections

**From Zhou et al. 2007 references**:

1. **Tao & Kokotovic 1996** [1]: Adaptive control with actuator nonlinearities (uses nonsmooth inverse)
2. **Tao et al. 2001** [2]: Optimal decoupling control with backlash
3. **Ahmad & Khorrami 1999** [4]: Adaptive control with backlash (known intervals)
4. **Tao & Kokotovic 1995** [5]: Output backlash (bounded intervals)
5. **Corradini & Orlando 2002** [8]: Variable structure control (known bounds)
6. **Su et al. 2000** [9]: Robust adaptive (projection, residual tracking)
7. **Zhou et al. 2004** [10]: Backstepping with backlash (disturbance treatment)
8. **Krstic et al. 1995** [11]: Nonlinear adaptive control design (backstepping foundation)

**Thesis positioning**:
- Improves on [10] with smooth inverse (no chattering)
- Extends [11] backstepping to backlash nonlinearity
- No parameter bounds needed (unlike [4], [5], [6], [8])
- Output feedback (more practical than [10])

---

## Citation Templates

### For Adaptive Backlash Inverse

```latex
To compensate the unknown backlash nonlinearity, we employ
the smooth adaptive inverse proposed in \cite[Eq.~(14)]{Zhou2007},
which avoids chattering through continuous functions χᵣ and χₗ
instead of discontinuous indicator functions.
```

### For Output Feedback Design

```latex
Following the output feedback backstepping approach in
\cite[Section~IV]{Zhou2007}, we design a state observer
to estimate unmeasured states, enabling controller implementation
without full state measurement.
```

### For Transient Performance

```latex
The L₂ norm of the tracking error is explicitly bounded as a
function of design parameters \cite[Theorem~1, Eq.~(63)]{Zhou2007},
allowing systematic tuning to achieve desired transient performance.
```

### For Smooth Approximation

```latex
To avoid chattering caused by sign functions in backstepping,
we use the smooth approximation sgᵢ(zᵢ) from \cite[Eq.~(35)]{Zhou2007},
which is (ρ - i + 1)th order differentiable.
```

---

## BibTeX Entry

```bibtex
@article{Zhou2007,
  author    = {Jing Zhou and Chengjin Zhang and Changyun Wen},
  title     = {Robust Adaptive Output Control of Uncertain Nonlinear
               Plants With Unknown Backlash Nonlinearity},
  journal   = {IEEE Transactions on Automatic Control},
  volume    = {52},
  number    = {3},
  pages     = {503--509},
  month     = {March},
  year      = {2007},
  doi       = {10.1109/TAC.2006.890473}
}
```

---

## Summary: Why This Paper Matters for DIP Thesis

**Core value**:
1. **Smooth backlash compensation** - Critical for real hardware implementation
2. **Output feedback** - Practical (only angle measurement needed)
3. **No parameter knowledge** - All backlash parameters adapted online
4. **Explicit performance** - Can predict/guarantee tracking accuracy
5. **Chattering avoidance** - Smooth control suitable for real actuators

**Direct applications to DIP**:
- Motor backlash compensation (gear trains, couplings)
- Observer-based control (encoders only on output angles)
- Smooth control laws (compatible with real actuators)
- Systematic parameter tuning (explicit bounds)

**Theoretical contributions**:
- Smooth inverse design (Eqs. 5-7)
- Tuning functions (solves over-parametrization)
- L₂ transient bounds (Eq. 63)
- Backstepping with output feedback + backlash

**Comparison with thesis controllers**:
- **Classical SMC**: Assumes perfect actuator
- **Adaptive SMC**: Can handle backlash if added to uncertainty
- **This approach**: Explicitly compensates backlash structure

**Use if DIP hardware has**:
- Gear backlash in motor transmission
- Cable stretch/slack in pulley systems
- Actuator dead-zone or hysteresis

---

**File created**: 2025-12-06
**Status**: Complete - ready for thesis integration
**Note**: This is NOT a swing-up control paper (INDEX.md has incorrect description)
**Actual topic**: Adaptive output feedback control with backlash actuator nonlinearity
