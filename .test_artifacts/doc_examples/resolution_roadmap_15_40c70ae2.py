# Example from: docs\testing\reports\2025-09-30\technical\resolution_roadmap.md
# Index: 15
# Runnable: True
# Hash: 40c70ae2

# Before (problematic):
def test_controller_performance():
    performance = evaluate_controller(controller)
    return performance > threshold  # WRONG: pytest ignores returns

# After (correct):
def test_controller_performance():
    performance = evaluate_controller(controller)
    assert performance > threshold, f"Performance {performance} below threshold {threshold}"