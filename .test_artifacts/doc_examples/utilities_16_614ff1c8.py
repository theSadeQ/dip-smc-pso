# Example from: docs\guides\api\utilities.md
# Index: 16
# Runnable: True
# Hash: 614ff1c8

from src.utils.analysis import (
    compute_ise, compute_itae, compute_overshoot,
    compute_settling_time, compute_control_effort
)

# Individual metrics
ise = compute_ise(t, state[:, 2:4])  # ISE for θ₁, θ₂
itae = compute_itae(t, state[:, 2:4])
overshoot = compute_overshoot(state[:, 2])  # First pendulum
settling = compute_settling_time(t, state[:, 2], threshold=0.02)
energy = compute_control_effort(t, control)