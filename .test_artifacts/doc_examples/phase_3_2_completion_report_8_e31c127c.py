# Example from: docs\benchmarks\phase_3_2_completion_report.md
# Index: 8
# Runnable: False
# Hash: e31c127c

@property
def gains(self):
    """Expose flattened gains array for optimization."""
    return np.concatenate([
        self.classical_gains,
        self.sta_gains,
        [self.adaptation_rate]
    ])

@gains.setter
def gains(self, value):
    """Accept flattened gains array from optimizer."""
    n_classical = len(self.classical_gains)
    n_sta = len(self.sta_gains)
    self.classical_gains = value[:n_classical]
    self.sta_gains = value[n_classical:n_classical+n_sta]
    self.adaptation_rate = value[-1]