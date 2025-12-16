#======================================================================================
#============ src/utils/monitoring/progress_tracker.py ============
#======================================================================================
"""
Progress Tracking Utilities for Background Jobs.

Provides simple utilities for MT-8 scripts to report progress updates
that can be polled by the Streamlit UI.

Usage in MT-8 scripts:
    >>> from src.utils.monitoring.progress_tracker import ProgressTracker
    >>>
    >>> # Initialize at start of script
    >>> tracker = ProgressTracker(job_id)
    >>>
    >>> # Update progress during PSO loop
    >>> for iteration in range(n_iterations):
    ...     for particle_idx in range(n_particles):
    ...         # ... PSO logic ...
    ...         tracker.update(
    ...             progress_pct=(iteration * n_particles + particle_idx) / (n_iterations * n_particles) * 100,
    ...             status_message=f"Iteration {iteration+1}/{n_iterations} | Particle {particle_idx+1}/{n_particles}",
    ...             eta_seconds=estimated_time_remaining
    ...         )
    >>>
    >>> # Mark as complete
    >>> tracker.complete(result_path="optimization_results/result.json")

Author: Claude Code (AI-assisted development)
Date: December 2025
"""

import json
import logging
import time
from pathlib import Path
from typing import Optional


class ProgressTracker:
    """
    Track progress for a background job.

    Writes progress updates to JSON file that can be polled by UI.
    """

    def __init__(self, job_id: Optional[str] = None, live_state_dir: str = ".live_state"):
        """
        Initialize progress tracker.

        Args:
            job_id: Unique job identifier (None if running without job tracking)
            live_state_dir: Root directory for job state files
        """
        self.job_id = job_id
        self.live_state_dir = Path(live_state_dir)
        self.enabled = job_id is not None

        if self.enabled:
            # Create job directory
            self.job_dir = self.live_state_dir / job_id
            self.job_dir.mkdir(parents=True, exist_ok=True)

            self.progress_file = self.job_dir / "progress.json"
            self.result_file = self.job_dir / "result.json"

            # Initialize progress file
            self.update(0.0, "Starting...")

            logging.info(f"Progress tracker initialized for job {job_id[:8]}")

    def update(
        self,
        progress_pct: float,
        status_message: str,
        eta_seconds: Optional[float] = None
    ):
        """
        Update progress for job.

        Args:
            progress_pct: Progress percentage (0-100)
            status_message: Human-readable status message
            eta_seconds: Estimated time remaining in seconds
        """
        if not self.enabled:
            return

        progress_data = {
            "job_id": self.job_id,
            "progress_pct": min(100.0, max(0.0, progress_pct)),
            "status_message": status_message,
            "eta_seconds": eta_seconds,
            "timestamp": time.time()
        }

        # Atomic write (write to temp file, then rename)
        temp_file = self.progress_file.with_suffix('.tmp')

        try:
            with open(temp_file, 'w') as f:
                json.dump(progress_data, f, indent=2)

            # Atomic rename
            temp_file.replace(self.progress_file)

        except Exception as e:
            logging.warning(f"Failed to update progress: {e}")

    def complete(self, result_path: Optional[str] = None, result_data: Optional[dict] = None):
        """
        Mark job as complete.

        Args:
            result_path: Path to result file (optional)
            result_data: Result data dictionary (optional, will be written to result.json)
        """
        if not self.enabled:
            return

        # Update progress to 100%
        self.update(100.0, "Completed")

        # Write result file
        if result_data:
            with open(self.result_file, 'w') as f:
                json.dump(result_data, f, indent=2)

        logging.info(f"Job {self.job_id[:8]} marked as complete")

    def fail(self, error_message: str):
        """
        Mark job as failed.

        Args:
            error_message: Error description
        """
        if not self.enabled:
            return

        self.update(0.0, f"Failed: {error_message}")

        # Write error to result file
        error_data = {
            "status": "failed",
            "error_message": error_message,
            "timestamp": time.time()
        }

        with open(self.result_file, 'w') as f:
            json.dump(error_data, f, indent=2)

        logging.error(f"Job {self.job_id[:8]} marked as failed: {error_message}")


class ProgressEstimator:
    """
    Estimate ETA for long-running operations.

    Tracks time per operation and estimates remaining time.
    """

    def __init__(self, total_operations: int, window_size: int = 10):
        """
        Initialize progress estimator.

        Args:
            total_operations: Total number of operations to complete
            window_size: Number of recent operations to average for ETA
        """
        self.total_operations = total_operations
        self.window_size = window_size
        self.operation_times = []
        self.completed_operations = 0
        self.start_time = time.time()

    def record_operation(self, operation_time: float):
        """
        Record time for a completed operation.

        Args:
            operation_time: Time taken for operation in seconds
        """
        self.operation_times.append(operation_time)
        self.completed_operations += 1

        # Keep only last N operations
        if len(self.operation_times) > self.window_size:
            self.operation_times.pop(0)

    def get_eta_seconds(self) -> Optional[float]:
        """
        Estimate remaining time in seconds.

        Returns:
            Estimated seconds remaining, or None if not enough data
        """
        if not self.operation_times:
            return None

        # Average time per operation
        avg_time = sum(self.operation_times) / len(self.operation_times)

        # Remaining operations
        remaining = self.total_operations - self.completed_operations

        return avg_time * remaining

    def get_progress_pct(self) -> float:
        """
        Get current progress percentage.

        Returns:
            Progress percentage (0-100)
        """
        if self.total_operations == 0:
            return 100.0

        return (self.completed_operations / self.total_operations) * 100.0
