# Example from: docs\theory\numerical_stability_methods.md
# Index: 2
# Runnable: False
# Hash: 144217f7

# Adaptive scaling based on condition number
if cond_num > self.max_cond or sv_ratio < 1e-8:
    # Extreme ill-conditioning - aggressive regularization
    if sv_ratio < 2e-9:
        reg_scale = max(self.alpha * s[0] * 1e5, ...)
    elif sv_ratio < 1e-8:
        reg_scale = max(self.alpha * s[0] * 1e4, ...)
    # ...