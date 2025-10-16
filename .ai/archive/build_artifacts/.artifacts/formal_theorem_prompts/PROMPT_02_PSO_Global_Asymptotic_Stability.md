# Citation Request: PSO-Optimized Gains for Global Asymptotic Stability

I need academic citations for the following theorem connecting PSO optimization to control system stability.

## THEOREM STATEMENT

"The PSO-optimized gains ensure global asymptotic stability of the double inverted pendulum (DIP) system."

## TECHNICAL CONTEXT

**Domain:** Particle Swarm Optimization (PSO) for controller gain tuning in underactuated mechanical systems

**System Description:**
- Double Inverted Pendulum (DIP): Two-link underactuated system with cart, highly nonlinear dynamics
- Controller gains: Parameters for sliding mode control (SMC) or PID controllers
- PSO optimization: Metaheuristic algorithm that searches gain space to minimize control objectives

**Mathematical Foundation:**
- Global asymptotic stability: System state converges to equilibrium from any initial condition as t → ∞
- Lyapunov stability theory: Existence of Lyapunov function V(x) with V̇(x) < 0 guarantees stability
- Optimization objective: PSO minimizes fitness function (e.g., settling time, overshoot, energy) while maintaining stability

**Key Claim:**
The theorem asserts that PSO-found gains don't just optimize performance metrics, but also guarantee theoretical stability properties. This connects metaheuristic optimization to rigorous stability theory.

## REQUIRED CITATIONS

Find 2-3 academic papers that:

1. **Demonstrate PSO for controller tuning** with proven stability guarantees (not just simulation results)
2. **Establish mathematical connection** between PSO-optimized parameters and Lyapunov stability
3. **Apply PSO to underactuated systems** (inverted pendulum, cart-pole, crane, acrobot) with stability analysis

**Prefer papers that:**
- Explicitly prove stability (not just show simulation convergence)
- Use Lyapunov methods to validate PSO-tuned controllers
- Address nonlinear/underactuated systems like inverted pendulums

## OUTPUT FORMAT

For each citation provide:

1. **Full Citation:** Authors, "Title," Venue, Year, Pages
2. **DOI or URL:** Direct link
3. **Relevance:** Explain how this paper connects PSO optimization to stability guarantees
4. **Key Theorem/Result:** Specific stability proof or theorem that validates PSO-tuned gains

## FOCUS AREAS

Seminal works in:
- PSO for PID/SMC/nonlinear controller tuning
- Stability analysis of optimized control systems
- Inverted pendulum control with metaheuristic optimization
- Lyapunov-based validation of heuristic optimization results

**Avoid:** Papers that only show PSO works in simulation without stability proofs.

Provide citations that rigorously support the claim that PSO-optimized gains ensure global asymptotic stability.
