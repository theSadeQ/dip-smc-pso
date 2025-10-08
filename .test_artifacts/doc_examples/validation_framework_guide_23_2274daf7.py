# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 23
# Runnable: True
# Hash: 2274daf7

# Validate in order of increasing specificity
gamma = require_finite(value, "adaptation_rate")        # 1. Finite
gamma = require_positive(gamma, "adaptation_rate")      # 2. Positive
gamma = require_in_range(gamma, "adaptation_rate",      # 3. Bounded
                        minimum=0.01, maximum=10.0)
# 4. Check stability implications (if needed)
if gamma > 1.0:
    logging.warning("Large adaptation rate may cause instability")