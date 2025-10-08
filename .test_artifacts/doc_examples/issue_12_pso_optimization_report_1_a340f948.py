# Example from: docs\issue_12_pso_optimization_report.md
# Index: 1
# Runnable: False
# Hash: a340f948

# Primary Objective: Maintain tracking performance
tracking_error_rms = sqrt(mean(theta1^2 + theta2^2))

# Secondary Objective: Reduce chattering
chattering_index = 0.7 * time_domain_index + 0.3 * freq_domain_index

where:
  time_domain_index = RMS(d(control)/dt)
  freq_domain_index = HF_power / total_power (f > 10 Hz)

# Combined Fitness
fitness = tracking_error_rms + 10.0 * max(0, chattering_index - 2.0)

# Constraints:
- tracking_error_rms < 0.1 rad
- chattering_index < 2.0
- control_effort < 100 N RMS