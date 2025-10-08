# Example from: docs\PSO_INTEGRATION_GUIDE.md
# Index: 6
# Runnable: True
# Hash: da1aa373

# Old interface still works
from src.controllers.factory import SMCFactory, SMCConfig

config = SMCConfig(gains=gains, max_force=100.0, dt=0.01)
controller = SMCFactory.create_controller(SMCType.CLASSICAL, config)

# New PSO interface provides simplified access
controller = create_smc_for_pso(SMCType.CLASSICAL, gains, plant_config)