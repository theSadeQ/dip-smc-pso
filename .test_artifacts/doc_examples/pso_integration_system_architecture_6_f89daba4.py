# Example from: docs\pso_integration_system_architecture.md
# Index: 6
# Runnable: True
# Hash: f89daba4

# Controller-specific gain vector dimensions:
GAIN_DIMENSIONS = {
    'classical_smc': 6,      # [c1, λ1, c2, λ2, K, kd]
    'sta_smc': 6,            # [K1, K2, k1, k2, λ1, λ2]
    'adaptive_smc': 5,       # [c1, λ1, c2, λ2, γ]
    'hybrid_adaptive_sta_smc': 4,  # [c1, λ1, c2, λ2]
    'swing_up_smc': 6        # Uses stabilizing controller gains
}