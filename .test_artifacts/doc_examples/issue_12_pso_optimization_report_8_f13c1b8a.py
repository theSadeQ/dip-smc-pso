# Example from: docs\issue_12_pso_optimization_report.md
# Index: 8
# Runnable: True
# Hash: f13c1b8a

control_derivative = np.gradient(control_signal, dt)
time_domain_index = np.sqrt(np.mean(control_derivative**2))