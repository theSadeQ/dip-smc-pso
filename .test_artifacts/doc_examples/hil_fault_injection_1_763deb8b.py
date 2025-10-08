# Example from: docs\reference\interfaces\hil_fault_injection.md
# Index: 1
# Runnable: True
# Hash: 763deb8b

from src.interfaces.hil.fault_injection import FaultInjector, FaultType

# Create fault injector
injector = FaultInjector()

# Add sensor bias fault
injector.add_fault(
    fault_type=FaultType.SENSOR_BIAS,
    target="theta1",  # First pendulum angle
    bias=0.1,  # 0.1 radian bias
    start_time=2.0,  # Start at 2 seconds
    duration=3.0  # Last for 3 seconds
)

# Apply fault during simulation
for t in np.arange(0, 10, 0.01):
    state = plant.get_state()
    faulty_state = injector.apply(state, t)
    control = controller.compute(faulty_state)