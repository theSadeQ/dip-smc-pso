# Citation Request: PSO Global Convergence for Unimodal Functions

I need academic citations for the probabilistic global convergence theorem of PSO.

## THEOREM STATEMENT

"Under the stability condition and with decreasing inertia weight, PSO converges to the global optimum with probability 1 for unimodal functions."

## TECHNICAL CONTEXT

**Domain:** Convergence theory of Particle Swarm Optimization for optimization problems

**Mathematical Framework:**

**Unimodal Function:**
- Function f: ℝⁿ → ℝ with exactly one local minimum (which is also the global minimum)
- Convex functions are unimodal (but not all unimodal functions are convex)
- Examples: sphere function, quadratic functions

**PSO with Decreasing Inertia:**
```
ω(t) = ω_max - (ω_max - ω_min) · t/T
```
- Starts with high ω (exploration)
- Gradually decreases to low ω (exploitation)
- Common range: ω ∈ [0.4, 0.9]

**Stability Condition:**
- Refers to parameter constraints ensuring particles don't diverge
- Typically involves relationship between ω, c₁, c₂
- Example: ω < 1 and c₁ + c₂ < 4ω

**Convergence with Probability 1:**
- Almost sure convergence: P(lim_{t→∞} x* = x_global) = 1
- Stronger than convergence in expectation or probability
- Requires stochastic convergence analysis

## THEOREM INTERPRETATION

This theorem establishes that:
1. **If** PSO parameters satisfy stability conditions
2. **And** inertia weight decreases over time (exploration → exploitation)
3. **Then** for unimodal optimization problems
4. **PSO will find** the global optimum with probability 1 (almost surely)

This is a fundamental theoretical result justifying PSO's effectiveness for convex/unimodal optimization.

## REQUIRED CITATIONS

Find 2-3 papers that:

1. **Prove almost sure convergence** of PSO to global optima under specific conditions
2. **Analyze PSO on unimodal/convex functions** with convergence guarantees
3. **Establish time-varying inertia weight** as a convergence mechanism

**Mathematical rigor required:**
- Stochastic convergence proofs (martingale theory, Markov chains, probability theory)
- Explicit statement of assumptions (unimodality, stability conditions)
- Proof techniques: monotone convergence, supermartingale convergence, Lyapunov methods

## OUTPUT FORMAT

For each citation:

1. **Full Citation:** Authors, "Title," Venue, Year
2. **DOI/URL:** Link
3. **Relevance:** What convergence result is proven? For what class of functions?
4. **Key Theorem:** Theorem number/statement about global convergence with probability 1

## FOCUS AREAS

Theoretical PSO convergence papers:
- **Van den Bergh & Engelbrecht:** Cooperative behavior and convergence
- **Jiang, Luo, Yang:** Stochastic convergence analysis
- **Kadirkamanathan et al.:** Stability and convergence of PSO
- **Shi & Eberhart:** Inertia weight strategies

**Key concepts:**
- Almost sure convergence (a.s. convergence)
- Convergence for unimodal/convex functions
- Time-varying inertia weight analysis
- Stochastic optimization theory

Provide citations that rigorously prove PSO's global convergence for unimodal functions with decreasing inertia.
