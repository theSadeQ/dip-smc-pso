"""Diagnostic: Check if classical_smc controller produces control signals."""

import numpy as np
from src.config import load_config
from src.controllers.factory import create_controller

# Load config
config = load_config("config.yaml")

# Create a classical_smc controller with default gains
gains = [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
controller = create_controller(
    'classical_smc',
    config=config.controllers.classical_smc,
    gains=gains
)

# Test with configured initial state (has error)
initial_state = np.array([0.0, 0.05, -0.03, 0.0, 0.0, 0.0])

print("=" * 80)
print("Controller Output Diagnostic")
print("=" * 80)
print(f"Controller: classical_smc")
print(f"Gains: {gains}")
print(f"Initial state (with error): {initial_state}")
print()

# Try to compute control
try:
    # Check if controller has compute_control method
    if hasattr(controller, 'compute_control'):
        print("Controller has compute_control method")

        # Try calling it
        state_vars = None
        history = None

        # Initialize if available
        if hasattr(controller, 'initialize_state'):
            state_vars = controller.initialize_state()
            print(f"Initialized state_vars: {state_vars}")

        if hasattr(controller, 'initialize_history'):
            history = controller.initialize_history()
            print(f"Initialized history: {history}")

        print()
        print("Computing control at t=0...")
        result = controller.compute_control(initial_state, state_vars, history)

        print(f"Control output: {result}")

        # Extract control value
        if hasattr(result, 'control'):
            u = result.control
        elif isinstance(result, tuple):
            u = result[0]
        else:
            u = result

        print(f"Control force u: {u}")
        print()

        if abs(u) < 1e-10:
            print("[ERROR] Control is effectively ZERO! Controller not actuating!")
        else:
            print(f"[OK] Control is non-zero: {u:.6f} N")

    else:
        print("[ERROR] Controller doesn't have compute_control method!")
        print(f"Available methods: {[m for m in dir(controller) if not m.startswith('_')]}")

except Exception as e:
    print(f"[ERROR] Exception while computing control: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)

# Now try a simple forward step to see if dynamics work
print("Testing dynamics integration...")
from src.plant.full_nonlinear_dynamics import FullNonlinearDIPDynamics

dynamics = controller.dynamics_model
print(f"Dynamics model: {type(dynamics).__name__}")

# Manually compute state derivative
x_dot = dynamics.f(0.0, initial_state, 0.0)  # Zero control
print(f"State derivative with u=0: {x_dot}")

x_dot_with_control = dynamics.f(0.0, initial_state, 10.0)  # Some control
print(f"State derivative with u=10: {x_dot_with_control}")

if np.allclose(x_dot, x_dot_with_control, atol=1e-10):
    print("[WARNING] Dynamics don't respond to control!")
else:
    print("[OK] Dynamics respond to control")
