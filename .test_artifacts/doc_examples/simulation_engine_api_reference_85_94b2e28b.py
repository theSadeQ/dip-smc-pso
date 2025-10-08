# Example from: docs\api\simulation_engine_api_reference.md
# Index: 85
# Runnable: True
# Hash: 94b2e28b

"""
Example 2: Batch Simulation for PSO Optimization
Demonstrates vectorized batch execution for parameter optimization
"""

import numpy as np
import matplotlib.pyplot as plt
from functools import partial
from src.config import load_config
from src.controllers import create_controller
from src.plant.models import LowRankDIPDynamics
from src.simulation.orchestrators import BatchOrchestrator
from src.simulation.integrators import IntegratorFactory
from src.optimization import PSOTuner

# ============================================================================
# STEP 1: Configuration and Setup
# ============================================================================
config = load_config('config.yaml')
dynamics = LowRankDIPDynamics(config.plant)
integrator = IntegratorFactory.create_integrator('rk4', dt=0.01)

# ============================================================================
# STEP 2: Define Controller Factory for PSO
# ============================================================================
def controller_factory(gains):
    """Create controller instance with candidate gains."""
    return create_controller(
        'classical_smc',
        config=config,
        gains=gains  # [k1, k2, λ1, λ2, K, kd]
    )

# ============================================================================
# STEP 3: Define Fitness Function with Batch Execution
# ============================================================================
def fitness_function(gains, n_trials=10):
    """
    Evaluate controller gains using batch simulation.

    Args:
        gains: Controller gains to evaluate
        n_trials: Number of Monte Carlo trials (different ICs)

    Returns:
        Fitness value (lower is better)
    """
    # Create controller
    controller = controller_factory(gains)

    # Generate batch of initial conditions (small perturbations)
    np.random.seed(42)  # Reproducibility
    batch_initial = np.zeros((n_trials, 6))
    batch_initial[:, 1] = np.random.uniform(0.05, 0.15, n_trials)  # theta1
    batch_initial[:, 2] = np.random.uniform(0.05, 0.15, n_trials)  # theta2

    # Precompute control sequence for all trials
    horizon = 500
    dt = 0.01
    controls = np.zeros((n_trials, horizon))

    # Temporary: compute control for each initial condition
    # (In practice, use controller in orchestrator loop)
    for i in range(n_trials):
        x_temp = batch_initial[i]
        for j in range(horizon):
            controls[i, j] = controller(j * dt, x_temp)
            # Simple Euler prediction for next control (approximation)
            x_temp = x_temp + dt * np.array([
                x_temp[3], x_temp[4], x_temp[5], 0, 0, 0
            ])

    # Execute batch simulation
    orchestrator = BatchOrchestrator(dynamics, integrator)
    result = orchestrator.execute(
        initial_state=batch_initial,
        control_inputs=controls,
        dt=dt,
        horizon=horizon,
        safety_guards=True
    )

    # Compute fitness metrics
    all_states = result.get_states()  # (n_trials, horizon+1, 6)

    fitness_values = []
    for i in range(n_trials):
        states_i = all_states[i]  # (horizon+1, 6)

        # Metric 1: Settling time (2% threshold)
        settled_mask = np.all(np.abs(states_i[:, :3]) < 0.02, axis=1)
        if np.any(settled_mask):
            settling_idx = np.where(settled_mask)[0][0]
            settling_time = settling_idx * dt
        else:
            settling_time = 5.0  # Penalty if never settled

        # Metric 2: Peak overshoot
        peak_overshoot = np.max(np.abs(states_i[:, :3]))

        # Metric 3: Integral squared error
        ise = np.sum(np.sum(states_i[:, :3]**2, axis=1)) * dt

        # Combined fitness (weighted sum)
        fitness_i = (
            2.0 * settling_time +        # Weight settling time heavily
            5.0 * peak_overshoot +        # Penalize overshoot
            0.1 * ise                     # Penalize tracking error
        )

        fitness_values.append(fitness_i)

    # Return mean fitness over all trials
    return np.mean(fitness_values)

# ============================================================================
# STEP 4: Configure and Run PSO Optimization
# ============================================================================
# Define gain bounds for classical SMC
# [k1, k2, λ1, λ2, K, kd]
bounds = [
    (1.0, 50.0),   # k1: position gain
    (1.0, 40.0),   # k2: position damping
    (1.0, 50.0),   # λ1: angle gain 1
    (1.0, 40.0),   # λ2: angle gain 2
    (10.0, 100.0), # K: switching gain
    (0.1, 10.0)    # kd: derivative gain
]

print("=" * 70)
print("PSO OPTIMIZATION WITH BATCH SIMULATION")
print("=" * 70)

# Create PSO tuner
tuner = PSOTuner(
    fitness_fn=partial(fitness_function, n_trials=10),
    bounds=bounds,
    swarm_size=20,
    max_iter=50,
    verbose=True
)

# Run optimization
result = tuner.optimise()

# ============================================================================
# STEP 5: Display Results
# ============================================================================
print("\n" + "=" * 70)
print("OPTIMIZATION RESULTS")
print("=" * 70)
print(f"Best fitness: {result['best_fitness']:.4f}")
print(f"Best gains: {result['best_gains']}")
print(f"Convergence iteration: {result['convergence_iter']}")

# ============================================================================
# STEP 6: Validate Optimal Gains
# ============================================================================
optimal_controller = controller_factory(result['best_gains'])

from src.simulation import run_simulation

t_val, x_val, u_val = run_simulation(
    controller=optimal_controller,
    dynamics_model=dynamics,
    sim_time=5.0,
    dt=0.01,
    initial_state=np.array([0, 0.1, 0.1, 0, 0, 0]),
    u_max=100.0
)

# Plot validation
fig, ax = plt.subplots(2, 1, figsize=(10, 8))

ax[0].plot(t_val, x_val[:, 1] * 180/np.pi, 'r-', label='Pole 1')
ax[0].plot(t_val, x_val[:, 2] * 180/np.pi, 'g-', label='Pole 2')
ax[0].set_ylabel('Angles (deg)')
ax[0].legend()
ax[0].grid(True)
ax[0].set_title('Optimal Controller Performance')

ax[1].plot(t_val[:-1], u_val, 'm-')
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Control (N)')
ax[1].grid(True)

plt.tight_layout()
plt.savefig('results/pso_batch_simulation.png', dpi=150)
plt.show()

print("\nValidation plot saved to: results/pso_batch_simulation.png")