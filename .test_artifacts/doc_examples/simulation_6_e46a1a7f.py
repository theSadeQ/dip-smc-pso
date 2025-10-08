# Example from: docs\guides\api\simulation.md
# Index: 6
# Runnable: True
# Hash: e46a1a7f

def progress_callback(t, state, control):
    """Called at each timestep."""
    print(f"t={t:.2f}s, θ₁={state[2]:.3f} rad, u={control:.2f} N")

result = runner.run(controller, callback=progress_callback)