# Example from: docs\memory_management_patterns.md
# Index: 13
# Runnable: True
# Hash: a2b10fcf

# Problem: History dict grows unbounded
history = controller.initialize_history()
for i in range(100000):
    control = controller.compute_control(state, state_vars, history)
    # history dict now contains 100000 entries

# Solution: Clear history periodically
if i % 1000 == 999:
    history = controller.initialize_history()