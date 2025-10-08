# Example from: docs\reports\issue_2_implementation_verification_report.md
# Index: 1
# Runnable: True
# Hash: eca254a5

# Gain positivity validation (lines 286-295)
self.alg_gain_K1 = require_positive(self.alg_gain_K1, "K1")
self.alg_gain_K2 = require_positive(self.alg_gain_K2, "K2")
self.surf_gain_k1 = require_positive(self.surf_gain_k1, "k1")
self.surf_gain_k2 = require_positive(self.surf_gain_k2, "k2")
self.surf_lam1 = require_positive(self.surf_lam1, "lam1")
self.surf_lam2 = require_positive(self.surf_lam2, "lam2")