# Example from: docs\reference\utils\development___init__.md
# Index: 3
# Runnable: True
# Hash: ecdffa52

from src.utils.development import RichDisplay
from IPython.display import display, Markdown

# Create rich display helper
rich = RichDisplay()

# Display simulation results
def show_results(results):
    # Text summary
    display(Markdown("## Simulation Results"))

    # Data table
    rich.display_table(results.metrics)

    # Interactive plot
    rich.display_plot(results.t, results.x)

    # Animation preview
    rich.display_animation(results, frames=100)

show_results(simulation_results)