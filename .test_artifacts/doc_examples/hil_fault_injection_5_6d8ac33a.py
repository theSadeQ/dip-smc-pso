# Example from: docs\reference\interfaces\hil_fault_injection.md
# Index: 5
# Runnable: True
# Hash: 6d8ac33a

from src.interfaces.hil.fault_injection import FaultInjector
from src.analysis.fault_detection import FDISystem

# Create fault injector and detector
injector = FaultInjector()
fdi = FDISystem(threshold=0.15)

# Inject sensor bias
injector.add_fault(
    fault_type=FaultType.SENSOR_BIAS,
    target="theta2",
    bias=0.2,
    start_time=5.0
)

# Track detection performance
detection_time = None
false_positives = 0

for t in np.arange(0, 10, 0.01):
    state = plant.get_state()
    faulty_state = injector.apply(state, t)

    # Check fault detection
    fault_detected = fdi.check(faulty_state)

    if fault_detected and detection_time is None and t >= 5.0:
        detection_time = t
        print(f"Fault detected at t={t:.2f}s (actual fault at 5.0s)")

    if fault_detected and t < 5.0:
        false_positives += 1

# Report results
print(f"Detection delay: {detection_time - 5.0:.3f}s")
print(f"False positives: {false_positives}")