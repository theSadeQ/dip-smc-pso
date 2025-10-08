# Example from: docs\testing\guides\coverage_quality_gates_troubleshooting.md
# Index: 5
# Runnable: True
# Hash: f653a8fd

# Uncovered: Safety saturation limits
   if abs(control_signal) > self.max_control:  # ← Safety limit not tested
       control_signal = np.sign(control_signal) * self.max_control