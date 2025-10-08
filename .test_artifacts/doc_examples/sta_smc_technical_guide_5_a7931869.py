# Example from: docs\controllers\sta_smc_technical_guide.md
# Index: 5
# Runnable: True
# Hash: a7931869

# Compute unsaturated and saturated control
u_raw = u_eq + u_cont + z - d·σ
u_sat = clip(u_raw, -max_force, max_force)

# Anti-windup adjustment
new_z = z - K₂·sgn_sigma·dt + Kaw·(u_sat - u_raw)·dt
                              ^^^^^^^^^^^^^^^^^^^^^^^^
                              Windup compensation