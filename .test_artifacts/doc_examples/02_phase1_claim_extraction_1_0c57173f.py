# Example from: docs\plans\citation_system\02_phase1_claim_extraction.md
# Index: 1
# Runnable: False
# Hash: 0c57173f

class MonolithicExtractor:  # ❌ Don't do this
    def extract_all(self, files):
        # 2000+ lines mixing docs + code + math
        # Result: Unmaintainable, low precision