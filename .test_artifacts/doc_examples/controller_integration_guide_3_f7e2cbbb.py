# Example from: docs\factory\controller_integration_guide.md
# Index: 3
# Runnable: False
# Hash: f7e2cbbb

def integrate_adaptive_smc(
    gains: List[float],
    plant_config: Any,
    adaptation_params: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Complete integration pattern for Adaptive SMC.

    Parameters:
    - gains: [k1, k2, λ1, λ2, γ] - 5 element array
    - Critical: γ (gamma) is adaptation rate in gains[4]
    - Adaptation: Additional parameters for online estimation
    """

    # 1. Parameter validation
    if len(gains) != 5:
        raise ValueError("Adaptive SMC requires exactly 5 gains")

    # Surface gains must be positive
    if any(g <= 0 for g in gains[:4]):
        raise ValueError("Surface gains (k1, k2, λ1, λ2) must be positive")

    # Adaptation rate validation
    gamma = gains[4]
    if gamma <= 0 or gamma > 10.0:
        raise ValueError(f"Adaptation rate γ={gamma} must be in (0, 10]")

    # 2. Adaptation parameters
    default_adaptation = {
        'leak_rate': 0.01,
        'adapt_rate_limit': 10.0,
        'K_min': 0.1,
        'K_max': 100.0,
        'K_init': 10.0,
        'alpha': 0.5,
        'dead_zone': 0.05,
        'smooth_switch': True
    }

    if adaptation_params:
        default_adaptation.update(adaptation_params)

    # 3. Configuration construction
    config = {
        'gains': gains,
        'max_force': 150.0,
        'dt': 0.001,
        'boundary_layer': 0.01,
        **default_adaptation,
        'dynamics_model': create_dynamics_model(plant_config)
    }

    # 4. Controller creation
    controller = create_controller('adaptive_smc', config)

    return {
        'controller': controller,
        'config': config,
        'adaptation_params': default_adaptation,
        'gamma_value': gamma,
        'integration_status': 'success'
    }

# Example usage:
result = integrate_adaptive_smc(
    gains=[25.0, 18.0, 15.0, 12.0, 3.5],
    plant_config=full_dip_config,
    adaptation_params={
        'leak_rate': 0.02,     # Faster parameter forgetting
        'adapt_rate_limit': 15.0, # Higher adaptation rate
        'alpha': 0.7           # Different adaptation law exponent
    }
)