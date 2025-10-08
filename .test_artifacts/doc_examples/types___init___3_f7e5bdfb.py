# Example from: docs\reference\utils\types___init__.md
# Index: 3
# Runnable: True
# Hash: f7e5bdfb

from src.utils.types import STAOutput

# Create immutable output
sta_output = STAOutput(u, state_vars, history)

# Attempt modification (will fail - NamedTuple is frozen)
try:
    sta_output.u = np.array([20.0])  # AttributeError
except AttributeError:
    print("Immutability enforced - cannot modify output")

# Correct approach: Create new output
modified_output = STAOutput(
    u=np.array([20.0]),
    state_vars=sta_output.state_vars,
    history=sta_output.history
)