#======================================================================================
#================= src/utils/monitoring/alerting.py =================
#======================================================================================
"""
Alerting and threshold monitoring system for production deployments.

This module provides real-time alerting for performance degradation, threshold
violations, and anomalous behavior in simulation runs.

Features:
    - Configurable threshold alerts (score, settling time, overshoot, etc.)
    - Performance degradation detection (comparing recent vs historical)
    - Alert history logging and persistence
    - Multi-channel notifications (log, file, future: email/Slack)
    - Alert severity levels (INFO, WARNING, CRITICAL)

Usage:
    >>> from src.utils.monitoring.alerting import AlertingSystem, AlertThresholds
    >>>
    >>> # Configure thresholds
    >>> thresholds = AlertThresholds(
    ...     min_score=50.0,
    ...     max_settling_time=5.0,
    ...     max_overshoot=20.0
    ... )
    >>>
    >>> # Initialize alerting system
    >>> alerting = AlertingSystem(thresholds=thresholds)
    >>>
    >>> # Check run for violations
    >>> alerts = alerting.check_run(run_id="2025-12-15_211320_adaptive_smc_nominal")
    >>> for alert in alerts:
    ...     print(f"{alert.severity}: {alert.message}")

Integration:
    - Works with DataManager for run data
    - Logs alerts to monitoring_data/logs/alerts.log
    - Can be integrated with email/Slack via callbacks

Author: Claude Code (AI-assisted development)
Date: December 2025
"""

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional, Callable

from src.utils.monitoring.data_manager import DataManager


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


@dataclass
class AlertThresholds:
    """Configurable alert thresholds for monitoring."""

    # Performance thresholds
    min_score: float = 40.0  # Minimum acceptable performance score
    max_settling_time: float = 10.0  # Maximum settling time (seconds)
    max_overshoot: float = 30.0  # Maximum overshoot (%)
    max_steady_state_error: float = 0.1  # Maximum steady-state error
    max_energy: float = 1000.0  # Maximum energy consumption (J)
    max_chattering: float = 50.0  # Maximum chattering amplitude

    # Degradation thresholds
    degradation_window: int = 10  # Number of recent runs to compare
    degradation_threshold: float = 0.2  # 20% degradation triggers alert


@dataclass
class Alert:
    """Single alert instance."""

    timestamp: float
    severity: AlertSeverity
    run_id: str
    controller: str
    metric: str
    value: float
    threshold: float
    message: str

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'timestamp': self.timestamp,
            'severity': self.severity.value,
            'run_id': self.run_id,
            'controller': self.controller,
            'metric': self.metric,
            'value': self.value,
            'threshold': self.threshold,
            'message': self.message
        }


class AlertingSystem:
    """
    Production alerting system for monitoring simulation runs.

    Monitors runs for threshold violations, performance degradation,
    and anomalous behavior. Logs alerts and optionally triggers callbacks.

    Attributes:
        thresholds: AlertThresholds configuration
        data_manager: DataManager instance for querying runs
        alert_log_path: Path to alert log file
        callbacks: List of callback functions to trigger on alerts
    """

    def __init__(
        self,
        thresholds: Optional[AlertThresholds] = None,
        data_manager: Optional[DataManager] = None,
        alert_log_dir: Path = Path("monitoring_data/logs")
    ):
        """
        Initialize alerting system.

        Args:
            thresholds: AlertThresholds configuration (uses defaults if None)
            data_manager: Optional DataManager instance
            alert_log_dir: Directory for alert logs
        """
        self.thresholds = thresholds or AlertThresholds()
        self.data_manager = data_manager or DataManager()

        # Setup alert logging
        self.alert_log_dir = Path(alert_log_dir)
        self.alert_log_dir.mkdir(parents=True, exist_ok=True)
        self.alert_log_path = self.alert_log_dir / "alerts.log"

        # Callback functions (for email, Slack, etc.)
        self.callbacks: List[Callable[[Alert], None]] = []

        logging.info(f"AlertingSystem initialized with log: {self.alert_log_path}")

    def add_callback(self, callback: Callable[[Alert], None]) -> None:
        """
        Add callback function to be triggered on alerts.

        Args:
            callback: Function that takes an Alert and performs an action
                     (e.g., send email, post to Slack)
        """
        self.callbacks.append(callback)
        logging.info(f"Added alert callback: {callback.__name__}")

    def check_run(self, run_id: str) -> List[Alert]:
        """
        Check a simulation run for threshold violations.

        Args:
            run_id: Run identifier to check

        Returns:
            List of Alert objects for any violations found
        """
        # Load run data
        run_data = self.data_manager.load_metadata(run_id)

        if not run_data or not run_data.summary:
            logging.warning(f"No data found for run {run_id}")
            return []

        alerts = []
        summary = run_data.summary

        # Check score threshold
        score = summary.get_score()
        if score < self.thresholds.min_score:
            alert = Alert(
                timestamp=datetime.now().timestamp(),
                severity=AlertSeverity.WARNING if score >= self.thresholds.min_score * 0.8 else AlertSeverity.CRITICAL,
                run_id=run_id,
                controller=run_data.controller,
                metric='score',
                value=score,
                threshold=self.thresholds.min_score,
                message=f"Performance score {score:.2f} below threshold {self.thresholds.min_score:.2f}"
            )
            alerts.append(alert)

        # Check settling time
        if summary.settling_time_s is not None and summary.settling_time_s > self.thresholds.max_settling_time:
            alert = Alert(
                timestamp=datetime.now().timestamp(),
                severity=AlertSeverity.WARNING,
                run_id=run_id,
                controller=run_data.controller,
                metric='settling_time',
                value=summary.settling_time_s,
                threshold=self.thresholds.max_settling_time,
                message=f"Settling time {summary.settling_time_s:.3f}s exceeds threshold {self.thresholds.max_settling_time:.3f}s"
            )
            alerts.append(alert)

        # Check overshoot
        if summary.overshoot_pct is not None and summary.overshoot_pct > self.thresholds.max_overshoot:
            alert = Alert(
                timestamp=datetime.now().timestamp(),
                severity=AlertSeverity.WARNING,
                run_id=run_id,
                controller=run_data.controller,
                metric='overshoot',
                value=summary.overshoot_pct,
                threshold=self.thresholds.max_overshoot,
                message=f"Overshoot {summary.overshoot_pct:.2f}% exceeds threshold {self.thresholds.max_overshoot:.2f}%"
            )
            alerts.append(alert)

        # Check steady-state error
        if summary.steady_state_error is not None and summary.steady_state_error > self.thresholds.max_steady_state_error:
            alert = Alert(
                timestamp=datetime.now().timestamp(),
                severity=AlertSeverity.WARNING,
                run_id=run_id,
                controller=run_data.controller,
                metric='steady_state_error',
                value=summary.steady_state_error,
                threshold=self.thresholds.max_steady_state_error,
                message=f"Steady-state error {summary.steady_state_error:.4f} exceeds threshold {self.thresholds.max_steady_state_error:.4f}"
            )
            alerts.append(alert)

        # Check energy
        if summary.energy_j is not None and summary.energy_j > self.thresholds.max_energy:
            alert = Alert(
                timestamp=datetime.now().timestamp(),
                severity=AlertSeverity.INFO,
                run_id=run_id,
                controller=run_data.controller,
                metric='energy',
                value=summary.energy_j,
                threshold=self.thresholds.max_energy,
                message=f"Energy consumption {summary.energy_j:.2f}J exceeds threshold {self.thresholds.max_energy:.2f}J"
            )
            alerts.append(alert)

        # Check chattering
        if summary.chattering_amplitude is not None and summary.chattering_amplitude > self.thresholds.max_chattering:
            alert = Alert(
                timestamp=datetime.now().timestamp(),
                severity=AlertSeverity.WARNING,
                run_id=run_id,
                controller=run_data.controller,
                metric='chattering',
                value=summary.chattering_amplitude,
                threshold=self.thresholds.max_chattering,
                message=f"Chattering amplitude {summary.chattering_amplitude:.2f} exceeds threshold {self.thresholds.max_chattering:.2f}"
            )
            alerts.append(alert)

        # Log and trigger callbacks for any alerts
        for alert in alerts:
            self._log_alert(alert)
            self._trigger_callbacks(alert)

        return alerts

    def check_degradation(self, controller: str, scenario: Optional[str] = None) -> Optional[Alert]:
        """
        Check for performance degradation by comparing recent runs to historical average.

        Args:
            controller: Controller name to check
            scenario: Optional scenario filter

        Returns:
            Alert if degradation detected, None otherwise
        """
        # Query recent runs
        recent_runs = self.data_manager.query_runs(
            controller=controller,
            scenario=scenario,
            limit=self.thresholds.degradation_window
        )

        if len(recent_runs) < 3:
            logging.info(f"Not enough recent runs for degradation check ({len(recent_runs)} < 3)")
            return None

        # Query historical runs (excluding recent)
        all_runs = self.data_manager.query_runs(
            controller=controller,
            scenario=scenario,
            limit=100
        )

        if len(all_runs) <= len(recent_runs):
            logging.info("Not enough historical data for degradation comparison")
            return None

        historical_runs = all_runs[len(recent_runs):]

        # Compute average scores
        recent_scores = [r.summary.get_score() for r in recent_runs if r.summary]
        historical_scores = [r.summary.get_score() for r in historical_runs if r.summary]

        if not recent_scores or not historical_scores:
            return None

        import numpy as np
        recent_avg = float(np.mean(recent_scores))
        historical_avg = float(np.mean(historical_scores))

        # Check for degradation
        if historical_avg > 0:
            degradation = (historical_avg - recent_avg) / historical_avg

            if degradation > self.thresholds.degradation_threshold:
                alert = Alert(
                    timestamp=datetime.now().timestamp(),
                    severity=AlertSeverity.CRITICAL,
                    run_id=f"degradation_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    controller=controller,
                    metric='degradation',
                    value=degradation * 100,  # As percentage
                    threshold=self.thresholds.degradation_threshold * 100,
                    message=f"Performance degradation detected: {degradation*100:.1f}% drop " +
                           f"(recent avg: {recent_avg:.2f} vs historical avg: {historical_avg:.2f})"
                )

                self._log_alert(alert)
                self._trigger_callbacks(alert)
                return alert

        return None

    def get_recent_alerts(self, limit: int = 50) -> List[Alert]:
        """
        Get recent alerts from log file.

        Args:
            limit: Maximum number of alerts to return

        Returns:
            List of Alert objects (most recent first)
        """
        if not self.alert_log_path.exists():
            return []

        alerts = []

        with open(self.alert_log_path, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    alert = Alert(
                        timestamp=data['timestamp'],
                        severity=AlertSeverity(data['severity']),
                        run_id=data['run_id'],
                        controller=data['controller'],
                        metric=data['metric'],
                        value=data['value'],
                        threshold=data['threshold'],
                        message=data['message']
                    )
                    alerts.append(alert)
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    logging.warning(f"Failed to parse alert line: {e}")

        # Return most recent first
        alerts.reverse()
        return alerts[:limit]

    def _log_alert(self, alert: Alert) -> None:
        """Log alert to file and Python logger."""
        # Log to Python logger
        log_msg = f"[{alert.severity.value}] {alert.controller} - {alert.message}"

        if alert.severity == AlertSeverity.CRITICAL:
            logging.error(log_msg)
        elif alert.severity == AlertSeverity.WARNING:
            logging.warning(log_msg)
        else:
            logging.info(log_msg)

        # Append to alert log file (JSON lines format)
        with open(self.alert_log_path, 'a') as f:
            f.write(json.dumps(alert.to_dict()) + '\n')

    def _trigger_callbacks(self, alert: Alert) -> None:
        """Trigger all registered callbacks with the alert."""
        for callback in self.callbacks:
            try:
                callback(alert)
            except Exception as e:
                logging.error(f"Alert callback {callback.__name__} failed: {e}")
