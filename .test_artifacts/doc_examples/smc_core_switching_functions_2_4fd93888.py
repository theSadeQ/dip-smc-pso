# Example from: docs\reference\controllers\smc_core_switching_functions.md
# Index: 2
# Runnable: True
# Hash: 4fd93888

import matplotlib.pyplot as plt

# Time series
t = np.linspace(0, 5, 5000)
s_trajectory = 0.02 * np.sin(10 * t) + 0.005 * np.random.randn(len(t))

# Different switching methods
u_sign = np.sign(s_trajectory)
u_sat = np.clip(s_trajectory / epsilon, -1, 1)
u_tanh = np.tanh(beta * s_trajectory / epsilon)

# Compute chattering index (control derivative)
chat_sign = np.sum(np.abs(np.diff(u_sign)))
chat_sat = np.sum(np.abs(np.diff(u_sat)))
chat_tanh = np.sum(np.abs(np.diff(u_tanh)))

print(f"Chattering index (sign):  {chat_sign:.1f}")
print(f"Chattering index (sat):   {chat_sat:.1f}")
print(f"Chattering index (tanh):  {chat_tanh:.1f}")  # Lowest