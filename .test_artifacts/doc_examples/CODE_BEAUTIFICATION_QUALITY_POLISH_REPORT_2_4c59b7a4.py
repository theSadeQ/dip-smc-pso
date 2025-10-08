# Example from: docs\reports\CODE_BEAUTIFICATION_QUALITY_POLISH_REPORT.md
# Index: 2
# Runnable: True
# Hash: 4c59b7a4

# Before: Hard dependencies
def create_controller():
    config = load_config()  # Fixed dependency

# After: Injectable dependencies
def create_controller(config: Optional[Dict] = None):
    config = config or load_config()  # Testable