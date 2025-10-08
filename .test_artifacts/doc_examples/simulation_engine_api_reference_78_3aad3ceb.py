# Example from: docs\api\simulation_engine_api_reference.md
# Index: 78
# Runnable: True
# Hash: 3aad3ceb

from src.simulation.safety import apply_safety_guards, SafetyViolationError

try:
    apply_safety_guards(x_current, step_idx, config)
except SafetyViolationError as e:
    print(f"Safety violation at step {step_idx}: {e}")
    # Truncate simulation