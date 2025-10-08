# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 12
# Runnable: True
# Hash: 7c6d31a0

# Reduced overshoot configuration (verified solution)
reduced_overshoot_config = SuperTwistingSMCConfig(
    gains=[8.0, 4.0, 12.0, 6.0, 4.85, 3.43],  # Optimized λ₁, λ₂
    max_force=150.0,
    K1=8.0,    # Algorithmic gain (maintained)
    K2=4.0,    # Reduced from 8.0 for damping
    power_exponent=0.5,
    dt=0.001
)