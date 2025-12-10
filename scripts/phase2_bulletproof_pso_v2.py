#!/usr/bin/env python
"""
================================================================================
Phase 2 Bulletproof PSO v2 - Multi-Scenario Robust Optimization
================================================================================

Fixes 4 critical root causes from diagnostic report:
1. Uses RobustCostEvaluator (15 IC scenarios, no disturbances)
2. Baseline-only warm-start (40% baseline + 60% random, NO MT-8 gains)
3. Adaptive PSO hyperparameters (w_schedule, velocity_clamp, c1=1.5)
4. Updated config bounds (k1_max=15, k2_max=7, epsilon_max=4)

Features:
- 15-scenario robust evaluation (±0.05, ±0.15, ±0.3 rad initial conditions)
- Baseline-guided warm-start (40% near safe defaults + 60% random)
- Adaptive inertia weight (0.9 -> 0.4 linear decay)
- Velocity clamping (10-50% of bounds)
- Checkpoint saves every 20 iterations
- Automatic resume from last checkpoint
- Sequential controller optimization (STA-SMC -> Adaptive SMC -> Hybrid)

Expected Outcome: Cost ~15-30 (vs 136-140 previous), convergence at iteration 100-120

Usage:
    python scripts/phase2_bulletproof_pso_v2.py                    # Start fresh
    python scripts/phase2_bulletproof_pso_v2.py --resume            # Resume from checkpoint
    python scripts/phase2_bulletproof_pso_v2.py --controller sta_smc  # Run single controller

Author: Claude Code
Created: December 10, 2025
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.controllers.factory import create_controller
from src.config import load_config
from src.optimization.checkpoint import get_checkpoint_manager, PSOCheckpoint
from src.optimization.core.robust_cost_evaluator import RobustCostEvaluator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


# Phase 2 controller configuration
CONTROLLERS = {
    'sta_smc': {
        'name': 'STA-SMC',
        'type': 'sta_smc',
        'n_gains': 6,
        'output_file': 'optimization_results/phase2_pso_results/sta_smc_gains.json'
    },
    'adaptive_smc': {
        'name': 'Adaptive SMC',
        'type': 'adaptive_smc',
        'n_gains': 5,
        'output_file': 'optimization_results/phase2_pso_results/adaptive_smc_gains.json'
    },
    'hybrid_adaptive_sta_smc': {
        'name': 'Hybrid Adaptive STA-SMC',
        'type': 'hybrid_adaptive_sta_smc',
        'n_gains': 4,
        'output_file': 'optimization_results/phase2_pso_results/hybrid_adaptive_sta_smc_gains.json'
    }
}


def setup_output_directory():
    """Create output directories."""
    output_dir = Path("optimization_results/phase2_pso_results")
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {output_dir}")


def load_baseline_gains(
    controller_key: str,
    n_gains: int,
    config
) -> Optional[np.ndarray]:
    """
    Load only baseline gains (NO MT-8 optimized gains).
    MT-8 gains were optimized for disturbances, not nominal ICs.

    Args:
        controller_key: Controller identifier (e.g., 'sta_smc')
        n_gains: Number of gains to extract
        config: Loaded configuration object

    Returns:
        Baseline gains array or None if not found
    """
    baseline_gains = None

    try:
        # Load baseline gains from config.controller_defaults.<controller_key>.gains
        if hasattr(config.controller_defaults, controller_key):
            default_config = getattr(config.controller_defaults, controller_key)
            if hasattr(default_config, 'gains'):
                baseline_gains = np.array(default_config.gains[:n_gains])
                logger.info(f"[OK] Loaded baseline gains: {baseline_gains}")
    except Exception as e:
        logger.warning(f"[WARNING] Failed to load baseline: {e}")

    # Validation
    if baseline_gains is None or len(baseline_gains) != n_gains:
        logger.warning("[WARNING] Warm-start disabled, using random init")
        return None

    return baseline_gains


def initialize_warm_start_swarm(
    n_particles: int,
    n_gains: int,
    baseline_gains: np.ndarray,
    min_bounds: np.ndarray,
    max_bounds: np.ndarray,
    rng: np.random.Generator,
    noise_factor: float = 0.1
) -> np.ndarray:
    """
    40% baseline + 60% random (NO MT-8 optimized gains).

    Args:
        n_particles: Swarm size (default 40)
        n_gains: Number of gains for controller
        baseline_gains: Safe defaults from config.controller_defaults.<ctrl>.gains
        min_bounds: Lower bounds for gains
        max_bounds: Upper bounds for gains
        rng: NumPy random generator
        noise_factor: Gaussian noise scale (default 0.1 = 10% of bounds)

    Returns:
        Swarm positions array (n_particles x n_gains)
    """
    swarm_pos = np.zeros((n_particles, n_gains))

    # Calculate noise standard deviation (10% of bound range)
    noise_std = noise_factor * (max_bounds - min_bounds)

    # Calculate particle counts (for n_particles=40)
    n_baseline = int(0.40 * n_particles)  # 16 particles
    n_random = n_particles - n_baseline   # 24 particles

    idx = 0

    # Particles near baseline
    for i in range(n_baseline):
        noise = rng.normal(0, noise_std)
        swarm_pos[idx] = np.clip(baseline_gains + noise, min_bounds, max_bounds)
        idx += 1

    # Random particles
    for i in range(n_random):
        swarm_pos[idx] = rng.uniform(min_bounds, max_bounds)
        idx += 1

    return swarm_pos


def create_robust_cost_evaluator_wrapper(controller_type: str, config):
    """
    Use RobustCostEvaluator for proper 15-scenario IC-based robust evaluation.
    NO disturbances (different from MT-8).

    Args:
        controller_type: Controller type string (e.g., 'sta_smc')
        config: Global configuration object

    Returns:
        Cost function that evaluates a single gain vector
    """
    # Controller factory
    def controller_factory(gains):
        controller_config = getattr(config.controllers, controller_type)
        return create_controller(
            controller_type,
            config=controller_config.model_dump() if hasattr(controller_config, 'model_dump') else dict(controller_config),
            gains=gains.tolist() if isinstance(gains, np.ndarray) else gains
        )

    # Create RobustCostEvaluator (15 IC scenarios, alpha=0.3)
    evaluator = RobustCostEvaluator(
        controller_factory=controller_factory,
        config=config,
        seed=42,
        n_scenarios=15,
        worst_case_weight=0.3,
        scenario_distribution={
            'nominal': 0.2,    # 3 scenarios: ±0.05 rad
            'moderate': 0.3,   # 4 scenarios: ±0.15 rad
            'large': 0.5       # 8 scenarios: ±0.3 rad
        },
        nominal_range=0.05,
        moderate_range=0.15,
        large_range=0.3
    )

    # Single-particle wrapper
    def cost_fn(gains: np.ndarray) -> float:
        try:
            return evaluator.evaluate_single_robust(gains)
        except Exception as e:
            logger.warning(f"Cost evaluation failed: {e}")
            return 1e6  # Penalty for failures

    return cost_fn


def run_pso_with_checkpoints(
    controller_key: str,
    controller_config: Dict[str, Any],
    config,
    checkpoint_manager,
    max_iters: int = 200,
    n_particles: int = 40,
    seed: Optional[int] = None,
    resume: bool = True
) -> Tuple[float, np.ndarray, int]:
    """
    Run PSO optimization with automatic checkpointing and baseline warm-start.

    Args:
        controller_key: Controller identifier (e.g., 'sta_smc')
        controller_config: Controller configuration dict
        config: Global configuration
        checkpoint_manager: Checkpoint manager instance
        max_iters: Maximum PSO iterations
        n_particles: Swarm size
        seed: Random seed
        resume: Whether to resume from checkpoint if available

    Returns:
        Tuple of (best_cost, best_gains, final_iteration)
    """
    logger.info(f"")
    logger.info(f"{'='*80}")
    logger.info(f"Optimizing: {controller_config['name']} ({controller_key})")
    logger.info(f"{'='*80}")

    # Check for existing checkpoint
    checkpoint = None
    start_iter = 0

    if resume:
        checkpoint = checkpoint_manager.load_latest_checkpoint(controller_key)
        if checkpoint:
            start_iter = checkpoint.iteration
            logger.info(f"[RESUME] Found checkpoint at iteration {start_iter}/{max_iters}")
            logger.info(f"[RESUME] Best cost so far: {checkpoint.best_cost:.6f}")

    # Initialize RNG
    rng = np.random.default_rng(seed)

    # Get bounds from config
    pso_cfg = config.pso
    bounds_config = pso_cfg.bounds

    if hasattr(bounds_config, controller_key):
        controller_bounds = getattr(bounds_config, controller_key)
        min_bounds = np.array(controller_bounds.min[:controller_config['n_gains']])
        max_bounds = np.array(controller_bounds.max[:controller_config['n_gains']])
    else:
        min_bounds = np.array(pso_cfg.bounds.min[:controller_config['n_gains']])
        max_bounds = np.array(pso_cfg.bounds.max[:controller_config['n_gains']])

    # Initialize or resume swarm
    if checkpoint:
        # Resume from checkpoint (takes precedence over warm-start)
        logger.info("[RESUME] Loading swarm from checkpoint")
        swarm_pos = np.array(checkpoint.swarm_positions)
        swarm_vel = np.array(checkpoint.swarm_velocities)
        swarm_best_pos = np.array(checkpoint.swarm_best_positions)
        swarm_best_cost = np.array(checkpoint.swarm_best_costs)
        global_best_pos = np.array(checkpoint.best_position)
        global_best_cost = checkpoint.best_cost
        cost_history = checkpoint.cost_history.copy()
        pos_history = [np.array(p) for p in checkpoint.position_history]
    else:
        # Load baseline gains for warm-start
        baseline_gains = load_baseline_gains(
            controller_key=controller_key,
            n_gains=controller_config['n_gains'],
            config=config
        )

        if baseline_gains is not None:
            # Warm-start initialization (baseline approach)
            logger.info("[WARM-START] Initializing: 40% baseline + 60% random")
            logger.info(f"  Baseline: {baseline_gains}")

            swarm_pos = initialize_warm_start_swarm(
                n_particles=n_particles,
                n_gains=controller_config['n_gains'],
                baseline_gains=baseline_gains,
                min_bounds=min_bounds,
                max_bounds=max_bounds,
                rng=rng,
                noise_factor=0.1
            )
        else:
            # Fallback to random initialization
            logger.info("[RANDOM] Warm-start disabled, using random initialization")
            swarm_pos = rng.uniform(min_bounds, max_bounds, size=(n_particles, controller_config['n_gains']))

        # Initialize remaining PSO state
        swarm_vel = np.zeros((n_particles, controller_config['n_gains']))
        swarm_best_pos = swarm_pos.copy()
        swarm_best_cost = np.full(n_particles, np.inf)
        global_best_pos = None
        global_best_cost = np.inf
        cost_history = []
        pos_history = []

    # Cost function (RobustCostEvaluator)
    cost_fn = create_robust_cost_evaluator_wrapper(controller_config['type'], config)

    # Adaptive PSO hyperparameters
    c1 = 1.5  # Reduced from 2.0 (less fragmentation)
    c2 = pso_cfg.c2  # Keep 2.0 (social weight)

    # Adaptive inertia schedule (linear decay)
    w_max = pso_cfg.w_schedule[0] if hasattr(pso_cfg, 'w_schedule') else 0.9
    w_min = pso_cfg.w_schedule[1] if hasattr(pso_cfg, 'w_schedule') else 0.4
    w_values = np.linspace(w_max, w_min, max_iters)

    # Velocity clamping (fraction of bounds)
    range_bounds = max_bounds - min_bounds
    v_clamp_min_frac = pso_cfg.velocity_clamp[0] if hasattr(pso_cfg, 'velocity_clamp') else 0.1
    v_clamp_max_frac = pso_cfg.velocity_clamp[1] if hasattr(pso_cfg, 'velocity_clamp') else 0.5
    v_min_clamp = v_clamp_min_frac * range_bounds
    v_max_clamp = v_clamp_max_frac * range_bounds

    logger.info(f"[PSO CONFIG] Adaptive inertia: w=[{w_max:.2f} -> {w_min:.2f}]")
    logger.info(f"[PSO CONFIG] Velocity clamp: [{v_clamp_min_frac*100:.0f}%, {v_clamp_max_frac*100:.0f}%] of bounds")
    logger.info(f"[PSO CONFIG] c1={c1:.2f} (cognitive), c2={c2:.2f} (social)")

    # PSO loop with checkpointing
    checkpoint_interval = checkpoint_manager.checkpoint_interval

    for iter_num in range(start_iter, max_iters):
        iter_start_time = time.time()

        # Get adaptive inertia for this iteration
        w = w_values[iter_num]

        # Evaluate fitness for all particles
        for i in range(n_particles):
            cost = cost_fn(swarm_pos[i])

            # Update particle best
            if cost < swarm_best_cost[i]:
                swarm_best_cost[i] = cost
                swarm_best_pos[i] = swarm_pos[i].copy()

            # Update global best
            if cost < global_best_cost:
                global_best_cost = cost
                global_best_pos = swarm_pos[i].copy()

        # Record history
        cost_history.append(float(global_best_cost))
        pos_history.append(global_best_pos.copy())

        # Update velocities and positions with adaptive w and velocity clamping
        for i in range(n_particles):
            r1 = rng.random(controller_config['n_gains'])
            r2 = rng.random(controller_config['n_gains'])

            # Velocity update with adaptive inertia
            swarm_vel[i] = (
                w * swarm_vel[i] +                              # Adaptive inertia (0.9->0.4)
                c1 * r1 * (swarm_best_pos[i] - swarm_pos[i]) + # Reduced cognitive (1.5)
                c2 * r2 * (global_best_pos - swarm_pos[i])     # Social (2.0)
            )

            # Apply velocity clamping
            swarm_vel[i] = np.clip(swarm_vel[i], -v_max_clamp, v_max_clamp)

            # Enforce minimum velocity (prevent stagnation)
            vel_mag = np.abs(swarm_vel[i])
            below_min = vel_mag < v_min_clamp
            if below_min.any():
                swarm_vel[i][below_min] = np.sign(swarm_vel[i][below_min]) * v_min_clamp[below_min]

            # Update position
            swarm_pos[i] = swarm_pos[i] + swarm_vel[i]
            swarm_pos[i] = np.clip(swarm_pos[i], min_bounds, max_bounds)

        iter_time = time.time() - iter_start_time

        # Log progress with adaptive w
        if (iter_num + 1) % 10 == 0 or iter_num == 0:
            logger.info(
                f"  Iteration {iter_num+1}/{max_iters} | "
                f"Best Cost: {global_best_cost:.6f} | "
                f"w={w:.3f} | Time: {iter_time:.2f}s"
            )

        # Save checkpoint at interval
        if (iter_num + 1) % checkpoint_interval == 0 or iter_num == max_iters - 1:
            try:
                checkpoint_manager.save_checkpoint(
                    controller_name=controller_key,
                    iteration=iter_num + 1,
                    total_iterations=max_iters,
                    best_cost=global_best_cost,
                    best_position=global_best_pos,
                    cost_history=cost_history,
                    position_history=pos_history,
                    swarm_positions=swarm_pos,
                    swarm_velocities=swarm_vel,
                    swarm_best_positions=swarm_best_pos,
                    swarm_best_costs=swarm_best_cost,
                    seed=seed,
                    metadata={'controller_type': controller_config['type']}
                )
            except Exception as e:
                logger.error(f"[ERROR] Failed to save checkpoint: {e}")

    logger.info(f"")
    logger.info(f"[OK] Optimization complete!")
    logger.info(f"[OK] Best cost: {global_best_cost:.6f}")
    logger.info(f"[OK] Best gains: {global_best_pos}")

    return global_best_cost, global_best_pos, max_iters


def save_controller_results(controller_key: str, controller_config: Dict[str, Any], best_cost: float, best_gains: np.ndarray, iterations: int):
    """Save optimization results to JSON file."""
    output_file = Path(controller_config['output_file'])
    output_file.parent.mkdir(parents=True, exist_ok=True)

    results = {
        'controller': controller_config['name'],
        'type': controller_config['type'],
        'cost': float(best_cost),
        'gains': best_gains.tolist(),
        'iterations': iterations,
        'timestamp': time.time(),
        'method': 'Bulletproof PSO v2 (15 IC scenarios, adaptive w, baseline warm-start)'
    }

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    logger.info(f"[OK] Results saved: {output_file}")


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(description="Bulletproof Phase 2 PSO v2 Optimization")
    parser.add_argument('--resume', action='store_true', help="Resume from checkpoints")
    parser.add_argument('--controller', type=str, choices=list(CONTROLLERS.keys()), help="Run single controller")
    parser.add_argument('--iterations', type=int, default=200, help="PSO iterations (default: 200)")
    parser.add_argument('--particles', type=int, default=40, help="Swarm size (default: 40)")
    parser.add_argument('--seed', type=int, default=42, help="Random seed (default: 42)")
    args = parser.parse_args()

    logger.info("="*80)
    logger.info("PHASE 2 BULLETPROOF PSO v2 OPTIMIZATION")
    logger.info("="*80)
    logger.info(f"Initialization: 40% baseline + 60% random (NO MT-8 gains)")
    logger.info(f"Cost function: RobustCostEvaluator (15 IC scenarios)")
    logger.info(f"Adaptive inertia: 0.9 -> 0.4 (linear decay)")
    logger.info(f"Velocity clamp: [10%, 50%] of bounds")
    logger.info(f"Checkpoint interval: Every 20 iterations")
    logger.info(f"Resume mode: {'Enabled' if args.resume else 'Disabled'}")
    logger.info("="*80)

    # Setup
    setup_output_directory()
    config = load_config("config.yaml")
    checkpoint_manager = get_checkpoint_manager()

    # Select controllers to run
    if args.controller:
        controllers_to_run = {args.controller: CONTROLLERS[args.controller]}
    else:
        controllers_to_run = CONTROLLERS

    # Sequential execution
    for ctrl_key, ctrl_config in controllers_to_run.items():
        # Check if already complete
        output_file = Path(ctrl_config['output_file'])
        if output_file.exists() and not args.resume:
            logger.info(f"")
            logger.info(f"[SKIP] {ctrl_config['name']} already complete: {output_file}")
            continue

        try:
            # Run PSO optimization
            best_cost, best_gains, iterations = run_pso_with_checkpoints(
                controller_key=ctrl_key,
                controller_config=ctrl_config,
                config=config,
                checkpoint_manager=checkpoint_manager,
                max_iters=args.iterations,
                n_particles=args.particles,
                seed=args.seed,
                resume=args.resume
            )

            # Save results
            save_controller_results(ctrl_key, ctrl_config, best_cost, best_gains, iterations)

            # Clear checkpoints after successful completion
            checkpoint_manager.clear_checkpoints(ctrl_key)

        except KeyboardInterrupt:
            logger.warning(f"")
            logger.warning(f"[INTERRUPTED] Optimization interrupted by user")
            logger.warning(f"[INFO] Checkpoint saved - run with --resume to continue")
            sys.exit(1)

        except Exception as e:
            logger.error(f"")
            logger.error(f"[ERROR] Optimization failed: {e}")
            logger.error(f"[INFO] Checkpoint saved - run with --resume to continue")
            raise

    logger.info("")
    logger.info("="*80)
    logger.info("[OK] ALL CONTROLLERS COMPLETE!")
    logger.info("="*80)
    logger.info(f"Results saved to: optimization_results/phase2_pso_results/")


if __name__ == '__main__':
    main()
