# Example from: docs\reference\utils\visualization___init__.md
# Index: 4
# Runnable: True
# Hash: 19e193e3

from src.utils.visualization import ProjectMovieGenerator, MovieScene

# Create movie generator
generator = ProjectMovieGenerator(
    title="DIP SMC PSO Project",
    output_path="project_overview.mp4",
    fps=30,
    resolution=(1920, 1080)
)

# Define scenes
scenes = [
    MovieScene('intro', duration=5.0, content="Title and overview"),
    MovieScene('simulation', duration=10.0, content=simulation_results),
    MovieScene('comparison', duration=8.0, content=comparison_data),
    MovieScene('conclusion', duration=3.0, content="Summary")
]

# Generate complete movie
generator.create_movie(scenes)