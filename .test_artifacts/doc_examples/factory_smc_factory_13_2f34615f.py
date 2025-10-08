# Example from: docs\reference\controllers\factory_smc_factory.md
# Index: 13
# Runnable: True
# Hash: 2f34615f

from src.controllers.factory import SMCFactory, SMCType

# Get gain requirements for each controller type
for ctrl_type in SMCType:
    spec = SMCFactory.get_gain_specification(ctrl_type)
    print(f"\n{ctrl_type.value}:")
    print(f"  Number of gains: {spec.n_gains}")
    print(f"  Gain names:      {spec.gain_names}")
    print(f"  Bounds:          {spec.bounds}")