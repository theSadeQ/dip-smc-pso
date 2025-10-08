# Example from: docs\analysis\COVERAGE_ANALYSIS_METHODOLOGY_FRAMEWORK.md
# Index: 4
# Runnable: True
# Hash: ac6c965e

# src/utils/coverage/monitoring.py
#==========================================================================================\\\
#=========================== src/utils/coverage/monitoring.py ========================\\\
#==========================================================================================\\\

"""Real-time coverage monitoring and alerting system."""

import time
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path

@dataclass
class CoverageMetrics:
    """Coverage metrics data structure."""
    timestamp: float
    overall_coverage: float
    critical_coverage: float
    safety_coverage: float
    branch_coverage: float
    test_count: int
    execution_time: float

class CoverageMonitor:
    """Real-time coverage monitoring with trend analysis."""

    def __init__(self, metrics_file: Path = Path("coverage_metrics.json")):
        self.metrics_file = metrics_file
        self.metrics_history: List[CoverageMetrics] = []
        self.load_metrics_history()

    def record_coverage_run(self, coverage_data: Dict) -> CoverageMetrics:
        """Record coverage metrics from test run."""
        metrics = CoverageMetrics(
            timestamp=time.time(),
            overall_coverage=coverage_data.get('overall', 0.0),
            critical_coverage=coverage_data.get('critical', 0.0),
            safety_coverage=coverage_data.get('safety', 0.0),
            branch_coverage=coverage_data.get('branch', 0.0),
            test_count=coverage_data.get('test_count', 0),
            execution_time=coverage_data.get('execution_time', 0.0)
        )

        self.metrics_history.append(metrics)
        self.save_metrics_history()
        return metrics

    def analyze_coverage_trends(self, window_size: int = 10) -> Dict:
        """Analyze coverage trends over recent runs."""
        if len(self.metrics_history) < window_size:
            return {"trend": "insufficient_data"}

        recent_metrics = self.metrics_history[-window_size:]

        # Calculate trend slopes
        def calculate_slope(values: List[float]) -> float:
            n = len(values)
            x_mean = sum(range(n)) / n
            y_mean = sum(values) / n

            numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
            denominator = sum((i - x_mean) ** 2 for i in range(n))

            return numerator / denominator if denominator != 0 else 0

        overall_slope = calculate_slope([m.overall_coverage for m in recent_metrics])
        critical_slope = calculate_slope([m.critical_coverage for m in recent_metrics])

        return {
            "overall_trend": "improving" if overall_slope > 0.1 else "declining" if overall_slope < -0.1 else "stable",
            "critical_trend": "improving" if critical_slope > 0.1 else "declining" if critical_slope < -0.1 else "stable",
            "overall_slope": overall_slope,
            "critical_slope": critical_slope,
            "latest_metrics": recent_metrics[-1].__dict__
        }

    def generate_coverage_alert(self, threshold_violations: List[str]) -> str:
        """Generate coverage alert for threshold violations."""
        if not threshold_violations:
            return "✅ All coverage thresholds met"

        alert = "🚨 COVERAGE THRESHOLD VIOLATIONS DETECTED\n\n"
        for violation in threshold_violations:
            alert += f"❌ {violation}\n"

        alert += "\n📊 Current Coverage Status:\n"
        latest = self.metrics_history[-1] if self.metrics_history else None
        if latest:
            alert += f"- Overall: {latest.overall_coverage:.1f}%\n"
            alert += f"- Critical: {latest.critical_coverage:.1f}%\n"
            alert += f"- Safety: {latest.safety_coverage:.1f}%\n"

        return alert

    def save_metrics_history(self):
        """Save metrics history to JSON file."""
        data = [m.__dict__ for m in self.metrics_history]
        with open(self.metrics_file, 'w') as f:
            json.dump(data, f, indent=2)

    def load_metrics_history(self):
        """Load metrics history from JSON file."""
        if self.metrics_file.exists():
            with open(self.metrics_file, 'r') as f:
                data = json.load(f)
                self.metrics_history = [CoverageMetrics(**item) for item in data]