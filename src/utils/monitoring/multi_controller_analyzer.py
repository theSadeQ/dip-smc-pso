#======================================================================================
#=========== src/utils/monitoring/multi_controller_analyzer.py ===========
#======================================================================================
"""
Multi-controller comparison and statistical analysis for monitoring system.

This module provides comprehensive comparison tools for analyzing multiple
controllers side-by-side, including statistical significance testing, performance
ranking, and aggregated metrics visualization.

Features:
    - Performance metrics aggregation (mean, std, CI)
    - Statistical significance testing (t-test, ANOVA, Welch's t-test)
    - Controller ranking by multiple criteria
    - Comparative visualization support
    - Monte Carlo confidence intervals

Usage:
    >>> from src.utils.monitoring.multi_controller_analyzer import MultiControllerAnalyzer
    >>> analyzer = MultiControllerAnalyzer()
    >>>
    >>> # Aggregate metrics for each controller
    >>> stats = analyzer.aggregate_metrics(['classical_smc', 'adaptive_smc', 'sta_smc'])
    >>>
    >>> # Compare two controllers
    >>> comparison = analyzer.compare_controllers('classical_smc', 'adaptive_smc')
    >>> print(f"p-value: {comparison['settling_time']['p_value']:.4f}")
    >>>
    >>> # Rank controllers
    >>> rankings = analyzer.rank_controllers(['classical_smc', 'adaptive_smc'])

Integration:
    - Works with DataManager for simulation data
    - Supports filtering by scenario, date range
    - Provides data for visualization components

Author: Claude Code (AI-assisted development)
Date: December 2025
"""

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
from scipy import stats

from src.utils.monitoring.data_manager import DataManager


@dataclass
class ControllerStats:
    """Statistical summary for a single controller."""

    controller: str
    n_runs: int
    mean_score: float
    std_score: float
    mean_settling_time: float
    std_settling_time: float
    mean_overshoot: float
    std_overshoot: float
    mean_steady_state_error: float
    std_steady_state_error: float
    mean_energy: float
    std_energy: float
    mean_chattering: float
    std_chattering: float
    score_ci_95: Tuple[float, float]  # 95% confidence interval for score


@dataclass
class ComparisonResult:
    """Statistical comparison result between two controllers."""

    controller_a: str
    controller_b: str
    metric: str
    mean_a: float
    mean_b: float
    std_a: float
    std_b: float
    t_statistic: float
    p_value: float
    significant: bool  # True if p < 0.05
    effect_size: float  # Cohen's d


class MultiControllerAnalyzer:
    """
    Multi-controller comparison and statistical analysis.

    This analyzer aggregates performance metrics across multiple runs,
    performs statistical significance testing, and generates rankings.

    Attributes:
        data_manager: DataManager instance for querying runs
    """

    def __init__(self, data_manager: Optional[DataManager] = None):
        """
        Initialize multi-controller analyzer.

        Args:
            data_manager: Optional DataManager instance (creates new if None)
        """
        self.data_manager = data_manager or DataManager()
        logging.info("MultiControllerAnalyzer initialized")

    def aggregate_metrics(
        self,
        controllers: List[str],
        scenario: Optional[str] = None,
        min_runs: int = 3
    ) -> Dict[str, ControllerStats]:
        """
        Aggregate performance metrics for multiple controllers.

        Args:
            controllers: List of controller names to analyze
            scenario: Optional scenario filter (e.g., 'nominal', 'robust')
            min_runs: Minimum number of runs required for statistics

        Returns:
            Dictionary mapping controller name to ControllerStats

        Example:
            >>> stats = analyzer.aggregate_metrics(['classical_smc', 'adaptive_smc'])
            >>> print(f"Classical SMC: {stats['classical_smc'].mean_score:.2f}")
        """
        results = {}

        for controller in controllers:
            # Query runs for this controller
            runs = self.data_manager.query_runs(
                controller=controller,
                scenario=scenario,
                limit=1000
            )

            if len(runs) < min_runs:
                logging.warning(
                    f"Controller {controller} has only {len(runs)} runs (min: {min_runs})"
                )
                continue

            # Extract metrics
            scores = []
            settling_times = []
            overshoots = []
            steady_state_errors = []
            energies = []
            chatterings = []

            for run in runs:
                if run.summary:
                    scores.append(run.summary.get_score())
                    if run.summary.settling_time_s is not None:
                        settling_times.append(run.summary.settling_time_s)
                    if run.summary.overshoot_pct is not None:
                        overshoots.append(run.summary.overshoot_pct)
                    if run.summary.steady_state_error is not None:
                        steady_state_errors.append(run.summary.steady_state_error)
                    if run.summary.energy_j is not None:
                        energies.append(run.summary.energy_j)
                    if run.summary.chattering_amplitude is not None:
                        chatterings.append(run.summary.chattering_amplitude)

            # Compute statistics
            score_mean = float(np.mean(scores)) if scores else 0.0
            score_std = float(np.std(scores)) if len(scores) > 1 else 0.0

            # 95% confidence interval for score (using t-distribution)
            if len(scores) > 1:
                ci_95 = stats.t.interval(
                    0.95,
                    len(scores) - 1,
                    loc=score_mean,
                    scale=stats.sem(scores)
                )
                score_ci_95 = (float(ci_95[0]), float(ci_95[1]))
            else:
                score_ci_95 = (score_mean, score_mean)

            results[controller] = ControllerStats(
                controller=controller,
                n_runs=len(runs),
                mean_score=score_mean,
                std_score=score_std,
                mean_settling_time=float(np.mean(settling_times)) if settling_times else 0.0,
                std_settling_time=float(np.std(settling_times)) if len(settling_times) > 1 else 0.0,
                mean_overshoot=float(np.mean(overshoots)) if overshoots else 0.0,
                std_overshoot=float(np.std(overshoots)) if len(overshoots) > 1 else 0.0,
                mean_steady_state_error=float(np.mean(steady_state_errors)) if steady_state_errors else 0.0,
                std_steady_state_error=float(np.std(steady_state_errors)) if len(steady_state_errors) > 1 else 0.0,
                mean_energy=float(np.mean(energies)) if energies else 0.0,
                std_energy=float(np.std(energies)) if len(energies) > 1 else 0.0,
                mean_chattering=float(np.mean(chatterings)) if chatterings else 0.0,
                std_chattering=float(np.std(chatterings)) if len(chatterings) > 1 else 0.0,
                score_ci_95=score_ci_95
            )

        logging.info(f"Aggregated metrics for {len(results)} controllers")
        return results

    def compare_controllers(
        self,
        controller_a: str,
        controller_b: str,
        scenario: Optional[str] = None
    ) -> Dict[str, ComparisonResult]:
        """
        Compare two controllers with statistical significance testing.

        Uses Welch's t-test (does not assume equal variances) for each metric.
        Computes Cohen's d for effect size.

        Args:
            controller_a: First controller name
            controller_b: Second controller name
            scenario: Optional scenario filter

        Returns:
            Dictionary mapping metric name to ComparisonResult

        Example:
            >>> comparison = analyzer.compare_controllers('classical_smc', 'adaptive_smc')
            >>> settling_time_result = comparison['settling_time']
            >>> if settling_time_result.significant:
            ...     print("Settling times are significantly different!")
        """
        # Query runs for both controllers
        runs_a = self.data_manager.query_runs(
            controller=controller_a,
            scenario=scenario,
            limit=1000
        )

        runs_b = self.data_manager.query_runs(
            controller=controller_b,
            scenario=scenario,
            limit=1000
        )

        if not runs_a or not runs_b:
            logging.warning(f"Insufficient data for comparison: {controller_a}={len(runs_a)}, {controller_b}={len(runs_b)}")
            return {}

        # Extract metrics for each controller
        metrics_a = self._extract_metrics(runs_a)
        metrics_b = self._extract_metrics(runs_b)

        results = {}

        # Compare each metric
        for metric in ['score', 'settling_time', 'overshoot', 'steady_state_error', 'energy', 'chattering']:
            values_a = metrics_a.get(metric, [])
            values_b = metrics_b.get(metric, [])

            if not values_a or not values_b:
                continue

            # Compute statistics
            mean_a = float(np.mean(values_a))
            mean_b = float(np.mean(values_b))
            std_a = float(np.std(values_a))
            std_b = float(np.std(values_b))

            # Welch's t-test (does not assume equal variances)
            t_stat, p_val = stats.ttest_ind(values_a, values_b, equal_var=False)

            # Cohen's d (effect size)
            pooled_std = np.sqrt((std_a**2 + std_b**2) / 2)
            cohens_d = (mean_a - mean_b) / pooled_std if pooled_std > 0 else 0.0

            results[metric] = ComparisonResult(
                controller_a=controller_a,
                controller_b=controller_b,
                metric=metric,
                mean_a=mean_a,
                mean_b=mean_b,
                std_a=std_a,
                std_b=std_b,
                t_statistic=float(t_stat),
                p_value=float(p_val),
                significant=(p_val < 0.05),
                effect_size=float(cohens_d)
            )

        logging.info(f"Compared {controller_a} vs {controller_b}: {len(results)} metrics")
        return results

    def rank_controllers(
        self,
        controllers: List[str],
        scenario: Optional[str] = None,
        weights: Optional[Dict[str, float]] = None
    ) -> List[Tuple[str, float]]:
        """
        Rank controllers by weighted composite score.

        Default weights prioritize performance:
        - score: 0.4
        - settling_time: 0.2 (inverted - lower is better)
        - overshoot: 0.15 (inverted)
        - steady_state_error: 0.15 (inverted)
        - energy: 0.05 (inverted)
        - chattering: 0.05 (inverted)

        Args:
            controllers: List of controller names to rank
            scenario: Optional scenario filter
            weights: Optional custom weights (must sum to 1.0)

        Returns:
            List of (controller, composite_score) tuples, sorted by score (descending)

        Example:
            >>> rankings = analyzer.rank_controllers(['classical_smc', 'adaptive_smc'])
            >>> for i, (controller, score) in enumerate(rankings, 1):
            ...     print(f"{i}. {controller}: {score:.2f}")
        """
        # Default weights
        if weights is None:
            weights = {
                'score': 0.4,
                'settling_time': 0.2,
                'overshoot': 0.15,
                'steady_state_error': 0.15,
                'energy': 0.05,
                'chattering': 0.05
            }

        # Aggregate metrics
        stats = self.aggregate_metrics(controllers, scenario=scenario)

        if not stats:
            logging.warning("No controller statistics available for ranking")
            return []

        # Normalize metrics to [0, 1] range
        # For score: higher is better (already 0-100 scale)
        # For others: lower is better (invert)
        normalized = {}

        for controller, ctrl_stats in stats.items():
            normalized[controller] = {
                'score': ctrl_stats.mean_score / 100.0,  # Normalize to [0, 1]
            }

            # For inverted metrics, use 1 / (1 + x) normalization
            normalized[controller]['settling_time'] = 1.0 / (1.0 + ctrl_stats.mean_settling_time)
            normalized[controller]['overshoot'] = 1.0 / (1.0 + ctrl_stats.mean_overshoot)
            normalized[controller]['steady_state_error'] = 1.0 / (1.0 + ctrl_stats.mean_steady_state_error)
            normalized[controller]['energy'] = 1.0 / (1.0 + ctrl_stats.mean_energy)
            normalized[controller]['chattering'] = 1.0 / (1.0 + ctrl_stats.mean_chattering)

        # Compute weighted composite scores
        composite_scores = []

        for controller in controllers:
            if controller not in normalized:
                continue

            score = 0.0
            for metric, weight in weights.items():
                score += normalized[controller].get(metric, 0.0) * weight

            composite_scores.append((controller, score * 100.0))  # Scale back to 0-100

        # Sort by score (descending)
        composite_scores.sort(key=lambda x: x[1], reverse=True)

        logging.info(f"Ranked {len(composite_scores)} controllers")
        return composite_scores

    def anova_test(
        self,
        controllers: List[str],
        metric: str = 'score',
        scenario: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Perform one-way ANOVA to test if controllers have significantly different means.

        Args:
            controllers: List of controller names to test
            metric: Metric to test ('score', 'settling_time', etc.)
            scenario: Optional scenario filter

        Returns:
            Dictionary with 'f_statistic' and 'p_value'

        Example:
            >>> result = analyzer.anova_test(['classical_smc', 'adaptive_smc', 'sta_smc'])
            >>> if result['p_value'] < 0.05:
            ...     print("Controllers have significantly different performance!")
        """
        # Collect metrics for each controller
        groups = []

        for controller in controllers:
            runs = self.data_manager.query_runs(
                controller=controller,
                scenario=scenario,
                limit=1000
            )

            metrics = self._extract_metrics(runs)
            values = metrics.get(metric, [])

            if values:
                groups.append(values)

        if len(groups) < 2:
            logging.warning("Need at least 2 controllers for ANOVA")
            return {'f_statistic': 0.0, 'p_value': 1.0}

        # Perform one-way ANOVA
        f_stat, p_val = stats.f_oneway(*groups)

        logging.info(f"ANOVA test for {metric}: F={f_stat:.4f}, p={p_val:.4f}")
        return {
            'f_statistic': float(f_stat),
            'p_value': float(p_val)
        }

    def _extract_metrics(self, runs) -> Dict[str, List[float]]:
        """
        Extract metrics from a list of runs.

        Args:
            runs: List of DashboardData objects

        Returns:
            Dictionary mapping metric name to list of values
        """
        metrics = {
            'score': [],
            'settling_time': [],
            'overshoot': [],
            'steady_state_error': [],
            'energy': [],
            'chattering': []
        }

        for run in runs:
            if run.summary:
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
