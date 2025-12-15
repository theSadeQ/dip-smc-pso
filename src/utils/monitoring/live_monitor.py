#======================================================================================\
#================== src/utils/monitoring/live_monitor.py ==================\
#======================================================================================\

"""
Live monitoring system for tracking simulation progress in real-time.

This module provides real-time monitoring capabilities for long-running simulations,
allowing users to track progress, view intermediate results, and abort if needed.

Features:
- Background simulation execution
- Real-time progress tracking via shared state file
- Abort/cancel functionality
- Intermediate metrics collection
- Streamlit integration with auto-refresh

Architecture:
    Main Process (Streamlit)
        |
        | start_live_run()
        v
    Background Process (simulate.py --save-results)
        |
        | writes to
        v
    State File (.live_state.json)
        ^
        | polls every 1s
        |
    Streamlit UI (live_monitor_ui.py)

Author: Claude Code (AI)
Date: 2025-12-15
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, List
import signal


class LiveRunStatus(Enum):
    """Status of a live monitoring session."""
    STARTING = "starting"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"
    ABORTED = "aborted"


@dataclass
class LiveMetrics:
    """
    Real-time metrics snapshot during simulation.

    Attributes:
        timestamp: Current simulation time (seconds)
        progress_pct: Completion percentage (0-100)
        elapsed_s: Wall-clock time elapsed (seconds)
        samples_completed: Number of timesteps completed
        samples_total: Total timesteps to complete
        current_score: Current performance score (0-100)
        current_error: Current tracking error
        current_control: Current control output
    """
    timestamp: float = 0.0
    progress_pct: float = 0.0
    elapsed_s: float = 0.0
    samples_completed: int = 0
    samples_total: int = 0
    current_score: float = 0.0
    current_error: float = 0.0
    current_control: float = 0.0


@dataclass
class LiveRunState:
    """
    Complete state of a live monitoring session.

    This state is persisted to a JSON file and polled by the UI
    for real-time updates.

    Attributes:
        session_id: Unique identifier for this session
        status: Current run status
        controller: Controller type being tested
        scenario: Scenario being simulated
        start_time: Wall-clock start time (epoch)
        end_time: Wall-clock end time (epoch, None if running)
        duration_s: Simulation duration (config parameter)
        metrics: Current metrics snapshot
        errors: List of error messages
        warnings: List of warning messages
        pid: Process ID of background simulation
    """
    session_id: str
    status: LiveRunStatus
    controller: str
    scenario: str
    start_time: float
    end_time: Optional[float] = None
    duration_s: float = 0.0
    metrics: LiveMetrics = field(default_factory=LiveMetrics)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    pid: Optional[int] = None
    run_id: Optional[str] = None  # Assigned when complete


class LiveMonitor:
    """
    Manager for live simulation monitoring sessions.

    This class handles starting simulations in background processes,
    tracking their progress via shared state files, and providing
    abort functionality.

    Usage:
        >>> monitor = LiveMonitor()
        >>> session_id = monitor.start_live_run(
        ...     controller='adaptive_smc',
        ...     scenario='nominal',
        ...     duration=60.0
        ... )
        >>>
        >>> # Poll for updates
        >>> while monitor.is_running(session_id):
        ...     state = monitor.get_state(session_id)
        ...     print(f"Progress: {state.metrics.progress_pct:.1f}%")
        ...     time.sleep(1)
        >>>
        >>> # Abort if needed
        >>> monitor.abort_run(session_id)
    """

    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize LiveMonitor.

        Args:
            base_path: Base directory for monitoring data
                      (defaults to monitoring_data/)
        """
        self.base_path = Path(base_path) if base_path else Path("monitoring_data")
        self.live_path = self.base_path / "live"
        self.live_path.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger("LiveMonitor")
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configure logging."""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _get_state_path(self, session_id: str) -> Path:
        """Get path to state file for a session."""
        return self.live_path / f"{session_id}.json"

    def _generate_session_id(self, controller: str, scenario: str) -> str:
        """Generate unique session ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"live_{timestamp}_{controller}_{scenario}"

    def start_live_run(self,
                      controller: str,
                      scenario: str = "nominal",
                      duration: float = 10.0,
                      dt: float = 0.01,
                      config_path: str = "config.yaml") -> str:
        """
        Start a new live monitoring session.

        Launches simulate.py in a background process and creates a state
        file for tracking progress.

        Args:
            controller: Controller type to test
            scenario: Scenario to simulate
            duration: Simulation duration (seconds)
            dt: Time step (seconds)
            config_path: Path to configuration file

        Returns:
            session_id: Unique identifier for this session

        Example:
            >>> monitor = LiveMonitor()
            >>> session_id = monitor.start_live_run(
            ...     controller='adaptive_smc',
            ...     duration=30.0
            ... )
            >>> print(f"Started session: {session_id}")
        """
        session_id = self._generate_session_id(controller, scenario)

        # Initialize state
        state = LiveRunState(
            session_id=session_id,
            status=LiveRunStatus.STARTING,
            controller=controller,
            scenario=scenario,
            start_time=time.time(),
            duration_s=duration,
            metrics=LiveMetrics(samples_total=int(duration / dt))
        )

        # Save initial state
        self._save_state(state)

        # Build command
        cmd = [
            "python", "simulate.py",
            "--controller", controller,
            "--duration", str(duration),
            "--dt", str(dt),
            "--save-results",
            "--config", config_path,
            "--live-session", session_id  # Special flag for live monitoring
        ]

        try:
            # Start background process
            # On Windows, use CREATE_NEW_PROCESS_GROUP to allow clean termination
            if os.name == 'nt':
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            else:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    preexec_fn=os.setsid
                )

            # Update state with PID
            state.pid = process.pid
            state.status = LiveRunStatus.RUNNING
            self._save_state(state)

            self.logger.info(f"Started live session: {session_id} (PID: {process.pid})")
            return session_id

        except Exception as e:
            state.status = LiveRunStatus.FAILED
            state.errors.append(f"Failed to start: {e}")
            self._save_state(state)
            self.logger.error(f"Failed to start session {session_id}: {e}")
            raise

    def get_state(self, session_id: str) -> Optional[LiveRunState]:
        """
        Get current state of a live session.

        Args:
            session_id: Session identifier

        Returns:
            LiveRunState object, or None if not found
        """
        state_path = self._get_state_path(session_id)

        if not state_path.exists():
            return None

        try:
            with open(state_path, 'r') as f:
                data = json.load(f)

            # Reconstruct state object
            state = LiveRunState(
                session_id=data['session_id'],
                status=LiveRunStatus(data['status']),
                controller=data['controller'],
                scenario=data['scenario'],
                start_time=data['start_time'],
                end_time=data.get('end_time'),
                duration_s=data['duration_s'],
                metrics=LiveMetrics(**data.get('metrics', {})),
                errors=data.get('errors', []),
                warnings=data.get('warnings', []),
                pid=data.get('pid'),
                run_id=data.get('run_id')
            )

            return state

        except Exception as e:
            self.logger.error(f"Failed to load state for {session_id}: {e}")
            return None

    def _save_state(self, state: LiveRunState) -> None:
        """Save state to JSON file."""
        state_path = self._get_state_path(state.session_id)

        # Convert to dict, handling enums
        data = asdict(state)
        data['status'] = state.status.value

        with open(state_path, 'w') as f:
            json.dump(data, f, indent=2)

    def update_metrics(self, session_id: str, metrics: LiveMetrics) -> None:
        """
        Update metrics for a running session.

        This is called periodically by the simulation process to report progress.

        Args:
            session_id: Session identifier
            metrics: Updated metrics snapshot
        """
        state = self.get_state(session_id)
        if not state:
            self.logger.warning(f"Cannot update metrics: session {session_id} not found")
            return

        state.metrics = metrics
        self._save_state(state)

    def mark_complete(self, session_id: str, run_id: str) -> None:
        """
        Mark a session as complete.

        Args:
            session_id: Session identifier
            run_id: Final run ID from DataManager
        """
        state = self.get_state(session_id)
        if not state:
            return

        state.status = LiveRunStatus.COMPLETE
        state.end_time = time.time()
        state.run_id = run_id
        state.metrics.progress_pct = 100.0
        self._save_state(state)

        self.logger.info(f"Session {session_id} completed: {run_id}")

    def mark_failed(self, session_id: str, error: str) -> None:
        """
        Mark a session as failed.

        Args:
            session_id: Session identifier
            error: Error message
        """
        state = self.get_state(session_id)
        if not state:
            return

        state.status = LiveRunStatus.FAILED
        state.end_time = time.time()
        state.errors.append(error)
        self._save_state(state)

        self.logger.error(f"Session {session_id} failed: {error}")

    def abort_run(self, session_id: str) -> bool:
        """
        Abort a running session.

        Sends SIGTERM (or Windows equivalent) to the background process
        and marks the session as aborted.

        Args:
            session_id: Session identifier

        Returns:
            True if successfully aborted, False otherwise
        """
        state = self.get_state(session_id)
        if not state or not state.pid:
            self.logger.warning(f"Cannot abort: session {session_id} not found or no PID")
            return False

        try:
            if os.name == 'nt':
                # Windows: send CTRL_BREAK_EVENT
                os.kill(state.pid, signal.CTRL_BREAK_EVENT)
            else:
                # Unix: send SIGTERM
                os.killpg(os.getpgid(state.pid), signal.SIGTERM)

            state.status = LiveRunStatus.ABORTED
            state.end_time = time.time()
            self._save_state(state)

            self.logger.info(f"Aborted session: {session_id}")
            return True

        except ProcessLookupError:
            # Process already terminated
            state.status = LiveRunStatus.ABORTED
            state.end_time = time.time()
            self._save_state(state)
            return True

        except Exception as e:
            self.logger.error(f"Failed to abort session {session_id}: {e}")
            return False

    def is_running(self, session_id: str) -> bool:
        """
        Check if a session is currently running.

        Args:
            session_id: Session identifier

        Returns:
            True if running, False otherwise
        """
        state = self.get_state(session_id)
        return state is not None and state.status in [LiveRunStatus.STARTING, LiveRunStatus.RUNNING]

    def cleanup_old_sessions(self, max_age_hours: int = 24) -> int:
        """
        Clean up old session state files.

        Args:
            max_age_hours: Remove sessions older than this many hours

        Returns:
            Number of sessions cleaned up
        """
        count = 0
        cutoff_time = time.time() - (max_age_hours * 3600)

        for state_file in self.live_path.glob("live_*.json"):
            try:
                state = self.get_state(state_file.stem)
                if state and state.end_time and state.end_time < cutoff_time:
                    state_file.unlink()
                    count += 1
            except Exception as e:
                self.logger.warning(f"Error cleaning up {state_file}: {e}")

        if count > 0:
            self.logger.info(f"Cleaned up {count} old sessions")

        return count

    def list_active_sessions(self) -> List[LiveRunState]:
        """
        List all active (running or starting) sessions.

        Returns:
            List of LiveRunState objects for active sessions
        """
        active = []

        for state_file in self.live_path.glob("live_*.json"):
            state = self.get_state(state_file.stem)
            if state and state.status in [LiveRunStatus.STARTING, LiveRunStatus.RUNNING]:
                active.append(state)

        return active


# Standalone test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    monitor = LiveMonitor()

    print("[INFO] Starting live monitoring test...")
    print()

    # Start a test session
    session_id = monitor.start_live_run(
        controller="adaptive_smc",
        duration=5.0
    )

    print(f"[OK] Started session: {session_id}")
    print()

    # Poll for updates
    while monitor.is_running(session_id):
        state = monitor.get_state(session_id)
        if state:
            print(f"Progress: {state.metrics.progress_pct:.1f}% | "
                  f"Elapsed: {state.metrics.elapsed_s:.1f}s | "
                  f"Status: {state.status.value}")
        time.sleep(1)

    # Check final state
    final_state = monitor.get_state(session_id)
    print()
    print(f"[OK] Session complete: {final_state.status.value}")
    if final_state.run_id:
        print(f"[OK] Run ID: {final_state.run_id}")
