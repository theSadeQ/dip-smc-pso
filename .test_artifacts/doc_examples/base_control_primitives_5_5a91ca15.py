# Example from: docs\reference\controllers\base_control_primitives.md
# Index: 5
# Runnable: True
# Hash: 5a91ca15

from src.controllers.base.control_primitives import (
    saturate, rate_limit, low_pass_filter, deadband
)

# Control pipeline
class ControlPipeline:
    def __init__(self, u_max, u_dot_max, tau_filter, deadband_threshold):
        self.u_max = u_max
        self.u_dot_max = u_dot_max
        self.tau = tau_filter
        self.deadband = deadband_threshold
        self.u_prev = 0.0
        self.u_filtered_prev = 0.0

    def process(self, u_raw, dt):
        # 1. Deadband (ignore small errors)
        u1 = deadband(u_raw, self.deadband)

        # 2. Rate limiting (prevent slew violations)
        u2 = rate_limit(u1, self.u_prev, self.u_dot_max, dt)

        # 3. Saturation (enforce actuator limits)
        u3 = saturate(u2, self.u_max)

        # 4. Low-pass filter (reduce high-frequency content)
        u4 = low_pass_filter(u3, self.u_filtered_prev, self.tau, dt)

        # Update history
        self.u_prev = u3  # Before filtering for rate limiting
        self.u_filtered_prev = u4

        return u4

# Usage
pipeline = ControlPipeline(
    u_max=100.0,
    u_dot_max=1000.0,
    tau_filter=0.05,
    deadband_threshold=0.5
)

u_raw = -75.0  # Raw controller output
u_final = pipeline.process(u_raw, dt=0.01)
print(f"Final control: {u_final:.2f} N")