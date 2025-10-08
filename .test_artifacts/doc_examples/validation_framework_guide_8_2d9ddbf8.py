# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 8
# Runnable: True
# Hash: 2d9ddbf8

from src.utils.validation.range_validators import require_probability

# Optimization parameters
mutation_rate = require_probability(0.1, "mutation_rate")     # ✅
crossover_prob = require_probability(0.8, "crossover_prob")   # ✅

# Statistical parameters
confidence_level = require_probability(0.95, "confidence")    # ✅

# Edge cases
min_prob = require_probability(0.0, "min_probability")        # ✅ (exactly 0)
max_prob = require_probability(1.0, "max_probability")        # ✅ (exactly 1)

# Invalid: outside [0, 1]
try:
    p = require_probability(1.5, "cognitive_parameter")
except ValueError as e:
    # Error: "cognitive_parameter must be in the interval [0.0, 1.0]; got 1.5"
    print(e)