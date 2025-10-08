# Example from: docs\pso_integration_technical_specification.md
# Index: 6
# Runnable: False
# Hash: 9587ec0a

# example-metadata:
# runnable: false

def compute_fitness_cost(t: np.ndarray, x: np.ndarray, u: np.ndarray, sigma: np.ndarray) -> float:
    """
    Multi-objective fitness function for PSO optimization.

    Mathematical Formulation:
    J = w₁∫₀ᵀ||e(t)||²dt + w₂∫₀ᵀu²(t)dt + w₃∫₀ᵀ(du/dt)²dt + w₄∫₀ᵀσ²(t)dt + P

    Where:
    - e(t) = x(t) - x_ref: state error vector
    - u(t): control effort
    - du/dt: control rate (chattering penalty)
    - σ(t): sliding variable magnitude
    - P: instability penalty for early termination

    Cost Function Components:
    1. State Error (ISE): ∫₀ᵀ||e(t)||²dt
    2. Control Effort: ∫₀ᵀu²(t)dt
    3. Control Rate: ∫₀ᵀ(du/dt)²dt
    4. Sliding Variable Energy: ∫₀ᵀσ²(t)dt
    5. Stability Penalty: Graded penalty for premature failure
    """
    dt = np.diff(t)
    dt_matrix = dt[None, :]  # Shape (1, N-1)

    # State error integration (all state components)
    state_error_sq = np.sum(x[:, :-1, :]**2 * dt_matrix[:, :, None], axis=(1, 2))

    # Control effort integration
    control_effort_sq = np.sum(u**2 * dt_matrix, axis=1)

    # Control rate penalty (anti-chattering)
    du = np.diff(u, axis=1, prepend=u[:, 0:1])
    control_rate_sq = np.sum(du**2 * dt_matrix, axis=1)

    # Sliding variable energy
    sliding_energy = np.sum(sigma**2 * dt_matrix, axis=1)

    # Instability detection and penalty
    instability_mask = detect_instability(x, u, sigma)
    stability_penalty = compute_graded_penalty(instability_mask, t)

    # Weighted cost aggregation
    total_cost = (
        weights.state_error * normalize(state_error_sq, norms.ise) +
        weights.control_effort * normalize(control_effort_sq, norms.control) +
        weights.control_rate * normalize(control_rate_sq, norms.rate) +
        weights.stability * normalize(sliding_energy, norms.sliding) +
        stability_penalty
    )

    return total_cost