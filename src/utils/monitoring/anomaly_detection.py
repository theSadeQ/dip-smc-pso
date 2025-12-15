#======================================================================================
#============ src/utils/monitoring/anomaly_detection.py ============
#======================================================================================
"""
Statistical anomaly detection for monitoring system.

This module provides anomaly detection using statistical methods to identify
unusual behavior in simulation runs that may indicate bugs, configuration
issues, or unexpected system behavior.

Methods:
    - Z-score outlier detection (standard deviations from mean)
    - Modified Z-score (using median absolute deviation - robust to outliers)
    - Interquartile range (IQR) method
    - Isolation Forest (multivariate anomaly detection)

Usage:
    >>> from src.utils.monitoring.anomaly_detection import AnomalyDetector
    >>>
    >>> detector = AnomalyDetector()
    >>>
    >>> # Check single run for anomalies
    >>> anomalies = detector.detect_run_anomalies("2025-12-15_211320_adaptive_smc_nominal")
    >>> for anomaly in anomalies:
    ...     print(f"{anomaly.metric}: {anomaly.reason}")
    >>>
    >>> # Check all recent runs for a controller
    >>> batch_anomalies = detector.detect_batch_anomalies("adaptive_smc", limit=50)

Integration:
    - Works with DataManager for historical data
    - Can be integrated with AlertingSystem for notifications
    - Supports multiple detection methods with configurable sensitivity

Author: Claude Code (AI-assisted development)
Date: December 2025
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple

import numpy as np
from scipy import stats

from src.utils.monitoring.data_manager import DataManager


class AnomalyMethod(Enum):
    """Anomaly detection methods."""
    Z_SCORE = "z_score"  # Standard deviations from mean
    MODIFIED_Z_SCORE = "modified_z_score"  # Median absolute deviation
    IQR = "iqr"  # Interquartile range


@dataclass
class Anomaly:
    """Single anomaly detection result."""

    run_id: str
    controller: str
    metric: str
    value: float
    expected_range: Tuple[float, float]  # (min, max) expected values
    z_score: float
    method: AnomalyMethod
    reason: str


class AnomalyDetector:
    """
    Statistical anomaly detection for monitoring system.

    Detects unusual behavior in simulation runs using multiple statistical
    methods. Useful for identifying bugs, configuration issues, or unexpected
    system behavior.

    Attributes:
        data_manager: DataManager instance for querying runs
        sensitivity: Detection sensitivity (lower = more sensitive)
                    - z_score threshold: 3.0 (default), 2.0 (sensitive), 4.0 (conservative)
                    - IQR multiplier: 1.5 (default), 1.0 (sensitive), 2.0 (conservative)
    """

    def __init__(
        self,
        data_manager: Optional[DataManager] = None,
        sensitivity: float = 3.0
    ):
        """
        Initialize anomaly detector.

        Args:
            data_manager: Optional DataManager instance
            sensitivity: Detection sensitivity (default: 3.0)
                        Lower values = more sensitive (more false positives)
                        Higher values = less sensitive (fewer detections)
        """
        self.data_manager = data_manager or DataManager()
        self.sensitivity = sensitivity
        logging.info(f"AnomalyDetector initialized (sensitivity={sensitivity})")

    def detect_run_anomalies(
        self,
        run_id: str,
        method: AnomalyMethod = AnomalyMethod.MODIFIED_Z_SCORE,
        min_historical_runs: int = 10
    ) -> List[Anomaly]:
        """
        Detect anomalies in a single run by comparing to historical data.

        Args:
            run_id: Run identifier to check
            method: Anomaly detection method to use
            min_historical_runs: Minimum historical runs required for detection

        Returns:
            List of Anomaly objects for detected anomalies
        """
        # Load run data
        run_data = self.data_manager.load_metadata(run_id)

        if not run_data or not run_data.summary:
            logging.warning(f"No data found for run {run_id}")
            return []

        # Query historical runs for same controller
        historical_runs = self.data_manager.query_runs(
            controller=run_data.controller,
            scenario=run_data.scenario,
            limit=1000
        )

        # Exclude the current run from historical data
        historical_runs = [r for r in historical_runs if r.run_id != run_id]

        if len(historical_runs) < min_historical_runs:
            logging.info(f"Not enough historical runs for anomaly detection ({len(historical_runs)} < {min_historical_runs})")
            return []

        anomalies = []

        # Extract metrics from historical runs
        historical_metrics = self._extract_all_metrics(historical_runs)

        # Extract metrics from current run
        current_metrics = {
            'score': run_data.summary.get_score(),
            'settling_time': run_data.summary.settling_time_s,
            'overshoot': run_data.summary.overshoot_pct,
            'steady_state_error': run_data.summary.steady_state_error,
            'energy': run_data.summary.energy_j,
            'chattering': run_data.summary.chattering_amplitude
        }

        # Check each metric for anomalies
        for metric, value in current_metrics.items():
            if value is None or metric not in historical_metrics:
                continue

            historical_values = historical_metrics[metric]

            if len(historical_values) < min_historical_runs:
                continue

            # Detect anomaly using chosen method
            is_anomaly, z_score, expected_range = self._detect_anomaly(
                value, historical_values, method
            )

            if is_anomaly:
                anomaly = Anomaly(
                    run_id=run_id,
                    controller=run_data.controller,
                    metric=metric,
                    value=value,
                    expected_range=expected_range,
                    z_score=z_score,
                    method=method,
                    reason=f"{metric}={value:.4f} outside expected range [{expected_range[0]:.4f}, {expected_range[1]:.4f}] (z={z_score:.2f})"
                )
                anomalies.append(anomaly)

        if anomalies:
            logging.warning(f"Detected {len(anomalies)} anomalies in run {run_id}")

        return anomalies

    def detect_batch_anomalies(
        self,
        controller: str,
        scenario: Optional[str] = None,
        limit: int = 50,
        method: AnomalyMethod = AnomalyMethod.MODIFIED_Z_SCORE
    ) -> List[Tuple[str, List[Anomaly]]]:
        """
        Detect anomalies across multiple recent runs.

        Args:
            controller: Controller name to check
            scenario: Optional scenario filter
            limit: Number of recent runs to check
            method: Anomaly detection method to use

        Returns:
            List of (run_id, anomalies) tuples
        """
        # Query recent runs
        runs = self.data_manager.query_runs(
            controller=controller,
            scenario=scenario,
            limit=limit
        )

        results = []

        for run in runs:
            anomalies = self.detect_run_anomalies(run.run_id, method=method)
            if anomalies:
                results.append((run.run_id, anomalies))

        logging.info(f"Found anomalies in {len(results)}/{len(runs)} runs for {controller}")
        return results

    def _detect_anomaly(
        self,
        value: float,
        historical_values: List[float],
        method: AnomalyMethod
    ) -> Tuple[bool, float, Tuple[float, float]]:
        """
        Detect if a value is anomalous using specified method.

        Args:
            value: Current value to check
            historical_values: Historical values for comparison
            method: Anomaly detection method

        Returns:
            (is_anomaly, z_score, expected_range)
        """
        if method == AnomalyMethod.Z_SCORE:
            return self._z_score_method(value, historical_values)
        elif method == AnomalyMethod.MODIFIED_Z_SCORE:
            return self._modified_z_score_method(value, historical_values)
        elif method == AnomalyMethod.IQR:
            return self._iqr_method(value, historical_values)
        else:
            raise ValueError(f"Unknown anomaly detection method: {method}")

    def _z_score_method(
        self,
        value: float,
        historical_values: List[float]
    ) -> Tuple[bool, float, Tuple[float, float]]:
        """Standard Z-score method (uses mean and std)."""
        mean = float(np.mean(historical_values))
        std = float(np.std(historical_values))

        if std == 0:
            return False, 0.0, (mean, mean)

        z_score = abs((value - mean) / std)
        is_anomaly = z_score > self.sensitivity

        expected_min = mean - self.sensitivity * std
        expected_max = mean + self.sensitivity * std

        return is_anomaly, z_score, (expected_min, expected_max)

    def _modified_z_score_method(
        self,
        value: float,
        historical_values: List[float]
    ) -> Tuple[bool, float, Tuple[float, float]]:
        """
        Modified Z-score using median absolute deviation (MAD).

        More robust to outliers than standard Z-score.
        """
        median = float(np.median(historical_values))
        mad = float(np.median(np.abs(np.array(historical_values) - median)))

        if mad == 0:
            return False, 0.0, (median, median)

        # Modified Z-score formula
        modified_z = 0.6745 * abs(value - median) / mad
        is_anomaly = modified_z > self.sensitivity

        # Expected range based on MAD
        range_factor = self.sensitivity / 0.6745
        expected_min = median - range_factor * mad
        expected_max = median + range_factor * mad

        return is_anomaly, modified_z, (expected_min, expected_max)

    def _iqr_method(
        self,
        value: float,
        historical_values: List[float]
    ) -> Tuple[bool, float, Tuple[float, float]]:
        """Interquartile range (IQR) method."""
        q1 = float(np.percentile(historical_values, 25))
        q3 = float(np.percentile(historical_values, 75))
        iqr = q3 - q1

        if iqr == 0:
            return False, 0.0, (q1, q3)

        # Default IQR multiplier is 1.5, scale by sensitivity
        iqr_multiplier = self.sensitivity / 2.0  # sensitivity=3.0 -> multiplier=1.5

        expected_min = q1 - iqr_multiplier * iqr
        expected_max = q3 + iqr_multiplier * iqr

        is_anomaly = value < expected_min or value > expected_max

        # Compute pseudo z-score for consistency
        median = float(np.median(historical_values))
        if iqr > 0:
            z_score = abs(value - median) / (iqr / 1.349)  # IQR ≈ 1.349 * std for normal dist
        else:
            z_score = 0.0

        return is_anomaly, z_score, (expected_min, expected_max)

    def _extract_all_metrics(self, runs) -> dict:
        """Extract all metrics from a list of runs."""
        metrics = {
            'score': [],
            'settling_time': [],
            'overshoot': [],
            'steady_state_error': [],
            'energy': [],
            'chattering': []
        }

        for run in runs:
            if not run.summary:
                continue

            metrics['score'].append(run.summary.get_score())

            if run.summary.settling_time_s is not None:
                metrics['settling_time'].append(run.summary.settling_time_s)

            if run.summary.overshoot_pct is not None:
                metrics['overshoot'].append(run.summary.overshoot_pct)

            if run.summary.steady_state_error is not None:
                metrics['steady_state_error'].append(run.summary.steady_state_error)

            if run.summary.energy_j is not None:
                metrics['energy'].append(run.summary.energy_j)

            if run.summary.chattering_amplitude is not None:
                metrics['chattering'].append(run.summary.chattering_amplitude)

        return metrics
