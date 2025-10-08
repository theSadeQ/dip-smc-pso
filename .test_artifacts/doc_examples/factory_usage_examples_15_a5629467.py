# Example from: docs\technical\factory_usage_examples.md
# Index: 15
# Runnable: True
# Hash: a5629467

# The factory has robust import fallbacks for dynamics models
from src.controllers.factory import create_controller

try:
    # Factory tries multiple import paths:
    # 1. src.core.dynamics.DIPDynamics (preferred)
    # 2. src.core.dynamics.DIPDynamics (alternative)
    # 3. src.plant.models.simplified.dynamics.SimplifiedDIPDynamics (fallback)

    controller = create_controller('classical_smc', gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0])
    print("Controller created successfully")

except ImportError as e:
    print(f"Import error: {e}")
    # This only happens if NO dynamics implementation is available