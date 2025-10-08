# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 6
# Runnable: True
# Hash: 46143e4d

# tests/conftest.py
from hypothesis import settings, Verbosity

# CI profile: fast, deterministic
settings.register_profile("ci", max_examples=50, deadline=500, verbosity=Verbosity.verbose)

# Development profile: moderate testing
settings.register_profile("dev", max_examples=100, deadline=1000)

# Thorough profile: comprehensive property testing
settings.register_profile("thorough", max_examples=1000, deadline=5000)

# Load profile from environment or default to CI
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "ci"))