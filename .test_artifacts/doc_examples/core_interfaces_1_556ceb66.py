# Example from: docs\reference\analysis\core_interfaces.md
# Index: 1
# Runnable: False
# Hash: 556ceb66

class Analyzer(Protocol):
    def analyze(self, data: Data) -> Result:
        ...