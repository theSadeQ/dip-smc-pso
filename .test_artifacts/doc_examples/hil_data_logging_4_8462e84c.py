# Example from: docs\reference\interfaces\hil_data_logging.md
# Index: 4
# Runnable: True
# Hash: 8462e84c

from src.interfaces.hil.data_logging import MultiLogger

# Log to multiple formats simultaneously
logger = MultiLogger(
    outputs=[
        ("hil_data.csv", "csv"),
        ("hil_data.h5", "hdf5"),
        ("hil_data.parquet", "parquet")
    ]
)

for t in np.arange(0, 10, 0.01):
    state = plant.get_state()
    control = controller.compute(state)

    # Log to all formats
    logger.log_all(time=t, state=state, control=control)

logger.close_all()