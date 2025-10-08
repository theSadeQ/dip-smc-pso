# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 7
# Runnable: False
# Hash: dc2e959d

# example-metadata:
# runnable: false

def create_smc_for_pso(smc_type: SMCType,
                      gains: List[float],
                      max_force: float = 100.0,
                      dt: float = 0.01) -> PSOControllerWrapper:
    """
    PSO-optimized controller creation with simplified interface.

    This function provides the optimal interface for PSO fitness functions:
    - Single-line controller creation
    - Automatic parameter validation
    - Performance-optimized wrapper
    - Error handling for invalid gains

    Mathematical Foundation:
    Each controller type has specific gain requirements:
    - Classical: [k1, k2, λ1, λ2, K, kd] with λᵢ > 0, K > 0
    - STA: [K1, K2, λ1, λ2, α1, α2] with K1 > K2 > 0
    - Adaptive: [k1, k2, λ1, λ2, γ] with 0.1 ≤ γ ≤ 20.0
    - Hybrid: [k1, k2, λ1, λ2] with surface gains > 0

    PSO Integration Example: