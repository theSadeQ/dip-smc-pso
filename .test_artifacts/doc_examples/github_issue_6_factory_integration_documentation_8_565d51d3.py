# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 8
# Runnable: False
# Hash: 565d51d3

def get_gain_bounds_for_pso(smc_type: SMCType) -> List[Tuple[float, float]]:
    """
    Get PSO optimization bounds based on control theory.

    Bounds are derived from:
    - Stability requirements (Lyapunov conditions)
    - Performance constraints (settling time, overshoot)
    - Physical limitations (actuator saturation)
    - Practical implementation limits

    Mathematical Derivation:

    Classical SMC Bounds:
    - Surface gains λᵢ: [1.0, 50.0] based on desired bandwidth
    - Position gains kᵢ: [0.1, 50.0] for reasonable pole placement
    - Switching gain K: [1.0, 200.0] for disturbance rejection
    - Damping gain kd: [0.0, 50.0] for chattering reduction

    Super-Twisting Bounds:
    - K1: [2.0, 100.0] with constraint K1 > K2
    - K2: [1.0, 99.0] ensuring convergence condition
    - Surface gains: [1.0, 50.0] for stability

    Adaptive SMC Bounds:
    - Surface gains: [1.0, 50.0] for stability
    - Adaptation rate γ: [0.1, 20.0] for bounded adaptation

    Returns:
        List of (lower_bound, upper_bound) tuples for each gain
    """
    bounds_map = {
        SMCType.CLASSICAL: [
            (0.1, 50.0),   # k1: position gain pendulum 1
            (0.1, 50.0),   # k2: position gain pendulum 2
            (1.0, 50.0),   # λ1: surface gain pendulum 1
            (1.0, 50.0),   # λ2: surface gain pendulum 2
            (1.0, 200.0),  # K: switching gain
            (0.0, 50.0)    # kd: damping gain
        ],

        SMCType.SUPER_TWISTING: [
            (2.0, 100.0),  # K1: primary twisting gain (K1 > K2)
            (1.0, 99.0),   # K2: secondary twisting gain
            (1.0, 50.0),   # λ1: surface gain pendulum 1
            (1.0, 50.0),   # λ2: surface gain pendulum 2
            (1.0, 50.0),   # α1: higher-order surface gain 1
            (1.0, 50.0)    # α2: higher-order surface gain 2
        ],

        SMCType.ADAPTIVE: [
            (0.1, 50.0),   # k1: position gain pendulum 1
            (0.1, 50.0),   # k2: position gain pendulum 2
            (1.0, 50.0),   # λ1: surface gain pendulum 1
            (1.0, 50.0),   # λ2: surface gain pendulum 2
            (0.1, 20.0)    # γ: adaptation rate
        ],

        SMCType.HYBRID: [
            (1.0, 50.0),   # k1: surface gain pendulum 1
            (1.0, 50.0),   # k2: surface gain pendulum 2
            (1.0, 50.0),   # λ1: surface gain 1
            (1.0, 50.0)    # λ2: surface gain 2
        ]
    }

    return bounds_map[smc_type]