# Example from: docs\reference\analysis\validation_metrics.md
# Index: 8
# Runnable: True
# Hash: 61ebc07c

import numpy as np

def compute_chattering_index(u, dt):
    """Quantify control chattering."""
    # Total variation of control signal
    tv = np.sum(np.abs(np.diff(u))) * dt
    return tv

chattering = compute_chattering_index(result.control, dt=0.01)
print(f"Chattering Index: {chattering:.4f}")

# Compare chattering across controllers
controllers = {
    'Classical': create_smc_for_pso(SMCType.CLASSICAL, [10, 8, 15, 12, 50, 5]),
    'STA': create_smc_for_pso(SMCType.SUPER_TWISTING, [25, 10, 15, 12, 20, 15]),
}

chattering_results = {}
for name, ctrl in controllers.items():
    result = run_simulation(ctrl, dynamics, [0.1, 0.05, 0, 0, 0, 0], 10.0, 0.01)
    chattering_results[name] = compute_chattering_index(result.control, 0.01)

for name, ci in chattering_results.items():
    print(f"{name} Chattering: {ci:.4f}")