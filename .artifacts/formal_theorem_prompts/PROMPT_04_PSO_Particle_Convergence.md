# Citation Request: PSO Particle Convergence Conditions

I need academic citations for the convergence theorem of individual particles in Particle Swarm Optimization.

## THEOREM STATEMENT

"The particle converges to a stable trajectory if [specific convergence conditions are met]."

## TECHNICAL CONTEXT

**Domain:** Convergence analysis of Particle Swarm Optimization algorithm

**PSO Algorithm Basics:**

**Velocity Update:**
```
v_i(t+1) = ω·v_i(t) + c₁·r₁·(p_i - x_i(t)) + c₂·r₂·(p_g - x_i(t))
```

**Position Update:**
```
x_i(t+1) = x_i(t) + v_i(t+1)
```

Where:
- x_i: position of particle i
- v_i: velocity of particle i
- p_i: personal best position
- p_g: global best position
- ω: inertia weight
- c₁, c₂: cognitive and social coefficients
- r₁, r₂: random numbers in [0,1]

**Convergence Concept:**
- Particle trajectory: sequence {x_i(t), v_i(t)} over time
- Stable trajectory: bounded motion, doesn't diverge to infinity
- Conditions typically involve relationships between ω, c₁, c₂

**What the Theorem Establishes:**
Mathematical conditions on PSO parameters (inertia weight, acceleration coefficients) that guarantee particles don't exhibit explosive divergence. This is fundamental for PSO to explore search space effectively without instability.

## REQUIRED CITATIONS

Find 2-3 seminal papers that:

1. **Derive convergence conditions** for PSO particle dynamics (mathematical analysis, not just empirical)
2. **Establish stability regions** in PSO parameter space (ω, c₁, c₂)
3. **Prove trajectory boundedness** or convergence theorems for individual particles

**Prefer papers with:**
- Rigorous mathematical analysis (differential equations, Lyapunov methods, linear systems theory)
- Explicit parameter bounds for stability (e.g., "if ω < 1 and c₁ + c₂ < 4, then...")
- Proofs of convergence or stability (not just simulation observations)

## OUTPUT FORMAT

For each citation:

1. **Full Citation:** Authors, "Title," Venue, Year
2. **DOI/URL:** Link to paper
3. **Relevance:** What convergence conditions or stability bounds does this paper establish?
4. **Key Result:** Specific theorem, equation, or parameter bounds (e.g., "ω ∈ [0.4, 0.9]")

## FOCUS AREAS

Seminal works on PSO theory:
- **Clerc & Kennedy (2002):** Constriction coefficient analysis
- **Van den Bergh (2002):** Convergence analysis Ph.D. thesis
- **Trelea (2003):** Stability and convergence analysis
- **Jiang et al. (2007):** Stochastic convergence analysis

**Mathematical approaches:**
- Order-1 and order-2 stability analysis
- Lyapunov stability of PSO dynamics
- Stochastic convergence theorems
- Linear system stability for particle motion

Provide citations that rigorously establish when PSO particles converge to stable trajectories.
