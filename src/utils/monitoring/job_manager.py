#======================================================================================
#================ src/utils/monitoring/job_manager.py ================
#======================================================================================
"""
Background Job Orchestration System for MT-8 Testing.

This module provides a comprehensive job management system for tracking and
controlling long-running background Python processes (PSO optimization, validation
tests, report generation, etc.) launched from the Streamlit web interface.

Key Features:
    - Multi-process orchestration with unique job IDs
    - Real-time progress tracking via JSON file polling
    - Job lifecycle management (launch, monitor, kill, cleanup)
    - Persistent job registry (survives browser refresh)
    - Progress estimation with ETA calculation

Usage:
    >>> from src.utils.monitoring.job_manager import JobManager
    >>>
    >>> manager = JobManager()
    >>>
    >>> # Launch background PSO optimization
    >>> job_id = manager.launch_job(
    ...     job_type="reproducibility_test",
    ...     script_path="scripts/mt8_reproducibility_test.py",
    ...     args={
    ...         "seed": 42,
    ...         "controller": "classical_smc",
    ...         "n_particles": 30,
    ...         "n_iterations": 50
    ...     }
    ... )
    >>>
    >>> # Poll for progress
    >>> job = manager.get_job_progress(job_id)
    >>> print(f"Progress: {job.progress_pct:.1f}% - {job.current_status}")
    >>>
    >>> # List all active jobs
    >>> active = manager.list_active_jobs()
    >>> print(f"{len(active)} jobs running")
    >>>
    >>> # Kill job if needed
    >>> manager.kill_job(job_id)

Integration:
    - Works with Streamlit UI for launching background processes
    - Compatible with all 11 MT-8 scripts (requires --job-id support)
    - Uses .live_state/ directory for persistent storage
    - Supports subprocess.Popen() non-blocking execution

Author: Claude Code (AI-assisted development)
Date: December 2025
"""

import json
import logging
import subprocess
import time
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

import psutil


@dataclass
class BackgroundJob:
    """
    Represents a single background job.

    Attributes:
        job_id: Unique identifier (UUID)
        job_type: Type of job (e.g., "reproducibility_test", "disturbance_validation")
        script_path: Path to Python script being executed
        args: Dictionary of command-line arguments passed to script
        status: Current status ("pending", "running", "completed", "failed", "killed")
        start_time: Job start timestamp (Unix time)
        end_time: Job end timestamp (Unix time, None if still running)
        progress_pct: Progress percentage (0-100)
        current_status: Human-readable status message
        eta_seconds: Estimated time remaining in seconds
        result_path: Path to final result JSON file
        process_id: OS process ID (for killing)
        error_message: Error message if job failed
    """

    job_id: str
    job_type: str
    script_path: str
    args: Dict[str, Any]
    status: str = "pending"  # pending, running, completed, failed, killed
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    progress_pct: float = 0.0
    current_status: str = "Initializing..."
    eta_seconds: Optional[float] = None
    result_path: Optional[str] = None
    process_id: Optional[int] = None
    error_message: Optional[str] = None


class JobManager:
    """
    Orchestrate multiple background Python processes.

    Manages job lifecycle from launch to completion, providing real-time
    progress tracking, process control, and persistent job registry.

    Attributes:
        jobs_registry_path: Path to active jobs JSON file
        jobs_history_path: Path to completed jobs JSON file
        live_state_dir: Root directory for job state files
        max_history_jobs: Maximum number of completed jobs to keep
    """

    def __init__(
        self,
        live_state_dir: str = ".live_state",
        max_history_jobs: int = 100
    ):
        """
        Initialize job manager.

        Args:
            live_state_dir: Directory for job state files
            max_history_jobs: Maximum completed jobs to keep in history
        """
        self.live_state_dir = Path(live_state_dir)
        self.jobs_registry_path = self.live_state_dir / "jobs_registry.json"
        self.jobs_history_path = self.live_state_dir / "jobs_history.json"
        self.max_history_jobs = max_history_jobs

        # Create directory structure
        self.live_state_dir.mkdir(parents=True, exist_ok=True)

        # Initialize empty registry if needed
        if not self.jobs_registry_path.exists():
            self._save_registry({})

        if not self.jobs_history_path.exists():
            self._save_history([])

        logging.info(f"JobManager initialized (state dir: {self.live_state_dir})")

    def launch_job(
        self,
        job_type: str,
        script_path: str,
        args: Dict[str, Any]
    ) -> str:
        """
        Launch background Python process and register job.

        Args:
            job_type: Type of job (e.g., "reproducibility_test", "disturbance_validation")
            script_path: Path to Python script to execute
            args: Dictionary of arguments to pass to script

        Returns:
            Job ID (UUID string)

        Example:
            >>> job_id = manager.launch_job(
            ...     job_type="reproducibility_test",
            ...     script_path="scripts/mt8_reproducibility_test.py",
            ...     args={"seed": 42, "controller": "classical_smc"}
            ... )
        """
        # Generate unique job ID
        job_id = str(uuid.uuid4())

        # Create job directory
        job_dir = self.live_state_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        # Build command
        cmd = self._build_command(script_path, job_id, args)

        # Create log file for stdout/stderr
        log_file = job_dir / "output.log"
        log_f = open(log_file, 'w')

        # Launch subprocess (non-blocking)
        try:
            process = subprocess.Popen(
                cmd,
                cwd=Path.cwd(),
                stdout=log_f,
                stderr=subprocess.STDOUT,  # Merge stderr into stdout
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if hasattr(subprocess, 'CREATE_NEW_PROCESS_GROUP') else 0
            )

            # Create job object
            job = BackgroundJob(
                job_id=job_id,
                job_type=job_type,
                script_path=str(script_path),
                args=args,
                status="running",
                start_time=time.time(),
                process_id=process.pid
            )

            # Save job to registry
            self._add_job_to_registry(job)

            # Save job metadata
            self._save_job_metadata(job_id, job)

            logging.info(f"Launched job {job_id[:8]} (type: {job_type}, PID: {process.pid})")
            return job_id

        except Exception as e:
            logging.error(f"Failed to launch job: {e}")
            raise

    def get_job_progress(self, job_id: str) -> Optional[BackgroundJob]:
        """
        Get current progress for a job.

        Polls progress.json file written by background script for latest status.

        Args:
            job_id: Job identifier

        Returns:
            BackgroundJob object with updated progress, or None if job not found
        """
        # Load job from registry
        job = self._load_job_from_registry(job_id)

        if not job:
            # Check history
            job = self._load_job_from_history(job_id)

        if not job:
            return None

        # If job is still running, poll progress file
        if job.status == "running":
            progress_file = self.live_state_dir / job_id / "progress.json"

            if progress_file.exists():
                try:
                    with open(progress_file, 'r') as f:
                        progress_data = json.load(f)

                    # Update job with latest progress
                    job.progress_pct = progress_data.get("progress_pct", job.progress_pct)
                    job.current_status = progress_data.get("status_message", job.current_status)
                    job.eta_seconds = progress_data.get("eta_seconds", job.eta_seconds)

                except json.JSONDecodeError:
                    logging.warning(f"Failed to parse progress.json for job {job_id[:8]}")

            # Check if job completed
            result_file = self.live_state_dir / job_id / "result.json"
            if result_file.exists():
                job.status = "completed"
                job.end_time = time.time()
                job.progress_pct = 100.0
                job.result_path = str(result_file)

                # Move to history
                self._move_job_to_history(job)

            # Check if process still alive
            if job.process_id and not self._is_process_alive(job.process_id):
                if job.status == "running":
                    # Process died without completing
                    job.status = "failed"
                    job.end_time = time.time()
                    job.error_message = "Process terminated unexpectedly"
                    self._move_job_to_history(job)

        return job

    def list_active_jobs(self) -> List[BackgroundJob]:
        """
        List all active (running/pending) jobs.

        Returns:
            List of BackgroundJob objects with status "running" or "pending"
        """
        registry = self._load_registry()
        jobs = []

        for job_id, job_data in registry.items():
            job = BackgroundJob(**job_data)

            # Update progress
            updated_job = self.get_job_progress(job_id)
            if updated_job and updated_job.status in ["running", "pending"]:
                jobs.append(updated_job)

        return jobs

    def list_completed_jobs(self, limit: int = 20) -> List[BackgroundJob]:
        """
        List recently completed jobs.

        Args:
            limit: Maximum number of jobs to return

        Returns:
            List of completed BackgroundJob objects (most recent first)
        """
        history = self._load_history()
        return [BackgroundJob(**job_data) for job_data in history[:limit]]

    def kill_job(self, job_id: str) -> bool:
        """
        Terminate a running job.

        Args:
            job_id: Job identifier

        Returns:
            True if job was killed successfully, False otherwise
        """
        job = self._load_job_from_registry(job_id)

        if not job or not job.process_id:
            logging.warning(f"Cannot kill job {job_id[:8]}: not found or no PID")
            return False

        try:
            # Kill process
            if self._is_process_alive(job.process_id):
                process = psutil.Process(job.process_id)
                process.terminate()

                # Wait up to 5 seconds for graceful shutdown
                try:
                    process.wait(timeout=5)
                except psutil.TimeoutExpired:
                    # Force kill
                    process.kill()

                logging.info(f"Killed job {job_id[:8]} (PID: {job.process_id})")

            # Update job status
            job.status = "killed"
            job.end_time = time.time()

            # Move to history
            self._move_job_to_history(job)

            return True

        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logging.error(f"Failed to kill job {job_id[:8]}: {e}")
            return False

    def cleanup_old_jobs(self, max_age_hours: int = 24) -> int:
        """
        Clean up completed jobs older than specified age.

        Args:
            max_age_hours: Maximum age in hours for completed jobs

        Returns:
            Number of jobs cleaned up
        """
        history = self._load_history()
        cutoff_time = time.time() - (max_age_hours * 3600)

        cleaned_count = 0
        new_history = []

        for job_data in history:
            job = BackgroundJob(**job_data)

            if job.end_time and job.end_time < cutoff_time:
                # Delete job directory
                job_dir = self.live_state_dir / job.job_id
                if job_dir.exists():
                    import shutil
                    shutil.rmtree(job_dir)
                    cleaned_count += 1
            else:
                new_history.append(job_data)

        self._save_history(new_history)
        logging.info(f"Cleaned up {cleaned_count} old jobs")

        return cleaned_count

    # ─────────────────────────── Private Helper Methods ───────────────────────────

    def _build_command(self, script_path: str, job_id: str, args: Dict[str, Any]) -> List[str]:
        """Build command-line arguments for subprocess."""
        cmd = ["python", str(script_path)]

        # Always add job_id
        cmd.extend(["--job-id", job_id])

        # Add other arguments
        for key, value in args.items():
            # Convert underscores to hyphens for CLI args
            arg_name = key.replace("_", "-")

            if isinstance(value, bool):
                if value:
                    cmd.append(f"--{arg_name}")
            elif isinstance(value, list):
                # Serialize lists as comma-separated strings
                cmd.extend([f"--{arg_name}", ",".join(map(str, value))])
            else:
                cmd.extend([f"--{arg_name}", str(value)])

        return cmd

    def _save_job_metadata(self, job_id: str, job: BackgroundJob):
        """Save job metadata to job directory."""
        metadata_file = self.live_state_dir / job_id / "metadata.json"

        with open(metadata_file, 'w') as f:
            json.dump(asdict(job), f, indent=2)

    def _load_registry(self) -> Dict[str, Dict]:
        """Load active jobs registry."""
        if not self.jobs_registry_path.exists():
            return {}

        with open(self.jobs_registry_path, 'r') as f:
            return json.load(f)

    def _save_registry(self, registry: Dict[str, Dict]):
        """Save active jobs registry."""
        with open(self.jobs_registry_path, 'w') as f:
            json.dump(registry, f, indent=2)

    def _load_history(self) -> List[Dict]:
        """Load completed jobs history."""
        if not self.jobs_history_path.exists():
            return []

        with open(self.jobs_history_path, 'r') as f:
            return json.load(f)

    def _save_history(self, history: List[Dict]):
        """Save completed jobs history."""
        # Keep only last N jobs
        history = history[:self.max_history_jobs]

        with open(self.jobs_history_path, 'w') as f:
            json.dump(history, f, indent=2)

    def _add_job_to_registry(self, job: BackgroundJob):
        """Add job to active registry."""
        registry = self._load_registry()
        registry[job.job_id] = asdict(job)
        self._save_registry(registry)

    def _remove_job_from_registry(self, job_id: str):
        """Remove job from active registry."""
        registry = self._load_registry()
        if job_id in registry:
            del registry[job_id]
            self._save_registry(registry)

    def _move_job_to_history(self, job: BackgroundJob):
        """Move job from registry to history."""
        # Remove from registry
        self._remove_job_from_registry(job.job_id)

        # Add to history (prepend so newest first)
        history = self._load_history()
        history.insert(0, asdict(job))
        self._save_history(history)

    def _load_job_from_registry(self, job_id: str) -> Optional[BackgroundJob]:
        """Load job from active registry."""
        registry = self._load_registry()

        if job_id in registry:
            return BackgroundJob(**registry[job_id])

        return None

    def _load_job_from_history(self, job_id: str) -> Optional[BackgroundJob]:
        """Load job from history."""
        history = self._load_history()

        for job_data in history:
            if job_data['job_id'] == job_id:
                return BackgroundJob(**job_data)

        return None

    def _is_process_alive(self, pid: int) -> bool:
        """Check if process with given PID is still running."""
        try:
            process = psutil.Process(pid)
            return process.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
