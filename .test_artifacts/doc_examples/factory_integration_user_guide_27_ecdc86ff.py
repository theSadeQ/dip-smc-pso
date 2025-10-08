# Example from: docs\factory\factory_integration_user_guide.md
# Index: 27
# Runnable: True
# Hash: ecdc86ff

# Legacy function names still work
from src.controllers.factory import (
    create_classical_smc_controller,  # Backward compatibility
    create_controller  # Preferred new interface
)

# Both work identically
legacy_controller = create_classical_smc_controller(
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
)

modern_controller = create_controller(
    'classical_smc',
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
)