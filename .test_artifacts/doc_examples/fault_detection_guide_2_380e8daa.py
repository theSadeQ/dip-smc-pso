# Example from: docs\fault_detection_guide.md
# Index: 2
# Runnable: True
# Hash: 380e8daa

# Access FDI history for custom analysis
import matplotlib.pyplot as plt

# After simulation with FDI enabled
times = fdi.times
residuals = fdi.residuals

# Plot residual statistics
plt.figure(figsize=(12, 8))

# Residual time series
plt.subplot(2, 2, 1)
plt.plot(times, residuals)
plt.axhline(fdi.residual_threshold, color='r', linestyle='--')
plt.ylabel('Residual Norm')
plt.title('FDI Residual History')

# Residual histogram
plt.subplot(2, 2, 2)
plt.hist(residuals, bins=50, alpha=0.7)
plt.xlabel('Residual Norm')
plt.ylabel('Frequency')
plt.title('Residual Distribution')

# Moving statistics
window = 50
if len(residuals) > window:
    moving_mean = np.convolve(residuals, np.ones(window)/window, mode='valid')
    moving_std = [np.std(residuals[i:i+window]) for i in range(len(residuals)-window+1)]

    plt.subplot(2, 2, 3)
    plt.plot(times[window-1:], moving_mean, label='Moving Mean')
    plt.plot(times[window-1:], np.array(moving_mean) + 3*np.array(moving_std),
             'r--', label='μ + 3σ')
    plt.ylabel('Residual Statistics')
    plt.legend()
    plt.title('Adaptive Threshold Evolution')

plt.tight_layout()
plt.show()