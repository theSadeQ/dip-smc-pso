# Example from: docs\guides\api\configuration.md
# Index: 9
# Runnable: True
# Hash: 8965fae3

from src.config.schemas import (
    DIPParams, ClassicalSMCConfig, SimulationConfig, Config
)

# Create physics parameters
physics = DIPParams(
    m0=1.5, m1=0.5, m2=0.75,
    l1=0.5, l2=0.75,
    b0=0.1, b1=0.01, b2=0.01,
    g=9.81
)

# Create controller config
controller_cfg = ClassicalSMCConfig(
    gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
    max_force=100.0,
    boundary_layer=0.01
)

# Create simulation config
sim_cfg = SimulationConfig(
    duration=5.0,
    dt=0.01,
    use_full_dynamics=False
)

# Assemble complete config
full_config = Config(
    dip_params=physics,
    controllers={'classical_smc': controller_cfg},
    simulation=sim_cfg
)