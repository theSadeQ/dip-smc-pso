# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 8
# Runnable: True
# Hash: b98c9ed7

def saturate_tanh(sigma, epsilon):
    return np.tanh(sigma / epsilon)