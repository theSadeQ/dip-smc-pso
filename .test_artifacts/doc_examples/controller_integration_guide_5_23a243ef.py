# Example from: docs\factory\controller_integration_guide.md
# Index: 5
# Runnable: True
# Hash: 23a243ef

def integrate_hybrid_smc(
    surface_gains: List[float],
    plant_config: Any,
    classical_gains: Optional[List[float]] = None,
    adaptive_gains: Optional[List[float]] = None,
    hybrid_mode: str = 'CLASSICAL_ADAPTIVE'
) -> Dict[str, Any]:
    """
    Complete integration pattern for Hybrid Adaptive-STA SMC.

    Parameters:
    - surface_gains: [k1, k2, λ1, λ2] - 4 element array (common sliding surface)
    - classical_gains: 6-element array for classical sub-controller
    - adaptive_gains: 5-element array for adaptive sub-controller
    - hybrid_mode: Switching strategy between controllers
    """

    # 1. Surface gains validation
    if len(surface_gains) != 4:
        raise ValueError("Hybrid SMC requires exactly 4 surface gains")

    if any(g <= 0 for g in surface_gains):
        raise ValueError("All surface gains must be positive")

    # 2. Sub-controller configuration
    if classical_gains is None:
        classical_gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]

    if adaptive_gains is None:
        adaptive_gains = [25.0, 18.0, 15.0, 12.0, 3.5]

    # 3. Create sub-configurations
    classical_config = ClassicalSMCConfig(
        gains=classical_gains,
        max_force=150.0,
        dt=0.001,
        boundary_layer=0.02
    )

    adaptive_config = AdaptiveSMCConfig(
        gains=adaptive_gains,
        max_force=150.0,
        dt=0.001,
        leak_rate=0.01,
        adapt_rate_limit=10.0,
        K_min=0.1,
        K_max=100.0,
        K_init=10.0,
        alpha=0.5
    )

    # 4. Hybrid mode configuration
    from src.controllers.smc.algorithms.hybrid.config import HybridMode
    mode_enum = HybridMode(hybrid_mode)

    # 5. Main configuration
    config = {
        'gains': surface_gains,
        'hybrid_mode': mode_enum,
        'dt': 0.001,
        'max_force': 150.0,
        'classical_config': classical_config,
        'adaptive_config': adaptive_config,
        'k1_init': 5.0,
        'k2_init': 3.0,
        'gamma1': 0.5,
        'gamma2': 0.3,
        'dynamics_model': create_dynamics_model(plant_config)
    }

    # 6. Controller creation
    controller = create_controller('hybrid_adaptive_sta_smc', config)

    return {
        'controller': controller,
        'config': config,
        'classical_config': classical_config,
        'adaptive_config': adaptive_config,
        'hybrid_mode': mode_enum,
        'integration_status': 'success'
    }

# Example usage:
result = integrate_hybrid_smc(
    surface_gains=[15.0, 12.0, 10.0, 8.0],
    plant_config=complex_dip_config,
    classical_gains=[22.0, 16.0, 14.0, 10.0, 40.0, 6.0],
    adaptive_gains=[28.0, 20.0, 18.0, 14.0, 4.0],
    hybrid_mode='CLASSICAL_ADAPTIVE'
)