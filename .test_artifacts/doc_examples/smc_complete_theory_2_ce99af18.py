# Example from: docs\mathematical_foundations\smc_complete_theory.md
# Index: 2
# Runnable: True
# Hash: ce99af18

if not np.isfinite(u):
       u = 0.0  # Emergency fallback
       log_error("Non-finite control value detected")