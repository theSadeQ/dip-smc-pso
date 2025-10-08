# Example from: docs\fault_detection_system_documentation.md
# Index: 22
# Runnable: False
# Hash: 24412f7c

def diagnose_missed_faults(fault_injection_results):
    """Analyze fault detection performance."""

    for fault_type, results in fault_injection_results.items():
        detection_rate = results['detected'] / results['total_injected']
        avg_delay = np.mean(results['detection_delays'])

        print(f"Fault type: {fault_type}")
        print(f"Detection rate: {detection_rate:.2%}")
        print(f"Average delay: {avg_delay:.1f} timesteps")

        if detection_rate < 0.95:  # < 95% detection rate
            print("LOW DETECTION RATE WARNING")
            if avg_delay > 50:
                print("RECOMMENDATION: Decrease threshold or persistence counter")
            else:
                print("RECOMMENDATION: Review fault signature and weights")