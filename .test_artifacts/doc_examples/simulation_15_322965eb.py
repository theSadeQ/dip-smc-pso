# Example from: docs\guides\api\simulation.md
# Index: 15
# Runnable: True
# Hash: 322965eb

# Track saturation events
if context.is_saturated(control, max_force=100.0):
    context.log_saturation_event(time=t, control=control)

# Get saturation statistics
stats = context.get_saturation_stats()
print(f"Saturated {stats['count']} times ({stats['percentage']:.1f}%)")