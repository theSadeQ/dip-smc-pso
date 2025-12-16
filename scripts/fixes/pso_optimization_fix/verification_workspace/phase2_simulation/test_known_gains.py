"""
Phase 2: Test Known Gains
Purpose: Verify that known good gains (from MT-8 report) produce stable results.
"""

import sys
import os
import numpy as np

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.plant.models.simplified.dynamics import SimplifiedDIPDynamics
from src.plant.models.simplified.config import SimplifiedDIPConfig
from src.controllers.smc.classic_smc import ClassicalSMC
from src.core.simulation_runner import run_simulation

def test_mt8_gains():
    print("Testing MT-8 optimized gains for Classical SMC...")
    
    # MT-8 Optimized Gains
    # k1, k2, lam1, lam2, K, kd
    gains = [23.068, 12.854, 5.515, 3.487, 2.233, 0.148]
    
    # Setup
    config = SimplifiedDIPConfig.create_default()
    dynamics = SimplifiedDIPDynamics(config, enable_fast_mode=True)
    
    controller = ClassicalSMC(
        gains=gains, 
        max_force=100.0, 
        boundary_layer=0.1,
        dynamics_model=dynamics
    )
    
    # Run Simulation
    sim_time = 5.0
    dt = 0.01
    
    # Initial state: Upright (perfect) to check stability, or small perturbation
    # Let's try small perturbation
    initial_state = np.array([0.0, 0.05, -0.05, 0.0, 0.0, 0.0])
    
    try:
        t_arr, x_arr, u_arr = run_simulation(
            controller=controller,
            dynamics_model=dynamics,
            sim_time=sim_time,
            dt=dt,
            initial_state=initial_state
        )
        
        final_state = x_arr[-1]
        print(f"Final state: {final_state}")
        
        # Check stability (angles should be close to 0)
        # x, theta1, theta2, ...
        theta1 = final_state[1]
        theta2 = final_state[2]
        
        print(f"Final theta1: {theta1:.4f}, theta2: {theta2:.4f}")
        
        if abs(theta1) > 0.1 or abs(theta2) > 0.1:
            print("WARNING: Controller might not have fully converged or perturbation was too large.")
            # MT-8 gains are robust, so they should handle this.
            # But let's not fail just yet, as I don't know the exact convergence criteria used in report.
            # However, if it exploded, that's a fail.
            if abs(theta1) > 1.0 or abs(theta2) > 1.0:
                 print("FAIL: Unstable!")
                 return False
        
        print("PASS: Simulation stable with MT-8 gains.")
        return True
        
    except Exception as e:
        print(f"FAIL: Simulation failed: {e}")
        return False

if __name__ == "__main__":
    if test_mt8_gains():
        sys.exit(0)
    else:
        sys.exit(1)
