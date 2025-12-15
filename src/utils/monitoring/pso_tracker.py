#======================================================================================
#================= src/utils/monitoring/pso_tracker.py =================
#======================================================================================
"""
PSO optimization run tracking for production monitoring system.

This module provides tracking capabilities for PSO optimization runs, including:
- Convergence history (gbest over iterations)
- Hyperparameter logging (swarm size, bounds, iterations)
- Individual simulation run linking
- Comparison and analysis tools

Architecture:
    PSORunTracker manages PSO optimization runs, storing:
    - Run metadata (controller, scenario, start/end time)
    - Hyperparameters (swarm size, iterations, bounds, inertia, cognitive, social)
    - Convergence history (gbest fitness per iteration)
    - Simulation run IDs (links to individual controller evaluations)
    - Final gains and performance metrics

Usage:
    >>> from src.utils.monitoring.pso_tracker import PSORunTracker
    >>> tracker = PSORunTracker()
    >>>
    >>> # Start PSO run
    >>> pso_run_id = tracker.start_pso_run(
    ...     controller='adaptive_smc',
    ...     scenario='nominal',
    ...     hyperparameters={'n_particles': 30, 'iterations': 50}
    ... )
    >>>
    >>> # Log iterations
    >>> for i, gbest_fitness in enumerate(gbest_history):
    ...     tracker.log_iteration(pso_run_id, i, gbest_fitness)
    >>>
    >>> # Complete run
    >>> tracker.complete_pso_run(pso_run_id, final_gains, final_score)

Integration:
    - Works with DataManager for simulation run tracking
    - Uses SQLite pso_runs table for indexing
    - Stores convergence data in JSON format
    - Links to individual simulation runs via run_id references

Author: Claude Code (AI-assisted development)
Date: December 2025
"""

import json
import logging
import sqlite3
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np


@dataclass
class PSOHyperparameters:
    """PSO optimization hyperparameters."""

    n_particles: int
    iterations: int
    bounds_lower: List[float]
    bounds_upper: List[float]
    inertia: float = 0.7298
    cognitive: float = 1.49618
    social: float = 1.49618
    seed: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class PSOIteration:
    """Single PSO iteration data."""

    iteration: int
    gbest_fitness: float
    gbest_position: List[float]
    timestamp: float


@dataclass
class PSORunData:
    """Complete PSO run data."""

    pso_run_id: str
    controller: str
    scenario: str
    start_time: float
    end_time: Optional[float]
    hyperparameters: PSOHyperparameters
    convergence: List[PSOIteration]
    final_gains: Optional[List[float]]
    final_score: Optional[float]
    simulation_run_ids: List[str]  # Links to individual simulation runs
    status: str  # 'running', 'complete', 'failed'


class PSORunTracker:
    """
    Tracks PSO optimization runs with convergence history and hyperparameters.

    This tracker manages PSO optimization runs, storing:
    - Run metadata (controller, scenario, timestamps)
    - Hyperparameters (swarm size, bounds, coefficients)
    - Convergence history (gbest per iteration)
    - Simulation run IDs (links to DataManager)
    - Final gains and performance

    Storage:
        - SQLite index: monitoring_data/index.db (pso_runs table)
        - JSON files: monitoring_data/pso_runs/{pso_run_id}.json

    Attributes:
        db_path: Path to SQLite database
        pso_runs_dir: Directory for PSO run JSON files
    """

    def __init__(self, data_dir: Path = Path("monitoring_data")):
        """
        Initialize PSO run tracker.

        Args:
            data_dir: Root directory for monitoring data
        """
        self.data_dir = Path(data_dir)
        self.db_path = self.data_dir / "index.db"
        self.pso_runs_dir = self.data_dir / "pso_runs"

        # Create directories
        self.pso_runs_dir.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._init_db()

        logging.info(f"PSORunTracker initialized at {self.data_dir}")

    def _init_db(self) -> None:
        """Initialize SQLite database with pso_runs table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create pso_runs table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pso_runs (
                pso_run_id TEXT PRIMARY KEY,
                controller TEXT NOT NULL,
                start_time REAL NOT NULL,
                end_time REAL,
                n_particles INTEGER,
                iterations INTEGER,
                final_score REAL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Add scenario column if it doesn't exist (migration for existing databases)
        try:
            cursor.execute("ALTER TABLE pso_runs ADD COLUMN scenario TEXT DEFAULT 'nominal'")
            conn.commit()
        except sqlite3.OperationalError:
            # Column already exists
            pass

        # Create index for fast queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_pso_controller_scenario
            ON pso_runs(controller, scenario)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_pso_status
            ON pso_runs(status)
        """)

        conn.commit()
        conn.close()

        logging.info("PSO runs database initialized")

    def start_pso_run(
        self,
        controller: str,
        scenario: str,
        hyperparameters: Dict[str, Any]
    ) -> str:
        """
        Start tracking a new PSO optimization run.

        Args:
            controller: Controller type (e.g., 'adaptive_smc')
            scenario: Scenario name (e.g., 'nominal', 'robust')
            hyperparameters: PSO hyperparameters dict

        Returns:
            PSO run ID (e.g., 'pso_20251215_203000_adaptive_smc')
        """
        # Generate unique run ID
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        pso_run_id = f"pso_{timestamp}_{controller}"

        # Create hyperparameters object
        hp = PSOHyperparameters(**hyperparameters)

        # Create run data
        run_data = PSORunData(
            pso_run_id=pso_run_id,
            controller=controller,
            scenario=scenario,
            start_time=time.time(),
            end_time=None,
            hyperparameters=hp,
            convergence=[],
            final_gains=None,
            final_score=None,
            simulation_run_ids=[],
            status='running'
        )

        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO pso_runs (
                pso_run_id, controller, start_time,
                n_particles, iterations, status, scenario
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pso_run_id,
            controller,
            run_data.start_time,
            hp.n_particles,
            hp.iterations,
            'running',
            scenario
        ))

        conn.commit()
        conn.close()

        # Save to JSON file
        self._save_run_data(run_data)

        logging.info(f"Started PSO run: {pso_run_id}")
        return pso_run_id

    def log_iteration(
        self,
        pso_run_id: str,
        iteration: int,
        gbest_fitness: float,
        gbest_position: List[float]
    ) -> None:
        """
        Log a single PSO iteration.

        Args:
            pso_run_id: PSO run identifier
            iteration: Iteration number (0-indexed)
            gbest_fitness: Global best fitness at this iteration
            gbest_position: Global best position (gains) at this iteration
        """
        # Load current run data
        run_data = self._load_run_data(pso_run_id)

        if not run_data:
            logging.warning(f"PSO run {pso_run_id} not found")
            return

        # Add iteration data
        iteration_data = PSOIteration(
            iteration=iteration,
            gbest_fitness=gbest_fitness,
            gbest_position=gbest_position,
            timestamp=time.time()
        )

        run_data.convergence.append(iteration_data)

        # Save updated data
        self._save_run_data(run_data)

    def link_simulation_run(self, pso_run_id: str, simulation_run_id: str) -> None:
        """
        Link a simulation run to this PSO run.

        Args:
            pso_run_id: PSO run identifier
            simulation_run_id: Simulation run ID from DataManager
        """
        run_data = self._load_run_data(pso_run_id)

        if not run_data:
            logging.warning(f"PSO run {pso_run_id} not found")
            return

        # Add simulation run ID if not already present
        if simulation_run_id not in run_data.simulation_run_ids:
            run_data.simulation_run_ids.append(simulation_run_id)
            self._save_run_data(run_data)

    def complete_pso_run(
        self,
        pso_run_id: str,
        final_gains: List[float],
        final_score: float
    ) -> None:
        """
        Mark PSO run as complete with final results.

        Args:
            pso_run_id: PSO run identifier
            final_gains: Final optimized gains
            final_score: Final performance score
        """
        run_data = self._load_run_data(pso_run_id)

        if not run_data:
            logging.warning(f"PSO run {pso_run_id} not found")
            return

        # Update run data
        run_data.end_time = time.time()
        run_data.final_gains = final_gains
        run_data.final_score = final_score
        run_data.status = 'complete'

        # Update database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE pso_runs
            SET end_time = ?, final_score = ?, status = ?
            WHERE pso_run_id = ?
        """, (run_data.end_time, final_score, 'complete', pso_run_id))

        conn.commit()
        conn.close()

        # Save to JSON
        self._save_run_data(run_data)

        logging.info(f"Completed PSO run: {pso_run_id} (score: {final_score:.2f})")

    def fail_pso_run(self, pso_run_id: str, error: str) -> None:
        """
        Mark PSO run as failed.

        Args:
            pso_run_id: PSO run identifier
            error: Error message
        """
        try:
            run_data = self._load_run_data(pso_run_id)
        except Exception as load_error:
            logging.warning(f"Failed to load PSO run data for {pso_run_id}: {load_error}")
            run_data = None

        if not run_data:
            # Can't load run data, just update database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE pso_runs
                SET end_time = ?, status = ?
                WHERE pso_run_id = ?
            """, (time.time(), 'failed', pso_run_id))

            conn.commit()
            conn.close()

            logging.error(f"Failed PSO run (DB only): {pso_run_id} - {error}")
            return

        run_data.end_time = time.time()
        run_data.status = 'failed'

        # Update database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE pso_runs
            SET end_time = ?, status = ?
            WHERE pso_run_id = ?
        """, (run_data.end_time, 'failed', pso_run_id))

        conn.commit()
        conn.close()

        # Save to JSON
        try:
            self._save_run_data(run_data)
        except Exception as save_error:
            logging.warning(f"Failed to save run data for {pso_run_id}: {save_error}")

        logging.error(f"Failed PSO run: {pso_run_id} - {error}")

    def query_pso_runs(
        self,
        controller: Optional[str] = None,
        scenario: Optional[str] = None,
        status: Optional[str] = None,
        min_score: Optional[float] = None,
        limit: int = 50
    ) -> List[PSORunData]:
        """
        Query PSO runs with filters.

        Args:
            controller: Filter by controller type
            scenario: Filter by scenario
            status: Filter by status ('running', 'complete', 'failed')
            min_score: Minimum final score threshold
            limit: Maximum number of runs to return

        Returns:
            List of PSORunData objects matching filters
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build query
        query = "SELECT pso_run_id FROM pso_runs WHERE 1=1"
        params = []

        if controller:
            query += " AND controller = ?"
            params.append(controller)

        if scenario:
            query += " AND scenario = ?"
            params.append(scenario)

        if status:
            query += " AND status = ?"
            params.append(status)

        if min_score is not None:
            query += " AND final_score >= ?"
            params.append(min_score)

        query += " ORDER BY start_time DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        # Load full data for each run
        results = []
        for row in rows:
            pso_run_id = row[0]
            run_data = self._load_run_data(pso_run_id)
            if run_data:
                results.append(run_data)

        logging.info(f"Query returned {len(results)} PSO runs")
        return results

    def _save_run_data(self, run_data: PSORunData) -> None:
        """Save PSO run data to JSON file."""
        file_path = self.pso_runs_dir / f"{run_data.pso_run_id}.json"

        # Convert to dict for JSON serialization
        data_dict = {
            'pso_run_id': run_data.pso_run_id,
            'controller': run_data.controller,
            'scenario': run_data.scenario,
            'start_time': run_data.start_time,
            'end_time': run_data.end_time,
            'hyperparameters': run_data.hyperparameters.to_dict(),
            'convergence': [
                {
                    'iteration': it.iteration,
                    'gbest_fitness': it.gbest_fitness,
                    'gbest_position': it.gbest_position,
                    'timestamp': it.timestamp
                }
                for it in run_data.convergence
            ],
            'final_gains': run_data.final_gains,
            'final_score': run_data.final_score,
            'simulation_run_ids': run_data.simulation_run_ids,
            'status': run_data.status
        }

        with open(file_path, 'w') as f:
            json.dump(data_dict, f, indent=2)

    def _load_run_data(self, pso_run_id: str) -> Optional[PSORunData]:
        """Load PSO run data from JSON file."""
        file_path = self.pso_runs_dir / f"{pso_run_id}.json"

        if not file_path.exists():
            return None

        with open(file_path, 'r') as f:
            data_dict = json.load(f)

        # Reconstruct objects
        hp = PSOHyperparameters(**data_dict['hyperparameters'])

        convergence = [
            PSOIteration(**it_dict)
            for it_dict in data_dict['convergence']
        ]

        return PSORunData(
            pso_run_id=data_dict['pso_run_id'],
            controller=data_dict['controller'],
            scenario=data_dict['scenario'],
            start_time=data_dict['start_time'],
            end_time=data_dict['end_time'],
            hyperparameters=hp,
            convergence=convergence,
            final_gains=data_dict['final_gains'],
            final_score=data_dict['final_score'],
            simulation_run_ids=data_dict['simulation_run_ids'],
            status=data_dict['status']
        )
