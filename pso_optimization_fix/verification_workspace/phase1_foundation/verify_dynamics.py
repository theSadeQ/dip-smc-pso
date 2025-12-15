"""
Phase 1: Verify Dynamics
Purpose: Ensure the underlying dynamics model works as expected before testing controllers.
"""

import sys
import os
import numpy as np

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.plant.models.simplified.dynamics import SimplifiedDIPDynamics
from src.plant.models.simplified.config import SimplifiedDIPConfig

def test_dynamics_sanity():
    print("Testing dynamics model sanity...")
    
    # Initialize parameters
    try:
        config = SimplifiedDIPConfig.create_default()
        dynamics = SimplifiedDIPDynamics(config, enable_fast_mode=True)
        print("Dynamics initialized successfully (Fast Mode).")
    except Exception as e:
        print(f"FAIL: Dynamics instantiation failed: {e}")
        return False
    
    # Test state: [x, theta1, theta2, x_dot, theta1_dot, theta2_dot]
    # Small perturbation from vertical
    state = np.array([0.0, 0.1, -0.1, 0.0, 0.0, 0.0])
    u = np.array([0.0]) # No control
    dt = 0.01
    
    # 1. Test Step Computation
    try:
        next_state = dynamics.step(state, u, dt)
        print(f"Next state computed: {next_state}")
        
        if np.any(np.isnan(next_state)):
            print("FAIL: NaN values in next state")
            return False
            
        if next_state.shape != (6,):
            print(f"FAIL: Incorrect shape {next_state.shape}, expected (6,)")
            return False
            
    except Exception as e:
        print(f"FAIL: Step computation raised exception: {e}")
        return False

    # 2. Test Integration Loop
    print("\nTesting integration loop...")
    steps = 100
    
    current_state = state.copy()
    for i in range(steps):
        try:
            current_state = dynamics.step(current_state, u, dt)
        except Exception as e:
            print(f"FAIL: Integration failed at step {i}: {e}")
            return False
            
    print(f"State after {steps} steps: {current_state}")
    
    if np.any(np.isnan(current_state)):
        print("FAIL: NaN values in simulation")
        return False
        
    if np.any(np.isinf(current_state)):
        print("FAIL: Infinite values in simulation")
        return False
        
    print("PASS: Dynamics verification successful.")
    return True

if __name__ == "__main__":
    if test_dynamics_sanity():
        sys.exit(0)
    else:
        sys.exit(1)
