# Example from: docs\workflows\complete_integration_guide.md
# Index: 2
# Runnable: True
# Hash: 1c5e39b3

# Monitor adaptation process
from src.utils.monitoring import AdaptationMonitor

monitor = AdaptationMonitor()
controller = create_controller('adaptive_smc', gains=[10, 8, 15, 12, 0.5])

# Run with monitoring
results = run_simulation_with_monitoring(
    controller=controller,
    monitor=monitor,
    duration=15.0  # Longer to observe adaptation
)

# Plot adaptation history
monitor.plot_adaptation_evolution()
monitor.save_adaptation_data('adaptation_log.json')