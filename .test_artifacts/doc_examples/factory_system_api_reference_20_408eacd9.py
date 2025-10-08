# Example from: docs\api\factory_system_api_reference.md
# Index: 20
# Runnable: True
# Hash: 408eacd9

from src.controllers.factory import get_default_gains, create_controller

# Create controllers with default and custom gains
gains_default = get_default_gains('classical_smc')
gains_custom = [30.0, 20.0, 15.0, 12.0, 45.0, 7.0]

controller_default = create_controller('classical_smc', gains=gains_default)
controller_custom = create_controller('classical_smc', gains=gains_custom)

# Compare performance
cost_default = evaluate(controller_default)
cost_custom = evaluate(controller_custom)
print(f"Default cost: {cost_default:.3f}")
print(f"Custom cost: {cost_custom:.3f}")
print(f"Improvement: {((cost_default - cost_custom) / cost_default * 100):.1f}%")