# Example from: docs\guides\how-to\result-analysis.md
# Index: 2
# Runnable: True
# Hash: 30d07160

# Manual ISE calculation
def compute_ise(time, state):
    """Compute ISE from state trajectory."""
    dt = time[1] - time[0]  # Assume uniform sampling
    error_norm = np.linalg.norm(state, axis=1)
    ise = np.sum(error_norm**2) * dt
    return ise

ise_manual = compute_ise(time, state)
print(f"ISE (manual): {ise_manual:.4f}")