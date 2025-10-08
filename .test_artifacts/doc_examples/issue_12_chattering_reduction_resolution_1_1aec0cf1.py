# Example from: docs\issue_12_chattering_reduction_resolution.md
# Index: 1
# Runnable: True
# Hash: 1aec0cf1

def get_chattering_index(self, control_history, dt=0.01):
    """FFT-based spectral analysis + time-domain Total Variation."""
    # Time-domain: RMS of control derivative
    control_derivative = np.gradient(control_array, dt)
    time_domain_index = np.sqrt(np.mean(control_derivative**2))

    # Frequency-domain: High-frequency power ratio (>10 Hz)
    from scipy.fft import fft, fftfreq
    spectrum = np.abs(fft(control_array))
    freqs = fftfreq(len(control_array), d=dt)
    hf_power = np.sum(spectrum[np.abs(freqs) > 10])
    freq_domain_index = hf_power / (np.sum(spectrum) + 1e-12)

    # Combined weighted index
    return 0.7 * time_domain_index + 0.3 * freq_domain_index