# Example from: docs\controllers\factory_system_guide.md
# Index: 10
# Runnable: True
# Hash: d77b8b09

from src.controllers.factory.smc_factory import (
    SMCFactory,                  # Core factory class
    SMCType,                     # Controller type enum
    SMCConfig,                   # Configuration dataclass
    create_smc_for_pso,          # PSO-optimized creation
    get_gain_bounds_for_pso,     # PSO bounds
    validate_smc_gains,          # Gain validation
)