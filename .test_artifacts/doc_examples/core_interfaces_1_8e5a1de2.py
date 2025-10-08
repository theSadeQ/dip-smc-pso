# Example from: docs\reference\analysis\core_interfaces.md
# Index: 1
# Runnable: False
# Hash: 8e5a1de2

# example-metadata:
# runnable: false

class Analyzer(Protocol):
    def analyze(self, data: Data) -> Result:
        ...