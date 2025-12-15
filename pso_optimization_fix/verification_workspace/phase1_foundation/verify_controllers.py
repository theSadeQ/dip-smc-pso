"""
Phase 1: Verify Controllers
Purpose: Ensure both Classical and Adaptive SMC controllers can be instantiated and produce valid outputs.
"""

import sys
import os
import numpy as np

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.controllers.smc.classic_smc import ClassicalSMC
from src.controllers.smc.adaptive_smc import AdaptiveSMC
from src.core.dynamics import DIPDynamics

def test_classical_smc():
    print("Testing Classical SMC...")
    
    # Gains: [k1, k2, lam1, lam2, K, kd]
    gains = [10.0, 10.0, 5.0, 5.0, 20.0, 1.0]
    max_force = 100.0
    boundary_layer = 0.1
    
    try:
        controller = ClassicalSMC(gains, max_force, boundary_layer)
        print("ClassicalSMC instantiated successfully.")
    except Exception as e:
        print(f"FAIL: ClassicalSMC instantiation failed: {e}")
        return False
        
    # Test control computation
    # State: [x, theta1, theta2, x_dot, theta1_dot, theta2_dot]
    state = np.array([0.0, 0.1, -0.1, 0.0, 0.1, -0.1])
    state_vars = controller.initialize_state()
    history = controller.initialize_history()
    
    try:
        output = controller.compute_control(state, state_vars, history)
        print(f"Control output: {output.u}")
        
        if np.isnan(output.u):
            print("FAIL: Control output is NaN")
            return False
            
        if abs(output.u) > max_force + 1e-6:
             print(f"FAIL: Control output {output.u} exceeds max force {max_force}")
             return False
             
        print("PASS: ClassicalSMC functional.")
        return True
        
    except Exception as e:
        print(f"FAIL: ClassicalSMC compute_control failed: {e}")
        return False

def test_adaptive_smc():
    print("\nTesting Adaptive SMC...")
    
    # Gains: [k1, k2, lam1, lam2, gamma]
    gains = [10.0, 10.0, 5.0, 5.0, 1.0]
    dt = 0.01
    max_force = 100.0
    leak_rate = 0.1
    adapt_rate_limit = 10.0
    K_min = 5.0
    K_max = 50.0
    smooth_switch = True
    boundary_layer = 0.1
    dead_zone = 0.01
    
    try:
        controller = AdaptiveSMC(
            gains=gains,
            dt=dt,
            max_force=max_force,
            leak_rate=leak_rate,
            adapt_rate_limit=adapt_rate_limit,
            K_min=K_min,
            K_max=K_max,
            smooth_switch=smooth_switch,
            boundary_layer=boundary_layer,
            dead_zone=dead_zone
        )
        print("AdaptiveSMC instantiated successfully.")
    except Exception as e:
        print(f"FAIL: AdaptiveSMC instantiation failed: {e}")
        return False
        
    # Test control computation
    state = np.array([0.0, 0.1, -0.1, 0.0, 0.1, -0.1])
    state_vars = controller.initialize_state()
    history = controller.initialize_history()
    
    try:
        # First step
        output1 = controller.compute_control(state, state_vars, history)
        print(f"Step 1 Output: u={output1.u}, K={output1.state[0]}")
        
        # Check if K updated (it should if outside deadzone)
        # Sigma approx: k1*dtheta1 + k2*dtheta2 + ... = 10*0.1 + 10*-0.1 ...
        # Actually let's just check it doesn't crash and returns valid values
        
        if np.isnan(output1.u):
            print("FAIL: Control output is NaN")
            return False

        # Second step (pass updated state)
        output2 = controller.compute_control(state, output1.state, history)
        print(f"Step 2 Output: u={output2.u}, K={output2.state[0]}")
        
        print("PASS: AdaptiveSMC functional.")
        return True
        
    except Exception as e:
        print(f"FAIL: AdaptiveSMC compute_control failed: {e}")
        return False

if __name__ == "__main__":
    c_pass = test_classical_smc()
    a_pass = test_adaptive_smc()
    
    if c_pass and a_pass:
        sys.exit(0)
    else:
        sys.exit(1)
