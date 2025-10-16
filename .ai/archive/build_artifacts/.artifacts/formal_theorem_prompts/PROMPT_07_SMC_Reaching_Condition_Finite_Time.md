# Citation Request: Finite-Time Reaching Condition in Sliding Mode Control

I need academic citations for the finite-time reaching theorem in sliding mode control.

## THEOREM STATEMENT

"Under the reaching condition, the system reaches the sliding surface in finite time bounded by [a specific function of initial conditions]."

## TECHNICAL CONTEXT

**Domain:** Sliding Mode Control reaching phase analysis

**Reaching Condition (Lyapunov Reaching Law):**

The classical reaching condition ensures convergence to sliding surface:
```
s · ṡ ≤ -η·|s|
```

Where:
- s: sliding surface value
- ṡ: time derivative of s
- η > 0: reaching law gain

**Alternative formulations:**
```
ṡ = -η·sgn(s)              (Constant rate reaching law)
ṡ = -η·sgn(s) - k·s        (Constant plus proportional)
V̇ = s·ṡ ≤ -η·|s|           (Lyapunov function approach)
```

**Finite-Time Bound Derivation:**

Starting from reaching condition:
```
d/dt(|s|) = sgn(s)·ṡ ≤ -η
```

Integrating:
```
|s(t)| ≤ |s(0)| - η·t
```

Setting |s(T)| = 0:
```
T_reach = |s(0)| / η
```

**Theorem Significance:**

Unlike asymptotic convergence (t → ∞), this theorem proves:
1. System reaches sliding surface in **finite** time
2. Reaching time is **bounded** and **computable** from initial conditions
3. Time bound depends on initial sliding variable |s(0)| and gain η

This is a fundamental result distinguishing sliding mode control from other robust control methods.

## REQUIRED CITATIONS

Find 2-3 papers/books that:

1. **Establish the reaching condition** and derive finite-time convergence proofs
2. **Provide time bounds** for reaching phase explicitly as function of initial conditions
3. **Prove finite-time stability** using Lyapunov or direct analysis methods

**Classic SMC references:**
- **Utkin (1977, 1992)** - Original sliding mode theory papers
- **Slotine & Li (1991)** - Applied Nonlinear Control, Chapter 7
- **Edwards & Spurgeon (1998)** - Sliding Mode Control: Theory and Applications
- **Shtessel et al. (2014)** - Sliding Mode Control and Observation
- **Khalil** - Nonlinear Systems (finite-time stability theorems)

## OUTPUT FORMAT

For each citation:

1. **Full Citation:** Authors, "Title," Venue, Year, Pages
2. **DOI/ISBN/URL:** Link
3. **Relevance:** Which theorem/section proves finite-time reaching?
4. **Key Result:** Explicit reaching time bound formula T_reach = f(s(0), η)

## FOCUS AREAS

Critical topics:
- Reaching condition formulations (s·ṡ ≤ -η|s|)
- Finite-time stability theory
- Reaching time bounds and estimation
- Lyapunov-based reaching law design
- Differences between asymptotic vs finite-time convergence

**Distinguish from:**
- Sliding phase (after reaching surface) - this is about reaching phase
- Asymptotic stability (t → ∞) - this is finite-time (t = T_reach)

Provide authoritative citations proving that the reaching condition guarantees finite-time convergence to sliding surface.
