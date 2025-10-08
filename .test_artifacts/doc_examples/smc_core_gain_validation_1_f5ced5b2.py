# Example from: docs\reference\controllers\smc_core_gain_validation.md
# Index: 1
# Runnable: True
# Hash: f5ced5b2

from src.controllers.smc.core.gain_validation import validate_hurwitz_criterion

# Test gains
gains = [10.0, 8.0, 15.0, 12.0, 50.0, 0.01]  # c1, c2, λ1, λ2, K, ε

is_hurwitz = validate_hurwitz_criterion(gains)

if is_hurwitz:
    print("Gains satisfy Hurwitz criterion (stable sliding surface)")
else:
    print("Warning: Gains violate Hurwitz criterion")