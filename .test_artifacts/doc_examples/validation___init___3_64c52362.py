# Example from: docs\reference\utils\validation___init__.md
# Index: 3
# Runnable: True
# Hash: 64c52362

from src.utils.validation import require_probability

def set_confidence_level(alpha: float):
    # Validate probability constraint
    validated_alpha = require_probability(
        alpha, name="confidence_level"
    )
    return validated_alpha

# Valid probability
alpha = set_confidence_level(0.95)  # ✓ Returns 0.95

# Invalid probability
try:
    alpha = set_confidence_level(1.5)  # ValueError: not in [0,1]
except ValueError as e:
    print(f"Invalid confidence: {e}")