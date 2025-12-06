# Citation Tracking: Plestan et al. (2010) - Adaptive Sliding Mode Control

## Document Metadata

- **Authors**: F. Plestan, Y. Shtessel, V. Brégeault, A. Poznyak
- **Title**: New methodologies for adaptive sliding mode control
- **Publication**: International Journal of Control, 2010, Vol. 83, No. 9, pp. 1907-1919
- **DOI/HAL**: hal-00626498
- **Pages**: 20 pages (including references and appendix)
- **Local Path**: `thesis/sources_archive/articles/Plestan2010_Adaptive_Sliding_Mode.pdf`

**Keywords**: Adaptive sliding mode control, gain adaptation, uncertainty bounds, chattering reduction, real sliding mode, Lyapunov stability

---

## Quick Reference: Core Contributions

1. **Algorithm 1 (pp. 5-8)**: Hybrid adaptive gain combining reaching phase and equivalent control estimation
2. **Algorithm 2 (pp. 8-11)**: Original adaptive gain without equivalent control, guarantees real sliding mode
3. **ε-tuning methodology (pp. 10-12)**: Systematic approach for boundary layer parameter selection
4. **No uncertainty bound knowledge required**: Both algorithms work with only boundedness assumption
5. **Experimental validation**: Electropneumatic actuator application (pp. 13-17)

---

## Section-by-Section Citation Guide

### Section 1: Introduction (pp. 2-3)

**Motivation for adaptive SMC**:
> "The objective is the not-requirement of the uncertainties bound... dynamical adaptation of the control gain in order to be as small as possible whereas sufficient to counteract the uncertainties/perturbations" (p. 3)

**Cite for**:
- Chattering problem in SMC (p. 2)
- Over-estimation of gains in classical SMC
- Comparison with existing adaptive methods [10, 13]

**Page 2, Column 2**:
- Chattering analysis references: [3, 4]
- Higher-order SMC approaches: [14, 1, 15, 16, 12, 19]
- Fuzzy adaptive SMC limitations: [18, 24]

---

### Section 2.1: Problem Statement (pp. 2-4)

**System class considered**:
```latex
ẋ = f(x) + g(x) · u                                    (1)
```

**Sliding variable dynamics**:
```latex
σ̇ = ∂σ/∂t + ∂σ/∂x · f(x) + ∂σ/∂x · g(x) · u
  = Ψ(x,t) + Γ(x,t) · u                               (2)
```

**Bounded uncertainty assumption** (p. 3):
```latex
|Ψ| ≤ Ψ_M,   0 < Γ_m ≤ Γ ≤ Γ_M                       (3)
```

**Key point**: "It is assumed that Ψ_M, Γ_m and Γ_M exist but are not known" (p. 3)

**Cite for**:
- Problem formulation for uncertain nonlinear systems
- Relative degree 1 assumption
- Unknown but bounded uncertainties

---

### Section 2.2: Sliding Mode Definitions (p. 4)

**Definition 1 - Ideal Sliding Mode**:
```latex
S = {x ∈ X | σ(x,t) = 0}
```
> "The motion on S is called 'sliding mode' with respect to the sliding variable σ" (p. 4)

**Definition 2 - Real Sliding Surface** (with δ > 0):
```latex
S* = {x ∈ X | |σ| < δ}                                (4)
```

**Definition 3 - Real Sliding Mode**:
> "The corresponding behavior of system (1) on (4) is called 'real sliding mode'" (p. 4)

**Cite for**:
- Distinction between ideal vs. real sliding mode
- Practical implementation considerations

---

### Section 2.2: Review of Existing Approaches (pp. 4-5)

**Theorem 1 (Huang et al. [10])** - Gain dynamics proportional to |σ|:
```latex
u = -K(t) · sign(σ(x,t))
K̇ = K̄ · |σ(x,t)|                                     (5)
```

**Drawback**: "When σ = 0, K̇ = 0... gain K is clearly over-estimated" (p. 5)

**Theorem 2 (Lee & Utkin [13])** - Equivalent control based:
```latex
K(t) = K̄ · |η| + χ
τ · η̇ + η = sign(σ(x,t))
```

**Requirement**: K̄ ≥ |Ψ/Γ| (needs uncertainty bound knowledge)

**Cite for**:
- Limitations of existing adaptive SMC methods
- Gain over-estimation problem
- Need for low-pass filter in equivalent control approach

---

## Section 3.1: Algorithm 1 - Hybrid Adaptive SMC (pp. 5-8)

### Control Law Structure

**Control input**:
```latex
u = -K · sign(σ(x,t))                                  (7)
```

**Gain dynamics - Reaching phase** (|σ| ≠ 0):
```latex
K̇ = K̄_1 · |σ(x,t)|                                   (8)
```
with K̄_1 > 0 and K(0) > 0

**Gain dynamics - Sliding phase** (σ = 0):
```latex
K(t) = K̄_2 · |η| + K̄_3
τη̇ + η = sign(σ(x,t))                                 (9)
```
with K̄_2 = K(t*), K̄_3 > 0, τ > 0

**Key innovation**: t* is the transition time from |σ| ≠ 0 to σ = 0

### Theoretical Results

**Lemma 1 (p. 6)**: Gain boundedness
> "There exists a positive constant K* so that K(t) ≤ K*, ∀t > 0"

**Theorem 3 (pp. 6-8)**: Finite-time convergence to ideal sliding mode
> "There exists a finite time t_F > 0 so that a sliding mode is established for all t ≥ t_F, i.e. σ(x,t) = 0 for t ≥ t_F"

**Lyapunov function** (p. 6):
```latex
V = (1/2)σ² + (1/2γ)(K - K*)²                         (10)
```

**Derivative during reaching phase** (p. 7):
```latex
V̇ = -(Γ_m · K* - Ψ_M) · |σ| - (-Γ_m · |σ| + K̄/γ · |σ|) · |K - K*|  (11)
```

**Convergence rate** (p. 7):
```latex
V̇ ≤ -β · V^(1/2)                                      (12)
```
with β = √2 min{β_σ, β_K√γ}

**Reaching time estimate** (p. 7):
```latex
t_r ≤ 2V(0)^(1/2) / β
```

### Implementation for Real Systems (pp. 7-8)

**Modified gain dynamics with boundary layer ε**:

**If |σ(x,t)| > ε > 0**:
```latex
K̇ = K̄_1 · |σ(x,t)|                                   (13)
```

**If |σ(x,t)| ≤ ε**:
```latex
K(t) = K̄_2 · |η| + K̄_3
τη̇ + η = sign(σ(x,t))                                 (14)
```

**Corollary 1 (p. 8)**: Real sliding mode establishment
> "There exists a finite time t_F > 0 so that a real sliding mode is established for all t ≥ t_F, i.e. |σ(x,t)| < ε for t ≥ t_F"

**Cite for**:
- Combining adaptive reaching with equivalent control
- Preventing gain over-estimation
- Practical implementation with boundary layer

---

## Section 3.2: Algorithm 2 - Original Adaptive SMC (pp. 8-11)

### Control Law Structure

**Control input**:
```latex
u = -K · sign(σ(x,t))                                  (15)
```

**Gain dynamics**:
```latex
K̇ = { K̄ · |σ(x,t)| · sign(|σ(x,t)| - ε)   if K > μ
    { μ                                      if K ≤ μ   (16)
```
with K(0) > 0, K̄ > 0, ε > 0, μ > 0 very small

**Key innovation**: Gain increases when |σ| > ε, decreases when |σ| < ε, automatically adjusts to uncertainty magnitude

### Theoretical Results

**Lemma 2 (p. 8)**: Gain boundedness (proof in Appendix p. 20)
> "The gain K(t) has an upper-bound, i.e. there exists a positive constant K* so that K(t) ≤ K*, ∀t > 0"

**Theorem 4 (pp. 8-11)**: Real sliding mode with bounded accuracy
> "There exists a finite time t_F > 0 so that a real sliding mode is established for all t ≥ t_F, i.e. |σ(x,t)| < δ for t ≥ t_F"

**Accuracy bound**:
```latex
δ = √(ε² + Ψ²_M / (K̄ Γ_m))                           (17)
```

**Lyapunov function** (p. 9):
```latex
V = (1/2)σ² + (1/2γ)(K - K*)²                         (18)
```

**Derivative analysis** (p. 9):
```latex
V̇ ≤ Ψ_M · |σ| - Γ_m · K · |σ| + (1/γ)(K - K*) · K̄ · |σ| · sign(|σ| - ε)
```

**Introducing β_K** (p. 9):
```latex
V̇ = -(−Ψ_M + Γ_m · K*) · |σ| - β_K · |K - K*| - ξ    (20)
```

where:
```latex
ξ = [-Γ_m · |σ| + K̄/γ · |σ| · sign(|σ| - ε) - β_K] · |K - K*|
```

### Case Analysis (pp. 9-11)

**Case 1: |σ| > ε** (p. 9)

ξ is positive if:
```latex
γ < K̄ · ε / (Γ_m · ε + β_K)                          (22)
```

Then:
```latex
V̇ ≤ -β · V^(1/2)                                      (23)
```

**Case 2: |σ| < ε** - Overshoot analysis (pp. 10-11)

Worst-case dynamics:
```latex
σ̇ = Ψ_M - K · Γ_m
K̇ = K̄ · |σ|                                          (24)
```

**Closed-form solution** (p. 10):
```latex
σ(t) = σ_0 cos(√(K̄Γ_m)t) + (Ψ_M - K_0 · Γ_m)/√(K̄Γ_m) · sin(√(K̄Γ_m)t)

K(t) = σ_0√(K̄/Γ_m) sin(√(K̄Γ_m)t) + (K_0 - Ψ_M/Γ_m) cos(√(K̄Γ_m)t) + Ψ_M/Γ_m   (25)
```

**Maximum amplitude**:
```latex
σ(t) = √(σ²_0 + (Ψ_M - K_0 · Γ_m)²/(K̄Γ_m)) sin(√(K̄Γ_m)t + Θ_σ)

K(t) = √(σ²_0 · K̄/Γ_m + (K_0 - Ψ_M/Γ_m)²) sin(√(K̄Γ_m)t + Θ_K) + Ψ_M/Γ_m    (26)
```

**Deriving accuracy bound** (p. 10):
When σ_0 = ε⁺ → ε:
```latex
δ = √(ε² + Ψ²_M/(K̄Γ_m))                              (27)
```

**Cite for**:
- Adaptive SMC without equivalent control
- Automatic gain adjustment to uncertainty level
- Explicit accuracy-parameter relationship
- Oscillation analysis during adaptation

---

## Section 4: ε-Tuning Methodology (pp. 10-12)

### Problem Statement

**Two failure modes**:
1. **ε too small**: |σ| never stays below ε → K increases indefinitely → instability
2. **ε too large**: |σ| always below ε → poor tracking accuracy

**Design principle**: "ε should rather be too large than too small" (p. 11)

### Tuning Methodology

**Requirement**: As long as K(t) ≥ |Ψ/Γ|, ensure |σ| < ε

**At time t_1 where |σ(t_1)| ≤ ε and K(t_1) ≥ |Ψ(t_1)/Γ(t_1)|**:

**Euler approximation** (p. 11):
```latex
σ(t_1 + T_e) ∼ σ(t_1) + [Ψ(t_1) - Γ(t_1) · K(t_1) · sign(σ(t_1))] · T_e   (29)
```

**Bound on derivative**:
```latex
|Ψ(t_1) - Γ(t_1) · K(t_1) · sign(σ(t_1))| ≤ 2Γ_M · K(t_1)
```

**Worst case** (σ(t_1) = 0):
```latex
|σ(t_1 + T_e)| ≤ 2Γ_M · K(t_1)T_e                     (30)
```

**Optimal time-varying ε** (p. 11):
```latex
ε(t) = 2Γ_M · K(t_1)T_e                               (31)
```

### Practical Simplification (pp. 11-12)

**For systems with nominal + uncertain parts**:
```latex
Ψ = Ψ_Nom + ΔΨ,   Γ = Γ_Nom + ΔΓ
```

**Control law transformation**:
```latex
u = (-Ψ_Nom + v) / Γ_Nom
```

**Transformed dynamics**:
```latex
σ̇ = (ΔΨ + Ψ_Nom/Γ_Nom · ΔΓ) + (1 - ΔΓ/Γ_Nom) · v    (32)
```

**If |Γ_Nom| ≥ |ΔΓ|**, then |1 - ΔΓ/Γ_Nom| ≤ 2

**Simplified ε tuning**:
```latex
ε(t) = 4K(t)T_e
```

**Cite for**:
- Systematic boundary layer parameter selection
- Time-varying ε approach
- Practical tuning guidelines
- Relationship between ε, K, and sampling time

---

## Section 5: Simulation Examples

### 5.1 Tutorial Example (pp. 12-13)

**System**:
```latex
σ̇ = Ψ(t) + u                                         (33)
```

**Parameters**:
- σ(0) = 10
- T_e = 0.0001 sec
- ε(t) = 2K(t) · T_e
- Ψ(t): time-varying unknown bounded function (Figure 1, p. 12)

**Algorithm 1 tuning** (p. 13):
- K(0) = 10
- K̄_1 = 1000
- K̄_3 = 1
- τ = 0.1 sec

**Algorithm 2 tuning** (p. 13):
- K(0) = 10
- K̄ = 1000
- μ = 0.1

**Results** (Figures 2-3, pp. 13-14):
> "Both control laws yield to very similar results... both adaptation algorithms provide the controller gain K(t) to follow closely the perturbation Ψ(t)... control gain K(t) is not over-estimated and control chattering is minimal" (p. 13)

### 5.2 Electropneumatic Actuator (pp. 13-17)

**System model** (p. 14):
```latex
ṗ_P = (krT/V_P(y))[q_mN(u,p_p) - S_P/(rT) p_P v]
ṗ_N = (krT/V_N(y))[q_mP(-u,p_N) + S_N/(rT) p_N v]
v̇ = (1/M)[S_P p_P - S_N p_N - bv - F_f - F_ext]
ẏ = v                                                  (34)
```

**Mass flow rate model** (p. 15):
```latex
q_mP(u,p_P) = φ_P(p_P) + ψ_P(p_P, sgn(u)) · u
q_mN(-u,p_N) = φ_N(p_N) - ψ_N(p_N, sgn(-u)) · u      (35)
```

**Uncertainties considered** (p. 15):
- Viscous/dry friction coefficients
- Mass flow rate ±15% on φ(·), ±5% on ψ(·)
- Total mass variation: 17-47 kg

**Sliding variable** (p. 15):
```latex
σ = λ²·(y - y_d(t)) + 2λ·(ẏ - ẏ_d(t)) + (ÿ - ÿ_d(t))  (36)
```

**Transformed dynamics**:
```latex
σ̇ = Ψ(·) + Γ(·) · u                                  (37)
Ψ(·) = Ψ_Nom(·) + ΔΨ(·),   Γ(·) = Γ_Nom(·) + ΔΓ(·)    (38)
```

**Control law**:
```latex
u = (1/Γ_Nom)(-Ψ_Nom + v)                             (39)
```

**Tuning parameters** (p. 16):
- T_e = 10⁻³ sec
- K̄ = 250
- K̄_1 = 50
- K(0) = 1
- λ = 33
- ε(t) = 4K(t)·T_e

**Algorithm 1 additional**:
- K̄_3 = 1
- τ = 0.1 sec

**Algorithm 2 additional**:
- μ = 0.1

**Test conditions** (p. 16):
- Mass variation: +20%
- Uncertainty on φ and ψ: -20%

**Results** (Figures 6-7, pp. 17-18):
> "Both strategies yield to quite similar results... Algorithm 1 induces lower magnitudes of control and gain in this time interval... implementation of Algorithm 2 is clearly more easy" (p. 16)

**Cite for**:
- Real system application example
- Parameter tuning guidelines
- Comparative performance analysis
- Practical implementation insights

---

## Appendix: Lemma Proofs (pp. 19-20)

### Proof of Lemma 1 (p. 19)

**Gain evolution for |σ| ≠ 0**:
1. K increases until K(t_1) > Ψ_M/Γ_m
2. At t_1, gain is large enough to make σ decrease
3. At t_2, σ = 0 and K(t_2) has bounded value
4. Therefore ∃K* > 0: K* > K(t), ∀t ≥ 0

### Proof of Lemma 2 (pp. 19-20)

**Cyclic behavior** (illustrated in Figure 8, p. 20):

1. **t_1**: K increases until K(t_1) = |Ψ(t_1)/Γ(t_1)|
2. **t_2**: |σ| < ε reached, K at maximum
3. **t_3**: K decreases to K(t_3) = |Ψ(t_3)/Γ(t_3)|
4. **t_4**: K insufficient, |σ(t_4)| > ε, cycle restarts

**Boundedness**:
```latex
K(t_i) = |Ψ(t_i)/Γ(t_i)| ≤ Ψ_M/Γ_m := K**
```

Therefore:
```latex
∃K*: K* ≤ K** ⟹ K(t) bounded ∀t
```

**Cite for**:
- Stability proof techniques
- Lyapunov-based analysis
- Gain boundedness arguments

---

## Key Equations Cross-Reference

| Equation | Page | Description | LaTeX |
|----------|------|-------------|-------|
| (1) | 2 | System dynamics | `ẋ = f(x) + g(x)·u` |
| (2) | 3 | Sliding variable dynamics | `σ̇ = Ψ(x,t) + Γ(x,t)·u` |
| (3) | 3 | Uncertainty bounds | `\|Ψ\| ≤ Ψ_M, 0 < Γ_m ≤ Γ ≤ Γ_M` |
| (4) | 4 | Real sliding surface | `S^* = \{x ∈ X \| \|σ\| < δ\}` |
| (5) | 4 | Huang et al. gain law | `K̇ = K̄·\|σ(x,t)\|` |
| (7) | 5 | Algorithm 1 control | `u = -K·sign(σ(x,t))` |
| (8) | 5 | Alg 1 reaching phase | `K̇ = K̄_1·\|σ(x,t)\|` |
| (9) | 5 | Alg 1 sliding phase | `K(t) = K̄_2·\|η\| + K̄_3` |
| (10) | 6 | Lyapunov function | `V = (1/2)σ² + (1/2γ)(K-K*)²` |
| (11) | 7 | V̇ decomposition | See p. 7 |
| (12) | 7 | Convergence rate | `V̇ ≤ -β·V^(1/2)` |
| (13) | 7 | Alg 1 modified (reach) | `K̇ = K̄_1·\|σ(x,t)\|` for \|σ\| > ε |
| (14) | 8 | Alg 1 modified (slide) | `K(t) = K̄_2·\|η\| + K̄_3` for \|σ\| ≤ ε |
| (15) | 8 | Algorithm 2 control | `u = -K·sign(σ(x,t))` |
| (16) | 8 | Alg 2 gain dynamics | `K̇ = K̄·\|σ\|·sign(\|σ\|-ε)` |
| (17) | 8 | Accuracy bound | `δ = √(ε² + Ψ²_M/(K̄Γ_m))` |
| (18) | 9 | Lyapunov (Alg 2) | `V = (1/2)σ² + (1/2γ)(K-K*)²` |
| (22) | 9 | γ condition | `γ < K̄·ε/(Γ_m·ε + β_K)` |
| (24) | 10 | Worst-case dynamics | `σ̇ = Ψ_M - K·Γ_m, K̇ = K̄·\|σ\|` |
| (25)-(26) | 10 | Overshoot solution | See pp. 10-11 |
| (27) | 10 | Accuracy (alt form) | `δ = √(ε² + Ψ²_M/(K̄Γ_m))` |
| (29) | 11 | Euler approximation | `σ(t_1+T_e) ∼ σ(t_1) + ...` |
| (30) | 11 | Worst-case bound | `\|σ(t_1+T_e)\| ≤ 2Γ_M·K(t_1)T_e` |
| (31) | 11 | Optimal ε | `ε(t) = 2Γ_M·K(t_1)T_e` |
| (32) | 12 | Transformed dynamics | See p. 12 |
| (36) | 15 | Electropneumatic σ | `σ = λ²·(y-y_d) + 2λ·(ẏ-ẏ_d) + (ÿ-ÿ_d)` |
| (39) | 16 | Nominal inversion | `u = (1/Γ_Nom)(-Ψ_Nom + v)` |

---

## Implementation Notes for DIP Thesis

### Algorithm Selection

**Algorithm 1 advantages**:
- Potentially lower control effort
- Uses equivalent control concept (established theory)
- Better initial transient in some cases

**Algorithm 1 disadvantages**:
- More parameters to tune (K̄_1, K̄_2, K̄_3, τ)
- Low-pass filter adds dynamics
- τ tuning is not trivial

**Algorithm 2 advantages** (recommended for DIP):
- Simpler implementation (fewer parameters)
- No low-pass filter required
- Explicit accuracy bound δ = √(ε² + Ψ²_M/(K̄Γ_m))
- Authors state "implementation... is clearly more easy" (p. 16)

**Algorithm 2 disadvantages**:
- May have higher initial gain overshoot
- Guarantees only real sliding mode (not ideal)

### Parameter Tuning Guidelines

**For Algorithm 2 applied to DIP**:

1. **Sampling time T_e**: Use 0.001 sec (1 kHz) or 0.0001 sec (10 kHz)

2. **Initial gain K(0)**: Start small (K(0) = 1-10)
   - System will automatically increase it
   - Prevents initial control saturation

3. **Adaptation rate K̄**:
   - Start with K̄ = 50-250
   - Larger K̄ → faster adaptation but more overshoot
   - Tune based on convergence speed vs. smoothness trade-off

4. **Boundary layer ε**:
   - Use time-varying: ε(t) = 4K(t)T_e
   - Or conservative constant: ε = 4K_max·T_e where K_max is estimated max gain

5. **Lower bound μ**: Set to 0.1-1.0 to prevent K → 0

6. **Accuracy estimate**:
   ```latex
   δ ≈ √(ε² + Ψ²_M/(K̄Γ_m))
   ```
   - After tuning, verify δ meets performance requirements

### DIP-Specific Adaptations

**Sliding variable for DIP** (4-DOF system):
```latex
σ_i = λ²_i·(θ_i - θ_{di}) + 2λ_i·(θ̇_i - θ̇_{di}) + (θ̈_i - θ̈_{di})
```
for i = 1,2 (two angles)

**Control gain per DOF**:
- Each σ_i has its own K_i(t)
- Independent adaptation: K̇_i = K̄_i·|σ_i|·sign(|σ_i| - ε_i)

**Uncertainty sources in DIP**:
- Model simplification errors (Ψ term)
- Unmodeled friction
- Parameter variations (mass, length, etc.)
- External disturbances
- Measurement noise

**Expected performance** (from electropneumatic example):
- Position tracking error: < 2mm for 400mm stroke
- Control effort: reasonable magnitude without saturation
- Adaptation time: 0.5-2 seconds to reach steady-state gain
- Gain follows disturbance magnitude closely

### Comparison with Classical SMC

**Classical SMC** (Slotine & Sastry 1983):
```latex
u = -K_constant·sign(σ)
K_constant ≥ (Ψ_M + η)/Γ_m
```

Requires:
- Knowledge of Ψ_M (max uncertainty)
- Conservative over-estimation
- Excessive chattering

**Plestan et al. Adaptive SMC** (Algorithm 2):
```latex
u = -K(t)·sign(σ)
K̇ = K̄·|σ|·sign(|σ| - ε)
```

Advantages:
- No knowledge of Ψ_M needed
- K adapts to actual disturbance level
- Reduced chattering
- Automatic gain adjustment to changing conditions

**Trade-off**: Real sliding mode (|σ| < δ) vs. ideal (σ = 0)

### Thesis Integration Checklist

- [ ] **Section 2.3** (Control Design): Present Algorithm 2 as main adaptive SMC
- [ ] **Section 2.4** (Stability Analysis): Cite Theorem 4 for finite-time convergence
- [ ] **Section 3.1** (Implementation): Use ε-tuning methodology from Section 4
- [ ] **Section 3.2** (Parameter Selection): Follow tuning guidelines from pp. 12-13, 16
- [ ] **Section 4.1** (Simulation Setup): Compare with classical SMC (show adaptation)
- [ ] **Section 4.2** (Results): Plot K(t) evolution, show gain follows disturbance
- [ ] **Section 4.3** (Chattering Analysis): Compare chattering with/without adaptation
- [ ] **Section 5** (Discussion): Discuss real vs. ideal sliding mode trade-off
- [ ] **References**: Include [Plestan2010] for adaptive SMC methodology

### Citation Templates

**For adaptive gain methodology**:
> "The adaptive gain law follows the approach of Plestan et al. [Plestan2010], where the gain K(t) dynamically adjusts based on the sliding variable magnitude, eliminating the need for a priori knowledge of uncertainty bounds."

**For avoiding over-estimation**:
> "Unlike classical SMC which requires conservative over-estimation of uncertainty bounds, the adaptive scheme [Plestan2010, Sec. 3.2] automatically adjusts the gain to match the actual disturbance level, reducing chattering while maintaining robustness."

**For real sliding mode**:
> "Following [Plestan2010, Theorem 4], the adaptive controller establishes a real sliding mode with accuracy δ = √(ε² + Ψ²_M/(K̄Γ_m)), providing explicit bounds on tracking performance."

**For ε-tuning**:
> "The boundary layer parameter is selected using the time-varying approach ε(t) = 4K(t)T_e [Plestan2010, p. 12], ensuring stability while maximizing accuracy."

**For implementation**:
> "Implementation follows the practical guidelines in [Plestan2010, Sec. 5.2] for sampled-data systems, with adaptation rate K̄ tuned to balance convergence speed and overshoot."

---

## Related Work Connections

**From Plestan et al. 2010 references**:

1. **Slotine & Sastry 1983** [22]: Classical SMC baseline - requires uncertainty bounds
2. **Utkin et al. 1999** [25]: General SMC theory and chattering analysis
3. **Levant 1993, 2001, 2007** [14, 15, 16]: Higher-order SMC - also needs bounds
4. **Huang et al. 2008** [10]: Previous adaptive approach - over-estimates gain
5. **Lee & Utkin 2007** [13]: Equivalent control approach - needs bounds for design
6. **Bartolini et al. 2000** [1]: Multi-input SMC
7. **Laghrouche et al. 2006, 2007** [11, 12]: Optimal HOSMC, integral sliding surfaces

**Thesis positioning**:
- Builds on classical SMC [Slotine1983]
- Improves upon by removing uncertainty bound requirement [Plestan2010]
- Reduces chattering compared to classical approach
- Simpler than higher-order SMC [Levant]
- More practical than fuzzy adaptive methods

---

## Page-by-Page Quick Reference

| Pages | Content | Key Equations | Use For |
|-------|---------|---------------|---------|
| 2-3 | Introduction, motivation | - | Problem context |
| 3-4 | Problem statement | (1)-(3) | System class |
| 4-5 | Existing methods review | (5), Thm 1-2 | Limitations |
| 5-8 | Algorithm 1 | (7)-(14), Thm 3 | Hybrid adaptive |
| 8-11 | Algorithm 2 | (15)-(27), Thm 4 | Main contribution |
| 10-12 | ε-tuning | (29)-(31) | Parameter selection |
| 12-13 | Tutorial example | (33) | Simple validation |
| 13-17 | Electropneumatic | (34)-(39) | Real system |
| 17-18 | Results discussion | Figs 6-7 | Performance |
| 19-20 | Appendix proofs | Lemmas 1-2 | Stability |

---

## Summary: Why This Paper Matters for DIP Thesis

**Core value**:
1. Eliminates need to know/estimate uncertainty bounds (major practical advantage)
2. Automatic gain tuning reduces chattering while maintaining robustness
3. Explicit accuracy bounds enable performance prediction
4. Validated on real nonlinear system (electropneumatic actuator)
5. Clear implementation guidelines with parameter tuning methodology

**Direct applications to DIP**:
- Uncertain pendulum parameters (length, mass, friction) → no need to bound them
- Time-varying disturbances → gain adapts automatically
- Sampling rate constraints → ε-tuning accounts for T_e
- Multi-DOF extension → independent K_i for each angle
- Chattering reduction → important for real hardware

**Theoretical contributions**:
- Lyapunov-based finite-time stability proofs (Theorems 3-4)
- Explicit accuracy-parameter relationships (Eq. 17, 27)
- Gain boundedness guarantees (Lemmas 1-2)
- Systematic design methodology (not just heuristic tuning)

**Use Algorithm 2** for DIP implementation - simpler, more robust, clearly superior for practical applications per authors' conclusion.

---

**File created**: 2025-12-06
**Status**: Complete - ready for thesis integration
**Next**: Khalil2002_tracking.md (Lyapunov stability theory and nonlinear systems)
