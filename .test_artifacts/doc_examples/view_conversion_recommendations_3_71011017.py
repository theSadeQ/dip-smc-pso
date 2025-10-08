# Example from: docs\analysis\view_conversion_recommendations.md
# Index: 3
# Runnable: True
# Hash: 71011017

# CORRECT (already optimized)
if init.ndim == 1:
    # broadcast across batch
    init_b = np.broadcast_to(init, (B, init.shape[0])).copy()  # ✅ Required