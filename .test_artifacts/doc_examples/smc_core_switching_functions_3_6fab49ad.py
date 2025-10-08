# Example from: docs\reference\controllers\smc_core_switching_functions.md
# Index: 3
# Runnable: True
# Hash: 6fab49ad

# Test different slope parameters
slopes = [1.0, 3.0, 5.0, 10.0, 20.0]

for beta in slopes:
    u = saturate(s, epsilon, method='tanh', slope=beta)

    # Estimate effective switching sharpness
    s_test = np.linspace(-3*epsilon, 3*epsilon, 100)
    u_test = saturate(s_test, epsilon, method='tanh', slope=beta)
    sharpness = np.mean(np.abs(np.diff(u_test))) / (6 * epsilon / 100)

    print(f"β={beta:4.1f}: u={u:6.4f}, sharpness={sharpness:.3f}")