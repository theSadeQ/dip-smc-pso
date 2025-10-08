# Example from: docs\fault_detection_system_documentation.md
# Index: 7
# Runnable: False
# Hash: ab39ae09

# example-metadata:
# runnable: false

class FaultTolerantController:
    def __init__(self, controller, dynamics_model):
        self.controller = controller
        self.fdi = FDIsystem(
            residual_threshold=0.05,  # Tuned for system noise level
            persistence_counter=5,    # Balance responsiveness vs. robustness
            adaptive=True,            # Handle varying operating conditions
            cusum_enabled=True        # Detect slow drifts
        )
        self.dynamics_model = dynamics_model
        self.fault_detected = False

    def compute_control(self, t, state, reference):
        # Fault detection
        if not self.fault_detected:
            status, residual = self.fdi.check(t, state, self.last_control, dt, self.dynamics_model)
            if status == "FAULT":
                self.fault_detected = True
                logging.critical(f"Fault detected at t={t:.3f}s")
                return self.safe_shutdown_sequence()

        # Normal control computation
        if not self.fault_detected:
            control = self.controller.compute_control(state, reference)
            self.last_control = control
            return control
        else:
            return self.fault_accommodation_control(state, reference)