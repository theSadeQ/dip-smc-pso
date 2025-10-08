# Example from: docs\factory\factory_integration_user_guide.md
# Index: 23
# Runnable: True
# Hash: c3298c7f

# Check required gain count
from src.controllers.factory import CONTROLLER_REGISTRY

controller_type = 'classical_smc'
required_count = CONTROLLER_REGISTRY[controller_type]['gain_count']
print(f"{controller_type} requires {required_count} gains")

# Provide correct number of gains
gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]  # 6 gains for classical SMC