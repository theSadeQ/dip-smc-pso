# Example from: docs\testing\guides\coverage_quality_gates_troubleshooting.md
# Index: 4
# Runnable: True
# Hash: 41479554

def test_sliding_surface_near_zero():
       state = np.array([1e-13, 1e-13, 0, 0, 0, 0])  # Near-zero state
       surface = controller.compute_sliding_surface(state, target)
       assert abs(surface) < 1e-10