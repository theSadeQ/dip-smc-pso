# Example from: docs\reference\interfaces\hil_fault_injection.md
# Index: 4
# Runnable: True
# Hash: f33fb4d5

from src.interfaces.hil.fault_injection import FaultInjector

# Multiple faults
injector = FaultInjector()

# Sensor noise
injector.add_fault(
    fault_type=FaultType.SENSOR_NOISE,
    target="theta1",
    noise_std=0.05,
    start_time=0.0
)

# Actuator delay
injector.add_fault(
    fault_type=FaultType.ACTUATOR_DELAY,
    delay_time=0.05,  # 50 ms delay
    start_time=4.0
)

# Communication latency spike
injector.add_fault(
    fault_type=FaultType.LATENCY_SPIKE,
    spike_probability=0.1,
    spike_duration=0.1,
    start_time=2.0
)

# Run with all faults
for t in np.arange(0, 10, 0.01):
    state = plant.get_state()
    faulty_state = injector.apply_all(state, t)
    control = controller.compute(faulty_state)
    faulty_control = injector.apply_all(control, t)
    plant.step(faulty_control)