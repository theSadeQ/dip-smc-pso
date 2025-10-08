# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 19
# Runnable: False
# Hash: e8a14187

# ✅ GOOD: Validate once at construction
class Controller:
    def __init__(self, gains):
        self.gains = [require_positive(g, f"gain_{i}") for i, g in enumerate(gains)]

    def compute_control(self, state):
        # Use validated self.gains - no repeated validation
        return self.gains @ state

# ❌ BAD: Repeated validation in hot loop
class Controller:
    def compute_control(self, state, gains):
        # Validation on every control step - wasteful!
        validated_gains = [require_positive(g, f"gain_{i}") for i, g in enumerate(gains)]
        return validated_gains @ state