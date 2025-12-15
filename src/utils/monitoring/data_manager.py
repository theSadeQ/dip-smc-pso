#======================================================================================\
#==================== src/utils/monitoring/data_manager.py ====================\
#======================================================================================\

"""
Production data management system for monitoring dashboard.

This module provides the core data orchestration layer for the production
monitoring system, handling hybrid storage (files + SQLite + memory cache),
live session management, and efficient querying.

Architecture:
    L1 Cache: Session cache (Streamlit st.session_state)
    L2 Cache: Memory cache (LRU, max 100 runs ~50MB)
    L3 Storage: File system (JSON + CSV + SQLite index)

Usage:
    dm = DataManager()

    # Store simulation run
    dm.store_run(dashboard_data)

    # Query historical runs
    runs = dm.query_runs(controller='adaptive_smc', limit=50)

    # Live monitoring
    session_id = dm.start_live_session('adaptive_smc')
    metrics = dm.get_live_metrics(session_id)
    dm.stop_live_session(session_id)
"""

import json
import sqlite3
import subprocess
import csv
import shutil
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import OrderedDict
import numpy as np
import pandas as pd

from .data_model import (
    DashboardData,
    PerformanceSummary,
    MetricsSnapshot,
    RunStatus
)


def convert_numpy_types(obj):
    """
    Recursively convert numpy types to Python native types for JSON serialization.

    Args:
        obj: Object to convert

    Returns:
        Object with numpy types converted to Python native types
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    else:
        return obj


class LRUCache:
    """
    Least Recently Used (LRU) cache for run metadata.

    Keeps most recently accessed runs in memory for fast access.
    """

    def __init__(self, max_size: int = 100):
        """
        Initialize LRU cache.

        Args:
            max_size: Maximum number of runs to cache
        """
        self.max_size = max_size
        self.cache: OrderedDict[str, DashboardData] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, run_id: str) -> Optional[DashboardData]:
        """Get run from cache (moves to end if found)."""
        if run_id in self.cache:
            self.hits += 1
            # Move to end (most recently used)
            self.cache.move_to_end(run_id)
            return self.cache[run_id]
        else:
            self.misses += 1
            return None

    def put(self, run_id: str, data: DashboardData) -> None:
        """Add run to cache (evicts oldest if full)."""
        if run_id in self.cache:
            # Update existing
            self.cache.move_to_end(run_id)
            self.cache[run_id] = data
        else:
            # Add new
            self.cache[run_id] = data
            self.cache.move_to_end(run_id)

            # Evict oldest if over capacity
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)  # Remove oldest (FIFO)

    def clear(self) -> None:
        """Clear cache."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0.0
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate_pct': hit_rate
        }


class DataManager:
    """
    Production data manager for monitoring system.

    Provides hybrid storage with three-tier caching:
    - L1: Session cache (Streamlit, outside this class)
    - L2: Memory LRU cache (this class)
    - L3: File system + SQLite index (this class)

    File Organization:
        monitoring_data/
        ├── runs/{run_id}/
        │   ├── metadata.json
        │   ├── timeseries.csv
        │   └── config.yaml
        ├── pso_runs/{pso_id}/
        ├── benchmarks/{benchmark_id}/
        ├── cache/
        └── index.db (SQLite)
    """

    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize data manager.

        Args:
            base_path: Base directory for monitoring data (default: monitoring_data/)
        """
        self.base_path = Path(base_path) if base_path else Path("monitoring_data")

        # Ensure directories exist
        self.runs_path = self.base_path / "runs"
        self.pso_path = self.base_path / "pso_runs"
        self.benchmarks_path = self.base_path / "benchmarks"
        self.cache_path = self.base_path / "cache"
        self.logs_path = self.base_path / "logs"

        for path in [self.runs_path, self.pso_path, self.benchmarks_path,
                     self.cache_path, self.logs_path]:
            path.mkdir(parents=True, exist_ok=True)

        # Logger (initialize early so _init_database can use it)
        self.logger = logging.getLogger("DataManager")
        self._setup_logging()

        # SQLite index
        self.db_path = self.base_path / "index.db"
        self._init_database()

        # L2 Memory cache
        self.cache = LRUCache(max_size=100)

        # Live sessions tracking
        self._live_sessions: Dict[str, Dict[str, Any]] = {}

    def _setup_logging(self) -> None:
        """Configure logging to file and console."""
        log_file = self.logs_path / f"data_manager_{datetime.now().strftime('%Y%m%d')}.log"

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        # Configure logger
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def _init_database(self) -> None:
        """Initialize SQLite database with schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Runs index table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                controller TEXT NOT NULL,
                scenario TEXT NOT NULL,
                status TEXT NOT NULL,
                settling_time REAL,
                overshoot REAL,
                steady_state_error REAL,
                energy REAL,
                chattering_index REAL,
                score REAL,
                duration_s REAL,
                created_at TEXT NOT NULL
            )
        """)

        # PSO runs index
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pso_runs (
                pso_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                controller TEXT NOT NULL,
                seed INTEGER,
                best_fitness REAL,
                iterations_converged INTEGER,
                created_at TEXT NOT NULL
            )
        """)

        # Benchmarks index
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS benchmarks (
                benchmark_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                scenario TEXT NOT NULL,
                num_controllers INTEGER,
                num_trials INTEGER,
                created_at TEXT NOT NULL
            )
        """)

        # Create indexes for fast queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_runs_controller ON runs(controller)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_runs_timestamp ON runs(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_runs_score ON runs(score)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pso_controller ON pso_runs(controller)")

        conn.commit()
        conn.close()

        self.logger.info(f"Database initialized at {self.db_path}")

    def generate_run_id(self, controller: str, scenario: str) -> str:
        """
        Generate unique run ID with timestamp.

        Format: {date}_{time}_{controller}_{scenario}
        Example: 2025-12-15_143022_adaptive_smc_nominal

        Args:
            controller: Controller type
            scenario: Scenario name

        Returns:
            Unique run ID string
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        return f"{timestamp}_{controller}_{scenario}"

    def store_run(self, data: DashboardData, save_timeseries: bool = True) -> str:
        """
        Store simulation run to file system and index.

        Args:
            data: DashboardData object to store
            save_timeseries: Whether to save full time-series CSV

        Returns:
            run_id of stored run
        """
        run_id = data.run_id
        run_dir = self.runs_path / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Save metadata.json
            metadata = {
                "run_id": data.run_id,
                "timestamp": datetime.now().isoformat(),
                "controller": {
                    "type": data.controller,
                    "config": data.config
                },
                "scenario": {
                    "type": data.scenario
                },
                "performance": data.summary.to_dict() if data.summary else {},
                "status": data.status.value,
                "start_time": data.start_time,
                "end_time": data.end_time,
                "duration_s": data.duration_s,
                "errors": data.errors,
                "warnings": data.warnings,
                "files": {
                    "timeseries": "timeseries.csv" if save_timeseries else None
                }
            }

            # Convert numpy types to Python native types for JSON serialization
            metadata = convert_numpy_types(metadata)

            metadata_path = run_dir / "metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            # Save timeseries.csv if requested
            if save_timeseries and data.snapshots:
                self._save_timeseries_csv(data, run_dir / "timeseries.csv")

            # Save config.yaml (snapshot of controller config)
            config_path = run_dir / "config.yaml"
            with open(config_path, 'w') as f:
                import yaml
                yaml.dump(data.config, f, default_flow_style=False)

            # Update SQLite index
            self._index_run(data)

            # Update L2 cache
            self.cache.put(run_id, data)

            self.logger.info(f"Stored run: {run_id}")
            return run_id

        except Exception as e:
            self.logger.error(f"Failed to store run {run_id}: {e}")
            raise

    def _save_timeseries_csv(self, data: DashboardData, filepath: Path) -> None:
        """Save time-series data to CSV."""
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                'time', 'x1', 'x2', 'x3', 'x4', 'u',
                'tracking_error', 'control_effort', 'chattering_metric'
            ])

            # Data rows
            for snap in data.snapshots:
                state = snap.state
                writer.writerow([
                    snap.timestamp_s,
                    state[0],  # theta1
                    state[1],  # theta2
                    state[2] if len(state) > 2 else 0.0,  # theta1_dot
                    state[3] if len(state) > 3 else 0.0,  # theta2_dot
                    snap.control_output,
                    snap.error_norm,
                    snap.control_effort,
                    snap.chattering_index
                ])

    def _index_run(self, data: DashboardData) -> None:
        """Add run to SQLite index for fast queries."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        summary = data.summary

        cursor.execute("""
            INSERT OR REPLACE INTO runs (
                run_id, timestamp, controller, scenario, status,
                settling_time, overshoot, steady_state_error, energy,
                chattering_index, score, duration_s, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.run_id,
            datetime.now().isoformat(),
            data.controller,
            data.scenario,
            data.status.value,
            summary.settling_time_s if summary else None,
            summary.overshoot_pct if summary else None,
            summary.steady_state_error if summary else None,
            summary.energy_j if summary else None,
            summary.chattering_amplitude if summary else None,
            summary.get_score() if summary else None,
            data.duration_s,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

    def load_metadata(self, run_id: str) -> Optional[DashboardData]:
        """
        Load run metadata from cache or disk.

        Args:
            run_id: Run identifier

        Returns:
            DashboardData object or None if not found
        """
        # Check L2 cache first
        cached = self.cache.get(run_id)
        if cached is not None:
            return cached

        # Load from disk
        metadata_path = self.runs_path / run_id / "metadata.json"

        if not metadata_path.exists():
            self.logger.warning(f"Metadata not found: {run_id}")
            return None

        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

            # Reconstruct DashboardData (without full snapshots for efficiency)
            summary = PerformanceSummary(**metadata['performance']) if metadata['performance'] else None

            data = DashboardData(
                run_id=metadata['run_id'],
                controller=metadata['controller']['type'],
                scenario=metadata['scenario']['type'],
                config=metadata['controller'].get('config', {}),
                snapshots=[],  # Don't load full timeseries for metadata queries
                summary=summary,
                status=RunStatus(metadata['status']),
                start_time=metadata['start_time'],
                end_time=metadata.get('end_time'),
                duration_s=metadata.get('duration_s', 0.0),
                errors=metadata.get('errors', []),
                warnings=metadata.get('warnings', [])
            )

            # Update cache
            self.cache.put(run_id, data)

            return data

        except Exception as e:
            self.logger.error(f"Failed to load metadata {run_id}: {e}")
            return None

    def load_timeseries(self, run_id: str) -> Optional[pd.DataFrame]:
        """
        Load time-series data from CSV.

        Args:
            run_id: Run identifier

        Returns:
            Pandas DataFrame with time-series data or None
        """
        csv_path = self.runs_path / run_id / "timeseries.csv"

        if not csv_path.exists():
            self.logger.warning(f"Timeseries not found: {run_id}")
            return None

        try:
            df = pd.read_csv(csv_path)
            return df
        except Exception as e:
            self.logger.error(f"Failed to load timeseries {run_id}: {e}")
            return None

    def query_runs(self,
                   controller: Optional[str] = None,
                   scenario: Optional[str] = None,
                   status: Optional[str] = None,
                   date_from: Optional[datetime] = None,
                   date_to: Optional[datetime] = None,
                   min_score: Optional[float] = None,
                   max_score: Optional[float] = None,
                   limit: int = 100,
                   offset: int = 0,
                   order_by: str = 'timestamp',
                   ascending: bool = False) -> List[DashboardData]:
        """
        Query runs with filters.

        Args:
            controller: Filter by controller type
            scenario: Filter by scenario
            status: Filter by run status
            date_from: Filter runs after this date
            date_to: Filter runs before this date
            min_score: Minimum performance score
            max_score: Maximum performance score
            limit: Maximum number of results
            offset: Number of results to skip (pagination)
            order_by: Sort column ('timestamp', 'score', 'settling_time')
            ascending: Sort order (False = descending)

        Returns:
            List of DashboardData objects matching filters
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build query
        query = "SELECT run_id FROM runs WHERE 1=1"
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

        if date_from:
            query += " AND timestamp >= ?"
            params.append(date_from.isoformat())

        if date_to:
            query += " AND timestamp <= ?"
            params.append(date_to.isoformat())

        if min_score is not None:
            query += " AND score >= ?"
            params.append(min_score)

        if max_score is not None:
            query += " AND score <= ?"
            params.append(max_score)

        # Order by
        order_col = order_by if order_by in ['timestamp', 'score', 'settling_time'] else 'timestamp'
        order_dir = "ASC" if ascending else "DESC"
        query += f" ORDER BY {order_col} {order_dir}"

        # Limit and offset
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)
        run_ids = [row[0] for row in cursor.fetchall()]

        conn.close()

        # Load metadata for each run
        results = []
        for run_id in run_ids:
            data = self.load_metadata(run_id)
            if data:
                results.append(data)

        self.logger.info(f"Query returned {len(results)} runs")
        return results

    def start_live_session(self, controller: str, scenario: str = "nominal",
                          config: Optional[Dict[str, Any]] = None) -> str:
        """
        Start a live monitoring session.

        Launches simulate.py in background and tracks metrics file.

        Args:
            controller: Controller type
            scenario: Scenario name
            config: Controller configuration

        Returns:
            session_id for tracking
        """
        session_id = f"live_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session_dir = self.cache_path / session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        metrics_file = session_dir / "metrics.csv"

        # Initialize metrics CSV
        with open(metrics_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'step', 'theta1', 'theta2', 'u', 'error'])

        # Note: simulate.py integration will be added in next phase
        # For now, just create session tracking

        self._live_sessions[session_id] = {
            "controller": controller,
            "scenario": scenario,
            "config": config or {},
            "metrics_file": metrics_file,
            "start_time": datetime.now(),
            "process": None  # Will hold subprocess handle
        }

        self.logger.info(f"Started live session: {session_id}")
        return session_id

    def get_live_metrics(self, session_id: str) -> Optional[pd.DataFrame]:
        """
        Get current live metrics from session.

        Args:
            session_id: Session identifier

        Returns:
            DataFrame with latest metrics or None
        """
        if session_id not in self._live_sessions:
            self.logger.warning(f"Session not found: {session_id}")
            return None

        session = self._live_sessions[session_id]
        metrics_file = session['metrics_file']

        if not metrics_file.exists():
            return None

        try:
            df = pd.read_csv(metrics_file)
            return df
        except Exception as e:
            self.logger.error(f"Failed to read live metrics: {e}")
            return None

    def stop_live_session(self, session_id: str) -> Optional[str]:
        """
        Stop live session and save results.

        Args:
            session_id: Session identifier

        Returns:
            run_id of saved run or None if failed
        """
        if session_id not in self._live_sessions:
            self.logger.warning(f"Session not found: {session_id}")
            return None

        session = self._live_sessions[session_id]

        # Terminate process if running
        if session['process']:
            session['process'].terminate()

        # TODO: Convert metrics to DashboardData and store
        # This will be implemented when simulate.py integration is added

        del self._live_sessions[session_id]
        self.logger.info(f"Stopped live session: {session_id}")

        return None  # Will return run_id after full implementation

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self.cache.get_stats()

    def cleanup_old_runs(self, days: int = 90, dry_run: bool = True) -> List[str]:
        """
        Delete runs older than specified days.

        Args:
            days: Delete runs older than this many days
            dry_run: If True, only return list without deleting

        Returns:
            List of run_ids that were/would be deleted
        """
        cutoff_date = datetime.now() - timedelta(days=days)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT run_id FROM runs
            WHERE timestamp < ?
        """, (cutoff_date.isoformat(),))

        old_runs = [row[0] for row in cursor.fetchall()]
        conn.close()

        if not dry_run:
            for run_id in old_runs:
                run_dir = self.runs_path / run_id
                if run_dir.exists():
                    shutil.rmtree(run_dir)
                    self.logger.info(f"Deleted old run: {run_id}")

            # Remove from index
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM runs WHERE timestamp < ?", (cutoff_date.isoformat(),))
            conn.commit()
            conn.close()

            # Clear from cache
            self.cache.clear()

        self.logger.info(f"Cleanup: {'Would delete' if dry_run else 'Deleted'} {len(old_runs)} runs older than {days} days")
        return old_runs


# Export
__all__ = ['DataManager', 'LRUCache']
