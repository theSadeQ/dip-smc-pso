# Example from: docs\guides\api\optimization.md
# Index: 12
# Runnable: True
# Hash: b3dc80a3

from src.controllers import get_gain_bounds_for_pso

# Get recommended bounds for each controller type
bounds_classical = get_gain_bounds_for_pso(SMCType.CLASSICAL)
# Returns: [(0.1, 50), (0.1, 50), (0.1, 50), (0.1, 50), (1.0, 200), (0.0, 50)]
#           k1      k2      λ1      λ2      K          ε

bounds_adaptive = get_gain_bounds_for_pso(SMCType.ADAPTIVE)
# Returns: [(0.1, 50), (0.1, 50), (0.1, 50), (0.1, 50), (0.01, 10)]
#           k1      k2      λ1      λ2      γ (adaptation rate)

bounds_sta = get_gain_bounds_for_pso(SMCType.SUPER_TWISTING)
# Returns: [(0.1, 50), (0.1, 50), (0.1, 50), (0.1, 50), (1.0, 100), (1.0, 100)]
#           k1      k2      λ1      λ2      α          β

bounds_hybrid = get_gain_bounds_for_pso(SMCType.HYBRID)
# Returns: [(0.1, 50), (0.1, 50), (0.1, 50), (0.1, 50)]
#           k1      k2      λ1      λ2