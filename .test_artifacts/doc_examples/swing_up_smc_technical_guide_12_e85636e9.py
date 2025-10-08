# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 12
# Runnable: True
# Hash: e85636e9

# Compute current energy
try:
    E_current = float(self.dyn.total_energy(state))
except Exception:
    E_current = 0.0  # Fallback for dummy dynamics

# Energy relative to bottom (down-down)
E_about_bottom = self.E_bottom - E_current

# Telemetry: normalized energy ratio
history["E_ratio"] = float(E_about_bottom / self.E_bottom)