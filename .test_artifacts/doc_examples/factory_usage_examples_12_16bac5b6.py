# Example from: docs\technical\factory_usage_examples.md
# Index: 12
# Runnable: True
# Hash: 16bac5b6

from src.controllers.factory import create_controller
import logging

# Configure logging to see factory warnings
logging.basicConfig(level=logging.INFO)

# Factory automatically handles invalid gains
try:
    # These gains violate SMC stability requirements (negative gains)
    invalid_gains = [-1.0, 5.0, 3.0, 2.0, 10.0, 1.0]

    controller = create_controller(
        controller_type='classical_smc',
        gains=invalid_gains
    )

    # Factory will:
    # 1. Detect invalid gains
    # 2. Log warning message
    # 3. Fall back to safe default gains
    # 4. Return working controller

    print("Controller created successfully with fallback gains")

except Exception as e:
    print(f"Controller creation failed: {e}")