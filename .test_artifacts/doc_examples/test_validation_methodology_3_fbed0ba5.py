# Example from: docs\mathematical_foundations\test_validation_methodology.md
# Index: 3
# Runnable: False
# Hash: fbed0ba5

# example-metadata:
# runnable: false

   def test_sliding_surface_gain_sensitivity():
       """Test that surface responds correctly to gain changes."""
       gains1 = [5, 3, 4, 2]
       gains2 = [10, 6, 8, 4]  # Doubled gains

       surface1 = LinearSlidingSurface(gains1)
       surface2 = LinearSlidingSurface(gains2)

       state = np.array([0.1, 0.1, 0.1, 0.05, 0.05, 0.05])

       s1 = surface1.compute(state)
       s2 = surface2.compute(state)

       # Surface value should double with doubled gains
       assert abs(s2 - 2 * s1) < 1e-10