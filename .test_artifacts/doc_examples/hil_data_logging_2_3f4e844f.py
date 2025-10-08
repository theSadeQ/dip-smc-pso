# Example from: docs\reference\interfaces\hil_data_logging.md
# Index: 2
# Runnable: True
# Hash: 3f4e844f

from src.interfaces.hil.data_logging import HDF5Logger

# HDF5 logger with compression
logger = HDF5Logger(
    output_path="hil_data.h5",
    compression="gzip",
    compression_opts=9  # Maximum compression
)

# Create datasets
logger.create_dataset("time", dtype=np.float64)
logger.create_dataset("state", shape=(6,), dtype=np.float64)
logger.create_dataset("control", dtype=np.float64)

# Log simulation data
for t in np.arange(0, 10, 0.01):
    state = plant.get_state()
    control = controller.compute(state)

    logger.append("time", t)
    logger.append("state", state)
    logger.append("control", control)

logger.close()