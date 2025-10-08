# Example from: docs\factory\controller_integration_guide.md
# Index: 4
# Runnable: False
# Hash: 1467a19c

def integrate_super_twisting_smc(
    gains: List[float],
    plant_config: Any,
    sta_params: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Complete integration pattern for Super-Twisting SMC.

    Parameters:
    - gains: [K1, K2, k1, k2, λ1, λ2] - 6 element array
    - STA: K1, K2 are super-twisting algorithm gains
    - Convergence: Finite-time convergence properties
    """

    # 1. Parameter validation
    if len(gains) != 6:
        raise ValueError("Super-Twisting SMC requires exactly 6 gains")

    if any(g <= 0 for g in gains):
        raise ValueError("All Super-Twisting SMC gains must be positive")

    # STA-specific validation
    K1, K2 = gains[0], gains[1]
    if K1 <= K2:
        logger.warning(f"STA recommendation: K1={K1} should be > K2={K2}")

    # 2. STA-specific parameters
    default_sta_params = {
        'power_exponent': 0.5,      # α = 0.5 for STA
        'regularization': 1e-6,     # Numerical stability
        'boundary_layer': 0.01,     # Built-in chattering reduction
        'switch_method': 'tanh',    # Smooth switching function
        'damping_gain': 0.0         # Additional damping if needed
    }

    if sta_params:
        default_sta_params.update(sta_params)

    # 3. Configuration construction
    config = {
        'gains': gains,
        'max_force': 150.0,
        'dt': 0.001,
        **default_sta_params,
        'dynamics_model': create_dynamics_model(plant_config)
    }

    # 4. Controller creation
    controller = create_controller('sta_smc', config)

    return {
        'controller': controller,
        'config': config,
        'sta_params': default_sta_params,
        'K1_K2_ratio': K1 / K2,
        'integration_status': 'success'
    }

# Example usage:
result = integrate_super_twisting_smc(
    gains=[35.0, 20.0, 25.0, 18.0, 12.0, 8.0],
    plant_config=full_nonlinear_config,
    sta_params={
        'power_exponent': 0.6,  # Slightly different convergence rate
        'switch_method': 'sigmoid', # Alternative switching function
        'damping_gain': 1.0     # Additional damping for robustness
    }
)