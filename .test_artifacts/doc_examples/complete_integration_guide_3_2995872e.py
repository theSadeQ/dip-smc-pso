# Example from: docs\workflows\complete_integration_guide.md
# Index: 3
# Runnable: True
# Hash: 2995872e

# Analyze chattering characteristics
from src.utils.analysis import ChatteringAnalyzer

controller = create_controller('sta_smc', gains=[25, 10, 15, 12, 20, 15])
results = run_simulation(controller=controller, duration=10.0)

analyzer = ChatteringAnalyzer()
chattering_metrics = analyzer.analyze(results.control_history)

print(f"Chattering index: {chattering_metrics.index:.4f}")
print(f"High-frequency content: {chattering_metrics.hf_content:.2f}%")