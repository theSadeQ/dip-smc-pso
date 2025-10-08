# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 20
# Runnable: True
# Hash: bee16724

# ✅ GOOD: Single validation for array
gains_array = np.array([require_positive(g, f"gain_{i}") for i, g in enumerate(gains)])

# ❌ BAD: Repeated validation in inner loops
for timestep in range(1000):
    for i, gain in enumerate(gains):
        validated = require_positive(gain, f"gain_{i}")  # Wasteful!