# Example from: docs\CLAUDE.md
# Index: 15
# Runnable: False
# Hash: 0fbfb9a1

# example-metadata:
# runnable: false

# Automatic cleanup when controller goes out of scope
def run_simulation():
    controller = ClassicalSMC(...)
    return simulate(controller, duration=5.0)
# Controller automatically cleaned up via __del__