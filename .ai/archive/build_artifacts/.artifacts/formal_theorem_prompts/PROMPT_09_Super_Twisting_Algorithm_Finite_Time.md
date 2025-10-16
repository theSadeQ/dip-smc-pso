# Citation Request: Super-Twisting Algorithm Finite-Time Convergence

I need academic citations for the finite-time convergence theorem of the Super-Twisting Algorithm (STA).

## THEOREM STATEMENT

"The super-twisting algorithm ensures finite-time convergence to the second-order sliding set {s = 0, ṡ = 0} if the parameters satisfy [specific conditions]."

## TECHNICAL CONTEXT

**Domain:** Second-Order Sliding Mode Control - Super-Twisting Algorithm (STA)

**Background:**

Classical SMC achieves first-order sliding (s = 0), but requires discontinuous control in the feedback loop, causing chattering.

Super-twisting achieves **second-order sliding** (s = 0 AND ṡ = 0) with:
- Continuous control signal (no chattering)
- Only sliding variable s needed (not ṡ)
- Finite-time convergence

**Super-Twisting Algorithm:**
```
u̇ = -α·sgn(s)
u = -λ·|s|^(1/2)·sgn(s) + u̇
```

Or equivalently:
```
u = -λ·|s|^(1/2)·sgn(s) - α·∫sgn(s)dt
```

Where:
- s: sliding variable
- λ, α > 0: algorithm gains
- |s|^(1/2): fractional power (0.5)
- sgn(s): sign function

**System Model:**

Consider second-order system:
```
ṡ = φ(t,x) + γ(t,x)·u
s̈ = φ̇ + γ̇·u + γ·u̇
```

With bounded uncertainty:
```
|φ̇| ≤ Φ
0 < γ_min ≤ γ ≤ γ_max
```

**Convergence Conditions:**

Parameters λ, α must satisfy specific inequalities involving bounds Φ, γ_min, γ_max.

Classic sufficient conditions (Levant 1993):
```
λ > √(2Φ/γ_min)
α > Φ/γ_min
```

Or with tighter bounds (Moreno & Osorio 2008):
```
λ² ≥ 4Φ·(α+Φ)/(γ_min·(α-Φ))
```

**Second-Order Sliding Mode:**

System reaches **second-order sliding set**:
```
S² = {(s, ṡ) : s = 0, ṡ = 0}
```

This is stronger than classical SMC which only achieves s = 0 (but ṡ may oscillate/chatter).

## THEOREM SIGNIFICANCE

Super-twisting algorithm represents major advancement:
1. **Chattering reduction:** Continuous control (no high-frequency switching)
2. **Robustness:** Works with bounded uncertainties like classical SMC
3. **Finite-time:** Convergence in finite time T < ∞
4. **Practical:** Only requires s measurement (not ṡ)

## REQUIRED CITATIONS

Find 2-3 papers that:

1. **Prove finite-time convergence** of super-twisting to second-order sliding set
2. **Establish parameter conditions** (λ, α) for convergence with bounded uncertainties
3. **Provide Lyapunov analysis** or convergence time bounds

**Essential references:**
- **Levant (1993, 2003)** - Original super-twisting algorithm papers
- **Moreno & Osorio (2008, 2012)** - Strict Lyapunov functions for STA
- **Shtessel et al. (2014)** - Sliding Mode Control and Observation, Chapter 5
- **Edwards & Shtessel (2016)** - Adaptive continuous higher order sliding mode control

## OUTPUT FORMAT

For each citation:

1. **Full Citation:** Authors, "Title," Journal/Conference, Year, Pages
2. **DOI/URL:** Link
3. **Relevance:** Which theorem establishes finite-time convergence to {s=0, ṡ=0}?
4. **Key Condition:** Parameter inequalities for λ, α guaranteeing convergence

## FOCUS AREAS

Critical topics:
- Super-twisting algorithm formulation
- Second-order sliding mode definition
- Finite-time convergence proofs (Lyapunov, homogeneity)
- Parameter tuning conditions
- Chattering reduction compared to classical SMC

**Historical context:**
- Levant (1993): Original STA paper
- Levant (2003): Homogeneity-based analysis
- Moreno & Osorio (2008): Strict Lyapunov function (major breakthrough)

Provide authoritative citations proving super-twisting's finite-time convergence to second-order sliding.
