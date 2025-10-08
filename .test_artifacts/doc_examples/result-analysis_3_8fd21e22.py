# Example from: docs\guides\how-to\result-analysis.md
# Index: 3
# Runnable: True
# Hash: 8fd21e22

def compute_itae(time, state):
    """Compute ITAE from state trajectory."""
    dt = time[1] - time[0]
    error_norm = np.linalg.norm(state, axis=1)
    itae = np.sum(time * np.abs(error_norm)) * dt
    return itae

itae_manual = compute_itae(time, state)
print(f"ITAE (manual): {itae_manual:.4f}")