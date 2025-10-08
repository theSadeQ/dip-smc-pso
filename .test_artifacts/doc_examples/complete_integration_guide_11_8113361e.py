# Example from: docs\workflows\complete_integration_guide.md
# Index: 11
# Runnable: True
# Hash: 8113361e

# Real-time monitoring setup
from src.utils.monitoring import RealTimeMonitor
from src.core.real_time_controller import RealTimeController

def real_time_integration():
    """Set up real-time control with monitoring."""

    # Create real-time controller
    rt_controller = RealTimeController(
        controller_type='hybrid_adaptive_sta_smc',
        control_frequency=1000,  # 1 kHz
        max_jitter=0.001  # 1ms max jitter
    )

    # Set up monitoring
    monitor = RealTimeMonitor(
        metrics=['latency', 'jitter', 'deadline_misses', 'cpu_usage'],
        alert_thresholds={
            'latency': 0.005,      # 5ms warning
            'jitter': 0.002,       # 2ms warning
            'deadline_miss_rate': 0.01,  # 1% warning
            'cpu_usage': 0.8       # 80% warning
        }
    )

    # Run real-time control loop
    rt_controller.run_with_monitoring(
        monitor=monitor,
        duration=60.0,  # 1 minute test
        safety_checks=True
    )

    # Generate real-time performance report
    monitor.generate_performance_report('realtime_performance.pdf')