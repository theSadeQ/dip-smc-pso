# Example from: docs\factory\controller_integration_guide.md
# Index: 2
# Runnable: False
# Hash: db823b18

def integrate_classical_smc(
    gains: List[float],
    plant_config: Any,
    optimization_bounds: Optional[Tuple[List[float], List[float]]] = None
) -> Dict[str, Any]:
    """
    Complete integration pattern for Classical SMC.

    Parameters:
    - gains: [k1, k2, λ1, λ2, K, kd] - 6 element array
    - Stability: All gains must be positive
    - Chattering: boundary_layer parameter required
    """

    # 1. Parameter validation
    if len(gains) != 6:
        raise ValueError("Classical SMC requires exactly 6 gains")

    if any(g <= 0 for g in gains):
        raise ValueError("All Classical SMC gains must be positive")

    # 2. Configuration construction
    config = {
        'gains': gains,
        'max_force': 150.0,
        'boundary_layer': 0.02,  # Chattering reduction
        'dt': 0.001,
        'dynamics_model': create_dynamics_model(plant_config)
    }

    # 3. Controller creation
    controller = create_controller('classical_smc', config)

    # 4. Integration validation
    validate_controller_plant_compatibility(controller, plant_config)

    return {
        'controller': controller,
        'config': config,
        'gain_bounds': optimization_bounds or get_default_bounds('classical_smc'),
        'integration_status': 'success'
    }

# Example usage:
result = integrate_classical_smc(
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    plant_config=simplified_dip_config,
    optimization_bounds=(
        [5.0, 5.0, 3.0, 3.0, 10.0, 1.0],    # Lower bounds
        [50.0, 40.0, 30.0, 25.0, 80.0, 15.0] # Upper bounds
    )
)