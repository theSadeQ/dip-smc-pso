# Example from: docs\reference\controllers\smc_core_switching_functions.md
# Index: 4
# Runnable: False
# Hash: e49bf6ac

def dead_zone_switching(s, epsilon, delta, K):
    """Switching with dead zone to avoid chattering near origin."""
    if abs(s) < delta:
        return 0.0
    else:
        return -K * saturate(s, epsilon, method='tanh')

# Parameters
delta = 0.1 * epsilon  # Dead zone 10% of boundary layer
K = 50.0

u_sw = dead_zone_switching(s, epsilon, delta, K)
print(f"Switching with dead zone: {u_sw:.2f} N")