"""
================================================================================
MT-6 Adaptive Boundary Layer PSO Optimization Script
================================================================================

Optimize adaptive boundary layer parameters (ε_min, α) using PSO to minimize
chattering while maintaining control performance.

Goal: Find optimal (ε_min, α) where:
  - ε_min: Base boundary layer thickness ∈ [0.001, 0.02]
  - α: Adaptive slope coefficient ∈ [0.0, 2.0]
  - Effective thickness: ε_eff = ε_min + α|ṡ|

Fitness Function:
  - Primary: chattering_index (70% weight)
  - Constraint: settling_time penalty if >5s (15% weight)
  - Constraint: overshoot penalty if >0.3 rad (15% weight)

PSO Configuration:
  - Swarm size: 20 particles
  - Iterations: 30
  - Fitness evaluation: average over 10 Monte Carlo runs
  - Random seed: 42 (reproducibility)

Author: Agent B (Multi-Agent Orchestration)
Created: October 2025 (Week 2, Task MT-6)
Reference: ROADMAP_EXISTING_PROJECT.md
"""

import json
import csv
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
import sys
import time
import logging

# Third-party for PSO
import pyswarms as ps
from pyswarms.utils.plotters import plot_cost_history

# Local imports
from src.controllers.smc.algorithms.classical.controller import ModularClassicalSMC
from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig
from src.plant.models.dynamics import DIPParams
from src.plant.models.simplified.config import SimplifiedDIPConfig
from src.plant.models.simplified.dynamics import SimplifiedDIPDynamics
from src.utils.analysis.chattering import compute_chattering_metrics

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class OptimizationResult:
    """Results from PSO optimization."""
    best_epsilon_min: float
    best_alpha: float
    best_fitness: float
    convergence_iterations: int
    fitness_improvement: float
    optimization_history: List[Dict[str, Any]]


def generate_initial_conditions(n_samples: int, seed: int = 42) -> np.ndarray:
    """
    Generate random initial conditions for Monte Carlo simulation.

    State vector: [x, theta1, theta2, x_dot, theta1_dot, theta2_dot]

    Args:
        n_samples: Number of initial condition samples
        seed: Random seed for reproducibility

    Returns:
        Array of shape (n_samples, 6) with random initial conditions
    """
    rng = np.random.default_rng(seed)

    # Random initial angles and velocities
    theta1 = rng.uniform(-0.3, 0.3, n_samples)  # ±0.3 rad
    theta2 = rng.uniform(-0.3, 0.3, n_samples)  # ±0.3 rad
    theta1_dot = rng.uniform(-0.5, 0.5, n_samples)  # ±0.5 rad/s
    theta2_dot = rng.uniform(-0.5, 0.5, n_samples)  # ±0.5 rad/s

    # Cart position and velocity (start at origin, small velocity)
    x = np.zeros(n_samples)
    x_dot = rng.uniform(-0.1, 0.1, n_samples)

    # Stack into state vectors
    initial_conditions = np.column_stack([x, theta1, theta2, x_dot, theta1_dot, theta2_dot])
    return initial_conditions


def compute_settling_time(state_history: np.ndarray, dt: float = 0.01,
                         tolerance: float = 0.02) -> float:
    """
    Compute settling time (time to reach within 2% of final value).

    Args:
        state_history: State trajectory (T, 6)
        dt: Time step
        tolerance: Settling tolerance (2% of final value)

    Returns:
        Settling time in seconds (inf if not settled)
    """
    # Check pendulum angles (indices 1, 2)
    theta1 = state_history[:, 1]
    theta2 = state_history[:, 2]

    # Upright position is θ = 0
    target = 0.0
    abs_error = np.maximum(np.abs(theta1 - target), np.abs(theta2 - target))

    # Find first time when error stays within tolerance
    settled_mask = abs_error < tolerance

    if not np.any(settled_mask):
        return float('inf')

    # Find first sustained settling
    for i in range(len(settled_mask) - 10):
        if np.all(settled_mask[i:i+10]):
            return i * dt

    return float('inf')


def compute_overshoot(state_history: np.ndarray) -> float:
    """
    Compute maximum overshoot in pendulum angles.

    Args:
        state_history: State trajectory (T, 6)

    Returns:
        Maximum overshoot in radians
    """
    theta1 = state_history[:, 1]
    theta2 = state_history[:, 2]

    # Maximum deviation from upright (0 rad)
    max_theta1 = np.max(np.abs(theta1))
    max_theta2 = np.max(np.abs(theta2))

    return max(max_theta1, max_theta2)


def evaluate_single_run(epsilon_min: float, alpha: float,
                       initial_condition: np.ndarray,
                       config: Any, dynamics_params: DIPParams,
                       dt: float = 0.01, T: float = 10.0) -> Dict[str, float]:
    """
    Evaluate adaptive boundary layer for a single initial condition.

    Args:
        epsilon_min: Base boundary layer thickness
        alpha: Adaptive slope coefficient
        initial_condition: Initial state (6,)
        config: Configuration object (unused, kept for interface compatibility)
        dynamics_params: Physics parameters
        dt: Time step
        T: Simulation duration

    Returns:
        Dictionary with metrics: chattering_index, settling_time, overshoot
    """
    # Create classical SMC config with adaptive boundary layer
    # Use PSO-optimized gains from gain optimization (Oct 19, 2025)
    # Source: optimization_results/gains_mt6_fixed.json
    gains = [23.67, 14.29, 8.87, 3.55, 6.52, 2.93]  # [k1, k2, lam1, lam2, K, kd] - PSO optimized

    smc_config = ClassicalSMCConfig(
        gains=gains,
        max_force=100.0,
        boundary_layer=epsilon_min,  # Base thickness
        boundary_layer_slope=alpha,  # Adaptive slope
        dt=dt
    )

    # Create controller
    controller = ModularClassicalSMC(smc_config)

    # Run simulation manually
    try:
        # Create dynamics config from DIPParams
        dip_config = SimplifiedDIPConfig(
            cart_mass=dynamics_params.cart_mass,
            pendulum1_mass=dynamics_params.pendulum1_mass,
            pendulum2_mass=dynamics_params.pendulum2_mass,
            pendulum1_length=dynamics_params.pendulum1_length,
            pendulum2_length=dynamics_params.pendulum2_length,
            pendulum1_com=dynamics_params.pendulum1_com,
            pendulum2_com=dynamics_params.pendulum2_com,
            pendulum1_inertia=dynamics_params.pendulum1_inertia,
            pendulum2_inertia=dynamics_params.pendulum2_inertia,
            cart_friction=dynamics_params.cart_damping,
            joint1_friction=dynamics_params.pendulum1_damping,
            joint2_friction=dynamics_params.pendulum2_damping,
            gravity=dynamics_params.gravity
        )
        dynamics = SimplifiedDIPDynamics(dip_config)

        # Initialize simulation
        n_steps = int(T / dt)
        state_history = np.zeros((n_steps, 6))
        control_history = np.zeros(n_steps)

        # Set initial state
        state = initial_condition.copy()
        state_history[0] = state

        # Simulation loop
        for i in range(1, n_steps):
            # Compute control
            ctrl_result = controller.compute_control(state, None, {})
            u = ctrl_result['u']
            control_history[i-1] = u

            # Apply dynamics
            state = dynamics.step(state, u, dt)
            state_history[i] = state

            # Check for divergence
            if np.any(np.abs(state) > 100):
                raise ValueError("Simulation diverged")

        # Last control value
        ctrl_result = controller.compute_control(state, None, {})
        control_history[-1] = ctrl_result['u']

        # Compute chattering index
        chattering_metrics = compute_chattering_metrics(control_history, dt)
        chattering_index = chattering_metrics.get('chattering_index', 0.0)

        # Compute settling time (relaxed tolerance to match Agent A baseline)
        settling_time = compute_settling_time(state_history, dt, tolerance=0.05)

        # Compute overshoot
        overshoot = compute_overshoot(state_history)

        return {
            'chattering_index': chattering_index,
            'settling_time': settling_time,
            'overshoot': overshoot,
            'success': True
        }

    except Exception as e:
        logger.warning(f"Simulation failed for ε={epsilon_min:.4f}, α={alpha:.4f}: {e}")
        return {
            'chattering_index': 1e6,
            'settling_time': 1e6,
            'overshoot': 1e6,
            'success': False
        }


def fitness_function(params: np.ndarray, mc_samples: int = 10, seed: int = 42,
                    dynamics_params: DIPParams = None) -> np.ndarray:
    """
    PSO fitness function: minimize chattering with performance constraints.

    Args:
        params: Parameter array (n_particles, 2) where each row is [epsilon_min, alpha]
        mc_samples: Number of Monte Carlo samples per evaluation
        seed: Random seed
        dynamics_params: Pre-loaded dynamics parameters (to avoid re-loading config)

    Returns:
        Fitness values (n_particles,) - lower is better
    """
    n_particles = params.shape[0]
    fitness_values = np.zeros(n_particles)

    # Use provided dynamics params or create default
    if dynamics_params is None:
        # Create default DIP parameters directly
        dynamics_params = DIPParams()

    # Generate initial conditions for Monte Carlo
    initial_conditions = generate_initial_conditions(mc_samples, seed=seed)

    for i in range(n_particles):
        epsilon_min, alpha = params[i]

        # Evaluate across Monte Carlo samples
        chattering_values = []
        settling_values = []
        overshoot_values = []
        success_count = 0

        for ic in initial_conditions:
            metrics = evaluate_single_run(
                epsilon_min, alpha, ic, None, dynamics_params,
                dt=0.01, T=10.0
            )

            if metrics['success']:
                chattering_values.append(metrics['chattering_index'])
                settling_values.append(metrics['settling_time'])
                overshoot_values.append(metrics['overshoot'])
                success_count += 1

        # If no successful runs, assign high penalty
        if success_count == 0:
            fitness_values[i] = 1e8
            continue

        # Average metrics
        avg_chattering = np.mean(chattering_values)
        avg_settling = np.mean(settling_values)
        avg_overshoot = np.mean(overshoot_values)

        # Fitness function (minimize):
        # - Primary: chattering_index (70% weight)
        # - Constraint: settling_time penalty if >5s (15% weight)
        # - Constraint: overshoot penalty if >0.3 rad (15% weight)

        chattering_cost = avg_chattering

        # Cap settling time to prevent inf penalties (max simulation duration = 10s)
        settling_capped = np.minimum(avg_settling, 10.0)
        settling_penalty = max(0, settling_capped - 5.0) * 10.0  # Max penalty = 50.0

        # Overshoot penalty (soft constraint)
        overshoot_penalty = max(0, avg_overshoot - 0.3) * 10.0  # Penalty if >0.3 rad

        # Numerical safety: clip all components to reasonable ranges
        chattering_clipped = np.clip(chattering_cost, 0.0, 100.0)
        settling_clipped = np.clip(settling_penalty, 0.0, 100.0)
        overshoot_clipped = np.clip(overshoot_penalty, 0.0, 100.0)

        # Combined fitness with safety check
        fitness = (0.70 * chattering_clipped +
                  0.15 * settling_clipped +
                  0.15 * overshoot_clipped)

        # Final safety check for non-finite values
        if not np.isfinite(fitness):
            fitness = 1e8  # Large penalty for invalid configurations

        fitness_values[i] = fitness

        logger.info(f"Particle {i}: ε={epsilon_min:.4f}, α={alpha:.2f} → "
                   f"chattering={avg_chattering:.4f}, settling={avg_settling:.2f}s, "
                   f"overshoot={avg_overshoot:.3f}rad, fitness={fitness:.4f}")

    return fitness_values


def run_pso_optimization(n_particles: int = 20, n_iterations: int = 30,
                        seed: int = 42) -> OptimizationResult:
    """
    Run PSO optimization to find best adaptive boundary layer parameters.

    Args:
        n_particles: Swarm size
        n_iterations: Number of iterations
        seed: Random seed

    Returns:
        OptimizationResult with best parameters and convergence info
    """
    logger.info("Starting PSO optimization for adaptive boundary layer...")
    logger.info(f"Swarm size: {n_particles}, Iterations: {n_iterations}, Seed: {seed}")

    # Create default dynamics parameters once
    dynamics_params = DIPParams()

    # Parameter bounds: [epsilon_min, alpha]
    min_bounds = np.array([0.001, 0.0])   # Lower bounds
    max_bounds = np.array([0.02, 2.0])    # Upper bounds
    bounds = (min_bounds, max_bounds)

    # PSO options (standard PSO parameters)
    options = {
        'c1': 0.5,  # Cognitive parameter
        'c2': 0.3,  # Social parameter
        'w': 0.9    # Inertia weight
    }

    # Initialize optimizer
    optimizer = ps.single.GlobalBestPSO(
        n_particles=n_particles,
        dimensions=2,
        options=options,
        bounds=bounds
    )

    # Track optimization history
    optimization_history = []

    # Custom cost function wrapper to track history
    def cost_wrapper(params):
        fitness = fitness_function(params, mc_samples=10, seed=seed,
                                  dynamics_params=dynamics_params)
        iteration = len(optimization_history) + 1
        best_idx = np.argmin(fitness)
        best_fitness = fitness[best_idx]
        best_params = params[best_idx]

        optimization_history.append({
            'iteration': iteration,
            'best_fitness': float(best_fitness),
            'best_epsilon_min': float(best_params[0]),
            'best_alpha': float(best_params[1]),
            'mean_fitness': float(np.mean(fitness)),
            'std_fitness': float(np.std(fitness))
        })

        logger.info(f"Iteration {iteration}/{n_iterations}: "
                   f"best_fitness={best_fitness:.4f}, "
                   f"best_params=[{best_params[0]:.4f}, {best_params[1]:.2f}]")

        return fitness

    # Run optimization
    np.random.seed(seed)
    best_cost, best_pos = optimizer.optimize(cost_wrapper, iters=n_iterations)

    # Extract results
    best_epsilon_min, best_alpha = best_pos
    initial_fitness = optimization_history[0]['best_fitness']
    final_fitness = best_cost
    fitness_improvement = initial_fitness - final_fitness

    # Find convergence iteration (when fitness change < 1%)
    convergence_iter = n_iterations
    for i in range(1, len(optimization_history)):
        prev_fitness = optimization_history[i-1]['best_fitness']
        curr_fitness = optimization_history[i]['best_fitness']
        if abs(curr_fitness - prev_fitness) / (prev_fitness + 1e-12) < 0.01:
            convergence_iter = i + 1
            break

    logger.info(f"Optimization complete!")
    logger.info(f"Best parameters: ε_min={best_epsilon_min:.4f}, α={best_alpha:.2f}")
    logger.info(f"Best fitness: {best_cost:.4f}")
    logger.info(f"Fitness improvement: {fitness_improvement:.4f}")
    logger.info(f"Convergence iteration: {convergence_iter}/{n_iterations}")

    return OptimizationResult(
        best_epsilon_min=best_epsilon_min,
        best_alpha=best_alpha,
        best_fitness=best_cost,
        convergence_iterations=convergence_iter,
        fitness_improvement=fitness_improvement,
        optimization_history=optimization_history
    )


def validate_best_parameters(epsilon_min: float, alpha: float,
                            n_runs: int = 100, seed: int = 42) -> Dict[str, Any]:
    """
    Validate best parameters with 100 Monte Carlo runs.

    Args:
        epsilon_min: Best base boundary layer thickness
        alpha: Best adaptive slope coefficient
        n_runs: Number of validation runs
        seed: Random seed

    Returns:
        Dictionary with validation statistics
    """
    logger.info(f"Validating best parameters with {n_runs} Monte Carlo runs...")

    # Create default dynamics parameters
    dynamics_params = DIPParams()

    # Generate initial conditions
    initial_conditions = generate_initial_conditions(n_runs, seed=seed)

    # Collect metrics
    chattering_values = []
    settling_values = []
    overshoot_values = []
    success_count = 0

    for i, ic in enumerate(initial_conditions):
        if (i + 1) % 20 == 0:
            logger.info(f"  Progress: {i+1}/{n_runs} runs")

        metrics = evaluate_single_run(
            epsilon_min, alpha, ic, None, dynamics_params,
            dt=0.01, T=10.0
        )

        if metrics['success']:
            chattering_values.append(metrics['chattering_index'])
            settling_values.append(metrics['settling_time'])
            overshoot_values.append(metrics['overshoot'])
            success_count += 1

    # Compute statistics
    chattering_array = np.array(chattering_values)
    settling_array = np.array(settling_values)
    overshoot_array = np.array(overshoot_values)

    # 95% confidence intervals (assuming normal distribution)
    from scipy import stats

    def compute_ci(data):
        mean = np.mean(data)
        std = np.std(data, ddof=1)
        se = std / np.sqrt(len(data))
        ci = stats.t.interval(0.95, len(data) - 1, loc=mean, scale=se)
        return mean, std, ci

    chat_mean, chat_std, chat_ci = compute_ci(chattering_array)
    settle_mean, settle_std, settle_ci = compute_ci(settling_array)
    over_mean, over_std, over_ci = compute_ci(overshoot_array)

    validation_stats = {
        'n_runs': n_runs,
        'success_count': success_count,
        'success_rate': success_count / n_runs,
        'chattering_index_mean': float(chat_mean),
        'chattering_index_std': float(chat_std),
        'chattering_index_ci_lower': float(chat_ci[0]),
        'chattering_index_ci_upper': float(chat_ci[1]),
        'settling_time_mean': float(settle_mean),
        'settling_time_std': float(settle_std),
        'settling_time_ci_lower': float(settle_ci[0]),
        'settling_time_ci_upper': float(settle_ci[1]),
        'overshoot_mean': float(over_mean),
        'overshoot_std': float(over_std),
        'overshoot_ci_lower': float(over_ci[0]),
        'overshoot_ci_upper': float(over_ci[1])
    }

    logger.info(f"Validation complete!")
    logger.info(f"Success rate: {validation_stats['success_rate']*100:.1f}%")
    logger.info(f"Chattering: {chat_mean:.4f} ± {chat_std:.4f} (95% CI: [{chat_ci[0]:.4f}, {chat_ci[1]:.4f}])")
    logger.info(f"Settling: {settle_mean:.2f} ± {settle_std:.2f}s (95% CI: [{settle_ci[0]:.2f}, {settle_ci[1]:.2f}])")
    logger.info(f"Overshoot: {over_mean:.3f} ± {over_std:.3f}rad (95% CI: [{over_ci[0]:.3f}, {over_ci[1]:.3f}])")

    return validation_stats


def save_results(opt_result: OptimizationResult, validation_stats: Dict[str, Any],
                output_csv: Path):
    """
    Save optimization results to CSV file.

    Args:
        opt_result: PSO optimization results
        validation_stats: Validation statistics
        output_csv: Output CSV path
    """
    logger.info(f"Saving results to {output_csv}...")

    # Prepare CSV rows (one row per PSO iteration)
    rows = []
    for entry in opt_result.optimization_history:
        rows.append({
            'iteration': entry['iteration'],
            'epsilon_min': entry['best_epsilon_min'],
            'alpha': entry['best_alpha'],
            'best_fitness': entry['best_fitness'],
            'mean_fitness': entry['mean_fitness'],
            'std_fitness': entry['std_fitness']
        })

    # Write to CSV
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    logger.info(f"Saved {len(rows)} optimization iterations to {output_csv}")

    # Also save summary JSON
    summary_json = output_csv.with_suffix('.json')
    summary = {
        'best_parameters': {
            'epsilon_min': opt_result.best_epsilon_min,
            'alpha': opt_result.best_alpha
        },
        'optimization_summary': {
            'best_fitness': opt_result.best_fitness,
            'convergence_iterations': opt_result.convergence_iterations,
            'fitness_improvement': opt_result.fitness_improvement
        },
        'validation_statistics': validation_stats
    }

    with open(summary_json, 'w') as f:
        json.dump(summary, f, indent=2)

    logger.info(f"Saved summary to {summary_json}")


def main():
    """Main optimization workflow."""
    logger.info("=" * 80)
    logger.info("MT-6 Adaptive Boundary Layer PSO Optimization")
    logger.info("=" * 80)

    # Configuration
    N_PARTICLES = 20
    N_ITERATIONS = 30
    N_VALIDATION_RUNS = 100
    SEED = 42
    OUTPUT_CSV = Path("benchmarks/MT6_adaptive_optimization.csv")

    # Step 1: Run PSO optimization
    logger.info("\nStep 1: PSO Optimization")
    logger.info("-" * 80)
    opt_result = run_pso_optimization(
        n_particles=N_PARTICLES,
        n_iterations=N_ITERATIONS,
        seed=SEED
    )

    # Step 2: Validate best parameters
    logger.info("\nStep 2: Validation with 100 Monte Carlo Runs")
    logger.info("-" * 80)
    validation_stats = validate_best_parameters(
        epsilon_min=opt_result.best_epsilon_min,
        alpha=opt_result.best_alpha,
        n_runs=N_VALIDATION_RUNS,
        seed=SEED
    )

    # Step 3: Save results
    logger.info("\nStep 3: Saving Results")
    logger.info("-" * 80)
    save_results(opt_result, validation_stats, OUTPUT_CSV)

    # Final summary
    logger.info("\n" + "=" * 80)
    logger.info("OPTIMIZATION COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Best Parameters:")
    logger.info(f"  ε_min = {opt_result.best_epsilon_min:.6f}")
    logger.info(f"  α = {opt_result.best_alpha:.6f}")
    logger.info(f"\nOptimization Summary:")
    logger.info(f"  Best Fitness: {opt_result.best_fitness:.6f}")
    logger.info(f"  Convergence: {opt_result.convergence_iterations}/{N_ITERATIONS} iterations")
    logger.info(f"  Improvement: {opt_result.fitness_improvement:.6f}")
    logger.info(f"\nValidation Results (100 runs):")
    logger.info(f"  Chattering: {validation_stats['chattering_index_mean']:.4f} ± {validation_stats['chattering_index_std']:.4f}")
    logger.info(f"  Settling: {validation_stats['settling_time_mean']:.2f} ± {validation_stats['settling_time_std']:.2f}s")
    logger.info(f"  Overshoot: {validation_stats['overshoot_mean']:.3f} ± {validation_stats['overshoot_std']:.3f}rad")
    logger.info(f"\nResults saved to: {OUTPUT_CSV}")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
