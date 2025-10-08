# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 16
# Runnable: True
# Hash: c88c6fd7

import matplotlib.pyplot as plt
import json
import pandas as pd
from datetime import datetime, timedelta

class PSOPerformanceDashboard:
    """Performance monitoring dashboard for PSO system."""

    def __init__(self, log_directory='./logs'):
        self.log_directory = Path(log_directory)

    def generate_performance_report(self, days=7):
        """Generate performance report for last N days."""

        # Collect health reports
        reports = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            report_file = self.log_directory / f"health_report_{date.strftime('%Y%m%d')}.json"

            if report_file.exists():
                with open(report_file) as f:
                    report = json.load(f)
                    report['date'] = date
                    reports.append(report)

        if not reports:
            print("No health reports found")
            return

        # Create performance dashboard
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('PSO System Performance Dashboard (Last 7 Days)')

        # Plot 1: Overall health status
        dates = [r['date'] for r in reports]
        statuses = [r['overall_status'] for r in reports]
        status_colors = {'healthy': 'green', 'warnings': 'yellow', 'degraded': 'orange', 'critical': 'red'}

        axes[0, 0].scatter(dates, range(len(dates)), c=[status_colors.get(s, 'gray') for s in statuses], s=100)
        axes[0, 0].set_title('System Health Status')
        axes[0, 0].set_yticks(range(len(dates)))
        axes[0, 0].set_yticklabels([d.strftime('%m/%d') for d in dates])

        # Plot 2: Performance metrics
        perf_times = [r.get('performance_metrics', {}).get('time_per_iteration', 0) for r in reports]
        axes[0, 1].plot(dates, perf_times, 'b-o')
        axes[0, 1].set_title('Optimization Performance')
        axes[0, 1].set_ylabel('Time per Iteration (s)')
        axes[0, 1].tick_params(axis='x', rotation=45)

        # Plot 3: System resources
        memory_usage = [r.get('component_status', {}).get('system_resources', {}).get('memory_gb', 0) for r in reports]
        cpu_usage = [r.get('component_status', {}).get('system_resources', {}).get('cpu_percent', 0) for r in reports]

        axes[1, 0].plot(dates, memory_usage, 'g-o', label='Memory (GB)')
        axes[1, 0].plot(dates, cpu_usage, 'r-o', label='CPU (%)')
        axes[1, 0].set_title('System Resources')
        axes[1, 0].legend()
        axes[1, 0].tick_params(axis='x', rotation=45)

        # Plot 4: Component status summary
        component_names = ['configuration', 'controller_factory', 'pso_engine', 'simulation_engine']
        component_health = {}

        for comp in component_names:
            health_scores = []
            for report in reports:
                status = report.get('component_status', {}).get(comp, {}).get('status', 'unknown')
                score = {'healthy': 3, 'warnings': 2, 'issues': 1, 'failed': 0}.get(status, 0)
                health_scores.append(score)
            component_health[comp] = sum(health_scores) / len(health_scores)

        comp_names = list(component_health.keys())
        comp_scores = list(component_health.values())

        axes[1, 1].bar(comp_names, comp_scores, color=['green' if s > 2.5 else 'orange' if s > 1.5 else 'red' for s in comp_scores])
        axes[1, 1].set_title('Component Health Average')
        axes[1, 1].set_ylabel('Health Score')
        axes[1, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig('pso_performance_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()

        # Generate summary statistics
        print("\n📊 PSO PERFORMANCE SUMMARY (Last 7 Days)")
        print("=" * 50)
        print(f"Average iteration time: {np.mean(perf_times):.2f}s")
        print(f"Best iteration time: {np.min(perf_times):.2f}s")
        print(f"Worst iteration time: {np.max(perf_times):.2f}s")
        print(f"Healthy days: {statuses.count('healthy')}/{len(statuses)}")

        return reports

# Usage
dashboard = PSOPerformanceDashboard()
reports = dashboard.generate_performance_report(days=7)