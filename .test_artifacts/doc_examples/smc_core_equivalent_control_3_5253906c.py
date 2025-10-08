# Example from: docs\reference\controllers\smc_core_equivalent_control.md
# Index: 3
# Runnable: False
# Hash: 5253906c

# Adaptive regularization based on conditioning
def adaptive_regularization(cond_number):
    if cond_number < 1e3:
        return 1e-6  # Minimal regularization
    elif cond_number < 1e6:
        return 1e-5  # Moderate regularization
    else:
        return 1e-4  # Strong regularization

alpha = adaptive_regularization(cond_number)
eq_control.set_regularization(alpha=alpha)
print(f"Using regularization: α={alpha:.2e}")