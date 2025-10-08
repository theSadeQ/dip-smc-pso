# Example from: docs\optimization_simulation\guide.md
# Index: 21
# Runnable: True
# Hash: 9ca48211

from src.simulation.engines.vector_sim import simulate_system_batch
from src.controllers import create_smc_for_pso, SMCType
import numpy as np
import matplotlib.pyplot as plt

# Define controller variants
controller_configs = [
    {"type": SMCType.CLASSICAL, "gains": [10.0, 8.0, 15.0, 12.0, 50.0, 5.0]},
    {"type": SMCType.CLASSICAL, "gains": [20.0, 15.0, 25.0, 20.0, 80.0, 10.0]},
    {"type": SMCType.CLASSICAL, "gains": [5.0, 4.0, 10.0, 8.0, 30.0, 2.0]},
]

# Create factory for each configuration
def make_factory(cfg):
    def factory(gains):
        return create_smc_for_pso(cfg["type"], gains, max_force=100.0)
    return factory

# Prepare particles array
particles = np.array([cfg["gains"] for cfg in controller_configs])

# Batch simulate
factory = make_factory(controller_configs[0])
t, x_batch, u_batch, sigma_batch = simulate_system_batch(
    controller_factory=factory,
    particles=particles,
    sim_time=5.0,
    dt=0.01,
    u_max=100.0
)

# Compute metrics for each controller
for i, cfg in enumerate(controller_configs):
    ise = np.sum(x_batch[i, :-1, :3]**2 * 0.01, axis=1).sum()
    u_rms = np.sqrt(np.mean(u_batch[i]**2))
    settling_time = np.argmax(np.all(np.abs(x_batch[i, :, :3]) < 0.01, axis=1)) * 0.01

    print(f"Controller {i+1}:")
    print(f"  ISE: {ise:.4f}")
    print(f"  RMS Control: {u_rms:.2f} N")
    print(f"  Settling Time: {settling_time:.2f} s")
    print()

# Plot comparison
fig, axes = plt.subplots(3, 1, figsize=(10, 8))
for i in range(len(controller_configs)):
    axes[0].plot(t, x_batch[i, :, 1], label=f"Controller {i+1}")
    axes[1].plot(t, x_batch[i, :, 2])
    axes[2].plot(t[:-1], u_batch[i])

axes[0].set_ylabel("θ₁ (rad)")
axes[1].set_ylabel("θ₂ (rad)")
axes[2].set_ylabel("Force (N)")
axes[2].set_xlabel("Time (s)")
axes[0].legend()
axes[0].grid(True)
axes[1].grid(True)
axes[2].grid(True)
plt.tight_layout()
plt.savefig("controller_comparison.png", dpi=150)