# Example from: docs\reference\utils\types___init__.md
# Index: 2
# Runnable: True
# Hash: 682b7493

from src.utils.types import ClassicalSMCOutput, AdaptiveSMCOutput
import numpy as np

def validate_output(output):
    # Runtime type checking
    if isinstance(output, ClassicalSMCOutput):
        print("Classical SMC output detected")
        assert hasattr(output, 'u')
        assert hasattr(output, 'state_vars')
        assert hasattr(output, 'history')
    elif isinstance(output, AdaptiveSMCOutput):
        print("Adaptive SMC output detected")
        assert hasattr(output, 'adaptive_gains')
    else:
        raise TypeError(f"Unknown output type: {type(output)}")

# Validate outputs
classical_output = ClassicalSMCOutput(u, state_vars, history)
validate_output(classical_output)  # ✓ Pass