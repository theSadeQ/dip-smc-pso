# Example from: docs\quality_gate_independence_framework.md
# Index: 11
# Runnable: False
# Hash: 6153c857

# example-metadata:
# runnable: false

class FrameworkHealthMonitor:
    """Monitors the health and effectiveness of the quality gate framework."""

    def __init__(self):
        self.health_metrics = {}
        self.performance_history = []
        self.failure_patterns = {}

    def monitor_framework_health(self) -> FrameworkHealthReport:
        """Monitor overall framework health and effectiveness."""

        # Monitor validation path reliability
        path_reliability = self._monitor_path_reliability()

        # Monitor failure tolerance effectiveness
        tolerance_effectiveness = self._monitor_tolerance_effectiveness()

        # Monitor deployment decision accuracy
        decision_accuracy = self._monitor_decision_accuracy()

        # Monitor framework performance
        performance_metrics = self._monitor_performance_metrics()

        return FrameworkHealthReport(
            overall_health=self._calculate_overall_health(
                path_reliability, tolerance_effectiveness, decision_accuracy, performance_metrics
            ),
            path_reliability=path_reliability,
            tolerance_effectiveness=tolerance_effectiveness,
            decision_accuracy=decision_accuracy,
            performance_metrics=performance_metrics,
            improvement_recommendations=self._generate_health_improvements(
                path_reliability, tolerance_effectiveness, decision_accuracy
            )
        )

    def _monitor_path_reliability(self) -> PathReliabilityReport:
        """Monitor reliability of individual validation paths."""

        path_reliability = {}

        for path_name in ['coverage', 'mathematical', 'performance', 'compliance']:
            # Calculate success rate over time
            recent_executions = self._get_recent_path_executions(path_name, days=30)

            success_rate = len([e for e in recent_executions if e.status == 'success']) / len(recent_executions)

            # Calculate average execution time
            avg_execution_time = np.mean([e.execution_time for e in recent_executions])

            # Identify failure patterns
            failure_patterns = self._analyze_failure_patterns(
                [e for e in recent_executions if e.status != 'success']
            )

            path_reliability[path_name] = PathReliability(
                success_rate=success_rate,
                average_execution_time=avg_execution_time,
                failure_patterns=failure_patterns,
                trend=self._calculate_reliability_trend(path_name)
            )

        return PathReliabilityReport(path_reliability=path_reliability)

    def _monitor_tolerance_effectiveness(self) -> ToleranceEffectivenessReport:
        """Monitor effectiveness of failure tolerance mechanisms."""

        # Analyze graceful degradation success
        degradation_events = self._get_recent_degradation_events(days=30)

        degradation_success_rate = len([
            e for e in degradation_events if e.recovery_successful
        ]) / len(degradation_events) if degradation_events else 1.0

        # Analyze partial success reporting accuracy
        partial_success_events = self._get_recent_partial_success_events(days=30)

        partial_success_accuracy = self._calculate_partial_success_accuracy(partial_success_events)

        return ToleranceEffectivenessReport(
            degradation_success_rate=degradation_success_rate,
            partial_success_accuracy=partial_success_accuracy,
            recovery_time_statistics=self._calculate_recovery_time_stats(degradation_events),
            effectiveness_trend=self._calculate_tolerance_trend()
        )