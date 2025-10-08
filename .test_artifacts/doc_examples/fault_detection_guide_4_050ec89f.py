# Example from: docs\fault_detection_guide.md
# Index: 4
# Runnable: False
# Hash: 050ec89f

# example-metadata:
# runnable: false

# Fault-tolerant control example
class FaultTolerantController:
    def __init__(self, primary_controller, backup_controller, fdi_system):
        self.primary = primary_controller
        self.backup = backup_controller
        self.fdi = fdi_system
        self.active_controller = primary_controller

    def compute_control(self, x, x_ref, t, u_prev, dt, dynamics):
        # FDI check
        status, residual = self.fdi.check(t, x, u_prev, dt, dynamics)

        # Switch controllers if fault detected
        if status == "FAULT" and self.active_controller == self.primary:
            logging.warning("Switching to backup controller due to fault")
            self.active_controller = self.backup

        return self.active_controller.compute_control(x, x_ref, t)