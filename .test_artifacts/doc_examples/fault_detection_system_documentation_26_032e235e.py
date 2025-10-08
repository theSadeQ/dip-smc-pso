# Example from: docs\fault_detection_system_documentation.md
# Index: 26
# Runnable: False
# Hash: 032e235e

# example-metadata:
# runnable: false

def tune_persistence_counter(fault_scenarios, detection_delay_target=20):
    """Tune persistence counter based on detection delay requirements."""

    optimal_persistence = {}

    for fault_type, magnitude in fault_scenarios.items():
        delays = []

        for persistence in range(1, 21):  # Test 1-20
            fdi = FDIsystem(persistence_counter=persistence)
            delay = simulate_fault_detection(fdi, fault_type, magnitude)
            delays.append(delay)

            if delay <= detection_delay_target:
                optimal_persistence[fault_type] = persistence
                break

    return optimal_persistence