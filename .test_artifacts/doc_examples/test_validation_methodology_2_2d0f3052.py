# Example from: docs\mathematical_foundations\test_validation_methodology.md
# Index: 2
# Runnable: True
# Hash: 2d0f3052

def test_sliding_surface_homogeneity():
       """Test that sliding surface is homogeneous of degree 1."""
       surface = LinearSlidingSurface(gains=[5, 3, 4, 2])

       state = np.array([0.1, 0.1, 0.1, 0.05, 0.05, 0.05])
       alpha = 2.5

       s_original = surface.compute(state)
       s_scaled = surface.compute(alpha * state)

       # Homogeneity: s(α·x) = α·s(x)
       assert abs(s_scaled - alpha * s_original) < 1e-10