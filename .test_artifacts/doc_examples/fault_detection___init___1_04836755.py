# Example from: docs\reference\analysis\fault_detection___init__.md
# Index: 1
# Runnable: False
# Hash: 04836755

class FDISystem:
    def generate_residual(y, u) -> r
    def adapt_threshold(r) -> tau
    def detect_fault(r, tau) -> bool
    def isolate_fault(r, signatures) -> fault_id