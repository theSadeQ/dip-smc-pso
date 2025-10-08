# Example from: docs\reference\interfaces\hil_fault_injection.md
# Index: 2
# Runnable: True
# Hash: 55e800ad

from src.interfaces.hil.fault_injection import FaultInjector, FaultType

# Actuator fault
injector = FaultInjector()

injector.add_fault(
    fault_type=FaultType.ACTUATOR_SATURATION,
    target="control",
    saturation_min=-50.0,  # Reduced from -100
    saturation_max=50.0,   # Reduced from +100
    start_time=5.0
)

# Simulation with fault
for t in np.arange(0, 10, 0.01):
    state = plant.get_state()
    control = controller.compute(state)
    faulty_control = injector.apply(control, t)
    plant.step(faulty_control)