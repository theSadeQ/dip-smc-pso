# Example from: docs\validation\simulation_result_validation.md
# Index: 45
# Runnable: True
# Hash: 1dcf328a

import matplotlib.pyplot as plt

# Show distribution, not just mean
plt.violinplot([data_A, data_B])
plt.boxplot([data_A, data_B])

# Show confidence intervals
plt.errorbar(x, means, yerr=confidence_intervals)