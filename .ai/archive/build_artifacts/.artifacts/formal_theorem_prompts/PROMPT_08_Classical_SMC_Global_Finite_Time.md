# Citation Request: Classical SMC Global Finite-Time Convergence

I need academic citations for the global finite-time convergence theorem of classical sliding mode control.

## THEOREM STATEMENT

"The classical SMC law with switching gain η > ρ (where ρ is the uncertainty bound) ensures global finite-time convergence to the sliding surface."

## TECHNICAL CONTEXT

**Domain:** Classical Sliding Mode Control for uncertain nonlinear systems

**System Model:**

Consider uncertain nonlinear system:
```
ẋ = f(x,t) + b(x,t)·u + d(x,t)
```

Where:
- f(x,t): nominal dynamics (known)
- b(x,t): control input gain (known, b > 0)
- d(x,t): matched uncertainty/disturbance (unknown but bounded)
- Uncertainty bound: |d(x,t)| ≤ ρ

**Classical SMC Control Law:**
```
u = u_eq - η·sgn(s)
```

Where:
- u_eq: equivalent control (makes ṡ = 0 in nominal case)
- η: switching gain
- sgn(s): sign function
- s: sliding surface

**Mathematical Structure:**
```
u_eq = -(1/b(x))·[∂s/∂x·f(x) + ∂s/∂t]
u = u_eq - (η/b(x))·sgn(s)
```

**Derivation of Convergence:**

Sliding surface dynamics:
```
ṡ = ∂s/∂x·(f + b·u + d) + ∂s/∂t
ṡ = ∂s/∂x·b·(-η·sgn(s)) + ∂s/∂x·d
ṡ = -b·η·sgn(s) + d
```

Choosing η > ρ/b_min ensures:
```
s·ṡ = s·(-b·η·sgn(s) + d)
     = -b·η·|s| + s·d
     ≤ -b·η·|s| + |d|·|s|
     ≤ -(b·η - |d|)·|s|
     ≤ -(b·η - ρ)·|s| < 0
```

This satisfies reaching condition → **finite-time convergence** to s = 0.

**Global Property:**
Works for **any initial condition** x(0), not just locally near equilibrium.

## THEOREM SIGNIFICANCE

This theorem establishes fundamental SMC properties:
1. **Robustness:** Convergence despite unknown disturbances d(x,t)
2. **Finite-time:** Not just asymptotic (t → ∞), but finite-time (t = T < ∞)
3. **Global:** From any initial state in state space
4. **Guaranteed by gain:** Simply choose η > ρ (larger than uncertainty bound)

## REQUIRED CITATIONS

Find 2-3 authoritative papers/books that:

1. **Prove global finite-time convergence** for classical SMC with uncertainty bounds
2. **Establish switching gain conditions** (η > ρ) for robustness
3. **Derive reaching time bounds** as function of η and ρ

**Essential references:**
- **Utkin (1977, 1992)** - Founding papers on variable structure systems
- **Slotine & Sastry (1983)** - Tracking control of nonlinear systems using sliding surfaces
- **Slotine & Li (1991)** - Applied Nonlinear Control, Chapter 7 (classical SMC)
- **Edwards & Spurgeon (1998)** - SMC Theory and Applications, Chapter 2
- **Khalil (2002)** - Nonlinear Systems, Section on sliding mode control

## OUTPUT FORMAT

For each citation:

1. **Full Citation:** Authors, "Title," Venue/Book, Year, Pages
2. **DOI/ISBN/URL:** Link
3. **Relevance:** Which theorem proves finite-time convergence with bounded uncertainties?
4. **Key Condition:** Statement of switching gain requirement (η > ρ or similar)

## FOCUS AREAS

Core topics:
- Classical sliding mode control structure
- Uncertainty bounds and matched disturbances
- Switching gain selection (η > ρ)
- Global finite-time stability proofs
- Robustness properties of SMC

**Distinguish from:**
- Super-twisting algorithm (higher-order SMC)
- Adaptive SMC (time-varying gains)
- Boundary layer methods (continuous approximation)

Provide seminal citations establishing classical SMC's global finite-time convergence under bounded uncertainties.
