"""
Phase 4: Verify Optimization Claims
Purpose: Verify if PSO optimized gains actually outperform baseline gains, and check for cost saturation.
"""

import sys
import os
import numpy as np
from types import SimpleNamespace

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.optimization.core.cost_evaluator import ControllerCostEvaluator
from src.controllers.factory import create_controller
from src.plant.models.simplified.config import SimplifiedDIPConfig
from src.controllers.smc.classic_smc import ClassicalSMC

def create_real_config():
    """Create a configuration object that matches the project defaults."""
    # We should try to load the actual config.yaml if possible, but fallback to code defaults
    # for reproducibility in this script.
    
    config = SimpleNamespace()
    
    # Physics (Defaults from SimplifiedDIPConfig)
    config.physics = SimplifiedDIPConfig.create_default()
    
    # Simulation
    config.simulation = SimpleNamespace()
    config.simulation.duration = 10.0 # From reports
    config.simulation.dt = 0.01
    
    # Cost Function (Weights from MT-8 Report/Code)
    config.cost_function = SimpleNamespace()
    config.cost_function.weights = SimpleNamespace()
    # Weights from report: we=50.0, wu=0.2, wud=0.1, ws=0.1
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
    """Wrapper to create controller from gains."""
    # Classical SMC gains: [k1, k2, lam1, lam2, K, kd]
    # Default max_force=100.0, boundary_layer=0.1 (from verify_simulations.py success)
    # MT-8 used max_force=100.0 (implied)
    return ClassicalSMC(gains, max_force=100.0, boundary_layer=0.1)

def verify_claims():
    print("Verifying PSO Optimization Claims...")
    
    config = create_real_config()
    evaluator = ControllerCostEvaluator(factory_wrapper, config, u_max=150.0) # Assume 150.0 as per prompt suspicion
    
    # 1. Gains from MT-8 Report (Classical SMC)
    # "Optimized Gains: [23.068, 12.854, 5.515, 3.487, 2.233, 0.148]"
    optimized_gains = np.array([23.068, 12.854, 5.515, 3.487, 2.233, 0.148])
    
    # 2. Baseline Gains (Defaults)
    # "Defaults: [5.0, 5.0, 5.0, 0.5, 0.5, 0.5]"
    baseline_gains = np.array([5.0, 5.0, 5.0, 0.5, 0.5, 0.5])
    
    print(f"\nEvaluating Optimized Gains: {optimized_gains}")
    opt_cost = evaluator.evaluate_single(optimized_gains)
    print(f"Optimized Cost: {opt_cost:.6f}")
    
    print(f"\nEvaluating Baseline Gains: {baseline_gains}")
    base_cost = evaluator.evaluate_single(baseline_gains)
    print(f"Baseline Cost: {base_cost:.6f}")
    
    # 3. Analysis
    print("\n--- Analysis ---")
    
    # Check for saturation
    is_saturated = (opt_cost < 1e-5) and (base_cost < 1e-5)
    
    if is_saturated:
        print("⚠️ COST SATURATION DETECTED")
        print(f"Both costs are effectively zero (floor: {evaluator.min_cost_floor})")
        print("The optimization likely found 'different' gains that hit the same minimum cost floor.")
    else:
        improvement = base_cost - opt_cost
        pct_improvement = (improvement / base_cost) * 100.0 if base_cost > 0 else 0.0
        print(f"Cost Improvement: {improvement:.6f} ({pct_improvement:.2f}%)")
        
        if improvement > 0:
            print("✅ Optimization showed improvement.")
        else:
            print("❌ Optimization FAILED to improve over baseline.")
            
    # Check if optimized gains actually stabilized (from internal knowledge of cost)
    # If cost > 1000, it failed.
    if opt_cost > 500.0:
        print("⚠️ Optimized gains resulted in high cost (likely unstable or passive penalty).")
        
    return True

if __name__ == "__main__":
    verify_claims()
    sys.exit(0)
