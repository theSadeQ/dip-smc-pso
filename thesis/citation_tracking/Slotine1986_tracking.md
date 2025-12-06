# Citation Tracking: Slotine & Coetsee (1986) - Adaptive Sliding Controller Synthesis

## Document Metadata

- **Authors**: J.-J. E. Slotine and J. A. Coetsee
- **Title**: Adaptive sliding controller synthesis for non-linear systems
- **Publication**: International Journal of Control, Vol. 43, No. 6, 1986
- **Pages**: pp. 1631-1651 (21 pages)
- **DOI**: 10.1080/00207178608933564
- **Institution**: Massachusetts Institute of Technology, Cambridge, MA 02139, U.S.A.
- **Local Path**: `thesis/sources_archive/manuelly downloaded/slotine1986.pdf`

**Keywords**: Adaptive control, sliding mode control, boundary layer, parameter estimation, chattering reduction, on-line adaptation, robustness

---

## Quick Reference: Core Contributions

1. **Boundary layer concept** - Time-varying thickness Φ(t) to eliminate chattering
2. **Adaptive SMC** - On-line parameter estimation coupled with sliding control
3. **Balance conditions** - Quantify trade-off between tracking precision and uncertainty
4. **Consistent adaptation rule** - Stops adaptation when inside boundary layer
5. **Modulated adaptation rate** - γ(t) prevents high-frequency excitation

**Key innovation**: Distance to boundary layer (sₐ) serves as natural measure for parameter adaptation quality

---

## Problem Statement (Section 2.1, pp. 1632-1633)

### System Model

**Non-linear system** (Eq. 1, p. 1632):
```latex
x^(n)(t) = f(X; t) + b(X; t)u(t) + d(t)                    (1)
```

where:
- **X** = [x ẋ ... x^(n-1)]^T: state vector
- **u(t)**: control input
- **f(X; t)**: unknown function (imprecision bounded by F(X,t))
- **b(X; t)**: unknown control gain (constant sign, bounded)
- **d(t)**: bounded disturbance

**Bounds**:
```latex
|Δf| ≤ F  (Δf = f - f̂ is estimation error on f)           (6)
```

**Tracking objective**: x(t) → xₐ(t) = [xₐ ẋₐ ... xₐ^(n-1)]^T

**Cite for**:
- Problem formulation for uncertain nonlinear systems
- Bounded function approximation assumption
- Tracking control problem definition

---

### Sliding Surface Definition (Eq. 2-3, p. 1632)

**Time-varying sliding surface** s(t) = 0:
```latex
s(X; t) := (d/dt + λ)^(n-1) x̃,  λ > 0                     (3)
```

where x̃ = x - xₐ is tracking error

**Property**: Remaining on s(t) = 0 ⟹ tracking error x̃ ≡ 0 (linear differential equation)

**Sliding condition** (Eq. 4, p. 1632):
```latex
(1/2)(d/dt)s²(X; t) ≤ -η|s|                                (4)
```

where η > 0 is a positive constant

**Cite for**:
- Sliding surface design for tracking
- Interpretation of λ as control bandwidth
- Sliding condition for convergence

---

## Robust Sliding Control Without Adaptation (Section 2.2-2.3)

### Perfect Tracking with Switched Control (Example 1, pp. 1633-1634)

**For second-order system** ẍ = f + u:

**Sliding surface**:
```latex
s := (d/dt + λ)x̃ = ẋ̃ + λx̃                                (7)
```

**Continuous approximation** û:
```latex
û = -f̂ + ẍₐ - λẋ̃                                          (8)
```

**Discontinuous term** (Eq. 9, p. 1634):
```latex
u := û - k sgn(s)                                          (9)
```

**Choosing k** (Eq. 10, p. 1634):
```latex
k := F + η                                                 (10)
```

verifies sliding condition (4)

**Cite for**:
- Switched control law design
- Role of k in overcoming uncertainty
- Chattering from discontinuous control

---

### Boundary Layer Concept (Section 2.3, pp. 1636-1638)

**Smoothing discontinuity** in thin boundary layer:
```latex
B(t) = {X; |s(X; t)| ≤ Φ};  Φ > 0
```

where Φ is boundary layer **thickness**, ε = Φ/λ^(n-1) is boundary layer **width**

**Modified control gain** (Eq. 15, p. 1636):
```latex
k̃(X; t) := k(X; t) - Φ                                    (15)
```

**Control law** becomes:
```latex
u = û - k̃ sat(s/Φ)
```

where sat is saturation function

**Tracking precision** (Eq. 13, p. 1636):
```latex
|x̃^(i)(t)| ≤ (2λ)^i ε,  i = 0, ..., n-1                  (13)
```

**Key insight** (p. 1637): Variable s is the output of a **stable first-order filter** with:
- Input: disturbances d(t) and uncertainty Δf
- Dynamics: ṡ = -k̃(X; t)s/Φ + (Δf(X; t) + d(t))

**Cite for**:
- Boundary layer for chattering elimination
- Trade-off between precision and control activity
- Filter interpretation of sliding variable dynamics

---

## Balance Conditions (Eq. 18-25, pp. 1637-1639)

### Defining Boundary Layer Thickness

**Time-varying Φ(t)** from balance condition (Eq. 18-19, pp. 1637-1638):
```latex
k̃(Xₐ; t)/Φ := λ                                           (18)

Φ̇ + λΦ = k(Xₐ; t)                                         (19)
```

**Interpretation**: Closed-loop system mimics nth order critically damped system

**For β ≠ 1** (gain margin uncertainty), balance conditions become (Eq. 21-23, p. 1638):
```latex
k(Xₐ; t) ≥ λΦ/βₐ ⇒ Φ + λΦ = βₐk(Xₐ; t)                    (21)

k(Xₐ; t) ≤ λΦ/βₐ ⇒ Φ + λΦ/βₐ² = k(Xₐ; t)/βₐ              (22)

k̃(X; t) := k(X; t) - k(Xₐ; t) + λΦ/βₐ                    (23)
```

**Initial condition** (Eq. 24, p. 1638):
```latex
Φ(0) := βₐk(Xₐ(0); 0)/λ                                    (24)
```

**Physical interpretation** (Eq. 25, p. 1638):
```latex
λ^n ε ≈ βₐk(Xₐ; t)
```

i.e., **(bandwidth)^n × (tracking precision) ≈ (parametric uncertainty along desired trajectory)**

**Cite for**:
- Time-varying boundary layer design
- Quantitative trade-off between precision and uncertainty
- Design guideline for boundary layer thickness

---

## Adaptive Sliding Control (Section 3)

### Basic Adaptive Controller (Section 3.1, pp. 1639-1641)

**System with unknown parameters** (Eq. 26-27, p. 1639):
```latex
x^(n) + ∑ᵢ₌₁ʳ aᵢYᵢ = bu + d                                (26)

ẍ + a₁ẋ + a₂x² = bu + d                                    (27)
```

where aᵢ, b are unknown but constant, |d(t)| ≤ D

**Lyapunov function** (Eq. 28, p. 1640):
```latex
V(t) = (1/2)[sₐ² + b((ĥ₁ - a₁/b)² + (ĥ₂ - a₂/b)² + (b̂⁻¹ - b⁻¹)²)]  (28)
```

where:
```latex
sₐ := s - Φ sat(s/Φ)                                       (29)
```

is **measure of algebraic distance** to boundary layer

**Control law** (Eq. 30, p. 1640):
```latex
u := ĥ₁ẋ + ĥ₂x² - b̂⁻¹[u* + (D + η) sat(s/Φ)]              (30)
```

where:
```latex
u* := -ẍₐ + 2λẋ̃ + λ²x̃                                     (31)
```

**Adaptation laws** (Eq. 32-34, p. 1640):
```latex
ḣ₁ := -ẋsₐ                                                 (32)
ḣ₂ := -x²sₐ                                                (33)
ḃ⁻¹ := [u* + (D + η) sat(s/Φ)]sₐ                          (34)
```

**Lyapunov derivative** (Eq. 35-36, p. 1640):
```latex
V̇(t) = (-(D + η) sat(s/Φ) + d)sₐ                          (35)

V̇(t) ≤ -η|sₐ|                                             (36)
```

**outside boundary layer**

**Key feature**: Adaptation ceases inside boundary layer (sₐ = 0), avoiding long-term drift

**Cite for**:
- Basic adaptive SMC structure
- sₐ as error signal for adaptation
- Consistent adaptation rule (stops in boundary layer)

---

### Weighted Parameter Error (Eq. 37-42, pp. 1640-1641)

**Lyapunov rewritten** (Eq. 37-38, p. 1640):
```latex
V(t) = (1/2)(sₐ² + rₐ²)                                    (37)

rₐ² := b[(ĥ₁ - a₁/b)² + (ĥ₂ - a₂/b)² + (b̂⁻¹ - b⁻¹)²]      (38)
```

**Composite measure** of parameter error. Can assign weights (Eq. 39-42, p. 1641):
```latex
rₐ² := b[(ĥ₁ - a₁/b)²/h₁ₙ + (ĥ₂ - a₂/b)²/h₂ₙ + (b̂⁻¹ - b⁻¹)²/bₙ]  (39)

ḣ₁ = -h²₁ₙẋsₐ                                              (40)
ḣ₂ = -h²₂ₙx²sₐ                                             (41)
ḃ⁻¹ = b²ₙ[u* + (D + η) sat(s/Φ)]sₐ                        (42)
```

where h₁ₙ, h₂ₙ, bₙ weight the relative importance of each parameter

**Cite for**:
- Weighted adaptation for different parameter sensitivities
- Normalized adaptation gains

---

### General Case (Eq. 43-47, p. 1641)

**Sliding surface**:
```latex
s = (d/dt + λ)ⁿ(∫₀ᵗ x̃ dτ)                                  (43)
```

**Control law**:
```latex
u = ∑ᵢ₌₁ʳ ĥᵢYᵢ - b̂⁻¹[u* + (D + η) sat(s/Φ)]
```

with:
```latex
u* = -xₐ^(n) + ∑ᵢ₌₁ⁿ (ⁿᵢ)λⁱx̃^(n-i)                         (44)
```

**Lyapunov**:
```latex
V(t) = (1/2)[sₐ² + b(∑ᵢ₌₀ʳ (ĥᵢ - aᵢ/b)²/hᵢₙ + (b̂⁻¹ - b⁻¹)²/bₙ)]  (45)
```

**Estimation rules**:
```latex
ḣᵢ = -h²ᵢₙYᵢsₐ,  i = 0, ..., r                             (46)
ḃ⁻¹ = b²ₙ[u* + (D + η) sat(s/Φ)]                          (47)
```

**Cite for**:
- General nth order adaptive SMC
- Extension to multi-parameter systems
- Integral sliding surface for higher relative degree

---

### Stopping Adaptation (p. 1642)

**Upper bound on b**: If ĥb̂⁻¹ ≥ 1, stop adaptation on b̂

**Upper/lower bounds on hᵢ**: Resume adaptation when bounds violated

**Cite for**:
- Practical adaptation limits
- Preventing parameter drift
- Known bounds utilization

---

## Hybrid Adaptive Sliding Control (Section 3.2, pp. 1642-1643)

**System with fast and slow parameters** (p. 1642):
```latex
ẍ + a₁ẋ + a₂(t)x² = (b* · b_f)u + d
```

where:
- a₁, b*: unknown constant ('slow')
- a₂(t): time-varying but bounded ('fast')
- b_f = b_f(t): time-varying, estimated as b̂_f(t)

**Gain margin**:
```latex
1/β_f ≤ b̂_f(t)/b_f(t) ≤ β_f;  β_f = β ≥ 1                (48)
```

**Lyapunov with time-varying coefficient** (Eq. 49, p. 1642):
```latex
V(t) = (1/2)[γ(t)sₐ² + b*((ĥ₁ - a₁/b*)²/b* + (b̂*⁻¹ - b*⁻¹)²)]  (49)
```

where γ(t) > 0 will modulate adaptation rate

**Lyapunov derivative** (Eq. 50, p. 1642):
```latex
V̇ = (1/2)γ̇sₐ² + γsₐṡₐ + b*[(ĥ₁ - a₁/b*)ḣ₁ + (b̂*⁻¹ - b*⁻¹)(b̂*⁻¹)˙]  (50)
```

**Modified sliding variable** (p. 1642):
```latex
ṡ = ṡ - Φ̇ sgn(s)  outside boundary layer
ṡₐ = 0           inside boundary layer
```

**Adaptation law** (Eq. 53-54, p. 1643):
```latex
ḣ₁ = -γ(t)ẋsₐ                                              (53)

ḃ*⁻¹ = γ(t)[u* + (Δa₂x² + D + η - Φ̇) sat(s/Φ) + γ̇sₐ]sₐ  (54)
```

**Modulated adaptation rate** (Eq. 52, p. 1643):
```latex
γ' ≥ max(0, γ̇/2γ)                                         (52)
```

**Lyapunov derivative** becomes (Eq. 55, p. 1643):
```latex
V̇ ≤ -γη|sₐ|                                               (55)
```

ensuring eventual convergence to boundary layer as long as γ(t) is bounded away from zero

**Cite for**:
- Hybrid adaptive SMC for mixed fast/slow parameters
- Time-varying adaptation rate modulation
- Avoiding high-frequency excitation

---

### Modulated Adaptation Rate (Section 3.3, pp. 1644-1645)

**Update law for γ(t)** (Eq. 59-60, pp. 1644-1645):
```latex
γ̇ + λγ = λ³(β ∑ᵢ₌₁ʳ h²ᵢₙY²ᵢₐ + η²)⁻¹                      (59)

γ' := max(2λ, γ̇/2γ)                                       (60)
```

where Y_{ia} = Yᵢ(Xₐ) is value of Yᵢ along desired trajectory

**Filter structure**: (58) mimics **second-order low-pass filter** with:
- Input: current dynamic uncertainty
- Output: integral of sₐ

**Physical interpretation**:
- Larger γ → faster adaptation (from (49), (55))
- But also increases frequency content of control u
- γ(t) update (59) provides trade-off

**Cite for**:
- Time-varying adaptation rate design
- Second-order low-pass filter structure
- Preventing high-frequency dynamics excitation

---

## Simulation Example (Section 4, pp. 1645-1647)

### Test System (Eq. 61, p. 1645)

**Inverted pendulum model**:
```latex
ẍ + (a_{1x} + a_{1f})ẋ + a₂ sin(x) = (b*b_f)uₐ + d(t)      (61)
```

**Actual parameters**:
```latex
b* = 1;  a₂ = -100;  a_{1x} = 2
```

**Time-varying parts**:
```latex
b_f = 1 + (1/4) sin(2t);  d(t) = 2 sin(2t);  a_{1f} = sin(2t)
```

**High-frequency unmodelled dynamics** (p. 1645):
```latex
üₐ + (2ξω)u̇ₐ + ω²uₐ = ω²u
```

with ξ = 0.3, ω = 100 rad/s (second-order filter)

**Control parameters** (pp. 1645-1646):
- λ = 15 rad/s (control bandwidth)
- Δa₁ = 1, D = 2, η = 0.5
- b̂_f = 2√(2/3), β = √2
- b*_{M} = 10 (known upper bound on b*)

**Adaptation laws** (Eq. 62-64, p. 1646):
```latex
ḣ₁ = -γh₁ₙẋsₐ                                              (62)
ḣ₂ = -γh₂ₙ sin(x)sₐ                                        (63)
ḃ*⁻¹ = b²ₙγ(t)[u* + (Δa₁|ẋ| + D + η - Φ̇) sat(s/Φ) + γ̇sₐ]sₐ  (64)
```

**Modulation** (Eq. 59 modified, p. 1646):
```latex
γ̇ + λγ = λ²[β(h₁ₙxₐ)² + (h₂ₙ sin(xₐ)²) + η²]⁻¹
```

**Results** (Figs. 5-9, pp. 1647-1650):
- **Tracking error**: Within 4% of maximum xₐ(t) after 0.5 s
- **Unmodelled dynamics**: Not visibly excited
- **Parameter estimates**: Do not reach true values precisely, but adequate for s to remain in boundary layer
- **Adaptation period**: Completed in about 0.5 s

**Cite for**:
- Validation example
- Parameter tuning guidelines
- Performance with unmodelled dynamics

---

## Key Equations Cross-Reference

| Equation | Page | Description | Use For |
|----------|------|-------------|---------|
| (1) | 1632 | System dynamics | Problem formulation |
| (3) | 1632 | Sliding surface s(X;t) | Surface design |
| (4) | 1632 | Sliding condition | Convergence guarantee |
| (9) | 1634 | Switched control u = û - k sgn(s) | Robust SMC |
| (13) | 1636 | Tracking precision bound | Performance |
| (15) | 1636 | Modified gain k̃ = k - Φ | Boundary layer |
| (18)-(19) | 1637 | Balance condition | Φ(t) design |
| (25) | 1638 | Physical interpretation | Bandwidth trade-off |
| (28) | 1640 | Lyapunov function | Adaptive stability |
| (29) | 1640 | Distance to boundary sₐ | Adaptation measure |
| (32)-(34) | 1640 | Adaptation laws | Parameter update |
| (39) | 1641 | Weighted parameter error | Normalized adaptation |
| (49) | 1642 | Time-varying Lyapunov | Hybrid adaptive |
| (53)-(54) | 1643 | Modulated adaptation | Fast/slow parameters |
| (59)-(60) | 1644 | Adaptation rate γ(t) | Frequency tuning |

---

## Implementation Notes for DIP Thesis

### Comparison with Classical SMC

**Classical SMC** (Slotine & Sastry 1983):
- Fixed control gain k
- Discontinuous control → chattering
- Requires knowledge of uncertainty bounds
- Constant bandwidth

**Adaptive SMC** (This paper, 1986):
- Time-varying parameters (ĥᵢ, b̂)
- Boundary layer → smooth control
- On-line parameter adaptation
- Time-varying Φ(t) based on uncertainty

**Advantages for DIP**:
1. **No a priori parameter knowledge** - Adapts to unknown pendulum mass, length, friction
2. **Chattering elimination** - Boundary layer makes control implementable on real hardware
3. **Consistent adaptation** - Stops when inside boundary layer (no long-term drift)
4. **Explicit trade-offs** - Balance conditions quantify precision vs. uncertainty

---

### DIP-Specific Adaptations

**For 2-DOF DIP** (arm angle θ₁, pendulum angle θ₂):

**System dynamics** (simplified):
```latex
θ̈₂ = a₁θ̈₁ + a₂ sin(θ₂) + a₃ sin(θ₁)
θ̈₁ = b*u + ...
```

**Unknown parameters**: a₁, a₂, a₃ (functions of masses, lengths)

**Sliding surface** for θ₂ → 0:
```latex
s = (d/dt + λ)θ̃₂,  θ̃₂ = θ₂ - 0
```

**Adaptive control**:
```latex
u = b̂*⁻¹[û - k̃ sat(s/Φ)]
û = estimated dynamics based on â₁, â₂, â₃
```

**Adaptation laws**:
```latex
â̇₁ = -γ(t) θ̈₁ sₐ
â̇₂ = -γ(t) sin(θ₂) sₐ
â̇₃ = -γ(t) sin(θ₁) sₐ
ḃ*⁻¹ = γ(t)[...] sₐ
```

**Balance condition for Φ(t)**:
```latex
Φ̇ + λΦ = k(θ₁ₐ, θ₂ₐ; t)
```

---

### Parameter Tuning Guidelines

**Control bandwidth λ**:
- Larger λ → faster tracking but needs higher control authority
- Choose λ ≈ 10-20 rad/s for DIP

**Boundary layer width ε**:
- From balance condition: λⁿε ≈ βk(Xₐ; t)
- Start with ε ≈ 0.05-0.1 rad

**Adaptation weights** hᵢₙ, bₙ:
- Set h₁ₙ = 1 (unit weights as default)
- Increase weight on critical parameters

**Modulation rate γ(t)**:
- Use (59) with β from gain margin estimate
- Initial γ(0) = λ² (fast initial adaptation)

**Safety margin η**:
- η ≈ 0.5-1.0 (small but positive)

---

### Practical Considerations

**Advantages**:
1. **Systematic design** - Balance conditions provide tuning guidelines
2. **Adaptation stops** - No drift inside boundary layer
3. **Smooth control** - Implementable on real hardware
4. **Explicit performance** - Tracking precision from (13)

**Limitations**:
1. **Not zero tracking** - Tracks to within boundary layer thickness
2. **Requires continuous differentiability** - For Lyapunov analysis
3. **Parameter convergence** - Parameters may not reach true values (only adequate for performance)
4. **Initial transient** - Adaptation period before reaching boundary layer

**When to use**:
- Unknown/time-varying plant parameters
- Chattering must be avoided
- Can tolerate tracking to ±ε (not zero error)
- Robustness to unmodelled dynamics important

---

## Related Work Connections

**From Slotine & Coetsee 1986 references**:

1. **Utkin 1977** [Utkin 1977]: Original variable structure control (SMC foundations)
2. **Filippov 1960**: Sliding surface theory
3. **Slotine & Sastry 1983**: Tracking control foundations (we have SlotineSastry1983_tracking.md)
4. **Slotine 1984**: Boundary layer concept, time-varying surface
5. **Slotine 1985**: High-performance robots application
6. **Yoerger & Slotine 1985**: Remotely operated underwater vehicles
7. **Narendra et al. 1980**: Model reference adaptive control
8. **Corless & Leitmann 1983**: Continuous adaptive control
9. **Gutman & Palmor 1982**: Control smoothing
10. **Astrom 1983, 1984**: Adaptive control, excitation and unmodelled dynamics

**Thesis positioning**:
- Builds on Slotine & Sastry 1983 (classical SMC)
- Adds parameter adaptation to sliding control
- Introduces systematic adaptation stopping rule
- Quantifies tracking/uncertainty trade-off

---

## Citation Templates

### For Boundary Layer Concept

```latex
To eliminate chattering while maintaining robustness, we employ
the boundary layer concept \cite[Section~2.3]{Slotine1986}, where
control discontinuity is smoothed within a thin layer of thickness Φ
around the sliding surface.
```

### For Adaptive SMC

```latex
Following the adaptive sliding control methodology of
\cite{Slotine1986}, we couple on-line parameter estimation with
sliding mode control, using the distance to the boundary layer sₐ
as the error signal for adaptation.
```

### For Balance Conditions

```latex
The boundary layer thickness Φ(t) is designed according to the
balance condition \cite[Eq.~(19)]{Slotine1986}, which quantifies
the trade-off between control bandwidth λ, tracking precision ε,
and parametric uncertainty k(Xₐ; t).
```

### For Consistent Adaptation

```latex
A key feature of the adaptive scheme \cite[Section~3.1]{Slotine1986}
is that adaptation ceases when the system enters the boundary layer,
avoiding the undesirable long-term parameter drift common in adaptive
control.
```

### For Modulated Adaptation Rate

```latex
To prevent excitation of high-frequency unmodelled dynamics, the
adaptation rate γ(t) is modulated according to \cite[Eq.~(59)]{Slotine1986},
implementing a second-order low-pass filter structure.
```

---

## BibTeX Entry

```bibtex
@article{Slotine1986,
  author    = {J.-J. E. Slotine and J. A. Coetsee},
  title     = {Adaptive sliding controller synthesis for non-linear systems},
  journal   = {International Journal of Control},
  volume    = {43},
  number    = {6},
  pages     = {1631--1651},
  year      = {1986},
  doi       = {10.1080/00207178608933564},
  publisher = {Taylor \& Francis}
}
```

---

## Summary: Why This Paper Matters for DIP Thesis

**Core value**:
1. **Systematic adaptive SMC design** - Couples parameter estimation with sliding control
2. **Chattering elimination** - Boundary layer makes SMC practically implementable
3. **Balance conditions** - Quantitative trade-off between performance and uncertainty
4. **Consistent adaptation** - Stops when inside boundary layer (no drift)
5. **Validated on real system** - Inverted pendulum with unmodelled dynamics

**Direct applications to DIP**:
- Unknown pendulum parameters (masses, lengths, friction) → adapt on-line
- Real hardware implementation → boundary layer eliminates chattering
- Time-varying disturbances → modulated adaptation rate
- Unmodelled flexibility/time delays → γ(t) prevents excitation

**Theoretical contributions**:
- Distance to boundary layer sₐ as adaptation measure
- Balance conditions (Eq. 19, 25) for Φ(t) design
- Weighted parameter error (Eq. 39) for normalization
- Modulated adaptation rate (Eq. 59) for frequency control

**Comparison with thesis controllers**:
- **Classical SMC**: Fixed k, chattering, no adaptation
- **This approach**: Adaptive parameters, smooth control, systematic design
- **Plestan2010**: Both adaptive, but different adaptation laws

**Use when**:
- Plant parameters unknown/time-varying
- Chattering unacceptable (real hardware)
- Can accept tracking to ±ε (not zero)
- Want systematic tuning guidelines

**Recommended for DIP**: This is an excellent approach for the thesis, providing both theoretical rigor and practical implementability.

---

**File created**: 2025-12-06
**Status**: Complete - ready for thesis integration
**Next**: Continue tracking remaining citations
