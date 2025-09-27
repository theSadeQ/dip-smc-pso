#==========================================================================================\\\
#================= optimization/issue_2_pso_surface_optimization.py ====================\\\
#==========================================================================================\\\

"""
🔵 PSO Optimization Engineer - Issue #2 Surface Parameter Optimization

Advanced PSO optimization for STA-SMC surface coefficients with damping constraints.
Implements constraint-aware optimization to achieve ζ ∈ [0.6,0.8] for overshoot resolution.

Author: PSO Optimization Engineer Agent
Purpose: Validate and optimize surface coefficients from Control Systems Specialist
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
import logging
from dataclasses import dataclass
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PSO_OptimizationConfig:
    """Configuration for PSO surface optimization."""
    # PSO Parameters
    n_particles: int = 30
    n_iterations: int = 150
    w: float = 0.7            # Inertia weight
    c1: float = 2.0           # Cognitive coefficient
    c2: float = 2.0           # Social coefficient

    # Optimization bounds
    K1_bounds: Tuple[float, float] = (5.0, 15.0)    # Algorithmic gain bounds
    K2_bounds: Tuple[float, float] = (3.0, 10.0)    # Algorithmic gain bounds
    k1_bounds: Tuple[float, float] = (8.0, 20.0)    # Surface gain bounds
    k2_bounds: Tuple[float, float] = (4.0, 12.0)    # Surface gain bounds
    lam1_bounds: Tuple[float, float] = (1.0, 8.0)   # λ1 constrained for ζ ∈ [0.6,0.8]
    lam2_bounds: Tuple[float, float] = (1.0, 6.0)   # λ2 constrained for ζ ∈ [0.6,0.8]

    # Damping constraints
    target_damping: float = 0.7
    damping_tolerance: float = 0.1      # ±0.1 → [0.6, 0.8]
    damping_penalty_weight: float = 100.0

    # Performance objectives
    overshoot_weight: float = 10.0
    settling_time_weight: float = 5.0
    control_effort_weight: float = 1.0
    robustness_weight: float = 2.0

class STA_SMC_PSO_Optimizer:
    """
    Advanced PSO optimizer for STA-SMC surface coefficient optimization.

    Implements constraint-aware PSO with damping ratio enforcement and
    multi-objective optimization for overshoot minimization.
    """

    def __init__(self, config: PSO_OptimizationConfig):
        """Initialize PSO optimizer with configuration."""
        self.config = config
        self.best_global_position = None
        self.best_global_cost = float('inf')
        self.convergence_history = []

        # Initialize particle swarm
        self.particles = self._initialize_particles()

        logger.info(f"🔵 PSO Optimizer initialized: {config.n_particles} particles, {config.n_iterations} iterations")
        logger.info(f"Damping constraints: ζ ∈ [{config.target_damping - config.damping_tolerance:.1f}, {config.target_damping + config.damping_tolerance:.1f}]")

    def _initialize_particles(self) -> Dict:
        """Initialize particle swarm with random positions and velocities."""
        n_dim = 6  # [K1, K2, k1, k2, λ1, λ2]
        n_particles = self.config.n_particles

        # Define bounds array
        bounds = np.array([
            self.config.K1_bounds,
            self.config.K2_bounds,
            self.config.k1_bounds,
            self.config.k2_bounds,
            self.config.lam1_bounds,
            self.config.lam2_bounds
        ])

        # Initialize positions within bounds
        positions = np.random.uniform(
            bounds[:, 0], bounds[:, 1],
            size=(n_particles, n_dim)
        )

        # Initialize velocities (10% of bound range)
        bound_range = bounds[:, 1] - bounds[:, 0]
        velocities = np.random.uniform(
            -0.1 * bound_range, 0.1 * bound_range,
            size=(n_particles, n_dim)
        )

        # Personal best tracking
        personal_best_positions = positions.copy()
        personal_best_costs = np.full(n_particles, float('inf'))

        particles = {
            'positions': positions,
            'velocities': velocities,
            'personal_best_positions': personal_best_positions,
            'personal_best_costs': personal_best_costs,
            'bounds': bounds
        }

        logger.info(f"Initialized {n_particles} particles with bounds:")
        for i, (param, bound) in enumerate(zip(['K1', 'K2', 'k1', 'k2', 'λ1', 'λ2'], bounds)):
            logger.info(f"  {param}: [{bound[0]:.1f}, {bound[1]:.1f}]")

        return particles

    def compute_damping_ratio(self, k: float, lam: float) -> float:
        """Compute damping ratio: ζ = λ/(2√k)"""
        return lam / (2 * np.sqrt(max(k, 1e-6)))  # Prevent division by zero

    def evaluate_damping_constraints(self, gains: np.ndarray) -> float:
        """Evaluate damping ratio constraints penalty."""
        K1, K2, k1, k2, lam1, lam2 = gains

        # Compute damping ratios
        zeta1 = self.compute_damping_ratio(k1, lam1)
        zeta2 = self.compute_damping_ratio(k2, lam2)

        # Target damping range
        zeta_min = self.config.target_damping - self.config.damping_tolerance
        zeta_max = self.config.target_damping + self.config.damping_tolerance

        # Penalty for violating damping constraints
        penalty = 0.0

        # Penalty for ζ1 outside [0.6, 0.8]
        if zeta1 < zeta_min:
            penalty += (zeta_min - zeta1) ** 2
        elif zeta1 > zeta_max:
            penalty += (zeta1 - zeta_max) ** 2

        # Penalty for ζ2 outside [0.6, 0.8]
        if zeta2 < zeta_min:
            penalty += (zeta_min - zeta2) ** 2
        elif zeta2 > zeta_max:
            penalty += (zeta2 - zeta_max) ** 2

        return penalty * self.config.damping_penalty_weight

    def estimate_performance_metrics(self, gains: np.ndarray) -> Dict[str, float]:
        """
        Estimate performance metrics for given gains.

        Since we don't have the full simulation here, we use analytical approximations
        based on control theory relationships.
        """
        K1, K2, k1, k2, lam1, lam2 = gains

        # Compute damping ratios
        zeta1 = self.compute_damping_ratio(k1, lam1)
        zeta2 = self.compute_damping_ratio(k2, lam2)

        # Overshoot estimation (analytical approximation)
        # For second-order system: %OS ≈ exp(-ζπ/√(1-ζ²)) × 100
        def estimate_overshoot(zeta):
            if zeta >= 1.0:
                return 0.0  # Overdamped, no overshoot
            elif zeta <= 0.0:
                return 100.0  # Underdamped, high overshoot
            else:
                return np.exp(-zeta * np.pi / np.sqrt(1 - zeta**2)) * 100

        overshoot1 = estimate_overshoot(zeta1)
        overshoot2 = estimate_overshoot(zeta2)
        overshoot_max = max(overshoot1, overshoot2)

        # Settling time estimation: t_s ≈ 4/(ζωn)
        omega_n1 = np.sqrt(k1 * lam1)
        omega_n2 = np.sqrt(k2 * lam2)
        settling_time1 = 4 / (zeta1 * omega_n1) if zeta1 > 0 else float('inf')
        settling_time2 = 4 / (zeta2 * omega_n2) if zeta2 > 0 else float('inf')
        settling_time_max = max(settling_time1, settling_time2)

        # Control effort (sum of algorithmic gains)
        control_effort = K1 + K2

        # Robustness metric (distance from optimal damping)
        robustness1 = 1.0 - abs(zeta1 - self.config.target_damping) / self.config.target_damping
        robustness2 = 1.0 - abs(zeta2 - self.config.target_damping) / self.config.target_damping
        robustness = min(robustness1, robustness2)

        return {
            'overshoot_max': overshoot_max,
            'settling_time_max': settling_time_max,
            'control_effort': control_effort,
            'robustness': robustness,
            'zeta1': zeta1,
            'zeta2': zeta2,
            'omega_n1': omega_n1,
            'omega_n2': omega_n2
        }

    def objective_function(self, gains: np.ndarray) -> float:
        """
        Multi-objective cost function for PSO optimization.

        Minimizes: overshoot, settling time, control effort
        Maximizes: robustness
        Enforces: damping ratio constraints
        """
        # Constraint penalty
        constraint_penalty = self.evaluate_damping_constraints(gains)

        # Performance metrics
        metrics = self.estimate_performance_metrics(gains)

        # Multi-objective cost
        cost = (
            self.config.overshoot_weight * metrics['overshoot_max'] +
            self.config.settling_time_weight * metrics['settling_time_max'] +
            self.config.control_effort_weight * metrics['control_effort'] -
            self.config.robustness_weight * metrics['robustness'] * 10 +  # Negative because we want to maximize
            constraint_penalty
        )

        return cost

    def update_particles(self, iteration: int):
        """Update particle positions and velocities using PSO equations."""
        positions = self.particles['positions']
        velocities = self.particles['velocities']
        personal_best_pos = self.particles['personal_best_positions']
        bounds = self.particles['bounds']

        n_particles, n_dim = positions.shape

        # Evaluate all particles
        for i in range(n_particles):
            cost = self.objective_function(positions[i])

            # Update personal best
            if cost < self.particles['personal_best_costs'][i]:
                self.particles['personal_best_costs'][i] = cost
                personal_best_pos[i] = positions[i].copy()

                # Update global best
                if cost < self.best_global_cost:
                    self.best_global_cost = cost
                    self.best_global_position = positions[i].copy()

        # Update velocities and positions
        for i in range(n_particles):
            # PSO velocity update
            r1, r2 = np.random.rand(2)

            velocities[i] = (
                self.config.w * velocities[i] +
                self.config.c1 * r1 * (personal_best_pos[i] - positions[i]) +
                self.config.c2 * r2 * (self.best_global_position - positions[i])
            )

            # Update position
            positions[i] += velocities[i]

            # Enforce bounds
            for j in range(n_dim):
                if positions[i, j] < bounds[j, 0]:
                    positions[i, j] = bounds[j, 0]
                    velocities[i, j] = 0  # Reset velocity component
                elif positions[i, j] > bounds[j, 1]:
                    positions[i, j] = bounds[j, 1]
                    velocities[i, j] = 0

        # Record convergence
        self.convergence_history.append({
            'iteration': iteration,
            'best_cost': self.best_global_cost,
            'best_position': self.best_global_position.copy()
        })

    def optimize(self) -> Dict:
        """Execute PSO optimization for surface coefficient tuning."""
        logger.info(f"🚀 Starting PSO optimization for Issue #2 surface coefficients...")

        for iteration in range(self.config.n_iterations):
            self.update_particles(iteration)

            if iteration % 25 == 0:
                metrics = self.estimate_performance_metrics(self.best_global_position)
                logger.info(f"Iteration {iteration:3d}: Cost={self.best_global_cost:.3f}, "
                          f"ζ1={metrics['zeta1']:.3f}, ζ2={metrics['zeta2']:.3f}, "
                          f"Overshoot={metrics['overshoot_max']:.1f}%")

        # Final analysis
        optimal_gains = self.best_global_position
        final_metrics = self.estimate_performance_metrics(optimal_gains)

        results = {
            'optimal_gains': optimal_gains.tolist(),
            'final_cost': self.best_global_cost,
            'performance_metrics': final_metrics,
            'convergence_history': self.convergence_history,
            'config': self.config
        }

        logger.info(f"✅ PSO optimization completed!")
        logger.info(f"Optimal gains: {optimal_gains}")
        logger.info(f"Final damping ratios: ζ1={final_metrics['zeta1']:.3f}, ζ2={final_metrics['zeta2']:.3f}")
        logger.info(f"Estimated overshoot: {final_metrics['overshoot_max']:.1f}%")

        return results

def validate_control_systems_solution():
    """Validate the Control Systems Specialist solution with PSO."""
    # Control Systems Specialist solution
    cs_solution = [8.0, 5.0, 12.0, 6.0, 4.85, 3.43]

    config = PSO_OptimizationConfig()
    optimizer = STA_SMC_PSO_Optimizer(config)

    # Evaluate CS solution
    cs_metrics = optimizer.estimate_performance_metrics(np.array(cs_solution))
    cs_cost = optimizer.objective_function(np.array(cs_solution))

    logger.info(f"🔍 Validating Control Systems Specialist solution:")
    logger.info(f"CS Solution: {cs_solution}")
    logger.info(f"CS Damping ratios: ζ1={cs_metrics['zeta1']:.3f}, ζ2={cs_metrics['zeta2']:.3f}")
    logger.info(f"CS Estimated overshoot: {cs_metrics['overshoot_max']:.1f}%")
    logger.info(f"CS Cost function: {cs_cost:.3f}")

    return cs_metrics, cs_cost

def main():
    """Execute complete PSO optimization analysis for Issue #2."""
    logger.info("🔵 PSO Optimization Engineer - Issue #2 Surface Parameter Optimization")
    logger.info("=" * 80)

    # Validate Control Systems solution first
    cs_metrics, cs_cost = validate_control_systems_solution()

    # Run PSO optimization
    config = PSO_OptimizationConfig()
    optimizer = STA_SMC_PSO_Optimizer(config)
    results = optimizer.optimize()

    # Compare solutions
    print(f"\n📊 OPTIMIZATION RESULTS COMPARISON")
    print("=" * 60)
    print(f"Control Systems Solution: {[8.0, 5.0, 12.0, 6.0, 4.85, 3.43]}")
    print(f"PSO Optimized Solution:   {[f'{x:.2f}' for x in results['optimal_gains']]}")
    print(f"")
    print(f"CS Damping Ratios:  ζ1={cs_metrics['zeta1']:.3f}, ζ2={cs_metrics['zeta2']:.3f}")
    print(f"PSO Damping Ratios: ζ1={results['performance_metrics']['zeta1']:.3f}, ζ2={results['performance_metrics']['zeta2']:.3f}")
    print(f"")
    print(f"CS Estimated Overshoot:  {cs_metrics['overshoot_max']:.1f}%")
    print(f"PSO Estimated Overshoot: {results['performance_metrics']['overshoot_max']:.1f}%")

    # Save results
    with open('optimization/issue_2_pso_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ PSO optimization complete. Results saved to issue_2_pso_results.json")
    print(f"🎯 Recommended gains for Issue #2: {[f'{x:.2f}' for x in results['optimal_gains']]}")

    return results

if __name__ == "__main__":
    results = main()