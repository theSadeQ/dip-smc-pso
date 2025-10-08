# Example from: docs\reference\interfaces\hil_data_logging.md
# Index: 3
# Runnable: True
# Hash: fad946e4

from src.interfaces.hil.data_logging import EventLogger

# Event-based logger
logger = EventLogger(
    output_path="events.csv",
    threshold=0.1  # Log when state changes > 0.1
)

last_state = None

for t in np.arange(0, 10, 0.01):
    state = plant.get_state()

    # Check if significant change
    if last_state is not None:
        state_change = np.linalg.norm(state - last_state)
        if state_change > logger.threshold:
            logger.log(time=t, state=state)

    last_state = state

logger.close()
print(f"Logged {logger.event_count} events")