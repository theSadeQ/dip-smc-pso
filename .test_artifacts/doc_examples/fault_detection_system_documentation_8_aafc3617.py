# Example from: docs\fault_detection_system_documentation.md
# Index: 8
# Runnable: False
# Hash: aafc3617

class SafetyManager:
    def __init__(self):
        # Primary fault detector (sensitive)
        self.primary_fdi = FDIsystem(residual_threshold=0.03, persistence_counter=3)

        # Secondary fault detector (conservative)
        self.secondary_fdi = FDIsystem(residual_threshold=0.1, persistence_counter=10)

        # Tertiary detector with different algorithm
        self.tertiary_fdi = EnhancedFaultDetector(
            FaultDetectionConfig(enable_cusum=True, enable_statistical_tests=True)
        )

    def assess_system_health(self, data):
        results = {}

        # Multiple detection layers
        results['primary'] = self.primary_fdi.check(...)
        results['secondary'] = self.secondary_fdi.check(...)
        results['tertiary'] = self.tertiary_fdi.detect(data)

        # Consensus-based fault declaration
        fault_votes = sum(1 for r in results.values() if self.indicates_fault(r))

        if fault_votes >= 2:  # Majority voting
            return "FAULT", results
        else:
            return "OK", results