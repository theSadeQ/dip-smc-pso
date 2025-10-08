# Example from: docs\reference\analysis\validation_monte_carlo.md
# Index: 7
# Runnable: True
# Hash: f20aa49b

import numpy as np

# Define correlated uncertainties (masses tend to vary together)
mean_params = np.array([1.0, 0.1, 0.05])  # cart, pole1, pole2 masses
cov_matrix = np.array([
    [0.04, 0.01, 0.005],   # cart mass variance and covariances
    [0.01, 0.004, 0.002],  # pole1 mass
    [0.005, 0.002, 0.001]  # pole2 mass
])

# Gaussian Monte Carlo
validator = MonteCarloValidator(
    controller_factory=controller_factory,
    uncertainty_model={
        'masses': {
            'type': 'gaussian',
            'mean': mean_params,
            'cov': cov_matrix
        }
    },
    n_samples=200
)

results = validator.run()

# Visualize uncertainty propagation
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
plt.hist(results['ise_samples'], bins=30, alpha=0.7, edgecolor='black')
plt.xlabel('ISE')
plt.ylabel('Frequency')
plt.title('Performance Distribution under Uncertainty')

plt.subplot(1, 2, 2)
plt.scatter(results['param_samples'][:, 0], results['ise_samples'], alpha=0.5)
plt.xlabel('Cart Mass Perturbation')
plt.ylabel('ISE')
plt.title('Sensitivity to Cart Mass')
plt.tight_layout()
plt.show()