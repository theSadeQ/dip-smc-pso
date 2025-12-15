"""
Phase 4: Verify Optimization Claims (Deep Dive)
Purpose: Remove the 'passive controller penalty' to reveal true underlying costs.
"""

import sys
import os
import numpy as np
from types import SimpleNamespace

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.optimization.core.cost_evaluator import ControllerCostEvaluator
from src.controllers.smc.classic_smc import ClassicalSMC
from src.plant.models.simplified.config import SimplifiedDIPConfig

# Copy-paste setup from previous script
def create_real_config():
    config = SimpleNamespace()
    config.physics = SimplifiedDIPConfig.create_default()
    config.simulation = SimpleNamespace()
    config.simulation.duration = 10.0
    config.simulation.dt = 0.01
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

def factory_wrapper(gains):
    return ClassicalSMC(gains, max_force=100.0, boundary_layer=0.1)

class PatchedEvaluator(ControllerCostEvaluator):
    def _compute_cost_from_traj(self, t, x_b, u_b, sigma_b):
        # Call original
        cost = super()._compute_cost_from_traj(t, x_b, u_b, sigma_b)
        
        # Manually remove the passive penalty if it was applied
        # Passive penalty is 0.1 * instability_penalty = 100.0
        # If cost is roughly 100.0 + epsilon, subtract 100.0
        
        passive_penalty = 0.1 * self.instability_penalty
        
        # Heuristic to remove it (since we don't have easy access to the mask inside)
        # Note: This is hacky but sufficient for diagnostics
        if np.any(cost >= passive_penalty):
             # Assuming cost was small before penalty
             cost = np.where(cost >= passive_penalty, cost - passive_penalty, cost)
             
        return cost

def verify_deep_dive():
    print("Deep Dive: Verifying underlying costs (ignoring passive penalty)...")
    
    config = create_real_config()
    # Use PatchedEvaluator
    evaluator = PatchedEvaluator(factory_wrapper, config, u_max=150.0)
    
    optimized_gains = np.array([23.068, 12.854, 5.515, 3.487, 2.233, 0.148])
    baseline_gains = np.array([5.0, 5.0, 5.0, 0.5, 0.5, 0.5])
    
    print(f"\nEvaluating Optimized Gains: {optimized_gains}")
    opt_cost = evaluator.evaluate_single(optimized_gains)
    print(f"Optimized Cost (Adjusted): {opt_cost:.6f}")
    
    print(f"\nEvaluating Baseline Gains: {baseline_gains}")
    base_cost = evaluator.evaluate_single(baseline_gains)
    print(f"Baseline Cost (Adjusted): {base_cost:.6f}")
    
    improvement = base_cost - opt_cost
    if base_cost > 0:
        pct_improvement = (improvement / base_cost) * 100.0
    else:
        pct_improvement = 0.0
        
    print(f"\nUnderlying Improvement: {improvement:.6f} ({pct_improvement:.2f}%)")
    
    return True

if __name__ == "__main__":
    verify_deep_dive()
    sys.exit(0)
