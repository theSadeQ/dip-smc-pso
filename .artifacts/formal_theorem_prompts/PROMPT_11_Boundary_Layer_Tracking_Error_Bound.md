# Citation Request: Boundary Layer Method Tracking Error Bound

I need academic citations for the ultimate bound theorem of boundary layer sliding mode control.

## THEOREM STATEMENT

"With the boundary layer method, the tracking error is ultimately bounded by [specific bound related to boundary layer thickness]."

## TECHNICAL CONTEXT

**Domain:** Chattering reduction in Sliding Mode Control via boundary layer approximation

**Chattering Problem:**

Classical SMC uses discontinuous control:
```
u = u_eq - η·sgn(s)
```

The sign function sgn(s) switches infinitely fast near s = 0, causing:
- High-frequency control oscillations (chattering)
- Actuator wear
- Excitation of unmodeled high-frequency dynamics
- Practical implementation issues

**Boundary Layer Solution:**

Replace discontinuous sgn(s) with continuous approximation inside boundary layer:
```
sgn(s) → sat(s/Φ) = {  s/Φ     if |s| ≤ Φ
                     { sgn(s)  if |s| > Φ
```

Or smooth approximation:
```
sgn(s) → s/(|s| + Φ)
sgn(s) → tanh(s/Φ)
```

Where Φ > 0 is the **boundary layer thickness**.

**Modified Control Law:**
```
u = u_eq - η·sat(s/Φ)
```

**Trade-off:**

**Benefits:**
- Continuous control (no chattering)
- Smooth control effort
- Implementable on real hardware

**Cost:**
- System no longer reaches s = 0 exactly
- Instead converges to boundary layer: |s| ≤ Φ
- Tracking error no longer zero, but **ultimately bounded**

**Ultimate Bound Derivation:**

Inside boundary layer (|s| ≤ Φ):
```
u = u_eq - η·(s/Φ)       (proportional control)
```

System behaves like:
```
ṡ = -η·(s/Φ) + d(t)      (d is bounded disturbance)
```

Analysis shows s converges to region:
```
|s(∞)| ≤ Φ·|d_max|/η
```

**Tracking Error Bound:**

For sliding surface s = c·e + ė (first-order):
```
|e(∞)| ≤ K·Φ             (K depends on c, d_max, η)
```

**Key insight:** Smaller Φ → smaller tracking error, but more chattering risk

## THEOREM SIGNIFICANCE

This theorem establishes fundamental trade-off in practical SMC:
1. **Chattering elimination:** Φ > 0 makes control continuous
2. **Bounded tracking:** Error bounded by O(Φ)
3. **Design parameter:** Choose Φ balancing smoothness vs accuracy
4. **Robustness preserved:** Still robust to matched uncertainties

## REQUIRED CITATIONS

Find 2-3 papers/books that:

1. **Derive tracking error bounds** for boundary layer SMC explicitly
2. **Establish ultimate boundedness** (not just asymptotic, but bounded region)
3. **Analyze trade-offs** between Φ, chattering, and tracking accuracy

**Classic references:**
- **Slotine & Li (1991)** - Applied Nonlinear Control, Section 7.4
- **Slotine (1984)** - "Sliding controller design for non-linear systems"
- **Burton & Zinober (1986)** - Continuous approximation of variable structure control
- **Edwards & Spurgeon (1998)** - SMC Theory and Applications, Chapter 3

## OUTPUT FORMAT

For each citation:

1. **Full Citation:** Authors, "Title," Venue, Year, Pages
2. **DOI/ISBN/URL:** Link
3. **Relevance:** Which section derives tracking error bound for boundary layer method?
4. **Key Result:** Explicit bound formula relating tracking error to Φ

## FOCUS AREAS

Critical topics:
- Boundary layer approximation of sign function
- Saturation function: sat(s/Φ)
- Ultimate boundedness vs asymptotic stability
- Trade-off analysis: Φ vs tracking accuracy vs chattering
- Continuous approximations of discontinuous control

**Mathematical tools:**
- Ultimate bound theorems (Khalil, Slotine)
- Lyapunov stability for bounded disturbances
- Input-to-state stability (ISS) if applicable

**Distinguish from:**
- Higher-order sliding modes (different approach to chattering)
- Observer-based continuous SMC
- Adaptive boundary layer (time-varying Φ)

Provide authoritative citations deriving tracking error bounds for boundary layer sliding mode control.
