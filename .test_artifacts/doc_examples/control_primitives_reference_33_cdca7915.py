# Example from: docs\controllers\control_primitives_reference.md
# Index: 33
# Runnable: True
# Hash: cdca7915

def __init__(self, gains, max_force, dt):
    # Validate immediately - fail fast
    self.gains = [require_positive(g, f"gains[{i}]") for i, g in enumerate(gains)]
    self.max_force = require_positive(max_force, "max_force")
    self.dt = require_positive(dt, "dt")