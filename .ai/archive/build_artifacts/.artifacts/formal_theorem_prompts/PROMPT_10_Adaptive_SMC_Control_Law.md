# Citation Request: Adaptive Sliding Mode Control Law Properties

I need academic citations for the properties and convergence theorem of adaptive sliding mode control.

## THEOREM STATEMENT

"The adaptive control law ensures [specific stability and adaptation properties]."

## TECHNICAL CONTEXT

**Domain:** Adaptive Sliding Mode Control for systems with unknown or time-varying uncertainties

**Motivation:**

Classical SMC requires knowing uncertainty bound ρ to set switching gain η > ρ.

**Problem:** What if ρ is:
- Unknown
- Time-varying
- Conservative estimates lead to excessive control effort/chattering

**Solution:** Adaptive SMC adjusts gain online based on sliding variable magnitude.

**Adaptive SMC Structure:**

**Classical SMC:**
```
u = u_eq - η·sgn(s)         (η constant, requires η > ρ)
```

**Adaptive SMC:**
```
u = u_eq - η(t)·sgn(s)      (η(t) adapts online)
η̇(t) = γ·|s|               (adaptation law)
```

Or with decay term:
```
η̇(t) = γ·|s| - σ·η(t)      (γ > 0, σ ≥ 0)
```

Where:
- η(t): time-varying switching gain
- γ: adaptation rate (positive constant)
- σ: decay rate (prevents η growing unbounded)
- |s|: sliding variable magnitude

**Adaptive Law Rationale:**

When |s| is large (far from surface):
- η̇ > 0: gain increases to accelerate reaching
- Provides stronger control authority

When |s| is small (near surface):
- η̇ ≈ 0: gain stabilizes
- Reduces chattering compared to conservative fixed gain

**Properties to Establish:**

1. **Stability:** System remains stable despite adaptive gain
2. **Convergence:** s(t) → 0 as t → ∞ (or finite-time)
3. **Bounded adaptation:** η(t) remains bounded (doesn't grow to ∞)
4. **Robustness:** Works for uncertainties within some class
5. **Chattering reduction:** Lower average gain than conservative fixed-gain SMC

## THEOREM SIGNIFICANCE

Adaptive SMC provides:
- **Automatic tuning:** No need to know ρ precisely
- **Reduced conservatism:** Gain adjusts to actual disturbance level
- **Better performance:** Lower chattering + same robustness

## REQUIRED CITATIONS

Find 2-3 papers that:

1. **Establish stability and convergence** of adaptive sliding mode control laws
2. **Prove boundedness** of adaptive gain η(t)
3. **Provide adaptation law designs** with mathematical analysis (Lyapunov or similar)

**Relevant works:**
- **Slotine & Li (1987, 1991)** - Adaptive sliding surface control
- **Sanner & Slotine (1992)** - Gaussian networks for direct adaptive control
- **Plestan et al. (2010)** - New methodologies for adaptive sliding mode control
- **Shtessel et al. (2014)** - Sliding Mode Control and Observation, Chapter 6

## OUTPUT FORMAT

For each citation:

1. **Full Citation:** Authors, "Title," Journal/Conference, Year, Pages
2. **DOI/URL:** Link
3. **Relevance:** What properties (stability, convergence, boundedness) are proven?
4. **Key Result:** Adaptation law formula and convergence theorem statement

## FOCUS AREAS

Essential topics:
- Adaptive gain adjustment in SMC
- Lyapunov-based adaptation laws
- Boundedness proofs for adaptive parameters
- Convergence analysis with time-varying gains
- Chattering reduction via adaptation

**Distinguish from:**
- Fixed-gain SMC (classical approach)
- Observer-based adaptive control (different architecture)
- Parameter estimation methods (focus here is on gain adaptation)

Provide rigorous citations establishing theoretical properties of adaptive sliding mode control laws.
