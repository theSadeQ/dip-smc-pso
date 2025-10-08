# Example from: docs\CLAUDE.md
# Index: 18
# Runnable: False
# Hash: e5747190

# example-metadata:
# runnable: false

controller = HybridAdaptiveSTASMC(gains=[...], dt=0.01, max_force=100, ...)
history = controller.initialize_history()

while running:
    control, state_vars, history = controller.compute_control(state, state_vars, history)

    # Hourly cleanup
    if time.time() - last_cleanup > 3600:
        history = controller.initialize_history()
        gc.collect()