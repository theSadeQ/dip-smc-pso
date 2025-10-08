# Example from: docs\reference\interfaces\hil_enhanced_hil.md
# Index: 5
# Runnable: True
# Hash: b5716ca4

from src.interfaces.hil.enhanced_hil import PerformanceProfiler

# Performance profiler
profiler = PerformanceProfiler()

# Profile simulation
profiler.start()

for t in np.arange(0, 10, 0.01):
    with profiler.section("dynamics"):
        state = plant.get_state()

    with profiler.section("control"):
        control = controller.compute(state)

    with profiler.section("communication"):
        client.send_control(control)

profiler.stop()

# Report profiling results
report = profiler.generate_report()
print(report.to_string())

# Identify bottlenecks
for section, time in report.sorted_sections():
    print(f"{section}: {time:.2f} ms ({report.percentage(section):.1f}%)")