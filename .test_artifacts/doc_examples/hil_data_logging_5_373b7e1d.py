# Example from: docs\reference\interfaces\hil_data_logging.md
# Index: 5
# Runnable: True
# Hash: 373b7e1d

from src.interfaces.hil.data_logging import DataLogger, Replay

# Log data
logger = DataLogger("original.csv", format="csv")
for t in np.arange(0, 10, 0.01):
    state = plant.get_state()
    control = controller.compute(state)
    logger.log(time=t, state=state, control=control)
logger.close()

# Replay simulation
replay = Replay("original.csv")

for entry in replay:
    t = entry["time"]
    state = entry["state"]
    control = entry["control"]

    # Reconstruct dynamics
    reconstructed_state = plant.step(control)

    # Compare original vs reconstructed
    error = np.linalg.norm(state - reconstructed_state)
    if error > 0.01:
        print(f"Reconstruction error at t={t:.2f}: {error:.4f}")

print("Replay complete")