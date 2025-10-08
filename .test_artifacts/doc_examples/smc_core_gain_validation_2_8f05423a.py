# Example from: docs\reference\controllers\smc_core_gain_validation.md
# Index: 2
# Runnable: True
# Hash: 8f05423a

from src.controllers.smc.core.gain_validation import check_control_authority

# Controller parameters
c1, c2, lambda1, lambda2, K, epsilon = gains
u_max = 100.0  # Maximum actuator force (N)

# Estimate peak equivalent control (worst case)
u_eq_max = 80.0  # From dynamics analysis

# Check if total control fits within limits
u_total_max = u_eq_max + K
margin = u_max - u_total_max

print(f"u_eq_max: {u_eq_max:.1f} N")
print(f"K:        {K:.1f} N")
print(f"u_total:  {u_total_max:.1f} N")
print(f"u_max:    {u_max:.1f} N")
print(f"Margin:   {margin:.1f} N ({100*margin/u_max:.1f}%)")

if margin < 0.1 * u_max:
    print("Warning: Insufficient control authority margin")