# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 24
# Runnable: False
# Hash: 6ae06329

def create_swing_up_controller(
    stabilizer_type: str,
    stabilizer_gains: List[float],
    swing_up_params: Dict,
    config: Config
) -> SwingUpSMC:
    """
    Factory for swing-up controller with any stabilizer.
    """
    # Create stabilizer via factory
    stabilizer = create_controller(
        stabilizer_type,
        gains=stabilizer_gains,
        config=config
    )

    # Create swing-up wrapper
    return SwingUpSMC(
        dynamics_model=config.dynamics,
        stabilizing_controller=stabilizer,
        **swing_up_params
    )

# Usage
swing_up = create_swing_up_controller(
    stabilizer_type='sta_smc',
    stabilizer_gains=[25, 10, 15, 12, 20, 15],
    swing_up_params={
        'energy_gain': 50.0,
        'switch_energy_factor': 0.95,
        'max_force': 20.0
    },
    config=config
)