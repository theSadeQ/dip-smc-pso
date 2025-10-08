# Example from: docs\reference\utils\development___init__.md
# Index: 5
# Runnable: True
# Hash: 37758865

from src.utils.development import InteractiveTuner
from ipywidgets import interact, FloatSlider

# Create interactive tuner
tuner = InteractiveTuner()

# Define interactive controller tuning
@interact(
    k1=FloatSlider(min=1, max=50, step=1, value=10),
    k2=FloatSlider(min=1, max=50, step=1, value=8),
    k3=FloatSlider(min=1, max=50, step=1, value=15)
)
def tune_controller(k1, k2, k3):
    # Update controller gains
    controller.set_gains([k1, k2, k3, 12.0, 50.0, 5.0])

    # Run simulation
    result = run_simulation(controller)

    # Display performance
    tuner.display_performance(result)

    return result

# Interactive tuning in Jupyter
# Sliders appear, live updates as you adjust