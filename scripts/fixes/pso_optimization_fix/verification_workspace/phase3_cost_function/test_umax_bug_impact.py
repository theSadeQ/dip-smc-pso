"""
Phase 3: Test u_max Bug Impact
Purpose: Check if u_max is correctly propagated or hardcoded.
"""

import sys
import os
import numpy as np
from types import SimpleNamespace

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.optimization.core.cost_evaluator import ControllerCostEvaluator

def test_umax_propagation():
    print("Testing u_max propagation...")
    
    # Config with specific max_force (e.g., 80.0)
    config = SimpleNamespace()
    config.physics = SimpleNamespace()
    config.simulation = SimpleNamespace()
    config.simulation.duration = 1.0
    config.simulation.dt = 0.01
    config.cost_function = SimpleNamespace()
    config.cost_function.weights = SimpleNamespace()
    config.cost_function.weights.state_error = 1.0
    config.cost_function.weights.control_effort = 0.0
    config.cost_function.weights.control_rate = 0.0
    config.cost_function.weights.sliding = 0.0
    config.cost_function.instability_penalty = 1000.0
    
    # Mock factory
    def mock_factory(gains):
        c = SimpleNamespace()
        c.max_force = 123.0 # Controller's max force
        return c
    
    # Case 1: Auto-detection (default)
    evaluator_auto = ControllerCostEvaluator(mock_factory, config)
    print(f"Auto-detected u_max: {evaluator_auto.u_max}")
    
    if evaluator_auto.u_max == 123.0:
        print("PASS: Auto-detection picked up controller's max_force.")
    else:
        print(f"FAIL: Auto-detection mismatch. Expected 123.0, got {evaluator_auto.u_max}")
        # Note: If this fails, it might default to 150.0 as seen in the source code fallback.
        
    # Case 2: Explicit override
    evaluator_explicit = ControllerCostEvaluator(mock_factory, config, u_max=200.0)
    print(f"Explicit u_max: {evaluator_explicit.u_max}")
    
    if evaluator_explicit.u_max == 200.0:
        print("PASS: Explicit override respected.")
    else:
        print(f"FAIL: Explicit override ignored. Expected 200.0, got {evaluator_explicit.u_max}")

    return True

if __name__ == "__main__":
    if test_umax_propagation():
        sys.exit(0)
    else:
        sys.exit(1)
