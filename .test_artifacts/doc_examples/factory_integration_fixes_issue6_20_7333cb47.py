# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 20
# Runnable: True
# Hash: 7333cb47

from src.controllers.factory import get_gain_bounds_for_pso, SMCType

# Get optimized bounds for each controller type
classical_bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
adaptive_bounds = get_gain_bounds_for_pso(SMCType.ADAPTIVE)
sta_bounds = get_gain_bounds_for_pso(SMCType.SUPER_TWISTING)
hybrid_bounds = get_gain_bounds_for_pso(SMCType.HYBRID)

print("Classical SMC bounds:")
print(f"  Lower: {classical_bounds[0]}")
print(f"  Upper: {classical_bounds[1]}")

# Output:
# Classical SMC bounds:
#   Lower: [1.0, 1.0, 1.0, 1.0, 5.0, 0.1]
#   Upper: [30.0, 30.0, 20.0, 20.0, 50.0, 10.0]