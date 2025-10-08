# Example from: docs\api\factory_system_api_reference.md
# Index: 48
# Runnable: True
# Hash: 23a7a894

from src.controllers.factory import create_controller

# Invalid: K1 ≤ K2 violates super-twisting stability
gains = [15.0, 20.0, 12.0, 8.0, 6.0, 4.0]  # K1=15 ≤ K2=20 ✗
try:
    controller = create_controller('sta_smc', gains=gains)
except ValueError as e:
    print(e)
    # Output: "Super-Twisting stability requires K1 > K2 > 0"