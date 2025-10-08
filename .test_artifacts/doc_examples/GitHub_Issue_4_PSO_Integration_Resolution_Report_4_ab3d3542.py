# Example from: docs\GitHub_Issue_4_PSO_Integration_Resolution_Report.md
# Index: 4
# Runnable: False
# Hash: ab3d3542

def create_smc_for_pso(
    smc_type: Union[SMCType, str],
    gains: Union[List[float], np.ndarray],
    plant_config_or_max_force: Union[Any, float] = 100.0,
    dt: float = 0.01,
    dynamics_model: Optional[Any] = None
) -> PSOControllerWrapper:
    """
    Convenience function optimized for PSO parameter tuning.

    Usage in PSO fitness function:
        controller = create_smc_for_pso(SMCType.CLASSICAL, pso_params)
        performance = evaluate_controller(controller, test_scenarios)
        return performance
    """
    # Handle different calling patterns
    if isinstance(plant_config_or_max_force, (int, float)):
        max_force = float(plant_config_or_max_force)
        final_dynamics_model = dynamics_model
    else:
        max_force = 100.0
        final_dynamics_model = plant_config_or_max_force

    controller = SMCFactory.create_from_gains(
        smc_type=smc_type,
        gains=gains,
        max_force=max_force,
        dt=dt,
        dynamics_model=final_dynamics_model
    )

    return PSOControllerWrapper(controller)

def get_gain_bounds_for_pso(smc_type: Union[SMCType, str]) -> Tuple[List[float], List[float]]:
    """Get PSO optimization bounds for SMC controller gains."""
    spec = SMCFactory.get_gain_specification(smc_type)
    bounds = spec.gain_bounds

    # Convert to PSO format: (lower_bounds, upper_bounds)
    lower_bounds = [bound[0] for bound in bounds]
    upper_bounds = [bound[1] for bound in bounds]

    return (lower_bounds, upper_bounds)

def validate_smc_gains(smc_type: Union[SMCType, str], gains: Union[List[float], np.ndarray]) -> bool:
    """Validate gains for SMC controller type with stability requirements."""
    try:
        spec = SMCFactory.get_gain_specification(smc_type)
        gains_array = np.asarray(gains)

        # Check length
        if len(gains_array) < spec.n_gains:
            return False

        # Check positivity for surface gains (SMC stability requirement)
        if smc_type in [SMCType.CLASSICAL, SMCType.ADAPTIVE, SMCType.SUPER_TWISTING]:
            if any(g <= 0 for g in gains_array[:4]):  # First 4 are surface gains
                return False
        elif smc_type == SMCType.HYBRID:
            if any(g <= 0 for g in gains_array[:4]):  # All 4 gains must be positive
                return False

        return True
    except Exception:
        return False