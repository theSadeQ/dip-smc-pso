# Example from: docs\fault_detection_guide.md
# Index: 3
# Runnable: False
# Hash: 9e183bed

# example-metadata:
# runnable: false

if status == "FAULT":
    # Log fault information
    logging.critical(f"FAULT at t={t:.3f}s: residual={residual_norm:.3f}")

    # Safety responses (choose appropriate action)

    # Option 1: Emergency stop
    u = 0.0

    # Option 2: Switch to safe controller
    controller = safe_mode_controller

    # Option 3: Graceful shutdown
    target_state = safe_equilibrium

    # Option 4: Reduce performance
    controller.reduce_gains(factor=0.5)