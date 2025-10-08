# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 10
# Runnable: True
# Hash: ba83c043

# tests/conftest.py
import random
import numpy as np

@pytest.fixture(autouse=True)
def reset_random_seeds():
    """Reset random seeds before each test for reproducibility."""
    seed = 42
    random.seed(seed)
    np.random.seed(seed)
    yield
    # Cleanup: restore to random state
    random.seed(None)
    np.random.seed(None)