# Example from: docs\tools\claim_extraction_guide.md
# Index: 10
# Runnable: True
# Hash: 9467a49f

# In merge_claims.py
def assign_priority(claim):
    if claim["type"] in ["theorem", "lemma"]:
        if claim["confidence"] < 0.8:  # Changed from 0.7
            return "CRITICAL"