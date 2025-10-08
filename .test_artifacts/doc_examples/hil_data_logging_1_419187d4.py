# Example from: docs\reference\interfaces\hil_data_logging.md
# Index: 1
# Runnable: True
# Hash: 419187d4

from src.interfaces.hil.data_logging import DataLogger

# Create logger
logger = DataLogger(
    output_path="hil_data.csv",
    format="csv",
    sample_rate=100.0  # 100 Hz
)

# Simulation with logging
for t in np.arange(0, 10, 0.01):
    state = plant.get_state()
    control = controller.compute(state)

    # Log data
    logger.log(time=t, state=state, control=control)

# Close logger
logger.close()
print("Data saved to hil_data.csv")