# Example from: docs\guides\workflows\pso-sta-smc.md
# Index: 5
# Runnable: False
# Hash: d29b0ecb

def sta_smc_cost_function(gains):
    """
    Custom cost for STA-SMC optimization.

    Objectives:
    1. Minimize ISE (performance)
    2. Minimize control effort (energy)
    3. Minimize control rate (smoothness)
    4. Ensure stability (K2 > 0.5·K1)
    """
    K1, K2, k1, k2, lambda1, lambda2 = gains

    # Stability penalty
    if K2 < 0.5 * K1:
        penalty = 1000.0  # Large penalty
    else:
        penalty = 0.0

    # Run simulation
    result = simulate_with_gains(gains)

    # Multi-objective cost
    cost = (
        1.0 * result['ise'] +           # Performance
        0.01 * result['control_effort'] + # Energy
        0.001 * result['control_rate'] +  # Smoothness
        penalty                           # Stability
    )

    return cost