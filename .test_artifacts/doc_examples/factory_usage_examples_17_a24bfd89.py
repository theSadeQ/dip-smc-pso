# Example from: docs\technical\factory_usage_examples.md
# Index: 17
# Runnable: True
# Hash: a24bfd89

from src.controllers.factory import create_controller, get_default_gains

# Efficient batch creation with different gain sets
controller_specs = [
    ('classical_smc', [8.0, 6.0, 4.0, 3.0, 15.0, 2.0]),
    ('sta_smc', [8.0, 4.0, 12.0, 6.0, 4.85, 3.43]),
    ('adaptive_smc', [12.0, 10.0, 6.0, 5.0, 2.5]),
    ('hybrid_adaptive_sta_smc', [8.0, 6.0, 4.0, 3.0])
]

controllers = {}
for controller_type, gains in controller_specs:
    controllers[controller_type] = create_controller(controller_type, gains=gains)

print(f"Created {len(controllers)} different controller types")