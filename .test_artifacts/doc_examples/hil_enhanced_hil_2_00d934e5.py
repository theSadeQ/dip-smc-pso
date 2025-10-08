# Example from: docs\reference\interfaces\hil_enhanced_hil.md
# Index: 2
# Runnable: True
# Hash: 00d934e5

from src.interfaces.hil.enhanced_hil import DisturbanceInjector

# Create disturbance injector
injector = DisturbanceInjector()

# Add sinusoidal disturbance
injector.add_disturbance(
    type="sinusoidal",
    amplitude=5.0,
    frequency=1.0,
    start_time=2.0
)

# Simulate with disturbance
for t in np.arange(0, 10, 0.01):
    state = plant.get_state()
    control = controller.compute(state)

    # Add disturbance
    disturbed_control = injector.apply(control, t)

    plant.step(disturbed_control)