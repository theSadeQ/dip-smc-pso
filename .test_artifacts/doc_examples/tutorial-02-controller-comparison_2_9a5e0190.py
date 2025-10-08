# Example from: docs\guides\tutorials\tutorial-02-controller-comparison.md
# Index: 2
# Runnable: True
# Hash: 9a5e0190

def compute_chattering_index(u, dt):
    """Chattering index = average absolute derivative of control signal."""
    du_dt = np.diff(u) / dt
    return np.mean(np.abs(du_dt))

# Compare chattering across controllers
for name, data in results.items():
    u = np.array(data['control'])
    chattering = compute_chattering_index(u, dt=0.01)
    print(f"{name:15s} chattering index: {chattering:.2f} N/s")