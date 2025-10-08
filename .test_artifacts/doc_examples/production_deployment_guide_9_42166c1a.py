# Example from: docs\factory\production_deployment_guide.md
# Index: 9
# Runnable: True
# Hash: 42166c1a

class FactoryCapacityPlanner:
    """Capacity planning for factory system."""

    def __init__(self):
        self.capacity_data = []

    def analyze_capacity_trends(self):
        """Analyze capacity trends and predict future needs."""

        # Collect current usage data
        current_metrics = self.collect_capacity_metrics()

        # Analyze trends
        trends = self.analyze_trends()

        # Generate recommendations
        recommendations = self.generate_capacity_recommendations(trends)

        return {
            'current_metrics': current_metrics,
            'trends': trends,
            'recommendations': recommendations
        }

    def collect_capacity_metrics(self):
        """Collect current capacity metrics."""

        import psutil
        import os

        process = psutil.Process(os.getpid())

        return {
            'timestamp': time.time(),
            'cpu_percent': process.cpu_percent(),
            'memory_mb': process.memory_info().rss / 1024 / 1024,
            'thread_count': process.num_threads(),
            'open_files': process.num_fds() if hasattr(process, 'num_fds') else 0
        }

    def analyze_trends(self):
        """Analyze usage trends."""

        if len(self.capacity_data) < 2:
            return {'insufficient_data': True}

        # Simple trend analysis
        recent_data = self.capacity_data[-10:]  # Last 10 measurements

        memory_trend = 'stable'
        cpu_trend = 'stable'

        if len(recent_data) >= 5:
            memory_values = [d['memory_mb'] for d in recent_data]
            cpu_values = [d['cpu_percent'] for d in recent_data]

            # Simple trend detection
            if memory_values[-1] > memory_values[0] * 1.2:
                memory_trend = 'increasing'
            elif memory_values[-1] < memory_values[0] * 0.8:
                memory_trend = 'decreasing'

            if cpu_values[-1] > cpu_values[0] * 1.2:
                cpu_trend = 'increasing'
            elif cpu_values[-1] < cpu_values[0] * 0.8:
                cpu_trend = 'decreasing'

        return {
            'memory_trend': memory_trend,
            'cpu_trend': cpu_trend,
            'data_points': len(recent_data)
        }

    def generate_capacity_recommendations(self, trends):
        """Generate capacity planning recommendations."""

        recommendations = []

        if trends.get('memory_trend') == 'increasing':
            recommendations.append({
                'type': 'memory',
                'action': 'Monitor memory usage closely and consider increasing memory limits',
                'priority': 'medium'
            })

        if trends.get('cpu_trend') == 'increasing':
            recommendations.append({
                'type': 'cpu',
                'action': 'Consider CPU optimization or horizontal scaling',
                'priority': 'medium'
            })

        return recommendations

# Setup capacity planner
capacity_planner = FactoryCapacityPlanner()