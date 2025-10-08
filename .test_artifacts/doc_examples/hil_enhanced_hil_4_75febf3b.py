# Example from: docs\reference\interfaces\hil_enhanced_hil.md
# Index: 4
# Runnable: True
# Hash: 75febf3b

from src.interfaces.hil.enhanced_hil import HardwareEmulator

# Hardware emulator
emulator = HardwareEmulator()

# Configure actuator model
emulator.set_actuator_model(
    bandwidth=50.0,  # 50 Hz bandwidth
    saturation=100.0,
    delay=0.01  # 10 ms delay
)

# Configure sensor model
emulator.set_sensor_model(
    noise_std=0.01,
    bias=0.005,
    dropout_rate=0.01
)

# Simulate with hardware emulation
for t in np.arange(0, 10, 0.01):
    state = plant.get_state()

    # Emulate sensor
    measured_state = emulator.sensor(state)

    # Compute control
    control = controller.compute(measured_state)

    # Emulate actuator
    actual_control = emulator.actuator(control)

    plant.step(actual_control)