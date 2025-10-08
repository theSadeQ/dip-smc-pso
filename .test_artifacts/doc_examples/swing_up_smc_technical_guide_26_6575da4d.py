# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 26
# Runnable: True
# Hash: 6575da4d

from src.optimization.algorithms.pso_optimizer import PSOTuner

def swing_up_factory_for_pso(stabilizer_gains):
    """
    Factory for PSO: tunes stabilizer, not swing-up.

    Args:
        stabilizer_gains: Gains for ClassicalSMC [k1, k2, λ1, λ2, K, kd]
    """
    stabilizer = ClassicalSMC(
        gains=stabilizer_gains,
        max_force=20.0,
        boundary_layer=0.01,
        dynamics_model=dynamics
    )

    return SwingUpSMC(
        dynamics_model=dynamics,
        stabilizing_controller=stabilizer,
        energy_gain=50.0  # Fixed
    )

# PSO bounds for ClassicalSMC stabilizer
bounds = [
    (0.1, 50.0),  # k1
    (0.1, 50.0),  # k2
    (0.1, 50.0),  # λ1
    (0.1, 50.0),  # λ2
    (1.0, 200.0), # K
    (0.0, 50.0)   # kd
]

tuner = PSOTuner(
    controller_factory=swing_up_factory_for_pso,
    config=config,
    bounds=bounds
)

result = tuner.optimise()
optimal_stabilizer_gains = result['best_pos']