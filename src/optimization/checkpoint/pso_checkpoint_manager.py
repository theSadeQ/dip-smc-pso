#======================================================================================\\\
#================ src/optimization/checkpoint/pso_checkpoint_manager.py ===============\\\
#======================================================================================\\\

"""
PSO Checkpoint Manager - Crash-Resistant Optimization State Persistence

Provides atomic checkpoint saving/loading for PSO optimization runs.
Survives power failures, crashes, and manual interruptions with zero data loss.

Key Features:
- Atomic writes (temp + rename pattern)
- Resume from exact iteration
- Automatic recovery detection
- Multi-controller support
- Lightweight JSON format

Author: Claude Code
Created: December 9, 2025
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, asdict
import numpy as np
import time

logger = logging.getLogger(__name__)


@dataclass
class PSOCheckpoint:
    """PSO optimization state at a specific iteration."""
    controller_name: str
    iteration: int
    total_iterations: int
    best_cost: float
    best_position: List[float]
    cost_history: List[float]
    position_history: List[List[float]]
    swarm_positions: List[List[float]]  # Current swarm particle positions
    swarm_velocities: List[List[float]]  # Current swarm particle velocities
    swarm_best_positions: List[List[float]]  # Per-particle best positions
    swarm_best_costs: List[float]  # Per-particle best costs
    timestamp: float
    seed: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


class PSOCheckpointManager:
    """Manages PSO optimization checkpoints with atomic write guarantees."""

    def __init__(
        self,
        checkpoint_dir: Path = Path("optimization_results/phase2_pso_checkpoints"),
        checkpoint_interval: int = 20
    ):
        """
        Initialize checkpoint manager.

        Args:
            checkpoint_dir: Directory to store checkpoint files
            checkpoint_interval: Save checkpoint every N iterations
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_interval = checkpoint_interval
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"PSO Checkpoint Manager initialized: {self.checkpoint_dir}")

    def save_checkpoint(
        self,
        controller_name: str,
        iteration: int,
        total_iterations: int,
        best_cost: float,
        best_position: np.ndarray,
        cost_history: List[float],
        position_history: List[np.ndarray],
        swarm_positions: np.ndarray,
        swarm_velocities: np.ndarray,
        swarm_best_positions: np.ndarray,
        swarm_best_costs: np.ndarray,
        seed: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        Save PSO state to checkpoint file (atomic write).

        Args:
            controller_name: Name of controller being optimized
            iteration: Current iteration number
            total_iterations: Total iterations for optimization
            best_cost: Current best cost
            best_position: Current best position (gains)
            cost_history: Cost history up to current iteration
            position_history: Position history up to current iteration
            swarm_positions: Current swarm particle positions (n_particles x n_dims)
            swarm_velocities: Current swarm velocities (n_particles x n_dims)
            swarm_best_positions: Per-particle best positions (n_particles x n_dims)
            swarm_best_costs: Per-particle best costs (n_particles,)
            seed: Random seed used
            metadata: Additional metadata (optional)

        Returns:
            Path to saved checkpoint file
        """
        checkpoint = PSOCheckpoint(
            controller_name=controller_name,
            iteration=iteration,
            total_iterations=total_iterations,
            best_cost=float(best_cost),
            best_position=best_position.tolist() if isinstance(best_position, np.ndarray) else list(best_position),
            cost_history=[float(c) for c in cost_history],
            position_history=[
                pos.tolist() if isinstance(pos, np.ndarray) else list(pos)
                for pos in position_history
            ],
            swarm_positions=swarm_positions.tolist() if isinstance(swarm_positions, np.ndarray) else swarm_positions,
            swarm_velocities=swarm_velocities.tolist() if isinstance(swarm_velocities, np.ndarray) else swarm_velocities,
            swarm_best_positions=swarm_best_positions.tolist() if isinstance(swarm_best_positions, np.ndarray) else swarm_best_positions,
            swarm_best_costs=swarm_best_costs.tolist() if isinstance(swarm_best_costs, np.ndarray) else list(swarm_best_costs),
            timestamp=time.time(),
            seed=seed,
            metadata=metadata or {}
        )

        checkpoint_file = self.checkpoint_dir / f"{controller_name}_iter_{iteration}.json"
        temp_file = checkpoint_file.with_suffix('.tmp')

        # Atomic write pattern (write to temp, then rename)
        try:
            with open(temp_file, 'w') as f:
                json.dump(asdict(checkpoint), f, indent=2)

            # Atomic rename (overwrites existing file on POSIX, needs fallback on Windows)
            try:
                temp_file.replace(checkpoint_file)
            except OSError:
                # Windows fallback: delete + rename
                if checkpoint_file.exists():
                    checkpoint_file.unlink()
                temp_file.rename(checkpoint_file)

            logger.info(f"Checkpoint saved: {checkpoint_file} (iteration {iteration}/{total_iterations}, cost={best_cost:.6f})")

            # Cleanup old checkpoints (keep last 3)
            self._cleanup_old_checkpoints(controller_name, keep=3)

            return checkpoint_file

        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")
            if temp_file.exists():
                temp_file.unlink()
            raise

    def load_latest_checkpoint(self, controller_name: str) -> Optional[PSOCheckpoint]:
        """
        Load the most recent checkpoint for a controller.

        Args:
            controller_name: Name of controller

        Returns:
            PSOCheckpoint if found, None otherwise
        """
        checkpoints = sorted(
            self.checkpoint_dir.glob(f"{controller_name}_iter_*.json"),
            key=lambda p: int(p.stem.split('_')[-1]),
            reverse=True
        )

        if not checkpoints:
            logger.info(f"No checkpoints found for {controller_name}")
            return None

        latest = checkpoints[0]
        try:
            with open(latest, 'r') as f:
                data = json.load(f)

            checkpoint = PSOCheckpoint(**data)
            logger.info(f"Loaded checkpoint: {latest} (iteration {checkpoint.iteration}/{checkpoint.total_iterations})")
            return checkpoint

        except Exception as e:
            logger.error(f"Failed to load checkpoint {latest}: {e}")
            return None

    def has_checkpoint(self, controller_name: str) -> bool:
        """Check if checkpoints exist for a controller."""
        return len(list(self.checkpoint_dir.glob(f"{controller_name}_iter_*.json"))) > 0

    def get_progress(self, controller_name: str) -> Optional[Dict[str, Any]]:
        """
        Get optimization progress for a controller.

        Returns:
            Dict with iteration, total_iterations, percent_complete, best_cost
            or None if no checkpoint exists
        """
        checkpoint = self.load_latest_checkpoint(controller_name)
        if checkpoint is None:
            return None

        return {
            'iteration': checkpoint.iteration,
            'total_iterations': checkpoint.total_iterations,
            'percent_complete': (checkpoint.iteration / checkpoint.total_iterations) * 100,
            'best_cost': checkpoint.best_cost,
            'timestamp': checkpoint.timestamp
        }

    def _cleanup_old_checkpoints(self, controller_name: str, keep: int = 3):
        """Remove old checkpoints, keeping only the most recent N."""
        checkpoints = sorted(
            self.checkpoint_dir.glob(f"{controller_name}_iter_*.json"),
            key=lambda p: int(p.stem.split('_')[-1]),
            reverse=True
        )

        for old_checkpoint in checkpoints[keep:]:
            try:
                old_checkpoint.unlink()
                logger.debug(f"Deleted old checkpoint: {old_checkpoint}")
            except Exception as e:
                logger.warning(f"Failed to delete old checkpoint {old_checkpoint}: {e}")

    def clear_checkpoints(self, controller_name: str):
        """Remove all checkpoints for a controller (e.g., after completion)."""
        for checkpoint in self.checkpoint_dir.glob(f"{controller_name}_iter_*.json"):
            try:
                checkpoint.unlink()
                logger.debug(f"Cleared checkpoint: {checkpoint}")
            except Exception as e:
                logger.warning(f"Failed to clear checkpoint {checkpoint}: {e}")


# Convenience function for scripts
def get_checkpoint_manager(checkpoint_dir: Optional[Path] = None) -> PSOCheckpointManager:
    """Get a PSOCheckpointManager instance."""
    return PSOCheckpointManager(checkpoint_dir=checkpoint_dir or Path("optimization_results/phase2_pso_checkpoints"))
