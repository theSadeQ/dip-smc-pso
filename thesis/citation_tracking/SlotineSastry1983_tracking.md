# Citation Tracking: Slotine & Sastry 1983 - Tracking Control Using Sliding Surfaces

## Document Metadata
- **Authors**: Jean-Jacques E. Slotine, Shankar S. Sastry
- **Title**: Tracking Control of Non-Linear Systems Using Sliding Surfaces with Application to Robot Manipulators
- **Publication**: MIT LIDS Technical Report LIDS-P-1264
- **Date**: December 1982
- **Institution**: Laboratory for Information and Decision Systems, MIT
- **Pages**: 55 pages
- **Keywords**: Nonlinear control, sliding-mode control, robotics

## Research Context
- **Funding**: AFOSR grant 82-0258, ONR grant N00014-82-K-0582 (NR-606-003)
- **Primary Contribution**: First systematic methodology for tracking (not just stabilization) using time-varying sliding surfaces
- **Innovation**: Eliminates "reaching phase" by using time-varying surfaces; continuous approximation reduces chattering

---

## Section-by-Section Citation Guide

### Abstract (p. 1)
**Main Result**: Methodology for accurate tracking in non-linear, time-varying systems with parameter variations and disturbances.

**Key Innovation**:
> "This idealized control law achieves perfect tracking; however, non-idealities in its implementation result in the generation of an undesirable high frequency component... we show how continuous control laws may be used to approximate the discontinuous control law to obtain robust tracking to within a prescribed accuracy."

**Citation Use**: When introducing sliding mode control for tracking vs. stabilization.

---

### Section 1: Introduction (pp. 2-5)

#### Page 2-3: Motivation and Background
**Filippov's Mathematical Foundation**:
> "The basic mathematical idea comes from Fillipov [1]: consider a piecewise continuous differential equation, with the right hand side discontinuous across a hypersurface."

**Citation**:
- **Page 2, ¶2**: Definition of sliding mode - trajectories slide along discontinuity surface
- **Equation Location**: Filippov reference [1] cited

**Thesis Use**: Background on mathematical foundations of SMC

#### Page 3-4: Problems with Existing Methodology
**Problem (i) - Reaching Phase**:
> "There is a 'reaching' phase in which the trajectories starting from a given initial condition off the sliding surface tend towards the sliding surface. The trajectories in this phase are sensitive to parameter variations."

**Citation**:
- **Page 3, lines 13-24**: Critique of high-gain feedback in reaching phase
- **Problem**: Extreme sensitivity to unmodelled dynamics, actuator saturation

**Thesis Use**: Justification for time-varying sliding surfaces

**Problem (ii) - Chattering**:
> "Unavoidable small imperfections in switching between control laws at the discontinuity surface result in the trajectory chattering rather than sliding along the switching surface."

**Citation**:
- **Page 4, lines 5-10**: Definition of chattering problem
- **Consequence**: Excites high-frequency unmodelled dynamics

**Thesis Use**: Motivation for boundary layer approach (Section 5)

#### Page 4-5: Novel Contributions
**Time-Varying Sliding Surfaces**:
> "We remove these drawbacks by developing and using the concept of a time-varying sliding surface in the state space."

**Citation**:
- **Page 4, lines 11-15**: Introduction of time-varying surfaces for tracking
- **Benefit**: Eliminates reaching phase

**Continuous Approximation**:
> "Further, by approximating the discontinuous control law by a continuous one, we trade off accuracy in tracking against the generation of high frequency chattering."

**Citation**:
- **Page 4, lines 15-18**: Boundary layer method preview
- **Trade-off**: Accuracy vs. chattering reduction

---

### Section 2: Dynamics of Systems with Switches (pp. 6-16)

#### Page 6-7: Filippov Solution Concept

**Discontinuous Differential Equation**:
```
ẋ = f₊(x)  for {x:s(x) > 0} =: G₊    (2.1)
ẋ = f₋(x)  for {x:s(x) < 0} =: G₋    (2.2)
```

**Citation**:
- **Equation (2.1)-(2.2), p. 6**: Standard form of discontinuous dynamics
- **Location**: s(x) = 0 is the switching surface S

**Thesis Use**: System model formulation

#### Page 10-11: Filippov's Definition

**Solution Concept** (Definition, p. 10):
> "An absolutely continuous function x(t): [0,T] → ℝⁿ is a solution of (2.3) if for almost all t ∈ [0,T]"

```latex
dx/dt ∈ ⋂_{δ>0} ⋂_N Conv f(B(x(t),δ) - N)    (2.4)
```

**Citation**:
- **Equation (2.4), p. 10**: Filippov solution definition
- **Key Concept**: Convex hull of limiting values excludes zero-measure sets

**Thesis Use**: Theoretical foundation for sliding mode existence

#### Page 11-12: Equivalent Control on Sliding Surface

**Filippov's Lemma** (Lemma 3 of [1]):
When λ₊(x*) < 0 and λ₋(x*) > 0 (trajectories point toward S):

```latex
ẋ* = f₀(x*) = [λ₋(x*)/(λ₊(x*) - λ₋(x*))]f₊(x*) + [λ₊(x*)/(λ₊(x*) - λ₋(x*))]f₋(x*)    (2.5-2.6)
```

where:
```latex
λ₊(x) = ∂s(x)/∂x · f₊(x),  λ₋(x) = ∂s(x)/∂x · f₋(x)
```

**Citation**:
- **Equations (2.5)-(2.6), p. 11**: Equivalent control formula
- **Key Property**: s(x*)·f₀(x*) = 0 (trajectory stays on S)
- **Physical Meaning**: Weighted average of f₊ and f₋

**Thesis Use**: Derivation of sliding mode dynamics

**Figure 4 Interpretation** (p. 12):
> "Note that s(x*)·f₀(x*) = 0 (see the construction of Figure 4) so that the trajectory slides along S once it hits S"

**Citation**:
- **Figure 4, p. 12**: Geometric construction of f₀(x) as convex combination
- **Interpretation**: f₀ lies in the plane tangent to S

#### Page 13: Sliding Conditions

**Local Sliding Condition**:
```latex
d/dt s²(x) < 0  for x ∈ B(x*, δ) - S    (2.7)
```

**Citation**:
- **Equation (2.7), p. 13**: Sufficient condition for trajectories to reach and stay on S
- **Interpretation**: s² is a Lyapunov function near S

**Global Sliding Condition**:
```latex
d/dt s²(x) < -ψ(|s|)  for x ∈ ℝⁿ    (2.8)
```

**Citation**:
- **Equation (2.8), p. 13**: Condition for global attraction to S
- **Requirement**: ψ is Class K function

**Thesis Use**: Stability proof for sliding mode existence

#### Page 14: Uniqueness Conditions

**Filippov's Theorem 14**:
> "So long as at least one of the two inequalities λ₋(x*) > 0, λ₊(x*) < 0 is satisfied at each point x* ∈ S, the system (2.3) has a unique solution (in the sense of Definition (2.4)) for a given initial condition."

**Citation**:
- **Condition (2.9), p. 14**: Uniqueness requirement
- **Rules out**: Ambiguous case of Figure 1(b) where both point away

**Thesis Use**: Well-posedness of sliding mode control

#### Page 14-16: Time-Varying Case

**Time-Varying Sliding Surface**:
Define M₀ in (x,t) space:
```latex
M₀ = {(x;t): s(x;t) = 0} ⊂ ℝⁿ⁺¹    (p. 14)
```

**Modified Sliding Conditions**:
```latex
λ₊(x;t) = ∂s/∂t + ∂s/∂x · f₊(x;t)
λ₋(x;t) = ∂s/∂t + ∂s/∂x · f₋(x;t)
```

**Citation**:
- **Page 14, lines 15-20**: Extension to time-varying surfaces
- **Key Modification**: Add ∂s/∂t term to account for moving surface

**Sections of M₀** (Definition, p. 15):
```latex
S(t) = {x ∈ ℝⁿ: s(x;t) = 0}    (2.13)
```

**Citation**:
- **Equation (2.13), p. 15**: Time-varying surface sections
- **Interpretation**: S(t) is a "moving" sliding surface

**Local Sliding Condition (Time-Varying)**:
```latex
d/dt s²(x;t) < 0  for x ∈ B(x*, δ) - S(t)    (2.14)
```

**Global Sliding Condition (Time-Varying)**:
```latex
d/dt s²(x;t) < -ψ(|s(x;t)|)  for x ∈ ℝⁿ - S(t)    (2.15)
```

**Citation**:
- **Equations (2.14)-(2.15), p. 16**: Sliding conditions for time-varying surfaces
- **Critical for tracking**: Allows desired trajectory to define S(t)

**Thesis Use**: Foundation for tracking controller design

---

### Section 3: Linear Time-Varying Systems (pp. 17-22)

#### Page 17-18: Problem Formulation

**System Dynamics**:
```latex
x₁⁽ⁿ⁾ + aₙ₋₁(t)x₁⁽ⁿ⁻¹⁾ + aₙ₋₂(t)x₁⁽ⁿ⁻²⁾ + ... + a₀(t)x₁ = u    (3.1)
```

**State Space Form**:
```latex
ẋ = A(t)x + Bu    (3.3)
```
where x = [x₁, ẋ₁, ..., x₁⁽ⁿ⁻¹⁾]ᵀ, B = [0, ..., 0, 1]ᵀ

**Citation**:
- **Equations (3.1), (3.3), pp. 17-18**: Controllable canonical form
- **Tracking Error**: x̃(t) = x(t) - xd(t) with x̃(0) = 0

**Thesis Use**: Example system for DIP formulation

#### Page 18: Sliding Surface Design

**Sliding Surface for Tracking**:
```latex
s(x;t) = Cx̃(t) = 0    (3.5)
```
where C = [c₁, ..., cₙ₋₁, 1]

**Constraint on Trajectory** (Equation 3.6, p. 18):
```latex
x₁⁽ⁿ⁻¹⁾ + Σᵢ₌₀ⁿ⁻² cᵢ₊₁x₁⁽ⁱ⁾ = xd₁⁽ⁿ⁻¹⁾ + Σᵢ₌₀ⁿ⁻² cᵢ₊₁xd₁⁽ⁱ⁾    (3.6)
```

**Citation**:
- **Equation (3.6), p. 18**: Error dynamics on sliding surface
- **Key Result**: With matching initial conditions → x(t) ≡ xd(t)

**Stability Requirement**:
> "The polynomial z^(n-1) + Σᵢ₌₀ⁿ⁻² cᵢ₊₁zⁱ is Hurwitz"

**Citation**:
- **Page 18, lines 10-12**: Stable sliding surface definition
- **Consequence**: Tracking errors decay exponentially if x̃(0) ≠ 0

**Thesis Use**: Design of sliding surface coefficients C

#### Page 18-20: Control Law Design

**Control Law Structure**:
```latex
u = βᵀ(x)·x + Σᵢ₌₁ⁿ⁻¹ kᵢ(x;t)x̃ᵢ₊₁ - kₙ sgn s    (3.7)
```

**Citation**:
- **Equation (3.7), pp. 18-19**: Discontinuous control structure
- **Components**:
  - β(x): Cancels known nonlinearities
  - kᵢ: Linear gains
  - kₙ sgn s: Discontinuous term for robustness

**Sliding Condition Derivation** (Equation 3.8, p. 19):
```latex
½ d/dt s²(x;t) = Σᵢ₌₁ⁿ [βᵢ(x) - aᵢ₋₁(t)]xᵢ·s + Σᵢ₌₁ⁿ⁻¹ (cᵢ + kᵢ(x;t))x̃ᵢ₊₁·s
                 - s·xdₙ₊₁ - kₙ|s|    (3.8)
```

**Citation**:
- **Equation (3.8), p. 19**: Lyapunov function derivative
- **Goal**: Make this negative definite

#### Page 19-20: Parameter Bounds

**Robust Gain Selection**:
```latex
βᵢ⁺ ≤ aᵢ₋₁(t)  ⟹  βᵢ(x) = βᵢ⁻(t) ≥ αᵢ₋₁(t)    (3.9)
βᵢ⁻ ≥ aᵢ₋₁(t)  ⟹  βᵢ(x) = βᵢ⁺(t) ≤ αᵢ₋₁(t)    (3.10)
```

**Citation**:
- **Equations (3.9)-(3.10), p. 19**: Switching logic based on parameter bounds
- **Robustness**: Only requires bounds αᵢ ≤ aᵢ(t) ≤ ᾱᵢ, not exact values

**Linear Gain Bounds**:
```latex
s·x̃ᵢ₊₁ > 0  ⟹  kᵢ(x;t) = Kᵢ⁺(t) ≤ -cᵢ    (3.11)
s·x̃ᵢ₊₁ < 0  ⟹  kᵢ(x;t) = Kᵢ⁻(t) ≥ -cᵢ    (3.12)
```

**Citation**:
- **Equations (3.11)-(3.12), p. 19**: Gain switching for stability
- **Note**: Discard kᵢx̃ᵢ₊₁ terms when cᵢ = 0

**Discontinuous Gain Bound**:
```latex
kₙ > v    (3.13)
```
where |ẍd₁(t)| ≤ v

**Citation**:
- **Equation (3.13), p. 20**: Bound for tracking desired trajectory
- **Physical Meaning**: Must overcome maximum desired acceleration

**Thesis Use**: Gain tuning methodology

#### Page 20-22: Disturbance Rejection

**Parameter Variation Bounds** (p. 20):
```latex
αᵢ < aᵢ(t) < ᾱᵢ  for i=0,...,n-1    (3.16)
```

**Citation**:
- **Equation (3.16), p. 20**: Required knowledge for robust control
- **Key Point**: Only bounds needed, not exact parameter values

**Disturbance Model** (p. 20-21):
```latex
d(x;t) = [0, ..., 0, d₁(x,t)]ᵀ
|d₁(x;t)| ≤ Σᵢ₌₁ⁿ δᵢ|xᵢ| + δ₀    (3.17-3.18)
```

**Modified Gain Bounds**:
```latex
βᵢ⁺ ≤ αᵢ₋₁ - δᵢ    (3.17)
βᵢ⁻ ≥ ᾱᵢ₋₁ + δᵢ    (3.17)
kₙ > v + δ₀        (3.18)
```

**Citation**:
- **Equations (3.17)-(3.18), p. 21**: Disturbance rejection requirements
- **Consequence**: Larger discontinuity needed for stronger disturbances

**Minimum Discontinuity**:
> "As expected, the minimum discontinuity in the control u (measured by βᵢ⁻ - βᵢ⁺ for i=1,...,n, Kᵢ⁻ - Kᵢ⁺ for j=1,...,n-1, and 2kₙ) required to reject disturbances and parameter variation increases with the strength of the disturbance"

**Citation**:
- **Page 21, lines 15-20**: Trade-off between robustness and control effort

**Thesis Use**: Disturbance analysis for DIP

#### Page 21-22: Choice of C and Transient Response

**Stable Sliding Surface Design**:
Example for n=2:
```latex
s(x̃;t) = (d/dt + λ)^(n-1) x̃₁    (3.18)
```

**For n=2**:
```latex
s = ẋ̃₁ + (1/T)x̃₁ = ẋ̃₁ + λx̃₁
```

**Transient Performance** (p. 22):
If x₁(0) = xd₁(0) + ε, then:
```latex
x₁(t) = xd₁(t) + εe^(-t/T)    (for T > 0)
```

**Citation**:
- **Equation (3.18), Example, p. 21-22**: First-order error dynamics
- **Design Parameter**: T controls convergence rate (larger T → faster)

**Thesis Use**: Selection of sliding surface parameters for desired dynamics

---

### Section 4: Non-Linear Systems (pp. 23-31)

#### Page 23-24: System Class

**General Form**:
```latex
θⱼ⁽ⁿʲ⁾ = fⱼ(θ₁, θ₂, ..., θₚ; t) + uⱼ,  j = 1,...,p    (4.1)
```

**State Vectors**:
```latex
θᵢ = [θᵢ, θ̇ᵢ, ..., θᵢ⁽ⁿⁱ⁻¹⁾]ᵀ
θ = [θ₁ᵀ, ..., θₚᵀ]ᵀ
|θ| = [|θ₁|ᵀ, ..., |θₚ|ᵀ]ᵀ
```

**Citation**:
- **Equation (4.1), p. 23**: Decoupled multi-input system form
- **Application**: Each joint controlled independently

**Polynomial Bound Assumption**:
```latex
|fⱼ(θ;t)| ≤ Fⱼ(|θ|;t)    (4.2)
```
where Fⱼ is a polynomial in |θ| with smooth, positive time-varying coefficients

**Citation**:
- **Equation (4.2), p. 23**: Key assumption enabling systematic design
- **Justification**: Trigonometric terms bounded by polynomials

**Thesis Use**: Formulation for DIP dynamics

#### Page 23-24: Tracking Problem

**Desired Trajectories**:
```latex
θdⱼ(t) = [θdⱼ, θ̇dⱼ, ..., θdⱼ⁽ⁿʲ⁻¹⁾]ᵀ
θ̃ⱼ(t) = θⱼ(t) - θdⱼ(t) = [θ̃ⱼ, θ̃̇ⱼ, ..., θ̃ⱼ⁽ⁿʲ⁻¹⁾]ᵀ
```

**Sliding Surfaces**:
```latex
Sⱼ(t) = {θⱼ: sⱼ(θⱼ;t) = 0}    (4.3)
```
where
```latex
sⱼ(θⱼ;t) = Cⱼθ̃ⱼ    (4.4)
```

**Citation**:
- **Equations (4.3)-(4.4), p. 23**: Sliding surface definition for multi-input case
- **Key**: Each surface depends only on θⱼ (decoupling)

**Stable Surface Requirement**:
> "Cⱼ is a constant row vector of the form [cⱼ₁,...,cⱼₙⱼ₋₁,1] such that the surface defined by (4.4) is stable... such that the polynomial z^(nⱼ-1) + Σᵢ₌₀^(nⱼ-2) cⱼᵢ₊₁z^i is Hurwitz"

**Citation**:
- **Page 24, lines 3-7**: Stability condition ensures error convergence

**Boundedness Assumption**:
```latex
|θ̈dⱼ⁽ⁿʲ⁾(t)| ≤ vⱼ(t)  ∀t ≥ 0    (4.5)
```

**Citation**:
- **Equation (4.5), p. 24**: Bound on desired trajectory derivatives

**Thesis Use**: Specifications for reference trajectories

#### Page 24-26: Control Law Structure

**Polynomial Term Representation** (Equation 4.6, p. 24):
A representative term in Fⱼ(θ;t):
```latex
Fⱼₖ = αⱼₖ(t) · ∏ᵢ₌₁ᵖ ∏ₗ₌₀^(nᵢ-1) (θᵢ⁽ˡ⁾)^m(i,ℓ,j,k)    (4.6)
```

**Citation**:
- **Equation (4.6), p. 24**: Structure of nonlinear terms
- **Components**:
  - αⱼₖ(t): Time-varying coefficient
  - m(i,ℓ,j,k): Integer power of θᵢ⁽ˡ⁾

**Control Law**:
```latex
uⱼ = Σₖ uⱼₖ(θ;t) + Σᵢ₌₁^(nⱼ-1) Kⱼᵢ(θ;t)θ̃ⱼ⁽ⁱ⁾ - Kⱼₙⱼ(θ;t) sgn sⱼ    (4.7)
```

where
```latex
uⱼₖ(θ;t) = βⱼₖ(θ;t) · ∏ᵢ₌₁ᵖ ∏ₗ₌₀^(nᵢ-1) (θᵢ⁽ˡ⁾)^m(i,ℓ,j,k)    (4.8)
```

**Citation**:
- **Equations (4.7)-(4.8), pp. 24-25**: General nonlinear control structure
- **Note**: Discard Kⱼᵢθ̃ⱼ⁽ⁱ⁾ terms when cⱼᵢ = 0

**Thesis Use**: Template for DIP controller

#### Page 26-27: Gain Switching Logic

**βⱼₖ Switching** (Equations 4.9-4.10, p. 26):
```latex
sⱼ · ∏ᵢ₌₁ᵖ ∏ₗ₌₀^(nᵢ-1) (θᵢ⁽ˡ⁾)^m(i,ℓ,j,k) < 0  ⟹  βⱼₖ(θ;t) = βⱼₖ⁻(t) ≥ αⱼₖ(t)    (4.9)

sⱼ · ∏ᵢ₌₁ᵖ ∏ₗ₌₀^(nᵢ-1) (θᵢ⁽ˡ⁾)^m(i,ℓ,j,k) > 0  ⟹  βⱼₖ(θ;t) = βⱼₖ⁺(t) ≤ -αⱼₖ(t)    (4.10)
```

**Citation**:
- **Equations (4.9)-(4.10), p. 26**: Sign-dependent gain switching
- **Simplification**: Only need sign of product, not numerical value

**Kⱼᵢ Switching** (Equations 4.11-4.12, p. 26):
```latex
sⱼ·θ̃ⱼ⁽ⁱ⁾ < 0  ⟹  Kⱼᵢ(θ;t) = Kⱼᵢ⁺(t) ≤ -cⱼᵢ    (4.11)
sⱼ·θ̃ⱼ⁽ⁱ⁾ > 0  ⟹  Kⱼᵢ(θ;t) = Kⱼᵢ⁻(t) ≥ -cⱼᵢ    (4.12)
```

**Citation**:
- **Equations (4.11)-(4.12), p. 26**: Linear term gain switching

**Discontinuous Gain**:
```latex
Kⱼₙⱼ(θ;t) > vⱼ(t)  uniformly in t    (4.13)
```

**Citation**:
- **Equation (4.13), p. 26**: Minimum sgn switching magnitude
- **Robustness**: Must dominate maximum desired trajectory variation

**Sliding Condition Verification** (p. 26-27):
```latex
½ d/dt sⱼ²(θⱼ;t) < -(kₙⱼ - vⱼ)|sⱼ(θⱼ;t)|    (derived from 4.8)
```

**Citation**:
- **Page 26, verification**: Shows global sliding condition (2.12) satisfied
- **Conclusion**: θⱼ(t) = θdⱼ(t) achieved

**Thesis Use**: Proof of tracking convergence

#### Page 27: Implementation Note

**Avoiding Numerical Calculation**:
> "The conditions (4.9), (4.10) are easier to verify than they appear: since we only need determine the sign of powers of θᵢ⁽ˡ⁾ we replace m(i,ℓ,j,k) by 0 or 1, according to whether m(i,ℓ,j,k) is even or odd, respectively."

**Citation**:
- **Page 26-27, footnote**: Computational simplification
- **Key**: Only sign matters, not magnitude

**Thesis Use**: Efficient implementation strategy

#### Page 27-28: Non-Sliding Surfaces

**Discontinuities at**:
- {θ: θᵢ⁽ˡ⁾ = 0} for odd m(i,ℓ,j,k)
- {θ: θⱼ⁽ⁱ⁾ = 0}
- {θ: sⱼ(θⱼ;t) = 0} (sliding surface)

**Verification**:
> "It is easy to verify, however, that the (possibly time-varying) discontinuity surfaces {θ:θ̃ᵢ⁽ˡ⁾ = 0}, and {θ:θⱼ⁽ⁱ⁾ = 0} are not sliding surfaces since for each θ* on any one of these surfaces, we have λ₊(θ*;t*) = λ₋(θ*,t*) ≠ 0"

**Citation**:
- **Equation (3.14), p. 27-28**: Non-sliding surface condition
- **Consequence**: Trajectories pass through uniquely (no chattering)

**Thesis Use**: Justification for not smoothing all discontinuities

#### Page 28-30: Disturbance Rejection

**Disturbance Model** (Equation 4.18, p. 28):
```latex
|dⱼ(θ;t)| ≤ δⱼ₀(t) + Σₖ δⱼₖ(t) ∏ᵢ₌₁ᵖ ∏ₗ₌₀^(nᵢ-1) |θᵢ⁽ˡ⁾|^m(i,ℓ,j,k)    (4.18)
```

**Modified Gain Bounds** (Equations 4.19-4.21, p. 29):
```latex
βⱼₖ⁻(t) ≥ αⱼₖ(t) + δⱼₖ(t)    (4.19)
βⱼₖ⁺(t) ≤ -αⱼₖ(t) - δⱼₖ(t)   (4.20)
Kⱼₙⱼ(θ;t) > vⱼ(t) + δⱼ₀(t)  uniformly in t    (4.21)
```

**Citation**:
- **Equations (4.19)-(4.21), p. 29**: Robustness to matched disturbances
- **Key**: Linear increase in required gain magnitude

**Invariance Property**:
> "Also, once the trajectory is on a sliding surface Sⱼ(t), its dynamics are governed by"
```latex
θ̃ⱼ⁽ⁿʲ⁻¹⁾ + Σᵢ₌₀^(nⱼ-2) cⱼᵢ₊₁θ̃ⱼ⁽ⁱ⁾ = 0    (4.24)
```
> "which does not contain the disturbance term."

**Citation**:
- **Equation (4.24), p. 30**: Error dynamics on sliding surface
- **Invariance**: Insensitive to matched disturbances during sliding mode

**Thesis Use**: Disturbance rejection analysis

#### Page 30-31: Extensions

**Generalization to bⱼ(θ;t) ≠ 1**:
For systems:
```latex
θⱼ⁽ⁿʲ⁾ = fⱼ(θ₁, θ₂,..., θₚ; t) + bⱼ(θ;t)uⱼ
```
with 0 < λⱼ(t) ≤ bⱼ(θ;t) ≤ ʷⱼ(t)

**Modified Gains** (p. 30):
```latex
βⱼₖ(θ;t) = βⱼₖ±(t) ≥ αⱼₖ(t)/λⱼ(t)
βⱼₖ(θ;t) = βⱼₖ±(t) ≤ αⱼₖ(t)/ʷⱼ(t)
Kⱼᵢ(θ;t) = Kⱼᵢ±(t) ≥ Max(-cⱼᵢ/λⱼ(t), -cⱼᵢ/ʷⱼ(t))
```

**Citation**:
- **Page 30, modification**: Extension to control effectiveness uncertainty
- **Application**: Actuator gain variations

**Other Function Classes** (p. 31):
> "We remark here that the development of this section using the polynomial bounds of equations (4.2), (4.18) can be generalized when fⱼ(θ;t), dⱼ(θ;t) are bounded by other classes of functions."

**Example**: If d₁ satisfies |d₁(θ)| < δ₁₀ + δ₁₁|θ₁| + exp(θ₂), add β₁₄ exp(θ₂) term with switching.

**Citation**:
- **Page 31, Example**: Extension to exponential/other bounds

**Thesis Use**: Adaptations for specific nonlinearities

---

### Section 5: Continuous Approximation (pp. 32-37)

#### Page 32-33: Motivation

**Chattering Problem**:
> "In practice, imperfections such as delays in switching, hysteresis in switching, will cause the trajectory to chatter along the sliding surface... This will of course be accompanied by a rapidly (time)-varying control law."

**Citation**:
- **Page 32, lines 3-8**: Practical limitations of discontinuous control
- **Consequence**: Excites unmodelled high-frequency dynamics

**Lack of Robustness to Modelling Approximations**:
> "Thus, while sliding mode control provides control laws which are robust to parameter variations and disturbance inputs, they are, in themselves, not robust to the usual modelling approximations"

**Citation**:
- **Page 32, lines 9-13**: Paradox of SMC - robust to some uncertainties, not others

**Thesis Use**: Justification for boundary layer approach

#### Page 32-33: Boundary Layer Concept

**Basic Idea**:
> "The basic idea is simple: it consists of 'smoothing' out the discontinuity in the control law at the switching surface, i.e., find... a continuous control law uⱼ(θ;t) whose terms are continuous functions of θ inside a small boundary layer neighboring the switching surface."

**Citation**:
- **Page 32, lines 18-22**: Boundary layer definition
- **Role**: "Smudged switching surface"

**Trade-off**:
> "The penalty paid for smudging the sliding surface is that the dynamics of the state trajectory inside the boundary layer are only an approximation to the desired dynamics on the sliding surface. The advantage of the scheme is that the state trajectory does not chatter very rapidly"

**Citation**:
- **Page 33, lines 1-5**: Accuracy vs. chattering trade-off

**Thesis Use**: Design philosophy for practical SMC

#### Page 33-34: Boundary Layer Definition

**Outer Boundary**:
```latex
s⁻ⱼ(θⱼ;t) = sⱼ(θⱼ;t) + cⱼ₁εⱼ    (5.2)
```

**Inner Boundary**:
```latex
s⁺ⱼ(θⱼ;t) = sⱼ(θⱼ;t) - cⱼ₁εⱼ    (5.3)
```

**Boundary Layer**:
```latex
Bⱼ(t) = {θ: s⁻ⱼ(θⱼ;t) > 0 and s⁺ⱼ(θⱼ;t) < 0}    (5.4)
```

**Citation**:
- **Equations (5.2)-(5.4), Figure 6, pp. 33-34**: Boundary layer construction
- **Width**: 2cⱼ₁εⱼ in sⱼ coordinate
- **Requirement**: cⱼ₁ > 0 (from Hurwitz condition)

**Figure 6 Interpretation**:
Shows three surfaces: s⁻ⱼ = 0, sⱼ = 0, s⁺ⱼ = 0 with boundary layer between outer surfaces.

**Citation**:
- **Figure 6, p. 34**: Geometric visualization of boundary layer

**Thesis Use**: Boundary layer width selection

#### Page 34-35: Continuous Control Law

**Outside Boundary Layer**:
Use discontinuous law (4.7)-(4.13) for:
- θ ∈ {θ: s⁻ⱼ(θⱼ;t) < 0} = S⁻ⱼ(t)
- θ ∈ {θ: s⁺ⱼ(θⱼ;t) > 0} = S⁺ⱼ(t)

**Sliding Conditions** (Equations 5.5-5.6, p. 35):
```latex
d/dt s⁻ⱼ(θⱼ;t) > 0  for θ ∈ S⁻ⱼ(t)    (5.5)
d/dt s⁺ⱼ(θⱼ;t) < 0  for θ ∈ S⁺ⱼ(t)    (5.6)
```

**Citation**:
- **Equations (5.5)-(5.6), p. 35**: Trajectories converge to and stay in Bⱼ(t)

**Invariance of Boundary Layer**:
> "Trajectories starting outside Bⱼ(t) tend towards Bⱼ(t), and further trajectories starting inside Bⱼ(t), stay in it for all future time."

**Citation**:
- **Page 35, lines 8-10**: Positive invariance property

**Inside Boundary Layer - Linear Interpolation**:
Replace kⱼₙⱼ sgn sⱼ with:
```latex
Kⱼ₂|sⱼ/5εⱼ|
```

**Figure 7 Illustration** (p. 34):
Shows smooth transition from β⁻ⱼₖ(t) to β⁺ⱼₖ(t) across boundary layer.

**Citation**:
- **Figure 7, p. 34**: Example interpolation scheme
- **Note**: Linear interpolation shown, but "any continuous interpolation... will suffice"

**General Interpolation**:
> "We claim that any continuous interpolation between uⱼ(θ;t) defined on S⁻ⱼ(t) and uⱼ(θ;t) defined on S⁺ⱼ(t) will suffice for our purposes (at least one such interpolation exists, by Urysohn's lemma [4])"

**Citation**:
- **Page 35, lines 15-18**: Flexibility in interpolation choice
- **Reference**: Urysohn's lemma for existence

**Thesis Use**: Implementation of continuous approximation

#### Page 35-37: Tracking Accuracy

**Trajectory Confinement** (Equation 5.7, p. 36):
If θ(0) ∈ B(0), then θ(t) ∈ B(t) for all time, yielding:
```latex
sⱼ(θⱼ;t) = cⱼ₁Δ(t)  ∀t > 0    (5.7)
```
where |Δ(t)| < εⱼ

**Citation**:
- **Equation (5.7), p. 36**: Bound on sliding variable

**Error Bound**:
> "Using the form of sⱼ(θⱼ;t) given by (5.1) it is then possible to bound |θ̃ⱼ(t) - θdⱼ(t)|"

**Example - First Order**:
For sⱼ = (d/dt + λⱼ)(θⱼ - θdⱼ) with matching initial conditions:
```latex
|θⱼ(t) - θdⱼ(t)| ≤ εⱼ  ∀t > 0    (5.8)
```

**Citation**:
- **Equation (5.8), p. 36**: Ultimate bound on tracking error
- **Linear Relationship**: Error proportional to boundary layer thickness

**Mismatched Initial Conditions** (p. 36):
```latex
|θⱼ(t) - θdⱼ(t)| ≤ εⱼ + P(t)|θ̃ⱼ(0)|e^(-λⱼt)
```
where P(t) is polynomial in t.

**Citation**:
- **Page 36, modification**: Exponentially decaying transient term

**Thesis Use**: Performance prediction from εⱼ selection

#### Page 37: Non-Chattering Verification

**Other Discontinuities**:
Recall control is also discontinuous at:
- {θ: θᵢ⁽ˡ⁾ = 0} for odd m(i,ℓ,j,k)
- {θ: θⱼ⁽ⁱ⁾ = 0}

**No Smoothing Needed**:
> "However, as noted in section 4, surfaces of the last two categories are not sliding surfaces (in particular our solution concept calls for a unique extension of trajectories through them). Hence, we need not replace the discontinuous control law at these surfaces by a continuous one - and, of course, no high frequency chattering is generated at these surfaces by switching imperfections."

**Citation**:
- **Page 37, lines 1-7**: Selective smoothing justification

**Thesis Use**: Computational efficiency (fewer interpolations)

---

### Section 6: Two-Link Manipulator (pp. 38-51)

#### Page 38-39: Motivation

**Control Challenge**:
> "The accurate, high-speed tracking of desired trajectories is the control-challenge in the development of modern industrial robots and manipulators. Typically, the equations of motion of these robots are highly non-linear and coupled."

**Citation**:
- **Page 38, lines 1-4**: Statement of robotic control problem

**Flexible Manufacturing Requirements**:
> "Also, the development of flexible manufacturing systems calls for robustness of performance with regard to the variation of the load, task or real time trajectory specification, as well as other 'disturbances'."

**Citation**:
- **Page 38, lines 4-7**: Variable load handling requirement

**Advantages Over Existing Methods**:
> "By design, our sliding mode feedback controller is robust to certain variations in parameter values, an improvement over the 'non-linear decoupling techniques' proposed by Freund [3], on-line computational schemes proposed by Luh, et al [6], [13], and the linearization techniques of Melouah, et al. [14]."

**Citation**:
- **Page 38, lines 17-21**: Comparison to state-of-art (1982)

**Thesis Use**: Motivation for SMC in robotics

#### Page 39-40: System Dynamics

**Two-Link Manipulator** (Figure 8, p. 40):
- Horizontal plane motion
- Equal length ℓ and mass m (normalized to 1)
- States: θ₁ (first link angle), θ₂ (second link relative angle)
- Inputs: T₁, T₂ (joint torques)

**Equations of Motion** (Equations 6.1-6.2, p. 39):
```latex
θ̈₁ = [2/3 T'₁ - (2/3 + cos θ₂)T'₂]/(16/9 - cos² θ₂)    (6.1)

θ̈₂ = [-(2/3 + cos θ₂)T'₁ + 2(5/3 + cos θ₂)T'₂]/(16/9 - cos² θ₂)    (6.2)
```

where:
```latex
T'₁ = 2T₁ + sin θ₂ · θ̇₂(2θ̇₁ + θ̇₂)
T'₂ = 2T₂ - sin θ₂ · θ̇₁²
```

**Citation**:
- **Equations (6.1)-(6.2), p. 39**: Manipulator dynamics (from [15])
- **Figure 8, p. 40**: Schematic diagram

**Thesis Use**: DIP dynamics comparison (underactuated vs. fully actuated)

#### Page 39-40: Control Transformation

**New Control Variables** (Equations 6.3-6.4, p. 39):
```latex
u₁ = 4/3 T'₁ - (4/3 + 2 cos θ₂)T'₂    (6.3)
u₂ = -(4/3 + 2 cos θ₂)T'₁ + (20/3 + 4 cos θ₂)T'₂    (6.4)
```

**Rationale**:
> "The idea behind (6.3) and (6.4) is that they are 'invertible' i.e. they can be solved to obtain T₁ and T₂ as functions of u₁ and u₂"

**Citation**:
- **Equations (6.3)-(6.4), p. 39**: Input transformation for decoupling

**Transformed Dynamics** (Equations 6.5-6.6, p. 41):
```latex
θ̈₁ = [2/3·sin θ₂·θ̇₂(2θ̇₁ + θ̇₂) - (2/3 + cos θ₂)sin θ₂·θ̇₁² + u₁]/(16/9 - cos² θ₂)    (6.5)

θ̈₂ = [-(2/3 + cos θ₂)sin θ₂·θ̇₂(2θ̇₁ + θ̇₂) - 2(5/3 + cos θ₂)sin θ₂·θ̇₁² + u₂]/(16/9 - cos² θ₂)    (6.6)
```

**Citation**:
- **Equations (6.5)-(6.6), p. 41**: Dynamics in new coordinates

**Thesis Use**: Feedback linearization comparison

#### Page 41-42: Sliding Surface Design

**Sliding Surfaces** (Equation 6.7, p. 41):
```latex
sⱼ(θⱼ;t) = (θⱼ - θdⱼ) + 5(θ̇ⱼ - θ̇dⱼ)  for j=1,2    (6.7)
```

**Citation**:
- **Equation (6.7), p. 41**: First-order error dynamics (n=2 case)
- **Coefficient**: λ = 5 rad/sec

**Desired Trajectory Bound** (Equation 6.8, p. 41):
```latex
|θ̈dⱼ(t)| ≤ 1.75 rad/sec²    (6.8)
```

**Citation**:
- **Equation (6.8), p. 41**: Only a priori knowledge required

**Control Structure** (Equations 6.9-6.10, p. 41):
```latex
u₁ = β₁₁θ̇₂(2θ̇₁ + θ̇₂) + β₁₂θ̇₁² + K₁₁(θ̇₁ - θ̇d₁) - K₁₂ sgn s₁    (6.9)

u₂ = β₂₁θ̇₂(2θ̇₁ + θ̇₂) + β₂₂θ̇₁² + K₂₁(θ̇₂ - θ̇d₂) - K₂₂ sgn s₂    (6.10)
```

**Note on Grouping**:
> "We choose to keep the terms θ̇₂(2θ̇₁ + θ̇₂) grouped in (6.9), (6.10), since they appear in this form in the system description (6.1), (6.2)."

**Citation**:
- **Equations (6.9)-(6.10), p. 41**: Control law structure
- **Page 41, note**: Computational efficiency consideration

**Non-Sliding Surface**:
> "The surface {θ: 2θ̇₁ + θ̇₂ = 0} is not a sliding surface... since trajectories can be uniquely continued through it."

**Citation**:
- **Page 41, lines 18-20**: No chattering at velocity constraints

**Thesis Use**: Controller implementation

#### Page 41-42: Gain Selection (No Load)

**Nominal Case (μ = 0)**:
```latex
β⁻₁₁ = -β⁺₁₁ = 1.27
β⁻₁₂ = β⁺₂₁ = -β⁺₁₂ = -β⁻₂₁ = 1.2
β⁻₂₂ = -β⁺₂₂ = 4.4
K⁻ⱼ₁ = -3.8; K⁺ⱼ₁ = -9
Kⱼ₂ = 3.15  for j=1,2
```

**Citation**:
- **Page 41-42**: Numerical gain values for unloaded manipulator

**Continuous Approximation** (p. 42):
Replace Kⱼ₂ sgn sⱼ with:
```latex
Kⱼ₂|sⱼ/5εⱼ|
```
with ε₁ = ε₂ = 1°

**Citation**:
- **Page 42, lines 9-13**: Boundary layer implementation
- **Tracking Accuracy**: ≤ 1° from Eq. (5.8)

**Thesis Use**: Gain tuning example

#### Page 42-43: Simulation Results (No Load)

**Implementation Details** (p. 42):
- Sampling rate: 50 Hz
- Measurement noise:
  - Angles: [0, 0.25]° uniform
  - Angular velocities: [0, 0.5]°/sec uniform
- Integration: 4th order Adams-Bashforth, 6.67 ms step
- Plotting rate: 150 points/sec

**Citation**:
- **Page 42, lines 15-21**: Simulation parameters

**Initial Conditions**:
```latex
θ₁(0) = -90°, θ₂(0) = 170°
θ̇₁(0) = θ̇₂(0) = 0
```

**Desired Trajectories** (p. 42-43):
```latex
θd₁(t) = -90° + 52.5°(1 - cos 1.26t)  for t ≤ 2.5
       = 15°  for t > 2.5

θd₂(t) = 170° - 60°(1 - cos 1.26t)  for t ≤ 2.5
       = 50°  for t > 2.5
```

**Citation**:
- **Page 42-43, trajectories**: Satisfy bound (6.8) when measured in radians

**Performance** (p. 43):
> "The simulation results show tracking to within an error of 0.7° in θ₁ and θ₂."

**Citation**:
- **Page 43, line 1**: Achieved tracking accuracy (better than 1° theoretical)

**Figure 9 Description** (pp. 43-44):
- 9a: θ₁(t), θ₂(t) trajectories
- 9b: T₁(t), T₂(t) control torques

**Citation**:
- **Figures 9a-b, pp. 43-44**: No-load simulation results

**Discontinuity Handling** (p. 43):
> "Note that θ̇d₁, θ̇d₂ and hence T₁, T₂ are discontinuous at t=2.5."

**Citation**:
- **Page 43, lines 2-3**: Controller handles trajectory discontinuities

**Thesis Use**: Baseline performance comparison

#### Page 43-45: Robustness to Load Variations

**Variable Load Problem**:
Demonstrate tracking with μ ∈ [0, 0.25] (payload at tip of second link).

**Modified Dynamics** (Equations 6.11-6.12, p. 45):
```latex
θ̈₁[2(5/3 + cos θ₂) + 4μ(1 + cos θ₂)] + θ̈₂[2/3 + cos θ₂ + 2μ(1 + cos θ₂)]
  = 2T₁ + sin θ₂·θ̇₂²(2θ̇₁ + θ̇₂)(1 + 2μ)    (6.11)

θ̈₂[2/3 + cos θ₂ + 2μ(1 + cos θ₂)] + θ̈₁[2/3 + 2μ]
  = 2T₂ - sin θ₂·θ̇₁²(1 + 2μ)    (6.12)
```

**Citation**:
- **Equations (6.11)-(6.12), p. 45**: Load-dependent dynamics (from [15])

**Robust Gain Selection** (p. 45):
To maintain sliding for μ ∈ [0, 0.25]:
```latex
β⁻₁₁ = -β⁺₁₁ = 1.2
β⁻₁₂ = β⁺₂₁ = -β⁺₁₂ = -β⁻₂₁ = 2.1
β⁻₂₂ = -β⁺₂₂ = 6.4
K⁻ⱼ₁ = -2.4; K⁺ⱼ₁ = -15.2  for j=1,2
```

**Citation**:
- **Page 45, gains**: Robust gain selection for load range

**K₁₂, K₂₂ with Torque Feedback** (Equations 6.13-6.14, p. 46):
Disturbance terms include T₁, T₂, leading to:
```latex
K₁₂ = 5.5 + |T₂|/2    (6.13)
K₂₂ = 5.5 + |T₁|/2 + |T₂|    (6.14)
```

**Simplification**:
> "From an inspection of the values of T₁ and T₂ in simulations, we found that their variation was small and that (6.13), (6.14) could be replaced by constant K₁₂, K₂₂ using conservative bounds"

**Citation**:
- **Equations (6.13)-(6.14), p. 46**: Adaptive discontinuous gains
- **Page 46, simplification**: Practical constant approximation

**Thesis Use**: Robust controller design

#### Page 46: Performance with Load Variations

**No Load (μ = 0)** - Figure 10 (pp. 47-48):
- Boundary layer: ε₁ = ε₂ = 2.5°
- Tracking error: 0.9°

**Full Load (μ = 0.25)** - Figure 11 (pp. 49-51):
- Boundary layer: ε₁ = ε₂ = 2.5°
- Tracking error: 1.9°
- Figure 11c: Phase portraits showing no noticeable chattering

**Citation**:
- **Figures 10-11, pp. 47-51**: Robust performance across load range
- **Page 46, results**: Quantified tracking accuracy

**Improvement Strategies** (p. 46):
> "The tracking error may be decreased by decreasing the sampling time and the εⱼ's."

**Citation**:
- **Page 46, line 18**: Performance tuning guidelines

**Thesis Use**: Validation of robust tracking

#### Page 46: Comparison to Young [11]

**Existing Work**:
> "Young [11] has proposed the use of classical sliding surface methodology to stabilize a two dimensional manipulator, and has suggested extensions to tracking."

**Novel Contributions**:
> "Our approach is explicitly for the purpose of tracking and does not involve a 'reaching' phase to the sliding surface. By decoupling a multiple-input problem into several single-input problems, we avoid the problems associated with reaching a 'hierarchy' of sliding surfaces. By smudging the control across the discontinuity surface we mitigate the extent of the chattering."

**Citation**:
- **Page 46, lines 19-27**: Advantages over hierarchical approach

**Thesis Use**: Literature comparison

---

### Section 7: Further Research (pp. 52)

**Open Problems**:

1. **System Class Extension** (p. 52, lines 2-4):
> "The methodology needs to be extended to more general classes of non-linear systems than those discussed in Section 4."

2. **Output Feedback** (lines 4-6):
> "In its present form, the feedback control law uses full state feedback - the case of output feedback (with observers) remains to be investigated."

3. **Noise Effects** (lines 6-8):
> "In a related context, the effects of measurement noise and process noise on the sliding mode control methodology have yet to be studied."

4. **Trade-off Quantification** (lines 8-11):
> "The continuous control laws of Section 5 were derived in order to trade off the generation of undesirable high frequency signal against tracking accuracy. The precise nature of this trade-off needs to be quantified."

5. **Sampled-Data Implementation** (lines 11-17):
> "Finally, the use of sampled-data control to implement the sliding mode control presents new problems in the analysis of the resultant hybrid scheme. While sampled-data control was in fact used successfully in the example of Section 6, we believe that further research needs to be done in this direction"

6. **Experimental Validation** (lines 18-23):
> "We are now in the process of implementing sliding mode control laws on different kinds of manipulators and simulating their performance. Given the inherent non-linearities involved in all but Cartesian manipulators, we feel that our methodology is particularly suited for this application."

**Citation**:
- **Page 52, entire section**: Research directions identified in 1982
- **Historical Note**: Many have since been addressed in literature

**Thesis Use**: Context for modern developments

---

## References Section (pp. 54-55)

**Key References Cited**:

1. **Filippov [1]**: "Differential Equations with Discontinuous Right Hand Side", AMS Translations, Vol. 62 (1960), pp. 199-231
   - **Foundation**: Mathematical theory for discontinuous differential equations

2. **Flügge-Lotz [2]**: Discontinuous Automatic Control, Princeton (1953)
   - **Historical**: Early work on on-off controllers

3. **Utkin [7]**: Sliding Mode and its Applications to Variable Structure Systems, Mir., Moscow (1978)
   - **Soviet Literature**: Comprehensive sliding mode theory

4. **Utkin [8]**: "A Survey: Variable Structure Systems with Sliding Modes", IEEE Trans. Auto. Control, AC-22 (1977), pp. 212-222
   - **Survey Paper**: Overview of VSS methodology

5. **Horn et al. [15]**: "Dynamics of a Three Degree of Freedom Kinematic Chain", MIT AI Lab Memo 478, Oct. 1977
   - **Manipulator Dynamics**: Source for equations (6.1)-(6.2), (6.11)-(6.12)

**Citation**:
- **References section, pp. 54-55**: Complete bibliography
- **Note**: [7] and [8] are foundational Utkin works

---

## Figure/Equation Cross-Reference Table

| Figure/Eq | Page | Description | Thesis Use |
|-----------|------|-------------|------------|
| Fig 1 | 7 | Phase portraits near switching surface | Chattering illustration |
| Fig 2 | 9 | Hysteretic switching regularization | Physical interpretation |
| Fig 3 | 9 | Regularization effects (decreasing Δ) | Chattering frequency |
| Fig 4 | 12 | Filippov's f₀ construction | Equivalent control |
| Eq 2.4 | 10 | Filippov solution definition | Theoretical foundation |
| Eq 2.7 | 13 | Local sliding condition | Stability proof |
| Eq 2.8 | 13 | Global sliding condition | Convergence guarantee |
| Eq 3.5 | 18 | Sliding surface s = Cx̃ | Linear system design |
| Eq 3.7 | 18 | Control law structure | Implementation template |
| Eq 4.1 | 23 | Decoupled multi-input system | DIP formulation |
| Eq 4.7 | 25 | Nonlinear control law | General controller |
| Fig 6 | 34 | Boundary layer geometry | Continuous approximation |
| Fig 7 | 34 | Gain interpolation example | Implementation |
| Eq 5.8 | 36 | Tracking error bound | Performance prediction |
| Fig 8 | 40 | Two-link manipulator schematic | System diagram |
| Eq 6.1-6.2 | 39 | Manipulator dynamics | Equations of motion |
| Fig 9 | 43-44 | No-load simulation | Baseline performance |
| Fig 10 | 47-48 | Modified controller (no load) | Robust design |
| Fig 11 | 49-51 | Full load simulation | Load rejection |

---

## Page-by-Page Quick Reference

| Pages | Section | Key Content |
|-------|---------|-------------|
| 1-2 | Abstract, Intro | Problem statement, chattering issue |
| 2-5 | Section 1 | Motivation, time-varying surfaces, continuous approximation |
| 6-16 | Section 2 | Filippov theory, sliding conditions, time-varying extension |
| 17-22 | Section 3 | Linear systems, control design, disturbance rejection |
| 23-31 | Section 4 | Nonlinear systems, polynomial bounds, decoupling |
| 32-37 | Section 5 | Boundary layer, continuous control, accuracy trade-off |
| 38-51 | Section 6 | Two-link manipulator, simulation, load variations |
| 52 | Section 7 | Future research directions |
| 53-55 | Appendix | Acknowledgments, references |

---

## Citation Templates for Thesis

### For Time-Varying Sliding Surfaces:
> Slotine and Sastry [1983] introduced time-varying sliding surfaces for tracking control, eliminating the reaching phase inherent in classical sliding mode approaches. The sliding surface s(x;t) = Cx̃(t) is designed such that the constraint s = 0 enforces desired error dynamics.

**Reference**: Equations (4.3)-(4.4), p. 23

### For Boundary Layer Method:
> To mitigate chattering while maintaining robustness, the discontinuous control law is approximated by a continuous function within a boundary layer of thickness 2ε around the sliding surface [Slotine & Sastry, 1983]. This trades tracking accuracy (bounded by ε) for reduced high-frequency control activity.

**Reference**: Section 5, Equations (5.2)-(5.8), pp. 32-37

### For Decoupled Multi-Input Design:
> For systems of the form θⱼ^(nⱼ) = fⱼ(θ₁,...,θₚ;t) + uⱼ, Slotine and Sastry [1983] showed that each input can be designed independently using separate sliding surfaces sⱼ(θⱼ;t) = 0, avoiding hierarchical reaching phases.

**Reference**: Equations (4.1)-(4.4), pp. 23-24

### For Robustness to Uncertainties:
> The sliding mode control law requires only polynomial bounds on the nonlinearities (|fⱼ| ≤ Fⱼ(|θ|;t)) rather than exact system models, achieving invariance to matched disturbances during sliding mode [Slotine & Sastry, 1983].

**Reference**: Equations (4.2), (4.18)-(4.21), (4.24), pp. 23, 28-30

---

## Notes for Thesis Writing

### DIP-Specific Adaptations:
1. **Underactuated System**: DIP has 4 DOF, 1 input (unlike 2-link with 2 DOF, 2 inputs)
   - Cannot directly apply decoupled design
   - Need hierarchical approach or partial feedback linearization

2. **Applicable Concepts**:
   - Time-varying sliding surfaces (Section 3-4)
   - Boundary layer continuous approximation (Section 5)
   - Robustness to parameter variations (Section 4, pp. 20-21, 28-30)
   - Polynomial bound methodology (Section 4, Eq. 4.2)

3. **Key Differences from 2-Link**:
   - DIP: Collocated actuator affects non-collocated coordinates indirectly
   - 2-Link: Direct actuation at each joint
   - May need swing-up phase before tracking

### Recommended Citations:
- **Introduction**: General SMC tracking methodology
- **Controller Design**: Time-varying sliding surface concept
- **Implementation**: Boundary layer for chattering reduction
- **Simulation**: Robustness validation approach

### Complementary Papers to Cite:
- Utkin 1977 [8]: Classical sliding mode theory
- Filippov 1960 [1]: Mathematical foundations
- Levant 2007: Higher-order sliding modes (if using)

---

## Summary Statistics

- **Total Pages**: 55
- **Sections**: 7 main sections
- **Equations**: ~80 numbered equations
- **Figures**: 11 figures
- **References**: 15 cited works
- **Key Theorems**: Filippov's solution concept, uniqueness conditions
- **Examples**: Linear system (Section 3), Two-link manipulator (Section 6)

---

## Thesis Integration Checklist

- [ ] Cite time-varying sliding surface concept (Section 1, 3-4)
- [ ] Reference boundary layer method (Section 5)
- [ ] Compare to hierarchical approaches (Section 6, p. 46)
- [ ] Discuss polynomial bounds for DIP nonlinearities (Section 4)
- [ ] Adapt tracking error analysis (Section 5, Eq. 5.8)
- [ ] Use discontinuous gain selection methodology (Section 4, Eq. 4.9-4.13)
- [ ] Reference chattering problem (Section 1, 5)
- [ ] Cite robustness properties (Section 3-4, disturbance rejection)

---

**End of Citation Tracking Document**

*This tracking file comprehensively maps all equations, theorems, figures, and key concepts from Slotine & Sastry 1983 for efficient thesis citation and reference.*
