# Example from: docs\technical\controller_factory_integration.md
# Index: 15
# Runnable: False
# Hash: 36b14dc5

class FactoryError(Exception):
    """Base factory error."""
    pass

class ConfigurationError(FactoryError):
    """Configuration validation error."""
    pass

class ControllerTypeError(FactoryError):
    """Unknown controller type error."""
    pass

class GainValidationError(FactoryError):
    """Gain validation error."""
    pass