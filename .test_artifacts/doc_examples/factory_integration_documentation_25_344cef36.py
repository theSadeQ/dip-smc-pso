# Example from: docs\factory_integration_documentation.md
# Index: 25
# Runnable: True
# Hash: 344cef36

import numpy as np

   gains = [10.0, 8.0, 15.0, 12.0, 50.0, 5.0]

   # Check basic validity
   assert len(gains) == 6, f"Expected 6 gains, got {len(gains)}"
   assert all(isinstance(g, (int, float)) for g in gains), "All gains must be numbers"
   assert all(np.isfinite(g) for g in gains), "All gains must be finite"
   assert all(g > 0 for g in gains), "All gains must be positive"