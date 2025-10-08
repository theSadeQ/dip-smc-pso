# Example from: docs\reports\CONTROLLER_OPTIMIZATION_REPORT.md
# Index: 4
# Runnable: True
# Hash: d3adb8a0

# Before: 6 gains (static + adaptive)
def gains(self) -> List[float]:
    static_gains = list(self.config.gains)
    current_adaptive_gain = self._adaptation.get_current_gain()
    return static_gains + [current_adaptive_gain]  # 6 gains

# After: 5 gains (static only)
def gains(self) -> List[float]:
    return list(self.config.gains)  # 5 gains as expected