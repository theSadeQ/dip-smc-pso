# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 22
# Runnable: True
# Hash: 705a4b53

import matplotlib.pyplot as plt

# Extract energy ratio from history
energy_ratios = [h.get("E_ratio", 0) for h in history_list]
modes = [h.get("mode", "swing") for h in history_list]

# Plot energy evolution
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t_array, energy_ratios)
plt.axhline(0.95, color='g', linestyle='--', label='Switch threshold')
plt.axhline(0.90, color='r', linestyle='--', label='Exit threshold')
plt.ylabel('Energy Ratio (E/E_bottom)')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
mode_numeric = [1 if m == "stabilize" else 0 for m in modes]
plt.plot(t_array, mode_numeric)
plt.ylabel('Mode (0=swing, 1=stabilize)')
plt.xlabel('Time (s)')
plt.grid(True)

plt.tight_layout()
plt.show()