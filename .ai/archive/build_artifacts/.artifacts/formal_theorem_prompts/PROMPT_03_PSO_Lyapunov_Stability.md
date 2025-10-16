# Citation Request: PSO-Optimized Gains Maintain Lyapunov Stability

I need academic citations for the following theorem on Lyapunov stability preservation under PSO optimization.

## THEOREM STATEMENT

"The PSO-optimized gains maintain Lyapunov stability for the closed-loop double inverted pendulum (DIP) system."

## TECHNICAL CONTEXT

**Domain:** Lyapunov stability theory applied to PSO-tuned controllers

**Mathematical Framework:**

**Lyapunov Stability Definition:**
- Equilibrium point x = 0 is Lyapunov stable if for all ε > 0, there exists δ > 0 such that ||x(0)|| < δ implies ||x(t)|| < ε for all t ≥ 0
- Asymptotic stability: Additionally requires x(t) → 0 as t → ∞
- Global stability: Property holds for all initial conditions

**Closed-Loop System:**
- Plant: Double inverted pendulum nonlinear dynamics ẋ = f(x, u)
- Controller: u = g(x, K) where K are the controller gains
- Closed-loop: ẋ = f(x, g(x, K))

**PSO Optimization:**
- Search space: Controller gain vector K ∈ ℝⁿ
- Fitness function: J(K) combines performance (tracking error, settling time) and stability margin
- Constraint: Optimized gains K* must satisfy stability conditions

**Critical Distinction from PROMPT_02:**
- PROMPT_02 focuses on "ensures global asymptotic stability" (stronger claim)
- This theorem focuses on "maintains Lyapunov stability" (preservation of an existing property)
- Implies PSO optimization doesn't destabilize an already stable design

## REQUIRED CITATIONS

Find 2-3 papers that:

1. **Formalize Lyapunov stability** constraints or objectives in PSO optimization
2. **Prove preservation** of stability properties when gains are optimized via metaheuristics
3. **Apply to closed-loop systems** with PSO-tuned feedback gains and Lyapunov stability verification

**Specifically seek:**
- Papers using Lyapunov functions as constraints in PSO fitness
- Stability-guaranteed PSO variants (e.g., constrained PSO)
- Closed-loop stability analysis for metaheuristic-tuned controllers

## OUTPUT FORMAT

For each citation:

1. **Full Citation:** Authors, "Title," Venue, Year
2. **DOI/URL:** Direct link
3. **Relevance:** How does this support maintaining Lyapunov stability under PSO tuning?
4. **Mathematical Result:** Specific theorem/lemma/constraint formulation that guarantees stability maintenance

## FOCUS AREAS

Key topics:
- Constrained optimization with stability guarantees
- Lyapunov stability as PSO objective/constraint
- Closed-loop system stability under parameter tuning
- Robust stability margins in optimized control

**Authors to consider:**
- Kennedy/Eberhart (PSO founders)
- Researchers combining PSO with Lyapunov theory
- Control theorists using metaheuristics with stability proofs

Provide citations establishing that PSO can maintain Lyapunov stability properties of closed-loop systems.
