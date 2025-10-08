# Example from: docs\benchmarks\phase_3_2_completion_report.md
# Index: 3
# Runnable: True
# Hash: 2deb8dd3

# Option 1: Add property to HybridSMCConfig
@property
def gains(self):
    return np.concatenate([self.classical_gains, self.sta_gains, [self.adaptation_rate]])

# Option 2: Update validation script to handle nested configs
if hasattr(config, 'gains'):
    gains = config.gains
elif hasattr(config, 'classical_gains'):
    gains = np.concatenate([config.classical_gains, config.sta_gains, [config.adaptation_rate]])