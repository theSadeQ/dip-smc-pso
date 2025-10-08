# Example from: docs\analysis\CONTROLLER_COVERAGE_TECHNICAL_ANALYSIS.md
# Index: 2
# Runnable: True
# Hash: b6be5f27

# All controller implementations include validated saturation:
u_saturated = np.clip(u_total, -self.config.max_force, self.config.max_force)
# Lines covered across all controller types