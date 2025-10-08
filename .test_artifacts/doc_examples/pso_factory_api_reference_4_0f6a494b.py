# Example from: docs\factory\pso_factory_api_reference.md
# Index: 4
# Runnable: False
# Hash: 0f6a494b

# example-metadata:
# runnable: false

def create_smc_for_pso(smc_type: SMCType,
                      gains: List[float],
                      max_force: float = 100.0,
                      dt: float = 0.01,
                      **kwargs) -> PSOControllerWrapper:
    """
    Primary function for creating SMC controllers in PSO fitness functions.

    This function provides the optimal interface for PSO optimization workflows:
    - Single-line controller creation
    - Automatic mathematical constraint validation
    - Performance-optimized wrapper for simplified control interface
    - Comprehensive error handling for robust PSO evaluation

    Mathematical Foundation:
    Each controller type implements specific sliding mode control laws:

    Classical SMC:
        u = -(k1·θ1 + k2·θ2) - (λ1·θ̇1 + λ2·θ̇2) - K·tanh(s/φ) - kd·ẋ
        s = λ1·e1 + λ2·e2 + ė1 + ė2

    Super-Twisting SMC:
        u̇ = -K1·sign(s) - K2·sign(ṡ)
        s = λ1·e1 + λ2·e2 + α1·ė1 + α2·ė2

    Adaptive SMC:
        u = u_eq + u_sw
        K̇ = γ|s| - σK  (online adaptation)

    Hybrid SMC:
        u = w1·u_adaptive + w2·u_sta  (mode switching)

    Args:
        smc_type: Controller type from SMCType enumeration
        gains: Gain array matching controller requirements:
            - Classical: [k1, k2, λ1, λ2, K, kd] (6 parameters)
            - STA: [K1, K2, λ1, λ2, α1, α2] (6 parameters)
            - Adaptive: [k1, k2, λ1, λ2, γ] (5 parameters)
            - Hybrid: [k1, k2, λ1, λ2] (4 parameters)
        max_force: Control force saturation limit [N]
        dt: Control timestep [s]
        **kwargs: Additional controller-specific parameters

    Returns:
        PSOControllerWrapper with simplified control interface

    Raises:
        ValueError: If gains violate mathematical constraints
        TypeError: If smc_type is not a valid SMCType
        ConfigurationError: If controller configuration is invalid

    Performance:
        - Creation time: <1ms typical
        - Memory overhead: <500B per wrapper
        - Thread-safe: Yes (for read operations)

    PSO Integration Example: