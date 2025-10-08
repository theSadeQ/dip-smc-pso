# Example from: docs\tools\regex_pattern_reference.md
# Index: 5
# Runnable: False
# Hash: 5c463161

# example-metadata:
# runnable: false

class FormalClaimExtractor:
    def __init__(self):
        # Compile once in constructor
        self.PATTERNS = {
            'theorem': re.compile(r'\*\*Theorem.*', re.DOTALL),
            'proof': re.compile(r'\*\*Proof.*', re.DOTALL),
        }

    def extract(self, file_content):
        # Reuse compiled patterns
        matches = self.PATTERNS['theorem'].finditer(file_content)