# Example from: docs\factory_integration_documentation.md
# Index: 34
# Runnable: False
# Hash: 9097ef99

# ❌ Imports all controllers at module level
from src.controllers.factory import (
    create_controller,
    create_classical_smc_controller,
    create_sta_smc_controller,
    # ... all functions
)

# ✅ Import only what you need
from src.controllers.factory import create_controller

# ✅ Or use lazy imports
def get_factory_function():
    from src.controllers.factory import create_pso_controller_factory
    return create_pso_controller_factory