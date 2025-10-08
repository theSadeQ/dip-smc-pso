# Example from: docs\fault_detection_system_documentation.md
# Index: 10
# Runnable: False
# Hash: d4a6944d

# example-metadata:
# runnable: false

class HILFaultDetection:
    def __init__(self, plant_server_config):
        self.fdi = FDIsystem(
            # HIL-specific tuning for communication delays
            persistence_counter=8,  # Account for network latency
            adaptive=True,          # Handle varying HIL conditions
            cusum_enabled=False     # Disable for real-time constraints
        )
        self.plant_server = PlantServer(plant_server_config)

    def run_hil_fault_detection(self):
        while self.plant_server.is_running():
            # Receive measurement from hardware
            measurement = self.plant_server.receive_measurement()

            # Fault detection with timing validation
            start = time.perf_counter()
            status, residual = self.fdi.check(
                measurement.timestamp,
                measurement.state,
                self.last_control,
                measurement.dt,
                self.dynamics_model
            )
            detection_time = time.perf_counter() - start

            # Send fault status to controller
            fault_message = FaultStatusMessage(
                status=status,
                residual=residual,
                detection_latency=detection_time
            )
            self.plant_server.send_fault_status(fault_message)