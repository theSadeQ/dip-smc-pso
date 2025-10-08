# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 9
# Runnable: True
# Hash: a6468e2c

def saturate_linear(sigma, epsilon):
    return np.clip(sigma / epsilon, -1.0, 1.0)