# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 28
# Runnable: False
# Hash: c86c9cc1

# 1. Widen hysteresis band
swing_up.exit_energy_factor = 0.85  # From 0.90 (wider band)

# 2. Use stronger stabilizer
stabilizer = SuperTwistingSMC(gains=[...])  # Instead of Classical

# 3. Add energy filtering
E_filtered = 0.9 * E_prev + 0.1 * E_current  # Low-pass filter