# Example from: docs\issue_12_pso_optimization_report.md
# Index: 9
# Runnable: True
# Hash: 21cdc3bc

spectrum = np.abs(fft(control_signal))
freqs = fftfreq(len(control_signal), d=dt)
hf_mask = np.abs(freqs) > 10.0  # High-frequency threshold
hf_power_ratio = sum(spectrum[hf_mask]) / sum(spectrum)