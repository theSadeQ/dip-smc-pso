# Example from: docs\reference\controllers\smc_core_gain_validation.md
# Index: 3
# Runnable: False
# Hash: bbe3c360

# Compute natural frequencies
omega_n1 = np.sqrt(c1 / lambda1)
omega_n2 = np.sqrt(c2 / lambda2)

# Sampling frequency (Hz)
f_s = 100  # Hz
omega_s = 2 * np.pi * f_s  # rad/s

# Check Nyquist criterion
if omega_n1 < omega_s / 5 and omega_n2 < omega_s / 5:
    print(f"✓ Frequencies safe: ω_n1={omega_n1:.2f}, ω_n2={omega_n2:.2f} rad/s")
else:
    print(f"✗ Aliasing risk: ω_n1={omega_n1:.2f}, ω_n2={omega_n2:.2f} rad/s")

# Check lower bound (avoid drift)
if omega_n1 > 0.5 and omega_n2 > 0.5:
    print("✓ Frequencies above DC drift threshold")
else:
    print("✗ Frequencies too low, drift risk")