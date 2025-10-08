# Example from: docs\reference\controllers\smc_core_sliding_surface.md
# Index: 4
# Runnable: False
# Hash: 1076cf90

# example-metadata:
# runnable: false

# Compute characteristic frequencies
c1, c2, lambda1, lambda2 = gains
omega_n1 = np.sqrt(c1 / lambda1)  # rad/s
omega_n2 = np.sqrt(c2 / lambda2)  # rad/s

print(f"Natural frequency 1: {omega_n1:.2f} rad/s")
print(f"Natural frequency 2: {omega_n2:.2f} rad/s")

# Check Nyquist criterion (sampling frequency 100 Hz)
omega_s = 2 * np.pi * 100  # rad/s
if omega_n1 < omega_s / 5 and omega_n2 < omega_s / 5:
    print("Frequencies safe for 100 Hz sampling")