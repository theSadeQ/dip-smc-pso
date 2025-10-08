# Example from: docs\PATTERNS.md
# Index: 20
# Runnable: True
# Hash: 7e3f6b89

# src/utils/reproducibility/seeding.py

def set_global_seed(seed: int) -> None:
    """Set seeds for all random number generators."""
    import random
    import numpy as np

    random.seed(seed)
    np.random.seed(seed)

    # Set environment variables for determinism
    import os
    os.environ['PYTHONHASHSEED'] = str(seed)

    # Numba RNG seeding (if applicable)
    try:
        import numba
        numba.core.config.RANDOM_SEED = seed
    except ImportError:
        pass

# Usage in all experiments
set_global_seed(42)  # Ensures reproducible results