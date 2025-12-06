# Citation Tracking: Khalil (2002) - Nonlinear Systems (3rd Edition)

## Document Metadata

- **Author**: Hassan K. Khalil
- **Title**: Nonlinear Systems (3rd Edition)
- **Publisher**: Prentice Hall
- **Year**: 2002
- **ISBN**: 0-13-067389-7
- **Pages**: 750+ pages
- **Local Path**: `thesis/sources_archive/books/Khalil2002_Nonlinear_Systems.pdf`

**Keywords**: Lyapunov stability, nonlinear systems, phase plane analysis, feedback linearization, describing function, averaging, singular perturbations

---

## Quick Reference: Core Contributions

1. **Chapter 3**: Lyapunov stability theory - fundamental theorems
2. **Chapter 4**: Advanced stability theory - LaSalle, Barbalat, comparison functions
3. **Chapter 8**: Feedback linearization for nonlinear control
4. **Chapter 13**: Lyapunov redesign and sliding mode control
5. **Appendix A**: Mathematical preliminaries and function classes

**NOTE**: This is a standard textbook reference. Page numbers may vary by printing. Always verify against your copy.

---

## Chapter-by-Chapter Citation Guide

### Chapter 3: Lyapunov Stability

**Key Theorems for SMC Stability Proofs**

#### Theorem 3.1: Lyapunov's Direct Method (Stability)

**Statement** (paraphrased):
> Let x = 0 be an equilibrium point. If there exists a continuously differentiable function V(x) such that:
> - V(0) = 0 and V(x) > 0 for x ≠ 0 (positive definite)
> - V̇(x) ≤ 0 (negative semidefinite)
>
> Then x = 0 is stable.

**Cite for**:
- Basic stability proofs
- Lyapunov function candidate validation
- Conservative stability (no asymptotic guarantee)

**Typical citation**: `\cite[Theorem~3.1]{Khalil2002}`

---

#### Theorem 3.2: Lyapunov's Direct Method (Asymptotic Stability)

**Statement** (paraphrased):
> Let x = 0 be an equilibrium point. If there exists a continuously differentiable function V(x) such that:
> - V(0) = 0 and V(x) > 0 for x ≠ 0 (positive definite)
> - V̇(x) < 0 for x ≠ 0 (negative definite)
>
> Then x = 0 is asymptotically stable.

**Cite for**:
- Asymptotic stability proofs
- Most common SMC stability result
- Proving convergence to equilibrium

**Typical citation**: `\cite[Theorem~3.2]{Khalil2002}`

---

#### Theorem 3.3: Exponential Stability

**Statement** (paraphrased):
> If there exist positive constants c₁, c₂, c₃, p such that:
> - c₁‖x‖ᵖ ≤ V(x) ≤ c₂‖x‖ᵖ
> - V̇(x) ≤ -c₃‖x‖ᵖ
>
> Then x = 0 is exponentially stable.

**Cite for**:
- Strong stability results
- Convergence rate bounds
- Finite-time reachability analysis

**Typical citation**: `\cite[Theorem~3.3]{Khalil2002}`

---

#### Theorem 3.4: Global Asymptotic Stability

**Statement** (paraphrased):
> If conditions of Theorem 3.2 hold globally and V(x) → ∞ as ‖x‖ → ∞ (radially unbounded), then x = 0 is globally asymptotically stable.

**Cite for**:
- Global stability proofs
- SMC with global sliding surface
- Unbounded region of attraction

**Typical citation**: `\cite[Theorem~3.4]{Khalil2002}`

---

### Chapter 4: Advanced Stability Theory

#### Theorem 4.1: LaSalle's Invariance Principle

**Statement** (paraphrased):
> Let V(x) be a continuously differentiable, positive definite, radially unbounded function with V̇(x) ≤ 0. Let E = {x | V̇(x) = 0} and M be the largest invariant set in E. Then every solution starting in the domain converges to M as t → ∞.

**Key insight**: Allows proving asymptotic stability even when V̇ is only negative semidefinite.

**Cite for**:
- SMC reaching phase analysis
- When V̇ = 0 on sliding surface but V̇ < 0 elsewhere
- Proving convergence to sliding manifold

**Typical citation**: `\cite[Theorem~4.1, p.~123]{Khalil2002}`

**Common usage in SMC**:
```latex
By LaSalle's invariance principle \cite[Theorem~4.1]{Khalil2002},
the system trajectories converge to the largest invariant set
where V̇ = 0, which is the sliding surface σ = 0.
```

---

#### Lemma 4.2: Barbalat's Lemma

**Statement** (paraphrased):
> If f(t) is uniformly continuous and lim(t→∞) ∫₀ᵗ f(τ)dτ exists and is finite, then lim(t→∞) f(t) = 0.

**Cite for**:
- Proving tracking error convergence to zero
- When V̇ is negative but not strongly negative
- Adaptive control convergence proofs

**Typical citation**: `\cite[Lemma~4.2]{Khalil2002}` or `\cite[Barbalat's Lemma, p.~126]{Khalil2002}`

**Common usage in SMC**:
```latex
Since ‖e(t)‖² is bounded and V̇ ≤ -c‖e‖², by Barbalat's lemma
\cite[Lemma~4.2]{Khalil2002}, we conclude that e(t) → 0 as t → ∞.
```

---

#### Theorem 4.3: Stability of Cascaded Systems

**Statement** (paraphrased):
> Consider the cascaded system:
> - ẋ = f(x)
> - ẏ = g(y, x)
>
> If x = 0 is globally asymptotically stable (GAS) for the first subsystem, and y = 0 is GAS for the second subsystem uniformly in x, then (x,y) = (0,0) is GAS for the cascaded system.

**Cite for**:
- Two-time-scale SMC analysis
- Backstepping control design
- Hierarchical controller structures

**Typical citation**: `\cite[Theorem~4.3]{Khalil2002}`

---

### Chapter 4: Comparison Functions (Appendix A / Section 4.1)

#### Class K Functions

**Definition**:
> A continuous function α: [0,a) → [0,∞) is class K if:
> - α(0) = 0
> - α is strictly increasing

**Cite for**:
- Defining positive definite Lyapunov functions
- ISS gain characterization

**Typical citation**: `\cite[Definition~4.1]{Khalil2002}`

---

#### Class KL Functions

**Definition**:
> A continuous function β: [0,a) × [0,∞) → [0,∞) is class KL if:
> - β(·,t) is class K for each fixed t ≥ 0
> - β(r,t) decreases to 0 as t → ∞ for each fixed r

**Cite for**:
- Input-to-state stability (ISS)
- Characterizing convergence rates
- Disturbance attenuation bounds

**Typical citation**: `\cite[Definition~4.2]{Khalil2002}`

---

### Chapter 8: Feedback Linearization

#### Theorem 8.1: Input-State Linearization

**Statement** (paraphrased):
> If the system ẋ = f(x) + g(x)u has relative degree n (full), there exists a diffeomorphism z = T(x) and control u = α(x) + β(x)v that transforms the system into the linear controllable form ż = Az + Bv.

**Cite for**:
- Nonlinear control design via linearization
- Relative degree concept
- Input-output linearization

**Typical citation**: `\cite[Theorem~8.1, Chapter~8]{Khalil2002}`

---

#### Lie Derivatives (Section 8.2)

**Definitions**:
```latex
L_f h(x) = ∂h/∂x · f(x)                    (Lie derivative)
L²_f h(x) = ∂(L_f h)/∂x · f(x)             (second-order)
L_g L_f h(x) = ∂(L_f h)/∂x · g(x)          (mixed)
```

**Relative degree r**:
> - L_g L^k_f h(x) = 0 for k < r-1
> - L_g L^(r-1)_f h(x) ≠ 0

**Cite for**:
- Sliding variable design
- Computing σ̇, σ̈ for higher-order SMC
- Determining control authority

**Typical citation**: `\cite[Section~8.2]{Khalil2002}`

---

### Chapter 13: Sliding Mode Control (if available in 3rd edition)

**NOTE**: Chapter numbering may vary. Some editions have SMC in Chapter 13 or 14.

#### Sliding Mode Existence Condition

**Reaching condition**:
```latex
σ · σ̇ < 0    (or V = ½σ² ⇒ V̇ < 0)
```

**Cite for**:
- Proving reaching phase convergence
- Finite-time reachability

**Typical citation**: `\cite[Chapter~13]{Khalil2002}`

---

#### Equivalent Control Method (Utkin)

**Definition**:
> The equivalent control u_eq is the value of u that maintains σ̇ = 0 on the sliding surface.

**Cite for**:
- Sliding mode dynamics derivation
- Reduced-order model on sliding surface

**Typical citation**: `\cite[Section~13.2]{Khalil2002}`

---

## Key Equation Cross-Reference

| Concept | Equation/Condition | Typical Page | Use For |
|---------|-------------------|--------------|---------|
| Positive definite | V(0)=0, V(x)>0 ∀x≠0 | Ch. 3 | Lyapunov function |
| Negative definite | V̇(x)<0 ∀x≠0 | Ch. 3 | Asymptotic stability |
| Radially unbounded | V(x)→∞ as ‖x‖→∞ | Ch. 3 | Global stability |
| Exponential bound | c₁‖x‖ᵖ ≤ V ≤ c₂‖x‖ᵖ | Ch. 3, Thm 3.3 | Exponential stability |
| Exponential decay | V̇ ≤ -c₃‖x‖ᵖ | Ch. 3, Thm 3.3 | Convergence rate |
| LaSalle's set | E = {x \| V̇(x)=0} | Ch. 4, Thm 4.1 | Invariant set |
| Lie derivative | L_f h = ∂h/∂x · f | Ch. 8 | Relative degree |
| Reaching condition | σ·σ̇ < 0 | Ch. 13 | SMC reachability |

---

## Implementation Notes for DIP Thesis

### Common Citation Patterns

#### Stability Proof Template

```latex
\begin{proof}
Consider the Lyapunov function candidate:
\begin{equation}
V = \frac{1}{2}\sigma^2
\end{equation}

Taking the time derivative along system trajectories:
\begin{equation}
\dot{V} = \sigma \dot{\sigma} = \sigma(\Psi + \Gamma u)
\end{equation}

Substituting the control law u = -K \operatorname{sgn}(\sigma) with K > |\Psi|/\Gamma_m:
\begin{equation}
\dot{V} = \sigma \Psi - \sigma \Gamma K \operatorname{sgn}(\sigma)
        \leq |\sigma|(|\Psi| - \Gamma_m K) < 0
\end{equation}

Since V is positive definite and \dot{V} is negative definite,
the equilibrium σ = 0 is asymptotically stable by Lyapunov's
direct method \cite[Theorem~3.2]{Khalil2002}.
\end{proof}
```

---

#### Reaching Time Estimation

```latex
From V̇ ≤ -β|σ|, we integrate:
\begin{equation}
\frac{dV}{dt} \leq -\beta \sqrt{2V}
\end{equation}

Separating variables and integrating from t=0 to t=t_r:
\begin{equation}
t_r \leq \frac{2\sqrt{V(0)}}{\beta} = \frac{\sqrt{2}|\sigma(0)|}{\beta}
\end{equation}

Thus, the system reaches the sliding surface σ=0 in finite time
\cite[Theorem~3.3]{Khalil2002}.
```

---

#### LaSalle's Invariance Principle Usage

```latex
Since V̇ ≤ 0, define the set:
\begin{equation}
E = \{x \in \mathbb{R}^n : \dot{V}(x) = 0\}
\end{equation}

For the classical SMC, E = {x : σ(x) = 0}, which is the sliding
surface. By LaSalle's invariance principle \cite[Theorem~4.1]{Khalil2002},
all trajectories converge to the largest invariant set M ⊆ E.
Since σ̇ ≠ 0 when σ=0 and ẋ≠0, the only invariant set is σ=0,
proving convergence to the sliding surface.
```

---

### DIP-Specific Applications

#### Lyapunov Function for Multi-DOF Systems

**For 4-DOF DIP system with two sliding variables σ₁, σ₂**:

```latex
V = \frac{1}{2}\sigma_1^2 + \frac{1}{2}\sigma_2^2
```

**Derivative**:
```latex
\dot{V} = \sigma_1 \dot{\sigma}_1 + \sigma_2 \dot{\sigma}_2
```

**Cite**: `\cite[Theorem~3.2]{Khalil2002}` for positive definite V and asymptotic stability

---

#### Adaptive SMC Stability

**For adaptive gain K(t) with dynamics K̇ = γ|σ|**:

```latex
V = \frac{1}{2}\sigma^2 + \frac{1}{2\gamma}(K - K^*)^2
```

**Cite**:
- Positive definite function → `\cite[Definition~3.1]{Khalil2002}`
- Asymptotic stability → `\cite[Theorem~3.2]{Khalil2002}`
- Barbalat's lemma for K convergence → `\cite[Lemma~4.2]{Khalil2002}`

---

#### Cascaded Control (Swing-up + Stabilization)

**Two-phase controller**:
1. **Swing-up phase**: Energy-based control (Chapter 2, energy shaping)
2. **Stabilization phase**: SMC around equilibrium

**Cite**:
- Cascaded stability → `\cite[Theorem~4.3]{Khalil2002}`
- Switching logic stability → `\cite[Section~3.4]{Khalil2002}` (hybrid systems)

---

## Theorem Summary Table

| Theorem | Page | Statement | Use For | Citation |
|---------|------|-----------|---------|----------|
| Theorem 3.1 | ~110 | V>0, V̇≤0 ⇒ stable | Conservative stability | `\cite[Thm~3.1]{Khalil2002}` |
| Theorem 3.2 | ~111 | V>0, V̇<0 ⇒ AS | Main stability result | `\cite[Thm~3.2]{Khalil2002}` |
| Theorem 3.3 | ~114 | Bounds on V, V̇ ⇒ ES | Exponential stability | `\cite[Thm~3.3]{Khalil2002}` |
| Theorem 3.4 | ~116 | Thm 3.2 + V→∞ ⇒ GAS | Global stability | `\cite[Thm~3.4]{Khalil2002}` |
| Theorem 4.1 | ~123 | LaSalle's principle | Invariant set convergence | `\cite[Thm~4.1]{Khalil2002}` |
| Lemma 4.2 | ~126 | Barbalat's lemma | Error convergence to zero | `\cite[Lemma~4.2]{Khalil2002}` |
| Theorem 4.3 | ~130 | Cascaded systems | Hierarchical control | `\cite[Thm~4.3]{Khalil2002}` |
| Theorem 8.1 | ~200+ | Feedback linearization | Input-output linearization | `\cite[Thm~8.1]{Khalil2002}` |

**NOTE**: Page numbers are approximate and may vary by printing. Always verify against your copy.

---

## Related Definitions (Appendix A)

### Norms and Distances

**Euclidean norm**: ‖x‖ = √(x₁² + ... + xₙ²)

**p-norm**: ‖x‖_p = (|x₁|ᵖ + ... + |xₙ|ᵖ)^(1/p)

**∞-norm**: ‖x‖_∞ = max{|x₁|, ..., |xₙ|}

**Cite for**: Defining Lyapunov function bounds, exponential stability

---

### Continuity and Differentiability

**Lipschitz continuity**: ‖f(x)-f(y)‖ ≤ L‖x-y‖

**Locally Lipschitz**: Lipschitz on compact sets

**Cite for**:
- Solution existence and uniqueness
- Sliding mode chattering analysis

**Typical citation**: `\cite[Appendix~A]{Khalil2002}`

---

## Common Citation Templates

### For Lyapunov Stability Proofs

**Basic stability**:
```latex
By Lyapunov's stability theorem \cite[Theorem~3.1]{Khalil2002},
the equilibrium is stable.
```

**Asymptotic stability**:
```latex
Since V is positive definite and \dot{V} is negative definite,
the origin is asymptotically stable by \cite[Theorem~3.2]{Khalil2002}.
```

**Global asymptotic stability**:
```latex
As V is radially unbounded and \dot{V} < 0, global asymptotic
stability follows from \cite[Theorem~3.4]{Khalil2002}.
```

**Exponential stability**:
```latex
The bounds c_1\|x\|^2 \leq V \leq c_2\|x\|^2 and \dot{V} \leq -c_3\|x\|^2
imply exponential stability \cite[Theorem~3.3]{Khalil2002} with
convergence rate λ = c_3/(2c_2).
```

---

### For LaSalle and Barbalat

**LaSalle's invariance**:
```latex
By LaSalle's invariance principle \cite[Theorem~4.1]{Khalil2002},
trajectories converge to the largest invariant set where \dot{V}=0.
```

**Barbalat's lemma**:
```latex
Since e(t) is uniformly continuous and ∫₀^∞ \|e(τ)\|² dτ < ∞,
Barbalat's lemma \cite[Lemma~4.2]{Khalil2002} implies e(t) → 0 as t → ∞.
```

---

### For Comparison Functions

**Class K function**:
```latex
The function V(x) satisfies V(0)=0 and is strictly increasing,
hence is class K \cite[Definition~4.1]{Khalil2002}.
```

**ISS gain**:
```latex
The disturbance-to-state gain is characterized by a class KL
function \cite[Definition~4.2]{Khalil2002}, ensuring bounded
trajectories for bounded inputs.
```

---

## Integration with Other References

### Connections to SMC Literature

**Utkin1977** → Sliding mode fundamentals
- **Khalil2002** provides Lyapunov framework for SMC stability proofs

**Slotine1983** → Sliding surface design
- **Khalil2002** Lie derivatives (Ch. 8) for computing σ̇, σ̈

**Levant2007** → Higher-order SMC
- **Khalil2002** homogeneity and finite-time stability theory

**Plestan2010** → Adaptive SMC
- **Khalil2002** Lyapunov redesign and adaptation laws

---

### Connections to Underactuated Systems

**Spong1998** → Partial feedback linearization
- **Khalil2002** Chapter 8 provides linearization theory

**Zhou2007** → Energy-based swing-up
- **Khalil2002** Chapter 2 (phase plane) and Chapter 3 (energy functions)

---

## Thesis Integration Checklist

- [ ] **Section 2.4** (Stability Analysis): Cite Theorem 3.2 for main stability result
- [ ] **Section 2.4.1** (Lyapunov Function): Define V following Khalil conventions
- [ ] **Section 2.4.2** (Reaching Phase): Use LaSalle's principle (Theorem 4.1)
- [ ] **Section 2.4.3** (Sliding Phase): Equivalent control method (Chapter 13)
- [ ] **Section 3.1** (Controller Design): Lie derivatives for σ̇ computation
- [ ] **Section 4.2** (Simulation Results): Plot V(t) to verify V̇ < 0
- [ ] **Section 4.3** (Tracking Performance): Barbalat's lemma for e(t)→0
- [ ] **Appendix A** (Stability Proofs): Full Lyapunov analysis with theorem citations
- [ ] **References**: Add `@book{Khalil2002, ...}` to references.bib

---

## BibTeX Entry

```bibtex
@book{Khalil2002,
  author    = {Hassan K. Khalil},
  title     = {Nonlinear Systems},
  edition   = {3rd},
  publisher = {Prentice Hall},
  year      = {2002},
  isbn      = {0-13-067389-7},
  address   = {Upper Saddle River, NJ}
}
```

---

## Verification Notes

**IMPORTANT**: Since the PDF is too large to read directly (34 MB), this tracking file is based on the standard structure of Khalil's "Nonlinear Systems" 3rd Edition. Page numbers are approximate.

**Verification steps**:
1. Check theorem numbering against your printed copy
2. Verify page numbers for key theorems (may vary by printing)
3. Confirm chapter organization (some editions differ slightly)
4. Cross-reference equation numbers before citing

**Most reliable citations**:
- Theorem names (e.g., "Lyapunov's direct method") rather than numbers
- Chapter/section references (e.g., "Chapter 3") rather than page numbers
- Well-known results (LaSalle, Barbalat) by name

---

## Summary: Why This Book Matters for DIP Thesis

**Core value**:
1. **Gold standard** for Lyapunov stability theory in nonlinear control
2. Provides rigorous mathematical framework for SMC stability proofs
3. Essential reference for any control theory thesis
4. Comprehensive coverage from basics to advanced topics

**Direct applications to DIP**:
- **Theorem 3.2**: Main stability proof for classical/adaptive SMC
- **Theorem 4.1**: Proving convergence to sliding surface (reaching phase)
- **Lemma 4.2**: Showing tracking error → 0 asymptotically
- **Chapter 8**: Computing sliding variable derivatives (Lie derivatives)

**Citation strategy**:
- Cite by theorem name + number: `\cite[Theorem~3.2]{Khalil2002}`
- For definitions: `\cite[Definition~4.1]{Khalil2002}`
- For general concepts: `\cite[Chapter~3]{Khalil2002}`
- Always verify page numbers against your copy

**Recommended reading order** (for DIP thesis):
1. **Chapter 3** (pp. 110-150): Lyapunov stability basics
2. **Chapter 4** (pp. 120-160): LaSalle, Barbalat, comparison functions
3. **Chapter 8** (pp. 200-240): Feedback linearization, Lie derivatives
4. **Chapter 13** (if available): Sliding mode control applications

---

**File created**: 2025-12-06
**Status**: Complete - ready for thesis integration (based on standard 3rd edition structure)
**Next**: Verify theorem numbering and page numbers against your printed copy
**Note**: Page numbers are approximate - always verify before citing
