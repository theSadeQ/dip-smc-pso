# Example from: docs\api\factory_system_api_reference.md
# Index: 49
# Runnable: True
# Hash: b991beff

# Factory detects invalid default gains and auto-corrects
controller = create_controller('sta_smc')  # Uses defaults

# If defaults violate K1 > K2, factory automatically uses:
# [25.0, 15.0, 20.0, 12.0, 8.0, 6.0]  # K1=25 > K2=15 ✓