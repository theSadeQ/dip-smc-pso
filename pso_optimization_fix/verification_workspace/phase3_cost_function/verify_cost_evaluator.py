"""
Phase 3: Verify Cost Evaluator
Purpose: Ensure the cost function is computed correctly and default weights are respected.
"""

import sys
import os
import numpy as np
from types import SimpleNamespace

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.optimization.core.cost_evaluator import ControllerCostEvaluator
from src.controllers.factory import create_controller # To get default controller for factory

def create_mock_config():
    """Create a mock configuration object mirroring the real one."""
    config = SimpleNamespace()
    
    # Physics
    config.physics = SimpleNamespace()
    
    # Simulation
    config.simulation = SimpleNamespace()
    config.simulation.duration = 5.0
    config.simulation.dt = 0.01
    
    # Cost Function
    config.cost_function = SimpleNamespace()
    config.cost_function.weights = SimpleNamespace()
    config.cost_function.weights.state_error = 50.0
    config.cost_function.weights.control_effort = 0.2
    config.cost_function.weights.control_rate = 0.1
    config.cost_function.weights.sliding = 0.1
    
    config.cost_function.normalisation = SimpleNamespace()
    config.cost_function.normalisation.state_error = 1.0
    config.cost_function.normalisation.control_effort = 1.0
    config.cost_function.normalisation.control_rate = 1.0
    config.cost_function.normalisation.sliding = 1.0
    
    config.cost_function.instability_penalty = 1000.0
    config.cost_function.min_cost_floor = 1e-6
    
    config.global_seed = 42
    
    return config

def mock_controller_factory(gains):
    """Mock controller factory that returns an object with max_force."""
    controller = SimpleNamespace()
    controller.max_force = 150.0
    return controller

def test_cost_calculation():
    print("Testing cost calculation logic...")
    
    config = create_mock_config()
    evaluator = ControllerCostEvaluator(mock_controller_factory, config)
    
    # Create dummy trajectory data
    # B=1 (batch size), N=100 (steps)
    B = 1
    N = 100
    t = np.linspace(0, 1.0, N+1)
    dt = 0.01
    
    # State: [x, theta1, theta2, x_dot, theta1_dot, theta2_dot]
    # Let's make a constant error state
    x_b = np.zeros((B, N+1, 6))
    x_b[:, :, 0] = 0.1 # Constant cart position error of 0.1
    
    # Control: Constant control of 1.0
    u_b = np.ones((B, N+1))
    
    # Sliding variable: Constant 0.0
    sigma_b = np.zeros((B, N+1))
    
    # Expected Cost Calculation:
    # 1. ISE: sum(x^2 * dt) * 50.0
    #    x^2 = 0.01 (only cart pos error)
    #    sum(0.01 * 0.01) over 100 steps = 0.01 * 0.01 * 100 = 0.01
    #    Weighted ISE = 0.01 * 50.0 = 0.5
    
    # 2. Control Effort: sum(u^2 * dt) * 0.2
    #    u^2 = 1.0
    #    sum(1.0 * 0.01) over 100 steps = 1.0 * 0.01 * 100 = 1.0
    #    Weighted Effort = 1.0 * 0.2 = 0.2
    
    # 3. Control Rate: sum(du^2 * dt) * 0.1
    #    du = 0 (constant control)
    #    Weighted Rate = 0.0
    
    # 4. Sliding Energy: 0.0
    
    # Total Expected Cost = 0.5 + 0.2 = 0.7
    
    print("Computing cost for constant error trajectory...")
    computed_cost = evaluator._compute_cost_from_traj(t, x_b, u_b, sigma_b)
    print(f"Computed Cost: {computed_cost[0]}")
    print(f"Expected Cost: ~0.7")
    
    if abs(computed_cost[0] - 0.7) < 1e-4:
        print("PASS: Cost calculation matches expected logic.")
        return True
    else:
        print(f"FAIL: Cost calculation mismatch. Diff: {abs(computed_cost[0] - 0.7)}")
        return False

def test_instability_penalty():
    print("\nTesting instability penalty...")
    config = create_mock_config()
    evaluator = ControllerCostEvaluator(mock_controller_factory, config)
    
    B = 1
    N = 100
    t = np.linspace(0, 1.0, N+1)
    
    # Unstable trajectory: Angle exceeds pi/2 at step 50
    x_b = np.zeros((B, N+1, 6))
    x_b[:, 50:, 1] = 2.0 # > pi/2
    
    u_b = np.zeros((B, N+1))
    sigma_b = np.zeros((B, N+1))
    
    computed_cost = evaluator._compute_cost_from_traj(t, x_b, u_b, sigma_b)
    print(f"Computed Cost (Unstable): {computed_cost[0]}")
    
    # It should be significantly larger than 0.7, likely > 1000
    if computed_cost[0] > 1000.0:
        print("PASS: Instability penalty applied.")
        return True
    else:
        print(f"FAIL: Instability penalty not applied correctly. Cost: {computed_cost[0]}")
        return False

if __name__ == "__main__":
    p1 = test_cost_calculation()
    p2 = test_instability_penalty()
    
    if p1 and p2:
        sys.exit(0)
    else:
        sys.exit(1)
