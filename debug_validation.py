#!/usr/bin/env python3

from src.controllers.factory.core.validation import validate_configuration

class MockConfig:
    """Mock configuration for testing."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Test the case that's failing
config = MockConfig(
    gains=[10.0, 8.0, 5.0, 4.0, 20.0, 2.0],
    dt=0.2  # Large timestep
)

result = validate_configuration(config, 'classical_smc')
print(f"Valid: {result.valid}")
print(f"Errors: {result.errors}")
print(f"Warnings: {result.warnings}")
print(f"Info: {result.info}")