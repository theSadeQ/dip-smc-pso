# Example from: docs\reference\interfaces\hil_enhanced_hil.md
# Index: 1
# Runnable: True
# Hash: 0ec3cde5

from src.interfaces.hil.enhanced_hil import ParameterSweep

# Parameter sweep
sweep = ParameterSweep()

# Define parameter ranges
sweep.add_parameter("mass_cart", values=np.linspace(0.8, 1.2, 5))
sweep.add_parameter("length_1", values=np.linspace(0.3, 0.5, 5))

# Run sweep
results = sweep.run()

# Analyze sensitivity
for param, result in results.items():
    print(f"{param}: sensitivity = {result.sensitivity:.4f}")