# Example from: docs\reference\controllers\smc_core_switching_functions.md
# Index: 5
# Runnable: True
# Hash: 8e73fd0e

from scipy import signal

# Create transfer function for tanh switching
# Approximation: linearize around s=0
# tanh(βs/ε) ≈ (β/ε)s for small s
gain_linear = beta / epsilon

# Frequency response
frequencies = np.logspace(-1, 3, 100)  # 0.1 to 1000 rad/s
w, mag, phase = signal.bode((gain_linear, [1, 0]), frequencies)

# Plot
plt.subplot(2, 1, 1)
plt.semilogx(w, mag)
plt.ylabel('Magnitude (dB)')
plt.title(f'Tanh Switching (β={beta}, ε={epsilon})')

plt.subplot(2, 1, 2)
plt.semilogx(w, phase)
plt.ylabel('Phase (deg)')
plt.xlabel('Frequency (rad/s)')
plt.show()