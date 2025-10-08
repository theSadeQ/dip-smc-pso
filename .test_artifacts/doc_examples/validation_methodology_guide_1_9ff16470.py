# Example from: docs\testing\validation_methodology_guide.md
# Index: 1
# Runnable: True
# Hash: 9ff16470

# tests/validation/test_sliding_surface_properties.py

import pytest
import numpy as np
from src.controllers.smc.core.sliding_surface import LinearSlidingSurface

class TestSlidingSurfaceLinearity:
    """Validate linearity property of sliding surfaces."""

    def test_linearity_property(self):
        """Test σ(x₁ + x₂) = σ(x₁) + σ(x₂) for linear surfaces."""
        gains = [5.0, 3.0, 4.0, 2.0]
        surface = LinearSlidingSurface(gains)

        # Generate test states
        x1 = np.array([0.1, 0.1, 0.1, 0.05, 0.05, 0.05])
        x2 = np.array([0.2, 0.2, 0.2, 0.1, 0.1, 0.1])

        # Compute sliding variables
        s1 = surface.compute(x1)
        s2 = surface.compute(x2)
        s_combined = surface.compute(x1 + x2)

        # Verify linearity: s(x1 + x2) = s(x1) + s(x2)
        assert abs(s_combined - (s1 + s2)) < 1e-10, (
            f"Linearity violated: s({x1}+{x2}) = {s_combined}, "
            f"but s({x1}) + s({x2}) = {s1 + s2}"
        )

    @pytest.mark.parametrize("k1,k2,lam1,lam2", [
        (5.0, 3.0, 4.0, 2.0),
        (10.0, 8.0, 15.0, 12.0),
        (1.0, 1.0, 1.0, 1.0),
    ])
    def test_linearity_various_gains(self, k1, k2, lam1, lam2):
        """Test linearity for various gain combinations."""
        gains = [k1, k2, lam1, lam2]
        surface = LinearSlidingSurface(gains)

        for _ in range(100):
            x1 = np.random.uniform(-1, 1, size=6)
            x2 = np.random.uniform(-1, 1, size=6)

            s1 = surface.compute(x1)
            s2 = surface.compute(x2)
            s_combined = surface.compute(x1 + x2)

            assert abs(s_combined - (s1 + s2)) < 1e-10