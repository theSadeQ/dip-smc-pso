# Example from: docs\mathematical_foundations\test_validation_methodology.md
# Index: 1
# Runnable: False
# Hash: 295433ac

# example-metadata:
# runnable: false

   def test_sliding_surface_linearity():
       """Test that sliding surface is linear in state."""
       surface = LinearSlidingSurface(gains=[5, 3, 4, 2])

       state1 = np.array([0.1, 0.1, 0.1, 0.05, 0.05, 0.05])
       state2 = np.array([0.2, 0.2, 0.2, 0.1, 0.1, 0.1])

       s1 = surface.compute(state1)
       s2 = surface.compute(state2)
       s_combined = surface.compute(state1 + state2)

       # Linearity: s(x1 + x2) = s(x1) + s(x2)
       assert abs(s_combined - (s1 + s2)) < 1e-10