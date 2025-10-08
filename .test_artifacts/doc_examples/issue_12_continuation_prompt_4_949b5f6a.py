# Example from: docs\issue_12_continuation_prompt.md
# Index: 4
# Runnable: False
# Hash: 949b5f6a

# example-metadata:
# runnable: false

# Time domain: RMS of control derivative
control_derivative = np.gradient(control_history, dt)
time_domain_index = np.sqrt(np.mean(control_derivative**2))

# Frequency domain: High-frequency power ratio
spectrum = np.abs(fft(control_history))
freqs = fftfreq(len(control_history), d=dt)
hf_power = np.sum(spectrum[np.abs(freqs) > 10.0])
total_power = np.sum(spectrum) + 1e-12
freq_domain_index = hf_power / total_power

# Composite index (0.7/0.3 weighting)
chattering_index = 0.7 * time_domain_index + 0.3 * freq_domain_index