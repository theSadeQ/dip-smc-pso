"""Debug: Test if dynamics.step() works correctly."""

import numpy as np
from src.config import load_config
from src.controllers.factory import create_controller

# Load config
config = load_config("config.yaml")

# Create controller
gains = [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
controller = create_controller(
    'classical_smc',
    config=config.controllers.classical_smc,
    gains=gains
)

# Initial state with error
x0 = np.array([0.0, 0.05, -0.03, 0.0, 0.0, 0.0])
dt = 0.01
u = -15.62  # Control value from earlier test

print("=" * 80)
print("Dynamics Step Test")
print("=" * 80)
print(f"Initial state: {x0}")
print(f"Control: {u}")
print(f"Timestep: {dt}")
print()

# Get dynamics model
print("Controller attributes:", [a for a in dir(controller) if not a.startswith('_')])
print()

if hasattr(controller, 'dynamics_model'):
    dynamics = controller.dynamics_model
elif hasattr(controller, '_dynamics_ref'):
    dynamics = controller._dynamics_ref
else:
    print("[ERROR] Controller has no dynamics_model or _dynamics_ref attribute!")
    dynamics = None

if dynamics:
    print(f"Dynamics model: {type(dynamics).__name__}")
    print()

# Test step
try:
    x_next = dynamics.step(x0, u, dt)
    print(f"[OK] Step succeeded")
    print(f"Next state: {x_next}")
    print(f"Is finite: {np.all(np.isfinite(x_next))}")
    print(f"State change: {np.linalg.norm(x_next - x0):.6e}")
except Exception as e:
    print(f"[ERROR] Step failed: {e}")
    import traceback
    traceback.print_exc()
