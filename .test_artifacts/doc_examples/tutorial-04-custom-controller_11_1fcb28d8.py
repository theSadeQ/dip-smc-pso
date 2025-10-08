# Example from: docs\guides\tutorials\tutorial-04-custom-controller.md
# Index: 11
# Runnable: False
# Hash: 1fcb28d8

# example-metadata:
# runnable: false

import logging
logger = logging.getLogger(__name__)

def compute_control(self, state, ...):
    s = self.compute_sliding_surface(state)
    logger.debug(f"Sliding surface: s={s:.4f}")

    control = ...
    logger.debug(f"Control output: u={control:.4f}")

    return control, state_vars, history