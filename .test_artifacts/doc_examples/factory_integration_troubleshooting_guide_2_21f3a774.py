# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 2
# Runnable: True
# Hash: 21f3a774

from src.controllers.factory import list_available_controllers

# Check what's actually available
available = list_available_controllers()
print(f"Available controllers: {available}")

# Use correct names
controller = create_controller('classical_smc')  # ✅ Correct
# controller = create_controller('classical')    # ❌ Incorrect