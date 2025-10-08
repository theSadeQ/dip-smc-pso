# Citation Request: Exponential Stability of Sliding Surface Dynamics

I need academic citations for the exponential stability theorem of sliding mode control surfaces.

## THEOREM STATEMENT

"If all sliding surface parameters c_i > 0, then the sliding surface dynamics are exponentially stable with convergence rates determined by c_i."

## TECHNICAL CONTEXT

**Domain:** Sliding Mode Control (SMC) theory - specifically sliding surface design

**Sliding Surface Definition:**

For an nth-order system, the sliding surface is typically defined as:
```
s = c₁e + c₂ė + c₃ë + ... + c_n e^(n-1) + e^(n)
```

Or in state-space form for tracking error e = x_d - x:
```
s = [c_n-1, c_n-2, ..., c_1, 1] · [e, ė, ë, ..., e^(n-1)]ᵀ
```

**Sliding Surface Dynamics:**

When system is constrained to sliding surface (s = 0), the error dynamics become:
```
e^(n) + c_n-1·e^(n-1) + ... + c₂·ë + c₁·ė = 0
```

This is a linear homogeneous ODE whose stability depends on polynomial:
```
λⁿ + c_n-1·λ^(n-1) + ... + c₂·λ² + c₁·λ = 0
```

**Exponential Stability:**

System is exponentially stable if all eigenvalues (roots of characteristic polynomial) have negative real parts:
```
Re(λ_i) < 0   for all i
```

Then solution decays exponentially:
```
||e(t)|| ≤ M·||e(0)||·exp(-α·t)
```

where α = min|Re(λ_i)| determines convergence rate.

**Theorem Interpretation:**

The theorem states that positive parameters c_i > 0 guarantee:
1. All roots of characteristic polynomial have negative real parts (Hurwitz stability)
2. Error converges exponentially to zero: e(t) → 0 as t → ∞
3. Convergence speed is determined by the choice of c_i values

## REQUIRED CITATIONS

Find 2-3 papers/books that:

1. **Establish Hurwitz stability conditions** for sliding surface parameter selection
2. **Prove exponential convergence** of sliding mode error dynamics for positive parameters
3. **Relate convergence rates** to sliding surface coefficients c_i

**Classic references preferred:**
- **Utkin** - Sliding mode control founding papers
- **Slotine & Li** - Applied Nonlinear Control (sliding surface design chapter)
- **Edwards & Spurgeon** - Sliding Mode Control: Theory and Applications
- **Khalil** - Nonlinear Systems (relevant exponential stability theorems)

## OUTPUT FORMAT

For each citation:

1. **Full Citation:** Authors, "Title," Book/Journal, Year, Pages
2. **DOI/ISBN/URL:** Link or identifier
3. **Relevance:** Which theorem/section establishes exponential stability of sliding surfaces?
4. **Key Equation:** Characteristic polynomial, stability condition, or convergence rate formula

## FOCUS AREAS

Essential topics:
- Sliding surface design and parameter selection
- Hurwitz polynomial stability
- Exponential stability of linear error dynamics
- Convergence rate analysis in sliding mode control
- Pole placement interpretation of c_i parameters

Provide authoritative citations establishing that positive sliding surface parameters guarantee exponential stability.
