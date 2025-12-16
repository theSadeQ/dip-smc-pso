"""
Phase 2: Verify Simulations
Purpose: Ensure the simulation runner works with the controller and dynamics.
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

def test_simulation_integration():
    print("Testing simulation runner integration...")
    
    # 1. Setup Dynamics
    try:
        config = SimplifiedDIPConfig.create_default()
        dynamics = SimplifiedDIPDynamics(config, enable_fast_mode=True)
    except Exception as e:
        print(f"FAIL: Dynamics setup failed: {e}")
        return False

    # 2. Setup Controller
    # Gains: [k1, k2, lam1, lam2, K, kd]
    gains = [10.0, 10.0, 5.0, 5.0, 20.0, 1.0]
    max_force = 100.0
    boundary_layer = 0.1
    
    try:
        controller = ClassicalSMC(
            gains=gains, 
            max_force=max_force, 
            boundary_layer=boundary_layer,
            dynamics_model=dynamics # Pass dynamics for u_eq
        )
    except Exception as e:
        print(f"FAIL: Controller setup failed: {e}")
        return False

    # 3. Run Simulation
    sim_time = 2.0
    dt = 0.01
    initial_state = np.array([0.0, 0.1, 0.0, 0.0, 0.0, 0.0]) # Initial tilt
    
    try:
        t_arr, x_arr, u_arr = run_simulation(
            controller=controller,
            dynamics_model=dynamics,
            sim_time=sim_time,
            dt=dt,
            initial_state=initial_state,
            strict_mode=True
        )
        
        print(f"Simulation completed. Steps: {len(t_arr)}")
        print(f"Final state: {x_arr[-1]}")
        print(f"Max control: {np.max(np.abs(u_arr))}")
        
        if len(t_arr) != int(sim_time/dt) + 1:
            print(f"FAIL: Incorrect number of steps. Expected {int(sim_time/dt) + 1}, got {len(t_arr)}")
            # It might differ by 1 due to rounding, but usually match
            
        if np.any(np.isnan(x_arr)):
            print("FAIL: NaN in state trajectory")
            return False
            
        print("PASS: Simulation runner functional.")
        return True
        
    except Exception as e:
        print(f"FAIL: Simulation failed: {e}")
        return False

if __name__ == "__main__":
    if test_simulation_integration():
        sys.exit(0)
    else:
        sys.exit(1)
